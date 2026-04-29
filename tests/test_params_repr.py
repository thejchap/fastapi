from typing import Any

from fastapi.params import Body, Cookie, Header, Param, Path, Query
from tryke import expect, test

test_data: list[Any] = ["teststr", None, ..., 1, []]


def get_user():
    return {}  # pragma: no cover


@test("Param repr with a string default")
def param_repr_str():
    expect(repr(Param("teststr")), "repr(Param('teststr'))").to_equal("Param(teststr)")


@test("Param repr with a None default")
def param_repr_none():
    expect(repr(Param(None)), "repr(Param(None))").to_equal("Param(None)")


@test("Param repr with an Ellipsis default")
def param_repr_ellipsis():
    expect(repr(Param(...)), "repr(Param(...))").to_equal("Param(PydanticUndefined)")


@test("Param repr with a numeric default")
def param_repr_number():
    expect(repr(Param(1)), "repr(Param(1))").to_equal("Param(1)")


@test("Param repr with a list default")
def param_repr_list():
    expect(repr(Param([])), "repr(Param([]))").to_equal("Param([])")


@test("Path repr renders as PydanticUndefined for both empty and Ellipsis")
def path_repr():
    expect(repr(Path()), "repr(Path())").to_equal("Path(PydanticUndefined)")
    expect(repr(Path(...)), "repr(Path(...))").to_equal("Path(PydanticUndefined)")


@test("Query repr with a string default")
def query_repr_str():
    expect(repr(Query("teststr")), "repr(Query('teststr'))").to_equal(
        "Query(teststr)"
    )


@test("Query repr with a None default")
def query_repr_none():
    expect(repr(Query(None)), "repr(Query(None))").to_equal("Query(None)")


@test("Query repr with an Ellipsis default")
def query_repr_ellipsis():
    expect(repr(Query(...)), "repr(Query(...))").to_equal("Query(PydanticUndefined)")


@test("Query repr with a numeric default")
def query_repr_number():
    expect(repr(Query(1)), "repr(Query(1))").to_equal("Query(1)")


@test("Query repr with a list default")
def query_repr_list():
    expect(repr(Query([])), "repr(Query([]))").to_equal("Query([])")


@test("Header repr with a string default")
def header_repr_str():
    expect(repr(Header("teststr")), "repr(Header('teststr'))").to_equal(
        "Header(teststr)"
    )


@test("Header repr with a None default")
def header_repr_none():
    expect(repr(Header(None)), "repr(Header(None))").to_equal("Header(None)")


@test("Header repr with an Ellipsis default")
def header_repr_ellipsis():
    expect(repr(Header(...)), "repr(Header(...))").to_equal(
        "Header(PydanticUndefined)"
    )


@test("Header repr with a numeric default")
def header_repr_number():
    expect(repr(Header(1)), "repr(Header(1))").to_equal("Header(1)")


@test("Header repr with a list default")
def header_repr_list():
    expect(repr(Header([])), "repr(Header([]))").to_equal("Header([])")


@test("Cookie repr with a string default")
def cookie_repr_str():
    expect(repr(Cookie("teststr")), "repr(Cookie('teststr'))").to_equal(
        "Cookie(teststr)"
    )


@test("Cookie repr with a None default")
def cookie_repr_none():
    expect(repr(Cookie(None)), "repr(Cookie(None))").to_equal("Cookie(None)")


@test("Cookie repr with an Ellipsis default")
def cookie_repr_ellipsis():
    expect(repr(Cookie(...)), "repr(Cookie(...))").to_equal(
        "Cookie(PydanticUndefined)"
    )


@test("Cookie repr with a numeric default")
def cookie_repr_number():
    expect(repr(Cookie(1)), "repr(Cookie(1))").to_equal("Cookie(1)")


@test("Cookie repr with a list default")
def cookie_repr_list():
    expect(repr(Cookie([])), "repr(Cookie([]))").to_equal("Cookie([])")


@test("Body repr with a string default")
def body_repr_str():
    expect(repr(Body("teststr")), "repr(Body('teststr'))").to_equal("Body(teststr)")


@test("Body repr with a None default")
def body_repr_none():
    expect(repr(Body(None)), "repr(Body(None))").to_equal("Body(None)")


@test("Body repr with an Ellipsis default")
def body_repr_ellipsis():
    expect(repr(Body(...)), "repr(Body(...))").to_equal("Body(PydanticUndefined)")


@test("Body repr with a numeric default")
def body_repr_number():
    expect(repr(Body(1)), "repr(Body(1))").to_equal("Body(1)")


@test("Body repr with a list default")
def body_repr_list():
    expect(repr(Body([])), "repr(Body([]))").to_equal("Body([])")
