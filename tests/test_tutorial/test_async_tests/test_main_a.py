import asyncio
from types import ModuleType
from typing import Any

import trio
from tryke import test

from docs_src.async_tests.app_a_py310.test_main import test_root


def _run(runner: ModuleType, fn: Any) -> None:
    # asyncio.run takes a coroutine; trio.run takes the callable itself.
    if runner is asyncio:
        runner.run(fn())
    else:
        runner.run(fn)


@test.cases(
    test.case("asyncio", runner=asyncio),
    test.case("trio", runner=trio),
)
def async_testing(runner: ModuleType) -> None:
    async def _body() -> None:
        await test_root()

    _run(runner, _body)


# Pytest discovered `test_root` here because it was imported at module scope.
# Mirror that by explicitly invoking it under both backends.
@test.cases(
    test.case("asyncio", runner=asyncio),
    test.case("trio", runner=trio),
)
def root(runner: ModuleType) -> None:
    async def _body() -> None:
        await test_root()

    _run(runner, _body)
