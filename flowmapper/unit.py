from __future__ import annotations

import importlib.resources as resource
from dataclasses import asdict, dataclass, field

from pint import UnitRegistry, errors

import flowmapper.jsonpath as jp

from .constants import UNITS_NORMALIZATION
from .utils import normalize_str

# Default pint units are at
# https://github.com/hgrecco/pint/blob/master/pint/default_en.txt
ureg = UnitRegistry()

with resource.as_file(
    resource.files("flowmapper").joinpath("data/units.txt")
) as filepath:
    ureg.load_definitions(filepath)


@dataclass
class Unit:
    value: str
    raw_value: str = ""
    raw_object: dict = field(default_factory=lambda: {})

    def __post_init__(self):
        if not self.raw_value:
            self.raw_value = self.value
        self.value = self.normalize(self.raw_value)

    @classmethod
    def from_dict(cls, d, spec):
        key = jp.root(spec)
        value = jp.extract(spec, d)
        result = Unit(
            value=None,
            raw_value=value,
            raw_object={key: d.get(key)},
        )
        return result

    def to_dict(self):
        return asdict(self)

    def __eq__(self, other):
        return self.value == other.value

    def conversion_factor(self, to: Unit):
        if self.value == to.value:
            result = 1.0
        else:
            try:
                result = ureg(self.value).to(ureg(to.value)).magnitude
            except errors.DimensionalityError:
                result = float("nan")
        return result

    @staticmethod
    def normalize(x):
        s = normalize_str(x)
        return UNITS_NORMALIZATION.get(s, s)
