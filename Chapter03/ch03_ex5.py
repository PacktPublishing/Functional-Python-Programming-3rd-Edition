"""Functional Python Programming 3e

Chapter 3, Example Set 5
"""

from collections.abc import Callable
from typing import TypeAlias

Extractor: TypeAlias = Callable[[tuple[int, int, int, str]], int]

red: Extractor = lambda color: color[0]

green: Extractor = lambda color: color[1]

blue: Extractor = lambda color: color[2]

REPL_rgb_functions = """
>>> color = (203, 65, 84, "Brick Red")
>>> red(color)
203
>>> green(color)
65
>>> blue(color)
84
"""


from collections.abc import Callable
from typing import TypeAlias

RGB: TypeAlias = tuple[int, int, int, str]

redt: Callable[[RGB], int] = lambda color: color[0]

REPL_rgb_typed_functions = """
>>> color = (203, 65, 84, "Brick Red")
>>> redt(color)
203
"""

REPL_rgb_functions_3 = """
>>> from collections.abc import Callable
>>> RGB = tuple[int, int, int]
>>> red: Callable[[RGB], int] = lambda color: color[0]
>>> green: Callable[[RGB], int] = lambda color: color[1]
>>> blue: Callable[[RGB], int] = lambda color: color[2]
>>> almond = (239, 222, 205)
>>> red(almond)
239
"""

from typing import NamedTuple


class Color(NamedTuple):
    """An RGB color."""

    red: int
    green: int
    blue: int
    name: str


REPL_color_tuple = """
>>> color = Color(203, 65, 84, "Brick Red")
>>> color.red
203
>>> color.green
65
>>> color.blue
84
"""

REPL_palette = """
>>> palette = [
...     Color(red=239, green=222, blue=205, name='Almond'),
...     Color(red=205, green=149, blue=117, name='Antique Brass'),
...     Color(red=253, green=217, blue=181, name='Apricot'),
...     Color(red=197, green=227, blue=132, name='Yellow Green'),
...     Color(red=255, green=174, blue=66, name='Yellow Orange')
... ]

>>> name_map = dict((c.name, c) for c in palette)

>>> name_map['Antique Brass']
Color(red=205, green=149, blue=117, name='Antique Brass')
>>> name_map['Yellow Orange']
Color(red=255, green=174, blue=66, name='Yellow Orange')
"""

### Some of this is teaser material for topics in Chapter 7

example = """GIMP Palette
Name: Small
Columns: 3
#
  0   0   0	Black
255 255 255	White
238  32  77	Red
28 172 120	Green
31 117 254	Blue
"""

import re
from typing import TextIO
from collections.abc import Iterator


def color_GPL_r(file_obj: TextIO) -> Iterator[Color]:
    """GPL Color Reader. Get body from the results of getting the header.

    Strictly recursive.

    >>> import io
    >>> data= io.StringIO("GIMP Palette\\nName: Crayola\\nColumns: 16\\n#\\n239 222 205	Almond\\n205 149 117	Antique Brass")
    >>> list( color_GPL_r(data))
    [Color(red=239, green=222, blue=205, name='Almond'), Color(red=205, green=149, blue=117, name='Antique Brass')]
    """
    header_pat = re.compile(r"GIMP Palette\nName:\s*(.*?)\nColumns:\s*(.*?)\n#\n", re.M)

    def read_head(file_obj: TextIO) -> tuple[TextIO, str, str, str]:
        headers = "".join(file_obj.readline() for _ in range(4))
        if match := header_pat.match(headers):
            return (
                file_obj,
                match.group(1),
                match.group(2),
                file_obj.readline().rstrip(),
            )
        else:
            raise ValueError(f"invalid {headers!r}")

    def read_tail(
        file_obj: TextIO, palette_name: str, columns: str, next_line: str
    ) -> Iterator[Color]:
        if len(next_line) == 0:
            return
        r, g, b, *name = next_line.split()
        yield Color(int(r), int(g), int(b), " ".join(name))
        yield from read_tail(
            file_obj, palette_name, columns, file_obj.readline().rstrip()
        )

    return read_tail(*read_head(file_obj))


