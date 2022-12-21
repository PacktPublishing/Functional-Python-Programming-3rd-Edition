"""Functional Python Programming 3e

Chapter 8, Example Set 2
"""

REPL_enumerate = """
>>> from itertools import count
>>> enumerate = lambda x, start=0: zip(count(start), x)

>>> list(zip(count(), iter('word')))
[(0, 'w'), (1, 'o'), (2, 'r'), (3, 'd')]
>>> list(enumerate(iter('word')))
[(0, 'w'), (1, 'o'), (2, 'r'), (3, 'd')]
"""

from collections.abc import Callable, Iterator
from typing import TypeVar

T = TypeVar("T")


def find_first(terminate: Callable[[T], bool], iterator: Iterator[T]) -> T:
    i = next(iterator)
    if terminate(i):
        return i
    return find_first(terminate, iterator)


from itertools import count
from collections.abc import Iterator
from typing import NamedTuple, TypeAlias

Pair = NamedTuple("Pair", [("flt_count", float), ("int_count", float)])
Pair_Gen: TypeAlias = Iterator[Pair]

source: Pair_Gen = (
    Pair(fc, ic) for fc, ic in zip(count(0, 0.1), (0.1 * c for c in count()))
)


def not_equal(pair: Pair) -> bool:
    return abs(pair.flt_count - pair.int_count) > 1.0e-12


REPL_accumulated_error_1 = """
>>> find_first(not_equal, source)
Pair(flt_count=92.799999999999, int_count=92.80000000000001)

>>> source: Pair_Gen = map(Pair, count(0, 0.1), (.1*c for c in count()))

>>> find_first(lambda pair: pair.flt_count != pair.int_count, source)
Pair(flt_count=0.6, int_count=0.6000000000000001)
"""

from collections.abc import Callable, Iterator
from typing import TypeVar

UT = TypeVar("UT")


def find_first_i(terminate: Callable[[UT], bool], iterator: Iterator[UT]) -> UT:
    for i in iterator:
        if terminate(i):
            return i
    raise StopIteration


REPL_accumulated_error_2 = """
>>> from itertools import count

>>> source_2: Pair_Gen = (
...   Pair(fc, ic) for fc, ic in 
...   zip(count(0, 0.1), (.1*c for c in count()))
... )
>>> neq6: Callable[[tuple[float, float]], bool] = lambda pair: abs(pair.flt_count - pair.int_count) > 1.0E-6
>>> find_first_i(neq6, source_2)
Pair(flt_count=94281.30000100001, int_count=94281.3)

>>> source_3 = map(Pair, count(0, 1/35), (c/35 for c in count()))
>>> find_first_i(neq6, source_3)
Pair(flt_count=73143.51428471429, int_count=73143.5142857143)

>>> source_4 = map(Pair, count(0, 1/35), (c/35 for c in count()))
>>> find_first_i(lambda pair: pair.flt_count != pair.int_count, source_4)
Pair(flt_count=0.2285714285714286, int_count=0.22857142857142856)
"""

REPL_fizz_buzz = """
>>> from itertools import cycle

>>> m3 = (i == 0 for i in cycle(range(3)))
>>> m5 = (i == 0 for i in cycle(range(5)))

>>> multipliers = zip(range(10), m3, m5)

This consumes from m3 and m5, changing their state

>>> list(multipliers)
[(0, True, True), (1, False, False), (2, False, False), ..., (9, True, False)]

Reset them for the following example

>>> m3 = (i == 0 for i in cycle(range(3)))
>>> m5 = (i == 0 for i in cycle(range(5)))

>>> multipliers = zip(range(10), m3, m5)
>>> total = sum(i
...     for i, *multipliers in multipliers
...     if any(multipliers)
... )

Reset the m3 and m5 cycles again for another example
>>> m3 = (i == 0 for i in cycle(range(3)))
>>> m5 = (i == 0 for i in cycle(range(5)))
>>> list(zip(range(10), m3, m5))
[(0, True, True), (1, False, False), (2, False, False), (3, True, False), (4, False, False), (5, False, True), (6, True, False), (7, False, False), (8, False, False), (9, True, False)]

>>> total
23
"""

