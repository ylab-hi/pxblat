#pragma GCC diagnostic ignored "-Wwrite-strings"
#include "gfServer.hpp"

#include <sstream>
#include <string>

#include "dbg.h"

namespace cppbinding {

bool boolean2bool(boolean b) { return b == TRUE; }
boolean bool2boolean(bool b) { return b ? TRUE : FALSE; }

/*
  Note about file(s) specified in the start command:
      The path(s) specified here are sent back exactly as-is
      to clients such as gfClient, hgBlat, webBlat.
      It is intended that relative paths are used.
      Absolute paths starting with '/' tend not to work
      unless the client is on the same machine as the server.
      For use with hgBlat and webBlat, cd to the directory where the file is
      and use the plain file name with no slashes.
        hgBlat will append the path(s) given to dbDb.nibPath.
       webBlat will append the path(s) given to path specified in webBlat.cfg.
      gfClient will append the path(s) given to the seqDir path specified.
*/

void setSocketTimeout(int sockfd, int delayInSeconds)
// put socket read and write timeout so it will not take forever to timeout
// during a read or write
{
  struct timeval tv;
  tv.tv_sec = delayInSeconds;
  tv.tv_usec = 0;
  setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char *)&tv, sizeof tv);
  setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, (const char *)&tv, sizeof tv);
}

// static boolean sendOk = TRUE;

void setSendOk(boolean &sendOk)
// Reset to OK to send
{
  sendOk = TRUE;
}

void errSendString(int sd, char *s, boolean &sendOk)
// Send string. If not OK, remember we had an error, do not try to write
// anything more on this connection.
{
  if (sendOk) sendOk = netSendString(sd, s);
}

void errSendLongString(int sd, char *s, boolean &sendOk)
// Send string unless we had an error already on the connection.
{
  if (sendOk) sendOk = netSendLongString(sd, s);
}

void logGenoFind(struct genoFind *gf)
/* debug log the genoFind parameters */
{
  logDebug("gf->isMapped: %d", gf->isMapped);
  logDebug("gf->maxPat: %d", gf->maxPat);
  logDebug("gf->minMatch: %d", gf->minMatch);
  logDebug("gf->maxGap: %d", gf->maxGap);
  logDebug("gf->tileSize: %d", gf->tileSize);
  logDebug("gf->stepSize: %d", gf->stepSize);
  logDebug("gf->tileSpaceSize: %d", gf->tileSpaceSize);
  logDebug("gf->tileMask: %dfrom . import server", gf->tileMask);
  logDebug("gf->sourceCount: %d", gf->sourceCount);
  logDebug("gf->isPep: %d", gf->isPep);
  logDebug("gf->allowOneMismatch: %d", gf->allowOneMismatch);
  logDebug("gf->noSimpRepMask: %d", gf->noSimpRepMask);
  logDebug("gf->segSize: %d", gf->segSize);
  logDebug("gf->totalSeqSize: %d", gf->totalSeqSize);
}

void logGenoFindIndex(struct genoFindIndex *gfIdx)
/* debug log the genoFind parameters in an genoFindIndex */
{
  logDebug("gfIdx->isTrans: %d", gfIdx->isTrans);
  logDebug("gfIdx->noSimpRepMask: %d", gfIdx->noSimpRepMask);
  if (gfIdx->untransGf != NULL)
    logGenoFind(gfIdx->untransGf);
  else
    logGenoFind(gfIdx->transGf[0][0]);
}

int getPortIx(char *portName)
/* Convert from ascii to integer. */
{
  if (!isdigit(portName[0])) errAbort("Expecting a port number got %s", portName);
  return atoi(portName);
}

/* Some variables to gather statistics on usage. */

// long baseCount = 0, blatCount = 0, aaCount = 0, pcrCount = 0;
// int warnCount = 0;
// int noSigCount = 0;
// int missCount = 0;
// int trimCount = 0;

void dnaQuery(struct genoFind *gf, struct dnaSeq *seq, int connectionHandle, struct hash *perSeqMaxHash,
              ServerOption const &options, UsageStats &stats, boolean &sendOk)
/* Handle a query for DNA/DNA match. */
{
  auto maxDnaHits = options.maxDnaHits;

  char buf[256];
  struct gfClump *clumpList = NULL, *clump;
  int limit = 1000;
  int clumpCount = 0, hitCount = -1;
  struct lm *lm = lmInit(0);

  if (seq->size > gf->tileSize + gf->stepSize + gf->stepSize) limit = maxDnaHits;
  clumpList = gfFindClumps(gf, seq, lm, &hitCount);
  if (clumpList == NULL) ++stats.missCount;
  for (clump = clumpList; clump != NULL; clump = clump->next) {
    struct gfSeqSource *ss = clump->target;
    sprintf(buf, "%d\t%d\t%s\t%d\t%d\t%d", clump->qStart, clump->qEnd, ss->fileName, clump->tStart - ss->start,
            clump->tEnd - ss->start, clump->hitCount);
    errSendString(connectionHandle, buf, sendOk);
    ++clumpCount;
    int perSeqCount = -1;
    if (perSeqMaxHash && ((perSeqCount = hashIntValDefault(perSeqMaxHash, ss->fileName, -1)) >= 0)) {
      if (perSeqCount >= (maxDnaHits / 2)) break;
      hashIncInt(perSeqMaxHash, ss->fileName);
    } else if (--limit < 0)
      break;
  }
  gfClumpFreeList(&clumpList);
  lmCleanup(&lm);
  logDebug("%lu %d clumps, %d hits", clock1000(), clumpCount, hitCount);

  dbg(clumpCount);
  dbg(hitCount);
}

void transQuery(struct genoFind *transGf[2][3], aaSeq *seq, int connectionHandle, ServerOption const &options,
                UsageStats &stats, boolean &sendOk)
/* Handle a query for protein/translated DNA match. */
{
  auto tileSize = options.tileSize;
  auto maxTransHits = options.maxTransHits;

  char buf[256];
  struct gfClump *clumps[3], *clump;
  int isRc, frame;
  char strand;
  struct dyString *dy = dyStringNew(1024);
  struct gfHit *hit;
  int clumpCount = 0, hitCount = 0, oneHit;
  struct lm *lm = lmInit(0);

  sprintf(buf, "tileSize %d", tileSize);
  errSendString(connectionHandle, buf, sendOk);
  for (frame = 0; frame < 3; ++frame) clumps[frame] = NULL;
  for (isRc = 0; isRc <= 1; ++isRc) {
    strand = (isRc ? '-' : '+');
    gfTransFindClumps(transGf[isRc], seq, clumps, lm, &oneHit);
    hitCount += oneHit;
    for (frame = 0; frame < 3; ++frame) {
      int limit = maxTransHits;
      for (clump = clumps[frame]; clump != NULL; clump = clump->next) {
        struct gfSeqSource *ss = clump->target;
        sprintf(buf, "%d\t%d\t%s\t%d\t%d\t%d\t%c\t%d", clump->qStart, clump->qEnd, ss->fileName,
                clump->tStart - ss->start, clump->tEnd - ss->start, clump->hitCount, strand, frame);
        errSendString(connectionHandle, buf, sendOk);
        dyStringClear(dy);
        for (hit = clump->hitList; hit != NULL; hit = hit->next)
          dyStringPrintf(dy, " %d %d", hit->qStart, hit->tStart - ss->start);
        errSendLongString(connectionHandle, dy->string, sendOk);
        ++clumpCount;
        if (--limit < 0) break;
      }
      gfClumpFreeList(&clumps[frame]);
    }
  }
  if (clumpCount == 0) ++stats.missCount;
  dyStringFree(&dy);
  lmCleanup(&lm);
  logDebug("%lu %d clumps, %d hits", clock1000(), clumpCount, hitCount);
}

void transTransQuery(struct genoFind *transGf[2][3], struct dnaSeq *seq, int connectionHandle,
                     ServerOption const &options, UsageStats &stats, boolean &sendOk)
