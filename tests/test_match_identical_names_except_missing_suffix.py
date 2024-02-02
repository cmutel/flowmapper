from flowmapper.flow import Flow
from flowmapper.match import match_identical_names_except_missing_suffix


def test_match_identical_names_except_missing_suffix(fields):
    source = {
        "Flowable": "Copper",
        "CAS No": "007440-50-8",
        "Unit": "kg",
        "Context": "Emissions to water/groundwater",
        "Flow UUID": "F277F190-A8A4-4A2D-AAF6-F6CB3772A545",
    }

    target = {
        "Flowable": "Copper, ion",
        "CASNo": "017493-86-6",
        "Unit": "kg",
        "Context": "water/ground-",
        "FlowUUID": "c3b659e5-35f1-408c-8cb5-b5f9b295c76e",
    }

    s = Flow(source, fields["source"])
    t = Flow(target, fields["target"])

    match = match_identical_names_except_missing_suffix(s, t, suffix="ion")
    assert match


def test_match_identical_names_except_missing_suffix_different_order(field_mapping):
    s = Flow(
        {"name": "Iron, ion", "unit": "g", "categories": ["Emissions to air", ""]},
        field_mapping["source"],
    )

    t = Flow(
        {
            "@id": "8dba66e2-0f2e-4038-84ef-1e40b4f573a6",
            "@unitId": "487df68b-4994-4027-8fdc-a4dc298257b7",
            "@casNumber": "007439-89-6",
            "name": {"@xml:lang": "en", "#text": "Iron"},
            "unitName": {"@xml:lang": "en", "#text": "kg"},
            "compartment": {
                "@subcompartmentId": "7011f0aa-f5f9-4901-8c10-884ad8296812",
                "compartment": {"@xml:lang": "en", "#text": "air"},
                "subcompartment": {"@xml:lang": "en", "#text": "unspecified"},
            },
        },
        field_mapping["target"],
    )

    match = match_identical_names_except_missing_suffix(s, t, suffix="ion")
    assert match
