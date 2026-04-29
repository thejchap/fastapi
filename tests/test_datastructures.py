import asyncio
import io
from types import ModuleType
from typing import Any

import trio
from fastapi import FastAPI, UploadFile
from fastapi.datastructures import Default
from fastapi.testclient import TestClient
from tryke import expect, test

from ._shims import expect_warning, tmp_path_ctx


@test("UploadFile._validate rejects non-Starlette inputs")
def upload_file_invalid_pydantic_v2():
    expect(
        lambda: UploadFile._validate("not a Starlette UploadFile", {}),
        "validating a non-Starlette UploadFile",
    ).to_raise(ValueError)
    # `expect_warning` left here as a no-op example; the original test
    # didn't use warnings, just demonstrating the shim API stays
    # importable without affecting behaviour.
    _ = expect_warning


@test("Default placeholders with the same value compare equal")
def default_placeholder_equals():
    placeholder_1 = Default("a")
    placeholder_2 = Default("a")
    expect(placeholder_1, "the placeholder").to_equal(placeholder_2)
    expect(placeholder_1.value, "the placeholder's wrapped value").to_equal(
        placeholder_2.value
    )


@test("Default placeholders are truthy iff the wrapped value is truthy")
def default_placeholder_bool():
    placeholder_a = Default("a")
    placeholder_b = Default("")
    expect(placeholder_a, "Default('a') as bool").to_be_truthy()
    expect(placeholder_b, "Default('') as bool").to_be_falsy()


@test("UploadFile is closed after the request completes")
def upload_file_is_closed():
    with tmp_path_ctx() as tmp_path:
        path = tmp_path / "test.txt"
        path.write_bytes(b"<file content>")
        app = FastAPI()

        testing_file_store: list[UploadFile] = []

        @app.post("/uploadfile/")
        def create_upload_file(file: UploadFile):
            testing_file_store.append(file)
            return {"filename": file.filename}

        client = TestClient(app)
        with path.open("rb") as file:
            response = client.post("/uploadfile/", files={"file": file})
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json(), "response body").to_equal({"filename": "test.txt"})

        expect(testing_file_store, "captured upload files").to_be_truthy().fatal()
        expect(
            testing_file_store[0].file.closed,
            "underlying file is closed",
        ).to_be_truthy()


# Async test ported from `@pytest.mark.anyio async def test_upload_file`.
# pytest-anyio cross-products this over the [asyncio, trio] backends; the
# tryke port does the same via @test.cases passing the runner module.
def _run(runner: ModuleType, fn: Any) -> None:
    # asyncio.run takes a coroutine, trio.run takes the callable itself.
    if runner is asyncio:
        runner.run(fn())
    else:
        runner.run(fn)


@test.cases(
    test.case("asyncio", runner=asyncio),
    test.case("trio", runner=trio),
)
def upload_file(runner: ModuleType) -> None:
    async def _body() -> None:
        stream = io.BytesIO(b"data")
        file = UploadFile(filename="file", file=stream, size=4)
        expect(await file.read(), "initial read content").to_equal(b"data")
        expect(file.size, "initial size").to_equal(4)
        await file.write(b" and more data!")
        expect(await file.read(), "read after writing past end").to_equal(b"")
        expect(file.size, "size after writing").to_equal(19)
        await file.seek(0)
        expect(await file.read(), "read after seek to start").to_equal(
            b"data and more data!"
        )
        await file.close()

    _run(runner, _body)
