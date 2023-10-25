# **Tutorial**

```{warning}
Make sure you have installed PxBLAT, otherwise please go-to ({doc}`installation`).
```

```{important}
We do not assume you already know common formats and BLAT, which is a standout within the bioinformatics landscape and is recognized for its capability to conduct genome sequence alignments.
BLAT can help us know where one or several sequences can be mapped to the reference for nucleotide or peptide sequences.
Assume we have multiple sequences, and want to know where these sequences can be mapped in reference sequence.
After reading the tutorial, you are supported to know how to use PxBLAT to align your sequences.
```

**PxBLAT** binds the codebase of [BLAT(v.37x1)][BLAT(v.37x1)], and aims to provide efficient and
ergonomic APIs. Let's take the journey to show features **PxBLAT** provides.

## 1. Understanding the FASTA Format

In bioinformatics, the FASTA format is a widely used text-based format for representing nucleotide sequences or peptide sequences and their associated information.
Below, we will introduce the FASTA format, its structure, and how it is utilized in bioinformatics applications.

The FASTA format is a simple, text-based format for representing biological sequences.
Each entry in a FASTA file begins with a single-line description, followed by the sequence data.
The description line is distinguished from the sequence data by a greater-than (`>`) symbol at the beginning.

### Structure of a FASTA File

Here is an example to illustrate the structure of a FASTA file:

```
>sequence1
ATGCTAGCTAGCTAGCTAGCTAGCTA
GCTAGCTAGCTAGCTAGCTAGCTAGC
TAGCTAGCTAGCTAGCTAGCTAGCTA
```

In this example:

- `>sequence1` are description lines for two different sequences.
- The sequences themselves are represented in the lines following the description lines.
- Sequences can span multiple lines for readability, and there are no line length restrictions.

In bioinformatics, the FASTA format is used to represent sequences for various applications, such as:

- Sequence alignment: Comparing sequences to find similarities and differences.
- Database search: Searching for sequences in large databases.
- Phylogenetics: Studying the evolutionary relationships between sequences.

The FASTA format is a fundamental part of bioinformatics, providing a simple and efficient way to represent biological sequences.
Understanding this format is crucial for anyone looking to work in the field or use bioinformatics tools, including **PxBLAT**.

## 2. Prepare Example Data

### Download sequences and reference examples

- Let's create a new directory first.

```bash
mkdir tutorial
cd tutorial
```

- Download reference data {download}`⬇️ test_ref.fa <tutorial_data/test_ref.fa>`, which is fasta format.

````{example} Download via wget
:collapsible: close

```bash
wget https://raw.githubusercontent.com/ylab-hi/pxblat/main/tests/data/test_ref.fa
```

````

Let's check the reference data

```console
$ head test_ref.fa
>chr1
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
taaccctaaccctaaccctaaccctaaccctaaccctaaccctaacccta
accctaaccctaaccctaaccctaaccctaaccctaaccctaaccctaac
cctaacccaaccctaaccctaaccctaaccctaaccctaaccctaacccc
taaccctaaccctaaccctaaccctaacctaaccctaaccctaaccctaa
ccctaaccctaaccctaaccctaaccctaacccctaaccctaaccctaaa
ccctaaaccctaaccctaaccctaaccctaaccctaaccccaaccccaac
cccaaccccaaccccaaccccaaccctaacccctaaccctaaccctaacc
ctaccctaaccctaaccctaaccctaaccctaaccctaacccctaacccc

$ wc -l test_ref.fa
301 test_ref.fa
```

- Download test sequences {download}`⬇️ test_case1.fa <tutorial_data/test_case1.fa>`, which is fasta format.

````{example} Download via wget
:collapsible: close

```bash
wget https://raw.githubusercontent.com/ylab-hi/pxblat/main/tests/data/test_case1.fa
```
````

Let's check test reference

```bash
$ head test_case1.fa
>case1
TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCA
CACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTC
TCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCA
A
```

Now we already have `test_case1.fa` and `test_ref.fa` for following analysis.

```bash
$ ls
test_case1.fa  test_ref.fa
```

## 3. Convert FASTA to 2bit

Before we query certain sequence to a reference `test_ref.fa`, we need to convert [fasta][fasta] format to [.2bit][.2bit] file for reference sequence `test_ref.fa`.
**PxBLAT** provides a function {func}`.fa_to_two_bit`.
Also, **PxBLAT** supports to convert the `.2bit` file back to fasta format via {func}`.two_bit_to_fa`, for example,

```{tip}
Click the blinking circle cross, and you will be blessed and get more information.
```

