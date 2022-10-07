import pandas as pd
import pytest
from numpy.testing import assert_array_equal

import tidybear as tb


@pytest.fixture()
def band_members():
    url = "https://raw.githubusercontent.com/mbmackenzie/tidybear/main/data/band_members.csv"
    return pd.read_csv(url)


@pytest.fixture()
def band_instrumments():
    url = "https://raw.githubusercontent.com/mbmackenzie/tidybear/main/data/band_instruments.csv"
    return pd.read_csv(url)


@pytest.fixture()
def starwars():
    url = "https://raw.githubusercontent.com/mbmackenzie/tidybear/main/data/starwars.csv"
    return pd.read_csv(url, encoding="latin1")


def test_counting(starwars):
    _ = tb.count(starwars, "species")
    assert _.shape == (38, 2)
    assert _.columns.tolist() == ["species", "n"]
    exp = pd.DataFrame({"species": ["Aleena", "Besalisk", "Cerean"], "n": [1, 1, 1]})
    assert_array_equal(_.head(3).values, exp)

    _ = tb.count(starwars, "species", sort=True)
    assert _.shape == (38, 2)
    assert _.columns.tolist() == ["species", "n"]
    assert pd.isna(_.iloc[2, 0])
    _.iloc[2, 0] = "(NA)"
    exp = pd.DataFrame({"species": ["Human", "Droid", "(NA)"], "n": [35, 6, 4]})
    assert_array_equal(_.head(3).values, exp.values)

    _ = tb.count(starwars, "sex", "gender", sort=True)
    assert _.shape == (6, 3)
    assert _.columns.tolist() == ["sex", "gender", "n"]
    exp = pd.DataFrame(
        {
            "sex": ["male", "female", "none"],
            "gender": ["masculine", "feminine", "masculine"],
            "n": [60, 16, 5],
        },
    )
    assert_array_equal(_.head(3).values, exp.values)


def test_filtering_joins(band_members, band_instrumments):
    # https://dplyr.tidyverse.org/reference/filter-joins.html

    _ = tb.semi_join(band_members, band_instrumments, by="name")
    assert _.shape == (2, 2)
    assert _.name.tolist() == ["John", "Paul"]
    assert _.band.tolist() == ["Beatles", "Beatles"]

    _ = tb.anti_join(band_members, band_instrumments, by="name")
    assert _.shape == (1, 2)
    assert _.name.tolist() == ["Mick"]
    assert _.band.tolist() == ["Stones"]
