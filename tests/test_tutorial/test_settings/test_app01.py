import importlib
import sys

from dirty_equals import IsAnyStr
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import ValidationError
from tryke import expect, test

from ..._shims import monkeypatch_ctx


def _mod_name(name: str) -> str:
    return f"docs_src.settings.{name}.main"


@test.cases(
    test.case("app01_py310", name="app01_py310"),
)
def settings_validation_error(name: str):
    mod_name = _mod_name(name)
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.delenv("ADMIN_EMAIL", raising=False)
        if mod_name in sys.modules:
            del sys.modules[mod_name]

        caught: ValidationError | None = None
        try:
            importlib.import_module(mod_name)
        except ValidationError as exc:
            caught = exc
        expect(caught).not_.to_be_none().fatal()
        assert caught is not None
        expect(caught.errors()).to_equal(
            [
                {
                    "loc": ("admin_email",),
                    "msg": "Field required",
                    "type": "missing",
                    "input": {},
                    "url": IsAnyStr,
                }
            ]
        )


@test.cases(
    test.case("app01_py310", name="app01_py310"),
)
def app(name: str):
    mod_name = _mod_name(name)
    with monkeypatch_ctx() as monkeypatch:
        if mod_name in sys.modules:
            del sys.modules[mod_name]
        monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
        main_mod = importlib.import_module(mod_name)
        client = TestClient(main_mod.app)

        response = client.get("/info")
        data = response.json()
        expect(data).to_equal(
            {
                "app_name": "Awesome API",
                "admin_email": "admin@example.com",
                "items_per_user": 50,
            }
        )


@test.cases(
    test.case("app01_py310", name="app01_py310"),
)
def openapi_schema(name: str):
    mod_name = _mod_name(name)
    with monkeypatch_ctx() as monkeypatch:
        if mod_name in sys.modules:
            del sys.modules[mod_name]
        monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
        main_mod = importlib.import_module(mod_name)
        client = TestClient(main_mod.app)

        response = client.get("/openapi.json")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal(
            snapshot(
                {
                    "openapi": "3.1.0",
                    "info": {"title": "FastAPI", "version": "0.1.0"},
                    "paths": {
                        "/info": {
                            "get": {
                                "operationId": "info_info_get",
                                "responses": {
                                    "200": {
                                        "description": "Successful Response",
                                        "content": {"application/json": {"schema": {}}},
                                    }
                                },
                                "summary": "Info",
                            }
                        }
                    },
                }
            )
        )
