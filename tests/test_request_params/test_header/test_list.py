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


@app.get("/required-list-str")
async def read_required_list_str(p: Annotated[list[str], Header()]):
    return {"p": p}


class HeaderModelRequiredListStr(BaseModel):
    p: list[str]


@app.get("/model-required-list-str")
def read_model_required_list_str(p: Annotated[HeaderModelRequiredListStr, Header()]):
    return {"p": p.p}


@test.cases(
    test.case("required-list-str", path="/required-list-str"),
    test.case("model-required-list-str", path="/model-required-list-str"),
)
def required_list_str_schema(path: str):
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
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
                    "in": "header",
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
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
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
    test.case("required-list-str", path="/required-list-str"),
    test.case("model-required-list-str", path="/model-required-list-str"),
)
def required_list_str(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias


@app.get("/required-list-alias")
async def read_required_list_alias(p: Annotated[list[str], Header(alias="p_alias")]):
    return {"p": p}


class HeaderModelRequiredListAlias(BaseModel):
    p: list[str] = Field(alias="p_alias")


@app.get("/model-required-list-alias")
async def read_model_required_list_alias(
    p: Annotated[HeaderModelRequiredListAlias, Header()],
):
    return {"p": p.p}


@test.cases(
    test.case("required-list-alias", path="/required-list-alias"),
    test.case("model-required-list-alias", path="/model-required-list-alias"),
)
def required_list_str_alias_schema(path: str):
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
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
                    "in": "header",
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
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
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
    test.case("required-list-alias", path="/required-list-alias"),
    test.case("model-required-list-alias", path="/model-required-list-alias"),
)
def required_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, IsPartialDict({"p": ["hello", "world"]})),
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
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Validation alias


@app.get("/required-list-validation-alias")
def read_required_list_validation_alias(
    p: Annotated[list[str], Header(validation_alias="p_val_alias")],
):
    return {"p": p}


class HeaderModelRequiredListValidationAlias(BaseModel):
    p: list[str] = Field(validation_alias="p_val_alias")


@app.get("/model-required-list-validation-alias")
async def read_model_required_list_validation_alias(
    p: Annotated[HeaderModelRequiredListValidationAlias, Header()],
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
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
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
                    "in": "header",
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
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
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
    test.case("required-list-validation-alias", path="/required-list-validation-alias"),
    test.case(
        "model-required-list-validation-alias",
        path="/model-required-list-validation-alias",
    ),
)
def required_list_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    expect(response.status_code, "status code").to_equal(422)

    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_val_alias"],
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
    response = client.get(
        path, headers=[("p_val_alias", "hello"), ("p_val_alias", "world")]
    )
    expect(response.status_code, "status code").to_equal(200).fatal()

    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias and validation alias


@app.get("/required-list-alias-and-validation-alias")
def read_required_list_alias_and_validation_alias(
    p: Annotated[list[str], Header(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


class HeaderModelRequiredListAliasAndValidationAlias(BaseModel):
    p: list[str] = Field(alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-required-list-alias-and-validation-alias")
def read_model_required_list_alias_and_validation_alias(
    p: Annotated[HeaderModelRequiredListAliasAndValidationAlias, Header()],
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
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
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
                    "in": "header",
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
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
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
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(None, IsPartialDict({"p": ["hello", "world"]})),
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
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["header", "p_val_alias"],
                    "msg": "Field required",
                    "input": IsOneOf(
                        None, IsPartialDict({"p_alias": ["hello", "world"]})
                    ),
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
    response = client.get(
        path, headers=[("p_val_alias", "hello"), ("p_val_alias", "world")]
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})
