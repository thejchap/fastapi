from dirty_equals import IsList
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from docs_src.path_operation_configuration.tutorial002_py310 import app


@fixture
def client() -> TestClient:
    return TestClient(app)


@test("POST /items/ creates an item")
def post_items(client: TestClient = Depends(client)):
    response = client.post(
        "/items/",
        json={
            "name": "Foo",
            "description": "Item description",
            "price": 42.0,
            "tax": 3.2,
            "tags": ["bar", "baz"],
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "name": "Foo",
            "description": "Item description",
            "price": 42.0,
            "tax": 3.2,
            "tags": IsList("bar", "baz", check_order=False),
        }
    )


@test("GET /items/ lists items")
def get_items(client: TestClient = Depends(client)):
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal([{"name": "Foo", "price": 42}])


@test("GET /users/ lists users")
def get_users(client: TestClient = Depends(client)):
    response = client.get("/users/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal([{"username": "johndoe"}])


@test("OpenAPI schema matches the snapshot")
def openapi_schema(client: TestClient = Depends(client)):
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
                            "tags": ["items"],
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        },
                        "post": {
                            "tags": ["items"],
                            "summary": "Create Item",
                            "operationId": "create_item_items__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Item"
                                            }
                                        }
                                    },
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
                        },
                    },
                    "/users/": {
                        "get": {
                            "tags": ["users"],
                            "summary": "Read Users",
                            "operationId": "read_users_users__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        }
                    },
                },
                "components": {
                    "schemas": {
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
                                "description": {
                                    "anyOf": [
                                        {
                                            "type": "string",
                                        },
                                        {
                                            "type": "null",
                                        },
                                    ],
                                    "title": "Description",
                                },
                                "name": {
                                    "title": "Name",
                                    "type": "string",
                                },
                                "price": {
                                    "title": "Price",
                                    "type": "number",
                                },
                                "tags": {
                                    "default": [],
                                    "items": {
                                        "type": "string",
                                    },
                                    "title": "Tags",
                                    "type": "array",
                                    "uniqueItems": True,
                                },
                                "tax": {
                                    "anyOf": [
                                        {
                                            "type": "number",
                                        },
                                        {
                                            "type": "null",
                                        },
                                    ],
                                    "title": "Tax",
                                },
                            },
                            "required": [
                                "name",
                                "price",
                            ],
                            "title": "Item",
                            "type": "object",
                        },
                        "ValidationError": {
                            "properties": {
                                "ctx": {"title": "Context", "type": "object"},
                                "input": {"title": "Input"},
                                "loc": {
                                    "items": {
                                        "anyOf": [
                                            {
                                                "type": "string",
                                            },
                                            {
                                                "type": "integer",
                                            },
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
