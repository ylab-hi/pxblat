from __future__ import annotations
import os
import sys
import typing
import subprocess
from ctypes.util import find_library
from pathlib import Path

import setuptools
from pybind11.setup_helpers import auto_cpp_level
from pybind11.setup_helpers import ParallelCompile
from pybind11.setup_helpers import Pybind11Extension
from setuptools import Distribution
from setuptools import Extension
from setuptools.command.build_ext import build_ext as _build_ext


DEBUG = False

class PxblatExtensionBuilder(_build_ext):
    def build_extension(self, extension: setuptools.extension.Extension) -> None:  # type: ignore
        extension.library_dirs.append(self.build_lib)  # type: ignore
        super().build_extension(extension)

    def build_extensions(self) -> None:
        """
        Build extensions, injecting C++ std for Pybind11Extension if needed.
        """

        if sys.platform == "darwin":
            # LDSHARED on macOS carries "-bundle", which clashes with the
            # "-dynamiclib" libpxblat needs. Strip it from the customized
            # compiler; each extension re-adds the flag it wants via
            # extra_link_args. Mutating sysconfig's LDSHARED instead is not
            # reliable across setuptools versions (broke with 82.x).
            for attr in ("linker_so", "linker_so_cxx"):
                linker = getattr(self.compiler, attr, None)
                if linker:
                    setattr(self.compiler, attr, [a for a in linker if a != "-bundle"])

        for ext in self.extensions:
            if hasattr(ext, "_cxx_level") and ext._cxx_level == 0:
                ext.cxx_std = auto_cpp_level(self.compiler)

        super().build_extensions()


def _get_pxblat_libname():
    builder = setuptools.command.build_ext.build_ext(Distribution())  # type: ignore
    full_name = builder.get_ext_filename("libpxblat")
    without_lib = full_name.split("lib", 1)[-1]
    without_so = without_lib.rsplit(".so", 1)[0]
    return without_so


def get_files_by_suffix(
    path: typing.Union[Path, str], suffix: typing.List[str]
) -> typing.Iterator[str]:
    """Get bindings."""
    if isinstance(path, str):
        path = Path(path)

    for file in path.iterdir():
        if file.is_dir():
            yield from get_files_by_suffix(file, suffix)
        if file.suffix in suffix:
            yield file.as_posix()


def filter_files(files, exclude=None):
    if exclude is None:
        exclude = []

    for file in files:
        file_name = Path(file).name
        if file_name not in exclude:
            yield file


# Optional multithreaded build
def get_thread_count():
    try:
        import multiprocessing

        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass
    return 1


def _prefix_dirs(prefix: Path) -> tuple[Path, Path] | None:
    """Return (lib_dir, include_dir) under an install prefix if both exist."""
    lib_dir, include_dir = prefix / "lib", prefix / "include"
    if lib_dir.is_dir() and include_dir.is_dir():
        return lib_dir, include_dir
    return None


def find_library_dirs(lib_name: str) -> tuple[Path, Path] | None:
    """Locate non-default -L/-I directories for ``lib_name``.

    Returns None when the library lives in the toolchain's default search
    path (the common case on Linux, where ``ctypes.util.find_library`` yields
    a bare soname such as ``libssl.so.3`` with no directory), so nothing needs
    to be added. Raises when the library cannot be found at all.
    """
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        found = _prefix_dirs(Path(conda_prefix))
        if found and any((found[0] / f"lib{lib_name}{ext}").exists() for ext in (".so", ".dylib", ".a")):
            print(f"{lib_name}: using CONDA_PREFIX {conda_prefix}")
            return found

    lib_path = find_library(lib_name)
    print(f"{lib_name} lib_path: {lib_path}")
    if lib_path is None:
        raise RuntimeError(
            f"Cannot find the {lib_name} library. Install the OpenSSL development package "
            "(libssl-dev / openssl-devel / brew install openssl) and retry."
        )

    path = Path(lib_path)
    if not path.is_absolute():
        return None
    return _prefix_dirs(path.parent.parent)


def find_openssl_libs_header() -> tuple[list[str], list[str]]:
    """Return extra (-L, -I) dirs for Homebrew's OpenSSL on macOS, if installed."""
    from shutil import which

    if sys.platform != "darwin" or not which("brew"):
        return [], []

    proc = subprocess.run(["brew", "--prefix", "openssl"], capture_output=True, text=True)
    if proc.returncode != 0:
        print("brew --prefix openssl failed; relying on default search paths")
        return [], []

    found = _prefix_dirs(Path(proc.stdout.strip()))
    if found is None:
        print("Homebrew openssl prefix has no lib/ and include/; relying on default search paths")
        return [], []

    print(f"Using Homebrew openssl at {found[0].parent}")
    return [found[0].as_posix()], [found[1].as_posix()]


