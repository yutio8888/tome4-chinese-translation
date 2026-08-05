"""Deterministic, type-sensitive signatures for JSON runtime semantics."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from .errors import ValidationError


def json_value_signature(value: Any, *, label: str = "JSON value") -> str:
    """Return a canonical JSON signature without Python's bool/int equality."""

    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError, OverflowError, RecursionError) as error:
        raise ValidationError(f"{label} has non-canonical JSON semantics") from error


def runtime_semantic_signature(
    entry: Mapping[str, Any], *, label: str = "translation"
) -> str:
    """Sign the fields that determine a translation's runtime value."""

    return json_value_signature(
        {
            "target": entry.get("target"),
            "args_order": entry.get("args_order"),
            "special": entry.get("special"),
        },
        label=f"{label} runtime semantics",
    )
