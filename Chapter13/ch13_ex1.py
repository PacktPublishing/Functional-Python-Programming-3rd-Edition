"""Functional Python Programming 3e

Chapter 13, Example Set 1
"""

from pymonad.tools import curry  # type: ignore[import]


@curry(4)  # type: ignore[misc]
def systolic_bp(bmi: float, age: float, gender_male: float, treatment: float) -> float:
    return 68.15 + 0.58 * bmi + 0.65 * age + 0.94 * gender_male + 6.44 * treatment


REPL_curry_1 = """
>>> systolic_bp(25, 50, 1, 0)
116.09

>>> systolic_bp(25, 50, 0, 1)
121.59

>>> systolic_bp( 25, 50, 1, 0 )
116.09
>>> systolic_bp( 25, 50, 0, 1 )
121.59

>>> treated = systolic_bp(25, 50, 0)
>>> treated(0)
115.15
>>> treated(1)
121.59
>>> treated = systolic_bp( 25, 50, 0 )
>>> treated(0)
115.15
>>> treated(1)
121.59

>>> g_t = systolic_bp(25, 50)
>>> g_t(1, 0)
116.09
>>> g_t(0, 1)
121.59
>>> g_t = systolic_bp( 25, 50 )
>>> g_t(1, 0)
116.09
>>> g_t(0, 1)
121.59
"""

REPL_curry_2 = """
>>> from pymonad.tools import curry
>>> from functools import reduce

>>> creduce = curry(2, reduce)

>>> from operator import add

>>> my_sum = creduce(add)
>>> my_sum([1,2,3])
6

>>> from operator import *
>>> sum = creduce(add)
>>> sum([1,2,3])
6

>>> my_max = creduce(lambda x,y: x if x > y else y)
>>> my_max([2,5,3])
5

>>> max = creduce(lambda x,y: x if x > y else y)
>>> max([2,5,3])
5
"""

from pymonad.tools import curry
from functools import reduce

creduce = curry(2, reduce)

import operator

prod = creduce(operator.mul)


from collections.abc import Iterable


@curry(1)  # type: ignore[misc]
def alt_range(n: int) -> Iterable[int]:
    if n == 0:
        return range(1, 2)  # Only the value [1]
    elif n % 2 == 0:
        return range(2, n + 1, 2)  # Even
    else:
        return range(1, n + 1, 2)  # Odd


REPL_prod_alt_range = """
>>> prod(alt_range(9))
945

>>> from pymonad.reader import Compose
>>> semi_fact = Compose(alt_range).then(prod)
>>> semi_fact(9)
945
"""

REPL_functor = """
>>> pi = lambda: 3.14
>>> pi()
3.14
"""

REPL_Maybe = """
>>> from pymonad.maybe import Maybe, Just, Nothing

>>> x1 = Maybe.apply(systolic_bp).to_arguments(Just(25), Just(50), Just(1), Just(0))
>>> x1.value
116.09

>>> x2 = Maybe.apply(systolic_bp).to_arguments(Just(25), Just(50), Just(1), Nothing)
>>> x2
Nothing
>>> x2.value is None
True
"""

REPL_ListMonad = """
>>> list(range(10))
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> from pymonad.list import ListMonad
>>> ListMonad(range(10))
[range(0, 10)]

>>> from pymonad.list import ListMonad

>>> x = ListMonad(range(10))
>>> x
[range(0, 10)]
>>> x[0]
range(0, 10)
>>> list(x[0])
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
"""

from collections.abc import Iterator
from pymonad.tools import curry


@curry(1)  # type: ignore[misc]
def range1n(n: int) -> range:
    if n == 0:
        return range(1, 2)  # Only the value 1
    return range(1, n + 1)


from pymonad.tools import curry


@curry(1)  # type: ignore[misc]
def n21(n: int) -> int:
    return 2 * n + 1


REPL_composition = """
>>> from pymonad.reader import Compose
>>> from pymonad.list import ListMonad

>>> fact = Compose(range1n).then(prod)
>>> seq1 = ListMonad(*range(20))

>>> f1 = seq1.map(fact)
>>> f1[:10]
[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

>>> fact(1)
1
>>> fact(2)
2
>>> fact(3)
6
>>> fact(1)
1

>>> semi_fact = Compose(alt_range).then(prod)
>>> f2 = seq1.map(n21).then(semi_fact)
>>> f2[:10]
[1, 3, 15, 105, 945, 10395, 135135, 2027025, 34459425, 654729075]

>>> semi_fact(9)
945
>>> semi_fact(1)
1
>>> semi_fact(2)
2
>>> semi_fact(3)
3
>>> semi_fact(4)
8
>>> semi_fact(5)
15
>>> semi_fact(0)
1

>>> import operator
>>> 2 * sum(map(operator.truediv, f1, f2))
3.1415919276751456
"""

REPL_functor = """
>>> from pymonad.maybe import Maybe, Just, Nothing
>>> x1 = Maybe.apply(systolic_bp).to_arguments(Just(25), Just(50), Just(1), Just(0))
>>> x1.value
116.09
>>> x2 = Maybe.apply(systolic_bp).to_arguments(Just(25), Just(50), Just(1), Nothing)
>>> x2.value is None
True

>>> pi = lambda: 3.14
>>> pi()
3.14
"""

REPL_functor2 = """
>>> from pymonad.reader import Compose
>>> from pymonad.list import ListMonad

>>> fact = Compose(range1n).then(prod)
>>> seq1 = ListMonad(*range(20))

>>> f1 = seq1.map(fact)
>>> f1[:10]
[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

>>> semi_fact = Compose(alt_range).then(prod)
>>> f2 = seq1.map(n21).then(semi_fact)
>>> f2[:10]
[1, 3, 15, 105, 945, 10395, 135135, 2027025, 34459425, 654729075]

>>> import operator
>>> 2 * sum(map(operator.truediv, f1, f2))
3.1415919276751456

>>> 2*sum(map(operator.truediv, f1, f2))
3.1415919276751456

>>> from pymonad.maybe import Maybe, Just, Nothing
>>> r = Just(3).map(fact)
>>> r
Just 6
>>> r.value
6
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
