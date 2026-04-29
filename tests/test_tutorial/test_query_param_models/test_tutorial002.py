from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("query_param_models", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def query_param_model(name: str):
    client = _client_for(name)
    response = client.get(
        "/items/",
        params={
            "limit": 10,
            "offset": 5,
            "order_by": "updated_at",
            "tags": ["tag1", "tag2"],
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "limit": 10,
            "offset": 5,
            "order_by": "updated_at",
            "tags": ["tag1", "tag2"],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def query_param_model_defaults(name: str):
    client = _client_for(name)
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "limit": 100,
            "offset": 0,
            "order_by": "created_at",
            "tags": [],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def query_param_model_invalid(name: str):
    client = _client_for(name)
    response = client.get(
        "/items/",
        params={
            "limit": 150,
            "offset": -1,
            "order_by": "invalid",
        },
    )
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "detail": [
                    {
                        "type": "less_than_equal",
                        "loc": ["query", "limit"],
                        "msg": "Input should be less than or equal to 100",
                        "input": "150",
                        "ctx": {"le": 100},
                    },
                    {
                        "type": "greater_than_equal",
                        "loc": ["query", "offset"],
                        "msg": "Input should be greater than or equal to 0",
                        "input": "-1",
                        "ctx": {"ge": 0},
                    },
                    {
                        "type": "literal_error",
                        "loc": ["query", "order_by"],
                        "msg": "Input should be 'created_at' or 'updated_at'",
                        "input": "invalid",
                        "ctx": {"expected": "'created_at' or 'updated_at'"},
                    },
                ]
            }
        )
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def query_param_model_extra(name: str):
    client = _client_for(name)
    response = client.get(
        "/items/",
        params={
            "limit": 10,
            "offset": 5,
            "order_by": "updated_at",
            "tags": ["tag1", "tag2"],
            "tool": "plumbus",
        },
    )
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "detail": [
                    {
                        "type": "extra_forbidden",
                        "loc": ["query", "tool"],
                        "msg": "Extra inputs are not permitted",
                        "input": "plumbus",
                    }
                ]
            }
        )
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
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
                    "/items/": {
                        "get": {
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "parameters": [
                                {
                                    "name": "limit",
                                    "in": "query",
                                    "required": False,
                                    "schema": {
                                        "type": "integer",
                                        "maximum": 100,
                                        "exclusiveMinimum": 0,
                                        "default": 100,
                                        "title": "Limit",
                                    },
                                },
                                {
                                    "name": "offset",
                                    "in": "query",
                                    "required": False,
                                    "schema": {
                                        "type": "integer",
                                        "minimum": 0,
                                        "default": 0,
                                        "title": "Offset",
                                    },
                                },
                                {
                                    "name": "order_by",
                                    "in": "query",
                                    "required": False,
                                    "schema": {
                                        "enum": ["created_at", "updated_at"],
                                        "type": "string",
                                        "default": "created_at",
                                        "title": "Order By",
                                    },
                                },
                                {
                                    "name": "tags",
                                    "in": "query",
                                    "required": False,
                                    "schema": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "default": [],
                                        "title": "Tags",
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
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "HTTPValidationError": {
                            "properties": {
                                "detail": {
                                    "items": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    },
                                    "type": "array",
                                    "title": "Detail",
                                }
                            },
                            "type": "object",
                            "title": "HTTPValidationError",
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
                                        ]
                                    },
                                    "type": "array",
                                    "title": "Location",
                                },
                                "msg": {"type": "string", "title": "Message"},
                                "type": {"type": "string", "title": "Error Type"},
                            },
                            "type": "object",
                            "required": ["loc", "msg", "type"],
                            "title": "ValidationError",
                        },
                    }
                },
            }
        )
    )
