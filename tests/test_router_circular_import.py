from fastapi import APIRouter
from tryke import expect, test


@test
def router_circular_import():
    router = APIRouter()

    expect(lambda: router.include_router(router)).to_raise(
        AssertionError,
        match="Cannot include the same APIRouter instance into itself. Did you mean to include a different router?",
    )
