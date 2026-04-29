from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2, OAuth2PasswordRequestFormStrict
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()

reusable_oauth2 = OAuth2(
    flows={
        "password": {
            "tokenUrl": "token",
            "scopes": {"read:users": "Read the users", "write:users": "Create users"},
        }
    }
)


class User(BaseModel):
    username: str


# Here we use string annotations to test them
def get_current_user(oauth_header: "str" = Security(reusable_oauth2)):
    user = User(username=oauth_header)
    return user


@app.post("/login")
# Here we use string annotations to test them
def login(form_data: "OAuth2PasswordRequestFormStrict" = Depends()):
    return form_data


@app.get("/users/me")
# Here we use string annotations to test them
def read_current_user(current_user: "User" = Depends(get_current_user)):
    return current_user


client = TestClient(app)


@test("OAuth2 reads Bearer authorization header verbatim")
def security_oauth2():
    response = client.get("/users/me", headers={"Authorization": "Bearer footokenbar"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"username": "Bearer footokenbar"})


@test("OAuth2 reads non-Bearer authorization header verbatim")
def security_oauth2_password_other_header():
    response = client.get("/users/me", headers={"Authorization": "Other footokenbar"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"username": "Other footokenbar"})


@test("OAuth2 rejects request without authorization header")
def security_oauth2_password_bearer_no_header():
    response = client.get("/users/me")
    expect(response.status_code, "status code").to_equal(401).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"], "WWW-Authenticate header").to_equal(
        "Bearer"
    )


@test("Strict OAuth2 password form rejects empty body")
def strict_login_no_data():
    response = client.post("/login")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "grant_type"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["body", "username"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["body", "password"],
                    "msg": "Field required",
                    "input": None,
                },
            ]
        }
    )


@test("Strict OAuth2 password form rejects missing grant_type")
def strict_login_no_grant_type():
    response = client.post("/login", data={"username": "johndoe", "password": "secret"})
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "grant_type"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case("incorrect value", grant_type="incorrect"),
    test.case("password with suffix", grant_type="passwordblah"),
    test.case("password with prefix", grant_type="blahpassword"),
)
def strict_login_incorrect_grant_type(grant_type: str):
    response = client.post(
        "/login",
        data={"username": "johndoe", "password": "secret", "grant_type": grant_type},
    )
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["body", "grant_type"],
                    "msg": "String should match pattern '^password$'",
                    "input": grant_type,
                    "ctx": {"pattern": "^password$"},
                }
            ]
        }
    )


@test("Strict OAuth2 password form accepts complete data")
def strict_login_correct_grant_type():
    response = client.post(
        "/login",
        data={"username": "johndoe", "password": "secret", "grant_type": "password"},
    )
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {
            "grant_type": "password",
            "username": "johndoe",
            "password": "secret",
            "scopes": [],
            "client_id": None,
            "client_secret": None,
        }
    )


@test("OpenAPI schema includes OAuth2 password flow")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/login": {
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
                            "operationId": "login_login_post",
                            "requestBody": {
                                "content": {
                                    "application/x-www-form-urlencoded": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_login_login_post"
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
                            "summary": "Read Current User",
                            "operationId": "read_current_user_users_me_get",
                            "security": [{"OAuth2": []}],
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "Body_login_login_post": {
                            "title": "Body_login_login_post",
                            "required": ["grant_type", "username", "password"],
                            "type": "object",
                            "properties": {
                                "grant_type": {
                                    "title": "Grant Type",
                                    "pattern": "^password$",
                                    "type": "string",
                                },
                                "username": {"title": "Username", "type": "string"},
                                "password": {"title": "Password", "type": "string"},
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
                        "OAuth2": {
                            "type": "oauth2",
                            "flows": {
                                "password": {
                                    "scopes": {
                                        "read:users": "Read the users",
                                        "write:users": "Create users",
                                    },
                                    "tokenUrl": "token",
                                }
                            },
                        }
                    },
                },
            }
        )
    )
