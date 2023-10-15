"""

makeshow printing utils

"""

import sys
from pathlib import Path
from typing import Dict, List, Optional


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


def print_list(my_list: List[str]) -> None:
    print("- ", end="")
    print("\n- ".join(my_list))


def print_usage(all_targets: Optional[List[str]] = None) -> None:
    print("Usage: python makeshow.py <target_name> [<target_name> ...]")
    print("")
    if all_targets is not None:
        print("Targets found in Makefile:")
        print_list(all_targets)
        print("")


def print_makefile_not_found_error(makefile_path: Path) -> None:
    print(f'ERROR: Makefile not found:\n  "{makefile_path.resolve()}"\n', file=sys.stderr)
    print(
        "Please run in a folder that contains a Makefile or use `--makefile_path` to specify the Makefile path.\n",
        file=sys.stderr,
    )


########################################################################################################################


def print_target_definition(target_definition: str, desired_target: str) -> None:
    if target_definition != "":
        print(target_definition)
    else:
        print(f"Target '{desired_target}' not found in Makefile.")


def print_target_definitions(all_target_definitions: Dict[str, str], targets_to_show: List[str], sep: str = "") -> None:
    print(sep)
    for target in targets_to_show:
        target_definition = all_target_definitions.get(target, f"(No definition found for target '{target}')")
        print_target_definition(target_definition, target)
        print(sep)
    return


########################################################################################################################
