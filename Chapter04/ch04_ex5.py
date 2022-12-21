"""Functional Python Programming 3e

Chapter 4, Example Set 5
"""

REPL_zip = """
>>> xi = [1.47, 1.50, 1.52, 1.55, 1.57, 1.60, 1.63, 1.65,
... 1.68, 1.70, 1.73, 1.75, 1.78, 1.80, 1.83,]
>>> yi = [52.21, 53.12, 54.48, 55.84, 57.20, 58.57, 59.93, 61.29,
... 63.11, 64.47, 66.28, 68.10, 69.92, 72.19, 74.46,]

>>> zip(xi, yi)
<zip object at ...>

>>> pairs = list(zip(xi, yi))
>>> pairs[:3]
[(1.47, 52.21), (1.5, 53.12), (1.52, 54.48)]
>>> pairs[-3:]
[(1.78, 69.92), (1.8, 72.19), (1.83, 74.46)]
"""

REPL_zip_degenerate_cases = """
>>> list(zip())
[]

>>> list(zip((1,2,3)))
[(1,), (2,), (3,)]

>>> list(zip((1, 2, 3), ('a', 'b')))
[(1, 'a'), (2, 'b')]
"""

REPL_unzip = """
>>> pairs = [(1.47, 52.21), (1.5, 53.12), (1.52, 54.48),
...     (1.55, 55.84), (1.57, 57.2), (1.6, 58.57),
...     (1.63, 59.93), (1.65, 61.29), (1.68, 63.11),
...     (1.7, 64.47), (1.73, 66.28), (1.75, 68.1),
...     (1.78, 69.92), (1.8, 72.19), (1.83, 74.46)]

>>> p0 = list(x[0] for x in pairs)
>>> p0[:3]
[1.47, 1.5, 1.52]
>>> p1 = list(x[1] for x in pairs)
>>> p1[:3]
[52.21, 53.12, 54.48]

>>> round(sum(p0*p1 for p0, p1 in pairs), 3)
1548.245

"""

REPL_flatten = """
>>> file = '''   2      3      5      7     11     13     17     19     23     29
...  31     37     41     43     47     53     59     61     67     71
...  73     79     83     89     97    101    103    107    109    113
... 127    131    137    139    149    151    157    163    167    173
... 179    181    191    193    197    199    211    223    227    229
... '''.splitlines()

>>> blocked = list(line.split() for line in file)
>>> from pprint import pprint
>>> pprint(blocked)
[['2', '3', '5', '7', '11', '13', '17', '19', '23', '29'],
 ['31', '37', '41', '43', '47', '53', '59', '61', '67', '71'],
 ...
 ['179', '181', '191', '193', '197', '199', '211', '223', '227', '229']]

>>> len(blocked)
5
>>> (x for line in blocked for x in line)
<generator object <genexpr> at ...>
>>> flat = list(x for line in blocked for x in line)
>>> len(flat)
50
>>> flat[:10]
['2', '3', '5', '7', '11', '13', '17', '19', '23', '29']
"""

from collections.abc import Iterable
from typing import Any


def flatten(data: Iterable[Iterable[Any]]) -> Iterable[Any]:
    for line in data:
        for x in line:
            yield x


def test_flatten() -> None:
    data = [
        "2      3      5      7     11     13     17     19     23     29".split(),
        "7841   7853   7867   7873   7877   7879   7883   7901   7907   7919".split(),
    ]
    assert list(map(int, flatten(data))) == [
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        7841,
        7853,
        7867,
        7873,
        7877,
        7879,
        7883,
        7901,
        7907,
        7919,
    ]


REPL_group = """
>>> flat = ['2', '3', '5', '7', '11', '13', '17', '19', '23', '29',
... '31', '37', '41', '43', '47', '53', '59', '61', '67', '71',
... ]

>>> flat_iter = iter(flat)
>>> (tuple(next(flat_iter) for i in range(5))
...     for row in range(len(flat) // 5)
... )
<generator object <genexpr> at ...>

>>> grouped = list(_)
>>> from pprint import pprint
>>> pprint(grouped)
[('2', '3', '5', '7', '11'),
 ('13', '17', '19', '23', '29'),
 ('31', '37', '41', '43', '47'),
 ('53', '59', '61', '67', '71')]
"""

from typing import TextIO, TypeVar, Any
from collections.abc import Iterator, Iterable, Sequence


