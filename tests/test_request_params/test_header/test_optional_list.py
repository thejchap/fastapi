from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field
from tryke import expect, test

app = FastAPI()

# =====================================================================================
# Without aliases


@app.get("/optional-list-str")
async def read_optional_list_str(
    p: Annotated[list[str] | None, Header()] = None,
):
    return {"p": p}


class HeaderModelOptionalListStr(BaseModel):
    p: list[str] | None = None


@app.get("/model-optional-list-str")
async def read_model_optional_list_str(
    p: Annotated[HeaderModelOptionalListStr, Header()],
):
    return {"p": p.p}


@test.cases(
    test.case("optional-list-str", path="/optional-list-str"),
    test.case("model-optional-list-str", path="/model-optional-list-str"),
)
def optional_list_str_schema(path: str):
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
        snapshot(
            [
                {
                    "required": False,
                    "schema": {
                        "anyOf": [
                            {"items": {"type": "string"}, "type": "array"},
                            {"type": "null"},
                        ],
                        "title": "P",
                    },
                    "name": "p",
                    "in": "header",
                }
            ]
        )
    )


@test.cases(
    test.case("optional-list-str", path="/optional-list-str"),
    test.case("model-optional-list-str", path="/model-optional-list-str"),
)
def optional_list_str_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-list-str", path="/optional-list-str"),
    test.case("model-optional-list-str", path="/model-optional-list-str"),
)
def optional_list_str(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias


@app.get("/optional-list-alias")
async def read_optional_list_alias(
    p: Annotated[list[str] | None, Header(alias="p_alias")] = None,
):
    return {"p": p}


class HeaderModelOptionalListAlias(BaseModel):
    p: list[str] | None = Field(None, alias="p_alias")


@app.get("/model-optional-list-alias")
async def read_model_optional_list_alias(
    p: Annotated[HeaderModelOptionalListAlias, Header()],
):
    return {"p": p.p}


@test.cases(
    test.case("optional-list-alias", path="/optional-list-alias"),
    test.case("model-optional-list-alias", path="/model-optional-list-alias"),
)
def optional_list_str_alias_schema(path: str):
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
        snapshot(
            [
                {
                    "required": False,
                    "schema": {
                        "anyOf": [
                            {"items": {"type": "string"}, "type": "array"},
                            {"type": "null"},
                        ],
                        "title": "P Alias",
                    },
                    "name": "p_alias",
                    "in": "header",
                }
            ]
        )
    )


@test.cases(
    test.case("optional-list-alias", path="/optional-list-alias"),
    test.case("model-optional-list-alias", path="/model-optional-list-alias"),
)
def optional_list_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-list-alias", path="/optional-list-alias"),
    test.case("model-optional-list-alias", path="/model-optional-list-alias"),
)
def optional_list_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": None})


@test.cases(
    test.case("optional-list-alias", path="/optional-list-alias"),
    test.case("model-optional-list-alias", path="/model-optional-list-alias"),
)
def optional_list_alias_by_alias(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Validation alias


@app.get("/optional-list-validation-alias")
def read_optional_list_validation_alias(
    p: Annotated[list[str] | None, Header(validation_alias="p_val_alias")] = None,
):
    return {"p": p}


class HeaderModelOptionalListValidationAlias(BaseModel):
    p: list[str] | None = Field(None, validation_alias="p_val_alias")


@app.get("/model-optional-list-validation-alias")
def read_model_optional_list_validation_alias(
    p: Annotated[HeaderModelOptionalListValidationAlias, Header()],
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
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
        snapshot(
            [
                {
                    "required": False,
                    "schema": {
                        "anyOf": [
                            {"items": {"type": "string"}, "type": "array"},
                            {"type": "null"},
                        ],
                        "title": "P Val Alias",
                    },
                    "name": "p_val_alias",
                    "in": "header",
                }
            ]
        )
    )


@test.cases(
    test.case("optional-list-validation-alias", path="/optional-list-validation-alias"),
    test.case(
        "model-optional-list-validation-alias",
        path="/model-optional-list-validation-alias",
    ),
)
def optional_list_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(200)
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
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
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
    response = client.get(
        path, headers=[("p_val_alias", "hello"), ("p_val_alias", "world")]
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})


# =====================================================================================
# Alias and validation alias


@app.get("/optional-list-alias-and-validation-alias")
def read_optional_list_alias_and_validation_alias(
    p: Annotated[
        list[str] | None, Header(alias="p_alias", validation_alias="p_val_alias")
    ] = None,
):
    return {"p": p}


class HeaderModelOptionalListAliasAndValidationAlias(BaseModel):
    p: list[str] | None = Field(None, alias="p_alias", validation_alias="p_val_alias")


@app.get("/model-optional-list-alias-and-validation-alias")
def read_model_optional_list_alias_and_validation_alias(
    p: Annotated[HeaderModelOptionalListAliasAndValidationAlias, Header()],
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
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
        snapshot(
            [
                {
                    "required": False,
                    "schema": {
                        "anyOf": [
                            {"items": {"type": "string"}, "type": "array"},
                            {"type": "null"},
                        ],
                        "title": "P Val Alias",
                    },
                    "name": "p_val_alias",
                    "in": "header",
                }
            ]
        )
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
def optional_list_alias_and_validation_alias_missing(path: str):
    client = TestClient(app)
    response = client.get(path)
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
def optional_list_alias_and_validation_alias_by_name(path: str):
    client = TestClient(app)
    response = client.get(path, headers=[("p", "hello"), ("p", "world")])
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
    response = client.get(path, headers=[("p_alias", "hello"), ("p_alias", "world")])
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
    response = client.get(
        path, headers=[("p_val_alias", "hello"), ("p_val_alias", "world")]
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": ["hello", "world"]})
