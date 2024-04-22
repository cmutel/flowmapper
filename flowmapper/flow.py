from typing import List

from .cas import CAS
from .context import Context
from .string_field import StringField
from .string_list import StringList
from .unit import Unit
from .utils import apply_transformations, generate_flow_id


class Flow:
    def __init__(
        self,
        data: dict,
        transformations: List[dict] | None = None,
    ):
        # Hash of sorted dict keys and values
        self.id = generate_flow_id(data)
        self.data = data
        self.transformed = apply_transformations(data, transformations)
        self.conversion_factor = self.transformed.get("conversion_factor")
        self.identifier = StringField(
            original=self.data.get("identifier"),
            transformed=self.transformed.get("identifier"),
            use_lowercase=False,
        )
        self.name = StringField(
            original=self.data.get("name"),
            transformed=self.transformed.get("name"),
        )
        self.unit = Unit(
            original=self.data.get("unit"),
            transformed=self.transformed.get("unit"),
        )
        self.context = Context(
            original=self.data.get("context"),
            transformed=self.transformed.get("context"),
        )
        self.cas = CAS(data.get("CAS number"))
        self.synonyms = StringList(
            original=self.data.get("synonyms", []),
            transformed=self.transformed.get("synonyms", []),
        )

    @property
    def missing(self):
        """This flow has been marked as missing in target list"""
        return self.transformed.get("__missing__")

    @property
    def export(self) -> dict:
        return {
            "name": self.name.original,
            "unit": self.unit.original,
            "identifier": self.identifier.original,
            "context": self.context.original,
            "CAS number": self.cas.export,
        }

    def __repr__(self) -> str:
        return f"{self.identifier} / {self.name} / {self.context} / {self.unit}"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    # Used in sorting
    def __lt__(self, other):
        return self.name.normalized < other.name.normalized
