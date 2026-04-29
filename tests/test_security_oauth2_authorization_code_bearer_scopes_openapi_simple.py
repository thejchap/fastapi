# Ref: https://github.com/fastapi/fastapi/issues/14454

from typing import Annotated

from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="api/oauth/authorize",
    tokenUrl="/api/oauth/token",
    scopes={"read": "Read access", "write": "Write access"},
)


async def get_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token


app = FastAPI(dependencies=[Depends(get_token)])


@app.get("/admin", dependencies=[Security(get_token, scopes=["read", "write"])])
async def read_admin():
    return {"message": "Admin Access"}


client = TestClient(app)


@test("Admin endpoint accepts Bearer token with required scopes")
def read_admin():
    response = client.get("/admin", headers={"Authorization": "Bearer faketoken"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Admin Access"})


@test("OpenAPI schema reflects scoped OAuth2 security requirements")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/admin": {
                        "get": {
                            "summary": "Read Admin",
                            "operationId": "read_admin_admin_get",
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
                    }
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
                                    "authorizationUrl": "api/oauth/authorize",
                                    "tokenUrl": "/api/oauth/token",
                                }
                            },
                        }
                    }
                },
            }
        )
    )
