from collections.abc import Iterable
from typing import Any

MISSING_VALUES = {
    "",
    "(unknown)",
    "(unspecified)",
    "null",
    "unknown",
    "unspecified",
}


class Context(Iterable):
    def __init__(self, original: Any, transformed: Any = None):
        self.original = original
        self.transformed = transformed or original
        self.normalized = self.normalize(self.transformed)

    def normalize(self, value: Any) -> tuple[str, ...]:
        if isinstance(value, (tuple, list)):
            intermediate = list(value)
        elif isinstance(value, str) and "/" in value:
            intermediate = list(value.split("/"))
        elif isinstance(value, str):
            intermediate = [value]
        else:
            raise ValueError(f"Can't understand input context {value}")

        intermediate = [elem.lower().strip() for elem in intermediate]

        if intermediate[-1] in MISSING_VALUES:
            intermediate = intermediate[:-1]

        return tuple(intermediate)

    def export_as_string(self):
        if isinstance(self.original, str):
            return self.original
        elif isinstance(self.original, (list, tuple)):
            return "✂️".join(self.original)
        else:
            return str(self.original)

    def __iter__(self):
        return iter(self.normalized)

    def __eq__(self, other):
        if self and other and isinstance(other, Context):
            return self.normalized == other.normalized
        else:
            try:
                normalized_other = self.normalize(other)
                return (self.normalized == normalized_other) or (self.original == normalized_other)
            except ValueError:
                return False

    def __repr__(self):
        return f"Context: '{self.original}' -> '{self.normalized}'"

    def __bool__(self):
        return bool(self.normalized)

    def __hash__(self):
        return hash(self.normalized)

    def __contains__(self, other):
        """This context is more generic than the `other` context.

        ```python
        Context("a/b/c") in Context("a/b")
        >>> True
        ```

        """
        if not isinstance(other, Context):
            return False
        return self.normalized == other.normalized[: len(self.normalized)]