def strip_head(source: TextIO, line: str) -> tuple[TextIO, str]:
    """Purely recursive strip headings until a blank line.

    >>> import io
    >>> data = io.StringIO( "heading\\n\\nbody\\nmore\\n" )
    >>> tail, first = strip_head(data, data.readline())
    >>> first
    'body\\n'
    >>> list(tail)
    ['more\\n']

    """
    if len(line.strip()) == 0:
        return source, source.readline()
    return strip_head(source, source.readline())


def get_columns(source: TextIO, line: str) -> Iterator[str]:
    """When reading 1000.txt, parse columns and exclude the trailing line.

    >>> import io
    >>> data = io.StringIO( "body\\nmore\\nend.\\n" )
    >>> list( get_columns(data, data.readline() ) )
    ['body\\n', 'more\\n']
    """
    if line.strip() == "end.":
        return
    yield line
    yield from get_columns(source, source.readline())


def parse_i(source: TextIO) -> Iterator[int]:
    """Imperative parsing.

    >>> import io
    >>> data = io.StringIO('''\\
    ...                         The First 1,000 Primes
    ...                          (the 1,000th is 7919)
    ...         For more information on primes see http://primes.utm.edu/
    ...
    ...      2      3      5      7     11     13     17     19     23     29
    ...   7841   7853   7867   7873   7877   7879   7883   7901   7907   7919
    ... end.
    ... ''')
    >>> list( parse_i(data))
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907, 7919]
    """
    for c in get_columns(*strip_head(source, source.readline())):
        for number_text in c.split():
            yield int(number_text)


def parse_g(source: TextIO) -> Iterator[int]:
    """Generator function parsing.

    >>> import io
    >>> data = io.StringIO('''\\
    ...                         The First 1,000 Primes
    ...                          (the 1,000th is 7919)
    ...         For more information on primes see http://primes.utm.edu/
    ...
    ...      2      3      5      7     11     13     17     19     23     29
    ...   7841   7853   7867   7873   7877   7879   7883   7901   7907   7919
    ... end.
    ... ''')
    >>> list(parse_g(data))
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907, 7919]
    """
    return (
        int(number_text)
        for c in get_columns(*strip_head(source, source.readline()))
        for number_text in c.split()
    )


from collections.abc import Sequence
from typing import TypeVar

ItemType = TypeVar("ItemType")
# Flat = Sequence[ItemType]
# Grouped = list[tuple[ItemType, ...]]


