from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.path_params.tutorial003_py310 import app

client = TestClient(app)


@test.cases(
    test.case("me", user_id="me", expected_response={"user_id": "the current user"}),
    test.case("alice", user_id="alice", expected_response={"user_id": "alice"}),
)
def get_users(user_id: str, expected_response: dict):
    response = client.get(f"/users/{user_id}")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(expected_response)


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
                    "/users/me": {
                        "get": {
                            "operationId": "read_user_me_users_me_get",
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {},
                                        },
                                    },
                                    "description": "Successful Response",
                                },
                            },
                            "summary": "Read User Me",
                        },
                    },
                    "/users/{user_id}": {
                        "get": {
                            "operationId": "read_user_users__user_id__get",
                            "parameters": [
                                {
                                    "in": "path",
                                    "name": "user_id",
                                    "required": True,
                                    "schema": {
                                        "title": "User Id",
                                        "type": "string",
                                    },
                                },
                            ],
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {},
                                        },
                                    },
                                    "description": "Successful Response",
                                },
                                "422": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError",
                                            },
                                        },
                                    },
                                    "description": "Validation Error",
                                },
                            },
                            "summary": "Read User",
                        },
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
