# Migration Guide: Poetry to uv

This document provides guidance for developers migrating from Poetry to uv for the pxblat project.

## Overview

As of version 1.2.1, pxblat has migrated from [Poetry](https://python-poetry.org/) to [uv](https://docs.astral.sh/uv/), a fast Python package installer and resolver. This migration provides:

- **Faster dependency resolution** - uv is 10-100x faster than pip/poetry
- **Better compatibility** - Standard PEP 621 `pyproject.toml` format
- **Simpler tooling** - One tool for installation, locking, and running
- **Better CI/CD integration** - Native GitHub Actions support

## What Changed

### 1. Project Configuration (`pyproject.toml`)

- Migrated from Poetry-specific format to PEP 621 standard
- Replaced `[tool.poetry]` with `[project]`
- Replaced `[tool.poetry.dependencies]` with `[project.dependencies]`
- Replaced `[tool.poetry.group.dev.dependencies]` with `[dependency-groups]`
- Changed build backend from `poetry-core` to `setuptools`

### 2. Lock File

- `poetry.lock` → `uv.lock`

### 3. Nox Integration

- Removed `nox-poetry` dependency
- Updated `noxfile.py` to use standard nox with uv

### 4. GitHub Actions

- Replaced Poetry installation steps with uv
- Updated workflows to use `astral-sh/setup-uv@v5`

## Migration Steps for Developers

### Prerequisites

Install uv:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Step 1: Update Your Local Repository

```bash
# Pull the latest changes
git pull origin main

# Remove old Poetry virtual environment (optional)
rm -rf .venv
```

### Step 2: Install Dependencies

Instead of `poetry install`, use:

```bash
# Install all dependencies including dev dependencies
uv sync

# Install without dev dependencies
uv sync --no-dev

# Install specific dependency groups
uv sync --group dev
```

### Step 3: Running Commands

| Poetry Command                   | uv Equivalent          |
| -------------------------------- | ---------------------- |
| `poetry run python`              | `uv run python`        |
| `poetry run pxblat`              | `uv run pxblat`        |
| `poetry run pytest`              | `uv run pytest`        |
| `poetry add package`             | `uv add package`       |
| `poetry add --group dev package` | `uv add --dev package` |
| `poetry remove package`          | `uv remove package`    |
| `poetry lock`                    | `uv lock`              |
| `poetry build`                   | `uv build`             |
| `poetry publish`                 | `uv publish`           |

### Step 4: Running Tests with Nox

No changes needed! Nox commands remain the same:

```bash
# Run all tests
nox

# Run specific session
nox -s tests

# Run for specific Python version
nox -s tests --python=3.10
```

## Command Reference

### Essential uv Commands

```bash
# Sync dependencies from uv.lock
uv sync

# Add a new dependency
uv add requests

# Add a development dependency
uv add --dev pytest

# Remove a dependency
uv remove requests

# Update dependencies
uv lock --upgrade

# Run a command in the virtual environment
uv run python script.py

# Build the package
uv build

# Publish to PyPI
uv publish
```

### Working with Virtual Environments

```bash
# Create a virtual environment (done automatically by uv sync)
uv venv

# Activate virtual environment manually (if needed)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install package in editable mode
uv pip install -e .
```

## CI/CD Changes

If you maintain forks or custom workflows:

### GitHub Actions Example

```yaml
- name: Set up Python
  uses: actions/setup-python@v6
  with:
    python-version: "3.10"

- name: Install uv
  uses: astral-sh/setup-uv@v5
  with:
    enable-cache: true
    cache-dependency-glob: "uv.lock"

- name: Install dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest
```

## Troubleshooting

### Issue: "uv: command not found"

**Solution**: Make sure uv is installed and in your PATH:

```bash
# Check installation
which uv  # macOS/Linux
where uv  # Windows

# Add to PATH if needed (macOS/Linux)
export PATH="$HOME/.local/bin:$PATH"
```

### Issue: Dependencies not resolving

**Solution**: Try updating the lock file:

```bash
uv lock --upgrade
```

### Issue: Virtual environment issues

**Solution**: Remove and recreate:

```bash
rm -rf .venv
uv sync
```

### Issue: Build failures

**Solution**: Ensure build dependencies are available:

```bash
# uv installs build dependencies automatically during build
uv build

# Or install them explicitly
uv sync --all-extras
```

## Benefits of uv

1. **Speed**: 10-100x faster than pip and significantly faster than Poetry
2. **Standards-based**: Uses PEP 621 `pyproject.toml` format
3. **Single tool**: Handles package installation, virtual environments, and project management
4. **Better resolution**: Improved dependency conflict resolution
5. **Active development**: Backed by Astral (creators of Ruff)

## Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [PEP 621 Specification](https://peps.python.org/pep-0621/)
- [Project pyproject.toml](./pyproject.toml)

## Questions?

If you encounter any issues during the migration, please:

1. Check this guide first
2. Review the [uv documentation](https://docs.astral.sh/uv/)
3. Open an issue on the [pxblat repository](https://github.com/ylab-hi/pxblat/issues)

---

**Note**: This migration maintains full backward compatibility with the package API. Only the development workflow and tooling have changed.
