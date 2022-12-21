"""Functional Python Programming 3e

Chapter 6, Example Set 3
"""

from collections.abc import Iterator
from enum import Enum
import re


class Token(Enum):
    SPACE = 1
    PARA = 2
    EOF = 3


def lexical_scan(some_source: str) -> Iterator[tuple[Token, str]]:
    previous_end = 0
    separator_pat = re.compile(r"\n\s*\n", re.M | re.S)
    for sep in separator_pat.finditer(some_source):
        start, end = sep.span()
        yield Token.PARA, some_source[previous_end:start]
        yield Token.SPACE, some_source[start:end]
        previous_end = end
    yield Token.PARA, some_source[previous_end:]
    yield Token.EOF, ""


import xml.etree.ElementTree as XML
import re

from typing import Tuple, List, Any


from collections.abc import Iterator
from typing import TextIO, cast


def comma_split(text: str) -> list[str]:
    return text.split(",")


def row_iter_kml(file_obj: TextIO) -> Iterator[list[str]]:
    ns_map = {
        "ns0": "http://www.opengis.net/kml/2.2",
        "ns1": "http://www.google.com/kml/ext/2.2",
    }
    xpath = "./ns0:Document/ns0:Folder/" "ns0:Placemark/ns0:Point/ns0:coordinates"
    doc = XML.parse(file_obj)
    return (
        comma_split(cast(str, coordinates.text))
        for coordinates in doc.findall(xpath, ns_map)
    )


REPL_test_row_iter_kml = """
>>> import io
>>> doc= io.StringIO('''<?xml version="1.0" encoding="UTF-8"?>
... <kml xmlns="http://www.opengis.net/kml/2.2"
...     xmlns:gx="http://www.google.com/kml/ext/2.2"
...     xmlns:kml="http://www.opengis.net/kml/2.2"
...     xmlns:atom="http://www.w3.org/2005/Atom">
... <Document>
...	    <Folder>
...		<name>Waypoints.kml</name>
...		<open>1</open>
...		<Placemark>
...			<Point>
...				<coordinates>-76.33029518659048,37.54901619777347,0</coordinates>
...			</Point>
...		</Placemark>
...    </Folder>
... </Document>
... </kml>''')
>>> list(row_iter_kml(doc))
[['-76.33029518659048', '37.54901619777347', '0']]
"""

from collections.abc import Iterator


def pick_lat_lon(lon: str, lat: str, alt: str) -> tuple[str, str]:
    return lat, lon


def float_lat_lon(row_iter: Iterator[list[str]]) -> Iterator[tuple[float, float]]:
    lat_lon_iter = (pick_lat_lon(*row) for row in row_iter)
    return ((float(lat), float(lon)) for lat, lon in lat_lon_iter)


def test_kml_parser() -> None:
    import urllib.request

    source_url = "file:./Winter%202012-2013.kml"
    with urllib.request.urlopen(source_url) as source:
        flat = tuple(float_lat_lon(row_iter_kml(source)))
    assert len(flat) == 74
    assert flat[0] == (37.54901619777347, -76.33029518659048)
    assert flat[-1] == (38.976334, -76.473503)


REPL_test_kml_parser = """
>>> import urllib.request
>>> source_url = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(source_url) as source:
...      flat = list(float_lat_lon(row_iter_kml(source)))
>>> len(flat)
74
>>> flat[0]
(37.54901619777347, -76.33029518659048)
>>> flat[-1]
(38.976334, -76.473503)

>>> from pprint import pprint
>>> pprint(flat)  # doctest: +ELLIPSIS
[(37.54901619777347, -76.33029518659048),
 ...
 (38.976334, -76.473503)]
"""

from collections.abc import Iterator
import csv
from typing import TextIO


def row_iter_csv(source: TextIO) -> Iterator[list[str]]:
    rdr = csv.reader(source, delimiter="\t")
    return rdr


from typing import cast


def float_none(data: str) -> float | None:
    try:
        data_f = float(data)
        return data_f
    except ValueError:
        return None


from collections.abc import Callable
from typing import TypeAlias

R_Float: TypeAlias = list[float | None]

float_row: Callable[[list[str]], R_Float] = lambda row: list(map(float_none, row))
all_numeric: Callable[[R_Float], bool] = lambda row: all(row) and len(row) == 8


def test_csv_parser() -> None:
    from pathlib import Path

    source_path = Path("Anscombe.txt")
    with source_path.open() as source:
        candidates = map(float_row, row_iter_csv(source))
        valid = filter(all_numeric, candidates)
        data = list(valid)
    assert len(data) == 11
    assert data[0] == [10.0, 8.04, 10.0, 9.14, 10.0, 7.46, 8.0, 6.58]
    assert data[-1] == [5.0, 5.68, 5.0, 4.74, 5.0, 5.73, 8.0, 6.89]


from collections.abc import Iterator
from typing import TextIO, TypeAlias

Head_Body: TypeAlias = tuple[tuple[str, str], Iterator[list[str]]]


def row_iter_gpl(file_obj: TextIO) -> Head_Body:
    header_pat = re.compile(r"GIMP Palette\nName:\s*(.*?)\nColumns:\s*(.*?)\n#\n", re.M)

    def read_head(file_obj: TextIO) -> tuple[tuple[str, str], TextIO]:
        if match := header_pat.match("".join(file_obj.readline() for _ in range(4))):
            return (match.group(1), match.group(2)), file_obj
        else:
            raise ValueError("invalid header")

    def read_tail(headers: tuple[str, str], file_obj: TextIO) -> Head_Body:
        return (headers, (next_line.split() for next_line in file_obj))

    return read_tail(*read_head(file_obj))


def test_row_iter_gpl() -> None:
    from pathlib import Path

    source_path = Path("crayola.gpl")
    with source_path.open() as source:
        (name, columns), text_iter = row_iter_gpl(source)
        text = list(text_iter)
    assert name == "Crayola"
    assert columns == "16"
    assert len(text) == 133
    assert text[0] == ["239", "222", "205", "Almond"]
    assert text[-1] == ["255", "174", "66", "Yellow", "Orange"]


from collections.abc import Iterator
from typing import NamedTuple


class Color(NamedTuple):
    red: int
    blue: int
    green: int
    name: str


def color_palette(
    headers: tuple[str, str], row_iter: Iterator[list[str]]
) -> tuple[str, str, tuple[Color, ...]]:
    name, columns = headers
    colors = tuple(
        Color(int(r), int(g), int(b), " ".join(name)) for r, g, b, *name in row_iter
    )
    return name, columns, colors


def test_color_palette() -> None:
    from pathlib import Path

    source_path = Path("crayola.gpl")
    with source_path.open() as source:
        name, columns, colors = color_palette(*row_iter_gpl(source))
    assert name == "Crayola"
    assert columns == "16"
    assert len(colors) == 133
    assert colors[0] == Color(red=239, blue=222, green=205, name="Almond")
    assert colors[-1] == Color(red=255, blue=174, green=66, name="Yellow Orange")


REPL_color_palette = """
>>> from pathlib import Path
>>> source_path = Path("crayola.gpl")
>>> with source_path.open() as source:
...     name, cols, colors = color_palette(
...         *row_iter_gpl(source)
...     )
>>> name
'Crayola'
>>> cols
'16'
>>> len(colors)
133
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
