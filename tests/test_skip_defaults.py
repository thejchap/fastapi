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


@test
def return_defaults():
    response = client.get("/")
    expect(response.json()).to_equal({"sub": {}})


@test
def return_exclude_unset():
    response = client.get("/exclude_unset")
    expect(response.json()).to_equal({"x": None, "y": "y"})


@test
def return_exclude_defaults():
    response = client.get("/exclude_defaults")
    expect(response.json()).to_equal({})


@test
def return_exclude_none():
    response = client.get("/exclude_none")
    expect(response.json()).to_equal({"y": "y", "z": "z"})


@test
def return_exclude_unset_none():
    response = client.get("/exclude_unset_none")
    expect(response.json()).to_equal({"y": "y"})
