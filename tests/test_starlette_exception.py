from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from starlette.exceptions import HTTPException as StarletteHTTPException
from tryke import expect, test

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Some custom header"},
        )
    return {"item": items[item_id]}


@app.get("/http-no-body-statuscode-exception")
async def no_body_status_code_exception():
    raise HTTPException(status_code=204)


@app.get("/http-no-body-statuscode-with-detail-exception")
async def no_body_status_code_with_detail_exception():
    raise HTTPException(status_code=204, detail="I should just disappear!")


@app.get("/starlette-items/{item_id}")
async def read_starlette_item(item_id: str):
    if item_id not in items:
        raise StarletteHTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


client = TestClient(app)


@test("Existing item returns 200 with body")
def get_item():
    response = client.get("/items/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"item": "The Foo Wrestlers"})


@test("HTTPException with custom headers reaches the response")
def get_item_not_found():
    response = client.get("/items/bar")
    expect(response.status_code, "status code").to_equal(404).fatal()
    expect(response.headers.get("x-error"), "X-Error header").to_equal(
        "Some custom header"
    )
    expect(response.json(), "response body").to_equal({"detail": "Item not found"})


@test("Starlette HTTPException returns expected body")
def get_starlette_item():
    response = client.get("/starlette-items/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"item": "The Foo Wrestlers"})


@test("Starlette HTTPException returns 404 without custom headers")
def get_starlette_item_not_found():
    response = client.get("/starlette-items/bar")
    expect(response.status_code, "status code").to_equal(404).fatal()
    expect(response.headers.get("x-error"), "X-Error header").to_be_none()
    expect(response.json(), "response body").to_equal({"detail": "Item not found"})


@test("HTTPException with no-body status code returns empty body")
def no_body_status_code_exception_handlers():
    response = client.get("/http-no-body-statuscode-exception")
    expect(response.status_code, "status code").to_equal(204)
    expect(response.content, "response content").to_be_falsy()


@test("HTTPException with no-body status code drops the detail")
def no_body_status_code_with_detail_exception_handlers():
    response = client.get("/http-no-body-statuscode-with-detail-exception")
    expect(response.status_code, "status code").to_equal(204)
    expect(response.content, "response content").to_be_falsy()


@test("OpenAPI schema reflects starlette exception routes")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/http-no-body-statuscode-exception": {
                        "get": {
                            "operationId": "no_body_status_code_exception_http_no_body_statuscode_exception_get",
                            "responses": {
                                "200": {
                                    "content": {"application/json": {"schema": {}}},
                                    "description": "Successful Response",
                                }
                            },
                            "summary": "No Body Status Code Exception",
                        }
                    },
                    "/http-no-body-statuscode-with-detail-exception": {
                        "get": {
                            "operationId": "no_body_status_code_with_detail_exception_http_no_body_statuscode_with_detail_exception_get",
                            "responses": {
                                "200": {
                                    "content": {"application/json": {"schema": {}}},
                                    "description": "Successful Response",
                                }
                            },
                            "summary": "No Body Status Code With Detail Exception",
                        }
                    },
                    "/items/{item_id}": {
                        "get": {
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
                            "summary": "Read Item",
                            "operationId": "read_item_items__item_id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                }
                            ],
                        }
                    },
                    "/starlette-items/{item_id}": {
                        "get": {
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
                            "summary": "Read Starlette Item",
                            "operationId": "read_starlette_item_starlette_items__item_id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                }
                            ],
                        }
                    },
                },
                "components": {
                    "schemas": {
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
