from fastapi.testclient import TestClient
from tryke import expect, test

from .main import app

client = TestClient(app)


@test("GET /text returns Hello World")
def text_get():
    response = client.get("/text")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("Hello World")


@test("Nonexistent path returns 404")
def nonexistent():
    response = client.get("/nonexistent")
    expect(response.status_code, "status code").to_equal(404).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Not Found"})


@test("/path/foobar returns the path string")
def path_foobar():
    response = client.get("/path/foobar")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foobar")


@test('/path/str/foobar returns "foobar"')
def path_str_foobar():
    response = client.get("/path/str/foobar")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foobar")


@test('/path/str/42 returns "42"')
def path_str_42():
    response = client.get("/path/str/42")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("42")


@test('/path/str/True returns "True"')
def path_str_True():
    response = client.get("/path/str/True")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("True")


@test("/path/int/foobar rejects non-int with 422")
def path_int_foobar():
    response = client.get("/path/int/foobar")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foobar",
                }
            ]
        }
    )


@test('/path/int/True rejects "True" with 422')
def path_int_True():
    response = client.get("/path/int/True")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "True",
                }
            ]
        }
    )


@test("/path/int/42 returns 42")
def path_int_42():
    response = client.get("/path/int/42")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(42)


@test("/path/int/42.5 rejects float with 422")
def path_int_42_5():
    response = client.get("/path/int/42.5")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "42.5",
                }
            ]
        }
    )


@test("/path/float/foobar rejects non-number with 422")
def path_float_foobar():
    response = client.get("/path/float/foobar")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "float_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid number, unable to parse string as a number",
                    "input": "foobar",
                }
            ]
        }
    )


@test('/path/float/True rejects "True" with 422')
def path_float_True():
    response = client.get("/path/float/True")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "float_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid number, unable to parse string as a number",
                    "input": "True",
                }
            ]
        }
    )


@test("/path/float/42 returns 42")
def path_float_42():
    response = client.get("/path/float/42")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(42)


@test("/path/float/42.5 returns 42.5")
def path_float_42_5():
    response = client.get("/path/float/42.5")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(42.5)


@test("/path/bool/foobar rejects non-bool with 422")
def path_bool_foobar():
    response = client.get("/path/bool/foobar")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "bool_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid boolean, unable to interpret input",
                    "input": "foobar",
                }
            ]
        }
    )


@test("/path/bool/True returns True")
def path_bool_True():
    response = client.get("/path/bool/True")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_be(True)


@test('/path/bool/42 rejects "42" with 422')
def path_bool_42():
    response = client.get("/path/bool/42")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "bool_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid boolean, unable to interpret input",
                    "input": "42",
                }
            ]
        }
    )


@test('/path/bool/42.5 rejects "42.5" with 422')
def path_bool_42_5():
    response = client.get("/path/bool/42.5")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "bool_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid boolean, unable to interpret input",
                    "input": "42.5",
                }
            ]
        }
    )


@test("/path/bool/1 returns True")
def path_bool_1():
    response = client.get("/path/bool/1")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_be(True)


@test("/path/bool/0 returns False")
def path_bool_0():
    response = client.get("/path/bool/0")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_be(False)


@test("/path/bool/true returns True")
def path_bool_true():
    response = client.get("/path/bool/true")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_be(True)


@test("/path/bool/False returns False")
def path_bool_False():
    response = client.get("/path/bool/False")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_be(False)


@test("/path/bool/false returns False")
def path_bool_false():
    response = client.get("/path/bool/false")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_be(False)


@test('/path/param/foo returns "foo"')
def path_param_foo():
    response = client.get("/path/param/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo")


@test("min_length path param accepts a string of the right length")
def path_param_minlength_foo():
    response = client.get("/path/param-minlength/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo")


@test("min_length path param rejects a too-short string")
def path_param_minlength_fo():
    response = client.get("/path/param-minlength/fo")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "string_too_short",
                    "loc": ["path", "item_id"],
                    "msg": "String should have at least 3 characters",
                    "input": "fo",
                    "ctx": {"min_length": 3},
                }
            ]
        }
    )


@test("max_length path param accepts a string of the right length")
def path_param_maxlength_foo():
    response = client.get("/path/param-maxlength/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo")


@test("max_length path param rejects a too-long string")
def path_param_maxlength_foobar():
    response = client.get("/path/param-maxlength/foobar")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "string_too_long",
                    "loc": ["path", "item_id"],
                    "msg": "String should have at most 3 characters",
                    "input": "foobar",
                    "ctx": {"max_length": 3},
                }
            ]
        }
    )


