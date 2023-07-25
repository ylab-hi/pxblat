from __future__ import annotations

from pathlib import Path

from Bio.SearchIO.BlatIO import BlatPslParser  # type: ignore

# https://github.com/biopython/biopython/blob/master/Bio/SearchIO/BlatIO.py


class PslOutput:
    """A class for PSL output."""

    def __init__(self, content: str, *, save_mem: bool = False) -> None:
        """Initialize the class."""
        self._content: str | None = None if save_mem else content
        self._iterable = iter(content.splitlines(keepends=True))

    def readline(self):
        """Read a line from the file."""
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


def get_handle(format: str, mapping):
    """Returns the handle associated with the given format from the mapping.

    This function takes a format string and a mapping from format strings to handles, and returns the handle associated
    with the given format. If the format is not in the mapping, it raises an error with a helpful message.

    Args:
        format (str): The format string for which to get the handle. This should be a lower case string.
        mapping (dict): The mapping from format strings to handles.

    Raises:
        ValueError: If the format is None, not a lower case string, or not in the mapping.
        TypeError: If the format is not a string.

    Returns:
        The handle associated with the given format.
    """
    try:
        handle = mapping[format]
    except KeyError:
        # handle the errors with helpful messages
        if format is None:
            raise ValueError("Format required (lower case string)") from None

        if not isinstance(format, str):
            raise TypeError("Need a string for the file format (lower case)") from None
        if format != format.lower():
            raise ValueError("Format string %r should be lower case" % format) from None

        msg = f"Unknown format {format!r}. Supported formats are {', '.join(mapping)}"
        raise ValueError(msg) from None

    else:
        return handle


def get_processor(format, mapping):
    """Returns the information object associated with the given format from the mapping.

    This function takes a format string and a mapping from format strings to information objects,
    and returns the information object associated with the given format. If the format is not in the mapping,
    it raises an error with a helpful message.

    Args:
        format (str): The format string for which to get the information object. This should be a lower case string.
        mapping (dict): The mapping from format strings to information objects.

    Raises:
        ValueError: If the format is None, not a lower case string, or not in the mapping.
        TypeError: If the format is not a string.

    Returns:
        obj_info: The information object associated with the given format.
    """
    try:
        obj_info = mapping[format]
    except KeyError:
        # handle the errors with helpful messages
        if format is None:
            msg = "Format required (lower case string)"
            raise ValueError(msg) from None
        if not isinstance(format, str):
            msg = "Need a string for the file format (lower case)"
            raise TypeError(msg) from None
        if format != format.lower():
            raise ValueError("Format string %r should be lower case" % format) from None

        msg = f"Unknown format {format!r}. Supported formats are {', '.join(mapping)}"
        raise ValueError(msg) from None

    else:
        return obj_info


def parse(content: str, format=None, **kwargs):
    """Parses the given content according to the specified format.

    This function takes a string content and a format string, gets the corresponding iterator and handle using the
    format from the '_ITERATOR_MAP' and '_HANDLE_MAP' respectively, and then yields the parsed content using the
    iterator.

    Args:
        content (str): The string content to parse.
        format (str, optional): The format string indicating how to parse the content. If not provided, 'psl' format will be used. Defaults to None.
        **kwargs: Arbitrary keyword arguments to be passed to the iterator function.

    Yields:
        The parsed content.

    Raises:
        ValueError: If the format is None after defaulting, not a lower case string, or not in the mapping.
        TypeError: If the format is not a string.
    """
    if format is None:
        format = "psl"

    iterator = get_processor(format, _ITERATOR_MAP)
    handle = get_handle(format, _HANDLE_MAP)
    yield from iterator(handle(content), **kwargs)


def read(content: str, format=None, **kwargs):
    """Reads and returns the first query result from the given content.

    This function takes a string content and a format string, parses the content using the `parse` function,
    and returns the first query result. If no results are found, or if more than one result is found, it raises an error.

    Args:
        content (str): The string content to parse and read.
        format (str, optional): The format string indicating how to parse the content. If not provided, 'psl' format will be used. Defaults to None.
        **kwargs: Arbitrary keyword arguments to be passed to the `parse` function.

    Returns:
        query_result: The first query result found in the content.

    Raises:
        ValueError: If no query results are found in the content, or if more than one query result is found.
        ValueError/TypeError: If there is an error in parsing the content. These exceptions are propagated from the `parse` function.
    """
    query_results = parse(content, format, **kwargs)
    try:
        query_result = next(query_results)
    except StopIteration:
        msg = "No query results found in handle"
        raise ValueError(msg) from None

    try:
        next(query_results)
        msg = "More than one query result found in handle"
        raise ValueError(msg)
    except StopIteration:
        pass

    return query_result


def _psl2sam(psl: str, samfile: Path):
    raise NotImplementedError


def psl2sam(psl: str | Path, samfile: Path):
    """Converts a psl file to a sam file."""
    if isinstance(psl, Path):
        psl = psl.read_text()
    elif Path(psl).exists():
        psl = Path(psl).read_text()

    _psl2sam(psl, samfile)
