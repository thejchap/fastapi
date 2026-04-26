from fastapi.dependencies.utils import get_typed_annotation
from tryke import expect, test


@test
def get_typed_annotation_test():
    # For coverage
    annotation = "None"
    typed_annotation = get_typed_annotation(annotation, globals())
    expect(typed_annotation).to_be_none()
