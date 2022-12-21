"""Functional Python Programming 3e

Chapter 9, Example Set 1

This requires ``MYPYPATH`` to include the ``stubs`` directory.
"""

REPL_product_demo = """
>>> cards = list(product(range(1, 14), '♣♦♥♠'))
>>> cards[:4]
[(1, '♣'), (1, '♦'), (1, '♥'), (1, '♠')]
>>> cards[4:8]
[(2, '♣'), (2, '♦'), (2, '♥'), (2, '♠')]
>>> cards[-4:]
[(13, '♣'), (13, '♦'), (13, '♥'), (13, '♠')]
"""

from collections.abc import Iterable, Iterator, Callable
from itertools import product
from typing import TypeVar

JTL = TypeVar("JTL")
JTR = TypeVar("JTR")


def join(
    t1: Iterable[JTL], t2: Iterable[JTR], where: Callable[[tuple[JTL, JTR]], bool]
) -> Iterable[tuple[JTL, JTR]]:
    return filter(where, product(t1, t2))


def test_join() -> None:
    t1 = [
        (1,),
        (2,),
        (3,),
        (3,),
        (4,),
        (8,),
        (5,),
        (4,),
        (6,),
        (3,),
        (7,),
    ]
    t2 = [
        (1, "h"),
        (2, "e"),
        (3, "l"),
        (4, "o"),
        (5, "w"),
        (6, "r"),
        (7, "d"),
        (8, " "),
    ]
    match = lambda a_b: a_b[0][0] == a_b[1][0]
    m = "".join(i[1][1] for i in join(t1, t2, where=match))
    assert m == "hello world"


from typing import NamedTuple


class Color(NamedTuple):
    rgb: tuple[int, int, int]
    name: str


REPL_color_test = """
>>> palette = [Color(rgb=(239, 222, 205), name='Almond'),
...  Color(rgb=(255, 255, 153), name='Canary'),
...  Color(rgb=(28, 172, 120), name='Green'),
...  Color(rgb=(255, 174, 66), name='Yellow Orange')
... ]

>>> palette = [Color(rgb=(239, 222, 205), name='Almond'), 
...  Color(rgb=(255, 255, 153), name='Canary'), 
...  Color(rgb=(28, 172, 120), name='Green'), 
...  Color(rgb=(255, 174, 66), name='Yellow Orange')
... ]
"""

from itertools import dropwhile, islice
import csv
from typing import Sequence, cast


def get_colors(filename: str = "crayola.gpl") -> Sequence[Color]:
    with open(filename) as source:
        rdr = csv.reader(source, delimiter="\t")
        rows = dropwhile(lambda row: row[0] != "#", rdr)
        color_rows = islice(rows, 1, None)
        colors = list(
            Color(cast(tuple[int, int, int], tuple(map(int, color.split()))), name)
            for color, name in color_rows
        )
    return colors


from collections.abc import Iterator
from PIL import Image  # type: ignore[import]

Point = tuple[int, int]
RGB = tuple[int, int, int]
Pixel = tuple[Point, RGB]


def pixel_iter(img: Image) -> Iterator[Pixel]:
    w, h = img.size
    return ((c, img.getpixel(c)) for c in product(range(w), range(h)))


REPL_pixel_iter = """
>>> from PIL import Image
>>> img = Image.open("IMG_2705.jpg")
>>> print(img) # doctest: +ELLIPSIS
<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=3648x2736 at ...

>>> pixel_subset = list(take(10, pixel_iter(img)))

>>> from pprint import pprint
>>> pprint(pixel_subset)
[((0, 0), (92, 139, 195)),
 ((0, 1), (92, 139, 195)),
 ((0, 2), (92, 139, 195)),
 ((0, 3), (91, 138, 194)),
 ((0, 4), (91, 138, 194)),
 ((0, 5), (91, 138, 194)),
 ((0, 6), (91, 138, 194)),
 ((0, 7), (91, 138, 194)),
 ((0, 8), (92, 139, 195)),
 ((0, 9), (93, 140, 196))]
"""

import math


def euclidean(pixel: RGB, color: Color) -> float:
    return math.sqrt(sum(map(lambda x_1, x_2: (x_1 - x_2) ** 2, pixel, color.rgb)))


