"""Functional Python Programming 3e

Chapter 1, Example Set 4
"""
import csv
from pathlib import Path
from typing import Any, TYPE_CHECKING

from collections import Counter
import csv
from pathlib import Path

DEFAULT_PATH = Path.cwd() / "address.csv"


def main(source_path: Path = DEFAULT_PATH) -> None:
    frequency: Counter[str] = Counter()
    with source_path.open() as source:
        rdr = csv.DictReader(source)
        for row in rdr:
            if "-" in row["ZIP"]:
                text_zip = row["ZIP"]
                missing_zeroes = 10 - len(text_zip)
                if missing_zeroes:
                    text_zip = missing_zeroes * "0" + text_zip
            else:
                text_zip = row["ZIP"]
                if 5 < len(row["ZIP"]) < 9:
                    missing_zeroes = 9 - len(text_zip)
                else:
                    missing_zeroes = 5 - len(text_zip)
                if missing_zeroes:
                    text_zip = missing_zeroes * "0" + text_zip
            frequency[text_zip] += 1
    print(frequency)


if __name__ == "__main__":
    main()

if TYPE_CHECKING:

    def zip_histogram(reader: csv.DictReader[str]) -> Counter[str]:
        pass


import pytest


@pytest.fixture
def mock_file(tmp_path: Path) -> Path:
    data_path = tmp_path / "data.csv"
    rows: list[dict[str, Any]] = [
        {"ZIP": 3801, "CITY": "Portsmouth", "STATE": "NH"},
        {"ZIP": 12345, "CITY": "Schenectady", "STATE": "NY"},
        {"ZIP": 641, "CITY": "Arecibo", "STATE": "PR"},
        {"ZIP": 38011234, "CITY": "Portsmouth", "STATE": "NH"},
        {"ZIP": "3801-1234", "CITY": "Portsmouth", "STATE": "NH"},
        {"ZIP": "12345-2345", "CITY": "Schenectady", "STATE": "NY"},
        {"ZIP": "641-1234", "CITY": "Arecibo", "STATE": "PR"},
    ]
    with data_path.open("w", newline="") as data_file:
        wtr = csv.DictWriter(data_file, ["ZIP", "CITY", "STATE"])
        wtr.writeheader()
        wtr.writerows(rows)
    return data_path


def test_zip_histogram(mock_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    main(mock_file)
    out, err = capsys.readouterr()
    assert out.splitlines() == [
        "Counter({'03801': 1, '12345': 1, '00641': 1, '038011234': 1, '03801-1234': 1, '12345-2345': 1, '00641-1234': 1})"
    ]
