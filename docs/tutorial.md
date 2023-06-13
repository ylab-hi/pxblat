# **Tutorial**

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
