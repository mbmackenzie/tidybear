from __future__ import annotations

from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import pandas as pd
from pandas import DataFrame
from pandas import Series

from tidybear.selectors import _ColumnList
from tidybear.selectors import TidySelector
from tidybear.utils import get_column_names


def count(
    df: DataFrame,
    columns: _ColumnList,
    *,
    sort: bool = False,
    name: str = "n",
) -> DataFrame:
    """Quickly count the unique values of one or more variables.

    Parameters
    ----------
    df : DataFrame
        The dataframe to use
    columns : str, TidySelectors, or list or str, TidySelectors
        The column(s) to group by.
    sort : bool
        If True, will show the largest groups at the top, by default False
    name: str
        What to rename the new column with counts. By default "n" is used.
    """

    groupby_cols = get_column_names(df.columns, columns)
    counts = df.groupby(groupby_cols).size().rename(name).reset_index()

    if sort:
        return counts.sort_values(name, ascending=False)
    else:
        return counts.sort_values(columns)


def join(
    left: pd.DataFrame,
    right: pd.DataFrame,
    how: str,
    *args: Any,
    **kwargs: str,
) -> pd.DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    *args : str
        The columns to join on
        Can be individual columns, or one list of columns
    **kwargs : str
        The columns to join, left="right"

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """

    left_on: List[str] = []
    right_on: List[str] = []

    if args:
        if len(args) > 1 and any([isinstance(arg, list) for arg in args]):
            raise ValueError(
                "Only individual names or one list of names " "can be passed as unnamed args"
            )

        if len(args) == 1 and isinstance(args[0], list):
            left_on.extend(args[0])
            right_on.extend(args[0])
        else:
            left_on.extend(args)
            right_on.extend(args)

    if kwargs:
        left_on.extend(kwargs.keys())
        right_on.extend(kwargs.values())

    return left.merge(
        right,
        how=how,
        left_on=left_on,
        right_on=right_on,
    )


JoinKey = Union[str, Sequence[str]]
ByKey = Union[JoinKey, Tuple[JoinKey, JoinKey]]


def _join(
    left: DataFrame,
    right: DataFrame,
    how: str,
    left_on: JoinKey,
    right_on: JoinKey,
) -> DataFrame:
    """join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    left_on : JoinKey
        The column(s) to join on the left
    right_on : JoinKey
        The column(s) to join on the right

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """
    return left.merge(right, how=how, left_on=left_on, right_on=right_on)


def _get_join_keys(by: ByKey) -> Tuple[JoinKey, JoinKey]:
    if isinstance(by, tuple):
        if len(by) == 2:
            return by  # type: ignore

        raise ValueError("if using tuple key, must be a tuple of length 2")

    return by, by


def inner_join(left: DataFrame, right: DataFrame, by: ByKey) -> DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    by: ByKey
        The columns to join on. Can be a single column name, for mutual column names on both sides,
        or a tuple of column names, for different column names on each side.

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """
    return _join(left, right, "inner", *_get_join_keys(by))


def left_join(left: DataFrame, right: DataFrame, by: ByKey) -> DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    by: ByKey
        The columns to join on. Can be a single column name, for mutual column names on both sides,
        or a tuple of column names, for different column names on each side.

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """
    return _join(left, right, "left", *_get_join_keys(by))


def right_join(left: DataFrame, right: DataFrame, by: ByKey) -> DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    by: ByKey
        The columns to join on. Can be a single column name, for mutual column names on both sides,
        or a tuple of column names, for different column names on each side.

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """
    return _join(left, right, "right", *_get_join_keys(by))


