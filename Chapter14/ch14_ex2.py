#!/usr/bin/env python3
"""Functional Python Programming

Chapter 14, Example Set 2
"""

# Some sample log lines for testing.

sample = """\
99.49.32.197 - - [01/Jun/2012:22:17:54 -0400] "GET /favicon.ico HTTP/1.1" 200 894 "-" "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"
66.249.71.25 - - [01/Jun/2012:22:17:55 -0400] "GET /book/python-2.6/html/p02/p02c10_adv_seq.html HTTP/1.1" 200 121825 "-" "Mediapartners-Google"
176.53.58.137 - - [01/Jun/2012:22:18:18 -0400] "GET /book/python-2.6/html/p04/p04c09_architecture.html HTTP/1.0" 200 193000 "http://www.itmaybeahack.com/book/python-2.6/html/p04/p04c09_architecture.html" "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0 ; .NET CLR 2.0.50215; SL Commerce Client v1.0; Tablet PC 2.0"
176.53.58.137 - - [01/Jun/2012:22:18:20 -0400] "GET /p03/p03c04_extending.html HTTP/1.0" 404 331 "http://www.itmaybeahack.com/p03/p03c04_extending.html" "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0 ; .NET CLR 2.0.50215; SL Commerce Client v1.0; Tablet PC 2.0"
176.53.58.137 - - [01/Jun/2012:22:18:20 -0400] "GET /p03c04_extending.html HTTP/1.0" 404 331 "http://www.itmaybeahack.com/p03c04_extending.html" "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0 ; .NET CLR 2.0.50215; SL Commerce Client v1.0; Tablet PC 2.0"
137.111.13.200 - - [01/Jun/2012:22:18:32 -0400] "GET /homepage/books/nonprog/html/_static/doctools.js HTTP/1.1" 200 6618 "http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5"
137.111.13.200 - - [01/Jun/2012:22:18:28 -0400] "GET /homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html HTTP/1.1" 200 29101 "http://www.google.com.au/url?sa=t&rct=j&q=defaultdict%20list&source=web&cd=3&ved=0CFoQFjAC&url=http%3A%2F%2Fwww.itmaybeahack.com%2Fhomepage%2Fbooks%2Fnonprog%2Fhtml%2Fp10_set_map%2Fp10_c04_defaultdict.html&ei=z3fJT8-nHce3iQfo6ZnNBg&usg=AFQjCNFckv6gmMcbvtMFDOyjAcVlQDiYvA&sig2=i12vAm4yVbB0QyMgUZmEgg" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5"
137.111.13.200 - - [01/Jun/2012:22:18:33 -0400] "GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1" 200 3224 "http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5"
"""

# Stage I: Lines of source.

from collections.abc import Iterator
import gzip
from pathlib import Path

import sys


def local_gzip(zip_path: Path) -> Iterator[str]:
    with gzip.open(zip_path, "rb") as log_file:
        yield from (line.decode("us-ascii").rstrip() for line in log_file)


from collections.abc import Iterator
import itertools
import ftplib
from typing import Any


def remote_source(**credentials: Any) -> Iterator[str]:
    """Web Hosting FTP URL.
    First, downloads the files. Then,
    uses local_gzip() to yield a sequence strings.
    """
    with ftplib.FTP("ftp.itmaybeahack.com", **credentials) as ftp:
        try:
            ftp.login()
        except ftplib.error_perm as e:
            if e.args[0].startswith("530"):
                pass
            else:
                raise
        ftp.cwd("logs")
        downloads: list[Path] = []
        for name in ftp.nlst():
            if name.startswith("."):
                continue
            command = "RETR {0}".format(name)
            ftp.retrbinary(command, open(name, "wb").write)
            downloads.append(Path(name))
        ftp.quit()
    return itertools.chain.from_iterable(map(local_gzip, downloads))


import pytest


@pytest.fixture
def example_log_dir(tmp_path: Path) -> Path:
    target = tmp_path / "example.log.gz"
    with gzip.open(target, "wb") as example:
        example.write(sample.encode("us-ascii"))
    return tmp_path


