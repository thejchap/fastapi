from typing import Annotated

from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test


@fixture
def client() -> TestClient:
    from pydantic import (
        BaseModel,
        ConfigDict,
        PlainSerializer,
        TypeAdapter,
        WithJsonSchema,
    )

    class FakeNumpyArray:
        def __init__(self):
            self.data = [1.0, 2.0, 3.0]

    FakeNumpyArrayPydantic = Annotated[
        FakeNumpyArray,
        WithJsonSchema(TypeAdapter(list[float]).json_schema()),
        PlainSerializer(lambda v: v.data),
    ]

    class MyModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
        custom_field: FakeNumpyArrayPydantic

    app = FastAPI()

    @app.get("/")
    def test() -> MyModel:
        return MyModel(custom_field=FakeNumpyArray())

    return TestClient(app)


@test
def get(client: TestClient = Depends(client)):
    response = client.get("/")
    expect(response.json()).to_equal({"custom_field": [1.0, 2.0, 3.0]})


@test
def typeadapter():
    # This test is only to confirm that Pydantic alone is working as expected
    from pydantic import (
        BaseModel,
        ConfigDict,
        PlainSerializer,
        TypeAdapter,
        WithJsonSchema,
    )

    class FakeNumpyArray:
        def __init__(self):
            self.data = [1.0, 2.0, 3.0]

    FakeNumpyArrayPydantic = Annotated[
        FakeNumpyArray,
        WithJsonSchema(TypeAdapter(list[float]).json_schema()),
        PlainSerializer(lambda v: v.data),
    ]

    class MyModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
        custom_field: FakeNumpyArrayPydantic

    ta = TypeAdapter(MyModel)
    expect(ta.dump_python(MyModel(custom_field=FakeNumpyArray()))).to_equal(
        {"custom_field": [1.0, 2.0, 3.0]}
    )
    expect(ta.json_schema()).to_equal(
        snapshot(
            {
                "properties": {
                    "custom_field": {
                        "items": {"type": "number"},
                        "title": "Custom Field",
                        "type": "array",
                    }
                },
                "required": ["custom_field"],
                "title": "MyModel",
                "type": "object",
            }
        )
    )


@test
def openapi_schema(client: TestClient = Depends(client)):
    response = client.get("openapi.json")
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/": {
                        "get": {
                            "summary": "Test",
                            "operationId": "test__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/MyModel"
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
                        "MyModel": {
                            "properties": {
                                "custom_field": {
                                    "items": {"type": "number"},
                                    "type": "array",
                                    "title": "Custom Field",
                                }
                            },
                            "type": "object",
                            "required": ["custom_field"],
                            "title": "MyModel",
                        }
                    }
                },
            }
        )
    )
