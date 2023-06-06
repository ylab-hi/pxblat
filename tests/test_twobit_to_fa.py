from pathlib import Path

from pxblat import two_bit_to_fa
from pxblat import TwoBitToFaOption


def test_create_two_bit_to_fa_option():
    option = TwoBitToFaOption().build()
    assert option


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


def test_bit2fa(
    reference,
    two_bit,
):
    output_file = Path("tests/data/test_bit2fa_tmp.fa")
    if output_file.exists():
        output_file.unlink()

    option = TwoBitToFaOption().build()

    two_bit_to_fa(
        two_bit,
        output_file,
        option=option,
    )

    compare_two_fas(reference, output_file)
