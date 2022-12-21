"""Functional Python Programming 3e

Chapter 15, Example Set 5
"""

import sys

### Data Access Layer -- No Flask Components

from Chapter03.ch03_ex4 import series, head_split_fixed, row_iter
from collections.abc import Callable, Iterable
from typing import NamedTuple, Any, cast


class Pair(NamedTuple):
    x: float
    y: float

    @classmethod
    def create(cls: type["Pair"], source: Iterable[str]) -> "Pair":
        return Pair(*map(float, source))


class Series(NamedTuple):
    series: str
    data: list[Pair]

    @classmethod
    def create(
        cls: type["Series"], name: str, source: Iterable[tuple[str, str]]
    ) -> "Series":
        return Series(name, list(map(Pair.create, source)))

    def _as_listofdicts(self) -> list[dict[str, Any]]:
        return [p._asdict() for p in self.data]


from pathlib import Path


def get_series_map(source_path: Path) -> dict[str, Series]:
    with source_path.open() as source:
        raw_data = list(head_split_fixed(row_iter(source)))
        series_iter = (
            Series.create(id_str, series(id_num, raw_data))
            for id_num, id_str in enumerate(["I", "II", "III", "IV"])
        )
        mapping = {series.series: series for series in series_iter}
    return mapping


REPL_get_series_map = """
>>> source = Path.cwd() / "Anscombe.txt"
>>> get_series_map(source)['I']
Series(series='I', data=[Pair(x=10.0, y=8.04), Pair(x=8.0, y=6.95), ...])
"""


def anscombe_filter(set_id: str, raw_data_map: dict[str, Series]) -> Series:
    return raw_data_map[set_id]


from collections.abc import Callable
from typing import Any, TypeAlias

Serializer: TypeAlias = Callable[[list[dict[str, Any]]], bytes]


def serialize(format: str | None, data: list[dict[str, Any]], **kwargs: str) -> bytes:
    """Relies on global SERIALIZERS, set separately"""
    if format is None:
        format = "text/html"
    function = SERIALIZERS.get(format.lower(), serialize_html)
    return function(data, **kwargs)


from collections.abc import Callable
from typing import TypeVar, ParamSpec
from functools import wraps

T = TypeVar("T")
P = ParamSpec("P")


def to_bytes(function: Callable[P, str]) -> Callable[P, bytes]:
    @wraps(function)
    def decorated(*args: P.args, **kwargs: P.kwargs) -> bytes:
        text = function(*args, **kwargs)
        return text.encode("utf-8")

    return decorated


import json


@to_bytes
def serialize_json(data: list[dict[str, Any]], **kwargs: str) -> str:
    text = json.dumps(data, sort_keys=True)
    return text


REPL_serialize_json = """
>>> s = Series("test", [Pair(2,3), Pair(5,7)])
>>> serialize_json([row._asdict() for row in s.data])
b'[{"x": 2, "y": 3}, {"x": 5, "y": 7}]'
"""

import csv
import io


@to_bytes
def serialize_csv(data: list[dict[str, Any]], **kwargs: str) -> str:
    buffer = io.StringIO()
    wtr = csv.DictWriter(buffer, sorted(data[0].keys()))
    wtr.writeheader()
    wtr.writerows(data)
    return buffer.getvalue()


REPL_serialize_csv = """
>>> s = Series("test", [Pair(2,3), Pair(5,7)])
>>> serialize_csv([row._asdict() for row in s.data])
b'x,y\\r\\n2,3\\r\\n5,7\\r\\n'
"""

import string
from textwrap import dedent

XML_TEMPLATE = string.Template(
    dedent(
        """\
    <?xml version="1.0" encoding="utf-8"?>
    ${document}
    """
    )
)


