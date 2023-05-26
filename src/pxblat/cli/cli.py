import typer

from .client import client
from .fa2twobit import faToTwoBit
from .server import server_app

app = typer.Typer(
    epilog="YangyangLi 2023 please cite me",
    context_settings={"help_option_names": ["-h", "--help"]},
)

app.command()(faToTwoBit)
app.command()(client)


app.add_typer(server_app, name="server")

if __name__ == "__main__":
    app()
