from fastapi.exceptions import FastAPIError
from tryke import expect, test

from ..._shims import import_tutorial


@test.cases(
    test.case("tutorial003_04_py310", module_name="tutorial003_04_py310"),
)
def invalid_response_model(module_name: str) -> None:
    expect(lambda: import_tutorial("response_model", module_name)).to_raise(
        FastAPIError
    )