def test_local_gzip(example_log_dir: Path) -> None:
    data = list(local_gzip(example_log_dir / "example.log.gz"))
    assert [len(line) for line in data] == [187, 144, 317, 266, 258, 335, 559, 336]


# Stage II: Access objects

from typing import NamedTuple, Optional, cast
import re


class Access(NamedTuple):
    host: str
    identity: str
    user: str
    time: str
    request: str
    status: str
    bytes: str
    referer: str
    user_agent: str

    @classmethod
    def create(cls: type, line: str) -> Optional["Access"]:
        format_pat = re.compile(
            r"(?P<host>[\d\.]+)\s+"
            r"(?P<identity>\S+)\s+"
            r"(?P<user>\S+)\s+"
            r"\[(?P<time>.+?)\]\s+"
            r'"(?P<request>.+?)"\s+'
            r"(?P<status>\d+)\s+"
            r"(?P<bytes>\S+)\s+"
            r'"(?P<referer>.*?)"\s+'
            r'"(?P<user_agent>.+?)"\s*'
        )
        if match := format_pat.match(line):
            return cast(Access, cls(**match.groupdict()))
        return None


from collections.abc import Iterator


def access_iter(source_iter: Iterator[str]) -> Iterator[Access]:
    for line in source_iter:
        if access := Access.create(line):
            yield access


def access_iter_2(source_iter: Iterator[str]) -> Iterator[Access]:
    return filter(None, map(Access.create, source_iter))


import itertools


def test_access_iter(example_log_dir: Path) -> None:
    file_iter = example_log_dir.glob("*.log.gz")
    lines = itertools.chain.from_iterable(map(local_gzip, file_iter))
    data = list(access_iter(lines))
    assert len(data) == 8
    assert data[0] == Access(
        host="99.49.32.197",
        identity="-",
        user="-",
        time="01/Jun/2012:22:17:54 -0400",
        request="GET /favicon.ico HTTP/1.1",
        status="200",
        bytes="894",
        referer="-",
        user_agent="Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
    )
    assert data[-1] == Access(
        host="137.111.13.200",
        identity="-",
        user="-",
        time="01/Jun/2012:22:18:33 -0400",
        request="GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1",
        status="200",
        bytes="3224",
        referer="http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5",
    )


def test_access_iter_2(example_log_dir: Path) -> None:
    file_iter = example_log_dir.glob("*.log.gz")
    lines = itertools.chain.from_iterable(map(local_gzip, file_iter))
    data = list(access_iter_2(lines))
    assert len(data) == 8
    assert data[0] == Access(
        host="99.49.32.197",
        identity="-",
        user="-",
        time="01/Jun/2012:22:17:54 -0400",
        request="GET /favicon.ico HTTP/1.1",
        status="200",
        bytes="894",
        referer="-",
        user_agent="Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
    )
    assert data[-1] == Access(
        host="137.111.13.200",
        identity="-",
        user="-",
        time="01/Jun/2012:22:18:33 -0400",
        request="GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1",
        status="200",
        bytes="3224",
        referer="http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html",
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5",
    )


# Stage III. Access Details objects

from typing import NamedTuple, Optional
import datetime
import urllib.parse


class AccessDetails(NamedTuple):
    access: Access
    time: datetime.datetime
    method: str
    url: urllib.parse.ParseResult
    protocol: str
    referrer: urllib.parse.ParseResult
    agent: dict[str, str]

    @classmethod
    def create(cls: type, access: Access) -> "AccessDetails":
        meth, url, protocol = parse_request(access.request)
        return AccessDetails(
            access=access,
            time=parse_time(access.time),
            method=meth,
            url=urllib.parse.urlparse(url),
            protocol=protocol,
            referrer=urllib.parse.urlparse(access.referer),
            agent=parse_agent(access.user_agent),
        )


from typing import Optional
import datetime
import re


def parse_request(request: str) -> tuple[str, str, str]:
    words = request.split()
    return words[0], " ".join(words[1:-1]), words[-1]


