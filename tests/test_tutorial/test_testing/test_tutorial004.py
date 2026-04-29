from tryke import test

from docs_src.app_testing.tutorial004_py310 import test_read_items


@test("tutorial004 test_read_items runs")
def main():
    test_read_items()


# Pytest discovered the imported `test_read_items` here at module scope; mirror
# that by re-invoking it under a dedicated tryke test.
@test("tutorial004 re-imported test_read_items runs again")
def read_items():
    test_read_items()
