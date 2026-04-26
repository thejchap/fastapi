#!/usr/bin/env bash

set -e
set -x

# Tryke does not yet have a `--cov` integration, so we drive coverage
# by wrapping it in `coverage run`. The pytest leg (scripts/tests/)
# still uses pytest-cov directly.
export PYTHONPATH=./docs_src
coverage run --context=tryke -m tryke test
pytest scripts/tests/ --cov --cov-context=test --cov-append ${@}
