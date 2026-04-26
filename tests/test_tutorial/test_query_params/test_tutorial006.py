from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("query_params", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
)
def foo_needy_very(name: str):
    client = _client_for(name)
    response = client.get("/items/foo?needy=very")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal(
        {
            "item_id": "foo",
            "needy": "very",
            "skip": 0,
            "limit": None,
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
)
def foo_no_needy(name: str):
    client = _client_for(name)
    response = client.get("/items/foo?skip=a&limit=b")
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "needy"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "int_parsing",
                    "loc": ["query", "skip"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "a",
                },
                {
                    "type": "int_parsing",
                    "loc": ["query", "limit"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "b",
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/{item_id}": {
                        "get": {
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
                            "summary": "Read User Item",
                            "operationId": "read_user_item_items__item_id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "Needy", "type": "string"},
                                    "name": "needy",
                                    "in": "query",
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "Skip",
                                        "type": "integer",
                                        "default": 0,
                                    },
                                    "name": "skip",
                                    "in": "query",
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "anyOf": [
                                            {"type": "integer"},
                                            {"type": "null"},
                                        ],
                                        "title": "Limit",
                                    },
                                    "name": "limit",
                                    "in": "query",
                                },
                            ],
                        }
                    }
                },
                "components": {
                    "schemas": {
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
