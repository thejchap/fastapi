from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("response_directly", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def path_operation(name: str):
    client = _client_for(name)
    expected_content = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """

    response = client.get("/legacy/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.headers["content-type"]).to_equal("application/xml")
    assert response.text == expected_content


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "info": {
                    "title": "FastAPI",
                    "version": "0.1.0",
                },
                "openapi": "3.1.0",
                "paths": {
                    "/legacy/": {
                        "get": {
                            "operationId": "get_legacy_data_legacy__get",
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {},
                                        },
                                    },
                                    "description": "Successful Response",
                                },
                            },
                            "summary": "Get Legacy Data",
                        },
                    },
                },
            }
        )
    )
