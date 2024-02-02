from flowmapper.utils import read_field_mapping

def test_read_field_mapping():
    expected = {
        "source": {
            "uuid": "",
            "name": "name",
            "synonyms": "",
            "context": "categories",
            "unit": "unit",
            "cas": "CAS",
        },
        "target": {
            "uuid": "@id",
            "name": "name.#text",
            "synonyms": ('synonym', ['#text']),
            "context": "compartment.*.#text",
            "unit": "unitName.#text",
            "cas": "@casNumber",
        },
    }
    actual = read_field_mapping("tests/data/field_mapping-sp-ei.py")
    assert expected == actual

