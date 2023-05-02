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

HEADER_DEST_PATH = Path("src/pyblat/extc/header")
LIB_DEST_PATH = Path("src/pyblat/extc/source")

LIB_BASE_PATH1 = Path("kent/src/lib")
LIB_BASE_PATH2 = Path("kent/src/jkOwnLib")

HEADER_BASE_PATH = Path("kent/src/inc")


def find_lib_source(lib_name):
    lib_path = LIB_BASE_PATH1 / f"{lib_name}.c"
    lib_path = lib_path if lib_path.exists() else LIB_BASE_PATH2 / f"{lib_name}.c"

    if lib_path.exists():
        logger.info(f"copying {lib_path} to {LIB_DEST_PATH}")
        return lib_path
    else:
        logger.warning(f"lib {lib_name} not found")
        return None


def copy_lib_source(lib_name):
    lib_path = LIB_BASE_PATH1 / f"{lib_name}.c"
    lib_path = lib_path if lib_path.exists() else LIB_BASE_PATH2 / f"{lib_name}.c"

    if lib_path.exists():
        shutil.copy(lib_path, LIB_DEST_PATH)
        logger.info(f"copying {lib_path} to {LIB_DEST_PATH}")
    else:
        logger.warning(f"lib {lib_name} not found")


def find_lib_header(lib_name):
    header_path = HEADER_BASE_PATH / f"{lib_name}.h"

    if not header_path.exists():
        if (LIB_BASE_PATH1 / f"{lib_name}.h").exists():
            logger.warning(
                f"header {lib_name} not found in {HEADER_BASE_PATH}, but found in {LIB_BASE_PATH1}"
            )
            header_path = LIB_BASE_PATH1 / f"{lib_name}.h"
        elif (LIB_BASE_PATH2 / f"{lib_name}.h").exists():
            logger.warning(
                f"header {lib_name} not found in {HEADER_BASE_PATH}, but found in {LIB_BASE_PATH2}"
            )
            header_path = LIB_BASE_PATH2 / f"{lib_name}.h"

    if not header_path.exists():
        logger.warning(f"header {lib_name} not found")
        return None
    else:
        return header_path


def copy_lib_header(lib_name):
    header_path = HEADER_BASE_PATH / f"{lib_name}.h"

    if not header_path.exists():
        if (LIB_BASE_PATH1 / f"{lib_name}.h").exists():
            logger.warning(
                f"header {lib_name} not found in {HEADER_BASE_PATH}, but found in {LIB_BASE_PATH1}"
            )
            header_path = LIB_BASE_PATH1 / f"{lib_name}.h"
        elif (LIB_BASE_PATH2 / f"{lib_name}.h").exists():
            logger.warning(
                f"header {lib_name} not found in {HEADER_BASE_PATH}, but found in {LIB_BASE_PATH2}"
            )
            header_path = LIB_BASE_PATH2 / f"{lib_name}.h"

    assert header_path.exists(), "header file not found"

    shutil.copy(header_path, HEADER_DEST_PATH)
    logger.info(f"copying {header_path} to {HEADER_DEST_PATH}")


def copy_header_source(lib_name: str):
    copy_lib_source(lib_name)
    copy_lib_header(lib_name)


def collect_header():
    headers = HEADER_DEST_PATH.rglob("*.h")
    return headers


def update():
    headers = collect_header()
    for header in headers:
        logger.info(f"processing {header}")
        lib_name = header.stem
        lib_header_path = find_lib_header(lib_name)
        lib_source_path = find_lib_source(lib_name)

        if lib_header_path is not None and lib_header_path.exists():
            shutil.copy(lib_header_path, header.parent)
            logger.info(f"copying {lib_header_path} to {header.parent}")
        else:
            logger.warning(f"header {lib_name} not found")

        if lib_source_path is not None and lib_source_path.exists():
            shutil.copy(
                lib_source_path,
                header.parent.parent.parent / "source" / header.parent.name,
            )
        else:
            logger.warning(f"source {lib_name} not found")


def main():
    lib_names = sys.argv[1:]
    if lib_names:
        for lib_name in lib_names:
            copy_header_source(lib_name)
    else:
        logger.warning("no lib name provided")


def cli():
    update()


def update_code():
    lib_names = []
    for lib_name in lib_names:
        copy_header_source(lib_name)


if __name__ == "__main__":
    main()
