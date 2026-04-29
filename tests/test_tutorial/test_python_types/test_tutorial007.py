from tryke import expect, test

from docs_src.python_types.tutorial007_py310 import process_items


@test("process_items returns the input pair")
def process_items_returns_pair():
    items_t = (1, 2, "foo")
    items_s = {b"a", b"b", b"c"}

    expect(
        process_items(items_t, items_s), "process_items result"
    ).to_equal((items_t, items_s))
