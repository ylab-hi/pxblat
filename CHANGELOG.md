# Changelog

All notable changes to this project will be documented in this file.

## [1.2.3] - 2025-10-29

### Bug Fixes

- Fix module shadowing issue in cibuildwheel by setting `CIBW_BUILD_FRONTEND: pip`
- Prevent project's `build.py` from being executed instead of PyPA `build` package
- Fix `ModuleNotFoundError: No module named 'setuptools'` in wheel builds

### Build

- Add `CIBW_BUILD_FRONTEND: pip` to all three cibuildwheel jobs (Linux, macOS x86_64, macOS ARM64)
- Ensure Poetry build system works correctly with cibuildwheel

## [1.2.2] - 2025-10-29

### Bug Fixes

- Fix artifact upload/download for GitHub Actions with actions/download-artifact@v6
- Add unique names to all artifacts (sdist and wheels)
- Update artifact download pattern matching and merging
- Fix packages_dir path from artifact/ to dist/
- Fix pypa/gh-action-pypi-publish parameter names (skip-existing, packages-dir)

### Build

- Named artifacts for better organization: dist, wheels-linux-_, wheels-macos-_, wheels-macos-arm64-\*
- Implement two-step artifact download with pattern matching
- Merge multiple wheel artifacts into single dist/ directory

## [1.2.0] - 2024-05-15

### Bug Fixes

- Update sphinx-immaterial version to ^0.11.11

### Features

- Add build_index function to generate precomputed index

### Miscellaneous Tasks

- Remove pysam for dev dependencies
- Add workflow step for listing workflows folder

### Styling

- Update pipx install commands in tests workflow
- Update Poetry and Nox installation commands
- Add type ignore to deprecated import

### Build

