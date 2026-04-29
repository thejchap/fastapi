import warnings

from fastapi import FastAPI
from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.responses import ORJSONResponse, UJSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test

from tests.utils import needs_orjson, needs_ujson

from ._shims import expect_warning

_NEEDS_ORJSON = needs_orjson()
_NEEDS_UJSON = needs_ujson()


class Item(BaseModel):
    name: str
    price: float


# ORJSON


def _make_orjson_app() -> FastAPI:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        app = FastAPI(default_response_class=ORJSONResponse)

    @app.get("/items")
    def get_items() -> Item:
        return Item(name="widget", price=9.99)

    return app


@test("ORJSONResponse still serialises the model body")
@test.skip_if(_NEEDS_ORJSON is not None, reason=_NEEDS_ORJSON or "")
def orjson_response_returns_correct_data():
    app = _make_orjson_app()
    client = TestClient(app)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        response = client.get("/items")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"name": "widget", "price": 9.99}
    )


@test("constructing ORJSONResponse emits deprecation warning")
@test.skip_if(_NEEDS_ORJSON is not None, reason=_NEEDS_ORJSON or "")
def orjson_response_emits_deprecation_warning():
    with expect_warning(
        FastAPIDeprecationWarning, match="ORJSONResponse is deprecated"
    ):
        ORJSONResponse(content={"hello": "world"})


# UJSON


def _make_ujson_app() -> FastAPI:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        app = FastAPI(default_response_class=UJSONResponse)

    @app.get("/items")
    def get_items() -> Item:
        return Item(name="widget", price=9.99)

    return app


@test("UJSONResponse still serialises the model body")
@test.skip_if(_NEEDS_UJSON is not None, reason=_NEEDS_UJSON or "")
def ujson_response_returns_correct_data():
    app = _make_ujson_app()
    client = TestClient(app)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        response = client.get("/items")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"name": "widget", "price": 9.99}
    )


@test("constructing UJSONResponse emits deprecation warning")
@test.skip_if(_NEEDS_UJSON is not None, reason=_NEEDS_UJSON or "")
def ujson_response_emits_deprecation_warning():
    with expect_warning(FastAPIDeprecationWarning, match="UJSONResponse is deprecated"):
        UJSONResponse(content={"hello": "world"})
