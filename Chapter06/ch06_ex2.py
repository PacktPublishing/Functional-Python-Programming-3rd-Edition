"""Functional Python Programming 3e

Chapter 6, Example Set 2
"""

from typing import Iterator, TypeAlias

Point: TypeAlias = tuple[float, float]


def syntax_check_1(trip: list[tuple[Point, Point, float]]) -> Iterator[float]:
    quantized = (5 * (dist // 5) for start, stop, dist in trip)
    return quantized


def syntax_check_2(trip: list[tuple[Point, Point, float]]) -> Iterator[float]:
    quantized = (5 * (dist // 5) for _, _, dist in trip)
    return quantized


def test_syntax_check_1() -> None:
    data = [((d, d), (d, d), d) for d in map(float, range(10))]
    q = list(syntax_check_1(data))
    assert q == [0, 0, 0, 0, 0, 5, 5, 5, 5, 5]


def test_syntax_check_2() -> None:
    data = [((d, d), (d, d), d) for d in map(float, range(10))]
    q = list(syntax_check_2(data))
    assert q == [0, 0, 0, 0, 0, 5, 5, 5, 5, 5]


REPL_quantized = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...    path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip = tuple((start, end, round(haversine(start, end),4))
...        for start, end in legs(path))

>>> len(trip)
73

# See Chapter 4 for ways to parse "file:./Winter%202012-2013.kml"
# We want to build a trip variable with the sequence of tuples

>>> from collections import Counter

>>> quantized = (5 * (dist // 5) for start, stop, dist in trip)
>>> summary = Counter(quantized)

>>> summary.most_common()
[(30.0, 15), (15.0, 9), ...]

>>> summary.most_common()
[(30.0, 15), (15.0, 9), ...]
"""


from collections.abc import Iterable
from typing import Any, TypeVar, Protocol, TypeAlias


class Comparable(Protocol):
    def __lt__(self, __other: Any) -> bool:
        ...

    def __gt__(self, __other: Any) -> bool:
        ...


SupportsRichComparisonT = TypeVar("SupportsRichComparisonT", bound=Comparable)

Leg: TypeAlias = tuple[Any, Any, float]


def group_sort(trip: Iterable[Leg]) -> dict[int, int]:
    def group(
        data: Iterable[SupportsRichComparisonT],
    ) -> Iterable[tuple[SupportsRichComparisonT, int]]:
        sorted_data = iter(sorted(data))
        previous, count = next(sorted_data), 1
        for d in sorted_data:
            if d == previous:
                count += 1
            else:
                yield previous, count
                previous, count = d, 1
        yield previous, count

    quantized = (int(5 * (dist // 5)) for beg, end, dist in trip)
    return dict(group(quantized))


def test_group_sort() -> None:
    trip = [
        (("s1",), ("e1",), 11),
        (("s2",), ("e2,"), 32),
        (("s3",), ("e3",), 23),
        (("s4",), ("e4",), 12),
    ]
    actual = group_sort(trip)
    assert actual == {10: 2, 20: 1, 30: 1}


REPL_head_tail = """
>>> C = [1,2,3,4,5]
>>> head, *tail = C
>>> head
1
>>> tail
[2, 3, 4, 5]
"""

from collections import defaultdict
from collections.abc import Callable, Sequence, Hashable
from typing import TypeVar

SeqItemT = TypeVar("SeqItemT")
ItemKeyT = TypeVar("ItemKeyT", bound=Hashable)


def group_by(
    key: Callable[[SeqItemT], ItemKeyT], data: Sequence[SeqItemT]
) -> dict[ItemKeyT, list[SeqItemT]]:
    def group_into(
        key: Callable[[SeqItemT], ItemKeyT],
        collection: Sequence[SeqItemT],
        group_dict: dict[ItemKeyT, list[SeqItemT]],
    ) -> dict[ItemKeyT, list[SeqItemT]]:
        if len(collection) == 0:
            return group_dict
        head, *tail = collection
        group_dict[key(head)].append(head)
        return group_into(key, tail, group_dict)

    return group_into(key, data, defaultdict(list))


def test_group_by() -> None:
    from Chapter04.ch04_ex1 import float_lat_lon, row_iter_kml, haversine, legs
    import urllib.request

    source_url = "file:./Winter%202012-2013.kml"
    with urllib.request.urlopen(source_url) as source:
        path = float_lat_lon(row_iter_kml(source))
        trip = tuple(
            (start, end, round(haversine(start, end), 4)) for start, end in legs(path)
        )

    binned_distance = lambda leg: 5 * (leg[2] // 5)
    by_distance = group_by(binned_distance, trip)
    summary = list(
        (distance, len(by_distance[distance])) for distance in sorted(by_distance)
    )
    assert summary == [
        (0.0, 4),
        (5.0, 5),
        (10.0, 5),
        (15.0, 9),
        (20.0, 5),
        (25.0, 5),
        (30.0, 15),
        (35.0, 5),
        (40.0, 3),
        (45.0, 3),
        (50.0, 3),
        (55.0, 1),
        (60.0, 3),
        (65.0, 1),
        (70.0, 2),
        (80.0, 1),
        (85.0, 1),
        (115.0, 1),
        (125.0, 1),
    ]


REPL_group_by = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...    path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip = tuple((start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> binned_distance = lambda leg: 5 * (leg[2] // 5)
>>> by_distance = group_by(binned_distance, trip)

>>> import pprint
>>> for distance in sorted(by_distance):
...     print(distance)
...     pprint.pprint(by_distance[distance])
0.0
[((35.505665, -76.653664), (35.508335, -76.654999), 0.1731),
 ((35.028175, -76.682495), (35.031334, -76.682663), 0.1898),
 ((25.4095, -77.910164), (25.425833, -77.832664), 4.3155),
 ((25.0765, -77.308167), (25.080334, -77.334), 1.4235)]
5.0
[((38.845501, -76.537331), (38.992832, -76.451332), 9.7151),
 ((34.972332, -76.585167), (35.028175, -76.682495), 5.8441),
 ((30.717167, -81.552498), (30.766333, -81.471832), 5.103),
 ((25.471333, -78.408165), (25.504833, -78.232834), 9.7128),
 ((23.9555, -76.31633), (24.099667, -76.401833), 9.844)]
...
125.0
[((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)]
"""


from collections import defaultdict
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

SeqT = TypeVar("SeqT")
KeyT = TypeVar("KeyT", bound=Hashable)


def partition(
    key: Callable[[SeqT], KeyT], data: Iterable[SeqT]
) -> dict[KeyT, list[SeqT]]:
    group_dict = defaultdict(list)
    for head in data:
        group_dict[key(head)].append(head)
        # ---------------------------------
    return group_dict


def test_partition() -> None:
    from Chapter04.ch04_ex1 import float_lat_lon, row_iter_kml, haversine, legs
    import urllib.request

    source_url = "file:./Winter%202012-2013.kml"
    with urllib.request.urlopen(source_url) as source:
        path = float_lat_lon(row_iter_kml(source))
        trip = tuple(
            (start, end, round(haversine(start, end), 4)) for start, end in legs(path)
        )

    binned_distance = lambda leg: 5 * (leg[2] // 5)
    by_distance = partition(binned_distance, trip)
    summary = list(
        (distance, len(by_distance[distance])) for distance in sorted(by_distance)
    )
    assert summary == [
        (0.0, 4),
        (5.0, 5),
        (10.0, 5),
        (15.0, 9),
        (20.0, 5),
        (25.0, 5),
        (30.0, 15),
        (35.0, 5),
        (40.0, 3),
        (45.0, 3),
        (50.0, 3),
        (55.0, 1),
        (60.0, 3),
        (65.0, 1),
        (70.0, 2),
        (80.0, 1),
        (85.0, 1),
        (115.0, 1),
        (125.0, 1),
    ]


# Legs are (start, end, distance) tuples

start = lambda s, e, d: s

end = lambda s, e, d: e

dist = lambda s, e, d: d

# start and end of a Leg are (lat, lon) tuples

latitude = lambda lat, lon: lat

longitude = lambda lat, lon: lon


REPL_test_extractors = """
>>> point = ((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
>>> start(*point)
(35.505665, -76.653664)

>>> end(*point)
(35.508335, -76.654999)

>>> dist(*point)
0.1731

>>> latitude(*start(*point))
35.505665
"""


REPL_test_sorted_max = """
>>> from Chapter04.ch04_ex1 import (
...    floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...    path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip = tuple((start, end, round(haversine(start, end),4))
...        for start, end in legs(path))

>>> binned_distance = lambda leg: 5 * (leg[2] // 5)
>>> by_distance = partition(binned_distance, trip)
>>> for distance in sorted(by_distance):
...     print(
...         distance,
...         max(by_distance[distance],
...         key=lambda pt: latitude(*start(*pt)))
...     )
0.0 ((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
5.0 ((38.845501, -76.537331), (38.992832, -76.451332), 9.7151)
10.0 ((36.444168, -76.3265), (36.297501, -76.217834), 10.2537)
...
125.0 ((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)

>>> binned_distance = lambda leg: 5 * (leg[2] // 5)
>>> by_distance = partition(binned_distance, trip)
>>> for distance in sorted(by_distance):
...     print(
...         distance,
...         max(by_distance[distance],
...         key=lambda pt: latitude(*start(*pt)))
...     )
0.0 ((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
5.0 ((38.845501, -76.537331), (38.992832, -76.451332), 9.7151)
10.0 ((36.444168, -76.3265), (36.297501, -76.217834), 10.2537)
15.0 ((37.840332, -76.27417), (37.547165, -76.32917), 17.7944)
20.0 ((37.547165, -76.32917), (37.181168, -76.411499), 22.3226)
25.0 ((36.297501, -76.217834), (35.935501, -75.939331), 25.5897)
30.0 ((38.331501, -76.459503), (38.845501, -76.537331), 31.0756)
35.0 ((38.992832, -76.451332), (38.331165, -76.459167), 39.7277)
40.0 ((36.843334, -76.298668), (37.549, -76.331169), 42.3962)
45.0 ((37.549, -76.331169), (38.330166, -76.458504), 47.2866)
50.0 ((33.276833, -78.979332), (32.832169, -79.93383), 54.9528)
55.0 ((31.1595, -81.421997), (31.9105, -80.780998), 55.7582)
60.0 ((29.887167, -81.30883), (29.050501, -80.651169), 60.8693)
65.0 ((31.671333, -80.933167), (30.717167, -81.552498), 65.5252)
70.0 ((31.9105, -80.780998), (32.83248254681784, -79.93379468285697), 70.0694)
80.0 ((34.204666, -77.800499), (33.276833, -78.979332), 81.0363)
85.0 ((32.832169, -79.93383), (31.671333, -80.933167), 86.2095)
115.0 ((29.050501, -80.651169), (27.186001, -80.139503), 115.1751)
125.0 ((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
"""


from collections.abc import Sequence


def sum_x0(data: Sequence[float]) -> float:
    return sum(1 for x in data)  # or len(data)


def sum_x1(data: Sequence[float]) -> float:
    return sum(x for x in data)  # or sum(data)


def sum_x2(data: Sequence[float]) -> float:
    return sum(x * x for x in data)


from collections.abc import Callable, Iterable
from typing import Any


def sum_f(function: Callable[[Any], float], data: Iterable[float]) -> float:
    return sum(function(x) for x in data)


REPL_sum_f = """
>>> data = [7.46, 6.77, 12.74, 7.11, 7.81,
...     8.84, 6.08, 5.39, 8.15, 6.42, 5.73]

>>> N = sum_f(lambda x: 1, data)  # x**0
>>> N
11
>>> S = sum_f(lambda x: x, data)  # x**1
>>> round(S, 2)
82.5
>>> S2 = sum_f(lambda x: x*x, data)  # x**2
>>> round(S2, 4)
659.9762
"""

from collections.abc import Callable, Iterable


def sum_filter_f(
    filter_f: Callable[[float], bool],
    function: Callable[[float], float],
    data: Iterable[float],
) -> float:
    return sum(function(x) for x in data if filter_f(x))


valid = lambda x: x is not None


def mean_f(predicate: Callable[[Any], bool], data: Sequence[float]) -> float:
    count_ = lambda x: 1
    sum_ = lambda x: x
    N = sum_filter_f(valid, count_, data)
    S = sum_filter_f(valid, sum_, data)
    return S / N


from pytest import approx
from typing import cast


def test_mean_f() -> None:
    data_1 = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]
    assert sum_x0(data_1) == 11
    assert sum_x1(data_1) == approx(82.5)
    assert sum_x2(data_1) == approx(659.9762)
    assert mean_f(lambda x: True, data_1) == approx(7.5)

    data_2: list[Any] = [None, None] + data_1[:5] + [None] + data_1[5:] + [None, None, None]  # type: ignore [operator]
    assert mean_f(lambda x: x is not None, data_2) == approx(7.5)


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
