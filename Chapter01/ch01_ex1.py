"""Functional Python Programming 3e

Chapter 1, Example Set 1
"""


def sum_numeric(limit: int = 10) -> int:
    s = 0
    for n in range(1, limit):
        if n % 3 == 0 or n % 5 == 0:
            s += n
    return s


def test_sum_numeric() -> None:
    assert sum_numeric() == 23


def sum_object_light(limit: int = 10) -> int:
    m: list[int] = list()
    for n in range(1, limit):
        if n % 3 == 0 or n % 5 == 0:
            m.append(n)
    return sum(m)


def test_some_object_light() -> None:
    assert sum_object_light() == 23


class Summable_List(list[int]):
    def sum(self) -> int:
        s = 0
        for v in self:
            s += v
        return s


def sum_full_oo(limit: int = 10) -> int:
    m = Summable_List()
    for n in range(1, 10):
        if n % 3 == 0 or n % 5 == 0:
            m.append(n)
    return m.sum()


def test_full_oo() -> None:
    assert sum_full_oo() == 23


from collections.abc import Sequence, Callable


def foldr(seq: Sequence[int], op: Callable[[int, int], int], init: int) -> int:
    """Recursive reduce operation, fold from right to left."""
    if len(seq) == 0:
        return init
    return op(seq[0], foldr(seq[1:], op, init))


def test_foldr() -> None:
    assert foldr([2, 3, 5, 7], lambda x, y: x + y, 0) == 17
    assert foldr([1, 2, 3, 4], lambda x, y: x * y, 1) == 24


from collections.abc import Sequence


def sumr(seq: Sequence[int]) -> int:
    if len(seq) == 0:
        return 0
    return seq[0] + sumr(seq[1:])


REPL_sumr = """
>>> sumr([7, 11])
18
>>> sumr([11])
11
>>> sumr([])
0
"""


from collections.abc import Sequence, Callable


def until(limit: int, filter_func: Callable[[int], bool], v: int) -> list[int]:
    if v == limit:
        return []
    elif filter_func(v):
        return [v] + until(limit, filter_func, v + 1)
    else:
        return until(limit, filter_func, v + 1)


def test_until() -> None:
    assert list(filter(lambda x: x % 3 == 0 or x % 5 == 0, range(10))) == [
        0,
        3,
        5,
        6,
        9,
    ]
    assert until(10, lambda x: x % 3 == 0 or x % 5 == 0, 0) == [0, 3, 5, 6, 9]


def mult_3_5(x: int) -> bool:
    return x % 3 == 0 or x % 5 == 0


REPL_until = """
>>> until(10, mult_3_5, 0)
[0, 3, 5, 6, 9]
"""


def sum_functional_1(limit: int = 10) -> int:
    mult_3_5 = lambda x: x % 3 == 0 or x % 5 == 0
    add = lambda x, y: x + y
    return foldr(until(limit, mult_3_5, 0), add, 0)


def sum_functional(limit: int = 10) -> int:
    return sumr(until(limit, mult_3_5, 0))


def test_sum_functional() -> None:
    assert sum_functional_1() == 23
    assert sum_functional() == 23


def sum_hybrid(limit: int = 10) -> int:
    return sum(n for n in range(1, limit) if n % 3 == 0 or n % 5 == 0)


def test_sum_hybrid() -> None:
    assert sum_hybrid() == 23


REPL_generator = """
>>> sum(
...     n for n in range(1, 10) 
...     if n % 3 == 0 or n % 5 == 0
... )
23
>>> n
Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
NameError: name 'n' is not defined
"""


def folding() -> None:
    """Performance differences from folding left or folding right.

    >>> 1+2+3+4
    10
    >>> ((1+2)+3)+4
    10
    >>> 1+(2+(3+4))
    10

    >>> ((([]+[1])+[2])+[3])+[4]
    [1, 2, 3, 4]
    >>> []+([1]+([2]+([3]+[4])))
    [1, 2, 3, 4]
    """
    import timeit

    # Short lists
    foldl = timeit.timeit("((([]+[1])+[2])+[3])+[4]")
    foldr = timeit.timeit("[]+([1]+([2]+([3]+[4])))")
    print(f"{foldl=:.3f}")
    print(f"{foldr=:.3f}")

    # Long lists. Stack limits us to 1,000
    from textwrap import dedent

    left_def = dedent(
        """
        def foldleft(n):
            if n == 0: return []
            return foldleft(n-1) + [n]
    """
    )
    foldl = timeit.timeit("foldleft(500)", setup=left_def, number=2000)
    right_def = dedent(
        """
        def foldright(n, v=1):
            if v == n: return [v]
            return [v] + foldright(n, v+1)
    """
    )
    foldr = timeit.timeit("foldright(500)", setup=right_def, number=2000)
    print(f"{foldl=:.3f}")
    print(f"{foldr=:.3f}")


def foldleft(n: int) -> list[int]:
    if n == 0:
        return []
    return foldleft(n - 1) + [n]


def foldright(n: int, v: int = 1) -> list[int]:
    if v == n:
        return [v]
    return [v] + foldright(n, v + 1)


def test_fold_left_right() -> None:
    assert foldleft(4) == foldright(4)
    assert foldleft(4) == [1, 2, 3, 4]


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}

if __name__ == "__main__":
    folding()
