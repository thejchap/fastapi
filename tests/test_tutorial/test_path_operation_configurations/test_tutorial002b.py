from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.path_operation_configuration.tutorial002b_py310 import app

client = TestClient(app)


@test
def get_items():
    response = client.get("/items/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(["Portal gun", "Plumbus"])


@test
def get_users():
    response = client.get("/users/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(["Rick", "Morty"])


@test
def openapi_schema():
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
