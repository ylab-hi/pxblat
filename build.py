from __future__ import annotations
import os
import shlex
import sys
import typing
import subprocess
from contextlib import contextmanager
from ctypes.util import find_library
from functools import wraps
from pathlib import Path

import distutils
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


def remove_env(key: str):
    """Remove environment variable."""
    env_cflags = os.environ.get("CFLAGS", "")
    env_cppflags = os.environ.get("CPPFLAGS", "")
    flags = shlex.split(env_cflags) + shlex.split(env_cppflags)

    for flag in flags:
        if flag.startswith(key):
            raise RuntimeError(f"Please remove {key} from CFLAGS and CPPFLAGS.")


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


def _get_cxx_compiler():
    cc = distutils.ccompiler.new_compiler()  # type: ignore
    distutils.sysconfig.customize_compiler(cc)  # type: ignore
    return cc.compiler_cxx[0]  # type: ignore


def find_lib_in_conda(lib_name: str):
    conda_prefix = os.environ.get("CONDA_PREFIX", None)
    if conda_prefix is not None:
        conda_lib_dir = Path(conda_prefix) / "lib"

        if (conda_lib_dir / f"lib{lib_name}.a").exists():
            return conda_lib_dir

        if (conda_lib_dir / f"lib{lib_name}.so").exists():
            return conda_lib_dir

        if (conda_lib_dir / f"lib{lib_name}.dylib").exists():
            return conda_lib_dir

    return None


def find_available_library(lib_name: str, *, ignores=[]):
    lib_path = find_library(lib_name)

    if lib_path is None:
        lib_path = find_lib_in_conda(lib_name)

    print(f"{lib_name} lib_path: {lib_path}")

    if not lib_path:
        if lib_name not in ignores:
            raise RuntimeError(f"Cannot find {lib_name} library.")
        return Path.cwd(), Path.cwd()

    header_path = Path(lib_path).parent.parent / "include"

    return Path(lib_path).parent, header_path


def find_openssl_libs_header():
    from shutil import which
    import platform

    current_platform = platform.system().lower()

    lib_paths = []
    head_paths = []

    if current_platform == "darwin" and which("brew"):
        openssl_dir = subprocess.getoutput('brew --prefix openssl')

        lib_paths.append(f"{openssl_dir}/lib")
        head_paths.append(f"{openssl_dir}/include")

        if not Path(lib_paths[0]).exists():
            print(f"Cannot find openssl lib in {lib_paths[0]}")
        else:
            print(f"Find openssl lib_paths: {lib_paths}")

        if not Path(head_paths[0]).exists():
            print(f"Cannot find openssl include in {head_paths[0]}")
        else:
            print(f"Find openssl include: {head_paths}")

    return lib_paths, head_paths


def _extra_compile_args_for_libpxblat():
    return [
        "-D_FILE_OFFSET_BITS=64",
        "-D_LARGEFILE_SOURCE",
        "-D_GNU_SOURCE",
        "-DMACHTYPE_$(MACHTYPE)",
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

for lib in external_libraries:
    lib_library_dir, lib_include_dir = find_available_library(lib, ignores=["m"])
    library_dirs.append(lib_library_dir.as_posix())
    include_dirs.append(lib_include_dir.as_posix())

if sys.platform == "win32":
    raise RuntimeError("Windows is not supported.")
elif sys.platform == "darwin":
    # See https://conda-forge.org/docs/maintainer/knowledge_base.html#newer-c-features-with-old-sdk
    extra_compile_args.append("-D_LIBCPP_DISABLE_AVAILABILITY")
    extra_compile_args.append("-undefined dynamic_lookup")
    hidden_visibility_args.append("-fvisibility=hidden")
    config_vars = distutils.sysconfig.get_config_vars()  # type: ignore
    config_vars["LDSHARED"] = config_vars["LDSHARED"].replace("-bundle", "")  # type: ignore
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
