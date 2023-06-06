#pragma GCC diagnostic ignored "-Wwrite-strings"
#include "twoBitToFa.hpp"

#include <sstream>
#include <stdexcept>

#include "dbg.h"
/* twoBitToFa - Convert all or part of twoBit file to fasta. */
/* Copyright (C) 2013 The Regents of the University of California
 * See kent/LICENSE or http://genome.ucsc.edu/license/ for licensing information. */

namespace cppbinding {

// char *clSeq = NULL;     /* Command line sequence. */
// int clStart = 0;        /* Start from command line. */
// int clEnd = 0;          /* End from command line. */
// char *clSeqList = NULL; /* file containing list of seq names */
// bool noMask = FALSE;    /* convert seq to upper case */
// char *clBpt = NULL;     /* External index file. */
// char *clBed = NULL;     /* Bed file that specifies bounds of sequences. */
// bool clBedPos = FALSE;

// static struct optionSpec options[] = {
//     {"seq", OPTION_STRING},     {"seqList", OPTION_STRING},
//     {"start", OPTION_INT},      {"end", OPTION_INT},
//     {"noMask", OPTION_BOOLEAN}, {"bpt", OPTION_STRING},
//     {"bed", OPTION_STRING},     {"bedPos", OPTION_BOOLEAN},
//     {"udcDir", OPTION_STRING},  {NULL, 0},
// };

void outputOne(struct twoBitFile *tbf, char *seqSpec, FILE *f, int start, int end, bool noMask)
/* Output sequence. */
{
  struct dnaSeq *seq = twoBitReadSeqFrag(tbf, seqSpec, start, end);
  if (noMask) toUpperN(seq->dna, seq->size);
  faWriteNext(f, seq->name, seq->dna, seq->size);
  dnaSeqFree(&seq);
}

static void processAllSeqs(struct twoBitFile *tbf, FILE *outFile, bool noMask)
/* get all sequences in a file */
{
  struct twoBitIndex *index;
  for (index = tbf->indexList; index != NULL; index = index->next) outputOne(tbf, index->name, outFile, 0, 0, noMask);
}

static void processSeqSpecs(struct twoBitFile *tbf, struct twoBitSeqSpec *tbss, FILE *outFile, bool noMask)
/* process list of twoBitSeqSpec objects */
{
  struct twoBitSeqSpec *s;
  for (s = tbss; s != NULL; s = s->next) outputOne(tbf, s->name, outFile, s->start, s->end, noMask);
}

struct dnaSeq *twoBitAndBedToSeq(struct twoBitFile *tbf, struct bed *bed)
/* Get sequence defined by bed.  Exclude introns. */
{
  struct dnaSeq *seq;
  if (bed->blockCount <= 1) {
    seq = twoBitReadSeqFrag(tbf, bed->chrom, bed->chromStart, bed->chromEnd);
    freeMem(seq->name);
    seq->name = cloneString(bed->name);
  } else {
    int totalBlockSize = bedTotalBlockSize(bed);
    // AllocVar(seq);
    dbg(sizeof(*seq));
    seq = (dnaSeq *)needMem(sizeof(*seq));

    seq->name = cloneString(bed->name);
    dbg(totalBlockSize + 1);
    seq->dna = (DNA *)needMem(totalBlockSize + 1);
    seq->size = totalBlockSize;
    int i;
    int seqOffset = 0;
    for (i = 0; i < bed->blockCount; ++i) {
      int exonSize = bed->blockSizes[i];
      int exonStart = bed->chromStart + bed->chromStarts[i];
      struct dnaSeq *exon = twoBitReadSeqFrag(tbf, bed->chrom, exonStart, exonStart + exonSize);
      memcpy(seq->dna + seqOffset, exon->dna, exonSize);
      seqOffset += exonSize;
      dnaSeqFree(&exon);
    }
  }
  if (bed->strand[0] == '-') reverseComplement(seq->dna, seq->size);
  return seq;
}

static void processSeqsFromBed(struct twoBitFile *tbf, char *bedFileName, FILE *outFile, bool clBedPos, bool noMask)
/* Get sequences defined by beds.  Exclude introns. */
{
  struct bed *bed, *bedList = bedLoadAll(bedFileName);
  for (bed = bedList; bed != NULL; bed = bed->next) {
    struct dnaSeq *seq = twoBitAndBedToSeq(tbf, bed);
    char *seqName = NULL;
    if (clBedPos) {
      char buf[1024];
      safef(buf, 1024, "%s:%d-%d", bed->chrom, bed->chromStart, bed->chromEnd);
      seqName = buf;
    } else
      seqName = seq->name;
    if (noMask) toUpperN(seq->dna, seq->size);
    faWriteNext(outFile, seqName, seq->dna, seq->size);
    dnaSeqFree(&seq);
  }
}

void twoBitToFa(std::string cppinName, std::string cppoutName, TwoBitToFaOption option)
/* twoBitToFa - Convert all or part of twoBit file to fasta. */

{
  // char *clSeq = NULL;     /* Command line sequence. */
  // int clStart = 0;        /* Start from command line. */
  // int clEnd = 0;          /* End from command line. */
  // char *clSeqList = NULL; /* file containing list of seq names */
  // bool noMask = FALSE;    /* convert seq to upper case */
  // char *clBpt = NULL;     /* External index file. */
  // char *clBed = NULL;     /* Bed file that specifies bounds of sequences. */
  // bool clBedPos = FALSE;

  auto inName = cppinName.data();
  auto outName = cppoutName.data();
  char *clSeq = option.seq.empty() ? NULL : option.seq.data();
  auto clStart = option.start;
  auto clEnd = option.end;
  char *clSeqList = option.seqList.empty() ? NULL : option.seqList.data();
  auto noMask = option.noMask;
  char *clBpt = option.bpt.empty() ? NULL : option.bpt.data();
  char *clBed = option.bed.empty() ? NULL : option.bed.data();
  auto clBedPos = option.bedPos;

  dnaUtilOpen();

  struct twoBitFile *tbf{};
  FILE *outFile = mustOpen(outName, "w");
  struct twoBitSpec *tbs{};

  if (clSeq != NULL) {
    char seqSpec[2 * PATH_LEN];
    if (clEnd > clStart)
      safef(seqSpec, sizeof(seqSpec), "%s:%s:%d-%d", inName, clSeq, clStart, clEnd);
    else
      safef(seqSpec, sizeof(seqSpec), "%s:%s", inName, clSeq);
    tbs = twoBitSpecNew(seqSpec);
  } else if (clSeqList != NULL)
    tbs = twoBitSpecNewFile(inName, clSeqList);
  else
    tbs = twoBitSpecNew(inName);

  if (tbs == NULL) errAbort("%s is not a twoBit file", inName);

  if (tbs->seqs != NULL && clBpt != NULL)
    tbf = twoBitOpenExternalBptIndex(tbs->fileName, clBpt);
  else
    tbf = twoBitOpen(tbs->fileName);
  if (clBed != NULL) {
    processSeqsFromBed(tbf, clBed, outFile, clBedPos, noMask);
  } else {
    if (tbs->seqs == NULL)
      processAllSeqs(tbf, outFile, noMask);
    else
      processSeqSpecs(tbf, tbs->seqs, outFile, noMask);
  }
  twoBitSpecFree(&tbs);
  carefulClose(&outFile);
  twoBitClose(&tbf);
}

TwoBitToFaOption &TwoBitToFaOption::withSeq(std::string const &seq_) {
  seq = seq_;
  return *this;
}

TwoBitToFaOption &TwoBitToFaOption::withStart(int start_) {
  start = start_;
  return *this;
}

TwoBitToFaOption &TwoBitToFaOption::withEnd(int end_) {
  end = end_;
  return *this;
}

TwoBitToFaOption &TwoBitToFaOption::withSeqList(std::string const &seqList_) {
  seqList = seqList_;
  return *this;
}

TwoBitToFaOption &TwoBitToFaOption::withNoMask(bool noMask_) {
  noMask = noMask_;
  return *this;
}

TwoBitToFaOption &TwoBitToFaOption::withBpt(std::string const &bpt_) {
  bpt = bpt_;
  return *this;
}

TwoBitToFaOption &TwoBitToFaOption::withBed(std::string const &bed_) {
  bed = bed_;
  return *this;
}

TwoBitToFaOption &TwoBitToFaOption::withBedPos(bool bedPos_) {
  bedPos = bedPos_;
  return *this;
}

TwoBitToFaOption &TwoBitToFaOption::withUdcDir(std::string const &udcDir_) {
  udcDir = udcDir_;
  return *this;
}

TwoBitToFaOption &TwoBitToFaOption::build() {
  //   if (argc != 3) usage();

  //   if (clBedPos && !clBed) errAbort("the -bedPos option requires the -bed option");
  //   if (clBed != NULL) {
  //     if (clSeqList != NULL) errAbort("Can only have seqList or bed options, not both.");
  //     if (clSeq != NULL) errAbort("Can only have seq or bed options, not both.");
  //   }
  //   if ((clStart > clEnd) && (clSeq == NULL)) errAbort("must specify -seq with -start and -end");
  //   if ((clSeq != NULL) && (clSeqList != NULL)) errAbort("can't specify both -seq and -seqList");

  udcSetDefaultDir(udcDir.data());

  if (bedPos && bed.empty())
    // errAbort("the -bedPos option requires the -bed option");
    throw std::runtime_error("the -bedPos option requires the -bed option");

  if (!bed.empty()) {
    if (!seqList.empty()) throw std::runtime_error("Can only have seqList or bed options, not both");
    if (!seq.empty()) throw std::runtime_error("Can only have seq or bed options, not both");
  }

  if (start > end && seq.empty()) throw std::runtime_error("must sepcify -seq with -start and -end");
  if (!seq.empty() && !seqList.empty()) throw std::runtime_error("Can only have seq or bed options, not both");

  return *this;
}

std::string TwoBitToFaOption::to_string() const {
  std::ostringstream ret{};
  ret << "TwoBitToFaOption(";
  ret << "seq: " << seq << ", ";
  ret << "start: " << start << ", ";
  ret << "end: " << end << ", ";
  ret << "seqList: " << seqList << ", ";
  ret << "noMask: " << noMask << ", ";
  ret << "bpt: " << bpt << ", ";
  ret << "bed: " << bed << ", ";
  ret << "bedPos: " << bedPos << ", ";
  ret << "udcDir: " << udcDir << ", ";
  ret << ")";

  return ret.str();
}

std::ostream &operator<<(std::ostream &os, TwoBitToFaOption const &option) {
  os << option.to_string();
  return os;
}

}  // namespace cppbinding
