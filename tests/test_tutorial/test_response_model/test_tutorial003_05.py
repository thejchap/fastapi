from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from docs_src.response_model.tutorial003_05_py310 import app


@fixture
def client() -> TestClient:
    return TestClient(app)


@test("GET /portal returns interdimensional portal message")
def get_portal(client: TestClient = Depends(client)):
    response = client.get("/portal")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"message": "Here's your interdimensional portal."}
    )


@test("GET /portal?teleport=true issues a 307 redirect")
def get_redirect(client: TestClient = Depends(client)):
    response = client.get("/portal", params={"teleport": True}, follow_redirects=False)
    expect(response.status_code, "status code").to_equal(307).fatal()
    expect(response.headers["location"], "Location header").to_equal(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )


@test("OpenAPI schema for tutorial003_05")
def openapi_schema(client: TestClient = Depends(client)):
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "OpenAPI schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/portal": {
                        "get": {
                            "summary": "Get Portal",
                            "operationId": "get_portal_portal_get",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "Teleport",
                                        "type": "boolean",
                                        "default": False,
                                    },
                                    "name": "teleport",
                                    "in": "query",
                                }
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
