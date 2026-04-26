from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient
from tryke import expect, test

from .utils import needs_py310


class Dep:
    def __call__(self, request: Request):
        return "test"


_NEEDS_PY310 = needs_py310()


@test.skip_if(_NEEDS_PY310 is not None, reason=_NEEDS_PY310 or "")
def stringified_annotations():
    app = FastAPI()

    client = TestClient(app)

    @app.get("/test/")
    def call(test: Annotated[str, Depends(Dep())]):
        return {"test": test}

    response = client.get("/test")
    expect(response.status_code).to_equal(200)
