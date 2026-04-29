from typing import Any

from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, ConfigDict, Field
from tryke import Depends, expect, fixture, test


@fixture
def client() -> TestClient:
    app = FastAPI()

    class ModelWithRef(BaseModel):
        ref: str = Field(validation_alias="$ref", serialization_alias="$ref")
        model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    @app.get("/", response_model=ModelWithRef)
    async def read_root() -> Any:
        return {"$ref": "some-ref"}

    return TestClient(app)


@test("model with $ref-aliased field serialises by alias")
def get(client: TestClient = Depends(client)):
    response = client.get("/")
    expect(response.json(), "response body").to_equal({"$ref": "some-ref"})


@test("OpenAPI schema preserves $ref-aliased property")
def openapi_schema(client: TestClient = Depends(client)):
    response = client.get("openapi.json")
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/": {
                        "get": {
                            "summary": "Read Root",
                            "operationId": "read_root__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/ModelWithRef"
                                            }
                                        }
                                    },
                                }
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "ModelWithRef": {
                            "properties": {"$ref": {"type": "string", "title": "$Ref"}},
                            "type": "object",
                            "required": ["$ref"],
                            "title": "ModelWithRef",
                        }
                    }
                },
            }
        )
    )
