# Ref: https://github.com/fastapi/fastapi/issues/14454

from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="authorize",
    tokenUrl="token",
    auto_error=True,
    scopes={"read": "Read access", "write": "Write access"},
)


async def get_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token


app = FastAPI(dependencies=[Depends(get_token)])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/with-oauth2-scheme",
    dependencies=[Security(oauth2_scheme, scopes=["read", "write"])],
)
async def read_with_oauth2_scheme():
    return {"message": "Admin Access"}


@app.get(
    "/with-get-token", dependencies=[Security(get_token, scopes=["read", "write"])]
)
async def read_with_get_token():
    return {"message": "Admin Access"}


router = APIRouter(dependencies=[Security(oauth2_scheme, scopes=["read"])])


@router.get("/items/")
async def read_items(token: str | None = Depends(oauth2_scheme)):
    return {"token": token}


@router.post("/items/")
async def create_item(
    token: str | None = Security(oauth2_scheme, scopes=["read", "write"]),
):
    return {"token": token}


app.include_router(router)

client = TestClient(app)


@test("App-level OAuth2 dependency authorises root request")
def root_test():
    response = client.get("/", headers={"Authorization": "Bearer testtoken"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Hello World"})


@test("Endpoint with Security(oauth2_scheme) accepts Bearer token")
def read_with_oauth2_scheme():
    response = client.get(
        "/with-oauth2-scheme", headers={"Authorization": "Bearer testtoken"}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Admin Access"})


@test("Endpoint with Security(get_token) accepts Bearer token")
def read_with_get_token():
    response = client.get(
        "/with-get-token", headers={"Authorization": "Bearer testtoken"}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Admin Access"})


@test("Router GET /items/ resolves token via OAuth2 dependency")
def read_token():
    response = client.get("/items/", headers={"Authorization": "Bearer testtoken"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"token": "testtoken"})


@test("Router POST /items/ resolves token with read+write scopes")
def create_token():
    response = client.post("/items/", headers={"Authorization": "Bearer testtoken"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"token": "testtoken"})


@test("OpenAPI schema reflects per-route OAuth2 scopes")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/": {
                        "get": {
                            "summary": "Root",
                            "operationId": "root__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "security": [{"OAuth2AuthorizationCodeBearer": []}],
                        }
                    },
                    "/with-oauth2-scheme": {
                        "get": {
                            "summary": "Read With Oauth2 Scheme",
                            "operationId": "read_with_oauth2_scheme_with_oauth2_scheme_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "security": [
                                {"OAuth2AuthorizationCodeBearer": ["read", "write"]}
                            ],
                        }
                    },
                    "/with-get-token": {
                        "get": {
                            "summary": "Read With Get Token",
                            "operationId": "read_with_get_token_with_get_token_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "security": [
                                {"OAuth2AuthorizationCodeBearer": ["read", "write"]}
                            ],
                        }
                    },
                    "/items/": {
                        "get": {
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "security": [
                                {"OAuth2AuthorizationCodeBearer": ["read"]},
                            ],
                        },
                        "post": {
                            "summary": "Create Item",
                            "operationId": "create_item_items__post",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "security": [
                                {"OAuth2AuthorizationCodeBearer": ["read", "write"]},
                            ],
                        },
                    },
                },
                "components": {
                    "securitySchemes": {
                        "OAuth2AuthorizationCodeBearer": {
                            "type": "oauth2",
                            "flows": {
                                "authorizationCode": {
                                    "scopes": {
                                        "read": "Read access",
                                        "write": "Write access",
                                    },
                                    "authorizationUrl": "authorize",
                                    "tokenUrl": "token",
                                }
                            },
                        }
                    }
                },
            }
        )
    )
