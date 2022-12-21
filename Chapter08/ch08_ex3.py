"""Functional Python Programming 3e

Chapter 8, Example Set 3
"""

from itertools import (
    accumulate,
    repeat,
    chain,
    starmap,
    tee,
    dropwhile,
    islice,
    groupby,
)

# Accumulate
# repeat(8128, times=13) -- only the first value is used
# other 13 are to create a sequence of values to drive the generator function

from typing import List


def digits_fixed(value: int, digits: int, base: int) -> List[int]:
    """
    >>> digits_fixed(8128, 16, 2)
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    """
    digits_reversed = (
        x % base for x in accumulate(repeat(value, digits), func=lambda x, y: x // base)
    )
    return list(reversed(list(digits_reversed)))


from typing import Callable, Iterator, TypeVar

T_ = TypeVar("T_")


def while_not(terminate: Callable[[T_], bool], iterator: Iterator[T_]) -> Iterator[T_]:
    """Iterator which terminates."""
    i = next(iterator)
    if terminate(i):
        return
    yield i
    yield from while_not(terminate, iterator)


def digits_variable(value: int, base: int) -> List[int]:
    """
    >>> digits_variable(8128, 2)
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    """
    digits_reversed = (
        x % base
        for x in while_not(
            lambda x: x == 0, accumulate(repeat(value), lambda x, y: x // base)
        )
    )
    return list(reversed(list(digits_reversed)))


def accumulating_collatz(start: int) -> Iterator[int]:
    """
    >>> list(accumulating_collatz(12))
    [12, 6, 3, 10, 5, 16, 8, 4, 2]
    """

    def syracuse(n: int) -> int:
        if n % 2 == 0:
            return n // 2
        return 3 * n + 1

    return while_not(
        lambda x: x == 1, accumulate(repeat(start), lambda a, b: syracuse(a))
    )


from Chapter04.ch04_ex1 import legs, haversine
from Chapter07.ch07_ex1 import LegNT


def quartiles(trip: list[LegNT]) -> list[int]:
    # print( trip[:2], trip[-1] )
    distances = (leg.distance for leg in trip)
    distance_accum = tuple(accumulate(distances))
    total = distance_accum[-1] + 1.0
    quartiles = list(int(4 * d / total) for d in distance_accum)
    # print( list(quartiles[a:a+16] for a in range(0,len(quartiles),16)) )
    return quartiles


def test_quartiles() -> None:
    from Chapter07.ch07_ex1 import get_trip

    trip = get_trip()
    quartile = quartiles(trip)
    assert len(quartile) == 73
    assert quartile == [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
    ]


import csv
from collections.abc import Iterator
from contextlib import ExitStack
from pathlib import Path
from typing import TextIO


def row_iter_csv_tab(*filepaths: Path) -> Iterator[list[str]]:
    with ExitStack() as stack:
        files: list[TextIO] = [stack.enter_context(path.open()) for path in filepaths]
        readers = map(lambda f: csv.reader(f, delimiter="\t"), files)
        yield from chain(*readers)


def test_row_iter_csv_tab() -> None:
    filenames = Path("Anscombe.txt"), Path("crayola.gpl")
    data = list(row_iter_csv_tab(*filenames))
    assert len(data) == 151
    assert data[0] == ["Anscombe's quartet"]
    assert data[14] == ["GIMP Palette"]


REPL_groupby = """
>>> from itertools import groupby
>>> from Chapter07.ch07_ex1 import get_trip

>>> source_url = "file:./Winter%202012-2013.kml"
>>> trip = get_trip(source_url)
>>> quartile = quartiles(trip)
>>> group_iter = groupby(zip(quartile, trip), key=lambda q_raw: q_raw[0])
>>> for group_key, group_iter in group_iter:
...    print(f"Group {group_key+1}: {len(list(group_iter))} legs")
Group 1: 23 legs
Group 2: 14 legs
Group 3: 19 legs
Group 4: 17 legs

"""

from collections import defaultdict
from collections.abc import Iterable, Callable, Hashable

DT = TypeVar("DT")
KT = TypeVar("KT", bound=Hashable)


def groupby_2(
    iterable: Iterable[DT], key: Callable[[DT], KT]
) -> Iterator[tuple[KT, Iterator[DT]]]:
    groups: dict[KT, list[DT]] = defaultdict(list)
    for item in iterable:
        groups[key(item)].append(item)
    for g in groups:
        yield g, iter(groups[g])


REPL_groupby_2 = """
>>> from Chapter07.ch07_ex1 import get_trip
>>> source_url = "file:./Winter%202012-2013.kml"
>>> trip = get_trip()
>>> quartile = quartiles(trip)
>>> group_iter = groupby_2(zip(quartile, trip), key=lambda q_raw: q_raw[0])
>>> for group_key, group_iter in group_iter:
...    print(f"Group {group_key+1}: {len(list(group_iter))} legs")
Group 1: 23 legs
Group 2: 14 legs
Group 3: 19 legs
Group 4: 17 legs

"""

from itertools import cycle, repeat


def subset_rule_iter(source: Iterable[DT], rule: Iterator[bool]) -> Iterator[DT]:
    return (v for v, keep in zip(source, rule) if keep)


all_rows = lambda: repeat(True)
subset = lambda n: (i == 0 for i in cycle(range(n)))
import random


def randomized(limit: int) -> Iterator[bool]:
    while True:
        yield random.randrange(limit) == 0


REPL_pairwise = """
>>> from itertools import pairwise

>>> text = "hello world"
>>> list(pairwise(text))
[('h', 'e'), ('e', 'l'), ('l', 'l'), ...]
"""

from itertools import compress, tee
from collections.abc import Iterable, Iterator, Callable
from typing import TypeVar

SrcT = TypeVar("SrcT")


def filter_concept(
    function: Callable[[SrcT], bool], source: Iterable[SrcT]
) -> Iterator[SrcT]:
    i1, i2 = tee(source, 2)
    return compress(i1, map(function, i2))


from typing import TypeVar

DataT = TypeVar("DataT")


def subset_gen(data: Iterable[DataT], rule: Iterable[bool]) -> Iterator[DataT]:
    return (v for v, keep in zip(data, rule) if keep)


REPL_compress = """
>>> import random
>>> random.seed(1)
>>> data = [random.randint(1, 12) for _ in range(12)]

>>> from itertools import compress

>>> copy = compress(data, all_rows())
>>> list(copy)
[3, 10, 2, 5, 2, 8, 8, 8, 11, 7, 4, 2]

>>> cycle_subset = compress(data, subset(3))
>>> list(cycle_subset)
[3, 5, 8, 7]

>>> random.seed(1)
>>> random_subset = compress(data, randomized(3))
>>> list(random_subset)
[3, 2, 2, 4, 2]
"""

REPL_islicing_A = """
>>> from Chapter04.ch04_ex5 import parse_g

>>> with open("1000.txt") as source:
...    flat = list(parse_g(source))

>>> flat[:10]
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

>>> flat[-10:]
[7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907, 7919]

Groups of five
>>> slices= [flat[i::5] for i in range(5)]
>>> fives= list(zip(*slices))
>>> fives[:2]
[(2, 3, 5, 7, 11), (13, 17, 19, 23, 29)]
>>> fives[-1]
(7879, 7883, 7901, 7907, 7919)

Non-overlapping pairs
>>> list(zip(flat[0::2], flat[1::2]))
[(2, 3), (5, 7), (11, 13), ...]

>>> pairs = list(zip(flat[0::2], flat[1::2]))
>>> len(pairs)
500
>>> pairs[:3]
[(2, 3), (5, 7), (11, 13)]
>>> pairs[-3:]
[(7877, 7879), (7883, 7901), (7907, 7919)]

>>> flat_iter_1 = iter(flat)
>>> flat_iter_2 = iter(flat)
>>> pairs = list(zip(
...     islice(flat_iter_1, 0, None, 2),
...     islice(flat_iter_2, 1, None, 2)
... ))
>>> len(pairs)
500
>>> pairs[:3]
[(2, 3), (5, 7), (11, 13)]
>>> pairs[-3:]
[(7877, 7879), (7883, 7901), (7907, 7919)]
>>> flat_iter_1 = iter(flat)
>>> flat_iter_2 = iter(flat)
>>> pairs = list(zip(
...     islice(flat_iter_1, 0, None, 2),
...     islice(flat_iter_2, 1, None, 2))
... )
>>> len(pairs)
500
>>> pairs[:3]
[(2, 3), (5, 7), (11, 13)]
>>> pairs[-3:]
[(7877, 7879), (7883, 7901), (7907, 7919)]

Legs -- overlapping pairs
>>> flat_iter_1 = iter(flat)
>>> flat_iter_2 = iter(flat)
>>> pairs = list(zip(islice(flat_iter_1, 0, None, 1), islice(flat_iter_2, 1, None, 1)))
>>> len(pairs)
999
>>> pairs[:3]
[(2, 3), (3, 5), (5, 7)]
>>> pairs[-3:]
[(7883, 7901), (7901, 7907), (7907, 7919)]

"""

REPL_dropping_A = """
>>> import csv
>>> from pathlib import Path

>>> source_path = Path("crayola.gpl")
>>> with source_path.open() as source:
...     rdr = csv.reader(source, delimiter='\\t')
...     row_iter = dropwhile(
...         lambda row: row[0] != '#', rdr
...     )
...     color_rows = islice(row_iter, 1, None)
...     colors = list(
...         (color.split(), name) for color, name in color_rows
...     )

>>> with open("crayola.gpl") as source:
...     rdr= csv.reader( source, delimiter='\\t' )
...     rows = dropwhile( lambda row: row[0] != '#', rdr )
...     color_rows = islice( rows, 1, None )
...     colors = list((color.split(), name) for color, name in color_rows)
>>> len(colors)
133
>>> colors[0]
(['239', '222', '205'], 'Almond')
>>> colors[-1]
(['255', '174', '66'], 'Yellow Orange')
"""

filterfalse_concept = lambda pred, iterable: filter(lambda x: not pred(x), iterable)

REPL_filter_false = """
>>> from itertools import filterfalse

>>> source = [0, False, 1, 2]
>>> list(filter(None, source))
[1, 2]

>>> filterfalse(None, source)
<itertools.filterfalse object at ...>
>>> list(_)
[0, False]

>>> raw_samples = list(range(11))
>>> rule = lambda x: x % 3 == 0 or x % 5 == 0
>>> iter_1, iter_2 = tee(iter(raw_samples), 2)

>>> rule_subset_iter = filter(rule, iter_1)
>>> not_rule_subset_iter = filterfalse(rule, iter_2)
>>> list(rule_subset_iter)
[0, 3, 5, 6, 9, 10]
>>> list(not_rule_subset_iter)
[1, 2, 4, 7, 8]
"""

map_concept = lambda function, arg_iter: (function(a) for a in arg_iter)

starmap_concept = (
    lambda function, arg_iter: (function(*a) for a in arg_iter)
    # ^-- Adds this * to decompose tuples
)


from Chapter04.ch04_ex1 import legs, haversine
from Chapter06.ch06_ex3 import row_iter_kml
from Chapter07.ch07_ex1 import float_lat_lon, LegNT, PointNT
import urllib.request
from collections.abc import Callable


def get_trip_starmap(url: str) -> List[LegNT]:
    make_leg: Callable[[PointNT, PointNT], LegNT] = lambda start, end: LegNT(
        start, end, haversine(start, end)
    )
    with urllib.request.urlopen(url) as source:
        path_iter = float_lat_lon(row_iter_kml(source))
        pair_iter = legs(path_iter)
        trip = list(starmap(make_leg, pair_iter))
        # -------- Used here
    return trip


def test_get_trip_starmap() -> None:
    trip = get_trip_starmap("file:./Winter%202012-2013.kml")
    assert len(trip) == 73
    assert trip[0] == LegNT(
        start=PointNT(latitude=37.54901619777347, longitude=-76.33029518659048),
        end=PointNT(latitude=37.840832, longitude=-76.273834),
        distance=17.724564798884984,
    )
    assert trip[-1] == LegNT(
        start=PointNT(latitude=38.330166, longitude=-76.458504),
        end=PointNT(latitude=38.976334, longitude=-76.473503),
        distance=38.801864781785845,
    )


REPL_test_get_trip = """
>>> from pprint import pprint
>>> source_url = "file:./Winter%202012-2013.kml"
>>> trip = get_trip_starmap(source_url)
>>> len(trip)
73
>>> pprint(trip[0])
LegNT(start=PointNT(latitude=37.54901619777347, longitude=-76.33029518659048), end=PointNT(latitude=37.840832, longitude=-76.273834), distance=17.724564798884984)

>>> pprint(trip[-1])
LegNT(start=PointNT(latitude=38.330166, longitude=-76.458504), end=PointNT(latitude=38.976334, longitude=-76.473503), distance=38.801864781785845)
"""


from collections.abc import Iterable


def mean_t(source: Iterable[float]) -> float:
    it_0, it_1 = tee(iter(source), 2)
    N = sum(1 for x in it_0)
    sum_x = sum(x for x in it_1)
    return sum_x / N


import pytest


@pytest.fixture
def anscombe() -> list[tuple[float, ...]]:
    import csv
    from pathlib import Path

    def is_number(x: str) -> bool:
        try:
            float(x)
            return True
        except ValueError:
            return False

    source_path = Path("Anscombe.txt")
    with source_path.open() as source:
        rdr = csv.reader(source, delimiter="\t")
        data_rows = dropwhile(lambda row: not all(map(is_number, row)), rdr)
        float_rows = map(lambda row: tuple(map(float, row)), data_rows)
        return list(float_rows)


def test_mean_t(anscombe: list[tuple[float, ...]]) -> None:
    x_I = (row[0] for row in anscombe)
    y_I = (row[1] for row in anscombe)
    assert mean_t(x_I) == pytest.approx(9.0, rel=1e-3)
    assert mean_t(y_I) == pytest.approx(7.5, rel=1e-3)


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
