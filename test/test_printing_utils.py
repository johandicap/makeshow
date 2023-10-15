"""

Makeshow printing utils - Unit tests

"""


from pytest import CaptureFixture
from shared_test_utils import capture_and_reemit_stdout_and_stderr

from utils.printing_utils import print_list


########################################################################################################################


def test_print_list(capsys: CaptureFixture[str]) -> None:
    # Given
    my_list = ["a", "b", "c"]
    # When
    print_list(my_list)
    stdout, stderr = capture_and_reemit_stdout_and_stderr(capsys)
    # Then
    # Verify that nothing is printed to stderr
    assert stderr == ""
    # Verify that the list was printed to stdout
    output_lines = stdout.split("\n")
    assert output_lines == ["- a", "- b", "- c", ""]


########################################################################################################################
