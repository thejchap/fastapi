from fastapi import Depends, FastAPI, Security
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()

oid = OpenIdConnect(
    openIdConnectUrl="/openid", description="OpenIdConnect security scheme"
)


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str = Security(oid)):
    user = User(username=oauth_header)
    return user


@app.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


client = TestClient(app)


@test("OpenIdConnect with description reads Bearer header")
def security_oauth2():
    response = client.get("/users/me", headers={"Authorization": "Bearer footokenbar"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"username": "Bearer footokenbar"})


@test("OpenIdConnect with description reads non-Bearer header")
def security_oauth2_password_other_header():
    response = client.get("/users/me", headers={"Authorization": "Other footokenbar"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"username": "Other footokenbar"})


@test("OpenIdConnect with description rejects missing header")
def security_oauth2_password_bearer_no_header():
    response = client.get("/users/me")
    expect(response.status_code, "status code").to_equal(401).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"], "WWW-Authenticate header").to_equal(
        "Bearer"
    )


@test("OpenAPI schema includes OpenIdConnect description")
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
                            "security": [{"OpenIdConnect": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "OpenIdConnect": {
                            "type": "openIdConnect",
                            "openIdConnectUrl": "/openid",
                            "description": "OpenIdConnect security scheme",
                        }
                    }
                },
            }
        )
    )
