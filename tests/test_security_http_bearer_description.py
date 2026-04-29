from fastapi import FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()

security = HTTPBearer(description="HTTP Bearer token scheme")


@app.get("/users/me")
def read_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}


client = TestClient(app)


@test("HTTPBearer with description authenticates with valid Bearer token")
def security_http_bearer():
    response = client.get("/users/me", headers={"Authorization": "Bearer foobar"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"scheme": "Bearer", "credentials": "foobar"}
    )


@test("HTTPBearer without credentials returns 401")
def security_http_bearer_no_credentials():
    response = client.get("/users/me")
    expect(response.status_code, "status code").to_equal(401).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"], "WWW-Authenticate header").to_equal(
        "Bearer"
    )


@test("HTTPBearer rejects non-Bearer scheme credentials")
def security_http_bearer_incorrect_scheme_credentials():
    response = client.get("/users/me", headers={"Authorization": "Basic notreally"})
    expect(response.status_code, "status code").to_equal(401).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"], "WWW-Authenticate header").to_equal(
        "Bearer"
    )


@test("OpenAPI schema includes HTTPBearer description")
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
                            "security": [{"HTTPBearer": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "HTTPBearer": {
                            "type": "http",
                            "scheme": "bearer",
                            "description": "HTTP Bearer token scheme",
                        }
                    }
                },
            }
        )
    )
