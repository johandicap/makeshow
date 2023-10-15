"""

Shared test utils

"""

import sys
from typing import Tuple

from _pytest.capture import CaptureResult
from pytest import CaptureFixture


########################################################################################################################


def capture_and_reemit_stdout_and_stderr(capsys: CaptureFixture[str]) -> Tuple[str, str]:
    """
    Capture (and re-emit) stdout and stderr using pytest's capsys fixture, see
        https://docs.pytest.org/en/7.1.x/reference/reference.html#std-fixture-capsys
    This is done so that the captured output is still shown by pytest if the test fails.
    Adapted from recapsys in https://stackoverflow.com/a/67928390
    :param capsys: Pytest fixture to capture stdout and stderr.
    :return: Capture result containing stdout and stderr.
    """
    capture_result: CaptureResult = capsys.readouterr()
    stdout: str = capture_result.out
    stderr: str = capture_result.err
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    return stdout, stderr


########################################################################################################################
