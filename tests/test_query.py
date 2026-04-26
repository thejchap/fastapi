from fastapi.testclient import TestClient
from tryke import expect, test

from .main import app

client = TestClient(app)


@test
def query():
    response = client.get("/query")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_query_baz():
    response = client.get("/query?query=baz")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar baz")


@test
def query_not_declared_baz():
    response = client.get("/query?not_declared=baz")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_optional():
    response = client.get("/query/optional")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar")


@test
def query_optional_query_baz():
    response = client.get("/query/optional?query=baz")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar baz")


@test
def query_optional_not_declared_baz():
    response = client.get("/query/optional?not_declared=baz")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar")


@test
def query_int():
    response = client.get("/query/int")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_int_query_42():
    response = client.get("/query/int?query=42")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar 42")


@test
def query_int_query_42_5():
    response = client.get("/query/int?query=42.5")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_int_query_baz():
    response = client.get("/query/int?query=baz")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_int_not_declared_baz():
    response = client.get("/query/int?not_declared=baz")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_int_optional():
    response = client.get("/query/int/optional")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar")


@test
def query_int_optional_query_50():
    response = client.get("/query/int/optional?query=50")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar 50")


@test
def query_int_optional_query_foo():
    response = client.get("/query/int/optional?query=foo")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_int_default():
    response = client.get("/query/int/default")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar 10")


@test
def query_int_default_query_50():
    response = client.get("/query/int/default?query=50")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar 50")


@test
def query_int_default_query_foo():
    response = client.get("/query/int/default?query=foo")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_param():
    response = client.get("/query/param")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar")


@test
def query_param_query_50():
    response = client.get("/query/param?query=50")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar 50")


@test
def query_param_required():
    response = client.get("/query/param-required")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_param_required_query_50():
    response = client.get("/query/param-required?query=50")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar 50")


@test
def query_param_required_int():
    response = client.get("/query/param-required/int")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_param_required_int_query_50():
    response = client.get("/query/param-required/int?query=50")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo bar 50")


@test
def query_param_required_int_query_foo():
    response = client.get("/query/param-required/int?query=foo")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def query_frozenset_query_1_query_1_query_2():
    response = client.get("/query/frozenset/?query=1&query=1&query=2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("1,2")


@test
def query_list():
    response = client.get("/query/list/?device_ids=1&device_ids=2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal([1, 2])


@test
def query_list_empty():
    response = client.get("/query/list/")
    expect(response.status_code).to_equal(422).fatal()


@test
def query_list_default():
    response = client.get("/query/list-default/?device_ids=1&device_ids=2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal([1, 2])


@test
def query_list_default_empty():
    response = client.get("/query/list-default/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal([])
