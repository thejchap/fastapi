from fastapi import Depends, FastAPI, Security
from fastapi.security import APIKeyCookie
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()

api_key = APIKeyCookie(name="key")


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(api_key)):
    user = User(username=oauth_header)
    return user


@app.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@test
def security_api_key():
    client = TestClient(app, cookies={"key": "secret"})
    response = client.get("/users/me")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"username": "secret"})


@test
def security_api_key_no_key():
    client = TestClient(app)
    response = client.get("/users/me")
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"]).to_equal("APIKey")


@test
def openapi_schema():
    client = TestClient(app)
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
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Read Current User",
                            "operationId": "read_current_user_users_me_get",
                            "security": [{"APIKeyCookie": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "APIKeyCookie": {
                            "type": "apiKey",
                            "name": "key",
                            "in": "cookie",
                        }
                    }
                },
            }
        )
    )
