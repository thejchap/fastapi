from typing import Annotated

from dirty_equals import IsOneOf
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field
from tryke import expect, test

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/required-str")
async def read_required_str(p: str):
    return {"p": p}


class QueryModelRequiredStr(BaseModel):
    p: str


@app.get("/model-required-str")
async def read_model_required_str(p: Annotated[QueryModelRequiredStr, Query()]):
    return {"p": p.p}


@test.cases(
    test.case("required-str", path="/required-str"),
    test.case("model-required-str", path="/model-required-str"),
)
def required_str_schema(path: str):
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {"title": "P", "type": "string"},
                    "name": "p",
                    "in": "query",
                }
            ]
        )
    )


@test.cases(
    test.case("required-str", path="/required-str"),
    test.case("model-required-str", path="/model-required-str"),
)
def required_str_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p"],
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
    response = client.get(f"{path}?p=hello")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Alias


@app.get("/required-alias")
async def read_required_alias(p: Annotated[str, Query(alias="p_alias")]):
    return {"p": p}


class QueryModelRequiredAlias(BaseModel):
    p: str = Field(alias="p_alias")


@app.get("/model-required-alias")
async def read_model_required_alias(p: Annotated[QueryModelRequiredAlias, Query()]):
    return {"p": p.p}


@test.cases(
    test.case("required-alias", path="/required-alias"),
    test.case("model-required-alias", path="/model-required-alias"),
)
def required_str_alias_schema(path: str):
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {"title": "P Alias", "type": "string"},
                    "name": "p_alias",
                    "in": "query",
                }
            ]
        )
    )


@test.cases(
    test.case("required-alias", path="/required-alias"),
    test.case("model-required-alias", path="/model-required-alias"),
)
def required_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_alias"],
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
    response = client.get(f"{path}?p=hello")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_alias"],
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
    response = client.get(f"{path}?p_alias=hello")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Validation alias


@app.get("/required-validation-alias")
def read_required_validation_alias(
    p: Annotated[str, Query(validation_alias="p_val_alias")],
):
    return {"p": p}


class QueryModelRequiredValidationAlias(BaseModel):
    p: str = Field(validation_alias="p_val_alias")


@app.get("/model-required-validation-alias")
def read_model_required_validation_alias(
    p: Annotated[QueryModelRequiredValidationAlias, Query()],
):
    return {"p": p.p}


@test.cases(
    test.case("required-validation-alias", path="/required-validation-alias"),
    test.case(
        "model-required-validation-alias", path="/model-required-validation-alias"
    ),
)
def required_validation_alias_schema(path: str):
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {"title": "P Val Alias", "type": "string"},
                    "name": "p_val_alias",
                    "in": "query",
                }
            ]
        )
    )


@test.cases(
    test.case("required-validation-alias", path="/required-validation-alias"),
    test.case(
        "model-required-validation-alias", path="/model-required-validation-alias"
    ),
)
def required_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_val_alias"],
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
    response = client.get(f"{path}?p=hello")
    expect(response.status_code, "status code").to_equal(422).fatal()

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_val_alias"],
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
    response = client.get(f"{path}?p_val_alias=hello")
    expect(response.status_code, "status code").to_equal(200).fatal()

    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Alias and validation alias


@app.get("/required-alias-and-validation-alias")
def read_required_alias_and_validation_alias(
    p: Annotated[str, Query(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class QueryModelRequiredAliasAndValidationAlias(BaseModel):
    p: str = Field(alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-alias-and-validation-alias")
def read_model_required_alias_and_validation_alias(
    p: Annotated[QueryModelRequiredAliasAndValidationAlias, Query()],
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
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {"title": "P Val Alias", "type": "string"},
                    "name": "p_val_alias",
                    "in": "query",
                }
            ]
        )
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
def required_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_val_alias"],
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
    response = client.get(f"{path}?p=hello")
    expect(response.status_code, "status code").to_equal(422)

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_val_alias"],
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
    response = client.get(f"{path}?p_alias=hello")
    expect(response.status_code, "status code").to_equal(422)

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_val_alias"],
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
    response = client.get(f"{path}?p_val_alias=hello")
    expect(response.status_code, "status code").to_equal(200).fatal()

    expect(response.json(), "response body").to_equal({"p": "hello"})
