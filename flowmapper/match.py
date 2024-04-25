import importlib.resources as resource
import re
import json
import math
import logging

from .flow import Flow
from .utils import (
    rm_parentheses_roman_numerals,
    rm_roman_numerals_ionic_state,
)

logger = logging.getLogger(__name__)

with resource.as_file(resource.files("flowmapper") / "data" / "places.json") as filepath:
    places = json.load(open(filepath))

ends_with_location = re.compile(",[ \t\r\f]+(?P<code>{})$".format("|".join([re.escape(string) for string in places])), re.IGNORECASE)
# All solutions I found for returning original string instead of
# lower case one were very ugly
location_reverser = {obj.lower(): obj for obj in places}

with resource.as_file(resource.files("flowmapper") / "data" / "names_and_locations.json") as filepath:
    names_and_locations = {o['source']: o for o in json.load(open(filepath))}


def format_match_result(s: Flow, t: Flow, conversion_factor: float, match_info: dict):
    target_result = t.export
    if match_info.get("location"):
        target_result.update({"location": match_info["location"]})

    result = {
        "source": s.export,
        "target": target_result,
        "conversion_factor": conversion_factor,
        "comment": match_info["comment"],
    }
    return result


def match_identical_identifier(s: Flow, t: Flow, comment: str = "Identical identifier"):
    if s.identifier and (s.identifier == t.identifier):
        return {"comment": comment}


def match_identical_names_in_synonyms(
    s: Flow, t: Flow, comment: str = "Identical synonyms"
):
    if (
        (t.synonyms and s.name in t.synonyms and s.context == t.context)
        or (s.synonyms and t.name in s.synonyms and s.context == t.context)
    ) and not math.isnan(s.unit.conversion_factor(t.unit)):
        return {"comment": comment}


def match_identical_cas_numbers(
    s: Flow, t: Flow, comment: str = "Identical CAS numbers"
):
    if (s.cas == t.cas) and (s.context == t.context):
        return {"comment": comment}


def match_identical_names(s: Flow, t: Flow, comment="Identical names"):
    if (s.name == t.name) and (s.context == t.context):
        return {"comment": comment}


def match_resources_with_wrong_subcontext(s: Flow, t: Flow):
    if (
        "resource" in s.context.normalized[0].lower()
        and "resource" in t.context.normalized[0].lower()
        and s.name == t.name
    ):
        return {"comment": "Resources with identical name but wrong subcontext"}


def match_identical_names_except_missing_suffix(
    s: Flow, t: Flow, suffix, comment="Identical names except missing suffix"
):
    if (
        (f"{s.name.normalized}, {suffix}" == t.name)
        or (f"{t.name.normalized}, {suffix}" == s.name)
        or (f"{s.name.normalized} {suffix}" == t.name)
        or (f"{t.name.normalized} {suffix}" == s.name)
    ) and s.context == t.context:
        return {"comment": comment}


def match_names_with_roman_numerals_in_parentheses(
    s: Flow, t: Flow, comment="With/without roman numerals in parentheses"
):
    if (
        rm_parentheses_roman_numerals(s.name.normalized)
        == rm_parentheses_roman_numerals(t.name.normalized)
        and s.context == t.context
    ):
        return {"comment": comment}


def match_custom_names_with_location_codes(s: Flow, t: Flow, comment="Custom names with location code"):
    match = ends_with_location.search(s.name.normalized)
    if match:
        location = location_reverser[match.group('code')]
        name = s.name.normalized.replace(match.group(), "")
        try:
            mapped_name = names_and_locations[name]['target']
        except KeyError:
            return
        if mapped_name == t.name.normalized and s.context == t.context:
            result = {"comment": comment, "location": location} | names_and_locations[name].get('extra', {})
            if (
                s.name.normalized.startswith("water")
                and s.unit.normalized == "cubic_meter"
                and t.unit.normalized == "kilogram"
            ):
                result["conversion_factor"] = 1000
            elif (
                s.name.normalized.startswith("water")
                and t.unit.normalized == "cubic_meter"
                and s.unit.normalized == "kilogram"
            ):
                result["conversion_factor"] = 0.001
            return result


def match_names_with_location_codes(s: Flow, t: Flow, comment="Name matching with location code"):
    match = ends_with_location.search(s.name.normalized)
    if match:
        location = location_reverser[match.group('code')]
        name = s.name.normalized.replace(match.group(), "")
        if name == t.name.normalized and s.context == t.context:
            result = {"comment": comment, "location": location}
            if (
                s.name.normalized.startswith("water")
                and s.unit.normalized == "cubic_meter"
                and t.unit.normalized == "kilogram"
            ):
                result["conversion_factor"] = 1000.
            elif (
                s.name.normalized.startswith("water")
                and t.unit.normalized == "cubic_meter"
                and s.unit.normalized == "kilogram"
            ):
                result["conversion_factor"] = 0.001
            return result


def match_non_ionic_state(
    s: Flow, t: Flow, comment="Non-ionic state if no better match"
):
    if (
        rm_roman_numerals_ionic_state(s.name.normalized) == t.name
        and s.context == t.context
    ):
        return {"comment": comment}


def match_biogenic_to_non_fossil(
    s: Flow, t: Flow, comment="Biogenic to non-fossil if no better match"
):
    if (
        s.name.normalized.removesuffix(", biogenic")
        == t.name.normalized.removesuffix(", non-fossil")
        and s.context == t.context
    ):
        return {"comment": comment}


def match_resources_with_suffix_in_ground(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(
        s, t, suffix="in ground", comment="Resources with suffix in ground"
    )


def match_flows_with_suffix_unspecified_origin(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(
        s, t, suffix="unspecified origin", comment="Flows with suffix unspecified origin"
    )


def match_resources_with_suffix_in_water(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(
        s, t, suffix="in water", comment="Resources with suffix in water"
    )


def match_resources_with_suffix_in_air(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(
        s, t, suffix="in air", comment="Resources with suffix in air"
    )


def match_emissions_with_suffix_ion(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(
        s, t, suffix="ion", comment="Match emissions with suffix ion"
    )


def match_rules():
    return [
        match_identical_identifier,
        match_identical_names,
        match_resources_with_suffix_in_ground,
        match_resources_with_suffix_in_water,
        match_resources_with_suffix_in_air,
        match_flows_with_suffix_unspecified_origin,
        match_resources_with_wrong_subcontext,
        match_emissions_with_suffix_ion,
        match_names_with_roman_numerals_in_parentheses,
        match_names_with_location_codes,
        match_custom_names_with_location_codes,
        match_identical_cas_numbers,
        match_non_ionic_state,
        match_biogenic_to_non_fossil,
        match_identical_names_in_synonyms,
    ]
