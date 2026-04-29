from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from tryke import expect, test

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/list-bytes", operation_id="list_bytes")
async def read_list_bytes(p: Annotated[list[bytes], File()]):
    return {"file_size": [len(file) for file in p]}


@app.post("/list-uploadfile", operation_id="list_uploadfile")
async def read_list_uploadfile(p: Annotated[list[UploadFile], File()]):
    return {"file_size": [file.size for file in p]}


@test.cases(
    test.case("list-bytes", path="/list-bytes"),
    test.case("list-uploadfile", path="/list-uploadfile"),
)
def list_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "contentMediaType": "application/octet-stream",
                    },
                    "title": "P",
                }
            },
            "required": ["p"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("list-bytes", path="/list-bytes"),
    test.case("list-uploadfile", path="/list-uploadfile"),
)
def list_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case("list-bytes", path="/list-bytes"),
    test.case("list-uploadfile", path="/list-uploadfile"),
)
def list_(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"file_size": [5, 5]})


# =====================================================================================
# Alias


@app.post("/list-bytes-alias", operation_id="list_bytes_alias")
async def read_list_bytes_alias(p: Annotated[list[bytes], File(alias="p_alias")]):
    return {"file_size": [len(file) for file in p]}


@app.post("/list-uploadfile-alias", operation_id="list_uploadfile_alias")
async def read_list_uploadfile_alias(
    p: Annotated[list[UploadFile], File(alias="p_alias")],
):
    return {"file_size": [file.size for file in p]}


@test.cases(
    test.case("list-bytes-alias", path="/list-bytes-alias"),
    test.case("list-uploadfile-alias", path="/list-uploadfile-alias"),
)
def list_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p_alias": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "contentMediaType": "application/octet-stream",
                    },
                    "title": "P Alias",
                }
            },
            "required": ["p_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("list-bytes-alias", path="/list-bytes-alias"),
    test.case("list-uploadfile-alias", path="/list-uploadfile-alias"),
)
def list_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case("list-bytes-alias", path="/list-bytes-alias"),
    test.case("list-uploadfile-alias", path="/list-uploadfile-alias"),
)
def list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case("list-bytes-alias", path="/list-bytes-alias"),
    test.case("list-uploadfile-alias", path="/list-uploadfile-alias"),
)
def list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file_size": [5, 5]})


# =====================================================================================
# Validation alias


@app.post("/list-bytes-validation-alias", operation_id="list_bytes_validation_alias")
def read_list_bytes_validation_alias(
    p: Annotated[list[bytes], File(validation_alias="p_val_alias")],
):
    return {"file_size": [len(file) for file in p]}


@app.post(
    "/list-uploadfile-validation-alias",
    operation_id="list_uploadfile_validation_alias",
)
def read_list_uploadfile_validation_alias(
    p: Annotated[list[UploadFile], File(validation_alias="p_val_alias")],
):
    return {"file_size": [file.size for file in p]}


@test.cases(
    test.case("list-bytes-validation-alias", path="/list-bytes-validation-alias"),
    test.case(
        "list-uploadfile-validation-alias", path="/list-uploadfile-validation-alias"
    ),
)
def list_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "contentMediaType": "application/octet-stream",
                    },
                    "title": "P Val Alias",
                }
            },
            "required": ["p_val_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("list-bytes-validation-alias", path="/list-bytes-validation-alias"),
    test.case(
        "list-uploadfile-validation-alias", path="/list-uploadfile-validation-alias"
    ),
)
def list_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case("list-bytes-validation-alias", path="/list-bytes-validation-alias"),
    test.case(
        "list-uploadfile-validation-alias", path="/list-uploadfile-validation-alias"
    ),
)
def list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello"), ("p", b"world")])
    expect(response.status_code, "status code").to_equal(422).fatal()

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case("list-bytes-validation-alias", path="/list-bytes-validation-alias"),
    test.case(
        "list-uploadfile-validation-alias", path="/list-uploadfile-validation-alias"
    ),
)
def list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file_size": [5, 5]})


# =====================================================================================
# Alias and validation alias


@app.post(
    "/list-bytes-alias-and-validation-alias",
    operation_id="list_bytes_alias_and_validation_alias",
)
def read_list_bytes_alias_and_validation_alias(
    p: Annotated[list[bytes], File(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"file_size": [len(file) for file in p]}


@app.post(
    "/list-uploadfile-alias-and-validation-alias",
    operation_id="list_uploadfile_alias_and_validation_alias",
)
def read_list_uploadfile_alias_and_validation_alias(
    p: Annotated[
        list[UploadFile], File(alias="p_alias", validation_alias="p_val_alias")
    ],
):
    return {"file_size": [file.size for file in p]}


@test.cases(
    test.case(
        "list-bytes-alias-and-validation-alias",
        path="/list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "list-uploadfile-alias-and-validation-alias",
        path="/list-uploadfile-alias-and-validation-alias",
    ),
)
def list_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "contentMediaType": "application/octet-stream",
                    },
                    "title": "P Val Alias",
                }
            },
            "required": ["p_val_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "list-bytes-alias-and-validation-alias",
        path="/list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "list-uploadfile-alias-and-validation-alias",
        path="/list-uploadfile-alias-and-validation-alias",
    ),
)
def list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case(
        "list-bytes-alias-and-validation-alias",
        path="/list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "list-uploadfile-alias-and-validation-alias",
        path="/list-uploadfile-alias-and-validation-alias",
    ),
)
def list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", "hello"), ("p", "world")])
    expect(response.status_code, "status code").to_equal(422)

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case(
        "list-bytes-alias-and-validation-alias",
        path="/list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "list-uploadfile-alias-and-validation-alias",
        path="/list-uploadfile-alias-and-validation-alias",
    ),
)
def list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello"), ("p_alias", b"world")])
    expect(response.status_code, "status code").to_equal(422).fatal()

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test.cases(
    test.case(
        "list-bytes-alias-and-validation-alias",
        path="/list-bytes-alias-and-validation-alias",
    ),
    test.case(
        "list-uploadfile-alias-and-validation-alias",
        path="/list-uploadfile-alias-and-validation-alias",
    ),
)
def list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(
        path, files=[("p_val_alias", b"hello"), ("p_val_alias", b"world")]
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file_size": [5, 5]})
