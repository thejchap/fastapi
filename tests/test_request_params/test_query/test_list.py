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


@app.get("/required-list-str")
async def read_required_list_str(p: Annotated[list[str], Query()]):
    return {"p": p}


class QueryModelRequiredListStr(BaseModel):
    p: list[str]


@app.get("/model-required-list-str")
def read_model_required_list_str(p: Annotated[QueryModelRequiredListStr, Query()]):
    return {"p": p.p}


@test.cases(
    test.case("required-list-str", path="/required-list-str"),
    test.case("model-required-list-str", path="/model-required-list-str"),
)
def required_list_str_schema(path: str):
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {
                        "title": "P",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "name": "p",
                    "in": "query",
                }
            ]
        )
    )


@test.cases(
    test.case("required-list-str", path="/required-list-str"),
    test.case("model-required-list-str", path="/model-required-list-str"),
)
def required_list_str_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
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
    test.case("required-list-str", path="/required-list-str"),
    test.case("model-required-list-str", path="/model-required-list-str"),
)
def required_list_str(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello&p=world")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias


@app.get("/required-list-alias")
async def read_required_list_alias(p: Annotated[list[str], Query(alias="p_alias")]):
    return {"p": p}


class QueryModelRequiredListAlias(BaseModel):
    p: list[str] = Field(alias="p_alias")


@app.get("/model-required-list-alias")
async def read_model_required_list_alias(
    p: Annotated[QueryModelRequiredListAlias, Query()],
):
    return {"p": p.p}


@test.cases(
    test.case("required-list-alias", path="/required-list-alias"),
    test.case("model-required-list-alias", path="/model-required-list-alias"),
)
def required_list_str_alias_schema(path: str):
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {
                        "title": "P Alias",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "name": "p_alias",
                    "in": "query",
                }
            ]
        )
    )


@test.cases(
    test.case("required-list-alias", path="/required-list-alias"),
    test.case("model-required-list-alias", path="/model-required-list-alias"),
)
def required_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
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
    test.case("required-list-alias", path="/required-list-alias"),
    test.case("model-required-list-alias", path="/model-required-list-alias"),
)
def required_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello&p=world")
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_alias"],
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
    response = client.get(f"{path}?p_alias=hello&p_alias=world")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Validation alias


@app.get("/required-list-validation-alias")
def read_required_list_validation_alias(
    p: Annotated[list[str], Query(validation_alias="p_val_alias")],
):
    return {"p": p}


class QueryModelRequiredListValidationAlias(BaseModel):
    p: list[str] = Field(validation_alias="p_val_alias")


@app.get("/model-required-list-validation-alias")
async def read_model_required_list_validation_alias(
    p: Annotated[QueryModelRequiredListValidationAlias, Query()],
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
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {
                        "title": "P Val Alias",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "name": "p_val_alias",
                    "in": "query",
                }
            ]
        )
    )


@test.cases(
    test.case("required-list-validation-alias", path="/required-list-validation-alias"),
    test.case(
        "model-required-list-validation-alias",
        path="/model-required-list-validation-alias",
    ),
)
def required_list_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
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
    test.case("required-list-validation-alias", path="/required-list-validation-alias"),
    test.case(
        "model-required-list-validation-alias",
        path="/model-required-list-validation-alias",
    ),
)
def required_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello&p=world")
    expect(response.status_code).to_equal(422)

    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, {"p": ["hello", "world"]}),
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
    response = client.get(f"{path}?p_val_alias=hello&p_val_alias=world")
    expect(response.status_code).to_equal(200).fatal()

    expect(response.json()).to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias and validation alias


@app.get("/required-list-alias-and-validation-alias")
def read_required_list_alias_and_validation_alias(
    p: Annotated[list[str], Query(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class QueryModelRequiredListAliasAndValidationAlias(BaseModel):
    p: list[str] = Field(alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-list-alias-and-validation-alias")
def read_model_required_list_alias_and_validation_alias(
    p: Annotated[QueryModelRequiredListAliasAndValidationAlias, Query()],
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
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {
                        "title": "P Val Alias",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "name": "p_val_alias",
                    "in": "query",
                }
            ]
        )
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
def required_list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
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
    response = client.get(f"{path}?p=hello&p=world")
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_val_alias"],
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
    response = client.get(f"{path}?p_alias=hello&p_alias=world")
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "p_val_alias"],
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
    response = client.get(f"{path}?p_val_alias=hello&p_val_alias=world")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"p": ["hello", "world"]})
