"""Functional Python Programming 3e

Chapter 8, Example Set 1
"""


REPL_trip = """
>>> from Chapter07.ch07_ex1 import get_trip
>>> source_url = "file:./Winter%202012-2013.kml"
>>> trip = get_trip(source_url)
>>> trip = get_trip()
>>> from textwrap import wrap
>>> from pprint import pprint

>>> trip[0]
LegNT(start=PointNT(latitude=37.54901619777347, longitude=-76.33029518659048), ...

>>> pprint(wrap(str(trip[0])))
['LegNT(start=PointNT(latitude=37.54901619777347,',
 'longitude=-76.33029518659048), end=PointNT(latitude=37.840832,',
 'longitude=-76.273834), distance=17.7246)']
>>> pprint(wrap(str(trip[-1])))
['LegNT(start=PointNT(latitude=38.330166, longitude=-76.458504),',
 'end=PointNT(latitude=38.976334, longitude=-76.473503),',
 'distance=38.8019)']
"""

from typing import NamedTuple


class Point(NamedTuple):
    latitude: float
    longitude: float


class Leg(NamedTuple):
    order: int
    start: Point
    end: Point
    distance: float


def pick_lat_lon(lon: str, lat: str, alt: str) -> tuple[str, str]:
    return lat, lon


from typing import Iterator, List


def float_lat_lon(row_iter: Iterator[List[str]]) -> Iterator[Point]:
    return (Point(*map(float, pick_lat_lon(*row))) for row in row_iter)


from typing import Iterator
from Chapter04.ch04_ex1 import haversine


def numbered_leg_iter(pair_iter: Iterator[tuple[Point, Point]]) -> Iterator[Leg]:
    for order, pair in enumerate(pair_iter):
        start, end = pair
        yield Leg(order, start, end, round(haversine(start, end), 4))


def test_numbered_leg_iter() -> None:
    from Chapter06.ch06_ex3 import row_iter_kml
    from Chapter04.ch04_ex1 import legs, haversine
    import urllib.request

    source_url = "file:./Winter%202012-2013.kml"
    with urllib.request.urlopen(source_url) as source:
        path_iter = float_lat_lon(row_iter_kml(source))
        pair_iter = legs(path_iter)
        trip_iter = numbered_leg_iter(pair_iter)
        trip = list(trip_iter)
    assert trip[0] == Leg(
        order=0,
        start=Point(latitude=37.54901619777347, longitude=-76.33029518659048),
        end=Point(latitude=37.840832, longitude=-76.273834),
        distance=17.7246,
    )
    assert trip[1] == Leg(
        order=1,
        start=Point(latitude=37.840832, longitude=-76.273834),
        end=Point(latitude=38.331501, longitude=-76.459503),
        distance=30.7382,
    )
    assert trip[-1] == Leg(
        order=72,
        start=Point(latitude=38.330166, longitude=-76.458504),
        end=Point(latitude=38.976334, longitude=-76.473503),
        distance=38.8019,
    )


REPL_test_parser = """
>>> from Chapter06.ch06_ex3 import row_iter_kml
>>> from Chapter04.ch04_ex1 import legs, haversine
>>> import urllib.request

>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...     path_iter = float_lat_lon(row_iter_kml(source))
...     pair_iter = legs(path_iter)
...     trip_iter = numbered_leg_iter(pair_iter)
...     trip = list(trip_iter)

>>> len(trip)
73
>>> trip[0]
Leg(order=0, start=Point(latitude=37.54901619777347, longitude=-76.33029518659048), end=Point(latitude=37.840832, longitude=-76.273834), distance=17.7246)
>>> trip[-1]
Leg(order=72, start=Point(latitude=38.330166, longitude=-76.458504), end=Point(latitude=38.976334, longitude=-76.473503), distance=38.8019)

"""

REPL_accumulate = """
>>> from Chapter06.ch06_ex3 import row_iter_kml
>>> from Chapter04.ch04_ex1 import legs, haversine
>>> import urllib.request

>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...     path_iter = float_lat_lon(row_iter_kml(source))
...     pair_iter = legs(path_iter)
...     trip_iter = numbered_leg_iter(pair_iter)
...     trip = list(trip_iter)

>>> from itertools import accumulate
>>> import math

>>> distances = (leg.distance for leg in trip)
>>> distance_accum = list(accumulate(distances))
>>> scale = math.ceil(distance_accum[-1] / 4)

>>> quartiles = list(int(scale*d) for d in distance_accum)
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
