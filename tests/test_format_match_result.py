from deepdiff import DeepDiff
from flowmapper.match import format_match_result
from flowmapper.flow import Flow

def test_format_match_result_missing_id():
    source = {
        "name": "Carbon dioxide, in air",
        "context": "Raw materials",
        "unit": "kg",
    }

    source_fields = {
            "uuid": "",
            "name": "name",
            "context": "context",
            "unit": "unit",
        }

    s = Flow(source, source_fields)

    target = {
        "id": "cc6a1abb-b123-4ca6-8f16-38209df609be",
        "name": "Carbon dioxide, in air",
        "context": "natural resource/in air",
        "unit": "kg",
    }

    target_fields = {
            "uuid": "id",
            "name": "name",
            "context": "context",
            "unit": "unit",
        }

    t = Flow(target, target_fields)

    actual = format_match_result(s, t, 1.0, {'is_match': True, 'comment': 'foo'})
    expected = {'source': {'name': 'Carbon dioxide, in air', 'context': 'Raw materials', 'unit': 'kg'}, 
                'target': {'uuid': 'cc6a1abb-b123-4ca6-8f16-38209df609be', 
                           'name': 'Carbon dioxide, in air',
                           'context': 'natural resource/in air',
                           'unit': 'kg'}, 
                'conversion_factor': 1.0,
                'comment': 'foo'}

    diff = DeepDiff(actual, expected)
    assert not diff
