"""Functional Python Programming 3e

Chapter 3, Example Set 2
"""

from decimal import Decimal

from decimal import Decimal


def clean_decimal(text: str | None) -> Decimal | None:
    if text is None:
        return None
    return Decimal(text.replace("$", "").replace(",", ""))


def test_clean_decimal() -> None:
    assert clean_decimal("$1,234.56") == Decimal("1234.56")
    assert clean_decimal(None) is None


"""Prefix function for str.replace(a,b)."""


def replace(text: str, a: str, b: str) -> str:
    return text.replace(a, b)


def test_replace() -> None:
    assert replace("$123", "$", "") == "123"


def clean_decimal_2(text: str | None) -> Decimal | None:
    if text is None:
        return None
    return Decimal(replace(replace(text, "$", ""), ",", ""))


def test_clean_decimal_2() -> None:
    assert clean_decimal_2("$1,234.56") == Decimal("1234.56")
    assert clean_decimal_2(None) is None


def remove(text: str, chars: str) -> str:
    """Remove all of the given chars from a string."""
    if chars:
        return remove(text.replace(chars[0], ""), chars[1:])
    return text


def clean_decimal_3(text: str | None) -> Decimal | None:
    if text is None:
        return None
    return Decimal(remove(text, "$,"))


def test_clean_decimal_3() -> None:
    assert clean_decimal_3("$1,234.56") == Decimal("1234.56")
    assert clean_decimal_3(None) is None


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}
