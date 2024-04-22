import logging

from .flow import Flow
from .utils import (
    extract_country_code,
    rm_parentheses_roman_numerals,
    rm_roman_numerals_ionic_state,
)

logger = logging.getLogger(__name__)


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
    ) and s.unit.conversion_factor(t.unit):
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


def match_names_with_country_codes(s: Flow, t: Flow, comment="Names with country code"):
    s_name, s_location = extract_country_code(s.name.normalized)
    if s_location and s_name == t.name and s.context == t.context:
        result = {"comment": comment, "location": s_location.upper()}
        if (
            s.name.normalized.lower().startswith("water")
            and t.name.normalized.lower().startswith("water")
            and s.unit.normalized == "cubic_meter"
            and t.unit.normalized == "kilogram"
        ):
            result["conversion_factor"] = 1000
        elif (
            s.name.normalized.lower().startswith("water")
            and t.name.normalized.lower().startswith("water")
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


def match_emissions_with_suffix_ion(s: Flow, t: Flow):
    return match_identical_names_except_missing_suffix(
        s, t, suffix="ion", comment="Match emissions with suffix ion"
    )


def match_rules():
    return [
        match_identical_identifier,
        match_identical_names,
        match_resources_with_suffix_in_ground,
        match_resources_with_wrong_subcontext,
        match_emissions_with_suffix_ion,
        match_names_with_roman_numerals_in_parentheses,
        match_names_with_country_codes,
        match_identical_cas_numbers,
        match_non_ionic_state,
        match_biogenic_to_non_fossil,
        match_identical_names_in_synonyms,
    ]
