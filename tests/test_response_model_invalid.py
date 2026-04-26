from fastapi import FastAPI
from fastapi.exceptions import FastAPIError
from tryke import expect, test


class NonPydanticModel:
    pass


@test
def invalid_response_model_raises():
    def _body() -> None:
        app = FastAPI()

        @app.get("/", response_model=NonPydanticModel)
        def read_root():
            pass  # pragma: nocover

    expect(_body).to_raise(FastAPIError)


@test
def invalid_response_model_sub_type_raises():
    def _body() -> None:
        app = FastAPI()

        @app.get("/", response_model=list[NonPydanticModel])
        def read_root():
            pass  # pragma: nocover

    expect(_body).to_raise(FastAPIError)


@test
def invalid_response_model_in_responses_raises():
    def _body() -> None:
        app = FastAPI()

        @app.get("/", responses={"500": {"model": NonPydanticModel}})
        def read_root():
            pass  # pragma: nocover

    expect(_body).to_raise(FastAPIError)


@test
def invalid_response_model_sub_type_in_responses_raises():
    def _body() -> None:
        app = FastAPI()

        @app.get("/", responses={"500": {"model": list[NonPydanticModel]}})
        def read_root():
            pass  # pragma: nocover

    expect(_body).to_raise(FastAPIError)
