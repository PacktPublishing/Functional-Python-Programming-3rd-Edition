"""Functional Python Programming 3e

Chapter 9, Example Set 3

http://www.tylervigen.com/view_correlation?id=7

http://www.tylervigen.com/view_correlation?id=97

http://www.tylervigen.com/view_correlation?id=3890

http://www.tylervigen.com/view_correlation?id=43
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


from typing import Optional


def column_data(*data_sets: list[str]) -> Iterator[list[str]]:
    """
    >>> s7 = ['', '2000', '2001', '2002', '2003', '2004', '2005', '2006',
    ...    '2007', '2008', '2009', '',
    ...    'Per capita consumption of cheese (US)Pounds (USDA)',
    ...    '29.8', '30.1', '30.5', '30.6', '31.3', '31.7', '32.6', '33.1',
    ...    '32.7', '32.8', '',
    ...     'Number of people who died by becoming tangled in their bedsheets'
    ...     'Deaths (US) (CDC)', '327', '456', '509', '497', '596', '573',
    ...     '661', '741', '809', '717', '', 'Correlation: 0.947091']
    >>> list(column_data(s7))  # doctest: +NORMALIZE_WHITESPACE
    [['year', 'Per capita consumption of cheese (US)Pounds (USDA)',
      'Number of people who died by becoming tangled in their bedsheetsDeaths (US) (CDC)'],
     ['2000', '29.8', '327'], ['2001', '30.1', '456'], ['2002', '30.5', '509'],
     ['2003', '30.6', '497'], ['2004', '31.3', '596'], ['2005', '31.7', '573'],
     ['2006', '32.6', '661'], ['2007', '33.1', '741'], ['2008', '32.7', '809'],
     ['2009', '32.8', '717']]
    """

    def year_fixup(row: list[str]) -> list[str]:
        return list(c or "year" for c in row)

    row = list(ds[g * 12] for ds in data_sets for g in range(3))
    yield year_fixup(row)

    # Can be done with filter(None, ...), also.
    for i in range(1, 12):
        row = list(ds[g * 12 + i] for ds in data_sets for g in range(3))
        if any(row):
            yield row


def test_column_data() -> None:
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
        "Number of people who died by becoming tangled in their bedsheets"
        "Deaths (US) (CDC)",
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
    actual = list(column_data(s7))
    expected = [
        [
            "year",
            "Per capita consumption of cheese (US)Pounds (USDA)",
            "Number of people who died by becoming tangled in their bedsheetsDeaths (US) (CDC)",
        ],
        ["2000", "29.8", "327"],
        ["2001", "30.1", "456"],
        ["2002", "30.5", "509"],
        ["2003", "30.6", "497"],
        ["2004", "31.3", "596"],
        ["2005", "31.7", "573"],
        ["2006", "32.6", "661"],
        ["2007", "33.1", "741"],
        ["2008", "32.7", "809"],
        ["2009", "32.8", "717"],
    ]
    assert actual == expected


from typing import Union


def num_cvt(string: str) -> float:
    """
    >>> num_cvt("2007")
    2007
    >>> num_cvt("3.14")
    3.14
    >>> num_cvt("1,234")
    1234
    """
    try:
        return int(string)
    except ValueError:
        pass
    try:
        return float(string)
    except ValueError:
        pass
    return int(string.replace(",", ""))


def test_num_cvt() -> None:
    assert num_cvt("2007") == 2007
    assert num_cvt("3.14") == 3.14
    assert num_cvt("1,234") == 1234


from typing import Iterable, Iterator


def convert(row_iter: Iterator[list[str]]) -> Union[Iterable[str], Iterable[float]]:
    """
    >>> s3890= ['', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '', 'Per capita consumption of mozzarella cheese (US)Pounds (USDA)', '9.3', '9.7', '9.7', '9.7', '9.9', '10.2', '10.5', '11', '10.6', '10.6', '', 'Civil engineering doctorates awarded (US)Degrees awarded (National Science Foundation)', '480', '501', '540', '552', '547', '622', '655', '701', '712', '708', '', 'Correlation: 0.958648']
    >>> list(convert(column_data(s3890)))
    [('year', 'Per capita consumption of mozzarella cheese (US)Pounds (USDA)', 'Civil engineering doctorates awarded (US)Degrees awarded (National Science Foundation)'), (2000, 9.3, 480), (2001, 9.7, 501), (2002, 9.7, 540), (2003, 9.7, 552), (2004, 9.9, 547), (2005, 10.2, 622), (2006, 10.5, 655), (2007, 11, 701), (2008, 10.6, 712), (2009, 10.6, 708)]
    """
    yield tuple(next(row_iter))  # Dont' convert the header
    for row in row_iter:
        yield tuple(map(num_cvt, row))


def test_convert() -> None:
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
    actual = list(convert(column_data(s3890)))
    expected = [
        (
            "year",
            "Per capita consumption of mozzarella cheese (US)Pounds (USDA)",
            "Civil engineering doctorates awarded (US)Degrees awarded (National Science Foundation)",
        ),
        (2000, 9.3, 480),
        (2001, 9.7, 501),
        (2002, 9.7, 540),
        (2003, 9.7, 552),
        (2004, 9.9, 547),
        (2005, 10.2, 622),
        (2006, 10.5, 655),
        (2007, 11, 701),
        (2008, 10.6, 712),
        (2009, 10.6, 708),
    ]
    assert actual == expected


# Raw data from the internet
# s7 = list(html_data_iter( "http://www.tylervigen.com/view_correlation?id=7" ))
# s3890 = list(html_data_iter( "http://www.tylervigen.com/view_correlation?id=3890" ))
# s97 = list(html_data_iter( "http://www.tylervigen.com/view_correlation?id=97" ))
# s43 = list(html_data_iter( "http://www.tylervigen.com/view_correlation?id=43" ))

# Saves some download and HTML parse bandwidth
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

from typing import TypeVar
from collections.abc import Iterator, Iterable

T = TypeVar("T")


def column(source: Iterable[list[T]], x: int) -> Iterator[T]:
    for row in source:
        yield row[x]


from collections.abc import Iterator
from itertools import *
from Chapter04.ch04_ex4 import corr


def multi_corr(source: list[list[float]]) -> Iterator[tuple[float, float, float]]:
    n = len(source[0])
    for p, q in combinations(range(n), 2):
        header_p, *data_p = list(column(source, p))
        header_q, *data_q = list(column(source, q))
        if header_p == header_q:
            continue
        r_pq = corr(data_p, data_q)
        yield header_p, header_q, r_pq


REPL_multi_corr = """
>>> source = list(convert(column_data(s7, s3890, s43)))
>>> len( source )
11
>>> source[0]
('year', 'Per capita consumption of cheese (US)Pounds (USDA)', 'Number of people who died by becoming tangled in their bedsheetsDeaths (US) (CDC)', 'year', 'Per capita consumption of mozzarella cheese (US)Pounds (USDA)', 'Civil engineering doctorates awarded (US)Degrees awarded (National Science Foundation)', 'year', 'US crude oil imports from VenezuelaMillions of barrels (Dept. of Energy)', 'Per capita consumption of high fructose corn syrup (US)Pounds (USDA)')

>>> results= list( multi_corr( source ) )
>>> len(results)
33
>>> print( "{2: 4.2f}: {0} vs {1}".format(*results[0]) )
 0.96: year vs Per capita consumption of cheese (US)Pounds (USDA)
>>> print( "{2: 4.2f}: {0} vs {1}".format(*results[15]) )
 0.94: Number of people who died by becoming tangled in their bedsheetsDeaths (US) (CDC) vs Civil engineering doctorates awarded (US)Degrees awarded (National Science Foundation)
>>> print( "{2: 4.2f}: {0} vs {1}".format(*results[25]) )
-0.64: Per capita consumption of mozzarella cheese (US)Pounds (USDA) vs US crude oil imports from VenezuelaMillions of barrels (Dept. of Energy)
>>> print( "{2: 4.2f}: {0} vs {1}".format(*results[32]) )
 0.88: US crude oil imports from VenezuelaMillions of barrels (Dept. of Energy) vs Per capita consumption of high fructose corn syrup (US)Pounds (USDA)

"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
