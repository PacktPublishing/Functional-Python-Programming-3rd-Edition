"""Functional Python Programming 3e

Chapter 5, Example Set 2
"""
import dis
from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar, cast

T_ = TypeVar("T_")


def mapping1(f: Callable[[T_], T_], C: Iterable[T_]) -> Iterator[T_]:
    return (f(a) for a in C)


def mapping2(f: Callable[[T_], T_], C: Iterable[T_]) -> Iterator[T_]:
    for a in C:
        yield f(a)


def test_mapping() -> None:
    expected = [
        1,
        2,
        4,
        8,
        16,
        32,
        64,
        128,
        256,
        512,
        1024,
        2048,
        4096,
        8192,
        16384,
        32768,
        65536,
        131072,
        262144,
        524288,
        1048576,
        2097152,
        4194304,
        8388608,
        16777216,
        33554432,
        67108864,
        134217728,
        268435456,
        536870912,
        1073741824,
        2147483648,
    ]
    transform: Callable[[int], int] = lambda x: cast(int, 2**x)
    assert list(mapping1(transform, range(32))) == expected
    assert list(mapping2(transform, range(32))) == expected


def performance() -> None:
    import timeit
    from textwrap import dedent

    print("Generator Expression Bytecode")
    dis.dis(mapping1)

    print("Generator Function Bytecode")
    dis.dis(mapping2)

    expr_time = timeit.timeit(
        """list(mapping1(lambda x: 2**x, range(32)))""",
        dedent(
            """
            def mapping1(f, C):
                return (f(a) for a in C)
        """
        ),
        number=200_000,
    )

    function_time = timeit.timeit(
        """list(mapping2(lambda x: 2**x, range(32)))""",
        dedent(
            """
            def mapping2(f, C):
                for a in C:
                   yield f(a)
        """
        ),
        number=200_000,
    )

    print(f"{expr_time=:.4f}")
    print(f"{function_time=:.4f}")


if __name__ == "__main__":
    performance()
