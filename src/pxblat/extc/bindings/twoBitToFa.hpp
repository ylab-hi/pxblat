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

// char *clSeq = NULL;     /* Command line sequence. */
// int clStart = 0;        /* Start from command line. */
// int clEnd = 0;          /* End from command line. */
// char *clSeqList = NULL; /* file containing list of seq names */
// bool noMask = FALSE;    /* convert seq to upper case */
// char *clBpt = NULL;     /* External index file. */
// char *clBed = NULL;     /* Bed file that specifies bounds of sequences. */
// bool clBedPos = FALSE;

struct TwoBitToFaOption {
  std::string seq{};
  int start{};
  int end{};
  std::string seqList{};
  bool noMask{};
  std::string clBpt{};
  std::string clBed{};
  bool clBedPos{};
  std::string udcDir{};
};

void twoBitToFa(std::string cppinName, std::string cppoutName);

}  // namespace cppbinding

#endif  // !#ifndef TWO_BIT_TO_FA_HPP
