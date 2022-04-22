import pytest

from tidybear import selectors


COLUMN_NAMES = ["name", "age", "height", "weight", "eye_color", "hair_color"]


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("name", ["name"]),
        ("_color", ["eye_color", "hair_color"]),
        ("a", ["name", "age", "hair_color"]),
    ],
)
def test_contains(pattern, expected):
    selector = selectors.contains(pattern)
    assert selector(COLUMN_NAMES) == expected


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("name", COLUMN_NAMES[1:]),
        ("_color", COLUMN_NAMES[:-2]),
        ("a", ["height", "weight", "eye_color"]),
    ],
)
def test_contains_negate(pattern, expected):
    selector = -selectors.contains(pattern)
    assert selector(COLUMN_NAMES) == expected
