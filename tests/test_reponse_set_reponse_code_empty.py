from typing import Any

from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()


@app.delete(
    "/{id}",
    status_code=204,
    response_model=None,
)
async def delete_deployment(
    id: int,
    response: Response,
) -> Any:
    response.status_code = 400
    return {"msg": "Status overwritten", "id": id}


client = TestClient(app)


@test("handler can override declared 204 status with body")
def dependency_set_status_code():
    response = client.delete("/1")
    expect(
        response.status_code == 400 and response.content,
        "overridden status with body",
    ).to_be_truthy()
    expect(response.json(), "response body").to_equal(
        {"msg": "Status overwritten", "id": 1}
    )


@test("OpenAPI schema reflects declared 204 status")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/{id}": {
                        "delete": {
                            "summary": "Delete Deployment",
                            "operationId": "delete_deployment__id__delete",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Id", "type": "integer"},
                                    "name": "id",
                                    "in": "path",
                                }
                            ],
                            "responses": {
                                "204": {"description": "Successful Response"},
                                "422": {
                                    "description": "Validation Error",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError"
                                            }
                                        }
                                    },
                                },
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "HTTPValidationError": {
                            "title": "HTTPValidationError",
                            "type": "object",
                            "properties": {
                                "detail": {
                                    "title": "Detail",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    },
                                }
                            },
                        },
                        "ValidationError": {
                            "title": "ValidationError",
                            "required": ["loc", "msg", "type"],
                            "type": "object",
                            "properties": {
                                "loc": {
                                    "title": "Location",
                                    "type": "array",
                                    "items": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "integer"},
                                        ]
                                    },
                                },
                                "msg": {"title": "Message", "type": "string"},
                                "type": {"title": "Error Type", "type": "string"},
                                "input": {"title": "Input"},
                                "ctx": {"title": "Context", "type": "object"},
                            },
                        },
                    }
                },
            }
        )
    )
