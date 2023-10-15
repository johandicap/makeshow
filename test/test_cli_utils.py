"""

Makeshow command-line interface utils - Unit tests

"""

from pathlib import Path
from typing import List

from utils.cli_utils import MakeshowParameters, parse_args


########################################################################################################################


def test_parse_args_empty() -> None:
    # Given
    args_list: List[str] = []
    # When
    params: MakeshowParameters = parse_args(args_list)
    # Then
    assert params.makefile_path.resolve() == Path("./Makefile").resolve()
    assert params.desired_targets == []
    assert not params.show_dependencies


########################################################################################################################


def test_parse_args_full() -> None:
    # Given
    args_list = ["--makefile_path", "./test/data/circular/Makefile", "--show_dependencies", "target1", "target2"]
    # When
    params: MakeshowParameters = parse_args(args_list)
    # Then
    assert params.makefile_path.resolve() == Path("./test/data/circular/Makefile").resolve()
    assert params.desired_targets == ["target1", "target2"]
    assert params.show_dependencies


########################################################################################################################
