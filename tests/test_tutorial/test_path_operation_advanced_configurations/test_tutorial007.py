from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("path_operation_advanced_configuration", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
)
def post(name: str):
    client = _client_for(name)
    yaml_data = """
        name: Deadpoolio
        tags:
        - x-force
        - x-men
        - x-avengers
        """
    response = client.post("/items/", content=yaml_data)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "name": "Deadpoolio",
            "tags": ["x-force", "x-men", "x-avengers"],
        }
    )


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
)
def post_broken_yaml(name: str):
    client = _client_for(name)
    yaml_data = """
        name: Deadpoolio
        tags:
        x - x-force
        x - x-men
        x - x-avengers
        """
    response = client.post("/items/", content=yaml_data)
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal({"detail": "Invalid YAML"})


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
)
def post_invalid(name: str):
    client = _client_for(name)
    yaml_data = """
        name: Deadpoolio
        tags:
        - x-force
        - x-men
        - x-avengers
        - sneaky: object
        """
    response = client.post("/items/", content=yaml_data)
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "string_type",
                    "loc": ["tags", 3],
                    "msg": "Input should be a valid string",
                    "input": {"sneaky": "object"},
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
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
                        "post": {
                            "summary": "Create Item",
                            "operationId": "create_item_items__post",
                            "requestBody": {
                                "content": {
                                    "application/x-yaml": {
                                        "schema": {
                                            "title": "Item",
                                            "required": ["name", "tags"],
                                            "type": "object",
                                            "properties": {
                                                "name": {
                                                    "title": "Name",
                                                    "type": "string",
                                                },
                                                "tags": {
                                                    "title": "Tags",
                                                    "type": "array",
                                                    "items": {"type": "string"},
                                                },
                                            },
                                        }
                                    }
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        }
                    }
                },
            }
        )
    )
