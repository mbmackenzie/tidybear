from typing import Iterable
from typing import List
from typing import Sequence
from typing import Union

from tidybear.selectors import TidySelector


def get_column_names(
    cols: Iterable[str],
    to_select: Sequence[Union[str, TidySelector]],
) -> List[str]:
    selected = []
    for item in to_select:
        if isinstance(item, str):
            selected.append(item)
        else:
            selected.extend(item(cols))

    return selected
