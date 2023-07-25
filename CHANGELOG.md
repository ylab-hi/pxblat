# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2023-06-13

### Bug Fixes

- Update urllib3 version to 1.26.9

### Documentation

- Add logo
- Update contact information in epilog
- Add installation guide for prerequisites
- Add tutorial and CLI usage to docs
- Update README.md [skip ci]
- Create .all-contributorsrc [skip ci]
- Update FAQ heading in installation.md

### Features

- Add twoBitToFa module
- Add support for twobittofa command
- Add PXBLATLIB macro to escape unused code
- Add linkcheck to build docs

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
- Remove unnecessary file in Install Dependencies script
- Remove unused code and update comments
- Remove unused Python IDLE3 binary
- Update installation.md and tests.yml files
- Update tests.yml and README.md
- Bump pybind11-stubgen from 0.15.0 to 0.15.1 (#38)
- Bump pytest from 7.3.1 to 7.3.2 (#37)
- Bump sphinx-autoapi from 2.1.0 to 2.1.1 (#36)
- Remove urllib3 dependency

### Refactor

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
- Add blat suit as benchmark
- Test correct result with blat suit

### Ci

- Fix poetry

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
- Format files
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
