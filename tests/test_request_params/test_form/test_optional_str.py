from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from tryke import expect, test

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-str", operation_id="optional_str")
async def read_optional_str(p: Annotated[str | None, Form()] = None):
    return {"p": p}


class FormModelOptionalStr(BaseModel):
    p: str | None = None


@app.post("/model-optional-str", operation_id="model_optional_str")
async def read_model_optional_str(p: Annotated[FormModelOptionalStr, Form()]):
    return {"p": p.p}


@test.cases(
    test.case("optional-str", path="/optional-str"),
    test.case("model-optional-str", path="/model-optional-str"),
)
def optional_str_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p": {"anyOf": [{"type": "string"}, {"type": "null"}], "title": "P"}
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("optional-str", path="/optional-str"),
    test.case("model-optional-str", path="/model-optional-str"),
)
def optional_str_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case("optional-str", path="/optional-str"),
    test.case("model-optional-str", path="/model-optional-str"),
)
def optional_str(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": "hello"})


# =====================================================================================
# Alias


@app.post("/optional-alias", operation_id="optional_alias")
async def read_optional_alias(
    p: Annotated[str | None, Form(alias="p_alias")] = None,
):
    return {"p": p}


class FormModelOptionalAlias(BaseModel):
    p: str | None = Field(None, alias="p_alias")


@app.post("/model-optional-alias", operation_id="model_optional_alias")
async def read_model_optional_alias(p: Annotated[FormModelOptionalAlias, Form()]):
    return {"p": p.p}


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_str_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p_alias": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "title": "P Alias",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": "hello"})


# =====================================================================================
# Validation alias


@app.post("/optional-validation-alias", operation_id="optional_validation_alias")
def read_optional_validation_alias(
    p: Annotated[str | None, Form(validation_alias="p_val_alias")] = None,
):
    return {"p": p}


class FormModelOptionalValidationAlias(BaseModel):
    p: str | None = Field(None, validation_alias="p_val_alias")


@app.post(
    "/model-optional-validation-alias", operation_id="model_optional_validation_alias"
)
def read_model_optional_validation_alias(
    p: Annotated[FormModelOptionalValidationAlias, Form()],
):
    return {"p": p.p}


@test.cases(
    test.case("optional-validation-alias", path="/optional-validation-alias"),
    test.case(
        "model-optional-validation-alias", path="/model-optional-validation-alias"
    ),
)
def optional_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "title": "P Val Alias",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("optional-validation-alias", path="/optional-validation-alias"),
    test.case(
        "model-optional-validation-alias", path="/model-optional-validation-alias"
    ),
)
def optional_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case("optional-validation-alias", path="/optional-validation-alias"),
    test.case(
        "model-optional-validation-alias", path="/model-optional-validation-alias"
    ),
)
def optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case("optional-validation-alias", path="/optional-validation-alias"),
    test.case(
        "model-optional-validation-alias", path="/model-optional-validation-alias"
    ),
)
def optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_val_alias": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": "hello"})


# =====================================================================================
# Alias and validation alias


@app.post(
    "/optional-alias-and-validation-alias",
    operation_id="optional_alias_and_validation_alias",
)
def read_optional_alias_and_validation_alias(
    p: Annotated[
        str | None, Form(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class FormModelOptionalAliasAndValidationAlias(BaseModel):
    p: str | None = Field(None, alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-optional-alias-and-validation-alias",
    operation_id="model_optional_alias_and_validation_alias",
)
def read_model_optional_alias_and_validation_alias(
    p: Annotated[FormModelOptionalAliasAndValidationAlias, Form()],
):
    return {"p": p.p}


@test.cases(
    test.case(
        "optional-alias-and-validation-alias",
        path="/optional-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-alias-and-validation-alias",
        path="/model-optional-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(app.openapi()["components"]["schemas"][body_model_name]).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "title": "P Val Alias",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "optional-alias-and-validation-alias",
        path="/optional-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-alias-and-validation-alias",
        path="/model-optional-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.post(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case(
        "optional-alias-and-validation-alias",
        path="/optional-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-alias-and-validation-alias",
        path="/model-optional-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case(
        "optional-alias-and-validation-alias",
        path="/optional-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-alias-and-validation-alias",
        path="/model-optional-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_alias": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case(
        "optional-alias-and-validation-alias",
        path="/optional-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-alias-and-validation-alias",
        path="/model-optional-alias-and-validation-alias",
    ),
)
def optional_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, data={"p_val_alias": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": "hello"})
