from typing import Callable
from pandas import DataFrame


def mutate(df: DataFrame, new_name: str, definition: Callable) -> DataFrame:
    """Create a new column in a dataframe using applied functions

    For example,

    ```python
    tb.mutate(df, "col_squared", lambda x: x.col**2)
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
    df[new_name] = df.apply(definition, axis=1)

    return df


def mutate_many(df: Callable, mutations: list[tuple[str, Callable]]) -> DataFrame:
    """Create new columns in a dataframe using applied functions

    Parameters
    ----------
    df : DataFrame
    mutations : list of tuples, ex. [(new_name, definition), ...]
        perform one mutation for each definition in the provided list.
        Later mutations can reference column names in earlier mutations.

    Returns
    -------
    DataFrame
    """
    for new_name, definition in mutations:
        df = mutate(df, new_name, definition)

    return df
