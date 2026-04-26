from typing import Annotated

from fastapi import Depends, FastAPI, Security
from fastapi.testclient import TestClient
from tryke import Depends as TrykeDepends
from tryke import expect, fixture, test


@fixture
def call_counter() -> dict[str, int]:
    return {"count": 0}


@fixture
def app(call_counter: dict[str, int] = TrykeDepends(call_counter)) -> FastAPI:
    def get_db():
        call_counter["count"] += 1
        return f"db_{call_counter['count']}"

    def get_user(db: Annotated[str, Depends(get_db)]):
        return "user"

    app = FastAPI()

    @app.get("/")
    def endpoint(
        db: Annotated[str, Depends(get_db)],
        user: Annotated[str, Security(get_user, scopes=["read"])],
    ):
        return {"db": db}

    return app


@fixture
def client(app: FastAPI = TrykeDepends(app)) -> TestClient:
    return TestClient(app)


@test
def security_scopes_dependency_called_once(
    client: TestClient = TrykeDepends(client),
    call_counter: dict[str, int] = TrykeDepends(call_counter),
):
    response = client.get("/")

    expect(response.status_code).to_equal(200)
    expect(call_counter["count"]).to_equal(1)
