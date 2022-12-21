"""Functional Python Programming 3e

Chapter 7, Example Set 4
"""

from typing import NamedTuple, Any


class RankData(NamedTuple):
    rank_seq: tuple[float, ...]
    raw: Any


from typing import NamedTuple, Any


class Rank_Data(NamedTuple):
    rank_seq: tuple[float, ...]
    raw: Any


def test_rank_data_class() -> None:
    """
    Two similar variations:
    - Rank_Data((rank,), data) -- singleton ranking
    - Rank_Data((rank, rank), data) -- multiple ranking
    """

    data = {"key1": 1, "key2": 2}
    r = Rank_Data((2, 7), data)
    assert r.rank_seq[0] == 2
    assert r.raw == {"key1": 1, "key2": 2}


REPL_test_rank_data = """
>>> raw_data = {'key1': 1, 'key2': 2}
>>> r = RankData((2, 7), raw_data)
>>> r.rank_seq[0]
2
>>> r.raw
{'key1': 1, 'key2': 2}
"""

from collections.abc import Iterator, Iterable
from typing import Any, TypeVar

LL_Type = TypeVar("LL_Type")


def legs(lat_lon_iter: Iterator[LL_Type]) -> Iterator[tuple[LL_Type, LL_Type]]:
    begin = next(lat_lon_iter)
    for end in lat_lon_iter:
        yield begin, end
        begin = end


from collections.abc import Iterator, Iterable, Sequence
from typing import Any, TypeVar

# Defined earlier
# LL_Type = TypeVar('LL_Type')


def legs_g(
    lat_lon_src: Iterator[LL_Type] | Sequence[LL_Type],
) -> Iterator[tuple[LL_Type, LL_Type]]:
    if isinstance(lat_lon_src, Sequence):
        return legs_g(iter(lat_lon_src))
    elif isinstance(lat_lon_src, Iterator):
        begin = next(lat_lon_src)
        for end in lat_lon_src:
            yield begin, end
            begin = end
    else:
        raise TypeError("not an Iterator or Sequence")


from collections.abc import Sequence, Iterator, Iterable
from typing import Any, TypeVar

# Defined earlier
# LL_Type = TypeVar('LL_Type')


def legs_m(
    lat_lon_src: Iterator[LL_Type] | Sequence[LL_Type],
) -> Iterator[tuple[LL_Type, LL_Type]]:

    match lat_lon_src:
        case Sequence():
            lat_lon_iter = iter(lat_lon_src)
        case Iterator() as lat_lon_iter:
            pass
        case _:
            raise TypeError("not an Iterator or Sequence")

    begin = next(lat_lon_iter)
    for end in lat_lon_iter:
        yield begin, end
        begin = end


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
