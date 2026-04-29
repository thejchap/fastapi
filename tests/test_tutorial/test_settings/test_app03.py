import importlib
from types import ModuleType

from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import monkeypatch_ctx


def _main_mod(name: str) -> ModuleType:
    return importlib.import_module(f"docs_src.settings.{name}.main")


@test.cases(
    test.case("app03_py310", name="app03_py310"),
    test.case("app03_an_py310", name="app03_an_py310"),
)
def settings(name: str):
    main_mod = _main_mod(name)
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
        settings = main_mod.get_settings()
        expect(settings.app_name, "settings.app_name").to_equal("Awesome API")
        expect(settings.admin_email, "settings.admin_email").to_equal(
            "admin@example.com"
        )
        expect(settings.items_per_user, "settings.items_per_user").to_equal(50)


@test.cases(
    test.case("app03_py310", name="app03_py310"),
    test.case("app03_an_py310", name="app03_an_py310"),
)
def endpoint(name: str):
    main_mod = _main_mod(name)
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
        client = TestClient(main_mod.app)
        response = client.get("/info")
        expect(response.status_code, "status code").to_equal(200)
        expect(response.json(), "info response").to_equal(
            {
                "app_name": "Awesome API",
                "admin_email": "admin@example.com",
                "items_per_user": 50,
            }
        )
