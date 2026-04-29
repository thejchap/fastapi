from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


@app.post("/form/python-list")
def post_form_param_list(items: list = Form()):
    return items


@app.post("/form/python-set")
def post_form_param_set(items: set = Form()):
    return items


@app.post("/form/python-tuple")
def post_form_param_tuple(items: tuple = Form()):
    return items


client = TestClient(app)


@test("Form param annotated with builtin list collects values")
def python_list_param_as_form():
    response = client.post(
        "/form/python-list", data={"items": ["first", "second", "third"]}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(["first", "second", "third"])


@test("Form param annotated with builtin set collects values")
def python_set_param_as_form():
    response = client.post(
        "/form/python-set", data={"items": ["first", "second", "third"]}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(set(response.json()), "response as set").to_equal(
        {"first", "second", "third"}
    )


@test("Form param annotated with builtin tuple collects values")
def python_tuple_param_as_form():
    response = client.post(
        "/form/python-tuple", data={"items": ["first", "second", "third"]}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(["first", "second", "third"])
