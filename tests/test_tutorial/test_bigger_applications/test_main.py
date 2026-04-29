from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from docs_src.bigger_applications.app_an_py310.main import app


@fixture
def client() -> TestClient:
    return TestClient(app)


@test("GET /users with valid token returns user list")
def users_token_jessica(client: TestClient = Depends(client)):
    response = client.get("/users?token=jessica")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        [{"username": "Rick"}, {"username": "Morty"}]
    )


@test("GET /users without token returns validation error")
def users_with_no_token(client: TestClient = Depends(client)):
    response = client.get("/users")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("GET /users/foo with valid token returns the user")
def users_foo_token_jessica(client: TestClient = Depends(client)):
    response = client.get("/users/foo?token=jessica")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"username": "foo"})


@test("GET /users/foo without token returns validation error")
def users_foo_with_no_token(client: TestClient = Depends(client)):
    response = client.get("/users/foo")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("GET /users/me with valid token returns current user")
def users_me_token_jessica(client: TestClient = Depends(client)):
    response = client.get("/users/me?token=jessica")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"username": "fakecurrentuser"})


@test("GET /users/me without token returns validation error")
def users_me_with_no_token(client: TestClient = Depends(client)):
    response = client.get("/users/me")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("GET /users with non-jessica token rejects request")
def users_token_monica_with_no_jessica(client: TestClient = Depends(client)):
    response = client.get("/users?token=monica")
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal(
        {"detail": "No Jessica token provided"}
    )


@test("GET /items with valid token returns item dict")
def items_token_jessica(client: TestClient = Depends(client)):
    response = client.get(
        "/items?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "plumbus": {"name": "Plumbus"},
            "gun": {"name": "Portal Gun"},
        }
    )


@test("GET /items without query token returns validation error")
def items_with_no_token_jessica(client: TestClient = Depends(client)):
    response = client.get("/items", headers={"X-Token": "fake-super-secret-token"})
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("GET /items/plumbus with valid token returns the item")
def items_plumbus_token_jessica(client: TestClient = Depends(client)):
    response = client.get(
        "/items/plumbus?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"name": "Plumbus", "item_id": "plumbus"}
    )


@test("GET /items/bar with valid token returns 404")
def items_bar_token_jessica(client: TestClient = Depends(client)):
    response = client.get(
        "/items/bar?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    expect(response.status_code, "status code").to_equal(404).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Item not found"})


@test("GET /items/plumbus without query token returns validation error")
def items_plumbus_with_no_token(client: TestClient = Depends(client)):
    response = client.get(
        "/items/plumbus", headers={"X-Token": "fake-super-secret-token"}
    )
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("GET /items with invalid X-Token header rejects request")
def items_with_invalid_token(client: TestClient = Depends(client)):
    response = client.get("/items?token=jessica", headers={"X-Token": "invalid"})
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "X-Token header invalid"})


@test("GET /items/bar with invalid X-Token header rejects request")
def items_bar_with_invalid_token(client: TestClient = Depends(client)):
    response = client.get("/items/bar?token=jessica", headers={"X-Token": "invalid"})
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "X-Token header invalid"})


@test("GET /items without X-Token header returns validation error")
def items_with_missing_x_token_header(client: TestClient = Depends(client)):
    response = client.get("/items?token=jessica")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("GET /items/plumbus without X-Token header returns validation error")
def items_plumbus_with_missing_x_token_header(client: TestClient = Depends(client)):
    response = client.get("/items/plumbus?token=jessica")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("GET / with valid token returns greeting")
def root_token_jessica(client: TestClient = Depends(client)):
    response = client.get("/?token=jessica")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"message": "Hello Bigger Applications!"}
    )


@test("GET / without token returns validation error")
def root_with_no_token(client: TestClient = Depends(client)):
    response = client.get("/")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("PUT /items/foo without headers returns validation error")
def put_no_header(client: TestClient = Depends(client)):
    response = client.put("/items/foo")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "token"],
                    "msg": "Field required",
                    "input": None,
                },
                {
                    "type": "missing",
                    "loc": ["header", "x-token"],
                    "msg": "Field required",
                    "input": None,
                },
            ]
        }
    )


