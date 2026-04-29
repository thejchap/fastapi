from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from tryke import expect, test

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-bytes", operation_id="optional_bytes")
async def read_optional_bytes(p: Annotated[bytes | None, File()] = None):
    return {"file_size": len(p) if p else None}


@app.post("/optional-uploadfile", operation_id="optional_uploadfile")
async def read_optional_uploadfile(p: Annotated[UploadFile | None, File()] = None):
    return {"file_size": p.size if p else None}


@test.cases(
    test.case("optional-bytes", path="/optional-bytes"),
    test.case("optional-uploadfile", path="/optional-uploadfile"),
)
def optional_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p": {
                    "anyOf": [
                        {
                            "type": "string",
                            "contentMediaType": "application/octet-stream",
                        },
                        {"type": "null"},
                    ],
                    "title": "P",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("optional-bytes", path="/optional-bytes"),
    test.case("optional-uploadfile", path="/optional-uploadfile"),
)
def optional_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file_size": None})


@test.cases(
    test.case("optional-bytes", path="/optional-bytes"),
    test.case("optional-uploadfile", path="/optional-uploadfile"),
)
def optional(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"file_size": 5})


# =====================================================================================
# Alias


@app.post("/optional-bytes-alias", operation_id="optional_bytes_alias")
async def read_optional_bytes_alias(
    p: Annotated[bytes | None, File(alias="p_alias")] = None,
):
    return {"file_size": len(p) if p else None}


@app.post("/optional-uploadfile-alias", operation_id="optional_uploadfile_alias")
async def read_optional_uploadfile_alias(
    p: Annotated[UploadFile | None, File(alias="p_alias")] = None,
):
    return {"file_size": p.size if p else None}


@test.cases(
    test.case("optional-bytes-alias", path="/optional-bytes-alias"),
    test.case("optional-uploadfile-alias", path="/optional-uploadfile-alias"),
)
def optional_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p_alias": {
                    "anyOf": [
                        {
                            "type": "string",
                            "contentMediaType": "application/octet-stream",
                        },
                        {"type": "null"},
                    ],
                    "title": "P Alias",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("optional-bytes-alias", path="/optional-bytes-alias"),
    test.case("optional-uploadfile-alias", path="/optional-uploadfile-alias"),
)
def optional_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"file_size": None})


@test.cases(
    test.case("optional-bytes-alias", path="/optional-bytes-alias"),
    test.case("optional-uploadfile-alias", path="/optional-uploadfile-alias"),
)
def optional_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"file_size": None})


@test.cases(
    test.case("optional-bytes-alias", path="/optional-bytes-alias"),
    test.case("optional-uploadfile-alias", path="/optional-uploadfile-alias"),
)
def optional_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file_size": 5})


# =====================================================================================
# Validation alias


@app.post(
    "/optional-bytes-validation-alias", operation_id="optional_bytes_validation_alias"
)
def read_optional_bytes_validation_alias(
    p: Annotated[bytes | None, File(validation_alias="p_val_alias")] = None,
):
    return {"file_size": len(p) if p else None}


@app.post(
    "/optional-uploadfile-validation-alias",
    operation_id="optional_uploadfile_validation_alias",
)
def read_optional_uploadfile_validation_alias(
    p: Annotated[UploadFile | None, File(validation_alias="p_val_alias")] = None,
):
    return {"file_size": p.size if p else None}


@test.cases(
    test.case(
        "optional-bytes-validation-alias", path="/optional-bytes-validation-alias"
    ),
    test.case(
        "optional-uploadfile-validation-alias",
        path="/optional-uploadfile-validation-alias",
    ),
)
def optional_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "anyOf": [
                        {
                            "type": "string",
                            "contentMediaType": "application/octet-stream",
                        },
                        {"type": "null"},
                    ],
                    "title": "P Val Alias",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "optional-bytes-validation-alias", path="/optional-bytes-validation-alias"
    ),
    test.case(
        "optional-uploadfile-validation-alias",
        path="/optional-uploadfile-validation-alias",
    ),
)
def optional_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-bytes-validation-alias", path="/optional-bytes-validation-alias"
    ),
    test.case(
        "optional-uploadfile-validation-alias",
        path="/optional-uploadfile-validation-alias",
    ),
)
def optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-bytes-validation-alias", path="/optional-bytes-validation-alias"
    ),
    test.case(
        "optional-uploadfile-validation-alias",
        path="/optional-uploadfile-validation-alias",
    ),
)
def optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file_size": 5})


# =====================================================================================
# Alias and validation alias


@app.post(
    "/optional-bytes-alias-and-validation-alias",
    operation_id="optional_bytes_alias_and_validation_alias",
)
def read_optional_bytes_alias_and_validation_alias(
    p: Annotated[
        bytes | None, File(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"file_size": len(p) if p else None}


@app.post(
    "/optional-uploadfile-alias-and-validation-alias",
    operation_id="optional_uploadfile_alias_and_validation_alias",
)
def read_optional_uploadfile_alias_and_validation_alias(
    p: Annotated[
        UploadFile | None, File(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"file_size": p.size if p else None}


@test.cases(
    test.case(
        "optional-bytes-alias-and-validation-alias",
        path="/optional-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-uploadfile-alias-and-validation-alias",
        path="/optional-uploadfile-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "anyOf": [
                        {
                            "type": "string",
                            "contentMediaType": "application/octet-stream",
                        },
                        {"type": "null"},
                    ],
                    "title": "P Val Alias",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "optional-bytes-alias-and-validation-alias",
        path="/optional-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-uploadfile-alias-and-validation-alias",
        path="/optional-uploadfile-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-bytes-alias-and-validation-alias",
        path="/optional-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-uploadfile-alias-and-validation-alias",
        path="/optional-uploadfile-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files={"p": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-bytes-alias-and-validation-alias",
        path="/optional-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-uploadfile-alias-and-validation-alias",
        path="/optional-uploadfile-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-bytes-alias-and-validation-alias",
        path="/optional-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-uploadfile-alias-and-validation-alias",
        path="/optional-uploadfile-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file_size": 5})
