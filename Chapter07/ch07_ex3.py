"""Functional Python Programming 3e

Chapter 7, Example Set 3
"""

import Chapter04.ch04_ex4

# Raw Data Parser

from typing import NamedTuple


class Pair(NamedTuple):
    x: float
    y: float


from typing import Iterator, Iterable, Sequence


def head_reader(rows: Iterator[Sequence[str]]) -> Iterator[Sequence[str]]:
    """Consumes three header rows and returns the iterator."""
    r0 = next(rows)
    r1 = next(rows)
    r2 = next(rows)
    assert set(r2) == {"x", "y"}, set(r2)
    return rows


def tail_reader(rows: Iterable[Sequence[str]]) -> Iterator[Sequence[float]]:
    return (tuple(map(float, row)) for row in rows)


def series(n: int, row_iter: Iterable[Sequence[float]]) -> Iterator[Pair]:
    return (Pair(*row[2 * n : 2 * n + 2]) for row in row_iter)


# Rank Correlation

from collections import defaultdict
from collections.abc import Callable, Iterator, Iterable, Hashable
from typing import NamedTuple, TypeVar, Any, Protocol, cast

BaseT = TypeVar("BaseT", int, str, float)
DataT = TypeVar("DataT")


def rank(
    data: Iterable[DataT], key: Callable[[DataT], BaseT]
) -> Iterator[tuple[float, DataT]]:
    def build_duplicates(
        duplicates: dict[BaseT, list[DataT]],
        data_iter: Iterator[DataT],
        key: Callable[[DataT], BaseT],
    ) -> dict[BaseT, list[DataT]]:
        for item in data_iter:
            duplicates[key(item)].append(item)
        return duplicates

    def rank_output(
        duplicates: dict[BaseT, list[DataT]], key_iter: Iterator[BaseT], base: int = 0
    ) -> Iterator[tuple[float, DataT]]:
        for k in key_iter:
            dups = len(duplicates[k])
            for value in duplicates[k]:
                yield (base + 1 + base + dups) / 2, value
            base += dups

    duplicates = build_duplicates(defaultdict(list), iter(data), key)
    return rank_output(duplicates, iter(sorted(duplicates.keys())), 0)


def test_rank() -> None:
    # Samples are 1-tuples
    data_1 = [(0.8,), (1.2,), (1.2,), (2.3,), (18.0,)]
    ranked_1 = list(rank(data_1, key=lambda x: x[0]))
    expected_1 = [
        (1.0, (0.8,)),
        (2.5, (1.2,)),
        (2.5, (1.2,)),
        (4.0, (2.3,)),
        (5.0, (18.0,)),
    ]
    assert ranked_1 == expected_1

    # Samples are two-tuples, we rank by 2nd value.
    data_2 = [(2.0, 0.8), (3.0, 1.2), (5.0, 1.2), (7.0, 2.3), (11.0, 18.0)]
    ranked_2 = list(rank(data_2, key=lambda x: x[1]))
    expected_2 = [
        (1.0, (2.0, 0.8)),
        (2.5, (3.0, 1.2)),
        (2.5, (5.0, 1.2)),
        (4.0, (7.0, 2.3)),
        (5.0, (11.0, 18.0)),
    ]
    assert ranked_2 == expected_2


REPL_test_rank = """
>>> from pprint import pprint

>>> data_1 = [(0.8,), (1.2,), (1.2,), (2.3,), (18.,)]
>>> ranked_1 = list(rank(data_1, lambda row: row[0]))
>>> pprint(ranked_1)
[(1.0, (0.8,)), (2.5, (1.2,)), (2.5, (1.2,)), (4.0, (2.3,)), (5.0, (18.0,))]

>>> from random import shuffle
>>> shuffle(data_1)
>>> ranked_1s = list(rank(data_1, lambda row: row[0]))
>>> ranked_1s == ranked_1
True

>>> data_2 = [(2., 0.8), (3., 1.2), (5., 1.2), (7., 2.3), (11., 18.)]
>>> ranked_2 = list(rank(data_2, key=lambda x: x[1],))
>>> pprint(ranked_2)
[(1.0, (2.0, 0.8)),
 (2.5, (3.0, 1.2)),
 (2.5, (5.0, 1.2)),
 (4.0, (7.0, 2.3)),
 (5.0, (11.0, 18.0))]
"""

