#include "gfClient2.hpp"

#include "gfClient.hpp"

int dots = 0;
int minScore = 30;
double minIdentity = 90;
char *outputFormat = "psl";
char *qType = "dna";
char *tType = "dna";
char *genome = NULL;
char *genomeDataDir = NULL;
boolean isDynamic = FALSE;
boolean nohead = FALSE;
long enterMainTime = 0;

namespace cppbinding2 {
// int main(int argc, char *argv[])
// /* Process command line. */
// {
//   optionInit(&argc, argv, optionSpecs);
//   if (argc != 6) usage();
//   if (optionExists("prot")) qType = tType = "prot";
//   qType = optionVal("q", qType);
//   tType = optionVal("t", tType);
//   if (sameWord(tType, "prot") || sameWord(tType, "dnax") || sameWord(tType, "rnax")) minIdentity = 25;
//   minIdentity = optionFloat("minIdentity", minIdentity);
//   minScore = optionInt("minScore", minScore);
//   dots = optionInt("dots", 0);
//   outputFormat = optionVal("out", outputFormat);
//   genome = optionVal("genome", NULL);
//   genomeDataDir = optionVal("genomeDataDir", NULL);
//   if ((genomeDataDir != NULL) && (genome == NULL)) errAbort("-genomeDataDir requires the -genome option");
//   if ((genome != NULL) && (genomeDataDir == NULL)) genomeDataDir = ".";
//   if (genomeDataDir != NULL) isDynamic = TRUE;

//   enterMainTime = clock1000();
//   /* set global for fuzzy find functions */
//   setFfIntronMax(optionInt("maxIntron", ffIntronMaxDefault));
//   gfClient(argv[1], argv[2], argv[3], argv[4], argv[5], tType, qType);
//   return 0;
// }

struct gfOutput *gvo;

void gfClient(char *hostName, char *portName, char *tSeqDir, char *inName, char *outName, char *tTypeName,
              char *qTypeName)
/* gfClient - A client for the genomic finding program that produces a .psl file. */
{
  struct lineFile *lf = lineFileOpen(inName, TRUE);
  static bioSeq seq;
  FILE *out = mustOpen(outName, "w");
  enum gfType qType = gfTypeFromName(qTypeName);
  enum gfType tType = gfTypeFromName(tTypeName);
  int dotMod = 0;
  char databaseName[256];
  struct hash *tFileCache = gfFileCacheNew();
  boolean gotConnection = FALSE;

  printf("hostName %s portName %s tSeqDir %s, inName %s, outName %s, tType %s qtype %s \n", hostName, portName, tSeqDir,
         inName, outName, tTypeName, qTypeName);

  // ffIntronMax enterMainTime
  printf(
      "dots %d minScore %d minIdentity %f outputFormat %s genome %s genomeDataDir %s isDynamic %d ffIntronMax%d "
      "enterMainTime %ld\n",
      dots, minScore, minIdentity, outputFormat, genome, genomeDataDir, isDynamic, ffIntronMax, enterMainTime);

  if (genome != NULL) {
    printf("genome %s\n", genome);
  }

  if (genomeDataDir != NULL) {
    printf("genomeDataDir %s\n", genomeDataDir);
  }

  snprintf(databaseName, sizeof(databaseName), "%s:%s", hostName, portName);

  gvo = gfOutputAny(outputFormat, cround(minIdentity * 10), qType == gftProt, tType == gftProt, nohead, databaseName,
                    23, 3.0e9, minIdentity, out);
  gfOutputHead(gvo, out);
  struct errCatch *errCatch = errCatchNew();
  if (errCatchStart(errCatch)) {
    struct gfConnection *conn = gfConnect(hostName, portName, genome, genomeDataDir);
    gotConnection = TRUE;
    while (faSomeSpeedReadNext(lf, &seq.dna, &seq.size, &seq.name, qType != gftProt)) {
      if (dots != 0) {
        if (++dotMod >= dots) {
          dotMod = 0;
          verboseDot();
        }
      }
      if (qType == gftProt && (tType == gftDnaX || tType == gftRnaX)) {
        gvo->reportTargetStrand = TRUE;
        gfAlignTrans(conn, tSeqDir, &seq, minScore, tFileCache, gvo);
      } else if ((qType == gftRnaX || qType == gftDnaX) && (tType == gftDnaX || tType == gftRnaX)) {
        gvo->reportTargetStrand = TRUE;
        gfAlignTransTrans(conn, tSeqDir, &seq, FALSE, minScore, tFileCache, gvo, qType == gftRnaX);
        if (qType == gftDnaX) {
          reverseComplement(seq.dna, seq.size);
          gfAlignTransTrans(conn, tSeqDir, &seq, TRUE, minScore, tFileCache, gvo, FALSE);
        }
      } else if ((tType == gftDna || tType == gftRna) && (qType == gftDna || qType == gftRna)) {
        gfAlignStrand(conn, tSeqDir, &seq, FALSE, minScore, tFileCache, gvo);
        reverseComplement(seq.dna, seq.size);
        gfAlignStrand(conn, tSeqDir, &seq, TRUE, minScore, tFileCache, gvo);
      } else {
        errAbort("Comparisons between %s queries and %s databases not yet supported", qTypeName, tTypeName);
      }
      gfOutputQuery(gvo, out);
    }
    gfDisconnect(&conn);
  } /*	if (errCatchStart(errCatch))	*/
  errCatchEnd(errCatch);
  if (errCatch->gotError) {
    if (isNotEmpty(errCatch->message->string)) warn("# error: %s", errCatch->message->string);
    if (gotConnection && isDynamic) {
      long et = clock1000() - enterMainTime;
      if (et > NET_TIMEOUT_MS)
        errAbort(
            "the dynamic server at %s:%s is taking too long to respond,\nperhaps overloaded at this time, try again "
            "later",
            hostName, portName);
      else if (et < NET_QUICKEXIT_MS)
        errAbort(
            "the dynamic server at %s:%s is returning an error immediately,\nperhaps overloaded at this time, try "
            "again later",
            hostName, portName);
      else
        errAbort("the dynamic server at %s:%s is returning an error at this time,\ntry again later", hostName,
                 portName);
    } else
      errAbort("gfClient error exit");
  }
  errCatchFree(&errCatch);

  if (out != stdout) printf("Output is in %s\n", outName);
  gfFileCacheFree(&tFileCache);
}

std::string pygfClient2(gfClientOption &option) {
  auto hostName = option.hostName.data();
  auto portName = option.portName.data();
  auto tSeqDir = option.SeqDir.data();

  auto inName = option.inName.data();
  auto outName = option.outName.data();

  // auto tTypeName = option.tType.data();
  // auto qTypeName = option.qType.data();

  minScore = option.minScore;
  minIdentity = option.minIdentity;
  outputFormat = option.outputFormat.data();
  qType = option.qType.data();
  tType = option.tType.data();

  genome = option.genome.empty() ? NULL : option.genome.data();
  genomeDataDir = option.genomeDataDir.empty() ? NULL : option.genomeDataDir.data();

  dots = option.dots;
  isDynamic = option.isDynamic;
  nohead = option.nohead ? TRUE : FALSE;

  enterMainTime = clock1000();
  setFfIntronMax(option.maxIntron);

  gfClient(hostName, portName, tSeqDir, inName, outName, qType, tType);

  return "";
}

}  // namespace cppbinding2
