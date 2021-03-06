import pytest
from pandas import DataFrame
from pandas import isna
from pandas.testing import assert_frame_equal

from tidybear import pivot_longer
from tidybear import pivot_wider


@pytest.fixture
def df_wide():
    return DataFrame(
        {
            "idx": [1, 2, 3],
            "A": [1, 2, 3],
            "B": [4, 5, 6],
        }
    )


@pytest.fixture
def df_long():
    return DataFrame(
        {
            "idx": [1, 2, 3, 1, 2, 3],
            "name": ["A", "A", "A", "B", "B", "B"],
            "value": [1, 2, 3, 4, 5, 6],
        }
    )


# PIVOT_LONGER


def test_pivot_longer_basic(df_wide, df_long):
    pivot = pivot_longer(df_wide, ["A", "B"])
    pivot = pivot.sort_values(["name", "idx"]).reset_index(drop=True)
    assert_frame_equal(pivot, df_long)


def test_pivot_longer_cols_are_index(df_wide, df_long):
    pivot = pivot_longer(df_wide, "idx", cols_are_index=True)
    pivot = pivot.sort_values(["name", "idx"]).reset_index(drop=True)
    assert_frame_equal(pivot, df_long)


def test_pivot_longer_drop_na(df_wide, df_long):

    df_wide["A"] = [1, 2, None]
    pivot = pivot_longer(df_wide, "idx", cols_are_index=True)
    pivot = pivot.sort_values(["name", "idx"]).reset_index(drop=True)

    assert pivot.shape[0] == df_long.shape[0] - 1
    assert pivot.value.tolist() == [1.0, 2.0, 4.0, 5.0, 6.0]


def test_pivot_longer_dont_drop_na(df_wide, df_long):

    df_wide["A"] = [1, 2, None]
    pivot = pivot_longer(df_wide, ["A", "B"], drop_na=False)
    pivot = pivot.sort_values(["name", "idx"]).reset_index(drop=True)

    assert pivot.shape[0] == df_long.shape[0]
    assert pivot.value.tolist()[:2] == [1.0, 2.0]
    assert pivot.value.tolist()[-3:] == [4.0, 5.0, 6.0]
    assert isna(pivot.value.tolist()[2])


# # PIVOT_WIDER


def test_pivot_wider_basic(df_long, df_wide):
    pivot = pivot_wider(df_long)
    pivot = pivot.sort_values(["idx"]).reset_index(drop=True)
    assert_frame_equal(pivot, df_wide)


def test_pivot_wider_multiple_values(df_long, df_wide):
    df_long.drop("value", axis=1, inplace=True)
    df_long["v1"] = [1, 2, 3, 4, 5, 6]
    df_long["v2"] = [7, 8, 9, 10, 11, 12]

    pivot = pivot_wider(df_long, values_from=["v1", "v2"])
    pivot = pivot.sort_values(["idx"]).reset_index(drop=True)

    assert pivot.columns.tolist() == ["idx", "v1_A", "v1_B", "v2_A", "v2_B"]
    assert pivot.v1_A.tolist() == [1, 2, 3]
    assert pivot.v1_B.tolist() == [4, 5, 6]
    assert pivot.v2_A.tolist() == [7, 8, 9]
    assert pivot.v2_B.tolist() == [10, 11, 12]


def test_pivot_wider_fill_na(df_long, df_wide):
    df_long.drop(index=[3], inplace=True)
    pivot = pivot_wider(df_long, fill_value=-1)
    pivot = pivot.sort_values(["idx"]).reset_index(drop=True)

    df_wide.iloc[0, 2] = -1
    df_wide["A"] = df_wide.A.astype(float)
    df_wide["B"] = df_wide.B.astype(float)

    assert_frame_equal(pivot, df_wide)
