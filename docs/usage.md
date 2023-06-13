# **CLI Usage**

## **Available CLIs**

| CLI                       |                               Usage                                |
| :------------------------ | :----------------------------------------------------------------: |
| [server](#server)         |      Make a server to quickly find where DNA occurs in genome      |
| [client](#client)         | A client for the genomic finding program that produces a .psl file |
| [fatotwobit](#fatotwobit) |               Convert DNA from fasta to 2bit format                |

We can get completion for current shell via `pxblat --install-completion`.
The help message is got from

```{code-block} bash

> pxblat -h
Usage: pxblat [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion            Install completion for the current shell.                                                                                                                                                                                                    │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                                                                                                                                             │
│ --help                -h        Show this message and exit.                                                                                                                                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ client                                 A client for the genomic finding program that produces a .psl file                                                                                                                                                                    │
│ fatotwobit                             Convert DNA from fasta to 2bit format                                                                                                                                                                                                 │
│ server                                 Make a server to quickly find where DNA occurs in genome                                                                                                                                                                              │
│ twobittofa                             Convert all or part of .2bit file to fasta                                                                                                                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

 YangyangLi 2023 yangyang.li@northwstern.edu
```

### **Server**

```{code-block} bash
> pxblat server -h
Usage: pxblat server [OPTIONS] COMMAND [ARGS]...

 Make a server to quickly find where DNA occurs in genome

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                                                                                                                                                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ files                    To get input file list                                                                                                                                                                                                                              │
│ start                    To set up a server                                                                                                                                                                                                                                  │
│ status                   To figure out if server is alive, on static instances get usage statics                                                                                                                                                                             │
│ stop                     To remove a server                                                                                                                                                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```{code-block} bash
pxblat server localhost 650000
```

### **Client**

### **fatotwobit**

### **twobittofa**

## **CLI Reference**

```{eval-rst}
.. click:: pxblat.cli.cli:typer_click_object
   :prog: pxblat
   :nested: full
```
