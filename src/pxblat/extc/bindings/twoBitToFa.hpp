#ifndef TWO_BIT_TO_FA_HPP
#define TWO_BIT_TO_FA_HPP
#include <string>

#include "bPlusTree.h"
#include "basicBed.h"
#include "common.h"
#include "dnaseq.h"
#include "fa.h"
#include "hash.h"
#include "linefile.h"
#include "options.h"
#include "twoBit.h"
#include "udc.h"

namespace cppbinding {

// -seq=name       Restrict this to just one sequence.\n"
//       "   -start=X        Start at given position in sequence (zero-based).\n"
//       "   -end=X          End at given position in sequence (non-inclusive).\n"
//       "   -seqList=file   File containing list of the desired sequence names \n"
//       "                   in the format seqSpec[:start-end], e.g. chr1 or chr1:0-189\n"
//       "                   where coordinates are half-open zero-based, i.e. [start,end).\n"
//       "   -noMask         Convert sequence to all upper case.\n"
//       "   -bpt=index.bpt  Use bpt index instead of built-in one.\n"
//       "   -bed=input.bed  Grab sequences specified by input.bed. Will exclude introns.\n"
//       "   -bedPos         With -bed, use chrom:start-end as the fasta ID in output.fa.\n"
//       "   -udcDir=/dir/to/cache  Place to put cache for remote bigBed/bigWigs.\n"
//       "\n"

// char *clSeq = NULL;     /* Command line sequence. */
// int clStart = 0;        /* Start from command line. */
// int clEnd = 0;          /* End from command line. */
// char *clSeqList = NULL; /* file containing list of seq names */
// bool noMask = FALSE;    /* convert seq to upper case */
// char *clBpt = NULL;     /* External index file. */
// char *clBed = NULL;     /* Bed file that specifies bounds of sequences. */
// bool clBedPos = FALSE;

struct TwoBitToFaOption {
  std::string seq{};      //        Restrict this to just one sequence.\n"
  int start{};            //        Start at given position in sequence (zero-based).\n"
  int end{};              //        End at given position in sequence (non-inclusive).\n"
  std::string seqList{};  //        File containing list of the desired sequence names \n"
                          //        in the format seqSpec[:start-end], e.g. chr1 or chr1:0-189\n"
                          //        where coordinates are half-open zero-based, i.e. [start,end).\n"
  bool noMask{};          //        Convert sequence to all upper case.\n"
  std::string bpt{};      //        -bpt=index.bpt  Use bpt index instead of built-in one.\n"
  std::string bed{};      //        -bed=input.bed  Grab sequences specified by input.bed. Will exclude introns.\n"
  bool bedPos{};          //        With -bed, use chrom:start-end as the fasta ID in output.fa.\n"
  std::string udcDir{udcDefaultDir()};  //        Place to put cache for remote bigBed/bigWigs.\n"

  TwoBitToFaOption() = default;

  TwoBitToFaOption& withSeq(std::string const& seq_);
  TwoBitToFaOption& withStart(int start_);
  TwoBitToFaOption& withEnd(int end_);
  TwoBitToFaOption& withSeqList(std::string const& seqList_);
  TwoBitToFaOption& withNoMask(bool noMask_);
  TwoBitToFaOption& withBpt(std::string const& bpt_);
  TwoBitToFaOption& withBed(std::string const& bed_);
  TwoBitToFaOption& withBedPos(bool bedPos_);
  TwoBitToFaOption& withUdcDir(std::string const& udcDir_);
  TwoBitToFaOption& build();

  std::string to_string() const;
  friend std::ostream& operator<<(std::ostream& os, TwoBitToFaOption const& option);
};

void twoBitToFa(std::string cppinName, std::string cppoutName, TwoBitToFaOption option);

}  // namespace cppbinding

#endif  // !#ifndef TWO_BIT_TO_FA_HPP
