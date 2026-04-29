from typing import Annotated

from fastapi import Depends, FastAPI, Path
from fastapi.param_functions import Query
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


@test("Annotated Path/Query defaults raise on registration")
def no_annotated_defaults():
    def _path_default():
        @app.get("/items/{item_id}/")
        async def get_item(item_id: Annotated[int, Path(default=1)]):
            pass  # pragma: nocover

    expect(_path_default, "registering a Path() with default").to_raise(
        AssertionError, match="Path parameters cannot have a default value"
    )

    def _query_default():
        @app.get("/")
        async def get(item_id: Annotated[int, Query(default=1)]):
            pass  # pragma: nocover

    expect(_query_default, "registering a Query() default in Annotated").to_raise(
        AssertionError,
        match=(
            "`Query` default value cannot be set in `Annotated` for 'item_id'. Set the"
            " default value with `=` instead."
        ),
    )


@test("conflicting Annotated/default declarations raise; multi-Query constraints stack")
def multiple_annotations():
    async def dep():
        pass  # pragma: nocover

    @app.get("/multi-query")
    async def get(foo: Annotated[int, Query(gt=2), Query(lt=10)]):
        return foo

    def _depends_in_annotated_with_default():
        @app.get("/")
        async def get2(foo: Annotated[int, Depends(dep)] = Depends(dep)):
            pass  # pragma: nocover

    expect(
        _depends_in_annotated_with_default,
        "Depends in Annotated plus default Depends",
    ).to_raise(
        AssertionError,
        match=(
            "Cannot specify `Depends` in `Annotated` and default value"
            " together for 'foo'"
        ),
    )

    def _fastapi_annotation_with_depends_default():
        @app.get("/")
        async def get3(foo: Annotated[int, Query(min_length=1)] = Depends(dep)):
            pass  # pragma: nocover

    expect(
        _fastapi_annotation_with_depends_default,
        "FastAPI annotation plus Depends default",
    ).to_raise(
        AssertionError,
        match=(
            "Cannot specify a FastAPI annotation in `Annotated` and `Depends` as a"
            " default value together for 'foo'"
        ),
    )

    client = TestClient(app)
    response = client.get("/multi-query", params={"foo": "5"})
    expect(response.status_code, "status code for valid value").to_equal(200).fatal()
    expect(response.json(), "echoed value").to_equal(5)

    response = client.get("/multi-query", params={"foo": "123"})
    expect(response.status_code, "status code for too-large value").to_equal(422)

    response = client.get("/multi-query", params={"foo": "1"})
    expect(response.status_code, "status code for too-small value").to_equal(422)
