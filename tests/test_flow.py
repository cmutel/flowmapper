from flowmapper.cas import CASField
from flowmapper.flow import Flow
from flowmapper.transformation_mapping import prepare_transformations


def test_flow_with_transformations_repr():
    d = {
        "name": "Carbon dioxide, in air",
        "context": ["Raw", "(unspecified)"],
        "unit": "kg",
        "cas": "000124-38-9",
    }

    transformations = prepare_transformations(
        [
            {
                "update": [
                    {
                        "source": {
                            "name": "Carbon dioxide, in air",
                            "context": ["Raw", "(unspecified)"],
                        },
                        "target": {"name": "Carbon dioxide"},
                    }
                ]
            }
        ]
    )

    f = Flow(d, transformations=transformations)
    expected = """Flow object:
    Identifier: StringField with missing original value
    Name: StringField: 'Carbon dioxide, in air' -> 'carbon dioxide'
    Context: ContextField: '['Raw', '(unspecified)']' -> '('raw',)'
    Unit: UnitField: 'kg' -> 'kg'"""

    assert repr(f) == expected


def test_flow_from_sp_categories(transformations):
    data = {
        "name": "Carbon dioxide, in air",
        "context": "resources/in air",
        "unit": "kg",
        "CAS number": "000124-38-9",
    }

    flow = Flow(data, transformations)
    assert not flow.identifier
    assert flow.name.original == "Carbon dioxide, in air"
    assert flow.name.normalized == "carbon dioxide, in air"
    assert flow.context.original == "resources/in air"
    assert flow.context.normalized == ("natural resource", "in air")


def test_flow_from_sp_missing(transformations):
    data = {"name": "Chrysotile", "context": "Raw/in ground", "unit": "kg"}

    flow = Flow(data, transformations)
    assert flow.name.original == "Chrysotile"
    expected = """Flow object:
    Identifier: StringField with missing original value
    Name: StringField: 'Chrysotile' -> 'chrysotile'
    Context: ContextField: 'Raw/in ground' -> '('natural resource', 'in ground')'
    Unit: UnitField: 'kg' -> 'kilogram'"""
    assert repr(flow) == expected
    assert flow.context.original == "Raw/in ground"
    assert flow.context.normalized == ("natural resource", "in ground")


def test_flow_cas():
    data = {
        "name": "Actinium",
        "CAS number": "007440-34-8",
        "chemical formula": "Ac\u007f",
        "synonyms": "Actinium",
        "unit": "kg",
        "Class": "Raw materials",
        "context": "Raw materials",
        "Description": "",
    }

    fields = {
        "identifier": "Flow UUID",
        "name": "name",
        "context": "context",
        "unit": "unit",
        "CAS number": "CAS No",
    }

    flow = Flow(data)
    assert flow.cas == CASField("007440-34-8")
    assert flow.cas == "7440-34-8"


def test_flow_from_ei():
    data = {
        "name": "1,3-Dioxolan-2-one",
        "CAS number": "000096-49-1",
        "chemical formula": "",
        "synonyms": "",
        "unit": "kg",
        "Class": "chemical",
        "ExternalReference": "",
        "Preferred": "",
        "context": "water/unspecified",
        "identifier": "5b7d620e-2238-5ec9-888a-6999218b6974",
        "AltUnit": "",
        "Var": "",
        "Second CAS": "96-49-1",
    }
    flow = Flow(data)
    assert flow.identifier == "5b7d620e-2238-5ec9-888a-6999218b6974"


def test_flow_with_synonyms(transformations):
    data = {
        "identifier": "f0cc0453-32c0-48f5-b8d4-fc87d100b8d9",
        "CAS number": "000078-79-5",
        "name": "Isoprene",
        "unit": "kg",
        "context": ["air", "low population density, long-term"],
        "synonyms": [
            "2-methylbuta-1,3-diene",
            "methyl bivinyl",
            "hemiterpene",
        ],
    }

    flow = Flow(data, transformations)
    assert [obj.original for obj in flow.synonyms] == [
        "2-methylbuta-1,3-diene",
        "methyl bivinyl",
        "hemiterpene",
    ]
