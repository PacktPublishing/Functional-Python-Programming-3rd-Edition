"""Functional Python Programming 3e

Chapter 15, Example Set 2
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import NoReturn


def server_demo() -> NoReturn:
    httpd = HTTPServer(("localhost", 8080), SimpleHTTPRequestHandler)
    print(f"Serving on http://localhost:8080...")
    while True:
        httpd.handle_request()
    httpd.shutdown()


import urllib.request


def urllib_get(url: str) -> tuple[int, str]:
    with urllib.request.urlopen(url) as response:
        body_bytes = response.read()
        encoding = response.headers.get_content_charset("utf-8")
        return response.status, body_bytes.decode(encoding)


from pathlib import Path
import pytest


@pytest.mark.server_file("Chapter15/ch15_ex2.py")
def test_server(running_server: Path) -> None:
    expected_body = (Path.cwd() / "Chapter15" / "demo.file").read_text()
    status, body = urllib_get("http://localhost:8080/Chapter15/demo.file")
    assert body == expected_body
    assert status == 200


if __name__ == "__main__":
    print("Starting demo")
    server_demo()
