from typing import Annotated, Any

from dirty_equals import IsOneOf
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from tryke import expect, test

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/required-str", operation_id="required_str")
async def read_required_str(p: Annotated[str, Body(embed=True)]):
    return {"p": p}


class BodyModelRequiredStr(BaseModel):
    p: str


@app.post("/model-required-str", operation_id="model_required_str")
async def read_model_required_str(p: BodyModelRequiredStr):
    return {"p": p.p}


@test.cases(
    test.case("required-str", path="/required-str"),
    test.case("model-required-str", path="/model-required-str"),
)
def required_str_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {"p": {"title": "P", "type": "string"}},
            "required": ["p"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("none-required-str", json=None, path="/required-str"),
    test.case("none-model-required-str", json=None, path="/model-required-str"),
    test.case("empty-dict-required-str", json={}, path="/required-str"),
    test.case("empty-dict-model-required-str", json={}, path="/model-required-str"),
)
def required_str_missing(path: str, json: dict[str, Any] | None):
    client = TestClient(app)
    response = client.post(path, json=json)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": IsOneOf(["body"], ["body", "p"]),
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    )


@test.cases(
    test.case("required-str", path="/required-str"),
    test.case("model-required-str", path="/model-required-str"),
)
def required_str(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Alias


@app.post("/required-alias", operation_id="required_alias")
async def read_required_alias(
    p: Annotated[str, Body(embed=True, alias="p_alias")],
):
    return {"p": p}


class BodyModelRequiredAlias(BaseModel):
    p: str = Field(alias="p_alias")


@app.post("/model-required-alias", operation_id="model_required_alias")
async def read_model_required_alias(p: BodyModelRequiredAlias):
    return {"p": p.p}


@test.cases(
    test.case("required-alias", path="/required-alias"),
    test.case("model-required-alias", path="/model-required-alias"),
)
def required_str_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {"p_alias": {"title": "P Alias", "type": "string"}},
            "required": ["p_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("none-required-alias", json=None, path="/required-alias"),
    test.case("none-model-required-alias", json=None, path="/model-required-alias"),
    test.case("empty-dict-required-alias", json={}, path="/required-alias"),
    test.case("empty-dict-model-required-alias", json={}, path="/model-required-alias"),
)
def required_alias_missing(path: str, json: dict[str, Any] | None):
    client = TestClient(app)
    response = client.post(path, json=json)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": IsOneOf(["body", "p_alias"], ["body"]),
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    )


@test.cases(
    test.case("required-alias", path="/required-alias"),
    test.case("model-required-alias", path="/model-required-alias"),
)
def required_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": "hello"})
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {"p": "hello"}),
                }
            ]
        }
    )


@test.cases(
    test.case("required-alias", path="/required-alias"),
    test.case("model-required-alias", path="/model-required-alias"),
)
def required_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_alias": "hello"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Validation alias


@app.post("/required-validation-alias", operation_id="required_validation_alias")
def read_required_validation_alias(
    p: Annotated[str, Body(embed=True, validation_alias="p_val_alias")],
):
    return {"p": p}


class BodyModelRequiredValidationAlias(BaseModel):
    p: str = Field(validation_alias="p_val_alias")


@app.post(
    "/model-required-validation-alias", operation_id="model_required_validation_alias"
)
def read_model_required_validation_alias(
    p: BodyModelRequiredValidationAlias,
):
    return {"p": p.p}


@test.cases(
    test.case("required-validation-alias", path="/required-validation-alias"),
    test.case(
        "model-required-validation-alias", path="/model-required-validation-alias"
    ),
)
def required_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {"p_val_alias": {"title": "P Val Alias", "type": "string"}},
            "required": ["p_val_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "none-required-validation-alias", json=None, path="/required-validation-alias"
    ),
    test.case(
        "none-model-required-validation-alias",
        json=None,
        path="/model-required-validation-alias",
    ),
    test.case(
        "empty-dict-required-validation-alias",
        json={},
        path="/required-validation-alias",
    ),
    test.case(
        "empty-dict-model-required-validation-alias",
        json={},
        path="/model-required-validation-alias",
    ),
)
def required_validation_alias_missing(path: str, json: dict[str, Any] | None):
    client = TestClient(app)
    response = client.post(path, json=json)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": IsOneOf(["body", "p_val_alias"], ["body"]),
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    )


