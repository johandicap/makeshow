#!/usr/bin/env python3
"""

Makeshow integration test

"""

import sys
from pathlib import Path

from _pytest.capture import CaptureResult
from pytest import CaptureFixture

from makeshow import run_makeshow
from utils import MakeshowParameters


########################################################################################################################


def capture_and_reemit_stdout_and_stderr(capsys: CaptureFixture[str]) -> CaptureResult:
    """
    Capture (and re-emit) stdout and stderr using pytest's capsys fixture, see
        https://docs.pytest.org/en/7.1.x/reference/reference.html#std-fixture-capsys
    This is done so that the captured output is still shown by pytest if the test fails.
    Adapted from recapsys in https://stackoverflow.com/a/67928390
    :param capsys: Pytest fixture to capture stdout and stderr.
    :return: Capture result containing stdout and stderr.
    """
    capture_result: CaptureResult = capsys.readouterr()
    sys.stdout.write(capture_result.out)
    sys.stderr.write(capture_result.err)
    return capture_result


########################################################################################################################


def test_makeshow_circular(capsys: CaptureFixture[str]) -> None:
    """
    Integration test to make sure makeshow doesn't crash on circular (cyclic) dependencies.
    :param capsys: Pytest fixture to capture stdout and stderr.
    """
    #
    # Given
    #
    makefile_path = Path("test/data/circular/Makefile").resolve()

    #
    # When
    #
    # Make sure that the test data is found
    if not makefile_path.is_file():
        raise FileNotFoundError(f'Test data Makefile not found: "{makefile_path}"')

    # Prepare parameters to run makeshow on the test data file
    params = MakeshowParameters(makefile_path=makefile_path, desired_targets=["a"], show_dependencies=True)

    # Run makeshow and capture its output
    run_makeshow(params)
    capture_result = capture_and_reemit_stdout_and_stderr(capsys)

    #
    # Then
    #
    # Verify that the dropped circular dependency was printed to stderr
    assert "Circular dependency dropped:" in capture_result.err
    # Verify that both targets and their definitions were printed to stdout
    output_lines = capture_result.out.split("\n")
    assert "a: b" in output_lines
    assert '\techo "a"' in output_lines
    assert "b: a" in output_lines
    assert '\techo "b"' in output_lines


########################################################################################################################
