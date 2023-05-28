# CLI Usage

## Available CLIs

| CLI                       |                               Usage                                |
| :------------------------ | :----------------------------------------------------------------: |
| [server](#server)         |      Make a server to quickly find where DNA occurs in genome      |
| [client](#client)         | A client for the genomic finding program that produces a .psl file |
| [fatotwobit](#fatotwobit) |               Convert DNA from fasta to 2bit format                |

```{code-block} console

> pxblat -h
 Usage: pxblat [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion            Install completion for the current shell.                                                                                                │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                                         │
│ --help                -h        Show this message and exit.                                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ client                   A client for the genomic finding program that produces a .psl file                                                                              │
│ fatotwobit               Convert DNA from fasta to 2bit format                                                                                                           │
│ server                   Make a server to quickly find where DNA occurs in genome                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

 YangyangLi 2023 yangyang.li@northwstern.edu
```

### server

### client

### fatotwobit

## CLI Reference

```{eval-rst}
.. click:: pxblat.cli.cli:typer_click_object
   :prog: pxblat
   :nested: full
```
