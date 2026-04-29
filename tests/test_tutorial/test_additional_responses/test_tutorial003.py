from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.additional_responses.tutorial003_py310 import app

client = TestClient(app)


@test("GET /items/foo returns the item")
def path_operation():
    response = client.get("/items/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"id": "foo", "value": "there goes my hero"}
    )


@test("GET /items/bar returns the 404 message")
def path_operation_not_found():
    response = client.get("/items/bar")
    expect(response.status_code, "status code").to_equal(404).fatal()
    expect(response.json(), "response body").to_equal({"message": "Item not found"})


@test("OpenAPI schema matches snapshot")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/{item_id}": {
                        "get": {
                            "responses": {
                                "404": {
                                    "description": "The item was not found",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Message"
                                            }
                                        }
                                    },
                                },
                                "200": {
                                    "description": "Item requested by ID",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Item"
                                            },
                                            "example": {
                                                "id": "bar",
                                                "value": "The bar tenders",
                                            },
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
                            "summary": "Read Item",
                            "operationId": "read_item_items__item_id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                }
                            ],
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "Item": {
                            "title": "Item",
                            "required": ["id", "value"],
                            "type": "object",
                            "properties": {
                                "id": {"title": "Id", "type": "string"},
                                "value": {"title": "Value", "type": "string"},
                            },
                        },
                        "Message": {
                            "title": "Message",
                            "required": ["message"],
                            "type": "object",
                            "properties": {
                                "message": {"title": "Message", "type": "string"}
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
