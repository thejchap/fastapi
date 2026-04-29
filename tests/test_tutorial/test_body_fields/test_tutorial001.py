from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("body_fields", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def items_5(name: str):
    client = _client_for(name)
    response = client.put("/items/5", json={"item": {"name": "Foo", "price": 3.0}})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "item_id": 5,
            "item": {"name": "Foo", "price": 3.0, "description": None, "tax": None},
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def items_6(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/6",
        json={
            "item": {
                "name": "Bar",
                "price": 0.2,
                "description": "Some bar",
                "tax": "5.4",
            }
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "item_id": 6,
            "item": {
                "name": "Bar",
                "price": 0.2,
                "description": "Some bar",
                "tax": 5.4,
            },
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def invalid_price(name: str):
    client = _client_for(name)
    response = client.put("/items/5", json={"item": {"name": "Foo", "price": -3.0}})
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["body", "item", "price"],
                    "msg": "Input should be greater than 0",
                    "input": -3.0,
                    "ctx": {"gt": 0.0},
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/{item_id}": {
                        "put": {
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
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_update_item_items__item_id__put"
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "Item": {
                            "title": "Item",
                            "required": ["name", "price"],
                            "type": "object",
                            "properties": {
                                "name": {"title": "Name", "type": "string"},
                                "description": {
                                    "title": "The description of the item",
                                    "anyOf": [
                                        {"maxLength": 300, "type": "string"},
                                        {"type": "null"},
                                    ],
                                },
                                "price": {
                                    "title": "Price",
                                    "exclusiveMinimum": 0.0,
                                    "type": "number",
                                    "description": "The price must be greater than zero",
                                },
                                "tax": {
                                    "title": "Tax",
                                    "anyOf": [{"type": "number"}, {"type": "null"}],
                                },
                            },
                        },
                        "Body_update_item_items__item_id__put": {
                            "title": "Body_update_item_items__item_id__put",
                            "required": ["item"],
                            "type": "object",
                            "properties": {
                                "item": {"$ref": "#/components/schemas/Item"}
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
