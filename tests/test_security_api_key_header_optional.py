from fastapi import Depends, FastAPI, Security
from fastapi.security import APIKeyHeader
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()

api_key = APIKeyHeader(name="key", auto_error=False)


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str | None = Security(api_key)):
    if oauth_header is None:
        return None
    user = User(username=oauth_header)
    return user


@app.get("/users/me")
def read_current_user(current_user: User | None = Depends(get_current_user)):
    if current_user is None:
        return {"msg": "Create an account first"}
    return current_user


client = TestClient(app)


@test("optional APIKeyHeader authenticates with valid header")
def security_api_key():
    response = client.get("/users/me", headers={"key": "secret"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"username": "secret"})


@test("optional APIKeyHeader passes None when header missing")
def security_api_key_no_key():
    response = client.get("/users/me")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"msg": "Create an account first"}
    )


@test("OpenAPI schema for optional APIKeyHeader")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
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
                            "security": [{"APIKeyHeader": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "APIKeyHeader": {
                            "type": "apiKey",
                            "name": "key",
                            "in": "header",
                        }
                    }
                },
            }
        )
    )
