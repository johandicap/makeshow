"""

Makeshow parsing utils - Unit tests

"""


from pathlib import Path

from utils.parsing_utils import load_lines_from_makefile_and_its_included_files


########################################################################################################################


def test_load_lines_from_makefile_and_its_included_files() -> None:
    # Given
    folder_path = Path(__file__).parent / "data" / "including"
    makefile_names = ["Makefile", "Makefile2"]
    # When
    for makefile_name in makefile_names:
        makefile_path = folder_path / makefile_name
        assert makefile_path.is_file(), f"Test data Makefile not found: '{makefile_path.absolute()}'"
        lines = load_lines_from_makefile_and_its_included_files(makefile_path)
        # Then
        assert "# Extra Makefile targets: b and c" in lines
        assert "b: a" in lines
        assert "c: b" in lines
        assert "# Extra Makefile targets: d and e" in lines
        assert "d: c" in lines
        assert "e: d" in lines


########################################################################################################################
