from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.query_params.tutorial005_py310 import app

client = TestClient(app)


@test("required query param is accepted")
def foo_needy_very():
    response = client.get("/items/foo?needy=very")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"item_id": "foo", "needy": "very"})


@test("missing required query param returns 422")
def foo_no_needy():
    response = client.get("/items/foo")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "needy"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("OpenAPI schema matches the snapshot")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "openapi schema").to_equal(
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
