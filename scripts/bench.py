import os
import random
import subprocess
import time
from multiprocessing import Process
from pathlib import Path
from typing import Optional

import typer
from pxblat import extc
from pxblat.server import Client
from pxblat.server import Server
from pxblat.server import status_server
from pysam import FastaFile
from rich import print

PORT = 65000

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
)


def option_stat():
    server_option = (
        extc.gfServerOption().withCanStop(True).withStepSize(5).withThreads(4).build()
    )
    stat = extc.UsageStats()

    return server_option, stat


def build_index_fa(infa: Path):
    samtools = Path("~/miniconda3/bin/samtools")
    samtools = os.path.expanduser(samtools)
    index_file = infa.with_suffix(".fai")

    if not index_file.exists():
        print(f"Indexing {infa}")
        subprocess.run([samtools, "faidx", infa])
        print(f"Indexing {infa} done.")


@app.command()
def extract_fa(infa: Path, chr: str):
    # build_index_fa(infa)

    fa = FastaFile(infa.as_posix())
    ret = fa.fetch(chr)
    with open(f"{chr}.fa", "w") as f:
        f.write(f">{chr}\n")
        f.write(ret)


def get_length(start: int, end: int, fixed: Optional[int] = None):
    if fixed is None:
        return random.randrange(start, end)
    else:
        return fixed


@app.command()
def create_bench_data(infa: Path, number_of_data: int):
    outdir = Path("./benchmark/fas/")

    if not outdir.exists():
        outdir.mkdir(parents=True)

    fa = FastaFile(infa.as_posix())

    chr_len = fa.get_reference_length("chr20")
    print(f"chr20 length: {chr_len}")

    for i in range(number_of_data):
        length = get_length(1000, 3000)
        print(f"length: {length}")

        start = random.randint(0, chr_len - length)
        end = start + length
        ret = fa.fetch("chr20", start, end)
        outfile = outdir / f"chr20_{start}_{end}.fa"
        print(f"Writing id {i} to {outfile}")
        with open(outfile, "w") as f:
            f.write(f">chr20_{start}_{end}\n")
            f.write(ret)


def run_cmd(cmd: str) -> None:
    """Function is used to run the command in the system.

    :param cmd: the command to be run
    """
    subprocess.check_call(cmd, shell=True)


# f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} tests/data/ tests/data/test_case2.fa testc2.psl"
# f"./bin/gfServer start localhost {PORT} tests/data/test_ref.2bit -canStop -stepSize=5 -debugLog"


def fas():
    for f in Path("./benchmark/fas/").glob("*.fa"):
        yield f


@app.command()
def runc():
    start_server_cmd = f"./bin/gfServer start localhost {PORT} benchmark/data/chr20.2bit -canStop -stepSize=5 -debugLog"
    process = Process(target=run_cmd, args=[start_server_cmd], daemon=True)
    process.start()

    time.sleep(20)

    server_option, stat = option_stat()
    print(status_server("localhost", PORT, server_option))

    for fa in fas():
        cmd = f"./bin/gfClient -minScore=20 -minIdentity=90 localhost {PORT} benchmark/data/ {fa} {fa}.psl"
        run_cmd(cmd)


# TODO: Debug here <05-16-23, Yangyang Li yangyang.li@northwestern.edu>
@app.command()
def runp():
    server_option, stat = option_stat()
    # two_bit = Path("tests/data/test_ref.2bit")
    two_bit = Path("benchmark/data/chr20.2bit")
    server = Server("localhost", PORT, two_bit, server_option)
    server.start()
    server.wait_ready()

    print(server.status())
    print(server.files())

    fa1 = list(fas())[0]

    # client_option = (
    #         extc.gfClientOption()
    #         .withMinScore(20)
    #         .withMinIdentity(90)
    #         .withHost("localhost")
    #         .withPort(str(start_server.port))
    #         .withSeqDir("tests/data/")
    #         .withInSeq(fa_seq1)
    #         .build()
    #     )
    print(fa1)

    # seq = "TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCACACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTCTCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCAA"
    seq = "tgtaattccaactactcaggaggctgaggcaggagaatcgcttgagcccaggaggcggaggttgcagtgagccgagatcgcaccattgcactctagcctgggagacaagagcgaaactctgtctcaaaaaaaaaaaaagaaccaagttgaagga"

    client_option = (
        extc.gfClientOption()
        .withMinScore(20)
        .withMinIdentity(90)
        .withHost("localhost")
        .withPort(str(server.port))
        .withSeqDir(two_bit.parent.as_posix())
        .withInSeq(seq)
        .build()
    )

    client = Client(client_option, server_option=server_option)
    client.start()

    ret = client.get()
    print(ret)


@app.command()
def test_result():
    pass


if __name__ == "__main__":
    app()
