from tryke import expect, test

from docs_src.python_types.tutorial005_py310 import get_items


@test("get_items returns a tuple")
def get_items_returns_tuple():
    res = get_items(
        "item_a",
        "item_b",
        "item_c",
        "item_d",
        "item_e",
    )
    expect(res, "get_items result").to_equal(
        ("item_a", "item_b", "item_c", "item_d", "item_e")
    )