from collections.abc import Iterable, Iterator
from itertools import cycle
from typing import TypeVar

DT = TypeVar("DT")


def subset_iter(source: Iterable[DT], cycle_size: int) -> Iterator[DT]:
    chooser = (x == 0 for x in cycle(range(cycle_size)))
    yield from (row for keep, row in zip(chooser, source) if keep)


import csv
from pathlib import Path


def csv_subset(source: Path, target: Path, cycle_size: int = 3) -> None:
    with (source.open() as source_file, target.open("w", newline="") as target_file):
        rdr = csv.reader(source_file, delimiter="\t")
        wtr = csv.writer(target_file)
        wtr.writerows(subset_iter(rdr, cycle_size))


def test_csv_subset(tmp_path: Path) -> None:
    import csv

    source_path = Path("Anscombe.txt")
    target_path = tmp_path / "subset.txt"
    csv_subset(source_path, target_path, 3)

    with target_path.open() as result:
        rdr = csv.reader(result)
        rows = list(rdr)
    assert rows == [
        ["Anscombe's quartet"],
        ["10.0", "8.04", "10.0", "9.14", "10.0", "7.46", "8.0", "6.58"],
        ["9.0", "8.81", "9.0", "8.77", "9.0", "7.11", "8.0", "8.84"],
        ["6.0", "7.24", "6.0", "6.13", "6.0", "6.08", "8.0", "5.25"],
        ["7.0", "4.82", "7.0", "7.26", "7.0", "6.42", "8.0", "7.91"],
    ]


from itertools import cycle, repeat


def subset_rule_iter(source: Iterable[DT], rule: Iterator[bool]) -> Iterator[DT]:
    return (v for v, keep in zip(source, rule) if keep)


all_rows = lambda: repeat(True)
subset = lambda n: (i == 0 for i in cycle(range(n)))

import random


def randomized(limit: int) -> Iterator[bool]:
    while True:
        yield random.randrange(limit) == 0


REPL_repeater = """
>>> import random
>>> random.seed(42)
>>> data = [random.randint(1, 12) for _ in range(12)]
>>> data
[11, 2, 1, 12, 5, 4, 4, 3, 12, 2, 11, 12]

>>> list(subset_rule_iter(data, all_rows()))
[11, 2, 1, 12, 5, 4, 4, 3, 12, 2, 11, 12]
>>> list(subset_rule_iter(data, subset(3)))
[11, 12, 4, 2]

>>> random.seed(42)
>>> list(subset_rule_iter(data, randomized(3)))
[2, 1, 4, 4, 3, 2]

>>> random.seed(42)
>>> data = [random.randint(1, 12) for _ in range(12)]
>>> data
[11, 2, 1, 12, 5, 4, 4, 3, 12, 2, 11, 12]

>>> [v for v, pick in zip(data, all_rows()) if pick]
[11, 2, 1, 12, 5, 4, 4, 3, 12, 2, 11, 12]
>>> [v for v, pick in zip(data, subset(3)) if pick]
[11, 12, 4, 2]
>>> random.seed(42)
>>> [v for v, pick in zip(data, randomized(3)) if pick]
[2, 1, 4, 4, 3, 2]

>>> from itertools import compress
>>> list(compress(data, all_rows()))
[11, 2, 1, 12, 5, 4, 4, 3, 12, 2, 11, 12]
>>> list(compress(data, subset(3)))
[11, 12, 4, 2]

>>> random.seed(42)
>>> list(compress(data, randomized(3)))
[2, 1, 4, 4, 3, 2]

"""

REPL_enumerate = """
>>> raw_values = [1.2, .8, 1.2, 2.3, 11, 18]

>>> tuple(enumerate(sorted(raw_values)))
((0, 0.8), (1, 1.2), (2, 1.2), (3, 2.3), (4, 11), (5, 18))
"""


REPL_squares = """
>>> from itertools import repeat
>>> squares = list(sum(repeat(i, times=i)) for i in range(10))
>>> print( squares )
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
