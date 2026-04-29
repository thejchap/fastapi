from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("custom_response", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial010_py310", name="tutorial010_py310"),
)
def get_custom_response(name: str):
    client = _client_for(name)
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.text, "response text").to_equal(
        snapshot("<h1>Items</h1><p>This is a list of items.</p>")
    )


@test.cases(
    test.case("tutorial010_py310", name="tutorial010_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
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
                                    "content": {
                                        "text/html": {"schema": {"type": "string"}}
                                    },
                                }
                            },
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                        }
                    }
                },
            }
        )
    )
