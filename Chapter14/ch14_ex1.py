"""Functional Python Programming 3e

Chapter 14, Example Set 1
"""
import math

# $
#     \Gamma(n) = \sqrt{2 \pi n} \left(\frac{n}{e}\right)^n
#     \left(
#       1 +
#       \frac{1}{(2^1)(6n)^1} +
#       \frac{1}{(2^3)(6n)^2} +
#       \frac{-139}{(2^3)(2\times 3\times 5)(6n)^3} +
#       \frac{-571}{(2^6)(2\times 3\times 5)(6n)^4}
#     \right)
# $


def some_function(n: float) -> float:
    """
    An approximation of the gamma function. A lot of work.
    """
    s: float = sum(
        (
            1,
            1 / ((2**1) * (6 * n) ** 1),
            1 / ((2**3) * (6 * n) ** 2),
            -139 / ((2**3) * (2 * 3 * 5) * (6 * n) ** 3),
            -571 / ((2**6) * (2 * 3 * 5) * (6 * n) ** 4),
        )
    )
    gamma: float = math.sqrt(2 * math.pi * n) * (n / math.e) ** n * s
    return gamma


def test_some_function() -> None:
    assert round(some_function(4), 3) == 24.0


def performance() -> None:
    import dis

    dis.disassemble(some_function.__code__)
    size = len(some_function.__code__.co_code)
    print(f"size {size} bytes")

    import timeit

    t = timeit.timeit(
        """some_function(4)""", """from Chapter14.ch14_ex1 import some_function"""
    )

    print(f"total time {t:.3f} sec. for 1,000,000 iterations")
    rate = 1_000_000 * size / t
    print(f"rate {rate:,.0f} bytecodes/sec")
    print(f"rate {rate/1_000_000:,.1f} Mbytes/sec")


if __name__ == "__main__":
    performance()
