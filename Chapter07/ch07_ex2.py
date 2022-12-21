"""Functional Python Programming 3e

Chapter 7, Example Set 2
"""

REPL_get_raw_data = """
>>> from Chapter03.ch03_ex4 import (
... series, head_map_filter, row_iter)
>>> from pathlib import Path

>>> source_path = Path("Anscombe.txt")
>>> with source_path.open() as source:
...     data = list(head_map_filter(row_iter(source)))
"""

from typing import NamedTuple


class Pair(NamedTuple):
    x: float
    y: float


def test_pair() -> None:
    p = Pair(1.0, 2.0)
    assert p.x == 1.0 and p.y == 2.0


from collections.abc import Callable, Iterable
from typing import TypeAlias

RawPairIter: TypeAlias = Iterable[tuple[float, float]]

pairs: Callable[[RawPairIter], list[Pair]] = lambda source: list(
    Pair(*row) for row in source
)

REPL_test_pairs = """
>>> from Chapter03.ch03_ex4 import (
... series, head_map_filter, row_iter)
>>> from pathlib import Path

>>> source_path = Path("Anscombe.txt")
>>> with source_path.open() as source:
...     data = list(head_map_filter(row_iter(source)))

>>> series_I = pairs(series(0, data))
>>> series_II = pairs(series(1, data))
>>> series_III = pairs(series(2, data))
>>> series_IV = pairs(series(3, data))

>>> from pprint import pprint

>>> pprint(series_I)
[Pair(x=10.0, y=8.04),
 Pair(x=8.0, y=6.95),
 ...
 Pair(x=5.0, y=5.68)]
"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
