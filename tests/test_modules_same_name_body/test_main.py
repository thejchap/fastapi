from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from .app.main import app

client = TestClient(app)


@test.cases(
    test.case("a-compute", path="/a/compute"),
    test.case("a-compute-slash", path="/a/compute/"),
    test.case("b-compute", path="/b/compute"),
    test.case("b-compute-slash", path="/b/compute/"),
)
def post(path: str):
    data = {"a": 2, "b": "foo"}
    response = client.post(path, json=data)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(data)


@test.cases(
    test.case("a-compute", path="/a/compute"),
    test.case("a-compute-slash", path="/a/compute/"),
    test.case("b-compute", path="/b/compute"),
    test.case("b-compute-slash", path="/b/compute/"),
)
def post_invalid(path: str):
    data = {"a": "bar", "b": "foo"}
    response = client.post(path, json=data)
    expect(response.status_code, "status code").to_equal(422)


@test("Same-named body modules produce a complete OpenAPI schema")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/a/compute": {
                        "post": {
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
                            "summary": "Compute",
                            "operationId": "compute_a_compute_post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_compute_a_compute_post"
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    },
                    "/b/compute/": {
                        "post": {
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
                            "summary": "Compute",
                            "operationId": "compute_b_compute__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_compute_b_compute__post"
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "Body_compute_b_compute__post": {
                            "title": "Body_compute_b_compute__post",
                            "required": ["a", "b"],
                            "type": "object",
                            "properties": {
                                "a": {"title": "A", "type": "integer"},
                                "b": {"title": "B", "type": "string"},
                            },
                        },
                        "Body_compute_a_compute_post": {
                            "title": "Body_compute_a_compute_post",
                            "required": ["a", "b"],
                            "type": "object",
                            "properties": {
                                "a": {"title": "A", "type": "integer"},
                                "b": {"title": "B", "type": "string"},
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
                    }
                },
            }
        )
    )
