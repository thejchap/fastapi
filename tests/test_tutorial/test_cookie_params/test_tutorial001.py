from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str, cookies: dict | None = None) -> TestClient:
    mod = import_tutorial("cookie_params", name)
    return TestClient(mod.app, cookies=cookies)


@test.cases(
    test.case(
        "py310 no cookies",
        mod_name="tutorial001_py310",
        path="/items",
        cookies=None,
        expected_status=200,
        expected_response={"ads_id": None},
    ),
    test.case(
        "py310 ads_id only",
        mod_name="tutorial001_py310",
        path="/items",
        cookies={"ads_id": "ads_track"},
        expected_status=200,
        expected_response={"ads_id": "ads_track"},
    ),
    test.case(
        "py310 both cookies",
        mod_name="tutorial001_py310",
        path="/items",
        cookies={"ads_id": "ads_track", "session": "cookiesession"},
        expected_status=200,
        expected_response={"ads_id": "ads_track"},
    ),
    test.case(
        "py310 session only",
        mod_name="tutorial001_py310",
        path="/items",
        cookies={"session": "cookiesession"},
        expected_status=200,
        expected_response={"ads_id": None},
    ),
    test.case(
        "an_py310 no cookies",
        mod_name="tutorial001_an_py310",
        path="/items",
        cookies=None,
        expected_status=200,
        expected_response={"ads_id": None},
    ),
    test.case(
        "an_py310 ads_id only",
        mod_name="tutorial001_an_py310",
        path="/items",
        cookies={"ads_id": "ads_track"},
        expected_status=200,
        expected_response={"ads_id": "ads_track"},
    ),
    test.case(
        "an_py310 both cookies",
        mod_name="tutorial001_an_py310",
        path="/items",
        cookies={"ads_id": "ads_track", "session": "cookiesession"},
        expected_status=200,
        expected_response={"ads_id": "ads_track"},
    ),
    test.case(
        "an_py310 session only",
        mod_name="tutorial001_an_py310",
        path="/items",
        cookies={"session": "cookiesession"},
        expected_status=200,
        expected_response={"ads_id": None},
    ),
)
def items(
    mod_name: str,
    path: str,
    cookies: dict | None,
    expected_status: int,
    expected_response: dict,
):
    client = _client_for(mod_name, cookies=cookies)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(expected_status)
    expect(response.json(), "response body").to_equal(expected_response)


@test.cases(
    test.case("tutorial001_py310", mod_name="tutorial001_py310"),
    test.case("tutorial001_an_py310", mod_name="tutorial001_an_py310"),
)
def openapi_schema(mod_name: str):
    client = _client_for(mod_name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/": {
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
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Ads Id",
                                    },
                                    "name": "ads_id",
                                    "in": "cookie",
                                }
                            ],
                        }
                    }
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
