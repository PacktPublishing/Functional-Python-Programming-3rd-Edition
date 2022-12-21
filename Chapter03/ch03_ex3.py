"""Functional Python Programming 3e

Chapter 3, Example Set 3
"""

import math

REPL_comprehension = """
>>> list(x**2 for x in range(10)) == [x**2 for x in range(10)]
True
"""

from collections.abc import Iterator


def candidates() -> Iterator[int]:
    for i in range(2, 1024):
        yield m1f(i)


REPL_yield_statement = """
>>> c = candidates()
>>> next(c)
3
>>> next(c)
7
>>> next(c)
15
>>> next(c)
31
"""

from Chapter03.ch03_ex1 import m1f

from collections.abc import Iterator


def bunch_of_numbers() -> Iterator[int]:
    for i in range(5):
        yield from range(i)


REPL_yield_from_statement = """
>>> list(bunch_of_numbers())
[0, 0, 1, 0, 1, 2, 0, 1, 2, 3]
"""

from collections.abc import Iterator
import math


def pfactorsl(x: int) -> Iterator[int]:
    if x % 2 == 0:
        yield 2
        if x // 2 > 1:
            yield from pfactorsl(x // 2)
        return
    for i in range(3, int(math.sqrt(x) + 0.5) + 1, 2):
        if x % i == 0:
            yield i
            if x // i > 1:
                yield from pfactorsl(x // i)
            return
    yield x


def test_pfactorsl() -> None:
    assert list(pfactorsl(1560)) == [2, 2, 2, 3, 5, 13]
    assert list(pfactorsl(2)) == [2]
    assert list(pfactorsl(3)) == [3]


REPL_test_pfactorsl_1 = """
>>> pfactorsl(1560)
<generator object pfactorsl at ...>

>>> list(pfactorsl(1560))
[2, 2, 2, 3, 5, 13]

>>> len(pfactorsl(1560))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'generator' has no len()
"""

REPL_test_pfactorsl_2 = """
>>> result = pfactorsl(1560)
>>> sum(result)
27

>>> sum(result)
0
"""

from collections.abc import Iterator


def pfactorsr(x: int) -> Iterator[int]:
    """Pure Recursion factors. Limited to numbers below about 4,000,000"""

    def factor_n(x: int, n: int) -> Iterator[int]:
        if n * n > x:
            yield x
            return
        if x % n == 0:
            yield n
            if x // n > 1:
                yield from factor_n(x // n, n)
        else:
            yield from factor_n(x, n + 2)

    if x % 2 == 0:
        yield 2
        if x // 2 > 1:
            yield from pfactorsr(x // 2)
        return
    yield from factor_n(x, 3)


def test_pfactorsr() -> None:
    assert list(pfactorsr(1560)) == [2, 2, 2, 3, 5, 13]
    assert list(pfactorsr(2)) == [2]
    assert list(pfactorsr(3)) == [3]


from collections.abc import Iterator


def divisorsr(n: int, a: int = 1) -> Iterator[int]:
    """Recursive divisors of n

    >>> list(divisorsr(26))
    [1, 2, 13]
    """
    if a == n:
        return
    if n % a == 0:
        yield a
    yield from divisorsr(n, a + 1)


def divisorsi(n: int) -> Iterator[int]:
    """Imperative divisors of n

    >>> list(divisorsi( 26 ))
    [1, 2, 13]
    """
    return (a for a in range(1, n) if n % a == 0)


def perfect(n: int) -> bool:
    """Perfect numbers test

    >>> perfect( 6 )
    True
    >>> perfect( 28 )
    True
    >>> perfect( 26 )
    False
    >>> perfect( 496 )
    True
    """
    return sum(divisorsr(n, 1)) == n


import itertools
from typing import Any
from collections.abc import Iterable


def limits(iterable: Iterable[Any]) -> Any:
    max_tee, min_tee = itertools.tee(iterable, 2)
    return max(max_tee), min(min_tee)


def test_limits() -> None:
    assert limits([1, 2, 3, 4, 5]) == (5, 1)


from collections.abc import Callable


def syntax_check_1() -> None:
    some_iterable = range(2)
    g: Callable[[int], int] = lambda x: x + 1
    f: Callable[[int], int] = lambda y: y * 2
    g_f_x = (g(f(x)) for x in some_iterable)

    assert list(g_f_x) == [1, 3]


def syntax_check_2() -> None:
    some_iterable = range(2)
    g: Callable[[int], int] = lambda x: x + 1
    f: Callable[[int], int] = lambda y: y * 2
    g_f_x = (g(y) for y in (f(x) for x in some_iterable))

    assert list(g_f_x) == [1, 3]


def syntax_check_3() -> None:
    some_iterable = range(2)
    g: Callable[[int], int] = lambda x: x + 1
    f: Callable[[int], int] = lambda y: y * 2
    f_x = (f(x) for x in some_iterable)

    g_f_x = (g(y) for y in f_x)
    assert list(g_f_x) == [1, 3]


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
