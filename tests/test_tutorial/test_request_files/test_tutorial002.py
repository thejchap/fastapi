from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial, tmp_path_ctx


def _app_for(name: str) -> FastAPI:
    mod = import_tutorial("request_files", name)
    return mod.app


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def post_form_no_body(name: str):
    client = TestClient(_app_for(name))
    response = client.post("/files/")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "files"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def post_body_json(name: str):
    client = TestClient(_app_for(name))
    response = client.post("/files/", json={"file": "Foo"})
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "files"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def post_files(name: str):
    app = _app_for(name)
    with tmp_path_ctx() as tmp_path:
        path = tmp_path / "test.txt"
        path.write_bytes(b"<file content>")
        path2 = tmp_path / "test2.txt"
        path2.write_bytes(b"<file content2>")

        client = TestClient(app)
        with path.open("rb") as file, path2.open("rb") as file2:
            response = client.post(
                "/files/",
                files=(
                    ("files", ("test.txt", file)),
                    ("files", ("test2.txt", file2)),
                ),
            )
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal({"file_sizes": [14, 15]})


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def post_upload_file(name: str):
    app = _app_for(name)
    with tmp_path_ctx() as tmp_path:
        path = tmp_path / "test.txt"
        path.write_bytes(b"<file content>")
        path2 = tmp_path / "test2.txt"
        path2.write_bytes(b"<file content2>")

        client = TestClient(app)
        with path.open("rb") as file, path2.open("rb") as file2:
            response = client.post(
                "/uploadfiles/",
                files=(
                    ("files", ("test.txt", file)),
                    ("files", ("test2.txt", file2)),
                ),
            )
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal({"filenames": ["test.txt", "test2.txt"]})


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def get_root(name: str):
    app = _app_for(name)
    client = TestClient(app)
    response = client.get("/")
    expect(response.status_code).to_equal(200).fatal()
    expect(b"<form" in response.content).to_be_truthy()


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def openapi_schema(name: str):
    client = TestClient(_app_for(name))
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/files/": {
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
                            "summary": "Create Files",
                            "operationId": "create_files_files__post",
                            "requestBody": {
                                "content": {
                                    "multipart/form-data": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_create_files_files__post"
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    },
                    "/uploadfiles/": {
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
                            "summary": "Create Upload Files",
                            "operationId": "create_upload_files_uploadfiles__post",
                            "requestBody": {
                                "content": {
                                    "multipart/form-data": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_create_upload_files_uploadfiles__post"
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    },
                    "/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Main",
                            "operationId": "main__get",
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "Body_create_upload_files_uploadfiles__post": {
                            "title": "Body_create_upload_files_uploadfiles__post",
                            "required": ["files"],
                            "type": "object",
                            "properties": {
                                "files": {
                                    "title": "Files",
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "contentMediaType": "application/octet-stream",
                                    },
                                }
                            },
                        },
                        "Body_create_files_files__post": {
                            "title": "Body_create_files_files__post",
                            "required": ["files"],
                            "type": "object",
                            "properties": {
                                "files": {
                                    "title": "Files",
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "contentMediaType": "application/octet-stream",
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
