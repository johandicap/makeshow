"""

Makeshow printing utils

"""

import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional


########################################################################################################################


def banner_string() -> str:
    """
    ASCII banner created using https://manytools.org/hacker-tools/ascii-banner/
    :return: ASCII banner as a string, starting and ending with a newline.
    """
    banner_lines = [
        r"",
        r"  __  __        _             _                 ",
        r" |  \/  | __ _ | |__ ___  ___| |_   ___ __ __ __",
        r" | |\/| |/ _` || / // -_)(_-<| ' \ / _ \\ V  V /",
        r" |_|  |_|\__,_||_\_\\___|/__/|_||_|\___/ \_/\_/ ",
        r"",
    ]
    return "\n".join(banner_lines)


def print_banner() -> None:
    print(banner_string())


def print_list(my_list: List[str], sep="*") -> None:
    print(f"{sep} ", end="")
    print(f"\n{sep} ".join(my_list))


def print_usage(makefile_path: Optional[Path], all_targets: Optional[List[str]] = None,
                coloring_func: Optional[Callable[[str], str]] = None) -> None:
    print("Usage: python makeshow.py <target_name> [<target_name> ...]")
    print("")
    print("This will print the definition of the provided Makefile targets.")
    print("")
    print("Highlighted options:")
    print("* Add -d to also print the definitions of the targets that the provided targets depend on.")
    print("* Use -m to print the entire Makefile (including includes) instead of specific targets.")
    if coloring_func is None:
        print("* Install 'pygments' to show Makefile contents and targets in color.")
    else:
        print("* Makefile targets will be shown in color now that 'pygments' in installed. Use -n to disable coloring.")
    print("")
    if makefile_path is not None:
        print("Makefile:")
        print(f"  {makefile_path.absolute()}")
        print("")
    if all_targets is not None:
        print("Targets found in Makefile:")
        print_list(all_targets)
        print("")


def print_makefile_not_found_error(makefile_path: Path) -> None:
    print(f'ERROR: Makefile not found:\n  "{makefile_path.resolve()}"\n', file=sys.stderr)
    print(
        "Please run in a folder that contains a Makefile"
        " or use `-m` / `--makefile_path` to specify the Makefile path.\n",
        file=sys.stderr,
    )


def print_entire_makefile(lines: List[str], coloring_func: Optional[Callable[[str], str]]) -> None:
    # Make sure there is exactly one newline before and after the actual makefile contents
    makefile_contents = "\n".join(lines).strip("\n")
    # Print makefile contents, possibly in color
    print("")
    if coloring_func is not None:
        print(coloring_func(makefile_contents))
    else:
        print(makefile_contents)
    print("")


########################################################################################################################


def print_target_definition(
    target_definition: str, desired_target: str, coloring_func: Optional[Callable[[str], str]] = None
) -> None:
    if target_definition != "":
        if coloring_func is not None:
            print(coloring_func(target_definition))
            # print_target_definition_in_color(target_definition)
        else:
            print(target_definition)
    else:
        print(f"Target '{desired_target}' not found in Makefile.")


def print_target_definitions(
    all_target_definitions: Dict[str, str],
    targets_to_show: List[str],
    sep: str = "",
    coloring_func: Optional[Callable[[str], str]] = None,
) -> None:
    print(sep)
    for target in targets_to_show:
        target_definition = all_target_definitions.get(target, f"(No definition found for target '{target}')")
        print_target_definition(target_definition, target, coloring_func=coloring_func)
        print(sep)
    return


########################################################################################################################
