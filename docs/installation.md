# Install

## **Prerequisites**

```{tip}
I highly recommend to install `PxBLAT` via `CONDA` such that you do not need to
install dependencies [goto ➡️](#get-started).
```

Before you begin with the installation and use of **PxBLAT**, there are certain prerequisites that need to be met.
The following sections detail the necessary software, hardware, and knowledge prerequisites that you should have before you start.
**PxBLAT** has been tested and runs on the following operating systems **Linux** and **MacOS**.
Choosing appropriate dependencies manager according to the operating systems.
You should have an active and stable internet connection for downloading and installing the software:

`````{md-tab-set}

````{md-tab-item} Brew
```{code-block} bash
brew install htslib openssl
```
````

````{md-tab-item} Conda
```{code-block} bash
conda install htslib openssl
```
````
````{md-tab-item} Apt-get
```{code-block} bash
apt-get update && apt-get install libhts-dev libssl-dev
```
````

`````

## **Get Started**

Installing **PxBLAT** via `CONDA` **do not requires** the prerequisites.
Installing **PxBLAT** via `PyPI` requires the prerequisites.
Once you have confirmed the prerequisites, you can proceed with the software installation:

`````{md-tab-set}

````{md-tab-item} Conda
```{code-block} bash
conda install pxblat
```
````

````{md-tab-item} Pip
```{code-block} bash
pip install pxblat
```
````

`````

``````{warning}
You meet the issue _*.h cannot found_ or _undefined symbol **_ If you install `pxblat` by `pip`.
If you have installed the prerequisites, the problem is caused by incorrect environment variable {envvar}`CFLAGS`, `CXXFLAGS`,
and `LDFLAGS`, which direct compiler and linker find right location of
dependencies so as to compile and link code properly.
**The easy solution** is to install  **PxBLAT**  via `conda`.
You can also set proper environment variable if `conda` is not accessible.


`````{md-tab-set}

````{md-tab-item} Bash/Zsh
```{code-block} bash
export CFLAGS="-Idependencies"
export CXXFLAGS="-Idependencies"
...
```
````

````{md-tab-item} Fish
```{code-block} fish
set -x CFLAGS="-Idependencies"
set -x CXXLAGS="-Idependencies"
...
```
````
`````

``````

## **FAQ (Frequently Asked Questions)**

1. I cannot download `PxBLAT` via `Conda` in MacOS with Arm (M1 or M2).

A: So far, conda build `PxBLAT` in x86 instead of arrch64.
Hence we can install [prerequisites](#prerequisites) manually via `brew` or `Conda`.
Then, we can use `pip install pxblat` to install `PxBLAT`.
