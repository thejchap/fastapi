from fastapi import FastAPI, Security
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()

security = HTTPBase(scheme="Other", description="Other Security Scheme")


@app.get("/users/me")
def read_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}


client = TestClient(app)


@test
def security_http_base():
    response = client.get("/users/me", headers={"Authorization": "Other foobar"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"scheme": "Other", "credentials": "foobar"})


@test
def security_http_base_no_credentials():
    response = client.get("/users/me")
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Other")


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
                    "securitySchemes": {
                        "HTTPBase": {
                            "type": "http",
                            "scheme": "Other",
                            "description": "Other Security Scheme",
                        }
                    }
                },
            }
        )
    )
