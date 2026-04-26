from unittest.mock import patch

from tryke import expect, test

from ..._shims import import_tutorial


@test.cases(
    test.case("tutorial008b_py310", name="tutorial008b_py310"),
    test.case("tutorial008b_py310 (alt)", name="tutorial008b_py310"),
)
def process_items(name: str):
    module = import_tutorial("python_types", name)
    with patch("builtins.print") as mock_print:
        module.process_item("a")

    expect(mock_print.call_count).to_equal(1)
    mock_print.assert_called_with("a")
