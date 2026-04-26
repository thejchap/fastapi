from tryke import test

from docs_src.app_testing.tutorial004_py310 import test_read_items


@test
def main():
    test_read_items()
