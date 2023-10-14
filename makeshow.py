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

TODO(jmb): Update these examples and the README examples with --show_dependencies.

"""

import argparse
import dataclasses
import sys
from pathlib import Path
from typing import Dict, List, Optional


########################################################################################################################


@dataclasses.dataclass
class MakeshowParameters:
    makefile_path: Path
    desired_targets: List[str]
    show_dependencies: bool


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

    lines = makefile_path.read_text().splitlines(keepends=False)
    all_targets = find_targets(lines)
    all_target_definitions = find_target_list_definitions(lines, all_targets)
    # TODO(jmb): Test these functions on some test data (e.g. Makefile or two)
    # TODO(jmb): Optimize the extraction of target list and target definitions later to reduce looping through 'lines'.

    if len(desired_targets) == 0:
        # Print usage and a list of detected targets
        print_banner()
        print_usage(all_targets)
        return

    if params.show_dependencies:
        all_target_dependencies = find_target_list_dependencies(lines, all_targets)
        dependency_chain = compute_dependency_chain_for_list_of_desired_targets(
            desired_targets, all_target_dependencies
        )
        targets_to_show = dependency_chain
    else:
        targets_to_show = desired_targets

    # Print the contents of the desired targets
    sep = ""  # "---"
    print(sep)
    for target in targets_to_show:
        target_definition = all_target_definitions.get(target, f"(No definition found for target '{target}')")
        print_target_definition(target_definition, target)
        print(sep)


########################################################################################################################


def parse_args(arg_list: List[str]) -> MakeshowParameters:
    # Parse given argument list
    parser = argparse.ArgumentParser(
        prog="makeshow",
        description="Show definitions of Makefile targets in the terminal.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--makefile_path", type=Path, default=Path("./Makefile"), help="Path to Makefile to show definitions from."
    )
    parser.add_argument(
        "-d",
        "--show_dependencies",
        action="store_true",
        help="Also show definitions of the targets that the given target(s) depend on.",
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
    )
    return params


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


def compute_dependency_chain_for_list_of_desired_targets(
    desired_targets: List[str], all_target_dependencies: Dict[str, List[str]]
) -> List[str]:
    # Add dummy target that depends on all the desired targets
    dummy_target = "____DUMMY____"
    assert (
        dummy_target not in all_target_dependencies.keys()
    ), f"ERROR: Dummy target '{dummy_target}' found in Makefile."
    extended_target_dependencies = all_target_dependencies.copy()  # NB: Shallow copy, so the lists are reused.
    extended_target_dependencies[dummy_target] = desired_targets
    dependency_chain_with_dummy = compute_dependency_chain(dummy_target, extended_target_dependencies)
    assert dependency_chain_with_dummy[-1] == dummy_target
    dependency_chain = dependency_chain_with_dummy[:-1]
    assert dummy_target not in dependency_chain
    return dependency_chain


########################################################################################################################


def compute_dependency_chain(x: str, dependencies: Dict[str, List[str]], seen: Optional[List[str]] = None) -> List[str]:
    chain = []
    if seen is None:
        seen = []
    seen.append(x)
    for dep in dependencies.get(x, []):
        if dep in seen:
            sys.stderr.write(f"makeshow: Circular dependency dropped: {x} <- {dep} (meaning '{x}' requires '{dep}')\n")
            continue
        dep_chain = compute_dependency_chain(dep, dependencies, seen)
        for y in dep_chain:
            if y not in chain:
                chain.append(y)
    if x not in chain:
        chain.append(x)
    return chain


########################################################################################################################


def find_target_list_dependencies(lines: List[str], targets: List[str]) -> Dict[str, List[str]]:
    # TODO(jmb): Add tests of this function. And maybe optimize it to reduce looping through 'lines'.
    target_dependencies: Dict[str, List[str]] = dict()
    for target in targets:
        target_dependencies[target] = find_single_target_dependencies(lines, target)
    return target_dependencies


def find_single_target_dependencies(lines: List[str], target: str) -> List[str]:
    dependency_list: List[str] = []
    for line in lines:
        if line.startswith(target + ":"):
            tail = line[len(target + ":") :]
            dependency_list = [t for t in tail.split(" ") if t != ""]
    return dependency_list


########################################################################################################################


def find_target_list_definitions(lines: List[str], targets: List[str]) -> Dict[str, str]:
    target_definitions: Dict[str, str] = dict()
    for target in targets:
        target_definitions[target] = find_single_target_definition(lines, target)
    return target_definitions


def find_single_target_definition(lines: List[str], target: str) -> str:
    definition = ""
    include = False

    for line in lines:
        if line.startswith(target + ":"):
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
