from unittest.mock import patch

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test


class Item(BaseModel):
    name: str
    price: float


app = FastAPI()


@app.get("/default")
def get_default() -> Item:
    return Item(name="widget", price=9.99)


@app.get("/explicit", response_class=JSONResponse)
def get_explicit() -> Item:
    return Item(name="widget", price=9.99)


client = TestClient(app)


@test("default response class skips json.dumps via Pydantic fast path")
def default_response_class_skips_json_dumps():
    """When no response_class is set, the fast path serializes directly to
    JSON bytes via Pydantic's dump_json and never calls json.dumps."""
    with patch(
        "starlette.responses.json.dumps", wraps=__import__("json").dumps
    ) as mock_dumps:
        response = client.get("/default")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"name": "widget", "price": 9.99}
    )
    mock_dumps.assert_not_called()


@test("explicit JSONResponse still goes through json.dumps")
def explicit_response_class_uses_json_dumps():
    """When response_class is explicitly set to JSONResponse, the normal path
    is used and json.dumps is called via JSONResponse.render()."""
    with patch(
        "starlette.responses.json.dumps", wraps=__import__("json").dumps
    ) as mock_dumps:
        response = client.get("/explicit")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"name": "widget", "price": 9.99}
    )
    mock_dumps.assert_called_once()
