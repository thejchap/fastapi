from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()

client = TestClient(app)


class Item(BaseModel):
    data: str


def duplicate_dependency(item: Item):
    return item


def dependency(item2: Item):
    return item2


def sub_duplicate_dependency(
    item: Item, sub_item: Item = Depends(duplicate_dependency)
):
    return [item, sub_item]


@app.post("/with-duplicates")
async def with_duplicates(item: Item, item2: Item = Depends(duplicate_dependency)):
    return [item, item2]


@app.post("/no-duplicates")
async def no_duplicates(item: Item, item2: Item = Depends(dependency)):
    return [item, item2]


@app.post("/with-duplicates-sub")
async def no_duplicates_sub(
    item: Item, sub_items: list[Item] = Depends(sub_duplicate_dependency)
):
    return [item, sub_items]


@test("missing item2 returns 422 when dependency uses distinct name")
def no_duplicates_invalid():
    response = client.post("/no-duplicates", json={"item": {"data": "myitem"}})
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "item2"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("distinct body fields are accepted on /no-duplicates")
def no_duplicates():
    response = client.post(
        "/no-duplicates",
        json={"item": {"data": "myitem"}, "item2": {"data": "myitem2"}},
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        [{"data": "myitem"}, {"data": "myitem2"}]
    )


@test("duplicate dependency type collapses into a single body field")
def duplicates():
    response = client.post("/with-duplicates", json={"data": "myitem"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        [{"data": "myitem"}, {"data": "myitem"}]
    )


@test("transitive duplicate dependencies collapse into a single body field")
def sub_duplicates():
    response = client.post("/with-duplicates-sub", json={"data": "myitem"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        [
            {"data": "myitem"},
            [{"data": "myitem"}, {"data": "myitem"}],
        ]
    )


@test("OpenAPI schema collapses duplicate dependencies appropriately")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/with-duplicates": {
                        "post": {
                            "summary": "With Duplicates",
                            "operationId": "with_duplicates_with_duplicates_post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
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
                        }
                    },
                    "/no-duplicates": {
                        "post": {
                            "summary": "No Duplicates",
                            "operationId": "no_duplicates_no_duplicates_post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_no_duplicates_no_duplicates_post"
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
                        }
                    },
                    "/with-duplicates-sub": {
                        "post": {
                            "summary": "No Duplicates Sub",
                            "operationId": "no_duplicates_sub_with_duplicates_sub_post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
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
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "Body_no_duplicates_no_duplicates_post": {
                            "title": "Body_no_duplicates_no_duplicates_post",
                            "required": ["item", "item2"],
                            "type": "object",
                            "properties": {
                                "item": {"$ref": "#/components/schemas/Item"},
                                "item2": {"$ref": "#/components/schemas/Item"},
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
                        "Item": {
                            "title": "Item",
                            "required": ["data"],
                            "type": "object",
                            "properties": {"data": {"title": "Data", "type": "string"}},
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
                    }
                },
            }
        )
    )
