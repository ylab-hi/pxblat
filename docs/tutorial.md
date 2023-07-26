# **Tutorial**

## Query Sequences

Most simple method to query sequence is to open {py:class}`pxblat.Server` in context mode

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
    )

    server_option = Server.create_option().build()
    with Server("localhost", port, two_bit, server_option) as server:
        work()  # (1)
        server.wait_for_ready()  # (2)
        result1 = client.query("ATCG")  # (3)
        result2 = client.query("AtcG")  # (4)
        result3 = client.query(["ATCG", "ATCG"])  # (5)
        result4 = client.query(["cgTA", "fasta.fa"])  # (6)

.. code-annotations::
    1. We can do some other stuffs that consuming time
    2. Block current thread to wait server to be ready
    #. :meth:`.Client.query` accepts a :class:`str` consisting of DNA or Protein Sequences e.g. `"ATCG"`
    #. :meth:`.Client.query` accepts a path of Fasta file e.g. `data/fasta1.fa`
    #. :meth:`.Client.query` accepts a :class:`list` of :class:`str` consisting of DNA or Protein Sequences e.g. `["ATCG","CTGAG"]`
    #. :meth:`.Client.query` accepts a :class:`list` of path of Fasta files e.g. `["data/fasta1.fa", "data/fasta2.fa"]`
    #. :meth:`.Client.query` accepts a :class:`list` of :class:`str` and path e.g. `["ATCG", "data/fasta1.fa"]`
```

`Client.query` accepts parameters of multiple types

1. A `Path` of Fasta file e.g. `data/fasta1.fa`
2. A list of `str` consisting of DNA or Protein Sequences e.g. `["ATCG","CTGAG"]`
3. A list of `Path` of Fasta files e.g. `["data/fasta1.fa", "data/fasta2.fa"]`
4. A list of `str` and `Path` e.g. `["ATCG", "data/fasta1.fa"]`

```{eval-rst}
.. code-block:: python

    html_theme_options = {
        "features": ["content.code.annotate"],  # (1)
    }

.. code-annotations::
    1. .. admonition:: Obsolete
           :class: failure

           This has no special effect because the :rst:dir:`code-annotations` directive
           automatically enables the feature.
```

```{eval-rst}
.. code-block:: cpp

    // What can I put in an annotation? (1)
    /* What about nested lists and emojis? (2) */

.. code-annotations::
    3. These annotations can have anything that Sphinx supports (including extensions).

       .. image:: desert-flower.jpg
           :width: 75%
    #. Indentation for lists' items that span multiple lines can be tricky in
       reStructuredText.

       0. First item in a nested list that starts with ``0``.
       #. Checkout the `sphinxemoji <https://sphinxemojicodes.rtfd.io>`_ extension to
          put emojis here.
```
