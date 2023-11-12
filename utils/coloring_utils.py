"""

Makeshow coloring utils

"""

import sys
from typing import Callable, Optional


########################################################################################################################


def get_optional_coloring_function(color_scheme: str, disable_coloring: bool) -> Optional[Callable[[str], str]]:
    """
    If the pygments library is installed, return a function that colors a given input text according to Makefile syntax.
    If not, None will be returned.
    :param color_scheme: The desired color scheme (i.e. pygments style, see https://pygments.org/styles).
    :param disable_coloring: Disable coloring by returning None, no matter if pygments is installed or not.
    :return: Coloring function or None.
    """
    # Return an empty optional if the pygments library isn't available for coloring
    try:
        import pygments.formatters
        import pygments.lexers
        import pygments.styles
    except ImportError:
        return None

    # Return an empty optional if coloring is disabled
    if disable_coloring:
        return None

    # Check if the provided color scheme (pygments style) is found
    style_name = color_scheme
    if style_name not in pygments.styles.get_all_styles():
        sys.stderr.write(f"WARNING: Style '{style_name}' not found. Coloring disabled.\n")
        return None

    # Create style, lexer and formatter
    style_obj = pygments.styles.get_style_by_name(style_name)
    lexer = pygments.lexers.MakefileLexer()
    formatter = pygments.formatters.Terminal256Formatter(style=style_obj)

    # Create coloring function
    def _coloring_func(text: str) -> str:
        return pygments.highlight(text, lexer=lexer, formatter=formatter).rstrip("\n")

    return _coloring_func


########################################################################################################################
