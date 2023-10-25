from pathlib import Path

import pytest
from pxblat import ClientOption
from pxblat.server import Server
from pxblat.server import Status


@pytest.fixture()
def port():
    return 65000


@pytest.fixture()
def reference():
    return Path("tests/data/test_ref.fa")


@pytest.fixture()
def two_bit():
    return Path("tests/data/test_ref.2bit")


@pytest.fixture()
def fa_seq1():
    return "TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCACACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTCTCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCAA"


@pytest.fixture()
def fa_seq2():
    return "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"


@pytest.fixture()
def fa_file1():
    return Path("tests/data/test_case1.fa")


@pytest.fixture()
def client_option(port):
    return (
        ClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(port))
        .withSeqDir("tests/data/")
        .withInName("tests/data/test_case1.fa")
        .build()
    )


@pytest.fixture()
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


@pytest.fixture()
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


@pytest.fixture()
def server_instance(port, two_bit):
    return Server("localhost", port, two_bit, can_stop=True, step_size=5,
                  use_others=True)


@pytest.fixture()
def start_server(server_instance):
    server = server_instance

    server.start()
    print(f"{server}")
    server.wait_ready(timeout=10, restart=False)
    return server
