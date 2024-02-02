from flowmapper.flow import Flow
from flowmapper.match import match_names_with_country_codes

def test_match_names_with_country_codes():
    fields = {"name": "name", "context": "context", "unit": "unit"}
    s = Flow({"name": "Ammonia, NL", "context": "air", "unit": "kg"}, fields)
    t = Flow({"name": "Ammonia", "context": "air", "unit": "kg"}, fields)

    actual = match_names_with_country_codes(s, t)
    expected = {
        "comment": "Names with country code", "location": "NL"
    }
    assert actual == expected
