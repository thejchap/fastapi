from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("body_multiple_params", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def put_all(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={
            "importance": 2,
            "item": {"name": "Foo", "price": 50.5},
            "user": {"username": "Dave"},
        },
        params={"q": "somequery"},
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "item_id": 5,
            "importance": 2,
            "item": {
                "name": "Foo",
                "price": 50.5,
                "description": None,
                "tax": None,
            },
            "user": {"username": "Dave", "full_name": None},
            "q": "somequery",
        }
    )


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def put_only_required(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={
            "importance": 2,
            "item": {"name": "Foo", "price": 50.5},
            "user": {"username": "Dave"},
        },
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "item_id": 5,
            "importance": 2,
            "item": {
                "name": "Foo",
                "price": 50.5,
                "description": None,
                "tax": None,
            },
            "user": {"username": "Dave", "full_name": None},
        }
    )


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def put_missing_body(name: str):
    client = _client_for(name)
    response = client.put("/items/5")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "input": None,
                    "loc": ["body", "item"],
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "input": None,
                    "loc": ["body", "user"],
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "input": None,
                    "loc": ["body", "importance"],
                    "msg": "Field required",
                    "type": "missing",
                },
            ],
        }
    )


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def put_empty_body(name: str):
    client = _client_for(name)
    response = client.put("/items/5", json={})
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "item"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["body", "user"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["body", "importance"],
                    "msg": "Field required",
                    "input": None,
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def put_invalid_importance(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={
            "importance": 0,
            "item": {"name": "Foo", "price": 50.5},
            "user": {"username": "Dave"},
        },
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "loc": ["body", "importance"],
                    "msg": "Input should be greater than 0",
                    "type": "greater_than",
                    "input": 0,
                    "ctx": {"gt": 0},
                },
            ],
        }
    )


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
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
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Q",
                                    },
                                    "name": "q",
                                    "in": "query",
                                },
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
                        "User": {
                            "title": "User",
                            "required": ["username"],
                            "type": "object",
                            "properties": {
                                "username": {"title": "Username", "type": "string"},
                                "full_name": {
                                    "title": "Full Name",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                            },
                        },
                        "Body_update_item_items__item_id__put": {
                            "title": "Body_update_item_items__item_id__put",
                            "required": ["item", "user", "importance"],
                            "type": "object",
                            "properties": {
                                "item": {"$ref": "#/components/schemas/Item"},
                                "user": {"$ref": "#/components/schemas/User"},
                                "importance": {
                                    "title": "Importance",
                                    "type": "integer",
                                    "exclusiveMinimum": 0.0,
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
