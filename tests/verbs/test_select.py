import pytest
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from tidybear import select


@pytest.fixture
def df() -> DataFrame:
    return DataFrame(
        {
            "idx": [1, 2, 3],
            "A": [1, 2, 3],
            "B": [4, 5, 6],
        }
    )


def test_select_single_col(df):
    assert_frame_equal(select(df, "A"), df.loc[:, ["A"]])


def test_select_multiple_col(df):
    assert_frame_equal(select(df, "A", "B"), df.loc[:, ["A", "B"]])


def test_select_kwarg_col(df):
    selected = select(df, a="A")

    check = df.loc[:, ["A"]]
    check.rename(columns={"A": "a"}, inplace=True)

    assert_frame_equal(selected, check)


def test_select_args_and_kwargs(df):
    selected = select(df, "A", b="B")

    check = df.loc[:, ["A", "B"]]
    check.rename(columns={"B": "b"}, inplace=True)
    assert_frame_equal(selected, check)
