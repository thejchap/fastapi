from unittest.mock import patch

from tryke import expect, test

from ..._shims import import_tutorial


@test.cases(
    test.case("tutorial009_py310", name="tutorial009_py310"),
    test.case("tutorial009_py310 (alt)", name="tutorial009_py310"),
)
def say_hi(name: str):
    module = import_tutorial("python_types", name)
    with patch("builtins.print") as mock_print:
        module.say_hi("FastAPI")
        module.say_hi()

    expect(mock_print.call_count).to_equal(2)
    call_args = [arg.args for arg in mock_print.call_args_list]
    expect(call_args).to_equal(
        [
            ("Hey FastAPI!",),
            ("Hello World",),
        ]
    )
