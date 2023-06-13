import typing as t
from pathlib import Path

from pxblat.extc import faToTwoBit
from pxblat.extc import twoBitToFa
from pxblat.extc import TwoBitToFaOption


__all__ = ["fa_to_two_bit", "two_bit_to_fa"]


def fa_to_two_bit(
    inFiles: t.List[str],
    outFile: str,
    noMask: bool = False,
    stripVersion: bool = False,
    ignoreDups: bool = False,
    useLong: bool = False,
):
    """Convert one or more FASTA files to two-bit format.

    Args:
        inFiles (List[str]): A list of paths to the input FASTA files.
        outFile (str): The path to the output two-bit file.
        noMask (bool, optional): If True, do not mask the output sequence. Defaults to False.
        stripVersion (bool, optional): If True, strip the version number from the sequence IDs. Defaults to False.
        ignoreDups (bool, optional): If True, ignore duplicate sequences in the input files. Defaults to False.
        useLong (bool, optional): If True, use the long format for the two-bit file. Defaults to False.

    Returns:
        None

    This function converts one or more input FASTA files to two-bit format and saves the result to the specified output file.
    The function takes several optional arguments that control the behavior of the conversion process, such as whether to mask
    the output sequence or strip the version number from the sequence IDs. The function returns None.

    Example:
        >>> fa_to_two_bit(['input.fasta'], 'output.2bit')
    """
    return faToTwoBit(inFiles, outFile, noMask, stripVersion, ignoreDups, useLong)


def two_bit_to_fa(
    inName: t.Union[str, Path], outName: t.Union[str, Path], option: TwoBitToFaOption
):
    if isinstance(inName, Path):
        inName = str(inName)

    if isinstance(outName, Path):
        outName = str(outName)

    return twoBitToFa(inName, outName, option)