@test("min/max-length path param accepts a string in range")
def path_param_min_maxlength_foo():
    response = client.get("/path/param-min_maxlength/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("foo")


@test("min/max-length path param rejects too-long string")
def path_param_min_maxlength_foobar():
    response = client.get("/path/param-min_maxlength/foobar")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "string_too_long",
                    "loc": ["path", "item_id"],
                    "msg": "String should have at most 3 characters",
                    "input": "foobar",
                    "ctx": {"max_length": 3},
                }
            ]
        }
    )


@test("min/max-length path param rejects too-short string")
def path_param_min_maxlength_f():
    response = client.get("/path/param-min_maxlength/f")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "string_too_short",
                    "loc": ["path", "item_id"],
                    "msg": "String should have at least 2 characters",
                    "input": "f",
                    "ctx": {"min_length": 2},
                }
            ]
        }
    )


@test("gt-constrained path param accepts a value above the bound")
def path_param_gt_42():
    response = client.get("/path/param-gt/42")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(42)


@test("gt-constrained path param rejects a value at the bound")
def path_param_gt_2():
    response = client.get("/path/param-gt/2")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 3",
                    "input": "2",
                    "ctx": {"gt": 3.0},
                }
            ]
        }
    )


@test("gt=0 path param accepts a small positive number")
def path_param_gt0_0_05():
    response = client.get("/path/param-gt0/0.05")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(0.05)


@test("gt=0 path param rejects zero")
def path_param_gt0_0():
    response = client.get("/path/param-gt0/0")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 0",
                    "input": "0",
                    "ctx": {"gt": 0.0},
                }
            ]
        }
    )


@test("ge-constrained path param accepts a value above the bound")
def path_param_ge_42():
    response = client.get("/path/param-ge/42")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(42)


@test("ge-constrained path param accepts the boundary value")
def path_param_ge_3():
    response = client.get("/path/param-ge/3")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(3)


@test("ge-constrained path param rejects a value below the bound")
def path_param_ge_2():
    response = client.get("/path/param-ge/2")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "greater_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than or equal to 3",
                    "input": "2",
                    "ctx": {"ge": 3.0},
                }
            ]
        }
    )


@test("lt-constrained path param rejects a value above the bound")
def path_param_lt_42():
    response = client.get("/path/param-lt/42")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 3",
                    "input": "42",
                    "ctx": {"lt": 3.0},
                }
            ]
        }
    )


@test("lt-constrained path param accepts a value below the bound")
def path_param_lt_2():
    response = client.get("/path/param-lt/2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(2)


@test("lt=0 path param accepts a negative number")
def path_param_lt0__1():
    response = client.get("/path/param-lt0/-1")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(-1)


@test("lt=0 path param rejects zero")
def path_param_lt0_0():
    response = client.get("/path/param-lt0/0")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 0",
                    "input": "0",
                    "ctx": {"lt": 0.0},
                }
            ]
        }
    )


@test("le-constrained path param rejects a value above the bound")
def path_param_le_42():
    response = client.get("/path/param-le/42")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "less_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than or equal to 3",
                    "input": "42",
                    "ctx": {"le": 3.0},
                }
            ]
        }
    )


@test("le-constrained path param accepts the boundary value")
def path_param_le_3():
    response = client.get("/path/param-le/3")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(3)


@test("le-constrained path param accepts a value below the bound")
def path_param_le_2():
    response = client.get("/path/param-le/2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(2)


@test("lt+gt path param accepts a value strictly inside the range")
def path_param_lt_gt_2():
    response = client.get("/path/param-lt-gt/2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(2)


@test("lt+gt path param rejects a value above the upper bound")
def path_param_lt_gt_4():
    response = client.get("/path/param-lt-gt/4")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 3",
                    "input": "4",
                    "ctx": {"lt": 3.0},
                }
            ]
        }
    )


@test("lt+gt path param rejects a value below the lower bound")
def path_param_lt_gt_0():
    response = client.get("/path/param-lt-gt/0")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 1",
                    "input": "0",
                    "ctx": {"gt": 1.0},
                }
            ]
        }
    )


@test("le+ge path param accepts a value inside the range")
def path_param_le_ge_2():
    response = client.get("/path/param-le-ge/2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(2)


@test("le+ge path param accepts the lower boundary value")
def path_param_le_ge_1():
    response = client.get("/path/param-le-ge/1")
    expect(response.status_code, "status code").to_equal(200).fatal()


@test("le+ge path param accepts the upper boundary value")
def path_param_le_ge_3():
    response = client.get("/path/param-le-ge/3")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(3)


@test("le+ge path param rejects a value above the upper bound")
def path_param_le_ge_4():
    response = client.get("/path/param-le-ge/4")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "less_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than or equal to 3",
                    "input": "4",
                    "ctx": {"le": 3.0},
                }
            ]
        }
    )


