from dataclasses import asdict, dataclass, field
from .constants import CONTEXT_MAPPING

import flowmapper.jsonpath as jp

@dataclass
class Context:
    value: str
    raw_value: str = ""
    raw_object: dict = field(default_factory=lambda: {})

    @classmethod
    def from_dict(cls, d, spec):
        if not spec:
            return Context(None)
        else:
            key = jp.root(spec)
            value = cls.ensure_list(jp.extract(spec, d))
            result = Context(
                value = cls.normalize_contexts(value),
                raw_value = '/'.join(value),
                raw_object = {key: d.get(key)},
            )
            return result

    def to_dict(self):
        return asdict(self)

    def __eq__(self, other):
        if self and other and isinstance(other, Context):
            return self.value == other.value
        elif self and other:
            return self.value == other
        else:
            return False

    def __bool__(self):
        return bool(self.value)

    def __hash__(self):
        return hash(self.value)

    @staticmethod
    def ensure_list(x):
        return x.split('/') if isinstance(x, str) else x

    @staticmethod
    def normalize_contexts(context: list[str]):
        result = '/'.join([
            segment.lower().rstrip('/')
            for segment in context 
            if segment and segment.lower() not in {'(unspecified)', 'unspecified'}
        ])
        
        return CONTEXT_MAPPING.get(result, result)