"""Zensus Collector CLI."""

import inspect
from typing import Any

import click
import typer
from rich import box
from rich.console import Console, RenderableType
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typer import rich_utils
from typer.core import TyperCommand

from .commands.create import collect
from .commands.drop import drop
from .commands.list import list_datasets


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


def _print_panel_options(
    *,
    name: str,
    params: list[click.Option] | list[click.Argument],
    ctx: click.Context,
    markup_mode: rich_utils.MarkupMode,
    console: Console,
):
    """Custom implementation of `typer.rich_utils._print_panel_options`"""
    options_rows: list[list[RenderableType]] = []
    required_rows: list[str | Text] = []
    for param in params:
        # Short and long form
        opt_long_strs = []
        opt_short_strs = []
        secondary_opt_long_strs = []
        secondary_opt_short_strs = []
        for opt_str in param.opts:
            if "--" in opt_str:
                opt_long_strs.append(opt_str)
            else:
                opt_short_strs.append(opt_str)
        for opt_str in param.secondary_opts:
            if "--" in opt_str:
                secondary_opt_long_strs.append(opt_str)
            else:
                secondary_opt_short_strs.append(opt_str)

        # Column for a metavar, if we have one
        metavar = Text(style=rich_utils.STYLE_METAVAR, overflow="fold")
        # TODO: when deprecating Click < 8.2, make ctx required
        signature = inspect.signature(param.make_metavar)
        if "ctx" in signature.parameters:
            metavar_str = param.make_metavar(ctx=ctx)
        else:
            # Click < 8.2
            metavar_str = param.make_metavar()  # type: ignore[call-arg]

        # Do it ourselves if this is a positional argument
        if isinstance(param, click.Argument) and param.name and metavar_str == param.name.upper():
            metavar_str = param.type.name.upper()

        # Skip booleans and choices (handled above)
        if metavar_str != "BOOLEAN":
            metavar.append(metavar_str)

        # Range - from
        # https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706
        # skip count with default range type
        if (
            isinstance(param.type, click.types._NumberRangeBase)
            and isinstance(param, click.Option)
            and not (param.count and param.type.min == 0 and param.type.max is None)
        ):
            range_str = param.type._describe_range()
            if range_str:
                metavar.append(rich_utils.RANGE_STRING.format(range_str))

        # Required asterisk
        required: str | Text = ""
        if param.required:
            required = Text(rich_utils.REQUIRED_SHORT_STRING, style=rich_utils.STYLE_REQUIRED_SHORT)

        # Highlighter to make [ | ] and <> dim
        class MetavarHighlighter(RegexHighlighter):
            highlights = [
                r"^(?P<metavar_sep>(\[|<))",
                r"(?P<metavar_sep>\|)",
                r"(?P<metavar_sep>(\]|>)$)",
            ]

        metavar_highlighter = MetavarHighlighter()

        required_rows.append(required)
        options_rows.append(
            [
                rich_utils.highlighter(",".join(opt_long_strs)),
                rich_utils.highlighter(",".join(opt_short_strs)),
                rich_utils.negative_highlighter(",".join(secondary_opt_long_strs)),
                rich_utils.negative_highlighter(",".join(secondary_opt_short_strs)),
                metavar_highlighter(metavar),
                rich_utils._get_parameter_help(param=param, ctx=ctx, markup_mode=markup_mode),
            ]
        )
        options_rows.append([])
    rows_with_required: list[list[RenderableType]] = []
    if any(required_rows):
        for required, row in zip(required_rows, options_rows):
            rows_with_required.append([required, *row])
    else:
        rows_with_required = options_rows
    if options_rows:
        t_styles: dict[str, Any] = {
            "show_lines": rich_utils.STYLE_OPTIONS_TABLE_SHOW_LINES,
            "leading": rich_utils.STYLE_OPTIONS_TABLE_LEADING,
            "box": rich_utils.STYLE_OPTIONS_TABLE_BOX,
            "border_style": rich_utils.STYLE_OPTIONS_TABLE_BORDER_STYLE,
            "row_styles": rich_utils.STYLE_OPTIONS_TABLE_ROW_STYLES,
            "pad_edge": rich_utils.STYLE_OPTIONS_TABLE_PAD_EDGE,
            "padding": rich_utils.STYLE_OPTIONS_TABLE_PADDING,
        }
        box_style = getattr(box, t_styles.pop("box"), None)

        options_table = Table(
            highlight=True, show_header=False, expand=True, box=box_style, **t_styles
        )
        for row in rows_with_required:
            options_table.add_row(*row)
        console.print(
            Panel(
                options_table,
                border_style=rich_utils.STYLE_OPTIONS_PANEL_BORDER,
                title=name,
                title_align=rich_utils.ALIGN_OPTIONS_PANEL,
            )
        )


class CustomCommand(TyperCommand):
    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter):
        """Custom override of help formatting"""
        return rich_utils.rich_format_help(
            obj=self,
            ctx=ctx,
            markup_mode=self.rich_markup_mode,
            print_options_panel_func=_print_panel_options,
        )


# Add commands directly to the main app
app.command(name="create", cls=CustomCommand)(collect)
app.command(name="list")(list_datasets)
app.command(name="drop")(drop)
