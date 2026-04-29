# This is more or less a workaround to make Depends and Security hashable
# as other tools that use them depend on that
# Ref: https://github.com/fastapi/fastapi/pull/14320

from fastapi import Depends, Security
from tryke import expect, test


def dep():
    pass


@test("Depends and Security hash consistently per (dep, scope)")
def depends_hashable():
    dep()  # just for coverage
    d1 = Depends(dep)
    d2 = Depends(dep)
    d3 = Depends(dep, scope="function")
    d4 = Depends(dep, scope="function")

    s1 = Security(dep)
    s2 = Security(dep)

    expect(hash(d1), "hash of equivalent Depends").to_equal(hash(d2))
    expect(hash(s1), "hash of equivalent Security").to_equal(hash(s2))
    expect(hash(d1), "hash differs by scope").not_.to_equal(hash(d3))
    expect(hash(d3), "hash of equivalent function-scoped Depends").to_equal(hash(d4))