@test("lt int path param accepts a value below the bound")
def path_param_lt_int_2():
    response = client.get("/path/param-lt-int/2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(2)


@test("lt int path param rejects a value above the bound")
def path_param_lt_int_42():
    response = client.get("/path/param-lt-int/42")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 3",
                    "input": "42",
                    "ctx": {"lt": 3},
                }
            ]
        }
    )


@test("lt int path param rejects a non-integer string")
def path_param_lt_int_2_7():
    response = client.get("/path/param-lt-int/2.7")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    )


@test("gt int path param accepts a value above the bound")
def path_param_gt_int_42():
    response = client.get("/path/param-gt-int/42")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(42)


@test("gt int path param rejects a value at the bound")
def path_param_gt_int_2():
    response = client.get("/path/param-gt-int/2")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 3",
                    "input": "2",
                    "ctx": {"gt": 3},
                }
            ]
        }
    )


@test("gt int path param rejects a non-integer string")
def path_param_gt_int_2_7():
    response = client.get("/path/param-gt-int/2.7")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    )


@test("le int path param rejects a value above the bound")
def path_param_le_int_42():
    response = client.get("/path/param-le-int/42")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "less_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than or equal to 3",
                    "input": "42",
                    "ctx": {"le": 3},
                }
            ]
        }
    )


@test("le int path param accepts the boundary value")
def path_param_le_int_3():
    response = client.get("/path/param-le-int/3")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(3)


@test("le int path param accepts a value below the bound")
def path_param_le_int_2():
    response = client.get("/path/param-le-int/2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(2)


@test("le int path param rejects a non-integer string")
def path_param_le_int_2_7():
    response = client.get("/path/param-le-int/2.7")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    )


@test("ge int path param accepts a value above the bound")
def path_param_ge_int_42():
    response = client.get("/path/param-ge-int/42")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(42)


@test("ge int path param accepts the boundary value")
def path_param_ge_int_3():
    response = client.get("/path/param-ge-int/3")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(3)


@test("ge int path param rejects a value below the bound")
def path_param_ge_int_2():
    response = client.get("/path/param-ge-int/2")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "greater_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than or equal to 3",
                    "input": "2",
                    "ctx": {"ge": 3},
                }
            ]
        }
    )


@test("ge int path param rejects a non-integer string")
def path_param_ge_int_2_7():
    response = client.get("/path/param-ge-int/2.7")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    )


@test("lt+gt int path param accepts a value inside the range")
def path_param_lt_gt_int_2():
    response = client.get("/path/param-lt-gt-int/2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(2)


@test("lt+gt int path param rejects a value above the bound")
def path_param_lt_gt_int_4():
    response = client.get("/path/param-lt-gt-int/4")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "less_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than 3",
                    "input": "4",
                    "ctx": {"lt": 3},
                }
            ]
        }
    )


@test("lt+gt int path param rejects a value below the bound")
def path_param_lt_gt_int_0():
    response = client.get("/path/param-lt-gt-int/0")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be greater than 1",
                    "input": "0",
                    "ctx": {"gt": 1},
                }
            ]
        }
    )


@test("lt+gt int path param rejects a non-integer string")
def path_param_lt_gt_int_2_7():
    response = client.get("/path/param-lt-gt-int/2.7")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    )


@test("le+ge int path param accepts a value inside the range")
def path_param_le_ge_int_2():
    response = client.get("/path/param-le-ge-int/2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(2)


@test("le+ge int path param accepts the lower boundary value")
def path_param_le_ge_int_1():
    response = client.get("/path/param-le-ge-int/1")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(1)


@test("le+ge int path param accepts the upper boundary value")
def path_param_le_ge_int_3():
    response = client.get("/path/param-le-ge-int/3")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(3)


@test("le+ge int path param rejects a value above the bound")
def path_param_le_ge_int_4():
    response = client.get("/path/param-le-ge-int/4")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "less_than_equal",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be less than or equal to 3",
                    "input": "4",
                    "ctx": {"le": 3},
                }
            ]
        }
    )


@test("le+ge int path param rejects a non-integer string")
def path_param_le_ge_int_2_7():
    response = client.get("/path/param-le-ge-int/2.7")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["path", "item_id"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "2.7",
                }
            ]
        }
    )
