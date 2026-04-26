from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.generate_clients.tutorial003_py310 import app

client = TestClient(app)


@test
def post_items():
    response = client.post("/items/", json={"name": "Foo", "price": 5})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"message": "Item received"})


@test
def post_users():
    response = client.post(
        "/users/", json={"username": "Foo", "email": "foo@example.com"}
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"message": "User received"})


@test
def get_items():
    response = client.get("/items/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        [
            {"name": "Plumbus", "price": 3},
            {"name": "Portal Gun", "price": 9001},
        ]
    )


@test
def openapi_schema():
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
                            "tags": ["items"],
                            "summary": "Get Items",
                            "operationId": "items-get_items",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "title": "Response Items-Get Items",
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/Item"
                                                },
                                            }
                                        }
                                    },
                                }
                            },
                        },
                        "post": {
                            "tags": ["items"],
                            "summary": "Create Item",
                            "operationId": "items-create_item",
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
                                                "$ref": "#/components/schemas/ResponseMessage"
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
                        "post": {
                            "tags": ["users"],
                            "summary": "Create User",
                            "operationId": "users-create_user",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/User"}
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
                                                "$ref": "#/components/schemas/ResponseMessage"
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
                        }
                    },
                },
                "components": {
                    "schemas": {
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
                        "Item": {
                            "title": "Item",
                            "required": ["name", "price"],
                            "type": "object",
                            "properties": {
                                "name": {"title": "Name", "type": "string"},
                                "price": {"title": "Price", "type": "number"},
                            },
                        },
                        "ResponseMessage": {
                            "title": "ResponseMessage",
                            "required": ["message"],
                            "type": "object",
                            "properties": {
                                "message": {"title": "Message", "type": "string"}
                            },
                        },
                        "User": {
                            "title": "User",
                            "required": ["username", "email"],
                            "type": "object",
                            "properties": {
                                "username": {"title": "Username", "type": "string"},
                                "email": {"title": "Email", "type": "string"},
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
                    }
                },
            }
        )
    )
