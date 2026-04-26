from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.custom_response.tutorial005_py310 import app

client = TestClient(app)


@test
def get():
    response = client.get("/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.text).to_equal("Hello World")


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
                    "/": {
                        "get": {
                            "summary": "Main",
                            "operationId": "main__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "text/plain": {"schema": {"type": "string"}}
                                    },
                                }
                            },
                        }
                    }
                },
            }
        )
    )
