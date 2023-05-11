import filecmp
from pathlib import Path

import pyblat
import pytest
from pyblat import extc


# open server from command line
# gfserver -canStop -log=test -stepSize=5 start localhost 88888 bitfiles

# query sever from command line
# gfclient -minScore=20 -minIdentity=90 localhost 88888 seqdir(twobit) in_fasta out_psl

# gfserver usage
# To set up a server:
#    gfServer start host port file(s)
#    where the files are .2bit or .nib format files specified relative to the current directory
# To remove a server:
#    gfServer stop host port
# To query a server with DNA sequence:
#    gfServer query host port probe.fa
# To query a server with protein sequence:
#    gfServer protQuery host port probe.fa
# To query a server with translated DNA sequence:
#    gfServer transQuery host port probe.fa
# To query server with PCR primers:
#    gfServer pcr host port fPrimer rPrimer maxDistance
# To process one probe fa file against a .2bit format genome (not starting server):
#    gfServer direct probe.fa file(s).2bit
# To test PCR without starting server:
#    gfServer pcrDirect fPrimer rPrimer file(s).2bit
# To figure out if server is alive, on static instances get usage statics as well:
#    gfServer status host port
#   For dynamic gfServer instances, specify -genome and optionally the -genomeDataDir
#   to get information on an untranslated genome index. Include -trans to get about information
#   about a translated genome index
# To get input file list:
#    gfServer files host port
# To generate a precomputed index:
#    gfServer index gfidx file(s)
#   where the files are .2bit or .nib format files.  Separate indexes are
#   be created for untranslated and translated queries.  These can be used
#   with a persistent server as with 'start -indexFile or a dynamic server.
#   They must follow the naming convention for for dynamic servers.
# To run a dynamic server (usually called by xinetd):
#    gfServer dynserver rootdir
#   Data files for genomes are found relative to the root directory.
#   Queries are made using the prefix of the file path relative to the root
#   directory.  The files $genome.2bit, $genome.untrans.gfidx, and
#   $genome.trans.gfidx are required. Typically the structure will be in
#   the form:
#       $rootdir/$genomeDataDir/$genome.2bit
#       $rootdir/$genomeDataDir/$genome.untrans.gfidx
#       $rootdir/$genomeDataDir/$genome.trans.gfidx
#   in this case, one would call gfClient with
#       -genome=$genome -genomeDataDir=$genomeDataDir
#   Often $genomeDataDir will be the same name as $genome, however it
#   can be a multi-level path. For instance:
#        GCA/902/686/455/GCA_902686455.1_mSciVul1.1/
#   The translated or untranslated index maybe omitted if there is no
#   need to handle that type of request.
#   The -perSeqMax functionality can be implemented by creating a file
#       $rootdir/$genomeDataDir/$genome.perseqmax


@pytest.fixture
def option_stat():
    PORT = 65000
    option = (
        extc.gfClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withTSeqDir("tests/data/")
        .withInName("tests/data/test_case1.fa")
        .build()
    )

    stat = extc.UsageStats()

    return option, stat


def test_fatwobit():
    test_file = Path("tests/data/test_ref.fa")
    output_file = Path("tests/data/test_ref.2bit")
    if output_file.exists():
        output_file.unlink()
    extc.faToTwoBit([test_file.as_posix()], output_file.as_posix())
    assert filecmp.cmp(output_file.as_posix(), "tests/data/test_ref.2bit")


def test_start_server(option_stat):
    (option, stat) = option_stat
    two_bit_file = Path("tests/data/test_ref.2bit")
    if not two_bit_file.exists():
        extc.faToTwoBit(["tests/data/test_ref.fa"], two_bit_file.as_posix())
    pyblat.server.start_server(
        "localhost", 88888, two_bit_file.as_posix(), option, stat
    )


def test_server_status():
    pass


def test_query_server():
    pass


def test_server_query():
    pass
