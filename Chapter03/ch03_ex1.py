"""Functional Python Programming 3e

Chapter 3, Example Set 1
"""
from typing import Callable
import pytest

global_adjustment: float


def some_function(a: float, b: float, t: float) -> float:
    return a + b * t + global_adjustment


def test_some_function() -> None:
    global global_adjustment
    global_adjustment = 13
    assert some_function(2, 3, 5) == 2 + 3 * 5 + global_adjustment


from pathlib import Path


def write_file(some_path: Path) -> None:
    result = "Hello, world!"
    with some_path.open("w") as output_file:
        output_file.write(result + "\n")


def test_write_file(tmp_path: Path) -> None:
    target = tmp_path / "write_file.out"
    write_file(target)
    assert target.read_text() == "Hello, world!\n"


from typing import TextIO

ifile: TextIO
ofile: TextIO


def open_files(iname: str, oname: str) -> None:
    """A bad idea..."""
    global ifile, ofile
    ifile = open(iname, "r")
    ofile = open(oname, "w")


def next_line_with(prefix: str) -> str | None:
    """Also a bad idea..."""
    line = ifile.readline()
    while line is not None and not line.startswith(prefix):
        line = ifile.readline()
    return line


def test_bad_ideas(tmp_path: Path) -> None:
    input = tmp_path / "bad_idea.in"
    input.write_text("Line 1\n* Line 2\n")
    output = tmp_path / "bad_idea.out"

    open_files(str(input), str(output))
    text = next_line_with("*")
    assert text == "* Line 2\n"


from collections.abc import Callable


class Mersenne1:
    def __init__(self, algorithm: Callable[[int], int]) -> None:
        self.pow2 = algorithm

    def __call__(self, arg: int) -> int:
        return self.pow2(arg) - 1


def shifty(b: int) -> int:
    return 1 << b


def multy(b: int) -> int:
    if b == 0:
        return 1
    return 2 * multy(b - 1)


def faster(b: int) -> int:
    if b == 0:
        return 1
    if b % 2 == 1:
        return 2 * faster(b - 1)
    t = faster(b // 2)
    return t * t


def test_mults() -> None:
    assert shifty(17) - 1 == 131071
    assert multy(17) - 1 == 131071
    assert faster(17) - 1 == 131071


# Implementations of Mersenne with strategy objects plugged in properly.

m1s = Mersenne1(shifty)

m1m = Mersenne1(multy)

m1f = Mersenne1(faster)


def test_mersenne_1() -> None:
    assert m1s(17) == 131071
    assert m1m(17) == 131071
    assert m1f(17) == 131071


REPL_test_mersenne1 = """
>>> m1s(17)
131071
>>> m1f(89)
618970019642690137449562111
"""

# Alternative Mersenne using class-level configuration.
# The syntax seems more awkward.

from typing import cast


class Mersenne2:
    """Requires client use ``staticmethod()``."""

    pow2: Callable[[int], int]

    def __call__(self, arg: int) -> int:
        # Disconnect this from being a ``self.pow2()`` reference.
        f: Callable[[int], int] = getattr(self, "pow2")
        return f(arg) - 1


class ShiftyMersenne(Mersenne2):
    pow2 = staticmethod(shifty)


class MultyMersenee(Mersenne2):
    pow2 = staticmethod(multy)


class FasterMersenne(Mersenne2):
    pow2 = staticmethod(faster)


m2s = ShiftyMersenne()
m2m = MultyMersenee()
m2f = FasterMersenne()


def test_mersenne() -> None:
    assert m1s(17) == 131071
    assert m1m(17) == 131071
    assert m1f(17) == 131071
    assert m2s(17) == 131071
    assert m2m(17) == 131071
    assert m2f(17) == 131071
    assert m1s(89) == 618970019642690137449562111
    assert m1m(89) == 618970019642690137449562111
    assert m1f(89) == 618970019642690137449562111
    with pytest.raises(RecursionError):
        assert m1m(1279) == 0
    assert (
        m1f(1279)
        == 10407932194664399081925240327364085538615262247266704805319112350403608059673360298012239441732324184842421613954281007791383566248323464908139906605677320762924129509389220345773183349661583550472959420547689811211693677147548478866962501384438260291732348885311160828538416585028255604666224831890918801847068222203140521026698435488732958028878050869736186900714720710555703168729087
    )


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}


def performance() -> None:
    import timeit

    print(
        m1s.pow2.__name__,
        timeit.timeit("""m1s(17)""", """from Chapter03.ch03_ex1 import m1s"""),
    )
    print(
        m1m.pow2.__name__,
        timeit.timeit("""m1m(17)""", """from Chapter03.ch03_ex1 import m1m"""),
    )
    print(
        m1f.pow2.__name__,
        timeit.timeit("""m1f(17)""", """from Chapter03.ch03_ex1 import m1f"""),
    )


if __name__ == "__main__":
    performance()