# Imperative Solution using a list
# Comments indicate how to use a queue instead.

from typing import Sequence


def rank2_imp(
    data: Sequence[tuple[BaseT, ...]],
    key: Callable[[tuple[BaseT, ...]], BaseT] = lambda x: x[0],
) -> Iterator[tuple[float, tuple[BaseT, ...]]]:
    """
    Alternative rank using a stateful queue object: optimized version.

    >>> data_1 = [(0.8,), (1.2,), (1.2,), (2.3,), (18.,)]
    >>> list(rank2_imp(data_1))
    [(1.0, (0.8,)), (2.5, (1.2,)), (2.5, (1.2,)), (4.0, (2.3,)), (5.0, (18.0,))]
    >>> data_2 = [(2., 0.8), (3., 1.2), (5., 1.2), (7., 2.3), (11., 18.)]
    >>> list(rank2_imp(data_2, key=lambda x:x[1]))
    [(1.0, (2.0, 0.8)), (2.5, (3.0, 1.2)), (2.5, (5.0, 1.2)), (4.0, (7.0, 2.3)), (5.0, (11.0, 18.0))]
    """
    data_iter = iter(sorted(data, key=key))
    base = 0
    same_rank = [next(data_iter)]  # Queue().append(data_iter)
    for value in data_iter:
        if key(value) == key(same_rank[0]):
            same_rank.append(value)  # or same_rank += [value]
        else:
            dups = len(same_rank)
            for dup_rank_item in same_rank:  # same_rank.pop()
                yield (base + 1 + base + dups) / 2, dup_rank_item
            base += dups
            same_rank = [value]  # same_rank.append()
    dups = len(same_rank)
    for value in same_rank:  # same_rank.pop()
        yield (base + 1 + base + dups) / 2, value


def rank2_rec(
    data: Sequence[tuple[BaseT, ...]],
    key: Callable[[tuple[BaseT, ...]], BaseT] = lambda x: x[0],
) -> Iterator[tuple[float, tuple[BaseT, ...]]]:
    """
    Alternative rank without a Counter object.
    Closer to properly recursive version.

    >>> data_1 = [(0.8,), (1.2,), (1.2,), (2.3,), (18.,)]
    >>> list(rank2_rec(data_1))
    [(1.0, (0.8,)), (2.5, (1.2,)), (2.5, (1.2,)), (4.0, (2.3,)), (5.0, (18.0,))]
    >>> data_2 = [(2., 0.8), (3., 1.2), (5., 1.2), (7., 2.3), (11., 18.)]
    >>> list(rank2_rec(data_2, key=lambda x:x[1]))
    [(1.0, (2.0, 0.8)), (2.5, (3.0, 1.2)), (2.5, (5.0, 1.2)), (4.0, (7.0, 2.3)), (5.0, (11.0, 18.0))]
    """

    def yield_sequence(
        rank: float, same_rank_iter: Iterator[tuple[BaseT, ...]]
    ) -> Iterator[tuple[float, tuple[BaseT, ...]]]:
        try:
            head = next(same_rank_iter)
        except StopIteration:
            return
        yield rank, head
        yield from yield_sequence(rank, same_rank_iter)

    def ranker(
        sorted_iter: Iterator[tuple[BaseT, ...]],
        base: int,
        same_rank_list: list[tuple[BaseT, ...]],
    ) -> Iterator[tuple[float, tuple[BaseT, ...]]]:
        try:
            value = next(sorted_iter)
        except StopIteration:
            dups = len(same_rank_list)
            yield from yield_sequence(
                (base + 1 + base + dups) / 2, iter(same_rank_list)
            )
            return
        if key(value) == key(same_rank_list[0]):
            yield from ranker(sorted_iter, base, same_rank_list + [value])
        else:
            dups = len(same_rank_list)
            yield from yield_sequence(
                (base + 1 + base + dups) / 2, iter(same_rank_list)
            )
            for rows in ranker(sorted_iter, base + dups, [value]):
                yield rows

    data_iter = iter(sorted(data, key=key))
    head = next(data_iter)
    yield from ranker(data_iter, 0, [head])


