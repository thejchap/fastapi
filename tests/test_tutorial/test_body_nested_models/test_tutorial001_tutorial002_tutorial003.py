from dirty_equals import IsList
from fastapi.testclient import TestClient
from inline_snapshot import Is, snapshot
from tryke import expect, test

from ..._shims import import_tutorial

UNTYPED_LIST_SCHEMA = {"type": "array", "items": {}}

LIST_OF_STR_SCHEMA = {"type": "array", "items": {"type": "string"}}

SET_OF_STR_SCHEMA = {"type": "array", "items": {"type": "string"}, "uniqueItems": True}


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("body_nested_models", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_py310", mod_name="tutorial001_py310"),
    test.case("tutorial002_py310", mod_name="tutorial002_py310"),
    test.case("tutorial003_py310", mod_name="tutorial003_py310"),
)
def put_all(mod_name: str):
    client = _client_for(mod_name)
    if mod_name.startswith("tutorial003"):
        tags_expected = IsList("foo", "bar", check_order=False)
    else:
        tags_expected = ["foo", "bar", "foo"]

    response = client.put(
        "/items/123",
        json={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
            "tags": ["foo", "bar", "foo"],
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "item_id": 123,
            "item": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
                "tags": tags_expected,
            },
        }
    )


@test.cases(
    test.case("tutorial001_py310", mod_name="tutorial001_py310"),
    test.case("tutorial002_py310", mod_name="tutorial002_py310"),
    test.case("tutorial003_py310", mod_name="tutorial003_py310"),
)
def put_only_required(mod_name: str):
    client = _client_for(mod_name)
    response = client.put(
        "/items/5",
        json={"name": "Foo", "price": 35.4},
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "item_id": 5,
            "item": {
                "name": "Foo",
                "description": None,
                "price": 35.4,
                "tax": None,
                "tags": [],
            },
        }
    )


@test.cases(
    test.case("tutorial001_py310", mod_name="tutorial001_py310"),
    test.case("tutorial002_py310", mod_name="tutorial002_py310"),
    test.case("tutorial003_py310", mod_name="tutorial003_py310"),
)
def put_empty_body(mod_name: str):
    client = _client_for(mod_name)
    response = client.put(
        "/items/5",
        json={},
    )
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "loc": ["body", "name"],
                    "input": {},
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "loc": ["body", "price"],
                    "input": {},
                    "msg": "Field required",
                    "type": "missing",
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial001_py310", mod_name="tutorial001_py310"),
    test.case("tutorial002_py310", mod_name="tutorial002_py310"),
    test.case("tutorial003_py310", mod_name="tutorial003_py310"),
)
def put_missing_required(mod_name: str):
    client = _client_for(mod_name)
    response = client.put(
        "/items/5",
        json={"description": "A very nice Item"},
    )
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "loc": ["body", "name"],
                    "input": {"description": "A very nice Item"},
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "loc": ["body", "price"],
                    "input": {"description": "A very nice Item"},
                    "msg": "Field required",
                    "type": "missing",
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial001_py310", mod_name="tutorial001_py310"),
    test.case("tutorial002_py310", mod_name="tutorial002_py310"),
    test.case("tutorial003_py310", mod_name="tutorial003_py310"),
)
def openapi_schema(mod_name: str):
    client = _client_for(mod_name)
    tags_schema = {"default": [], "title": "Tags"}
    if mod_name.startswith("tutorial001"):
        tags_schema.update(UNTYPED_LIST_SCHEMA)
    elif mod_name.startswith("tutorial002"):
        tags_schema.update(LIST_OF_STR_SCHEMA)
    elif mod_name.startswith("tutorial003"):
        tags_schema.update(SET_OF_STR_SCHEMA)

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
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Item",
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
                            "properties": {
                                "name": {
                                    "title": "Name",
                                    "type": "string",
                                },
                                "description": {
                                    "title": "Description",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                                "price": {
                                    "title": "Price",
                                    "type": "number",
                                },
                                "tax": {
                                    "title": "Tax",
                                    "anyOf": [{"type": "number"}, {"type": "null"}],
                                },
                                "tags": Is(tags_schema),
                            },
                            "required": [
                                "name",
                                "price",
                            ],
                            "title": "Item",
                            "type": "object",
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
