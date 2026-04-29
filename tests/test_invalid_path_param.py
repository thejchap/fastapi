from fastapi import FastAPI
from pydantic import BaseModel
from tryke import expect, test


@test("Path param of list[Model] is rejected")
def invalid_sequence():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/{id}")
        def read_items(id: list[Item]):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(AssertionError)


@test("Path param of tuple[Model, Model] is rejected")
def invalid_tuple():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/{id}")
        def read_items(id: tuple[Item, Item]):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(AssertionError)


@test("Path param of dict[str, Model] is rejected")
def invalid_dict():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/{id}")
        def read_items(id: dict[str, Item]):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(AssertionError)


@test("Path param of bare list is rejected")
def invalid_simple_list():
    def _body():
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: list):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(AssertionError)


@test("Path param of bare tuple is rejected")
def invalid_simple_tuple():
    def _body():
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: tuple):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(AssertionError)


@test("Path param of bare set is rejected")
def invalid_simple_set():
    def _body():
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: set):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(AssertionError)


@test("Path param of bare dict is rejected")
def invalid_simple_dict():
    def _body():
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: dict):
            pass  # pragma: no cover

    expect(_body, "registering the route").to_raise(AssertionError)
