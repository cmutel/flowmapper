config = {
    "uuid": ["", "@id"],
    "name": ["name", "name.#text"],
    "synonyms": ["", ("synonym", ["#text"])],
    "context": ["categories", "compartment.*.#text"],
    "unit": ["unit", "unitName.#text"],
    "cas": ["CAS", "@casNumber"],
}
