import pandas as pd
import pytest
from numpy import nan as NA
from numpy.testing import assert_array_equal
from pandas import DataFrame
from pandas import isna
from pandas.testing import assert_frame_equal

import tidybear as tb


@pytest.fixture
def df() -> DataFrame:
    return DataFrame(
        {
            "idx": [1, 2, 3],
            "A": [1, 2, 3],
            "B": [4, 5, 6],
            "C": ["a", "b", "b"],
        }
    )


@pytest.fixture
def rename_df():
    return DataFrame({"A": [1, 2], "B": [3, 4]})


@pytest.fixture
def slice_df():
    return DataFrame({"A": [1, 2, 1, 2, 1, 2, 1, 2], "B": [1, 2, 3, 4, 5, 6, 7, 8]})


@pytest.fixture
def data():
    return DataFrame({"A": [1, 2]})


@pytest.fixture
def students():
    return pd.DataFrame(
        {
            "student_id": [1, 2, 3, 4, 5],
            "name": ["John", "Jane", "Jack", "Jill", "Jenny"],
            "grade": [10, 8, 12, 9, 7],
        }
    )


@pytest.fixture
def classes():
    return pd.DataFrame(
        {
            "class_id": [1, 2, 2, 3, 3],
            "student_id": [1, 2, 3, 6, 7],
        }
    )


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


def test_count(df):
    counts = tb.count(df, "C")
    assert counts.columns.tolist() == ["C", "n"]
    assert counts.C.tolist() == ["a", "b"]
    assert counts.n.tolist() == [1, 2]


def test_count_with_sort(df):
    counts = tb.count(df, "C", sort=True)
    assert counts.columns.tolist() == ["C", "n"]
    assert counts.C.tolist() == ["b", "a"]
    assert counts.n.tolist() == [2, 1]


def test_filter_with_no_args(students):
    df = tb.filter(students)
    assert df.equals(students)


def test_filter_with_single_str(students):
    df = tb.filter(students, "grade > 8")
    assert df.equals(students.loc[(students["grade"] > 8), :])


def test_filter_with_multiple_str(students):
    df = tb.filter(students, "grade > 8", "grade < 12")
    assert df.equals(students.loc[(students["grade"] > 8) & (students["grade"] < 12), :])


def test_filter_with_single_lambda(students):
    df = tb.filter(students, lambda x: x.grade > 8)
    assert df.equals(students.loc[(students["grade"] > 8), :])


def test_filter_with_multiple_lambda(students):
    df = tb.filter(students, lambda x: x.grade > 8, lambda x: x.grade < 12)
    assert df.equals(students.loc[(students["grade"] > 8) & (students["grade"] < 12), :])


def test_filter_with_both_str_and_lambda(students):
    df = tb.filter(students, "grade > 8", lambda x: x.grade < 12)
    assert df.equals(students.loc[(students["grade"] > 8) & (students["grade"] < 12), :])


def test_inner_join(students, classes):
    result = tb.inner_join(students, classes, "student_id")
    assert result.equals(
        pd.DataFrame(
            {
                "student_id": [1, 2, 3],
                "name": ["John", "Jane", "Jack"],
                "grade": [10, 8, 12],
                "class_id": [1, 2, 2],
            }
        )
    )


def test_left_join(students, classes):
    result = tb.left_join(students, classes, "student_id")
    assert result.equals(
        pd.DataFrame(
            {
                "student_id": [1, 2, 3, 4, 5],
                "name": ["John", "Jane", "Jack", "Jill", "Jenny"],
                "grade": [10, 8, 12, 9, 7],
                "class_id": [1, 2, 2, NA, NA],
            }
        )
    )


def test_right_join(students, classes):
    result = tb.right_join(students, classes, "student_id")
    assert result.equals(
        pd.DataFrame(
            {
                "student_id": [1, 2, 3, 6, 7],
                "name": ["John", "Jane", "Jack", NA, NA],
                "grade": [10, 8, 12, NA, NA],
                "class_id": [1, 2, 2, 3, 3],
            }
        )
    )


def test_outer_join(students, classes):
    result = tb.outer_join(students, classes, "student_id")
    assert result.equals(
        pd.DataFrame(
            {
                "student_id": [1, 2, 3, 4, 5, 6, 7],
                "name": ["John", "Jane", "Jack", "Jill", "Jenny", NA, NA],
                "grade": [10, 8, 12, 9, 7, NA, NA],
                "class_id": [1, 2, 2, NA, NA, 3, 3],
            }
        )
    )


