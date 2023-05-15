import filecmp

from pxblat.cli import app
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


def test_query_server_cli(start_server, port, fa_file1, tmp_path):
    out = tmp_path / "t.psl"
    result = runner.invoke(
        app,
        [
            "client",
            "localhost",
            str(port),
            "tests/data/",
            fa_file1,
            out.as_posix(),
            "--minScore",
            "20",
            "--minIdentity",
            "90",
        ],
    )

    assert result.exit_code == 0
