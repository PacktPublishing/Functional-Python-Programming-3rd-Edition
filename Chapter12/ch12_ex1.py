"""Functional Python Programming 3e

Chapter 12, Example Set 1
"""
import pytest


from collections.abc import Callable
from functools import wraps


def nullable(
    function: Callable[[float], float]
) -> Callable[[float | None], float | None]:
    @wraps(function)
    def null_wrapper(value: float | None) -> float | None:
        return None if value is None else function(value)

    return null_wrapper


import math


@nullable
def st_miles(nm: float) -> float:
    return 1.15078 * nm


# reveal_type(st_miles)

REPL_st_miles = """
>>> some_data = [8.7, 86.9, None, 43.4, 60]
>>> scaled = map(st_miles, some_data)
>>> list(scaled)
[10.011785999999999, 100.002782, None, 49.94385199999999, 69.04679999999999]
"""


@nullable
def nround4(x: float) -> float:
    return round(x, 4)


REPL_st_miles_nround4 = """
>>> some_data = [8.7, 86.9, None, 43.4, 60]
>>> scaled = map(st_miles, some_data)
>>> [nround4(v) for v in scaled]
[10.0118, 100.0028, None, 49.9439, 69.0468]

"""

st_miles_2: Callable[[float | None], float | None] = nullable(lambda nm: nm * 1.15078)
nround4_2: Callable[[float | None], float | None] = nullable(lambda x: round(x, 4))


def test_Null_st_miles() -> None:
    some_data = [8.7, 86.9, None, 43.4, 60]
    scaled = map(st_miles_2, some_data)
    rounded = [nround4_2(v) for v in scaled]
    assert rounded == [10.0118, 100.0028, None, 49.9439, 69.0468]


from typing import TypeVar, ParamSpec

NT = TypeVar("NT")
NP = ParamSpec("NP")


def null2(function: Callable[NP, NT]) -> Callable[NP, NT | None]:
    @wraps(function)
    def null_wrapper(*args: NP.args, **kwargs: NP.kwargs) -> NT | None:
        try:
            return function(*args, **kwargs)
        except TypeError as e:
            if "NoneType" in e.args[0]:
                return None
            raise

    return null_wrapper


def test_null2() -> None:
    """Note that mypy spots several suspicious constructs."""
    ndivmod = null2(divmod)
    assert ndivmod(None, 2) is None  # type: ignore[arg-type]
    assert ndivmod(2, None) is None  # type: ignore[misc]
    with pytest.raises(TypeError):
        ndivmod("22", "7")  # type: ignore[arg-type]


# Relies on ParamSpec and TypeVar defined earlier.

import logging


def logged(function: Callable[NP, NT]) -> Callable[NP, NT]:
    @wraps(function)
    def log_wrapper(*args: NP.args, **kwargs: NP.kwargs) -> NT:
        log = logging.getLogger(function.__qualname__)
        try:
            result = function(*args, **kwargs)
            log.info("(%r %r) => %r", args, kwargs, result)
            return result
        except Exception:
            log.exception("(%r %r)", args, kwargs)
            raise

    return log_wrapper


