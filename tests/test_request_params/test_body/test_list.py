from typing import Annotated

from dirty_equals import IsOneOf, IsPartialDict
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from tryke import expect, test

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/required-list-str", operation_id="required_list_str")
async def read_required_list_str(p: Annotated[list[str], Body(embed=True)]):
    return {"p": p}


class BodyModelRequiredListStr(BaseModel):
    p: list[str]


@app.post("/model-required-list-str", operation_id="model_required_list_str")
def read_model_required_list_str(p: BodyModelRequiredListStr):
    return {"p": p.p}


@test.cases(
    test.case("required-list-str", path="/required-list-str"),
    test.case("model-required-list-str", path="/model-required-list-str"),
)
def required_list_str_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p": {
                    "items": {"type": "string"},
                    "title": "P",
                    "type": "array",
                },
            },
            "required": ["p"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("required-list-str-none", path="/required-list-str", json=None),
    test.case("required-list-str-empty", path="/required-list-str", json={}),
    test.case(
        "model-required-list-str-none", path="/model-required-list-str", json=None
    ),
    test.case(
        "model-required-list-str-empty", path="/model-required-list-str", json={}
    ),
)
def required_list_str_missing(path: str, json: dict | None):
    client = TestClient(app)
    response = client.post(path, json=json)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": IsOneOf(["body", "p"], ["body"]),
                    "msg": "Field required",
                    "input": IsOneOf(None, {}),
                }
            ]
        }
    )


@test.cases(
    test.case("required-list-str", path="/required-list-str"),
    test.case("model-required-list-str", path="/model-required-list-str"),
)
def required_list_str(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias


@app.post("/required-list-alias", operation_id="required_list_alias")
async def read_required_list_alias(
    p: Annotated[list[str], Body(embed=True, alias="p_alias")],
):
    return {"p": p}


class BodyModelRequiredListAlias(BaseModel):
    p: list[str] = Field(alias="p_alias")


@app.post("/model-required-list-alias", operation_id="model_required_list_alias")
async def read_model_required_list_alias(p: BodyModelRequiredListAlias):
    return {"p": p.p}


@test.cases(
    test.case("required-list-alias", path="/required-list-alias"),
    test.case("model-required-list-alias", path="/model-required-list-alias"),
)
def required_list_str_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p_alias": {
                    "items": {"type": "string"},
                    "title": "P Alias",
                    "type": "array",
                },
            },
            "required": ["p_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case("required-list-alias-none", path="/required-list-alias", json=None),
    test.case("required-list-alias-empty", path="/required-list-alias", json={}),
    test.case(
        "model-required-list-alias-none", path="/model-required-list-alias", json=None
    ),
    test.case(
        "model-required-list-alias-empty", path="/model-required-list-alias", json={}
    ),
)
def required_list_alias_missing(path: str, json: dict | None):
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
    test.case("required-list-alias", path="/required-list-alias"),
    test.case("model-required-list-alias", path="/model-required-list-alias"),
)
def required_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {"p": ["hello", "world"]}),
                }
            ]
        }
    )


@test.cases(
    test.case("required-list-alias", path="/required-list-alias"),
    test.case("model-required-list-alias", path="/model-required-list-alias"),
)
def required_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_alias": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Validation alias


@app.post(
    "/required-list-validation-alias", operation_id="required_list_validation_alias"
)
def read_required_list_validation_alias(
    p: Annotated[list[str], Body(embed=True, validation_alias="p_val_alias")],
):
    return {"p": p}


class BodyModelRequiredListValidationAlias(BaseModel):
    p: list[str] = Field(validation_alias="p_val_alias")


@app.post(
    "/model-required-list-validation-alias",
    operation_id="model_required_list_validation_alias",
)
async def read_model_required_list_validation_alias(
    p: BodyModelRequiredListValidationAlias,
):
    return {"p": p.p}


