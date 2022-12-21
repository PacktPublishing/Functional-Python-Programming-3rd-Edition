"""Functional Python Programming 3e

Chapter 4, Example Set 3
"""

REPL_sum_len = """
>>> sum(())
0
>>> len(())
0
"""

from collections.abc import Sequence


def mean(items: Sequence[float]) -> float:
    return sum(items) / len(items)


def test_mean() -> None:
    d = [4, 36, 45, 50, 75]
    assert mean(d) == 42.0


import math
from collections.abc import Sequence


def stdev(data: Sequence[float]) -> float:

    s0 = len(data)  # sum(1 for x in data)
    s1 = sum(data)  # sum(x for x in data)
    s2 = sum(x**2 for x in data)

    mean = s1 / s0
    stdev = math.sqrt(s2 / s0 - mean**2)
    return stdev


def test_stdev() -> None:
    d = [2, 4, 4, 4, 5, 5, 7, 9]
    assert mean(d) == 5.0
    assert stdev(d) == 2.0


def z(x: float, m_x: float, s_x: float) -> float:
    return (x - m_x) / s_x


def test_z() -> None:
    d = [2, 4, 4, 4, 5, 5, 7, 9]
    assert list(z(x, mean(d), stdev(d)) for x in d) == [
        -1.5,
        -0.5,
        -0.5,
        -0.5,
        0.0,
        0.0,
        1.0,
        2.0,
    ]


REPL_test_mean_stdev_z = """
>>> d = [2, 4, 4, 4, 5, 5, 7, 9]
>>> list(z(x, mean(d), stdev(d)) for x in d)
[-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]
"""

REPL_filter_sorted = """
>>> from Chapter04.ch04_ex1 import (
...     floats_from_pair, float_lat_lon, row_iter_kml, legs,
...     haversine)
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path = floats_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip = tuple((start, end, round(haversine(start, end),4))
...        for start, end in legs(path))

>>> dist = lambda leg: leg[2]
>>> long = list(filter(lambda leg: dist(leg) >= 50, trip))
>>> len(long)
14
>>> long[0]
((34.204666, -77.800499), (33.276833, -78.979332), 81.0363)
>>> long[-1]
((31.9105, -80.780998), (32.83248254681784, -79.93379468285697), 70.0694)

>>> s1 = sorted(dist(x) for x in trip)
>>> s1[0]
0.1731
>>> s1[-1]
129.7748

>>> s2 = (sorted(trip, key=dist))
>>> s2[0]
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
>>> s2[-1]
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)

>>> from Chapter04.ch04_ex4 import mean, stdev, z

>>> dist_data = list(map(dist, trip))
>>> μ_d = mean(dist_data)
>>> σ_d = stdev(dist_data)
>>> print(f"Average leg {μ_d} with {σ_d=}, Z(0)={z(0, μ_d, σ_d)}")
Average leg 33.99131780821918 with σ_d=24.158473730346035, Z(0)=-1.407014291864054

>>> outlier = lambda leg: abs(z(dist(leg),μ_d,σ_d)) > 3
>>> print("Outliers", list(filter(outlier, trip)))
Outliers [((29.050501, -80.651169), (27.186001, -80.139503), 115.1751), ((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)]
"""

REPL_map = """
>>> from Chapter04.ch04_ex1 import (
...     floats_from_pair, float_lat_lon, row_iter_kml, haversine, legs
... )
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= tuple(floats_from_pair(float_lat_lon(row_iter_kml(source))))
...    trip= tuple((start, end, round(haversine(start, end),4))
...        for start, end in legs(iter(path)))

>>> distances1 = tuple(map(lambda s_e: (s_e[0], s_e[1], haversine(*s_e)),
...    zip(path, path[1:])))

>>> len(distances1)
73
>>> distances1[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.724564798884984)
>>> distances1[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.801864781785845)

>>> distances2 = tuple(map(lambda s, e: (s, e, haversine(s, e)), path, path[1:]))

>>> len(distances2)
73
>>> distances2[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.724564798884984)
>>> distances2[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.801864781785845)

"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
