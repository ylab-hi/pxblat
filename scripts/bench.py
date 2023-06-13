import os
import random
import subprocess
from pathlib import Path
from typing import Optional

import typer
from pxblat import extc
from pysam import FastaFile
from rich import print

PORT = 65000

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
)


def option_stat():
    server_option = (
        extc.ServerOption().withCanStop(True).withStepSize(5).withThreads(4).build()
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


if __name__ == "__main__":
    app()
