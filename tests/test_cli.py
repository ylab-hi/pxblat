import filecmp

import pytest
from pxblat.cli import app
from pxblat.server import Server
from typer.testing import CliRunner

runner = CliRunner()


def read_fa_seq(file):
    res = ""
    with open(file) as f:
        for line in f:
            if line.startswith(">"):
                continue
            else:
                res += line.strip()
    return res


def compare_two_fas(file1, file2):
    file1_seq = read_fa_seq(file1)
    file2_seq = read_fa_seq(file2)
    assert file1_seq == file2_seq


def test_call():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_twobit2fa_cli(tmp_path, reference, two_bit):
    out = tmp_path / "testcli.fa"
    result = runner.invoke(app, ["twobittofa", two_bit.as_posix(), out.as_posix()])
    assert result.exit_code == 0
    assert out.exists()
    compare_two_fas(reference, out)


def test_fa2twobit_cli(tmp_path, two_bit):
    out = tmp_path / "testcli.2bit"

    result = runner.invoke(
        app, ["fatotwobit", "tests/data/test_ref.fa", out.as_posix()]
    )

    assert result.exit_code == 0
    assert out.exists()
    assert filecmp.cmp(out.as_posix(), two_bit)


@pytest.fixture()
def start_server2(server_instance, port, two_bit):
    server = Server("localhost", port + 1, two_bit, can_stop=True, step_size=5, use_others=True)
    server.start()

    server.wait_ready()
    return server


@pytest.mark.skip()
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
