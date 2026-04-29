from fastapi import FastAPI
from fastapi.exceptions import FastAPIError
from tryke import expect, test


class NonPydanticModel:
    pass


@test("non-Pydantic response_model raises FastAPIError")
def invalid_response_model_raises():
    def _body() -> None:
        app = FastAPI()

        @app.get("/", response_model=NonPydanticModel)
        def read_root():
            pass  # pragma: nocover

    expect(_body, "registering route with non-Pydantic response_model").to_raise(
        FastAPIError
    )


@test("non-Pydantic sub-type response_model raises FastAPIError")
def invalid_response_model_sub_type_raises():
    def _body() -> None:
        app = FastAPI()

        @app.get("/", response_model=list[NonPydanticModel])
        def read_root():
            pass  # pragma: nocover

    expect(
        _body, "registering route with non-Pydantic response_model sub-type"
    ).to_raise(FastAPIError)


@test("non-Pydantic responses[].model raises FastAPIError")
def invalid_response_model_in_responses_raises():
    def _body() -> None:
        app = FastAPI()

        @app.get("/", responses={"500": {"model": NonPydanticModel}})
        def read_root():
            pass  # pragma: nocover

    expect(
        _body, "registering route with non-Pydantic responses[].model"
    ).to_raise(FastAPIError)


@test("non-Pydantic sub-type responses[].model raises FastAPIError")
def invalid_response_model_sub_type_in_responses_raises():
    def _body() -> None:
        app = FastAPI()

        @app.get("/", responses={"500": {"model": list[NonPydanticModel]}})
        def read_root():
            pass  # pragma: nocover

    expect(
        _body, "registering route with non-Pydantic responses[].model sub-type"
    ).to_raise(FastAPIError)
