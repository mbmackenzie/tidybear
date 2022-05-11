import pandas as pd
import pytest

import tidybear as tb


@pytest.fixture
def data():
    return pd.DataFrame({"idx": [1, 2, 3, 4, 5], "a": [1, 1, 2, 3, 3], "b": [3, 3, 4, 1, 2]})


def test_chain1(data):
    d1 = data.tb_rename(x1="a", x2="b").tb_count("x1").tb_count("n").tb_count("nn")

    print(d1)
