from flowmapper.utils import generate_flow_id


def test_generate_flow_id():
    flow1 = {
        "name": "1,4-Butanediol",
        "categories": ["Air", "(unspecified)"],
        "unit": "kg",
        "CAS": "000110-63-4",
    }

    flow2 = {
        "CAS": "000110-63-4",
        "name": "1,4-Butanediol",
        "categories": [
            "Air",
            "(unspecified)",
        ],
        "unit": "kg",
    }

    expected = "9b680160081438f81d551c724c30b09b"
    assert generate_flow_id(flow1) == expected
    assert generate_flow_id(flow2) == expected
