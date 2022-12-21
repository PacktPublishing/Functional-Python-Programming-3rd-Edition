"""Functional Python Programming 3e

Chapter 4, Example Set 1
"""

import urllib.request
import xml.etree.ElementTree as XML
import csv
from typing import List, TextIO, Iterable, Tuple, Iterator

from collections.abc import Callable, Sequence
from typing import Any, TypeAlias

Extractor: TypeAlias = Callable[[Sequence[Any]], Any]

fst: Extractor = lambda x: x[0]
snd: Extractor = lambda x: x[1]


def test_fst_snd() -> None:
    assert fst([1, 2, 3]) == 1
    assert snd([1, 2, 3]) == 2


from collections.abc import Iterable
from typing import TextIO
import xml.etree.ElementTree as XML


def row_iter_kml(file_obj: TextIO) -> Iterable[list[str]]:
    ns_map = {
        "ns0": "http://www.opengis.net/kml/2.2",
        "ns1": "http://www.google.com/kml/ext/2.2",
    }
    path_to_points = (
        "./ns0:Document/ns0:Folder/ns0:Placemark/" "ns0:Point/ns0:coordinates"
    )
    doc = XML.parse(file_obj)
    text_blocks = (
        coordinates.text for coordinates in doc.iterfind(path_to_points, ns_map)
    )
    return (comma_split(text) for text in text_blocks if text is not None)


def test_row_iter_kml() -> None:
    import io
    from textwrap import dedent

    doc = io.StringIO(
        dedent(
            """\
            <?xml version="1.0" encoding="UTF-8"?>
            <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
            <Document>
                <Folder>
                <name>Waypoints.kml</name>
                <open>1</open>
                <Placemark>
                    <Point>
                        <coordinates>-76.33029518659048,37.54901619777347,0</coordinates>
                    </Point>
                </Placemark>
               </Folder>
            </Document>
            </kml>
        """
        )
    )
    assert list(row_iter_kml(doc)) == [["-76.33029518659048", "37.54901619777347", "0"]]


def comma_split(text: str) -> list[str]:
    return text.split(",")


REPL_raw_data = """
>>> from pprint import pprint
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...     v1 = list(row_iter_kml(source))
>>> pprint(v1)
[['-76.33029518659048', '37.54901619777347', '0'],
 ['-76.27383399999999', '37.840832', '0'],
 ['-76.459503', '38.331501', '0'],
 ...
 ['-76.47350299999999', '38.976334', '0']]
"""


def test_comma_split() -> None:
    assert comma_split("a,b,c") == "a,b,c".split(",")


def pick_lat_lon(lon: str, lat: str, alt: str) -> tuple[str, str]:
    return lat, lon


def test_pick_lat_lon() -> None:
    assert pick_lat_lon(*["-76.459503", "38.331501", "0"]) == (
        "38.331501",
        "-76.459503",
    )


from collections.abc import Iterable
from typing import TypeAlias

Rows: TypeAlias = Iterable[list[str]]
LL_Text: TypeAlias = tuple[str, str]


def lat_lon_kml(row_iter: Rows) -> Iterable[LL_Text]:
    return (pick_lat_lon(*row) for row in row_iter)


def test_lat_lon_kml() -> None:
    data = [["-76.33029518659048", "37.54901619777347", "0"]]
    assert list(lat_lon_kml(data)) == [("37.54901619777347", "-76.33029518659048")]


REPL_test_lat_lon_kml = """
>>> data = [['-76.33029518659048', '37.54901619777347', '0']]
>>> list(lat_lon_kml( data ))
[('37.54901619777347', '-76.33029518659048')]
"""

REPL_lat_lon_kml = """
>>> import urllib
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...     v1 = tuple(lat_lon_kml(row_iter_kml(source)))
>>> v1[0]
('37.54901619777347', '-76.33029518659048')
>>> v1[-1]
('38.976334', '-76.47350299999999')
"""

from typing import cast


def float_lat_lon(row_iter: Iterable[list[str]]) -> Iterator[tuple[float, float]]:
    return (
        cast(tuple[float, float], tuple(map(float, pick_lat_lon(*row))))
        for row in row_iter
    )


def test_float_lat_lon() -> None:
    from textwrap import dedent

    data = [["-76.33029518659048", "37.54901619777347", "0"]]
    assert list(float_lat_lon(data)) == [(37.54901619777347, -76.33029518659048)]

    source_url = "file:./Winter%202012-2013.kml"
    with urllib.request.urlopen(source_url) as source:
        v1 = tuple(float_lat_lon(row_iter_kml(source)))
    first = (37.54901619777347, -76.33029518659048)
    last = (38.976334, -76.47350299999999)
    assert v1[0] == first
    assert v1[-1] == last


