"""Functional Python Programming 3e

Chapter 15, Example Set 3
"""

from collections.abc import Iterable
from wsgiref.simple_server import make_server, demo_app
import wsgiref.util
import urllib
import urllib.parse
from pathlib import Path
import sys

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed.wsgi import WSGIApplication, WSGIEnvironment, StartResponse

from textwrap import dedent

TEST_TEMPLATE = dedent(
    """\
    <!DOCTYPE html>
    <html>
    <head><title>Run Tests</title></head>
    <body>
    <h1>Tests</h1>
    <p>Results</p>
    <pre><code>{0}
    </code></pre>
    <form method="POST" action="">
    <hr/>
    <input type="submit" value="Run Tests"/>
    </form>
    </body>
    </html>
    """
)


def selftest_app(
    environ: "WSGIEnvironment", start_response: "StartResponse"
) -> Iterable[bytes]:
    """Runs the unit test suite."""
    if environ["REQUEST_METHOD"] == "GET":
        # send form and previous results (if any)
        if environ["QUERY_STRING"]:
            query = urllib.parse.parse_qs(environ["QUERY_STRING"])
            file_path = Path(environ["TMPDIR"]) / query["filename"][0]
            with file_path.open() as result_file:
                results = result_file.read()
        else:
            results = ""
        page = TEST_TEMPLATE.format(results)
        content = page.encode("utf-8")
        headers = [
            ("Content-Type", 'text/html; charset="utf-8"'),
            ("Content-Length", str(len(content))),
        ]
        start_response("200 OK", headers)
        return [content]
    elif environ["REQUEST_METHOD"] == "POST":
        # Run doctest, collect data in a cache file
        import doctest
        from contextlib import redirect_stdout, redirect_stderr

        file_path = Path(environ["TMPDIR"]) / "results.log"
        with file_path.open("w") as result_file:
            with redirect_stdout(result_file), redirect_stderr(result_file):
                for file_path in Path.cwd().glob("*.py"):
                    doctest.testfile(str(file_path))
        filename_query = {"filename": file_path.name}
        encoded_filename = urllib.parse.urlencode(filename_query)
        headers = [("Location", f"/test?{encoded_filename}")]
        start_response("302 FOUND", headers)
        return []
    start_response("400 NOT ALLOWED", [])
    return []


INDEX_TEMPLATE_HEAD = dedent(
    """\
    <!DOCTYPE html>
    <html>
    <head><title>Chapter 15</title></head>
    <body><h1>Files in {0}</h1>
    """
)

INDEX_TEMPLATE_FOOT = dedent(
    """
    </body></html>
    """
)


def index_app(
    environ: "WSGIEnvironment", start_response: "StartResponse"
) -> Iterable[bytes]:
    """Displays an index of available files."""
    log = environ["wsgi.errors"]
    print("PATH_INFO '{0}'".format(environ["PATH_INFO"]), file=log)
    page = INDEX_TEMPLATE_HEAD.format(environ.get("PATH_INFO", "."))
    for entry in (Path.cwd() / environ["PATH_INFO"][1:]).glob("*"):
        if entry.name.startswith("."):
            continue
        rel_path = entry.relative_to(Path.cwd())
        page += '<p><a href="/static/{0}">{1}</a></p>'.format(rel_path, entry.name)
    page += INDEX_TEMPLATE_FOOT
    content = page.encode("utf-8")
    headers = [
        ("Content-Type", 'text/html; charset="utf-8"'),
        ("Content-Length", str(len(content))),
    ]
    start_response("200 OK", headers)
    return [content]


def headers(content: bytes) -> list[tuple[str, str]]:
    return [
        ("Content-Type", 'text/plain;charset="utf-8"'),
        ("Content-Length", str(len(content))),
    ]


def static_text_app(
    environ: "WSGIEnvironment", start_response: "StartResponse"
) -> Iterable[bytes]:
    log = environ["wsgi.errors"]
    try:
        static_path = Path.cwd() / environ["PATH_INFO"][1:]
        with static_path.open() as static_file:
            print(f"{static_path=}", file=log)
            content = static_file.read().encode("utf-8")
            start_response("200 OK", headers(content))
            return [content]
    except IsADirectoryError as exc:
        return index_app(environ, start_response)
    except FileNotFoundError as exc:
        print(f"{static_path=} {exc=}", file=log)
        message = f"Not Found {environ['PATH_INFO']}".encode("utf-8")
        start_response("404 NOT FOUND", headers(message))
        return [message]


WELCOME_TEMPLATE = dedent(
    """\
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Chapter 15</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    </head>
    <body>
    <div class="container">
    <h1>Chapter 15</h1>
    <p><a href="demo" class="btn btn-default" role="button">The WSGI Demo App</a></p>
    <p><a href="static" class="btn btn-default" role="button">All Files</a></p>
    <p><a href="static/Chapter15/ch15_ex3.py" class="btn btn-default" role="button">This File</a></p>
    </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    </body>
    </html>
    """
)


def welcome_app(
    environ: "WSGIEnvironment", start_response: "StartResponse"
) -> Iterable[bytes]:
    """Displays a page of greeting information."""
    content = WELCOME_TEMPLATE.encode("utf-8")
    headers = [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(content))),
    ]
    start_response("200 OK", headers)
    return [content]


from wsgiref.simple_server import demo_app

SCRIPT_MAP: dict[str, "WSGIApplication"] = {
    "demo": demo_app,
    "static": static_text_app,
    "index.html": welcome_app,
    "": welcome_app,
}


def routing(
    environ: "WSGIEnvironment", start_response: "StartResponse"
) -> Iterable[bytes]:
    top_level = wsgiref.util.shift_path_info(environ)
    if top_level:
        app = SCRIPT_MAP.get(top_level, welcome_app)
    else:
        app = welcome_app
    content = app(environ, start_response)
    return content


def server_demo() -> None:
    httpd = make_server("", 8080, routing)
    print("Serving HTTP on port 8080...")

    # Respond to requests until process is killed
    httpd.serve_forever()


import urllib.request


def urllib_get(url: str) -> tuple[int, str]:
    with urllib.request.urlopen(url) as response:
        body_bytes = response.read()
        encoding = response.headers.get_content_charset("utf-8")
        return response.status, body_bytes.decode(encoding)


import pytest


@pytest.mark.server_file("Chapter15/ch15_ex3.py")
def test_server(running_server: Path) -> None:
    # demo app part of WSGI ref
    status, body = urllib_get("http://localhost:8080/demo/some/path/to/data")
    assert status == 200
    print(body)

    # static
    status, body = urllib_get("http://localhost:8080/static/Chapter15/demo.file")
    assert status == 200
    assert body == (Path.cwd() / "Chapter15" / "demo.file").read_text()

    # static/index
    status, body = urllib_get("http://localhost:8080/static/")
    assert status == 200
    assert "<h1>Files in /</h1>" in body

    # welcome
    status, body = urllib_get("http://localhost:8080/welcome/")
    assert status == 200
    assert body == WELCOME_TEMPLATE


if __name__ == "__main__":
    server_demo()
