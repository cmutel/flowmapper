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
    pass



# def test_context():
#     data = {
#         "name": "Carbon dioxide, in air",
#         "context": ["Raw", "(unspecified)"],
#         "unit": "kg",
#         "CAS": "000124-38-9",
#     }
#     fields = "context"
#     actual = Context.from_dict(data, fields).to_dict()
#     expected = {
#         "value": "natural resource/in ground",
#         "raw_value": "Raw/(unspecified)",
#         "raw_object": {"context": ["Raw", "(unspecified)"]},
#     }
#     assert actual == expected


# def test_trailing_slash():
#     c1 = Context.from_dict({"context": ["Raw", "(unspecified)"]}, "context")
#     c2 = Context.from_dict({"context": ["Raw"]}, "context")
#     c3 = Context.from_dict({"context": ["Raw/"]}, "context")
#     assert c1.value == c2.value
#     assert c2.value == c3.value
#     "/".join(c1.value)


# def test_unspecified():
#     c1 = Context.from_dict(
#         {
#             "compartment": {
#                 "@subcompartmentId": "e47f0a6c-3be8-4027-9eee-de251784f708",
#                 "compartment": {"@xml:lang": "en", "#text": "water"},
#                 "subcompartment": {"@xml:lang": "en", "#text": "unspecified"},
#             },
#         },
#         "compartment.*.#text",
#     )

#     c2 = Context.from_dict({"context": ["Emissions to water", ""]}, "context")
#     c3 = Context.from_dict({"context": ["Water", "(unspecified)"]}, "context")
#     c4 = Context.from_dict({"context": ["Water", ""]}, "context")
#     c5 = Context.from_dict({"context": ["Water/", ""]}, "context")
#     c6 = Context.from_dict({"context": ["Water/"]}, "context")
#     c7 = Context.from_dict({"context": "Water/(unspecified)"}, "context")
#     c8 = Context.from_dict({"context": "Water/unspecified"}, "context")
#     c9 = Context.from_dict({"context": "Water/"}, "context")
#     c10 = Context.from_dict({"context": "Water"}, "context")
#     c11 = Context.from_dict(
#         {"context": [{"name": "Water"}, {"name": "unspecified"}]}, ("context", ["name"])
#     )
#     c12 = Context.from_dict({"context": ["Water"]}, "context")

#     actual = set(
#         [
#             c1.value,
#             c2.value,
#             c3.value,
#             c4.value,
#             c5.value,
#             c6.value,
#             c7.value,
#             c8.value,
#             c9.value,
#             c10.value,
#             c11.value,
#             c12.value,
#         ]
#     )
#     expected = {"water"}
#     assert actual == expected
