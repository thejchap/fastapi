from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.handling_errors.tutorial003_py310 import app

client = TestClient(app)


@test("GET /unicorns/shinny returns the unicorn")
def get():
    response = client.get("/unicorns/shinny")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"unicorn_name": "shinny"})


@test("GET /unicorns/yolo invokes the custom exception handler")
def get_exception():
    response = client.get("/unicorns/yolo")
    expect(response.status_code, "status code").to_equal(418).fatal()
    expect(response.json(), "response body").to_equal(
        {"message": "Oops! yolo did something. There goes a rainbow..."}
    )


@test("OpenAPI schema matches snapshot")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/unicorns/{name}": {
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
                            "summary": "Read Unicorn",
                            "operationId": "read_unicorn_unicorns__name__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Name", "type": "string"},
                                    "name": "name",
                                    "in": "path",
                                }
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
