"""Functional Python Programming 3e

Chapter 10, Flatten some NIST sample data.

"""
from collections.abc import Iterator
import csv
import io
from pprint import pprint
import random
from typing import TextIO, Any

raw_data = """\
Group 1	6.9	5.4	5.8	4.6	4.0
Group 2	8.3	6.8	7.8	9.2	6.5
Group 3	8.0	10.5	8.1	6.9	9.3
Group 4	5.8	3.8	6.1	5.6	6.2
"""


def row_iter_tab(source: TextIO) -> Iterator[list[str]]:
    rdr = csv.reader(source, delimiter="\t")
    return rdr


def pieces(grouped: list[list[str]]) -> Iterator[tuple[Any, float]]:
    for row in grouped:
        yield from ((row[0][-1], float(v)) for v in row[1:])


if __name__ == "__main__":
    source = io.StringIO(raw_data)
    grouped = list(row_iter_tab(source))
    data = list(pieces(grouped))
    random.shuffle(data)
    pprint(data)
