from tryke import expect, test

from docs_src.python_types.tutorial003_py310 import get_name_with_age


@test("get_name_with_age rejects an int age")
def get_name_with_age_pass_int():
    expect(
        lambda: get_name_with_age("John", 30),
        "calling get_name_with_age with an int age",
    ).to_raise(TypeError)


@test("get_name_with_age accepts a str age")
def get_name_with_age_pass_str():
    expect(
        get_name_with_age("John", "30"), "result for a str age"
    ).to_equal("John is this old: 30")
