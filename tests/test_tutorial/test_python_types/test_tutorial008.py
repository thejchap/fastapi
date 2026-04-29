from unittest.mock import patch

from tryke import expect, test

from docs_src.python_types.tutorial008_py310 import process_items


@test("process_items prints keys and values")
def process_items_prints_keys_and_values():
    with patch("builtins.print") as mock_print:
        process_items({"a": 1.0, "b": 2.5})

    expect(mock_print.call_count, "print call count").to_equal(4)
    call_args = [arg.args for arg in mock_print.call_args_list]
    expect(call_args, "captured print call args").to_equal(
        [
            ("a",),
            (1.0,),
            ("b",),
            (2.5,),
        ]
    )
