import importlib
import runpy
import sys
import unittest

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

MOD_NAME = "docs_src.debugging.tutorial001_py310"


@fixture
def client() -> TestClient:
    mod = importlib.import_module(MOD_NAME)
    return TestClient(mod.app)


@test("uvicorn.run is not called when the module is imported")
def uvicorn_run_is_not_called_on_import():
    if sys.modules.get(MOD_NAME):
        del sys.modules[MOD_NAME]
    with unittest.mock.patch("uvicorn.run") as uvicorn_run_mock:
        importlib.import_module(MOD_NAME)
    uvicorn_run_mock.assert_not_called()


@test("GET / returns the hello-world payload")
def get_root(client: TestClient = Depends(client)):
    response = client.get("/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"hello world": "ba"})


@test("uvicorn.run is called when the module runs as __main__")
def uvicorn_run_called_when_run_as_main():
    # Just for coverage.
    if sys.modules.get(MOD_NAME):
        del sys.modules[MOD_NAME]
    with unittest.mock.patch("uvicorn.run") as uvicorn_run_mock:
        runpy.run_module(MOD_NAME, run_name="__main__")

    uvicorn_run_mock.assert_called_once_with(
        unittest.mock.ANY, host="0.0.0.0", port=8000
    )


@test("OpenAPI schema matches snapshot")
def openapi_schema(client: TestClient = Depends(client)):
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/": {
                        "get": {
                            "summary": "Root",
                            "operationId": "root__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                            },
                        }
                    }
                },
            }
        )
    )
