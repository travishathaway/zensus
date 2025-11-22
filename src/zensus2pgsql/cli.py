"""Zensus Collector CLI."""

import typer

from .commands.create import collect
from .commands.drop import drop
from .commands.list import list_datasets
from .typer_overrides import TyperCommandOverride


def _version_callback(value: bool):
    if value:
        from . import __version__

        typer.echo(f"zensus2pgsql version: {__version__}")
        raise typer.Exit()


def _add_display_configuration(ctx: typer.Context):
    print(ctx)


app = typer.Typer(help="Zensus 2022 Gitterdaten PostgreSQL importer", no_args_is_help=True)


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit.",
        is_eager=True,
        callback=_version_callback,
    ),
):
    """Zensus 2022 Gitterdaten PostgreSQL importer."""
    ctx.params["custom_layout"] = True


# Add commands directly to the main app
app.command(name="create", cls=TyperCommandOverride)(collect)
app.command(name="list")(list_datasets)
app.command(name="drop")(drop)