@to_bytes
def serialize_xml(
    data: list[dict[str, Any]], *, document_tag: str = "Series", row_tag: str = "Pair"
) -> str:
    """
    >>> s = Series("test", [Pair(2,3), Pair(5,7)])
    >>> serialize_xml([row._asdict() for row in s.data], document_tag="Series", row_tag="Pair")
    b'<?xml version="1.0" encoding="utf-8"?>\\n<Series><Pair><x>2</x><y>3</y></Pair><Pair><x>5</x><y>7</y></Pair></Series>\\n'

    """
    cells_iter = ("".join(f"<{k}>{v!s}</{k}>" for k, v in row.items()) for row in data)
    rows = "".join(f"<{row_tag}>{cells}</{row_tag}>" for cells in cells_iter)
    document = f"<{document_tag}>{rows}</{document_tag}>"
    text = XML_TEMPLATE.substitute(document=document)
    return text


import string
from textwrap import dedent

HTML_TEMPLATE = string.Template(
    dedent(
        """\
    <html>
    <head><title>Anscombe Series</title></head>
    <body>
        <table>
            <thead>
                ${head}
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>
    </body>
    </html>
    """
    )
)


@to_bytes
def serialize_html(data: list[dict[str, Any]], **kwargs: str) -> str:
    """
    >>> s = Series("test", [Pair(2,3), Pair(5,7)])
    >>> serialize_html([row._asdict() for row in s.data])
    b'<html>...<tr><td column="x">2</td><td column="y">3</td></tr>\\n<tr><td column="x">5</td><td column="y">7</td></tr>...'
    """
    header_cells = "".join(f"<td>{name}</td>" for name in data[0].keys())
    header = f"<tr>{header_cells}</tr>"
    cells_iter = (
        "".join(f'<td column="{k}">{v!s}</td>' for k, v in row.items()) for row in data
    )
    rows = "\n".join(f"<tr>{cells}</tr>" for cells in cells_iter)
    text = HTML_TEMPLATE.substitute(head=header, rows=rows)
    return text


SERIALIZERS: dict[str, Serializer] = {
    "application/xml": serialize_xml,
    "text/html": serialize_html,
    "application/json": serialize_json,
    "text/csv": serialize_csv,
}


import pytest


def test_pair() -> None:
    p = Pair(*[3, 5])
    assert p.x == 3
    assert p.y == 5


def test_series() -> None:
    s = Series("test", [Pair(2, 3), Pair(5, 7)])
    assert s.series == "test"
    assert s.data[0] == Pair(2, 3)
    assert s.data[1] == Pair(5, 7)


def test_get_series_map() -> None:
    source = Path.cwd() / "Anscombe.txt"
    mapping = get_series_map(source)
    assert set(mapping.keys()) == {"I", "II", "III", "IV"}
    assert len(mapping["I"].data) == 11
    assert len(mapping["II"].data) == 11
    assert len(mapping["III"].data) == 11
    assert len(mapping["IV"].data) == 11


def test_anscombe_filter() -> None:
    s = Series("I", [Pair(2, 3), Pair(5, 7)])
    mapping = {s.series: s}
    assert anscombe_filter("I", mapping) == s
    with pytest.raises(KeyError):
        anscombe_filter("II", mapping)


def test_serialize() -> None:
    s = Series("I", [Pair(2, 3), Pair(5, 7)])
    assert serialize("text/csv", s._as_listofdicts()) == (b"x,y\r\n2,3\r\n5,7\r\n")
    assert serialize("application/json", s._as_listofdicts()) == (
        b'[{"x": 2, "y": 3}, {"x": 5, "y": 7}]'
    )
    html_content = serialize("text/html", s._as_listofdicts())
    assert b'<tr><td column="x">2</td><td column="y">3</td></tr>' in html_content
    assert b'<tr><td column="x">5</td><td column="y">7</td></tr>' in html_content
    assert serialize(
        "application/xml", s._as_listofdicts(), document_tag="Series", row_tag="Pair"
    ) == (
        b'<?xml version="1.0" encoding="utf-8"?>\n<Series><Pair><x>2</x><y>3</y></Pair><Pair><x>5</x><y>7</y></Pair></Series>\n'
    )


### Web Layer

from flask import Flask

app = Flask(__name__)


from pathlib import Path

app.config["FILE_PATH"] = Path.cwd() / "Anscombe.txt"

from flask import request, abort, make_response, Response


