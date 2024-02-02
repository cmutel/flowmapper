from flowmapper.flow import Flow
import math


def test_get_conversion_factor(field_mapping):
    s = Flow(
        {
            "name": "Protactinium-234",
            "unit": "Bq",
            "categories": ["Emissions to air", "low. pop."],
        },
        field_mapping["source"],
    )

    t = Flow(
        {
            "@id": "fb13070e-06f1-4964-832f-a23945b880cc",
            "@unitId": "4923348e-591b-4772-b224-d19df86f04c9",
            "name": {"@xml:lang": "en", "#text": "Protactinium-234"},
            "unitName": {"@xml:lang": "en", "#text": "kBq"},
            "compartment": {
                "@subcompartmentId": "be7e06e9-0bf5-462e-99dc-fe4aee383c48",
                "compartment": {"@xml:lang": "en", "#text": "air"},
                "subcompartment": {
                    "@xml:lang": "en",
                    "#text": "non-urban air or from high stacks",
                },
            },
        },
        field_mapping["target"],
    )

    actual = s.unit.conversion_factor(t.unit)
    expected = 1e-3
    assert actual == expected


def test_get_conversion_factor_water(field_mapping):
    s = Flow(
        {"name": "Water", "unit": "kg", "categories": ["Emissions to water", ""]},
        field_mapping["source"],
    )

    t = Flow(
        {
            "@id": "2404b41a-2eed-4e9d-8ab6-783946fdf5d6",
            "@unitId": "de5b3c87-0e35-4fb0-9765-4f3ba34c99e5",
            "@casNumber": "007732-18-5",
            "name": {"@xml:lang": "en", "#text": "Water"},
            "unitName": {"@xml:lang": "en", "#text": "m3"},
            "compartment": {
                "@subcompartmentId": "e47f0a6c-3be8-4027-9eee-de251784f708",
                "compartment": {"@xml:lang": "en", "#text": "water"},
                "subcompartment": {"@xml:lang": "en", "#text": "unspecified"},
            },
        },
        field_mapping["target"],
    )

    actual = s.unit.conversion_factor(t.unit)
    assert math.isnan(actual)


def test_get_conversion_factor_m3y(field_mapping):
    s = Flow(
        {
            "name": "Volume occupied, reservoir",
            "unit": "m3y",
            "categories": ["Resources", "in water"],
        },
        field_mapping["source"],
    )

    t = Flow(
        {
            "@id": "9a9d71c7-79f7-42d0-af47-282d22a7cf07",
            "@unitId": "481b9712-c417-44f1-bfba-38d58088173c",
            "name": {"@xml:lang": "en", "#text": "Volume occupied, reservoir"},
            "unitName": {"@xml:lang": "en", "#text": "m3*year"},
            "compartment": {
                "@subcompartmentId": "30347aef-a90b-46ba-8746-b53741aa779d",
                "compartment": {"@xml:lang": "en", "#text": "natural resource"},
                "subcompartment": {"@xml:lang": "en", "#text": "in water"},
            },
        },
        field_mapping["target"],
    )

    actual = s.unit.conversion_factor(t.unit)
    expected = 1
    assert actual == expected


def test_get_conversion_factor_m2a(field_mapping):
    s = Flow(
        {
            "name": "Occupation, annual crop",
            "unit": "m2a",
            "categories": ["Resources", "land"],
        },
        field_mapping["source"],
    )

    t = Flow(
        {
            "@id": "c5aafa60-495c-461c-a1d4-b262a34c45b9",
            "@unitId": "eb955b7c-7bed-401f-9c76-5db716ca3640",
            "name": {"@xml:lang": "en", "#text": "Occupation, annual crop"},
            "unitName": {"@xml:lang": "en", "#text": "m2*year"},
            "compartment": {
                "@subcompartmentId": "7d704b6f-d455-4f41-9c28-50b4f372f315",
                "compartment": {"@xml:lang": "en", "#text": "natural resource"},
                "subcompartment": {"@xml:lang": "en", "#text": "land"},
            },
        },
        field_mapping["target"],
    )

    actual = s.unit.conversion_factor(t.unit)
    expected = 1
    assert actual == expected


def test_get_conversion_factor_nan(field_mapping):
    s = Flow(
        {
            "name": "Radium-226/kg",
            "unit": "kg",
            "categories": ["Emissions to water", ""],
        },
        field_mapping["source"],
    )

    t = Flow(
        {
            "@id": "74a0aabb-e11b-4f3b-8921-45e447b33393",
            "@unitId": "4923348e-591b-4772-b224-d19df86f04c9",
            "@casNumber": "013982-63-3",
            "name": {"@xml:lang": "en", "#text": "Radium-226"},
            "unitName": {"@xml:lang": "en", "#text": "kBq"},
            "compartment": {
                "@subcompartmentId": "65f8d2a1-63ed-479c-b86c-3bcf38e86320",
                "compartment": {"@xml:lang": "en", "#text": "water"},
                "subcompartment": {"@xml:lang": "en", "#text": "ocean"},
            },
        },
        field_mapping["target"],
    )

    actual = s.unit.conversion_factor(t.unit)
    assert math.isnan(actual)
