from typing import Annotated

from dirty_equals import IsOneOf
from fastapi import Cookie, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field
from tryke import expect, test

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/required-str")
async def read_required_str(p: Annotated[str, Cookie()]):
    return {"p": p}


class CookieModelRequiredStr(BaseModel):
    p: str


@app.get("/model-required-str")
async def read_model_required_str(p: Annotated[CookieModelRequiredStr, Cookie()]):
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
                    "in": "cookie",
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
                    "loc": ["cookie", "p"],
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
    client.cookies.set("p", "hello")
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Alias


@app.get("/required-alias")
async def read_required_alias(p: Annotated[str, Cookie(alias="p_alias")]):
    return {"p": p}


class CookieModelRequiredAlias(BaseModel):
    p: str = Field(alias="p_alias")


@app.get("/model-required-alias")
async def read_model_required_alias(p: Annotated[CookieModelRequiredAlias, Cookie()]):
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
                    "in": "cookie",
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
                    "loc": ["cookie", "p_alias"],
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
    client.cookies.set("p", "hello")
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["cookie", "p_alias"],
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
    client.cookies.set("p_alias", "hello")
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Validation alias


@app.get("/required-validation-alias")
def read_required_validation_alias(
    p: Annotated[str, Cookie(validation_alias="p_val_alias")],
):
    return {"p": p}


class CookieModelRequiredValidationAlias(BaseModel):
    p: str = Field(validation_alias="p_val_alias")


@app.get("/model-required-validation-alias")
def read_model_required_validation_alias(
    p: Annotated[CookieModelRequiredValidationAlias, Cookie()],
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
                    "in": "cookie",
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
                    "loc": ["cookie", "p_val_alias"],
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
    client.cookies.set("p", "hello")
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(422).fatal()

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["cookie", "p_val_alias"],
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
    client.cookies.set("p_val_alias", "hello")
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": "hello"})


# =====================================================================================
# Alias and validation alias


@app.get("/required-alias-and-validation-alias")
def read_required_alias_and_validation_alias(
    p: Annotated[str, Cookie(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class CookieModelRequiredAliasAndValidationAlias(BaseModel):
    p: str = Field(alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-alias-and-validation-alias")
def read_model_required_alias_and_validation_alias(
    p: Annotated[CookieModelRequiredAliasAndValidationAlias, Cookie()],
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
                    "in": "cookie",
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
                    "loc": ["cookie", "p_val_alias"],
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
    client.cookies.set("p", "hello")
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(422)

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["cookie", "p_val_alias"],
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
    client.cookies.set("p_alias", "hello")
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(422)

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["cookie", "p_val_alias"],
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
    client.cookies.set("p_val_alias", "hello")
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(200).fatal()

    expect(response.json(), "response body").to_equal({"p": "hello"})
