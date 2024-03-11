import math
from typing import TypeVar, Generic, Any
import importlib.resources as resource

from pint import UnitRegistry, errors

from .constants import STANDARD_UNITS_NORMALIZATION, PINT_MAPPING
from .utils import normalize_str

ureg = UnitRegistry()

with resource.as_file(
    resource.files("flowmapper") / "data" / "units.txt"
) as filepath:
    ureg.load_definitions(filepath)

U = TypeVar('U')


class Unit(Generic[U]):
    def __init__(self, value: str, standard_normalizations: bool = True):
        self.original = value
        if self.is_uri(value):
            # Private attribute, could change in future
            self._glossary_entry = self.resolve_uri(value)
            self.normalized = normalize_str(self._glossary_entry['label'])
        else:
            self.normalized = normalize_str(value)

        if standard_normalizations:
            self.normalized = STANDARD_UNITS_NORMALIZATION.get(self.normalized.lower(), self.normalized)

        # Private attribute, could change in future
        self._pint_compatible = PINT_MAPPING.get(self.normalized, self.normalized)

    def is_uri(self, value: str) -> bool:
        # Placeholder for when we support glossary entries
        return False

    def resolve_uri(self, uri: str) -> None:
        # Placeholder
        pass

    def __eq__(self, other: Any):
        if isinstance(other, Unit):
            return self.normalized == other.normalized or self.conversion_factor(other) == 1
        elif isinstance(other, str):
            return self.normalized == other
        else:
            return False

    def compatible(self, other: Any):
        if not isinstance(other, Unit):
            return False
        else:
            return math.isfinite(self.conversion_factor(other))

    def conversion_factor(self, to: U) -> float:
        if self.normalized == to.normalized:
            result = 1.0
        else:
            try:
                result = ureg(self._pint_compatible).to(ureg(to._pint_compatible)).magnitude
            except errors.DimensionalityError:
                result = float("nan")
        return result
