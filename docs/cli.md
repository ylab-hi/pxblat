# **CLI Usage**

## **1. CLIs Overview**

[![cli](images/cli.gif)](cli)

| CLI                          |                               Usage                                |
| :--------------------------- | :----------------------------------------------------------------: |
| [server](#11-server)         |      Make a server to quickly find where DNA occurs in genome      |
| [client](#12-client)         | A client for the genomic finding program that produces a .psl file |
| [fatotwobit](#13-fatotwobit) |                    Convert fasta to 2bit format                    |
| [twobittofa](#14-twobittofa) |                    Convert 2bit to fasta format                    |

We can get completion for current shell via `pxblat --install-completion`.
The help message is got from

```bash
$ pxblat -h

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

### **1.1 Server**

```bash
$ pxblat server -h

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

#### Start a server

```bash
$ pxblat server start localhost 650000 twobit.2bit
```

```bash
$ pxblat server start -h

 Usage: pxblat server start [OPTIONS] HOST PORT TWO_BIT

 To set up a server.
 gfServer start host port file(s)
 where the files are .2bit or .nib format files specified relative to the current directory

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    host         TEXT     [default: None] [required]                                                                                                         │
│ *    port         INTEGER  [default: None] [required]                                                                                                         │
│ *    two_bit      FILE     Two bit file [default: None] [required]                                                                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --tile-size              INTEGER  Size of n-mers to index.  Default is 11 for nucleotides, 4 for proteins (or translated nucleotides). [default: 11]          │
│ --stepSize               INTEGER  Spacing between tiles. Default is tileSize. [default: 11]                                                                   │
│ --min-match              INTEGER  Number of n-mer matches that trigger detailed alignment. Default is 2 for nucleotides, 3 for proteins. [default: 2]         │
│ --trans                           Translate database to protein in 6 frames.                                                                                  │
│ --log                    TEXT     Keep a log file that records server requests. [default: None]                                                               │
│ --mask                            Use masking from .2bit file.                                                                                                │
│ --repMatch               INTEGER  Number of occurrences of a tile (n-mer) that triggers repeat masking the tile. Default is 1024. [default: 0]                │
│ --noSimpRepMask                   Suppresses simple repeat masking.                                                                                           │
│ --maxDnaHits             INTEGER  Maximum number of hits for a DNA query that are sent from the server. [default: 100]                                        │
│ --maxTransHits           INTEGER  Maximum number of hits for a translated query that are sent from the server. [default: 200]                                 │
│ --maxNtSize              INTEGER  Maximum size of untranslated DNA query sequence. [default: 40000]                                                           │
│ --perSeqMax              FILE     File contains one seq filename (possibly with ':seq' suffix) per line. [default: None]                                      │
│ --canStop                         If set, a quit message will actually take down the server.                                                                  │
│ --indexFile              FILE     Index file create by gfServer index. [default: None]                                                                      │
│ --timeout                INTEGER  Timeout in seconds. [default: 90]                                                                                           │
│ --help           -h               Show this message and exit.                                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Get files of a running server

```bash
$ pxblat server files localhost 650000
```

```bash
$ pxblat server files -h

 Usage: pxblat server files [OPTIONS] HOST PORT

 To get input file list.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    host      TEXT     [default: None] [required]                                                                                                            │
│ *    port      INTEGER  [default: None] [required]                                                                                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Get status of a running server

```bash
$ pxblat server status localhost 650000
```

```bash
$ pxblat server status -h

 Usage: pxblat server status [OPTIONS] HOST PORT

 To figure out if server is alive, on static instances get usage statics.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    host      TEXT     [default: None] [required]                                                                                                            │
│ *    port      INTEGER  [default: None] [required]                                                                                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --trans            Translate database to protein in 6 frames.                                                                                                 │
│ --help   -h        Show this message and exit.                                                                                                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Stop a running server

```bash
$ pxblat server stop localhost 650000
```

```bash
$ pxblat server stop -h

 Usage: pxblat server stop [OPTIONS] HOST PORT

 To remove a server.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    host      TEXT     [default: None] [required]                                                                                                            │
│ *    port      INTEGER  [default: None] [required]                                                                                                            │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### **1.2 Client**

```bash
$ pxblat client localhost 65000 twobit_dir fasta1.fa out.psl
```

```bash
$ pxblat client -h

 Usage: pxblat client [OPTIONS] HOST PORT SEQDIR INFASTA OUTPSL

 A client for the genomic finding program that produces a .psl file.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    host         TEXT     The name of the machine running the gfServer [default: None] [required]                                        │
│ *    port         INTEGER  The same port that you started the gfServer with [default: None] [required]                                    │
│ *    seqdir       PATH     The path of the .2bit or .nib files relative to the current dir [default: None] [required]                     │
│ *    infasta      PATH     Fasta format file.  May contain multiple records [default: None] [required]                                    │
│ *    outpsl       PATH     where to put the output [default: None] [required]                                                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --type           -t      TEXT     Database type. Type is one of: dna, prot, dnax [default: dna]                                           │
│ --qtype          -q      TEXT     Query type. Type is one of: dna, rna, prot, dnax, rnax [default: dna]                                   │
│ --prot                            Synonymous with -t=prot -q=prot.                                                                        │
│ --dots                   INTEGER  Output a dot every N query sequences. [default: 0]                                                      │
│ --nohead                          Suppresses 5-line psl header.                                                                           │
│ --minScore               INTEGER  Sets minimum score.  This is twice the matches minus the mismatches minus some sort of gap penalty.     │
│                                   Default is 30.                                                                                          │
│                                   [default: 30]                                                                                           │
│ --minIdentity            INTEGER  Sets minimum sequence identity (in percent).  Default is 90 for nucleotide searches, 25 for protein or  │
│                                   translated protein searches.                                                                            │
│                                   [default: 90.0]                                                                                         │
│ --out                    TEXT     Controls output file format.  Type is one of: psl, pslx, axt, maf, sim4, wublast, blast, blast8, blast9 │
│                                   [default: psl]                                                                                          │
│ --maxIntron              INTEGER  Sets maximum intron size. Default is 750000. [default: 750000]                                          │
│ --genome                 TEXT     dynamic                                                                                                 │
│ --genomeDataDir          TEXT     dynamic                                                                                                 │
│ --help           -h               Show this message and exit.                                                                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### **1.3 fatotwobit**

```bash
$ pxblat fatotwobit in.fa out.2bit
```

```bash
$ pxblat fatotwobit -h

 Usage: pxblat fatotwobit [OPTIONS] in.fa [inf2.fa in3.fa ...] out.2bit

 Convert DNA from fasta to 2bit format.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    infa         in.fa [inf2.fa in3.fa ...]  The fasta files [required]                                                                  │
│ *    out2bit      out.2bit                    The output file [required]                                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --long                    Use 64-bit offsets for index. Allow for twoBit to contain more than 4Gb of sequence.                            │
│ --nomask                  Ignore lower-case masking in fa file.                                                                           │
│ --stripVersion            Strip off version number after '.' for GenBank accessions.                                                      │
│ --ignoreDups              Convert first sequence only if there are duplicate sequence names. Use 'twoBitDup' to find duplicate sequences. │
│ --help          -h        Show this message and exit.                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### **1.4 twobittofa**

```bash
$ pxblat twobittofa input.2bit out.fa
```

```bash
$ pxblat twobittofa -h

 Usage: pxblat twobittofa [OPTIONS] input.2bit out.fa

 Convert all or part of .2bit file to fasta.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    input2bit      input.2bit  The input 2bit file [default: None] [required]                                                            │
│ *    outputfa       out.fa      The output fasta file [required]                                                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --seq              TEXT     Restrict this to just one sequence.                                                                           │
│ --start            INTEGER  Start at given position in sequence (zero-based). [default: 0]                                                │
│ --end              INTEGER  End at given position in sequence (non-inclusive). [default: 0]                                               │
│ --seqList          TEXT     File containing list of the desired sequence names                                                            │
│ --noMask                    Convert sequence to all upper case.                                                                           │
│ --bpt              TEXT     Use bpt index instead of built-in one.                                                                        │
│ --bed              TEXT     Grab sequences specified by input.bed.                                                                        │
│ --bedPos                    With -bed, use chrom:start-end as the fasta ID in output.fa.                                                  │
│ --udcDir           TEXT     Place to put cache for remote bigBed/bigWigs.                                                                 │
│ --help     -h               Show this message and exit.                                                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## **2. Reference**

```{eval-rst}
.. click:: pxblat.cli.cli:typer_click_object
   :prog: pxblat
   :nested: full
```
