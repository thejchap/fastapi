import runpy
from unittest.mock import patch

from tryke import expect, test


@test.cases(
    test.case("tutorial011_py310", module_name="tutorial011_py310"),
)
def run_module(module_name: str):
    with patch("builtins.print") as mock_print:
        runpy.run_module(f"docs_src.python_types.{module_name}", run_name="__main__")

    expect(mock_print.call_count, "print call count").to_equal(2)
    call_args = [str(arg.args[0]) for arg in mock_print.call_args_list]
    expect(call_args, "captured print call args").to_equal(
        [
            "id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]",
            "123",
        ]
    )
