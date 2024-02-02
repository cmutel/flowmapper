from deepdiff import DeepDiff

from flowmapper.flow import Flow
from flowmapper.match import match_identical_names


def test_match_identical_names(fields):
    source = {
        "Flowable": "Carbon dioxide, in air",
        "CAS No": "000124-38-9",
        "Unit": "kg",
        "Context": "Resources/in air",
        "Flow UUID": "32722990-B7D8-44A8-BC7D-EC3A89F533FF",
    }

    target = {
        "Flowable": "Carbon dioxide, in air",
        "CASNo": "000124-38-9",
        "Unit": "kg",
        "Context": "natural resource/in air",
        "FlowUUID": "cc6a1abb-b123-4ca6-8f16-38209df609be",
    }

    s = Flow(source, fields['source'])
    t = Flow(target, fields['target'])

    match = match_identical_names(s, t)
    assert match


def test_match_identical_names_jsonpath(field_mapping):
    source = {
        "name": "Carbon dioxide, in air",
        "categories": ["Raw", "(unspecified)"],
        "unit": "kg",
        "CAS": "000124-38-9",
    }

    target = {
        "@id": "cc6a1abb-b123-4ca6-8f16-38209df609be",
        "@casNumber": "000124-38-9",
        "name": {"@xml:lang": "en", "#text": "Carbon dioxide, in air"},
        "unitName": {"@xml:lang": "en", "#text": "kg"},
        "compartment": {
            "@subcompartmentId": "45bb416c-a63b-429f-8754-b3f76a069c43",
            "compartment": {"@xml:lang": "en", "#text": "natural resource"},
            "subcompartment": {"@xml:lang": "en", "#text": "in air"},
        },
    }

    s = Flow(source, field_mapping['source'])
    t = Flow(target, field_mapping['target'])
    
    match = match_identical_names(s, t)
    assert not match