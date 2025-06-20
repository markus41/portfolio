"""Minimal fallback implementation of the jsonschema.validate API."""

from __future__ import annotations

from typing import Any, Dict


class ValidationError(Exception):
    """Exception raised when validation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def validate(instance: Any, schema: Dict[str, Any]) -> None:
    """Very small subset of JSON Schema validation.

    Only supports ``type`` checks for "object" and "array" and the ``required``
    and ``properties`` keywords used by the team schema. The function raises
    :class:`ValidationError` if the instance does not conform to the schema.
    """

    def _check(value: Any, sch: Dict[str, Any]) -> None:
        t = sch.get("type")
        if t == "object":
            if not isinstance(value, dict):
                raise ValidationError("expected object")
            for req in sch.get("required", []):
                if req not in value:
                    raise ValidationError(f"'{req}' is required")
            for key, subschema in sch.get("properties", {}).items():
                if key in value:
                    _check(value[key], subschema)
        elif t == "array":
            if not isinstance(value, list):
                raise ValidationError("expected array")
            for item in value:
                if "items" in sch:
                    _check(item, sch["items"])

    _check(instance, schema)
