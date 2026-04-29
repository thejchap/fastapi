from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("dependencies", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial012_py310", name="tutorial012_py310"),
    test.case("tutorial012_an_py310", name="tutorial012_an_py310"),
)
def get_no_headers_items(name: str):
    client = _client_for(name)
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["header", "x-key"],
                    "msg": "Field required",
                    "input": None,
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial012_py310", name="tutorial012_py310"),
    test.case("tutorial012_an_py310", name="tutorial012_an_py310"),
)
def get_no_headers_users(name: str):
    client = _client_for(name)
    response = client.get("/users/")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["header", "x-key"],
                    "msg": "Field required",
                    "input": None,
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial012_py310", name="tutorial012_py310"),
    test.case("tutorial012_an_py310", name="tutorial012_an_py310"),
)
def get_invalid_one_header_items(name: str):
    client = _client_for(name)
    response = client.get("/items/", headers={"X-Token": "invalid"})
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "X-Token header invalid"})


@test.cases(
    test.case("tutorial012_py310", name="tutorial012_py310"),
    test.case("tutorial012_an_py310", name="tutorial012_an_py310"),
)
def get_invalid_one_users(name: str):
    client = _client_for(name)
    response = client.get("/users/", headers={"X-Token": "invalid"})
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "X-Token header invalid"})


@test.cases(
    test.case("tutorial012_py310", name="tutorial012_py310"),
    test.case("tutorial012_an_py310", name="tutorial012_an_py310"),
)
def get_invalid_second_header_items(name: str):
    client = _client_for(name)
    response = client.get(
        "/items/", headers={"X-Token": "fake-super-secret-token", "X-Key": "invalid"}
    )
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "X-Key header invalid"})


@test.cases(
    test.case("tutorial012_py310", name="tutorial012_py310"),
    test.case("tutorial012_an_py310", name="tutorial012_an_py310"),
)
def get_invalid_second_header_users(name: str):
    client = _client_for(name)
    response = client.get(
        "/users/", headers={"X-Token": "fake-super-secret-token", "X-Key": "invalid"}
    )
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "X-Key header invalid"})


@test.cases(
    test.case("tutorial012_py310", name="tutorial012_py310"),
    test.case("tutorial012_an_py310", name="tutorial012_an_py310"),
)
def get_valid_headers_items(name: str):
    client = _client_for(name)
    response = client.get(
        "/items/",
        headers={
            "X-Token": "fake-super-secret-token",
            "X-Key": "fake-super-secret-key",
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal([{"item": "Portal Gun"}, {"item": "Plumbus"}])


@test.cases(
    test.case("tutorial012_py310", name="tutorial012_py310"),
    test.case("tutorial012_an_py310", name="tutorial012_an_py310"),
)
def get_valid_headers_users(name: str):
    client = _client_for(name)
    response = client.get(
        "/users/",
        headers={
            "X-Token": "fake-super-secret-token",
            "X-Key": "fake-super-secret-key",
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal([{"username": "Rick"}, {"username": "Morty"}])


@test.cases(
    test.case("tutorial012_py310", name="tutorial012_py310"),
    test.case("tutorial012_an_py310", name="tutorial012_an_py310"),
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
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "X-Token", "type": "string"},
                                    "name": "x-token",
                                    "in": "header",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "X-Key", "type": "string"},
                                    "name": "x-key",
                                    "in": "header",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "422": {
                                    "description": "Validation Error",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError"
                                            }
                                        }
                                    },
                                },
                            },
                        }
                    },
                    "/users/": {
                        "get": {
                            "summary": "Read Users",
                            "operationId": "read_users_users__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "X-Token", "type": "string"},
                                    "name": "x-token",
                                    "in": "header",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "X-Key", "type": "string"},
                                    "name": "x-key",
                                    "in": "header",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "422": {
                                    "description": "Validation Error",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError"
                                            }
                                        }
                                    },
                                },
                            },
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "HTTPValidationError": {
                            "title": "HTTPValidationError",
                            "type": "object",
                            "properties": {
                                "detail": {
                                    "title": "Detail",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    },
                                }
                            },
                        },
                        "ValidationError": {
                            "title": "ValidationError",
                            "required": ["loc", "msg", "type"],
                            "type": "object",
                            "properties": {
                                "loc": {
                                    "title": "Location",
                                    "type": "array",
                                    "items": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "integer"},
                                        ]
                                    },
                                },
                                "msg": {"title": "Message", "type": "string"},
                                "type": {"title": "Error Type", "type": "string"},
                                "input": {"title": "Input"},
                                "ctx": {"title": "Context", "type": "object"},
                            },
                        },
                    }
                },
            }
        )
    )
