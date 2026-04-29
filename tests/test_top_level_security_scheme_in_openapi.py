# Test security scheme at the top level, including OpenAPI
# Ref: https://github.com/fastapi/fastapi/discussions/14263
# Ref: https://github.com/fastapi/fastapi/issues/14271
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()

bearer_scheme = HTTPBearer()


@app.get("/", dependencies=[Depends(bearer_scheme)])
async def get_root():
    return {"message": "Hello, World!"}


client = TestClient(app)


@test("Top-level Bearer dependency authorises GET /")
def get_root_ok():
    response = client.get("/", headers={"Authorization": "Bearer token"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Hello, World!"})


@test("Top-level Bearer dependency rejects unauthenticated GET /")
def get_root_no_token():
    response = client.get("/")
    expect(response.status_code, "status code").to_equal(401).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Not authenticated"})


@test("Top-level security scheme appears in OpenAPI schema")
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
                            "summary": "Get Root",
                            "operationId": "get_root__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "security": [{"HTTPBearer": []}],
                        }
                    }
                },
                "components": {
                    "securitySchemes": {
                        "HTTPBearer": {"type": "http", "scheme": "bearer"}
                    }
                },
            }
        )
    )
