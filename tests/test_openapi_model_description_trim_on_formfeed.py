from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()


class MyModel(BaseModel):
    """
    A model with a form feed character in the title.
    \f
    Text after form feed character.
    """


@app.get("/foo")
def foo(v: MyModel):  # pragma: no cover
    pass


client = TestClient(app)


@test("Model description is trimmed at the form-feed character")
def openapi():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    openapi_schema = response.json()

    expect(
        openapi_schema["components"]["schemas"]["MyModel"]["description"],
        "MyModel description",
    ).to_equal("A model with a form feed character in the title.\n")
