"""Functional Python Programming 3e

Chapter 4, Example Set 4

Definitions of mean, stddev, Pearson correlation
and linear estimation.

http://en.wikipedia.org/wiki/Mean

http://en.wikipedia.org/wiki/Standard_deviation

http://en.wikipedia.org/wiki/Standard_score

http://en.wikipedia.org/wiki/Normalization_(statistics)

http://en.wikipedia.org/wiki/Simple_linear_regression
"""
from math import sqrt
from collections.abc import Sequence


def s0(samples: Sequence[float]) -> float:
    return sum(1 for x in samples)  # or len(data)


def s1(samples: Sequence[float]) -> float:
    return sum(x for x in samples)  # or sum(data)


def s2(samples: Sequence[float]) -> float:
    return sum(x * x for x in samples)


def test_s0_s1_s2() -> None:
    data = [2, 3, 5, 7]
    assert s0(data) == 4
    assert s1(data) == 17
    assert s2(data) == 87


from math import sqrt
from collections.abc import Sequence


def mean(samples: Sequence[float]) -> float:
    return s1(samples) / s0(samples)


def stdev(samples: Sequence[float]) -> float:
    N = s0(samples)
    return sqrt((s2(samples) / N) - (s1(samples) / N) ** 2)


def test_mean() -> None:
    d = [4, 36, 45, 50, 75]
    assert mean(d) == 42.0


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


REPL_test_z = """
>>> d = [2, 4, 4, 4, 5, 5, 7, 9]
>>> list(z(x, mean(d), stdev(d)) for x in d)
[-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]
"""


def corr(samples1: Sequence[float], samples2: Sequence[float]) -> float:
    m_1, s_1 = mean(samples1), stdev(samples1)
    m_2, s_2 = mean(samples2), stdev(samples2)
    z_1 = (z(x, m_1, s_1) for x in samples1)
    z_2 = (z(x, m_2, s_2) for x in samples2)
    r = sum(zx1 * zx2 for zx1, zx2 in zip(z_1, z_2)) / len(samples1)
    return r


from pytest import approx


def test_corr() -> None:
    xi = [
        1.47,
        1.50,
        1.52,
        1.55,
        1.57,
        1.60,
        1.63,
        1.65,
        1.68,
        1.70,
        1.73,
        1.75,
        1.78,
        1.80,
        1.83,
    ]
    yi = [
        52.21,
        53.12,
        54.48,
        55.84,
        57.20,
        58.57,
        59.93,
        61.29,
        63.11,
        64.47,
        66.28,
        68.10,
        69.92,
        72.19,
        74.46,
    ]
    assert corr(xi, yi) == approx(0.994583)


REPL_test_correlation = """
>>> xi = [1.47, 1.50, 1.52, 1.55, 1.57, 1.60, 1.63, 1.65,
... 1.68, 1.70, 1.73, 1.75, 1.78, 1.80, 1.83,]

>>> yi = [52.21,53.12,54.48,55.84,57.20,58.57,59.93,61.29,
... 63.11, 64.47, 66.28, 68.10, 69.92, 72.19, 74.46,]

>>> round(corr(xi, yi), 5)
0.99458
"""

from typing import Tuple


def linest(x_list: Sequence[float], y_list: Sequence[float]) -> Tuple[float, float]:
    """Linear Least-Squares Estimation.

    >>> xi= [1.47, 1.50, 1.52, 1.55, 1.57, 1.60, 1.63, 1.65,
    ...     1.68, 1.70, 1.73, 1.75, 1.78, 1.80, 1.83,] #  Height (m)
    >>> yi= [52.21, 53.12, 54.48, 55.84, 57.20, 58.57, 59.93, 61.29,
    ...     63.11, 64.47, 66.28, 68.10, 69.92, 72.19, 74.46,] #  Mass (kg)
    >>> assert len(xi) == len(yi)
    >>> alpha, beta = linest(xi, yi)
    >>> round(alpha,3)
    -39.062
    >>> round(beta,3)
    61.272
    """
    r_xy = corr(x_list, y_list)
    m_x, s_x = mean(x_list), stdev(x_list)
    m_y, s_y = mean(y_list), stdev(y_list)
    beta = r_xy * s_y / s_x
    alpha = m_y - beta * m_x
    return alpha, beta


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
