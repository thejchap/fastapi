from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from ..._shims import expect_warning

with expect_warning(DeprecationWarning):
    from docs_src.events.tutorial002_py310 import app as _app


@fixture(per="scope")
def app() -> FastAPI:
    return _app


@test
def events(app: FastAPI = Depends(app)):
    with TestClient(app) as client:
        response = client.get("/items/")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal([{"name": "Foo"}])
    with open("log.txt") as log:
        expect(log.read()).to_contain("Application shutdown")


@test
def openapi_schema(app: FastAPI = Depends(app)):
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal(
            snapshot(
                {
                    "openapi": "3.1.0",
                    "info": {"title": "FastAPI", "version": "0.1.0"},
                    "paths": {
                        "/items/": {
                            "get": {
                                "responses": {
                                    "200": {
                                        "description": "Successful Response",
                                        "content": {"application/json": {"schema": {}}},
                                    }
                                },
                                "summary": "Read Items",
                                "operationId": "read_items_items__get",
                            }
                        }
                    },
                }
            )
        )
