from fastapi import FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPDigest
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()

security = HTTPDigest()


@app.get("/users/me")
def read_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}


client = TestClient(app)


@test("HTTP Digest auth accepts valid Digest header")
def security_http_digest():
    response = client.get("/users/me", headers={"Authorization": "Digest foobar"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"scheme": "Digest", "credentials": "foobar"}
    )


@test("HTTP Digest auth rejects request without credentials")
def security_http_digest_no_credentials():
    response = client.get("/users/me")
    expect(response.status_code, "status code").to_equal(401).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"], "WWW-Authenticate header").to_equal(
        "Digest"
    )


@test("HTTP Digest auth rejects incorrect scheme")
def security_http_digest_incorrect_scheme_credentials():
    response = client.get(
        "/users/me", headers={"Authorization": "Other invalidauthorization"}
    )
    expect(response.status_code, "status code").to_equal(401).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"], "WWW-Authenticate header").to_equal(
        "Digest"
    )


@test("OpenAPI schema includes HTTPDigest security scheme")
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
                            "security": [{"HTTPDigest": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "HTTPDigest": {"type": "http", "scheme": "digest"}
                    }
                },
            }
        )
    )
