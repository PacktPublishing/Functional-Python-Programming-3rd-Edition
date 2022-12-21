"""Functional Python Programming 3e

Chapter 11, Example Set 1
"""

from collections.abc import Iterable
from functools import reduce


def prod(data: Iterable[int]) -> int:
    """
    >>> prod((1,2,3))
    6
    """
    return reduce(lambda x, y: x * y, data, 1)


year_cheese = [
    (2000, 29.87),
    (2001, 30.12),
    (2002, 30.6),
    (2003, 30.66),
    (2004, 31.33),
    (2005, 32.62),
    (2006, 32.73),
    (2007, 33.5),
    (2008, 32.84),
    (2009, 33.02),
    (2010, 32.92),
]
#
#
#
#
# REPL_itemgetter = """
#
#
# >>> from operator import itemgetter
# >>> itemgetter(0)([1, 2, 3])
# 1
#
#
#
# >>> min(year_cheese, key=snd)
# (2000, 29.87)
# >>> max(year_cheese, key=itemgetter(1))
# (2007, 33.5)
#
#
#
#
# """
#
#
#
# REPL_year_cheese = """
#
#
# >>> year_cheese_2 = list(YearCheese(*yc) for yc in year_cheese)
#
#
#
# >>> year_cheese_2  # doctest: +NORMALIZE_WHITESPACE
# [YearCheese(year=2000, cheese=29.87), YearCheese(year=2001, cheese=30.12),
#  YearCheese(year=2002, cheese=30.6), YearCheese(year=2003, cheese=30.66),
#  YearCheese(year=2004, cheese=31.33), YearCheese(year=2005, cheese=32.62),
#  YearCheese(year=2006, cheese=32.73), YearCheese(year=2007, cheese=33.5),
#  YearCheese(year=2008, cheese=32.84), YearCheese(year=2009, cheese=33.02),
#  YearCheese(year=2010, cheese=32.92)]
#
# >>> from operator import attrgetter
# >>> min(year_cheese_2, key=attrgetter('cheese'))
# YearCheese(year=2000, cheese=29.87)
# >>> max(year_cheese_2, key=lambda x: x.cheese )
# YearCheese(year=2007, cheese=33.5)
# """

g_f = [
    1,
    1 / 12,
    1 / 288,
    -139 / 51840,
    -571 / 2488320,
    163879 / 209018880,
    5246819 / 75246796800,
]

g = [
    (1, 1),
    (1, 12),
    (1, 288),
    (-139, 51840),
    (-571, 2488320),
    (163879, 209018880),
    (5246819, 75246796800),
]


REPL_starmap1 = """
>>> from itertools import starmap
>>> from fractions import Fraction
>>> from operator import truediv

>>> round(sum(starmap(truediv, g)), 6)
1.084749
>>> round(sum(g_f), 6)
1.084749
>>> f = sum(Fraction(*x) for x in g)
>>> f
Fraction(81623851739, 75246796800)
>>> round(float(f), 6)
1.084749
"""

REPL_starmap_d = """
>>> from itertools import starmap, zip_longest
>>> d = starmap(pow, zip_longest([], range(4), fillvalue=60))
>>> list(d)
[1, 60, 3600, 216000]
"""

REPL_starmap2 = """
>>> from operator import truediv
>>> from itertools import starmap, zip_longest

>>> d = starmap(pow, zip_longest([], range(4), fillvalue=60))
>>> p = (3, 8, 29, 44)
>>> pi = sum(starmap(truediv, zip(p, d)))
>>> pi
3.1415925925925925

>>> d = starmap(pow, zip_longest([], range(4), fillvalue=60))
>>> p = (3, 8, 29, 44)
>>> pi = sum(starmap(truediv, zip(p, d)))
>>> pi
3.1415925925925925

>>> d = starmap(pow, zip_longest([], range(4), fillvalue=60))
>>> pi = sum(map(truediv, p, d))
>>> pi
3.1415925925925925

>>> d = starmap(pow, zip_longest([], range(4), fillvalue=60))
>>> pi = sum(map(truediv, p, d))
>>> pi
3.1415925925925925
"""


REPL_starmap3 = """
>>> from itertools import starmap
>>> from itertools import count, takewhile
>>> from operator import truediv

>>> from Chapter06.ch06_ex1 import fact
>>> from itertools import count, takewhile
>>> num = map(fact, count())
>>> den = map(semifact, (2*n+1 for n in count()))

>>> terms = takewhile(
... lambda t: t > 1E-10, map(truediv, num, den))

>>> round(float(2*sum(terms)), 8)
3.14159265

>>> num = map(fact, count())
>>> den = map(semifact, (2*n+1 for n in count()))
>>> terms = takewhile(
...     lambda t: t > 1E-10, map(truediv, num, den))
>>> round(float(2*sum(terms)), 8)
3.14159265
"""


def semifact(n: int) -> int:
    match n:
        case 0 | 1:
            return 1
        case 2:
            return 2
        case _:
            return semifact(n - 2) * n


def test_semifact() -> None:
    assert semifact(0) == 1
    assert semifact(1) == 1
    assert semifact(2) == 2
    assert semifact(3) == 3
    assert semifact(4) == 8
    assert semifact(5) == 15
    assert semifact(9) == 945


REPL_reduction = """
>>> import functools, operator
>>> sum=  functools.partial(functools.reduce, operator.add)
>>> sum([1,2,3])
6
>>> prod = functools.partial(functools.reduce, operator.mul)
>>> prod( [1,2,3,4] )
24
>>> fact = lambda n: 1 if n < 2 else n*prod(range(1,n))
>>> fact(4)
24
>>> fact(0)
1
>>> fact(1)
1
"""

REPL_unordered = """
>>> {'a': 1, 'a': 2}
{'a': 2}
"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