- Bump setuptools from 69.0.3 to 69.1.0
- Bump ruff from 0.2.1 to 0.2.2
- Bump pytest from 8.0.0 to 8.0.1
- Bump urllib3 from 2.2.0 to 2.2.1
- Bump virtualenv in /.github/workflows
- Bump poetry from 1.7.1 to 1.8.0 in /.github/workflows
- Bump pytest from 8.0.1 to 8.0.2
- Bump setuptools from 69.1.0 to 69.1.1
- Bump rich from 13.7.0 to 13.7.1
- Bump pypa/gh-action-pypi-publish from 1.8.11 to 1.8.12
- Bump poetry from 1.8.0 to 1.8.1 in /.github/workflows
- Bump ruff from 0.2.2 to 0.3.0
- Bump poetry from 1.8.1 to 1.8.2 in /.github/workflows
- Bump nox from 2023.4.22 to 2024.3.2 in /.github/workflows
- Bump pytest from 8.0.2 to 8.1.0
- Bump nox from 2023.4.22 to 2024.3.2
- Bump pybind11-stubgen from 2.4.2 to 2.5
- Bump ruff from 0.3.0 to 0.3.1
- Bump pypa/cibuildwheel from 2.16.5 to 2.17.0
- Bump pypa/gh-action-pypi-publish from 1.8.12 to 1.8.14
- Bump setuptools from 69.1.1 to 69.2.0
- Bump ruff from 0.3.2 to 0.3.3
- Bump ruff from 0.3.3 to 0.3.4
- Bump typer from 0.9.0 to 0.10.0
- Bump delocate from 0.10.7 to 0.11.0 (#286)
- Bump typer from 0.10.0 to 0.11.0
- Bump typer from 0.11.0 to 0.11.1
- Bump pybind11-stubgen from 2.5 to 2.5.1
- Bump pybind11 from 2.11.1 to 2.12.0
- Bump typer from 0.11.1 to 0.12.0
- Bump typer from 0.12.0 to 0.12.3
- Bump sphinx-autobuild from 2024.2.4 to 2024.4.13
- Bump ruff from 0.3.4 to 0.3.7
- Bump setuptools from 69.2.0 to 69.5.1
- Bump nox from 2024.3.2 to 2024.4.15
- Bump nox from 2024.3.2 to 2024.4.15 in /.github/workflows
- Bump sphinx-autobuild from 2024.4.13 to 2024.4.16
- Bump virtualenv in /.github/workflows
- Bump sphinx from 7.2.6 to 7.3.6
- Bump virtualenv in /.github/workflows
- Bump sphinx from 7.3.6 to 7.3.7
- Bump ruff from 0.3.7 to 0.4.0
- Bump ruff from 0.4.0 to 0.4.1
- Bump virtualenv in /.github/workflows
- Bump myst-parser from 2.0.0 to 3.0.0 in /docs
- Bump myst-parser from 2.0.0 to 3.0.0
- Bump mypy from 1.9.0 to 1.10.0
- Bump ruff from 0.4.1 to 0.4.2
- Bump virtualenv in /.github/workflows
- Bump myst-parser from 3.0.0 to 3.0.1 in /docs
- Bump pytest from 8.1.1 to 8.2.0
- Bump pytest-xdist from 3.5.0 to 3.6.1
- Bump myst-parser from 3.0.0 to 3.0.1
- Bump mashumaro from 3.12 to 3.13
- Bump poetry from 1.8.2 to 1.8.3 in /.github/workflows
- Bump virtualenv in /.github/workflows
- Bump sphinx-click from 5.1.0 to 5.2.2
- Update pre-commit hooks and dependencies

### Ci

- Add step to check current directory

## [1.1.9] - 2023-11-01

### Bug Fixes

- Fix import error in fa2twobit.py

### Documentation

- Update installation.md with bug reporting information
- Update tutorial.md and pyproject.toml files

### Features

- Update version to 1.1.2
- Add skip test for macOS arm64 in CI workflow
- Add script to find library path
- Use setuppy
- Install cibuildwheel and build wheels
- Remove setuppy

### Miscellaneous Tasks

- Comment out dependency installation step
- Remove unused code
- Remove unnecessary steps
- Update release.yml and pyproject.toml files
- Update Python version requirements
- Add Python 3.8 to python_versions
- Update Python version and import annotations
- Update test matrix
- Update release and test workflow
- Bump version to 1.1.3
- Update Python version requirement
- Bump version to 1.1.4
- Bump version to 1.1.5
- Update version to 1.1.6
- Update version to 1.1.7
- Comment out unnecessary code in release.yml
- Remove build_wheels_linux step
- Update pypa/cibuildwheel to v2.16.2
- Update build_wheels_linux and build_wheels_macos configurations
- Update version to 1.1.8
- Update Python versions and dependencies
- Update release workflow
- Update find_lib.py script
- Update release.yml file
- Update release.yml to remove unnecessary code
- Update release.yml file
- Update version to 1.1.9

### Refactor

- Remove unnecessary code and add RAISE_ERROR flag
- Remove unused variable and print statements
- Refactor setup.py code
- Comment out unnecessary code lines

### Styling

- Update code style badge
- Import fix

### Build

- Add DYLD_LIBRARY_PATH to delocate commands
- Remove unnecessary build configurations
- Remove numpy dependency
- Update manylinux images for macOS job
- Update cibw_build options and delocate-wheel command
- Update macOS deployment target to 12.0
- Add delocate as a dependency for cibuildwheel
- Update macOS version and architecture for cibuildwheel
- Configure Homebrew and Install Dependencies
- Install openssl@3 using Homebrew

### Build_wheels_macos

- Enable build_wheels_macos_arm64

## [1.1.1] - 2023-10-27

### Features

- Add find_openssl_libs() function

### Miscellaneous Tasks

- Update version to 1.1.1

### Styling

- Remove unused library "z"

### Ci

- Update release workflow to skip if no tag

## [1.1.0] - 2023-10-27

### Bug Fixes

- Uncomment "hts" external library

### Features

- Update version to 1.1.0

### Miscellaneous Tasks

- Remove unused external library
- Remove unnecessary installation of htslib and update OpenSSL dependencies

### Refactor

- Comment out unused code in build.py and linefile.c

### Build

- Update package dependencies and installation

## [1.0.3] - 2023-10-27

### Documentation

- Update README.md with documentation links and instructions
- Update URLs in README and pyproject.toml
- Update changelog for v1.0.1

### Miscellaneous Tasks

- Update upload_to_test_pypi step
- Add update command in Makefile
- Add concurrency settings for workflows
- Update version to 1.0.1
- Update version to 1.0.2
- Update version to 1.0.2
- Update version to 1.0.3

### Styling

- Update ruff-pre-commit to v0.1.3

### Build

- Remove depdendency

## [1.0.0] - 2023-10-25

### Bug Fixes

- Validate two_bit file before starting server
- Fix logic bug in \_cpsl function

### Documentation

- Update version number to v0.3.10
- Update installation guide and compatibility matrix
- Rewrite toturial
- Update tutorial and conf.py
- Add code example for turorial
- Update README.md
- Polish tutorial
- Update link in tutorial
- Update tutorial.md with proper Python script execution and comments
- Add CLI documentation link to tutorial.md

### Features

- Add optional parameters to `Server` constructor
- Add new options for starting the server
- Add server option 'can stop' and 'step size'
- Add documentation for Client class and methods
- Add Pure Python BLAT code for creating our own `BLAT`

### Miscellaneous Tasks

- Bump actions/checkout from 3 to 4
- Bump virtualenv in /.github/workflows
- Bump docker/setup-qemu-action from 2 to 3
- Bump pypa/cibuildwheel from 2.12.3 to 2.16.2
- Update .pre-commit-config.yaml and pyproject.toml
- Add platform badge to README.md
- Remove unused code and properties
- Update release workflow configuration
- Update version to 1.0.0

### Styling

- Remove unnecessary parentheses and simplify code
- Update code style badge URL

### Build

- Update python dependencies

### Chroe

- Update dependencies

## [0.3.10] - 2023-10-24

### Features

- Update version to 0.3.10

## [0.3.9] - 2023-10-24

### Features

- Update version to 0.3.9

### Miscellaneous Tasks

- Update version to 0.3.8

## [0.3.7] - 2023-10-24

### Features

- Add tests for Python 3.11 and 3.12 on macOS
- Update supported Python versions

### Miscellaneous Tasks

- Remove unnecessary OS Independent classifier
- Update release workflow and dependencies
- Update CIBW_BEFORE_ALL command in release.yml
- Update package installation command
- Update build dependencies
- Update cibw_build and cibw_archs configurations
- Update CIBW_BEFORE_ALL command
- Update release.yml and pyproject.toml configurations
- Update manylinux x86_64 image version
- Update cibw_build and cibw_archs values
- Remove commented out code and unused steps
- Update test command in release.yml
- Update release workflow
- Update tests.yml configuration
- Update Python version range
- Update python dependency
- Update version to 0.3.7

### Refactor

- Update python version requirement and add numpy dependency

### Testing

- Importing tests

### Build

- Add sdist artifact to release workflow
- Update CIBW_BEFORE_ALL command
- Update build dependencies
- Use manylinux1 image and skip musllinux builds
- Add Homebrew dependencies and configure
- Update setuptools requirement
- Update python version

### Ci

- Upgrade Python version to 3.11

## [0.3.6] - 2023-10-23

### Styling

- Update pyproject.toml version and license

### Build

- Remove numpy dependency

## [0.3.5] - 2023-10-23

### Documentation

- Remove unnecessary section in README.md

### Miscellaneous Tasks

- Update version to 0.3.4
- Update dependencies
- Bump pip from 23.2.1 to 23.3 in /.github/workflows
- Bump psutil from 5.9.5 to 5.9.6
- Update dependencies
- Bump release-drafter/release-drafter from 5.24.0 to 5.25.0
- Bump ruff from 0.0.292 to 0.1.0
- Bump mypy from 1.6.0 to 1.6.1
- Bump black from 23.9.1 to 23.10.0
- Bump urllib3 from 2.0.4 to 2.0.7
- Update dependencies
- Bump ruff from 0.1.0 to 0.1.1
- Bump pybind11-stubgen from 2.3 to 2.3.4
- Bump pip from 23.3 to 23.3.1 in /.github/workflows
- Update pxblat version to 0.3.5

### Styling

- Fix typo in README.md

## [0.3.4] - 2023-10-11

### Features

- Add pr_agent.yml workflow for pull requests and comments

### Miscellaneous Tasks

- Remove unnecessary lines from README.md
- Bump virtualenv in /.github/workflows
- Bump ruff from 0.0.286 to 0.0.287
- Bump pytest from 7.4.0 to 7.4.1
- Bump pybind11-stubgen from 1.2 to 2.0.2 (#128)
- Bump loguru from 0.7.0 to 0.7.1
- Bump actions/checkout from 3 to 4
- Bump pybind11-stubgen from 2.0.2 to 2.1
- Bump setuptools from 68.1.2 to 68.2.0
- Bump pytest from 7.4.1 to 7.4.2
- Bump crazy-max/ghaction-github-labeler from 4.2.0 to 5.0.0
- Bump black from 23.7.0 to 23.9.1
- Bump virtualenv in /.github/workflows
- Bump ruff from 0.0.287 to 0.0.288
- Bump mashumaro from 3.9.1 to 3.10
- Bump setuptools from 68.2.1 to 68.2.2
- Bump sphinx from 7.2.5 to 7.2.6
- Bump rich from 13.5.2 to 13.5.3
- Bump ruff from 0.0.288 to 0.0.290
- Bump pybind11-stubgen from 2.1 to 2.2
- Bump ruff from 0.0.290 to 0.0.291
- Bump pybind11-stubgen from 2.2 to 2.2.1
- Bump pybind11-stubgen from 2.2.1 to 2.2.2
- Bump pybind11-stubgen from 2.2.2 to 2.3
- Bump sphinx-autoapi from 2.1.1 to 3.0.0 (#153)
- Bump rich from 13.5.3 to 13.6.0
- Bump seaborn from 0.12.2 to 0.13.0 (#156)
- Bump ruff from 0.0.291 to 0.0.292
- Bump ipython from 8.15.0 to 8.16.1
- Bump pysam from 0.21.0 to 0.22.0
- Update version to 0.3.3
- Bump mypy from 1.5.1 to 1.6.0
- Update dependencies and version numbers

## [0.3.2] - 2023-09-01

### Miscellaneous Tasks

- Bump sphinxcontrib-bibtex from 2.5.0 to 2.6.1
- Bump ruff from 0.0.285 to 0.0.286
- Bump sphinx from 7.2.2 to 7.2.4
- Bump pybind11-stubgen from 0.16.2 to 1.1
- Bump pybind11-stubgen from 1.1 to 1.2
- Bump crazy-max/ghaction-github-labeler from 4.1.0 to 4.2.0
- Update version to 0.3.2

### Refactor

- Simplify code in client.py and server.py
- Simplify nested loop for printing hsps in client query

### Build

- Update pre-commit and typos dependencies

## [0.3.1] - 2023-08-22

### Documentation

- Update docuemnt for CLIs
- Add FAQ for installing PxBLAT on MacOS Arm
- Update citation link in README.md
- Update README.md
- Update contributors and pre-commit config versions
- Add documentation for `create_client_option` function
- Add example files for users to try
- Update README.md with more detailed explanation

### Features

- Add version information to CLI output
- Update version to 0.3.1

### Miscellaneous Tasks

- Update lock file
- Update sys.path in conf.py
- Cerate figures for paper
- Bump rich from 13.4.2 to 13.5.0
- Bump ruff from 0.0.280 to 0.0.281
- Bump numpy from 1.25.1 to 1.25.2
- Bump rich from 13.5.0 to 13.5.1
- Bump ruff from 0.0.281 to 0.0.282
- Bump rich from 13.5.0 to 13.5.2 (#95)
- Bump mashumaro from 3.8.1 to 3.9
- Update repository link in README.md
- Bump ruff from 0.0.282 to 0.0.283
- Bump ruff from 0.0.283 to 0.0.284
- Bump pypa/gh-action-pypi-publish from 1.8.8 to 1.8.10
- Bump mypy from 1.4.1 to 1.5.0
- Bump virtualenv in /.github/workflows
- Bump setuptools from 68.0.0 to 68.1.0
- Bump mypy from 1.5.0 to 1.5.1
- Bump sphinx-click from 4.4.0 to 5.0.1
- Bump ruff from 0.0.284 to 0.0.285 (#109)
- Bump sphinx-immaterial from 0.11.6 to 0.11.7
- Bump setuptools from 68.1.0 to 68.1.2
- Bump sphinx-click from 4.4.0 to 5.0.1 in /docs
- Cache pip packages and Poetry virtual environment
- Remove Docker workflow configuration
- Update pre-commit hooks versions
- Bump poetry from 1.5.1 to 1.6.0 in /.github/workflows
- Bump poetry from 1.6.0 to 1.6.1 in /.github/workflows
- Update test workflow configuration
- Bump sphinx from 7.1.2 to 7.2.2

### Refactor

- Remove unnecessary import statement
- Assign version info to query result

### Styling

- Simplify code formatting and remove unnecessary lines
- Change port number in tutorial code example

### Testing

- Add benchmark result for hsp compared to BLAT

### Build

- Add caching for macOS dependencies

### Ci

- Update crate-ci/typos to v1.16.8

## [0.3.0] - 2023-07-27

### Bug Fixes

- Find free port in specified range
- Fix file existence check in query method

### Documentation

- Update Sphinx configuration and requirements
- Remove autodoc2 and update API generation groups
- Use ruff docs
- Remove d417
- Add rst prolog and python highlighting
- Add references and annotations to conf.py and tutorial.md
- Update Sphinx configuration and requirements
- Remove autodoc2 and update API generation groups
- Use ruff docs
- Remove d417
- Add rst prolog and python highlighting
- Add references and annotations to conf.py and tutorial.md
- Update README.md [skip ci]
- Update .all-contributorsrc [skip ci]
- Fix the error of docs build
- Update API example in README.md
- Draft a tutorial

### Features

- Add test_gevent.py
- Implemt new client and add tests
- Change query api to be more friendly and use gevent to implement query
- Make `__repr__` equals to `__str__`
- Add fa_to_two_bit function and update tutorial.md
- Add static method create_option()

### Miscellaneous Tasks

- Remove obsolete test_pickle file
- Remove obsolete test_pickle file
- Add/update pre-commit and commitizen config
- Add commitizen and update pre-commit hooks
- Bump myst-parser from 1.0.0 to 2.0.0
- Bump myst-parser from 1.0.0 to 2.0.0 in /docs
- Update version to v0.2.0 and add example in README
- Bump ruff from 0.0.272 to 0.0.274
- Bump setuptools from 67.8.0 to 68.0.0
- Bump invoke from 2.1.2 to 2.1.3
- Bump ruff from 0.0.274 to 0.0.275
- Bump mashumaro from 3.7 to 3.8
- Bump mashumaro from 3.8 to 3.8.1
- Bump pytest from 7.3.2 to 7.4.0
- Update lock file
- Remove unnecessary MACHTYPE variable assignment
- Bump ruff from 0.0.275 to 0.0.276
- Bump pybind11-stubgen from 0.15.1 to 0.16.1 (#60)
- Bump sphinx-immaterial from 0.11.4 to 0.11.5 (#59)
- Bump release-drafter/release-drafter from 5.23.0 to 5.24.0
- Bump pypa/gh-action-pypi-publish from 1.8.6 to 1.8.7
- Bump virtualenv in /.github/workflows
- Bump ruff from 0.0.276 to 0.0.277
- Bump numpy from 1.25.0 to 1.25.1
- Bump nox-poetry from 1.0.2 to 1.0.3
- Bump nox-poetry from 1.0.2 to 1.0.3 in /.github/workflows
- Bump black from 23.3.0 to 23.7.0
- Bump pypa/gh-action-pypi-publish from 1.8.7 to 1.8.8
- Bump virtualenv in /.github/workflows
- Bump pybind11 from 2.10.4 to 2.11.1
- Bump pybind11-stubgen from 0.16.1 to 0.16.2
- Bump pip from 23.1.2 to 23.2 in /.github/workflows
- Bump invoke from 2.1.3 to 2.2.0
- Bump ruff from 0.0.277 to 0.0.278
- Bump ruff from 0.0.278 to 0.0.280
- Bump pip from 23.2 to 23.2.1 in /.github/workflows
- Update pyproject.toml and remove unused timeout parameter
- Bump virtualenv in /.github/workflows
- Update lock files
- Upadte dependencies
- Add sphnix_click as dev dependency
- Bump gevent from 22.10.2 to 23.7.0
- Bump urllib3 from 2.0.3 to 2.0.4 (#86)
- Bump gevent from 22.10.2 to 23.7.0
- Remove unused Signal class
- Update version to 0.3.0

### Refactor

- Clean up pyproject.toml formatting and remove unused files
- Clean up and optimize client code
- Refactor query_server_by_file method
- Simplify query method and remove unnecessary code
- Split fas on single directory
- Fix typos and formatting in code and documentation
- Simplify error message handling
- Remove unnecessary logger.debug statements
- Remove unused function
- Rename copy function for clarity

### Styling

- Fix formatting and spacing in README and installation.md
- Fix formatting and spacing in README and installation.md
- Fix typo in Makefile target name
- Update pre-commit hooks and remove commented code in utils.py
- Enbale more linter rules

### Testing

- Add smoke test for set_state function
- Add smoke test for set_state function
- Add new test data
- Add benchmark tests for pxblat results and bpresult and bcresult tests
- Add failing tests
- Add test files to fix the bug about (open too many files)
- Remove unnecessary code
- Rename test_gevent.py to test_client.py

### Build

- Update Ruff version to v0.0.276
- Update symbolic links for OpenSSL installation
- Update lock file
- Addd gevent
- Add py-spy dependency

### Ci

- Fix ci error
- Make typing annotation to be compatible with py39
- Fix the ci errors of tests
- Fix ci error for tests

## [0.2.0] - 2023-06-13

### Bug Fixes

- Update urllib3 version to 1.26.9

### Documentation

- Add logo
- Update contact information in epilog
- Add installation guide for prerequisites
- Add tutorial and CLI usage to docs
- Update CLI list in usage.md
- Add installation instructions for pxblat
- Update README.md [skip ci]
- Create .all-contributorsrc [skip ci]
- Add tutorial and CLI usage to docs
- Update CLI list in usage.md
- Add installation instructions for pxblat
- Update CLI usage and add completion command
- Update FAQ heading in installation.md

### Features

- Add twoBitToFa conversion function
- Draft new features
- Finish cpp implementation
- Add twobit2fa.py script and CLI arguments
- Add linkcheck to build docs
- Finish twobit2fa cpp
- Add twoBitToFa module and bind it in \_extc.cpp
- Add PXBLATLIB macro to escape unused code
- Add support for twobittofa command
- Add twoBitToFa conversion function
- Draft new features
- Finish cpp implementation
- Add twobit2fa.py script and CLI arguments
- Add linkcheck to build docs
- Finish twobit2fa cpp
- Add twoBitToFa module and bind it in \_extc.cpp
- Add PXBLATLIB macro to escape unused code
- Add support for twobittofa command

### Miscellaneous Tasks

- Update aicommits to use conventional type
- Bump deprecated from 1.2.13 to 1.2.14
- Bump urllib3 from 1.26.9 to 2.0.2
- Bump pybind11-stubgen from 0.14.0 to 0.15.0 (#15)
- Bump poetry from 1.5.0 to 1.5.1 in /.github/workflows
- Bump scienceplots from 2.0.1 to 2.1.0
- Bump rich from 13.3.5 to 13.4.1
- Bump sphinx-immaterial from 0.11.3 to 0.11.4
- Bump ipython from 8.13.2 to 8.14.0
- Update pull_request configuration and remove empty line
- Add search_source to Makefile commands
- Bump urllib3 from 1.26.9 to 2.0.2
- Bump ruff from 0.0.270 to 0.0.271 (#32)
- Bump ruff from 0.0.271 to 0.0.272
- Bump urllib3 from 2.0.2 to 2.0.3 (#34)
- Remove 2to3 binary on macOS build workflow
- Rename directories and update tasks
- Remove unnecessary file for macos-latest build
- Update lock file
- Remove unnecessary file in Install Dependencies script
- Remove unused code and update comments
- Remove unused Python IDLE3 binary
- Update installation.md and tests.yml files
- Update tests.yml and README.md
- Bump pybind11-stubgen from 0.15.0 to 0.15.1 (#38)
- Bump pytest from 7.3.1 to 7.3.2 (#37)
- Bump sphinx-autoapi from 2.1.0 to 2.1.1 (#36)
- Remove urllib3 dependency
- Update version to 0.2.0 and change log

### Refactor

- Add udcDir option to twoBitToFa() function
- Add udcDir option to twoBitToFa() function
- Rename gfClientOption to ClientOption
- Rename gfServerOption to ServerOption
- Throw exceptions instead of aborting
- Remove unnecessary horizontal lines and update installation instructions in README.md

### Styling

- Remove commented code in twoBitToFa.hpp
- Update file path in test_server.py
- Remove commented code in twoBitToFa.hpp
- Update file path in test_server.py
- Remove blank line in README.md
- Fix capitalization of executable names
- Remove comments and emphasize headings in installation.md
- Remove unnecessary commented lines and update dependencies in tests.yml, fix a typo in tutorial.md
- Update macOS dependencies installation command and update README features section
- Update font weights in CSS file

### Testing

- Add test for twobit2fa
- Add test for twobit2fa
- Add blat suit as benchmark
- Test correct result with blat suit

### Ci

- Fix peotry

## [0.1.6] - 2023-05-27

### Bug Fixes

- Add path

### Documentation

- Customiza document

## [0.1.5] - 2023-05-26

### Documentation

- Add doc draft

### Miscellaneous Tasks

- Bump sphinx-click from 4.3.0 to 4.4.0 in /docs
- Bump pybind11-stubgen from 0.13.0 to 0.14.0

## [0.1.4] - 2023-05-26

### Features

- Fallback to use source code

### Miscellaneous Tasks

- Bump sphinx from 5.3.0 to 7.0.1 in /docs
- Bump linkify-it-py from 2.0.0 to 2.0.2 in /docs
- Bump sphinx-click from 4.3.0 to 4.4.0 in /docs (#9)
- Bump myst-parser from 0.18.1 to 1.0.0 in /docs (#8)
- Bump pybind11-stubgen from 0.13.0 to 0.14.0
- Bump ruff from 0.0.263 to 0.0.270 (#5)
- Bump invoke from 2.1.1 to 2.1.2 (#6)
- Bump setuptools from 67.7.2 to 67.8.0 (#4)
- Bump actions/checkout from 2 to 3
- Bump docker/build-push-action from 3 to 4
- Update changelog, bump version to 0.1.4 in pyproject.toml

### Build

- Refactor build script

## [0.1.3] - 2023-05-25

### Bug Fixes

- Fix the bug that make result consistent with c
- It is optional to output file when client
- Use strong type for status and add test

### Documentation

- Add descriptions to the make targets

### Features

- Complie for gfClient and gfServer
- Complie for blat
- Rename directory
- Add py binding
- Add header guide for cpp
- Add binging for gfServer
- Implement cpp gfserver
- Refactor gfserver binding
- Create static lib
- Fix c code error from cxx compiler
- Add start sever in cpp
- Add test for python
- Use invoke
- Add more ruff rule
- Do not abort when check status
- Add bindings
- Add native python for client
- Change client binding
- Foramt files
- Avoide global variable
- Pass extra parameter
- Add debug printer
- Add boolean parameter to dynamicServerQuery and errorSafeQuery functions
- Use binder
- Add docker for binder
- Use binder
- Update binding
- Add Signal class to **init**.pyi
- Use thread pool for every client
- Rename macro round to cround
- Splite handle client func
- Finish one-thread-per-client mode
- Rename pyblat to pxblat
- Create cli application
- Creat cli application
- Refactor cli
- Refactor cli
- Add benchmark data
- Use sequences as client input
- Add test for fatotwobit
- Implement server
- Add test for client and server
- Finish test and add bencharmk
- Refactor server
- Refactor test
- Improve buffer size for client to hold more content
- Add plot script
- Test for performance
- Prepare to public
- Add binder code
- Add docs draft

### Miscellaneous Tasks

- Comment out removal of binder files
- Add git add . command to commit target in Makefile
- Update TODO list with new tasks and mark parser gfclient result as completed

### Refactor

- Add options for gfserver
- Add cpp binding
- Comment out unused logInfo calls and replace uglyf calls with dbg calls

<!-- generated by git-cliff -->
