"""Compatibility shims used by the tryke port of the pytest test suite.

These exist because pytest provides several builtin fixtures and helpers
(`tmp_path`, `monkeypatch`, `capsys`, `caplog`, `pytest.warns`) that have
no direct Tryke equivalent yet. Each shim is intentionally small and only
covers the surface area the FastAPI suite actually exercises.

Everything here is exposed as a **context manager**, not a `@fixture`.
Module-level `@fixture` declarations in tryke run for every test in the
enclosing scope regardless of whether the test depends on them, so
defining them here as fixtures would tax every test in a file even when
unused. Context managers keep the cost per-test pay-as-you-go and make
the conversion mechanical:

    pytest:                                 tryke:
    def test_x(monkeypatch):                @test
        monkeypatch.setenv(...)             def x():
                                                with monkeypatch_ctx() as mp:
                                                    mp.setenv(...)
"""

from __future__ import annotations

import contextlib
import importlib
import importlib.util
import io
import logging
import os
import re
import shutil
import sys
import tempfile
import warnings
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any


# `filterwarnings = ["error"]` from the pytest config: any warning escaping
# a test becomes an error. Tryke has no equivalent today, so we install the
# filter at import time. Tests that legitimately emit a warning use
# `expect_warning(...)` to silence it locally.
def install_warning_filter() -> None:
    warnings.simplefilter("error")


install_warning_filter()


_UNSET: Any = object()


@dataclass
class MonkeyPatch:
    """Subset of pytest's `MonkeyPatch` covering the surface area the
    FastAPI test suite uses (`setenv`, `delenv`, `setattr`, `delattr`,
    `syspath_prepend`, `chdir`)."""

    _undo_env: list[tuple[str, str | None]] = field(default_factory=list)
    _undo_attr: list[tuple[Any, str, Any, bool]] = field(default_factory=list)
    _undo_syspath: list[int] = field(default_factory=list)
    _undo_chdir: str | None = None

    def setenv(self, name: str, value: str, prepend: str | None = None) -> None:
        previous = os.environ.get(name)
        self._undo_env.append((name, previous))
        os.environ[name] = (
            f"{value}{prepend}{previous}" if prepend and previous is not None else value
        )

    def delenv(self, name: str, raising: bool = True) -> None:
        if name not in os.environ:
            if raising:
                raise KeyError(name)
            self._undo_env.append((name, None))
            return
        self._undo_env.append((name, os.environ[name]))
        del os.environ[name]

    def setattr(
        self, target: Any, name: str, value: Any = _UNSET, raising: bool = True
    ) -> None:
        if isinstance(target, str) and value is _UNSET:
            module_path, _, attr_name = target.rpartition(".")
            module = importlib.import_module(module_path)
            target, name, value = module, attr_name, name
        had_attr = hasattr(target, name)
        if raising and not had_attr:
            raise AttributeError(name)
        previous = getattr(target, name, None)
        self._undo_attr.append((target, name, previous, had_attr))
        setattr(target, name, value)

    def delattr(self, target: Any, name: str, raising: bool = True) -> None:
        had_attr = hasattr(target, name)
        if raising and not had_attr:
            raise AttributeError(name)
        previous = getattr(target, name, None)
        self._undo_attr.append((target, name, previous, had_attr))
        delattr(target, name)

    def syspath_prepend(self, path: str | Path) -> None:
        self._undo_syspath.append(0)
        sys.path.insert(0, str(path))

    def chdir(self, path: str | Path) -> None:
        if self._undo_chdir is None:
            self._undo_chdir = os.getcwd()
        os.chdir(path)

    def undo(self) -> None:
        for name, previous in reversed(self._undo_env):
            if previous is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = previous
        self._undo_env.clear()
        for target, name, previous, had_attr in reversed(self._undo_attr):
            if had_attr:
                setattr(target, name, previous)
            else:
                with contextlib.suppress(AttributeError):
                    delattr(target, name)
        self._undo_attr.clear()
        for index in self._undo_syspath:
            with contextlib.suppress(IndexError):
                sys.path.pop(index)
        self._undo_syspath.clear()
        if self._undo_chdir is not None:
            os.chdir(self._undo_chdir)
            self._undo_chdir = None


@contextmanager
def monkeypatch_ctx() -> Iterator[MonkeyPatch]:
    mp = MonkeyPatch()
    try:
        yield mp
    finally:
        mp.undo()


