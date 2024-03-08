from dataclasses import asdict, dataclass, field

import flowmapper.jsonpath as jp

from .utils import normalize_str


@dataclass
class FlowProperty:
    value: str = None
    raw_value: str = None
    raw_object: dict = field(default_factory=lambda: {})

    def __post_init__(self):
        raw_value = self.value
        self.value = self.normalize(self.value)
        if raw_value != self.value:
            self.raw_value = raw_value

    @classmethod
    def from_dict(cls, d, spec):
        if spec:
            key = jp.root(spec)
            value = jp.extract(spec, d)
            result = FlowProperty(
                value=cls.normalize(value),
                raw_value=value,
                raw_object={key: d.get(key)},
            )
        else:
            result = FlowProperty(None)
        return result

    def to_dict(self):
        return asdict(self)

    def __eq__(self, other):
        result = False
        if self and other:
            if isinstance(other, FlowProperty):
                result = self.value == other.value
            else:
                result = self.value == other
        return result

    def __bool__(self):
        return bool(self.value)

    def __repr__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)

    @staticmethod
    def normalize(x):
        if x is None:
            result = None
        elif isinstance(x, str):
            result = normalize_str(x)
        else:
            result = [normalize_str(s) for s in x if s]
        return result