def test_logged_divmod_1(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    ldivmod = logged(divmod)
    with pytest.raises(TypeError):
        ldivmod(3, None)  # type: ignore[misc]
    assert caplog.text.startswith("ERROR    divmod:ch12_ex1.py:")


def test_logged_divmod_2(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    ldivmod = logged(divmod)
    ldivmod(22, 7)
    assert caplog.text.startswith("INFO     divmod:ch12_ex1.py:")


def stringify(argument_function: Callable[[int, int], int]) -> Callable[[str], str]:
    @wraps(argument_function)
    def two_part_wrapper(text: str) -> str:
        # The "before" part
        arg1, arg2 = map(int, text.split(","))
        int_result = argument_function(arg1, arg2)
        # The "after" part
        return str(int_result)

    return two_part_wrapper


REPL_two_part_wrapper = """
>>> @stringify
... def the_model(m: int, s: int) -> int:
...     return m * 45 + s * 3
...
>>> the_model("5,6")
'243'

>>> 5*45 + 6*3
243
"""

from collections.abc import Callable
import decimal
from typing import Any, Union, TypeVar, TypeAlias

Number: TypeAlias = Union[decimal.Decimal, float]
NumT = TypeVar("NumT", bound=Number)


def bad_data(function: Callable[[str], NumT]) -> Callable[[str], NumT]:
    @wraps(function)
    def wrap_bad_data(source: str, **kwargs: Any) -> NumT:
        try:
            return function(source, **kwargs)
        except (ValueError, decimal.InvalidOperation):
            cleaned = source.replace(",", "")
            return function(cleaned, **kwargs)

    return wrap_bad_data


from decimal import Decimal

bd_int = bad_data(int)
bd_float = bad_data(float)
bd_decimal = bad_data(Decimal)

REPL_bad_data = """
>>> bd_int("13")
13
>>> bd_int("1,371")
1371
>>> bd_int("1,371", base=16)
4977

>>> from decimal import Decimal
>>> bd_int( "13" )
13
>>> bd_int( "1,371" )
1371
>>> bd_int( "1,371", base=16 )
4977
>>> bd_float("17")
17.0
>>> bd_float("1,701")
1701.0
>>> bd_decimal(19)
Decimal('19')
>>> bd_decimal("1,956")
Decimal('1956')
"""

from collections.abc import Callable
import decimal
from typing import Any, TypeVar

T = TypeVar("T")


def bad_char_remove(
    *bad_chars: str,
) -> Callable[[Callable[[str], T]], Callable[[str], T]]:
    def cr_decorator(function: Callable[[str], T]) -> Callable[[str], T]:
        def clean_list(text: str, *, to_replace: tuple[str, ...]) -> str:
            if to_replace:
                return clean_list(
                    text.replace(to_replace[0], ""), to_replace=to_replace[1:]
                )
            return text

        @wraps(function)
        def wrap_char_remove(text: str, **kwargs: Any) -> T:
            try:
                return function(text, **kwargs)
            except (ValueError, decimal.InvalidOperation):
                cleaned = clean_list(text, to_replace=bad_chars)
                return function(cleaned, **kwargs)

        return wrap_char_remove

    return cr_decorator


from decimal import Decimal
from typing import Any


@bad_char_remove("$", ",")
def currency(text: str, **kw: Any) -> Decimal:
    return Decimal(text, **kw)


REPL_bad_char_remove = """
>>> currency("13")
Decimal('13')
>>> currency("$3.14")
Decimal('3.14')
>>> currency("$1,701.00")
Decimal('1701.00')

>>> currency( "13" )
Decimal('13')
>>> currency( "$3.14" )
Decimal('3.14')
>>> currency( "$1,701.00" )
Decimal('1701.00')
"""


# This is limited to only str -> T conversions
# We can't (easily) fold in KW arguments


def then_convert(
    convert_function: Callable[[str], T]
) -> Callable[[Callable[[str], str]], Callable[[str], T]]:
    def concrete_decorator(clean_func: Callable[[str], str]) -> Callable[[str], T]:
        @wraps(clean_func)
        def cc_wrapper(text: str) -> T:
            try:
                return convert_function(text)
            except (ValueError, decimal.InvalidOperation):
                cleaned = clean_func(text)
                return convert_function(cleaned)

        return cc_wrapper

    return concrete_decorator


@then_convert(int)
def drop_punct(text: str) -> str:  # Callable[[str], str] is Not the *real* signature!
    return text.replace(",", "").replace("$", "")


# reveal_type(drop_punct)

REPL_then_convert_1 = """
>>> drop_punct("1,701")
1701
>>> drop_punct("97")
97
>>>
"""

REPL_then_convert_2 = """
>>> def drop_punct(text):
...    return text.replace(",", "").replace("$", "")
>>> drop_punct_int = then_convert(int)(drop_punct)
>>> drop_punct_int("1,701")
1701
>>> drop_punct_int("97")
97
>>>
"""

# Much nicer

from collections.abc import Callable
from typing import Any, TypeVar

# Defined Earlier:
# T = TypeVar('T')


def cleanse_before(
    cleanse_function: Callable[[str], Any]
) -> Callable[[Callable[[str], T]], Callable[[str], T]]:
    def concrete_decorator(converter: Callable[[str], T]) -> Callable[[str], T]:
        @wraps(converter)
        def cc_wrapper(text: str, **kwargs: Any) -> T:
            try:
                return converter(text, **kwargs)
            except (ValueError, decimal.InvalidOperation):
                cleaned = cleanse_function(text)
                return converter(cleaned, **kwargs)

        return cc_wrapper

    return concrete_decorator


def drop_punct2(text: str) -> str:
    return text.replace(",", "").replace("$", "")


@cleanse_before(drop_punct2)
def to_int(text: str, base: int = 10) -> int:
    return int(text, base)


to_int2 = cleanse_before(drop_punct2)(int)

# reveal_type(to_int)
# reveal_type(to_int2)
# reveal_type(int)

REPL_cleanse_before = """
>>> to_int("1,701")
1701
>>> to_int("97")
97
>>> to_int2("1,701")
1701
>>> to_int2("97")
97
"""

from collections.abc import Iterable, Iterator
from typing import cast, TypeAlias

# Note TypeVar T and ParamSpec P defined above
FloatFuncT: TypeAlias = Callable[..., Iterator[float]]
FDT = TypeVar("FDT", bound=FloatFuncT)


def normalized(mean: float, stdev: float) -> FDT:
    z_score: Callable[[float], float] = lambda x: (x - mean) / stdev

    def concrete_decorator(function: FDT) -> FDT:
        @wraps(function)
        def wrapped(data_arg: Iterable[float]) -> Iterator[float]:
            z = map(z_score, data_arg)
            return function(z)

        return cast(FDT, wrapped)

    return cast(FDT, concrete_decorator)


REPL_normalized = """
>>> d = [ 2, 4, 4, 4, 5, 5, 7, 9 ]
>>> from Chapter04.ch04_ex4 import mean, stdev
>>> m_d, s_d =  mean(d), stdev(d)
>>> @normalized(m_d, s_d)
... def norm_list(d):
...    return list(d)
>>> norm_list(d)
[-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]

Alternative, just to show it works.
>>> z = lambda x, m, s: (x-m)/s
>>> list(z(x, mean(d), stdev(d)) for x in d)
[-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]

>>> @normalized(m_d, s_d)
... def norm_sum(d):
...      return sum(d)
>>> norm_sum(d)
0.0

"""

__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
