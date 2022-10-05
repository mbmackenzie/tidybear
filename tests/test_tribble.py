from tidybear.tribble import tribble


def test_tribble():
    df = tribble(
        "~colA",
        "~colB",
        "a",
        1,
        "b",
        2,
        "c",
        3,
    )

    assert df.columns.tolist() == ["colA", "colB"]
    assert df["colA"].values.tolist() == ["a", "b", "c"]
    assert df["colB"].values.tolist() == [1, 2, 3]
