import pandas as pd
import pytest
from numpy import nan as NA

from tidybear import cross_join
from tidybear import inner_join
from tidybear import left_join
from tidybear import outer_join
from tidybear import right_join

# from tidybear.verbs.join import join


@pytest.fixture
def students() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "student_id": [1, 2, 3, 4, 5],
            "name": ["John", "Jane", "Jack", "Jill", "Jenny"],
            "grade": [10, 8, 12, 9, 7],
        }
    )


@pytest.fixture
def classes() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "class_id": [1, 2, 2, 3, 3],
            "student_id": [1, 2, 3, 6, 7],
        }
    )


def test_inner_join(students: pd.DataFrame, classes: pd.DataFrame) -> None:
    result = inner_join(students, classes, "student_id")
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


def test_left_join(students: pd.DataFrame, classes: pd.DataFrame) -> None:
    result = left_join(students, classes, "student_id")
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


def test_right_join(students: pd.DataFrame, classes: pd.DataFrame) -> None:
    result = right_join(students, classes, "student_id")
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


def test_outer_join(students: pd.DataFrame, classes: pd.DataFrame) -> None:
    result = outer_join(students, classes, "student_id")
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


def test_cross_join(students: pd.DataFrame) -> None:
    result = cross_join(students, pd.DataFrame({"active": [1, 0]}))
    result = result[["student_id", "active"]]

    assert result.equals(
        pd.DataFrame(
            {
                "student_id": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
                "active": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            }
        )
    )
