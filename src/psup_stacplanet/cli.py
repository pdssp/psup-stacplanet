from pathlib import Path
from typing import Annotated

import typer

import psup_stacplanet.funcs as F

app = typer.Typer(help="Utils for PSUP STACPLANET")


@app.callback()
def callback():
    """
    PSUP STACPLANET
    """


@app.command()
def read_inventory(
    inventory_csv: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
):
    F.read_inventory(inventory_csv)


@app.command()
def create_catalog(
    inventory_csv: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    root_catalog: Annotated[
        Path,
        typer.Option(
            exists=False,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
):
    F.create_catalog(inventory_csv, root_catalog)
