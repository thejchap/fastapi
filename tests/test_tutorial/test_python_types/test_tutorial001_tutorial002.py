import runpy
from unittest.mock import patch

from tryke import test


@test.cases(
    test.case("tutorial001_py310", module_name="tutorial001_py310"),
    test.case("tutorial002_py310", module_name="tutorial002_py310"),
)
def run_module(module_name: str):
    with patch("builtins.print") as mock_print:
        runpy.run_module(f"docs_src.python_types.{module_name}", run_name="__main__")

    mock_print.assert_called_with("John Doe")
