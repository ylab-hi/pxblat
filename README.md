# <img src="https://raw.githubusercontent.com/cauliyang/pxblat/main/docs/_static/logo.png" alt="logo" height=100> **PxBLAT** [![social](https://img.shields.io/github/stars/cauliyang/pxblat?style=social)](https://github.com/cauliyang/pxblat/stargazers)

_An Efficient and Ergonomic Python Binding Library for BLAT_

[![python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)](https://www.python.org/)
[![c++](https://img.shields.io/badge/C++-00599C.svg?style=for-the-badge&logo=C++&logoColor=white)](https://en.cppreference.com/w/)
[![c](https://img.shields.io/badge/C-A8B9CC.svg?style=for-the-badge&logo=C&logoColor=black)](https://www.gnu.org/software/gnu-c-manual/)
[![pypi](https://img.shields.io/pypi/v/pxblat.svg?style=for-the-badge)][pypi]
[![conda](https://img.shields.io/conda/vn/bioconda/pxblat?style=for-the-badge)][conda]
![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux&style=for-the-badge)
![macOS](https://img.shields.io/badge/-OSX-black?logo=apple&style=for-the-badge)
[![pyversion](https://img.shields.io/pypi/pyversions/pxblat?style=for-the-badge)][pypi]
[![tests](https://img.shields.io/github/actions/workflow/status/cauliyang/pxblat/tests.yml?style=for-the-badge&logo=github&label=Tests)](https://github.com/cauliyang/pxblat/actions/workflows/tests.yml)
[![Codecov](https://img.shields.io/codecov/c/github/cauliyang/pxblat/main?style=for-the-badge)](https://app.codecov.io/gh/cauliyang/pxblat)
[![docs](https://img.shields.io/readthedocs/pxblat?style=for-the-badge)](https://pxblat.readthedocs.io/en/latest/)
[![download](https://img.shields.io/pypi/dm/pxblat?logo=pypi&label=pypi%20download&style=for-the-badge)][pypi]
[![condadownload](https://img.shields.io/conda/dn/bioconda/pxblat?style=for-the-badge&logo=anaconda&label=Conda%20Download)][conda]
[![precommit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg?style=for-the-badge)](https://github.com/charliermarsh/ruff)
[![release](https://img.shields.io/github/release-date/cauliyang/pxblat?style=for-the-badge)](https://github.com/cauliyang/pxblat/releases)
[![open-issue](https://img.shields.io/github/issues-raw/cauliyang/pxblat?style=for-the-badge)][open-issue]
[![close-issue](https://img.shields.io/github/issues-closed-raw/cauliyang/pxblat?style=for-the-badge)][close-issue]
[![activity](https://img.shields.io/github/commit-activity/m/cauliyang/pxblat?style=for-the-badge)][repo]
[![lastcommit](https://img.shields.io/github/last-commit/cauliyang/pxblat?style=for-the-badge)][repo]
[![opull](https://img.shields.io/github/issues-pr-raw/cauliyang/pxblat?style=for-the-badge)][opull]
[![all contributors](https://img.shields.io/github/all-contributors/cauliyang/pxblat?style=for-the-badge)](#contributors)

<!-- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)][colab] -->

[repo]: https://github.com/ylab-hi/pxblat
[open-issue]: https://github.com/cauliyang/pxblat/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc
[close-issue]: https://github.com/cauliyang/pxblat/issues?q=is%3Aissue+sort%3Aupdated-desc+is%3Aclosed
[opull]: https://github.com/cauliyang/pxblat/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc
[conda]: https://bioconda.github.io/recipes/pxblat/README.html
[pypi]: https://pypi.org/project/pxblat/
[colab]: https://colab.research.google.com/drive/1TXb9GBmYa2EYezwBKbD-y9Xg6MC2gL36

## Why PxBLAT?

When conducting extensive queries, using the `blat` of `BLAT` suite can prove to be quite inefficient, especially if these operations aren't grouped. The tasks are allocated sporadically, often interspersed among other tasks.
In general, the choice narrows down to either utilizing `blat` or combining `gfServer` with `gfClient`.
Indeed, `blat` is a program that launches `gfServer`, conducts the sequence query via `gfClient`, and then proceeds to terminate the server.

This approach is far from ideal when performing numerous queries that aren't grouped since `blat` repeatedly initializes and shuts down `gfServer` for each query, resulting in substantial overhead.
This overhead consists of the time required for the server to index the reference, contingent on the reference's size.
To index the human genome (hg38), for example, would take approximately five minutes.

A more efficient solution would involve initializing `gfServer` once and invoking `gfClient` multiple times for the queries.
However, `gfServer` and `gfClient` are only accessible via the command line.
This necessitates managing system calls (for instance, `subprocess` or `os.system`), intermediate temporary files, and format conversion, further diminishing performance.

That is why `PxBLAT` holds its position.
It resolves the issues mentioned above while introducing handy features like `port retry`, `use current running server`, etc.

## 📚 **Table of Contents**

- [ **PxBLAT** ](#-pxblat-)
  - [📚 **Table of Contents**](#-table-of-contents)
  - [🔮 **Features**](#-features)
  - [📎 **Citation**](#-citation)
  - [🚀 **Getting Started**](#-getting-started)
  - [🤝 **Contributing**](#-contributing)
  - [🪪 **License**](#-license)
  - [🤗 **Contributors**](#contributors)
  - [🙏 **Acknowledgments**](#-acknowledgments)

## 🔮 **Features**

- **Zero System Calls**: Avoids system calls, leading to a smoother, quicker operation.<br>
- **Ergonomics**: With an ergonomic design, `PxBLAT` aims for a seamless user experience.<br>
- **No External Dependencies**: `PxBLAT` operates independently without any external dependencies.<br>
- **Self-Monitoring**: No need to trawl through log files; `PxBLAT` monitors its status internally.<br>
- **Robust Validation**: Extensively tested to ensure reliable performance and superior stability as BLAT.<br>
- **Format-Agnostic:** `PxBLAT` doesn't require you to worry about file formats.<br>
- **In-Memory Processing**: `PxBLAT` discards the need for intermediate files by doing all its operations in memory, ensuring speed and efficiency.<br>

## 📎 **Citation**

PxBLAT is scientific software, with a published paper in the BioRxiv.
Check the [published](https://www.biorxiv.org/content/10.1101/2023.08.02.551686v2) to read the paper.

```bibtex
@article {Li2023pxblat,
	author = {Yangyang Li and Rendong Yang},
	title = {PxBLAT: An Ergonomic and Efficient Python Binding Library for BLAT},
	elocation-id = {2023.08.02.551686},
	year = {2023},
	doi = {10.1101/2023.08.02.551686},
	publisher = {Cold Spring Harbor Laboratory},
	url = {https://www.biorxiv.org/content/10.1101/2023.08.02.551686v2},
	journal = {bioRxiv}
}
```

## 🚀 **Getting Started**

Welcome to PxBLAT! To kickstart your journey and get the most out of this tool, we have prepared a comprehensive [documentation](https://pxblat.readthedocs.io/en/latest/installation.html).
Inside, you’ll find detailed guides, examples, and all the necessary information to help you navigate and utilize PxBLAT effectively.

### Need Help or Found an Issue?

If you encounter any issues or if something is not clear in the documentation, do not hesitate to [open an issue](https://github.com/ylab-hi/pxblat/issues/new/choose).
We are here to help and appreciate your feedback for improving PxBLAT.

### Show Your Support

If PxBLAT has been beneficial to your projects or you appreciate the work put into it, consider leaving a ⭐️ [Star](https://github.com/ylab-hi/pxblat/stargazers) on our GitHub repository.
Your support means the world to us and motivates us to continue enhancing PxBLAT.

Let’s embark on this journey together and make the most out of PxBLAT! 🎉
Please see the [document](https://pxblat.readthedocs.io/en/latest/installation.html) for details and more examples.

## 🤝 **Contributing**

Contributions are always welcome! Please follow these steps:

1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).

```bash
git checkout -b new-feature-branch
```

4. Take changes to the project's codebase.
5. Install the latest package

```bash
poetry install
```

6. Test your changes

```bash
pytest -vlsx tests
```

7. Commit your changes to your local branch with a clear commit message that explains the changes you've made.

```bash
git commit -m 'Implemented new feature.'
```

8. Push your changes to your forked repository on GitHub using the following command

```bash
git push origin new-feature-branch
```

Create a pull request to the original repository.
Open a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.

## 🪪 **License**

**PxBLAT is modified from blat, the license is the same as blat. The source code and
executables are freely available for academic, nonprofit, and personal use.
Commercial licensing information is available on the Kent Informatics website
(https://kentinformatics.com/).**

## **Contributors**

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://yangyangli.top"><img src="https://avatars.githubusercontent.com/u/38903141?v=4?s=100" width="100px;" alt="yangliz5"/><br /><sub><b>yangliz5</b></sub></a><br /><a href="#maintenance-cauliyang" title="Maintenance">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mencian"><img src="https://avatars.githubusercontent.com/u/71105179?v=4?s=100" width="100px;" alt="Joshua Zhuang"/><br /><sub><b>Joshua Zhuang</b></sub></a><br /><a href="#infra-mencian" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
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

## 🙏 **Acknowledgments**

- [BLAT](http://genome.ucsc.edu/goldenPath/help/blatSpec.html)
- [UCSC](https://github.com/ucscGenomeBrowser/kent)
- [pybind11](https://github.com/pybind/pybind11/tree/stable)

<!-- github-only -->

<br>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=cauliyang/pxblat&type=Date&theme=light" />
  <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=cauliyang/pxblat&type=Date" />
  <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=cauliyang/pxblat&type=Date" />
</picture>
