from tryke import test

from docs_src.app_testing.tutorial002_py310 import test_read_main, test_websocket


@test
def main():
    test_read_main()


@test
def ws():
    test_websocket()
