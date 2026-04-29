from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from docs_src.response_model.tutorial003_py310 import app


@fixture
def client() -> TestClient:
    return TestClient(app)


@test("POST /user filters password from UserOut response")
def post_user(client: TestClient = Depends(client)):
    response = client.post(
        "/user/",
        json={
            "username": "foo",
            "password": "fighter",
            "email": "foo@example.com",
            "full_name": "Grave Dohl",
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "username": "foo",
            "email": "foo@example.com",
            "full_name": "Grave Dohl",
        }
    )


@test("OpenAPI schema for tutorial003")
def openapi_schema(client: TestClient = Depends(client)):
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "OpenAPI schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/user/": {
                        "post": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/UserOut"
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
                            "summary": "Create User",
                            "operationId": "create_user_user__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/UserIn"
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "UserOut": {
                            "title": "UserOut",
                            "required": ["username", "email"],
                            "type": "object",
                            "properties": {
                                "username": {"title": "Username", "type": "string"},
                                "email": {
                                    "title": "Email",
                                    "type": "string",
                                    "format": "email",
                                },
                                "full_name": {
                                    "title": "Full Name",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                            },
                        },
                        "UserIn": {
                            "title": "UserIn",
                            "required": ["username", "password", "email"],
                            "type": "object",
                            "properties": {
                                "username": {"title": "Username", "type": "string"},
                                "password": {"title": "Password", "type": "string"},
                                "email": {
                                    "title": "Email",
                                    "type": "string",
                                    "format": "email",
                                },
                                "full_name": {
                                    "title": "Full Name",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                            },
                        },
                        "ValidationError": {
                            "title": "ValidationError",
                            "required": ["loc", "msg", "type"],
                            "type": "object",
                            "properties": {
                                "ctx": {"title": "Context", "type": "object"},
                                "input": {"title": "Input"},
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
