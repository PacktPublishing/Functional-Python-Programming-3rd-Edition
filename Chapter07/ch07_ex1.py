"""Functional Python Programming 3e

Chapter 7, Example Set 1
"""

REPL_tuples = """
>>> some_leg = (
...     (37.549016, -76.330295),
...     (37.840832, -76.273834),
...     17.7246
... )
>>> some_leg
((37.549016, -76.330295), (37.840832, -76.273834), 17.7246)

>>> start = lambda leg: leg[0]
>>> end = lambda leg: leg[1]
>>> distance = lambda leg: leg[2]

>>> latitude = lambda pt: pt[0]
>>> longitude = lambda pt: pt[1]

>>> latitude(start(some_leg))
37.549016

>>> start_s = lambda start, end, distance: start
>>> end_s = lambda start, end, distance: end
>>> distance_s = lambda start, end, distance: distance

>>> latitude_s = lambda lat, lon: lat
>>> longitude_s = lambda lat, lon: lon

>>> longitude_s(*start_s(*some_leg))
-76.330295

"""

from collections.abc import Callable
from typing import TypeAlias

Point: TypeAlias = tuple[float, float]
Leg: TypeAlias = tuple[Point, Point, float]

start: Callable[[Leg], Point] = lambda leg: leg[0]


from typing import NamedTuple


class PointNT(NamedTuple):
    latitude: float
    longitude: float


class LegNT(NamedTuple):
    start: PointNT
    end: PointNT
    distance: float


REPL_named_tuples = """
>>> first_leg = LegNT(
...     PointNT(29.050501, -80.651169),
...     PointNT(27.186001, -80.139503),
...     115.1751)
>>> first_leg.start.latitude
29.050501
"""

from collections.abc import Iterable, Iterator
from Chapter04.ch04_ex1 import pick_lat_lon


def float_lat_lon_tuple(row_iter: Iterable[list[str]]) -> Iterator[tuple[float, float]]:
    lat_lon_iter = (pick_lat_lon(*row) for row in row_iter)
    return ((float(lat), float(lon)) for lat, lon in lat_lon_iter)


from collections.abc import Sequence


def test_float_lat_lon_tuple() -> None:
    source = [["1", "2", "alt"], ["2", "3", "alt"]]
    actual = list(float_lat_lon_tuple(iter(source)))
    assert actual == [(2.0, 1.0), (3.0, 2.0)]


from Chapter04.ch04_ex1 import pick_lat_lon
from typing import Iterable, Iterator


def float_lat_lon(row_iter: Iterable[list[str]]) -> Iterator[PointNT]:
    # ------
    lat_lon_iter = (pick_lat_lon(*row) for row in row_iter)
    return (
        PointNT(float(lat), float(lon))
        # ------
        for lat, lon in lat_lon_iter
    )


from collections.abc import Sequence


def test_float_lat_lon() -> None:
    source = [["1", "2", "alt"], ["2", "3", "alt"]]
    actual = list(float_lat_lon_tuple(iter(source)))
    assert actual == [(2.0, 1.0), (3.0, 2.0)]


import codecs

from collections.abc import Iterable, Iterator
from typing import cast, TextIO
import urllib.request
from Chapter04.ch04_ex1 import legs, haversine, row_iter_kml

source_url = "file:./Winter%202012-2013.kml"


def get_trip(url: str = source_url) -> list[LegNT]:
    with urllib.request.urlopen(url) as source:
        path_iter = float_lat_lon(row_iter_kml(source))
        pair_iter = legs(path_iter)
        trip_iter = (
            LegNT(start, end, round(haversine(start, end), 4))
            for start, end in pair_iter
        )
        trip = list(trip_iter)
    return trip


REPL_test_trip = """
>>> source_url = "file:./Winter%202012-2013.kml"
>>> trip = get_trip(source_url)

>>> trip[0].start
PointNT(latitude=37.54901619777347, longitude=-76.33029518659048)
>>> trip[0].end
PointNT(latitude=37.840832, longitude=-76.273834)
>>> trip[0].distance
17.7246
"""

REPL_find_given_leg_demo = """
>>> source_url = "file:./Winter%202012-2013.kml"
>>> trip = get_trip(source_url)
>>> leg = next(filter(lambda leg: int(leg.distance)==115, trip))
>>> leg.start.latitude
29.050501
"""

import math


class PointE(NamedTuple):
    latitude: float
    longitude: float

    def distance(self, other: "PointE", R: float = 360 * 60 / math.tau) -> float:
        """Equirectangular, 'flat-earth' distance."""
        Δφ = math.radians(self.latitude) - math.radians(other.latitude)
        Δλ = math.radians(self.longitude) - math.radians(other.longitude)
        mid_φ = (math.radians(self.latitude) - math.radians(other.latitude)) / 2
        x = R * Δλ * math.cos(mid_φ)
        y = R * Δφ
        return math.hypot(x, y)


REPL_test_pointe = """
>>> start = PointE(latitude=38.330166, longitude=-76.458504)
>>> end = PointE(latitude=38.976334, longitude=-76.473503)

# Apply the distance() method of the start object...
>>> leg = LegNT(start, end, round(start.distance(end), 4))
>>> leg.start == start
True
>>> leg.end == end
True
>>> leg.distance
38.7805
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PointDC:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class LegDC:
    start: PointDC
    end: PointDC
    distance: float


REPL_test_dataclass = """
>>> first_leg = LegDC(
...     PointDC(29.050501, -80.651169),
...     PointDC(27.186001, -80.139503),
...     115.1751)
>>> first_leg.start.latitude
29.050501
"""

from typing import NamedTuple


class EagerLeg(NamedTuple):
    start: Point
    end: Point
    distance: float

    @classmethod
    def create(cls, start: Point, end: Point) -> "EagerLeg":
        return cls(start=start, end=end, distance=round(haversine(start, end), 4))


REPL_test_eager_leg = """
>>> start = PointNT(29.050501, -80.651169) 
>>> end = PointNT(27.186001, -80.139503) 
>>> leg = EagerLeg.create(start, end)
>>> leg.distance
115.1751
"""

from typing import NamedTuple


class LazyLeg(NamedTuple):
    start: Point
    end: Point

    @property
    def distance(self) -> float:
        return round(haversine(self.start, self.end), 4)

    @classmethod
    def create(cls, start: Point, end: Point) -> "LazyLeg":
        return cls(start=start, end=end)


REPL_test_lazy_leg = """
>>> start = PointNT(29.050501, -80.651169) 
>>> end = PointNT(27.186001, -80.139503) 
>>> leg = LazyLeg.create(start, end)
>>> leg.distance
115.1751
"""

REPL_test_constructors = """
>>> start = PointNT(latitude=37.54901619777347, longitude=-76.33029518659048)
>>> end = PointNT(latitude=37.840832, longitude=-76.273834)

>>> LegNT(start, end, round(haversine(start, end), 4))
LegNT(start=PointNT(latitude=37.54901619777347, longitude=-76.33029518659048), end=PointNT(latitude=37.840832, longitude=-76.273834), distance=17.7246)

>>> row = ['-76.459503', '38.331501', '0']
>>> PointNT(*map(float, pick_lat_lon(*row)))
PointNT(latitude=38.331501, longitude=-76.459503)

>>> PointNT(longitude=float(row[0]), latitude=float(row[1]))
PointNT(latitude=38.331501, longitude=-76.459503)
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
