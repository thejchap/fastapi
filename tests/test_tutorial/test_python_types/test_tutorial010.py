from tryke import expect, test

from docs_src.python_types.tutorial010_py310 import Person, get_person_name


@test("get_person_name returns the person's name")
def get_person_name_returns_name():
    expect(
        get_person_name(Person("John Doe")), "person name"
    ).to_equal("John Doe")
