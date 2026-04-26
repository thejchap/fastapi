import warnings

from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import needs_orjson

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FastAPIDeprecationWarning)
    from docs_src.custom_response.tutorial001b_py310 import app

client = TestClient(app)

_SKIP_ORJSON = needs_orjson()


if not _SKIP_ORJSON:

    @test
    def get_custom_response():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FastAPIDeprecationWarning)
            response = client.get("/items/")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal([{"item_id": "Foo"}])

    @test
    def openapi_schema():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FastAPIDeprecationWarning)
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
