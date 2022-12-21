"""Functional Python Programming 3e

Chapter 7, Example Set 5
"""
from typing import NamedTuple, Type
from dataclasses import dataclass

import sys
import gc

from typing import NamedTuple


class LargeNT(NamedTuple):
    a: str
    b: int
    c: float
    d: complex


@dataclass(frozen=True)
class LargeDC:
    a: str
    b: int
    c: float
    d: complex


@dataclass(frozen=True, slots=True)
class LargeDC_Slots:
    a: str
    b: int
    c: float
    d: complex


from typing import Type, Any


def sizing(obj_type: Type[Any]) -> None:
    big_sequence = [
        obj_type(f"Hello, {i}", 42 * i, 3.1415926 * i, i + 2j) for i in range(1_000_000)
    ]
    sys._clear_type_cache()
    gc.collect()
    print(f"{obj_type.__name__} {sys.getallocatedblocks()}")
    del big_sequence


def baseline(context: str) -> None:
    sys._clear_type_cache()
    gc.collect()
    print(f"{context:4s} {sys.getallocatedblocks()}")


if __name__ == "__main__":
    baseline("pre")
    sizing(LargeNT)
    sizing(LargeDC)
    sizing(LargeDC_Slots)
    baseline("post")