```{eval-rst}
.. code-block:: python
    :name: fa_to_two_bit_block
    :linenos:

    from pxblat import fa_to_two_bit

    fa_to_two_bit(
        ["test_ref.fa"],  # (1)!
        "test_ref.2bit",  # (2)!
        noMask=False,
        stripVersion=False,
        ignoreDups=False,
        useLong=False,
    )

    print("Done")

.. code-annotations::
    #. Same as `BLAT`, :func:`.fa_to_two_bit` can accept  multilple inputs
    #. Output file path
```

Let's create a Python file named `2bit.py`, and copy and paste [code above](#fa_to_two_bit_block) to `2bit.py`.
Then, execute the `2bit.py`

```bash
python 2bit.py
```

After, we will get a new file named `test_ref.2bit`, which is the 2bit file we
need to align sequences to reference.

```bash
$ ls
2bit.py  test_case1.fa  test_ref.2bit  test_ref.fa
```

The code equals `faToTwoBit fasta1.fa out.2bit` by `BLAT(v. 37x1)`.

```bash
$ faToTwoBit
faToTwoBit - Convert DNA from fasta to 2bit format
usage:
   faToTwoBit in.fa [in2.fa in3.fa ...] out.2bit
options:
   -long          use 64-bit offsets for index.   Allow for twoBit to contain more than 4Gb of sequence.
                  NOT COMPATIBLE WITH OLDER CODE.
   -noMask        Ignore lower-case masking in fa file.
   -stripVersion  Strip off version number after '.' for GenBank accessions.
   -ignoreDups    Convert first sequence only if there are duplicate sequence
                  names.  Use 'twoBitDup' to find duplicate sequences.
$ faToTwoBit test_ref.fa test_ref.2bit
$ ls
test_ref.2bit test_ref.fa
```

Moreover, **PxBLAT** provides flexible options to allow conducting the conversion in {doc}`cli`.

## 4. Query Sequences

**PxBLAT** contains {class}`pxblat.Server` and {class}`pxblat.Client`.
We use them to align our sequences in two steps.

1. Start {class}`pxblat.Server`
2. {class}`pxblat.Client` send our sequence to {class}`pxblat.Server` for
   alignment

Generally, {class}`pxblat.Server` has three status including `preparing`, `ready`, and `stop`.
It only accepts sequence alignment task in `ready` status.
Hence, in real life we need to make sure the {class}`pxblat.Server` is in `ready` status before {class}`pxblat.Client`send sequences.
**PxBLAT** allow this process more smooth without bothering intermediate file.

**PxBLAT** provide several ways to start the {class}`pxblat.Server`.

### 4.1 Start {class}`pxblat.Server` in context mode

```{eval-rst}
.. code-block:: python
    :name: query_context_block
    :linenos:

    from pxblat import Client, Server


    def query_context():
        host = "localhost"  # (1)!
        port = 65000  # (2)!
        seq_dir = "."  # (3)!
        two_bit = "./test_ref.2bit"  # (4)!

        client = Client(
            host=host,
            port=port,
            seq_dir=seq_dir,
            min_score=20,  # (5)!
            min_identity=90,  # (6)!
        )

        with Server(host, port, two_bit, can_stop=True, step_size=5) as server:
            # work() assume work() is your own function that takes time to prepare something
            server.wait_ready()  # (7)!
            result1 = client.query("ATCG")  # (8)!
            result2 = client.query("AtcG")  # (9)!
            result3 = client.query("test_case1.fa")  # (10)!
            result4 = client.query(["ATCG", "ATCG"])  # (11)!
            result5 = client.query(["test_case1.fa"])  # (12)!
            result6 = client.query(["cgTA", "test_case1.fa"])  # (13)!
            print(result3[0]) # print result


    if __name__ == "__main__":
        query_context()

.. code-annotations::
    #. :attr:`.Client.host` is the hostname or IP address of the current running :class:`.Server`.
    #. :attr:`.Client.post` is the port number of the current running :class:`.Server`.
    #. :attr:`.Client.seq_dir` is the directory including `test_ref.fa` and `test_ref.2bit`
    #. `two_bit` is the 2bit file that :ref:`we already create <fa_to_two_bit_block>`
    #. :attr:`.Client.min_score`  is the minimum score for the alignment.
    #. :attr:`.Client.min_identity`  is the minimum identity for the alignment.
    #. block current thread to wait server to be ready
    #. :meth:`.Client.query` accepts a :class:`str` consisting of nucleotide or peptide sequences, e.g. `"ATCG"`
    #. :meth:`.Client.query` accepts nucleotide or peptide sequences that are case-insensitive, e.g. `"AtcG"`
    #. :meth:`.Client.query` accepts a path of fasta file, e.g. `"./test_case1.fa"`
    #. :meth:`.Client.query` accepts a :class:`list` of :class:`str` consisting of nucleotide or peptide sequences, e.g. `["ATCG","CTGAG"]`
    #. :meth:`.Client.query` accepts a :class:`list` of path of fasta files, e.g. `["test_case1.fa"]`
    #. :meth:`.Client.query` accepts a :class:`list` of :class:`str` and path, e.g. `["ATCG", "test_case1.fa"]`
```

