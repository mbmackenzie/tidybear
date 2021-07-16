# TidyBear

A tidy approach to pandas.

## Groupby and Summarise

Take the dataframe

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "gr": list("AAABBBB"),
    "val": [1, 2, 3, 7, 8, 8, 9]
})
```

To summarise this you could do something like this...

```python
g = df.groupby("gr")

summary = pd.concat([
    g.size().rename("n"),
    g.val.sum().rename("sum_val"),
    g.val.mean().round(3).rename("mean_val"),
    g.val.median().rename("median_val"),
    g.val.apply(lambda x: len(x.unique())).rename("n_distinct_val"),
    ((g.val.max() + g.val.min()) / 2).rename("midpoint")
], axis=1)
```

Or you could do this...

```python
import tidybear as tb

with tb.GroupBy(df, "gr") as g:
    
    # built in statistcs
    tb.Stat.size()
    tb.Stat.agg(["sum", "mean", "median"], "val", decimals=3)
    
    # custom stats
    tb.Stat("n_distinct_val", g.val.apply(lambda x: len(x.unique())))
    
    # use 'temp' keyword to return series and use it later
    max_val = tb.Stat.max("val", temp=True)
    min_val = tb.Stat.min("val", temp=True)
    tb.Stat("midpoint", (max_val + min_val) / 2)
    
    summary = g.summarise()
```

In both cases, `summary` would be the following dataframe:


| gr | n | sum_val | mean_val | median_val | n_distinct_val | midpoint |
|:---|--:|--------:|---------:|-----------:|---------------:|---------:|
| A  | 3 |       6 |        2 |          2 |              3 |        2 |
| B  | 4 |      32 |        8 |          8 |              3 |        8 |