import os
import random
import subprocess
from pathlib import Path
from typing import Optional

import typer
from pysam import FastaFile
from rich import print

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
)


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


def runc():
    pass


def runp():
    pass


@app.command()
def test_result():
    pass


if __name__ == "__main__":
    app()
