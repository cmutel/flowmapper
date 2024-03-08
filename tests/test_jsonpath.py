import flowmapper.jsonpath as jp


def test_basic_access():
    data = {
        "name": "Chrysotile",
        "context": ["Resources", "in ground"],
        "unit": {"kg": 1},
    }

    assert (
        jp.extract(
            "name",
            data,
        )
        == "Chrysotile"
    )
    assert jp.extract("context.0", data) == "Resources"


def test_special_characters():
    data = {
        "@id": "be73218b-18af-492e-96e6-addd309d1e32",
        "name": {"#text": "Zinc, in ground", "@xml:lang": "en"},
    }

    assert jp.extract("@id", data) == "be73218b-18af-492e-96e6-addd309d1e32"
    assert jp.extract("name.#text", data) == "Zinc, in ground"


def test_nested_data_access():
    data = {
        "@id": "f0cc0453-32c0-48f5-b8d4-fc87d100b8d9",
        "@casNumber": "000078-79-5",
        "name": {"@xml:lang": "en", "#text": "Isoprene"},
        "synonym": [
            {"@xml:lang": "en", "#text": "2-methylbuta-1,3-diene"},
            {"@xml:lang": "en", "#text": "methyl bivinyl"},
        ],
    }

    assert jp.extract(("synonym", ["#text"]), data) == [
        "2-methylbuta-1,3-diene",
        "methyl bivinyl",
    ]


def test_root():
    assert (
        jp.root(".unit") == ""
    )  # this could be a problem if there are . in column names
    assert jp.root("unit") == "unit"
    assert jp.root("unit.name") == "unit"
    assert jp.root("unit.foo.bar") == "unit"
    assert jp.root(("synonym", ["#text"])) == "synonym"