{meth}`.Client.query` accepts parameters of several types:

- Path of fasta file e.g. `./test_case1.fa`
- {class}`str` consisting of nucleotide or peptide sequences that are case-insensitive, e.g. `ATCG`, or `ATcg`
- {class}`list` of {class}`str` consisting of nucleotide or peptide sequences that are case-insensitive, e.g. `["AtcG","CTGAG"]`
- {class}`list` of path of fasta files, e.g. `["data/fasta1.fa", "./test_case1.fa"]`
- {class}`list` of `str` and path, e.g. `["ATCG", "data/fasta1.fa"]`

Let's Create a new Python script named `query_context.py`, and copy and paste [code above](#query_context_block) to the script.
Then execute the Python script.

```bash
$ python query_context.py
Program: blat (v.37x1)
  Query: case1 (151)
         <unknown description>
 Target: <unknown target>
   Hits: ----  -----  ----------------------------------------------------------
            #  # HSP  ID + description
         ----  -----  ----------------------------------------------------------
            0      1  chr1  <unknown description>
```

{meth}`.Client.query` return [`QueryResult`](#query-result), which is introduced later.

### 4.2 Start {class}`pxblat.Server` in general mode

```{eval-rst}
.. code-block:: python
    :name: query_general_block
    :linenos:

    from pxblat import Client, Server

    def query_general():
        host = "localhost"
        port = 65000
        seq_dir = "."
        two_bit = "./test_ref.2bit"

        client = Client(
            host=host,
            port=port,
            seq_dir=seq_dir,
            min_score=20,
            min_identity=90,
        )

        server = Server(host, port, two_bit, can_stop=True, step_size=5)
        server.start() # (1)!
        # work() assume work() is your own function that takes time to prepare something
        server.wait_ready() # (2)!
        result1 = client.query(["actg", "test_case1.fa"])
        # another_work() assume the func is your own function that takes time
        result2 = client.query("test_case1.fa")
        server.stop()  # (3)!

        print(f"{result1=}")
        print(f"{result2=}")


    if __name__ == "__main__":
        query_general()

.. code-annotations::
    #. start server
    #. block until the server  is ready
    #. stop the current running server
```

```{note}
the explanation of parameters including `two_bit` and `seq_dir` etc. is same as
[previous code](#query_context_block)
```

Let's Create a new Python script named `query_general.py`, and copy and paste [code above](#query_general_block) to the script.
Then execute the Python script.

```bash
$ python query_general.py
result1=[None, QueryResult(id='case1', 1 hits)]
result2=[QueryResult(id='case1', 1 hits)]
```

```{note}
`None` means the sequence cannot be mapped to the reference.
```

Although {class}`.Server` and {class}`.Client` already consider most contexts, **PxBLAT** provides {class}`.ClientThread` that can launch a thread to
query sequence.
Free feel to check that if you have interests.

## 5. Query Result

Right now we know how to query certain sequence to the reference, and let's dive into the query result and manipulate that together.

Here we use contexts mode to align sequence, and modify a little bit based on [previous code](#query_context_block)

````{example} query_context (hint: convenient to copy)
:collapsible: close

```python
from pxblat import Client, Server

def query_context():
    host = "localhost"
    port = 65000
    seq_dir = "."
    two_bit = "./test_ref.2bit"
    client = Client(
    host=host,
    port=port,
    seq_dir=seq_dir,
    min_score=20,
    min_identity=90,
    )
    with Server(host, port, two_bit, can_stop=True, step_size=5) as server:
        # work() assume work() is your own function that takes time to prepare something
        server.wait_ready()
        result1 = client.query("ATCG")
        result2 = client.query("AtcG")
        result3 = client.query("test_case1.fa")
        result4 = client.query(["ATCG", "ATCG"])
        result5 = client.query(["test_case1.fa"])
        result6 = client.query(["cgTA", "test_case1.fa"])
    return [result1, result2, result3, result4, result5, result6]
```
````

```{eval-rst}

.. code-block:: pycon
   :name: query_result_block

   >>> from pxblat import Client, Server
   >>> def query_context():
   ...     host = "localhost"
   ...     port = 65000
   ...     seq_dir = "."
   ...     two_bit = "./test_ref.2bit"
   ...     client = Client(
   ...     host=host,
   ...     port=port,
   ...     seq_dir=seq_dir,
   ...     min_score=20,
   ...     min_identity=90,
   ...     )
   ...     with Server(host, port, two_bit, can_stop=True, step_size=5) as server:
   ...         # work() assume work() is your own function that takes time to prepare something
   ...         server.wait_ready()
   ...         result1 = client.query("ATCG")
   ...         result2 = client.query("AtcG")
   ...         result3 = client.query("test_case1.fa")
   ...         result4 = client.query(["ATCG", "ATCG"])
   ...         result5 = client.query(["test_case1.fa"])
   ...         result6 = client.query(["cgTA", "test_case1.fa"])
   ...     return [result1, result2, result3, result4, result5, result6]
   >>> results = query_context() # get all alignment results
   >>> results
   [[None], [None], [QueryResult(id='case1', 1 hits)], [None, None], [QueryResult(id='case1', 1 hits)], [None, QueryResult(id='case1', 1 hits)]]
   >>> results[2] # let's pick up the result of test_case1.fa
   [QueryResult(id='case1', 1 hits)]
   >>> result3 = results[2]
   >>> result3
   [QueryResult(id='case1', 1 hits)]
   >>> print(result3[0]) # let's show information of the result
   Program: blat (v.37x1)
     Query: case1 (151)
            <unknown description>
    Target: <unknown target>
      Hits: ----  -----  ----------------------------------------------------------
               #  # HSP  ID + description
            ----  -----  ----------------------------------------------------------
               0      1  chr1  <unknown description>
   >>> result = result3[0] # let's get the element in the result list
   >>> result
   QueryResult(id='case1', 1 hits)
   >>> print(result)
   Program: blat (v.37x1)
     Query: case1 (151)
            <unknown description>
    Target: <unknown target>
      Hits: ----  -----  ----------------------------------------------------------
               #  # HSP  ID + description
            ----  -----  ----------------------------------------------------------
               0      1  chr1  <unknown description>
   >>> result.hsps # check all  high-scoring pairs (HSPs)
   [HSP(hit_id='chr1', query_id='case1', 1 fragments)]
   >>> result[0] # check the top hsp
   Hit(id='chr1', query_id='case1', 1 hsps)
   >>> print(result[0]) # show more information about top hsp
   Query: case1
          <unknown description>
     Hit: chr1 (14999)
          <unknown description>
    HSPs: ----  --------  ---------  ------  ---------------  ---------------------
             #   E-value  Bit score    Span      Query range              Hit range
          ----  --------  ---------  ------  ---------------  ---------------------
             0         ?          ?       ?          [0:151]          [12699:12850]
   >>> top_hsp = result.hsps[0]
   >>> top_hsp
   HSP(hit_id='chr1', query_id='case1', 1 fragments)
   >>> print(top_hsp)
         Query: case1 <unknown description>
           Hit: chr1 <unknown description>
   Query range: [0:151] (1)
     Hit range: [12699:12850] (1)
   Quick stats: evalue ?; bitscore ?
     Fragments: 1 (? columns)
   >>> top_hsp.query_id # test_case1's id in top_hsp
   'case1'
   >>> top_hsp.query_range # test_case1's query_range in top_hsp
   (0, 151)
   >>> top_hsp.query_span # test_case1's query_span in top_hsp
   151
   >>> top_hsp.query_start # test_case1's query_start in top_hsp
   0
   >>> top_hsp.query_strand # test_case1's query_strand in top_hsp
   1
   >>> top_hsp.hit_id # in top_hsp, test_case1 hit `chr1` of the reference
   'chr1'
   >>> top_hsp.hit_range #  in top_hsp, test_case1 hit (12699, 12850) of the reference
   (12699, 12850)
   >>> top_hsp.hit_start
   12699
   >>> top_hsp.hit_strand # in top_hsp, test_case1 hit strand of the reference (1 means positive strand)
   1
   >>> top_hsp.
   top_hsp.aln                 top_hsp.hit_frame           top_hsp.ident_pct           top_hsp.query_frame_all
   top_hsp.aln_all             top_hsp.hit_frame_all       top_hsp.is_fragmented       top_hsp.query_gap_num
   top_hsp.aln_annotation      top_hsp.hit_gap_num         top_hsp.match_num           top_hsp.query_gapopen_num
   top_hsp.aln_annotation_all  top_hsp.hit_gapopen_num     top_hsp.match_rep_num       top_hsp.query_id
   top_hsp.aln_span            top_hsp.hit_id              top_hsp.mismatch_num        top_hsp.query_inter_ranges
   top_hsp.fragment            top_hsp.hit_inter_ranges    top_hsp.molecule_type       top_hsp.query_inter_spans
   top_hsp.fragments           top_hsp.hit_inter_spans     top_hsp.n_num               top_hsp.query_is_protein
   top_hsp.gap_num             top_hsp.hit_range           top_hsp.output_index        top_hsp.query_range
   top_hsp.gapopen_num         top_hsp.hit_range_all       top_hsp.query               top_hsp.query_range_all
   top_hsp.hit                 top_hsp.hit_span            top_hsp.query_all           top_hsp.query_span
   top_hsp.hit_all             top_hsp.hit_span_all        top_hsp.query_description   top_hsp.query_span_all
   top_hsp.hit_description     top_hsp.hit_start           top_hsp.query_end           top_hsp.query_start
   top_hsp.hit_end             top_hsp.hit_start_all       top_hsp.query_end_all       top_hsp.query_start_all
   top_hsp.hit_end_all         top_hsp.hit_strand          top_hsp.query_features      top_hsp.query_strand
   top_hsp.hit_features        top_hsp.hit_strand_all      top_hsp.query_features_all  top_hsp.query_strand_all
   top_hsp.hit_features_all    top_hsp.ident_num           top_hsp.query_frame         top_hsp.score

```

````{example} query_result code
:collapsible: close

```{literalinclude} tutorial_data/query_result.py
```

````

We can precisely determine the regions of our sequence that align with specific parts of the reference.
We are able to know strand, start position, and end position for alignment part
both for our sequence and the reference.
The last part of [code example](#query_result_block) shows all methods of a high-scoring pairs (HSP).

## 6. APIs Compared to `BLAT`

So far, **PxBLAT** provides APIs, including {class}`.Client`, {class}`.Server`, {func}`.two_bit_to_fa` and {func}`.fa_to_two_bit`,
as well as other useful functions ({doc}`reference`).
**PxBLAT** is able to finish the most significant features of `BLAT`.
Here is a table in which the features are compared.

```{list-table} APIs Comparison
   :header-rows: 1
   :align: center

   * - PxBLAT
     - BLAT
   * - {class}`.Client`
     - [gfClient][gfClient]
   * - {class}`.Server`
     - [gfServer][gfServer]
   * - {func}`.two_bit_to_fa`
     - [twoBitToFa][twoBitToFa]
   * - {func}`.fa_to_two_bit`
     - [faToTwoBit][faToTwoBit]

```

## 7. Beyond APIs

Even though `PxBLAT` is designed as library, it provides command-line tools
using its APIs.
That could provide more choices for user according to different situations.
{doc}`reference` contain more details, and do not hesitate to check.

```{bug}
please feel free to [edit the tutorial](https://github.com/ylab-hi/pxblat/edit/main/docs/tutorial.md) or [open an issue](https://github.com/ylab-hi/pxblat/issues/new/choose), if you find some unclear or wrong statement.

```

<!-- links -->

[gfclient]: https://genome.ucsc.edu/goldenpath/help/blatSpec.html#gfClientUsage
[gfserver]: https://genome.ucsc.edu/goldenpath/help/blatSpec.html#gfServerUsage
[twobittofa]: https://genome.ucsc.edu/goldenpath/help/blatSpec.html#twoBitToFaUsage
[fatotwobit]: https://genome.ucsc.edu/goldenpath/help/blatSpec.html#faToTwoBitUsage
[.2bit]: https://genome.ucsc.edu/FAQ/FAQformat.html#format7
[fasta]: https://en.wikipedia.org/wiki/FASTA_format#:~:text=In%20bioinformatics%20and%20biochemistry%2C%20the,represented%20using%20single%2Dletter%20codes.&text=The%20format%20allows%20for%20sequence%20names%20and%20comments%20to%20precede%20the%20sequences
[blat(v.37x1)]: https://github.com/ucscGenomeBrowser/kent
[bio]: https://biopython.org/docs/latest/api/Bio.SearchIO.html?highlight=queryresult
[chr20.fa]: https://raw.githubusercontent.com/ylab-hi/pxblat/main/benchmark/data/chr20.fa
[chr20.2bit]: https://raw.githubusercontent.com/ylab-hi/pxblat/main/benchmark/data/chr20.2bit
