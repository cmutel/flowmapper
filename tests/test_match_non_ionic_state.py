from flowmapper.flow import Flow
from flowmapper.flowmap import Flowmap


def test_match_non_ionic_state():
    s = [
        Flow({"name": "Mercury (II)", "context": "air", "unit": "kg"}),
        Flow({"name": "Manganese (II)", "context": "air", "unit": "kg"}),
    ]
    t = [
        Flow({"name": "Mercury", "context": "air", "unit": "kg", "identifier": "foo"}),
        Flow(
            {
                "name": "Manganese II",
                "context": "air",
                "unit": "kg",
                "identifier": "bar",
            }
        ),
    ]

    flowmap = Flowmap(s, t)
    actual = flowmap.to_randonneur()
    expected = [
        {
            "source": {"name": "Manganese (II)", "context": "air", "unit": "kg"},
            "target": {
                "identifier": "bar",
                "name": "Manganese II",
                "context": "air",
                "unit": "kg",
            },
            "conversion_factor": 1.0,
            "comment": "With/without roman numerals in parentheses",
        },
        {
            "source": {"name": "Mercury (II)", "context": "air", "unit": "kg"},
            "target": {
                "identifier": "foo",
                "name": "Mercury",
                "context": "air",
                "unit": "kg",
            },
            "conversion_factor": 1.0,
            "comment": "Non-ionic state if no better match",
        },
    ]
    assert actual == expected
