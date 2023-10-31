import sys
from ctypes.util import find_library
from pathlib import Path


def main():
    """Find a library and print its path."""
    libname = sys.argv[1]
    libpath = find_library(libname)
    if libpath is None:
        print(f"Could not find library {libname}")  # noqa: T201
        return 1
    libbase = Path(libpath)
    libbase = libbase.resolve()
    print(libbase)  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())
