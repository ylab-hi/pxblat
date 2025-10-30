"""Setup script for pxblat with custom pybind11 build."""
import sys
from pathlib import Path
from setuptools import setup

# Add the current directory to the path to ensure build.py can be imported
sys.path.insert(0, str(Path(__file__).parent.resolve()))

# Import and run the build configuration
import build as build_module

# Configuration dictionary
setup_kwargs = {}

# Call the custom build function from build.py
build_module.build(setup_kwargs)

# Run setup with combined configuration
setup(
    **setup_kwargs,
)
