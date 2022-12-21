"""Functional Python Programming 3e

Chapter 10, Example Set 3
"""

from functools import partial


def performance() -> None:
    import timeit
    from textwrap import dedent

    partial_time = timeit.timeit(
        """exp2(12)""",
        setup=dedent(
            """
            from functools import partial
            exp2 = partial(pow, 2)
        """
        ),
    )

    lambda_time = timeit.timeit("""exp2(12)""", setup="""exp2 = lambda y: pow(2, y)""")
    print(f"partial {partial_time:.3f}")
    print(f"lambda  {lambda_time:.3f}")


REPL_correctness = """
>>> exp2 = partial(pow, 2)
>>> exp2(12)
4096
>>> exp2(17)-1
131071

>>> exp2 = partial(pow, 2)
>>> exp2(12)
4096
>>> exp2(17)-1
131071

>>> exp2 = lambda y: pow(2, y)

>>> exp2 = lambda y: pow(2, y)
>>> exp2(12)
4096
>>> exp2(17)-1
131071
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}

if __name__ == "__main__":
    performance()
