import pytest
from pxblat import extc
from pxblat.server import Server
from pxblat.server import Status


@pytest.fixture
def port():
    return 65000


@pytest.fixture
def two_bit():
    return "tests/data/test_ref.2bit"


@pytest.fixture
def fa_seq1():
    return "TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCACACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTCTCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCAA"


@pytest.fixture
def fa_seq2():
    return "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"


@pytest.fixture
def fa_file1():
    return "tests/data/test_case1.fa"


@pytest.fixture
def server_option():
    return extc.gfServerOption().withCanStop(True).withStepSize(5).build()


@pytest.fixture
def client_option(port):
    return (
        extc.gfClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(port))
        .withSeqDir("tests/data/")
        .withInName("tests/data/test_case1.fa")
        .build()
    )


@pytest.fixture
def expected_status():
    return {
        "version": "37x1",
        "serverType": "static",
        "type": "nucleotide",
        "host": "localhost",
        "port": "65000",
        "tileSize": "11",
        "stepSize": "5",
        "minMatch": "2",
        "pcr requests": "0",
        "blat requests": "0",
        "bases": "0",
        "misses": "0",
        "noSig": "0",
        "trimmed": "0",
        "warnings": "0",
    }


@pytest.fixture
def expected_status_instance():
    return Status(
        version="37x1",
        serverType="static",
        types="nucleotide",
        host="localhost",
        port=65000,
        tileSize=11,
        stepSize=5,
        minMatch=2,
        pcr_requests=0,
        blat_requests=0,
        bases=0,
        misses=0,
        noSig=0,
        trimmed=0,
        warnings=0,
    )


@pytest.fixture
def start_server(server_option, port, two_bit):
    server = Server("localhost", port, two_bit, server_option, use_others=True)
    server.start()
    print(f"{server}")
    server.wait_ready(timeout=10, restart=False)
    yield server
    # server.stop()
