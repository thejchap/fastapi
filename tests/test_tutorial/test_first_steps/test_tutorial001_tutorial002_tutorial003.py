from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("first_steps", name)
    return TestClient(mod.app)


@test.cases(
    test.case(
        "tutorial001 root",
        name="tutorial001_py310",
        path="/",
        expected_status=200,
        expected_response={"message": "Hello World"},
    ),
    test.case(
        "tutorial001 nonexistent",
        name="tutorial001_py310",
        path="/nonexistent",
        expected_status=404,
        expected_response={"detail": "Not Found"},
    ),
    test.case(
        "tutorial003 root",
        name="tutorial003_py310",
        path="/",
        expected_status=200,
        expected_response={"message": "Hello World"},
    ),
    test.case(
        "tutorial003 nonexistent",
        name="tutorial003_py310",
        path="/nonexistent",
        expected_status=404,
        expected_response={"detail": "Not Found"},
    ),
)
def get_path(name: str, path: str, expected_status: int, expected_response: dict):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code).to_equal(expected_status).fatal()
    expect(response.json()).to_equal(expected_response)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial003_py310", name="tutorial003_py310"),
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
                    "/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Root",
                            "operationId": "root__get",
                        }
                    }
                },
            }
        )
    )
