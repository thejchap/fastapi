from fastapi.openapi.models import Schema, SchemaType
from tryke import expect, test


@test.cases(
    test.case("array", type_value="array"),
    test.case("string-null", type_value=["string", "null"]),
    test.case("none", type_value=None),
)
def allowed_schema_type(
    type_value: SchemaType | list[SchemaType] | None,
) -> None:
    """Test that Schema accepts SchemaType, List[SchemaType] and None for type field."""
    schema = Schema(type=type_value)
    expect(schema.type).to_equal(type_value)


@test
def invalid_type_value() -> None:
    """Test that Schema raises ValueError for invalid type values."""
    expect(lambda: Schema(type=True)).to_raise(  # type: ignore[arg-type]
        ValueError, match="2 validation errors for Schema"
    )
