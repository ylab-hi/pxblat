import os
import shlex
import typing
from contextlib import contextmanager
from ctypes.util import find_library
from functools import wraps
from pathlib import Path

from pybind11.setup_helpers import build_ext
from pybind11.setup_helpers import Pybind11Extension


header_path = []
lib_path = []


def find_available_library(lib_name: str):
    lib_path = find_library(lib_name)
    if not lib_path:
        raise RuntimeError(f"Cannot find {lib_name} library.")

    header_path = Path(lib_path).parent.parent / "include"

    return Path(lib_path), header_path


external_htslib_libraries = ["z", "hts", "ssl", "crypto", "m"]


for lb in external_htslib_libraries:
    find_available_library(lb)


def remove_env(key: str):
    """Remove environment variable."""
    env_cflags = os.environ.get("CFLAGS", "")
    env_cppflags = os.environ.get("CPPFLAGS", "")
    flags = shlex.split(env_cflags) + shlex.split(env_cppflags)

    for flag in flags:
        if flag.startswith(key):
            raise RuntimeError(f"Please remove {key} from CFLAGS and CPPFLAGS.")


def find_lib_path_in_conda(lib_name: str):
    check_conda_env()

    conda_path = Path(os.environ["CONDA_PREFIX"])
    lib_dir = conda_path / "lib"
    conda_path / "include"

    lib_path_linux = lib_dir / f"lib{lib_name}.so"
    lib_path_macos = lib_dir / f"lib{lib_name}.dylib"
    lib_path_static = lib_dir / f"lib{lib_name}.a"

    if lib_path_linux.exists():
        return lib_path_linux
    elif lib_path_macos.exists():
        return lib_path_macos
    elif lib_path_static.exists():
        return lib_path_static

    return None


def check_conda_env() -> None:
    """Check if conda env is activated."""
    if "CONDA_PREFIX" not in os.environ:
        raise RuntimeError("Please activate conda env first.")


def check_hts_path(hts_lib_path: Path, hts_include_path: Path) -> None:
    """Check if htslib path is valid."""
    header_path = hts_include_path / "htslib"
    if not header_path.exists():
        raise RuntimeError("Please install htslib first.")

    lib_path_linux = hts_lib_path / "libhts.so"
    lib_path_macos = hts_lib_path / "libhts.dylib"
    lib_path_static = hts_lib_path / "libhts.a"

    if (
        not lib_path_linux.exists()
        and not lib_path_static.exists()
        and not lib_path_macos.exists()
    ):
        raise RuntimeError("Please install htslib first.")


def get_hts_lib_path() -> tuple[Path, Path]:
    """Get htslib path."""
    remove_env("-g")
    check_conda_env()
    conda_path = Path(os.environ["CONDA_PREFIX"])

    htslib_library_dir = conda_path / "lib"
    htslib_include_dir = conda_path / "include"

    check_hts_path(htslib_library_dir, htslib_include_dir)

    return htslib_library_dir, htslib_include_dir


@contextmanager
def change_dir(path: str):
    """Change directory."""
    save_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(save_dir)


def change_env(key: str, value: str):
    """Change environment variable."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            old_env = os.environ.get(key, None)
            os.environ[key] = old_env + " " + value if old_env else value
            func(*args, **kwargs)
            os.environ[key] = old_env if old_env else " "

        return wrapper

    return decorator


def get_files(
    path: typing.Union[Path, str], suffix: typing.List[str]
) -> typing.Iterator[str]:
    """Get bindings."""
    if isinstance(path, str):
        path = Path(path)

    for file in path.iterdir():
        if file.is_dir():
            yield from get_files(file, suffix)
        if file.suffix in suffix:
            yield file.as_posix()


def filter_files(files, exclude=None):
    if exclude is None:
        exclude = []

    for file in files:
        file_name = Path(file).name
        if file_name not in exclude:
            yield file


def get_extra_options():
    return [
        "-g",
        "-D_FILE_OFFSET_BITS=64",
        "-D_LARGEFILE_SOURCE",
        "-D_GNU_SOURCE",
        "-DMACHTYPE_$(MACHTYPE)",
        # "-DDBG_MACRO_DISABLE",
    ]


SOURCES = (
    [
        "src/pxblat/extc/bindings/faToTwoBit.cpp",
        "src/pxblat/extc/bindings/gfServer.cpp",
        "src/pxblat/extc/bindings/pygfServer.cpp",
        "src/pxblat/extc/bindings/gfClient.cpp",
        "src/pxblat/extc/bindings/gfClient2.cpp",
    ]
    + list(filter_files(get_files("src/pxblat/extc/bindings/binder", [".cpp"])))
    + list(filter_files(get_files("src/pxblat/extc/src/core", [".c"])))
    + list(
        filter_files(get_files("src/pxblat/extc/src/aux", [".c"]), exclude=["net.c"])
    )
    + list(filter_files(get_files("src/pxblat/extc/src/net", [".c"])))
)


def build(setup_kwargs):
    """Build cpp extension."""
    ext_modules = [
        Pybind11Extension(
            "pxblat._extc",
            language="c++",
            sources=SOURCES,
            include_dirs=header_path
            + [
                "src/pxblat/extc/include/core",
                "src/pxblat/extc/include/aux",
                "src/pxblat/extc/include/net",
                "src/pxblat/extc/bindings",
            ],
            library_dirs=lib_path,
            libraries=external_htslib_libraries,
            extra_compile_args=get_extra_options(),
        )
    ]
    setup_kwargs.update(
        {
            "ext_modules": ext_modules,
            "cmdclass": {"build_ext": build_ext},
            "zip_safe": False,
        }
    )
