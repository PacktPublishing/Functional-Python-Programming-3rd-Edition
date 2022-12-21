"""Functional Python Programming 3e

Chapter 9, Example Set 2

An example of an optimization problem:

https://utw11041.utweb.utexas.edu/ORMM/models/unit/combinatorics/permute.html

"""

import csv
import io

# Cost data
cost_data = """\
14,11,6,20,12,9,4
15,28,34,4,12,24,21
16,31,22,18,31,15,23
20,18,9,15,30,4,18
24,8,24,30,28,25,4
3,23,22,11,5,30,5
13,7,5,10,7,7,32
"""


def get_cost_matrix() -> list[tuple[int, ...]]:
    with io.StringIO(cost_data) as source:
        rdr = csv.reader(source)
        cost = list(tuple(map(int, row)) for row in rdr)
    return cost


from itertools import permutations


def assignment(cost: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    n_tasks = len(cost)
    perms = permutations(range(n_tasks))
    alt = [
        (sum(cost[task][agent] for agent, task in enumerate(perm)), perm)
        for perm in perms
    ]
    m = min(alt)[0]
    return [ans for s, ans in alt if s == m]


REPL_assignment = """
>>> from pprint import pprint
>>> cost = get_cost_matrix()
>>> len(cost)
7
>>> pprint(cost)
[(14, 11, 6, 20, 12, 9, 4),
 (15, 28, 34, 4, 12, 24, 21),
 (16, 31, 22, 18, 31, 15, 23),
 (20, 18, 9, 15, 30, 4, 18),
 (24, 8, 24, 30, 28, 25, 4),
 (3, 23, 22, 11, 5, 30, 5),
 (13, 7, 5, 10, 7, 7, 32)]

>>> solutions = assignment(cost)
>>> pprint(solutions)
[(2, 4, 6, 1, 5, 3, 0), (2, 6, 0, 1, 5, 3, 4)]

The original example was 1-based, so we subtract 1 from each assignment...
>>> expected = tuple(map(lambda x:x-1, [3,5,7,2,6,4,1] ) )
>>> expected
(2, 4, 6, 1, 5, 3, 0)
>>> expected in solutions
True
"""


def performance() -> None:
    """Takes almost 1 minute."""
    import timeit

    perf = timeit.timeit(
        """list(permutations(range(10)))""",
        """from itertools import permutations""",
        number=100,
    )

    print(f"10! hands in {perf/100:.3f} seconds")


REPL_combinations = """
>>> from itertools import combinations, product

>>> hands = list(
...     combinations(
...         tuple(
...             product(range(13), '♠♥♦♣')
...         ), 5
...     )
... )

>>> hands = list(
...     combinations( 
...         tuple(
...             product(range(13),'♠♥♦♣')
...         ), 5
...     )
... )
>>> print(len(hands))
2598960
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}


if __name__ == "__main__":
    performance()
