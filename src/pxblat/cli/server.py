from pathlib import Path

import typer
from rich import print

from pxblat.extc import UsageStats
from pxblat.server import (
    create_server_option,
    start_server_mt,
    status_server,
    stop_server,
)
from pxblat.server import files as server_files

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


default_option = create_server_option()

server_app = typer.Typer(
    help="Make a server to quickly find where DNA occurs in genome",
)


tileSize: int = typer.Option(
    default_option.tileSize,
    "--tile-size",
    help="Size of n-mers to index.  Default is 11 for nucleotides, 4 for proteins (or translated nucleotides).",
)

stepSize: int = typer.Option(
    default_option.stepSize,
    "--stepSize",
    help="Spacing between tiles. Default is tileSize.",
)

minMatch: int = typer.Option(
    default_option.minMatch,
    "--min-match",
    help="Number of n-mer matches that trigger detailed alignment. Default is 2 for nucleotides, 3 for proteins.",
)

trans: bool = typer.Option(
    default_option.trans,
    "--trans",
    help="Translate database to protein in 6 frames.",
)

log: str = typer.Option(
    None,
    "--log",
    exists=True,
    dir_okay=False,
    help="Keep a log file that records server requests.",
)

mask: bool = typer.Option(
    default_option.mask,
    "--mask",
    help="Use masking from .2bit file.",
)

repMatch: int = typer.Option(
    default_option.repMatch,
    "--repMatch",
    help="Number of occurrences of a tile (n-mer) that triggers repeat masking the tile. Default is 1024.",
)

noSimpRepMask: bool = typer.Option(
    default_option.noSimpRepMask,
    "--noSimpRepMask",
    help="Suppresses simple repeat masking.",
)

maxDnaHits: int = typer.Option(
    default_option.maxDnaHits,
    "--maxDnaHits",
    help="Maximum number of hits for a DNA query that are sent from the server.",
)

maxTransHits: int = typer.Option(
    default_option.maxTransHits,
    "--maxTransHits",
    help="Maximum number of hits for a translated query that are sent from the server.",
)

maxNtSize: int = typer.Option(
    default_option.maxNtSize,
    "--maxNtSize",
    help="Maximum size of untranslated DNA query sequence.",
)

perSeqMax: Path = typer.Option(
    None,
    "--perSeqMax",
    exists=True,
    dir_okay=False,
    help="File contains one seq filename (possibly with ':seq' suffix) per line.",
)

canStop: bool = typer.Option(
    default_option.canStop,
    "--canStop",
    help="If set, a quit message will actually take down the server.",
)

indexFile: Path = typer.Option(
    None,
    "--indexFile",
    exists=True,
    dir_okay=False,
    help="Index file create by `gfServer index'.",
)
timeout: int = typer.Option(
    default_option.timeout,
    "--timeout",
    help="Timeout in seconds.",
)


two_bit: Path = typer.Argument(
    ...,
    exists=True,
    dir_okay=False,
    help="Two bit file",
)

threads: int = typer.Option(2, "--threads", help="Number of threads to use")


@server_app.command()
def start(
    host: str,
    port: int,
    two_bit: Path = two_bit,
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
    _threads: int = threads,
):
    """To set up a server.

    gfServer start host port file(s)

    where the files are .2bit or .nib format files specified relative to the current directory
    """
    server_option = (
        create_server_option()
        .withTileSize(tileSize)
        .withStepSize(stepSize)
        .withMinMatch(minMatch)
        .withTrans(trans)
        .withMask(mask)
        .withRepMatch(repMatch)
        .withNoSimpRepMask(noSimpRepMask)
        .withMaxDnaHits(maxDnaHits)
        .withMaxTransHits(maxTransHits)
        .withMaxNtSize(maxNtSize)
        .withCanStop(canStop)
        .withTimeout(timeout)
    )

    if log is not None:
        server_option.withLog(log)

    if perSeqMax is not None:
        server_option.withPerSeqMax(perSeqMax.as_posix())

    if indexFile is not None:
        server_option.withIndexFile(indexFile.as_posix())

    server_option.build()

    stat = UsageStats()

    start_server_mt(
        host,
        port,
        two_bit.as_posix(),
        server_option,
        stat,
        try_new_port=False,
    )


@server_app.command()
def stop(host: str, port: int):
    """To remove a server."""
    stop_server(host, port)


@server_app.command()
def status(
    host: str,
    port: int,
    trans: bool = trans,
):
    """To figure out if server is alive, on static instances get usage statics."""
    server_option = create_server_option().withTrans(trans)
    server_option.build()
    ret = status_server(host, port, server_option)
    print(ret)


@server_app.command()
def files(host: str, port: int):
    """To get input file list."""
    ret = server_files(host, port)
    print(ret)