/* Handle a query for protein/translated DNA match. */
{
  auto tileSize = options.tileSize;
  auto maxTransHits = options.maxTransHits;

  char buf[256];
  struct gfClump *clumps[3][3], *clump;
  int isRc, qFrame, tFrame;
  char strand;
  struct trans3 *t3 = trans3New(seq);
  struct dyString *dy = dyStringNew(1024);
  struct gfHit *hit;
  int clumpCount = 0, hitCount = 0, oneCount;

  sprintf(buf, "tileSize %d", tileSize);
  errSendString(connectionHandle, buf, sendOk);
  for (qFrame = 0; qFrame < 3; ++qFrame)
    for (tFrame = 0; tFrame < 3; ++tFrame) clumps[qFrame][tFrame] = NULL;
  for (isRc = 0; isRc <= 1; ++isRc) {
    struct lm *lm = lmInit(0);
    strand = (isRc ? '-' : '+');
    gfTransTransFindClumps(transGf[isRc], t3->trans, clumps, lm, &oneCount);
    hitCount += oneCount;
    for (qFrame = 0; qFrame < 3; ++qFrame) {
      for (tFrame = 0; tFrame < 3; ++tFrame) {
        int limit = maxTransHits;
        for (clump = clumps[qFrame][tFrame]; clump != NULL; clump = clump->next) {
          struct gfSeqSource *ss = clump->target;
          sprintf(buf, "%d\t%d\t%s\t%d\t%d\t%d\t%c\t%d\t%d", clump->qStart, clump->qEnd, ss->fileName,
                  clump->tStart - ss->start, clump->tEnd - ss->start, clump->hitCount, strand, qFrame, tFrame);
          errSendString(connectionHandle, buf, sendOk);
          dyStringClear(dy);
          for (hit = clump->hitList; hit != NULL; hit = hit->next) {
            dyStringPrintf(dy, " %d %d", hit->qStart, hit->tStart - ss->start);
          }
          errSendLongString(connectionHandle, dy->string, sendOk);
          ++clumpCount;
          if (--limit < 0) break;
        }
        gfClumpFreeList(&clumps[qFrame][tFrame]);
      }
    }
    lmCleanup(&lm);
  }
  trans3Free(&t3);
  if (clumpCount == 0) ++stats.missCount;
  logDebug("%lu %d clumps, %d hits", clock1000(), clumpCount, hitCount);
}

void pcrQuery(struct genoFind *gf, char *fPrimer, char *rPrimer, int maxDistance, int connectionHandle, boolean &sendOk)
/* Do PCR query and report results down socket. */
{
  int fPrimerSize = strlen(fPrimer);
  int rPrimerSize = strlen(rPrimer);
  struct gfClump *clumpList, *clump;
  int clumpCount = 0;
  char buf[256];

  clumpList = gfPcrClumps(gf, fPrimer, fPrimerSize, rPrimer, rPrimerSize, 0, maxDistance);
  for (clump = clumpList; clump != NULL; clump = clump->next) {
    struct gfSeqSource *ss = clump->target;
    safef(buf, sizeof(buf), "%s\t%d\t%d\t+", ss->fileName, clump->tStart, clump->tEnd);
    errSendString(connectionHandle, buf, sendOk);
    ++clumpCount;
  }
  gfClumpFreeList(&clumpList);

  clumpList = gfPcrClumps(gf, rPrimer, rPrimerSize, fPrimer, fPrimerSize, 0, maxDistance);

  for (clump = clumpList; clump != NULL; clump = clump->next) {
    struct gfSeqSource *ss = clump->target;
    safef(buf, sizeof(buf), "%s\t%d\t%d\t-", ss->fileName, clump->tStart, clump->tEnd);
    errSendString(connectionHandle, buf, sendOk);
    ++clumpCount;
  }
  gfClumpFreeList(&clumpList);
  errSendString(connectionHandle, "end", sendOk);
  logDebug("%lu PCR %s %s %d clumps", clock1000(), fPrimer, rPrimer, clumpCount);
}

// NOTE: may have some problems <05-09-23>
static jmp_buf gfRecover;
static char *ripCord = NULL;  // A little memory to give back to system *during error recovery.

void gfAbort()
//  Abort query.
{
  freez(&ripCord);
  longjmp(gfRecover, -1);
}

void errorSafeSetup()
/* Start up error safe stuff. */
{
  pushAbortHandler(gfAbort);  // must come before memTracker
  memTrackerStart();
  ripCord = (char *)needMem(64 * 1024); /* Memory for error recovery. memTrackerEnd frees */
}

void errorSafeCleanup()
/* Clean up and report problem. */
{
  memTrackerEnd();
  popAbortHandler();  // must come after memTracker
}

void errorSafeCleanupMess(int connectionHandle, char *message, boolean &sendOk)
/* Clean up and report problem. */
{
  errorSafeCleanup();
  logError("Recovering from error via longjmp");
  errSendString(connectionHandle, message, sendOk);
}

void errorSafeQuery(boolean doTrans, boolean queryIsProt, struct dnaSeq *seq, struct genoFindIndex *gfIdx,
                    int connectionHandle, char *buf, struct hash *perSeqMaxHash, ServerOption const &options,
                    UsageStats &stats, boolean &sendOk)
/* Wrap error handling code around index query. */
{
  int status;
  errorSafeSetup();
  status = setjmp(gfRecover);
  if (status == 0) /* Always true except after long jump. */
  {
    if (doTrans) {
      if (queryIsProt)
        transQuery(gfIdx->transGf, seq, connectionHandle, options, stats, sendOk);
      else
        transTransQuery(gfIdx->transGf, seq, connectionHandle, options, stats, sendOk);
    } else
      dnaQuery(gfIdx->untransGf, seq, connectionHandle, perSeqMaxHash, options, stats, sendOk);
    errorSafeCleanup();
  } else /* They long jumped here because of an error. */
  {
    errorSafeCleanupMess(connectionHandle, "Error: gfServer out of memory. Try reducing size of query.", sendOk);
  }
}

void errorSafePcr(struct genoFind *gf, char *fPrimer, char *rPrimer, int maxDistance, int connectionHandle,
                  boolean &sendOk)
/* Wrap error handling around pcr index query. */
{
  int status;
  errorSafeSetup();
  status = setjmp(gfRecover);
  if (status == 0) /* Always true except after long jump. */
  {
    pcrQuery(gf, fPrimer, rPrimer, maxDistance, connectionHandle, sendOk);
    errorSafeCleanup();
  } else /* They long jumped here because of an error. */
  {
    errorSafeCleanupMess(connectionHandle, "Error: gfServer out of memory.", sendOk);
  }
}

boolean badPcrPrimerSeq(char *s)
/* Return TRUE if have a character we can't handle in sequence. */
{
  unsigned char c;
  while ((c = *s++) != 0) {
    if (ntVal[c] < 0) return TRUE;
  }
  return FALSE;
}

boolean haveFileBaseName(char *baseName, int fileCount, char *seqFiles[])
/* check if the file list contains the base name of the per-seq max spec */
{
  int i;
  for (i = 0; i < fileCount; i++)
    if (sameString(findTail(seqFiles[i], '/'), baseName)) return TRUE;
  return FALSE;
}

struct hash *buildPerSeqMax(int fileCount, char *seqFiles[], char *perSeqMaxFile)
/* do work of building perSeqMaxhash */
{
  struct hash *perSeqMaxHash = hashNew(0);
  struct lineFile *lf = lineFileOpen(perSeqMaxFile, TRUE);
  char *line;
  while (lineFileNextReal(lf, &line)) {
    // Make sure line contains a valid seq filename (before optional ':seq'),
    // directories are ignored
    char *seqFile = findTail(trimSpaces(line), '/');
    char copy[strlen(seqFile) + 1];
    safecpy(copy, sizeof copy, seqFile);
    char *colon = strrchr(copy, ':');
    if (colon) *colon = '\0';
    if (haveFileBaseName(copy, fileCount, seqFiles) < 0)
      lineFileAbort(lf,
                    "'%s' does not appear to be a sequence file from the "
                    "command line",
                    copy);
    hashAddInt(perSeqMaxHash, seqFile, 0);
  }
  lineFileClose(&lf);
  return perSeqMaxHash;
}

struct hash *maybePerSeqMax(int fileCount, char *seqFiles[], ServerOption &options)
/* If options include -perSeqMax=file, then read the sequences named in the file
 * into a hash for testing membership in the set of sequences to exclude from
 * -maxDnaHits accounting. */
{
  // char *fileName = optionVal("perSeqMax", NULL);
  char *fileName = options.perSeqMax.empty() ? NULL : options.perSeqMax.data();

  if (isNotEmpty(fileName))
    return buildPerSeqMax(fileCount, seqFiles, fileName);
  else
    return NULL;
}

void hashZeroVals(struct hash *hash)
/* Set the value of every element of hash to NULL (0 for ints). */
{
  struct hashEl *hel;
  struct hashCookie cookie = hashFirst(hash);
  while ((hel = hashNext(&cookie)) != NULL) hel->val = 0;
}

