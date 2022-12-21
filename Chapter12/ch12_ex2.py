"""Functional Python Programming 3e

Chapter 12, Example Set 2
"""
from collections.abc import Callable
from functools import wraps
from typing import cast, TypeVar, TypeAlias

IntFuncT: TypeAlias = Callable[[int], int]
DFT = TypeVar("DFT", bound=IntFuncT)


def compose(func1: DFT) -> Callable[[DFT], DFT]:
    def concrete_decorator(func2: DFT) -> DFT:
        @wraps(func2)
        def composite(arg: int) -> int:
            return func1(func2(arg))

        return cast(DFT, composite)

    return concrete_decorator


def minus1(x: int) -> int:
    return x - 1


@compose(minus1)
def pow2(x: int) -> int:
    return cast(int, 2**x)


# Note the obscure name. This creates a Mersenne prime, but it's called pow2

REPL_example_1 = """
>>> pow2(17)
131071
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
