from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.path_operation_configuration.tutorial002b_py310 import app

client = TestClient(app)


@test("GET /items/ lists items")
def get_items():
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(["Portal gun", "Plumbus"])


@test("GET /users/ lists users")
def get_users():
    response = client.get("/users/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(["Rick", "Morty"])


@test("OpenAPI schema matches the snapshot")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/": {
                        "get": {
                            "tags": ["items"],
                            "summary": "Get Items",
                            "operationId": "get_items_items__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        }
                    },
                    "/users/": {
                        "get": {
                            "tags": ["users"],
                            "summary": "Read Users",
                            "operationId": "read_users_users__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        }
                    },
                },
            }
        )
    )
