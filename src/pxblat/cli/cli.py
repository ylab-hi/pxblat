"""Command line interface for pxblat."""
import sys
from datetime import datetime

import typer

from pxblat import __version__

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


@app.callback()
def common():  # noqa: D103
    pass


common.__doc__ = f"""{typer.style("Version", fg=typer.colors.YELLOW, bold=True)}: {typer.style(f"{__version__}", fg=typer.colors.GREEN, bold=True)}"""


if "sphinx" in sys.modules and __name__ != "__main__":
    # Create the typer click object to generate docs with sphinx-click
    typer_click_object = typer.main.get_command(app)


if __name__ == "__main__":
    app()
