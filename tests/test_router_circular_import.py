from fastapi import APIRouter
from tryke import expect, test


@test("router cannot include itself")
def router_circular_import():
    router = APIRouter()

    expect(
        lambda: router.include_router(router),
        "including a router into itself",
    ).to_raise(
        AssertionError,
        match="Cannot include the same APIRouter instance into itself. Did you mean to include a different router?",
    )
