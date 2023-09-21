#!/usr/bin/env python3
"""

makeshow.py - Show definitions of Makefile targets

Usage:
    ./makeshow.py
        Will show usage instructions and print a list of targets found in the Makefile.
    ./makeshow.py target1
        Will print the definition of Makefile target "target1".
    ./makeshow.py target1 target2 ... targetN
        Will print the definitions of Makefile targets 1 to N.

"""

import argparse
import dataclasses
import sys
from pathlib import Path
from typing import List, Optional


########################################################################################################################


@dataclasses.dataclass
class MakeshowParameters:
    makefile_path: Path
    desired_targets: List[str]


########################################################################################################################


def main(arg_list: List[str]) -> None:
    params = parse_args(arg_list)
    run_makeshow(params)


########################################################################################################################


def run_makeshow(params: MakeshowParameters) -> None:
    # Extract parameters
    makefile_path = params.makefile_path
    desired_targets = params.desired_targets

    # Go
    if not makefile_path.is_file():
        print_banner()
        print_makefile_not_found_error(makefile_path)
        exit(17)

    text = makefile_path.read_text()
    lines = text.splitlines(keepends=False)
    targets = find_targets(lines)

    if len(desired_targets) == 0:
        # Print usage and a list of detected targets
        print_banner()
        print_usage(targets)
    else:
        sep = ""  # "---"
        # Print the contents of the desired targets
        print(sep)
        for desired_target in desired_targets:
            target_definition = find_target_definition(lines, targets, desired_target)
            print_target_definition(target_definition, desired_target)
            print(sep)


########################################################################################################################


def parse_args(arg_list: List[str]) -> MakeshowParameters:
    # Parse given argument list
    parser = argparse.ArgumentParser(
        prog="Makeshow",
        description="Show definitions of Makefile targets in the terminal.",
        epilog="",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--makefile_path", type=Path, default=Path("./Makefile"), help="Path to Makefile to show definitions from."
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
    )
    return params


########################################################################################################################


def print_banner() -> None:
    """
    ASCII banner created using https://manytools.org/hacker-tools/ascii-banner/
    """
    print(r"  __  __        _             _                 ")
    print(r" |  \/  | __ _ | |__ ___  ___| |_   ___ __ __ __")
    print(r" | |\/| |/ _` || / // -_)(_-<| ' \ / _ \\ V  V /")
    print(r" |_|  |_|\__,_||_\_\\___|/__/|_||_|\___/ \_/\_/ ")
    print("")


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


def print_list(my_list: List[str]) -> None:
    print("- ", end="")
    print("\n- ".join(my_list))


########################################################################################################################


def print_target_definition(target_definition: str, desired_target: str) -> None:
    if target_definition != "":
        print(target_definition)
    else:
        print(f"Target '{desired_target}' not found in Makefile.")


########################################################################################################################


def find_target_definition(lines: List[str], targets: List[str], desired_target: str) -> str:
    if desired_target not in targets:
        return ""

    definition = ""
    include = False

    for line in lines:
        if line.startswith(desired_target + ":"):
            include = True
            definition = line + "\n"
        elif include:
            if line.startswith(" ") or line.startswith("\t") or line == "":
                definition += line + "\n"
            else:
                break

    return definition.strip("\n")


########################################################################################################################


def find_targets(lines: List[str]) -> List[str]:
    targets_and_blanks = [identify_target_in_line(line) for line in lines]
    targets = [t for t in targets_and_blanks if t != ""]
    return targets


def identify_target_in_line(line: str) -> str:
    first = line.split(" ")[0]
    target = first[:-1] if first.endswith(":") and not first.startswith(".") else ""
    return target


########################################################################################################################


if __name__ == "__main__":
    main(sys.argv[1:])