def test_crossing(students):
    result = tb.crossing(students, pd.DataFrame({"active": [1, 0]}))
    result = result[["student_id", "active"]]

    assert result.equals(
        pd.DataFrame(
            {
                "student_id": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
                "active": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            }
        )
    )


def test_semi_join(students, classes):
    result = tb.semi_join(students, classes, "student_id")
    assert result.equals(
        pd.DataFrame(
            {
                "student_id": [1, 2, 3],
                "name": ["John", "Jane", "Jack"],
                "grade": [10, 8, 12],
            }
        )
    )


def test_mutate_one_col(data):
    result = tb.mutate(data, aplus1=lambda x: x.A + 1)
    assert result.columns.tolist() == ["A", "aplus1"]
    assert result.aplus1.tolist() == [2, 3]


def test_mutate_mult_col(data):
    result = tb.mutate(data, aplus1=lambda x: x.A + 1, atimes4=lambda x: x.A * 4)
    assert result.columns.tolist() == ["A", "aplus1", "atimes4"]
    assert result.aplus1.tolist() == [2, 3]
    assert result.atimes4.tolist() == [4, 8]


def test_pivot_longer_basic(df_wide, df_long):
    pivot = tb.pivot_longer(df_wide, ["A", "B"])
    pivot = pivot.sort_values(["name", "idx"]).reset_index(drop=True)
    assert_frame_equal(pivot, df_long)


def test_pivot_longer_cols_are_index(df_wide, df_long):
    pivot = tb.pivot_longer(df_wide, "idx", cols_are_index=True)
    pivot = pivot.sort_values(["name", "idx"]).reset_index(drop=True)
    assert_frame_equal(pivot, df_long)


def test_pivot_longer_drop_na(df_wide, df_long):

    df_wide["A"] = [1, 2, None]
    pivot = tb.pivot_longer(df_wide, "idx", cols_are_index=True)
    pivot = pivot.sort_values(["name", "idx"]).reset_index(drop=True)

    assert pivot.shape[0] == df_long.shape[0] - 1
    assert pivot.value.tolist() == [1.0, 2.0, 4.0, 5.0, 6.0]


def test_pivot_longer_dont_drop_na(df_wide, df_long):

    df_wide["A"] = [1, 2, None]
    pivot = tb.pivot_longer(df_wide, ["A", "B"], drop_na=False)
    pivot = pivot.sort_values(["name", "idx"]).reset_index(drop=True)

    assert pivot.shape[0] == df_long.shape[0]
    assert pivot.value.tolist()[:2] == [1.0, 2.0]
    assert pivot.value.tolist()[-3:] == [4.0, 5.0, 6.0]
    assert isna(pivot.value.tolist()[2])


def test_pivot_wider_basic(df_long, df_wide):
    pivot = tb.pivot_wider(df_long)
    pivot = pivot.sort_values(["idx"]).reset_index(drop=True)
    assert_frame_equal(pivot, df_wide)


def test_pivot_wider_multiple_values(df_long, df_wide):
    df_long.drop("value", axis=1, inplace=True)
    df_long["v1"] = [1, 2, 3, 4, 5, 6]
    df_long["v2"] = [7, 8, 9, 10, 11, 12]

    pivot = tb.pivot_wider(df_long, values_from=["v1", "v2"])
    pivot = pivot.sort_values(["idx"]).reset_index(drop=True)

    assert pivot.columns.tolist() == ["idx", "v1_A", "v1_B", "v2_A", "v2_B"]
    assert pivot.v1_A.tolist() == [1, 2, 3]
    assert pivot.v1_B.tolist() == [4, 5, 6]
    assert pivot.v2_A.tolist() == [7, 8, 9]
    assert pivot.v2_B.tolist() == [10, 11, 12]


def test_pivot_wider_fill_na(df_long, df_wide):
    df_long.drop(index=[3], inplace=True)
    pivot = tb.pivot_wider(df_long, fill_value=-1)
    pivot = pivot.sort_values(["idx"]).reset_index(drop=True)

    df_wide.iloc[0, 2] = -1
    df_wide["A"] = df_wide.A.astype(float)
    df_wide["B"] = df_wide.B.astype(float)

    assert_frame_equal(pivot, df_wide)


