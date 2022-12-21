"""Functional Python Programming 3e

Chapter 5, Example Set 3
"""

from collections.abc import Callable
from typing import Any


class NullAware:
    def __init__(self, some_func: Callable[[Any], Any]) -> None:
        self.some_func = some_func

    def __call__(self, arg: Any) -> Any:
        return None if arg is None else self.some_func(arg)


import math

null_log_scale = NullAware(math.log)

null_round_4 = NullAware(lambda x: round(x, 4))


REPL_test_NullAware = """
>>> some_data = [10, 100, None, 50, 60]
>>> scaled = map(null_log_scale, some_data)
>>> [null_round_4(v) for v in scaled]
[2.3026, 4.6052, None, 3.912, 4.0943]
"""

from collections.abc import Callable, Iterable


class Sum_Filter:
    __slots__ = ["filter", "function"]

    def __init__(
        self, filter: Callable[[float], bool], func: Callable[[float], float]
    ) -> None:
        self.filter = filter
        self.function = func

    def __call__(self, iterable: Iterable[float]) -> float:
        return sum(self.function(x) for x in iterable if self.filter(x))


count_not_none = Sum_Filter(lambda x: x is not None, lambda x: 1)


REPL_test_Sum_Filter = """
>>> some_data = [10, 100, None, 50, 60]
>>> count_not_none(some_data)
4

>>> some_data = [10, 100, None, 50, 60]
>>> count_not_none(some_data)
4
"""

from collections.abc import Callable, Iterator, Iterable
from typing import TypeAlias

Predicate: TypeAlias = Callable[[float], bool]
Transformation: TypeAlias = Callable[[float], float]


def sum_filter_f(
    filter_f: Predicate, function: Transformation, data: Iterable[float]
) -> float:
    return sum(function(x) for x in data if filter_f(x))


count_ = lambda x: 1
sum_ = lambda x: x
valid = lambda x: x is not None

REPL_test_sum_filter_f = """
>>> from Chapter05.ch05_ex1 import numbers_from_rows
>>> text= '''      2      3      5      7     11     13     17     19     23     29
...     31     37     41     43     47     53     59     61     67     71
...    179    181    191    193    197    199    211    223    227    229'''

>>> data = tuple(numbers_from_rows(int, text))
>>> len(data)
30

>>> sum_filter_f( valid, count_, data )
30
>>> sum_filter_f( valid, sum_, data )
2669
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