# Spearman Rank-Order Correlation

from pyrsistent import PRecord, field, PMap, pmap


class Ranked_XY(PRecord):  # type: ignore [type-arg]
    rank = field(type=PMap)
    raw = field(type=Pair)


def rank_xy(pairs: Sequence[Pair]) -> Iterator[Ranked_XY]:
    data = list(Ranked_XY(rank=pmap(), raw=p) for p in pairs)

    for attribute_name in ("x", "y"):
        ranked = rank(data, lambda rxy: cast(float, getattr(rxy.raw, attribute_name)))
        data = list(
            original.set(
                rank=original.rank.set(attribute_name, r)  # type: ignore [arg-type]
            )
            for r, original in ranked
        )

    yield from iter(data)


from collections.abc import Sequence


def rank_corr(pairs: Sequence[Pair]) -> float:
    ranked = rank_xy(pairs)
    sum_d_2 = sum(
        (r.rank["x"] - r.rank["y"]) ** 2  # type: ignore[operator, index]
        for r in ranked
    )
    n = len(pairs)
    return 1 - 6 * sum_d_2 / (n * (n**2 - 1))


from pytest import fixture


@fixture
def series_data() -> list[Pair]:
    data = [
        Pair(x=10.0, y=8.04),
        Pair(x=8.0, y=6.95),
        Pair(x=13.0, y=7.58),
        Pair(x=9.0, y=8.81),
        Pair(x=11.0, y=8.33),
        Pair(x=14.0, y=9.96),
        Pair(x=6.0, y=7.24),
        Pair(x=4.0, y=4.26),
        Pair(x=12.0, y=10.84),
        Pair(x=7.0, y=4.82),
        Pair(x=5.0, y=5.68),
    ]
    return data


@fixture
def hght_mass_data() -> list[Pair]:
    data = [
        Pair(x=1.47, y=52.21),
        Pair(x=1.5, y=53.12),
        Pair(x=1.52, y=54.48),
        Pair(x=1.55, y=55.84),
        Pair(x=1.57, y=57.2),
        Pair(x=1.6, y=58.57),
        Pair(x=1.63, y=59.93),
        Pair(x=1.65, y=61.29),
        Pair(x=1.68, y=63.11),
        Pair(x=1.7, y=64.47),
        Pair(x=1.73, y=66.28),
        Pair(x=1.75, y=68.1),
        Pair(x=1.78, y=69.92),
        Pair(x=1.8, y=72.19),
        Pair(x=1.83, y=74.46),
    ]
    return data


def test_spearman_rank_corr(
    series_data: list[Pair], hght_mass_data: list[Pair]
) -> None:
    data = [
        Pair(x=86.0, y=0.0),
        Pair(x=97.0, y=20.0),
        Pair(x=99.0, y=28.0),
        Pair(x=100.0, y=27.0),
        Pair(x=101.0, y=50.0),
        Pair(x=103.0, y=29.0),
        Pair(x=106.0, y=7.0),
        Pair(x=110.0, y=17.0),
        Pair(x=112.0, y=6.0),
        Pair(x=113.0, y=12.0),
    ]
    r = rank_corr(data)
    assert round(r, 9) == -0.175757576

    assert round(rank_corr(series_data), 3) == 0.818

    # Note that Pearson R for Anscombe data set I is 0.816.
    # The difference, while small, is significant.

    assert round(rank_corr(hght_mass_data), 3) == 1.0


