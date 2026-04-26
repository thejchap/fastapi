from tryke import expect, test

from docs_src.python_types.tutorial004_py310 import get_name_with_age


@test
def get_name_with_age_pass_int():
    expect(get_name_with_age("John", 30)).to_equal("John is this old: 30")
