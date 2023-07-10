# -*- coding: utf-8 -*-
import pytest
from pxblat import Client
from rich import print


def test_gclient(
    start_server,
    server_option,
    fa_seq1,
    fa_file1,
):
    client = Client(
        host="localhost",
        port=start_server.port,
        seq_dir="tests/data/",
        min_score=20,
        min_identity=90,
        server_option=server_option,
    )

    ret = client.query([fa_seq1, fa_seq1, fa_file1])
    for r in ret:
        print(r)


@pytest.mark.parametrize(
    "parse",
    [True, False],
)
def test_gclient_parse(start_server, fa_seq1, fa_file1, parse):
    client = Client(
        host="localhost",
        port=start_server.port,
        seq_dir="tests/data/",
        min_score=20,
        min_identity=90,
        parse=parse,
    )

    ret = client.query([fa_seq1, fa_seq1, fa_file1])
    for r in ret:
        print(r)
