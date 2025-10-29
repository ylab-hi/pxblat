# **Tutorial**

```{warning}
Before proceeding, ensure you have PxBLAT installed. If not, please refer to our ({doc}`installation`).
```

```{important}
In this tutorial, we aim to introduce you to PxBLAT, a powerful tool for genome sequence alignments.
We cater to both beginners and those new to BLAT, ensuring a comprehensive understanding by the end.
By the end of this guide, you should be able to use PxBLAT confidently for aligning nucleotide or peptide sequences.
```

**PxBLAT** builds upon the foundation of [BLAT(v.37x1)][BLAT(v.37x1)], striving to provide both efficient and user-friendly APIs.
Let's embark on a journey to explore the features and capabilities that **PxBLAT** offers.

In this tutorial, we will be utilizing data derived from human samples as our primary example.
Let's presume we have acquired several sequences from human sources; however, the precise locations of these sequences within the human reference genome remain unknown.
Utilizing PxBLAT, we can align these sequences to the human reference genome, facilitating the identification of their accurate genomic locations.
For instance, through this alignment, we may discover that one of the sequences originates from chromosome 1 of the human reference genome.

## 1. Grasping the FASTA Format

In the realm of bioinformatics, the FASTA format stands as a text-based standard for denoting nucleotide or peptide sequences alongside their pertinent information.
This section is dedicated to elucidating the FASTA format, its structural components, and its prevalent applications in bioinformatics.

### FASTA Format Demystified

The FASTA format is characterized by its simplicity, encapsulating biological sequences in a text-based file.
Each entry within a FASTA file commences with a description line, immediately followed by the sequence data.
Notably, the description line is marked by a greater-than (`>`) symbol at its beginning.

Consider the following example to better understand the structure of a FASTA file:

```
>sequence1
ATGCTAGCTAGCTAGCTAGCTAGCTA
GCTAGCTAGCTAGCTAGCTAGCTAGC
TAGCTAGCTAGCTAGCTAGCTAGCTA
```

In this example:

- `>sequence1` signifies the description line for the sequence.
- The sequence data is encapsulated in the subsequent lines.
- For enhanced readability, sequences can extend across multiple lines, and there is no restriction on line length.

fasta files find extensive applications in various bioinformatics tasks, including but not limited to:

- Sequence alignment: Identifying similarities and distinctions between sequences.
- Database search: Scouring large databases for specific sequences.
- Phylogenetics: Analyzing the evolutionary connections between sequences.

Grasping the fasta format is indispensable for anyone aspiring to thrive in bioinformatics or utilize tools like **PxBLAT**.

## 2. Preparing Example Data

### Acquiring Sequences and Reference Data

- Begin by creating a new directory:

```bash
mkdir tutorial
cd tutorial
```

- Download reference data {download}`⬇️ test_ref.fa <tutorial_data/test_ref.fa>`(in fasta format).

The file `test_ref.fa` represents a segment of chromosome 1 from the human reference genome (hg38).

````{example} Download via wget
:collapsible: close

```bash
wget https://raw.githubusercontent.com/ylab-hi/pxblat/main/docs/tutorial_data/test_ref.fa
```

````

Inspect the reference data:

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

- Download test sequences {download}`⬇️ test_case1.fa <tutorial_data/test_case1.fa>`(in fasta format).

````{example} Download via wget
:collapsible: close

```bash
wget https://raw.githubusercontent.com/ylab-hi/pxblat/main/docs/tutorial_data/test_case1.fa
```
````

Inspect the test sequences:

```bash
$ head test_case1.fa
>case1
TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCA
CACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTC
TCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCA
A
```

With `test_case1.fa` and `test_ref.fa` now available, we're set to proceed to the next steps of the analysis.

```bash
$ ls
test_case1.fa  test_ref.fa
```

## 3. Transforming FASTA to 2bit Format

In order to align a query sequence to our reference `test_ref.fa`, it's necessary to convert the FASTA formatted file to a .2bit file.
**PxBLAT** facilitates this process with the {func}`.fa_to_two_bit` function.
Additionally, **PxBLAT** allows for the conversion of .2bit files back to the FASTA format using the {func}`.two_bit_to_fa` function.
For further insights and usage details, refer to the following tip.

```{tip}
Click on the blinking circle cross icon for comprehensive information and usage examples.
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
    #. Define the path for the output .2bit file.
```

