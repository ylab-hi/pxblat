#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: YangyangLi
@contact: yangyang.li@northwestern.edu
@version: 0.0.1
@license: MIT Licence
@file: cli.py.py
@time: 2020/12/28 10:21 PM
"""
import shutil
import sys
from pathlib import Path

from loguru import logger


logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
)


def find_lib_source_path(lib_name):
    pass


def find_lib_header_path(lib_name):
    pass


def find_lib_path(lib_name):
    pass


def copy_header_source(lib_name: str):
    header_dest_path = Path("src/pyblat/extc/header")
    lib_dest_path = Path("src/pyblat/extc/source")

    lib_base_path1 = Path("kent/src/lib")
    lib_base_path2 = Path("kent/src/jkOwnLib")
    header_base_path = Path("kent/src/inc")

    header_path = header_base_path / f"{lib_name}.h"

    if not header_path.exists():
        if (lib_base_path1 / f"{lib_name}.h").exists():
            logger.warning(
                f"header {lib_name} not found in {header_base_path}, but found in {lib_base_path1}"
            )
            header_path = lib_base_path1 / f"{lib_name}.h"
        elif (lib_base_path2 / f"{lib_name}.h").exists():
            logger.warning(
                f"header {lib_name} not found in {header_base_path}, but found in {lib_base_path2}"
            )
            header_path = lib_base_path2 / f"{lib_name}.h"

    assert header_path.exists(), "header file not found"

    lib_path = lib_base_path1 / f"{lib_name}.c"
    lib_path = lib_path if lib_path.exists() else lib_base_path2 / f"{lib_name}.c"

    shutil.copy(header_path, header_dest_path)
    logger.info(f"copying {header_path} to {header_dest_path}")

    if lib_path.exists():
        shutil.copy(lib_path, lib_dest_path)
        logger.info(f"copying {lib_path} to {lib_dest_path}")
    else:
        logger.warning(f"lib {lib_name} not found")


def main():
    lib_names = sys.argv[1:]
    if lib_names:
        for lib_name in lib_names:
            copy_header_source(lib_name)
    else:
        logger.warning("no lib name provided")


def update_code():
    lib_names = []
    for lib_name in lib_names:
        copy_header_source(lib_name)


if __name__ == "__main__":
    main()
