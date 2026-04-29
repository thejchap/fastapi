from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from tryke import expect, test

app = FastAPI()


class FormModel(BaseModel):
    username: str
    lastname: str
    age: int | None = None
    tags: list[str] = ["foo", "bar"]
    alias_with: str = Field(alias="with", default="nothing")


class FormModelExtraAllow(BaseModel):
    param: str

    model_config = {"extra": "allow"}


@app.post("/form/")
def post_form(user: Annotated[FormModel, Form()]):
    return user


@app.post("/form-extra-allow/")
def post_form_extra_allow(params: Annotated[FormModelExtraAllow, Form()]):
    return params


client = TestClient(app)


@test("Form model populated from a complete form payload")
def send_all_data():
    response = client.post(
        "/form/",
        data={
            "username": "Rick",
            "lastname": "Sanchez",
            "age": "70",
            "tags": ["plumbus", "citadel"],
            "with": "something",
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "username": "Rick",
            "lastname": "Sanchez",
            "age": 70,
            "tags": ["plumbus", "citadel"],
            "with": "something",
        }
    )


@test("Form model uses defaults when optional fields are omitted")
def defaults():
    response = client.post("/form/", data={"username": "Rick", "lastname": "Sanchez"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "username": "Rick",
            "lastname": "Sanchez",
            "age": None,
            "tags": ["foo", "bar"],
            "with": "nothing",
        }
    )


@test("Form model returns 422 with field-level errors on invalid data")
def invalid_data():
    response = client.post(
        "/form/",
        data={
            "username": "Rick",
            "lastname": "Sanchez",
            "age": "seventy",
            "tags": ["plumbus", "citadel"],
        },
    )
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["body", "age"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "seventy",
                }
            ]
        }
    )


@test("Form model returns 422 with missing-field errors when no data is sent")
def no_data():
    response = client.post("/form/")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "username"],
                    "msg": "Field required",
                    "input": {"tags": ["foo", "bar"], "with": "nothing"},
                },
                {
                    "type": "missing",
                    "loc": ["body", "lastname"],
                    "msg": "Field required",
                    "input": {"tags": ["foo", "bar"], "with": "nothing"},
                },
            ]
        }
    )


@test("Form model with extra=allow keeps a single unknown field")
def extra_param_single():
    response = client.post(
        "/form-extra-allow/",
        data={
            "param": "123",
            "extra_param": "456",
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "param": "123",
            "extra_param": "456",
        }
    )


@test("Form model with extra=allow keeps a list of unknown values")
def extra_param_list():
    response = client.post(
        "/form-extra-allow/",
        data={
            "param": "123",
            "extra_params": ["456", "789"],
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "param": "123",
            "extra_params": ["456", "789"],
        }
    )
