from collections.abc import AsyncGenerator, Generator
from functools import partial
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


def function_dependency(value: str) -> str:
    return value


async def async_function_dependency(value: str) -> str:
    return value


def gen_dependency(value: str) -> Generator[str]:
    yield value


async def async_gen_dependency(value: str) -> AsyncGenerator[str]:
    yield value


class CallableDependency:
    def __call__(self, value: str) -> str:
        return value


class CallableGenDependency:
    def __call__(self, value: str) -> Generator[str]:
        yield value


class AsyncCallableDependency:
    async def __call__(self, value: str) -> str:
        return value


class AsyncCallableGenDependency:
    async def __call__(self, value: str) -> AsyncGenerator[str]:
        yield value


class MethodsDependency:
    def synchronous(self, value: str) -> str:
        return value

    async def asynchronous(self, value: str) -> str:
        return value

    def synchronous_gen(self, value: str) -> Generator[str]:
        yield value

    async def asynchronous_gen(self, value: str) -> AsyncGenerator[str]:
        yield value


callable_dependency = CallableDependency()
callable_gen_dependency = CallableGenDependency()
async_callable_dependency = AsyncCallableDependency()
async_callable_gen_dependency = AsyncCallableGenDependency()
methods_dependency = MethodsDependency()


@app.get("/partial-function-dependency")
async def get_partial_function_dependency(
    value: Annotated[
        str, Depends(partial(function_dependency, "partial-function-dependency"))
    ],
) -> str:
    return value


@app.get("/partial-async-function-dependency")
async def get_partial_async_function_dependency(
    value: Annotated[
        str,
        Depends(
            partial(async_function_dependency, "partial-async-function-dependency")
        ),
    ],
) -> str:
    return value


@app.get("/partial-gen-dependency")
async def get_partial_gen_dependency(
    value: Annotated[str, Depends(partial(gen_dependency, "partial-gen-dependency"))],
) -> str:
    return value


@app.get("/partial-async-gen-dependency")
async def get_partial_async_gen_dependency(
    value: Annotated[
        str, Depends(partial(async_gen_dependency, "partial-async-gen-dependency"))
    ],
) -> str:
    return value


@app.get("/partial-callable-dependency")
async def get_partial_callable_dependency(
    value: Annotated[
        str, Depends(partial(callable_dependency, "partial-callable-dependency"))
    ],
) -> str:
    return value


@app.get("/partial-callable-gen-dependency")
async def get_partial_callable_gen_dependency(
    value: Annotated[
        str,
        Depends(partial(callable_gen_dependency, "partial-callable-gen-dependency")),
    ],
) -> str:
    return value


@app.get("/partial-async-callable-dependency")
async def get_partial_async_callable_dependency(
    value: Annotated[
        str,
        Depends(
            partial(async_callable_dependency, "partial-async-callable-dependency")
        ),
    ],
) -> str:
    return value


@app.get("/partial-async-callable-gen-dependency")
async def get_partial_async_callable_gen_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                async_callable_gen_dependency, "partial-async-callable-gen-dependency"
            )
        ),
    ],
) -> str:
    return value


@app.get("/partial-synchronous-method-dependency")
async def get_partial_synchronous_method_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                methods_dependency.synchronous, "partial-synchronous-method-dependency"
            )
        ),
    ],
) -> str:
    return value


@app.get("/partial-synchronous-method-gen-dependency")
async def get_partial_synchronous_method_gen_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                methods_dependency.synchronous_gen,
                "partial-synchronous-method-gen-dependency",
            )
        ),
    ],
) -> str:
    return value


@app.get("/partial-asynchronous-method-dependency")
async def get_partial_asynchronous_method_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                methods_dependency.asynchronous,
                "partial-asynchronous-method-dependency",
            )
        ),
    ],
) -> str:
    return value


@app.get("/partial-asynchronous-method-gen-dependency")
async def get_partial_asynchronous_method_gen_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                methods_dependency.asynchronous_gen,
                "partial-asynchronous-method-gen-dependency",
            )
        ),
    ],
) -> str:
    return value


client = TestClient(app)


@test.cases(
    test.case(
        "partial-function-dependency",
        route="/partial-function-dependency",
        value="partial-function-dependency",
    ),
    test.case(
        "partial-async-function-dependency",
        route="/partial-async-function-dependency",
        value="partial-async-function-dependency",
    ),
    test.case(
        "partial-gen-dependency",
        route="/partial-gen-dependency",
        value="partial-gen-dependency",
    ),
    test.case(
        "partial-async-gen-dependency",
        route="/partial-async-gen-dependency",
        value="partial-async-gen-dependency",
    ),
    test.case(
        "partial-callable-dependency",
        route="/partial-callable-dependency",
        value="partial-callable-dependency",
    ),
    test.case(
        "partial-callable-gen-dependency",
        route="/partial-callable-gen-dependency",
        value="partial-callable-gen-dependency",
    ),
    test.case(
        "partial-async-callable-dependency",
        route="/partial-async-callable-dependency",
        value="partial-async-callable-dependency",
    ),
    test.case(
        "partial-async-callable-gen-dependency",
        route="/partial-async-callable-gen-dependency",
        value="partial-async-callable-gen-dependency",
    ),
    test.case(
        "partial-synchronous-method-dependency",
        route="/partial-synchronous-method-dependency",
        value="partial-synchronous-method-dependency",
    ),
    test.case(
        "partial-synchronous-method-gen-dependency",
        route="/partial-synchronous-method-gen-dependency",
        value="partial-synchronous-method-gen-dependency",
    ),
    test.case(
        "partial-asynchronous-method-dependency",
        route="/partial-asynchronous-method-dependency",
        value="partial-asynchronous-method-dependency",
    ),
    test.case(
        "partial-asynchronous-method-gen-dependency",
        route="/partial-asynchronous-method-gen-dependency",
        value="partial-asynchronous-method-gen-dependency",
    ),
)
def dependency_types_with_partial(route: str, value: str) -> None:
    response = client.get(route)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(value)
