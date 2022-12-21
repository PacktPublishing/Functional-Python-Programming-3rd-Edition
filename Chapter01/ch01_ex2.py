"""Functional Python Programming 3e

Chapter 1, Example Set 2

Newton-Raphson root-finding via bisection.

http://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf

Translated from Miranda to Python.
Translated from Miranda to Python.

..  math::

    a_{i+1} = (a_i+n/a_i)/2

Converges on

..  math::

    a = (a+n/a)/2

So

..  math::

    2a  &= a+n/a \\\\
    a   &= n/a \\\\
    a^2 &= n \\\\
    a   &= \\sqrt n
"""
from collections.abc import Callable, Iterator, Iterable

# next_ = lambda n, x: (x+n/x)/2


def next_(n: float, x: float) -> float:
    return (x + n / x) / 2


REPL_next = """
>>> n = 2
>>> f = lambda x: next_(n, x)
>>> a0 = 1.0
>>> [round(x, 4)
... for x in (a0, f(a0), f(f(a0)), f(f(f(a0))),)
... ]
[1.0, 1.5, 1.4167, 1.4142]
"""

from collections.abc import Iterator, Callable


def repeat(f: Callable[[float], float], a: float) -> Iterator[float]:
    yield a
    yield from repeat(f, f(a))


REPL_repeat = """
>>> rpt = repeat(lambda x: x+1, 0)
>>> next(rpt)
0
>>> next(rpt)
1
>>> next(rpt)
2
>>> next(rpt)
3
"""

REPL_syntax_check = """
>>> def f():
...     for x in some_iter: yield x
>>> def g():
...     yield from some_iter
"""

from collections.abc import Iterator


def within(ε: float, iterable: Iterator[float]) -> float:
    def head_tail(ε: float, a: float, iterable: Iterator[float]) -> float:
        b = next(iterable)
        if abs(a - b) <= ε:
            return b
        return head_tail(ε, b, iterable)

    return head_tail(ε, next(iterable), iterable)


REPL_within = """
>>> within(.5, iter([3, 2, 1, .5, .25]))
0.5
"""


def sqrt(n: float) -> float:
    return within(ε=0.0001, iterable=repeat(lambda x: next_(n, x), 1.0))


from pytest import approx


def test_sqrt() -> None:
    assert round(next_(2, 1.5), 4) == approx(1.4167)
    n = 2
    f: Callable[[float], float] = lambda x: next_(n, x)
    a_0 = 1.0
    assert [
        round(x, 4)
        for x in (
            a_0,
            f(a_0),
            f(f(a_0)),
            f(f(f(a_0))),
        )
    ] == [1.0, 1.5, approx(1.4167), approx(1.4142)]
    assert within(0.5, iter([3, 2, 1, 0.5, 0.25])) == 0.5

    assert round(sqrt(3), 6) == approx(1.732051)
    sqrt_3 = sqrt(3)
    assert sqrt_3 ** 2 == approx(3.0)


REPL_sqrt = """
>>> round(sqrt(3), 6)
1.732051
>>> round(1.732051**2, 5)
3.0
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
