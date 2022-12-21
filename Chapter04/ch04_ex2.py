"""Functional Python Programming 3e

Chapter 4, Example Set 2
Also used in Chapter 5.
"""

REPL_all_any = """
>>> from Chapter02.ch02_ex1 import isprimei as isprime
>>> someset = {2, 3, 5, 7, 11, 13}
>>> all(isprime(x) for x in someset)
True
>>> someset = {2, 3, 5, 7, 11, 13, 15}
>>> all(isprime(x) for x in someset)
False
>>> not_p_1 = not all(isprime(x) for x in someset)
>>> not_p_1
True
>>> not_p_2 = any(not isprime(x) for x in someset)
>>> not_p_2
True

>>> all(())
True
>>> any(())
False
"""


from typing import Any, TypeVar, TypeAlias
from collections.abc import Iterable, Iterator

Waypoint: TypeAlias = tuple[float, float]
Leg: TypeAlias = tuple[Waypoint, Waypoint, float]


def wrap(leg_iter: Iterable[Leg]) -> Iterator[tuple[float, Leg]]:
    return ((leg[2], leg) for leg in leg_iter)


T_ = TypeVar("T_")


def unwrap(dist_leg: tuple[Any, T_]) -> T_:
    distance, leg = dist_leg
    return leg


def by_dist(leg: Leg) -> float:
    lat, lon, dist = leg
    return dist


REPL_max_alternatives = """
>>> from Chapter04.ch04_ex1 import (
...     floats_from_pair, float_lat_lon, row_iter_kml, legs,
...     haversine)
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip = tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> long = max(dist for start, end, dist in trip)
>>> short = min(dist for start, end, dist in trip)
>>> long
129.7748
>>> short
0.1731

>>> long, short = unwrap( max( wrap( trip ) ) ), unwrap( min( wrap( trip ) ) )
>>> long
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
>>> short
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)

>>> long, short = max(trip, key=by_dist), min(trip, key=by_dist)
>>> long
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
>>> short
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
"""

from collections.abc import Iterable, Callable
from typing import Any, Protocol


class Sortable(Protocol):
    def __lt__(self, other: Any) -> bool:
        ...


def max_like(trip: Iterable[Leg], key: Callable[[Leg], Sortable] = lambda x: x) -> Leg:
    """
    >>> max_like([1, 3, 2])
    3
    """
    wrapped = ((key(leg), leg) for leg in trip)
    return sorted(wrapped)[-1][1]


start: Callable[[tuple[Any, ...]], Any] = lambda x: x[0]
end: Callable[[tuple[Any, ...]], Any] = lambda x: x[1]
dist: Callable[[tuple[Any, ...]], Any] = lambda x: x[2]

lat: Callable[[tuple[Any, ...]], Any] = lambda x: x[0]
lon: Callable[[tuple[Any, ...]], Any] = lambda x: x[1]

REPL_min_max = """
>>> from Chapter04.ch04_ex1 import (
...     floats_from_pair, float_lat_lon, row_iter_kml, legs,
...     haversine)
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip = tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> long, short = max(trip, key=dist), min(trip, key=dist)
>>> long
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
>>> short
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)

>>> north = min( trip, key=lambda x: lat(start(x)) )
>>> north
((23.9555, -76.31633), (24.099667, -76.401833), 9.844)

"""

REPL_conversion = """
>>> from Chapter04.ch04_ex1 import (
...     floats_from_pair, float_lat_lon, row_iter_kml, legs,
...     haversine)
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip = tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> statute1 = list( (start(x),end(x),dist(x)*6076.12/5280) for x in trip )
>>> statute2 = list( map( lambda x: (start(x),end(x),dist(x)*6076.12/5280), trip ) )
>>> statute3 = list( (b, e, d*6076.12/5280) for b, e, d in trip )

>>> assert statute1 == statute2
>>> assert statute1 == statute3

>>> statute1[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 20.397120559090908)

>>> statute1[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 44.652462240151515)

"""


def performance() -> None:
    import timeit

    map_time = timeit.timeit(
        """list(map(int,data))""",
        """data = ['2', '3', '5', '7', '11', '13', '17', '19', '23', '29', '31', '37', '41', '43', '47', '53', '59', '61', '67', '71', '73', '79', '83', '89', '97', '101', '103', '107', '109', '113', '127', '131', '137', '139', '149', '151', '157', '163', '167', '173', '179', '181', '191', '193', '197', '199', '211', '223', '227', '229']""",
    )
    print(f"map {map_time:.4f}")
    expr_time = timeit.timeit(
        """list(int(v) for v in data)""",
        """data = ['2', '3', '5', '7', '11', '13', '17', '19', '23', '29', '31', '37', '41', '43', '47', '53', '59', '61', '67', '71', '73', '79', '83', '89', '97', '101', '103', '107', '109', '113', '127', '131', '137', '139', '149', '151', '157', '163', '167', '173', '179', '181', '191', '193', '197', '199', '211', '223', '227', '229']""",
    )
    print(f"expr {expr_time:.4f}")


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}


if __name__ == "__main__":
    performance()
