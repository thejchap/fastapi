from tryke import test

from ..._shims import expect_warning


@test("tutorial003 lifespan event handlers emit DeprecationWarning")
def main():
    with expect_warning(DeprecationWarning):
        from docs_src.app_testing.tutorial003_py310 import test_read_items
    test_read_items()
