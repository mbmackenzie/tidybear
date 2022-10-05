import pytest

from tidybear import selectors


COLUMN_NAMES = ["name", "age", "height", "weight", "eye_color", "hair_color"]


def _selector_helper(selector, expected, param=None):
    if param is not None:
        return selector(param)(COLUMN_NAMES) == expected

    return selector()(COLUMN_NAMES) == expected


def test_everything():
    assert _selector_helper(selectors.everything, COLUMN_NAMES)


def test_last_col():
    assert _selector_helper(selectors.last_col, ["hair_color"])


def test_first_col():
    assert _selector_helper(selectors.first_col, ["name"])


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("name", ["name"]),
        ("_color", ["eye_color", "hair_color"]),
        ("a", ["name", "age", "hair_color"]),
    ],
)
def test_contains(pattern, expected):
    assert _selector_helper(selectors.contains, expected, pattern)


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("(h|w)eight", ["height", "weight"]),
        (".*", COLUMN_NAMES),
    ],
)
def test_matches(pattern, expected):
    assert _selector_helper(selectors.matches, expected, pattern)


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("n", ["name"]),
        ("h", ["height", "hair_color"]),
    ],
)
def test_starts_with(pattern, expected):
    assert _selector_helper(selectors.starts_with, expected, pattern)


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("t", ["height", "weight"]),
        ("e", ["name", "age"]),
    ],
)
def test_ends_with(pattern, expected):
    assert _selector_helper(selectors.ends_with, expected, pattern)


@pytest.mark.parametrize(
    "prefix,values,width,expected",
    [
        ("col", range(1, 3), 0, ["col1", "col2"]),
        ("ft", range(1, 4), 0, []),
        ("ft", range(1, 4), 2, ["ft01", "ft02", "ft03"]),
    ],
)
def test_num_range(prefix, values, width, expected):
    columns = ["col1", "col2", "ft01", "ft02", "ft03"]
    selector = selectors.num_range(prefix, values, width=width)

    assert selector(columns) == expected


def test_tidyselector_negate():
    selector = -selectors.everything()
    assert selector(COLUMN_NAMES) == []


def test_tidyselector_filter_columns():
    assert selectors.everything().filter_columns(COLUMN_NAMES) == COLUMN_NAMES


@pytest.mark.parametrize(
    "these_columns,expected", [(["name"], ["name"]), (["name", "age"], ["name", "age"])]
)
def test_all_of(these_columns, expected):
    assert _selector_helper(selectors.all_of, expected, these_columns)


def test_all_of_fails():
    with pytest.raises(ValueError):
        selectors.all_of(["name", "age", "mass"])(COLUMN_NAMES)


@pytest.mark.parametrize(
    "these_columns,expected",
    [
        (["name"], ["name"]),
        (["name", "age"], ["name", "age"]),
        (["name", "age", "mass"], ["name", "age"]),
    ],
)
def test_any_of(these_columns, expected):
    assert _selector_helper(selectors.any_of, expected, these_columns)
