#!/usr/bin/env bash

set -e
set -x

export PYTHONPATH=./docs_src

# Main test suite is now run by Tryke. tests/benchmarks/ still uses
# pytest-codspeed and is excluded from Tryke discovery (see [tool.tryke]
# in pyproject.toml). scripts/tests/ also remains on pytest until a
# separate migration pass.
tryke test ${@}
pytest scripts/tests/ ${@}