REPL_test_float_lat_lon = """
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v0 = list(row_iter_kml(source))
>>> len(v0)
74
>>> v0[0]
['-76.33029518659048', '37.54901619777347', '0']
>>> v0[-1]
['-76.47350299999999', '38.976334', '0']

>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v2 = tuple(float_lat_lon(row_iter_kml(source)))
>>> len(v2)
74
>>> v2[0]
(37.54901619777347, -76.33029518659048)
>>> v2[-1]
(38.976334, -76.473503)
"""


def lat_lon_csv(source: TextIO) -> Iterator[list[str]]:
    """Lat_lon values built from a CSV source."""
    rdr = csv.reader(source)
    header = next(rdr)
    return rdr


from collections.abc import Iterator, Iterable
from typing import Any, TypeVar

T1 = TypeVar("T1")


def pairs(iterator: Iterator[T1]) -> Iterator[tuple[T1, T1]]:
    def pair_from(head: Any, iterable_tail: Iterator[T1]) -> Iterator[tuple[T1, T1]]:
        try:
            nxt = next(iterable_tail)
        except StopIteration:
            return
        yield head, nxt
        yield from pair_from(nxt, iterable_tail)

    try:
        yield from pair_from(next(iterator), iterator)
    except StopIteration:
        return iter([])


