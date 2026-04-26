from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field
from tryke import expect, test

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/optional-str")
async def read_optional_str(p: str | None = None):
    return {"p": p}


class QueryModelOptionalStr(BaseModel):
    p: str | None = None


@app.get("/model-optional-str")
async def read_model_optional_str(p: Annotated[QueryModelOptionalStr, Query()]):
    return {"p": p.p}


@test.cases(
    test.case("optional-str", path="/optional-str"),
    test.case("model-optional-str", path="/model-optional-str"),
)
def optional_str_schema(path: str):
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": False,
                    "schema": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "title": "P",
                    },
                    "name": "p",
                    "in": "query",
                }
            ]
        )
    )


@test.cases(
    test.case("optional-str", path="/optional-str"),
    test.case("model-optional-str", path="/model-optional-str"),
)
def optional_str_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case("optional-str", path="/optional-str"),
    test.case("model-optional-str", path="/model-optional-str"),
)
def optional_str(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": "hello"})


# =====================================================================================
# Alias


@app.get("/optional-alias")
async def read_optional_alias(
    p: Annotated[str | None, Query(alias="p_alias")] = None,
):
    return {"p": p}


class QueryModelOptionalAlias(BaseModel):
    p: str | None = Field(None, alias="p_alias")


@app.get("/model-optional-alias")
async def read_model_optional_alias(p: Annotated[QueryModelOptionalAlias, Query()]):
    return {"p": p.p}


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_str_alias_schema(path: str):
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": False,
                    "schema": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "title": "P Alias",
                    },
                    "name": "p_alias",
                    "in": "query",
                }
            ]
        )
    )


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p=hello")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": None})


@test.cases(
    test.case("optional-alias", path="/optional-alias"),
    test.case("model-optional-alias", path="/model-optional-alias"),
)
def optional_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(f"{path}?p_alias=hello")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": "hello"})


# =====================================================================================
# Validation alias


@app.get("/optional-validation-alias")
def read_optional_validation_alias(
    p: Annotated[str | None, Query(validation_alias="p_val_alias")] = None,
):
    return {"p": p}


class QueryModelOptionalValidationAlias(BaseModel):
    p: str | None = Field(None, validation_alias="p_val_alias")


@app.get("/model-optional-validation-alias")
def read_model_optional_validation_alias(
    p: Annotated[QueryModelOptionalValidationAlias, Query()],
):
    return {"p": p.p}


@test.cases(
    test.case("optional-validation-alias", path="/optional-validation-alias"),
    test.case(
        "model-optional-validation-alias", path="/model-optional-validation-alias"
    ),
)
def optional_validation_alias_schema(path: str):
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": False,
                    "schema": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "title": "P Val Alias",
                    },
                    "name": "p_val_alias",
                    "in": "query",
                }
            ]
        )
    )


@test.cases(
    test.case("optional-validation-alias", path="/optional-validation-alias"),
    test.case(
        "model-optional-validation-alias", path="/model-optional-validation-alias"
    ),
)
def optional_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
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
    response = client.get(f"{path}?p=hello")
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
    response = client.get(f"{path}?p_val_alias=hello")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": "hello"})


# =====================================================================================
# Alias and validation alias


@app.get("/optional-alias-and-validation-alias")
def read_optional_alias_and_validation_alias(
    p: Annotated[
        str | None, Query(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class QueryModelOptionalAliasAndValidationAlias(BaseModel):
    p: str | None = Field(None, alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-optional-alias-and-validation-alias")
def read_model_optional_alias_and_validation_alias(
    p: Annotated[QueryModelOptionalAliasAndValidationAlias, Query()],
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
    expect(app.openapi()["paths"][path]["get"]["parameters"]).to_equal(
        snapshot(
            [
                {
                    "required": False,
                    "schema": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "title": "P Val Alias",
                    },
                    "name": "p_val_alias",
                    "in": "query",
                }
            ]
        )
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
    response = client.get(path)
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
    response = client.get(f"{path}?p=hello")
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
    response = client.get(f"{path}?p_alias=hello")
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
    response = client.get(f"{path}?p_val_alias=hello")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"p": "hello"})
