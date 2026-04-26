from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.response_model.tutorial003_03_py310 import app

client = TestClient(app)


@test
def get_portal():
    response = client.get("/teleport", follow_redirects=False)
    expect(response.status_code).to_equal(307).fatal()
    expect(response.headers["location"]).to_equal(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )


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
                    "/teleport": {
                        "get": {
                            "summary": "Get Teleport",
                            "operationId": "get_teleport_teleport_get",
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
