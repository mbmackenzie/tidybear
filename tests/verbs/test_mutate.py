import pytest
from pandas import DataFrame

from tidybear import mutate


@pytest.fixture
def data():
    return DataFrame({"A": [1, 2]})


def test_mutate_one_col(data):
    result = mutate(data, aplus1=lambda x: x.A + 1)
    assert result.columns.tolist() == ["A", "aplus1"]
    assert result.aplus1.tolist() == [2, 3]


def test_mutate_mult_col(data):
    result = mutate(data, aplus1=lambda x: x.A + 1, atimes4=lambda x: x.A * 4)
    assert result.columns.tolist() == ["A", "aplus1", "atimes4"]
    assert result.aplus1.tolist() == [2, 3]
    assert result.atimes4.tolist() == [4, 8]
