"""Functional Python Programming 3e

Chapter 15, Example Set 1
"""
import http.client
import urllib.request
from contextlib import closing
from pathlib import Path

import urllib.request


def urllib_get(url: str) -> tuple[int, str]:
    with urllib.request.urlopen(url) as response:
        body_bytes = response.read()
        encoding = response.headers.get_content_charset("utf-8")
        return response.status, body_bytes.decode(encoding)


import pytest


@pytest.mark.internet_required
def test_urllib_get() -> None:
    status, content = urllib_get("https://slott-softwarearchitect.blogspot.com")
    assert status == 200
    assert content.startswith("<!DOCTYPE html>")


from unittest.mock import Mock, MagicMock, call


@pytest.fixture
def mock_urlopen(monkeypatch: pytest.MonkeyPatch) -> Mock:
    mock_urlopen = Mock(
        return_value=MagicMock(
            __enter__=Mock(
                name="urlopen function",
                return_value=Mock(
                    name="urlopen instance",
                    read=Mock(return_value=b"<!DOCTYPE html>"),
                    status=200,
                    headers=Mock(get_content_charset=Mock(return_value="utf-8")),
                ),
            )
        )
    )
    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)
    return mock_urlopen


def test_get_with_mock(mock_urlopen: Mock) -> None:
    status, content = urllib_get("https://slott-softwarearchitect.blogspot.com")
    assert status == 200
    assert content.startswith("<!DOCTYPE html>")
    assert mock_urlopen.mock_calls == [
        call("https://slott-softwarearchitect.blogspot.com")
    ]


# Using http.client instead of urllib.request
def client_demo(url: str, save_as: Path) -> None:
    with closing(http.client.HTTPConnection(url, 80)) as server:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        }
        server.request("GET", "/", headers=headers)
        response = server.getresponse()
        print(response.status, response.reason)
        body = response.read()
        print(body)
        with save_as.open("wb") as result:
            result.write(body)


if __name__ == "__main__":
    urllib_get("https://slott-softwarearchitect.blogspot.com")
