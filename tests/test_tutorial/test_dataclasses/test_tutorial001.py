from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("dataclasses_", name)
    client = TestClient(mod.app)
    client.headers.clear()
    return client


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def post_item(name: str):
    client = _client_for(name)
    response = client.post("/items/", json={"name": "Foo", "price": 3})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "name": "Foo",
            "price": 3,
            "description": None,
            "tax": None,
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def post_invalid_item(name: str):
    client = _client_for(name)
    response = client.post("/items/", json={"name": "Foo", "price": "invalid price"})
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "float_parsing",
                    "loc": ["body", "price"],
                    "msg": "Input should be a valid number, unable to parse string as a number",
                    "input": "invalid price",
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/": {
                        "post": {
                            "summary": "Create Item",
                            "operationId": "create_item_items__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
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
                                "price": {"title": "Price", "type": "number"},
                                "description": {
                                    "title": "Description",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
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