def outer_join(left: DataFrame, right: DataFrame, by: ByKey) -> DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    by: ByKey
        The columns to join on. Can be a single column name, for mutual column names on both sides,
        or a tuple of column names, for different column names on each side.

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """
    return _join(left, right, "outer", *_get_join_keys(by))


def semi_join(left: DataFrame, right: DataFrame, by: ByKey) -> DataFrame:
    """Semi join two dataframes, i.e., return all rows and columns from the left dataframe
    that have a match in the right dataframe. The columns from the right dataframe are not
    included in the result.

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    by: ByKey
        The columns to join on. Can be a single column name, for mutual column names on both sides,
        or a tuple of column names, for different column names on each side.
    """

    return _join(left, right, "inner", *_get_join_keys(by)).reindex(columns=left.columns)


def anti_join(left: DataFrame, right: DataFrame, by: ByKey) -> DataFrame:
    """Anti join two dataframes, i.e., return all rows and columns from the left dataframe
    that do not have a match in the right dataframe. The columns from the right dataframe are not
    included in the result.

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    by: ByKey
        The columns to join on. Can be a single column name, for mutual column names on both sides,
        or a tuple of column names, for different column names on each side.
    """

    return (
        _join(left.assign(_left=True), right.assign(_right=True), "left", *_get_join_keys(by))
        .where(lambda x: x._right.isna())
        .dropna(subset=["_left"])
        .reindex(columns=left.columns)
    )


def crossing(left: DataFrame, right: DataFrame) -> DataFrame:
    """Cross join two dataframes

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    """

    return left.merge(right, how="cross")


def mutate(df: DataFrame, **kwargs: Callable[..., Any]) -> DataFrame:
    """Create a new column in a dataframe using applied functions

    ```python
    tb.mutate(df, col_squared=lambda x: x.col**2)
    ```

    Parameters
    ----------
    df : DataFrame
    new_name : str
        the name of the new column to create
    definition : function
        the function to apply

    Returns
    -------
    DataFrame
    """

    df = df.copy()

    for name, definition in kwargs.items():
        df[name] = df.apply(definition, axis=1)

    return df


def pivot_wider(
    df: pd.DataFrame,
    *,
    names_from: str = "name",
    values_from: Union[List[str], str] = "value",
    fill_value: Optional[Any] = None,
    prefix_names: bool = False,
) -> pd.DataFrame:
    """
    Transform a dataframe from long to wide

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to transform
    names_from : str
        The column name to pivot on
    values_from : str, List[str]
        The column name to pivot on
        If multiple names are passed, the columns will be <value>_<name>
    fill_value : Optional[Any]
        The value to fill in the new column

    >>> df = pd.DataFrame({"idx": [1, 2], "name": ["a", "a"], "value": [3, 4]})
    >>> pivot_wider(df)
       idx  a
    0    1  3
    1    2  4

    Returns
    -------
    pandas.DataFrame
        The transformed dataframe
    """

    df = df.copy()

    if isinstance(values_from, str):
        values_from = [values_from]

    index_cols = [c for c in df.columns if c not in [names_from, *values_from]]
    df = df.pivot(index=index_cols, columns=names_from, values=values_from)

    if len(values_from) == 1 and not prefix_names:
        df.columns = [name for _, name in df.columns.to_flat_index()]
    else:
        df.columns = [f"{value}_{name}" for value, name in df.columns.to_flat_index()]

    if fill_value is not None:
        df = df.fillna(fill_value)

    return df.reset_index()


def pivot_longer(
    df: pd.DataFrame,
    cols: _ColumnList,
    *,
    names_to: str = "name",
    values_to: str = "value",
    drop_na: bool = True,
    cols_are_index: bool = False,
) -> pd.DataFrame:
    """
    Transform a dataframe from wide to long

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to transform
    cols : str, list[str], TidySelector
        The columns to pivot on, use all the others as the index
    names_to : str
        The new name for the name column
    values_to : str
        the new name for the value column
    drop_na : bool, optional
        Whether to drop rows with missing values, default True
    cols_are_index : bool, optional
        Whether the columns are the index or the columns to pivot on, default False

    Examples
    --------

    >>> df = pd.DataFrame({"idx": [1, 2], "a": [1, 2], "b": [1, 2]})
    >>> pivot_longer(df, index="idx")
       idx name  value
    0    1    a      1
    1    1    b      1
    2    2    a      2
    3    2    b      2

    Returns
    -------
    pandas.DataFrame
        The transformed dataframe
    """

    df = df.copy()

    columns = get_column_names(df.columns, cols)
    index_columns = columns if cols_are_index else [c for c in df.columns if c not in columns]

    if len(index_columns) > 0:
        df.set_index(index_columns, inplace=True)

    df = df.stack(dropna=False).reset_index()
    df.columns = [*index_columns, names_to, values_to]

    if drop_na:
        df = df.dropna(subset=[values_to])

    return df


def rename(df: DataFrame, *args: Any, **kwargs: Any) -> DataFrame:
    """Rename the columns of a dataframe

    You can use this function is a few different ways.
    - Use a list of strings to be used as the new column names.
      In this case the length of the list must equal the number
      of columns in the dataframe.
    - Use the new column names as arguments to the function.
      Again the number of arguments passed must equal the number
      of columns in the dataframe.
    - Use a dictionary with the keys as existing column names and
      values as the new column names.
    - Use keyword arguments with the key as new column names
      and values as the old columns names.

    Parameters
    ----------
    df : DataFrame

    Returns
    -------
    DataFrame

    Examples
    --------

    ```
    >>> import pandas as pd
    >>> import tidybear as tb
    >>>
    >>> df = pd.DataFrame({"A": [1, 2],"B": [3, 4]})
    >>> df
    A  B
    0  1  3
    1  2  4
    >>> tb.rename(df, ["X", "Y"])
    X  Y
    0  1  3
    1  2  4
    >>> tb.rename(df, "X", "Y")
    X  Y
    0  1  3
    1  2  4
    >>> tb.rename(df, {"A": "X", "B": "Y"})
    X  Y
    0  1  3
    1  2  4
    >>> tb.rename(df, X="A", Y="B")
    X  Y
    0  1  3
    1  2  4
    ```
    """
    df = df.copy()
    if len(kwargs) > 0:
        return df.rename(columns={v: k for k, v in kwargs.items()})

    if len(args) == 1 and isinstance(args[0], dict):
        return df.rename(columns=args[0])

    if len(args) >= 1:
        new_cols = args[0] if isinstance(args[0], list) else list(args)

        assert len(new_cols) == df.shape[1], (
            f"Number of columns provided ({len(new_cols)}) "
            f"does not match the number of features in the dataframe ({df.shape[1]})."
        )

        df.columns = new_cols
        return df

    return df


def select(
    df: pd.DataFrame,
    *args: Union[str, TidySelector],
    **kwargs: str,
) -> pd.DataFrame:
    """Select columns from a dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to select columns from
    *args : str
        The column names to select
    **kwargs : str
        The column names to select and rename, new_name="old_name"

    Examples
    --------

    >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    >>> select(df, "A")
       A
    0  1

    1  2
    2  3

    >>> select(df, "A", "A")
       A  A
    0  1  1
    1  2  2
    2  3  3

    >>> select(df, b="B")
       b
    0  4
    1  5
    2  6

    """

    to_select: List[Union[str, TidySelector]] = []

    if args:
        to_select.extend(args)

    if kwargs:
        to_select.extend(kwargs.values())
        rename_dict = {v: k for k, v in kwargs.items()}

    to_select_names = get_column_names(df.columns, to_select)
    selected = df.loc[:, to_select_names].copy()

    if kwargs:
        selected.rename(columns=rename_dict, inplace=True)

    return selected


def _slice(
    df: DataFrame,
    order_by: str,
    n: int,
    ascending: bool,
    groupby: Union[str, List[str], None] = None,
) -> DataFrame:
    df = df.copy()

    if groupby:
        return (
            df.groupby(groupby, group_keys=False)
            .apply(lambda x: _slice(x, order_by, n, ascending))
            .reset_index(drop=True)
        )

    return df.sort_values(order_by, ascending=ascending).head(n)


def slice_max(
    df: DataFrame,
    *,
    order_by: str,
    n: int,
    groupby: Union[str, List[str], None] = None,
) -> DataFrame:
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


def slice_min(
    df: DataFrame,
    *,
    order_by: str,
    n: int,
    groupby: Union[str, List[str], None] = None,
) -> DataFrame:
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


def filter(
    df: DataFrame,
    *args: Union[str, Callable[[DataFrame], Series]],
    subset_cols: Optional[Union[str, Sequence[str]]] = None,
) -> DataFrame:
    """Filter a dataframe

    Parameters
    ----------
    df : DataFrame
    *args : str or callable
        The column name or a callable function that returns a boolean series

    Returns
    -------
    DataFrame
    """

    if len(args) == 0:
        return df.copy()

    new_df = df.copy()
    for arg in args:

        if isinstance(arg, str):
            new_df = new_df.query(arg)
        else:
            new_df = new_df.where(arg).dropna(how="all", subset=subset_cols or df.columns)

    return df.loc[new_df.index].copy()
