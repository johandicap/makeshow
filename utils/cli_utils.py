"""

Makeshow command-line interface utils

"""

import argparse
import dataclasses
from pathlib import Path
from typing import List


########################################################################################################################


@dataclasses.dataclass
class MakeshowParameters:
    makefile_path: Path
    desired_targets: List[str]
    show_dependencies: bool
    show_makefile_instead: bool
    disable_coloring: bool
    color_scheme: str


########################################################################################################################


def parse_args(arg_list: List[str]) -> MakeshowParameters:
    # Parse given argument list
    parser = argparse.ArgumentParser(
        prog="makeshow",
        description="Show definitions of Makefile targets in the terminal.",
        epilog="Copyright \N{COPYRIGHT SIGN} 2023 Johan M. V. Bruun",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-m",
        "--makefile_path",
        type=Path,
        default=Path("./Makefile"),
        help="Path to Makefile to show definitions from.",
    )
    parser.add_argument(
        "-d",
        "--show_dependencies",
        action="store_true",
        help="Also show definitions of the targets that the given target(s) depend on.",
    )
    parser.add_argument(
        "-s",
        "--show_makefile_instead",
        action="store_true",
        help="Show the Makefile (including its included files) instead of one or more target definitions.",
    )
    parser.add_argument(
        "-n",
        "--no_colors",
        action="store_true",
        help="Do not use colors when printing Makefile contents or target definitions.",
    )
    parser.add_argument(
        "-c",
        "--color_scheme",
        type=str,
        default="one-dark",
        help="Color scheme, e.g. 'one-dark', 'github-dark', or 'dracula', see https://pygments.org/styles."
        " Requires the 'pygments' package to be installed.",
    )
    parser.add_argument(
        "desired_targets",
        type=str,
        default=[],
        nargs=argparse.REMAINDER,
        help="One or more Makefile target names to show definitions of.",
    )
    args = parser.parse_args(arg_list)
    # Create parameters object
    params = MakeshowParameters(
        makefile_path=args.makefile_path,
        desired_targets=args.desired_targets,
        show_dependencies=args.show_dependencies,
        show_makefile_instead=args.show_makefile_instead,
        disable_coloring=args.no_colors,
        color_scheme=args.color_scheme,
    )
    return params


########################################################################################################################
