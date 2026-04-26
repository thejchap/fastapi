from fastapi import FastAPI, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)


@app.get("/items/")
async def read_items(token: str | None = Security(oauth2_scheme)):
    if token is None:
        return {"msg": "Create an account first"}
    return {"token": token}


client = TestClient(app)


@test
def no_token():
    response = client.get("/items")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"msg": "Create an account first"})


@test
def token():
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"token": "testtoken"})


@test
def incorrect_token():
    response = client.get("/items", headers={"Authorization": "Notexistent testtoken"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"msg": "Create an account first"})


@test
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "security": [{"OAuth2PasswordBearer": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "OAuth2PasswordBearer": {
                            "type": "oauth2",
                            "flows": {"password": {"scopes": {}, "tokenUrl": "/token"}},
                        }
                    }
                },
            }
        )
    )
