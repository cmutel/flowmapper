import flowmapper.jsonpath as jp

from .unit import Unit
from .cas import CAS
from .context import Context
from .utils import generate_flow_id, transform_flow, find_transformation
from .flowproperty import FlowProperty


class Flow:
    def __init__(
        self,
        original,
        fields=None,
        transformations=None,
    ):
        transformation = find_transformation(original, transformations)
        transformed = (
            transform_flow(original, transformation) if transformation else original
        )
        fields = fields if fields else {k:k for k in original}
        uuid_spec = fields.get("uuid")
        name_spec = fields.get("name")
        synonyms_spec = fields.get("synonyms")
        context_spec = fields.get("context")
        unit_spec = fields.get("unit")
        cas_spec = fields.get("cas")

        self.id = generate_flow_id(original)
        self.conversion_factor = transformation.get("conversion_factor") if transformation else None
        self.uuid = jp.extract(uuid_spec, transformed)
        self.uuid_raw_value = jp.extract(uuid_spec, original)
        self.uuid_raw_object = jp.extract(uuid_spec, original, "object")
        self.name = FlowProperty.from_dict(transformed, name_spec)
        self.name_raw_value = jp.extract(name_spec, original)
        self.name_raw_object = jp.extract(name_spec, original, "object")
        self.synonyms = FlowProperty.from_dict(transformed, synonyms_spec)
        self.synonyms_raw_value = jp.extract(synonyms_spec, original)
        self.synonyms_raw_object = jp.extract(synonyms_spec, original, "object")
        self.context = Context.from_dict(transformed, context_spec)
        self.context_raw_value = jp.extract(context_spec, original)
        self.context_raw_object = jp.extract(context_spec, original, "object")
        self.unit = Unit.from_dict(transformed, fields["unit"])
        self.unit_raw_value = jp.extract(unit_spec, original)
        self.unit_raw_object = jp.extract(unit_spec, original, "object")
        self.cas = CAS(jp.extract(cas_spec, transformed))
        self.cas_raw_value = jp.extract(cas_spec, original)
        self.cas_raw_object = jp.extract(cas_spec, original, "object")
        self.raw = original
        self.transformed = transformed

    def __repr__(self) -> str:
        transformed = "*" if self.raw != self.transformed else ""
        return f"{self.name_raw_value}{transformed} (in {self.unit.raw_value}) <{self.context.raw_value}> [uuid:{self.uuid_raw_value}]"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.name.raw_value < other.name.raw_value