@test.cases(
    test.case("required-validation-alias", path="/required-validation-alias"),
    test.case(
        "model-required-validation-alias", path="/model-required-validation-alias"
    ),
)
def required_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": "hello"})
    expect(response.status_code, "status code").to_equal(422).fatal()

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {"p": "hello"}),
                }
            ]
        }
    )


@test.cases(
    test.case("required-validation-alias", path="/required-validation-alias"),
    test.case(
        "model-required-validation-alias", path="/model-required-validation-alias"
    ),
)
def required_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_val_alias": "hello"})
    expect(response.status_code, "status code").to_equal(200).fatal()

    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Alias and validation alias


@app.post(
    "/required-alias-and-validation-alias",
    operation_id="required_alias_and_validation_alias",
)
def read_required_alias_and_validation_alias(
    p: Annotated[
        str, Body(embed=True, alias="p_alias", validation_alias="p_val_alias")
    ],
):
    return {"p": p}


class BodyModelRequiredAliasAndValidationAlias(BaseModel):
    p: str = Field(alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-required-alias-and-validation-alias",
    operation_id="model_required_alias_and_validation_alias",
)
def read_model_required_alias_and_validation_alias(
    p: BodyModelRequiredAliasAndValidationAlias,
):
    return {"p": p.p}


@test.cases(
    test.case(
        "required-alias-and-validation-alias",
        path="/required-alias-and-validation-alias",
    ),
    test.case(
        "model-required-alias-and-validation-alias",
        path="/model-required-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {"p_val_alias": {"title": "P Val Alias", "type": "string"}},
            "required": ["p_val_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "none-required-alias-and-validation-alias",
        json=None,
        path="/required-alias-and-validation-alias",
    ),
    test.case(
        "none-model-required-alias-and-validation-alias",
        json=None,
        path="/model-required-alias-and-validation-alias",
    ),
    test.case(
        "empty-dict-required-alias-and-validation-alias",
        json={},
        path="/required-alias-and-validation-alias",
    ),
    test.case(
        "empty-dict-model-required-alias-and-validation-alias",
        json={},
        path="/model-required-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_missing(path: str, json: dict[str, Any] | None):
    client = TestClient(app)
    response = client.post(path, json=json)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": IsOneOf(["body"], ["body", "p_val_alias"]),
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    )


@test.cases(
    test.case(
        "required-alias-and-validation-alias",
        path="/required-alias-and-validation-alias",
    ),
    test.case(
        "model-required-alias-and-validation-alias",
        path="/model-required-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": "hello"})
    expect(response.status_code, "status code").to_equal(422)

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {"p": "hello"}),
                }
            ]
        }
    )


@test.cases(
    test.case(
        "required-alias-and-validation-alias",
        path="/required-alias-and-validation-alias",
    ),
    test.case(
        "model-required-alias-and-validation-alias",
        path="/model-required-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_alias": "hello"})
    expect(response.status_code, "status code").to_equal(422).fatal()

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {"p_alias": "hello"}),
                }
            ]
        }
    )


@test.cases(
    test.case(
        "required-alias-and-validation-alias",
        path="/required-alias-and-validation-alias",
    ),
    test.case(
        "model-required-alias-and-validation-alias",
        path="/model-required-alias-and-validation-alias",
    ),
)
def required_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_val_alias": "hello"})
    expect(response.status_code, "status code").to_equal(200).fatal()

    expect(response.json(), "response body").to_equal({"p": "hello"})
