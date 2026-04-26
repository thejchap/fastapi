from fastapi.testclient import TestClient
from tryke import expect, test

from .main import app

client = TestClient(app)


@test
def text_get():
    response = client.get("/text")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("Hello World")


@test
def nonexistent():
    response = client.get("/nonexistent")
    expect(response.status_code).to_equal(404).fatal()
    expect(response.json()).to_equal({"detail": "Not Found"})


@test
def path_foobar():
    response = client.get("/path/foobar")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foobar")


@test
def path_str_foobar():
    response = client.get("/path/str/foobar")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foobar")


@test
def path_str_42():
    response = client.get("/path/str/42")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("42")


@test
def path_str_True():
    response = client.get("/path/str/True")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("True")


@test
def path_int_foobar():
    response = client.get("/path/int/foobar")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_int_True():
    response = client.get("/path/int/True")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_int_42():
    response = client.get("/path/int/42")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(42)


@test
def path_int_42_5():
    response = client.get("/path/int/42.5")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_float_foobar():
    response = client.get("/path/float/foobar")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_float_True():
    response = client.get("/path/float/True")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_float_42():
    response = client.get("/path/float/42")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(42)


@test
def path_float_42_5():
    response = client.get("/path/float/42.5")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(42.5)


@test
def path_bool_foobar():
    response = client.get("/path/bool/foobar")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_bool_True():
    response = client.get("/path/bool/True")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_be(True)


@test
def path_bool_42():
    response = client.get("/path/bool/42")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_bool_42_5():
    response = client.get("/path/bool/42.5")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_bool_1():
    response = client.get("/path/bool/1")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_be(True)


@test
def path_bool_0():
    response = client.get("/path/bool/0")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_be(False)


@test
def path_bool_true():
    response = client.get("/path/bool/true")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_be(True)


@test
def path_bool_False():
    response = client.get("/path/bool/False")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_be(False)


@test
def path_bool_false():
    response = client.get("/path/bool/false")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_be(False)


@test
def path_param_foo():
    response = client.get("/path/param/foo")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo")


@test
def path_param_minlength_foo():
    response = client.get("/path/param-minlength/foo")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo")


@test
def path_param_minlength_fo():
    response = client.get("/path/param-minlength/fo")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_maxlength_foo():
    response = client.get("/path/param-maxlength/foo")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo")


@test
def path_param_maxlength_foobar():
    response = client.get("/path/param-maxlength/foobar")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_min_maxlength_foo():
    response = client.get("/path/param-min_maxlength/foo")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo")


@test
def path_param_min_maxlength_foobar():
    response = client.get("/path/param-min_maxlength/foobar")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_min_maxlength_f():
    response = client.get("/path/param-min_maxlength/f")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_gt_42():
    response = client.get("/path/param-gt/42")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(42)


@test
def path_param_gt_2():
    response = client.get("/path/param-gt/2")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_gt0_0_05():
    response = client.get("/path/param-gt0/0.05")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(0.05)


@test
def path_param_gt0_0():
    response = client.get("/path/param-gt0/0")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_ge_42():
    response = client.get("/path/param-ge/42")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(42)


@test
def path_param_ge_3():
    response = client.get("/path/param-ge/3")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(3)


@test
def path_param_ge_2():
    response = client.get("/path/param-ge/2")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_lt_42():
    response = client.get("/path/param-lt/42")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_lt_2():
    response = client.get("/path/param-lt/2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(2)


@test
def path_param_lt0__1():
    response = client.get("/path/param-lt0/-1")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(-1)


@test
def path_param_lt0_0():
    response = client.get("/path/param-lt0/0")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_le_42():
    response = client.get("/path/param-le/42")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_le_3():
    response = client.get("/path/param-le/3")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(3)


@test
def path_param_le_2():
    response = client.get("/path/param-le/2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(2)


@test
def path_param_lt_gt_2():
    response = client.get("/path/param-lt-gt/2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(2)


@test
def path_param_lt_gt_4():
    response = client.get("/path/param-lt-gt/4")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_lt_gt_0():
    response = client.get("/path/param-lt-gt/0")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_le_ge_2():
    response = client.get("/path/param-le-ge/2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(2)


@test
def path_param_le_ge_1():
    response = client.get("/path/param-le-ge/1")
    expect(response.status_code).to_equal(200).fatal()


@test
def path_param_le_ge_3():
    response = client.get("/path/param-le-ge/3")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(3)


@test
def path_param_le_ge_4():
    response = client.get("/path/param-le-ge/4")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_lt_int_2():
    response = client.get("/path/param-lt-int/2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(2)


@test
def path_param_lt_int_42():
    response = client.get("/path/param-lt-int/42")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_lt_int_2_7():
    response = client.get("/path/param-lt-int/2.7")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_gt_int_42():
    response = client.get("/path/param-gt-int/42")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(42)


@test
def path_param_gt_int_2():
    response = client.get("/path/param-gt-int/2")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_gt_int_2_7():
    response = client.get("/path/param-gt-int/2.7")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_le_int_42():
    response = client.get("/path/param-le-int/42")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_le_int_3():
    response = client.get("/path/param-le-int/3")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(3)


@test
def path_param_le_int_2():
    response = client.get("/path/param-le-int/2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(2)


@test
def path_param_le_int_2_7():
    response = client.get("/path/param-le-int/2.7")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_ge_int_42():
    response = client.get("/path/param-ge-int/42")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(42)


@test
def path_param_ge_int_3():
    response = client.get("/path/param-ge-int/3")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(3)


@test
def path_param_ge_int_2():
    response = client.get("/path/param-ge-int/2")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_ge_int_2_7():
    response = client.get("/path/param-ge-int/2.7")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_lt_gt_int_2():
    response = client.get("/path/param-lt-gt-int/2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(2)


@test
def path_param_lt_gt_int_4():
    response = client.get("/path/param-lt-gt-int/4")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_lt_gt_int_0():
    response = client.get("/path/param-lt-gt-int/0")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_lt_gt_int_2_7():
    response = client.get("/path/param-lt-gt-int/2.7")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_le_ge_int_2():
    response = client.get("/path/param-le-ge-int/2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(2)


@test
def path_param_le_ge_int_1():
    response = client.get("/path/param-le-ge-int/1")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(1)


@test
def path_param_le_ge_int_3():
    response = client.get("/path/param-le-ge-int/3")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(3)


@test
def path_param_le_ge_int_4():
    response = client.get("/path/param-le-ge-int/4")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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


@test
def path_param_le_ge_int_2_7():
    response = client.get("/path/param-le-ge-int/2.7")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
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
