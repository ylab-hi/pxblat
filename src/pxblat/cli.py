import logging
from pathlib import Path

import typer
from rich import print
from rich.logging import RichHandler

from .server.basic import faToTwoBit

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("pxblat")


app = typer.Typer(
    epilog="YangyangLi 2023 please cite me",
    context_settings={"help_option_names": ["-h", "--help"]},
)
# faToTwoBit - Convert DNA from fasta to 2bit format
# usage:
#    faToTwoBit in.fa [in2.fa in3.fa ...] out.2bit
# options:
#    -long          use 64-bit offsets for index.   Allow for twoBit to contain more than 4Gb of sequence.
#                   NOT COMPATIBLE WITH OLDER CODE.
#    -noMask        Ignore lower-case masking in fa file.
#    -stripVersion  Strip off version number after '.' for GenBank accessions.
#    -ignoreDups    Convert first sequence only if there are duplicate sequence
#                   names.  Use 'twoBitDup' to find duplicate sequences.
# /p


@app.command()
def fa2TwoBit(
    infa: list[Path],
    out2bit: Path,
    long: bool = False,
    noMask: bool = False,
    stripVersion: bool = False,
    ignoreDups: bool = False,
):
    """faToTwoBit - Convert DNA from fasta to 2bit format

    usage:

       faToTwoBit in.fa [in2.fa in3.fa ...] out.2bit

    options:

       -long          use 64-bit offsets for index.   Allow for twoBit to contain more than 4Gb of sequence.
                      NOT COMPATIBLE WITH OLDER CODE.

       -noMask        Ignore lower-case masking in fa file.

       -stripVersion  Strip off version number after '.' for GenBank accessions.

       -ignoreDups    Convert first sequence only if there are duplicate sequence
                      names.  Use 'twoBitDup' to find duplicate sequences."""

    for file in infa:
        if not file.exists():
            raise typer.Abort(f"{file} does not exist")

    if out2bit.exists():
        log.warning(f"{out2bit} exist will be overide")

    faToTwoBit(
        [f.as_posix() for f in infa],
        out2bit.as_posix(),
        noMask,
        stripVersion,
        ignoreDups,
        long,
    )


@app.command()
def server(host: str, port: int):
    print(f"{host=}")
    print(f"{port=}")


@app.command()
def client(host: str, port: int):
    print(f"{host=}")
    print(f"{port=}")


if __name__ == "__main__":
    app()
