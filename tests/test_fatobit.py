import pytest
import pyblat
from pathlib import Path
import filecmp


# open server from command line
# gfserver -canStop -log=test -stepSize=5 start localhost 88888 bitfiles"

# query sever from command line
# gfclient -minScore=20 -minIdentity=90 localhost 88888 in_fasta out_psl"


def test_fatwobit():
    test_file = Path("tests/data/test_ref.fa")
    output_file = Path("tests/data/test_ref.2bit")
    if output_file.exists():
        output_file.unlink()
    pyblat.faToTwoBit([test_file.as_posix()], output_file.as_posix())

    assert filecmp.cmp(output_file.as_posix(), "tests/data/test_ref.2bit")
