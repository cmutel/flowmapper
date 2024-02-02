from typing import Literal
from glom import Coalesce, glom

def root(spec):
    result = None
    if isinstance(spec, str):
        result = spec.split('.')[0]
    else:
        try:
            result = next(iter(spec))
        except TypeError:
            pass
    return result

def extract(spec, data, type: Literal['value', 'object'] = 'value'):
    if spec and type == 'value':
        return glom(data, Coalesce(spec, default = ''))
    if spec and type == 'object' and data.get(root(spec)):
        key = root(spec)
        return {key: data[key]}
    else:
        return None
