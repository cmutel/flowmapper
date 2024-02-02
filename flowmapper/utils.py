import copy
import json
from collections import Counter
from pathlib import Path
import hashlib
import re
from typing import Optional, Union
import unicodedata
from randonneur import migrate_datasets
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
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
    fields = getattr(module, 'config', None)
    if not fields:
        raise Exception(f'{filepath} does not define a dict named config with field mapping information.')

    result = {
        'source': {},
        'target': {}
    }

    for key, values in fields.items():
        if len(values) == 1:
            result['source'][key] = values[0]
            result['target'][key] = values[0]
        else:
            result['source'][key] = values[0]
            result['target'][key] = values[1]
    
    return result


def generate_flow_id(flow: dict):
    flow_str = json.dumps(flow, sort_keys=True)
    result = hashlib.md5(flow_str.encode('utf-8')).hexdigest()
    return result


def read_flowlist(filepath: Path):
    with open(filepath, 'r') as fs:
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
        with open(filepath, 'r') as fs:
            migration_data.extend(json.load(fs))
    
    result = {'update': migration_data}
    return result

def rm_parentheses_roman_numerals(s: str):
    pattern = r'\(\s*([ivxlcdm]+)\s*\)'
    return re.sub(pattern, r'\1', s)

def rm_roman_numerals_ionic_state(s: str):
    pattern = r'\s*\(\s*[ivxlcdm]+\s*\)'
    return re.sub(pattern, '', s)

def extract_country_code(s: str) -> tuple[str, Optional[str]]:
    # Regex to find a two-letter uppercase code following a comma and optional whitespace
    match = re.search(r',\s*([a-z]{2})$', s)

    if match:
        # Extract the country code and the preceding part of the string
        country_code = match.group(1)
        rest_of_string = s[:match.start()].strip()
        return (rest_of_string, country_code)
    else:
        return (s, None)

def normalize_str(s):
    return unicodedata.normalize('NFC', s).strip().lower()

def transform_flow(flow, transformation):
    result = copy.copy(flow)
    result.update(transformation['target'])
    return result

def matcher(source, target):
    return all(target.get(key) == value for key, value in source.items())

def find_transformation(flow, transformations):
    if not transformations:
        return None
    for transformation in transformations['update']:
        if matcher(transformation['source'], flow):
            return transformation
