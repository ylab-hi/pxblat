#include <stdexcept>
#pragma GCC diagnostic ignored "-Wwrite-strings"

#include "bs_thread_pool.hpp"
#include "dbg.h"
#include "gfServer.hpp"
#include "pygfServer.hpp"

namespace cppbinding {

void pyerrorSafeQuery(boolean doTrans, boolean queryIsProt, struct dnaSeq *seq, struct genoFindIndex *gfIdx,
                      int connectionHandle, char *buf, struct hash *perSeqMaxHash, ServerOption const &options,
                      UsageStats &stats, boolean &sendOk)
/* Wrap error handling code around index query. */
{
  // status = setjmp(gfRecover);
  // if (status == 0) /* Always true except after long jump. */
  // {
  if (doTrans) {
    if (queryIsProt)
      transQuery(gfIdx->transGf, seq, connectionHandle, options, stats, sendOk);
    else
      transTransQuery(gfIdx->transGf, seq, connectionHandle, options, stats, sendOk);
  } else
    dnaQuery(gfIdx->untransGf, seq, connectionHandle, perSeqMaxHash, options, stats, sendOk);
  // errorSafeCleanup();
  // }
  // else /* They long jumped here because of an error. */
  // {
  // errorSafeCleanupMess(connectionHandle, "Error: gfServer out of memory. Try reducing size of query.", sendOk);
  // }
}

boolean pynetSendString(int sd, char *s)
/* Send a string down a socket - length byte first. */
{
  int length = strlen(s);
  UBYTE len;

  if (length > 255) errAbort("Trying to send a string longer than 255 bytes (%d bytes)", length);
  // throw std::runtime_error("Trying to send a string longer than 255 bytes");
  len = length;
  if (write(sd, &len, 1) < 0) {
    warn("Couldn't send string to socket");
    return FALSE;
  }
  if (write(sd, s, length) < 0) {
    warn("Couldn't send string to socket");
    return FALSE;
  }
  return TRUE;
}

void pyerrSendString(int sd, char *s, boolean &sendOk)
// Send string. If not OK, remember we had an error, do not try to write
// anything more on this connection.
{
  if (sendOk) sendOk = pynetSendString(sd, s);
}

void handle_client(int connectionHandle, std::string hostName, std::string portName, int fileCount,
                   std::vector<std::string> const &seqFiles, hash *perSeqMaxHash, genoFindIndex *gfIdx,
                   ServerOption const &option) {
  // dbg("begin func ", connectionHandle, hostName, portName, fileCount, seqFiles, perSeqMaxHash, gfIdx, option);

  // print current thread id

  dbg("thread id: ", std::this_thread::get_id());

  // auto ipLog = option.ipLog;
  auto minMatch = option.minMatch;
  // auto maxGap = option.maxGap;
  auto tileSize = option.tileSize;
  // auto repMatch = option.repMatch;
  auto stepSize = option.stepSize;
  auto timeout = option.timeout;
  auto maxAaSize = option.maxAaSize;
  auto maxNtSize = option.maxNtSize;

  boolean seqLog = bool2boolean(option.seqLog);
  // boolean canStop = bool2boolean(option.canStop);
  boolean doTrans = bool2boolean(option.trans);
  // boolean doMask = bool2boolean(option.mask);
  // boolean allowOneMismatch = bool2boolean(option.allowOneMismatch);
  // boolean noSimpRepMask = bool2boolean(option.noSimpRepMask);

  boolean sendOk = TRUE;
  UsageStats stats{};

  char buf[256];
  char *line{nullptr};
  char *command{nullptr};

  setSocketTimeout(connectionHandle, timeout);

  int readSize = read(connectionHandle, buf, sizeof(buf) - 1);

  if (readSize < 0) {
    warn("Error reading from socket: %s", strerror(errno));
    ++stats.warnCount;
    close(connectionHandle);
    return;
  }

  if (readSize == 0) {
    // warn("Zero sized query");
    dbg("Zero sized query");
    ++stats.warnCount;
    close(connectionHandle);
    return;
  }

  buf[readSize] = 0;
  // logDebug("%s", buf);
  if (!startsWith(gfSignature(), buf)) {
    ++stats.noSigCount;
    close(connectionHandle);
    return;
  }

  line = buf + strlen(gfSignature());
  command = nextWord(&line);
  dbg("receive", command);

  if (sameString("quit", command)) {
    // WARN: workaround <Yangyang Li yangyang.li@northwestern.edu>
    exit(0);
    // throw std::invalid_argument("exit server");
  }

  if (sameString("status", command) || sameString("transInfo", command) || sameString("untransInfo", command)) {
    // sleep 10 s
    sleep(10);
    sprintf(buf, "version %s", gfVersion);
    pyerrSendString(connectionHandle, buf, sendOk);
    pyerrSendString(connectionHandle, "serverType static", sendOk);
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "type %s", (doTrans ? "translated" : "nucleotide"));
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "host %s", hostName.data());
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "port %s", portName.data());
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "tileSize %d", tileSize);
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "stepSize %d", stepSize);
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "minMatch %d", minMatch);
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "pcr requests %ld", stats.pcrCount);
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "blat requests %ld", stats.blatCount);
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "bases %ld", stats.baseCount);
    pyerrSendString(connectionHandle, buf, sendOk);
    if (doTrans) {
      sprintf(buf, "aa %ld", stats.aaCount);
      pyerrSendString(connectionHandle, buf, sendOk);
    }
    sprintf(buf, "misses %d", stats.missCount);
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "noSig %d", stats.noSigCount);
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "trimmed %d", stats.trimCount);
    pyerrSendString(connectionHandle, buf, sendOk);
    sprintf(buf, "warnings %d", stats.warnCount);
    pyerrSendString(connectionHandle, buf, sendOk);
    pyerrSendString(connectionHandle, "end", sendOk);
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
              dbg("query", seq.dna);

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
              errorSafeQuery(doTrans, queryIsProt, &seq, gfIdx, connectionHandle, buf, perSeqMaxHash, option, stats,
                             sendOk);
              if (perSeqMaxHash) hashZeroVals(perSeqMaxHash);
            }
            freez(&seq.dna);
          }
          pyerrSendString(connectionHandle, "end", sendOk);
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
    pyerrSendString(connectionHandle, buf, sendOk);
    for (i = 0; i < fileCount; ++i) {
      sprintf(buf, "%s", seqFiles[i].data());
      pyerrSendString(connectionHandle, buf, sendOk);
    }
  } else {
    warn("Unknown command %s", command);
    ++stats.warnCount;
  }
  close(connectionHandle);
  // connectionHandle = 0;
}

