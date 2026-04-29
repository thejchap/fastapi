from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

router = APIRouter()

sub_router = APIRouter()

app = FastAPI()


@sub_router.get("/")
def read_item():
    return {"id": "foo"}


router.include_router(sub_router, prefix="/items")

app.include_router(router)

client = TestClient(app)


@test("nested router path operation returns expected payload")
def path_operation():
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"id": "foo"})


@test("OpenAPI schema matches snapshot")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
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
                            "summary": "Read Item",
                            "operationId": "read_item_items__get",
                        }
                    }
                },
            }
        )
    )
