from typing import Annotated

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, WithJsonSchema
from tryke import expect, test

app = FastAPI()


class Item(BaseModel):
    name: str

    description: Annotated[str | None, WithJsonSchema({"type": ["string", "null"]})] = (
        None
    )

    model_config = {
        "json_schema_extra": {
            "x-something-internal": {"level": 4},
        }
    }


@app.get("/foo", response_model=Item)
def foo():
    return {"name": "Foo item"}


client = TestClient(app)


item_schema = {
    "title": "Item",
    "required": ["name"],
    "type": "object",
    "x-something-internal": {
        "level": 4,
    },
    "properties": {
        "name": {
            "title": "Name",
            "type": "string",
        },
        "description": {
            "title": "Description",
            "type": ["string", "null"],
        },
    },
}


@test("custom WithJsonSchema and json_schema_extra appear in OpenAPI schema")
def custom_response_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(
        response.json()["components"]["schemas"]["Item"],
        "Item component schema",
    ).to_equal(item_schema)


@test("GET /foo returns the Item with description defaulted to None")
def response():
    # For coverage
    response = client.get("/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"name": "Foo item", "description": None}
    )
