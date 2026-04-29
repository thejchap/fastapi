from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from docs_src.body.tutorial003_py310 import app


@fixture
def client() -> TestClient:
    return TestClient(app)


@test("PUT with all fields succeeds")
def put_all(client: TestClient = Depends(client)):
    response = client.put(
        "/items/123",
        json={"name": "Foo", "price": 50.1, "description": "Some Foo", "tax": 0.3},
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "item_id": 123,
            "name": "Foo",
            "price": 50.1,
            "description": "Some Foo",
            "tax": 0.3,
        }
    )


@test("PUT with only required fields succeeds")
def put_only_required(client: TestClient = Depends(client)):
    response = client.put(
        "/items/123",
        json={"name": "Foo", "price": 50.1},
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "item_id": 123,
            "name": "Foo",
            "price": 50.1,
            "description": None,
            "tax": None,
        }
    )


@test("PUT with empty body returns missing-field errors")
def put_with_no_data(client: TestClient = Depends(client)):
    response = client.put("/items/123", json={})
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "input": {},
                },
                {
                    "type": "missing",
                    "loc": ["body", "price"],
                    "msg": "Field required",
                    "input": {},
                },
            ]
        }
    )


@test("OpenAPI schema matches snapshot")
def openapi_schema(client: TestClient = Depends(client)):
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
                                        "schema": {"$ref": "#/components/schemas/Item"}
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
