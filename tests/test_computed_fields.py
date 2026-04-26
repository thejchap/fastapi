from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test


def _client_for(separate_input_output_schemas: bool) -> TestClient:
    app = FastAPI(separate_input_output_schemas=separate_input_output_schemas)

    from pydantic import BaseModel, computed_field

    class Rectangle(BaseModel):
        width: int
        length: int

        @computed_field
        @property
        def area(self) -> int:
            return self.width * self.length

    @app.get("/")
    def read_root() -> Rectangle:
        return Rectangle(width=3, length=4)

    @app.get("/responses", responses={200: {"model": Rectangle}})
    def read_responses() -> Rectangle:
        return Rectangle(width=3, length=4)

    return TestClient(app)


@test.cases(
    test.case("on /", separate_input_output_schemas=True, path="/"),
    test.case("on /responses", separate_input_output_schemas=True, path="/responses"),
    test.case("off /", separate_input_output_schemas=False, path="/"),
    test.case("off /responses", separate_input_output_schemas=False, path="/responses"),
)
def get(separate_input_output_schemas: bool, path: str):
    client = _client_for(separate_input_output_schemas)
    response = client.get(path)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"width": 3, "length": 4, "area": 12})


@test.cases(
    test.case("on", separate_input_output_schemas=True),
    test.case("off", separate_input_output_schemas=False),
)
def openapi_schema(separate_input_output_schemas: bool):
    client = _client_for(separate_input_output_schemas)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
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
                                                "$ref": "#/components/schemas/Rectangle"
                                            }
                                        }
                                    },
                                }
                            },
                        }
                    },
                    "/responses": {
                        "get": {
                            "summary": "Read Responses",
                            "operationId": "read_responses_responses_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Rectangle"
                                            }
                                        }
                                    },
                                }
                            },
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "Rectangle": {
                            "properties": {
                                "width": {"type": "integer", "title": "Width"},
                                "length": {"type": "integer", "title": "Length"},
                                "area": {
                                    "type": "integer",
                                    "title": "Area",
                                    "readOnly": True,
                                },
                            },
                            "type": "object",
                            "required": ["width", "length", "area"],
                            "title": "Rectangle",
                        }
                    }
                },
            }
        )
    )
