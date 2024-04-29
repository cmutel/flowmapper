from flowmapper.string_list import StringList


def test_string_list_empty():
    sl = StringList([])
    assert sl.data == []
    assert list(iter(sl)) == []
    assert len(sl) == 0
    assert not sl
    assert repr(sl) == "StringList: Empty"
    assert 1 not in sl


def test_string_list_no_transformed():
    sl = StringList(["A", "b"])
    assert "A" in sl
    assert "b" in sl
    assert len(sl) == 2
    assert sl
    assert (
        repr(sl)
        == "StringList: [\"StringField: 'A' -> 'a'\", \"StringField: 'b' -> 'b'\"]"
    )
    assert list(iter(sl)) == ["a", "b"]
    assert sl.data[0].original == "A"
    assert sl.data[0].normalized == "a"


def test_string_list_transformed():
    sl = StringList(["A", "b"], ["A*", "b"])
    assert "A*" in sl
    assert "b" in sl
    assert len(sl) == 2
    assert sl
    assert (
        repr(sl)
        == "StringList: [\"StringField: 'A' -> 'a*'\", \"StringField: 'b' -> 'b'\"]"
    )
    assert list(iter(sl)) == ["a*", "b"]
    assert sl.data[0].original == "A"
    assert sl.data[0].normalized == "a*"
