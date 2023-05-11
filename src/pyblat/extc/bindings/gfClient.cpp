#include "gfClient.hpp"

#include <sstream>

#pragma GCC diagnostic ignored "-Wwrite-strings"

/* gfClient - A client for the genomic finding program that produces a .psl file. */
/* Copyright 2001-2003 Jim Kent.  All rights reserved. */

namespace cppbinding {

std::string read_inmem_file(FILE *file) {
  std::ostringstream ret_str{};
  fseek(file, 0, SEEK_SET);

  char line[1024];

  while (fgets(line, sizeof(line), file) != NULL) {
    ret_str << line;
  }
  return ret_str.str();
}

std::string pygfClient(gfClientOption &option)
/* gfClient - A client for the genomic finding program that produces a .psl file. */
{
  int enterMainTime = 0;

  auto hostName = option.hostName.data();
  auto portName = option.portName.data();

  auto minIdentity = option.minIdentity;
  auto dots = option.dots;
  auto minScore = option.minScore;
  auto outputFormat = option.outputFormat.data();
  auto isDynamic = option.isDynamic;

  auto qTypeName = option.qType.data();
  auto tTypeName = option.tType.data();
  auto inName = option.inName.data();
  auto outName = option.outName.data();
  auto tSeqDir = option.tSeqDir.data();

  boolean nohead = option.nohead ? TRUE : FALSE;

  auto genome = option.genome.empty() ? NULL : option.genome.data();
  auto genomeDataDir = option.genomeDataDir.empty() ? NULL : option.genomeDataDir.data();

  char buffer[1024];
  FILE *out = fmemopen(buffer, strlen(buffer), "w+");
  if (out == NULL) {
    errAbort("Can't open in memory file %s", outName);
  }

  struct gfOutput *gvo;

  struct lineFile *lf = lineFileOpen(inName, TRUE);
  static bioSeq seq;
  // FILE *out = mustOpen(outName, "w");
  enum gfType qType = gfTypeFromName(qTypeName);
  enum gfType tType = gfTypeFromName(tTypeName);
  int dotMod = 0;
  char databaseName[256];
  struct hash *tFileCache = gfFileCacheNew();

  boolean gotConnection = FALSE;

  snprintf(databaseName, sizeof(databaseName), "%s:%s", hostName, portName);

  gvo = gfOutputAny(outputFormat, round(minIdentity * 10), qType == gftProt, tType == gftProt, nohead, databaseName, 23,
                    3.0e9, minIdentity, out);
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

  // if (out != stdout) printf("Output is in %s\n", outName);
  gfFileCacheFree(&tFileCache);
  return read_inmem_file(out);
}

gfClientOption &gfClientOption::build() {
  // char *hostName, char *portName, char *tSeqDir, char *inName, char *outName, char *tTypeName, char *qTypeName
  if (tType == "prot" || tType == "dnax" || tType == "rnax") minIdentity = 25;

  if (!genomeDataDir.empty() && genome.empty()) errAbort("-genomeDataDir requires the -genome option");
  if (!genome.empty() && genomeDataDir.empty()) genomeDataDir = ".";
  if (!genomeDataDir.empty()) isDynamic = true;

  return *this;
}

gfClientOption &gfClientOption::withHost(const std::string &hostName_) {
  hostName = hostName_;
  return *this;
}

gfClientOption &gfClientOption::withPort(const std::string &portName_) {
  portName = portName_;
  return *this;
}

gfClientOption &gfClientOption::withTType(const std::string &tType_) {
  tType = tType_;
  return *this;
}

gfClientOption &gfClientOption::withQType(const std::string &qType_) {
  qType = qType_;
  return *this;
}

gfClientOption &gfClientOption::withDots(int dots_) {
  dots = dots_;
  return *this;
}

gfClientOption &gfClientOption::withNohead(bool nohead_) {
  nohead = nohead_;
  return *this;
}

gfClientOption &gfClientOption::withMinScore(int minScore_) {
  minScore = minScore_;
  return *this;
}

gfClientOption &gfClientOption::withMinIdentity(double minIdentity_) {
  minIdentity = minIdentity_;
  return *this;
}

gfClientOption &gfClientOption::withOutputFormat(const std::string &outputFormat_) {
  outputFormat = outputFormat_;
  return *this;
}

gfClientOption &gfClientOption::withMaxIntron(long maxIntron_) {
  maxIntron = maxIntron_;
  return *this;
}

gfClientOption &gfClientOption::withGenome(const std::string &genome_) {
  genome = genome_;
  return *this;
}

gfClientOption &gfClientOption::withGenomeDataDir(const std::string &genomeDataDir_) {
  genomeDataDir = genomeDataDir_;
  return *this;
}

gfClientOption &gfClientOption::withIsDynamic(bool isDynamic_) {
  isDynamic = isDynamic_;
  return *this;
}

gfClientOption &gfClientOption::withTSeqDir(const std::string &tSeqDir_) {
  tSeqDir = tSeqDir_;
  return *this;
}

gfClientOption &gfClientOption::withInName(const std::string &inName_) {
  inName = inName_;
  return *this;
}

gfClientOption &gfClientOption::withOutName(const std::string &outName_) {
  outName = outName_;
  return *this;
}

std::string gfClientOption::to_string() const {
  std::ostringstream ret{};

  ret << "gfClientOption(";
  ret << "hostName=" << hostName;
  ret << ", portName=" << portName;
  ret << ", tType=" << tType;
  ret << ", qType=" << qType;
  ret << ", dots=" << dots;
  ret << ", nohead=" << std::boolalpha << nohead;
  ret << ", minScore=" << minScore;
  ret << ", minIdentity=" << minIdentity;
  ret << ", outputFormat=" << outputFormat;
  ret << ", maxIntron=" << maxIntron;
  ret << ", genome=" << genome;
  ret << ", genomeDataDir=" << genomeDataDir;
  ret << ", isDynamic=" << std::boolalpha << isDynamic;
  ret << ", tSeqDir=" << tSeqDir;
  ret << ", inName=" << inName;
  ret << ", outName=" << outName;
  ret << ")";

  return ret.str();
}
}  // namespace cppbinding
