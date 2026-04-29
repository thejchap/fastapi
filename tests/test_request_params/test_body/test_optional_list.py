from typing import Annotated

from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from tryke import expect, test

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-list-str", operation_id="optional_list_str")
async def read_optional_list_str(
    p: Annotated[list[str] | None, Body(embed=True)] = None,
):
    return {"p": p}


class BodyModelOptionalListStr(BaseModel):
    p: list[str] | None = None


@app.post("/model-optional-list-str", operation_id="model_optional_list_str")
async def read_model_optional_list_str(p: BodyModelOptionalListStr):
    return {"p": p.p}


@test.cases(
    test.case("optional-list-str", path="/optional-list-str"),
    test.case("model-optional-list-str", path="/model-optional-list-str"),
)
def optional_list_str_schema(path: str):
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
                        {"items": {"type": "string"}, "type": "array"},
                        {"type": "null"},
                    ],
                    "title": "P",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test("Missing optional list[str] body returns 200 with null")
def optional_list_str_missing():
    client = TestClient(app)
    response = client.post("/optional-list-str")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test("Missing optional list[str] model body returns 422")
def model_optional_list_str_missing():
    client = TestClient(app)
    response = client.post("/model-optional-list-str")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "input": None,
                    "loc": ["body"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ]
        }
    )


@test.cases(
    test.case("optional-list-str", path="/optional-list-str"),
    test.case("model-optional-list-str", path="/model-optional-list-str"),
)
def optional_list_str_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-list-str", path="/optional-list-str"),
    test.case("model-optional-list-str", path="/model-optional-list-str"),
)
def optional_list_str(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias


@app.post("/optional-list-alias", operation_id="optional_list_alias")
async def read_optional_list_alias(
    p: Annotated[list[str] | None, Body(embed=True, alias="p_alias")] = None,
):
    return {"p": p}


class BodyModelOptionalListAlias(BaseModel):
    p: list[str] | None = Field(None, alias="p_alias")


@app.post("/model-optional-list-alias", operation_id="model_optional_list_alias")
async def read_model_optional_list_alias(p: BodyModelOptionalListAlias):
    return {"p": p.p}


@test.cases(
    test.case("optional-list-alias", path="/optional-list-alias"),
    test.case("model-optional-list-alias", path="/model-optional-list-alias"),
)
def optional_list_str_alias_schema(path: str):
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
                        {"items": {"type": "string"}, "type": "array"},
                        {"type": "null"},
                    ],
                    "title": "P Alias",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test("Missing optional list[str] alias body returns 200 with null")
def optional_list_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-list-alias")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test("Missing optional list[str] alias model body returns 422")
def model_optional_list_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-list-alias")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "input": None,
                    "loc": ["body"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ]
        }
    )


@test.cases(
    test.case("optional-list-alias", path="/optional-list-alias"),
    test.case("model-optional-list-alias", path="/model-optional-list-alias"),
)
def optional_list_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-list-alias", path="/optional-list-alias"),
    test.case("model-optional-list-alias", path="/model-optional-list-alias"),
)
def optional_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-list-alias", path="/optional-list-alias"),
    test.case("model-optional-list-alias", path="/model-optional-list-alias"),
)
def optional_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_alias": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Validation alias


@app.post(
    "/optional-list-validation-alias", operation_id="optional_list_validation_alias"
)
def read_optional_list_validation_alias(
    p: Annotated[
        list[str] | None, Body(embed=True, validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class BodyModelOptionalListValidationAlias(BaseModel):
    p: list[str] | None = Field(None, validation_alias="p_val_alias")


@app.post(
    "/model-optional-list-validation-alias",
    operation_id="model_optional_list_validation_alias",
)
def read_model_optional_list_validation_alias(
    p: BodyModelOptionalListValidationAlias,
):
    return {"p": p.p}


@test.cases(
    test.case("optional-list-validation-alias", path="/optional-list-validation-alias"),
    test.case(
        "model-optional-list-validation-alias",
        path="/model-optional-list-validation-alias",
    ),
)
def optional_list_validation_alias_schema(path: str):
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
                        {"items": {"type": "string"}, "type": "array"},
                        {"type": "null"},
                    ],
                    "title": "P Val Alias",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test("Missing optional list[str] validation_alias body returns 200")
def optional_list_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-list-validation-alias")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test("Missing optional list[str] validation_alias model returns 422")
def model_optional_list_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-list-validation-alias")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "input": None,
                    "loc": ["body"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ]
        }
    )


@test.cases(
    test.case("optional-list-validation-alias", path="/optional-list-validation-alias"),
    test.case(
        "model-optional-list-validation-alias",
        path="/model-optional-list-validation-alias",
    ),
)
def optional_list_validation_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-list-validation-alias", path="/optional-list-validation-alias"),
    test.case(
        "model-optional-list-validation-alias",
        path="/model-optional-list-validation-alias",
    ),
)
def optional_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-list-validation-alias", path="/optional-list-validation-alias"),
    test.case(
        "model-optional-list-validation-alias",
        path="/model-optional-list-validation-alias",
    ),
)
def optional_list_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_val_alias": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias and validation alias


@app.post(
    "/optional-list-alias-and-validation-alias",
    operation_id="optional_list_alias_and_validation_alias",
)
def read_optional_list_alias_and_validation_alias(
    p: Annotated[
        list[str] | None,
        Body(embed=True, alias="p_alias", validation_alias="p_val_alias"),
    ] = None,
):
    return {"p": p}


class BodyModelOptionalListAliasAndValidationAlias(BaseModel):
    p: list[str] | None = Field(None, alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-optional-list-alias-and-validation-alias",
    operation_id="model_optional_list_alias_and_validation_alias",
)
def read_model_optional_list_alias_and_validation_alias(
    p: BodyModelOptionalListAliasAndValidationAlias,
):
    return {"p": p.p}


@test.cases(
    test.case(
        "optional-list-alias-and-validation-alias",
        path="/optional-list-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-list-alias-and-validation-alias",
        path="/model-optional-list-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_schema(path: str):
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
                        {"items": {"type": "string"}, "type": "array"},
                        {"type": "null"},
                    ],
                    "title": "P Val Alias",
                }
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test("Missing optional list[str] alias+validation_alias returns 200")
def optional_list_alias_and_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-list-alias-and-validation-alias")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test("Missing optional list[str] alias+validation_alias model returns 422")
def model_optional_list_alias_and_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-list-alias-and-validation-alias")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "input": None,
                    "loc": ["body"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ]
        }
    )


@test.cases(
    test.case(
        "optional-list-alias-and-validation-alias",
        path="/optional-list-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-list-alias-and-validation-alias",
        path="/model-optional-list-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case(
        "optional-list-alias-and-validation-alias",
        path="/optional-list-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-list-alias-and-validation-alias",
        path="/model-optional-list-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case(
        "optional-list-alias-and-validation-alias",
        path="/optional-list-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-list-alias-and-validation-alias",
        path="/model-optional-list-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_alias": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case(
        "optional-list-alias-and-validation-alias",
        path="/optional-list-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-list-alias-and-validation-alias",
        path="/model-optional-list-alias-and-validation-alias",
    ),
)
def optional_list_alias_and_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_val_alias": ["hello", "world"]})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})