def format() -> str:
    if arg := request.args.get("form"):
        try:
            return {
                "xml": "application/xml",
                "html": "text/html",
                "json": "application/json",
                "csv": "text/csv",
            }[arg]
        except KeyError:
            abort(404, "Unknown ?form=")
    else:
        return request.accept_mimetypes.best or "text/html"


from flask import request, abort, make_response, Response


@app.route("/anscombe/")
def index_view() -> Response:
    # 1. Validate
    response_format = format()
    # 2. Get data
    data = get_series_map(app.config["FILE_PATH"])
    index_listofdicts = [{"Series": k} for k in data.keys()]
    # 3. Prepare Response
    try:
        content_bytes = serialize(
            response_format, index_listofdicts, document_tag="Index", row_tag="Series"
        )
        response = make_response(content_bytes, 200, {"Content-Type": response_format})
        return response
    except KeyError:
        abort(404, f"Unknown {response_format=}")


@app.route("/anscombe/<series_id>")
def series_view(series_id: str, form: str | None = None) -> Response:
    # 1. Validate
    response_format = format()
    # 2. Get data (and validate some more)
    data = get_series_map(app.config["FILE_PATH"])
    try:
        dataset = anscombe_filter(series_id, data)._as_listofdicts()
    except KeyError:
        abort(404, "Unknown Series")
    # 3. Prepare Response
    try:
        content_bytes = serialize(
            response_format, dataset, document_tag="Series", row_tag="Pair"
        )
        response = make_response(content_bytes, 200, {"Content-Type": response_format})
        return response
    except KeyError:
        abort(404, f"Unknown {response_format=}")


import yaml
from flask import jsonify
from flask.testing import FlaskClient
from collections.abc import Iterator
from os import environ


@app.route("/openapi.json")
def openapi_view() -> Response:
    with (
        Path(environ.get('CH15_OPENAPIPATH', '.')) / "openapi.yaml"
    ).open() as source:
        spec = yaml.load(source, Loader=yaml.SafeLoader)
    return jsonify(spec)


@pytest.fixture()
def test_app() -> Iterator[Flask]:
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def app_client(test_app: Flask) -> FlaskClient:
    return test_app.test_client()


def test_index_view(app_client: FlaskClient) -> None:
    response = app_client.get("/anscombe", follow_redirects=True)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html"
    assert "<html>" in response.data.decode("utf-8")
    response_2 = app_client.get(
        "/anscombe", headers={"Accept": "application/json"}, follow_redirects=True
    )
    assert response_2.status_code == 200
    assert response_2.headers["Content-Type"] == "application/json"
    assert response_2.json == [
        {"Series": "I"},
        {"Series": "II"},
        {"Series": "III"},
        {"Series": "IV"},
    ]


def test_series_view(app_client: FlaskClient) -> None:
    response = app_client.get("/anscombe/I")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html"
    assert "<html>" in response.data.decode("utf-8")
    response_2 = app_client.get("/anscombe/I", headers={"Accept": "application/json"})
    assert response_2.status_code == 200
    assert response_2.headers["Content-Type"] == "application/json"
    assert response_2.json == [
        {"x": 10.0, "y": 8.04},
        {"x": 8.0, "y": 6.95},
        {"x": 13.0, "y": 7.58},
        {"x": 9.0, "y": 8.81},
        {"x": 11.0, "y": 8.33},
        {"x": 14.0, "y": 9.96},
        {"x": 6.0, "y": 7.24},
        {"x": 4.0, "y": 4.26},
        {"x": 12.0, "y": 10.84},
        {"x": 7.0, "y": 4.82},
        {"x": 5.0, "y": 5.68},
    ]


def test_openapi(app_client: FlaskClient) -> None:
    response = app_client.get("/openapi.json", follow_redirects=True)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json["info"]["title"] == "Anscombe Server"  # type: ignore[index]
    assert response.json["info"]["version"] == "1.0.0"  # type: ignore[index]


__test__ = {name: value for name, value in globals().items() if name.startswith("REPL")}

if __name__ == "__main__":
    app.run(debug=True)
