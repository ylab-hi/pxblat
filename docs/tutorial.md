# **Tutorial**

## Query Sequences

Use {py:class}`pxblat.Server` in context mode

```{code-block} python
from pxblat import Server
from pxblat import Client

server_option = Server.create_option()
client_option = Client.create_option()

with Server(server_option).start() as server:
    client = Client(client_option)
    ret = client.query("TACAT")
```

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

       .. graphviz::

           digraph { A -> B }
       .. image:: desert-flower.jpg
           :width: 75%
    #. Indentation for lists' items that span multiple lines can be tricky in
       reStructuredText.

       0. First item in a nested list that starts with ``0``.
       #. Checkout the `sphinxemoji <https://sphinxemojicodes.rtfd.io>`_ extension to
          put emojis here.
```
