import typing as t
from pathlib import Path
from typing import Optional

from Bio.SearchIO.BlatIO import BlatPslParser  # type: ignore


class PslOutput:
    def __init__(self, content: str, save_mem: bool = False):
        self._content: Optional[str] = None if save_mem else content
        self._iterable = iter(content.splitlines(keepends=True))

    def readline(self):
        try:
            return next(self._iterable)
        except StopIteration:
            return ""


_ITERATOR_MAP = {
    "psl": BlatPslParser,
}

_HANDLE_MAP = {
    "psl": PslOutput,
}

# https://github.com/biopython/biopython/blob/master/Bio/SearchIO/BlatIO.py


def get_handle(format: str, mapping):
    try:
        handle = mapping[format]
    except KeyError:
        # handle the errors with helpful messages
        if format is None:
            raise ValueError("Format required (lower case string)") from None
        elif not isinstance(format, str):
            raise TypeError("Need a string for the file format (lower case)") from None
        elif format != format.lower():
            raise ValueError("Format string %r should be lower case" % format) from None
        else:
            raise ValueError(
                "Unknown format %r. Supported formats are %r"
                % (format, "', '".join(mapping))
            ) from None

    else:
        return handle


def get_processor(format, mapping):
    try:
        obj_info = mapping[format]
    except KeyError:
        # handle the errors with helpful messages
        if format is None:
            raise ValueError("Format required (lower case string)") from None
        elif not isinstance(format, str):
            raise TypeError("Need a string for the file format (lower case)") from None
        elif format != format.lower():
            raise ValueError("Format string %r should be lower case" % format) from None
        else:
            raise ValueError(
                "Unknown format %r. Supported formats are %r"
                % (format, "', '".join(mapping))
            ) from None

    else:
        return obj_info


def parse(content: str, format=None, **kwargs):
    if format is None:
        format = "psl"

    iterator = get_processor(format, _ITERATOR_MAP)
    handle = get_handle(format, _HANDLE_MAP)
    yield from iterator(handle(content), **kwargs)


def read(content: str, format=None, **kwargs):
    query_results = parse(content, format, **kwargs)
    try:
        query_result = next(query_results)
    except StopIteration:
        raise ValueError("No query results found in handle") from None

    try:
        next(query_results)
        raise ValueError("More than one query result found in handle")
    except StopIteration:
        pass

    return query_result


def _psl2sam(psl: str, samfile: Path):
    raise NotImplementedError


def psl2sam(psl: t.Union[str, Path], samfile: Path):
    if isinstance(psl, Path):
        psl = psl.read_text()
    elif Path(psl).exists():
        psl = Path(psl).read_text()

    _psl2sam(psl, samfile)
