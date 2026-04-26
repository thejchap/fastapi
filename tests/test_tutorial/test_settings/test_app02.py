import importlib
from types import ModuleType

from tryke import expect, test

from ..._shims import monkeypatch_ctx


def _mod_path(name: str) -> str:
    return f"docs_src.settings.{name}"


def _main_mod(name: str) -> ModuleType:
    return importlib.import_module(f"{_mod_path(name)}.main")


def _test_main_mod(name: str) -> ModuleType:
    return importlib.import_module(f"{_mod_path(name)}.test_main")


@test.cases(
    test.case("app02_py310", name="app02_py310"),
    test.case("app02_an_py310", name="app02_an_py310"),
)
def settings(name: str):
    main_mod = _main_mod(name)
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
        settings = main_mod.get_settings()
        expect(settings.app_name).to_equal("Awesome API")
        expect(settings.items_per_user).to_equal(50)


@test.cases(
    test.case("app02_py310", name="app02_py310"),
    test.case("app02_an_py310", name="app02_an_py310"),
)
def override_settings(name: str):
    test_main_mod = _test_main_mod(name)
    test_main_mod.test_app()