void checkIndexFileName(char *gfxFile, char *seqFile, ServerOption const &options)
/* validate that index matches conventions, as base name is stored in index */
{
  boolean doTrans = bool2boolean(options.trans);

  char seqBaseName[FILENAME_LEN], seqExt[FILEEXT_LEN];
  splitPath(seqFile, NULL, seqBaseName, seqExt);
  if ((strlen(seqBaseName) == 0) || !sameString(seqExt, ".2bit"))
    errAbort(
        "gfServer index requires a two-bit genome file with a base name "
        "of `myGenome.2bit`, got %s%s",
        seqBaseName, seqExt);

  char gfxBaseName[FILENAME_LEN], gfxExt[FILEEXT_LEN];
  splitPath(gfxFile, NULL, gfxBaseName, gfxExt);
  if (!sameString(gfxExt, ".gfidx")) errAbort("gfServer index must have an file extension of '.gfidx', got %s", gfxExt);
  char expectBaseName[FILENAME_LEN];
  safef(expectBaseName, sizeof(expectBaseName), "%s.%s", seqBaseName, (doTrans ? "trans" : "untrans"));
  if (!sameString(gfxBaseName, expectBaseName))
    errAbort("%s index file base name must be '%s.gfidx', got %s%s", (doTrans ? "translated" : "untranslated"),
             expectBaseName, gfxBaseName, gfxExt);
}

void dynWarnErrorVa(char *msg, va_list args)
/* warnHandler to log and send back an error response */
{
  char buf[4096];
  int msgLen = vsnprintf(buf, sizeof(buf) - 1, msg, args);
  buf[msgLen] = '\0';
  logError("%s", buf);
  printf("Error: %s\n", buf);
}

struct dynSession
/* information on dynamic server connection session.  This is all data
 * currently cached.  If is not changed if the genome and query mode is the
 * same as the previous request.
 */
{
  boolean isTrans;              // translated
  char genome[256];             // genome name
  struct hash *perSeqMaxHash;   // max hits per sequence
  struct genoFindIndex *gfIdx;  // index
};

struct genoFindIndex *loadGfIndex(char *gfIdxFile, boolean isTrans, ServerOption &options)
/* load index and set globals from it */
{
  struct genoFindIndex *gfIdx = genoFindIndexLoad(gfIdxFile, isTrans);
  struct genoFind *gf = isTrans ? gfIdx->transGf[0][0] : gfIdx->untransGf;

  // minMatch = gf->minMatch;
  // maxGap = gf->maxGap;
  // tileSize = gf->tileSize;
  // noSimpRepMask = gf->noSimpRepMask;
  // allowOneMismatch = gf->allowOneMismatch;
  // stepSize = gf->stepSize;

  options.minMatch = gf->minMatch;
  options.maxGap = gf->maxGap;
  options.tileSize = gf->tileSize;
  options.noSimpRepMask = gf->noSimpRepMask;
  options.allowOneMismatch = gf->allowOneMismatch;
  options.stepSize = gf->stepSize;

  logGenoFindIndex(gfIdx);
  return gfIdx;
}

void dynWarnHandler(char *format, va_list args)
/* log error warning and error message, along with printing */
{
  logErrorVa(format, args);
  vfprintf(stderr, format, args);
  fputc('\n', stderr);
}

void dynSessionInit(struct dynSession *dynSession, char *rootDir, char *genome, char *genomeDataDir, boolean isTrans,
                    ServerOption &options)
/* Initialize or reinitialize a dynSession object */
{
  if ((!isSafeRelativePath(genome)) || (strchr(genome, '/') != NULL))
    errAbort("genome argument can't contain '/' or '..': %s", genome);
  if (!isSafeRelativePath(genomeDataDir))
    errAbort(
        "genomeDataDir argument must be a relative path without '..' "
        "elements: %s",
        genomeDataDir);

  // will free current content if initialized
  genoFindIndexFree(&dynSession->gfIdx);
  hashFree(&dynSession->perSeqMaxHash);

  time_t startTime = clock1000();
  dynSession->isTrans = isTrans;
  safecpy(dynSession->genome, sizeof(dynSession->genome), genome);

  // construct path to sequence and index files
  char seqFileDir[PATH_LEN];
  safef(seqFileDir, sizeof(seqFileDir), "%s/%s", rootDir, genomeDataDir);

  char seqFile[PATH_LEN];
  safef(seqFile, PATH_LEN, "%s/%s.2bit", seqFileDir, genome);
  if (!fileExists(seqFile)) errAbort("sequence file for %s does not exist: %s", genome, seqFile);

  char gfIdxFile[PATH_LEN];
  safef(gfIdxFile, PATH_LEN, "%s/%s.%s.gfidx", seqFileDir, genome, isTrans ? "trans" : "untrans");
  if (!fileExists(gfIdxFile)) errAbort("gf index file for %s does not exist: %s", genome, gfIdxFile);
  dynSession->gfIdx = loadGfIndex(gfIdxFile, isTrans, options);

  char perSeqMaxFile[PATH_LEN];
  safef(perSeqMaxFile, PATH_LEN, "%s/%s.perseqmax", seqFileDir, genome);
  if (fileExists(perSeqMaxFile)) {
    /* only the basename of the file is saved in the index */
    char *slash = strrchr(seqFile, '/');
    char *seqFiles[1] = {(slash != NULL) ? slash + 1 : seqFile};
    dynSession->perSeqMaxHash = buildPerSeqMax(1, seqFiles, perSeqMaxFile);
  }
  logInfo("dynserver: index loading completed in %4.3f seconds", 0.001 * (clock1000() - startTime));
}

char *dynReadCommand(char *rootDir)
/* read command and log, NULL if no more */
{
  char buf[PATH_LEN];
  int readSize = read(STDIN_FILENO, buf, sizeof(buf) - 1);
  if (readSize < 0) errAbort("EOF from client");
  if (readSize == 0) return NULL;
  buf[readSize] = '\0';
  if (!startsWith(gfSignature(), buf)) errAbort("query does not start with signature, got '%s'", buf);
  char *cmd = cloneString(buf + strlen(gfSignature()));
  logInfo("dynserver: %s", cmd);
  return cmd;
}

// static const int DYN_CMD_MAX_ARGS = 8;  // more than needed to check for junk

int dynNextCommand(char *rootDir, struct dynSession *dynSession, char **args, ServerOption &options)
/* Read query request from stdin and (re)initialize session to match
 * parameters.  Return number of arguments or zero on EOF
 *
 * Commands are in the format:
 *  signature+command genome genomeDataDir [arg ...]
 *  signature+status
 */
{
  const int DYN_CMD_MAX_ARGS = 8;  // more than needed to check for junk
  char *cmdStr = dynReadCommand(rootDir);
  if (cmdStr == NULL) return 0;

  int numArgs = chopByWhite(cmdStr, args, DYN_CMD_MAX_ARGS);
  if (numArgs == 0) errAbort("empty command");
  if (sameWord(args[0], "status")) return numArgs;  // special case; does not use an index.

  if (numArgs < 3) errAbort("expected at least 3 arguments for a dynamic server command");
  boolean isTrans =
      sameString("protQuery", args[0]) || sameString("transQuery", args[0]) || sameString("transInfo", args[0]);

  // initialize session if new or changed
  if ((dynSession->isTrans != isTrans) || (!sameString(dynSession->genome, args[1])))
    dynSessionInit(dynSession, rootDir, args[1], args[2], isTrans, options);
  return numArgs;
}

struct dnaSeq *dynReadQuerySeq(int qSize, boolean isTrans, boolean queryIsProt, ServerOption const &options)
/* read the DNA sequence from the query, filtering junk  */
{
  auto maxAaSize = options.maxAaSize;
  auto maxNtSize = options.maxNtSize;

  struct dnaSeq *seq;
  // AllocVar(seq);
  seq = (dnaSeq *)needMem(sizeof(*seq));
  seq->size = qSize;
  seq->dna = (char *)needLargeMem(qSize + 1);
  if (gfReadMulti(STDIN_FILENO, seq->dna, qSize) != qSize) errAbort("read of %d bytes of query sequence failed", qSize);
  seq->dna[qSize] = '\0';

  if (queryIsProt) {
    seq->size = aaFilteredSize(seq->dna);
    aaFilter(seq->dna, seq->dna);
  } else {
    seq->size = dnaFilteredSize(seq->dna);
    dnaFilter(seq->dna, seq->dna);
  }
  int maxSize = (isTrans ? maxAaSize : maxNtSize);
  if (seq->size > maxSize) {
    seq->size = maxSize;
    seq->dna[maxSize] = 0;
  }

  return seq;
}

void dynamicServerQuery(struct dynSession *dynSession, int numArgs, char **args, ServerOption const &options,
                        UsageStats &stats, boolean &sendOk)
