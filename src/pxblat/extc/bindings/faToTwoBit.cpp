#pragma GCC diagnostic ignored "-Wwrite-strings"

#include "faToTwoBit.hpp"

#include <stdexcept>

namespace cppbinding {

void unknownToN(char *s, int size)
/* Convert non ACGT characters to N. */
{
  char c;
  int i;
  for (i = 0; i < size; ++i) {
    c = s[i];
    if (ntChars[(int)c] == 0) {
      if (isupper(c))
        s[i] = 'N';
      else
        s[i] = 'n';
    }
  }
}

//-1 errAbort("Duplicate sequence name %s", seq.name);
int faToTwoBit(std::vector<std::string> &inFiles, std::string &outFile, bool noMask, bool stripVersion, bool ignoreDups,
               bool useLong)

/* Convert inFiles in fasta format to outfile in 2 bit
 * format. */
{
  dnaUtilOpen();

  struct twoBit *twoBitList = NULL, *twoBit;
  // int i;
  struct hash *uniqHash = newHash(18);
  FILE *f;

  for (auto &fileName : inFiles) {
    struct lineFile *lf = lineFileOpen(fileName.data(), TRUE);
    struct dnaSeq seq;
    ZeroVar(&seq);
    while (faMixedSpeedReadNext(lf, &seq.dna, &seq.size, &seq.name)) {
      if (seq.size == 0) {
        warn("Skipping item %s which has no sequence.\n", seq.name);
        continue;
      }

      /* strip off version number */
      if (stripVersion) {
        char *sp = NULL;
        sp = strchr(seq.name, '.');
        if (sp != NULL) *sp = '\0';
      }

      if (hashLookup(uniqHash, seq.name)) {
        if (!ignoreDups)
          // errAbort("Duplicate sequence name %s", seq.name);
          throw std::runtime_error("Duplicate sequence name " + std::string(seq.name));
        // return -1;

        else
          continue;
      }
      hashAdd(uniqHash, seq.name, NULL);
      if (noMask)
        faToDna(seq.dna, seq.size);
      else
        unknownToN(seq.dna, seq.size);
      twoBit = twoBitFromDnaSeq(&seq, !noMask);
      slAddHead(&twoBitList, twoBit);
    }
    lineFileClose(&lf);
  }

  slReverse(&twoBitList);
  f = mustOpen(outFile.data(), "wb");
  twoBitWriteHeaderExt(twoBitList, f, useLong);
  for (twoBit = twoBitList; twoBit != NULL; twoBit = twoBit->next) {
    twoBitWriteOne(twoBit, f);
  }
  carefulClose(&f);

  return 0;
}
}  // namespace cppbinding
