import asyncio

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.path_params.tutorial003b_py310 import app, read_users2

client = TestClient(app)


@test
def get_users():
    response = client.get("/users")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(["Rick", "Morty"])


@test
def read_users2_coverage():
    # Just for coverage.
    expect(asyncio.run(read_users2())).to_equal(["Bean", "Elfo"])


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