/* handle search queries
 *
 *  signature+command genome genomeDataDir qsize
 */
{
  struct genoFindIndex *gfIdx = dynSession->gfIdx;
  if (numArgs != 4) errAbort("expected 4 words in %s command, got %d", args[0], numArgs);
  int qSize = atoi(args[3]);

  boolean queryIsProt = sameString(args[0], "protQuery");
  mustWriteFd(STDOUT_FILENO, (void *)"Y", 1);
  struct dnaSeq *seq = dynReadQuerySeq(qSize, gfIdx->isTrans, queryIsProt, options);
  if (gfIdx->isTrans) {
    if (queryIsProt)
      transQuery(gfIdx->transGf, seq, STDOUT_FILENO, options, stats, sendOk);
    else
      transTransQuery(gfIdx->transGf, seq, STDOUT_FILENO, options, stats, sendOk);
  } else {
    dnaQuery(gfIdx->untransGf, seq, STDOUT_FILENO, dynSession->perSeqMaxHash, options, stats, sendOk);
  }
  netSendString(STDOUT_FILENO, "end");
}

void dynamicServerInfo(struct dynSession *dynSession, int numArgs, char **args)
/* handle one of the info or status commands commands
 *
 *  signature+untransInfo genome genomeDataDir
 *  signature+transInfo genome genomeDataDir
 */
{
  struct genoFindIndex *gfIdx = dynSession->gfIdx;
  if (numArgs != 3) errAbort("expected 3 words in %s command, got %d", args[0], numArgs);

  char buf[256];
  struct genoFind *gf = gfIdx->isTrans ? gfIdx->transGf[0][0] : gfIdx->untransGf;
  sprintf(buf, "version %s", gfVersion);
  netSendString(STDOUT_FILENO, buf);
  netSendString(STDOUT_FILENO, "serverType dynamic");
  sprintf(buf, "type %s", (gfIdx->isTrans ? "translated" : "nucleotide"));
  netSendString(STDOUT_FILENO, buf);
  sprintf(buf, "tileSize %d", gf->tileSize);
  netSendString(STDOUT_FILENO, buf);
  sprintf(buf, "stepSize %d", gf->stepSize);
  netSendString(STDOUT_FILENO, buf);
  sprintf(buf, "minMatch %d", gf->minMatch);
  netSendString(STDOUT_FILENO, buf);
  netSendString(STDOUT_FILENO, "end");
}

void dynamicServerStatus(int numArgs, char **args)
/* return enough information to indicate server is working without opening
 * a genome index.
 *
 *  signature+status
 */
{
  if (numArgs != 1) errAbort("expected 1 word in %s command, got %d", args[0], numArgs);
  char buf[256];
  sprintf(buf, "version %s", gfVersion);
  netSendString(STDOUT_FILENO, buf);
  netSendString(STDOUT_FILENO, "serverType dynamic");
  netSendString(STDOUT_FILENO, "end");
}

void dynamicServerPcr(struct dynSession *dynSession, int numArgs, char **args, boolean &sendOk)
/* Execute a PCR query
 *
 *  signature+command genome genomeDataDir forward reverse maxDistance
 */
{
  struct genoFindIndex *gfIdx = dynSession->gfIdx;
  if (numArgs != 6) errAbort("expected 6 words in %s command, got %d", args[0], numArgs);
  char *fPrimer = args[3];
  char *rPrimer = args[4];
  int maxDistance = atoi(args[5]);
  if (badPcrPrimerSeq(fPrimer) || badPcrPrimerSeq(rPrimer)) errAbort("Can only handle ACGT in primer sequences.");
  pcrQuery(gfIdx->untransGf, fPrimer, rPrimer, maxDistance, STDOUT_FILENO, sendOk);
}

bool dynamicServerCommand(char *rootDir, struct dynSession *dynSession, ServerOption &options, UsageStats &stats,
                          boolean &sendOk)
/* Execute one command from stdin, (re)initializing session as needed */
{
  const int DYN_CMD_MAX_ARGS = 8;  // more than needed to check for junk

  time_t startTime = clock1000();
  char *args[DYN_CMD_MAX_ARGS];
  int numArgs = dynNextCommand(rootDir, dynSession, args, options);
  if (numArgs == 0) return FALSE;
  if (sameString("query", args[0]) || sameString("protQuery", args[0]) || sameString("transQuery", args[0])) {
    dynamicServerQuery(dynSession, numArgs, args, options, stats, sendOk);
  } else if (sameString("status", args[0])) {
    dynamicServerStatus(numArgs, args);
  } else if (sameString("untransInfo", args[0]) || sameString("transInfo", args[0])) {
    dynamicServerInfo(dynSession, numArgs, args);
  } else if (sameString("pcr", args[0])) {
    dynamicServerPcr(dynSession, numArgs, args, sendOk);
  } else
    errAbort("invalid command '%s'", args[0]);

  logInfo("dynserver: %s completed in %4.3f seconds", args[0], 0.001 * (clock1000() - startTime));
  freeMem(args[0]);
  return TRUE;
}

void gfServer(ServerOption &options)
/* Process command line. */
{
  char *command;

  gfCatchPipes();
  dnaUtilOpen();

  command = "test";

  // tileSize = optionInt("tileSize", tileSize);
  // stepSize = optionInt("stepSize", tileSize);

  // if (optionExists("repMatch"))
  // repMatch = optionInt("repMatch", 0);
  // else
  // repMatch = gfDefaultRepMatch(tileSize, stepSize, doTrans);

  // minMatch = optionInt("minMatch", minMatch);
  // maxDnaHits = optionInt("maxDnaHits", maxDnaHits);
  // maxTransHits = optionInt("maxTransHits", maxTransHits);
  // maxNtSize = optionInt("maxNtSize", maxNtSize);
  // maxAaSize = optionInt("maxAaSize", maxAaSize);

  // seqLog = optionExists("seqLog");
  // ipLog = optionExists("ipLog");
  // doMask = optionExists("mask");
  // canStop = optionExists("canStop");
  // noSimpRepMask = optionExists("noSimpRepMask");

  // auto indexFile = options.indexFile.empty() ? NULL : options.indexFile.data();

  // no need to get from command line
  auto genome = options.genome.empty() ? NULL : options.genome.data();
  auto genomeDataDir = options.genomeDataDir.empty() ? NULL : options.genomeDataDir.data();

  if ((genomeDataDir != NULL) && (genome == NULL)) errAbort("-genomeDataDir requires the -genome option");
  if ((genome != NULL) && (genomeDataDir == NULL)) genomeDataDir = ".";

  // auto timeout = options.timeout;

  // if (optionExists("log")) logOpenFile(argv[0], optionVal("log", NULL));
  // if (optionExists("syslog")) logOpenSyslog(argv[0], optionVal("logFacility", NULL));
  // if (optionExists("debugLog")) logSetMinPriority("debug");

  if (sameWord(command, "direct")) {
    printf("direct\n");
    // genoFindDirect(argv[2], argc - 3, argv + 3);
  } else if (sameWord(command, "pcrDirect")) {
    // if (argc < 5) usage();
    // genoPcrDirect(argv[2], argv[3], argc - 4, argv + 4);
    printf("pcrDirect\n");
  } else if (sameWord(command, "start")) {
    // if (argc < 5) usage();
    // startServer(argv[2], argv[3], argc - 4, argv + 4);
    printf("start\n");
  } else if (sameWord(command, "stop")) {
    // if (argc != 4) usage();
    // stopServer(argv[2], argv[3]);
    printf("stop\n");
  } else if (sameWord(command, "query")) {
    // if (argc != 5) usage();
    // queryServer(command, argv[2], argv[3], argv[4], FALSE, FALSE);
    printf("query\n");
  } else if (sameWord(command, "protQuery")) {
    // if (argc != 5) usage();
    // queryServer(command, argv[2], argv[3], argv[4], TRUE, TRUE);
    printf("protQuery\n");
  } else if (sameWord(command, "transQuery")) {
    // if (argc != 5) usage();
    // queryServer(command, argv[2], argv[3], argv[4], TRUE, FALSE);
    printf("transQuery\n");
  } else if (sameWord(command, "pcr")) {
    // if (argc != 7) usage();
    // pcrServer(argv[2], argv[3], argv[4], argv[5], atoi(argv[6]));
    printf("pcr\n");
  } else if (sameWord(command, "status")) {
    // if (argc != 4) usage();
    // if (statusServer(argv[2], argv[3])) {
    // exit(-1);
    // }
    printf("status\n");
  } else if (sameWord(command, "files")) {
    // if (argc != 4) usage();
    // getFileList(argv[2], argv[3]);
    printf("files\n");
  } else if (sameWord(command, "index")) {
    // if (argc < 4) usage();
    // buildIndex(argv[2], argc - 3, argv + 3);
    printf("index\n");
  } else if (sameWord(command, "dynserver")) {
    // if (argc < 3) usage();
    // dynamicServer(argv[2]);
    printf("dynserver\n");
  } else {
    // usage(options);
    printf("usage\n");
  }
}

