"""Functional Python Programming 3e

Chapter 5, Example Set 1
"""

REPL_max = """
>>> max(1, 2, 3)
3
>>> max((1,2,3,4))
4
"""

REPL_example = """
[
 ((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246),
 ((37.840832, -76.273834), (38.331501, -76.459503), 30.7382),
 ((38.331501, -76.459503), (38.845501, -76.537331), 31.0756),
 ((36.843334, -76.298668), (37.549, -76.331169), 42.3962),
 ((37.549, -76.331169), (38.330166, -76.458504), 47.2866),
 ((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)
]
"""

REPL_long_short = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> data = "file:./Winter%202012-2013.kml"

>>> with urllib.request.urlopen(data) as source:
...     path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...     trip = list(
...         (start, end, round(haversine(start, end), 4))
...         for start, end in legs(path)
...     )

>>> longest = max(dist for start, end, dist in trip)
>>> shortest = min(dist for start, end, dist in trip)

>>> longest
129.7748
>>> shortest
0.1731
"""

from collections.abc import Iterator, Iterable
from typing import Any


def wrap(leg_iter: Iterable[Any]) -> Iterable[tuple[Any, Any]]:
    return ((leg[2], leg) for leg in leg_iter)


def unwrap(dist_leg: tuple[Any, Any]) -> Any:
    distance, leg = dist_leg
    return leg


REPL_long_short_2 = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> data = "file:./Winter%202012-2013.kml"

>>> with urllib.request.urlopen(data) as source:
...     path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...     trip = list(
...         (start, end, round(haversine(start, end), 4))
...         for start, end in legs(path)
...     )

>>> longest = unwrap(max(wrap(trip)))
>>> longest
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)

>>> short = unwrap(min(wrap(trip)))
>>> short
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
"""


def by_dist(leg: tuple[Any, Any, Any]) -> Any:
    lat, lon, dist = leg
    return dist


REPL_long_short_3 = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> data = "file:./Winter%202012-2013.kml"

>>> with urllib.request.urlopen(data) as source:
...     path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...     trip = list(
...         (start, end, round(haversine(start, end), 4))
...         for start, end in legs(path)
...     )

>>> longest = max(trip, key=by_dist)
>>> longest
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)

>>> short = min(trip, key=by_dist)
>>> short
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
"""

REPL_test_long_short_4 = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> data = "file:./Winter%202012-2013.kml"

>>> with urllib.request.urlopen(data) as source:
...     path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...     trip = list(
...         (start, end, round(haversine(start, end), 4))
...         for start, end in legs(path)
...     )

>>> longest = max(trip, key=lambda leg: leg[2])
>>> shortest = min(trip, key=lambda leg: leg[2])

>>> longest
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
>>> shortest
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
"""

start = lambda x: x[0]
end = lambda x: x[1]
dist = lambda x: x[2]

REPL_test_long_short_5 = """
>>> longest = ((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
>>> dist(longest)
129.7748

>>> from operator import itemgetter 
>>> start = itemgetter(0)
>>> start(longest)
(27.154167, -80.195663)

>>> lat = itemgetter(0)
>>> lon = itemgetter(1)
>>> lat(start(longest))
27.154167
"""

# The following REPL example uses a triple-" string.
'''
>>> text= """\
... 2 3 5 7 11 13 17 19 23 29
... 31 37 41 43 47 53 59 61 67 71
... 73 79 83 89 97 101 103 107 109 113
... 127 131 137 139 149 151 157 163 167 173
... 179 181 191 193 197 199 211 223 227 229
... """

>>> data = list(
...     v
...     for line in text.splitlines()
...         for v in line.split()
... )

>>> data
['2', '3', '5', '7', '11', '13', '17', '19', '23', '29', '31', '37', '41', '43', '47', '53', '59', '61', '67', '71', '73', '79', '83', '89', '97', '101', '103', '107', '109', '113', '127', '131', '137', '139', '149', '151', '157', '163', '167', '173', '179', '181', '191', '193', '197', '199', '211', '223', '227', '229']

>>> list(map(int, data))
[2, 3, 5, 7, 11, 13, 17, 19, ..., 229]
'''


