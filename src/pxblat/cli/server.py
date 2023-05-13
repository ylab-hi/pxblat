from pathlib import Path

import typer
from pxblat.server import create_server_option


# gfServer v 37x1 - Make a server to quickly find where DNA occurs in genome

#    To set up a server:
#       gfServer start host port file(s)
#       where the files are .2bit or .nib format files specified relative to the current directory

#    To remove a server:
#       gfServer stop host port

#    To query a server with DNA sequence:
#       gfServer query host port probe.fa

#    To query a server with protein sequence:
#       gfServer protQuery host port probe.fa

#    To query a server with translated DNA sequence:
#       gfServer transQuery host port probe.fa

#    To query server with PCR primers:
#       gfServer pcr host port fPrimer rPrimer maxDistance

#    To process one probe fa file against a .2bit format genome (not starting server):
#       gfServer direct probe.fa file(s).2bit

#    To test PCR without starting server:
#       gfServer pcrDirect fPrimer rPrimer file(s).2bit

#    To figure out if server is alive, on static instances get usage statics as well:
#       gfServer status host port
#      For dynamic gfServer instances, specify -genome and optionally the -genomeDataDir
#      to get information on an untranslated genome index. Include -trans to get about information
#      about a translated genome index

#    To get input file list:
#       gfServer files host port

#    To generate a precomputed index:
#       gfServer index gfidx file(s)
#      where the files are .2bit or .nib format files.  Separate indexes are
#      be created for untranslated and translated queries.  These can be used
#      with a persistent server as with 'start -indexFile or a dynamic server.
#      They must follow the naming convention for for dynamic servers.

#    To run a dynamic server (usually called by xinetd):
#       gfServer dynserver rootdir
#      Data files for genomes are found relative to the root directory.
#      Queries are made using the prefix of the file path relative to the root
#      directory.  The files $genome.2bit, $genome.untrans.gfidx, and
#      $genome.trans.gfidx are required. Typically the structure will be in
#      the form:
#          $rootdir/$genomeDataDir/$genome.2bit
#          $rootdir/$genomeDataDir/$genome.untrans.gfidx
#          $rootdir/$genomeDataDir/$genome.trans.gfidx
#      in this case, one would call gfClient with
#          -genome=$genome -genomeDataDir=$genomeDataDir
#      Often $genomeDataDir will be the same name as $genome, however it
#      can be a multi-level path. For instance:
#           GCA/902/686/455/GCA_902686455.1_mSciVul1.1/
#      The translated or untranslated index maybe omitted if there is no
#      need to handle that type of request.
#      The -perSeqMax functionality can be implemented by creating a file
#          $rootdir/$genomeDataDir/$genome.perseqmax


default_config = create_server_option()

server_app = typer.Typer(
    help="Make a server to quickly find where DNA occurs in genome"
)


tileSize: int = typer.Option(
    default_config.tileSize,
    "--tile-size",
    help="Size of n-mers to index.  Default is 11 for nucleotides, 4 for proteins (or translated nucleotides).",
)

stepSize: int = typer.Option(
    default_config.stepSize,
    "--stepSize",
    help="Spacing between tiles. Default is tileSize.",
)

minMatch: int = typer.Option(
    default_config.minMatch,
    "--min-match",
    help="Number of n-mer matches that trigger detailed alignment. Default is 2 for nucleotides, 3 for proteins.",
)

trans: bool = typer.Option(
    default_config.trans, "--trans", help="Translate database to protein in 6 frames."
)

log: str = typer.Option(
    default_config.log, "--log", help="Keep a log file that records server requests."
)

mask: bool = typer.Option(
    default_config.mask, "--mask", help="Use masking from .2bit file."
)

repMatch: int = typer.Option(
    default_config.repMatch,
    "--repMatch",
    help="Number of occurrences of a tile (n-mer) that triggers repeat masking the tile. Default is 1024.",
)

noSimpRepMask: bool = typer.Option(
    default_config.noSimpRepMask,
    "--noSimpRepMask",
    help="Suppresses simple repeat masking.",
)

maxDnaHits: int = typer.Option(
    default_config.maxDnaHits,
    "--maxDnaHits",
    help="Maximum number of hits for a DNA query that are sent from the server.",
)

maxTransHits: int = typer.Option(
    default_config.maxTransHits,
    "--maxTransHits",
    help="Maximum number of hits for a translated query that are sent from the server.",
)

maxNtSize: int = typer.Option(
    default_config.maxNtSize,
    "--maxNtSize",
    help="Maximum size of untranslated DNA query sequence.",
)

perSeqMax: Path = typer.Option(
    default_config.perSeqMax,
    "--perSeqMax",
    help="File contains one seq filename (possibly with ':seq' suffix) per line.",
)

canStop: bool = typer.Option(
    default_config.canStop,
    "--canStop",
    help="If set, a quit message will actually take down the server.",
)

indexFile: Path = typer.Option(
    default_config.indexFile,
    "--indexFile",
    help="Index file create by `gfServer index'.",
)

timeout: int = typer.Option(
    default_config.timeout, "--timeout", help="Timeout in seconds."
)


@server_app.command()
def start(
    host: str,
    port: int,
    tileSize: int = tileSize,
    stepSize: int = stepSize,
    minMatch: int = minMatch,
    trans: bool = trans,
    log: str = log,
    mask: bool = mask,
    repMatch: int = repMatch,
    noSimpRepMask: bool = noSimpRepMask,
    maxDnaHits: int = maxDnaHits,
    maxTransHits: int = maxTransHits,
    maxNtSize: int = maxNtSize,
    perSeqMax: Path = perSeqMax,
    canStop: bool = canStop,
    indexFile: Path = indexFile,
    timeout: int = timeout,
):
    """To set up a server

    gfServer start host port file(s)

    where the files are .2bit or .nib format files specified relative to the current directory
    """


@server_app.command()
def stop(host: str, port: int):
    print(f"{host=} {port=}")
