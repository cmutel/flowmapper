from flowmapper.flow import Flow
from flowmapper.match import match_biogenic_to_non_fossil

def test_match_biogenic_to_non_fossil():
    fields = {"name": "name", "context": "context", "unit": "unit"}
    s = Flow({"name": "Oils, biogenic", "context": "air", "unit": "kg"}, fields)
    t = Flow({"name": "Oils, non-fossil", "context": "air", "unit": "kg"}, fields)

    actual = match_biogenic_to_non_fossil(s, t)
    expected = {
        "comment": "Biogenic to non-fossil if no better match"
    }
    assert actual == expected
