"""Functional Python Programming 3e

Chapter 6, Example Set 1
"""
import sys


def add(a: int, b: int) -> int:
    if a == 0:
        return b
    else:
        return add(a - 1, b + 1)


def test_add() -> None:
    assert add(3, 5) == 8


def fact(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)


def test_fact() -> None:
    assert fact(0) == 1
    assert fact(1) == 1
    assert fact(7) == 5040


def facti(n: int) -> int:
    if n == 0:
        return 1
    f = 1
    for i in range(2, n + 1):
        f = f * i
    return f


def test_facti() -> None:
    assert facti(0) == 1
    assert facti(1) == 1
    assert facti(2) == 2
    assert facti(3) == 6
    assert facti(4) == 24
    assert facti(7) == 5040
    from math import factorial

    assert facti(1000) == factorial(1000)
    assert facti(2000) == factorial(2000)
    if sys.version_info.minor > 10:
        sys.set_int_max_str_digits(6000)  # type: ignore [attr-defined]
    assert len(str(facti(2000))) == 5736


from collections import deque


def fasts(n: int) -> int:
    # Establish pending work
    pending: deque[int] = deque()
    while n != 0:
        pending.append(n)
        n = n - 1
    # Complete the pending work
    r = 1
    while pending:
        r *= pending.pop()
    return r


def test_facts() -> None:
    assert fasts(0) == 1
    assert fasts(1) == 1
    assert fasts(2) == 2
    assert fasts(3) == 6
    assert fasts(4) == 24
    assert fasts(7) == 5040
    from math import factorial

    assert fasts(1000) == factorial(1000)
    assert fasts(2000) == factorial(2000)
    if sys.version_info.minor > 10:
        sys.set_int_max_str_digits(6000)  # type: ignore [attr-defined]
    assert len(str(fasts(2000))) == 5736


from collections import deque
from pathlib import Path


def all_print(start: Path) -> int:
    count = 0
    pending: deque[Path] = deque([start])
    while pending:
        dir_path = pending.pop()
        for path in dir_path.iterdir():
            if path.is_file():
                if path.suffix == ".py":
                    count += path.read_text().count("print")
            elif path.is_dir():
                if not path.stem.startswith("."):
                    pending.append(path)
            else:  # Ignore other filesystem objects
                pass
    return count


def test_all_print() -> None:
    from pathlib import Path

    assert all_print(Path.cwd()) == 232  # Depends on EXACT code content -- very fiddly


def fastexp(a: float, n: int) -> float:
    if n == 0:
        return 1
    elif n % 2 == 1:
        return a * fastexp(a, n - 1)
    else:
        t = fastexp(a, n // 2)
        return t * t


def test_fastexp() -> None:
    assert fastexp(3, 11) == 177147
    assert fastexp(2, 20) == 1048576


def fib(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


def test_fib() -> None:
    assert fib(20) == 6765
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5


def fibi(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    f_n2, f_n1 = 1, 1
    for _ in range(2, n):
        f_n2, f_n1 = f_n1, f_n2 + f_n1
    return f_n1


def test_fibi() -> None:
    assert fibi(20) == 6765
    assert fibi(0) == 0
    assert fibi(1) == 1
    assert fibi(2) == 1
    assert fibi(3) == 2
    assert fibi(4) == 3
    assert fibi(5) == 5


def fibi2(n: int) -> int:
    f = [0, 1] + [0 for _ in range(2, n + 1)]
    for i in range(2, n + 1):
        f[i] = f[i - 1] + f[i - 2]
    return f[n]


def test_fibi2() -> None:
    assert fibi2(20) == 6765
    assert fibi2(0) == 0
    assert fibi2(1) == 1
    assert fibi2(2) == 1
    assert fibi2(3) == 2
    assert fibi2(4) == 3
    assert fibi2(5) == 5


from collections.abc import Callable, Sequence
from typing import Any, TypeVar

MapD = TypeVar("MapD")
MapR = TypeVar("MapR")


def mapr(f: Callable[[MapD], MapR], collection: Sequence[MapD]) -> list[MapR]:
    if len(collection) == 0:
        return []
    return mapr(f, collection[:-1]) + [f(collection[-1])]


from typing import cast


def test_mapr() -> None:
    assert mapr(lambda x: cast(int, 2**x), [0, 1, 2, 3, 4]) == [1, 2, 4, 8, 16]


from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar

DomT = TypeVar("DomT")
RngT = TypeVar("RngT")


def mapf(f: Callable[[DomT], RngT], C: Iterable[DomT]) -> Iterator[RngT]:
    return (f(x) for x in C)


def test_mapf() -> None:
    assert list(mapf(lambda x: cast(int, 2**x), [0, 1, 2, 3, 4])) == [1, 2, 4, 8, 16]


def mapg(f: Callable[[DomT], RngT], C: Iterable[DomT]) -> Iterator[RngT]:
    for x in C:
        yield f(x)


def test_mapg() -> None:
    assert list(mapg(lambda x: cast(int, 2**x), [0, 1, 2, 3, 4])) == [1, 2, 4, 8, 16]


REPL_test_mapg = """
>>> list(mapg(lambda x: 2 ** x, [0, 1, 2, 3, 4]))
[1, 2, 4, 8, 16]
"""


def fastexp_w(a: float, n: int) -> float:
    if n == 0:
        return 1
    else:
        q, r = divmod(n, 2)
        if r == 1:
            return a * fastexp_w(a, n - 1)
        else:
            return (t := fastexp_w(a, q)) * t


def test_fastexp_w() -> None:
    assert fastexp_w(3, 11) == 177147
    assert fastexp_w(2, 20) == 1048576


from collections.abc import Sequence


def prodrc(collection: Sequence[float]) -> float:
    if len(collection) == 0:
        return 1
    return collection[0] * prodrc(collection[1:])


def test_prod_rc() -> None:
    assert prodrc([1, 2, 3, 4, 5, 6, 7]) == 5040


from collections.abc import Iterator


def prodri(items: Iterator[float]) -> float:
    try:
        head = next(items)
    except StopIteration:
        return 1
    return head * prodri(items)


def test_prod_ri() -> None:
    assert prodri(iter([1, 2, 3, 4, 5, 6, 7])) == 5040


REPL_prod_ri = """
>>> prodri(iter([1,2,3,4,5,6,7]))
5040
"""

from collections.abc import Iterable


def prodi(items: Iterable[float]) -> float:
    p: float = 1
    for n in items:
        p *= n
    return p


def test_prod_i() -> None:
    assert prodi(iter([1, 2, 3, 4, 5, 6, 7])) == 5040


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
