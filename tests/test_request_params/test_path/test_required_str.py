from typing import Annotated

from fastapi import FastAPI, Path
from fastapi.testclient import TestClient
from inline_snapshot import Is, snapshot
from tryke import expect, test

app = FastAPI()


@app.get("/required-str/{p}")
async def read_required_str(p: Annotated[str, Path()]):
    return {"p": p}


@app.get("/required-alias/{p_alias}")
async def read_required_alias(p: Annotated[str, Path(alias="p_alias")]):
    return {"p": p}


@app.get("/required-validation-alias/{p_val_alias}")
def read_required_validation_alias(
    p: Annotated[str, Path(validation_alias="p_val_alias")],
):
    return {"p": p}


@app.get("/required-alias-and-validation-alias/{p_val_alias}")
def read_required_alias_and_validation_alias(
    p: Annotated[str, Path(alias="p_alias", validation_alias="p_val_alias")],
):
    return {"p": p}


@test.cases(
    test.case(
        "required-str", path="/required-str/{p}", expected_name="p", expected_title="P"
    ),
    test.case(
        "required-alias",
        path="/required-alias/{p_alias}",
        expected_name="p_alias",
        expected_title="P Alias",
    ),
    test.case(
        "required-validation-alias",
        path="/required-validation-alias/{p_val_alias}",
        expected_name="p_val_alias",
        expected_title="P Val Alias",
    ),
    test.case(
        "required-alias-and-validation-alias",
        path="/required-alias-and-validation-alias/{p_val_alias}",
        expected_name="p_val_alias",
        expected_title="P Val Alias",
    ),
)
def schema(path: str, expected_name: str, expected_title: str):
    expect(
        app.openapi()["paths"][path]["get"]["parameters"],
        "openapi parameters",
    ).to_equal(
        snapshot(
            [
                {
                    "required": True,
                    "schema": {"title": Is(expected_title), "type": "string"},
                    "name": Is(expected_name),
                    "in": "path",
                }
            ]
        )
    )


@test.cases(
    test.case("required-str", path="/required-str"),
    test.case("required-alias", path="/required-alias"),
    test.case("required-validation-alias", path="/required-validation-alias"),
    test.case(
        "required-alias-and-validation-alias",
        path="/required-alias-and-validation-alias",
    ),
)
def success(path: str):
    client = TestClient(app)
    response = client.get(f"{path}/hello")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"p": "hello"})
