from flowmapper.string_field import StringField


def test_string_field_empty():
    sf = StringField(None)
    assert sf.original is None
    assert sf.normalized == ""
    assert sf != ""
    assert sf != "a"
    assert sf != StringField("a")
    assert sf is not None
    assert not sf
    assert repr(sf) == "StringField with missing original value"


def test_string_field_no_transformed():
    sf = StringField("A", use_lowercase=False)
    assert sf.original == "A"
    assert sf.normalized == "A"
    assert sf == "A"
    assert sf != "a"
    assert sf == StringField("A", use_lowercase=True)
    assert sf == StringField("A", use_lowercase=False)
    assert sf != "B"
    assert not sf.use_lowercase
    assert sf
    assert repr(sf) == "StringField: 'A' -> 'A'"


def test_string_field_no_transformed_lowercase():
    sf = StringField("A", use_lowercase=True)
    assert sf.original == "A"
    assert sf.normalized == "a"
    assert sf == "a"
    assert sf == "A"
    assert sf == StringField("A", use_lowercase=True)
    assert sf == StringField("A", use_lowercase=False)
    assert sf != "B"
    assert sf.use_lowercase
    assert sf
    assert repr(sf) == "StringField: 'A' -> 'a'"


def test_string_field_transformed():
    sf = StringField("A*", use_lowercase=False)
    assert sf.original == "A*"
    assert sf.normalized == "A*"
    assert sf != "A"
    assert sf != "a*"
    assert sf == "A*"
    assert sf == StringField("A*", use_lowercase=True)
    assert sf == StringField("A*", use_lowercase=False)
    assert sf != "B"
    assert not sf.use_lowercase
    assert sf
    assert repr(sf) == "StringField: 'A*' -> 'A*'"


def test_string_field_transformed_lowercase():
    sf = StringField("A*", use_lowercase=True)
    assert sf.original == "A*"
    assert sf.normalized == "a*"
    assert sf == "a*"
    assert sf == "A*"
    assert sf == StringField("A*", use_lowercase=True)
    assert sf == StringField("A*", use_lowercase=False)
    assert sf != "B"
    assert sf.use_lowercase
    assert sf
    assert repr(sf) == "StringField: 'A*' -> 'a*'"
