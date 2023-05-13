/* patSpace - a homology finding algorithm that occurs mostly in
 * pattern space (as opposed to offset space).
 *
 * This file is copyright 2000 Jim Kent, but license is hereby
 * granted for all use - public, private or commercial. */


#ifndef PATSPACE_H
#define PATSPACE_H

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

#ifndef DNASEQ_H
#include "dnaseq.h"
#endif

struct patSpace *makePatSpace(
    struct dnaSeq **seqArray,       /* Array of sequence lists. */
    int seqArrayCount,              /* Size of above array. */
    int seedSize,	            /* Alignment seed size - 10 or 11. Must match oocFileName */
    char *oocFileName,              /* File with tiles to filter out, may be NULL. */
    int minMatch,                   /* Minimum # of matching tiles.  4 is good. */
    int maxGap                      /* Maximum gap size - 32k is good for
                                       cDNA (introns), 500 is good for DNA assembly. */
    );
/* Allocate a pattern space and fill from sequences.  (Each element of
   seqArray is a list of sequences. */

void freePatSpace(struct patSpace **pPatSpace);
/* Free up a pattern space. */

struct patClump
/* This holds pattern space output - a list of homologous clumps. */
    {
    struct patClump *next;     /* Link to next in list. */
    int bacIx;                 /* Index of .fa file where hit occurs. */
    int seqIx;                 /* Index of contig where hit occurs. */
    struct dnaSeq *seq;        /* Sequence in which hit occurs. */
    int start;                 /* Start offset within sequence. */
    int size;                  /* Size of block within sequence. */
    };

struct patClump *patSpaceFindOne(struct patSpace *ps, DNA *dna, int dnaSize);
/* Find occurrences of DNA in patSpace. The resulting list can be
 * freed with slFreeList. */


#ifdef __cplusplus
}
#endif  // __cplusplus



#endif /* PATSPACE_H */
