from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("query_params", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case(
        "tutorial004_py310 /users/123/items/foo",
        name="tutorial004_py310",
        path="/users/123/items/foo",
        expected_json={
            "item_id": "foo",
            "owner_id": 123,
            "description": "This is an amazing item that has a long description",
        },
    ),
    test.case(
        "tutorial004_py310 /users/1/items/bar?q",
        name="tutorial004_py310",
        path="/users/1/items/bar?q=somequery",
        expected_json={
            "item_id": "bar",
            "owner_id": 1,
            "q": "somequery",
            "description": "This is an amazing item that has a long description",
        },
    ),
    test.case(
        "tutorial004_py310 /users/42/items/baz?short",
        name="tutorial004_py310",
        path="/users/42/items/baz?short=true",
        expected_json={"item_id": "baz", "owner_id": 42},
    ),
)
def read_user_item(name: str, path: str, expected_json: dict):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal(expected_json)


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
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
                    "/users/{user_id}/items/{item_id}": {
                        "get": {
                            "summary": "Read User Item",
                            "operationId": "read_user_item_users__user_id__items__item_id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "User Id", "type": "integer"},
                                    "name": "user_id",
                                    "in": "path",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "Q",
                                        "anyOf": [
                                            {
                                                "type": "string",
                                            },
                                            {
                                                "type": "null",
                                            },
                                        ],
                                    },
                                    "name": "q",
                                    "in": "query",
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "Short",
                                        "type": "boolean",
                                        "default": False,
                                    },
                                    "name": "short",
                                    "in": "query",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
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
