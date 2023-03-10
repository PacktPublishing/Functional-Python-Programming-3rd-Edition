"""Functional Python Programming 3e

Chapter 11, Example Set 3
"""

from bs4 import BeautifulSoup  # type: ignore[import]
import urllib.request
from collections.abc import Iterator


def html_data_iter(url: str) -> Iterator[str]:
    with urllib.request.urlopen(url) as page:
        soup = BeautifulSoup(page.read(), "html.parser")
        data = soup.html.body.table.table
        for subtable in data.table:
            for c in subtable.children:
                yield c.text


# Raw data from the internet
# s7 = list(html_data_iter( "http://www.tylervigen.com/view_correlation?id=7" ))
# s3890 = list(html_data_iter( "http://www.tylervigen.com/view_correlation?id=3890" ))
# s97 = list(html_data_iter( "http://www.tylervigen.com/view_correlation?id=97" ))
# s43 = list(html_data_iter( "http://www.tylervigen.com/view_correlation?id=43" ))

# These save some download and HTML parse bandwidth
s7 = [
    "",
    "2000",
    "2001",
    "2002",
    "2003",
    "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "",
    "Per capita consumption of cheese (US)Pounds (USDA)",
    "29.8",
    "30.1",
    "30.5",
    "30.6",
    "31.3",
    "31.7",
    "32.6",
    "33.1",
    "32.7",
    "32.8",
    "",
    "Number of people who died by becoming tangled in their bedsheetsDeaths (US) (CDC)",
    "327",
    "456",
    "509",
    "497",
    "596",
    "573",
    "661",
    "741",
    "809",
    "717",
    "",
    "Correlation: 0.947091",
]
s3890 = [
    "",
    "2000",
    "2001",
    "2002",
    "2003",
    "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "",
    "Per capita consumption of mozzarella cheese (US)Pounds (USDA)",
    "9.3",
    "9.7",
    "9.7",
    "9.7",
    "9.9",
    "10.2",
    "10.5",
    "11",
    "10.6",
    "10.6",
    "",
    "Civil engineering doctorates awarded (US)Degrees awarded (National Science Foundation)",
    "480",
    "501",
    "540",
    "552",
    "547",
    "622",
    "655",
    "701",
    "712",
    "708",
    "",
    "Correlation: 0.958648",
]
s97 = [
    "",
    "2000",
    "2001",
    "2002",
    "2003",
    "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "",
    "Total revenue generated by arcades (US)Dollars in millions (US Census)",
    "1,196",
    "1,176",
    "1,269",
    "1,240",
    "1,307",
    "1,435",
    "1,601",
    "1,654",
    "1,803",
    "1,734",
    "",
    "Computer science doctorates awarded (US)Degrees awarded (National Science Foundation)",
    "861",
    "830",
    "809",
    "867",
    "948",
    "1,129",
    "1,453",
    "1,656",
    "1,787",
    "1,611",
    "",
    "Correlation: 0.985065",
]
s43 = [
    "",
    "2000",
    "2001",
    "2002",
    "2003",
    "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "",
    "US crude oil imports from VenezuelaMillions of barrels (Dept. of Energy)",
    "446",
    "471",
    "438",
    "436",
    "473",
    "449",
    "416",
    "420",
    "381",
    "352",
    "",
    "Per capita consumption of high fructose corn syrup (US)Pounds (USDA)",
    "62.6",
    "62.5",
    "62.8",
    "60.9",
    "59.8",
    "59.1",
    "58.2",
    "56.1",
    "53",
    "50.1",
    "",
    "Correlation: 0.884883",
]

REPL_partition_1 = """
>>> from toolz.itertoolz import partition, interleave

>>> data_iter = partition(3, interleave(partition(12, s7)))
>>> data = list(data_iter)

>>> from pprint import pprint
>>> pprint(data)
[('',
  'Per capita consumption of cheese (US)Pounds (USDA)',
  'Number of people who died by becoming tangled in their bedsheetsDeaths (US) '
  '(CDC)'),
 ('2000', '29.8', '327'),
 ('2001', '30.1', '456'),
 ('2002', '30.5', '509'),
 ('2003', '30.6', '497'),
 ('2004', '31.3', '596'),
 ('2005', '31.7', '573'),
 ('2006', '32.6', '661'),
 ('2007', '33.1', '741'),
 ('2008', '32.7', '809'),
 ('2009', '32.8', '717'),
 ('', '', '')]
"""

from toolz.itertoolz import cons, drop  # type: ignore[import]
from toolz.recipes import partitionby  # type: ignore[import]

ROW_COUNT = 0


def row_counter(item: str) -> int:
    global ROW_COUNT
    rc = ROW_COUNT
    if item == "":
        ROW_COUNT += 1
    return rc


