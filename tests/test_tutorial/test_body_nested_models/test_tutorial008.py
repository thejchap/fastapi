from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("body_nested_models", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial008_py310", name="tutorial008_py310"),
)
def post_body(name: str):
    client = _client_for(name)
    data = [
        {"url": "http://example.com/", "name": "Example"},
        {"url": "http://fastapi.tiangolo.com/", "name": "FastAPI"},
    ]
    response = client.post("/images/multiple", json=data)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(data)


@test.cases(
    test.case("tutorial008_py310", name="tutorial008_py310"),
)
def post_invalid_list_item(name: str):
    client = _client_for(name)
    data = [{"url": "not a valid url", "name": "Example"}]
    response = client.post("/images/multiple", json=data)
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "loc": ["body", 0, "url"],
                    "input": "not a valid url",
                    "msg": "Input should be a valid URL, relative URL without a base",
                    "type": "url_parsing",
                    "ctx": {"error": "relative URL without a base"},
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial008_py310", name="tutorial008_py310"),
)
def post_not_a_list(name: str):
    client = _client_for(name)
    data = {"url": "http://example.com/", "name": "Example"}
    response = client.post("/images/multiple", json=data)
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "loc": ["body"],
                    "input": {
                        "name": "Example",
                        "url": "http://example.com/",
                    },
                    "msg": "Input should be a valid list",
                    "type": "list_type",
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial008_py310", name="tutorial008_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/images/multiple/": {
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
                            "summary": "Create Multiple Images",
                            "operationId": "create_multiple_images_images_multiple__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "title": "Images",
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Image"
                                            },
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "Image": {
                            "properties": {
                                "url": {
                                    "title": "Url",
                                    "type": "string",
                                    "format": "uri",
                                    "maxLength": 2083,
                                    "minLength": 1,
                                },
                                "name": {
                                    "title": "Name",
                                    "type": "string",
                                },
                            },
                            "required": ["url", "name"],
                            "title": "Image",
                            "type": "object",
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
