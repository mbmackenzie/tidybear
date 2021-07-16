from pandas.core import groupby
import pytest

import numpy as np
import pandas as pd

from tidybear import GroupBy, Stat
from tidybear.groupby import NoActiveGroupByError

@pytest.fixture
def data():
    n = 1000
    df = pd.DataFrame({
        "A": np.random.choice(list("abc"), size=n),
        "B": np.random.choice(list("wxyz"), size=n),
        "C": np.random.randint(0, 100, size=n),
        "D": np.random.randint(0, 100, size=n)
    })
    return df

def test_groupby_not_active(data):
    """Outside of a with statment, there should be no active GroupBy."""    
    with pytest.raises(NoActiveGroupByError):
        GroupBy.grouping_is_active()

    g = GroupBy(data, "A")
    with pytest.raises(NoActiveGroupByError):
        g.grouping_is_active()

def test_groupby_is_active(data):
    """In a with statement, there should be an active GroupBy."""
    with GroupBy(data, "A") as g:
        assert g.grouping_is_active()
        assert GroupBy.grouping_is_active()
        assert GroupBy.active_grouping == g

def test_groupby_same_series(data):
    """You should be able to access all the columns of your dataframed that are not grouped"""
    pd_g = data.groupby("A")
    with GroupBy(data, "A") as tb_g:
        for col in data.columns:
            pd_col = pd_g[col]
            tb_col = tb_g.get(col)
            
            for (pd_, tb_) in zip(pd_col, tb_col):
                assert pd_[0] == tb_[0]
                pd.testing.assert_series_equal(pd_[1], tb_[1])