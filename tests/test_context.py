import pytest

from flowmapper.context import MISSING_VALUES, Context


def test_context_uses_transformed():
    c = Context(
        original="Raw/(unspecified)",
        transformed=["Raw", "(unspecified)"],
    )
    assert c == ["Raw", "(unspecified)"]
    assert c.transformed == ["Raw", "(unspecified)"]


def test_context_transformed_from_tuple():
    c = Context(
        original="Raw/(unspecified)",
        transformed=("Raw", "(unspecified)"),
    )
    assert c == ["Raw", "(unspecified)"]
    assert c.transformed == ("Raw", "(unspecified)")


def test_context_transformed_from_string_with_slash():
    c = Context(
        original="Raw/(unspecified)",
        transformed="Raw/(unspecified)",
    )
    assert c == ["Raw", "(unspecified)"]
    assert c.transformed == "Raw/(unspecified)"


def test_context_transformed_from_string():
    c = Context(
        original="Raw/(unspecified)",
        transformed="Raw",
    )
    assert c == ["Raw", "(unspecified)"]
    assert c.transformed == "Raw"


def test_context_transformed_not_given():
    c = Context(
        original="Raw/(unspecified)",
    )
    assert c == ["Raw", "(unspecified)"]
    assert c.transformed == "Raw/(unspecified)"


def test_context_normalize_tuple():
    c = Context(
        original=("Raw",),
    )
    assert c.normalized == ("raw",)


def test_context_normalize_string_with_slash():
    c = Context(
        original="A/B",
    )
    assert c.normalized == ("a", "b")


def test_context_normalize_string():
    c = Context(
        original="A-B",
    )
    assert c.normalized == ("a-b",)


def test_context_normalize_error():
    class Foo:
        pass

    with pytest.raises(ValueError):
        Context(Foo())


def test_context_normalize_lowercase():
    c = Context(
        original="A-B",
    )
    assert c.normalized == ("a-b",)


def test_context_normalize_strip():
    c = Context(
        original=" A-B\t\n",
    )
    assert c.normalized == ("a-b",)


@pytest.mark.parametrize("string", MISSING_VALUES)
def test_context_missing_values(string):
    c = Context(
        original=("A", string),
    )
    assert c.original == ("A", string)
    assert c.normalized == ("a",)


def test_context_generic_dunder():
    c = Context("A/B")
    assert repr(c) == "('a', 'b')"
    assert repr(Context("")) == "()"
    assert bool(c)
    assert isinstance(hash(c), int)
    assert list(c) == ['a', 'b']


def test_context_in():
    a = Context("A")
    b = Context("A/B")
    assert b in a
    assert a not in b


def test_context_export_as_string():
    assert Context(["A", "B"]).export_as_string() == "A✂️B"
    assert Context("A/B").export_as_string() == "A/B"
    c = Context("A/B")
    c.original = {"A": "B"}
    with pytest.raises(ValueError):
        c.export_as_string()
