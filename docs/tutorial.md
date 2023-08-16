# **Tutorial**

`PxBLAT` binds the codebase of [BLAT(v.37x1)][BLAT(v.37x1)], and aims to provide efficient and
ergonomic APIs. Let's take the journey to show features `PxBLAT` provides.

## APIs Compared to `BLAT`

So far, `PxBLAT` provides four main APIs, including {class}`.Client`, {class}`.Server`, {func}`.two_bit_to_fa` and {func}`.fa_to_two_bit`,
as well as other useful functions ({doc}`reference`).
`PxBLAT` is able to finish the most significant features of `BLAT`.
Here is a table in which the features are compared.

| PxBLAT                 | BLAT                     |
| :--------------------- | :----------------------- |
| {class}`.Client`       | [gfClient][gfClient]     |
| {class}`.Server`       | [gfServer][gfServer]     |
| {func}`.two_bit_to_fa` | [twoBitToFa][twoBitToFa] |
| {func}`.fa_to_two_bit` | [faToTwoBit][faToTwoBit] |

## Options Design

`PxBLAT` uses a extra class to hold and change parameters for {class}`.Server`
and {class}`.TwoBitToFaOption`.
The design is a trick to mimic named parameter, and is used in Cpp and Rust.
Python may not need to the design but it still benefit if the parameters are too
long.
For example, `PxBLAT` can create and change parameters of {class}`.Server` via {meth}`.Server.create_option`.
The chain methods of options is builder pattern which is used in Cpp and Rust.

```{tip}
Click the blinking circle cross, and you will be blessed and get more information.
```

```{eval-rst}
.. code-block:: python
    :linenos:

    from pxblat import Server

    server_option = Server.create_option().withStepSize(3).withTileSize(10).build()  # (1)!
    server = Server("localhost", port, two_bit, server_option)

.. code-annotations::
    #. we change step size and tile size
```

The options have same parameter as its command line version of `BLAT`.
{doc}`reference` includes all possible parameters the option will accept.

## From FASTA to 2bit

Before we query certain sequence to a reference, we need to generate [.2bit][.2bit] file from [fasta][fasta] format.
`PxBLAT` provides a free function {func}`.fa_to_two_bit`.
Also, `PxBLAT` support to convert the `.2bit` file back to fasta format via {func}`.two_bit_to_fa`, for example,

```{eval-rst}
.. code-block:: python
    :linenos:

    from pxblat import fa_to_two_bit

    fa_to_two_bit(
        ["fasta1.fa"],  # (1)!
        "out.2bit",  # (2)!
        noMask=False,
        stripVersion=False,
        ignoreDups=False,
        useLong=False,
    )

.. code-annotations::
    #. Same as `BLAT`, :func:`.fa_to_two_bit` can accept  multilple inputs
    #. Output file path
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
$ faToTwoBit fasta1.fa out.2bit
$ ls
out.2bit fasta1.fa
```

Moreover, `PxBLAT` provides flexible options to allow conducting the conversion in {doc}`cli`.

## Query Sequences

Most simple method to query sequence is to open {class}`pxblat.Server` in context mode

