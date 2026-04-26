from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("security", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def no_token(name: str):
    client = _client_for(name)
    response = client.get("/items")
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def token(name: str):
    client = _client_for(name)
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"token": "testtoken"})


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def incorrect_token(name: str):
    client = _client_for(name)
    response = client.get("/items", headers={"Authorization": "Notexistent testtoken"})
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})
    expect(response.headers["WWW-Authenticate"]).to_equal("Bearer")


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
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
                    "/items/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "security": [{"OAuth2PasswordBearer": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "OAuth2PasswordBearer": {
                            "type": "oauth2",
                            "flows": {"password": {"scopes": {}, "tokenUrl": "token"}},
                        }
                    }
                },
            }
        )
    )