def manhattan(pixel: RGB, color: Color) -> float:
    return sum(map(lambda x_1, x_2: abs(x_1 - x_2), pixel, color.rgb))


def max_d(pixel: RGB, color: Color) -> float:
    return max(map(lambda x, y: abs(x - y), pixel, color.rgb))


from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def take(n: int, iterable: Iterable[T]) -> list[T]:
    """Return first n items of the iterable as a list"""
    return list(islice(iterable, n))


from collections.abc import Iterable
from itertools import groupby


def matching_1(
    pixels: Iterable[Pixel], colors: Iterable[Color]
) -> Iterator[tuple[Point, RGB, Color, float]]:

    distances = (
        (pixel[0], pixel[1], color, euclidean(pixel[1], color))
        for pixel, color in product(pixels, colors)
    )
    for _, choices in groupby(distances, key=lambda xy_p_c_d: xy_p_c_d[0]):
        yield min(choices, key=lambda xypcd: xypcd[3])


REPL_matching_1 = """
>>> from pprint import pprint

>>> img = Image.open("IMG_2705.jpg")
>>> print(img) # doctest: +ELLIPSIS
<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=3648x2736 at ...

>>> colors = get_colors()
>>> color_subset = list(islice(colors,0,None,len(colors)//6))
>>> pprint(color_subset)
[Color(rgb=(239, 222, 205), name='Almond'),
 Color(rgb=(255, 255, 153), name='Canary'),
 Color(rgb=(28, 172, 120), name='Green'),
 Color(rgb=(48, 186, 143), name='Mountain Meadow'),
 Color(rgb=(255, 73, 108), name='Radical Red'),
 Color(rgb=(253, 94, 83), name='Sunset Orange'),
 Color(rgb=(255, 174, 66), name='Yellow Orange')]
     
>>> pixel_subset = list(take(10, pixel_iter(img)))
>>> pprint(pixel_subset)
[((0, 0), (92, 139, 195)),
 ((0, 1), (92, 139, 195)),
 ((0, 2), (92, 139, 195)),
 ((0, 3), (91, 138, 194)),
 ((0, 4), (91, 138, 194)),
 ((0, 5), (91, 138, 194)),
 ((0, 6), (91, 138, 194)),
 ((0, 7), (91, 138, 194)),
 ((0, 8), (92, 139, 195)),
 ((0, 9), (93, 140, 196))]
 

>>> distances = (
...     (pixel[0], pixel[1], color, euclidean(pixel[1], color))
...     for pixel, color in product(pixel_subset, color_subset)
... )
>>> pprint(list(distances))  # doctext: +ELLIPSIS
[((0, 0),
  (92, 139, 195),
  Color(rgb=(239, 222, 205), name='Almond'),
  169.10943202553784),
 ((0, 0),
  (92, 139, 195),
  Color(rgb=(255, 255, 153), name='Canary'),
  204.42357985320578),
 ((0, 0),
  (92, 139, 195),
  Color(rgb=(28, 172, 120), name='Green'),
  103.97114984456024),
 ((0, 0),
  (92, 139, 195),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.75868534480233),
...

>>> pprint(list(matching_1(pixel_subset, color_subset)))
[((0, 0),
  (92, 139, 195),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.75868534480233),
 ((0, 1),
  (92, 139, 195),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.75868534480233),
 ((0, 2),
  (92, 139, 195),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.75868534480233),
 ((0, 3),
  (91, 138, 194),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.18272324521742),
 ((0, 4),
  (91, 138, 194),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.18272324521742),
 ((0, 5),
  (91, 138, 194),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.18272324521742),
 ((0, 6),
  (91, 138, 194),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.18272324521742),
 ((0, 7),
  (91, 138, 194),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.18272324521742),
 ((0, 8),
  (92, 139, 195),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  82.75868534480233),
 ((0, 9),
  (93, 140, 196),
  Color(rgb=(48, 186, 143), name='Mountain Meadow'),
  83.36666000266533)]
"""

example_matching_1_full = """
This takes a loooong time -- don't actually do this.
Note that the name of the string doesn't start with REPL to avoid running it as part of the test suite.

>>> colors = get_colors()
>>> img = Image.open("IMG_2705.jpg")
>>> revised = list(matching_1(pixel_iter(img), colors))
>>> revised[:10]
"""


