"""Functional Python Programming 3e

Chapter 7, Example Set 6
"""

REPL_demo_1 = """
>>> import pyrsistent
>>> v = pyrsistent.pmap({"hello": 42, "world": 3.14159})
>>> v  # doctest: +SKIP
pmap({'hello': 42, 'world': 3.14159})
>>> v['hello']
42
>>> v['world']
3.14159
>>> v2 = v.set("another", 2.71828)
>>> v2    # doctest: +SKIP
pmap({'hello': 42, 'world': 3.14159, 'another': 2.71828})
>>> v    # doctest: +SKIP
pmap({'hello': 42, 'world': 3.14159})
"""

from pyrsistent import PRecord, field


class PointPR(PRecord):  # type: ignore [type-arg]
    latitude = field(type=float)
    longitude = field(type=float)


class LegPR(PRecord):  # type: ignore [type-arg]
    start = field(type=PointPR)
    end = field(type=PointPR)
    distance = field(type=float)


def test_point_pr() -> None:
    pt = PointPR(latitude=1.0, longitude=2.0)
    assert pt.latitude == 1.0
    assert pt.longitude == 2.0


def test_leg_pr() -> None:
    start = PointPR(latitude=37.549016, longitude=-76.330295)
    end = PointPR(latitude=37.840832, longitude=-76.273834)
    leg = LegPR(start=start, end=end, distance=17.7246)
    assert leg.distance == 17.7246


from math import isclose, modf


def to_dm(format: dict[str, str], point: float) -> str:
    """Use {"+": "N", "-": "S"} for latitude; {"+": "E", "-": "W"} for longitude."""
    sign = "-" if point < 0 else "+"
    ms, d = modf(abs(point))
    ms = 60 * ms
    # Handle the 59.999 case:
    if isclose(ms, 60, rel_tol=1e-5):
        ms = 0.0
        d += 1
    return f"{d:3.0f}°{ms:.3f}'{format.get(sign, sign)}"


def test_to_dm() -> None:
    assert to_dm({"+": "N", "-": "S"}, 37.549016) == " 37°32.941'N"
    assert to_dm({"+": "E", "-": "W"}, -76.330295) == " 76°19.818'W"


from pyrsistent import PRecord, field


class PointPR_S(PRecord):  # type: ignore[type-arg]
    latitude = field(
        type=float,
        serializer=(
            lambda format, value: to_dm((format or {}) | {"+": "N", "-": "S"}, value)
        ),
    )
    longitude = field(
        type=float,
        serializer=(
            lambda format, value: to_dm((format or {}) | {"+": "E", "-": "W"}, value)
        ),
    )


REPL_test_pointer = """
>>> p = PointPR_S(latitude=32.842833333, longitude=-79.929166666)
>>> p.serialize()  # doctest: +SKIP
{'latitude': " 32°50.570'N", 'longitude': " 79°55.750'W"}
"""

# Reusing some previous example code.

from typing import NamedTuple


class PointNT(NamedTuple):
    latitude: float
    longitude: float


class LegNT(NamedTuple):
    start: PointNT
    end: PointNT
    distance: float


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


from collections.abc import Iterable, Iterator
from typing import TextIO
import urllib.request
from Chapter04.ch04_ex1 import legs, haversine, row_iter_kml
from pyrsistent import pvector
from pyrsistent.typing import PVector

source_url = "file:./Winter%202012-2013.kml"


def get_trip_p(url: str = source_url) -> PVector[LegPR]:
    with urllib.request.urlopen(url) as source:
        path_iter = float_lat_lon(row_iter_kml(source))
        pair_iter = legs(path_iter)
        trip_iter = (
            LegPR(
                start=PointPR.create(start._asdict()),
                end=PointPR.create(end._asdict()),
                distance=round(haversine(start, end), 4),
            )
            # --------------------------------------------
            for start, end in pair_iter
        )
        trip = pvector(trip_iter)
        # ------
    return trip


def test_get_trip_p() -> None:
    t = get_trip_p(source_url)
    assert t[0] == LegPR(
        end=PointPR(latitude=37.840832, longitude=-76.273834),
        start=PointPR(latitude=37.54901619777347, longitude=-76.33029518659048),
        distance=17.7246,
    )
    assert t[-1] == LegPR(
        distance=38.8019,
        end=PointPR(latitude=38.976334, longitude=-76.473503),
        start=PointPR(latitude=38.330166, longitude=-76.458504),
    )


REPL_asdict = """
>>> p = PointNT(2, 3)
>>> p._asdict()
{'latitude': 2, 'longitude': 3}
"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
