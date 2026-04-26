from typing import Any

from fastapi.params import Body, Cookie, Header, Param, Path, Query
from tryke import expect, test

test_data: list[Any] = ["teststr", None, ..., 1, []]


def get_user():
    return {}  # pragma: no cover


@test
def param_repr_str():
    expect(repr(Param("teststr"))).to_equal("Param(teststr)")


@test
def param_repr_none():
    expect(repr(Param(None))).to_equal("Param(None)")


@test
def param_repr_ellipsis():
    expect(repr(Param(...))).to_equal("Param(PydanticUndefined)")


@test
def param_repr_number():
    expect(repr(Param(1))).to_equal("Param(1)")


@test
def param_repr_list():
    expect(repr(Param([]))).to_equal("Param([])")


@test
def path_repr():
    expect(repr(Path())).to_equal("Path(PydanticUndefined)")
    expect(repr(Path(...))).to_equal("Path(PydanticUndefined)")


@test
def query_repr_str():
    expect(repr(Query("teststr"))).to_equal("Query(teststr)")


@test
def query_repr_none():
    expect(repr(Query(None))).to_equal("Query(None)")


@test
def query_repr_ellipsis():
    expect(repr(Query(...))).to_equal("Query(PydanticUndefined)")


@test
def query_repr_number():
    expect(repr(Query(1))).to_equal("Query(1)")


@test
def query_repr_list():
    expect(repr(Query([]))).to_equal("Query([])")


@test
def header_repr_str():
    expect(repr(Header("teststr"))).to_equal("Header(teststr)")


@test
def header_repr_none():
    expect(repr(Header(None))).to_equal("Header(None)")


@test
def header_repr_ellipsis():
    expect(repr(Header(...))).to_equal("Header(PydanticUndefined)")


@test
def header_repr_number():
    expect(repr(Header(1))).to_equal("Header(1)")


@test
def header_repr_list():
    expect(repr(Header([]))).to_equal("Header([])")


@test
def cookie_repr_str():
    expect(repr(Cookie("teststr"))).to_equal("Cookie(teststr)")


@test
def cookie_repr_none():
    expect(repr(Cookie(None))).to_equal("Cookie(None)")


@test
def cookie_repr_ellipsis():
    expect(repr(Cookie(...))).to_equal("Cookie(PydanticUndefined)")


@test
def cookie_repr_number():
    expect(repr(Cookie(1))).to_equal("Cookie(1)")


@test
def cookie_repr_list():
    expect(repr(Cookie([]))).to_equal("Cookie([])")


@test
def body_repr_str():
    expect(repr(Body("teststr"))).to_equal("Body(teststr)")


@test
def body_repr_none():
    expect(repr(Body(None))).to_equal("Body(None)")


@test
def body_repr_ellipsis():
    expect(repr(Body(...))).to_equal("Body(PydanticUndefined)")


@test
def body_repr_number():
    expect(repr(Body(1))).to_equal("Body(1)")


@test
def body_repr_list():
    expect(repr(Body([]))).to_equal("Body([])")
