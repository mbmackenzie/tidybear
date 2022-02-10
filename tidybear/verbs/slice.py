from __future__ import annotations

from pandas import DataFrame


def _slice(df: DataFrame, order_by: str, n: int, ascending: bool, groupby: list[str] | str = None):
    df = df.copy()

    if groupby:
        return df.groupby(groupby) \
            .apply(lambda x: _slice(x, order_by, n, ascending)) \
            .reset_index(drop=True)

    return df.sort_values(order_by, ascending=ascending).head(n)


def slice_max(df: DataFrame, order_by: str, n: int, groupby: str = None):
    """Get the top N elements of a dataframe of group.

    Parameters
    ----------
    df : DataFrame
    order_by : str
        The column to order the values by
    n : int
        The number of elements to get
    groupby : str or list, optional
        Get top n elements by group. These columns used for groupby, by default None

    Returns
    -------
    Dataframe
    """
    return _slice(df, order_by, n, False, groupby)


def slice_min(df: DataFrame, order_by: str, n: int, groupby: str = None):
    """Get the bottom N elements of a dataframe of group.

    Parameters
    ----------
    df : DataFrame
    order_by : str
        The column to order the values by
    n : int
        The number of elements to get
    groupby : str or list, optional
        Get bottom n elements by group. These columns used for groupby, by default None

    Returns
    -------
    Dataframe
    """
    return _slice(df, order_by, n, True, groupby)
