"""Schema validity for structured output.

Validates the parsed JSON against a schema given in scorer options:

    {"type": "json_schema", "options": {"schema": {...}}}

Implements a documented SUBSET of JSON Schema (kept dependency-free):
type (object/array/string/number/integer/boolean/null), properties, required,
items, enum, additionalProperties (boolean). Anything fancier belongs in a
custom scorer — see docs/extending.md.
"""

from __future__ import annotations

from ..adapters import ParsedOutput
from ..errors import GateConfigError
from ..loading import DatasetItem
from ..metrics import HIGHER
from . import Scorer, item_result, register_scorer

_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "null": type(None),
}


def validate_against_schema(value, schema: dict, path: str = "$") -> list[str]:
    """Return a list of human-readable violations; empty list means valid."""
    errors: list[str] = []
    stype = schema.get("type")
    if stype is not None:
        expected = _TYPES.get(stype)
        if expected is None:
            raise GateConfigError(f"json_schema scorer: unsupported type '{stype}' at {path}")
        # bool is an int subclass in Python; keep JSON semantics strict.
        if isinstance(value, bool) and stype in ("number", "integer"):
            errors.append(f"{path}: expected {stype}, got boolean")
            return errors
        if not isinstance(value, expected):
            errors.append(f"{path}: expected {stype}, got {type(value).__name__}")
            return errors
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum {schema['enum']}")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required property '{key}'")
        properties = schema.get("properties", {})
        for key, sub in properties.items():
            if key in value:
                errors.extend(validate_against_schema(value[key], sub, f"{path}.{key}"))
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            if extras:
                errors.append(f"{path}: unexpected properties {extras}")
    if isinstance(value, list) and "items" in schema:
        for i, element in enumerate(value):
            errors.extend(validate_against_schema(element, schema["items"], f"{path}[{i}]"))
    return errors


class JsonSchemaScorer(Scorer):
    name = "json_schema"
    version = "1"
    metrics = {
        "schema.valid_rate": {"direction": HIGHER, "kind": "rate", "mode": "pass_rate"},
    }

    def __init__(self, options: dict):
        super().__init__(options)
        self.schema = self.options.get("schema")
        if not isinstance(self.schema, dict):
            raise GateConfigError("json_schema scorer requires options.schema (an object)")

    def score_item(self, item: DatasetItem, output: ParsedOutput) -> dict[str, dict]:
        if output.json_obj is None:
            return {
                "schema.valid_rate": item_result(
                    applicable=True, passed=False,
                    detail=output.parse_error or "no JSON object in output",
                )
            }
        violations = validate_against_schema(output.json_obj, self.schema)
        return {
            "schema.valid_rate": item_result(
                applicable=True,
                passed=not violations,
                detail="; ".join(violations) or None,
            )
        }


register_scorer("json_schema", JsonSchemaScorer)