REPL_spearman_test = """
>>> data = [Pair(x=10.0, y=8.04),
... Pair(x=8.0, y=6.95),
... Pair(x=13.0, y=7.58), Pair(x=9.0, y=8.81),
... Pair(x=11.0, y=8.33), Pair(x=14.0, y=9.96),
... Pair(x=6.0, y=7.24), Pair(x=4.0, y=4.26),
... Pair(x=12.0, y=10.84), Pair(x=7.0, y=4.82),
... Pair(x=5.0, y=5.68)]
>>> round(pearson_corr(data), 3)
0.816
"""

from collections.abc import Sequence
from Chapter04.ch04_ex4 import corr


def pearson_corr(pairs: Sequence[Pair]) -> float:
    X = tuple(p.x for p in pairs)
    Y = tuple(p.y for p in pairs)
    return corr(X, Y)


def test_pearson_corr(series_data: list[Pair], hght_mass_data: list[Pair]) -> None:
    assert round(pearson_corr(series_data), 3) == 0.816

    assert round(pearson_corr(hght_mass_data), 5) == 0.99458


REPL_test_all = """
>>> import csv
>>> from io import StringIO
>>> Anscombe = '''\
... Anscombe's quartet
... I\\tII\\tIII\\tIV
... x\\ty\\tx\\ty\\tx\\ty\\tx\\ty
... 10.0\\t8.04\\t10.0\\t9.14\\t10.0\\t7.46\\t8.0\\t6.58
... 8.0\\t6.95\\t8.0\\t8.14\\t8.0\\t6.77\\t8.0\\t5.76
... 13.0\\t7.58\\t13.0\\t8.74\\t13.0\\t12.74\\t8.0\\t7.71
... 9.0\\t8.81\\t9.0\\t8.77\\t9.0\\t7.11\\t8.0\\t8.84
... 11.0\\t8.33\\t11.0\\t9.26\\t11.0\\t7.81\\t8.0\\t8.47
... 14.0\\t9.96\\t14.0\\t8.10\\t14.0\\t8.84\\t8.0\\t7.04
... 6.0\\t7.24\\t6.0\\t6.13\\t6.0\\t6.08\\t8.0\\t5.25
... 4.0\\t4.26\\t4.0\\t3.10\\t4.0\\t5.39\\t19.0\\t12.50
... 12.0\\t10.84\\t12.0\\t9.13\\t12.0\\t8.15\\t8.0\\t5.56
... 7.0\\t4.82\\t7.0\\t7.26\\t7.0\\t6.42\\t8.0\\t7.91
... 5.0\\t5.68\\t5.0\\t4.74\\t5.0\\t5.73\\t8.0\\t6.89
... '''
>>> with StringIO(Anscombe) as source:
...        rdr= csv.reader( source, delimiter='\\t' )
...        data= tuple(tail_reader( head_reader(rdr) ))
...        s_I= tuple(series(0, data))
...        s_II= tuple(series(1, data))
...        s_III= tuple(series(2, data))
...        s_IV= tuple(series(3, data))
>>> print( "Set {0:>4s}, {1:.3f}, {2:.3f}".format(
...        "I", rank_corr( s_I ), pearson_corr( s_I ) ) )
Set    I, 0.818, 0.816
>>> print( "Set {0:>4s}, {1:.3f}, {2:.3f}".format(
...        "II", rank_corr( s_II ), pearson_corr( s_II ) ) )
Set   II, 0.691, 0.816
>>> print( "Set {0:>4s}, {1:.3f}, {2:.3f}".format(
...        "III", rank_corr( s_III ), pearson_corr( s_III ) ) )
Set  III, 0.991, 0.816
>>> print( "Set {0:>4s}, {1:.3f}, {2:.3f}".format(
...     "IV", rank_corr( s_IV ), pearson_corr( s_IV ) ) )
Set   IV, 0.625, 0.817
"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
