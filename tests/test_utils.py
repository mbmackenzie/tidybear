import pytest

from tidybear import utils
from tidybear.selectors import contains

COLUMN_NAMES = ["name", "age", "height", "weight", "eye_color", "hair_color"]


@pytest.mark.parametrize(
    "to_select,expected",
    [
        (["name"], ["name"]),
        (["name", "height"], ["name", "height"]),
        (["name", contains("color")], ["name", "eye_color", "hair_color"]),
    ],
)
def test_get_column_names(to_select, expected):
    assert utils.get_column_names(COLUMN_NAMES, to_select) == expected
