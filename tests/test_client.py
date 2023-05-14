import pytest
from pxblat.extc import gfClientOption
from pxblat.extc import UsageStats
from pxblat.server import query_server


@pytest.fixture
def option_stat():
    PORT = 65000
    client_option = (
        gfClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(PORT))
        .withTSeqDir("tests/data/")
        .withInName("tests/data/test_case1.fa")
        .build()
    )

    stat = UsageStats()
    return client_option, stat


def test_client(option_stat):
    (option, _) = option_stat

    query_server(option)


def test_client_thread(option_stat):
    (option, stat) = option_stat
