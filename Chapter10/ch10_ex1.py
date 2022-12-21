"""Functional Python Programming 3e

Chapter 10, Example Set 1
"""


def fib(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


def test_fib() -> None:
    assert fib(20) == 6765
    assert fib(1) == 1


from functools import lru_cache


@lru_cache(128)
def fibc(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibc(n - 1) + fibc(n - 2)


def test_fibc() -> None:
    assert fibc(20) == 6765
    assert fibc(1) == 1


def performance_fib() -> None:
    from textwrap import dedent
    import timeit

    naive_time = timeit.timeit(
        """fib(20)""", setup="""from Chapter10.ch10_ex1 import fib""", number=1000
    )

    cached_time = timeit.timeit(
        """fibc(20); fibc.cache_clear()""",
        setup="""from Chapter10.ch10_ex1 import fibc""",
        number=1000,
    )

    print(f"Naive {naive_time:.3f}")
    print(f"Cached {cached_time:.3f}")


def nfact(n: int) -> int:
    if n == 0:
        return 1
    return n * nfact(n - 1)


def test_nfact() -> None:
    assert nfact(5) == 120


@lru_cache(maxsize=128)
def cfact(n: int) -> int:
    if n == 0:
        return 1
    return n * cfact(n - 1)


def test_cfact() -> None:
    assert cfact(5) == 120


from collections.abc import Callable


def binom(p: int, r: int, fact: Callable[[int], int]) -> int:
    return fact(p) // (fact(r) * fact(p - r))


def test_binom() -> None:
    assert nfact(5) == 120
    assert binom(52, 5, nfact) == 2598960
    assert binom(52, 5, cfact) == 2598960


def performance_fact() -> None:
    import timeit

    naive_time = timeit.timeit(
        """binom(52, 5, nfact)""",
        setup="""from Chapter10.ch10_ex1 import binom, nfact""",
        number=10000,
    )

    cached_time = timeit.timeit(
        """binom(52, 5, cfact)""",
        setup="""from Chapter10.ch10_ex1 import binom, cfact""",
        number=10000,
    )

    cached_with_clear_time = timeit.timeit(
        """binom(52, 5, cfact); cfact.cache_clear()""",
        setup="""from Chapter10.ch10_ex1 import binom, cfact""",
        number=10000,
    )
    print(f"Naive Factorial {naive_time:.3f}")
    print(f"Cached Factorial, Dirty {cached_time:.3f}")
    print(f"Cached Factorial, Cleared {cached_with_clear_time:.3f}")


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}

if __name__ == "__main__":
    performance_fib()
    performance_fact()
