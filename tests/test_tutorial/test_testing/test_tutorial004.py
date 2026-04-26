from tryke import test

from docs_src.app_testing.tutorial004_py310 import test_read_items


@test
def main():
    test_read_items()


# Pytest discovered the imported `test_read_items` here at module scope; mirror
# that by re-invoking it under a dedicated tryke test.
@test
def read_items():
    test_read_items()
