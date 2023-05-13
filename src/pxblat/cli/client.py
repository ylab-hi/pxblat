import typer

from .log import log
from pathlib import Path
from rich import print


# gfClient v. 37x1 - A client for the genomic finding program that produces a .psl file
# usage:
#    gfClient host port seqDir in.fa out.psl
# where
#    host is the name of the machine running the gfServer
#    port is the same port that you started the gfServer with
#    seqDir is the path of the .2bit or .nib files relative to the current dir
#        (note these are needed by the client as well as the server)
#    in.fa is a fasta format file.  May contain multiple records
#    out.psl is where to put the output
# options:
#    -t=type       Database type. Type is one of:
#                    dna - DNA sequence
#                    prot - protein sequence
#                    dnax - DNA sequence translated in six frames to protein
#                  The default is dna.
#    -q=type       Query type. Type is one of:
#                    dna - DNA sequence
#                    rna - RNA sequence
#                    prot - protein sequence
#                    dnax - DNA sequence translated in six frames to protein
#                    rnax - DNA sequence translated in three frames to protein
#    -prot         Synonymous with -t=prot -q=prot.
#    -dots=N       Output a dot every N query sequences.
#    -nohead       Suppresses 5-line psl header.
#    -minScore=N   Sets minimum score.  This is twice the matches minus the
#                  mismatches minus some sort of gap penalty.  Default is 30.
#    -minIdentity=N   Sets minimum sequence identity (in percent).  Default is
#                  90 for nucleotide searches, 25 for protein or translated
#                  protein searches.
#    -out=type     Controls output file format.  Type is one of:
#                    psl - Default.  Tab-separated format without actual sequence
#                    pslx - Tab-separated format with sequence
#                    axt - blastz-associated axt format
#                    maf - multiz-associated maf format
#                    sim4 - similar to sim4 format
#                    wublast - similar to wublast format
#                    blast - similar to NCBI blast format
#                    blast8- NCBI blast tabular format
#                    blast9 - NCBI blast tabular format with comments
#    -maxIntron=N   Sets maximum intron size. Default is 750000.
#    -genome=name  When using a dynamic gfServer, The genome name is used to
#                  find the data files relative to the dynamic gfServer root, named
#                  in the form $genome.2bit, $genome.untrans.gfidx, and $genome.trans.gfidx
#    -genomeDataDir=path
#                  When using a dynamic gfServer, this is the dynamic gfServer root directory
#                  that contained the genome data files.  Defaults to being the root directory.


def client(
    host: str = typer.Argument(help="The name of the machine running the gfServer"),
    port: int = typer.Argument(help="The same port that you started the gfServer with"),
    seqDir: Path = typer.Argument(
        help="The path of the .2bit or .nib files relative to the current dir"
    ),
    infasta: Path = typer.Argument(
        help="Fasta format file.  May contain multiple records"
    ),
    outpsl: Path = typer.Argument(help="where to put the output"),
    t: str = typer.Option(
        "dna",
        "--type",
        "-t",
        help="Database type. Type is one of: dna, prot, dnax",
    ),
    q: str = typer.Option(
        "dna",
        "--qtype",
        "-q",
        help="Query type. Type is one of: dna, rna, prot, dnax, rnax",
    ),
    prot: bool = typer.Option(False, "--prot", help="Synonymous with -t=prot -q=prot."),
    dots: int = typer.Option(0, "--dots", help="Output a dot every N query sequences."),
    nohead: bool = typer.Option(
        False, "--nohead", help="Suppresses 5-line psl header."
    ),
    minnScore: int = typer.Option(
        30,
        "--minScore",
        help="Sets minimum score.  This is twice the matches minus the mismatches minus some sort of gap penalty.  Default is 30.",
    ),
    minIdentity: int = typer.Option(
        90,
        "--minIdentity",
        help="Sets minimum sequence identity (in percent).  Default is 90 for nucleotide searches, 25 for protein or translated protein searches.",
    ),
    out: str = typer.Option(
        "psl",
        "--out",
        help="Controls output file format.  Type is one of: psl, pslx, axt, maf, sim4, wublast, blast, blast8, blast9",
    ),
    maxIntron: int = typer.Option(
        750000, "--maxIntron", help="Sets maximum intron size. Default is 750000."
    ),
    genome: str = typer.Option("", "--genome", help="dynamic"),
    genomeDataDir: str = typer.Option("", "--genomeDataDir", help="dynamic"),
):
    """A client for the genomic finding program that produces a .psl file"""

    print(
        f"{host=}, {port=}, {seqDir=}, {infasta=}, {outpsl=}, {t=}, {q=}, {prot=}, {dots=}, {nohead=}, {minnScore=}, {minIdentity=}, {out=}, {maxIntron=}, {genome=}, {genomeDataDir=}"
    )