def test_rename_no_args(df):
    assert_frame_equal(df, tb.rename(df))


def test_rename_with_list(df):
    renamed = tb.rename(df, ["W", "X", "Y", "Z"])
    assert renamed.columns.tolist() == ["W", "X", "Y", "Z"]
    assert_array_equal(df.values, renamed.values)


def test_rename_with_args(df):
    renamed = tb.rename(df, "W", "X", "Y", "Z")
    assert renamed.columns.tolist() == ["W", "X", "Y", "Z"]
    assert_array_equal(df.values, renamed.values)


def test_rename_all_with_dict(df):
    renamed = tb.rename(df, {"idx": "W", "A": "X", "B": "Y", "C": "Z"})
    assert renamed.columns.tolist() == ["W", "X", "Y", "Z"]
    assert_array_equal(df.values, renamed.values)


def test_rename_some_with_dict(df):
    renamed = tb.rename(df, {"B": "Y"})
    assert renamed.columns.tolist() == ["idx", "A", "Y", "C"]
    assert_array_equal(df.values, renamed.values)


def test_rename_no_cols_dict(df):
    renamed = tb.rename(df, {"D": "ZZ"})
    assert_frame_equal(df, renamed)


def test_rename_all_with_kwargs(df):
    renamed = tb.rename(df, W="idx", X="A", Y="B", Z="C")
    assert renamed.columns.tolist() == ["W", "X", "Y", "Z"]
    assert_array_equal(df.values, renamed.values)


def test_rename_some_with_kwargs(df):
    renamed = tb.rename(df, Y="B")
    assert renamed.columns.tolist() == ["idx", "A", "Y", "C"]
    assert_array_equal(df.values, renamed.values)


def test_rename_no_cols_kwargs(df):
    renamed = tb.rename(df, Z="D")
    assert_frame_equal(df, renamed)


def test_rename_fails_with_list(df):
    # too few
    with pytest.raises(AssertionError):
        tb.rename(df, ["W", "X", "Y"])

    # too many
    with pytest.raises(AssertionError):
        tb.rename(df, ["W", "X", "Y", "Z", "ZZ"])


def test_rename_fails_with_args(df):
    # too few
    with pytest.raises(AssertionError):
        tb.rename(df, "W", "X", "Y")

    # too many
    with pytest.raises(AssertionError):
        tb.rename(df, "W", "X", "Y", "Z", "ZZ")


def test_select_single_col(df):
    assert_frame_equal(tb.select(df, "A"), df.loc[:, ["A"]])


def test_select_multiple_col(df):
    assert_frame_equal(tb.select(df, "A", "B"), df.loc[:, ["A", "B"]])


def test_select_kwarg_col(df):
    selected = tb.select(df, a="A")

    check = df.loc[:, ["A"]]
    check.rename(columns={"A": "a"}, inplace=True)

    assert_frame_equal(selected, check)


def test_select_args_and_kwargs(df):
    selected = tb.select(df, "A", b="B")

    check = df.loc[:, ["A", "B"]]
    check.rename(columns={"B": "b"}, inplace=True)
    assert_frame_equal(selected, check)


def test_slice_max_no_group(slice_df):
    for n in range(1, 9):
        top_rows = tb.slice_max(slice_df, order_by="B", n=n)
        assert top_rows.B.tolist() == list(range(8, 8 - n, -1))


def test_slice_max_yes_group(slice_df):
    for n in range(1, 5):
        top_rows = tb.slice_max(slice_df, order_by="B", n=n, groupby="A")
        assert top_rows[top_rows.A == 1].B.tolist() == list(range(7, 8 - (2 * n), -2))
        assert top_rows[top_rows.A == 2].B.tolist() == list(range(8, 8 - (2 * n), -2))


def test_slice_min_no_group(slice_df):
    for n in range(1, 9):
        bottom_rows = tb.slice_min(slice_df, order_by="B", n=n)
        assert bottom_rows.B.tolist() == list(range(1, n + 1))


def test_slice_min_yes_group(slice_df):
    for n in range(1, 5):
        bottom_rows = tb.slice_min(slice_df, order_by="B", n=n, groupby="A")
        assert bottom_rows[bottom_rows.A == 1].B.tolist() == list(range(1, 2 * n, 2))
        assert bottom_rows[bottom_rows.A == 2].B.tolist() == list(range(2, 2 * n + 1, 2))
