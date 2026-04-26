from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.handling_errors.tutorial005_py310 import app

client = TestClient(app)


@test
def post_validation_error():
    response = client.post("/items/", json={"title": "towel", "size": "XL"})
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["body", "size"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "XL",
                }
            ],
            "body": {"title": "towel", "size": "XL"},
        }
    )


@test
def post():
    data = {"title": "towel", "size": 5}
    response = client.post("/items/", json=data)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(data)


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
                        "post": {
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
                            "required": ["title", "size"],
                            "type": "object",
                            "properties": {
                                "title": {"title": "Title", "type": "string"},
                                "size": {"title": "Size", "type": "integer"},
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
