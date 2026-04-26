from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("dependencies", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case(
        "tutorial001_py310 /items",
        name="tutorial001_py310",
        path="/items",
        expected_status=200,
        expected_response={"q": None, "skip": 0, "limit": 100},
    ),
    test.case(
        "tutorial001_py310 /items?q=foo",
        name="tutorial001_py310",
        path="/items?q=foo",
        expected_status=200,
        expected_response={"q": "foo", "skip": 0, "limit": 100},
    ),
    test.case(
        "tutorial001_py310 /items?q=foo&skip=5",
        name="tutorial001_py310",
        path="/items?q=foo&skip=5",
        expected_status=200,
        expected_response={"q": "foo", "skip": 5, "limit": 100},
    ),
    test.case(
        "tutorial001_py310 /items?q=foo&skip=5&limit=30",
        name="tutorial001_py310",
        path="/items?q=foo&skip=5&limit=30",
        expected_status=200,
        expected_response={"q": "foo", "skip": 5, "limit": 30},
    ),
    test.case(
        "tutorial001_py310 /users",
        name="tutorial001_py310",
        path="/users",
        expected_status=200,
        expected_response={"q": None, "skip": 0, "limit": 100},
    ),
    test.case(
        "tutorial001_an_py310 /items",
        name="tutorial001_an_py310",
        path="/items",
        expected_status=200,
        expected_response={"q": None, "skip": 0, "limit": 100},
    ),
    test.case(
        "tutorial001_an_py310 /items?q=foo",
        name="tutorial001_an_py310",
        path="/items?q=foo",
        expected_status=200,
        expected_response={"q": "foo", "skip": 0, "limit": 100},
    ),
    test.case(
        "tutorial001_an_py310 /items?q=foo&skip=5",
        name="tutorial001_an_py310",
        path="/items?q=foo&skip=5",
        expected_status=200,
        expected_response={"q": "foo", "skip": 5, "limit": 100},
    ),
    test.case(
        "tutorial001_an_py310 /items?q=foo&skip=5&limit=30",
        name="tutorial001_an_py310",
        path="/items?q=foo&skip=5&limit=30",
        expected_status=200,
        expected_response={"q": "foo", "skip": 5, "limit": 30},
    ),
    test.case(
        "tutorial001_an_py310 /users",
        name="tutorial001_an_py310",
        path="/users",
        expected_status=200,
        expected_response={"q": None, "skip": 0, "limit": 100},
    ),
    test.case(
        "tutorial001_02_an_py310 /items",
        name="tutorial001_02_an_py310",
        path="/items",
        expected_status=200,
        expected_response={"q": None, "skip": 0, "limit": 100},
    ),
    test.case(
        "tutorial001_02_an_py310 /items?q=foo",
        name="tutorial001_02_an_py310",
        path="/items?q=foo",
        expected_status=200,
        expected_response={"q": "foo", "skip": 0, "limit": 100},
    ),
    test.case(
        "tutorial001_02_an_py310 /items?q=foo&skip=5",
        name="tutorial001_02_an_py310",
        path="/items?q=foo&skip=5",
        expected_status=200,
        expected_response={"q": "foo", "skip": 5, "limit": 100},
    ),
    test.case(
        "tutorial001_02_an_py310 /items?q=foo&skip=5&limit=30",
        name="tutorial001_02_an_py310",
        path="/items?q=foo&skip=5&limit=30",
        expected_status=200,
        expected_response={"q": "foo", "skip": 5, "limit": 30},
    ),
    test.case(
        "tutorial001_02_an_py310 /users",
        name="tutorial001_02_an_py310",
        path="/users",
        expected_status=200,
        expected_response={"q": None, "skip": 0, "limit": 100},
    ),
)
def get(name: str, path: str, expected_status: int, expected_response: dict):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code).to_equal(expected_status)
    expect(response.json()).to_equal(expected_response)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
    test.case("tutorial001_02_an_py310", name="tutorial001_02_an_py310"),
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
                    "/items/": {
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
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Q",
                                    },
                                    "name": "q",
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
                                        "title": "Limit",
                                        "type": "integer",
                                        "default": 100,
                                    },
                                    "name": "limit",
                                    "in": "query",
                                },
                            ],
                        }
                    },
                    "/users/": {
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
                            "summary": "Read Users",
                            "operationId": "read_users_users__get",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Q",
                                    },
                                    "name": "q",
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
                                        "title": "Limit",
                                        "type": "integer",
                                        "default": 100,
                                    },
                                    "name": "limit",
                                    "in": "query",
                                },
                            ],
                        }
                    },
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
