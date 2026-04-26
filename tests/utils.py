"""Shared helpers used by test modules in this suite.

The pre-migration version of this file exposed `needs_pyXXX` as
`pytest.mark.skipif(...)` markers that callers attached to
`pytest.param(...)` rows. Tryke's `@test.cases` accepts a `skip="reason"`
kwarg per case, so we now expose these as zero-arg helpers that return
`str | None` — the skip reason if the condition is met, otherwise `None`
to mean "do not skip". Callers do `test.case("a", ..., skip=needs_py310())`.
"""

from __future__ import annotations

import importlib.util
import sys

# Re-export the migration shims so legacy import paths
# (`from .utils import needs_py310`) keep working in any module that has
# not yet been ported.
from ._shims import (
    capture_logs,
    capture_output,
    expect_warning,
    import_tutorial,
    monkeypatch_ctx,
    needs_orjson,  # noqa: F401
    tmp_path_ctx,
)


def needs_py310() -> str | None:
    return None if sys.version_info >= (3, 10) else "requires python3.10+"


def needs_py314() -> str | None:
    return None if sys.version_info >= (3, 14) else "requires python3.14+"


def needs_ujson() -> str | None:
    return None if importlib.util.find_spec("ujson") is not None else "requires ujson"


def skip_module_if_py_gte_314() -> str | None:
    """Module-level skip helper. Returns a reason string (truthy) when
    the running interpreter is Python 3.14+, else `None`. Pattern at
    the top of a module:

        from tests.utils import skip_module_if_py_gte_314

        _SKIP = skip_module_if_py_gte_314()
        if not _SKIP:
            @test
            def …
    """
    if sys.version_info >= (3, 14):
        return "requires python3.13-"
    return None


__all__ = [
    "capture_logs",
    "capture_output",
    "expect_warning",
    "import_tutorial",
    "monkeypatch_ctx",
    "needs_orjson",
    "needs_py310",
    "needs_py314",
    "needs_ujson",
    "skip_module_if_py_gte_314",
    "tmp_path_ctx",
]
