"""Functional Python Programming 3e

Chapter 15, Test Configuration
"""
from collections.abc import Iterator
from pathlib import Path
import subprocess
import time

import pytest

def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers", "server_file(file): mark test to use a specific file"
    )

@pytest.fixture
def running_server(request: pytest.FixtureRequest) -> Iterator[Path]:
    """
    Runs the named module as a WSGI server.
    Ideally, this is scope="module"
    """
    server_file = request.node.get_closest_marker("server_file").args[0]

    log_path = Path.cwd() / "server.log"
    with log_path.open("w") as log_file:
        log_file.write(f"Starting server {server_file!r}...\n")
        with subprocess.Popen(
            ["python", server_file],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True
        ) as server:
            time.sleep(1)  # Allow child to start
            log_file.write(f"Startup Failure? {server.poll()=}\n")
            log_file.flush()

            yield log_path  # Wait while tests run

            log_file.write(f"Killing {server.pid=}\n")
            server.kill()
            time.sleep(0.5)  # Allow child to finish
            log_file.write(f"Final {server.poll()=}\n")
            log_file.flush()