def parse_time(ts: str) -> datetime.datetime:
    return datetime.datetime.strptime(ts, "%d/%b/%Y:%H:%M:%S %z")


def parse_agent(user_agent: str) -> dict[str, str]:
    agent_pat = re.compile(
        r"(?P<product>\S*?)\s+"
        r"\((?P<system>.*?)\)\s*"
        r"(?P<platform_details_extensions>.*)"
    )

    if agent_match := agent_pat.match(user_agent):
        return agent_match.groupdict()
    return {}


from collections.abc import Iterable, Iterator


def access_detail_iter(access_iter: Iterable[Access]) -> Iterator[AccessDetails]:
    for access in access_iter:
        yield AccessDetails.create(access)


from collections.abc import Iterable, Iterator


def access_detail_iter_2(access_iter: Iterable[Access]) -> Iterator[AccessDetails]:
    return map(AccessDetails.create, access_iter)


def test_access_detail_iter(example_log_dir: Path) -> None:
    file_iter = example_log_dir.glob("*.log.gz")
    lines = itertools.chain.from_iterable(map(local_gzip, file_iter))
    data = list(access_detail_iter(access_iter(lines)))
    assert len(data) == 8
    assert data[0] == AccessDetails(
        access=Access(
            host="99.49.32.197",
            identity="-",
            user="-",
            time="01/Jun/2012:22:17:54 -0400",
            request="GET /favicon.ico HTTP/1.1",
            status="200",
            bytes="894",
            referer="-",
            user_agent="Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        ),
        time=datetime.datetime(
            2012,
            6,
            1,
            22,
            17,
            54,
            tzinfo=datetime.timezone(datetime.timedelta(-1, 72000)),
        ),
        method="GET",
        url=ParseResult(
            scheme="", netloc="", path="/favicon.ico", params="", query="", fragment=""
        ),
        protocol="HTTP/1.1",
        referrer=ParseResult(
            scheme="", netloc="", path="-", params="", query="", fragment=""
        ),
        agent=dict(
            product="Mozilla/5.0",
            system="Windows NT 6.0",
            platform_details_extensions="AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        ),
    )
    assert data[-1] == AccessDetails(
        access=Access(
            host="137.111.13.200",
            identity="-",
            user="-",
            time="01/Jun/2012:22:18:33 -0400",
            request="GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1",
            status="200",
            bytes="3224",
            referer="http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5",
        ),
        time=datetime.datetime(
            2012,
            6,
            1,
            22,
            18,
            33,
            tzinfo=datetime.timezone(datetime.timedelta(-1, 72000)),
        ),
        method="GET",
        url=ParseResult(
            scheme="",
            netloc="",
            path="/homepage/books/nonprog/html/_static/pygments.css",
            params="",
            query="",
            fragment="",
        ),
        protocol="HTTP/1.1",
        referrer=ParseResult(
            scheme="http",
            netloc="www.itmaybeahack.com",
            path="/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html",
            params="",
            query="",
            fragment="",
        ),
        agent=dict(
            product="Mozilla/5.0",
            system="Macintosh; Intel Mac OS X 10_7_4",
            platform_details_extensions="AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5",
        ),
    )


from urllib.parse import ParseResult


def test_access_detail_iter_2(example_log_dir: Path) -> None:
    file_iter = example_log_dir.glob("*.log.gz")
    lines = itertools.chain.from_iterable(map(local_gzip, file_iter))
    data = list(access_detail_iter_2(access_iter_2(lines)))
    assert len(data) == 8
    assert data[0] == AccessDetails(
        access=Access(
            host="99.49.32.197",
            identity="-",
            user="-",
            time="01/Jun/2012:22:17:54 -0400",
            request="GET /favicon.ico HTTP/1.1",
            status="200",
            bytes="894",
            referer="-",
            user_agent="Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        ),
        time=datetime.datetime(
            2012,
            6,
            1,
            22,
            17,
            54,
            tzinfo=datetime.timezone(datetime.timedelta(-1, 72000)),
        ),
        method="GET",
        url=ParseResult(
            scheme="", netloc="", path="/favicon.ico", params="", query="", fragment=""
        ),
        protocol="HTTP/1.1",
        referrer=ParseResult(
            scheme="", netloc="", path="-", params="", query="", fragment=""
        ),
        agent=dict(
            product="Mozilla/5.0",
            system="Windows NT 6.0",
            platform_details_extensions="AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        ),
    )
    assert data[-1] == AccessDetails(
        access=Access(
            host="137.111.13.200",
            identity="-",
            user="-",
            time="01/Jun/2012:22:18:33 -0400",
            request="GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1",
            status="200",
            bytes="3224",
            referer="http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5",
        ),
        time=datetime.datetime(
            2012,
            6,
            1,
            22,
            18,
            33,
            tzinfo=datetime.timezone(datetime.timedelta(-1, 72000)),
        ),
        method="GET",
        url=ParseResult(
            scheme="",
            netloc="",
            path="/homepage/books/nonprog/html/_static/pygments.css",
            params="",
            query="",
            fragment="",
        ),
        protocol="HTTP/1.1",
        referrer=ParseResult(
            scheme="http",
            netloc="www.itmaybeahack.com",
            path="/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html",
            params="",
            query="",
            fragment="",
        ),
        agent=dict(
            product="Mozilla/5.0",
            system="Macintosh; Intel Mac OS X 10_7_4",
            platform_details_extensions="AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5",
        ),
    )


# Stage IV: Reduce clutter

from typing import Iterable, Iterator


def non_empty_path(detail: AccessDetails) -> bool:
    path = detail.url.path.split("/")
    return any(path)


def non_excluded_names(detail: AccessDetails) -> bool:
    "Exclude by name; include names not in a list."
    name_exclude = {
        "favicon.ico",
        "robots.txt",
        "index.php",
        "humans.txt",
        "a2test",
        "ping",
        "dompdf.php",
        "crossdomain.xml",
        "_images",
        "search.html",
        "genindex.html",
        "searchindex.js",
        "modindex.html",
        "py-modindex.html",
    }
    path = detail.url.path.split("/")
    return not any(p in name_exclude for p in path)


def non_excluded_ext(detail: AccessDetails) -> bool:
    "Exclude by extension; include names not in a list."
    ext_exclude = {
        ".png",
        ".js",
        ".css",
    }
    path = detail.url.path.split("/")
    final = path[-1]
    return not any(final.endswith(ext) for ext in ext_exclude)


def path_filter(
    access_details_iter: Iterable[AccessDetails],
) -> Iterable[AccessDetails]:
    non_empty = filter(non_empty_path, access_details_iter)
    nx_name = filter(non_excluded_names, non_empty)
    nx_ext = filter(non_excluded_ext, nx_name)
    yield from nx_ext


def test_path_filter(example_log_dir: Path) -> None:
    file_iter = example_log_dir.glob("*.log.gz")
    lines = itertools.chain.from_iterable(map(local_gzip, file_iter))
    data = access_detail_iter(access_iter(lines))
    clean_data = list(path_filter(data))
    assert len(clean_data) == 5
    assert clean_data[0] == AccessDetails(
        access=Access(
            host="66.249.71.25",
            identity="-",
            user="-",
            time="01/Jun/2012:22:17:55 -0400",
            request="GET /book/python-2.6/html/p02/p02c10_adv_seq.html HTTP/1.1",
            status="200",
            bytes="121825",
            referer="-",
            user_agent="Mediapartners-Google",
        ),
        time=datetime.datetime(
            2012,
            6,
            1,
            22,
            17,
            55,
            tzinfo=datetime.timezone(datetime.timedelta(-1, 72000)),
        ),
        method="GET",
        url=ParseResult(
            scheme="",
            netloc="",
            path="/book/python-2.6/html/p02/p02c10_adv_seq.html",
            params="",
            query="",
            fragment="",
        ),
        protocol="HTTP/1.1",
        referrer=ParseResult(
            scheme="", netloc="", path="-", params="", query="", fragment=""
        ),
        agent={},
    )
    assert clean_data[-1] == AccessDetails(
        access=Access(
            host="137.111.13.200",
            identity="-",
            user="-",
            time="01/Jun/2012:22:18:28 -0400",
            request="GET /homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html HTTP/1.1",
            status="200",
            bytes="29101",
            referer="http://www.google.com.au/url?sa=t&rct=j&q=defaultdict%20list&source=web&cd=3&ved=0CFoQFjAC&url=http%3A%2F%2Fwww.itmaybeahack.com%2Fhomepage%2Fbooks%2Fnonprog%2Fhtml%2Fp10_set_map%2Fp10_c04_defaultdict.html&ei=z3fJT8-nHce3iQfo6ZnNBg&usg=AFQjCNFckv6gmMcbvtMFDOyjAcVlQDiYvA&sig2=i12vAm4yVbB0QyMgUZmEgg",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5",
        ),
        time=datetime.datetime(
            2012,
            6,
            1,
            22,
            18,
            28,
            tzinfo=datetime.timezone(datetime.timedelta(-1, 72000)),
        ),
        method="GET",
        url=ParseResult(
            scheme="",
            netloc="",
            path="/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html",
            params="",
            query="",
            fragment="",
        ),
        protocol="HTTP/1.1",
        referrer=ParseResult(
            scheme="http",
            netloc="www.google.com.au",
            path="/url",
            params="",
            query="sa=t&rct=j&q=defaultdict%20list&source=web&cd=3&ved=0CFoQFjAC&url=http%3A%2F%2Fwww.itmaybeahack.com%2Fhomepage%2Fbooks%2Fnonprog%2Fhtml%2Fp10_set_map%2Fp10_c04_defaultdict.html&ei=z3fJT8-nHce3iQfo6ZnNBg&usg=AFQjCNFckv6gmMcbvtMFDOyjAcVlQDiYvA&sig2=i12vAm4yVbB0QyMgUZmEgg",
            fragment="",
        ),
        agent=dict(
            product="Mozilla/5.0",
            system="Macintosh; Intel Mac OS X 10_7_4",
            platform_details_extensions="AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5",
        ),
    )


from collections.abc import Iterable, Iterator


def book_filter(
    access_details_iter: Iterable[AccessDetails],
) -> Iterator[AccessDetails]:
    def book_in_path(detail: AccessDetails) -> bool:
        path = tuple(item for item in detail.url.path.split("/") if item)
        return path[0] == "book" and len(path) > 1

    return filter(book_in_path, access_details_iter)


def test_book_filter(example_log_dir: Path) -> None:
    file_iter = example_log_dir.glob("*.log.gz")
    lines = itertools.chain.from_iterable(map(local_gzip, file_iter))
    data = list(book_filter(path_filter(access_detail_iter(access_iter(lines)))))
    books = list(d.url.path for d in data)
    assert books == [
        "/book/python-2.6/html/p02/p02c10_adv_seq.html",
        "/book/python-2.6/html/p04/p04c09_architecture.html",
    ]


from collections import Counter


def reduce_book_total(access_details_iter: Iterable[AccessDetails]) -> dict[str, int]:
    counts: Counter[str] = Counter(detail.url.path for detail in access_details_iter)
    return counts


def test_book_count(example_log_dir: Path) -> None:
    file_iter = example_log_dir.glob("*.log.gz")
    lines = itertools.chain.from_iterable(map(local_gzip, file_iter))
    data = list(book_filter(path_filter(access_detail_iter(access_iter(lines)))))
    totals = reduce_book_total(data)
    assert list((k, totals[k]) for k in sorted(totals.keys())) == [
        ("/book/python-2.6/html/p02/p02c10_adv_seq.html", 1),
        ("/book/python-2.6/html/p04/p04c09_architecture.html", 1),
    ]


def analysis(log_path: Path) -> dict[str, int]:
    """Count book chapters in a given log"""
    details = access_detail_iter(access_iter(local_gzip(log_path)))
    books = book_filter(path_filter(details))
    totals = reduce_book_total(books)
    return totals


from collections.abc import Callable
from typing import cast, Any, TypeAlias
from functools import wraps
import time

FuncT: TypeAlias = Callable[..., Any]
DecoT: TypeAlias = Callable[[FuncT], FuncT]


def show_time(label: str) -> DecoT:
    def show_time_decorator(function: FuncT) -> FuncT:
        @wraps(function)
        def timed_function(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = function(*args, **kwargs)
            end = time.perf_counter()
            print(f"{label} time: {end - start:.2f}s")

        return cast(FuncT, timed_function)

    return cast(DecoT, show_time_decorator)


SAMPLE_DATA = Path.home() / "Documents" / "Work" / "ItMayBeAHack"
LOG_PATTERN = "*itmaybeahack.com*.gz"

import multiprocessing
from concurrent import futures


@show_time("multiprocessing/imap_unordered")
def demo_mp(root: Path = SAMPLE_DATA, pool_size: int | None = None) -> None:
    pool_size = multiprocessing.cpu_count() if pool_size is None else pool_size
    combined: Counter[str] = Counter()
    with multiprocessing.Pool(pool_size) as workers:
        file_iter = list(root.glob(LOG_PATTERN))
        results_iter = workers.imap_unordered(analysis, file_iter)
        for result in results_iter:
            combined.update(result)
    print(combined)


@show_time("multiprocessing/map_async")
def demo_mp_async(root: Path = SAMPLE_DATA, pool_size: int | None = None) -> None:
    pool_size = multiprocessing.cpu_count() if pool_size is None else pool_size
    combined: Counter[str] = Counter()
    with multiprocessing.Pool(pool_size) as workers:
        file_iter = root.glob(LOG_PATTERN)
        results = workers.map_async(analysis, file_iter)
        for result in results.get():
            combined.update(result)
    print(combined)


@show_time("concurrent.futures/threadpool")
def demo_cf_threads(root: Path = SAMPLE_DATA, pool_size: int = 4) -> None:
    pattern = "*itmaybeahack.com*.gz"
    combined: Counter[str] = Counter()
    with futures.ProcessPoolExecutor(max_workers=pool_size) as workers:
        file_iter = root.glob(LOG_PATTERN)
        for result in workers.map(analysis, file_iter):
            combined.update(result)
    print(combined)


@show_time("concurrent.futures/processpool")
def demo_cf_procs(root: Path = SAMPLE_DATA, pool_size: int = 4) -> None:
    combined: Counter[str] = Counter()
    with futures.ProcessPoolExecutor(max_workers=pool_size) as workers:
        file_iter = root.glob(LOG_PATTERN)
        for result in workers.map(analysis, file_iter):
            combined.update(result)
    print(combined)


@show_time("benchmark one file")
def benchmark() -> None:
    median_file = SAMPLE_DATA / "itmaybeahack.com.bkup-May-2012.gz"
    analysis(median_file)


def estimates(rate: float | None = None) -> None:
    """If rate is none, benchmark() to get time?"""
    pattern = "*itmaybeahack.com*.gz"
    if rate is None:
        median_path = SAMPLE_DATA / "itmaybeahack.com.bkup-May-2012.gz"
        median_size = median_path.stat().st_size
        median_time = 16.5  # From benchmark()
        rate = median_time / median_size
    t = 0
    for path in SAMPLE_DATA.glob(pattern):
        sz = path.stat().st_size
        print(f"name {path.name:40s} size {sz:10,d} est. time {sz*rate:5.1f}")
        t += sz
    print(f"total {t:,d} est. time {t*rate:.1f}")


if __name__ == "__main__":
    # benchmark()  # 16.5 seconds
    estimates()  # Estimate 86 seconds total
    demo_mp()  # 27 seconds (about 1/4)
    demo_mp_async()  # 27 seconds
    # demo_cf_threads() # time 106, pool size 4
    # demo_cf_procs() # time 40, pool size 4
