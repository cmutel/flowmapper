from flowmapper.flowproperty import FlowProperty


def test_empty():
    p1 = FlowProperty("")
    p2 = FlowProperty("")
    assert not p1
    assert p1 != p2


def test_list_with_falsy_values():
    p1 = FlowProperty(["", "FOO", None])
    p1 == ["foo"]


def test_get():
    d = {"foo": 1, "FOO": 2}
    p = FlowProperty("FOO")
    assert d.get(p) == 1


def test_equals():
    p1 = FlowProperty("foo")
    p2 = FlowProperty("FOO")
    p3 = FlowProperty()
    assert p1 == "foo"
    assert p2 == "foo"
    assert p2 != "FOO"
    assert p1 == p2
    assert p1 != p3

    p3 = FlowProperty(["foo", "bar"])
    p4 = FlowProperty(["FOO", "BAR"])
    assert p3 == ["foo", "bar"]
    assert p4 == ["foo", "bar"]
    assert p4 != ["FOO", "BAR"]
    assert p3 == p4


def test_init():
    n = FlowProperty.from_dict({"flowable": "\u0055\u0308ber"}, "flowable")
    assert n.value == "\u00FCber"
    assert n.raw_value == "\u0055\u0308ber"
    assert n.raw_object == {"flowable": "\u0055\u0308ber"}
    assert n.to_dict() == {
        "value": "über",
        "raw_value": "Über",
        "raw_object": {"flowable": "Über"},
    }


def test_init_synonyms():
    s = FlowProperty.from_dict(
        {
            "synonym": [
                {"@xml:lang": "en", "#text": "Cumol"},
                {"@xml:lang": "en", "#text": "isopropylbenzene"},
            ]
        },
        ("synonym", ["#text"]),
    )
