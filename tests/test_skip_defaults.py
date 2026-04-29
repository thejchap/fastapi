from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()


class SubModel(BaseModel):
    a: str | None = "foo"


class Model(BaseModel):
    x: int | None = None
    sub: SubModel


class ModelSubclass(Model):
    y: int
    z: int = 0
    w: int | None = None


class ModelDefaults(BaseModel):
    w: str | None = None
    x: str | None = None
    y: str = "y"
    z: str = "z"


@app.get("/", response_model=Model, response_model_exclude_unset=True)
def get_root() -> ModelSubclass:
    return ModelSubclass(sub={}, y=1, z=0)


@app.get(
    "/exclude_unset", response_model=ModelDefaults, response_model_exclude_unset=True
)
def get_exclude_unset() -> ModelDefaults:
    return ModelDefaults(x=None, y="y")


@app.get(
    "/exclude_defaults",
    response_model=ModelDefaults,
    response_model_exclude_defaults=True,
)
def get_exclude_defaults() -> ModelDefaults:
    return ModelDefaults(x=None, y="y")


@app.get(
    "/exclude_none", response_model=ModelDefaults, response_model_exclude_none=True
)
def get_exclude_none() -> ModelDefaults:
    return ModelDefaults(x=None, y="y")


@app.get(
    "/exclude_unset_none",
    response_model=ModelDefaults,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
def get_exclude_unset_none() -> ModelDefaults:
    return ModelDefaults(x=None, y="y")


client = TestClient(app)


@test("response_model_exclude_unset omits unset fields including subclass extras")
def return_defaults():
    response = client.get("/")
    expect(response.json(), "response body").to_equal({"sub": {}})


@test("response_model_exclude_unset keeps explicitly set fields")
def return_exclude_unset():
    response = client.get("/exclude_unset")
    expect(response.json(), "response body").to_equal({"x": None, "y": "y"})


@test("response_model_exclude_defaults drops fields equal to defaults")
def return_exclude_defaults():
    response = client.get("/exclude_defaults")
    expect(response.json(), "response body").to_equal({})


@test("response_model_exclude_none drops only None-valued fields")
def return_exclude_none():
    response = client.get("/exclude_none")
    expect(response.json(), "response body").to_equal({"y": "y", "z": "z"})


@test("Combining exclude_unset and exclude_none drops both")
def return_exclude_unset_none():
    response = client.get("/exclude_unset_none")
    expect(response.json(), "response body").to_equal({"y": "y"})
