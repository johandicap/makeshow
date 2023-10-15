"""

Makeshow parsing utils

"""


from pathlib import Path
from typing import Dict, List, Tuple


########################################################################################################################


def load_lines_from_makefile_and_its_included_files(makefile_path: Path) -> List[str]:
    lines = makefile_path.read_text().splitlines(keepends=False)
    # TODO(jmb): Support includes!
    return lines


########################################################################################################################


def extract_targets_and_target_definitions(lines: List[str]) -> Tuple[List[str], Dict[str, str]]:
    # TODO(jmb): Potentially parse properly, https://www.gnu.org/software/make/manual/html_node/Parsing-Makefiles.html
    all_targets = find_targets(lines)
    all_target_definitions = find_target_list_definitions(lines, all_targets)
    # TODO(jmb): Optimize the extraction of target list and target definitions later to reduce looping through 'lines'.
    # TODO(jmb): Test these functions on some test data (e.g. Makefile or two)
    # TODO(jmb): Maybe only return all_target_definitions and obtain all_targets as list(all_target_definitions.keys())
    return all_targets, all_target_definitions


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