REPL_sm_trip = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> data = "file:./Winter%202012-2013.kml"

>>> with urllib.request.urlopen(data) as source:
...     path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...     trip = list(
...         (start, end, round(haversine(start, end), 4))
...         for start, end in legs(path)
...     )

>>> len(trip)
73
>>> trip[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)

>>> from operator import itemgetter 
>>> start = itemgetter(0)
>>> end = itemgetter(1)
>>> dist = itemgetter(2)
>>> sm_trip = map(
...     lambda x: (start(x), end(x), dist(x) * 6076.12 / 5280),
...     trip
... )

>>> sm_trip
<map object at ...>

>>> list(sm_trip)
[((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 20.397120559090908)...

>>> sm_trip = (
...     (start(x), end(x), dist(x) * 6076.12 / 5280)
...     for x in trip
... )

>>> list(sm_trip)
[((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 20.397120559090908)...

"""

REPL_map_syntax = """
>>> function = lambda x_y: (x_y[0] * 8 + x_y[1])
>>> one_iterable = [1, 2, 3]
>>> another_iterable = [4, 5, 6]
>>> map(function, zip(one_iterable, another_iterable))
<map object at ...>
>>> list(_)
[12, 21, 30]

"""

from collections.abc import Callable, Iterable
from typing import Any


def example_map_syntax_1(
    function: Callable[..., Any],
    one_iterable: Iterable[Any],
    another_iterable: Iterable[Any],
) -> Any:
    return map(function, zip(one_iterable, another_iterable))


def test_example_map_1() -> None:
    function = lambda x_y: (x_y[0] * 8 + x_y[1])
    one_iterable = [1, 2, 3]
    another_iterable = [4, 5, 6]
    r = example_map_syntax_1(function, one_iterable, another_iterable)
    assert list(r) == [12, 21, 30]


def example_map_syntax_2(
    function: Callable[..., Any],
    one_iterable: Iterable[Any],
    another_iterable: Iterable[Any],
) -> Any:
    return (function(x, y) for x, y in zip(one_iterable, another_iterable))


def test_example_map_2() -> None:
    function = lambda x, y: (x * 8 + y)
    one_iterable = [1, 2, 3]
    another_iterable = [4, 5, 6]
    r = example_map_syntax_2(function, one_iterable, another_iterable)
    assert list(r) == [12, 21, 30]


REPL_zip_demo = """
>>> waypoints = range(4)
>>> zip(waypoints, waypoints[1:])
<zip object at ...>

>>> list(zip(waypoints, waypoints[1:]))
[(0, 1), (1, 2), (2, 3)]
"""

REPL_distance = """

>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine
... )
>>> import urllib.request

>>> data = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(data) as source:
...     path_gen = floats_from_pair(
...         float_lat_lon(row_iter_kml(source)))
...     path = list(path_gen)

>>> distances_1 = map(
...     lambda s_e: (s_e[0], s_e[1], haversine(*s_e)),
...     zip(path, path[1:])
... )

>>> list(distances_1)
[((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.724564798884984), ...

>>> distances_2 = map(
...     lambda s, e: (s, e, haversine(s, e)),
...     path, path[1:]
... )
>>> list(distances_2)
[((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.724564798884984), ...

"""

REPL_filter_legs = """
>>> trip = [
...        ((0, 0), (1, 1), 1.4*18),
...        ((1, 1), (3, 3), 2.8*18),
...        ((3, 3), (3, 0), 3*18),
...    ]

>>> long_legs = list(
...     filter(lambda leg: dist(leg) >= 50, trip)
... )

>>> long_legs
[((1, 1), (3, 3), 50.4), ((3, 3), (3, 0), 54)]

"""

REPL_filter_fizz_buzz = """
>>> filter(lambda x: x % 3 == 0 or x % 5 == 0, range(10))
<filter object at ...>
>>> sum(_)
23

>>> list(x for x in range(10) if x % 3 == 0 or x % 5 == 0)
[0, 3, 5, 6, 9]

>>> from Chapter02.ch02_ex1 import isprimeg

>>> list(filter(isprimeg, range(100)))
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
"""

REPL_outliers = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> data = "file:./Winter%202012-2013.kml"

>>> with urllib.request.urlopen(data) as source:
...     path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...     trip = list(
...         (start, end, round(haversine(start, end), 4))
...         for start, end in legs(path)
...     )

>>> from Chapter04.ch04_ex3 import mean, stdev, z

>>> dist_data = list(map(dist, trip))
>>> μ_d = mean(dist_data)
>>> σ_d = stdev(dist_data)

>>> outlier = lambda leg: abs(z(dist(leg), μ_d, σ_d)) > 3

>>> list(filter(outlier, trip))
[((29.050501, -80.651169), (27.186001, -80.139503), 115.1751), ((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)]

"""


REPL_iter = """
>>> source = [1, 2, 3, None, 4, 5, 6]
>>> tail = iter(source.pop, None)
>>> list(tail)
[6, 5, 4]
"""

REPL_sorted = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> data = "file:./Winter%202012-2013.kml"

>>> with urllib.request.urlopen(data) as source:
...     path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...     trip = list(
...         (start, end, round(haversine(start, end), 4))
...         for start, end in legs(path)
...     )

>>> sorted(dist(x) for x in trip)
[0.1731, 0.1898, 1.4235, 4.3155, ... 86.2095, 115.1751, 129.7748]

>>> sorted(trip, key=dist)
[((35.505665, -76.653664), (35.508335, -76.654999), 0.1731), ...

>>> from operator import itemgetter
>>> dist = itemgetter(2)
"""

REPL_higher_order_map_1 = """
>>> f = lambda x: 2**x - 1
>>> C = [8, 16, 32]
>>> list(map(f, C))
[255, 65535, 4294967295]
>>> list((f(x) for x in C))
[255, 65535, 4294967295]
"""

from collections.abc import Callable, Iterable, Iterator
from typing import Any


def mymap(f: Callable[[Any], Any], C: Iterable[Any]) -> Iterator[Any]:
    for x in C:
        yield f(x)


REPL_higher_order_map_2 = """
>>> f = lambda x: 2**x - 1
>>> C = [8, 16, 32]
>>> list(mymap(f, C))
[255, 65535, 4294967295]
"""

REPL_higher_order_filter_1 = """
>>> f = lambda x: x % 3 == 0
>>> C = [14, 15, 16, 17, 18]
>>> list(filter(f, C))
[15, 18]
>>> list((x for x in C if f(x)))
[15, 18]
"""

from collections.abc import Callable, Iterable, Iterator
from typing import Any


def myfilter(f: Callable[[Any], bool], C: Iterable[Any]) -> Iterator[Any]:
    for x in C:
        if f(x):
            yield x


REPL_higher_order_filter_2 = """
>>> f = lambda x: x % 3 == 0
>>> C = [14, 15, 16, 17, 18]
>>> list(myfilter(f, C))
[15, 18]
"""

from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeAlias

Conv_F: TypeAlias = Callable[[float], float]
Leg: TypeAlias = tuple[Any, Any, float]


def convert(conversion: Conv_F, trip: Iterable[Leg]) -> Iterator[float]:
    return (conversion(distance) for start, end, distance in trip)


from collections.abc import Callable
from typing import TypeAlias

Conversion: TypeAlias = Callable[[float], float]

to_miles: Conversion = lambda nm: nm * 6076.12 / 5280

to_km: Conversion = lambda nm: nm * 1.852

to_nm: Conversion = lambda nm: nm

from collections.abc import Callable
from operator import itemgetter
from typing import TypeAlias

Selector: TypeAlias = Callable[[tuple[Any, ...]], Any]

fst: Selector = itemgetter(0)

snd: Selector = itemgetter(1)

sel2: Selector = itemgetter(2)

from collections.abc import Callable

to_miles_sel2: Callable[[tuple[Any, Any, float]], float] = lambda s_e_d: to_miles(
    sel2(s_e_d)
)

REPL_test_convert = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> data = "file:./Winter%202012-2013.kml"

>>> with urllib.request.urlopen(data) as source:
...     path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...     trip = list(
...         (start, end, round(haversine(start, end), 4))
...         for start, end in legs(path)
...     )

>>> trip[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)
>>> trip[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)

>>> convert(to_miles, trip)
<generator object ...>
>>> miles = list(convert(to_miles, trip))
>>> trip[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)
>>> miles[0]
20.397120559090908
>>> trip[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)
>>> miles[-1]
44.652462240151515

>>> miles2 = list(
...     to_miles_sel2(s_e_d) for s_e_d in trip
... )

>>> miles2[0]
20.397120559090908
>>> miles2[-1]
44.652462240151515

>>> assert miles == miles2
"""

from collections.abc import Callable, Iterable, Iterator
from typing import TypeAlias

Point: TypeAlias = tuple[float, float]
Leg_Raw: TypeAlias = tuple[Point, Point]
Point_Func: TypeAlias = Callable[[Point, Point], float]
Leg_D: TypeAlias = tuple[Point, Point, float]


def cons_distance(
    distance: Point_Func, legs_iter: Iterable[Leg_Raw]
) -> Iterator[Leg_D]:
    return ((start, end, round(distance(start, end), 4)) for start, end in legs_iter)


REPL_test_cons_distance = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request

>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...    path = floats_from_pair(
...        float_lat_lon(row_iter_kml(source))
...    )
...    trip2 = tuple(
...        cons_distance(haversine, legs(iter(path)))
...    )

>>> trip2[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)
>>> trip2[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)

"""

from collections.abc import Callable, Iterable, Iterator
from typing import Any


def cons_distance3(
    distance: Point_Func, legs_iter: Iterable[Leg_Raw]
) -> Iterator[Leg_D]:
    return (leg + (round(distance(*leg), 4),) for leg in legs_iter)  # 1-tuple


REPL_test_cons_distance3 = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...    path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip3 = tuple(cons_distance3( haversine, legs(iter(path))))

>>> trip3[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)
>>> trip3[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)

"""

from collections.abc import Callable, Iterator
from typing import TypeAlias

Num_Conv: TypeAlias = Callable[[str], float]


def numbers_from_rows(conversion: Num_Conv, text: str) -> Iterator[float]:
    return (conversion(value) for line in text.splitlines() for value in line.split())


# Code uses triple-" string
REPL_test_numbers_from_rows = '''
>>> text = """2 3 5 7 11 13 17 19 23 29
... 31 37 41 43 47 53 59 61 67 71
... 73 79 83 89 97 101 103 107 109 113
... 127 131 137 139 149 151 157 163 167 173
... 179 181 191 193 197 199 211 223 227 229
... """

>>> data = list(
...     v
...     for line in text.splitlines()
...         for v in line.split()
... )
>>> data
['2', '3', '5', '7', '11', '13', '17', '19', '23', '29', '31', '37',...

>>> list(numbers_from_rows(float, text))
[2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0, 19.0, 23.0, 29.0, 31.0, 37.0, 41.0, 43.0, 47.0, 53.0, 59.0, 61.0, 67.0, 71.0, 73.0, 79.0, 83.0, 89.0, 97.0, 101.0, 103.0, 107.0, 109.0, 113.0, 127.0, 131.0, 137.0, 139.0, 149.0, 151.0, 157.0, 163.0, 167.0, 173.0, 179.0, 181.0, 191.0, 193.0, 197.0, 199.0, 211.0, 223.0, 227.0, 229.0]

>>> text = (value
...     for line in text.splitlines()
...        for value in line.split()
... )
>>> numbers = map(float, text)
>>> list(numbers)
[2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0, 19.0, 23.0, 29.0, 31.0, 37.0, 41.0, 43.0, 47.0, 53.0, 59.0, 61.0, 67.0, 71.0, 73.0, 79.0, 83.0, 89.0, 97.0, 101.0, 103.0, 107.0, 109.0, 113.0, 127.0, 131.0, 137.0, 139.0, 149.0, 151.0, 157.0, 163.0, 167.0, 173.0, 179.0, 181.0, 191.0, 193.0, 197.0, 199.0, 211.0, 223.0, 227.0, 229.0]

'''

from collections.abc import Iterator
from typing import TypeVar

ItemT = TypeVar("ItemT")


def group_by_iter(n: int, iterable: Iterator[ItemT]) -> Iterator[tuple[ItemT, ...]]:
    def group(n: int, iterable: Iterator[ItemT]) -> Iterator[ItemT]:
        for i in range(n):
            try:
                yield next(iterable)
            except StopIteration:
                return

    while row := tuple(group(n, iterable)):
        yield row


def test_group_by_iter() -> None:
    rule = lambda x: x % 3 == 0 or x % 5 == 0
    actual = list(group_by_iter(7, filter(rule, range(1, 50))))
    expected = [
        (3, 5, 6, 9, 10, 12, 15),
        (18, 20, 21, 24, 25, 27, 30),
        (33, 35, 36, 39, 40, 42, 45),
        (48,),
    ]
    assert actual == expected


REPL_demo_group_by_iter = """
>>> from pprint import pprint
>>> data = list(
...     filter(lambda x: x % 3 == 0 or x % 5 == 0, range(1, 50))
... )
>>> data 
[3, 5, 6, 9, 10, ..., 48]
>>> grouped = list(group_by_iter(7, iter(data)))
>>> pprint(grouped)
[(3, 5, 6, 9, 10, 12, 15),
 (18, 20, 21, 24, 25, 27, 30),
 (33, 35, 36, 39, 40, 42, 45),
 (48,)]
"""


from collections.abc import Callable, Iterator, Iterable
from typing import Any, TypeAlias

ItemFilterPredicate: TypeAlias = Callable[[Any], bool]


def group_filter_iter(
    n: int, predicate: ItemFilterPredicate, items: Iterator[ItemT]
) -> Iterator[tuple[ItemT, ...]]:
    def group(n: int, iterable: Iterator[ItemT]) -> Iterator[ItemT]:
        for i in range(n):
            try:
                yield next(iterable)
            except StopIteration:
                return

    subset = filter(predicate, items)
    # ^-- Added this to apply the filter
    while row := tuple(group(n, subset)):
        # ^-- Changed to use the filter
        yield row


from typing import cast


def test_group_filter_iter() -> None:
    rule: ItemFilterPredicate = lambda x: cast(bool, x % 3 == 0 or x % 5 == 0)
    actual: list[tuple[int, ...]] = list(group_filter_iter(7, rule, iter(range(1, 50))))
    expected = [
        (3, 5, 6, 9, 10, 12, 15),
        (18, 20, 21, 24, 25, 27, 30),
        (33, 35, 36, 39, 40, 42, 45),
        (48,),
    ]
    assert actual == expected


REPL_compare_group = """
>>> rule: ItemFilterPredicate = lambda x: x % 3 == 0 or x % 5 == 0
>>> groups_explicit = list(
...    group_by_iter(7, filter(rule, range(1, 50)))
... )
>>> groups = list(
...     group_filter_iter(7, rule, iter(range(1, 50)))
... )
>>> assert groups == groups_explicit
"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
