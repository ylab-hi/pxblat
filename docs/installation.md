# **Installation Guide**

Welcome to the installation guide for **PxBLAT**!
Below, you'll find straightforward instructions on how to install **PxBLAT** on your system.
You can choose between `CONDA` and `PyPI` for installation, depending on your preference.

## Get started

Installing **PxBLAT** is a breeze, whether you prefer using `CONDA` or `PyPI`.
Simply follow the tabs below to choose your preferred installation method.

`````{md-tab-set}

````{md-tab-item} Pip

To install using `pip`, run the following command in your terminal:

```{code-block} bash
pip install pxblat
```

This will fetch the latest version of **PxBLAT** and install it on your system.
````

````{md-tab-item} Conda

To install using `conda`, execute the following command:

```{code-block} bash
conda install pxblat
```
This command will install **PxBLAT** from the [conda] repository.
````

`````

## Compatibility and Support

Below is a compatibility matrix that shows the support status of **PxBLAT** across different platforms and Python versions.

### [Conda Support][conda]

| Python Version | Linux x86_64 | macOS Intel |
| :------------: | :----------: | :---------: |
|      3.9       |      ✅      |     ✅      |
|      3.10      |      ✅      |     ✅      |
|      3.11      |      ✅      |     ✅      |
|      3.12      |      ⚫      |     ⚫      |

### [PyPI Support][pypi]

| Python Version | Linux x86_64 | macOS Intel | macOS Apple Silicon |
| :------------: | :----------: | :---------: | :-----------------: |
|      3.9       |      ✅      |     ✅      |         ✅          |
|      3.10      |      ✅      |     ✅      |         ✅          |
|      3.11      |      ✅      |     ✅      |         ✅          |
|      3.12      |      ⚫      |     ⚫      |         ⚫          |

## Frequently Asked Questions (FAQ)

- **Q1**: I'm unable to install `PxBLAT` via `Conda` on my macOS device with an Arm-based processor (M1 or M2). What should I do?

  > **A**: Currently, `Conda` provides **PxBLAT** built for x86 architectures. For Arm-based macOS devices, we recommend installing **PxBLAT** via `PyPI` instead:

  ```bash
  pip install pxblat
  ```

```{bug}
As we continuously strive to improve the precision and comprehensibility of this documentation, your insights and observations become crucial.
Should you come across any inconsistencies or issues, we encourage you to [open an issue](https://github.com/ylab-hi/pxblat/issues/new/choose) on our GitHub repository.
Your contributions are immensely valuable, playing a pivotal role in helping us uphold and enhance the quality and accuracy of our documentation.
We appreciate your commitment to excellence and look forward to your feedback.
```

You've successfully installed **PxBLAT**! Feel free to dive into a real usage case ({doc}`tutorial`) to start exploring its functionalities.

<!-- links -->

[conda]: https://anaconda.org/bioconda/pxblat
[pypi]: https://pypi.org/project/pxblat/
