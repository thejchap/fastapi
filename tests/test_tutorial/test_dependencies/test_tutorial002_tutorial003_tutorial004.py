from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("dependencies", name)
    client = TestClient(mod.app)
    return client


_ITEMS_FULL = {
    "items": [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
}
_GET_PATH_CASES: list[tuple[str, int, dict]] = [
    ("/items", 200, _ITEMS_FULL),
    ("/items?q=foo", 200, {**_ITEMS_FULL, "q": "foo"}),
    (
        "/items?q=foo&skip=1",
        200,
        {"items": [{"item_name": "Bar"}, {"item_name": "Baz"}], "q": "foo"},
    ),
    (
        "/items?q=bar&limit=2",
        200,
        {"items": [{"item_name": "Foo"}, {"item_name": "Bar"}], "q": "bar"},
    ),
    ("/items?q=bar&skip=1&limit=1", 200, {"items": [{"item_name": "Bar"}], "q": "bar"}),
    ("/items?limit=1&q=bar&skip=1", 200, {"items": [{"item_name": "Bar"}], "q": "bar"}),
]
_GET_NAMES = [
    "tutorial002_py310",
    "tutorial002_an_py310",
    "tutorial003_py310",
    "tutorial003_an_py310",
    "tutorial004_py310",
    "tutorial004_an_py310",
]


@test.cases(
    test.case(
        "tutorial002_py310 /items",
        name="tutorial002_py310",
        path="/items",
        expected_status=200,
        expected_response=_GET_PATH_CASES[0][2],
    ),
    test.case(
        "tutorial002_py310 /items?q=foo",
        name="tutorial002_py310",
        path="/items?q=foo",
        expected_status=200,
        expected_response=_GET_PATH_CASES[1][2],
    ),
    test.case(
        "tutorial002_py310 /items?q=foo&skip=1",
        name="tutorial002_py310",
        path="/items?q=foo&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[2][2],
    ),
    test.case(
        "tutorial002_py310 /items?q=bar&limit=2",
        name="tutorial002_py310",
        path="/items?q=bar&limit=2",
        expected_status=200,
        expected_response=_GET_PATH_CASES[3][2],
    ),
    test.case(
        "tutorial002_py310 /items?q=bar&skip=1&limit=1",
        name="tutorial002_py310",
        path="/items?q=bar&skip=1&limit=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[4][2],
    ),
    test.case(
        "tutorial002_py310 /items?limit=1&q=bar&skip=1",
        name="tutorial002_py310",
        path="/items?limit=1&q=bar&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[5][2],
    ),
    test.case(
        "tutorial002_an_py310 /items",
        name="tutorial002_an_py310",
        path="/items",
        expected_status=200,
        expected_response=_GET_PATH_CASES[0][2],
    ),
    test.case(
        "tutorial002_an_py310 /items?q=foo",
        name="tutorial002_an_py310",
        path="/items?q=foo",
        expected_status=200,
        expected_response=_GET_PATH_CASES[1][2],
    ),
    test.case(
        "tutorial002_an_py310 /items?q=foo&skip=1",
        name="tutorial002_an_py310",
        path="/items?q=foo&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[2][2],
    ),
    test.case(
        "tutorial002_an_py310 /items?q=bar&limit=2",
        name="tutorial002_an_py310",
        path="/items?q=bar&limit=2",
        expected_status=200,
        expected_response=_GET_PATH_CASES[3][2],
    ),
    test.case(
        "tutorial002_an_py310 /items?q=bar&skip=1&limit=1",
        name="tutorial002_an_py310",
        path="/items?q=bar&skip=1&limit=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[4][2],
    ),
    test.case(
        "tutorial002_an_py310 /items?limit=1&q=bar&skip=1",
        name="tutorial002_an_py310",
        path="/items?limit=1&q=bar&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[5][2],
    ),
    test.case(
        "tutorial003_py310 /items",
        name="tutorial003_py310",
        path="/items",
        expected_status=200,
        expected_response=_GET_PATH_CASES[0][2],
    ),
    test.case(
        "tutorial003_py310 /items?q=foo",
        name="tutorial003_py310",
        path="/items?q=foo",
        expected_status=200,
        expected_response=_GET_PATH_CASES[1][2],
    ),
    test.case(
        "tutorial003_py310 /items?q=foo&skip=1",
        name="tutorial003_py310",
        path="/items?q=foo&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[2][2],
    ),
    test.case(
        "tutorial003_py310 /items?q=bar&limit=2",
        name="tutorial003_py310",
        path="/items?q=bar&limit=2",
        expected_status=200,
        expected_response=_GET_PATH_CASES[3][2],
    ),
    test.case(
        "tutorial003_py310 /items?q=bar&skip=1&limit=1",
        name="tutorial003_py310",
        path="/items?q=bar&skip=1&limit=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[4][2],
    ),
    test.case(
        "tutorial003_py310 /items?limit=1&q=bar&skip=1",
        name="tutorial003_py310",
        path="/items?limit=1&q=bar&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[5][2],
    ),
    test.case(
        "tutorial003_an_py310 /items",
        name="tutorial003_an_py310",
        path="/items",
        expected_status=200,
        expected_response=_GET_PATH_CASES[0][2],
    ),
    test.case(
        "tutorial003_an_py310 /items?q=foo",
        name="tutorial003_an_py310",
        path="/items?q=foo",
        expected_status=200,
        expected_response=_GET_PATH_CASES[1][2],
    ),
    test.case(
        "tutorial003_an_py310 /items?q=foo&skip=1",
        name="tutorial003_an_py310",
        path="/items?q=foo&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[2][2],
    ),
    test.case(
        "tutorial003_an_py310 /items?q=bar&limit=2",
        name="tutorial003_an_py310",
        path="/items?q=bar&limit=2",
        expected_status=200,
        expected_response=_GET_PATH_CASES[3][2],
    ),
    test.case(
        "tutorial003_an_py310 /items?q=bar&skip=1&limit=1",
        name="tutorial003_an_py310",
        path="/items?q=bar&skip=1&limit=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[4][2],
    ),
    test.case(
        "tutorial003_an_py310 /items?limit=1&q=bar&skip=1",
        name="tutorial003_an_py310",
        path="/items?limit=1&q=bar&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[5][2],
    ),
    test.case(
        "tutorial004_py310 /items",
        name="tutorial004_py310",
        path="/items",
        expected_status=200,
        expected_response=_GET_PATH_CASES[0][2],
    ),
    test.case(
        "tutorial004_py310 /items?q=foo",
        name="tutorial004_py310",
        path="/items?q=foo",
        expected_status=200,
        expected_response=_GET_PATH_CASES[1][2],
    ),
    test.case(
        "tutorial004_py310 /items?q=foo&skip=1",
        name="tutorial004_py310",
        path="/items?q=foo&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[2][2],
    ),
    test.case(
        "tutorial004_py310 /items?q=bar&limit=2",
        name="tutorial004_py310",
        path="/items?q=bar&limit=2",
        expected_status=200,
        expected_response=_GET_PATH_CASES[3][2],
    ),
    test.case(
        "tutorial004_py310 /items?q=bar&skip=1&limit=1",
        name="tutorial004_py310",
        path="/items?q=bar&skip=1&limit=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[4][2],
    ),
    test.case(
        "tutorial004_py310 /items?limit=1&q=bar&skip=1",
        name="tutorial004_py310",
        path="/items?limit=1&q=bar&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[5][2],
    ),
    test.case(
        "tutorial004_an_py310 /items",
        name="tutorial004_an_py310",
        path="/items",
        expected_status=200,
        expected_response=_GET_PATH_CASES[0][2],
    ),
    test.case(
        "tutorial004_an_py310 /items?q=foo",
        name="tutorial004_an_py310",
        path="/items?q=foo",
        expected_status=200,
        expected_response=_GET_PATH_CASES[1][2],
    ),
    test.case(
        "tutorial004_an_py310 /items?q=foo&skip=1",
        name="tutorial004_an_py310",
        path="/items?q=foo&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[2][2],
    ),
    test.case(
        "tutorial004_an_py310 /items?q=bar&limit=2",
        name="tutorial004_an_py310",
        path="/items?q=bar&limit=2",
        expected_status=200,
        expected_response=_GET_PATH_CASES[3][2],
    ),
    test.case(
        "tutorial004_an_py310 /items?q=bar&skip=1&limit=1",
        name="tutorial004_an_py310",
        path="/items?q=bar&skip=1&limit=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[4][2],
    ),
    test.case(
        "tutorial004_an_py310 /items?limit=1&q=bar&skip=1",
        name="tutorial004_an_py310",
        path="/items?limit=1&q=bar&skip=1",
        expected_status=200,
        expected_response=_GET_PATH_CASES[5][2],
    ),
)
def get(name: str, path: str, expected_status: int, expected_response: dict):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(expected_status)
    expect(response.json(), "response body").to_equal(expected_response)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
    test.case("tutorial004_py310", name="tutorial004_py310"),
    test.case("tutorial004_an_py310", name="tutorial004_an_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
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
                                        "title": "Q",
                                    },
                                    "name": "q",
                                    "in": "query",
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "Skip",
                                        "type": "integer",
                                        "default": 0,
                                    },
                                    "name": "skip",
                                    "in": "query",
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "Limit",
                                        "type": "integer",
                                        "default": 100,
                                    },
                                    "name": "limit",
                                    "in": "query",
                                },
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
