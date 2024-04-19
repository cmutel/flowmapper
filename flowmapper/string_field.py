from typing import TypeVar, Generic, Any
from .utils import normalize_str

SF = TypeVar('SF')


class StringField(Generic[SF]):
    def __init__(self, value: str | None):
        self.original = value
        self.normalized = normalize_str(value)
        self.lowercase = self.normalized.lower()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, StringField):
            return self.normalized == other.normalized
        elif isinstance(other, str):
            return self.normalized == other
        else:
            return False

    def __repr__(self) -> str:
        return self.original or "(missing original value)"
