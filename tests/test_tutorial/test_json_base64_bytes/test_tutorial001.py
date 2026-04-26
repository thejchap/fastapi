from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("json_base64_bytes", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def post_data(name: str):
    client = _client_for(name)
    response = client.post(
        "/data",
        json={
            "description": "A file",
            "data": "SGVsbG8sIFdvcmxkIQ==",
        },
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {"description": "A file", "content": "Hello, World!"}
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def get_data(name: str):
    client = _client_for(name)
    response = client.get("/data")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"description": "A plumbus", "data": "aGVsbG8="})


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def post_data_in_out(name: str):
    client = _client_for(name)
    response = client.post(
        "/data-in-out",
        json={
            "description": "A plumbus",
            "data": "SGVsbG8sIFdvcmxkIQ==",
        },
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "description": "A plumbus",
            "data": "SGVsbG8sIFdvcmxkIQ==",
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/data": {
                        "get": {
                            "summary": "Get Data",
                            "operationId": "get_data_data_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/DataOutput"
                                            }
                                        }
                                    },
                                }
                            },
                        },
                        "post": {
                            "summary": "Post Data",
                            "operationId": "post_data_data_post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/DataInput"
                                        }
                                    }
                                },
                                "required": True,
                            },
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
                        },
                    },
                    "/data-in-out": {
                        "post": {
                            "summary": "Post Data In Out",
                            "operationId": "post_data_in_out_data_in_out_post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/DataInputOutput"
                                        }
                                    }
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/DataInputOutput"
                                            }
                                        }
                                    },
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
                        "DataInput": {
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "title": "Description",
                                },
                                "data": {
                                    "type": "string",
                                    "contentEncoding": "base64",
                                    "contentMediaType": "application/octet-stream",
                                    "title": "Data",
                                },
                            },
                            "type": "object",
                            "required": ["description", "data"],
                            "title": "DataInput",
                        },
                        "DataInputOutput": {
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "title": "Description",
                                },
                                "data": {
                                    "type": "string",
                                    "contentEncoding": "base64",
                                    "contentMediaType": "application/octet-stream",
                                    "title": "Data",
                                },
                            },
                            "type": "object",
                            "required": ["description", "data"],
                            "title": "DataInputOutput",
                        },
                        "DataOutput": {
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "title": "Description",
                                },
                                "data": {
                                    "type": "string",
                                    "contentEncoding": "base64",
                                    "contentMediaType": "application/octet-stream",
                                    "title": "Data",
                                },
                            },
                            "type": "object",
                            "required": ["description", "data"],
                            "title": "DataOutput",
                        },
                        "HTTPValidationError": {
                            "properties": {
                                "detail": {
                                    "items": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    },
                                    "type": "array",
                                    "title": "Detail",
                                }
                            },
                            "type": "object",
                            "title": "HTTPValidationError",
                        },
                        "ValidationError": {
                            "properties": {
                                "ctx": {"title": "Context", "type": "object"},
                                "input": {"title": "Input"},
                                "loc": {
                                    "items": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "integer"},
                                        ]
                                    },
                                    "type": "array",
                                    "title": "Location",
                                },
                                "msg": {"type": "string", "title": "Message"},
                                "type": {"type": "string", "title": "Error Type"},
                            },
                            "type": "object",
                            "required": ["loc", "msg", "type"],
                            "title": "ValidationError",
                        },
                    }
                },
            }
        )
    )
