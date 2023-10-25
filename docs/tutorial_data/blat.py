from pathlib import Path

from pxblat import Client, Server, fa_to_two_bit


def check_path(path):
    """Check that the path exists."""
    if not Path(path).exists():
        raise FileNotFoundError(path)


def blat(seqs, ref, host, port):
    """Align sequences to a reference genome."""
    ref = Path(ref)
    check_path(ref)
    two_bit = ref.with_suffix(".2bit")

    if not two_bit.exists():
        fa_to_two_bit(
            [ref.as_posix()], two_bit.as_posix(), noMask=False, stripVersion=False, ignoreDups=False, useLong=False
        )

    client = Client(
        host,
        port,
        seq_dir=ref.parent.as_posix(),
        min_score=20,
        min_identity=90,
    )

    server = Server(host, port, two_bit.as_posix())

    with server:
        server.wait_ready()
        return client.query(seqs)


if __name__ == "__main__":
    # The sequence to align is `test_case1.fa`
    seqs = [
        "TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCACACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTCTCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCAA"
    ]

    results = blat(seqs, "test_ref.fa", "localhost", 65000)
    print(results[0])

    for hsp in results[0].hsps:
        print(hsp)
