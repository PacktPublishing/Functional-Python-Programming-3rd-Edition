"""Functional Python Programming 3e

Chapter 13, Example Set 2
"""
from pymonad.tools import curry  # type: ignore[import]
from pymonad.maybe import Maybe, Just, Nothing  # type: ignore[import]
from pymonad.list import ListMonad  # type: ignore[import]
from pymonad.reader import Compose  # type: ignore[import]
from pymonad.io import IO  # type: ignore[import]
from pathlib import Path


@curry(2)  # type: ignore[misc]
def skip_header(source: IO, data: Maybe) -> Maybe:
    l_0 = source.run().rstrip()
    # print(l_0)  # Anscombe's quartet
    l_1 = source.run().rstrip()
    # print(l_1)  # I	II	III	IV
    l_2 = source.run().rstrip()
    # print(l_2)  # x	y	x	y	x	y	x	y
    return data


@curry(2)  # type: ignore[misc]
def read_rest(source: IO, data: Maybe) -> Maybe:
    txt = source.run().rstrip()
    if txt:
        row = ListMonad(*txt.split("\t")).then(float)
        return Just(data + [row]).then(read_rest(source))
    else:
        return data


def anscombe() -> Maybe:
    source_path = Path("Anscombe.txt")
    with source_path.open() as source:
        io = IO(source.readline)
        data = Just([]).then(skip_header(io)).then(read_rest(io))
    return data


def test_anscome_parser() -> None:
    d = anscombe()
    print(f"{d=}")
    print(f"{type(d)=}")
    print(f"{d.value[0]=}")
    print(f"{type(d.value[0])=}")
    assert d.value[0].value == [10.0, 8.04, 10.0, 9.14, 10.0, 7.46, 8.0, 6.58]
    assert d.value[-1].value == [5.0, 5.68, 5.0, 4.74, 5.0, 5.73, 8.0, 6.89]


import random


def rng() -> tuple[int, int]:
    return (random.randint(1, 6), random.randint(1, 6))


from collections.abc import Callable
from typing import TypeAlias

DiceT: TypeAlias = Callable[[], tuple[int, int]]

from pymonad.tools import curry
from pymonad.maybe import Maybe, Just


@curry(2)  # type: ignore[misc]
def initial_roll(dice: DiceT, status: Maybe) -> Maybe:
    d = dice()
    if sum(d) in (7, 11):
        return Just(("pass", sum(d), [d]))
    elif sum(d) in (2, 3, 12):
        return Just(("fail", sum(d), [d]))
    else:
        return Just(("point", sum(d), [d]))


from pymonad.tools import curry
from pymonad.maybe import Maybe, Just


@curry(2)  # type: ignore[misc]
def point_roll(dice: DiceT, status: Maybe) -> Maybe:
    prev, point, so_far = status
    if prev != "point":
        # won or lost on a previous throw
        return Just(status)

    d = dice()
    if sum(d) == 7:
        return Just(("fail", point, so_far + [d]))
    elif sum(d) == point:
        return Just(("pass", point, so_far + [d]))
    else:
        return Just(("point", point, so_far + [d])).then(point_roll(dice))


from pymonad.maybe import Maybe, Just


def game_chain(dice: DiceT) -> Maybe:
    outcome = Just(("", 0, [])).then(initial_roll(dice)).then(point_roll(dice))
    return outcome


from unittest.mock import Mock


def test_game_win() -> None:
    dice = Mock(side_effect=[(3, 4)])
    r = game_chain(dice)
    assert r.value == ("pass", 7, [(3, 4)])


def test_game_point_win() -> None:
    dice = Mock(side_effect=[(3, 3), (2, 2), (3, 3)])
    r = game_chain(dice)
    assert r.value == ("pass", 6, [(3, 3), (2, 2), (3, 3)])
