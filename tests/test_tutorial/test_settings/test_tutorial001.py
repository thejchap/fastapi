from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial, monkeypatch_ctx


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def settings(name: str):
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
        mod = import_tutorial("settings", name)
        app = mod.app
        client = TestClient(app)
        response = client.get("/info")
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json(), "info response").to_equal(
            {
                "app_name": "Awesome API",
                "admin_email": "admin@example.com",
                "items_per_user": 50,
            }
        )
