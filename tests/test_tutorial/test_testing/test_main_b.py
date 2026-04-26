from tryke import test

from ..._shims import import_tutorial


@test.cases(
    test.case("app_b_py310", name="app_b_py310.test_main"),
    test.case("app_b_an_py310", name="app_b_an_py310.test_main"),
)
def app(name: str):
    test_main = import_tutorial("app_testing", name)
    test_main.test_create_existing_item()
    test_main.test_create_item()
    test_main.test_create_item_bad_token()
    test_main.test_read_nonexistent_item()
    test_main.test_read_item()
    test_main.test_read_item_bad_token()
