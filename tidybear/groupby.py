import pandas as pd
from typing import List, Union

class NoActiveGroupByError(Exception):
    """No active GroupBy"""
    pass

class GroupBy:
    """Simplified API for performing groupby and summarise opperations in pandas.

    Parameters
    ----------
    df : DataFrame
        The dataframe to group.
    groups : str, List[str]
        Used to determine the groups for the groupby.

    Properties
    ----------
    groups : str, List[str]
        The grouping variables that were used.
    <df_columns> :
        You can access the columns of the DataFrameGroupBy object using the 'dot' syntax. 
        To get the grouped columns with the string name, use `get` method. 

    Functions
    ----------
    size : get group sizes
    get : get the grouped column by name
    summarise or summarize : cocatenate all active stats into a single dataframe.  

    Examples
    ----------
    ```
    >>> import pandas as pd
    >>> import tidybear as tb
    >>> 
    >>> df = pd.DataFrame({
    ...     "gr": list("AAABBBB"),
    ...     "val": [1, 2, 3, 7, 8, 8, 9]
    ... })
    >>>
    >>> with tb.GroupBy(df, "gr") as g:
    ...     tb.Stat.size()
    ...     summary = g.summarise()
        n
    gr   
    A   3
    B   4
    ```
    """    
    active_grouping = None
    active_stats = []

    @staticmethod
    def grouping_is_active():
        if GroupBy.active_grouping is None:
            raise NoActiveGroupByError("No active GroupBy.")
        
        return True
    
    def __init__(self, df: pd.DataFrame, groups):
        """Creates an active grouping that can track and summarise provided Stats. Must be used within a with statement.
        
        Parameters
        ----------
        df : DataFrame
            The dataframe to group.
        groups : str, List[str]
            Used to determine the groups for the groupby
        """        
        self.__groups = groups
        self.__g = df.groupby(groups)

        # for col in df.columns:
        #     setattr(self, col, self.__g[col])
        
    def __enter__(self):
        GroupBy.active_grouping = self
        return self
        
    def __exit__(self, *args):
        GroupBy.active_grouping = None
        GroupBy.active_stats = []
    
    @property
    def groups(self) -> Union[str, List[str]]:
        """Get the grouping variables

        Returns
        -------
        str, List[str]
        """        
        return self.__groups
    
    def size(self) -> pd.Series:
        """Compute group sizes.

        Returns
        -------
        Series
            Number of rows in each group as a Series
        """        
        return self.__g.size()

    def get(self, column: str) -> pd.Series:
        """Access a grouped column by name

        Parameters
        ----------
        column : str
            The name of the column

        Returns
        -------
        pd.Series
            The grouped column

        Example
        -------
        ```
        >>> import pandas as pd
        >>> from tidybear import GroupBy, Stat
        >>>
        >>> df = pd.DataFrame({"gr": list("AABB"), "val": [1, 2, 3, 4]})
        >>>
        >>> with GroupBy(df, "gr") as g:
        ...     Stat("sum1", g.val.sum()) #is equivalent
        ...     Stat("sum2", g.get("val").sum()) #to this
        ...     summary = g.summarise()
        ...
        >>> summary
            sum1  sum2
        gr            
        A      3     3
        B      7     7
        """        
        return self.__g[column]

    def summarise(self) -> pd.DataFrame:
        """Concatenate all active stats into a single dataframe. 
        It will naturally join on the grouped columns.

        ```
        return pd.concat(active_stats, axis=1)
        ```

        Returns
        -------
        pd.DataFrame
            Final summary of all stats
        """        
        return pd.concat(GroupBy.active_stats, axis=1)

    def summarize(self) -> pd.DataFrame:
        """Concatenate all active stats into a single dataframe. 
        It will naturally join on the grouped columns.

        ```
        return pd.concat(active_stats, axis=1)
        ```

        Returns
        -------
        pd.DataFrame
            Final summary of all stats
        """        
        return self.summarise()

    def __str__(self):
        return f"GroupBy({self.groups})"