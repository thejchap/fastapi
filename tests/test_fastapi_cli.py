import os
import subprocess
import sys
from unittest.mock import patch

import fastapi.cli
from tryke import expect, test


@test
def fastapi_cli():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "fastapi",
            "dev",
            "non_existent_file.py",
        ],
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    expect(result.returncode).to_equal(1).fatal()
    expect(result.stdout).to_contain("Path does not exist non_existent_file.py")


@test
def fastapi_cli_not_installed():
    captured: RuntimeError | None = None
    with patch.object(fastapi.cli, "cli_main", None):
        try:
            fastapi.cli.main()
        except RuntimeError as exc:
            captured = exc
    expect(captured).not_.to_be_none().fatal()
    expect(str(captured)).to_contain("To use the fastapi command, please install")
