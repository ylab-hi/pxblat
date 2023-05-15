import pytest
from pxblat.extc import gfClientOption
from pxblat.extc import UsageStats
from pxblat.server import check_port_open
from pxblat.server import query_server


PORT = 65000


@pytest.fixture
def fa1():
    return "TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCACACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTCTCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCAA"


@pytest.fixture
def option_stat():
    client_option = (
        gfClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir("tests/data/")
        .withInName("tests/data/test_case1.fa")
        .build()
    )

    stat = UsageStats()
    return client_option, stat


def test_client_for_mem_fa(fa1):
    if check_port_open("localhost", PORT):
        # pytest.skip("server not started")
        print("server not started")

    # .withInName("tests/data/test_case1.fa")
    client_option = (
        gfClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withSeqDir("tests/data/")
        .withInSeq(fa1)
        .build()
    )

    query_server(client_option)


def test_client_thread(option_stat):
    (option, stat) = option_stat
