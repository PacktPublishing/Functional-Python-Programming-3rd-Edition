"""Functional Python Programming 3e

Chapter 2, Example Set 1
"""

REPL_function_as_object = """
>>> def example(a, b, **kw):
...     return a*b
...
>>> type(example)
<class 'function'>
>>> example.__code__.co_varnames
('a', 'b', 'kw')
>>> example.__code__.co_argcount
2
"""

REPL_lambda = """
>>> mersenne = lambda x: 2 ** x - 1
>>> mersenne(17)
131071
"""

REPL_lambda_side_effect = """
>>> default_zip = lambda row: row.setdefault('ZIP', '00000')

>>> r_0 = {'CITY': 'Vaca Key'}
>>> default_zip(r_0)
'00000'
>>> r_0
{'CITY': 'Vaca Key', 'ZIP': '00000'}

>>> r_1 = {'CITY': 'Asheville', 'ZIP': 27891}
>>> default_zip(r_1)
27891

"""


REPL_higher_order = """
>>> year_cheese = [(2000, 29.87), (2001, 30.12),
...     (2002, 30.6), (2003, 30.66), (2004, 31.33),
...     (2005, 32.62), (2006, 32.73), (2007, 33.5),
...     (2008, 32.84), (2009, 33.02), (2010, 32.92)]

>>> max(year_cheese)
(2010, 32.92)

>>> max(year_cheese, key=lambda yc: yc[1])
(2007, 33.5)

>>> max(map(lambda yc: (yc[1], yc), year_cheese))[1]
(2007, 33.5)

>>> snd = lambda x: x[1]
>>> snd(max(map(lambda yc: (yc[1], yc), year_cheese)))
(2007, 33.5)

"""


REPL_and_short_circuit = """
>>> 0 and print("right")
0

>>> True and print("right")
right
"""

from collections.abc import Iterator


def numbers(stop: int) -> Iterator[int]:
    for i in range(stop):
        print(f"{i=}")
        yield i


def sum_to(limit: int) -> int:
    sum: int = 0
    for i in numbers(1_024):
        if i == limit:
            break
        sum += i
    return sum


REPL_sum_to = """
>>> sum_to(5)
i=0
i=1
i=2
i=3
i=4
i=5
10
"""

# This is ex 4 a, but the interpolation become
# too complex, so it's a copy-and-poste
REPL_not_any_ex = """
>>> import math
>>> n = 97
>>> not any(
...     n % p == 0
...     for p in range(2, int(math.sqrt(n))+1)
... )
True
"""


def isprimer(n: int) -> bool:
    def iscoprime(k: int, a: int, b: int) -> bool:
        """Is k coprime with a value in the given range?"""
        if a == b:
            return True
        return (k % a != 0) and iscoprime(k, a + 1, b)

    return iscoprime(n, 2, int(math.sqrt(n)) + 1)


def test_isprimer() -> None:
    assert isprimer(2)
    assert tuple(isprimer(x) for x in range(3, 11)) == (
        True,
        False,
        True,
        False,
        True,
        False,
        False,
        False,
    )


def isprimei(n: int) -> bool:
    """Is n prime?"""
    if n < 2:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        for i in range(3, 1 + int(math.sqrt(n)), 2):
            if n % i == 0:
                return False
        return True


def test_isprimei() -> None:
    assert isprimei(2)
    assert tuple(isprimei(x) for x in range(3, 11)) == (
        True,
        False,
        True,
        False,
        True,
        False,
        False,
        False,
    )


REPL_test_isprimei = """

"""


