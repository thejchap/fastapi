from fastapi import FastAPI, Query
from pydantic import BaseModel
from tryke import expect, test


@test("Query param of list[Model] is rejected")
def invalid_sequence():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/")
        def read_items(q: list[Item] = Query(default=None)):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(
        AssertionError,
        match="Query parameter 'q' must be one of the supported types",
    )


@test("Query param of tuple[Model, Model] is rejected")
def invalid_tuple():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/")
        def read_items(q: tuple[Item, Item] = Query(default=None)):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(
        AssertionError,
        match="Query parameter 'q' must be one of the supported types",
    )


@test("Query param of dict[str, Model] is rejected")
def invalid_dict():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/")
        def read_items(q: dict[str, Item] = Query(default=None)):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(
        AssertionError,
        match="Query parameter 'q' must be one of the supported types",
    )


@test("Query param of bare dict is rejected")
def invalid_simple_dict():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/")
        def read_items(q: dict | None = Query(default=None)):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(
        AssertionError,
        match="Query parameter 'q' must be one of the supported types",
    )
