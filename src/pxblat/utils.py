"""Utility functions for pxblat."""
import functools
import io
import os
import sys
import tempfile
import typing
from contextlib import contextmanager


class Result:
    """A class to represent the result of a command."""

    def __init__(
        self,
        returncode: typing.Any,
        stdout: str,
        stderr: str,
    ) -> None:
        """Initialize a Result object."""
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

    def __repr__(self) -> str:
        """Return the representation of a Result object."""
        return f"Result(stdout={self.stdout}, stderr={self.stderr}, returncode={self.returncode})"

    def is_ok(self) -> bool:
        """Return True if the returncode is 0."""
        assert isinstance(self.returncode, int)
        return self.returncode == 0

    def result(self):
        """Return the returncode."""
        assert not isinstance(self.returncode, int)
        return self.returncode


@contextmanager
def stdout_redirected(to=os.devnull):
    """Import os.

    with stdout_redirected(to=filename):
        print("from Python")
        os.system("echo non-Python applications are also supported")
    """
    fd = sys.stdout.fileno()

    def _redirect_stdout(to):
        sys.stdout.close()  # + implicit flush()
        os.dup2(to.fileno(), fd)  # fd writes to 'to' file
        sys.stdout = os.fdopen(fd, "w")  # Python writes to fd

    with os.fdopen(os.dup(fd), "w") as old_stdout:
        if isinstance(to, str):
            with open(to, "w") as file:
                _redirect_stdout(to=file)
        elif isinstance(to, io.TextIOBase):
            _redirect_stdout(to=to)
        try:
            yield  # allow code to be run with the redirected stdout
        finally:
            _redirect_stdout(to=old_stdout)  # restore stdout.
            # buffering and flags such as


@contextmanager
def stderr_redirected(to=os.devnull):
    """Import os.

    with stdout_redirected(to=filename):
        print("from Python")
        os.system("echo non-Python applications are also supported")
    """
    fd = sys.stderr.fileno()

    def _redirect_stdout(to):
        sys.stderr.close()  # + implicit flush()
        os.dup2(to.fileno(), fd)  # fd writes to 'to' file
        sys.stderr = os.fdopen(fd, "w")  # Python writes to fd

    with os.fdopen(os.dup(fd), "w") as old_stdout:
        if isinstance(to, str):
            with open(to, "w") as file:
                _redirect_stdout(to=file)
        elif isinstance(to, io.TextIOBase):
            _redirect_stdout(to=to)
        try:
            yield  # allow code to be run with the redirected stdout
        finally:
            _redirect_stdout(to=old_stdout)  # restore stdout.


def redirected(func):
    """Redirect stdout and stderr to a temporary file."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        stdout = ""
        stderr = ""

        stdout_file = tempfile.TemporaryFile("w+")
        stderr_file = tempfile.TemporaryFile("w+")

        with stdout_redirected(to=stdout_file), stderr_redirected(to=stderr_file):  # type: ignore
            ret = func(*args, **kwargs)

        stdout_file.seek(0)
        stderr_file.seek(0)

        stdout = stdout_file.read()
        stderr = stderr_file.read()

        stderr_file.close()
        stdout_file.close()

        return Result(ret, stdout, stderr)

    return wrapper
