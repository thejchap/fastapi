from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()


class JsonApiResponse(JSONResponse):
    media_type = "application/vnd.api+json"


class Error(BaseModel):
    status: str
    title: str


class JsonApiError(BaseModel):
    errors: list[Error]


@app.get(
    "/a/{id}",
    response_class=JsonApiResponse,
    responses={422: {"description": "Error", "model": JsonApiError}},
)
async def a(id):
    pass  # pragma: no cover


client = TestClient(app)


@test("OpenAPI schema uses custom 422 model and media type")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/a/{id}": {
                        "get": {
                            "responses": {
                                "422": {
                                    "description": "Error",
                                    "content": {
                                        "application/vnd.api+json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/JsonApiError"
                                            }
                                        }
                                    },
                                },
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/vnd.api+json": {"schema": {}}
                                    },
                                },
                            },
                            "summary": "A",
                            "operationId": "a_a__id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Id"},
                                    "name": "id",
                                    "in": "path",
                                }
                            ],
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "Error": {
                            "title": "Error",
                            "required": ["status", "title"],
                            "type": "object",
                            "properties": {
                                "status": {"title": "Status", "type": "string"},
                                "title": {"title": "Title", "type": "string"},
                            },
                        },
                        "JsonApiError": {
                            "title": "JsonApiError",
                            "required": ["errors"],
                            "type": "object",
                            "properties": {
                                "errors": {
                                    "title": "Errors",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Error"},
                                }
                            },
                        },
                    }
                },
            }
        )
    )
