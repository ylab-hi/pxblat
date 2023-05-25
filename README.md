# PxBLAT

<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>
pxblat
</h1>
<h3 align="center">PxBLAT: An Efficient and Ergonomics Python Binding Library for BLAT</h3>
<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="" />
<img src="https://img.shields.io/badge/Markdown-000000.svg?style=for-the-badge&logo=Markdown&logoColor=white" alt="pack" />
<img src="https://img.shields.io/badge/C++-00599C.svg?style=for-the-badge&logo=C++&logoColor=white" alt="h" />
<img src="https://img.shields.io/badge/C-A8B9CC.svg?style=for-the-badge&logo=C&logoColor=black" alt="python" />
</p>

</div>

---

## 📚 Table of Contents

- [📚 Table of Contents](#-table-of-contents)
- [📍Overview](#-introdcution)
- [🔮 Features](#-features)
- [⚙️ Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🏎💨 Getting Started](#-getting-started)
- [🗺 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [🪪 License](#-license)
- [📫 Contact](#-contact)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🔮 Feautres

- no intermidiate files, all in memory
- no system call
- no need to bother with log files to get status of tool
- no need to worry about file format
- no other dependency
- higher proformance and Ergonomics (compare with current blat endpoint)

## TODO

- [x] parser gfclient result
- [x] parse gfserver query result
- [x] multi-connection server
- [ ] benchmarking multi connection and original version
- [x] test result with original version
- [ ] fix build.py to build ssl, hts, maybe libuv when install with pip
- [ ] add tool to conda channel
- [ ] add too to dokerhub
- [ ] add tool to pip
- [ ] change abort to throw exceptions

---

<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-src-open.svg" width="80" />

## 🚀 Getting Started

### ✅ Prerequisites

Before you begin, ensure that you have the following prerequisites installed:

> `[📌  INSERT-PROJECT-PREREQUISITES]`

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

<hr />

## 🛠 Future Development

- [x] [📌 COMPLETED-TASK]
- [ ] [📌 INSERT-TASK]
- [ ] [📌 INSERT-TASK]

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

---

## 🙏 Acknowledgments

[📌 INSERT-DESCRIPTION]

---
