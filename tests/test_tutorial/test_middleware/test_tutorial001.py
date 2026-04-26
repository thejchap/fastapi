from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.middleware.tutorial001_py310 import app

client = TestClient(app)


@test
def response_headers():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.headers).to_contain("X-Process-Time")


@test
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {
                    "title": "FastAPI",
                    "version": "0.1.0",
                },
                "paths": {},
            }
        )
    )
