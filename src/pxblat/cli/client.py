from pathlib import Path

import typer

from pxblat.extc import pygfClient
from pxblat.server import create_client_option

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
#                  When using a dynamic gfServer, this is the dynamic gfServer root directory
#                  that contained the genome data files.  Defaults to being the root directory.


default_option = create_client_option()


def client(
    host: str = typer.Argument(
        ...,
        help="The name of the machine running the gfServer",
    ),
    port: int = typer.Argument(
        ...,
        help="The same port that you started the gfServer with",
    ),
    seqdir: Path = typer.Argument(
        ...,
        dir_okay=True,
        help="The path of the .2bit or .nib files relative to the current dir",
    ),
    infasta: Path = typer.Argument(
        ...,
        help="Fasta format file.  May contain multiple records",
    ),
    outpsl: Path = typer.Argument(..., help="where to put the output"),
    tType: str = typer.Option(
        default_option.tType,
        "--type",
        "-t",
        help="Database type. Type is one of: dna, prot, dnax",
    ),
    qType: str = typer.Option(
        default_option.qType,
        "--qtype",
        "-q",
        help="Query type. Type is one of: dna, rna, prot, dnax, rnax",
    ),
    prot: bool = typer.Option(False, "--prot", help="Synonymous with -t=prot -q=prot."),
    dots: int = typer.Option(
        default_option.dots,
        "--dots",
        help="Output a dot every N query sequences.",
    ),
    nohead: bool = typer.Option(
        default_option.nohead,
        "--nohead",
        help="Suppresses 5-line psl header.",
    ),
    minnScore: int = typer.Option(
        default_option.minScore,
        "--minScore",
        help="Sets minimum score.  This is twice the matches minus the mismatches minus some sort of gap penalty.  Default is 30.",
    ),
    minIdentity: int = typer.Option(
        default_option.minIdentity,
        "--minIdentity",
        help="Sets minimum sequence identity (in percent).  Default is 90 for nucleotide searches, 25 for protein or translated protein searches.",
    ),
    out: str = typer.Option(
        default_option.outputFormat,
        "--out",
        help="Controls output file format.  Type is one of: psl, pslx, axt, maf, sim4, wublast, blast, blast8, blast9",
    ),
    maxIntron: int = typer.Option(
        default_option.maxIntron,
        "--maxIntron",
        help="Sets maximum intron size. Default is 750000.",
    ),
    genome: str = typer.Option(default_option.genome, "--genome", help="dynamic"),
    genomeDataDir: str = typer.Option(
        default_option.genomeDataDir,
        "--genomeDataDir",
        help="dynamic",
    ),
):
    """A client for the genomic finding program that produces a .psl file."""
    if prot:
        tType = "prot"
        qType = "prot"

    client_option = (
        create_client_option()
        .withHost(host)
        .withPort(str(port))
        .withSeqDir(seqdir.as_posix())
        .withInName(infasta.as_posix())
        .withOutName(outpsl.as_posix())
        .withTType(tType)
        .withQType(qType)
        .withDots(dots)
        .withNohead(nohead)
        .withMinScore(minnScore)
        .withMinIdentity(minIdentity)
        .withOutputFormat(out)
        .withMaxIntron(maxIntron)
        .withGenome(genome)
        .withGenomeDataDir(genomeDataDir)
        .build()
    )

    pygfClient(client_option)
