from typing import Any, Generic, TypeVar

from .utils import normalize_str

SF = TypeVar("SF")


class StringField(Generic[SF]):
    def __init__(
        self,
        original: str | None,
        transformed: str | None = None,
        use_lowercase: bool = True,
    ):
        self.original = original
        self.normalized = normalize_str(transformed or original)
        if use_lowercase:
            self.normalized = self.normalized.lower()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, StringField):
            return self.normalized == other.normalized
        elif isinstance(other, str):
            return self.normalized == other
        else:
            return False

    def __repr__(self) -> str:
        return self.original or "(missing original value)"
