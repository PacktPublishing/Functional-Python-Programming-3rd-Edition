"""Functional Python Programming 3e

Chapter 10, Example Set 2
"""

from typing import NamedTuple


class Card1(NamedTuple):
    rank: int
    suit: str


REPL_card1 = """
>>> c2s = Card1(2, '\u2660')
>>> c2h = Card1(2, '\u2665')
>>> c2s
Card1(rank=2, suit='♠')
>>> c2h
Card1(rank=2, suit='♥')

Undesirable for some games:

>>> c2h == c2s
False

>>> c2s= Card1(2, '\u2660')
>>> c2s.rank
2
>>> c2s.suit
'\u2660'
>>> c2s
Card1(rank=2, suit='♠')
>>> len(c2s)
2

This is *incorrect* behavior for games where
rank is the only relevant attribute

>>> c2h= Card1(2, '\u2665')
>>> c2h == c2s
False
>>> "{0}== {1}: {2}".format( c2s, c2h, c2h == c2s )
"Card1(rank=2, suit='♠')== Card1(rank=2, suit='♥'): False"
"""

from collections.abc import Iterable
from functools import total_ordering
from typing import Union, Any, cast, TypeAlias

CardInt: TypeAlias = Union["Card", int]


@total_ordering
class Card(tuple[str, int]):
    """Rank-only comparisons."""

    Suits = "\u2660", "\u2665", "\u2666", "\u2663"
    __slots__ = ()

    def __new__(cls, rank: int, suit: str) -> "Card":
        obj = super().__new__(
            Card,
            cast(
                Iterable[Any],
                [
                    suit,
                    rank,
                ],
            ),
        )
        return obj

    def __str__(self) -> str:
        return f"{self.rank:2d}{self.suit}"

    @property
    def rank(self) -> int:
        return self[1]

    @property
    def suit(self) -> str:
        return self[0]

    def __eq__(self, other: Any) -> bool:
        match other:
            case Card():
                return self.rank == cast(Card, other).rank
            case int():
                return self.rank == other
            case _:
                return NotImplemented

    def __lt__(self, other: Any) -> bool:
        match other:
            case Card():
                return self.rank < cast(Card, other).rank
            case int():
                return self.rank < other
            case _:
                return NotImplemented


def test_card() -> None:
    c2s = Card(2, "\u2660")
    c2h = Card(2, "\u2665")
    assert c2s == c2h
    assert c2s == 2
    assert 2 == c2s


REPL_eq = """
>>> c2s = Card(2, '\u2660')
>>> c2s.rank
2
>>> c2s.suit
'♠'
>>> c2s
('♠', 2)
>>> len(c2s)
2

This is correct behavior for games where
rank is the only relevant attribute

>>> c2h = Card(2, '\u2665')
>>> c2h == c2s
True
>>> "{0} == {1}: {2}".format(c2s, c2h, c2h == c2s)
' 2♠ ==  2♥: True'
>>> c2h == 2
True
>>> 2 == c2h
True
"""

REPL_order = """
>>> c2s = Card(2, '\u2660')
>>> c3h = Card(3, '\u2665')
>>> c4c = Card(4, '\u2663')
>>> c2s <= c3h < c4c
True
>>> c3h >= c3h
True
>>> c3h > c2s
True
>>> c4c != c2s
True
"""

REPL_extra_comparisons = """
These don't work, the logic doesn't fit with total_ordering.

>>> c4c = Card(4, '\u2663')
>>> try:
...     print("c4c > 3", c4c > 3)
... except TypeError as e:
...     print(e)
'>' not supported between instances of 'Card' and 'int'
>>> try:
...     print("3 < c4c", 3 < c4c)
... except TypeError as e:
...     print(e)
'<' not supported between instances of 'int' and 'Card'
"""

from functools import total_ordering


@total_ordering
class Card2(NamedTuple):
    rank: int
    suit: str

    def __str__(self) -> str:
        return f"{self.rank:2d}{self.suit}"

    def __eq__(self, other: Any) -> bool:
        match other:
            case Card2():
                return self.rank == other.rank
            case int():
                return self.rank == other
            case _:
                return NotImplemented

    def __lt__(self, other: Any) -> bool:
        match other:
            case Card2():
                return self.rank < other.rank
            case int():
                return self.rank < other
            case _:
                return NotImplemented


def test_card2() -> None:
    c2s = Card2(2, "\u2660")
    c2h = Card2(2, "\u2665")
    assert c2s == c2h
    assert c2s == 2
    assert 2 == c2s


REPL_eq_2 = """
>>> c2s = Card2(2, '\u2660')
>>> c2s.rank
2
>>> c2s.suit
'\u2660'
>>> c2s
Card2(rank=2, suit='\u2660')
>>> len(c2s)
2

This is correct behavior for games where
rank is the only relevant attribute

>>> c2s = Card2(2, '\u2660')
>>> c2h = Card2(2, '\u2665')
>>> c2h == c2s
True

>>> c2h == 2
True
>>> 2 == c2h
True

>>> c2h = Card2(2, '\u2665')
>>> c2h == c2s
True

>>> c2h == 2
True
>>> 2 == c2h
True
"""

REPL_order_2 = """
>>> c2s = Card2(2, '\u2660')
>>> c3h = Card2(3, '\u2665')
>>> c4c = Card2(4, '\u2663')
>>> c2s <= c3h < c4c
True

>>> c2s = Card2(2, '\u2660')
>>> c3h = Card2(3, '\u2665')
>>> c4c = Card2(4, '\u2663')
>>> c2s <= c3h < c4c
True
>>> c3h >= c3h
True
>>> c3h > c2s
True
>>> c4c != c2s
True
"""

REPL_extra_comparisons_2 = """
These don't work, the logic doesn't fit with total_ordering.

>>> c4c = Card2(4, '\u2663')
>>> try:
...     print("c4c > 3", c4c > 3)
... except TypeError as e:
...     print(e)
'>' not supported between instances of 'Card2' and 'int'
>>> try:
...     print("3 < c4c", 3 < c4c)
... except TypeError as e:
...     print(e)
'<' not supported between instances of 'int' and 'Card2'
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
