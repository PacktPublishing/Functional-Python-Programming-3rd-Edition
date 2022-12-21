"""Functional Python Programming 3e

Chapter 16, Example Set 3
"""

from fractions import Fraction
from functools import lru_cache, reduce
import operator


@lru_cache(128)
def fact(k: int) -> int:
    if k < 2:
        return 1
    return reduce(operator.mul, range(2, int(k) + 1))


def test_fact() -> None:
    assert fact(1) == 1
    assert fact(2) == 2
    assert fact(3) == 6
    assert fact(4) == 24


from collections.abc import Iterator, Iterable, Callable
from fractions import Fraction
from typing import cast
import warnings


def gamma(s: Fraction | int, z: Fraction | int) -> Fraction:
    def terms(s: Fraction | int, z: Fraction | int) -> Iterator[Fraction]:
        """Terms for computing partial gamma"""
        for k in range(100):
            t2 = Fraction(z ** (s + k)) / (s + k)
            term = Fraction((-1) ** k, fact(k)) * t2
            yield term
        warnings.warn("More than 100 terms requested")

    def take_until(
        test_function: Callable[..., bool], source: Iterable[Fraction]
    ) -> Iterator[Fraction]:
        """Take from source until function is false."""
        for v in source:
            if test_function(v):
                return
            yield v

    ε = 1e-8
    insignificant: Callable[[Fraction], bool] = lambda t: abs(t) < ε
    g = sum(take_until(insignificant, terms(s, z)))
    # cast() from Union[Fraction, int] to Fraction
    return cast(Fraction, g)


from pytest import approx


def test_gamma() -> None:
    import math

    assert round(float(gamma(1, 2)), 7) == 0.8646647
    assert round(1 - math.exp(-2), 7) == 0.8646647
    assert round(float(gamma(1, 3)), 7) == 0.9502129
    assert round(1 - math.exp(-3), 7) == 0.9502129
    assert round(float(gamma(Fraction(1, 2), Fraction(2))), 7) == 1.6918067
    assert round(math.sqrt(math.pi) * math.erf(math.sqrt(2)), 7) == 1.6918067
    g = gamma(Fraction(1, 2), Fraction(2)).limit_denominator(1000000)
    assert g == Fraction(144438, 85375)
    assert round(float(g), 7) == 1.6918067


pi = Fraction(5_419_351, 1_725_033)
# Fraction(817_696_623, 260_280_919)

sqrt_pi = Fraction(677_622_787, 382_307_718)

from typing import Union


def Gamma_Half(k: Union[int, Fraction]) -> Fraction:
    match k:
        case int():
            g = Fraction(fact(k - 1), 1)
        case Fraction() if k.denominator == 1:
            g = Fraction(fact(k - 1), 1)
        case Fraction() if k.denominator == 2:
            n = k - Fraction(1, 2)
            g = fact(2 * n) / (Fraction(4**n) * fact(n)) * sqrt_pi
        case _:
            raise ValueError(f"Can't compute Γ({k})")
    return g


def test_gamma_half() -> None:
    import math

    assert Gamma_Half(2) == 1
    assert Gamma_Half(3) == 2
    assert Gamma_Half(4) == 6
    assert Gamma_Half(5) == 24

    g = Gamma_Half(Fraction(1, 2))  # Varies with sqrt_pi setting
    assert g.limit_denominator(2_000_000) == Fraction(582540, 328663)
    assert round(float(g), 7) == 1.7724539
    assert round(math.sqrt(math.pi), 7) == 1.7724539

    g = Gamma_Half(Fraction(3, 2))  # Varies with sqrt_pi setting
    assert g.limit_denominator(2_000_000) == Fraction(291270, 328663)
    assert round(float(g), 7) == 0.8862269
    assert round(math.sqrt(math.pi) / 2, 7) == 0.8862269


REPL_Gamma_Half = """
>>> g = Gamma_Half(Fraction(3, 2))
>>> g.limit_denominator(2_000_000)
Fraction(291270, 328663)
"""


def cdf(x: Union[Fraction, float], k: int) -> Fraction:
    """X² cumulative distribution function.

    :param x: X² value, sum (obs[i]-exp[i])**2/exp[i]}
        for parallel sequences of observed and expected values.
    :param k: degrees of freedom >= 1; often len(data)-1
    """

    return 1 - gamma(Fraction(k, 2), Fraction(x / 2)) / Gamma_Half(Fraction(k, 2))


def test_cdf() -> None:
    # From http://en.wikipedia.org/wiki/Chi-squared_distribution

    assert round(float(cdf(0.004, 1)), 2) == 0.95
    assert cdf(0.004, 1).limit_denominator(100) == Fraction(94, 99)
    assert round(float(cdf(10.83, 1)), 3) == 0.001
    assert cdf(10.83, 1).limit_denominator(1000) == Fraction(1, 1000)
    assert round(float(cdf(3.94, 10)), 2) == 0.95
    assert cdf(3.94, 10).limit_denominator(100) == Fraction(19, 20)
    assert round(float(cdf(29.59, 10)), 3) == 0.001
    assert cdf(29.59, 10).limit_denominator(10000) == Fraction(8, 8005)

    expected = [0.95, 0.90, 0.80, 0.70, 0.50, 0.30, 0.20, 0.10, 0.05, 0.01, 0.001]
    chi2 = [0.004, 0.02, 0.06, 0.15, 0.46, 1.07, 1.64, 2.71, 3.84, 6.64, 10.83]
    act = [round(float(x), 3) for x in map(cdf, chi2, [1] * len(chi2))]
    assert act == [0.95, 0.888, 0.806, 0.699, 0.498, 0.301, 0.2, 0.1, 0.05, 0.01, 0.001]

    # From http://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm

    assert round(float(cdf(19.18, 6)), 5) == 0.00387
    assert round(float(cdf(12.5916, 6)), 2) == 0.05
    assert cdf(19.18, 6).limit_denominator(1000) == Fraction(3, 775)

    # From http://www.itl.nist.gov/div898/handbook/prc/section4/prc46.htm

    assert round(float(cdf(12.131, 4)), 5) == 0.0164  # 0.01639 shown in reference
    assert cdf(12.131, 4).limit_denominator(1000) == Fraction(16, 975)
    assert round(float(cdf(9.488, 4)), 2) == 0.05
    assert cdf(9.488, 4).limit_denominator(1000) == Fraction(1, 20)


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
