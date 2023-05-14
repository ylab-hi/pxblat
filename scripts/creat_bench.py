import os
import random
import subprocess
from pathlib import Path

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

    fa = FastaFile(infa)
    ret = fa.fetch(chr)
    with open(f"{chr}.fa", "w") as f:
        f.write(f">{chr}\n")
        f.write(ret)


@app.command()
def create_bench_data(infa: Path, number_of_data: int):
    fa = FastaFile(infa)
    chr_len = fa.get_reference_length("chr20")
    print(f"chr20 length: {chr_len}")

    for _i in range(number_of_data):
        start = random.randint(0, chr_len - 1000)
        end = start + 1000
        ret = fa.fetch("chr20", start, end)
        with open(f"chr20_{start}_{end}.fa", "w") as f:
            f.write(f">chr20_{start}_{end}\n")
            f.write(ret)


if __name__ == "__main__":
    app()
