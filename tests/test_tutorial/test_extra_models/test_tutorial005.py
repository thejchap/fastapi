from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("extra_models", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
)
def get_items(name: str):
    client = _client_for(name)
    response = client.get("/keyword-weights/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"foo": 2.3, "bar": 3.4})


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
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
                    "/keyword-weights/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "title": "Response Read Keyword Weights Keyword Weights  Get",
                                                "type": "object",
                                                "additionalProperties": {
                                                    "type": "number"
                                                },
                                            }
                                        }
                                    },
                                }
                            },
                            "summary": "Read Keyword Weights",
                            "operationId": "read_keyword_weights_keyword_weights__get",
                        }
                    }
                },
            }
        )
    )
