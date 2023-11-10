"""

Makeshow parsing utils

"""


from pathlib import Path
from typing import Dict, List, Tuple


########################################################################################################################


def load_lines_from_makefile_and_its_included_files(makefile_path: Path) -> List[str]:
    # Load Makefile
    original_lines = read_lines_and_handle_backslashes(makefile_path, err_msg="Makefile not found:")

    # Handle include statements
    lines = []
    last_include_line = -1
    for i, line in enumerate(original_lines):
        if line.startswith("include "):
            # First add the lines since last include line
            lines.extend(original_lines[(last_include_line + 1) : i])
            # Then gather lines from each include argument and add them
            incl_args = line[len("include ") :].split(" ")
            for include_file_arg in incl_args:
                lines_to_add = load_lines_from_included_file(makefile_path, include_file_arg)
                lines.append("")  # Add an empty line before the included lines
                lines.extend(lines_to_add)
                lines.append("")  # Add an empty line after the included lines
            # Keep track of the last include line in order to add remaining original lines
            last_include_line = i
    # Add remaning original lines
    lines.extend(original_lines[(last_include_line + 1) :])

    # Append a potentially missing newline at the end
    if len(lines) > 0 and lines[-1] != "":
        lines.append("")

    # Eliminate all instances of three or more consequitive newlines (to avoid excessive spacing)
    text = "\n".join(lines)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    lines = text.splitlines(keepends=False)
    return lines


def load_lines_from_included_file(makefile_path: Path, include_file: str) -> List[str]:
    # Obtain path to the include file
    include_file_path = makefile_path.parent / include_file
    lines = read_lines_and_handle_backslashes(include_file_path, err_msg="Include file not found:")
    return lines


def read_lines_and_handle_backslashes(file_path: Path, err_msg: str = "File not found:") -> List[str]:
    # Verify that the given file exists
    if not file_path.is_file():
        raise FileNotFoundError(f"{err_msg} '{file_path}'")

    # Load all lines of the file
    text = file_path.read_text()

    # Handle backslashes
    text = text.replace("\\\n\t", "")
    text = text.replace("\\\n", " ")
    # NB: This is backslash handling is not complete, but it covers all the cases that I've encountered in practice.

    # Split into lines and return them
    lines = text.splitlines(keepends=False)
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
    tail = ""
    found = False
    for line in lines:
        if line.startswith(target + ":"):
            tail = line[len(target + ":") :]
            found = True
        elif line.startswith(target + " :"):
            tail = line[len(target + " :") :]
            found = True
        if found:
            dependency_list = [t for t in tail.split(" ") if t != ""]
            break
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
        elif line.startswith(target + " :"):
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
    parts = line.split(" ")
    first = parts[0]
    if first.startswith("."):
        target = ""
    elif first.endswith(":"):
        target = first[:-1]
    elif len(parts) >= 2 and parts[1] == ":":
        target = first
    else:
        target = ""
    return target


########################################################################################################################
