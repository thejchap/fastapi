from fastapi.dependencies.utils import get_typed_annotation
from tryke import expect, test


@test("get_typed_annotation resolves the string 'None' to None")
def get_typed_annotation_test():
    # For coverage
    annotation = "None"
    typed_annotation = get_typed_annotation(annotation, globals())
    expect(typed_annotation, "resolved annotation").to_be_none()