def _extra_compile_args_for_libpxblat():
    # kent's MACHTYPE_* macros only special-case ppc/alpha, which we do not target.
    return [
        "-D_FILE_OFFSET_BITS=64",
        "-D_LARGEFILE_SOURCE",
        "-D_GNU_SOURCE",
        "-DPXBLATLIB",
    ]


def _include_dirs_for_libpxblat():
    return [
        "src/pxblat/extc/include/core",
        "src/pxblat/extc/include/aux",
        "src/pxblat/extc/include/net",
    ]


def _include_dirs_for_pxblat():
    return [
        "src/pxblat/extc/bindings",
    ]


def _extra_compile_args_for_pxblat():
    flag = []
    if not DEBUG:
        flag.append("-DDBG_MACRO_DISABLE")
    return flag


ParallelCompile(f"{get_thread_count()}").install()


openssl_lib, openssl_include = find_openssl_libs_header()

extra_compile_args = ["-pthread"]
hidden_visibility_args = []
include_dirs: list[str] = [] + openssl_include
library_dirs: list[str] = [] + openssl_lib
python_module_link_args = []
base_library_link_args: list[str] = []
external_libraries = [
    "ssl",
    "crypto",
    "m",
]

for lib in ("ssl", "crypto"):
    found = find_library_dirs(lib)
    if found is not None:
        lib_dir, include_dir = (p.as_posix() for p in found)
        if lib_dir not in library_dirs:
            library_dirs.append(lib_dir)
        if include_dir not in include_dirs:
            include_dirs.append(include_dir)

if sys.platform == "win32":
    raise RuntimeError("Windows is not supported.")
elif sys.platform == "darwin":
    # See https://conda-forge.org/docs/maintainer/knowledge_base.html#newer-c-features-with-old-sdk
    extra_compile_args.append("-D_LIBCPP_DISABLE_AVAILABILITY")
    extra_compile_args.append("-undefined dynamic_lookup")
    hidden_visibility_args.append("-fvisibility=hidden")
    python_module_link_args.append("-bundle")
    builder = setuptools.command.build_ext.build_ext(Distribution())  # type: ignore
    full_name = builder.get_ext_filename("libpxblat")
    print(f"full_name: {full_name}")
    base_library_link_args.append(
        f"-Wl,-dylib_install_name,@loader_path/../{full_name}"
    )
    base_library_link_args.append("-dynamiclib")
else:
    hidden_visibility_args.append("-fvisibility=hidden")
    python_module_link_args.append("-Wl,-rpath,$ORIGIN/..")


def get_extension_modules():
    extension_modules = []

    """
    Extension module which is actually a plain C++ library without Python bindings
    """
    libpxblat_sources = (
        list(filter_files(get_files_by_suffix("src/pxblat/extc/src/core", [".c"])))
        + list(
            filter_files(
                get_files_by_suffix("src/pxblat/extc/src/aux", [".c"]),
                exclude=["net.c"],
            )
        )
        + list(filter_files(get_files_by_suffix("src/pxblat/extc/src/net", [".c"])))
    )

    pxblat_library = Extension(
        "libpxblat",
        language="c",
        sources=libpxblat_sources,
        include_dirs=include_dirs + _include_dirs_for_libpxblat(),
        extra_compile_args=_extra_compile_args_for_libpxblat() + extra_compile_args,
        extra_link_args=base_library_link_args,
        libraries=external_libraries,
        library_dirs=library_dirs,
    )

    pxblat_libs = [_get_pxblat_libname()]
    extension_modules.append(pxblat_library)

    """
    An extension module which contains the main Python bindings for libblat
    """
    pxblat_python_sources = [
        "src/pxblat/extc/bindings/faToTwoBit.cpp",
        "src/pxblat/extc/bindings/twoBitToFa.cpp",
        "src/pxblat/extc/bindings/gfServer.cpp",
        "src/pxblat/extc/bindings/pygfServer.cpp",
        "src/pxblat/extc/bindings/gfClient.cpp",
    ] + list(
        filter_files(get_files_by_suffix("src/pxblat/extc/bindings/binder", [".cpp"]))
    )

    pxblat_python = Pybind11Extension(
        "pxblat._extc",
        language="c++",
        sources=pxblat_python_sources,
        include_dirs=include_dirs
        + _include_dirs_for_libpxblat()
        + _include_dirs_for_pxblat(),
        extra_compile_args=extra_compile_args
        + hidden_visibility_args
        + _extra_compile_args_for_pxblat(),
        libraries=external_libraries + pxblat_libs,
        extra_link_args=python_module_link_args,
        library_dirs=library_dirs,
    )

    extension_modules.append(pxblat_python)
    return extension_modules


def build(setup_kwargs):
    """Build cpp extension."""
    ext_modules = get_extension_modules()
    setup_kwargs.update(
        {
            "ext_modules": ext_modules,
            "cmdclass": {"build_ext": PxblatExtensionBuilder},
            "zip_safe": False,
            "package_data": {"pxblat": ["py.typed", "*so"]},
        }
    )