def test_pairs() -> None:
    trip = iter([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    assert list(pairs(trip)) == [
        ((0, 0), (1, 0)),
        ((1, 0), (1, 1)),
        ((1, 1), (0, 1)),
        ((0, 1), (0, 0)),
    ]


from collections.abc import Iterator, Iterable
from typing import Any, TypeVar

LL_Type = TypeVar("LL_Type")


def legs(lat_lon_iter: Iterator[LL_Type]) -> Iterator[tuple[LL_Type, LL_Type]]:
    begin = next(lat_lon_iter)
    for end in lat_lon_iter:
        yield begin, end
        begin = end


def test_legs() -> None:
    trip = iter([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    assert tuple(legs(trip)) == (
        ((0, 0), (1, 0)),
        ((1, 0), (1, 1)),
        ((1, 1), (0, 1)),
        ((0, 1), (0, 0)),
    )


REPL_demo = """
>>> items = list(range(5))
>>> [items[0:2], items[1:3], items[2:4], ..., items[-2:]]
[[0, 1], [1, 2], [2, 3], Ellipsis, [3, 4]]
>>> list(zip(items, items[1:]))
[(0, 1), (1, 2), (2, 3), (3, 4)]
"""

REPL_legs_iter_example = """
# Iterator as input:
>>> list(legs(x for x in range(3)))
[(0, 1), (1, 2)]

# List object as input:
>>> list(legs([0, 1, 2]))
Traceback (most recent call last):
...
TypeError: 'list' object is not an iterator

# Explicit iterator created from list object:
>>> list(legs(iter([0,1,2])))
[(0, 1), (1, 2)]
"""

from collections.abc import Iterator, Iterable, Callable
from typing import TypeAlias

Waypoint: TypeAlias = tuple[float, float]
Pairs_Iter: TypeAlias = Iterator[Waypoint]
Leg: TypeAlias = tuple[Waypoint, Waypoint]
Leg_Iter: TypeAlias = Iterable[Leg]


def legs_filter(
    lat_lon_iter: Pairs_Iter, rejection_rule: Callable[[Waypoint, Waypoint], bool]
) -> Leg_Iter:
    begin = next(lat_lon_iter)
    for end in lat_lon_iter:
        if rejection_rule(begin, end):
            pass
        else:
            yield begin, end
        begin = end


def test_legs_filter() -> None:
    trip = iter([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (0, 1), (0, 0)])
    some_rule = lambda b, e: b[0] == 0
    assert list(legs_filter(trip, some_rule)) == [
        ((1, 0), (2, 0)),
        ((2, 0), (2, 1)),
        ((2, 1), (2, 2)),
        ((2, 2), (0, 1)),
    ]


REPL_test_trip = """
>>> import urllib
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...     trip = list(
...         legs(
...            (float(lat), float(lon))
...            for lat, lon in lat_lon_kml(row_iter_kml(source))
...         )
...     )

>>> trip  # doctest: +ELLIPSIS
[((37.54901619777347, -76.33029518659048), (37.840832, -76.273834)), ..., ((38.330166, -76.458504), (38.976334, -76.473503))]

>>> import urllib
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...     ll_iter = (
...         (float(lat), float(lon))
...         for lat, lon in lat_lon_kml(row_iter_kml(source))
...     )
...     trip = list(
...         legs(ll_iter)
...     )

>>> trip  # doctest: +ELLIPSIS
[((37.54901619777347, -76.33029518659048), (37.840832, -76.273834)), ..., ((38.330166, -76.458504), (38.976334, -76.473503))]

"""

from collections.abc import Iterator, Iterable
from typing import TypeAlias

Text_Iter: TypeAlias = Iterable[tuple[str, str]]
LL_Iter: TypeAlias = Iterable[tuple[float, float]]


def floats_from_pair(lat_lon_iter: Text_Iter) -> LL_Iter:
    return ((float(lat), float(lon)) for lat, lon in lat_lon_iter)


def test_floats_from_pair() -> None:
    trip = [("1", "2"), ("2.718", "3.142")]
    assert tuple(floats_from_pair(trip)) == ((1.0, 2.0), (2.718, 3.142))


REPL_floats_from_pair = """
>>> import urllib
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...     trip = list(
...         legs(
...             floats_from_pair(
...                 lat_lon_kml(
...                     row_iter_kml(source))))
...     )

>>> trip  # doctest: +ELLIPSIS
[((37.54901619777347, -76.33029518659048), (37.840832, -76.273834)), ..., ((38.330166, -76.458504), (38.976334, -76.473503))]

"""

from math import radians, sin, cos, sqrt, asin
from typing import TypeAlias

MI = 3959
NM = 3440
KM = 6371

Point: TypeAlias = tuple[float, float]


def haversine(p1: Point, p2: Point, R: float = NM) -> float:
    lat_1, lon_1 = p1
    lat_2, lon_2 = p2
    Δ_lat = radians(lat_2 - lat_1)
    Δ_lon = radians(lon_2 - lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)

    a = sqrt(sin(Δ_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(Δ_lon / 2) ** 2)
    c = 2 * asin(a)
    return R * c


def test_haversine() -> None:
    from pytest import approx

    assert round(haversine((36.12, -86.67), (33.94, -118.40), R=6372.8), 5) == approx(
        2887.25995
    )


REPL_haversine_demo = """
>>> import urllib
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...     trip = (
...         (start, end, round(haversine(start, end), 4))
...         for start,end in
...             legs(
...                 floats_from_pair(
...                     lat_lon_kml(row_iter_kml(source))
...                 )
...             )
...     )
...     for start, end, dist in trip:
...         print(f"({start} to {end} is {dist:.1f}")
((37.54901619777347, -76.33029518659048) to (37.840832, -76.273834) is 17.7
((37.840832, -76.273834) to (38.331501, -76.459503) is 30.7
((38.331501, -76.459503) to (38.845501, -76.537331) is 31.1
((38.845501, -76.537331) to (38.992832, -76.451332) is 9.7
...
"""


import itertools
from typing import Iterable, TypeVar


REPL_test_parse_2 = """
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v0 = tuple(legs(float_lat_lon(row_iter_kml(source)) ) )
>>> len(v0)
73
>>> v0[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834))
>>> v0[-1]
((38.330166, -76.458504), (38.976334, -76.473503))

>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v1 = tuple(pairs(float_lat_lon(row_iter_kml(source)) ) )
>>> len(v1)
73
>>> v1[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834))
>>> v1[-1]
((38.330166, -76.458504), (38.976334, -76.473503))

>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v2 = tuple(legs( floats_from_pair(lat_lon_kml(row_iter_kml(source)))))
>>> len(v2)
73
>>> v2[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834))
>>> v2[-1]
((38.330166, -76.458504), (38.976334, -76.473503))

"""

REPL_test_parse_3 = """
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     flt = tuple( (float(lat), float(lon)) for lat,lon in float_lat_lon(row_iter_kml(source)) )
>>> len(flt)
74
>>> flt[0]
(37.54901619777347, -76.33029518659048)
>>> flt[-1]
(38.976334, -76.473503)

"""

REPL_test_haversine = """
>>> trip = iter([(0,0), (1,0), (1,1), (0,1), (0,0)])  # about 240 NM

>>> list((lat, lon, round(haversine(lat, lon), 4)) for lat, lon in legs(trip))
[((0, 0), (1, 0), 60.0393), ((1, 0), (1, 1), 60.0302), ((1, 1), (0, 1), 60.0393), ((0, 1), (0, 0), 60.0393)]
"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