def row_iter_gpl(file_obj: TextIO) -> tuple[str, str, Iterator[list[str]]]:
    """GPL Color Reader. Get body from the results of getting the header.

    Uses a higher-level function in the form of a generator expression. Somewhat simpler.

    >>> import io
    >>> data = io.StringIO("GIMP Palette\\nName: Crayola\\nColumns: 16\\n#\\n239 222 205	Almond\\n205 149 117	Antique Brass")
    >>> name, columns, colors= row_iter_gpl(data)
    >>> name
    'Crayola'
    >>> list(colors)
    [['239', '222', '205', 'Almond'], ['205', '149', '117', 'Antique', 'Brass']]

    """
    header_pat = re.compile(r"GIMP Palette\nName:\s*(.*?)\nColumns:\s*(.*?)\n#\n", re.M)

    def read_head(file_obj: TextIO) -> tuple[str, str, TextIO]:
        headers = "".join(file_obj.readline() for _ in range(4))
        if match := header_pat.match(headers):
            return match.group(1), match.group(2), file_obj
        else:
            raise ValueError(f"invalid {headers!r}")

    def read_tail(
        name: str, columns: str, file_obj: TextIO
    ) -> tuple[str, str, Iterator[list[str]]]:
        return name, columns, (next_line.split() for next_line in file_obj)

    return read_tail(*read_head(file_obj))


def color_GPL_g(file_obj: TextIO) -> Iterator[Color]:
    """GPL Color Reader. Generator function version which leverages
    the lower-level row_iter_gpl() function.

    >>> import io
    >>> data = io.StringIO("GIMP Palette\\nName: Crayola\\nColumns: 16\\n#\\n239 222 205	Almond\\n205 149 117	Antique Brass")
    >>> list(color_GPL_g(data))
    [Color(red=239, green=222, blue=205, name='Almond'), Color(red=205, green=149, blue=117, name='Antique Brass')]
    """
    name, columns, row_iter = row_iter_gpl(file_obj)
    return (
        Color(int(r), int(g), int(b), " ".join(name)) for r, g, b, *name in row_iter
    )


from collections.abc import Iterator


def load_colors(row_iter_gpl: tuple[str, str, Iterator[list[str]]]) -> dict[str, Color]:
    """Load colors from the ``crayola.gpl`` file, building a mapping.

    >>> import io
    >>> source= io.StringIO(example)
    >>> colors= load_colors(row_iter_gpl(source))
    >>> [colors[k] for k in sorted(colors)]
    [Color(red=0, green=0, blue=0, name='Black'), Color(red=31, green=117, blue=254, name='Blue'), Color(red=28, green=172, blue=120, name='Green'), Color(red=238, green=32, blue=77, name='Red'), Color(red=255, green=255, blue=255, name='White')]
    """
    name, columns, row_iter = row_iter_gpl
    colors = tuple(
        Color(int(r), int(g), int(b), " ".join(name)) for r, g, b, *name in row_iter
    )
    # print( colors )
    mapping = dict((c.name, c) for c in colors)
    # print( mapping )
    return mapping


REPL_test_gpl = """
>>> import io
>>> tuple(color_GPL_r(io.StringIO(example)))
(Color(red=0, green=0, blue=0, name='Black'), Color(red=255, green=255, blue=255, name='White'), Color(red=238, green=32, blue=77, name='Red'), Color(red=28, green=172, blue=120, name='Green'), Color(red=31, green=117, blue=254, name='Blue'))
>>> tuple(color_GPL_g(io.StringIO(example)))
(Color(red=0, green=0, blue=0, name='Black'), Color(red=255, green=255, blue=255, name='White'), Color(red=238, green=32, blue=77, name='Red'), Color(red=28, green=172, blue=120, name='Green'), Color(red=31, green=117, blue=254, name='Blue'))
"""

### End of the Chapter 7 side-bar...
### Back to Chapter 3 test cases.

import bisect
from collections.abc import Mapping, Iterable
from typing import Any


class StaticMapping(Mapping[str, Color]):
    def __init__(self, iterable: Iterable[tuple[str, Color]]) -> None:
        self._data: tuple[tuple[str, Color], ...] = tuple(iterable)
        self._keys: tuple[str, ...] = tuple(sorted(key for key, _ in self._data))

    def __getitem__(self, key: str) -> Color:
        ix = bisect.bisect_left(self._keys, key)
        if ix != len(self._keys) and self._keys[ix] == key:
            return self._data[ix][1]
        raise ValueError(f"{key!r} not found")

    def __iter__(self) -> Iterator[str]:
        return iter(self._keys)

    def __len__(self) -> int:
        return len(self._keys)


REPL_static_mapping = """
>>> import io
>>> c = StaticMapping( (c.name, c) for c in color_GPL_r(io.StringIO(example)) )
>>> c.get("Black")
Color(red=0, green=0, blue=0, name='Black')
"""


def test_static_mapping() -> None:
    import io

    c = StaticMapping((c.name, c) for c in color_GPL_r(io.StringIO(example)))
    assert c.get("Black") == Color(red=0, green=0, blue=0, name="Black")


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
