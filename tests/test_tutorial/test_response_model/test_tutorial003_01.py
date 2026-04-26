from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from docs_src.response_model.tutorial003_01_py310 import app


@fixture
def client() -> TestClient:
    return TestClient(app)


@test
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
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "username": "foo",
            "email": "foo@example.com",
            "full_name": "Grave Dohl",
        }
    )


@test
def openapi_schema(client: TestClient = Depends(client)):
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/user/": {
                        "post": {
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
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/BaseUser"
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
                    }
                },
                "components": {
                    "schemas": {
                        "BaseUser": {
                            "title": "BaseUser",
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
                        "UserIn": {
                            "title": "UserIn",
                            "required": ["username", "email", "password"],
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
                                "password": {"title": "Password", "type": "string"},
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
                    }
                },
            }
        )
    )