REPL_partition_2 = """
>>> year_fixup = cons("year", drop(1, s7))
>>> year, series_1, series_2, extra = list(partitionby(row_counter, year_fixup))
>>> data = list(zip(year, series_1, series_2))

>>> from pprint import pprint
>>> pprint(data)
[('year',
  'Per capita consumption of cheese (US)Pounds (USDA)',
  'Number of people who died by becoming tangled in their bedsheetsDeaths (US) '
  '(CDC)'),
 ('2000', '29.8', '327'),
 ('2001', '30.1', '456'),
 ('2002', '30.5', '509'),
 ('2003', '30.6', '497'),
 ('2004', '31.3', '596'),
 ('2005', '31.7', '573'),
 ('2006', '32.6', '661'),
 ('2007', '33.1', '741'),
 ('2008', '32.7', '809'),
 ('2009', '32.8', '717'),
 ('', '', '')]
"""

from toolz.itertoolz import cons, drop
from toolz.recipes import partitionby


def make_samples(source: list[str]) -> list[dict[str, float]]:
    # Drop the first "" and prepend "year"
    year_fixup = cons("year", drop(1, source))
    # Restructure to 12 groups of 3
    year, series_1, series_2, extra = list(partitionby(row_counter, year_fixup))
    # Drop the first and the (empty) last
    samples = [
        {"year": int(year), "series_1": float(series_1), "series_2": float(series_2)}
        for year, series_1, series_2 in drop(1, zip(year, series_1, series_2))
        if year
    ]
    return samples


def test_make_samples() -> None:
    s7 = [
        "",
        "2000",
        "2001",
        "2002",
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "",
        "Per capita consumption of cheese (US)Pounds (USDA)",
        "29.8",
        "30.1",
        "30.5",
        "30.6",
        "31.3",
        "31.7",
        "32.6",
        "33.1",
        "32.7",
        "32.8",
        "",
        "Number of people who died by becoming tangled in their bedsheetsDeaths (US) (CDC)",
        "327",
        "456",
        "509",
        "497",
        "596",
        "573",
        "661",
        "741",
        "809",
        "717",
        "",
        "Correlation: 0.947091",
    ]
    s = make_samples(s7)
    assert s == [
        {"series_1": 29.8, "series_2": 327.0, "year": 2000},
        {"series_1": 30.1, "series_2": 456.0, "year": 2001},
        {"series_1": 30.5, "series_2": 509.0, "year": 2002},
        {"series_1": 30.6, "series_2": 497.0, "year": 2003},
        {"series_1": 31.3, "series_2": 596.0, "year": 2004},
        {"series_1": 31.7, "series_2": 573.0, "year": 2005},
        {"series_1": 32.6, "series_2": 661.0, "year": 2006},
        {"series_1": 33.1, "series_2": 741.0, "year": 2007},
        {"series_1": 32.7, "series_2": 809.0, "year": 2008},
        {"series_1": 32.8, "series_2": 717.0, "year": 2009},
    ]


REPL_correlate = """
from bs4 import BeautifulSoup  # type: ignore[import]
import urllib.request
from collections.abc import Iterator

def html_data_iter(url: str) -> Iterator[str]:
    with urllib.request.urlopen(url) as page:
        soup = BeautifulSoup(page.read(), 'html.parser')
        data = soup.html.body.table.table
        for subtable in data.table:
            for c in subtable.children:
                yield c.text

>>> from toolz.dicttoolz import get_in
>>> from Chapter04.ch04_ex4 import corr

>>> samples = make_samples(s7)
>>> s_1 = [get_in(['series_1'], s) for s in samples]
>>> s_2 = [get_in(['series_2'], s) for s in samples]
>>> round(corr(s_1, s_2), 6)
0.947091
"""

REPL_curry = """
>>> from toolz.functoolz import curry
>>> def some_model(a: float, b: float, x: float) -> float:
...     return x**a * b

>>> curried_model = curry(some_model)
>>> cm_a = curried_model(1.0134)
>>> cm_ab = cm_a(0.7724)
>>> expected = cm_ab(1500)
>>> round(expected, 2)
1277.89
"""

REPL_compose = """
>>> from toolz.itertoolz import interleave, partition, drop
>>> from toolz.functoolz import compose, curry
>>> steps = [
...     curry(partition, 3),
...     interleave,
...     curry(partition, 12),
... ]
>>> xform = compose(*steps)
>>> data = list(xform(s7))

>>> from pprint import pprint
>>> pprint(data)  # doctest+ ELLIPSIS
[('',
  'Per capita consumption of cheese (US)Pounds (USDA)',
  'Number of people who died by becoming tangled in their bedsheetsDeaths (US) '
  '(CDC)'),
 ('2000', '29.8', '327'),
...
 ('2009', '32.8', '717'),
 ('', '', '')]
"""

REPL_pipe = """
>>> from toolz.itertoolz import interleave, partition, drop
>>> from toolz.functoolz import pipe, curry

>>> data_iter = pipe(s7, curry(partition, 12), interleave, curry(partition, 3))
>>> data = list(data_iter)

>>> from pprint import pprint
>>> pprint(data)  # doctext: +ELLIPSIS
[('',
  'Per capita consumption of cheese (US)Pounds (USDA)',
  'Number of people who died by becoming tangled in their bedsheetsDeaths (US) '
  '(CDC)'),
 ('2000', '29.8', '327'),
...
 ('2009', '32.8', '717'),
 ('', '', '')]
"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
