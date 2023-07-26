"""Command line interface for pxblat."""
import sys
from datetime import datetime

import typer

from .client import client
from .fa2twobit import faToTwoBit
from .server import server_app
from .twobit2fa import twoBitToFa

app = typer.Typer(
    epilog=f"YangyangLi {datetime.now().year} yangyang.li@northwstern.edu",
    context_settings={"help_option_names": ["-h", "--help"]},
)

app.command()(faToTwoBit)
app.command()(client)
app.command()(twoBitToFa)


app.add_typer(server_app, name="server")


if "sphinx" in sys.modules and __name__ != "__main__":
    # Create the typer click object to generate docs with sphinx-click
    typer_click_object = typer.main.get_command(app)


if __name__ == "__main__":
    app()