// cpp implementation
void genoFindDirect(std::string &probeName, int fileCount, std::vector<std::string> &seqFiles,
                    ServerOption const &options)
/* Don't set up server - just directly look for matches. */
{
  auto minMatch = options.minMatch;
  auto maxGap = options.maxGap;
  auto tileSize = options.tileSize;
  auto repMatch = options.repMatch;
  auto stepSize = options.stepSize;

  boolean doTrans = bool2boolean(options.trans);
  boolean allowOneMismatch = bool2boolean(options.allowOneMismatch);
  boolean noSimpRepMask = bool2boolean(options.noSimpRepMask);

  std::vector<char *> cseqFiles{};
  cseqFiles.reserve(seqFiles.size());
  for (auto &string : seqFiles) {
    cseqFiles.push_back(string.data());
  }

  struct genoFind *gf = NULL;
  struct lineFile *lf = lineFileOpen(probeName.data(), TRUE);
  struct dnaSeq seq;
  int hitCount = 0, clumpCount = 0, oneHit;
  ZeroVar(&seq);

  if (doTrans) errAbort("Don't support translated direct stuff currently, sorry");

  gf = gfIndexNibsAndTwoBits(fileCount, cseqFiles.data(), minMatch, maxGap, tileSize, repMatch, FALSE, allowOneMismatch,
                             stepSize, noSimpRepMask);

  while (faSpeedReadNext(lf, &seq.dna, &seq.size, &seq.name)) {
    struct lm *lm = lmInit(0);
    struct gfClump *clumpList = gfFindClumps(gf, &seq, lm, &oneHit), *clump;
    hitCount += oneHit;
    for (clump = clumpList; clump != NULL; clump = clump->next) {
      ++clumpCount;
      printf("%s ", seq.name);
      gfClumpDump(gf, clump, stdout);
    }
    gfClumpFreeList(&clumpList);
    lmCleanup(&lm);
  }
  lineFileClose(&lf);
  genoFindFree(&gf);
}

void genoPcrDirect(std::string &fPrimer, std::string &rPrimer, int fileCount, std::vector<std::string> &seqFiles,
                   ServerOption const &options) {
  auto minMatch = options.minMatch;
  auto maxGap = options.maxGap;
  auto tileSize = options.tileSize;
  auto repMatch = options.repMatch;
  auto stepSize = options.stepSize;

  boolean allowOneMismatch = bool2boolean(options.allowOneMismatch);
  boolean noSimpRepMask = bool2boolean(options.noSimpRepMask);

  std::vector<char *> cseqFiles{};
  cseqFiles.reserve(seqFiles.size());
  for (auto &string : seqFiles) {
    cseqFiles.push_back(string.data());
  }

  struct genoFind *gf = NULL;
  int fPrimerSize = strlen(fPrimer.data());
  int rPrimerSize = strlen(rPrimer.data());
  struct gfClump *clumpList, *clump;
  time_t startTime, endTime;

  startTime = clock1000();
  gf = gfIndexNibsAndTwoBits(fileCount, cseqFiles.data(), minMatch, maxGap, tileSize, repMatch, FALSE, allowOneMismatch,
                             stepSize, noSimpRepMask);
  endTime = clock1000();
  printf("Index built in %4.3f seconds\n", 0.001 * (endTime - startTime));

  printf("plus strand:\n");
  startTime = clock1000();
  clumpList = gfPcrClumps(gf, fPrimer.data(), fPrimerSize, rPrimer.data(), rPrimerSize, 0, 4 * 1024);
  endTime = clock1000();
  printf("Index searched in %4.3f seconds\n", 0.001 * (endTime - startTime));
  for (clump = clumpList; clump != NULL; clump = clump->next) {
    /* Clumps from gfPcrClumps have already had target->start subtracted out
     * of their coords, but gfClumpDump assumes they have not and does the
     * subtraction; rather than write a new gfClumpDump, tweak here: */
    clump->tStart += clump->target->start;
    clump->tEnd += clump->target->start;
    gfClumpDump(gf, clump, stdout);
  }
  printf("minus strand:\n");
  startTime = clock1000();
  clumpList = gfPcrClumps(gf, rPrimer.data(), rPrimerSize, fPrimer.data(), fPrimerSize, 0, 4 * 1024);
  endTime = clock1000();
  printf("Index searched in %4.3f seconds\n", 0.001 * (endTime - startTime));
  for (clump = clumpList; clump != NULL; clump = clump->next) {
    /* Same as above, tweak before gfClumpDump: */
    clump->tStart += clump->target->start;
    clump->tEnd += clump->target->start;
    gfClumpDump(gf, clump, stdout);
  }

  genoFindFree(&gf);
}

