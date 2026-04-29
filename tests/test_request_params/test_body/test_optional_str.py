from typing import Annotated

from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from tryke import expect, test

from .utils import get_body_model_name

app = FastAPI()

# =====================================================================================
# Without aliases


@app.post("/optional-str", operation_id="optional_str")
async def read_optional_str(p: Annotated[str | None, Body(embed=True)] = None):
    return {"p": p}


class BodyModelOptionalStr(BaseModel):
    p: str | None = None


@app.post("/model-optional-str", operation_id="model_optional_str")
async def read_model_optional_str(p: BodyModelOptionalStr):
    return {"p": p.p}


@test.cases(
    test.case("optional-str", path="/optional-str"),
    test.case("model-optional-str", path="/model-optional-str"),
)
def optional_str_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
        {
            "properties": {
                "p": {"anyOf": [{"type": "string"}, {"type": "null"}], "title": "P"}
            },
            "title": body_model_name,
            "type": "object",
        }
    )


@test("Missing optional str body returns 200 with null")
def optional_str_missing():
    client = TestClient(app)
    response = client.post("/optional-str")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test("Missing optional str model body returns 422")
def model_optional_str_missing():
    client = TestClient(app)
    response = client.post("/model-optional-str")
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
    test.case("optional-str", path="/optional-str"),
    test.case("model-optional-str", path="/model-optional-str"),
)
def optional_str_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-str", path="/optional-str"),
    test.case("model-optional-str", path="/model-optional-str"),
)
def optional_str(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Alias


@app.post("/optional-alias", operation_id="optional_alias")
async def read_optional_alias(
    p: Annotated[str | None, Body(embed=True, alias="p_alias")] = None,
):
    return {"p": p}


class BodyModelOptionalAlias(BaseModel):
    p: str | None = Field(None, alias="p_alias")


@app.post("/model-optional-alias", operation_id="model_optional_alias")
async def read_model_optional_alias(p: BodyModelOptionalAlias):
    return {"p": p.p}


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_str_alias_schema(path: str):
    openapi = app.openapi()
    body_model_name = get_body_model_name(openapi, path)

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
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


@test("Missing optional str alias body returns 200 with null")
def optional_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-alias")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test("Missing optional str alias model body returns 422")
def model_optional_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-alias")
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
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def model_optional_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_alias": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Validation alias


@app.post("/optional-validation-alias", operation_id="optional_validation_alias")
def read_optional_validation_alias(
    p: Annotated[str | None, Body(embed=True, validation_alias="p_val_alias")] = None,
):
    return {"p": p}


class BodyModelOptionalValidationAlias(BaseModel):
    p: str | None = Field(None, validation_alias="p_val_alias")


@app.post(
    "/model-optional-validation-alias", operation_id="model_optional_validation_alias"
)
def read_model_optional_validation_alias(
    p: BodyModelOptionalValidationAlias,
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

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
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


@test("Missing optional str validation_alias body returns 200")
def optional_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-validation-alias")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test("Missing optional str validation_alias model returns 422")
def model_optional_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-validation-alias")
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
    test.case("optional-validation-alias", path="/optional-validation-alias"),
    test.case(
        "model-optional-validation-alias", path="/model-optional-validation-alias"
    ),
)
def model_optional_validation_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-validation-alias", path="/optional-validation-alias"),
    test.case(
        "model-optional-validation-alias", path="/model-optional-validation-alias"
    ),
)
def optional_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-validation-alias", path="/optional-validation-alias"),
    test.case(
        "model-optional-validation-alias", path="/model-optional-validation-alias"
    ),
)
def optional_validation_alias_by_validation_alias(path: str):
    client = TestClient(app)
    response = client.post(path, json={"p_val_alias": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Alias and validation alias


@app.post(
    "/optional-alias-and-validation-alias",
    operation_id="optional_alias_and_validation_alias",
)
def read_optional_alias_and_validation_alias(
    p: Annotated[
        str | None, Body(embed=True, alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class BodyModelOptionalAliasAndValidationAlias(BaseModel):
    p: str | None = Field(None, alias="p_alias", validation_alias="p_val_alias")


@app.post(
    "/model-optional-alias-and-validation-alias",
    operation_id="model_optional_alias_and_validation_alias",
)
def read_model_optional_alias_and_validation_alias(
    p: BodyModelOptionalAliasAndValidationAlias,
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

    expect(
        app.openapi()["components"]["schemas"][body_model_name],
        "request body schema",
    ).to_equal(
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


@test("Missing optional str alias+validation_alias returns 200")
def optional_alias_and_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/optional-alias-and-validation-alias")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test("Missing optional str alias+validation_alias model returns 422")
def model_optional_alias_and_validation_alias_missing():
    client = TestClient(app)
    response = client.post("/model-optional-alias-and-validation-alias")
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
        "optional-alias-and-validation-alias",
        path="/optional-alias-and-validation-alias",
    ),
    test.case(
        "model-optional-alias-and-validation-alias",
        path="/model-optional-alias-and-validation-alias",
    ),
)
def model_optional_alias_and_validation_alias_missing_empty_dict(path: str):
    client = TestClient(app)
    response = client.post(path, json={})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


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
    response = client.post(path, json={"p": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


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
    response = client.post(path, json={"p_alias": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


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
    response = client.post(path, json={"p_val_alias": "hello"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": "hello"})
