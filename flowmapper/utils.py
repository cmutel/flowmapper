import copy
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Optional, Union

import importlib.util


def import_module(filepath):
    filepath = Path(filepath)
    module_name = filepath.stem
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_field_mapping(filepath: Path):
    module = import_module(filepath)
    fields = getattr(module, "config", None)
    if not fields:
        raise Exception(
            f"{filepath} does not define a dict named config with field mapping information."
        )

    result = {"source": {}, "target": {}}

    for key, values in fields.items():
        if len(values) == 1:
            result["source"][key] = values[0]
            result["target"][key] = values[0]
        else:
            result["source"][key] = values[0]
            result["target"][key] = values[1]

    return result


def generate_flow_id(flow: dict):
    flow_str = json.dumps(flow, sort_keys=True)
    result = hashlib.md5(flow_str.encode("utf-8")).hexdigest()
    return result


def read_flowlist(filepath: Path):
    with open(filepath, "r") as fs:
        result = json.load(fs)
    return result


def read_migration_files(*filepaths: Union[str, Path]):
    """
    Read and aggregate migration data from multiple JSON files.

    This function opens and reads a series of JSON files, each containing migration data as a list of dicts without the change type.
    It aggregates all changes into a single list and returns it wrapped in a dictionary
    under the change type 'update'.

    Parameters
    ----------
    *filepaths : Path
        Variable length argument list of Path objects.

    Returns
    -------
    dict
        A dictionary containing a single key 'update', which maps to a list. This list is
        an aggregation of the data from all the JSON files read.
    """
    migration_data = []

    for filepath in filepaths:
        filepath = Path(filepath)
        with open(filepath, "r") as fs:
            migration_data.extend(json.load(fs))

    result = {"update": migration_data}
    return result


def rm_parentheses_roman_numerals(s: str):
    pattern = r"\(\s*([ivxlcdm]+)\s*\)"
    return re.sub(pattern, r"\1", s)


def rm_roman_numerals_ionic_state(s: str):
    pattern = r"\s*\(\s*[ivxlcdm]+\s*\)"
    return re.sub(pattern, "", s)


COUNTRY_CODES = "|".join(
    {
        "AD",
        "AE",
        "AF",
        "AG",
        "AI",
        "AL",
        "AM",
        "AN",
        "AO",
        "AQ",
        "AR",
        "AS",
        "AT",
        "AU",
        "AW",
        "AX",
        "AZ",
        "BA",
        "BB",
        "BD",
        "BE",
        "BF",
        "BG",
        "BH",
        "BI",
        "BJ",
        "BM",
        "BN",
        "BO",
        "BR",
        "BS",
        "BT",
        "BV",
        "BW",
        "BY",
        "BZ",
        "CA",
        "CC",
        "CD",
        "CF",
        "CG",
        "CH",
        "CI",
        "CK",
        "CL",
        "CM",
        "CN",
        "CO",
        "CR",
        "CS",
        "CU",
        "CV",
        "CX",
        "CY",
        "CZ",
        "DE",
        "DJ",
        "DK",
        "DM",
        "DO",
        "DZ",
        "EC",
        "EE",
        "EG",
        "EH",
        "ER",
        "ES",
        "ET",
        "FI",
        "FJ",
        "FK",
        "FM",
        "FO",
        "FR",
        "GA",
        "GB",
        "GD",
        "GE",
        "GF",
        "GG",
        "GH",
        "GI",
        "GL",
        "GM",
        "GN",
        "GP",
        "GQ",
        "GR",
        "GS",
        "GT",
        "GU",
        "GW",
        "GY",
        "HK",
        "HM",
        "HN",
        "HR",
        "HT",
        "HU",
        "ID",
        "IE",
        "IL",
        "IM",
        "IN",
        "IO",
        "IQ",
        "IR",
        "IS",
        "IT",
        "JE",
        "JM",
        "JO",
        "JP",
        "KE",
        "KG",
        "KH",
        "KI",
        "KM",
        "KN",
        "KP",
        "KR",
        "KW",
        "KY",
        "KZ",
        "LA",
        "LB",
        "LC",
        "LI",
        "LK",
        "LR",
        "LS",
        "LT",
        "LU",
        "LV",
        "LY",
        "MA",
        "MC",
        "MD",
        "MG",
        "MH",
        "MK",
        "ML",
        "MM",
        "MN",
        "MO",
        "MP",
        "MQ",
        "MR",
        "MS",
        "MT",
        "MU",
        "MV",
        "MW",
        "MX",
        "MY",
        "MZ",
        "NA",
        "NC",
        "NE",
        "NF",
        "NG",
        "NI",
        "NL",
        "NO",
        "NP",
        "NR",
        "NU",
        "NZ",
        "OM",
        "PA",
        "PE",
        "PF",
        "PG",
        "PH",
        "PK",
        "PL",
        "PM",
        "PN",
        "PR",
        "PS",
        "PT",
        "PW",
        "PY",
        "QA",
        "RE",
        "RO",
        "RS",
        "RU",
        "RW",
        "SA",
        "SB",
        "SC",
        "SD",
        "SE",
        "SG",
        "SH",
        "SI",
        "SJ",
        "SK",
        "SL",
        "SM",
        "SN",
        "SO",
        "SR",
        "ST",
        "SV",
        "SY",
        "SZ",
        "TC",
        "TD",
        "TF",
        "TG",
        "TH",
        "TJ",
        "TK",
        "TL",
        "TM",
        "TN",
        "TO",
        "TR",
        "TT",
        "TV",
        "TW",
        "TZ",
        "UA",
        "UG",
        "UM",
        "US",
        "UY",
        "UZ",
        "VA",
        "VC",
        "VE",
        "VG",
        "VI",
        "VN",
        "VU",
        "WF",
        "WS",
        "YE",
        "YT",
        "ZA",
        "ZM",
        "ZW",
        "RER",
        "GLO",
        "OECD",
        "Europe",
        "RAF",
    }
)

# Regex to find a two-letter uppercase code following a comma and optional whitespace
country_code_regex = re.compile(r",\s*({})$".format(COUNTRY_CODES))


def extract_country_code(s: str) -> tuple[str, Optional[str]]:
    match = re.search(country_code_regex, s)

    if match:
        # Extract the country code and the preceding part of the string
        country_code = match.group(1)
        rest_of_string = s[: match.start()].strip()
        return (rest_of_string, country_code)
    else:
        return (s, None)


def normalize_str(s):
    return unicodedata.normalize("NFC", s).strip().lower()


def transform_flow(flow, transformation):
    result = copy.copy(flow)
    result.update(transformation["target"])
    return result


def matcher(source, target):
    return all(target.get(key) == value for key, value in source.items())


def find_transformation(flow, transformations):
    if not transformations:
        return None
    for transformation in transformations["update"]:
        if matcher(transformation["source"], flow):
            return transformation
