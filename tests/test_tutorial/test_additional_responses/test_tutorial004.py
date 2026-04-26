import os
import shutil

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("additional_responses", name)
    client = TestClient(mod.app)
    client.headers.clear()
    return client


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
)
def path_operation(name: str):
    client = _client_for(name)
    response = client.get("/items/foo")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"id": "foo", "value": "there goes my hero"})


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
)
def path_operation_img(name: str):
    client = _client_for(name)
    shutil.copy("./docs/en/docs/img/favicon.png", "./image.png")
    response = client.get("/items/foo?img=1")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.headers["Content-Type"]).to_equal("image/png")
    expect(len(response.content)).to_be_truthy()
    os.remove("./image.png")


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/{item_id}": {
                        "get": {
                            "responses": {
                                "404": {"description": "Item not found"},
                                "302": {"description": "The item was moved"},
                                "403": {"description": "Not enough privileges"},
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "image/png": {},
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Item"
                                            }
                                        },
                                    },
                                },
                                "422": {
                                    "description": "Validation Error",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError"
                                            }
                                        }
                                    },
                                },
                            },
                            "summary": "Read Item",
                            "operationId": "read_item_items__item_id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "anyOf": [
                                            {"type": "boolean"},
                                            {"type": "null"},
                                        ],
                                        "title": "Img",
                                    },
                                    "name": "img",
                                    "in": "query",
                                },
                            ],
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "Item": {
                            "title": "Item",
                            "required": ["id", "value"],
                            "type": "object",
                            "properties": {
                                "id": {"title": "Id", "type": "string"},
                                "value": {"title": "Value", "type": "string"},
                            },
                        },
                        "ValidationError": {
                            "title": "ValidationError",
                            "required": ["loc", "msg", "type"],
                            "type": "object",
                            "properties": {
                                "loc": {
                                    "title": "Location",
                                    "type": "array",
                                    "items": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "integer"},
                                        ]
                                    },
                                },
                                "msg": {"title": "Message", "type": "string"},
                                "type": {"title": "Error Type", "type": "string"},
                                "input": {"title": "Input"},
                                "ctx": {"title": "Context", "type": "object"},
                            },
                        },
                        "HTTPValidationError": {
                            "title": "HTTPValidationError",
                            "type": "object",
                            "properties": {
                                "detail": {
                                    "title": "Detail",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    },
                                }
                            },
                        },
                    }
                },
            }
        )
    )
