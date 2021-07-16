import pandas as pd

from typing import List, Union

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
        assert GroupBy.active_grouping is not None, "No active GroupBy."
    
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

        for col in df.columns:
            setattr(self, col, self.__g[col])
        
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

class Stat:
    """A way to collect statistics and other summary features within the context of a `GroupBy`.

    The `Stat` class offers 2 ways of defining summary statistics:
    1. Manually creating a `Stat` object and providing the name and series
    2. Using one of the built in summary statistics

    Either way, creating a `Stat` will append it to the active `GroupBy` object, and prior to 
    exiting the with statement, you can call `GroupBy.summarise` to concatenate all your stats into a single dataframe.

    In order to create a `Stat`, you must first have an active GroupBy (using a with statement), otherwise you will get an error.
    
    Examples
    --------
    ```
    >>> import pandas as pd
    >>> import tidybear as tb
    >>> 
    >>> df = pd.DataFrame({"gr": list("AABB"), "val": [1, 2, 3, 4]})
    >>>
    >>> with tb.GroupBy(df, "gr") as g:
    ...     tb.Stat.size() #auto names "n"
    ...     tb.Stat.mean("val") #auto names "mean_val"
    ...     tb.Stat("first_val", g.val.first())
    ...
    ...     summary = g.summarise()
    ...
    >>> summary
        n  mean_val  first_val
    gr                        
    A   2       1.5          1
    B   2       3.5          3
    ```
    """

    def __init__(self, name: str, series: pd.Series):
        """Create a custom Stat within your GroupBy.

        Parameters
        ----------
        name : str
            What to name the stat
        series : pd.Series
            The values of the stat
        """        
        GroupBy.grouping_is_active()
        GroupBy.active_stats.append(series.rename(name))
    
    @staticmethod
    def size(name="n") -> pd.Series:
        """Compute group sizes.

        Parameters
        ----------
        name : str, optional
            What to name series, by default "n"

        Returns
        -------
        pd.Series
            Number of rows in each group.
        """        
        GroupBy.grouping_is_active()
        Stat(name, GroupBy.active_grouping.size())

    @staticmethod
    def agg(func: Union[str, List[str]], 
            column: str, 
            decimals: int = None, 
            name: str = None, 
            temp:bool = False) -> Union[pd.Series, pd.DataFrame]:
        """Aggregate using one or more operations over the specified variable.

        Parameters
        ----------
        func : str or list
            Function(s) to use for aggregating the data. See pd.Series.agg for acceptable strings.
        column : str
            Name of column to aggregate
        decimals : int, optional
            Number of decimals to round to, by default None
        name : str, optional
            New name of series, by default None. If none the name will be "{func}_{column}". 
            If multiple funcions are provided this parameter is ignored.
        temp : bool, optional, by default False
            If False, the Stat is appended to the active GroupBy. 
            If True, no Stat is appended, and instead the renamed series is returned for further operation.

        Returns
        -------
        Series or DataFrame
        """            
        
        GroupBy.grouping_is_active()
        if isinstance(func, list):
            for f in func:
                Stat.agg(f, column, decimals=decimals)
            return

        if not name:
            name = func + "_" + column

        agg = GroupBy.active_grouping.get(column).agg(func)

        if decimals:
            agg = agg.round(decimals)
        
        if temp:
            return agg
        else:
            Stat(name, agg)

    @staticmethod
    def sum(column: str, decimals: int = None, name: str = None, temp:bool = False):
        """Compute sum of group values.
        
        See `Stat.agg()` for further details.
        """        
        return Stat.agg("sum", column, decimals, name, temp)

    @staticmethod
    def mean(column: str, decimals: int = None, name: str = None, temp:bool = False):
        """Compute mean of group values.
        
        See `Stat.agg()` for further details.
        """     
        return Stat.agg("mean", column, decimals, name, temp)

    @staticmethod
    def median(column: str, decimals: int = None, name: str = None, temp:bool = False):
        """Compute median of group values.
        
        See `Stat.agg()` for further details.
        """  
        return Stat.agg("median", column, decimals, name, temp)

    @staticmethod
    def max(column: str, decimals: int = None, name: str = None, temp:bool = False):
        """Compute max of group values.
        
        See `Stat.agg()` for further details.
        """  
        return Stat.agg("max", column, decimals, name, temp)

    @staticmethod
    def min(column: str, decimals: int = None, name: str = None, temp:bool = False):
        """Compute min of group values.
        
        See `Stat.agg()` for further details.
        """  
        return Stat.agg("min", column, decimals, name, temp)