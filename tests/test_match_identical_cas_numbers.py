from deepdiff import DeepDiff

from flowmapper.flow import Flow
from flowmapper.match import match_identical_cas_numbers


def test_match_identical_cas_numbers(fields):
    source = {
        "Flowable": "1-Propanol",
        "CAS No": "000071-23-8",
        "Formula": "",
        "Synonyms": "1-Propanol",
        "Unit": "kg",
        "Class": "Waterborne emissions",
        "Context": "Emissions to water/groundwater",
        "Flow UUID": "8C31919B-2D42-4CAD-A10E-8084CCD6BE99",
        "Description": "Formula: C3H8O\u007f",
    }

    target = {
        "Flowable": "Propanol",
        "CASNo": "000071-23-8",
        "Formula": "",
        "Synonyms": "propan-1-ol, 1-propanol, propyl alcohol, n-propanol, n-propyl alcohol",
        "Unit": "kg",
        "Class": "chemical",
        "ExternalReference": "",
        "Preferred": "",
        "Context": "water/ground-",
        "FlowUUID": "85500204-9d88-40ae-9f0b-3ceba0e7a74f",
        "AltUnit": "",
        "Var": "",
        "Second CAS": "71-31-8; 19986-23-3; 71-23-8; 64118-40-7; 4712-36-1; 142583-61-7; 71-23-8",
    }

    s = Flow(source, fields['source'])
    t = Flow(target, fields['target'])

    match = match_identical_cas_numbers(s, t)
    assert match


def test_match_missing_cas_numbers(fields):
    source = {
        "Flowable": "1-Propanol",
        "CAS No": "",
        "Formula": "",
        "Synonyms": "1-Propanol",
        "Unit": "kg",
        "Class": "Waterborne emissions",
        "Context": "Emissions to water/groundwater",
        "Flow UUID": "8C31919B-2D42-4CAD-A10E-8084CCD6BE99",
        "Description": "Formula: C3H8O\u007f",
    }

    target = {
        "Flowable": "Propanol",
        "CASNo": "",
        "Formula": "",
        "Synonyms": "propan-1-ol, 1-propanol, propyl alcohol, n-propanol, n-propyl alcohol",
        "Unit": "kg",
        "Class": "chemical",
        "ExternalReference": "",
        "Preferred": "",
        "Context": "water/ground-",
        "FlowUUID": "85500204-9d88-40ae-9f0b-3ceba0e7a74f",
        "AltUnit": "",
        "Var": "",
        "Second CAS": "71-31-8; 19986-23-3; 71-23-8; 64118-40-7; 4712-36-1; 142583-61-7; 71-23-8",
    }

    s = Flow(source, fields['source'])
    t = Flow(target, fields['target'])

    match = match_identical_cas_numbers(s, t)
    assert not match
