#!/usr/bin/env python3
"""

Makeshow dependency resolver unit tests

"""

from utils import compute_dependency_chain


########################################################################################################################


def test_compute_dependency_chain_simple() -> None:
    # Given
    all_target_dependencies = {"a": ["b"], "b": ["c"], "c": ["d"]}
    desired_target = "a"
    expected_chain = ["d", "c", "b", "a"]
    # When
    dependency_chain = compute_dependency_chain(desired_target, all_target_dependencies)
    # Then
    assert dependency_chain == expected_chain
    print(17)


########################################################################################################################


def test_compute_dependency_chain_complex() -> None:
    # Given
    all_target_dependencies = {"a": ["b", "c", "e", "j"], "b": ["c"], "c": ["d"], "d": ["f", "g"], "h": ["i"]}
    desired_target = "a"
    expected_chain = ["f", "g", "d", "c", "b", "e", "j", "a"]
    # When
    dependency_chain = compute_dependency_chain(desired_target, all_target_dependencies)
    # Then
    assert dependency_chain == expected_chain


########################################################################################################################


def test_compute_dependency_chain_circular() -> None:
    # Given
    all_target_dependencies = {"a": ["b"], "b": ["a"]}
    desired_target = "a"
    expected_chain = ["b", "a"]
    # When
    dependency_chain = compute_dependency_chain(desired_target, all_target_dependencies)
    # Then
    assert dependency_chain == expected_chain


########################################################################################################################


def test_compute_dependency_chain_circular_again() -> None:
    # Given
    all_target_dependencies = {"a": ["b"], "b": ["c"], "c": ["a"], "d": ["e"]}
    desired_target = "a"
    expected_chain = ["c", "b", "a"]
    # When
    dependency_chain = compute_dependency_chain(desired_target, all_target_dependencies)
    # Then
    assert dependency_chain == expected_chain


########################################################################################################################
