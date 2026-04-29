"""
Regression test: Ensure app-level responses with Union models and content/examples
don't accumulate duplicate $ref entries in anyOf arrays.
See https://github.com/fastapi/fastapi/pull/14463
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import expect, test


class ModelA(BaseModel):
    a: str


class ModelB(BaseModel):
    b: str


app = FastAPI(
    responses={
        500: {
            "model": ModelA | ModelB,
            "content": {"application/json": {"examples": {"Case A": {"value": "a"}}}},
        }
    }
)


@app.get("/route1")
async def route1():
    pass  # pragma: no cover


@app.get("/route2")
async def route2():
    pass  # pragma: no cover


client = TestClient(app)


@test("OpenAPI Union responses don't duplicate $ref entries in anyOf")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/route1": {
                        "get": {
                            "summary": "Route1",
                            "operationId": "route1_route1_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "500": {
                                    "description": "Internal Server Error",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "anyOf": [
                                                    {
                                                        "$ref": "#/components/schemas/ModelA"
                                                    },
                                                    {
                                                        "$ref": "#/components/schemas/ModelB"
                                                    },
                                                ],
                                                "title": "Response 500 Route1 Route1 Get",
                                            },
                                            "examples": {"Case A": {"value": "a"}},
                                        }
                                    },
                                },
                            },
                        }
                    },
                    "/route2": {
                        "get": {
                            "summary": "Route2",
                            "operationId": "route2_route2_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "500": {
                                    "description": "Internal Server Error",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "anyOf": [
                                                    {
                                                        "$ref": "#/components/schemas/ModelA"
                                                    },
                                                    {
                                                        "$ref": "#/components/schemas/ModelB"
                                                    },
                                                ],
                                                "title": "Response 500 Route2 Route2 Get",
                                            },
                                            "examples": {"Case A": {"value": "a"}},
                                        }
                                    },
                                },
                            },
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "ModelA": {
                            "properties": {"a": {"type": "string", "title": "A"}},
                            "type": "object",
                            "required": ["a"],
                            "title": "ModelA",
                        },
                        "ModelB": {
                            "properties": {"b": {"type": "string", "title": "B"}},
                            "type": "object",
                            "required": ["b"],
                            "title": "ModelB",
                        },
                    }
                },
            }
        )
    )
