from tryke import expect, test

from docs_src.python_types.tutorial013_py310 import say_hello


@test
def say_hello_returns_greeting():
    expect(say_hello("FastAPI")).to_equal("Hello FastAPI")
