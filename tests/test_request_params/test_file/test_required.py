from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from tryke import expect, test

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/required-bytes", operation_id="required_bytes")
async def read_required_bytes(p: Annotated[bytes, File()]):
    return {"file_size": len(p)}


@app.post("/required-uploadfile", operation_id="required_uploadfile")
async def read_required_uploadfile(p: Annotated[UploadFile, File()]):
    return {"file_size": p.size}


@test.cases(
    test.case("required-bytes", path="/required-bytes"),
    test.case("required-uploadfile", path="/required-uploadfile"),
)
def required_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p": {
                    "title": "P",
                    "type": "string",
                    "contentMediaType": "application/octet-stream",
                }
            },
            "required": ["p"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("required-bytes", path="/required-bytes"),
    test.case("required-uploadfile", path="/required-uploadfile"),
)
def required_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
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
    test.case("required-bytes", path="/required-bytes"),
    test.case("required-uploadfile", path="/required-uploadfile"),
)
def required(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"file_size": 5})


# =====================================================================================
# Alias


@app.post("/required-bytes-alias", operation_id="required_bytes_alias")
async def read_required_bytes_alias(p: Annotated[bytes, File(alias="p_alias")]):
    return {"file_size": len(p)}


@app.post("/required-uploadfile-alias", operation_id="required_uploadfile_alias")
async def read_required_uploadfile_alias(
    p: Annotated[UploadFile, File(alias="p_alias")],
):
    return {"file_size": p.size}


@test.cases(
    test.case("required-bytes-alias", path="/required-bytes-alias"),
    test.case("required-uploadfile-alias", path="/required-uploadfile-alias"),
)
def required_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p_alias": {
                    "title": "P Alias",
                    "type": "string",
                    "contentMediaType": "application/octet-stream",
                }
            },
            "required": ["p_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("required-bytes-alias", path="/required-bytes-alias"),
    test.case("required-uploadfile-alias", path="/required-uploadfile-alias"),
)
def required_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
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
    test.case("required-bytes-alias", path="/required-bytes-alias"),
    test.case("required-uploadfile-alias", path="/required-uploadfile-alias"),
)
def required_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
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
    test.case("required-bytes-alias", path="/required-bytes-alias"),
    test.case("required-uploadfile-alias", path="/required-uploadfile-alias"),
)
def required_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": 5})


# =====================================================================================
# Validation alias


@app.post(
    "/required-bytes-validation-alias", operation_id="required_bytes_validation_alias"
)
def read_required_bytes_validation_alias(
    p: Annotated[bytes, File(validation_alias="p_val_alias")],
):
    return {"file_size": len(p)}


@app.post(
    "/required-uploadfile-validation-alias",
    operation_id="required_uploadfile_validation_alias",
)
def read_required_uploadfile_validation_alias(
    p: Annotated[UploadFile, File(validation_alias="p_val_alias")],
):
    return {"file_size": p.size}


@test.cases(
    test.case(
        "required-bytes-validation-alias", path="/required-bytes-validation-alias"
    ),
    test.case(
        "required-uploadfile-validation-alias",
        path="/required-uploadfile-validation-alias",
    ),
)
def required_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "title": "P Val Alias",
                    "type": "string",
                    "contentMediaType": "application/octet-stream",
                }
            },
            "required": ["p_val_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "required-bytes-validation-alias", path="/required-bytes-validation-alias"
    ),
    test.case(
        "required-uploadfile-validation-alias",
        path="/required-uploadfile-validation-alias",
    ),
)
def required_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
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
        "required-bytes-validation-alias", path="/required-bytes-validation-alias"
    ),
    test.case(
        "required-uploadfile-validation-alias",
        path="/required-uploadfile-validation-alias",
    ),
)
def required_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p", b"hello")])
    expect(response.status_code).to_equal(422).fatal()

    expect(response.json()).to_equal(
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
        "required-bytes-validation-alias", path="/required-bytes-validation-alias"
    ),
    test.case(
        "required-uploadfile-validation-alias",
        path="/required-uploadfile-validation-alias",
    ),
)
def required_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": 5})


# =====================================================================================
# Alias and validation alias


@app.post(
    "/required-bytes-alias-and-validation-alias",
    operation_id="required_bytes_alias_and_validation_alias",
)
def read_required_bytes_alias_and_validation_alias(
    p: Annotated[bytes, File(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"file_size": len(p)}


@app.post(
    "/required-uploadfile-alias-and-validation-alias",
    operation_id="required_uploadfile_alias_and_validation_alias",
)
def read_required_uploadfile_alias_and_validation_alias(
    p: Annotated[UploadFile, File(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"file_size": p.size}


@test.cases(
    test.case(
        "required-bytes-alias-and-validation-alias",
        path="/required-bytes-alias-and-validation-alias",
    ),
    test.case(
        "required-uploadfile-alias-and-validation-alias",
        path="/required-uploadfile-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "title": "P Val Alias",
                    "type": "string",
                    "contentMediaType": "application/octet-stream",
                }
            },
            "required": ["p_val_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "required-bytes-alias-and-validation-alias",
        path="/required-bytes-alias-and-validation-alias",
    ),
    test.case(
        "required-uploadfile-alias-and-validation-alias",
        path="/required-uploadfile-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
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
        "required-bytes-alias-and-validation-alias",
        path="/required-bytes-alias-and-validation-alias",
    ),
    test.case(
        "required-uploadfile-alias-and-validation-alias",
        path="/required-uploadfile-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, files={"p": "hello"})
    expect(response.status_code).to_equal(422)

    expect(response.json()).to_equal(
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
        "required-bytes-alias-and-validation-alias",
        path="/required-bytes-alias-and-validation-alias",
    ),
    test.case(
        "required-uploadfile-alias-and-validation-alias",
        path="/required-uploadfile-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_alias", b"hello")])
    expect(response.status_code).to_equal(422).fatal()

    expect(response.json()).to_equal(
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
        "required-bytes-alias-and-validation-alias",
        path="/required-bytes-alias-and-validation-alias",
    ),
    test.case(
        "required-uploadfile-alias-and-validation-alias",
        path="/required-uploadfile-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, files=[("p_val_alias", b"hello")])
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"file_size": 5})
