from tryke import expect, test

from docs_src.python_types.tutorial010_py310 import Person, get_person_name


@test
def get_person_name_returns_name():
    expect(get_person_name(Person("John Doe"))).to_equal("John Doe")
