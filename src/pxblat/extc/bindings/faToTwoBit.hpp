#ifndef CFA_TO_TWO_BIT_H
#define CFA_TO_TWO_BIT_H

#include <algorithm>
using std::max;
using std::min;

#include <string>
#include <vector>

#include "common.h"
#include "dnaseq.h"
#include "dnautil.h"
#include "fa.h"
#include "hash.h"
#include "linefile.h"
#include "options.h"
#include "twoBit.h"

namespace cppbinding {
// "faToTwoBit - Convert DNA from fasta to 2bit format\n"
// "usage:\n"
// "   faToTwoBit in.fa [in2.fa in3.fa ...] out.2bit\n"
// "options:\n"
// "   -long          use 64-bit offsets for index.   Allow for twoBit to "
// "contain more than 4Gb of sequence. \n"
// "                  NOT COMPATIBLE WITH OLDER CODE.\n"
// "   -noMask        Ignore lower-case masking in fa file.\n"
// "   -stripVersion  Strip off version number after '.' for GenBank "
// "accessions.\n"
// "   -ignoreDups    Convert first sequence only if there are duplicate "
// "sequence\n"
// "                  names.  Use 'twoBitDup' to find duplicate sequences.");
int faToTwoBit(std::vector<std::string> &inFiles, std::string &outFile, bool noMask = false, bool stripVersion = false,
               bool ignoreDups = false, bool useLong = false);

void unknownToN(char *s, int size);

}  // namespace cppbinding

#endif  // CFA_TO_TWO_BIT_H