```{eval-rst}
.. code-block:: python
    :linenos:

    from pxblat import Server, Client

    client = Client(
        host="localhost",
        port=65000,  # (1)!
        seq_dir=two_bit,  # (2)!
        min_score=20,
        min_identity=90,
    )

    server_option = Server.create_option().withCanStop(True).withStepSize(5).build()  # (3)!
    with Server("localhost", port, two_bit, server_option) as server:
        work()  # (4)!
        server.wait_for_ready()  # (5)!
        result1 = client.query("ATCG")  # (6)!
        result2 = client.query("AtcG")  # (7)!
        result3 = client.query(["ATCG", "ATCG"])  # (8)!
        result4 = client.query(["fasta1.fa", "fasta2.fa"])  # (9)!
        result5 = client.query(["cgTA", "fasta.fa"])  # (10)!

.. code-annotations::
    #. The port number of current running :class:`.Server`
    #. The two bit files from reference, and we can get it via :func:`.fa_to_two_bit` or via  :doc:`cli`
    #. Create :class:`.ServerOption` with specific parameters for :class:`.Server`
    #. We can do some other stuffs that consuming time
    #. Block current thread to wait server to be ready
    #. :meth:`.Client.query` accepts a :class:`str` consisting of DNA or Protein Sequences, e.g. `"ATCG"`
    #. :meth:`.Client.query` accepts a path of Fasta file, e.g. `"data/fasta1.fa"`
    #. :meth:`.Client.query` accepts a :class:`list` of :class:`str` consisting of DNA or Protein Sequences, e.g. `["ATCG","CTGAG"]`
    #. :meth:`.Client.query` accepts a :class:`list` of path of Fasta files, e.g. `["data/fasta1.fa", "data/fasta2.fa"]`
    #. :meth:`.Client.query` accepts a :class:`list` of :class:`str` and path, e.g. `["ATCG", "data/fasta1.fa"]`
```

{meth}`.Client.query` accepts parameters of several types:

1. Path of Fasta file e.g. `data/fasta1.fa`
2. {class}`list` of {class}`str` consisting of DNA or Protein Sequences, e.g. `["ATCG","CTGAG"]`
3. {class}`list` of path of Fasta files, e.g. `["data/fasta1.fa", "data/fasta2.fa"]`
4. {class}`list` of `str` and path, e.g. `["ATCG", "data/fasta1.fa"]`
5. {meth}`.Client.query` accepts a {class}`list` of {class}`str` and path, e.g. `["ATCG", "data/fasta1.fa"]`

