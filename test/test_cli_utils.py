#!/usr/bin/env python3
"""

test_cli_utils.py

"""

from pathlib import Path
from utils import parse_args, MakeshowParameters


########################################################################################################################


def test_parse_args_minimal():
    # Given
    args_list = ["target1"]
    # When
    params: MakeshowParameters = parse_args(args_list)
    # Then
    assert params.makefile_path.resolve() == Path("./Makefile").resolve()
    assert params.desired_targets == ["target1"]
    assert not params.show_dependencies


########################################################################################################################


def test_parse_args_full():
    # Given
    args_list = ["--makefile_path", "./test/data/circular/Makefile", "--show_dependencies", "target1", "target2"]
    # When
    params: MakeshowParameters = parse_args(args_list)
    # Then
    assert params.makefile_path.resolve() == Path("./test/data/circular/Makefile").resolve()
    assert params.desired_targets == ["target1", "target2"]
    assert params.show_dependencies


########################################################################################################################