genoFindIndex *pybuildIndex4Server(std::string &hostName, std::string &portName, int fileCount, char *seqFiles[],
                                   hash *perSeqMaxHash, ServerOption &option) {
  auto indexFile = option.indexFile.empty() ? NULL : option.indexFile.data();

  // auto ipLog = option.ipLog;
  auto minMatch = option.minMatch;
  auto maxGap = option.maxGap;
  auto tileSize = option.tileSize;
  auto repMatch = option.repMatch;
  auto stepSize = option.stepSize;
  // auto timeout = option.timeout;
  // auto maxAaSize = option.maxAaSize;
  // auto maxNtSize = option.maxNtSize;

  // boolean seqLog = bool2boolean(option.seqLog);
  // boolean canStop = bool2boolean(option.canStop);
  boolean doTrans = bool2boolean(option.trans);
  boolean doMask = bool2boolean(option.mask);
  boolean allowOneMismatch = bool2boolean(option.allowOneMismatch);
  boolean noSimpRepMask = bool2boolean(option.noSimpRepMask);

  struct genoFindIndex *gfIdx = NULL;
  time_t curtime;
  struct tm *loctime;
  char timestr[256];

  netBlockBrokenPipes();

  curtime = time(NULL);                                          /* Get the current time. */
  loctime = localtime(&curtime);                                 /* Convert it to local time representation. */
  strftime(timestr, sizeof(timestr), "%Y-%m-%d %H:%M", loctime); /* formate datetime as string */

  logInfo("gfServer version %s on host %s, port %s  (%s)", gfVersion, hostName.data(), portName.data(), timestr);
  perSeqMaxHash = maybePerSeqMax(fileCount, seqFiles, option);

  time_t startIndexTime = clock1000();
  if (indexFile == NULL) {
    char const *desc = doTrans ? "translated" : "untranslated";
    // uglyf("starting %s server...\n", desc);
    dbg("starting %s server...", desc);
    // logInfo("setting up %s index", desc);
    gfIdx = genoFindIndexBuild(fileCount, seqFiles, minMatch, maxGap, tileSize, repMatch, doTrans, NULL,
                               allowOneMismatch, doMask, stepSize, noSimpRepMask);
    logInfo("index building completed in %4.3f seconds", 0.001 * (clock1000() - startIndexTime));
  } else {
    gfIdx = genoFindIndexLoad(indexFile, doTrans);
    logInfo("index loading completed in %4.3f seconds", 0.001 * (clock1000() - startIndexTime));
  }
  logGenoFindIndex(gfIdx);
  return gfIdx;
}
// void startServer(char *hostName, char *portName, int fileCount, char *seqFiles[])
void startServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                 ServerOption &options, UsageStats &stats)
/* Load up index and hang out in RAM. */
{
  auto indexFile = options.indexFile.empty() ? NULL : options.indexFile.data();

  auto ipLog = options.ipLog;
  auto minMatch = options.minMatch;
  auto maxGap = options.maxGap;
  auto tileSize = options.tileSize;
  auto repMatch = options.repMatch;
  auto stepSize = options.stepSize;
  auto timeout = options.timeout;
  auto maxAaSize = options.maxAaSize;
  auto maxNtSize = options.maxNtSize;

  boolean seqLog = bool2boolean(options.seqLog);
  boolean canStop = bool2boolean(options.canStop);
  boolean doTrans = bool2boolean(options.trans);
  boolean doMask = bool2boolean(options.mask);
  boolean allowOneMismatch = bool2boolean(options.allowOneMismatch);
  boolean noSimpRepMask = bool2boolean(options.noSimpRepMask);

  boolean sendOk = TRUE;
  std::vector<char *> cseqFiles{};
  cseqFiles.reserve(seqFiles.size());
  for (auto &string : seqFiles) {
    cseqFiles.push_back(string.data());
  }

  struct genoFindIndex *gfIdx = NULL;
  char buf[256];
  char *line, *command;
  struct sockaddr_in6 fromAddr;
  socklen_t fromLen;
  int readSize;
  int socketHandle = 0, connectionHandle = 0;
  int port = atoi(portName.data());
  time_t curtime;
  struct tm *loctime;
  char timestr[256];

  netBlockBrokenPipes();

  curtime = time(NULL);                                          /* Get the current time. */
  loctime = localtime(&curtime);                                 /* Convert it to local time representation. */
  strftime(timestr, sizeof(timestr), "%Y-%m-%d %H:%M", loctime); /* formate datetime as string */

  logInfo("gfServer version %s on host %s, port %s  (%s)", gfVersion, hostName.data(), portName.data(), timestr);
  printf("gfServer version %s on host %s, port %d  (%s)", gfVersion, hostName.data(), port, timestr);
  struct hash *perSeqMaxHash = maybePerSeqMax(fileCount, cseqFiles.data(), options);

  time_t startIndexTime = clock1000();
  if (indexFile == NULL) {
    char const *desc = doTrans ? "translated" : "untranslated";
    // uglyf("starting %s server...\n", desc);
    dbg("starting %s server...\n", desc);
    // logInfo("setting up %s index", desc);

    dbg(hostName, portName, fileCount, cseqFiles, options, stats);
    gfIdx = genoFindIndexBuild(fileCount, cseqFiles.data(), minMatch, maxGap, tileSize, repMatch, doTrans, NULL,
                               allowOneMismatch, doMask, stepSize, noSimpRepMask);
    logInfo("index building completed in %4.3f seconds", 0.001 * (clock1000() - startIndexTime));
  } else {
    gfIdx = genoFindIndexLoad(indexFile, doTrans);
    logInfo("index loading completed in %4.3f seconds", 0.001 * (clock1000() - startIndexTime));
  }
  logGenoFindIndex(gfIdx);

  /* Set up socket.  Get ready to listen to it. */
  socketHandle = netAcceptingSocket(port, 100);
  if (socketHandle < 0) errAbort("Fatal Error: Unable to open listening socket on port %d.", port);

  logInfo("Server ready for queries!");
  printf("Server ready for queries!\n");

  int connectFailCount = 0;
  for (;;) {
    ZeroVar(&fromAddr);
    fromLen = sizeof(fromAddr);
    connectionHandle = accept(socketHandle, (struct sockaddr *)&fromAddr, &fromLen);
    setSendOk(sendOk);
    if (connectionHandle < 0) {
      warn("Error accepting the connection");
      ++stats.warnCount;
      ++connectFailCount;
      if (connectFailCount >= 100)
        errAbort(
            "100 continuous connection failures, no point in filling up "
            "the log in an infinite loop.");
      continue;
    } else {
      connectFailCount = 0;
    }
    setSocketTimeout(connectionHandle, timeout);
    if (ipLog) {
      struct sockaddr_in6 clientAddr;
      unsigned int addrlen = sizeof(clientAddr);
      getpeername(connectionHandle, (struct sockaddr *)&clientAddr, &addrlen);
      char ipStr[NI_MAXHOST];
      getAddrAsString6n4((struct sockaddr_storage *)&clientAddr, ipStr, sizeof ipStr);
      logInfo("gfServer version %s on host %s, port %s connection from %s", gfVersion, hostName.data(), portName.data(),
              ipStr);
    }
    readSize = read(connectionHandle, buf, sizeof(buf) - 1);
    if (readSize < 0) {
      warn("Error reading from socket: %s", strerror(errno));
      ++stats.warnCount;
      close(connectionHandle);
      continue;
    }
    if (readSize == 0) {
      warn("Zero sized query");
      ++stats.warnCount;
      close(connectionHandle);
      continue;
    }
    buf[readSize] = 0;
    logDebug("%s", buf);
    if (!startsWith(gfSignature(), buf)) {
      ++stats.noSigCount;
      close(connectionHandle);
      continue;
    }

    line = buf + strlen(gfSignature());
    command = nextWord(&line);

    if (sameString("quit", command)) {
      if (canStop)
        break;
      else
        logError("Ignoring quit message");
    } else if (sameString("status", command) || sameString("transInfo", command) ||
               sameString("untransInfo", command)) {
      // dbg(hostName, portName, fileCount, cseqFiles, options, stats);

      dbg(connectionHandle, hostName, portName, fileCount, seqFiles, perSeqMaxHash, gfIdx, options);
      // sleep 10 s
      sleep(10);
      sprintf(buf, "version %s", gfVersion);
      errSendString(connectionHandle, buf, sendOk);
      errSendString(connectionHandle, "serverType static", sendOk);
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "type %s", (doTrans ? "translated" : "nucleotide"));
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "host %s", hostName.data());
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "port %s", portName.data());
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "tileSize %d", tileSize);
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "stepSize %d", stepSize);
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "minMatch %d", minMatch);
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "pcr requests %ld", stats.pcrCount);
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "blat requests %ld", stats.blatCount);
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "bases %ld", stats.baseCount);
      errSendString(connectionHandle, buf, sendOk);
      if (doTrans) {
        sprintf(buf, "aa %ld", stats.aaCount);
        errSendString(connectionHandle, buf, sendOk);
      }
      sprintf(buf, "misses %d", stats.missCount);
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "noSig %d", stats.noSigCount);
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "trimmed %d", stats.trimCount);
      errSendString(connectionHandle, buf, sendOk);
      sprintf(buf, "warnings %d", stats.warnCount);
      errSendString(connectionHandle, buf, sendOk);
      errSendString(connectionHandle, "end", sendOk);
    } else if (sameString("query", command) || sameString("protQuery", command) || sameString("transQuery", command)) {
      boolean queryIsProt = sameString(command, "protQuery");
      char *s = nextWord(&line);
      if (s == NULL || !isdigit(s[0])) {
        warn("Expecting query size after query command");
        ++stats.warnCount;
      } else {
        struct dnaSeq seq;
        ZeroVar(&seq);

        if (queryIsProt && !doTrans) {
          warn("protein query sent to nucleotide server");
          ++stats.warnCount;
          queryIsProt = FALSE;
        } else {
          buf[0] = 'Y';
          if (write(connectionHandle, buf, 1) == 1) {
            seq.size = atoi(s);
            seq.name = NULL;
            if (seq.size > 0) {
              ++stats.blatCount;
              seq.dna = (char *)needLargeMem(seq.size + 1);
              if (gfReadMulti(connectionHandle, seq.dna, seq.size) != seq.size) {
                warn("Didn't sockRecieveString all %d bytes of query sequence", seq.size);
                ++stats.warnCount;
              } else {
                int maxSize = (doTrans ? maxAaSize : maxNtSize);

                seq.dna[seq.size] = 0;
                if (queryIsProt) {
                  seq.size = aaFilteredSize(seq.dna);
                  aaFilter(seq.dna, seq.dna);
                } else {
                  seq.size = dnaFilteredSize(seq.dna);
                  dnaFilter(seq.dna, seq.dna);
                }
                if (seq.size > maxSize) {
                  ++stats.trimCount;
                  seq.size = maxSize;
                  seq.dna[maxSize] = 0;
                }
                if (queryIsProt)
                  stats.aaCount += seq.size;
                else
                  stats.baseCount += seq.size;
                if (seqLog && (logGetFile() != NULL)) {
                  FILE *lf = logGetFile();
                  faWriteNext(lf, "query", seq.dna, seq.size);
                  fflush(lf);
                }
                errorSafeQuery(doTrans, queryIsProt, &seq, gfIdx, connectionHandle, buf, perSeqMaxHash, options, stats,
                               sendOk);
                if (perSeqMaxHash) hashZeroVals(perSeqMaxHash);
              }
              freez(&seq.dna);
            }
            errSendString(connectionHandle, "end", sendOk);
          }
        }
      }
    } else if (sameString("pcr", command)) {
      char *f = nextWord(&line);
      char *r = nextWord(&line);
      char *s = nextWord(&line);
      int maxDistance;
      ++stats.pcrCount;
      if (s == NULL || !isdigit(s[0])) {
        warn("Badly formatted pcr command");
        ++stats.warnCount;
      } else if (doTrans) {
        warn("Can't pcr on translated server");
        ++stats.warnCount;
      } else if (badPcrPrimerSeq(f) || badPcrPrimerSeq(r)) {
        warn("Can only handle ACGT in primer sequences.");
        ++stats.warnCount;
      } else {
        maxDistance = atoi(s);
        errorSafePcr(gfIdx->untransGf, f, r, maxDistance, connectionHandle, sendOk);
      }
    } else if (sameString("files", command)) {
      int i;
      sprintf(buf, "%d", fileCount);
      errSendString(connectionHandle, buf, sendOk);
      for (i = 0; i < fileCount; ++i) {
        sprintf(buf, "%s", seqFiles[i].data());
        errSendString(connectionHandle, buf, sendOk);
      }
    } else {
      warn("Unknown command %s", command);
      ++stats.warnCount;
    }
    close(connectionHandle);
    connectionHandle = 0;
  }
  close(socketHandle);
}

