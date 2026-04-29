import importlib
import warnings
from contextlib import contextmanager

from dirty_equals import IsInt
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from sqlalchemy import StaticPool
from sqlmodel import SQLModel, create_engine
from sqlmodel.main import default_registry
from tryke import expect, test

from ..._shims import import_tutorial


def clear_sqlmodel():
    # Clear the tables in the metadata for the default base model.
    SQLModel.metadata.clear()
    # Clear the Models associated with the registry, to avoid warnings.
    default_registry.dispose()


@contextmanager
def _client_for(name: str):
    clear_sqlmodel()
    # TODO: remove when updating SQL tutorial to use new lifespan API.
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        mod = import_tutorial("sql_databases", name)
        clear_sqlmodel()
        importlib.reload(mod)
    mod.sqlite_url = "sqlite://"
    mod.engine = create_engine(
        mod.sqlite_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    with TestClient(mod.app) as c:
        try:
            yield c
        finally:
            mod.engine.dispose()


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def crud_app(name: str):
    with _client_for(name) as client:
        # TODO: this warns that SQLModel.from_orm is deprecated in Pydantic v1, refactor
        # this if using obj.model_validate becomes independent of Pydantic v2.
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            # No heroes before creating.
            response = client.get("heroes/")
            expect(response.status_code, "status code").to_equal(200).fatal()
            expect(response.json(), "initial heroes list").to_equal([])

            # Create a hero.
            response = client.post(
                "/heroes/",
                json={
                    "id": 999,
                    "name": "Dead Pond",
                    "age": 30,
                    "secret_name": "Dive Wilson",
                },
            )
            expect(response.status_code, "status code").to_equal(200).fatal()
            expect(response.json(), "created hero").to_equal(
                snapshot(
                    {
                        "age": 30,
                        "secret_name": "Dive Wilson",
                        "id": 999,
                        "name": "Dead Pond",
                    }
                )
            )

            # Read a hero.
            hero_id = response.json()["id"]
            response = client.get(f"/heroes/{hero_id}")
            expect(response.status_code, "status code").to_equal(200).fatal()
            expect(response.json(), "fetched hero").to_equal(
                snapshot(
                    {
                        "name": "Dead Pond",
                        "age": 30,
                        "id": 999,
                        "secret_name": "Dive Wilson",
                    }
                )
            )

            # Read all heroes — create more first.
            response = client.post(
                "/heroes/",
                json={
                    "name": "Spider-Boy",
                    "age": 18,
                    "secret_name": "Pedro Parqueador",
                },
            )
            expect(response.status_code, "status code").to_equal(200).fatal()
            response = client.post(
                "/heroes/", json={"name": "Rusty-Man", "secret_name": "Tommy Sharp"}
            )
            expect(response.status_code, "status code").to_equal(200).fatal()

            response = client.get("/heroes/")
            expect(response.status_code, "status code").to_equal(200).fatal()
            expect(response.json(), "all heroes").to_equal(
                snapshot(
                    [
                        {
                            "name": "Dead Pond",
                            "age": 30,
                            "id": IsInt(),
                            "secret_name": "Dive Wilson",
                        },
                        {
                            "name": "Spider-Boy",
                            "age": 18,
                            "id": IsInt(),
                            "secret_name": "Pedro Parqueador",
                        },
                        {
                            "name": "Rusty-Man",
                            "age": None,
                            "id": IsInt(),
                            "secret_name": "Tommy Sharp",
                        },
                    ]
                )
            )

            response = client.get("/heroes/?offset=1&limit=1")
            expect(response.status_code, "status code").to_equal(200).fatal()
            expect(response.json(), "paged heroes").to_equal(
                snapshot(
                    [
                        {
                            "name": "Spider-Boy",
                            "age": 18,
                            "id": IsInt(),
                            "secret_name": "Pedro Parqueador",
                        }
                    ]
                )
            )

            # Delete a hero.
            response = client.delete(f"/heroes/{hero_id}")
            expect(response.status_code, "status code").to_equal(200).fatal()
            expect(response.json(), "delete response").to_equal(snapshot({"ok": True}))

            response = client.get(f"/heroes/{hero_id}")
            expect(response.status_code, "status code").to_equal(404).fatal()

            response = client.delete(f"/heroes/{hero_id}")
            expect(response.status_code, "status code").to_equal(404).fatal()
            expect(response.json(), "not found body").to_equal(
                snapshot({"detail": "Hero not found"})
            )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def openapi_schema(name: str):
    with _client_for(name) as client:
        response = client.get("/openapi.json")
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json(), "OpenAPI schema").to_equal(
            snapshot(
                {
                    "openapi": "3.1.0",
                    "info": {"title": "FastAPI", "version": "0.1.0"},
                    "paths": {
                        "/heroes/": {
                            "post": {
                                "summary": "Create Hero",
                                "operationId": "create_hero_heroes__post",
                                "requestBody": {
                                    "required": True,
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Hero"
                                            }
                                        }
                                    },
                                },
                                "responses": {
                                    "200": {
                                        "description": "Successful Response",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "$ref": "#/components/schemas/Hero"
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
                            },
                            "get": {
                                "summary": "Read Heroes",
                                "operationId": "read_heroes_heroes__get",
                                "parameters": [
                                    {
                                        "name": "offset",
                                        "in": "query",
                                        "required": False,
                                        "schema": {
                                            "type": "integer",
                                            "default": 0,
                                            "title": "Offset",
                                        },
                                    },
                                    {
                                        "name": "limit",
                                        "in": "query",
                                        "required": False,
                                        "schema": {
                                            "type": "integer",
                                            "maximum": 100,
                                            "default": 100,
                                            "title": "Limit",
                                        },
                                    },
                                ],
                                "responses": {
                                    "200": {
                                        "description": "Successful Response",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "type": "array",
                                                    "items": {
                                                        "$ref": "#/components/schemas/Hero"
                                                    },
                                                    "title": "Response Read Heroes Heroes  Get",
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
                            },
                        },
                        "/heroes/{hero_id}": {
                            "get": {
                                "summary": "Read Hero",
                                "operationId": "read_hero_heroes__hero_id__get",
                                "parameters": [
                                    {
                                        "name": "hero_id",
                                        "in": "path",
                                        "required": True,
                                        "schema": {
                                            "type": "integer",
                                            "title": "Hero Id",
                                        },
                                    }
                                ],
                                "responses": {
                                    "200": {
                                        "description": "Successful Response",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "$ref": "#/components/schemas/Hero"
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
                            },
                            "delete": {
                                "summary": "Delete Hero",
                                "operationId": "delete_hero_heroes__hero_id__delete",
                                "parameters": [
                                    {
                                        "name": "hero_id",
                                        "in": "path",
                                        "required": True,
                                        "schema": {
                                            "type": "integer",
                                            "title": "Hero Id",
                                        },
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
                            },
                        },
                    },
                    "components": {
                        "schemas": {
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
                            "Hero": {
                                "properties": {
                                    "id": {
                                        "anyOf": [
                                            {"type": "integer"},
                                            {"type": "null"},
                                        ],
                                        "title": "Id",
                                    },
                                    "name": {"type": "string", "title": "Name"},
                                    "age": {
                                        "anyOf": [
                                            {"type": "integer"},
                                            {"type": "null"},
                                        ],
                                        "title": "Age",
                                    },
                                    "secret_name": {
                                        "type": "string",
                                        "title": "Secret Name",
                                    },
                                },
                                "type": "object",
                                "required": ["name", "secret_name"],
                                "title": "Hero",
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
