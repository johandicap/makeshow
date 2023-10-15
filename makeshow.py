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
    ./makeshow.py --show_dependencies target1
        Will print the definition of Makefile target "target1" and its dependencies, e.g. targets 3, 5 and 17.

"""

import sys
from typing import List

import utils


########################################################################################################################


def main(arg_list: List[str]) -> int:
    params = utils.parse_args(arg_list)
    return run_makeshow(params)


########################################################################################################################


def run_makeshow(params: utils.MakeshowParameters) -> int:
    # Extract parameters
    makefile_path = params.makefile_path
    desired_targets = params.desired_targets

    # Show error message if given Makefile is not found
    if not makefile_path.is_file():
        utils.print_banner()
        utils.print_makefile_not_found_error(makefile_path)
        return 17

    # Load Makefile contents
    lines = utils.load_lines_from_makefile_and_its_included_files(makefile_path)

    # Extract targets and their definitions
    all_targets, all_target_definitions = utils.extract_targets_and_target_definitions(lines)

    # If no targets are given, print usage and a list of detected targets
    if len(desired_targets) == 0:
        utils.print_banner()
        utils.print_usage(all_targets)
        return 0

    # Determine list of targets to show
    if params.show_dependencies:
        all_target_dependencies = utils.find_target_list_dependencies(lines, all_targets)
        dependency_chain = utils.compute_dependency_chain_for_list_of_desired_targets(
            desired_targets, all_target_dependencies
        )
        targets_to_show = dependency_chain
    else:
        targets_to_show = desired_targets

    # Print the contents of the desired targets
    utils.print_target_definitions(all_target_definitions, targets_to_show)
    return 0


########################################################################################################################


if __name__ == "__main__":
    main(sys.argv[1:])
