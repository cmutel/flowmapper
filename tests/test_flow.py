from flowmapper.cas import CAS
from flowmapper.flow import Flow

def test_flow_with_transformations_repr():
    d = {
        "name": "Carbon dioxide, in air",
        "context": ["Raw", "(unspecified)"],
        "unit": "kg",
        "cas": "000124-38-9",
    }

    transformations = {"update": [
        {
            "source": {"name": "Carbon dioxide, in air", "context": ["Raw", "(unspecified)"]},
            "target": {"name": "Carbon dioxide"},
        }
    ]}

    f = Flow(d, transformations=transformations)
    
    assert repr(f) == "Carbon dioxide, in air* (in kg) <Raw/(unspecified)> [uuid:None]"


def test_flow_with_jsonpath_expr():
    data = {
        "@id": "87883a4e-1e3e-4c9d-90c0-f1bea36f8014",
        "@unitId": "487df68b-4994-4027-8fdc-a4dc298257b7",
        "@casNumber": "007664-41-7",
        "name": {"@xml:lang": "en", "#text": "Ammonia"},
        "unitName": {"@xml:lang": "en", "#text": "kg"},
        "compartment": {
            "@subcompartmentId": "7011f0aa-f5f9-4901-8c10-884ad8296812",
            "compartment": {"@xml:lang": "en", "#text": "air"},
            "subcompartment": {"@xml:lang": "en", "#text": "unspecified"},
        },
    }

    fields = {
        "cas": "@casNumber",
        "context": "compartment.*.#text",
        "name": "name.#text",
        "unit": "unitName.#text",
        "uuid": "@id",
    }

    flow = Flow(data, fields)
    assert flow.name.value == "ammonia"
    assert flow.name.raw_value == "Ammonia"
    assert flow.name.raw_object == {"name": {"@xml:lang": "en", "#text": "Ammonia"}}
    assert not flow.synonyms
    assert flow.context.value == "air"
    assert flow.unit.value == "kilogram"
    assert flow.unit.raw_value == "kg"
    assert flow.unit.raw_object == {"unitName": {"@xml:lang": "en", "#text": "kg"}}


def test_flow_from_sp_categories():
    data = {
        "name": "Carbon dioxide, in air",
        "categories": ["Raw", "(unspecified)"],
        "unit": "kg",
        "CAS": "000124-38-9",
    }

    fields = {
        "name": "name",
        "context": "categories",
        "unit": "unit",
        "cas": "CAS",
    }

    flow = Flow(data, fields)
    assert flow.uuid is None
    assert flow.name.raw_value == "Carbon dioxide, in air"
    assert flow.context.raw_value == "Raw/(unspecified)"
    assert id(flow.raw) == id(data)


def test_flow_from_sp_missing():
    data = {"name": "Chrysotile", "context": ["Resources", "in ground"], "unit": "kg"}

    fields = {
        "name": "name",
        "context": "context",
        "unit": "unit",
    }

    flow = Flow(data, fields)
    assert flow.name.raw_value == "Chrysotile"
    assert repr(flow.cas) == ""
    assert flow.context.raw_value == "Resources/in ground"


def test_flow_from_sp():
    data = {
        "Flowable": "Actinium",
        "CAS No": "007440-34-8",
        "Formula": "Ac\u007f",
        "Synonyms": "Actinium",
        "Unit": "kg",
        "Class": "Raw materials",
        "Context": "Raw materials",
        "Flow UUID": "90004354-71D3-47E8-B322-300BA5A98F7B",
        "Description": "",
    }

    fields = {
        "uuid": "Flow UUID",
        "name": "Flowable",
        "context": "Context",
        "unit": "Unit",
        "cas": "CAS No",
    }

    flow = Flow(data, fields)
    assert flow.uuid == "90004354-71D3-47E8-B322-300BA5A98F7B"
    assert flow.cas == CAS("007440-34-8")
    assert flow.cas.cas == "7440-34-8"


def test_flow_from_ei():
    data = {
        "Flowable": "1,3-Dioxolan-2-one",
        "CASNo": "000096-49-1",
        "Formula": "",
        "Synonyms": "",
        "Unit": "kg",
        "Class": "chemical",
        "ExternalReference": "",
        "Preferred": "",
        "Context": "water/unspecified",
        "FlowUUID": "5b7d620e-2238-5ec9-888a-6999218b6974",
        "AltUnit": "",
        "Var": "",
        "Second CAS": "96-49-1",
    }

    fields = {
        "uuid": "FlowUUID",
        "name": "Flowable",
        "context": "Context",
        "unit": "Unit",
        "cas": "CASNo",
    }

    flow = Flow(data, fields)
    assert flow.uuid == "5b7d620e-2238-5ec9-888a-6999218b6974"


def test_flow_with_synonyms(field_mapping):
    data = {
        "@id": "f0cc0453-32c0-48f5-b8d4-fc87d100b8d9",
        "@unitId": "487df68b-4994-4027-8fdc-a4dc298257b7",
        "@casNumber": "000078-79-5",
        "name": {"@xml:lang": "en", "#text": "Isoprene"},
        "unitName": {"@xml:lang": "en", "#text": "kg"},
        "compartment": {
            "@subcompartmentId": "23dbff79-8037-43e7-b270-5a3da416a284",
            "compartment": {"@xml:lang": "en", "#text": "air"},
            "subcompartment": {
                "@xml:lang": "en",
                "#text": "low population density, long-term",
            },
        },
        "synonym": [
            {"@xml:lang": "en", "#text": "2-methylbuta-1,3-diene"},
            {"@xml:lang": "en", "#text": "methyl bivinyl"},
            {"@xml:lang": "en", "#text": "hemiterpene"},
        ],
    }

    flow = Flow(data, field_mapping["target"])
    assert flow.synonyms.raw_value == [
        "2-methylbuta-1,3-diene",
        "methyl bivinyl",
        "hemiterpene",
    ]


