from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("authentication_error_status_code", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def get_me(name: str):
    client = _client_for(name)
    response = client.get("/me", headers={"Authorization": "Bearer secrettoken"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "message": "You are authenticated",
            "token": "secrettoken",
        }
    )


@test.cases(
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def get_me_no_credentials(name: str):
    client = _client_for(name)
    response = client.get("/me")
    expect(response.status_code).to_equal(403).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})


@test.cases(
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
                    "/me": {
                        "get": {
                            "summary": "Read Me",
                            "operationId": "read_me_me_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "security": [{"HTTPBearer403": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "HTTPBearer403": {"type": "http", "scheme": "bearer"}
                    }
                },
            }
        )
    )
