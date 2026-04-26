from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("security", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
)
def login(name: str):
    client = _client_for(name)
    response = client.post("/token", data={"username": "johndoe", "password": "secret"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {"access_token": "johndoe", "token_type": "bearer"}
    )


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
)
def login_incorrect_password(name: str):
    client = _client_for(name)
    response = client.post(
        "/token", data={"username": "johndoe", "password": "incorrect"}
    )
    expect(response.status_code).to_equal(400).fatal()
    expect(response.json()).to_equal({"detail": "Incorrect username or password"})


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
)
def login_incorrect_username(name: str):
    client = _client_for(name)
    response = client.post("/token", data={"username": "foo", "password": "secret"})
    expect(response.status_code).to_equal(400).fatal()
    expect(response.json()).to_equal({"detail": "Incorrect username or password"})


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
)
def no_token(name: str):
    client = _client_for(name)
    response = client.get("/users/me")
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
)
def token(name: str):
    client = _client_for(name)
    response = client.get("/users/me", headers={"Authorization": "Bearer johndoe"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "fakehashedsecret",
            "disabled": False,
        }
    )


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
)
def incorrect_token(name: str):
    client = _client_for(name)
    response = client.get("/users/me", headers={"Authorization": "Bearer nonexistent"})
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
)
def incorrect_token_type(name: str):
    client = _client_for(name)
    response = client.get(
        "/users/me", headers={"Authorization": "Notexistent testtoken"}
    )
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
)
def inactive_user(name: str):
    client = _client_for(name)
    response = client.get("/users/me", headers={"Authorization": "Bearer alice"})
    expect(response.status_code).to_equal(400).fatal()
    expect(response.json()).to_equal({"detail": "Inactive user"})


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/token": {
                        "post": {
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
                            "summary": "Login",
                            "operationId": "login_token_post",
                            "requestBody": {
                                "content": {
                                    "application/x-www-form-urlencoded": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_login_token_post"
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    },
                    "/users/me": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Read Users Me",
                            "operationId": "read_users_me_users_me_get",
                            "security": [{"OAuth2PasswordBearer": []}],
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "Body_login_token_post": {
                            "title": "Body_login_token_post",
                            "required": ["username", "password"],
                            "type": "object",
                            "properties": {
                                "grant_type": {
                                    "title": "Grant Type",
                                    "anyOf": [
                                        {"pattern": "^password$", "type": "string"},
                                        {"type": "null"},
                                    ],
                                },
                                "username": {"title": "Username", "type": "string"},
                                "password": {
                                    "title": "Password",
                                    "type": "string",
                                    "format": "password",
                                },
                                "scope": {
                                    "title": "Scope",
                                    "type": "string",
                                    "default": "",
                                },
                                "client_id": {
                                    "title": "Client Id",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                                "client_secret": {
                                    "title": "Client Secret",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "format": "password",
                                },
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
                    },
                    "securitySchemes": {
                        "OAuth2PasswordBearer": {
                            "type": "oauth2",
                            "flows": {"password": {"scopes": {}, "tokenUrl": "token"}},
                        }
                    },
                },
            }
        )
    )
