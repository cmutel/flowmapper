from flowmapper.flow import Flow
from flowmapper.match import match_custom_names_with_location_codes


def test_match_names_with_country_codes():
    s = Flow({"name": "Water (ersatz), net cons., irrigation, HU", "context": "air", "unit": "kg"})
    t = Flow({"name": "water, unspecified natural origin", "context": "air", "unit": "kg"})

    actual = match_custom_names_with_location_codes(s, t)
    expected = {"comment": "Custom names with location code", "location": "HU", "irrigation": True}
    assert actual == expected
