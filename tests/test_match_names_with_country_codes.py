from flowmapper.flow import Flow
from flowmapper.match import match_names_with_location_codes


def test_match_names_with_country_codes():
    s = Flow({"name": "Ammonia, NL", "context": "air", "unit": "kg"})
    t = Flow({"name": "Ammonia", "context": "air", "unit": "kg"})

    actual = match_names_with_location_codes(s, t)
    expected = {"comment": "Names with location code", "location": "NL"}
    assert actual == expected