@contextmanager
def tmp_path_ctx() -> Iterator[Path]:
    """Context-manager replacement for pytest's `tmp_path` fixture."""
    path = Path(tempfile.mkdtemp(prefix="tryke-"))
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


@dataclass
class CapturedOutput:
    out: str = ""
    err: str = ""

    def readouterr(self) -> CapturedOutput:
        # Mirrors capsys.readouterr() — the FastAPI suite calls this.
        snapshot = CapturedOutput(out=self.out, err=self.err)
        self.out = ""
        self.err = ""
        return snapshot


@contextmanager
def capture_output() -> Iterator[CapturedOutput]:
    """Replacement for pytest's `capsys`. Captures Python-level
    stdout/stderr; subprocess output is not captured."""
    buf_out, buf_err = io.StringIO(), io.StringIO()
    captured = CapturedOutput()
    try:
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            yield captured
    finally:
        captured.out = buf_out.getvalue()
        captured.err = buf_err.getvalue()


@dataclass
class CapturedLogRecord:
    name: str
    levelno: int
    levelname: str
    message: str
    raw: logging.LogRecord


@dataclass
class LogCapture:
    records: list[CapturedLogRecord] = field(default_factory=list)

    @property
    def messages(self) -> list[str]:
        return [r.message for r in self.records]

    @property
    def text(self) -> str:
        return "\n".join(self.messages)


@contextmanager
def capture_logs(
    logger: str | logging.Logger | None = None, level: int = logging.NOTSET
) -> Iterator[LogCapture]:
    """Replacement for pytest's `caplog`. Attaches a list-collecting
    handler to the named logger (or the root logger) for the duration of
    the block."""
    target = logger if isinstance(logger, logging.Logger) else logging.getLogger(logger)
    capture = LogCapture()

    class _Handler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            capture.records.append(
                CapturedLogRecord(
                    name=record.name,
                    levelno=record.levelno,
                    levelname=record.levelname,
                    message=record.getMessage(),
                    raw=record,
                )
            )

    handler = _Handler(level=level)
    previous_level = target.level
    target.addHandler(handler)
    if level != logging.NOTSET:
        target.setLevel(level)
    try:
        yield capture
    finally:
        target.removeHandler(handler)
        target.setLevel(previous_level)


@contextmanager
def expect_warning(
    category: type[Warning] = Warning, match: str | None = None
) -> Iterator[list[warnings.WarningMessage]]:
    """Replacement for `pytest.warns(...)`. Runs the body with the
    `error` warning filter relaxed and asserts at least one matching
    warning was emitted."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        yield caught
    matched = [
        w
        for w in caught
        if issubclass(w.category, category)
        and (match is None or re.search(match, str(w.message)))
    ]
    if not matched:
        seen = (
            ", ".join(f"{w.category.__name__}: {w.message}" for w in caught)
            or "no warnings"
        )
        message = (
            f"expected at least one {category.__name__}"
            + (f" matching /{match}/" if match else "")
            + f"; got {seen}"
        )
        raise AssertionError(message)


def needs_py310() -> str | None:
    """Skip-reason helper kept for parity with the original
    `needs_py310` mark; with `requires-python = ">=3.13"` it is always
    `None`. Use as `skip=needs_py310()` on a `test.case(...)`."""
    return None if sys.version_info >= (3, 10) else "requires Python 3.10+"


def needs_pydanticv2() -> str | None:
    return None  # FastAPI is now Pydantic v2 only.


_HAS_ORJSON = importlib.util.find_spec("orjson") is not None


def needs_orjson() -> str | None:
    return None if _HAS_ORJSON else "requires orjson"


def import_tutorial(package: str, name: str, *, base: str = "docs_src") -> ModuleType:
    """Convenience wrapper for the `test_tutorial/` files that
    historically used `importlib.import_module(f"{base}.{package}.{name}")`
    inside a fixture parametrized over many `tutorialNNN_*` variants.
    Listing those statically would mean a literal copy of the docs_src
    tree, so we accept tryke's `--changed` re-run cost (one warning per
    file) and centralise the dynamic import here."""
    return importlib.import_module(f"{base}.{package}.{name}")


__all__ = [
    "CapturedLogRecord",
    "CapturedOutput",
    "LogCapture",
    "MonkeyPatch",
    "capture_logs",
    "capture_output",
    "expect_warning",
    "import_tutorial",
    "install_warning_filter",
    "monkeypatch_ctx",
    "needs_orjson",
    "needs_py310",
    "needs_pydanticv2",
    "tmp_path_ctx",
]
