"""Fixtures for flowmapper"""

import pytest
from flowmapper.utils import read_field_mapping, read_flowlist, read_migration_files
from flowmapper.flow import Flow

@pytest.fixture
def field_mapping():
    result = {
        "source": {
            "name": "name",
            "context": "categories",
            "unit": "unit",
        },
        "target": {
            "uuid": "@id",
            "context": "compartment.*.#text",
            "name": "name.#text",
            "synonyms": ("synonym", ["#text"]),
            "unit": "unitName.#text",
        },
    }
    return result


@pytest.fixture
def fields():
    result = {
        "source": {
            "uuid": "Flow UUID",
            "name": "Flowable",
            "context": "Context",
            "unit": "Unit",
            "cas": "CAS No",
        },
        "target": {
            "uuid": "FlowUUID",
            "name": "Flowable",
            "context": "Context",
            "unit": "Unit",
            "cas": "CASNo",
        },
    }

    return result


@pytest.fixture
def source_flows():
    fields = read_field_mapping("tests/data/field_mapping-sp-ei.py")
    result = [
        Flow(flow, fields["source"]) for flow in read_flowlist("tests/data/sp.json")
    ]
    return result


@pytest.fixture
def target_flows():
    fields = read_field_mapping("tests/data/field_mapping-sp-ei.py")
    result = [
        Flow(flow, fields["target"]) for flow in read_flowlist("tests/data/ei-3.7.json")
    ]
    return result


@pytest.fixture
def flows_ei39():
    transformations = read_migration_files("tests/data/migrations.json")
    fields = {
        "uuid": "@id",
        "name": "name.#text",
        "synonyms": ("synonym", ["#text"]),
        "context": "compartment.*.#text",
        "unit": "unitName.#text",
        "cas": "@casNumber",
    }
    result = [Flow(flow, fields, transformations) for flow in read_flowlist("tests/data/ei-3.9.json")]
    return result


@pytest.fixture
def flows_ei310():
    fields = {
        "uuid": "@id",
        "name": "name.#text",
        "synonyms": ("synonym", ["#text"]),
        "context": "compartment.*.#text",
        "unit": "unitName.#text",
        "cas": "@casNumber",
    }
    result = [Flow(flow, fields) for flow in read_flowlist("tests/data/ei-3.10.json")]
    return result
