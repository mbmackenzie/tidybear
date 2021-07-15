import pandas as pd

from typing import List, Union

class GroupBy:
    active_summary = None
    active_stats = []
    
    def __init__(self, df, groups):
        self.__groups = groups
        self.__g = df.groupby(groups)

        for col in df.columns:
            setattr(self, col, self.__g[col])
        
    def __enter__(self):
        GroupBy.active_summary = self
        return self
        
    def __exit__(self, *args):
        GroupBy.active_summary = None
        GroupBy.active_stats = []
    
    @property
    def groups(self):
        return self.__groups
    
    def _get_size(self):
        return self.__g.size()

    def _get_col(self, column):
        return self.__g[column]

    def summarise(self):
        return pd.concat(GroupBy.active_stats, axis=1)

class Stat:
    def __init__(self, name, series):
        assert GroupBy.active_summary is not None, "Can't instantiate Stat object outside of GroupBy"
        GroupBy.active_stats.append(series.rename(name))
    
class Stats:

    # assert GroupBy.active_summary is not None, "No active GroupBy"

    @staticmethod
    def size(name="n"):
        Stat(name, GroupBy.active_summary._get_size())

    @staticmethod
    def agg(func, column:str, decimals=None, name=None, temp=False):

        if isinstance(func, list):
            for f in func:
                Stats.agg(f, column, decimals=decimals)
            return

        if not name:
            name = func + "_" + column

        agg = GroupBy.active_summary._get_col(column).agg(func)

        if decimals:
            agg = agg.round(decimals)
        
        if temp:
            return agg
        else:
            Stat(name, agg)

    @staticmethod
    def sum(column, decimals=None, name=None, temp=False):
        return Stats.agg("sum", column, decimals, name, temp)

    @staticmethod
    def mean(column, decimals=None, name=None, temp=False):
        return Stats.agg("mean", column, decimals, name, temp)

    @staticmethod
    def median(column, decimals=None, name=None, temp=False):
        return Stats.agg("median", column, decimals, name, temp)

    @staticmethod
    def max(column, decimals=None, name=None, temp=False):
        return Stats.agg("max", column, decimals, name, temp)

    @staticmethod
    def min(column, decimals=None, name=None, temp=False):
        return Stats.agg("min", column, decimals, name, temp)