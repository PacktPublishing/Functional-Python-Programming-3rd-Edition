"""Functional Python Programming 3e

Chapter 1, Example Set 3
"""

import math


def distance(
    lat1: float, lon1: float, lat2: float, lon2: float, R: float = 360 * 60 / math.tau
) -> float:
    """Equirectangular, 'flat-earth' distance."""
    Δφ = math.radians(lat1) - math.radians(lat2)
    Δλ = math.radians(lon1) - math.radians(lon2)
    mid_φ = (math.radians(lat1) + math.radians(lat2)) / 2
    x = R * Δλ * math.cos(mid_φ)
    y = R * Δφ
    return math.hypot(x, y)


def redundant(
    lat1: float, lon1: float, lat2: float, lon2: float, R: float = 360 * 60 / math.tau
) -> float:
    d = math.hypot(
        R
        * (math.radians(lon1) - math.radians(lon2))
        * math.cos((math.radians(lat1) + math.radians(lat2)) / 2),
        R * (math.radians(lat1) - math.radians(lat2)),
    )
    return d


def imperative(
    lat_1: float,
    lon_1: float,
    lat_2: float,
    lon_2: float,
    R: float = 360 * 60 / math.tau,
) -> float:
    rlat_1 = math.radians(lat_1)
    rlat_2 = math.radians(lat_2)
    dlat = rlat_1 - rlat_2
    rlon_1 = math.radians(lon_1)
    rlon_2 = math.radians(lon_2)
    dlon = rlon_1 - rlon_2
    lat_m = rlat_1 + rlat_2
    lat_m = lat_m / 2
    c = math.cos(lat_m)
    x = R * dlon
    x = x * c
    y = R * dlat
    x2 = x ** 2
    y2 = y ** 2
    x2y2 = x2 + y2
    d = math.sqrt(x2y2)
    return d


from pytest import approx


def test_distance_imperative() -> None:
    assert distance(32.82950, -79.93021, 32.74412, -79.85226) == approx(
        6.4577, rel=1e-4
    )
    assert imperative(32.82950, -79.93021, 32.74412, -79.85226) == approx(
        6.4577, rel=1e-4
    )
    assert redundant(32.82950, -79.93021, 32.74412, -79.85226) == approx(
        6.4577, rel=1e-4
    )
