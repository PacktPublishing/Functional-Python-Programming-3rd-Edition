"""Functional Python Programming 3e

Chapter 10, Example Set 6
"""

from functools import singledispatch
from typing import Any


@singledispatch
def zip_format(zip: Any) -> str:
    raise NotImplementedError(f"unsupported {type(zip)} for zip_format()")


@zip_format.register
def _(zip: int) -> str:
    return f"{zip:05d}"


@zip_format.register
def _(zip: float) -> str:
    return f"{zip:05.0f}"


@zip_format.register
def _(zip: str) -> str:
    if "-" in zip:
        zip, box = zip.split("-")
    return f"{zip:0>5s}"


REPL_demo_zip = """
>>> zip_format(12345)
'12345'
>>> zip_format(1005)
'01005'
>>> zip_format(12345.0)
'12345'
>>> zip_format(1105.0)
'01105'
>>> zip_format("12345")
'12345'
>>> zip_format("01005")
'01005'
>>> zip_format("1005")
'01005'
>>> zip_format("01005-1234")
'01005'
>>> zip_format(["11234", "0102"])
Traceback (most recent call last):
...
NotImplementedError: unsupported <class 'list'> for zip_format()
"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
