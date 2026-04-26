from typing import Annotated, Any
from unittest.mock import Mock, patch

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.dependencies.tutorial010_py310 import get_db


@test
def get_db_endpoint():
    app = FastAPI()

    @app.get("/")
    def read_root(c: Annotated[Any, Depends(get_db)]):
        return {"c": str(c)}

    client = TestClient(app)

    dbsession_mock = Mock()

    with patch(
        "docs_src.dependencies.tutorial010_py310.DBSession",
        return_value=dbsession_mock,
        create=True,
    ):
        response = client.get("/")

    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"c": str(dbsession_mock)})
