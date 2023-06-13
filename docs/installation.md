# Install

## **Prerequisites**

Before you begin with the installation and use of `pxblat`, there are certain prerequisites that need to be met.
The following sections detail the necessary software, hardware, and knowledge prerequisites that you should have before you start.
`pxblat` has been tested and runs on the following operating systems **Linux** and **macOS**.
Programming Languages and Libraries: You should have the following installed:

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

``````{tip}
You meet the issue _*.h canot found_ or _undefined symbol **_ If you install `pxblat` by `pip`.
The problem is caused by incorrect environment variable `CFLAGS`, `CXXFLAGS`,
and `LDFLAGS`, which direct compiler and linker find right location of
dependencies so as to compile and link code properly.
**The easy solution** is to install `pxblat` via `conda`.
You can also set proper environment variable if `conda` is not accessible.



`````{md-tab-set}

````{md-tab-item} Bash
```{code-block} bash
export CFLAGS="test"
```
````

````{md-tab-item} Fish
```{code-block} fish
set -gs CFLAGS="test"
```
````
`````

``````
