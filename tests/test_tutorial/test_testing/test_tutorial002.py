from tryke import test

from docs_src.app_testing.tutorial002_py310 import test_read_main, test_websocket


@test
def main():
    test_read_main()


@test
def ws():
    test_websocket()


# Pytest discovered the imported `test_read_main` and `test_websocket` here at
# module scope; mirror that by re-invoking each under dedicated tryke tests.
@test
def read_main():
    test_read_main()


@test
def websocket():
    test_websocket()