@test.cases(
    test.case("required-list-validation-alias", path="/required-list-validation-alias"),
    test.case(
        "model-required-list-validation-alias",
        path="/model-required-list-validation-alias",
    ),
)
def required_list_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "items": {"type": "string"},
                    "title": "P Val Alias",
                    "type": "array",
                },
            },
            "required": ["p_val_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "required-list-validation-alias-none",
        path="/required-list-validation-alias",
        json=None,
    ),
    test.case(
        "required-list-validation-alias-empty",
        path="/required-list-validation-alias",
        json={},
    ),
    test.case(
        "model-required-list-validation-alias-none",
        path="/model-required-list-validation-alias",
        json=None,
    ),
    test.case(
        "model-required-list-validation-alias-empty",
        path="/model-required-list-validation-alias",
        json={},
    ),
)
def required_list_validation_alias_missing(path: str, json: dict | None):
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
    test.case("required-list-validation-alias", path="/required-list-validation-alias"),
    test.case(
        "model-required-list-validation-alias",
        path="/model-required-list-validation-alias",
    ),
)
def required_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(422).fatal()

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, IsPartialDict({"p": ["hello", "world"]})),
                }
            ]
        }
    )


@test.cases(
    test.case("required-list-validation-alias", path="/required-list-validation-alias"),
    test.case(
        "model-required-list-validation-alias",
        path="/model-required-list-validation-alias",
    ),
)
def required_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_val_alias": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias and validation alias


@app.post(
    "/required-list-alias-and-validation-alias",
    operation_id="required_list_alias_and_validation_alias",
)
def read_required_list_alias_and_validation_alias(
    p: Annotated[
        list[str], Body(embed=True, alias="p_alias", validation_alias="p_val_alias")
    ],
):
    return {"p": p}


class BodyModelRequiredListAliasAndValidationAlias(BaseModel):
    p: list[str] = Field(alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-required-list-alias-and-validation-alias",
    operation_id="model_required_list_alias_and_validation_alias",
)
def read_model_required_list_alias_and_validation_alias(
    p: BodyModelRequiredListAliasAndValidationAlias,
):
    return {"p": p.p}


@test.cases(
    test.case(
        "required-list-alias-and-validation-alias",
        path="/required-list-alias-and-validation-alias",
    ),
    test.case(
        "model-required-list-alias-and-validation-alias",
        path="/model-required-list-alias-and-validation-alias",
    ),
)
def required_list_alias_and_validation_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p_val_alias": {
                    "items": {"type": "string"},
                    "title": "P Val Alias",
                    "type": "array",
                },
            },
            "required": ["p_val_alias"],
            "title": body_model_name,
            "type": "object",
        }
    )


@test.cases(
    test.case(
        "required-list-alias-and-validation-alias-none",
        path="/required-list-alias-and-validation-alias",
        json=None,
    ),
    test.case(
        "required-list-alias-and-validation-alias-empty",
        path="/required-list-alias-and-validation-alias",
        json={},
    ),
    test.case(
        "model-required-list-alias-and-validation-alias-none",
        path="/model-required-list-alias-and-validation-alias",
        json=None,
    ),
    test.case(
        "model-required-list-alias-and-validation-alias-empty",
        path="/model-required-list-alias-and-validation-alias",
        json={},
    ),
)
def required_list_alias_and_validation_alias_missing(path: str, json):
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
        "required-list-alias-and-validation-alias",
        path="/required-list-alias-and-validation-alias",
    ),
    test.case(
        "model-required-list-alias-and-validation-alias",
        path="/model-required-list-alias-and-validation-alias",
    ),
)
def required_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {"p": ["hello", "world"]}),
                }
            ]
        }
    )


@test.cases(
    test.case(
        "required-list-alias-and-validation-alias",
        path="/required-list-alias-and-validation-alias",
    ),
    test.case(
        "model-required-list-alias-and-validation-alias",
        path="/model-required-list-alias-and-validation-alias",
    ),
)
def required_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_alias": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(422).fatal()

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {"p_alias": ["hello", "world"]}),
                }
            ]
        }
    )


@test.cases(
    test.case(
        "required-list-alias-and-validation-alias",
        path="/required-list-alias-and-validation-alias",
    ),
    test.case(
        "model-required-list-alias-and-validation-alias",
        path="/model-required-list-alias-and-validation-alias",
    ),
)
def required_list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_val_alias": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})