void stopServer(std::string &hostName, std::string &portName)
/* Send stop message to server. */
{
  char buf[256];
  int sd = 0;

  sd = netMustConnectTo(hostName.data(), portName.data());
  sprintf(buf, "%squit", gfSignature());
  mustWriteFd(sd, buf, strlen(buf));
  close(sd);
  printf("sent stop message to server\n");
}

std::string pyqueryServer(std::string &type, std::string &hostName, std::string &portName, std::string &faName,
                          bool complex, bool isProt)
/* Send simple query to server and report results. */
{
  auto ret_str = std::ostringstream{};

  char buf[256];
  int sd = 0;
  bioSeq *seq = faReadSeq(faName.data(), !isProt);
  int matchCount = 0;

  /* Put together query command. */
  sd = netMustConnectTo(hostName.data(), portName.data());
  sprintf(buf, "%s%s %d", gfSignature(), type.data(), seq->size);
  mustWriteFd(sd, buf, strlen(buf));

  if (read(sd, buf, 1) < 0) errAbort("queryServer: read failed: %s", strerror(errno));
  // if (read(sd, buf, 1) < 0) return std::nullopt;
  if (buf[0] != 'Y') errAbort("Expecting 'Y' from server, got %c", buf[0]);
  // if (buf[0] != 'Y') return std::nullopt;
  mustWriteFd(sd, seq->dna, seq->size);

  if (complex) {
    char *s = netRecieveString(sd, buf);
    printf("%s\n", s);
  }

  for (;;) {
    if (netGetString(sd, buf) == NULL) break;
    if (sameString(buf, "end")) {
      // printf("%d matches\n", matchCount);
      ret_str << matchCount << " matches"
              << "\n";
      break;
    } else if (startsWith("Error:", buf)) {
      errAbort("%s", buf);
      break;
    } else {
      // printf("%s\n", buf);
      ret_str << buf << "\n";
      if (complex) {
        char *s = netGetLongString(sd);
        if (s == NULL) break;
        // printf("%s\n", s);
        ret_str << s << "\n";
        freeMem(s);
      }
    }
    ++matchCount;
  }
  close(sd);
  return ret_str.str();
}

// void queryServer(char *type, char *hostName, char *portName, char *faName, boolean complex, boolean isProt)
void queryServer(std::string &type, std::string &hostName, std::string &portName, std::string &faName, bool complex,
                 bool isProt)
/* Send simple query to server and report results. */
{
  char buf[256];
  int sd = 0;
  bioSeq *seq = faReadSeq(faName.data(), !isProt);
  int matchCount = 0;

  /* Put together query command. */
  sd = netMustConnectTo(hostName.data(), portName.data());
  sprintf(buf, "%s%s %d", gfSignature(), type.data(), seq->size);
  mustWriteFd(sd, buf, strlen(buf));

  if (read(sd, buf, 1) < 0) errAbort("queryServer: read failed: %s", strerror(errno));
  if (buf[0] != 'Y') errAbort("Expecting 'Y' from server, got %c", buf[0]);
  mustWriteFd(sd, seq->dna, seq->size);

  if (complex) {
    char *s = netRecieveString(sd, buf);
    printf("%s\n", s);
  }

  for (;;) {
    if (netGetString(sd, buf) == NULL) break;
    if (sameString(buf, "end")) {
      printf("%d matches\n", matchCount);
      break;
    } else if (startsWith("Error:", buf)) {
      errAbort("%s", buf);
      break;
    } else {
      printf("%s\n", buf);
      if (complex) {
        char *s = netGetLongString(sd);
        if (s == NULL) break;
        printf("%s\n", s);
        freeMem(s);
      }
    }
    ++matchCount;
  }
  close(sd);
}

void pcrServer(std::string &hostName, std::string &portName, std::string &fPrimer, std::string &rPrimer, int maxSize)
/* Do a PCR query to server daemon. */
{
  char buf[256];
  int sd = 0;

  /* Put together query command and send. */
  sd = netMustConnectTo(hostName.data(), portName.data());
  sprintf(buf, "%spcr %s %s %d", gfSignature(), fPrimer.data(), rPrimer.data(), maxSize);
  mustWriteFd(sd, buf, strlen(buf));

  /* Fetch and display results. */
  for (;;) {
    if (netGetString(sd, buf) == NULL) break;
    if (sameString(buf, "end"))
      break;
    else if (startsWith("Error:", buf)) {
      errAbort("%s", buf);
      break;
    } else {
      printf("%s\n", buf);
    }
  }
  close(sd);
}

std::string pystatusServer(std::string &hostName, std::string &portName, ServerOption &options)
/* Send status message to server arnd report result. */
{
  auto ret_str = std::ostringstream{};
  auto genome = options.genome.empty() ? NULL : options.genome.data();
  auto genomeDataDir = options.genomeDataDir.empty() ? NULL : options.genomeDataDir.data();
  boolean doTrans = bool2boolean(options.trans);

  char buf[256];
  int sd = 0;
  int ret = 0;

  /* Put together command. */
  sd = netMustConnectTo(hostName.data(), portName.data());
  if (genome == NULL)
    sprintf(buf, "%sstatus", gfSignature());
  else
    sprintf(buf, "%s%s %s %s", gfSignature(), (doTrans ? "transInfo" : "untransInfo"), genome, genomeDataDir);

  mustWriteFd(sd, buf, strlen(buf));

  for (;;) {
    if (netGetString(sd, buf) == NULL) {
      warn("Error reading status information from %s:%s", hostName.data(), portName.data());
      ret = -1;
      break;
    }
    if (sameString(buf, "end"))
      break;
    else
      ret_str << buf << "\n";
  }
  close(sd);
  return ret_str.str();
}

int statusServer(std::string &hostName, std::string &portName, ServerOption &options)
/* Send status message to server arnd report result. */
{
  auto genome = options.genome.empty() ? NULL : options.genome.data();
  auto genomeDataDir = options.genomeDataDir.empty() ? NULL : options.genomeDataDir.data();
  boolean doTrans = bool2boolean(options.trans);

  char buf[256];
  int sd = 0;
  int ret = 0;

  /* Put together command. */
  sd = netMustConnectTo(hostName.data(), portName.data());
  if (genome == NULL)
    sprintf(buf, "%sstatus", gfSignature());
  else
    sprintf(buf, "%s%s %s %s", gfSignature(), (doTrans ? "transInfo" : "untransInfo"), genome, genomeDataDir);

  printf("%s\n", buf);
  mustWriteFd(sd, buf, strlen(buf));

  for (;;) {
    if (netGetString(sd, buf) == NULL) {
      warn("Error reading status information from %s:%s", hostName.data(), portName.data());
      ret = -1;
      break;
    }
    if (sameString(buf, "end"))
      break;
    else
      printf("%s from status\n", buf);
  }
  close(sd);
  return (ret);
}

std::string pygetFileList(std::string &hostName, std::string &portName)
/* Get and display input file list. */
{
  auto res = std::ostringstream{};
  char buf[256];
  int sd = 0;
  int fileCount;
  int i;

  /* Put together command. */
  sd = netMustConnectTo(hostName.data(), portName.data());
  sprintf(buf, "%sfiles", gfSignature());
  mustWriteFd(sd, buf, strlen(buf));

  /* Get count of files, and then each file name. */
  if (netGetString(sd, buf) != NULL) {
    fileCount = atoi(buf);
    for (i = 0; i < fileCount; ++i) {
      // printf("%s\n", netRecieveString(sd, buf));
      res << netRecieveString(sd, buf) << "\n";
    }
  }
  close(sd);
  return res.str();
}

void getFileList(std::string &hostName, std::string &portName)
/* Get and display input file list. */
{
  char buf[256];
  int sd = 0;
  int fileCount;
  int i;

  /* Put together command. */
  sd = netMustConnectTo(hostName.data(), portName.data());
  sprintf(buf, "%sfiles", gfSignature());
  mustWriteFd(sd, buf, strlen(buf));

  /* Get count of files, and then each file name. */
  if (netGetString(sd, buf) != NULL) {
    fileCount = atoi(buf);
    for (i = 0; i < fileCount; ++i) {
      printf("%s\n", netRecieveString(sd, buf));
    }
  }
  close(sd);
}