def group_by_seq(n: int, sequence: Sequence[ItemType]) -> list[tuple[ItemType, ...]]:
    flat_iter = iter(sequence)
    full_sized_items = list(
        tuple(next(flat_iter) for i in range(n)) for row in range(len(sequence) // n)
    )
    trailer = tuple(flat_iter)
    if trailer:
        return full_sized_items + [trailer]
    else:
        return full_sized_items


def test_group_by_seq() -> None:
    flat = [
        "2",
        "3",
        "5",
        "7",
        "11",
        "13",
        "17",
        "19",
        "23",
        "29",
        "31",
        "37",
        "41",
        "43",
        "47",
        "53",
        "59",
        "61",
        "67",
        "71",
    ]
    assert group_by_seq(2, flat) == [
        ("2", "3"),
        ("5", "7"),
        ("11", "13"),
        ("17", "19"),
        ("23", "29"),
        ("31", "37"),
        ("41", "43"),
        ("47", "53"),
        ("59", "61"),
        ("67", "71"),
    ]


from collections.abc import Iterator
from typing import TypeVar

ItemT = TypeVar("ItemT")


def group_by_iter(n: int, iterable: Iterator[ItemT]) -> Iterator[tuple[ItemT, ...]]:
    def group(n: int, iterable: Iterator[ItemT]) -> Iterator[ItemT]:
        for i in range(n):
            try:
                yield next(iterable)
            except StopIteration:
                return

    while row := tuple(group(n, iterable)):
        yield row


def test_group_by_iter() -> None:
    flat = [
        "2",
        "3",
        "5",
        "7",
        "11",
        "13",
        "17",
        "19",
        "23",
        "29",
        "31",
        "37",
        "41",
        "43",
        "47",
        "53",
        "59",
        "61",
        "67",
        "71",
    ]
    assert list(group_by_iter(2, iter(flat))) == [
        ("2", "3"),
        ("5", "7"),
        ("11", "13"),
        ("17", "19"),
        ("23", "29"),
        ("31", "37"),
        ("41", "43"),
        ("47", "53"),
        ("59", "61"),
        ("67", "71"),
    ]


from itertools import zip_longest


def group_by_slice(
    n: int, sequence: Sequence[ItemType]
) -> Iterator[tuple[ItemType, ...]]:
    return zip_longest(*(sequence[i::n] for i in range(n)))


REPL_zip_group = """
>>> flat = ['2', '3', '5', '7', '11', '13', '17', '19', '23', '29',
...     '31', '37', '41', '43', '47', '53', '59', '61', '67', '71',
... ]

>>> pairs = list(zip(flat[0::2], flat[1::2]))
>>> pairs[:3]
[('2', '3'), ('5', '7'), ('11', '13')]
>>> pairs[-3:]
[('47', '53'), ('59', '61'), ('67', '71')]

>>> n = 2
>>> pairs = list(
...     zip(*(flat [i::n] for i in range(n)))
... )
>>> pairs[:5]
[('2', '3'), ('5', '7'), ('11', '13'), ('17', '19'), ('23', '29')]
"""

from collections.abc import Iterator


def digits(x: int, base: int) -> Iterator[int]:
    if x == 0:
        return
    yield x % base
    yield from digits(x // base, base)


def test_digits() -> None:
    assert tuple(digits(126, 2)) == (0, 1, 1, 1, 1, 1, 1)
    assert tuple(digits(126, 16)) == (14, 7)


def to_base(x: int, base: int) -> Iterator[int]:
    return reversed(tuple(digits(x, base)))


def test_to_base() -> None:
    assert tuple(to_base(126, 2)) == (1, 1, 1, 1, 1, 1, 0)
    assert bin(126) == "0b1111110"
    assert tuple(to_base(126, 16)) == (7, 14)
    assert hex(126) == "0x7e"


REPL_enumerate = """
>>> xi = [1.47, 1.50, 1.52, 1.55, 1.57, 1.60, 1.63, 1.65,
... 1.68, 1.70, 1.73, 1.75, 1.78, 1.80, 1.83,]

>>> yi = [52.21,53.12,54.48,55.84,57.20,58.57,59.93,61.29,
... 63.11, 64.47, 66.28, 68.10, 69.92, 72.19, 74.46,]

>>> xi[:3]
[1.47, 1.5, 1.52]
>>> len(xi)
15

>>> id_values = list(enumerate(xi))
>>> id_values[:3]
[(0, 1.47), (1, 1.5), (2, 1.52)]
>>> len(id_values)
15
"""

REPL_parser_test = """
>>> text= '''   2      3      5      7     11     13     17     19     23     29
...  31     37     41     43     47     53     59     61     67     71
... 179    181    191    193    197    199    211    223    227    229
... '''
>>> data= list(v for line in text.splitlines() for v in line.split())
>>> data
['2', '3', '5', '7', '11', '13', '17', '19', '23', '29', '31', '37', '41', '43', '47', '53', '59', '61', '67', '71', '179', '181', '191', '193', '197', '199', '211', '223', '227', '229']

>>> file = text.splitlines()
>>> blocked = list(line.split() for line in file)
>>> blocked
[['2', '3', '5', '7', '11', '13', '17', '19', '23', '29'], ['31', '37', '41', '43', '47', '53', '59', '61', '67', '71'], ['179', '181', '191', '193', '197', '199', '211', '223', '227', '229']]

>>> (x for line in blocked for x in line)  # doctest: +ELLIPSIS
<generator object <genexpr> at ...>
>>> list(_)
['2', '3', '5', '7', '11', '13', '17', '19', '23', '29', '31', '37', '41', '43', '47', '53', '59', '61', '67', '71', '179', '181', '191', '193', '197', '199', '211', '223', '227', '229']
"""

REPL_grouping_test = """
>>> with open("1000.txt") as source:
...     flat = list(parse_g(source))
>>> len(flat)
1000

>>> group7_seq = group_by_seq(7, flat)
>>> group7_seq[-1]
(7877, 7879, 7883, 7901, 7907, 7919)

>>> demo = list(x for line in group7_seq for x in line)
>>> demo == flat
True

>>> group7_iter = list(group_by_iter(7, iter(flat)))

>>> group7_iter[-1]
(7877, 7879, 7883, 7901, 7907, 7919)

>>> demo = list(x for line in group7_iter for x in line)
>>> demo == flat
True

>>> all = list(group_by_slice(7, flat))
>>> all[0]
(2, 3, 5, 7, 11, 13, 17)
>>> all[-1]
(7877, 7879, 7883, 7901, 7907, 7919, None)
"""


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
