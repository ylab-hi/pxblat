#ifndef CFA_TO_TWO_BIT_H
#define CFA_TO_TWO_BIT_H

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

void faToTwoBit(std::vector<std::string> &inFiles, std::string &outFile,
                bool noMask, bool stripVersion, bool ignoreDups, bool useLong);

void unknownToN(char *s, int size);

#endif  // CFA_TO_TWO_BIT_H