void buildIndex(std::string &gfxFile, int fileCount, std::vector<std::string> seqFiles, ServerOption const &options)
/* build pre-computed index for seqFiles and write to gfxFile */
{
  auto minMatch = options.minMatch;
  auto maxGap = options.maxGap;
  auto tileSize = options.tileSize;
  auto repMatch = options.repMatch;
  auto stepSize = options.stepSize;

  boolean doTrans = bool2boolean(options.trans);
  boolean allowOneMismatch = bool2boolean(options.allowOneMismatch);
  boolean doMask = bool2boolean(options.mask);
  boolean noSimpRepMask = bool2boolean(options.noSimpRepMask);

  std::vector<char *> cseqFiles{};
  cseqFiles.reserve(seqFiles.size());
  for (auto &string : seqFiles) {
    cseqFiles.push_back(string.data());
  }

  if (fileCount > 1) errAbort("gfServer index only works with a single genome file");
  checkIndexFileName(gfxFile.data(), cseqFiles.front(), options);

  struct genoFindIndex *gfIdx = genoFindIndexBuild(fileCount, cseqFiles.data(), minMatch, maxGap, tileSize, repMatch,
                                                   doTrans, NULL, allowOneMismatch, doMask, stepSize, noSimpRepMask);
  genoFindIndexWrite(gfIdx, gfxFile.data());
}

void dynamicServer(std::string &rootDir, ServerOption &options, UsageStats &stats, boolean &sendOk)
/* dynamic server for inetd. Read query from stdin, open index, query, respond,
 * exit. only one query at a time */
{
  pushWarnHandler(dynWarnHandler);
  logDebug("dynamicServer connect");
  struct runTimes startTimes = getTimesInSeconds();

  // make sure errors are logged
  pushWarnHandler(dynWarnErrorVa);
  struct dynSession dynSession;
  ZeroVar(&dynSession);

  while (dynamicServerCommand(rootDir.data(), &dynSession, options, stats, sendOk)) continue;

  struct runTimes endTimes = getTimesInSeconds();
  logInfo("dynserver: exit: clock: %0.4f user: %0.4f system: %0.4f (seconds)",
          endTimes.clockSecs - startTimes.clockSecs, endTimes.userSecs - startTimes.userSecs,
          endTimes.sysSecs - startTimes.sysSecs);

  logDebug("dynamicServer disconnect");
}

ServerOption &ServerOption::build() {
  if (trans) {
    tileSize = 4;
    stepSize = tileSize;
    minMatch = 3;
    maxGap = 0;
    repMatch = gfPepMaxTileUse;
  }

  if (repMatch == 0)
    repMatch = gfDefaultRepMatch(tileSize, stepSize, bool2boolean(trans));
  else
    repMatch = 0;

  return *this;
}

ServerOption &ServerOption::withCanStop(bool canStop_) {
  canStop = canStop_;
  return *this;
}

ServerOption &ServerOption::withLog(std::string log_) {
  log = std::move(log_);
  return *this;
}

ServerOption &ServerOption::withLogFacility(std::string logFacility_) {
  logFacility = std::move(logFacility_);
  return *this;
}

ServerOption &ServerOption::withMask(bool mask_) {
  mask = mask_;
  return *this;
}

ServerOption &ServerOption::withMaxAaSize(int maxAaSize_) {
  maxAaSize = maxAaSize_;
  return *this;
}

ServerOption &ServerOption::withMaxDnaHits(int maxDnaHits_) {
  maxDnaHits = maxDnaHits_;
  return *this;
}

ServerOption &ServerOption::withMaxGap(int maxGap_) {
  maxGap = maxGap_;
  return *this;
}

ServerOption &ServerOption::withMaxNtSize(int maxNtSize_) {
  maxNtSize = maxNtSize_;
  return *this;
}

ServerOption &ServerOption::withMaxTransHits(int maxTransHits_) {
  maxTransHits = maxTransHits_;
  return *this;
}

ServerOption &ServerOption::withMinMatch(int minMatch_) {
  minMatch = minMatch_;
  return *this;
}

ServerOption &ServerOption::withRepMatch(int repMatch_) {
  repMatch = repMatch_;
  return *this;
}

ServerOption &ServerOption::withSeqLog(bool seqLog_) {
  seqLog = seqLog_;
  return *this;
}

ServerOption &ServerOption::withIpLog(bool ipLog_) {
  ipLog = ipLog_;
  return *this;
}

ServerOption &ServerOption::withDebugLog(bool debugLog_) {
  debugLog = debugLog_;
  return *this;
}

ServerOption &ServerOption::withTileSize(int tileSize_) {
  tileSize = tileSize_;
  return *this;
}

ServerOption &ServerOption::withStepSize(int stepSize_) {
  stepSize = stepSize_;
  return *this;
}

ServerOption &ServerOption::withTrans(bool trans_) {
  trans = trans_;
  return *this;
}

ServerOption &ServerOption::withSyslog(bool syslog_) {
  syslog = syslog_;
  return *this;
}

ServerOption &ServerOption::withPerSeqMax(std::string perSeqMax_) {
  perSeqMax = std::move(perSeqMax_);
  return *this;
}

ServerOption &ServerOption::withNoSimpRepMask(bool noSimpRepMask_) {
  noSimpRepMask = noSimpRepMask_;
  return *this;
}

ServerOption &ServerOption::withIndexFile(std::string indexFile_) {
  indexFile = std::move(indexFile_);
  return *this;
}

ServerOption &ServerOption::withTimeout(int timeout_) {
  timeout = timeout_;
  return *this;
}

ServerOption &ServerOption::withThreads(int threads_) {
  threads = threads_;
  return *this;
}

std::string ServerOption::to_string() const {
  std::stringstream s{};
  s << "ServerOption(";
  s << "canStop: " << std::boolalpha << canStop;
  s << ", log: " << log;
  s << ", logFacility: " << logFacility;
  s << ", mask: " << mask;
  s << ", maxAaSize: " << maxAaSize;
  s << ", maxDnaHits: " << maxDnaHits;
  s << ", maxGap: " << maxGap;
  s << ", maxNtSize: " << maxNtSize;
  s << ", maxTransHits: " << maxTransHits;
  s << ", minMatch: " << minMatch;
  s << ", repMatch: " << repMatch;
  s << ", seqLog: " << std::boolalpha << seqLog;
  s << ", ipLog: " << std::boolalpha << ipLog;
  s << ", debugLog: " << std::boolalpha << debugLog;
  s << ", tileSize: " << tileSize;
  s << ", stepSize: " << stepSize;
  s << ", trans: " << std::boolalpha << trans;
  s << ", syslog: " << std::boolalpha << syslog;
  s << ", perSeqMax: " << perSeqMax;
  s << ", noSimpRepMask: " << std::boolalpha << noSimpRepMask;
  s << ", indexFile: " << indexFile;
  s << ", timeout: " << timeout;
  s << ", genome: " << genome;
  s << ", genomeDataDir: " << genomeDataDir;
  s << ", threads: " << threads;
  s << ", allowOneMismatch: " << std::boolalpha << allowOneMismatch << ")";

  return s.str();
}

std::ostream &operator<<(std::ostream &os, const ServerOption &option) {
  os << option.to_string();
  return os;
}

std::ostream &operator<<(std::ostream &os, const UsageStats &stats) {
  os << "UsageStats(";
  os << "baseCount: " << stats.baseCount;
  os << ", blatCount: " << stats.blatCount;
  os << ", aaCount: " << stats.aaCount;
  os << ", pcrCount: " << stats.pcrCount;
  os << ", warnCount: " << stats.warnCount;
  os << ", noSigCount: " << stats.noSigCount;
  os << ", missCount: " << stats.missCount;
  os << ", trimCount: " << stats.trimCount;
  os << ")";
  return os;
}

int globalint = 1;

void test_stdout() {
  printf("stdout\n");
  globalint += 1;
  printf("globalint is %d\n", globalint);
}
void test_add(int &a) { a += 1; }
void test_stat(UsageStats &stats) {
  stats.baseCount += 1;
  stats.blatCount += 1;
  stats.aaCount += 1;
  stats.pcrCount += 1;
  stats.warnCount += 1;
  stats.noSigCount += 1;
  stats.missCount += 1;
  stats.trimCount += 1;
}

void test_exception() { throw std::runtime_error("test exception"); }

}  // namespace cppbinding