def matching_2(
    pixels: Iterable[Pixel], colors: Iterable[Color]
) -> Iterator[tuple[Point, RGB, Color, float]]:

    for xy, pixel in pixels:
        choices = map(lambda color: (xy, pixel, color, euclidean(pixel, color)), colors)
        yield min(choices, key=lambda xypcd: xypcd[3])


REPL_matching_2 = """
>>> img = Image.open("IMG_2705.jpg")
>>> print(img) # doctest: +ELLIPSIS
<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=3648x2736 at ...

>>> colors= get_colors()
>>> color_subset= list(islice(colors,0,None,len(colors)//6))
>>> print( color_subset )
[Color(rgb=(239, 222, 205), name='Almond'), Color(rgb=(255, 255, 153), name='Canary'), Color(rgb=(28, 172, 120), name='Green'), Color(rgb=(48, 186, 143), name='Mountain Meadow'), Color(rgb=(255, 73, 108), name='Radical Red'), Color(rgb=(253, 94, 83), name='Sunset Orange'), Color(rgb=(255, 174, 66), name='Yellow Orange')]

>>> pixel_subset= tuple(take(10,pixel_iter(img)))

>>> from pprint import pprint
>>> print( list(matching_2(pixel_subset, color_subset)))
[((0, 0), (92, 139, 195), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.75868534480233), ((0, 1), (92, 139, 195), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.75868534480233), ((0, 2), (92, 139, 195), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.75868534480233), ((0, 3), (91, 138, 194), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.18272324521742), ((0, 4), (91, 138, 194), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.18272324521742), ((0, 5), (91, 138, 194), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.18272324521742), ((0, 6), (91, 138, 194), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.18272324521742), ((0, 7), (91, 138, 194), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.18272324521742), ((0, 8), (92, 139, 195), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.75868534480233), ((0, 9), (93, 140, 196), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 83.36666000266533)]

"""

example_matching_2_full = """
This takes a loooong time -- don't actually do this.
Note that the name of the string doesn't start with REPL to avoid running it as part of the test suite.

>>> colors = get_colors()
>>> img = Image.open("IMG_2705.jpg")
>>> revised = list( matching_2(pixel_iter(img), colors))
>>> revised[:10]
"""

REPL_noise_bits = """
>>> r = 15
>>> r_f = 15/256
>>> r_f
0.05859375
>>> r_f + 1/100 - 1/100
0.05859374999999999

>>> r = 15
>>> r_f = 15/256
>>> r_f
0.05859375
>>> r_f + 1/100 - 1/100
0.05859374999999999

"""

from collections import defaultdict, Counter


def gather_colors() -> defaultdict[RGB, list[Point]]:
    img = Image.open("IMG_2705.jpg")

    palette = defaultdict(list)
    for xy, rgb in pixel_iter(img):
        palette[rgb].append(xy)

    w, h = img.size
    print(f"total pixels {w*h}")
    print(f"total colors {len(palette)}")
    return palette


from typing import cast
from collections import defaultdict


def simplify_colors(
    palette: defaultdict[RGB, list[Point]], mask: int
) -> Counter[tuple[int, int, int]]:
    subset: Counter[tuple[int, int, int]] = Counter()
    for c in palette:
        masked_color = cast(tuple[int, int, int], tuple(map(lambda x: x & mask, c)))
        subset[masked_color] += 1
    return subset


REPL_mask = """
>>> bin(200)
'0b11001000'
>>> 200 & 0b11100000
192
>>> bin(192)
'0b11000000'
"""


REPL_simplify_colors = """
>>> palette = gather_colors()
total pixels 9980928
total colors 194537
>>> masks = [0b11100000, 0b11110000, 0b11111000, 0b11111100]
>>> subsets = {m: simplify_colors(palette, m) for m in masks}
>>> for m in masks:
...     print(bin(m), len(subsets[m]))
0b11100000 202
0b11110000 1048
0b11111000 5296
0b11111100 25182

"""

from collections.abc import Sequence


