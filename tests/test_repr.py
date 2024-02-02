from flowmapper.flow import Flow
from flowmapper.flowmap import Flowmap
from pprint import pprint

    # def __repr__(self) -> str:
    #     # id_original = f"uuid:{self.uuid_raw_value}" if self.uuid_raw_value else f"id:{self.id}"
    #     # transformed = "*" if self.raw != self.transformed else ""
    #     original = f"{self.name_raw_value} (in {self.unit.raw_value}) <{self.context.raw_value}> [uuid:{self.uuid_raw_value}]"
    #     transformed = f"{self.name.value} (in {self.unit.value}) <{self.context.value}> [uuid:{self.uuid}]"
    #     if self.raw == self.transformed:
    #         return original
    #     else:
    #         return f"Original: {original}\nTransformed: {transformed}"

fields = {
    "uuid": "@id",
    "name": "name.#text",
    "synonyms": ("synonym", ["#text"]),
    "context": "compartment.*.#text",
    "unit": "unitName.#text",
    "cas": "@casNumber",
}

transformation = {
    "update": [
        {
            "source": {"@id": "4f777e05-70f9-4a18-a406-d8232325073f"},
            "target": {"@id": "b6b4201e-0561-5992-912f-e729fbf04e41"},
        }
    ]
}

source = {
    "@id": "4f777e05-70f9-4a18-a406-d8232325073f",
    "@unitId": "487df68b-4994-4027-8fdc-a4dc298257b7",
    "@formula": "C10H13Cl2NO3",
    "@casNumber": "002008-39-1",
    "name": {"@xml:lang": "en", "#text": "2,4-D amines"},
    "unitName": {"@xml:lang": "en", "#text": "kg"},
    "compartment": {
        "@subcompartmentId": "be7e06e9-0bf5-462e-99dc-fe4aee383c48",
        "compartment": {"@xml:lang": "en", "#text": "air"},
        "subcompartment": {
            "@xml:lang": "en",
            "#text": "non-urban air or from high stacks",
        },
    },
    "synonym": [
        {"@xml:lang": "en", "#text": "2-(2,4-dichlorophenoxy)acetic acid"},
        {"@xml:lang": "en", "#text": "2,4-D dimethylamine salt"},
        {"@xml:lang": "en", "#text": "N-methylmethanamine"},
    ],
}

target = {
    "@id": "b6b4201e-0561-5992-912f-e729fbf04e41",
    "@unitId": "487df68b-4994-4027-8fdc-a4dc298257b7",
    "@formula": "C10H13Cl2NO3",
    "@casNumber": "002008-39-1",
    "name": {"@xml:lang": "en", "#text": "2,4-D dimethylamine salt"},
    "unitName": {"@xml:lang": "en", "#text": "kg"},
    "compartment": {
        "@subcompartmentId": "be7e06e9-0bf5-462e-99dc-fe4aee383c48",
        "compartment": {"@xml:lang": "en", "#text": "air"},
        "subcompartment": {
            "@xml:lang": "en",
            "#text": "non-urban air or from high stacks",
        },
    },
}

s1 = Flow(source, fields)
s2 = Flow(source, fields, transformation)

t = Flow(target, fields)

s1
s2
t

flowmap = Flowmap([s1, s2], [t])
pprint(flowmap.mappings)