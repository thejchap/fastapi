from unittest.mock import patch

from tryke import expect, test

from docs_src.python_types.tutorial006_py310 import process_items


@test
def process_items_prints_each():
    with patch("builtins.print") as mock_print:
        process_items(["item_a", "item_b", "item_c"])

    expect(mock_print.call_count).to_equal(3)
    call_args = [arg.args for arg in mock_print.call_args_list]
    expect(call_args).to_equal(
        [
            ("item_a",),
            ("item_b",),
            ("item_c",),
        ]
    )
