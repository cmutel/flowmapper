from flowmapper.flow import Flow
from flowmapper.match import match_identical_names_in_synonyms

def test_match_identical_names_in_synonyms(field_mapping):
    source = {
        "name": "Sulfuric acid",
        "unit": "kg",
        "categories": ["Emissions to water", ""],
    }

    target = {
        "@id": "8570c45a-8c78-4709-9b8f-fb88314d9e9d",
        "@unitId": "487df68b-4994-4027-8fdc-a4dc298257b7",
        "@formula": "H8N2O4S",
        "@casNumber": "007783-20-2",
        "name": {"@xml:lang": "en", "#text": "Ammonium sulfate"},
        "unitName": {"@xml:lang": "en", "#text": "kg"},
        "compartment": {
            "@subcompartmentId": "e47f0a6c-3be8-4027-9eee-de251784f708",
            "compartment": {"@xml:lang": "en", "#text": "water"},
            "subcompartment": {"@xml:lang": "en", "#text": "unspecified"},
        },
        "synonym": [
            {"@xml:lang": "en", "#text": "Diammonium sulfate"},
            {"@xml:lang": "en", "#text": "Mascagnite"},
            {"@xml:lang": "en", "#text": "Sulfuric acid"},
            {"@xml:lang": "en", "#text": "Actamaster"},
            {"@xml:lang": "en", "#text": "Diammonium salt"},
            {"@xml:lang": "en", "#text": "Dolamin"},
        ],
    }

    s = Flow(source, field_mapping["source"])
    t = Flow(target, field_mapping["target"])

    match = match_identical_names_in_synonyms(s, t)
    assert match
