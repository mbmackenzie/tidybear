import pandas as pd
import pytest

import tidybear as tb


@pytest.fixture()
def band_members():
    # https://github.com/tidyverse/dplyr/blob/main/data/band_members.rda

    return pd.DataFrame(
        {
            "name": ["Mick", "John", "Paul"],
            "band": ["Stones", "Beatles", "Beatles"],
        }
    )


@pytest.fixture()
def band_instrumments():
    return pd.DataFrame(
        {
            "name": ["John", "Paul", "Keith"],
            "instrument": ["guitar", "bass", "Guitar"],
        }
    )


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
