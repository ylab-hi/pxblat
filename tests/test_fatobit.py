import filecmp
from pathlib import Path

from pxblat.server import fa_to_two_bit


def test_fatwobit():
    test_file = Path("tests/data/test_ref.fa")
    output_file = Path("tests/data/test_ref_for_test.2bit")

    if output_file.exists():
        output_file.unlink()

    fa_to_two_bit([test_file.as_posix()], output_file.as_posix())
    assert filecmp.cmp(output_file.as_posix(), "tests/data/test_ref.2bit")
