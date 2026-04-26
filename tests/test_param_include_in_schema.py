from fastapi import Cookie, FastAPI, Header, Path, Query
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()


@app.get("/hidden_cookie")
async def hidden_cookie(
    hidden_cookie: str | None = Cookie(default=None, include_in_schema=False),
):
    return {"hidden_cookie": hidden_cookie}


@app.get("/hidden_header")
async def hidden_header(
    hidden_header: str | None = Header(default=None, include_in_schema=False),
):
    return {"hidden_header": hidden_header}


@app.get("/hidden_path/{hidden_path}")
async def hidden_path(hidden_path: str = Path(include_in_schema=False)):
    return {"hidden_path": hidden_path}


@app.get("/hidden_query")
async def hidden_query(
    hidden_query: str | None = Query(default=None, include_in_schema=False),
):
    return {"hidden_query": hidden_query}


@test.cases(
    test.case("none", path="/hidden_cookie", cookies={}, expected_status=200, expected_response={"hidden_cookie": None}),
    test.case("set", path="/hidden_cookie", cookies={"hidden_cookie": "somevalue"}, expected_status=200, expected_response={"hidden_cookie": "somevalue"}),
)
def hidden_cookie(path: str, cookies: dict, expected_status: int, expected_response: dict):
    client = TestClient(app, cookies=cookies)
    response = client.get(path)
    expect(response.status_code).to_equal(expected_status).fatal()
    expect(response.json()).to_equal(expected_response)


@test.cases(
    test.case("none", path="/hidden_header", headers={}, expected_status=200, expected_response={"hidden_header": None}),
    test.case("set", path="/hidden_header", headers={"Hidden-Header": "somevalue"}, expected_status=200, expected_response={"hidden_header": "somevalue"}),
)
def hidden_header(path: str, headers: dict, expected_status: int, expected_response: dict):
    client = TestClient(app)
    response = client.get(path, headers=headers)
    expect(response.status_code).to_equal(expected_status).fatal()
    expect(response.json()).to_equal(expected_response)


@test
def hidden_path():
    client = TestClient(app)
    response = client.get("/hidden_path/hidden_path")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"hidden_path": "hidden_path"})


@test.cases(
    test.case("none", path="/hidden_query", expected_status=200, expected_response={"hidden_query": None}),
    test.case("set", path="/hidden_query?hidden_query=somevalue", expected_status=200, expected_response={"hidden_query": "somevalue"}),
)
def hidden_query(path: str, expected_status: int, expected_response: dict):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code).to_equal(expected_status).fatal()
    expect(response.json()).to_equal(expected_response)


@test
def openapi_schema():
    client = TestClient(app)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/hidden_cookie": {
                    "get": {
                        "summary": "Hidden Cookie",
                        "operationId": "hidden_cookie_hidden_cookie_get",
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
                "/hidden_header": {
                    "get": {
                        "summary": "Hidden Header",
                        "operationId": "hidden_header_hidden_header_get",
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
                "/hidden_path/{hidden_path}": {
                    "get": {
                        "summary": "Hidden Path",
                        "operationId": "hidden_path_hidden_path__hidden_path__get",
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
                "/hidden_query": {
                    "get": {
                        "summary": "Hidden Query",
                        "operationId": "hidden_query_hidden_query_get",
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
                    "ValidationError": {
                        "title": "ValidationError",
                        "required": ["loc", "msg", "type"],
                        "type": "object",
                        "properties": {
                            "loc": {
                                "title": "Location",
                                "type": "array",
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
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
    ))
