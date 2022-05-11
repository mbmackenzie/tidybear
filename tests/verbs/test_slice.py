import pytest
from pandas import DataFrame

from tidybear import slice_max
from tidybear import slice_min


@pytest.fixture
def df():
    return DataFrame({"A": [1, 2, 1, 2, 1, 2, 1, 2], "B": [1, 2, 3, 4, 5, 6, 7, 8]})


def test_slice_max_no_group(df):
    for n in range(1, 9):
        top_rows = slice_max(df, order_by="B", n=n)
        assert top_rows.B.tolist() == list(range(8, 8 - n, -1))


def test_slice_max_yes_group(df):
    for n in range(1, 5):
        top_rows = slice_max(df, order_by="B", n=n, groupby="A")
        assert top_rows[top_rows.A == 1].B.tolist() == list(range(7, 8 - (2 * n), -2))
        assert top_rows[top_rows.A == 2].B.tolist() == list(range(8, 8 - (2 * n), -2))


def test_slice_min_no_group(df):
    for n in range(1, 9):
        bottom_rows = slice_min(df, order_by="B", n=n)
        assert bottom_rows.B.tolist() == list(range(1, n + 1))


def test_slice_min_yes_group(df):
    for n in range(1, 5):
        bottom_rows = slice_min(df, order_by="B", n=n, groupby="A")
        assert bottom_rows[bottom_rows.A == 1].B.tolist() == list(range(1, 2 * n, 2))
        assert bottom_rows[bottom_rows.A == 2].B.tolist() == list(range(2, 2 * n + 1, 2))
