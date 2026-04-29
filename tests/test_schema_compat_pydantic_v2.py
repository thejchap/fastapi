from dirty_equals import IsOneOf
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import Depends, expect, fixture, test


@fixture
def client() -> TestClient:
    from enum import Enum

    app = FastAPI()

    class PlatformRole(str, Enum):
        admin = "admin"
        user = "user"

    class OtherRole(str, Enum): ...

    class User(BaseModel):
        username: str
        role: PlatformRole | OtherRole

    @app.get("/users")
    async def get_user() -> User:
        return {"username": "alice", "role": "admin"}

    return TestClient(app)


@test("Union of empty Enum and populated Enum serialises returned dict")
def get(client: TestClient = Depends(client)):
    response = client.get("/users")
    expect(response.json(), "response body").to_equal(
        {"username": "alice", "role": "admin"}
    )


@test("OpenAPI schema for Union of empty + populated Enum (Pydantic v2)")
def openapi_schema(client: TestClient = Depends(client)):
    response = client.get("openapi.json")
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/users": {
                        "get": {
                            "summary": "Get User",
                            "operationId": "get_user_users_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/User"
                                            }
                                        }
                                    },
                                }
                            },
                        }
                    }
                },
                "components": {
                    "schemas": IsOneOf(
                        # Pydantic >= 2.11: no top-level OtherRole
                        {
                            "PlatformRole": {
                                "type": "string",
                                "enum": ["admin", "user"],
                                "title": "PlatformRole",
                            },
                            "User": {
                                "properties": {
                                    "username": {"type": "string", "title": "Username"},
                                    "role": {
                                        "anyOf": [
                                            {
                                                "$ref": "#/components/schemas/PlatformRole"
                                            },
                                            {"enum": [], "title": "OtherRole"},
                                        ],
                                        "title": "Role",
                                    },
                                },
                                "type": "object",
                                "required": ["username", "role"],
                                "title": "User",
                            },
                        },
                        # Pydantic < 2.11: adds a top-level OtherRole schema
                        {
                            "OtherRole": {
                                "enum": [],
                                "title": "OtherRole",
                            },
                            "PlatformRole": {
                                "type": "string",
                                "enum": ["admin", "user"],
                                "title": "PlatformRole",
                            },
                            "User": {
                                "properties": {
                                    "username": {"type": "string", "title": "Username"},
                                    "role": {
                                        "anyOf": [
                                            {
                                                "$ref": "#/components/schemas/PlatformRole"
                                            },
                                            {"enum": [], "title": "OtherRole"},
                                        ],
                                        "title": "Role",
                                    },
                                },
                                "type": "object",
                                "required": ["username", "role"],
                                "title": "User",
                            },
                        },
                    )
                },
            }
        )
    )
