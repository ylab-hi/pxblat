import filecmp

import pytest
from pxblat.cli import app
from pxblat.server import Server
from typer.testing import CliRunner

runner = CliRunner()


def test_call():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_fa2twobit_cli(tmp_path, two_bit):
    out = tmp_path / "testcli.2bit"

    result = runner.invoke(
        app, ["fatotwobit", "tests/data/test_ref.fa", out.as_posix()]
    )

    assert result.exit_code == 0
    assert out.exists()
    assert filecmp.cmp(out.as_posix(), two_bit)


@pytest.fixture
def start_server2(server_option, port, two_bit):
    server = Server("localhost", port + 1, two_bit, server_option, use_others=True)
    server.start()

    server.wait_ready()
    yield server


@pytest.mark.skip
def test_query_server_cli(start_server2, port, fa_file1, tmp_path):
    out = tmp_path / "t.psl"
    result = runner.invoke(
        app,
        [
            "client",
            "localhost",
            str(port + 1),
            "tests/data/",
            fa_file1.as_posix(),
            out.as_posix(),
            "--minScore",
            "20",
            "--minIdentity",
            "90",
        ],
    )

    assert result.exit_code == 0
