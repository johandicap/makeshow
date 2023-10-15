"""

Makeshow integration test

"""

from pathlib import Path

from pytest import CaptureFixture
from shared_test_utils import capture_and_reemit_stdout_and_stderr

from makeshow import run_makeshow
from utils import MakeshowParameters


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
