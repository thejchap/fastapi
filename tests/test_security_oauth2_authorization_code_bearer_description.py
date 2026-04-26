from fastapi import FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="authorize",
    tokenUrl="token",
    description="OAuth2 Code Bearer",
    auto_error=True,
)


@app.get("/items/")
async def read_items(token: str | None = Security(oauth2_scheme)):
    return {"token": token}


client = TestClient(app)


@test
def no_token():
    response = client.get("/items")
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})


@test
def incorrect_token():
    response = client.get("/items", headers={"Authorization": "Non-existent testtoken"})
    expect(response.status_code).to_equal(401).fatal()
    expect(response.json()).to_equal({"detail": "Not authenticated"})


@test
def token():
    response = client.get("/items", headers={"Authorization": "Bearer testtoken"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"token": "testtoken"})


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
                            "security": [{"OAuth2AuthorizationCodeBearer": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "OAuth2AuthorizationCodeBearer": {
                            "type": "oauth2",
                            "flows": {
                                "authorizationCode": {
                                    "authorizationUrl": "authorize",
                                    "tokenUrl": "token",
                                    "scopes": {},
                                }
                            },
                            "description": "OAuth2 Code Bearer",
                        }
                    }
                },
            }
        )
    )
