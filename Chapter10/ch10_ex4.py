"""Functional Python Programming 3e

Chapter 10, Example Set 4
"""

REPL_reductions = """
>>> d = [2, 4, 4, 4, 5, 5, 7, 9]

>>> from functools import reduce

>>> reduce(lambda x, y: x+y, d)
40
>>> 2+4+4+4+5+5+7+9
40

>>> ((((((2+4)+4)+4)+5)+5)+7)+9
40

>>> reduce(lambda x, y: x+y**2, d, 0)
232

>>> 0 + 2**2 + 4**2 + 4**2 + 4**2 + 5**2 + 5**2 + 7**2 + 9**2
232

>>> 2 + 4**2 + 4**2 + 4**2 + 5**2 + 5**2 + 7**2 + 9**2
230

"""


from collections.abc import Callable
from functools import reduce
from typing import cast, TypeAlias

FloatFT: TypeAlias = Callable[[float, float], float]

sum2 = lambda data: reduce(cast(FloatFT, lambda x, y: x + y**2), data, 0.0)
sum = lambda data: reduce(cast(FloatFT, lambda x, y: x + y), data, 0.0)
count = lambda data: reduce(cast(FloatFT, lambda x, y: x + 1), data, 0.0)
min = lambda data: reduce(cast(FloatFT, lambda x, y: x if x < y else y), data)
max = lambda data: reduce(cast(FloatFT, lambda x, y: x if x > y else y), data)

test_reductions = """
>>> import math
>>> d = [ 2, 4, 4, 4, 5, 5, 7, 9 ]
>>> sum2(d)
232.0
>>> sum(d)
40.0
>>> count(d)
8.0
>>> sum(d)/count(d)
5.0
>>> math.sqrt((sum2(d)/count(d))-(sum(d)/count(d))**2)
2.0
>>> max(d)
9
>>> min(d)
2
"""

from collections.abc import Callable, Iterable
from functools import reduce
from typing import TypeVar, cast

ST = TypeVar("ST")


def map_reduce(
    map_fun: Callable[[ST], float],
    reduce_fun: Callable[[float, float], float],
    source: Iterable[ST],
    initial: float = 0,
) -> float:
    return reduce(reduce_fun, map(map_fun, source), initial)


from collections.abc import Iterable


def sum2_mr(source_iter: Iterable[float]) -> float:
    return map_reduce(
        map_fun=lambda y: y**2,
        reduce_fun=lambda x, y: x + y,
        source=source_iter,
        initial=0,
    )


def test_sum2_mr() -> None:
    d = [2, 4, 4, 4, 5, 5, 7, 9]
    assert sum2_mr(d) == 232


from collections.abc import Iterable
import operator


def sum2_mr2(source: Iterable[float]) -> float:
    return map_reduce(lambda y: y**2, operator.add, source, 0)


def test_sum2_mr2() -> None:
    d = [2, 4, 4, 4, 5, 5, 7, 9]
    assert sum2_mr2(d) == 232


def count_mr(source: Iterable[float]) -> float:
    return map_reduce(lambda y: 1, lambda x, y: x + y, source, 0)


def test_count_mr() -> None:
    d = [2, 4, 4, 4, 5, 5, 7, 9]
    assert count_mr(d) == 8


REPL_bad_idea = """
>>> list_of_strings = ["Hello, ", "World!"]
>>> reduce(operator.add, list_of_strings, "")
'Hello, World!'
"""

REPL_reduce_initial = """
>>> import operator
>>> from functools import reduce
>>> d = []
>>> reduce(operator.add, d, "hello world")
'hello world'
"""

from functools import partial, reduce

psum2 = partial(reduce, lambda x, y: x + y**2)
pcount = partial(reduce, lambda x, y: x + 1)

REPL_psum_pcount = """
>>> d = [2, 4, 4, 4, 5, 5, 7, 9]
>>> sum2(d)
232.0
>>> psum2(d)
230

>>> count(d)
8.0
>>> pcount(d)
9

>>> psum2(d) == sum2(d)
False
>>> pcount(d) == count(d)
False
"""


from collections.abc import Callable, Iterable
from functools import reduce


def comma_fix(data: str) -> float:
    try:
        return float(data)
    except ValueError:
        return float(data.replace(",", ""))


def clean_sum(cleaner: Callable[[str], float], data: Iterable[str]) -> float:
    return reduce(operator.add, map(cleaner, data))


def test_clean_sum() -> None:
    d = (
        "1,196",
        "1,176",
        "1,269",
        "1,240",
        "1,307",
        "1,435",
        "1,601",
        "1,654",
        "1,803",
        "1,734",
    )
    assert clean_sum(comma_fix, d) == 14415.0


REPL_test_clean_sum = """
>>> d = ('1,196', '1,176', '1,269', '1,240', '1,307',
... '1,435', '1,601', '1,654', '1,803', '1,734')

>>> clean_sum(comma_fix, d)
14415.0
"""

REPL_many_functions = """
>>> d = (
...     '1,196', '1,176', '1,269', '1,240', '1,307',
...     '1,435', '1,601', '1,654', '1,803', '1,734')
>>> sum = clean_sum(comma_fix, d)
>>> comma_fix_squared = lambda x: comma_fix(x)**2
>>> sum_2 = clean_sum(comma_fix_squared, d)
>>> sum
14415.0
>>> sum_2
21285309.0
"""

import operator

sum_p = partial(reduce, operator.add)

test_sump = """
>>> iterable = [2, 4, 4, 4, 5, 5, 7, 9]
>>> sum_p(iterable)
40
>>> sum_p(map(lambda x:x**2, iterable))
232
>>> reduce(lambda x, y: x+y**2, iterable, 0)
232
>>> reduce(lambda x, y: x+y**2, iterable)
230
"""


def performance() -> None:
    import timeit
    import sys

    print("Strings | Reduce | Join")
    for source_len in range(100, 1000, 100):
        data = repr(["x"] * source_len)
        op_r = f'reduce(operator.add, {data}, "")'
        op_j = f'"".join({data})'
        r = timeit.timeit(
            op_r, """from functools import reduce; import operator""", number=10_000
        )
        j = timeit.timeit(op_j, number=10_000)
        print(f"{source_len:7d} | {r:.4f} | {j:.4f}")


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}

if __name__ == "__main__":
    performance()
