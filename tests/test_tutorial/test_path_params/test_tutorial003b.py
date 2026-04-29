import asyncio

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.path_params.tutorial003b_py310 import app, read_users2

client = TestClient(app)


@test("GET /users/ lists users")
def get_users():
    response = client.get("/users")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(["Rick", "Morty"])


@test("read_users2 coroutine returns the expected list")
def read_users2_coverage():
    # Just for coverage.
    expect(asyncio.run(read_users2()), "read_users2 result").to_equal(
        ["Bean", "Elfo"]
    )


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
                    "/users": {
                        "get": {
                            "operationId": "read_users2_users_get",
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
                            "summary": "Read Users2",
                        },
                    },
                },
            }
        )
    )
