"""

makeshow dependency utils

"""

import sys
from typing import Dict, List, Optional


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
