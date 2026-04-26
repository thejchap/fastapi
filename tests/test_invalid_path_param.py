from fastapi import FastAPI
from pydantic import BaseModel
from tryke import expect, test


@test
def invalid_sequence():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/{id}")
        def read_items(id: list[Item]):
            pass  # pragma: no cover

    expect(_body).to_raise(AssertionError)


@test
def invalid_tuple():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/{id}")
        def read_items(id: tuple[Item, Item]):
            pass  # pragma: no cover

    expect(_body).to_raise(AssertionError)


@test
def invalid_dict():
    def _body():
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/{id}")
        def read_items(id: dict[str, Item]):
            pass  # pragma: no cover

    expect(_body).to_raise(AssertionError)


@test
def invalid_simple_list():
    def _body():
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: list):
            pass  # pragma: no cover

    expect(_body).to_raise(AssertionError)


@test
def invalid_simple_tuple():
    def _body():
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: tuple):
            pass  # pragma: no cover

    expect(_body).to_raise(AssertionError)


@test
def invalid_simple_set():
    def _body():
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: set):
            pass  # pragma: no cover

    expect(_body).to_raise(AssertionError)


@test
def invalid_simple_dict():
    def _body():
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: dict):
            pass  # pragma: no cover

    expect(_body).to_raise(AssertionError)
