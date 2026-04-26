from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test


async def some_value() -> int:
    return 123


type DependedValue = Annotated[int, Depends(some_value)]


@test
def pep695_type_dependencies():
    app = FastAPI()

    @app.get("/")
    async def get_with_dep(value: DependedValue) -> str:  # noqa
        return f"value: {value}"

    client = TestClient(app)
    response = client.get("/")
    expect(response.status_code).to_equal(200)
    expect(response.text).to_equal('"value: 123"')
