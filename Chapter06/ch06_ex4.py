"""Functional Python Programming 3e

Chapter 6, Example Set 4
"""
from pytest import CaptureFixture
from typing import Callable, Any, Iterator, cast


def syracuse(n: int) -> int:
    """The Syracuse function, central to the Collatz conjecture.

    >>> syracuse(6)
    3
    >>> syracuse(3)
    10
    >>> syracuse(10)
    5
    >>> syracuse(5)
    16
    >>> syracuse(16)
    8
    """
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def until(
    termination: Callable[[Any], bool], function: Callable[[int], int], seed: int
) -> Iterator[int]:
    """Evaluate until a termination condition is true

    >>> list( until(lambda x: x==1, syracuse, 13) )
    [13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    """
    yield seed
    if termination(seed):
        return
    else:
        yield from until(termination, function, function(seed))


def test_until(capsys: CaptureFixture[str]) -> None:
    from textwrap import dedent

    for i in range(1, 27):
        seq = list(until(lambda x: cast(bool, x == 1), syracuse, i))
        print(i, len(seq))

    out, err = capsys.readouterr()
    assert out == dedent(
        """\
        1 1
        2 2
        3 8
        4 3
        5 6
        6 9
        7 17
        8 4
        9 20
        10 7
        11 15
        12 10
        13 10
        14 18
        15 18
        16 5
        17 13
        18 21
        19 21
        20 8
        21 8
        22 16
        23 16
        24 11
        25 24
        26 11
        """
    )
