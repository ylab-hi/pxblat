"""Nox sessions."""
import os
import shutil
import sys
from pathlib import Path
from textwrap import dedent

import glob
import os

import nox

try:
    from nox_poetry import Session, session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None


package = "pxblat"
python_versions = ["3.11", "3.10", "3.9"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = (
    "pre-commit",
    "safety",
    "mypy",
    "tests",
    "docs-build",
)
DEBUG = False


def poetry_install():
    if DEBUG:
        return ["poetry", "install", "-vvv"]
    else:
        return ["poetry", "install"]


def activate_virtualenv_in_precommit_hooks(session: Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Args:
        session: The Session object.
    """
    assert session.bin is not None  # noqa: S101

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        text = hook.read_text()
        bindir = repr(session.bin)[1:-1]  # strip quotes
        if not (
            Path("A") == Path("a") and bindir.lower() in text.lower() or bindir in text
        ):
            continue

        lines = text.splitlines()
        if not (lines[0].startswith("#!") and "python" in lines[0].lower()):
            continue

        header = dedent(
            f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """
        )

        lines.insert(1, header)
        hook.write_text("\n".join(lines))

def find_wheel(dist_dir='dist'):
    # The pattern to match wheel files
    pattern = os.path.join(dist_dir, '*.whl')

    # Use glob to find all wheel files in the dist directory
    wheel_files = glob.glob(pattern)

    if not wheel_files:
        raise FileNotFoundError(f"No wheel files found in {dist_dir}")

    # Assuming you want the first wheel file found
    # If you have multiple wheel files, you may need to add logic to select the correct one
    wheel_file = wheel_files[0]

    return Path(wheel_file)

@session(python=python_versions)
def build_wheel(session: Session) -> None:
    """Run the test suite."""
    session.run("make", "clean", external=True)
    session.run("poetry","install","--no-dev", external=True)
    session.run("rm", "-rf", "fixed_wheels", external=True)
    session.run("poetry", "build", external=True)
    session.install("delocate", "pybind11", "wheel")
    wheel_location = find_wheel()
    print(f'Wheel file located at: {wheel_location}')
    session.run("delocate-listdeps", wheel_location.as_posix())
    session.run("delocate-wheel", "-w", "fixed_wheels", "-v", wheel_location.as_posix())
    new_wheel_location = find_wheel('fixed_wheels')
    session.run("mv", new_wheel_location.as_posix(), wheel_location.parent.as_posix(), external=True)
    session.run("rm", "-rf", "fixed_wheels", external=True)
    session.run("delocate-listdeps", wheel_location.as_posix())
    session.run("poetry", "publish", "--skip-existing", external=True)


@session(name="pre-commit", python="3.10")
def precommit(session: Session) -> None:
    """Lint using pre-commit."""
    args = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]
    session.install(
        "black",
        "darglint",
        "pep8-naming",
        "pre-commit",
        "pre-commit-hooks",
        "reorder-python-imports",
    )
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@session(python="3.10")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", "--full-report", f"--file={requirements}")


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["src", "tests", "docs/conf.py"]
    session.run(*poetry_install(), external=True)
    session.install("mypy", "pytest")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.run(*poetry_install(), external=True)
    session.install("coverage[toml]", "pytest", "pygments")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@session
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(name="docs-build", python="3.10")
def docs_build(session: Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    if not session.posargs and "FORCE_COLOR" in os.environ:
        args.insert(0, "--color")

    session.run(*poetry_install(), external=True)

    session.install(
        "sphinx",
        "sphinx-immaterial",
        "sphinx-autobuild",
        "sphinx-click",
        "myst_parser",
        "pyyaml",
    )

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@nox.session
def linkcheck(session: Session) -> None:
    """Build the documentation."""
    args = session.posargs or [
        "-b",
        "linkcheck",
        "-W",
        "--keep-going",
        "docs",
        "docs/_build",
    ]

    builddir = Path("docs", "_build")
    if builddir.exists():
        shutil.rmtree(builddir)

    session.install("-r", "docs/requirements.txt")

    session.run("sphinx-build", *args)


@session(python="3.10")
def docs(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.run(*poetry_install(), external=True)
    session.install(
        "sphinx",
        "sphinx-immaterial",
        "sphinx-autobuild",
        "sphinx-click",
        "myst_parser",
        "pyyaml",
    )

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
