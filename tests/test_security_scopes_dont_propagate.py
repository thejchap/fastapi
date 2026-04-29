# Ref: https://github.com/tiangolo/fastapi/issues/5623

from typing import Annotated, Any

from fastapi import FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient
from tryke import expect, test


async def security1(scopes: SecurityScopes):
    return scopes.scopes


async def security2(scopes: SecurityScopes):
    return scopes.scopes


async def dep3(
    dep1: Annotated[list[str], Security(security1, scopes=["scope1"])],
    dep2: Annotated[list[str], Security(security2, scopes=["scope2"])],
):
    return {"dep1": dep1, "dep2": dep2}


app = FastAPI()


@app.get("/scopes")
def get_scopes(
    dep3: Annotated[dict[str, Any], Security(dep3, scopes=["scope3"])],
):
    return dep3


client = TestClient(app)


@test("Sibling Security dependencies do not see each other's scopes")
def security_scopes_dont_propagate():
    response = client.get("/scopes")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {
            "dep1": ["scope3", "scope1"],
            "dep2": ["scope3", "scope2"],
        }
    )
