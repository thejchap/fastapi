from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.sub_applications.tutorial001_py310 import app

client = TestClient(app)


@test
def main():
    response = client.get("/app")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"message": "Hello World from main app"})


@test
def sub():
    response = client.get("/subapi/sub")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"message": "Hello World from sub API"})


@test
def openapi_schema_main():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/app": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Read Main",
                            "operationId": "read_main_app_get",
                        }
                    }
                },
            }
        )
    )


@test
def openapi_schema_sub():
    response = client.get("/subapi/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/sub": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Read Sub",
                            "operationId": "read_sub_sub_get",
                        }
                    }
                },
                "servers": [{"url": "/subapi"}],
            }
        )
    )
