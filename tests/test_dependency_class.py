from collections.abc import AsyncGenerator, Generator

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


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


@app.get("/callable-dependency-class")
async def get_callable_dependency_class(
    value: str, instance: CallableDependency = Depends()
):
    return instance(value)


@app.get("/callable-gen-dependency-class")
async def get_callable_gen_dependency_class(
    value: str, instance: CallableGenDependency = Depends()
):
    return next(instance(value))


@app.get("/async-callable-dependency-class")
async def get_async_callable_dependency_class(
    value: str, instance: AsyncCallableDependency = Depends()
):
    return await instance(value)


@app.get("/async-callable-gen-dependency-class")
async def get_async_callable_gen_dependency_class(
    value: str, instance: AsyncCallableGenDependency = Depends()
):
    return await instance(value).__anext__()


@app.get("/callable-dependency")
async def get_callable_dependency(value: str = Depends(callable_dependency)):
    return value


@app.get("/callable-gen-dependency")
async def get_callable_gen_dependency(value: str = Depends(callable_gen_dependency)):
    return value


@app.get("/async-callable-dependency")
async def get_async_callable_dependency(
    value: str = Depends(async_callable_dependency),
):
    return value


@app.get("/async-callable-gen-dependency")
async def get_async_callable_gen_dependency(
    value: str = Depends(async_callable_gen_dependency),
):
    return value


@app.get("/synchronous-method-dependency")
async def get_synchronous_method_dependency(
    value: str = Depends(methods_dependency.synchronous),
):
    return value


@app.get("/synchronous-method-gen-dependency")
async def get_synchronous_method_gen_dependency(
    value: str = Depends(methods_dependency.synchronous_gen),
):
    return value


@app.get("/asynchronous-method-dependency")
async def get_asynchronous_method_dependency(
    value: str = Depends(methods_dependency.asynchronous),
):
    return value


@app.get("/asynchronous-method-gen-dependency")
async def get_asynchronous_method_gen_dependency(
    value: str = Depends(methods_dependency.asynchronous_gen),
):
    return value


client = TestClient(app)


@test.cases(
    test.case(
        "callable-dependency", route="/callable-dependency", value="callable-dependency"
    ),
    test.case(
        "callable-gen-dependency",
        route="/callable-gen-dependency",
        value="callable-gen-dependency",
    ),
    test.case(
        "async-callable-dependency",
        route="/async-callable-dependency",
        value="async-callable-dependency",
    ),
    test.case(
        "async-callable-gen-dependency",
        route="/async-callable-gen-dependency",
        value="async-callable-gen-dependency",
    ),
    test.case(
        "synchronous-method-dependency",
        route="/synchronous-method-dependency",
        value="synchronous-method-dependency",
    ),
    test.case(
        "synchronous-method-gen-dependency",
        route="/synchronous-method-gen-dependency",
        value="synchronous-method-gen-dependency",
    ),
    test.case(
        "asynchronous-method-dependency",
        route="/asynchronous-method-dependency",
        value="asynchronous-method-dependency",
    ),
    test.case(
        "asynchronous-method-gen-dependency",
        route="/asynchronous-method-gen-dependency",
        value="asynchronous-method-gen-dependency",
    ),
    test.case(
        "callable-dependency-class",
        route="/callable-dependency-class",
        value="callable-dependency-class",
    ),
    test.case(
        "callable-gen-dependency-class",
        route="/callable-gen-dependency-class",
        value="callable-gen-dependency-class",
    ),
    test.case(
        "async-callable-dependency-class",
        route="/async-callable-dependency-class",
        value="async-callable-dependency-class",
    ),
    test.case(
        "async-callable-gen-dependency-class",
        route="/async-callable-gen-dependency-class",
        value="async-callable-gen-dependency-class",
    ),
)
def class_dependency(route: str, value: str):
    response = client.get(route, params={"value": value})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(value)