int pystartServer(std::string &hostName, std::string &portName, int fileCount, std::vector<std::string> &seqFiles,
                  ServerOption &option, UsageStats &stats) {
  BS::thread_pool pool(option.threads);

  std::vector<char *> cseqFiles{};
  cseqFiles.reserve(seqFiles.size());
  for (auto &string : seqFiles) {
    cseqFiles.push_back(string.data());
  }

  struct sockaddr_in6 fromAddr;
  socklen_t fromLen;

  int socketHandle = 0;
  int port = atoi(portName.data());

  hash *perSeqMaxHash = nullptr;
  genoFindIndex *gfIdx = pybuildIndex4Server(hostName, portName, fileCount, cseqFiles.data(), perSeqMaxHash, option);

  /* Set up socket.  Get ready to listen to it. */
  socketHandle = netAcceptingSocket(port, 100);
  if (socketHandle < 0)
    throw std::runtime_error("Fatal Error: Unable to open listening socket on port " + portName + ".");
  // errAbort("Fatal Error: Unable to open listening socket on port %d.", port);

  int connectFailCount = 0;
  for (;;) {
    ZeroVar(&fromAddr);
    fromLen = sizeof(fromAddr);
    int connectionHandle = accept(socketHandle, (struct sockaddr *)&fromAddr, &fromLen);

    // setSendOk(sendOk);

    if (connectionHandle < 0) {
      warn("Error accepting the connection");
      ++stats.warnCount;
      ++connectFailCount;

      if (connectFailCount >= 100)
        // errAbort( "100 continuous connection failures, no point in filling up " "the log in an infinite loop.");
        throw std::runtime_error(
            "100 continuous connection failures, no point in filling up the log in an infinite loop.");
      continue;
    } else {
      connectFailCount = 0;
    }

    // dbg("before ", connectionHandle, hostName, portName, fileCount, seqFiles, perSeqMaxHash, gfIdx, option);
    // handle_client(connectionHandle, hostName, portName, fileCount, seqFiles, perSeqMaxHash, gfIdx, option);
    pool.push_task(handle_client, connectionHandle, hostName, portName, fileCount, seqFiles, perSeqMaxHash, gfIdx,
                   option);
  }

  pool.wait_for_tasks();

  close(socketHandle);
  return 0;
}

}  // namespace cppbinding