@test("PUT /items/foo with invalid X-Token rejects request")
def put_invalid_header(client: TestClient = Depends(client)):
    response = client.put("/items/foo", headers={"X-Token": "invalid"})
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "X-Token header invalid"})


@test("PUT /items/plumbus updates the item")
def put(client: TestClient = Depends(client)):
    response = client.put(
        "/items/plumbus?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"item_id": "plumbus", "name": "The great Plumbus"}
    )


@test("PUT /items/bar returns 403 forbidden")
def put_forbidden(client: TestClient = Depends(client)):
    response = client.put(
        "/items/bar?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    expect(response.status_code, "status code").to_equal(403).fatal()
    expect(response.json(), "response body").to_equal(
        {"detail": "You can only update the item: plumbus"}
    )


@test("POST /admin/ with valid headers returns greeting")
def admin(client: TestClient = Depends(client)):
    response = client.post(
        "/admin/?token=jessica", headers={"X-Token": "fake-super-secret-token"}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"message": "Admin getting schwifty"}
    )


@test("POST /admin/ with invalid X-Token rejects request")
def admin_invalid_header(client: TestClient = Depends(client)):
    response = client.post("/admin/", headers={"X-Token": "invalid"})
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "X-Token header invalid"})


@test("OpenAPI schema matches snapshot")
def openapi_schema(client: TestClient = Depends(client)):
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/users/": {
                        "get": {
                            "tags": ["users"],
                            "summary": "Read Users",
                            "operationId": "read_users_users__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Token", "type": "string"},
                                    "name": "token",
                                    "in": "query",
                                }
                            ],
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
                    "/users/me": {
                        "get": {
                            "tags": ["users"],
                            "summary": "Read User Me",
                            "operationId": "read_user_me_users_me_get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Token", "type": "string"},
                                    "name": "token",
                                    "in": "query",
                                }
                            ],
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
                    "/users/{username}": {
                        "get": {
                            "tags": ["users"],
                            "summary": "Read User",
                            "operationId": "read_user_users__username__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Username", "type": "string"},
                                    "name": "username",
                                    "in": "path",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "Token", "type": "string"},
                                    "name": "token",
                                    "in": "query",
                                },
                            ],
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
                    "/items/": {
                        "get": {
                            "tags": ["items"],
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Token", "type": "string"},
                                    "name": "token",
                                    "in": "query",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "X-Token", "type": "string"},
                                    "name": "x-token",
                                    "in": "header",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "404": {"description": "Not found"},
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
                    "/items/{item_id}": {
                        "get": {
                            "tags": ["items"],
                            "summary": "Read Item",
                            "operationId": "read_item_items__item_id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "Token", "type": "string"},
                                    "name": "token",
                                    "in": "query",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "X-Token", "type": "string"},
                                    "name": "x-token",
                                    "in": "header",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "404": {"description": "Not found"},
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
                        "put": {
                            "tags": ["items", "custom"],
                            "summary": "Update Item",
                            "operationId": "update_item_items__item_id__put",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "Token", "type": "string"},
                                    "name": "token",
                                    "in": "query",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "X-Token", "type": "string"},
                                    "name": "x-token",
                                    "in": "header",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "404": {"description": "Not found"},
                                "403": {"description": "Operation forbidden"},
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
                    "/admin/": {
                        "post": {
                            "tags": ["admin"],
                            "summary": "Update Admin",
                            "operationId": "update_admin_admin__post",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Token", "type": "string"},
                                    "name": "token",
                                    "in": "query",
                                },
                                {
                                    "required": True,
                                    "schema": {"title": "X-Token", "type": "string"},
                                    "name": "x-token",
                                    "in": "header",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "418": {"description": "I'm a teapot"},
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
                    "/": {
                        "get": {
                            "summary": "Root",
                            "operationId": "root__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Token", "type": "string"},
                                    "name": "token",
                                    "in": "query",
                                }
                            ],
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
