from pathlib import Path

import typer

# twoBitToFa - Convert all or part of .2bit file to fasta
# usage:
#    twoBitToFa input.2bit output.fa
# options:
#    -seq=name       Restrict this to just one sequence.
#    -start=X        Start at given position in sequence (zero-based).
#    -end=X          End at given position in sequence (non-inclusive).
#    -seqList=file   File containing list of the desired sequence names
#                    in the format seqSpec[:start-end], e.g. chr1 or chr1:0-189
#                    where coordinates are half-open zero-based, i.e. [start,end).
#    -noMask         Convert sequence to all upper case.
#    -bpt=index.bpt  Use bpt index instead of built-in one.
#    -bed=input.bed  Grab sequences specified by input.bed. Will exclude introns.
#    -bedPos         With -bed, use chrom:start-end as the fasta ID in output.fa.
#    -udcDir=/dir/to/cache  Place to put cache for remote bigBed/bigWigs.
# Sequence and range may also be specified as part of the input
# file name using the syntax:
#       /path/input.2bit:name
#    or
#       /path/input.2bit:name:start-end


def twoBitToFa(
    input2bit: Path = typer.Argument(
        ...,
        exists=True,
        dir_okay=False,
        readable=True,
        metavar="input.2bit",
        help="The input 2bit file",
    ),
    outputfa: Path = typer.Argument(
        ...,
        dir_okay=False,
        writable=True,
        show_default=False,
        metavar="out.fa",
        help="The output fasta file",
    ),
    # seq: str = typer.Option(),
):
    raise NotImplementedError
