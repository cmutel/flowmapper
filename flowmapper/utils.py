import copy
import hashlib
import json
import re
import unicodedata
from collections.abc import Collection, Mapping
from pathlib import Path
from typing import Any, List, Optional, Union


def generate_flow_id(flow: dict):
    flow_str = json.dumps(flow, sort_keys=True)
    result = hashlib.md5(flow_str.encode("utf-8")).hexdigest()
    return result


def read_flowlist(filepath: Path):
    with open(filepath, "r") as fs:
        result = json.load(fs)
    return result


def read_migration_files(*filepaths: Union[str, Path]) -> List[dict]:
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
        with open(Path(filepath), "r") as fs:
            migration_data.append(json.load(fs))

    return migration_data


def rm_parentheses_roman_numerals(s: str):
    pattern = r"\(\s*([ivxlcdm]+)\s*\)"
    return re.sub(pattern, r"\1", s)


def rm_roman_numerals_ionic_state(s: str):
    pattern = r"\s*\(\s*[ivxlcdm]+\s*\)"
    return re.sub(pattern, "", s)


def extract_country_code(s: str) -> tuple[str, Optional[str]]:
    # Regex to find a two-letter uppercase code following a comma and optional whitespace
    match = re.search(r",\s*([a-z]{2})$", s)

    if match:
        # Extract the country code and the preceding part of the string
        country_code = match.group(1)
        rest_of_string = s[: match.start()].strip()
        return (rest_of_string, country_code)
    else:
        return (s, None)


def normalize_str(s):
    if s is not None:
        return unicodedata.normalize("NFC", s).strip()
    else:
        return ""


def transform_flow(flow, transformation):
    result = copy.copy(flow)
    result.update(transformation["target"])
    return result


def matcher(source, target):
    return all(target.get(key) == value for key, value in source.items())


def rowercase(obj: Any) -> Any:
    """Recursively transform everything to lower case recursively"""
    if isinstance(obj, str):
        return obj.lower()
    elif isinstance(obj, Mapping):
        return type(obj)([(rowercase(k), rowercase(v)) for k, v in obj.items()])
    elif isinstance(obj, Collection):
        return type(obj)([rowercase(o) for o in obj])
    else:
        return obj


def match_sort_order(obj: dict) -> tuple:
    return (
        not obj["from"].name,
        obj["from"].name.normalized,
        not obj["from"].context,
        obj["from"].context.export_as_string(),
    )


def apply_transformations(obj: dict, transformations: List[dict] | None) -> dict:
    if not transformations:
        return obj
    obj = copy.deepcopy(obj)
    lower = rowercase(obj)

    for dataset in transformations:
        for transformation_obj in dataset.get("create", []):
            if matcher(
                transformation_obj,
                lower if dataset.get("case-insensitive") else obj,
            ):
                # Marked an needs to be created; missing in target list
                obj["__missing__"] = True
                break
        for transformation_obj in dataset.get("update", []):
            if transformation_obj["source"] == obj:
                obj.update(transformation_obj["target"])
                if "conversion_factor" in transformation_obj:
                    obj["conversion_factor"] = transformation_obj["conversion_factor"]
                break

    return obj
