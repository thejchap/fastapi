from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from tryke import expect, test

app = FastAPI()


class ResponseModel(BaseModel):
    code: int = 200
    message: str = Field(default_factory=lambda: "Successful operation.")


@app.get(
    "/response_model_has_default_factory_return_dict",
    response_model=ResponseModel,
)
async def response_model_has_default_factory_return_dict():
    return {"code": 200}


@app.get(
    "/response_model_has_default_factory_return_model",
    response_model=ResponseModel,
)
async def response_model_has_default_factory_return_model():
    return ResponseModel()


client = TestClient(app)


@test("default_factory fills missing field when handler returns dict")
def response_model_has_default_factory_return_dict():  # noqa: F811
    response = client.get("/response_model_has_default_factory_return_dict")

    expect(response.status_code, "status code").to_equal(200).fatal()

    expect(response.json()["code"], "code field").to_equal(200)
    expect(response.json()["message"], "message field").to_equal("Successful operation.")


@test("default_factory fills missing field when handler returns model")
def response_model_has_default_factory_return_model():  # noqa: F811
    response = client.get("/response_model_has_default_factory_return_model")

    expect(response.status_code, "status code").to_equal(200).fatal()

    expect(response.json()["code"], "code field").to_equal(200)
    expect(response.json()["message"], "message field").to_equal("Successful operation.")
