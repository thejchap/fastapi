from fastapi import FastAPI, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()

security = HTTPBase(scheme="Other", auto_error=False)


@app.get("/users/me")
def read_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
):
    if credentials is None:
        return {"msg": "Create an account first"}
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}


client = TestClient(app)


@test("optional HTTPBase authenticates with valid credentials")
def security_http_base():
    response = client.get("/users/me", headers={"Authorization": "Other foobar"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"scheme": "Other", "credentials": "foobar"}
    )


@test("optional HTTPBase passes None when credentials missing")
def security_http_base_no_credentials():
    response = client.get("/users/me")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"msg": "Create an account first"}
    )


@test("OpenAPI schema for optional HTTPBase")
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
                            "security": [{"HTTPBase": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {"HTTPBase": {"type": "http", "scheme": "Other"}}
                },
            }
        )
    )
