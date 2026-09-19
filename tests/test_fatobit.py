import filecmp

from pxblat import fa_to_two_bit


def test_fatwobit(
    reference,
    tmp_path,
):
    output_file = tmp_path / "test_ref_for_test.2bit"

    fa_to_two_bit([reference.as_posix()], output_file.as_posix())
    assert filecmp.cmp(output_file.as_posix(), "tests/data/test_ref.2bit")
