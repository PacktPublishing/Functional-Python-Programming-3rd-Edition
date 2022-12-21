"""Functional Python Programming 3e

Chapter 16, Example Set 2

See  http://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm
"""

# Original data from the NIST handbook.
# Three rows for each shift.
# Four columns for each defect.
expected_defects = [
    [15, 21, 45, 13],
    [26, 31, 34, 5],
    [33, 17, 49, 20],
]

# Raw data reader.

from typing import TextIO, NamedTuple, TypeAlias
import csv
from collections import Counter


class Defect(NamedTuple):
    shift: str  # domain is '1', '2', '3'
    defect_type: str
    serial_number: str


Shift_Type: TypeAlias = tuple[str, str]


def defect_reduce(input_file: TextIO) -> Counter[Shift_Type]:
    rdr = csv.DictReader(input_file)
    defect_iter = (Defect(**row) for row in rdr)
    shift_type_iter = (
        (row.shift, row.defect_type) for row in defect_iter if row.defect_type
    )
    tally = Counter(shift_type_iter)
    return tally


REPL_defect_reduce = """
>>> from pathlib import Path

>>> source_path = Path.cwd() / "qa_data.csv"
>>> with source_path.open() as input:
...     defect_counts = defect_reduce(input)
>>> from pprint import pprint

>>> pprint(defect_counts)
Counter({('3', 'C'): 49,
         ('1', 'C'): 45,
         ('2', 'C'): 34,
         ('3', 'A'): 33,
         ('2', 'B'): 31,
         ('2', 'A'): 26,
         ('1', 'B'): 21,
         ('3', 'D'): 20,
         ('3', 'B'): 17,
         ('1', 'A'): 15,
         ('1', 'D'): 13,
         ('2', 'D'): 5})
"""


from collections.abc import Callable
from typing import TypeAlias

ShiftDefect: TypeAlias = tuple[str, str]
SourceCounter: TypeAlias = Counter[ShiftDefect]


def summarize_by(
    subset_key: Callable[[ShiftDefect], str], source: SourceCounter
) -> Counter[str]:
    grouped_iter = (Counter({subset_key(k): v}) for k, v in source.items())
    return sum(grouped_iter, Counter())


REPL_summarize_by = """
>>> from pathlib import Path

>>> source_path = Path.cwd() / "qa_data.csv"
>>> with source_path.open() as input:
...     defect_counts = defect_reduce(input)
>>> from pprint import pprint

>>> pprint(defect_counts)
Counter({('3', 'C'): 49,
         ('1', 'C'): 45,
         ('2', 'C'): 34,
         ('3', 'A'): 33,
         ('2', 'B'): 31,
         ('2', 'A'): 26,
         ('1', 'B'): 21,
         ('3', 'D'): 20,
         ('3', 'B'): 17,
         ('1', 'A'): 15,
         ('1', 'D'): 13,
         ('2', 'D'): 5})

>>> total = sum(defect_counts.values())
>>> total
309

>>> shift_totals = summarize_by(lambda s_d: s_d[0], defect_counts)
>>> type_totals = summarize_by(lambda s_d: s_d[1], defect_counts)

>>> shift_totals
Counter({'3': 119, '2': 96, '1': 94})
>>> type_totals
Counter({'C': 128, 'A': 74, 'B': 69, 'D': 38})
"""


from fractions import Fraction


def probability_by(
    subset_key: Callable[[ShiftDefect], str], source: SourceCounter
) -> dict[str, Fraction]:
    total = sum(source.values())
    sub_totals = summarize_by(subset_key, source)
    return {k: Fraction(sub_totals[k], total) for k in sub_totals}


REPL_fractions = """
>>> from pathlib import Path

>>> source_path = Path.cwd() / "qa_data.csv"
>>> with source_path.open() as input:
...     defect_counts = defect_reduce(input)

>>> P_shift = probability_by(lambda s_d: s_d[0], defect_counts)
>>> P_type = probability_by(lambda s_d: s_d[1], defect_counts)

>>> from pprint import pprint

>>> pprint(P_shift, width=64)
{'1': Fraction(94, 309),
 '2': Fraction(32, 103),
 '3': Fraction(119, 309)}

>>> pprint(P_type, width=64)
{'A': Fraction(74, 309),
 'B': Fraction(23, 103),
 'C': Fraction(128, 309),
 'D': Fraction(38, 309)}
"""


