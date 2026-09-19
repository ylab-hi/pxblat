# binder/ — generated pybind11 bindings

Everything in this directory except `.clang-format` is **generated code**:
do not hand-edit `_extc.cpp`, `_extc.modules`, `_extc.sources`,
`faToTwoBit.cpp`, `gfClient.cpp`, `gfServer.cpp`, `gfServer_1.cpp`,
`pygfServer.cpp`, or `twoBitToFa.cpp`. Edits made directly to those files
are silently discarded the next time the bindings are regenerated. If a
binding needs to change, change its C++ source under
`src/pxblat/extc/bindings/*.hpp` / `*.cpp` (the project-authored files one
directory up) and regenerate. `.clang-format` here is a small hand-maintained
sentinel (`DisableFormat: true`) that tells clang-format-aware tooling to
leave this generated output alone; it is not itself binder output.

## What this is

The files here are produced by [RosettaCommons/binder](https://github.com/RosettaCommons/binder),
a tool that parses C++ headers via libclang and emits one pybind11 `.cpp`
translation unit per input header, plus a root module (`_extc.cpp`) that
wires all of the per-header `bind_*` functions together into the single
`pxblat._extc` extension module. `_extc.modules` and `_extc.sources` are
binder's own manifest of the namespaces and generated source files it
produced, consumed by `build.py` to decide what to compile and how to name
the pybind11 submodules.

## Inputs

- `all_includes.hpp` (repo root) — the umbrella header binder parses. It
  `#include`s every project-authored bindings header
  (`gfClient.hpp`, `gfServer.hpp`, `pygfServer.hpp`, `faToTwoBit.hpp`,
  `twoBitToFa.hpp`, ...) plus the standard library headers those headers
  transitively need. Add a new header here when a new bindings file needs to
  be exposed to Python.
- `binder.cfg` (repo root) — binder's
  [config file](https://cppbinder.readthedocs.io/en/latest/config.html#command-line-options):
  restricts binding generation to the `cppbinding` namespace and excludes
  (`-function cppbinding::...`) internal helpers that should stay C++-only
  (error/socket plumbing, dynamic-server internals, etc.).

## How to regenerate

The `binder` target in the repo's `Makefile` runs binder inside the
`yangliz5/binder-pxblat` container image (built from the project's
`Dockerfile`, which installs binder + a matching libclang) via Singularity:

```sh
make binder
```

which expands to:

```sh
singularity run -B .:/bind docker://yangliz5/binder-pxblat \
    binder --root-module _extc \
    --prefix /bind/src/pxblat/extc/bindings/binder \
    --config /bind/binder.cfg \
    --include-pybind11-stl \
    /bind/all_includes.hpp \
    -- -I/bind/src/pxblat/extc/include/core \
    -I/bind/src/pxblat/extc/include/aux \
    -I/bind/src/pxblat/extc/include/net \
    -I/bind/src/pxblat/extc/bindings \
    --std=c++17 \
    -DNDEBUG
```

`-B .:/bind` bind-mounts the repo root into the container at `/bind`, so
`--prefix` writes straight back into this directory (`git diff` afterward
shows exactly what changed). The trailing `-I...`/`--std=c++17`/`-DNDEBUG`
arguments after `--` are the compiler flags binder hands to libclang so it
can actually parse `all_includes.hpp` and everything it pulls in; they must
stay in sync with the real build flags in `build.py`
(`_include_dirs_for_pxblat`/`_extra_compile_args_for_pxblat`).

After regenerating, review the diff, then rebuild the extension (`poetry
install` / `pip install -e .`) to confirm the new bindings compile and the
Python-visible API (`src/pxblat/extc/__init__.pyi`, regenerated separately
via `make stubs`) still matches what callers expect.

## Why Singularity instead of plain `docker run`

The image is pulled straight from Docker Hub (`docker://yangliz5/binder-pxblat`);
Singularity's `docker://` transport lets contributors on shared/HPC-style
Linux hosts (where a Docker daemon usually is not available or not
permitted) run the same container without root or a running daemon.
Anyone with a working Docker install can run the equivalent
`docker run --rm -v "$PWD:/bind" yangliz5/binder-pxblat binder ...` command
directly, using the same `binder ...` arguments as above.