{meth}`.Client.query` return [Bio.SearchIO.QueryResult](#query-result).

We may need to query sequences in more general way, for example,

```{eval-rst}
.. code-block:: python
    :linenos:

    from pxblat import Server, Client

    client = Client(
        host="localhost",
        port=port,
        seq_dir=two_bit,
        min_score=20,
        min_identity=90,
        wait_ready=True,  # (1)!
    )

    server_option = Server.create_option().withCanStop(True).withStepSize(5).build()
    server = Server("localhost", port, two_bit, server_option)
    server.start()
    work()  # (2)!
    # server.wait_ready()
    # (3)!
    result1 = client.query(["actg", "fasta.fa"])
    other_work()
    result2 = client.query("fasta.fa")
    server.stop()  # (4)!

.. code-annotations::
    #. The parameter `wait_ready` is used to control if the client need to check and wait current server to be ready or query directly.
    #. May a task consuming long time
    #. No need to wait current running server  to be ready, and the job will be done by :class:`.Client`
    #. Stop the current running server
```

Although {class}`.Server` and {class}`.Client` already consider most contexts, `PxBLAT` provides {class}`.ClientThread` that can launch a thread to
query sequence.
However, {class}`.ClientThread` only query one sequence at one time.
Its APIs are still not stable so far.
Free feel to check that if you have interests.

## Query Result

`PxBLAT` aims to introduce as few concepts as possible so that users do not need to take time to learn.
The query result is the same as `QueryResult` of [Bio][Bio].
Hence, we can manipulate the query result as shown below.

```{eval-rst}
.. py:class:: QueryResult

    Class representing search results from a single query.

    QueryResult is the container object that stores all search hits from a
    single search query. It is the top-level object returned by SearchIO's two
    main functions, ``read`` and ``parse``. Depending on the search results and
    search output format, a QueryResult object will contain zero or more Hit
    objects (see Hit).

    You can take a quick look at a QueryResult's contents and attributes by
    invoking ``print`` on it::

        >>> from Bio import SearchIO
        >>> qresult = next(SearchIO.parse('Blast/mirna.xml', 'blast-xml'))
        >>> print(qresult)
        Program: blastn (2.2.27+)
          Query: 33211 (61)
                 mir_1
         Target: refseq_rna
           Hits: ----  -----  ----------------------------------------------------------
                    #  # HSP  ID + description
                 ----  -----  ----------------------------------------------------------
                    0      1  gi|262205317|ref|NR_030195.1|  Homo sapiens microRNA 52...
                    1      1  gi|301171311|ref|NR_035856.1|  Pan troglodytes microRNA...
                    2      1  gi|270133242|ref|NR_032573.1|  Macaca mulatta microRNA ...
                    3      2  gi|301171322|ref|NR_035857.1|  Pan troglodytes microRNA...
                    4      1  gi|301171267|ref|NR_035851.1|  Pan troglodytes microRNA...
                    5      2  gi|262205330|ref|NR_030198.1|  Homo sapiens microRNA 52...
                    6      1  gi|262205302|ref|NR_030191.1|  Homo sapiens microRNA 51...
                    7      1  gi|301171259|ref|NR_035850.1|  Pan troglodytes microRNA...
                    8      1  gi|262205451|ref|NR_030222.1|  Homo sapiens microRNA 51...
                    9      2  gi|301171447|ref|NR_035871.1|  Pan troglodytes microRNA...
                   10      1  gi|301171276|ref|NR_035852.1|  Pan troglodytes microRNA...
                   11      1  gi|262205290|ref|NR_030188.1|  Homo sapiens microRNA 51...
        ...

    If you just want to know how many hits a QueryResult has, you can invoke
    ``len`` on it. Alternatively, you can simply type its name in the interpreter::

        >>> len(qresult)
        100
        >>> qresult
        QueryResult(id='33211', 100 hits)

    QueryResult behaves like a hybrid of Python's built-in list and dictionary.
    You can retrieve its items (Hit objects) using the integer index of the
    item, just like regular Python lists::

        >>> first_hit = qresult[0]
        >>> first_hit
        Hit(id='gi|262205317|ref|NR_030195.1|', query_id='33211', 1 hsps)

    You can slice QueryResult objects as well. Slicing will return a new
    QueryResult object containing only the sliced hits::

        >>> sliced_qresult = qresult[:3]    # slice the first three hits
        >>> len(qresult)
        100
        >>> len(sliced_qresult)
        3
        >>> print(sliced_qresult)
        Program: blastn (2.2.27+)
          Query: 33211 (61)
                 mir_1
         Target: refseq_rna
           Hits: ----  -----  ----------------------------------------------------------
                    #  # HSP  ID + description
                 ----  -----  ----------------------------------------------------------
                    0      1  gi|262205317|ref|NR_030195.1|  Homo sapiens microRNA 52...
                    1      1  gi|301171311|ref|NR_035856.1|  Pan troglodytes microRNA...
                    2      1  gi|270133242|ref|NR_032573.1|  Macaca mulatta microRNA ...

    Like Python dictionaries, you can also retrieve hits using the hit's ID.
    This is useful for retrieving hits that you know should exist in a given
    search::

        >>> hit = qresult['gi|262205317|ref|NR_030195.1|']
        >>> hit
        Hit(id='gi|262205317|ref|NR_030195.1|', query_id='33211', 1 hsps)

    You can also replace a Hit in QueryResult with another Hit using either the
    integer index or hit key string. Note that the replacing object must be a
    Hit that has the same ``query_id`` property as the QueryResult object.

    If you're not sure whether a QueryResult contains a particular hit, you can
    use the hit ID to check for membership first::

        >>> 'gi|262205317|ref|NR_030195.1|' in qresult
        True
        >>> 'gi|262380031|ref|NR_023426.1|' in qresult
        False

    Or, if you just want to know the rank / position of a given hit, you can
    use the hit ID as an argument for the ``index`` method. Note that the values
    returned will be zero-based. So zero (0) means the hit is the first in the
    QueryResult, three (3) means the hit is the fourth item, and so on. If the
    hit does not exist in the QueryResult, a ``ValueError`` will be raised.

        >>> qresult.index('gi|262205317|ref|NR_030195.1|')
        0
        >>> qresult.index('gi|262205330|ref|NR_030198.1|')
        5
        >>> qresult.index('gi|262380031|ref|NR_023426.1|')
        Traceback (most recent call last):
        ...
        ValueError: ...

    To ease working with a large number of hits, QueryResult has several
    ``filter`` and ``map`` methods, analogous to Python's built-in functions with
    the same names. There are ``filter`` and ``map`` methods available for
    operations over both Hit objects or HSP objects. As an example, here we are
    using the ``hit_map`` method to rename all hit IDs within a QueryResult::

        >>> def renamer(hit):
        ...     hit.id = hit.id.split('|')[3]
        ...     return hit
        >>> mapped_qresult = qresult.hit_map(renamer)
        >>> print(mapped_qresult)
        Program: blastn (2.2.27+)
          Query: 33211 (61)
                 mir_1
         Target: refseq_rna
           Hits: ----  -----  ----------------------------------------------------------
                    #  # HSP  ID + description
                 ----  -----  ----------------------------------------------------------
                    0      1  NR_030195.1  Homo sapiens microRNA 520b (MIR520B), micr...
                    1      1  NR_035856.1  Pan troglodytes microRNA mir-520b (MIR520B...
                    2      1  NR_032573.1  Macaca mulatta microRNA mir-519a (MIR519A)...
        ...

    The principle for other ``map`` and ``filter`` methods are similar: they accept
    a function, applies it, and returns a new QueryResult object.

    There are also other methods useful for working with list-like objects:
    ``append``, ``pop``, and ``sort``. More details and examples are available in
    their respective documentations.

    Finally, just like Python lists and dictionaries, QueryResult objects are
    iterable. Iteration over QueryResults will yield Hit objects::

        >>> for hit in qresult[:4]:     # iterate over the first four items
        ...     hit
        ...
        Hit(id='gi|262205317|ref|NR_030195.1|', query_id='33211', 1 hsps)
        Hit(id='gi|301171311|ref|NR_035856.1|', query_id='33211', 1 hsps)
        Hit(id='gi|270133242|ref|NR_032573.1|', query_id='33211', 1 hsps)
        Hit(id='gi|301171322|ref|NR_035857.1|', query_id='33211', 2 hsps)

    If you need access to all the hits in a QueryResult object, you can get
    them in a list using the ``hits`` property. Similarly, access to all hit IDs is
    available through the ``hit_keys`` property.

        >>> qresult.hits
        [Hit(id='gi|262205317|ref|NR_030195.1|', query_id='33211', 1 hsps), ...]
        >>> qresult.hit_keys
        ['gi|262205317|ref|NR_030195.1|', 'gi|301171311|ref|NR_035856.1|', ...]

```

## Beyond APIs

Even though `PxBLAT` is designed as library, it provides command-line tools
using its APIs.
That could provide more choices for user according to different situations.
{doc}`reference` contain more details, and do not hesitate to check.

## Caveats

{class}`.ServerOption` hold most important parameters that are passed to {class}`.Server`.

<!-- links -->

[gfclient]: https://genome.ucsc.edu/goldenpath/help/blatSpec.html#gfClientUsage
[gfserver]: https://genome.ucsc.edu/goldenpath/help/blatSpec.html#gfServerUsage
[twobittofa]: https://genome.ucsc.edu/goldenpath/help/blatSpec.html#twoBitToFaUsage
[fatotwobit]: https://genome.ucsc.edu/goldenpath/help/blatSpec.html#faToTwoBitUsage
[.2bit]: https://genome.ucsc.edu/FAQ/FAQformat.html#format7
[fasta]: https://en.wikipedia.org/wiki/FASTA_format#:~:text=In%20bioinformatics%20and%20biochemistry%2C%20the,represented%20using%20single%2Dletter%20codes.&text=The%20format%20allows%20for%20sequence%20names%20and%20comments%20to%20precede%20the%20sequences
[blat(v.37x1)]: https://github.com/ucscGenomeBrowser/kent
[bio]: https://biopython.org/docs/latest/api/Bio.SearchIO.html?highlight=queryresult
