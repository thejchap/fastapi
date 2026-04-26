from base64 import b64encode

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("security", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
    test.case("tutorial007_an_py310", name="tutorial007_an_py310"),
)
def security_http_basic(name: str):
    client = _client_for(name)
    response = client.get("/users/me", auth=("stanleyjobson", "swordfish"))
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"username": "stanleyjobson"})


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
    test.case("tutorial007_an_py310", name="tutorial007_an_py310"),
)
def security_http_basic_no_credentials(name: str):
    client = _client_for(name)
    response = client.get("/users/me")
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.status_code).to_equal(401).fatal()
    expect(response.headers["WWW-Authenticate"]).to_equal("Basic")


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
    test.case("tutorial007_an_py310", name="tutorial007_an_py310"),
)
def security_http_basic_invalid_credentials(name: str):
    client = _client_for(name)
    response = client.get(
        "/users/me", headers={"Authorization": "Basic notabase64token"}
    )
    expect(response.status_code).to_equal(401).fatal()
    expect(response.headers["WWW-Authenticate"]).to_equal("Basic")
    expect(response.json()).to_equal({"detail": "Not authenticated"})


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
    test.case("tutorial007_an_py310", name="tutorial007_an_py310"),
)
def security_http_basic_non_basic_credentials(name: str):
    client = _client_for(name)
    payload = b64encode(b"johnsecret").decode("ascii")
    auth_header = f"Basic {payload}"
    response = client.get("/users/me", headers={"Authorization": auth_header})
    expect(response.status_code).to_equal(401).fatal()
    expect(response.headers["WWW-Authenticate"]).to_equal("Basic")
    expect(response.json()).to_equal({"detail": "Not authenticated"})


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
    test.case("tutorial007_an_py310", name="tutorial007_an_py310"),
)
def security_http_basic_invalid_username(name: str):
    client = _client_for(name)
    response = client.get("/users/me", auth=("alice", "swordfish"))
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Incorrect username or password"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Basic")


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
    test.case("tutorial007_an_py310", name="tutorial007_an_py310"),
)
def security_http_basic_invalid_password(name: str):
    client = _client_for(name)
    response = client.get("/users/me", auth=("stanleyjobson", "wrongpassword"))
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Incorrect username or password"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Basic")


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
    test.case("tutorial007_an_py310", name="tutorial007_an_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
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
                        "HTTPBasic": {"type": "http", "scheme": "basic"}
                    }
                },
            }
        )
    )
