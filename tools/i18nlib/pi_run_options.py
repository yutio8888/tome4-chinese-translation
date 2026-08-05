"""Shared validation for Pi runner options with no runner dependencies."""

from __future__ import annotations

from typing import Any

from .errors import ValidationError


_UNSET = object()


def validate_pi_run_options(
    *,
    provider: Any,
    model: Any,
    thinking: Any,
    timeout: Any,
    strict: Any,
    use_cache: Any = _UNSET,
    force: Any = _UNSET,
    evaluator_id: Any = _UNSET,
) -> None:
    """Reject malformed core options before a runner performs any I/O."""
    for label, value in (
        ("provider", provider),
        ("model", model),
        ("thinking", thinking),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"Pi {label} must be a non-empty string")
    if type(timeout) is not int or timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    if type(strict) is not bool:
        raise ValidationError("--strict must be a boolean")
    if use_cache is not _UNSET and type(use_cache) is not bool:
        raise ValidationError("--cache must be a boolean")
    if force is not _UNSET and type(force) is not bool:
        raise ValidationError("--force must be a boolean")
    if evaluator_id is not _UNSET and (
        not isinstance(evaluator_id, str) or not evaluator_id.strip()
    ):
        raise ValidationError("Pi evaluator must be a non-empty string")
