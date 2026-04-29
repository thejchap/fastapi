from fastapi import Depends, FastAPI, Security
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()

oid = OpenIdConnect(openIdConnectUrl="/openid", auto_error=False)


class User(BaseModel):
    username: str


def get_current_user(oauth_header: str | None = Security(oid)):
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


@test("Optional OpenIdConnect reads Bearer authorization header")
def security_oauth2():
    response = client.get("/users/me", headers={"Authorization": "Bearer footokenbar"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"username": "Bearer footokenbar"})


@test("Optional OpenIdConnect reads non-Bearer authorization header")
def security_oauth2_password_other_header():
    response = client.get("/users/me", headers={"Authorization": "Other footokenbar"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"username": "Other footokenbar"})


@test("Optional OpenIdConnect allows missing authorization header")
def security_oauth2_password_bearer_no_header():
    response = client.get("/users/me")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"msg": "Create an account first"}
    )


@test("OpenAPI schema includes optional OpenIdConnect scheme")
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
                        }
                    }
                },
            }
        )
    )
