from pathlib import Path

import typer

from pxblat import TwoBitToFaOption, two_bit_to_fa

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


# out: str = typer.Option(
#        default_option.outputFormat,
#        "--out",
#    ),


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
    seq: str = typer.Option("", "--seq", help="Restrict this to just one sequence."),
    start: int = typer.Option(
        0,
        "--start",
        help="Start at given position in sequence (zero-based).",
    ),
    end: int = typer.Option(
        0,
        "--end",
        help="End at given position in sequence (non-inclusive).",
    ),
    seqList: str = typer.Option(
        "",
        "--seqList",
        help="File containing list of the desired sequence names",
    ),
    noMask: bool = typer.Option(
        False,
        "--noMask",
        help="Convert sequence to all upper case.",
    ),
    bpt: str = typer.Option("", "--bpt", help="Use bpt index instead of built-in one."),
    bed: str = typer.Option("", "--bed", help="Grab sequences specified by input.bed."),
    bedPos: bool = typer.Option(
        False,
        "--bedPos",
        help="With -bed, use chrom:start-end as the fasta ID in output.fa.",
    ),
    udcDir: str = typer.Option(
        "",
        "--udcDir",
        help="Place to put cache for remote bigBed/bigWigs.",
    ),
):
    """Convert all or part of .2bit file to fasta."""
    if seqList and not Path(seqList).exists():
        msg = f"{seqList} does not exist"
        raise typer.BadParameter(msg)

    if bpt and not Path(bpt).exists():
        msg = f"{bpt} does not exist"
        raise typer.BadParameter(msg)

    if bed and not Path(bed).exists():
        msg = f"{bed} does not exist"
        raise typer.BadParameter(msg)

    if udcDir and not Path(udcDir).exists():
        msg = f"{udcDir} does not exist"
        raise typer.BadParameter(msg)

    option = TwoBitToFaOption()
    option.withSeq(seq).withStart(start).withEnd(end).withSeqList(seqList).withNoMask(
        noMask,
    ).withBpt(bpt).withBed(bed).withBedPos(bedPos).withUdcDir(udcDir).build()

    two_bit_to_fa(input2bit, outputfa, option=option)
