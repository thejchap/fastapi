from types import ModuleType
from unittest.mock import patch

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _module_for(name: str) -> ModuleType:
    return import_tutorial("security", name)


def get_access_token(*, username="johndoe", password="secret", client: TestClient):
    data = {"username": username, "password": password}
    response = client.post("/token", data=data)
    content = response.json()
    access_token = content.get("access_token")
    return access_token


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def login(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.post("/token", data={"username": "johndoe", "password": "secret"})
    expect(response.status_code).to_equal(200).fatal()
    content = response.json()
    expect(content).to_contain("access_token")
    expect(content["token_type"]).to_equal("bearer")


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def login_incorrect_password(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.post(
        "/token", data={"username": "johndoe", "password": "incorrect"}
    )
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Incorrect username or password"})


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def login_incorrect_username(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.post("/token", data={"username": "foo", "password": "secret"})
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Incorrect username or password"})


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def no_token(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.get("/users/me")
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def token(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    access_token = get_access_token(client=client)
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "disabled": False,
        }
    )


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def incorrect_token(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.get("/users/me", headers={"Authorization": "Bearer nonexistent"})
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Could not validate credentials"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def incorrect_token_type(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.get(
        "/users/me", headers={"Authorization": "Notexistent testtoken"}
    )
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def verify_password(name: str):
    mod = _module_for(name)
    expect(
        mod.verify_password("secret", mod.fake_users_db["johndoe"]["hashed_password"])
    ).to_be_truthy()


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def get_password_hash(name: str):
    mod = _module_for(name)
    expect(mod.get_password_hash("johndoe")).to_be_truthy()


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def create_access_token(name: str):
    mod = _module_for(name)
    access_token = mod.create_access_token(data={"data": "foo"})
    expect(access_token).to_be_truthy()


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def token_no_sub(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiZm9vIn0.9ynBhuYb4e6aW3oJr_K_TBgwcMTDpRToQIE25L57rOE"
        },
    )
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Could not validate credentials"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def token_no_username(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmb28ifQ.NnExK_dlNAYyzACrXtXDrcWOgGY2JuPbI4eDaHdfK5Y"
        },
    )
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Could not validate credentials"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def token_nonexistent_user(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VybmFtZTpib2IifQ.HcfCW67Uda-0gz54ZWTqmtgJnZeNem0Q757eTa9EZuw"
        },
    )
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Could not validate credentials"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def token_inactive_user(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    alice_user_data = {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": mod.get_password_hash("secretalice"),
        "disabled": True,
    }
    with patch.dict(f"{mod.__name__}.fake_users_db", {"alice": alice_user_data}):
        access_token = get_access_token(
            username="alice", password="secretalice", client=client
        )
        response = client.get(
            "/users/me", headers={"Authorization": f"Bearer {access_token}"}
        )
    expect(response.status_code).to_equal(400).fatal()
    expect(response.json()).to_equal({"detail": "Inactive user"})


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def read_items(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    access_token = get_access_token(client=client)
    response = client.get(
        "/users/me/items/", headers={"Authorization": f"Bearer {access_token}"}
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal([{"item_id": "Foo", "owner": "johndoe"}])


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def openapi_schema(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
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
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Token"
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
                            "summary": "Login For Access Token",
                            "operationId": "login_for_access_token_token_post",
                            "requestBody": {
                                "content": {
                                    "application/x-www-form-urlencoded": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_login_for_access_token_token_post"
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    },
                    "/users/me/": {
                        "get": {
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
                            "summary": "Read Users Me",
                            "operationId": "read_users_me_users_me__get",
                            "security": [{"OAuth2PasswordBearer": []}],
                        }
                    },
                    "/users/me/items/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Read Own Items",
                            "operationId": "read_own_items_users_me_items__get",
                            "security": [{"OAuth2PasswordBearer": []}],
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "User": {
                            "title": "User",
                            "required": ["username"],
                            "type": "object",
                            "properties": {
                                "username": {"title": "Username", "type": "string"},
                                "email": {
                                    "title": "Email",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                                "full_name": {
                                    "title": "Full Name",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                                "disabled": {
                                    "title": "Disabled",
                                    "anyOf": [{"type": "boolean"}, {"type": "null"}],
                                },
                            },
                        },
                        "Token": {
                            "title": "Token",
                            "required": ["access_token", "token_type"],
                            "type": "object",
                            "properties": {
                                "access_token": {
                                    "title": "Access Token",
                                    "type": "string",
                                },
                                "token_type": {"title": "Token Type", "type": "string"},
                            },
                        },
                        "Body_login_for_access_token_token_post": {
                            "title": "Body_login_for_access_token_token_post",
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
                            "flows": {
                                "password": {
                                    "scopes": {},
                                    "tokenUrl": "token",
                                }
                            },
                        }
                    },
                },
            }
        )
    )
