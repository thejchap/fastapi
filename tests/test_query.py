from fastapi.testclient import TestClient
from tryke import expect, test

from .main import app

client = TestClient(app)


@test("missing required query param returns 422")
def query():
    response = client.get("/query")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("required query param accepts value")
def query_query_baz():
    response = client.get("/query?query=baz")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar baz")


@test("undeclared query params do not satisfy required")
def query_not_declared_baz():
    response = client.get("/query?not_declared=baz")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("optional query param can be omitted")
def query_optional():
    response = client.get("/query/optional")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar")


@test("optional query param accepts value")
def query_optional_query_baz():
    response = client.get("/query/optional?query=baz")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar baz")


@test("optional query ignores undeclared params")
def query_optional_not_declared_baz():
    response = client.get("/query/optional?not_declared=baz")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar")


@test("missing required int query param returns 422")
def query_int():
    response = client.get("/query/int")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("int query param accepts integer value")
def query_int_query_42():
    response = client.get("/query/int?query=42")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar 42")


@test("int query param rejects float value")
def query_int_query_42_5():
    response = client.get("/query/int?query=42.5")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "42.5",
                }
            ]
        }
    )


@test("int query param rejects non-numeric value")
def query_int_query_baz():
    response = client.get("/query/int?query=baz")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "baz",
                }
            ]
        }
    )


@test("int query undeclared params do not satisfy required")
def query_int_not_declared_baz():
    response = client.get("/query/int?not_declared=baz")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("optional int query can be omitted")
def query_int_optional():
    response = client.get("/query/int/optional")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar")


@test("optional int query accepts integer value")
def query_int_optional_query_50():
    response = client.get("/query/int/optional?query=50")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar 50")


@test("optional int query rejects non-numeric")
def query_int_optional_query_foo():
    response = client.get("/query/int/optional?query=foo")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foo",
                }
            ]
        }
    )


@test("int query default is used when omitted")
def query_int_default():
    response = client.get("/query/int/default")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar 10")


@test("int query default is overridden by value")
def query_int_default_query_50():
    response = client.get("/query/int/default?query=50")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar 50")


@test("int query default rejects non-numeric value")
def query_int_default_query_foo():
    response = client.get("/query/int/default?query=foo")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foo",
                }
            ]
        }
    )


@test("Query() param can be omitted")
def query_param():
    response = client.get("/query/param")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar")


@test("Query() param accepts value")
def query_param_query_50():
    response = client.get("/query/param?query=50")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar 50")


@test("required Query() param missing returns 422")
def query_param_required():
    response = client.get("/query/param-required")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("required Query() param accepts value")
def query_param_required_query_50():
    response = client.get("/query/param-required?query=50")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar 50")


@test("required int Query() param missing returns 422")
def query_param_required_int():
    response = client.get("/query/param-required/int")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "query"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("required int Query() accepts integer")
def query_param_required_int_query_50():
    response = client.get("/query/param-required/int?query=50")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo bar 50")


@test("required int Query() rejects non-numeric")
def query_param_required_int_query_foo():
    response = client.get("/query/param-required/int?query=foo")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["query", "query"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foo",
                }
            ]
        }
    )


@test("frozenset query dedupes repeated values")
def query_frozenset_query_1_query_1_query_2():
    response = client.get("/query/frozenset/?query=1&query=1&query=2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("1,2")


@test("list query collects repeated values")
def query_list():
    response = client.get("/query/list/?device_ids=1&device_ids=2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal([1, 2])


@test("required list query missing returns 422")
def query_list_empty():
    response = client.get("/query/list/")
    expect(response.status_code, "status code").to_equal(422).fatal()


@test("list-default query collects repeated values")
def query_list_default():
    response = client.get("/query/list-default/?device_ids=1&device_ids=2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal([1, 2])


@test("list-default query returns empty when omitted")
def query_list_default_empty():
    response = client.get("/query/list-default/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal([])
