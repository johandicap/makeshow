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

import sys
from pathlib import Path
from typing import List


########################################################################################################################


def main(argv: List[str]) -> None:

    # Prepare
    file_path = Path("./Makefile")
    
    # Go
    desired_targets = argv[1:]

    assert file_path.is_file(), f"File not found: \"{file_path}\""

    text = file_path.read_text()
    lines = text.splitlines(keepends=False)
    targets = find_targets(lines)
    
    if len(desired_targets) == 0:
        print("")
        print("Usage: python makeshow.py <target_name>")
        print("")
        print("Targets found in Makefile:")
        print_list(targets)
        print("")
    else:
        print("---")
        for desired_target in desired_targets:
            target_definition = find_target_definition(lines, targets, desired_target)
            print_target_definition(target_definition, desired_target)
    return


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
    print("---")


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
            if line.startswith(" ") or line.startswith("\t"):
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
    main(sys.argv)
