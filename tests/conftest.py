import pytest
from pxblat import extc
from pxblat.server import Server


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
    return (
        extc.gfServerOption().withCanStop(True).withStepSize(5).withThreads(2).build()
    )


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
def start_server(server_option, port, two_bit):
    server = Server("localhost", port, two_bit, server_option, use_others=True)
    server.start()

    server.wait_ready()
    yield server
