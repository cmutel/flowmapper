import pytest

from flowmapper.cas import CASField


def test_cas_init():
    cas = CASField("0000096-49-1")
    assert cas.original == "0000096-49-1"
    assert cas.transformed == "96-49-1"
    assert cas.digits == (9, 6, 4, 9, 1)


def test_cas_init_empty_string():
    cas = CASField("")
    assert cas.original == ""
    assert cas.transformed == ""
    assert cas.digits == ()


def test_cas_init_none():
    cas = CASField(None)
    assert cas.original is None
    assert cas.transformed == ""
    assert cas.digits == ()


def test_cas_init_error():
    with pytest.raises(TypeError):
        CASField(96491)


def test_cas_export():
    assert CASField("7782-40-3").export == "7782-40-3"
    assert CASField("7782403").export == "7782-40-3"
    assert CASField("0007782403").export == "7782-40-3"
    assert CASField("").export == ""
    assert CASField(None).export == ""


def test_invalid_cas_check_digit():
    assert not CASField("96-49-2").valid
    assert CASField("96-49-2").check_digit_expected == 1


def test_cas_repr():
    repr(CASField("0000096-49-1")) == "Valid CASField: '0000096-49-1' -> '96-49-1'"
    repr(CASField("0000096-49-2")) == "Invalid CASField: '0000096-49-2' -> '96-49-2'"
    repr(CASField("")) == "CASField with missing original value"


def test_equality_comparison():
    assert CASField("\t\n\n007440-05-3") == CASField("7440-05-3")
    assert CASField("7440-05-3") == "0007440-05-3"
    assert CASField("7440-05-3") == "7440-05-3"
    assert not CASField("7440-05-3") == "7782-40-3"
    assert not CASField("7440-05-3") == CASField("7782-40-3")
    assert not CASField("") == CASField("7782-40-3")
    assert not CASField("7440-05-3") == CASField("")
    assert not CASField("") == CASField("")
    assert not CASField(None) == CASField("")
    assert not CASField("") == CASField(None)
