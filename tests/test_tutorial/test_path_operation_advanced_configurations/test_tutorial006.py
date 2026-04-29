from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.path_operation_advanced_configuration.tutorial006_py310 import app

client = TestClient(app)


@test("POST /items/ reads the raw body without Pydantic parsing")
def post():
    response = client.post("/items/", content=b"this is actually not validated")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "size": 30,
            "content": {
                "name": "Maaaagic",
                "price": 42,
                "description": "Just kiddin', no magic here. ✨",
            },
        }
    )


@test("openapi_extra defines a custom requestBody schema")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
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
                                    "application/json": {
                                        "schema": {
                                            "required": ["name", "price"],
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"},
                                                "price": {"type": "number"},
                                                "description": {"type": "string"},
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
