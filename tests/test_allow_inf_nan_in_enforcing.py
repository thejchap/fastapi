from typing import Annotated

from fastapi import Body, FastAPI, Query
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


@app.post("/")
async def get(
    x: Annotated[float, Query(allow_inf_nan=True)] = 0,
    y: Annotated[float, Query(allow_inf_nan=False)] = 0,
    z: Annotated[float, Query()] = 0,
    b: Annotated[float, Body(allow_inf_nan=False)] = 0,
) -> str:
    return "OK"


client = TestClient(app)


@test.cases(
    test.case("-1", value="-1", code=200),
    test.case("inf", value="inf", code=200),
    test.case("-inf", value="-inf", code=200),
    test.case("nan", value="nan", code=200),
    test.case("0", value="0", code=200),
    test.case("342", value="342", code=200),
)
def allow_inf_nan_param_true(value: str, code: int):
    response = client.post(f"/?x={value}")
    expect(response.status_code, "status code").to_equal(code)


@test.cases(
    test.case("-1", value="-1", code=200),
    test.case("inf", value="inf", code=422),
    test.case("-inf", value="-inf", code=422),
    test.case("nan", value="nan", code=422),
    test.case("0", value="0", code=200),
    test.case("342", value="342", code=200),
)
def allow_inf_nan_param_false(value: str, code: int):
    response = client.post(f"/?y={value}")
    expect(response.status_code, "status code").to_equal(code)


@test.cases(
    test.case("-1", value="-1", code=200),
    test.case("inf", value="inf", code=200),
    test.case("-inf", value="-inf", code=200),
    test.case("nan", value="nan", code=200),
    test.case("0", value="0", code=200),
    test.case("342", value="342", code=200),
)
def allow_inf_nan_param_default(value: str, code: int):
    response = client.post(f"/?z={value}")
    expect(response.status_code, "status code").to_equal(code)


@test.cases(
    test.case("-1", value="-1", code=200),
    test.case("inf", value="inf", code=422),
    test.case("-inf", value="-inf", code=422),
    test.case("nan", value="nan", code=422),
    test.case("0", value="0", code=200),
    test.case("342", value="342", code=200),
)
def allow_inf_nan_body(value: str, code: int):
    response = client.post("/", json=value)
    expect(response.status_code, "status code").to_equal(code)
