from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial, tmp_path_ctx


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("request_files", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_02_py310", name="tutorial001_02_py310"),
    test.case("tutorial001_02_an_py310", name="tutorial001_02_an_py310"),
)
def post_form_no_body(name: str):
    client = _client_for(name)
    response = client.post("/files/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "No file sent"})


@test.cases(
    test.case("tutorial001_02_py310", name="tutorial001_02_py310"),
    test.case("tutorial001_02_an_py310", name="tutorial001_02_an_py310"),
)
def post_uploadfile_no_body(name: str):
    client = _client_for(name)
    response = client.post("/uploadfile/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "No upload file sent"})


@test.cases(
    test.case("tutorial001_02_py310", name="tutorial001_02_py310"),
    test.case("tutorial001_02_an_py310", name="tutorial001_02_an_py310"),
)
def post_file(name: str):
    client = _client_for(name)
    with tmp_path_ctx() as tmp_path:
        path = tmp_path / "test.txt"
        path.write_bytes(b"<file content>")

        with path.open("rb") as file:
            response = client.post("/files/", files={"file": file})
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json(), "response body").to_equal({"file_size": 14})


@test.cases(
    test.case("tutorial001_02_py310", name="tutorial001_02_py310"),
    test.case("tutorial001_02_an_py310", name="tutorial001_02_an_py310"),
)
def post_upload_file(name: str):
    client = _client_for(name)
    with tmp_path_ctx() as tmp_path:
        path = tmp_path / "test.txt"
        path.write_bytes(b"<file content>")

        with path.open("rb") as file:
            response = client.post("/uploadfile/", files={"file": file})
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json(), "response body").to_equal({"filename": "test.txt"})


@test.cases(
    test.case("tutorial001_02_py310", name="tutorial001_02_py310"),
    test.case("tutorial001_02_an_py310", name="tutorial001_02_an_py310"),
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
                    "/files/": {
                        "post": {
                            "summary": "Create File",
                            "operationId": "create_file_files__post",
                            "requestBody": {
                                "content": {
                                    "multipart/form-data": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_create_file_files__post"
                                        }
                                    }
                                }
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
                    "/uploadfile/": {
                        "post": {
                            "summary": "Create Upload File",
                            "operationId": "create_upload_file_uploadfile__post",
                            "requestBody": {
                                "content": {
                                    "multipart/form-data": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_create_upload_file_uploadfile__post"
                                        }
                                    }
                                }
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
                        "Body_create_file_files__post": {
                            "title": "Body_create_file_files__post",
                            "type": "object",
                            "properties": {
                                "file": {
                                    "title": "File",
                                    "anyOf": [
                                        {
                                            "type": "string",
                                            "contentMediaType": "application/octet-stream",
                                        },
                                        {"type": "null"},
                                    ],
                                }
                            },
                        },
                        "Body_create_upload_file_uploadfile__post": {
                            "title": "Body_create_upload_file_uploadfile__post",
                            "type": "object",
                            "properties": {
                                "file": {
                                    "title": "File",
                                    "anyOf": [
                                        {
                                            "type": "string",
                                            "contentMediaType": "application/octet-stream",
                                        },
                                        {"type": "null"},
                                    ],
                                }
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
                        "ValidationError": {
                            "title": "ValidationError",
                            "required": ["loc", "msg", "type"],
                            "type": "object",
                            "properties": {
                                "ctx": {"title": "Context", "type": "object"},
                                "input": {"title": "Input"},
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
                            },
                        },
                    }
                },
            }
        )
    )
