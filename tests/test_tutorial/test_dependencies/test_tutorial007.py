import asyncio
from contextlib import asynccontextmanager
from unittest.mock import Mock, patch

from tryke import expect, test

from docs_src.dependencies.tutorial007_py310 import get_db


@test("get_db async generator closes the DB session")
def get_db_coverage():
    # Just for coverage.
    async def test_async_gen():
        cm = asynccontextmanager(get_db)
        async with cm() as db_session:
            return db_session

    dbsession_moock = Mock()

    with patch(
        "docs_src.dependencies.tutorial007_py310.DBSession",
        return_value=dbsession_moock,
        create=True,
    ):
        value = asyncio.run(test_async_gen())

    expect(value, "value").to_be(dbsession_moock)
    dbsession_moock.close.assert_called_once()
