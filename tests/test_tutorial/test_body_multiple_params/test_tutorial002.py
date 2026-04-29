from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("body_multiple_params", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def post_all(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={
            "item": {
                "name": "Foo",
                "price": 50.5,
                "description": "Some Foo",
                "tax": 0.1,
            },
            "user": {"username": "johndoe", "full_name": "John Doe"},
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "item_id": 5,
            "item": {
                "name": "Foo",
                "price": 50.5,
                "description": "Some Foo",
                "tax": 0.1,
            },
            "user": {"username": "johndoe", "full_name": "John Doe"},
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def post_required(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={
            "item": {"name": "Foo", "price": 50.5},
            "user": {"username": "johndoe"},
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "item_id": 5,
            "item": {
                "name": "Foo",
                "price": 50.5,
                "description": None,
                "tax": None,
            },
            "user": {"username": "johndoe", "full_name": None},
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def post_no_body(name: str):
    client = _client_for(name)
    response = client.put("/items/5", json=None)
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
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
            ],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def post_no_item(name: str):
    client = _client_for(name)
    response = client.put("/items/5", json={"user": {"username": "johndoe"}})
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "input": None,
                    "loc": ["body", "item"],
                    "msg": "Field required",
                    "type": "missing",
                },
            ],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def post_no_user(name: str):
    client = _client_for(name)
    response = client.put("/items/5", json={"item": {"name": "Foo", "price": 50.5}})
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "input": None,
                    "loc": ["body", "user"],
                    "msg": "Field required",
                    "type": "missing",
                },
            ],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def post_missing_required_field_in_item(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5", json={"item": {"name": "Foo"}, "user": {"username": "johndoe"}}
    )
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "input": {"name": "Foo"},
                    "loc": ["body", "item", "price"],
                    "msg": "Field required",
                    "type": "missing",
                },
            ],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def post_missing_required_field_in_user(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={"item": {"name": "Foo", "price": 50.5}, "user": {"ful_name": "John Doe"}},
    )
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "input": {"ful_name": "John Doe"},
                    "loc": ["body", "user", "username"],
                    "msg": "Field required",
                    "type": "missing",
                },
            ],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def post_id_foo(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/foo",
        json={
            "item": {"name": "Foo", "price": 50.5},
            "user": {"username": "johndoe"},
        },
    )
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foo",
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "info": {
                    "title": "FastAPI",
                    "version": "0.1.0",
                },
                "openapi": "3.1.0",
                "paths": {
                    "/items/{item_id}": {
                        "put": {
                            "operationId": "update_item_items__item_id__put",
                            "parameters": [
                                {
                                    "in": "path",
                                    "name": "item_id",
                                    "required": True,
                                    "schema": {
                                        "title": "Item Id",
                                        "type": "integer",
                                    },
                                },
                            ],
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_update_item_items__item_id__put",
                                        },
                                    },
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {},
                                        },
                                    },
                                    "description": "Successful Response",
                                },
                                "422": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError",
                                            },
                                        },
                                    },
                                    "description": "Validation Error",
                                },
                            },
                            "summary": "Update Item",
                        },
                    },
                },
                "components": {
                    "schemas": {
                        "Body_update_item_items__item_id__put": {
                            "properties": {
                                "item": {
                                    "$ref": "#/components/schemas/Item",
                                },
                                "user": {
                                    "$ref": "#/components/schemas/User",
                                },
                            },
                            "required": [
                                "item",
                                "user",
                            ],
                            "title": "Body_update_item_items__item_id__put",
                            "type": "object",
                        },
                        "HTTPValidationError": {
                            "properties": {
                                "detail": {
                                    "items": {
                                        "$ref": "#/components/schemas/ValidationError",
                                    },
                                    "title": "Detail",
                                    "type": "array",
                                },
                            },
                            "title": "HTTPValidationError",
                            "type": "object",
                        },
                        "Item": {
                            "properties": {
                                "name": {
                                    "title": "Name",
                                    "type": "string",
                                },
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
                            "required": [
                                "name",
                                "price",
                            ],
                            "title": "Item",
                            "type": "object",
                        },
                        "User": {
                            "properties": {
                                "username": {
                                    "title": "Username",
                                    "type": "string",
                                },
                                "full_name": {
                                    "title": "Full Name",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                            },
                            "required": [
                                "username",
                            ],
                            "title": "User",
                            "type": "object",
                        },
                        "ValidationError": {
                            "properties": {
                                "ctx": {"title": "Context", "type": "object"},
                                "input": {"title": "Input"},
                                "loc": {
                                    "items": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "integer"},
                                        ],
                                    },
                                    "title": "Location",
                                    "type": "array",
                                },
                                "msg": {
                                    "title": "Message",
                                    "type": "string",
                                },
                                "type": {
                                    "title": "Error Type",
                                    "type": "string",
                                },
                            },
                            "required": [
                                "loc",
                                "msg",
                                "type",
                            ],
                            "title": "ValidationError",
                            "type": "object",
                        },
                    },
                },
            }
        )
    )
