from tryke import test

from docs_src.async_tests.app_a_py310.test_main import test_root


@test
async def async_testing():
    await test_root()
