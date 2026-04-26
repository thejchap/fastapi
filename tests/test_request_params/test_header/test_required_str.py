from typing import Annotated

from dirty_equals import AnyThing, IsOneOf, IsPartialDict
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field
from tryke import expect, test

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/required-str")
async def read_required_str(p: Annotated[str, Header()]):
    return {"p": p}


class HeaderModelRequiredStr(BaseModel):
    p: str


@app.get("/model-required-str")
async def read_model_required_str(p: Annotated[HeaderModelRequiredStr, Header()]):
    return {"p": p.p}


@test.cases(
    test.case("required-str", path="/required-str"),
    test.case("model-required-str", path="/model-required-str"),
)
def required_str_schema(path: str):
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {"title": "P", "type": "string"},
                    "name": "p",
                    "in": "header",
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
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p"],
                    "msg": "Field required",
                    "input": AnyThing,
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
    response = client.get(path, headers={"p": "hello"})
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": "hello"})


# =====================================================================================
# Alias


@app.get("/required-alias")
async def read_required_alias(p: Annotated[str, Header(alias="p_alias")]):
    return {"p": p}


class HeaderModelRequiredAlias(BaseModel):
    p: str = Field(alias="p_alias")


@app.get("/model-required-alias")
async def read_model_required_alias(p: Annotated[HeaderModelRequiredAlias, Header()]):
    return {"p": p.p}


@test.cases(
    test.case("required-alias", path="/required-alias"),
    test.case("model-required-alias", path="/model-required-alias"),
)
def required_str_alias_schema(path: str):
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {"title": "P Alias", "type": "string"},
                    "name": "p_alias",
                    "in": "header",
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
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_alias"],
                    "msg": "Field required",
                    "input": AnyThing,
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
    response = client.get(path, headers={"p": "hello"})
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, IsPartialDict({"p": "hello"})),
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
    response = client.get(path, headers={"p_alias": "hello"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"p": "hello"})


# =====================================================================================
# Validation alias


@app.get("/required-validation-alias")
def read_required_validation_alias(
    p: Annotated[str, Header(validation_alias="p_val_alias")],
):
    return {"p": p}


class HeaderModelRequiredValidationAlias(BaseModel):
    p: str = Field(validation_alias="p_val_alias")


@app.get("/model-required-validation-alias")
def read_model_required_validation_alias(
    p: Annotated[HeaderModelRequiredValidationAlias, Header()],
):
    return {"p": p.p}


@test.cases(
    test.case("required-validation-alias", path="/required-validation-alias"),
    test.case(
        "model-required-validation-alias", path="/model-required-validation-alias"
    ),
)
def required_validation_alias_schema(path: str):
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {"title": "P Val Alias", "type": "string"},
                    "name": "p_val_alias",
                    "in": "header",
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
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_val_alias"],
                    "msg": "Field required",
                    "input": AnyThing,
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
    response = client.get(path, headers={"p": "hello"})
    expect(response.status_code).to_equal(422).fatal()

    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, IsPartialDict({"p": "hello"})),
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
    response = client.get(path, headers={"p_val_alias": "hello"})
    expect(response.status_code).to_equal(200).fatal()

    expect(response.json()).to_equal({"p": "hello"})


# =====================================================================================
# Alias and validation alias


@app.get("/required-alias-and-validation-alias")
def read_required_alias_and_validation_alias(
    p: Annotated[str, Header(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class HeaderModelRequiredAliasAndValidationAlias(BaseModel):
    p: str = Field(alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-alias-and-validation-alias")
def read_model_required_alias_and_validation_alias(
    p: Annotated[HeaderModelRequiredAliasAndValidationAlias, Header()],
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
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {"title": "P Val Alias", "type": "string"},
                    "name": "p_val_alias",
                    "in": "header",
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
    expect(response.status_code).to_equal(422)
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_val_alias"],
                    "msg": "Field required",
                    "input": AnyThing,
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
    response = client.get(path, headers={"p": "hello"})
    expect(response.status_code).to_equal(422)

    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, IsPartialDict({"p": "hello"})),
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
    response = client.get(path, headers={"p_alias": "hello"})
    expect(response.status_code).to_equal(422)

    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, IsPartialDict({"p_alias": "hello"})),
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
    response = client.get(path, headers={"p_val_alias": "hello"})
    expect(response.status_code).to_equal(200).fatal()

    expect(response.json()).to_equal({"p": "hello"})
