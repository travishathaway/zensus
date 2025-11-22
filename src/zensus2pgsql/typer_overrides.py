"""
Module containing overrides for typer

This is used to customize the help output
"""

import inspect

import click
from rich.console import Console, Group, RenderableType
from rich.constrain import Constrain
from rich.emoji import Emoji
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text
from typer import rich_utils
from typer.core import TyperArgument, TyperCommand, TyperOption, _get_default_string


def _make_rich_text(
    *, text: str, style: str = "", markup_mode: rich_utils.MarkupMode
) -> Markdown | Text:
    """Take a string, remove indentations, and return styled text.

    By default, the text is not parsed for any special formatting.
    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == rich_utils.MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    if markup_mode == rich_utils.MARKUP_MODE_RICH:
        return rich_utils.highlighter(Text.from_markup(text, style=style))
    return rich_utils.highlighter(Text(text, style=style))


def _print_panel_options(
    name: str,
    params: list[TyperOption] | list[TyperArgument],
    ctx: click.Context,
    markup_mode: rich_utils.MarkupMode,
    console: Console,
):
    """
    Custom implementation of `typer.rich_utils._print_panel_options`

    Displays options in a simple text-based format:
        -s, --long-option <TYPE>
            Description of the option
            [default: value]

    """
    if not params:
        return

    # Indentation constants
    OPTION_INDENT = 2  # Indent for option line (e.g., "  -v, --verbose")
    DESCRIPTION_INDENT = 6  # Indent for description and default

    renderables: list[RenderableType] = []

    for param in params:
        # Collect short and long options
        opt_long_strs = []
        opt_short_strs = []
        for opt_str in param.opts:
            if "--" in opt_str:
                opt_long_strs.append(opt_str)
            else:
                opt_short_strs.append(opt_str)

        # Get metavar (type indicator)
        signature = inspect.signature(param.make_metavar)
        if "ctx" in signature.parameters:
            metavar_str = param.make_metavar(ctx=ctx)
        else:
            metavar_str = param.make_metavar()  # type: ignore[call-arg]

        # For positional arguments, use the type name
        if isinstance(param, click.Argument) and param.name and metavar_str == param.name.upper():
            metavar_str = param.type.name.upper()

        # Skip BOOLEAN metavar
        if metavar_str == "BOOLEAN":
            metavar_str = ""

        # Add range info if applicable
        if (
            isinstance(param.type, click.types._NumberRangeBase)
            and isinstance(param, click.Option)
            and not (param.count and param.type.min == 0 and param.type.max is None)
        ):
            range_str = param.type._describe_range()
            if range_str:
                metavar_str += rich_utils.RANGE_STRING.format(range_str)

        # Build the first line: -s, --long-option <TYPE>
        first_line = Text()

        # Add short options
        if opt_short_strs:
            first_line.append(",".join(opt_short_strs), style=rich_utils.STYLE_OPTION)
            if opt_long_strs:
                first_line.append(", ")

        # Add long options
        if opt_long_strs:
            first_line.append(",".join(opt_long_strs), style=rich_utils.STYLE_OPTION)

        # Add metavar/type
        if metavar_str:
            first_line.append(" ")
            first_line.append(metavar_str, style=rich_utils.STYLE_METAVAR)

        # Add required indicator
        if param.required:
            first_line.append(" ")
            first_line.append(
                rich_utils.REQUIRED_SHORT_STRING, style=rich_utils.STYLE_REQUIRED_SHORT
            )

        # Add the option line with padding for consistent indent on wrap
        renderables.append(Padding(first_line, (0, 0, 0, OPTION_INDENT)))

        # Main help text
        help_value: str | None = getattr(param, "help", None)
        if help_value:
            paragraphs = help_value.split("\n\n")
            # Remove single linebreaks
            if markup_mode != rich_utils.MARKUP_MODE_MARKDOWN:
                paragraphs = [
                    x.replace("\n", " ").strip()
                    if not x.startswith("\b")
                    else "{}\n".format(x.strip("\b\n"))
                    for x in paragraphs
                ]
            help_text = _make_rich_text(
                text="\n".join(paragraphs).strip(),
                style=rich_utils.STYLE_OPTION_HELP,
                markup_mode=markup_mode,
            )
            renderables.append(Padding(help_text, (0, 0, 0, DESCRIPTION_INDENT)))

        # Add default value if present
        if (
            isinstance(param, (click.Option, click.Argument))
            and param.default is not None
            and param.show_default
        ):
            default_val = param.default
            # Handle callable defaults
            if callable(default_val):
                default_val = default_val()
            # Don't show empty defaults or False for flags
            if default_val not in (None, (), [], "", False):
                default_string = _get_default_string(
                    param,
                    ctx=ctx,
                    show_default_is_str=isinstance(default_val, str),
                    default_value=default_val,
                )
                default_text = Text(f"[default: {default_string}]", style="dim")
                renderables.append(Padding(default_text, (0, 0, 0, DESCRIPTION_INDENT)))

        # Add blank line between options
        renderables.append(Text(""))

    # Print the panel with all options using Group
    console.print(
        Panel(
            Constrain(Group(*renderables), width=80),
            border_style=rich_utils.STYLE_OPTIONS_PANEL_BORDER,
            title=name,
            title_align=rich_utils.ALIGN_OPTIONS_PANEL,
        )
    )


class TyperCommandOverride(TyperCommand):
    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter):
        """Custom override of help formatting"""
        return rich_utils.rich_format_help(
            obj=self,
            ctx=ctx,
            markup_mode=self.rich_markup_mode,
            print_options_panel_func=_print_panel_options,
        )
