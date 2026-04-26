from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from tryke import expect, test

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-list-bytes")
async def read_optional_list_bytes(p: Annotated[list[bytes] | None, File()] = None):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile")
async def read_optional_list_uploadfile(
    p: Annotated[list[UploadFile] | None, File()] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


@test.cases(
    test.case("optional-list-bytes", path="/optional-list-bytes"),
    test.case("optional-list-uploadfile", path="/optional-list-uploadfile"),
)
def optional_list_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p": {
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "contentMediaType": "application/octet-stream",
                            },
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
    test.case("optional-list-bytes", path="/optional-list-bytes"),
    test.case("optional-list-uploadfile", path="/optional-list-uploadfile"),
)
def optional_list_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": None})


@test.cases(
    test.case("optional-list-bytes", path="/optional-list-bytes"),
    test.case("optional-list-uploadfile", path="/optional-list-uploadfile"),
)
def optional_list(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"file_size": [5, 5]})


# =====================================================================================
# Alias


@app.post("/optional-list-bytes-alias")
async def read_optional_list_bytes_alias(
    p: Annotated[list[bytes] | None, File(alias="p_alias")] = None,
):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile-alias")
async def read_optional_list_uploadfile_alias(
    p: Annotated[list[UploadFile] | None, File(alias="p_alias")] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


@test.cases(
    test.case("optional-list-bytes-alias", path="/optional-list-bytes-alias"),
    test.case("optional-list-uploadfile-alias", path="/optional-list-uploadfile-alias"),
)
def optional_list_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p_alias": {
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "contentMediaType": "application/octet-stream",
                            },
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
    test.case("optional-list-bytes-alias", path="/optional-list-bytes-alias"),
    test.case("optional-list-uploadfile-alias", path="/optional-list-uploadfile-alias"),
)
def optional_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"file_size": None})


@test.cases(
    test.case("optional-list-bytes-alias", path="/optional-list-bytes-alias"),
    test.case("optional-list-uploadfile-alias", path="/optional-list-uploadfile-alias"),
)
def optional_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": None})


@test.cases(
    test.case("optional-list-bytes-alias", path="/optional-list-bytes-alias"),
    test.case("optional-list-uploadfile-alias", path="/optional-list-uploadfile-alias"),
)
def optional_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": [5, 5]})


# =====================================================================================
# Validation alias


@app.post("/optional-list-bytes-validation-alias")
def read_optional_list_bytes_validation_alias(
    p: Annotated[list[bytes] | None, File(validation_alias="p_val_alias")] = None,
):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile-validation-alias")
def read_optional_list_uploadfile_validation_alias(
    p: Annotated[list[UploadFile] | None, File(validation_alias="p_val_alias")] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


@test.cases(
    test.case(
        "optional-list-bytes-validation-alias",
        path="/optional-list-bytes-validation-alias",
    ),
    test.case(
        "optional-list-uploadfile-validation-alias",
        path="/optional-list-uploadfile-validation-alias",
    ),
)
def optional_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "contentMediaType": "application/octet-stream",
                            },
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
        "optional-list-bytes-validation-alias",
        path="/optional-list-bytes-validation-alias",
    ),
    test.case(
        "optional-list-uploadfile-validation-alias",
        path="/optional-list-uploadfile-validation-alias",
    ),
)
def optional_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-list-bytes-validation-alias",
        path="/optional-list-bytes-validation-alias",
    ),
    test.case(
        "optional-list-uploadfile-validation-alias",
        path="/optional-list-uploadfile-validation-alias",
    ),
)
def optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-list-bytes-validation-alias",
        path="/optional-list-bytes-validation-alias",
    ),
    test.case(
        "optional-list-uploadfile-validation-alias",
        path="/optional-list-uploadfile-validation-alias",
    ),
)
def optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": [5, 5]})


# =====================================================================================
# Alias and validation alias


@app.post("/optional-list-bytes-alias-and-validation-alias")
def read_optional_list_bytes_alias_and_validation_alias(
    p: Annotated[
        list[bytes] | None, File(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"file_size": [len(file) for file in p] if p else None}


@app.post("/optional-list-uploadfile-alias-and-validation-alias")
def read_optional_list_uploadfile_alias_and_validation_alias(
    p: Annotated[
        list[UploadFile] | None,
        File(alias="p_alias", validation_alias="p_val_alias"),
    ] = None,
):
    return {"file_size": [file.size for file in p] if p else None}


@test.cases(
    test.case(
        "optional-list-bytes-alias-and-validation-alias",
        path="/optional-list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-list-uploadfile-alias-and-validation-alias",
        path="/optional-list-uploadfile-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "anyOf": [
                        {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "contentMediaType": "application/octet-stream",
                            },
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
        "optional-list-bytes-alias-and-validation-alias",
        path="/optional-list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-list-uploadfile-alias-and-validation-alias",
        path="/optional-list-uploadfile-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-list-bytes-alias-and-validation-alias",
        path="/optional-list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-list-uploadfile-alias-and-validation-alias",
        path="/optional-list-uploadfile-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files={"p": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-list-bytes-alias-and-validation-alias",
        path="/optional-list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-list-uploadfile-alias-and-validation-alias",
        path="/optional-list-uploadfile-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": None})


@test.cases(
    test.case(
        "optional-list-bytes-alias-and-validation-alias",
        path="/optional-list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "optional-list-uploadfile-alias-and-validation-alias",
        path="/optional-list-uploadfile-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": [5, 5]})