def isprimeg(n: int) -> bool:
    """Is n prime?

    >>> isprimeg(2)
    True
    >>> tuple(isprimeg(x) for x in range(3,11))
    (True, False, True, False, True, False, False, False)

    Remarkably slow for large primes, for example, M_61=2**61-1.

    >>> isprimeg(62710593)
    False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return not any(n % p == 0 for p in range(3, int(math.sqrt(n)) + 1, 2))


def test_isprimeg() -> None:
    assert isprimeg(2)
    assert tuple(isprimeg(x) for x in range(3, 11)) == (
        True,
        False,
        True,
        False,
        True,
        False,
        False,
        False,
    )


import math


def isprimem(n: int) -> bool:
    match n:
        case _ if n < 2:
            prime = False
        case 2:
            prime = True
        case _ if n % 2 == 0:
            prime = False
        case _:
            for i in range(3, 1 + int(math.sqrt(n)), 2):
                if n % i == 0:
                    # Stop as soon as we know...
                    return False
            prime = True
    return prime


def test_isprimem() -> None:
    assert isprimem(2)
    assert tuple(isprimem(x) for x in range(3, 11)) == (
        True,
        False,
        True,
        False,
        True,
        False,
        False,
        False,
    )


def test_all_isprime() -> None:
    assert isprimei(131071)
    assert isprimer(131071)
    assert isprimeg(131071)
    assert isprimem(131071)


def namedtuples() -> None:
    """nametuple vs. class performance"""
    from textwrap import dedent
    import timeit

    class_time = timeit.timeit(
        dedent(
            """
            x= X(1,2,3)
        """
        ),
        dedent(
            """
            class X:
                def __init__(self, a, b, c):
                    self.a= a
                    self.b= b
                    self.c= c
        """
        ),
    )
    print(f"class {class_time:.4f}")

    tuple_time = timeit.timeit("""x = (1,2,3)""")
    print(f"tuple {tuple_time:.4f}")

    collections_nt_time = timeit.timeit(
        dedent(
            """
            x = X(1,2,3)
        """
        ),
        dedent(
            """
            from collections import namedtuple
            X = namedtuple("X", ("a", "b", "c"))
        """
        ),
    )
    print(f"namedtuple {collections_nt_time:.4f}")

    typing_nt_time = timeit.timeit(
        dedent(
            """
            x = X(1,2,3)
        """
        ),
        dedent(
            """
            from typing import NamedTuple
            class X(NamedTuple):
                a: str
                b: str
                c: str
        """
        ),
    )
    print(f"NamedTuple {typing_nt_time:.4f}")


def recursion() -> None:
    """Recursion Performance Comparison."""
    from textwrap import dedent
    import timeit

    isprimei_time = timeit.timeit(
        dedent(
            """
            isprimei(131071)
        """
        ),
        dedent(
            """
            import math
            def isprimei(n):
                if n < 2: return False
                if n == 2: return True
                if n % 2 == 0: return False
                for i in range(3,1+int(math.sqrt(n)),2):
                    if n % i == 0:
                        return False
                return True
        """
        ),
        number=100_000,
    )

    isprimer_time = timeit.timeit(
        dedent(
            """
            isprimer(131071)
        """
        ),
        dedent(
            """
            import math
            def isprimer(n: int) -> bool:
                def iscoprime(k: int, a: int, b: int) -> bool:
                    if a == b: return True
                    return (k % a != 0) and iscoprime(k, a+1, b)
                return iscoprime(n, 2, int(math.sqrt(n)) + 1)
        """
        ),
        number=100_000,
    )

    isprimeg_time = timeit.timeit(
        dedent(
            """
            isprimeg(131071)
        """
        ),
        dedent(
            """
            import math
            def isprimeg(n):
                if n < 2: return False
                if n == 2: return True
                if n % 2 == 0: return False
                return not any(n%p==0 for p in range(3,int(math.sqrt(n))+2))
        """
        ),
        number=100_000,
    )
    print(f"{isprimei_time=:.4f}")
    print(f"{isprimer_time=:.4f}")
    print(f"{isprimeg_time=:.4f}")


def limit_of_performance() -> None:
    """We can see that testing a large prime is
    quite slow. Testing large non-primes is quite fast.

    This can take over a minute to run.
    """
    import time

    t = time.perf_counter()
    for i in range(30, 89):
        m = 2 ** i - 1
        print(i, m, end=" ")
        if isprimeg(m):
            print("prime", end=" ")
        else:
            print("composite", end=" ")
        print(f"{time.perf_counter() - t:.4f}")


# from Chapter02.ch02_ex1 import isprimei
from functools import reduce
import time
from typing import TextIO

# Teasing some material from Chapter 4...


def strip_head(source: TextIO, line: str) -> tuple[TextIO, str]:
    if len(line.strip()) == 0:
        return source, source.readline()
    return strip_head(source, source.readline())


def get_columns(source: TextIO, line: str) -> Iterator[str]:
    if line.strip() == "end.":
        return
    yield line
    yield from get_columns(source, source.readline())


def parse_g(source: TextIO) -> Iterator[int]:
    return (
        int(number_text)
        for c in get_columns(*strip_head(source, source.readline()))
        for number_text in c.split()
    )


def performance() -> None:
    """
    Compare three kinds of generators

    Use :func:`isprimei` because it's fastest.
    """
    with open("1000.txt") as source:
        primes = list(parse_g(source))
    assert len(primes) == 1000

    start = time.perf_counter()
    for repeat in range(1000):
        assert all(isprimei(x) for x in primes)
    print(f"all() {time.perf_counter() - start:.3f}")

    start = time.perf_counter()
    for repeat in range(1000):
        assert not any(not isprimei(x) for x in primes)
    print(f"not any() {time.perf_counter() - start:.3f}")

    start = time.perf_counter()
    for repeat in range(1000):
        assert reduce(lambda x, y: x and y, (isprimei(x) for x in primes))
    print(f"reduce(and,...) {time.perf_counter() - start:.3f}")


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}

if __name__ == "__main__":
    namedtuples()
    recursion()
    # limit_of_performance()
