from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("schema_extra_example", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
    test.case("tutorial005_an_py310", name="tutorial005_an_py310"),
)
def post_body_example(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    )
    expect(response.status_code).to_equal(200)


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
    test.case("tutorial005_an_py310", name="tutorial005_an_py310"),
)
def openapi_schema(name: str) -> None:
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
                        "put": {
                            "summary": "Update Item",
                            "operationId": "update_item_items__item_id__put",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "integer"},
                                    "name": "item_id",
                                    "in": "path",
                                }
                            ],
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"},
                                        "examples": {
                                            "normal": {
                                                "summary": "A normal example",
                                                "description": "A **normal** item works correctly.",
                                                "value": {
                                                    "name": "Foo",
                                                    "description": "A very nice Item",
                                                    "price": 35.4,
                                                    "tax": 3.2,
                                                },
                                            },
                                            "converted": {
                                                "summary": "An example with converted data",
                                                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                                                "value": {
                                                    "name": "Bar",
                                                    "price": "35.4",
                                                },
                                            },
                                            "invalid": {
                                                "summary": "Invalid data is rejected with an error",
                                                "value": {
                                                    "name": "Baz",
                                                    "price": "thirty five point four",
                                                },
                                            },
                                        },
                                    }
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
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
                        }
                    }
                },
                "components": {
                    "schemas": {
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
                        "Item": {
                            "title": "Item",
                            "required": ["name", "price"],
                            "type": "object",
                            "properties": {
                                "name": {"title": "Name", "type": "string"},
                                "description": {
                                    "title": "Description",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                                "price": {"title": "Price", "type": "number"},
                                "tax": {
                                    "title": "Tax",
                                    "anyOf": [{"type": "number"}, {"type": "null"}],
                                },
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
                    }
                },
            }
        )
    )