def expected(source: SourceCounter) -> dict[ShiftDefect, Fraction]:
    total = sum(source.values())
    P_shift = probability_by(lambda s_d: s_d[0], source)
    P_type = probability_by(lambda s_d: s_d[1], source)
    return {
        (s, t): P_shift[s] * P_type[t] * total
        for t in sorted(P_type)
        for s in sorted(P_shift)
    }


REPL_expected = """
>>> from pathlib import Path

>>> source_path = Path.cwd() / "qa_data.csv"
>>> with source_path.open() as input:
...     defect_counts = defect_reduce(input)

>>> from pprint import pprint

>>> pprint(expected(defect_counts))
{('1', 'A'): Fraction(6956, 309),
 ('1', 'B'): Fraction(2162, 103),
 ('1', 'C'): Fraction(12032, 309),
 ('1', 'D'): Fraction(3572, 309),
 ('2', 'A'): Fraction(2368, 103),
 ('2', 'B'): Fraction(2208, 103),
 ('2', 'C'): Fraction(4096, 103),
 ('2', 'D'): Fraction(1216, 103),
 ('3', 'A'): Fraction(8806, 309),
 ('3', 'B'): Fraction(2737, 103),
 ('3', 'C'): Fraction(15232, 309),
 ('3', 'D'): Fraction(4522, 309)}
"""

from rich.table import Table
from rich.console import Console


def contingency_table(
    expected: dict[ShiftDefect, Fraction], defect_counts: Counter[ShiftDefect]
) -> None:
    total = sum(defect_counts.values())
    shift_totals = summarize_by(lambda s_d: s_d[0], defect_counts)
    type_totals = summarize_by(lambda s_d: s_d[1], defect_counts)

    table = Table(title="Contingency Table")
    table.add_column("shift")
    for defect_type in sorted(type_totals):
        table.add_column(f"{defect_type} obs")
        table.add_column(f"{defect_type} exp")
    table.add_column("total")

    for s in sorted(shift_totals):
        row = [f"{s}"]
        for t in sorted(type_totals):
            row.append(f"{defect_counts[s,t]:3d}")
            row.append(f"{float(expected[s,t]):5.2f}")
        row.append(f"{shift_totals[s]:3d}")
        table.add_row(*row)

    footers = ["total"]
    for t in sorted(type_totals):
        footers.append(f"{type_totals[t]:3d}")
        footers.append("")
    footers.append(f"{total:3d}")
    table.add_row(*footers)

    console = Console()
    console.print(table)


REPL_contingency_table = """
>>> from pathlib import Path

>>> source_path = Path.cwd() / "qa_data.csv"
>>> with source_path.open() as input:
...     defect_counts = defect_reduce(input)


"""


def chi2(defect_counts: Counter[ShiftDefect]) -> Fraction:
    total = sum(defect_counts.values())
    shift_totals = summarize_by(lambda s_d: s_d[0], defect_counts)
    type_totals = summarize_by(lambda s_d: s_d[1], defect_counts)

    expected_counts = expected(defect_counts)

    diff_sq_e: Callable[[Fraction, int], Fraction] = lambda e, o: (e - o) ** 2 / e

    chi2 = sum(
        diff_sq_e(expected_counts[s, t], defect_counts[s, t])
        for s in shift_totals
        for t in type_totals
    )
    return Fraction(chi2)  # convert any int result to Fraction


REPL_chi2 = """
>>> from pathlib import Path

>>> source_path = Path.cwd() / "qa_data.csv"
>>> with source_path.open() as input:
...     defect_counts = defect_reduce(input)

>>> round(float(chi2(defect_counts)), 2)
19.18
>>> chi2(defect_counts).limit_denominator(20)
Fraction(326, 17)
"""


from Chapter16.ch16_ex3 import cdf
from pathlib import Path


def demo() -> None:
    source_path = Path.cwd() / "qa_data.csv"
    with source_path.open() as input_file:
        defect_counts = defect_reduce(input_file)

    contingency_table(expected(defect_counts), defect_counts)

    x2 = chi2(defect_counts)
    print(f"χ² = {float(x2):.2f}")
    print(f"χ² = {x2.limit_denominator(50)}, P = {float(cdf(x2, 6)):0.3%}")
    print(f"χ² = {x2.limit_denominator(100)}, P = {cdf(x2, 6).limit_denominator(1000)}")


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}

if __name__ == "__main__":
    demo()
