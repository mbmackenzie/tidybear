import pytest
from pandas import DataFrame

from tidybear import count


@pytest.fixture
def df() -> DataFrame:
    return DataFrame(
        {
            "idx": [1, 2, 3, 4],
            "A": [1, 2, 2, 3],
        }
    )


def test_count(df):
    counts = count(df, "A")
    assert counts.columns.tolist() == ["A", "n"]
    assert counts.A.tolist() == [1, 2, 3]
    assert counts.n.tolist() == [1, 2, 1]


def test_count_with_sort(df):
    counts = count(df, "A", sort=True)
    assert counts.columns.tolist() == ["A", "n"]
    assert counts.A.tolist() == [2, 1, 3]
    assert counts.n.tolist() == [2, 1, 1]
