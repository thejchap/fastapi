from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.path_operation_configuration.tutorial006_py310 import app

client = TestClient(app)


@test.cases(
    test.case(
        "items",
        path="/items/",
        expected_status=200,
        expected_response=[{"name": "Foo", "price": 42}],
    ),
    test.case(
        "users",
        path="/users/",
        expected_status=200,
        expected_response=[{"username": "johndoe"}],
    ),
    test.case(
        "elements",
        path="/elements/",
        expected_status=200,
        expected_response=[{"item_id": "Foo"}],
    ),
)
def query_params_str_validations(
    path: str, expected_status: int, expected_response: list
):
    response = client.get(path)
    expect(response.status_code).to_equal(expected_status).fatal()
    expect(response.json()).to_equal(expected_response)


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
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "tags": ["items"],
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                        }
                    },
                    "/users/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "tags": ["users"],
                            "summary": "Read Users",
                            "operationId": "read_users_users__get",
                        }
                    },
                    "/elements/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "tags": ["items"],
                            "summary": "Read Elements",
                            "operationId": "read_elements_elements__get",
                            "deprecated": True,
                        }
                    },
                },
            }
        )
    )
