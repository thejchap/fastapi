from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

from .utils import needs_py314

if TYPE_CHECKING:  # pragma: no cover

    class DummyUser: ...


_NEEDS_PY314 = needs_py314()


@test.skip_if(_NEEDS_PY314 is not None, reason=_NEEDS_PY314 or "")
def stringified_annotation():
    # python3.14: Use forward reference without "from __future__ import annotations"
    async def get_current_user() -> DummyUser | None:
        return None

    app = FastAPI()

    client = TestClient(app)

    @app.get("/")
    async def get(
        current_user: Annotated[DummyUser | None, Depends(get_current_user)],
    ) -> str:
        return "hello world"

    response = client.get("/")
    expect(response.status_code).to_equal(200)
