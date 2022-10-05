import pandas as pd
import pytest

from tidybear import filter


@pytest.fixture
def students():
    return pd.DataFrame(
        {
            "student_id": [1, 2, 3, 4, 5],
            "name": ["John", "Jane", "Jack", "Jill", "Jenny"],
            "grade": [10, 8, 12, 9, 7],
        }
    )


def test_filter_with_no_args(students):
    df = filter(students)
    assert df.equals(students)


def test_filter_with_single_str(students):
    df = filter(students, "grade > 8")
    assert df.equals(students.loc[(students["grade"] > 8), :])


def test_filter_with_multiple_str(students):
    df = filter(students, "grade > 8", "grade < 12")
    assert df.equals(students.loc[(students["grade"] > 8) & (students["grade"] < 12), :])


def test_filter_with_single_lambda(students):
    df = filter(students, lambda x: x.grade > 8)
    assert df.equals(students.loc[(students["grade"] > 8), :])


def test_filter_with_multiple_lambda(students):
    df = filter(students, lambda x: x.grade > 8, lambda x: x.grade < 12)
    assert df.equals(students.loc[(students["grade"] > 8) & (students["grade"] < 12), :])


def test_filter_with_both_str_and_lambda(students):
    df = filter(students, "grade > 8", lambda x: x.grade < 12)
    assert df.equals(students.loc[(students["grade"] > 8) & (students["grade"] < 12), :])
