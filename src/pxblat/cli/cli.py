import typer

from .fa2twobit import fa2TwoBit
from .client import client
from .server import server_app

app = typer.Typer(
    epilog="YangyangLi 2023 please cite me",
    context_settings={"help_option_names": ["-h", "--help"]},
)

app.command()(fa2TwoBit)
app.command()(client)


app.add_typer(server_app, name="server")
