# <img src="https://raw.githubusercontent.com/cauliyang/pxblat/main/docs/_static/logo.png" alt="logo" height=100> **PxBLAT** [![social](https://img.shields.io/github/stars/cauliyang/pxblat?style=social)](https://github.com/cauliyang/pxblat/stargazers)

_An Efficient and Ergonomics Python Binding Library for BLAT_

[![python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)](https://www.python.org/)
[![c++](https://img.shields.io/badge/C++-00599C.svg?style=for-the-badge&logo=C++&logoColor=white)](https://en.cppreference.com/w/)
[![c](https://img.shields.io/badge/C-A8B9CC.svg?style=for-the-badge&logo=C&logoColor=black)](https://www.gnu.org/software/gnu-c-manual/)
[![pypi](https://img.shields.io/pypi/v/pxblat.svg?style=for-the-badge)](https://pypi.org/project/pxblat/)
[![pyversion](https://img.shields.io/pypi/pyversions/pxblat?style=for-the-badge)](https://pypi.org/project/pxblat/)
[![license](https://img.shields.io/pypi/l/pxblat?style=for-the-badge)](https://opensource.org/licenses/mit)
[![precommit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json&style=for-the-badge)](https://github.com/charliermarsh/ruff)
[![download](https://img.shields.io/pypi/dm/pxblat?style=for-the-badge)](https://pypi.org/project/pxblat/)
[![Codecov](https://img.shields.io/codecov/c/github/cauliyang/pxblat/main?style=for-the-badge)](https://app.codecov.io/gh/cauliyang/pxblat)
[![docs](https://img.shields.io/readthedocs/pxblat?style=for-the-badge)](https://pxblat.readthedocs.io/en/latest/)
[![release](https://img.shields.io/github/release-date/cauliyang/pxblat?style=for-the-badge)](https://github.com/cauliyang/pxblat/releases)
[![open-issue](https://img.shields.io/github/issues-raw/cauliyang/pxblat?style=for-the-badge)](https://github.com/cauliyang/pxblat/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc)
[![close-issue](https://img.shields.io/github/issues-closed-raw/cauliyang/pxblat?style=for-the-badge)][close-issue]
[![activity](https://img.shields.io/github/commit-activity/m/cauliyang/pxblat?style=for-the-badge)][repo]
[![lastcommit](https://img.shields.io/github/last-commit/cauliyang/pxblat?style=for-the-badge)][repo]
[![opull](https://img.shields.io/github/issues-pr-raw/cauliyang/pxblat?style=for-the-badge)][opull]
[![tests](https://github.com/cauliyang/pxblat/actions/workflows/tests.yml/badge.svg?style=for-the-badge)](https://github.com/cauliyang/pxblat/actions/workflows/tests.yml)
[![all contributors](https://img.shields.io/github/all-contributors/cauliyang/pxblat?style=for-the-badge)](#contributors)

[repo]: https://github.com/cauliyang/pxblat
[close-issue]: https://github.com/cauliyang/pxblat/issues?q=is%3Aissue+sort%3Aupdated-desc+is%3Aclosed
[opull]: https://github.com/cauliyang/pxblat/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc

---

## 📚 Table of Contents

- [📚 Table of Contents](#-table-of-contents)
- [🔮 Features](#-features)
- [🏎💨 Getting Started](#-getting-started)
- [🤝 Contributing](#-contributing)
- [🪪 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🔮 Features

**In-Memory Processing**: `PxBlAT` discards the need for intermediate files by doing all its operations in memory, ensuring speed and efficiency.
**Zero System Calls**: Avoids system calls, leading to a smoother, quicker operation.
**Self-Monitoring**: No need to trawl through log files; `PxBlAT` monitors its status internally and keeps you updated.
**Format-Agnostic:** `PxBlAT` doesn't require you to worry about file formats.
**No External Dependencies**: `PxBlAT` operates independently without any external dependencies.
**Ergonomics**: With an ergonomic design, `PxBlAT` aims for a seamless user experience.

## To-do

- [x] parser gfclient result
- [x] parse gfserver query result
- [x] benchmarking multi connection and original version
- [x] test result with original version
- [x] fix build.py to build ssl, hts, maybe libuv when install with pip
- [ ] add tool to conda channel
- [x] add tool to pip
- [x] change abort to throw exceptions
- [x] implement twobit2fa
- [ ] implement psl2sam

---

## 🚀 Getting Started

```bash
pip install pxblat
```

```bash
conda install pxblat
```

### ✅ Prerequisites

Before you begin, ensure that you have the following prerequisites installed:

> You need to install `openssl` and `htslib` first.

### 💻 Installation

1. Clone the pxblat repository:

```sh
git clone https://github.com/cauliyang/pxblat.git
```

2. Change to the project directory:

```sh
cd pxblat
```

3. Install the dependencies:

```sh
poetry install
```

### 🤖 Using pxblat

```sh
pxblat
```

### 🧪 Running Tests

```sh
pytest
```

---

## 🤝 Contributing

Contributions are always welcome! Please follow these steps:

1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).

```sh
git checkout -b new-feature-branch
```

4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.

```sh
git commit -m 'Implemented new feature.'
```

6. Push your changes to your forked repository on GitHub using the following command

```sh
git push origin new-feature-branch
```

7. Create a pull request to the original repository.
   Open a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
   The project maintainers will review your changes and provide feedback or merge them into the main branch.

---

## 🪪 License

This project is licensed under the `[📌  INSERT-LICENSE-TYPE]` License. See the [LICENSE](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository) file for additional info.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://yangyangli.top"><img src="https://avatars.githubusercontent.com/u/38903141?v=4?s=100" width="100px;" alt="yangliz5"/><br /><sub><b>yangliz5</b></sub></a><br /><a href="#maintenance-cauliyang" title="Maintenance">🚧</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

---

## 🙏 Acknowledgments

[📌 INSERT-DESCRIPTION]

---

<!-- github-only -->
