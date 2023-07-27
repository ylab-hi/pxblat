# <img src="https://raw.githubusercontent.com/cauliyang/pxblat/main/docs/_static/logo.png" alt="logo" height=100> **PxBLAT** [![social](https://img.shields.io/github/stars/cauliyang/pxblat?style=social)](https://github.com/cauliyang/pxblat/stargazers)

_An Efficient and Ergonomics Python Binding Library for BLAT_

[![python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)](https://www.python.org/)
[![c++](https://img.shields.io/badge/C++-00599C.svg?style=for-the-badge&logo=C++&logoColor=white)](https://en.cppreference.com/w/)
[![c](https://img.shields.io/badge/C-A8B9CC.svg?style=for-the-badge&logo=C&logoColor=black)](https://www.gnu.org/software/gnu-c-manual/)
[![pypi](https://img.shields.io/pypi/v/pxblat.svg?style=for-the-badge)][pypi]
[![conda](https://img.shields.io/conda/vn/bioconda/pxblat?style=for-the-badge)][conda]
[![pyversion](https://img.shields.io/pypi/pyversions/pxblat?style=for-the-badge)][pypi]
[![license](https://img.shields.io/pypi/l/pxblat?style=for-the-badge)](https://opensource.org/licenses/mit)
[![tests](https://img.shields.io/github/actions/workflow/status/cauliyang/pxblat/tests.yml?style=for-the-badge&logo=github&label=Tests)](https://github.com/cauliyang/pxblat/actions/workflows/tests.yml)
[![Codecov](https://img.shields.io/codecov/c/github/cauliyang/pxblat/main?style=for-the-badge)](https://app.codecov.io/gh/cauliyang/pxblat)
[![docs](https://img.shields.io/readthedocs/pxblat?style=for-the-badge)](https://pxblat.readthedocs.io/en/latest/)
[![download](https://img.shields.io/pypi/dm/pxblat?logo=pypi&label=pypi%20download&style=for-the-badge)][pypi]
[![condadownload](https://img.shields.io/conda/dn/bioconda/pxblat?style=for-the-badge&logo=anaconda&label=Conda%20Download)][conda]
[![precommit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json&style=for-the-badge)](https://github.com/charliermarsh/ruff)
[![release](https://img.shields.io/github/release-date/cauliyang/pxblat?style=for-the-badge)](https://github.com/cauliyang/pxblat/releases)
[![open-issue](https://img.shields.io/github/issues-raw/cauliyang/pxblat?style=for-the-badge)][open-issue]
[![close-issue](https://img.shields.io/github/issues-closed-raw/cauliyang/pxblat?style=for-the-badge)][close-issue]
[![activity](https://img.shields.io/github/commit-activity/m/cauliyang/pxblat?style=for-the-badge)][repo]
[![lastcommit](https://img.shields.io/github/last-commit/cauliyang/pxblat?style=for-the-badge)][repo]
[![opull](https://img.shields.io/github/issues-pr-raw/cauliyang/pxblat?style=for-the-badge)][opull]
[![all contributors](https://img.shields.io/github/all-contributors/cauliyang/pxblat?style=for-the-badge)](#contributors)

[repo]: https://github.com/cauliyang/pxblat
[open-issue]: https://github.com/cauliyang/pxblat/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc
[close-issue]: https://github.com/cauliyang/pxblat/issues?q=is%3Aissue+sort%3Aupdated-desc+is%3Aclosed
[opull]: https://github.com/cauliyang/pxblat/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc
[conda]: https://bioconda.github.io/recipes/pxblat/README.html
[pypi]: https://pypi.org/project/pxblat/

## 📚 **Table of Contents**

- [ **PxBLAT** ](#-pxblat-)
  - [📚 **Table of Contents**](#-table-of-contents)
  - [🔮 **Features**](#-features)
  - [📎 **Citation**](#-citation)
  - [🚀 **Getting Started**](#-getting-started)
    - [🤖 **Using PxBLAT**](#-using-pxblat)
  - [🤝 **Contributing**](#-contributing)
  - [🪪 **License**](#-license)
  - [**Contributors**](#contributors)
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

PxBLAT is scientific software, with a published paper in the [Journal].
Check the [published] to read the paper.

## 🚀 **Getting Started**

The first step in starting your journey with `PxBLAT` is to install the tool.
To do this, there are two options shown as below:

- **PyPI**

```bash
pip install pxblat
```

- **CONDA** via [Bioconda](https://bioconda.github.io/)

```bash
conda install pxblat
```

Congratulations! You've successfully installed `PxBLAT` on your local machine.
If you have some issues, please check the [document](https://pxblat.readthedocs.io/en/latest/installation.html) first before opening a issue.

### 🤖 **Using PxBLAT**

- **API Example**

```python
from pxblat import Server
from pxblat import Client

client = Client(
    host="localhost",
    port=port,
    seq_dir=two_bit,
    min_score=20,
    min_identity=90,
)

server_option = Server.create_option().build()
with Server("localhost", port, two_bit, server_option) as server:
    work()  # do some other stuffs that consuming time
    server.wait_for_ready()
    result1 = client.query("ATCG")
    result2 = client.query("AtcG")
    result3 = client.query(["ATCG", "ATCG"])
    result4 = client.query(["cgTA", "fasta.fa"])
```

Moreover, `PxBLAT` provide command line tool that has same functions as `BLAT`.

```console
❯ pxblat -h

 Usage: pxblat [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion            Install completion for the current shell.                                                                    │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                             │
│ --help                -h        Show this message and exit.                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ client               A client for the genomic finding program that produces a .psl file.                                                     │
│ fatotwobit           Convert DNA from fasta to 2bit format.                                                                                  │
│ server               Make a server to quickly find where DNA occurs in genome                                                                │
│ twobittofa           Convert all or part of .2bit file to fasta.                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

 YangyangLi 2023 yangyang.li@northwstern.edu
```

Please see the [document](https://pxblat.readthedocs.io/en/latest/) for details.

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

This project is licensed under the [MIT](https://opensource.org/licenses/mit) License. See the [LICENSE](https://github.com/cauliyang/pxblat/blob/main/LICENSE) file for additional info.
The license of [BLAT](http://genome.ucsc.edu/goldenPath/help/blatSpec.html) is [here](https://genome.ucsc.edu/license/).

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