def make_color_map(colors: Sequence[Color]) -> dict[RGB, Color]:
    bit3 = range(0, 256, 0b0010_0000)

    best_iter = (
        min((euclidean(rgb, c), rgb, c) for c in colors)
        for rgb in product(bit3, bit3, bit3)
    )
    color_map = dict((b[1], b[2]) for b in best_iter)
    return color_map


REPL_make_color_map = """
>>> colors = get_colors()
>>> m = make_color_map(colors)
>>> len(m)
512
>>> m[(0,0,0)]
Color(rgb=(0, 0, 0), name='Black')
>>> m[(224,224,224)]
Color(rgb=(219, 215, 210), name='Timberwolf')

"""


def clone_picture(color_map: dict[RGB, Color], filename: str = "IMG_2705.jpg") -> None:
    mask = 0b1110_0000
    img = Image.open(filename)
    clone = img.copy()
    for xy, rgb in pixel_iter(img):
        r, g, b = rgb
        repl = color_map[(mask & r, mask & g, mask & b)]
        clone.putpixel(xy, repl.rgb)
    clone.show()


import time


def demo_clone_picture() -> None:
    start = time.perf_counter()
    color_map = make_color_map(get_colors())
    clone_picture(color_map)
    print(time.perf_counter() - start, "seconds")


def performance() -> None:
    import timeit
    from textwrap import dedent

    euclidean_time = timeit.timeit(
        dedent(
            """
            euclidean((92, 139, 195), Color(rgb=(239, 222, 205), name='Almond'))
        """
        ),
        setup=dedent(
            """
            from typing import NamedTuple
            class Color(NamedTuple):
                rgb: tuple[int, ...]
                name: str
            import math
            def euclidean(pixel, color):
               return math.sqrt(sum(map(lambda x,y: (x-y)**2, pixel, color.rgb)))
        """
        ),
    )

    manhattan_time = timeit.timeit(
        dedent(
            """
            manhattan((92, 139, 195), Color(rgb=(239, 222, 205), name='Almond'))
        """
        ),
        setup=dedent(
            """
            from typing import NamedTuple
            class Color(NamedTuple):
                rgb: tuple[int, ...]
                name: str
            def manhattan(pixel, color):
                return sum(map(lambda x,y: abs(x-y), pixel, color.rgb))
        """
        ),
    )

    min_choices_time = timeit.timeit(
        dedent(
            """
            min(choices, key=lambda xypcd: xypcd[3])
        """
        ),
        setup=dedent(
            """
            from typing import NamedTuple
            class Color(NamedTuple):
                rgb: tuple[int, ...]
                name: str
            choices=(((0, 0), (92, 139, 195), Color(rgb=(239, 222, 205), name='Almond'), 169.10943202553784), ((0, 0), (92, 139, 195), Color(rgb=(255, 255, 153), name='Canary'), 204.42357985320578), ((0, 0), (92, 139, 195), Color(rgb=(28, 172, 120), name='Green'), 103.97114984456024), ((0, 0), (92, 139, 195), Color(rgb=(48, 186, 143), name='Mountain Meadow'), 82.75868534480233), ((0, 0), (92, 139, 195), Color(rgb=(255, 73, 108), name='Radical Red'), 196.19887869200477), ((0, 0), (92, 139, 195), Color(rgb=(253, 94, 83), name='Sunset Orange'), 201.2212712413874), ((0, 0), (92, 139, 195), Color(rgb=(255, 174, 66), name='Yellow Orange'), 210.7961100210343))
        """
        ),
    )
    print(f"Euclidean {euclidean_time:.3f}")
    print(f"Manhattan {manhattan_time:.3f}")
    print(f"min(choices,...) {min_choices_time:.3f}")


REPL_combinations = """
>>> import itertools
>>> from pprint import pprint
>>> pprint(
... list(itertools.combinations([1,2,3,4,5,6], 2))
... )
[(1, 2),
 (1, 3),
 (1, 4),
...
 (4, 6),
 (5, 6)]
>>> pprint(
... list(itertools.combinations_with_replacement([1,2,3,4,5,6], 2))
... )
[(1, 1),
 (1, 2),
 (1, 3),
...
 (5, 5),
 (5, 6),
 (6, 6)]
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}

if __name__ == "__main__":
    performance()