To proceed, create a Python script named `2bit.py` and paste the [code provided above](#fa_to_two_bit_block) into the script.
Execute the script with the following command:

```bash
python 2bit.py
```

After, we will get a new file named `test_ref.2bit` in working directory, which is the 2bit file we
need to align sequences to reference.

```bash
$ ls
2bit.py  test_case1.fa  test_ref.2bit  test_ref.fa
```

It's worth noting that this operation is equivalent to running `faToTwoBit fasta1.fa out.2bit` using `BLAT(v. 37x1)`.

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

For those who prefer command line interfaces, **PxBLAT** offers a variety of options for conversion available in {doc}`cli`.

## 4. Conducting Sequence Queries

**PxBLAT** provides two main classes for aligning sequences: {class}`pxblat.Server` and {class}`pxblat.Client`.
The alignment process is executed in two primary steps:

1. Initiate the {class}`pxblat.Server`.
2. Utilize {class}`pxblat.Client` to send sequence to {class}`pxblat.Server` for alignment.

Typically, {class}`pxblat.Server` operates in one of three statuses: `preparing`, `ready`, or `stop`.
It's crucial that the server is in the `ready` status before attempting to send sequences for alignment with {class}`pxblat.Client`.
**PxBLAT** is designed to streamline this process, mitigating the need for dealing with intermediate files.

Below, we provide various methods for starting the {class}`pxblat.Server`:

### 4.1 Launching {class}`pxblat.Server` in Context Mode

In this section, we delve into initiating the {class}`pxblat.Server` utilizing the context mode and sending queries through {class}`pxblat.Client`.

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
    #. :attr:`.Client.port` is the port number of the current running :class:`.Server`.
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

The {meth}`.Client.query` method is versatile, accepting a variety of parameter types:

- Path of fasta file e.g. `./test_case1.fa`
- {class}`str` consisting of nucleotide or peptide sequences that are case-insensitive, e.g. `ATCG`, or `ATcg`
- {class}`list` of {class}`str` consisting of nucleotide or peptide sequences that are case-insensitive, e.g. `["AtcG","CTGAG"]`
- {class}`list` of path of fasta files, e.g. `["data/fasta1.fa", "./test_case1.fa"]`
- {class}`list` of `str` and path, e.g. `["ATCG", "data/fasta1.fa"]`

Proceed by creating a Python script named `query_context.py`.
Copy and paste the [relevant code](#query_context_block) into this script and then execute it with Python.

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

The {meth}`.Client.query` method will return a `QueryResult` object, which we will explore in greater detail later in the documentation.

### 4.2 Launching {class}`pxblat.Server` in General Mode

In this mode, the {class}`pxblat.Server` is initiated in a more general setting.

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
The parameters `two_bit`, `seq_dir`, and others are defined similarly to what has been described in the [previous section](#query_context_block).
```

Start by creating a new Python script named `query_general.py`.
Copy and paste the [corresponding code](#query_general_block) into the script, and then execute it.

```bash
$ python query_general.py
result1=[None, QueryResult(id='case1', 1 hits)]
result2=[QueryResult(id='case1', 1 hits)]
```

In the results shown above:

- `None` signifies that the sequence could not be aligned or mapped to the reference.
- `QueryResult` instances provide details of the alignment, including the identifier of the query and the number of hits found.

Despite {class}`.Server` and {class}`.Client` being designed to handle most use cases, **PxBLAT** goes a step further by providing the {class}`.ClientThread` class.
This allows for the initiation of a thread to handle sequence queries.
For those interested, it is worth exploring this feature further.

## 5. Understanding Query Results

Having learned how to query sequences against a reference, it's now time to delve into the query results and learn how to manipulate and understand them.

We will continue using the context mode for sequence alignment, making slight modifications based on the [previous example](#query_context_block).

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

In this documentation snippet, we elucidate certain attributes and their corresponding data extracted from the alignment process:

- `top_hsp.query_id` denotes the identifier of the sequence provided in `test_case1.fa`.

```
>case1
TGAGAGGCATCTGGCCCTCCCTGCGCTGTGCCAGCAGCTTGGAGAACCCA
CACTCAATGAACGCAGCACTCCACTACCCAGGAAATGCCTTCCTGCCCTC
TCCTCATCCCATCCCTGGGCAGGGGACATGCAACTGTCTACAAGGTGCCA
A
```

- `top_hsp.query_range` encapsulates the starting and ending positions `(0, 151)` that have been aligned to the reference sequence. It's pertinent to note that the range `(0, 151)` is formatted as left-closed and right-open, denoted as `[0, 151)`.
- `top_hsp.query_span` signifies the length of the sequence segment that has been aligned to the reference.
- `top_hsp.query_start` and `top_hsp.query_end` respectively mark the starting and ending positions of the alignment.
- `top_hsp.query_strand` identifies the strand orientation of the query sequence.
- Methods prefixed with `hit`, for example `top_hsp.hit_*`, exhibit analogous information, albeit pertaining to the reference sequence rather than the query sequence.

After receiving the query results, we can precisely identify which regions of our sequence align with specific parts of the reference sequence.
This includes information about the strand, start position, and end position for the alignment on both our sequence and the reference.
The last part of the [code example](#query_result_block) showcases all the methods available for handling high-scoring pairs (HSPs).

## 6. API Comparison with `BLAT`

**PxBLAT** offers a comprehensive set of APIs, including {class}`.Client`, {class}`.Server`, {func}`.two_bit_to_fa`, {func}`.fa_to_two_bit`, among other useful functions detailed in the [reference documentation](reference).

Below is a table comparing the features of **PxBLAT** to those of `BLAT`:

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

## 7. Crafting Our Own `BLAT` Using Pure Python

Now that we have acquired the knowledge on how to align sequences to a reference and analyze the query results, it's time to consolidate all the previously covered code to create our own version of `BLAT`.

````{example} blat.py - Pure Python BLAT
:collapsible: close

```{literalinclude} tutorial_data/blat.py
```
````

```{note}
Remember to modify the directory path to include `test_ref.fa` when attempting to run the code.
```

Upon executing the script with the command:

```bash
$ python blat.py
Program: blat (v.37x1)
  Query: /var/folders/s3/vs6nrrg52sdfjk3z90p7ndt94gg4tq/T/tmptzggbu4h (151)
         <unknown description>
 Target: <unknown target>
   Hits: ----  -----  ----------------------------------------------------------
            #  # HSP  ID + description
         ----  -----  ----------------------------------------------------------
            0      1  chr1  <unknown description>
      Query: /var/folders/s3/vs6nrrg52sdfjk3z90p7ndt94gg4tq/T/tmptzggbu4h <un...
        Hit: chr1 <unknown description>
Query range: [0:151] (1)
  Hit range: [12699:12850] (1)
Quick stats: evalue ?; bitscore ?
  Fragments: 1 (? columns)
```

By integrating this functionality into a Python script, we have successfully demonstrated how one can leverage the `PxBLAT` library to recreate the core functionalities of `BLAT`, all while enjoying the benefits and conveniences that come with using Python.

## 8. Best Practices: Resource Management for Large-Scale Alignments

When processing many sequences (hundreds or thousands), proper resource management is essential to prevent issues like file descriptor exhaustion or memory leaks. This section demonstrates best practices for handling large-scale BLAT alignments.

### Improved BLAT Function

Here's a robust implementation for aligning multiple sequences with proper resource management:

```{literalinclude} tutorial_data/improved_blat_example.py
:language: python
:linenos:
:lines: 1-75
:emphasize-lines: 51-56,58-64,67-73
```

**Key Features:**

1. **Server Context Manager**: Server is initialized and managed with a context manager for proper cleanup
2. **Wait for Readiness**: Explicitly waits for the server to be ready before proceeding
3. **Client Scoping**: Client is created **inside** the server context **after** `wait_ready()` to prevent race conditions
4. **Automatic 2bit Conversion**: Checks if the 2bit file exists and creates it if needed
5. **Progress Tracking**: Reports progress every 100 sequences

### Batch Processing

For very large datasets (10,000+ sequences), consider batch processing:

```{literalinclude} tutorial_data/improved_blat_example.py
:language: python
:linenos:
:lines: 78-141
:emphasize-lines: 113-118,120-126,128-139
```

**Batch Processing Benefits:**

- **Memory efficiency**: Process chunks at a time instead of loading everything
- **Progress monitoring**: Clear visibility into processing status
- **Flexibility**: Adjust batch size based on your system resources
- **Proper initialization order**: Client created after server is ready, same as the basic version

### Usage Example

To use these functions in your own code:

```python
from pathlib import Path

# Your sequences as (name, sequence) tuples
sequences = [
    ("gene1", "ATCGATCGATCG"),
    ("gene2", "GCTAGCTAGCTA"),
    # ... thousands more
]

ref_genome = Path("reference.fa")

# Use the improved blat function (defined in the example above)
results = blat(sequences, ref_genome)
print(f"Aligned {len(results)} sequences successfully!")
```

### Performance Tips

1. **Use appropriate batch sizes**: 100-500 sequences per batch is typically optimal
2. **Monitor system resources**: Use `ulimit -n` to check file descriptor limits
3. **Always create Client after server is ready**: Initialize the `Client` inside the server context after calling `server.wait_ready()` to avoid race conditions
4. **Consider server reuse**: Keep the server running for multiple batches
5. **Enable logging**: Set up logging to track long-running jobs

```{tip}
The complete improved BLAT example with all features shown above is available in the repository at `docs/tutorial_data/improved_blat_example.py`. You can download it directly from:
https://github.com/ylab-hi/pxblat/blob/main/docs/tutorial_data/improved_blat_example.py
```

## 9. Beyond APIs: Command-Line Tools

[![cli](images/cli.gif)](cli)

While `PxBLAT` is primarily designed as a library, it also offers command-line tools built on top of its APIs.
This provides users with additional options and flexibility, catering to a variety of use cases.
For more detailed information on these tools, refer to the [CLI documentation](cli).

## 10. Sharing Your Feedback and Reporting Issues

In our ongoing effort to enhance the clarity and accuracy of this tutorial, we invite you to share your insights and observations.
If you come across any statements that are unclear, or if you identify any inaccuracies, please feel empowered to [make direct edits to the tutorial](https://github.com/ylab-hi/pxblat/edit/main/docs/tutorial.md) or [initiate an issue](https://github.com/ylab-hi/pxblat/issues/new/choose) to bring it to our attention.
Your contributions are invaluable to us, and play a crucial role in ensuring that our documentation meets the highest standards of quality and precision.

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
