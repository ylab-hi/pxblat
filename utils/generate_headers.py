#!/usr/bin/env python3
"""Generate headers for all files in one header file.

@author: YangyangLi
"""
import re
import sys
import typing as t
from pathlib import Path


def replace_to_arrow(string: str) -> str:
    """Replace all '' to <>."""
    pattern = re.compile(r"\"(.*)\"")
    return pattern.sub(r"<\1>", string)


def get_headers_from_file(path: Path) -> t.Iterator[str]:
    """Get headers from file."""
    with open(path) as f:
        for line in f:
            if line.startswith("#include"):
                yield replace_to_arrow(line.strip())

    yield f"#include <{path.name}>"


def generate_headers(path: Path) -> t.Iterator[str]:
    """Generate headers for all files in one header file."""
    suffix = (".hpp", ".h")

    for path_ in path.rglob("*.h*"):
        if path_.suffix in suffix:
            yield from get_headers_from_file(path_)


def check_if_block(path: str, block_list: t.List[str]) -> bool:
    """Check if the block list is valid."""
    name = path[path.find("<") + 1 : path.find(">")]
    for item in block_list:
        if name.startswith(item):
            return True

    return False


def write_headers_to_file(
    path: Path, headers: t.Iterator[str], block_list: t.List[str]
) -> None:
    """Write headers to file."""
    with open(path, "w") as f:
        for header in headers:
            if not check_if_block(header, block_list):
                f.write(header + "\n")


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        print("Please specify the path of the headers file.")
    else:
        if not path.exists() or path.is_file():
            print("Path does not exist.")
            raise SystemExit
        if path.is_dir():
            write_headers_to_file(
                Path("./all_includes.hpp"), generate_headers(path), sys.argv[2:]
            )

        print("Done. Please check the file 'all_includes.hpp'.")


if __name__ == "__main__":
    main()
