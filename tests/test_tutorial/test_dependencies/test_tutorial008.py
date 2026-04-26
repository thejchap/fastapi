import sys
from typing import Annotated, Any
from unittest.mock import Mock, patch

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _module_for(name: str):
    return import_tutorial("dependencies", name)


@test.cases(
    test.case("tutorial008_py310", name="tutorial008_py310"),
    test.case(
        "tutorial008_an_py310",
        name="tutorial008_an_py310",
        # Original pytest skipped via `xfail` for py<3.14; we keep the
        # case but skip if the runtime cannot evaluate Annotated forwardref.
        skip="Fails with `NameError: name 'DepA' is not defined`"
        if sys.version_info < (3, 14)
        else None,
    ),
)
def get_db(name: str):
    module = _module_for(name)
    app = FastAPI()

    @app.get("/")
    def read_root(c: Annotated[Any, Depends(module.dependency_c)]):
        return {"c": str(c)}

    client = TestClient(app)

    a_mock = Mock()
    b_mock = Mock()
    c_mock = Mock()

    with (
        patch(
            f"{module.__name__}.generate_dep_a",
            return_value=a_mock,
            create=True,
        ),
        patch(
            f"{module.__name__}.generate_dep_b",
            return_value=b_mock,
            create=True,
        ),
        patch(
            f"{module.__name__}.generate_dep_c",
            return_value=c_mock,
            create=True,
        ),
    ):
        response = client.get("/")

    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"c": str(c_mock)})
