"""Functional Python Programming 3e

Chapter 10, Example Set 5
"""

from collections import defaultdict
from collections.abc import Iterable, Callable, Iterator
from typing import Any, TypeVar, Protocol, cast

DT = TypeVar("DT")


class Comparable(Protocol):
    def __lt__(self, __other: Any) -> bool:
        ...

    def __gt__(self, __other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...


KT = TypeVar("KT", bound=Comparable)


def partition(
    source: Iterable[DT],
    key: Callable[[DT], KT] = cast(Callable[[DT], KT], lambda x: x),
) -> Iterator[tuple[KT, Iterator[DT]]]:
    """Sorting deferred."""
    pd: dict[KT, list[DT]] = defaultdict(list)
    for item in source:
        pd[key(item)].append(item)
    for k in sorted(pd):
        yield k, iter(pd[k])


from itertools import groupby
from collections.abc import Iterable, Callable, Iterator


def partition_s(
    source: Iterable[DT],
    key: Callable[[DT], KT] = cast(Callable[[DT], KT], lambda x: x),
) -> Iterable[tuple[KT, Iterator[DT]]]:
    """Sort source data"""
    return groupby(sorted(source, key=key), key)


REPL_data = """
>>> data = [('4', 6.1), ('1', 4.0), ('2', 8.3), ('2', 6.5),
... ('1', 4.6), ('2', 6.8), ('3', 9.3), ('2', 7.8),
... ('2', 9.2), ('4', 5.6), ('3', 10.5), ('1', 5.8),
... ('4', 3.8), ('3', 8.1), ('3', 8.0), ('1', 6.9),
... ('3', 6.9), ('4', 6.2), ('1', 5.4), ('4', 5.8)]

>>> data = [('4', 6.1), ('1', 4.0), ('2', 8.3), ('2', 6.5),
... ('1', 4.6), ('2', 6.8), ('3', 9.3), ('2', 7.8),
... ('2', 9.2), ('4', 5.6), ('3', 10.5), ('1', 5.8),
... ('4', 3.8), ('3', 8.1), ('3', 8.0), ('1', 6.9),
... ('3', 6.9), ('4', 6.2), ('1', 5.4), ('4', 5.8)]

>>> for key, group_iter in partition(data, key=lambda x: x[0]):
...     print(key, tuple(group_iter))
1 (('1', 4.0), ('1', 4.6), ('1', 5.8), ('1', 6.9), ('1', 5.4))
2 (('2', 8.3), ('2', 6.5), ('2', 6.8), ('2', 7.8), ('2', 9.2))
3 (('3', 9.3), ('3', 10.5), ('3', 8.1), ('3', 8.0), ('3', 6.9))
4 (('4', 6.1), ('4', 5.6), ('4', 3.8), ('4', 6.2), ('4', 5.8))

>>> for key, group_iter in partition(data, key=lambda x:x[0]):
...     print(key, tuple(group_iter))
1 (('1', 4.0), ('1', 4.6), ('1', 5.8), ('1', 6.9), ('1', 5.4))
2 (('2', 8.3), ('2', 6.5), ('2', 6.8), ('2', 7.8), ('2', 9.2))
3 (('3', 9.3), ('3', 10.5), ('3', 8.1), ('3', 8.0), ('3', 6.9))
4 (('4', 6.1), ('4', 5.6), ('4', 3.8), ('4', 6.2), ('4', 5.8))

>>> for key, group_iter in partition_s(data, key=lambda x:x[0]):
...     print(key, tuple(group_iter))
1 (('1', 4.0), ('1', 4.6), ('1', 5.8), ('1', 6.9), ('1', 5.4))
2 (('2', 8.3), ('2', 6.5), ('2', 6.8), ('2', 7.8), ('2', 9.2))
3 (('3', 9.3), ('3', 10.5), ('3', 8.1), ('3', 8.0), ('3', 6.9))
4 (('4', 6.1), ('4', 5.6), ('4', 3.8), ('4', 6.2), ('4', 5.8))

"""

from collections.abc import Iterable, Sequence


def summarize(
    key: KT, item_iter: Iterable[tuple[KT, float]]
) -> tuple[KT, float, float]:
    # mean = lambda seq: sum(seq) / len(seq)
    def mean(seq: Sequence[float]) -> float:
        return sum(seq) / len(seq)

    # var = lambda mean, seq: sum((x - mean) ** 2 / (len(seq)-1) for x in seq)
    def var(mean: float, seq: Sequence[float]) -> float:
        return sum((x - mean) ** 2 / (len(seq) - 1) for x in seq)

    values = tuple(v for k, v in item_iter)
    m = mean(values)
    return key, m, var(m, values)


REPL_summarize = """
>>> data = [('4', 6.1), ('1', 4.0), ('2', 8.3), ('2', 6.5), ('1', 4.6),
... ('2', 6.8), ('3', 9.3), ('2', 7.8), ('2', 9.2), ('4', 5.6),
... ('3', 10.5), ('1', 5.8), ('4', 3.8), ('3', 8.1), ('3', 8.0),
... ('1', 6.9), ('3', 6.9), ('4', 6.2), ('1', 5.4), ('4', 5.8)]

>>> from itertools import starmap
>>> partition1 = partition(data, key=lambda x: x[0])
>>> groups1 = starmap(summarize, partition1)

>>> from itertools import starmap
>>> partition1 = partition(data, key=lambda x:x[0])
>>> groups1 = starmap(summarize, partition1)
>>> for g, s, s2 in groups1:
...     print(g, round(s,2), round(s2,2))
1 5.34 1.25
2 7.72 1.22
3 8.56 1.9
4 5.5 0.96

>>> import statistics
>>> for k, item_iter in partition(data, key=lambda x:x[0]):
...     values = tuple(v for k, v in item_iter)
...     print(k, round(statistics.mean(values),2), round(statistics.variance(values),2))
1 5.34 1.25
2 7.72 1.22
3 8.56 1.9
4 5.5 0.96

>>> partition2 = partition_s(data, key=lambda x: x[0])
>>> groups2 = starmap(summarize, partition2)

>>> for g, s, s2 in groups2:
...     print(g, round(s,2), round(s2,2))
1 5.34 1.25
2 7.72 1.22
3 8.56 1.9
4 5.5 0.96

>>> partition2 = partition_s(data, key=lambda x:x[0])
>>> groups2 = starmap(summarize, partition2)
>>> for g, s, s2 in groups2:
...     print(g, round(s,2), round(s2,2))
1 5.34 1.25
2 7.72 1.22
3 8.56 1.9
4 5.5 0.96



"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
