import json
from pathlib import Path

import xmltodict


def reformat(obj: dict) -> dict:
    data = {
        'identifier': obj['@id'],
        'unit': obj['unitName']['#text'],
        'context': [
            obj['compartment']['compartment']['#text'],
            obj['compartment']['subcompartment']['#text'],
        ],
        'name': obj['name']['#text'],
    }
    if obj.get('synonym') and isinstance(obj['synonym'], list):
        data['synonyms'] = [s['#text'] for s in obj['synonym'] if '#text' in s]
    elif obj.get('synonym') and '#text' in obj['synonym']:
        data['synonyms'] = [obj['synonym']['#text']]
    if "@casNumber" in obj:
        data["CAS number"] = obj['@casNumber']
    return data


def ecospold2_biosphere_extractor(input_path: Path, output_path: Path) -> None:
    if not input_path.name == "ElementaryExchanges.xml":
        raise ValueError("`input_path` must be for a `ElementaryExchanges.xml` file")
    with open(input_path) as fs:
        ei_xml = xmltodict.parse(
            fs.read(),
            strip_whitespace=False
        )['validElementaryExchanges']['elementaryExchange']

    with open(output_path, 'w') as fs:
        json.dump([reformat(obj) for obj in ei_xml], fs, indent=2)
    return True
