from tryke import test

from docs_src.app_testing.tutorial002_py310 import test_read_main, test_websocket


@test("tutorial002 test_read_main runs")
def main():
    test_read_main()


@test("tutorial002 test_websocket runs")
def ws():
    test_websocket()


# Pytest discovered the imported `test_read_main` and `test_websocket` here at
# module scope; mirror that by re-invoking each under dedicated tryke tests.
@test("tutorial002 re-imported test_read_main runs again")
def read_main():
    test_read_main()


@test("tutorial002 re-imported test_websocket runs again")
def websocket():
    test_websocket()
