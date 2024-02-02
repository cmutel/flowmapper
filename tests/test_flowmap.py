import pandas as pd
import json
from flowmapper import Flowmap
from flowmapper.match import (
    match_emissions_with_suffix_ion,
    match_identical_names,
)

def test_flowmap_remove_duplicates(source_flows, target_flows, snapshot):
    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.source_flows
    assert actual == snapshot

def test_flowmap_mappings(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.mappings[0]
    assert list(actual.keys()) == [
        "from",
        "to",
        "conversion_factor",
        "match_rule",
        "match_rule_priority",
        "info",
    ]
    assert actual["match_rule"] == "match_identical_names"


def test_flowmap_to_randonneur(source_flows, target_flows, snapshot):
    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.to_randonneur()
    assert actual == snapshot

def test_flowmap_to_randonneur_export(source_flows, target_flows, snapshot, tmp_path):
    flowmap = Flowmap(source_flows, target_flows)
    flowmap.to_randonneur(tmp_path / "randonneur.json")
    with open(tmp_path / "randonneur.json", "r") as fs:
        actual = json.load(fs)
    assert actual == snapshot

def test_flowmap_with_custom_rules_no_match(source_flows, target_flows, snapshot):
    flowmap = Flowmap(
        source_flows,
        target_flows,
        rules=[match_emissions_with_suffix_ion],
    )
    actual = flowmap.mappings
    assert actual == snapshot


def test_flowmap_with_custom_rules_match(source_flows, target_flows, snapshot):
    flowmap = Flowmap(source_flows, target_flows, rules=[match_identical_names])
    actual = flowmap.to_randonneur()
    assert actual == snapshot


def test_flowmap_to_glad(source_flows, target_flows):
    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.to_glad()
    expected = {
        "SourceFlowName": ["1,4-Butanediol", "Ammonia, FR"],
        "SourceFlowUUID": [None, None],
        "SourceFlowContext": ["Air/(unspecified)", "Emissions to air/low. pop."],
        "SourceUnit": ["kg", "kg"],
        "MatchCondition": ["", ""],
        "ConversionFactor": [1.0, 1.0],
        "TargetFlowName": ["1,4-Butanediol", "Ammonia"],
        "TargetFlowUUID": [
            "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
            "0f440cc0-0f74-446d-99d6-8ff0e97a2444",
        ],
        "TargetFlowContext": [
            "air/unspecified",
            "air/non-urban air or from high stacks",
        ],
        "TargetUnit": ["kg", "kg"],
        "MemoMapper": ["Identical names", "Names with country code"],
    }
    assert actual.equals(pd.DataFrame(expected))

def test_flowmap_to_glad_export(source_flows, target_flows, tmp_path):
    flowmap = Flowmap(source_flows, target_flows)
    flowmap.to_glad(tmp_path / "glad.xlsx")
    actual = pd.read_excel(tmp_path / "glad.xlsx")
    expected = {
        "SourceFlowName": ["1,4-Butanediol", "Ammonia, FR"],
        "SourceFlowUUID": [float("nan"), float("nan")],
        "SourceFlowContext": ["Air/(unspecified)", "Emissions to air/low. pop."],
        "SourceUnit": ["kg", "kg"],
        "MatchCondition": [float("nan"), float("nan")],
        "ConversionFactor": [1, 1],
        "TargetFlowName": ["1,4-Butanediol", "Ammonia"],
        "TargetFlowUUID": [
            "09db39be-d9a6-4fc3-8d25-1f80b23e9131",
            "0f440cc0-0f74-446d-99d6-8ff0e97a2444",
        ],
        "TargetFlowContext": [
            "air/unspecified",
            "air/non-urban air or from high stacks",
        ],
        "TargetUnit": ["kg", "kg"],
        "MemoMapper": ["Identical names", "Names with country code"],
    }
    assert actual.equals(pd.DataFrame(expected))

def test_flowmap_export_matched(source_flows, target_flows, snapshot):
    flowmap = Flowmap(source_flows, target_flows)
    actual = [flow.raw for flow in flowmap.matched_source]
    assert actual == snapshot

def test_flowmap_export_unmatched(source_flows, target_flows, snapshot):
    flowmap = Flowmap(source_flows, target_flows)
    actual = [flow.raw for flow in flowmap.unmatched_source]
    assert actual == snapshot

def test_flowmap_nomatch_rule(source_flows, target_flows, snapshot):
    nomatch = lambda flow: flow.context.value == "air/urban air close to ground"
    flowmap = Flowmap(source_flows, target_flows, nomatch_rules=[nomatch])

    actual = [flow.raw for flow in flowmap.source_flows_nomatch]
    assert actual == snapshot

def test_flowmap_nomatch_rule_false(source_flows, target_flows, snapshot):
    nomatch = lambda flow: flow.context.value == "water"
    flowmap = Flowmap(source_flows, target_flows, nomatch_rules=[nomatch])

    actual = [flow.raw for flow in flowmap.source_flows]
    assert actual == snapshot

def test_flowmap_nomatch_multiple_rules(source_flows, target_flows, snapshot):
    nomatch1 = lambda flow: flow.context.value == "air/urban air close to ground"
    nomatch2 = lambda flow: flow.context.value == "air"
    flowmap = Flowmap(source_flows, target_flows, nomatch_rules=[nomatch1, nomatch2])

    actual = [flow.raw for flow in flowmap.source_flows_nomatch]
    assert actual == snapshot

def test_flowmap_mappings_ei_ei(target_flows, snapshot):
    flowmap = Flowmap(target_flows, target_flows)
    actual = flowmap.to_randonneur()
    assert actual == snapshot

def test_flowmap_mappings_ei39_ei310(flows_ei39, flows_ei310, snapshot):
    flowmap = Flowmap(flows_ei39, flows_ei310)
    actual = flowmap.to_randonneur()
    assert actual == snapshot
