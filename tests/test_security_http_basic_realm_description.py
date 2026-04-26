from base64 import b64encode

from fastapi import FastAPI, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()

security = HTTPBasic(realm="simple", description="HTTPBasic scheme")


@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Security(security)):
    return {"username": credentials.username, "password": credentials.password}


client = TestClient(app)


@test
def security_http_basic():
    response = client.get("/users/me", auth=("john", "secret"))
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"username": "john", "password": "secret"})


@test
def security_http_basic_no_credentials():
    response = client.get("/users/me")
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.status_code).to_equal(401)
    expect(response.headers["WWW-Authenticate"]).to_equal('Basic realm="simple"')


@test
def security_http_basic_invalid_credentials():
    response = client.get(
        "/users/me", headers={"Authorization": "Basic notabase64token"}
    )
    expect(response.status_code).to_equal(401).fatal()
    expect(response.headers["WWW-Authenticate"]).to_equal('Basic realm="simple"')
    expect(response.json()).to_equal({"detail": "Not authenticated"})


@test
def security_http_basic_non_basic_credentials():
    payload = b64encode(b"johnsecret").decode("ascii")
    auth_header = f"Basic {payload}"
    response = client.get("/users/me", headers={"Authorization": auth_header})
    expect(response.status_code).to_equal(401).fatal()
    expect(response.headers["WWW-Authenticate"]).to_equal('Basic realm="simple"')
    expect(response.json()).to_equal({"detail": "Not authenticated"})


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
                            "security": [{"HTTPBasic": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "HTTPBasic": {
                            "type": "http",
                            "scheme": "basic",
                            "description": "HTTPBasic scheme",
                        }
                    }
                },
            }
        )
    )
