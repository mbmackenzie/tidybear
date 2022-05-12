from typing import Any
from typing import Dict

import pandas as pd


def tribble(*args: Any) -> pd.DataFrame:
    """Create a dataframe"""

    colnames = []
    for arg in args:
        if arg.startswith("~"):
            colnames.append(arg[1:])
        else:
            break

    n_cols = len(colnames)
    data: Dict[str, Any] = {col: [] for col in colnames}

    for i, arg in enumerate(args[n_cols:]):
        col = colnames[i % n_cols]
        data[col].append(arg)

    n_rows = len(data[colnames[0]])
    return pd.DataFrame(data, index=range(n_rows))
