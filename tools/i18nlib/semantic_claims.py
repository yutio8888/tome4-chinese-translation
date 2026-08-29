"""Exact, deterministic validation for semantic-claim regression registries."""

from __future__ import annotations

import json
import math
import re
from itertools import product
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

from .config import repository_root
from .errors import ValidationError
from .lint import extract_format_tokens


REGISTRY_SCHEMA_VERSION = 1
DEFAULT_REGISTRY = repository_root() / "evidence/quality/semantic-claim-regressions-v1.json"

_STATUS = {"confirmed", "pending"}
_QUANTITY_KINDS = {
    "damage", "heal", "shield", "duration", "count", "percent", "radius",
    "other_numeric", "unknown",
}
_EXPLICITNESS = {"explicit_scope", "ambiguous_scope"}
_EXPLICITNESS_ORDER = {"ambiguous_scope": 0, "explicit_scope": 1}
_SCOPES = {"on_apply", "per_tick", "total_over_effect", "on_expire", "unknown"}
_PHASES = {"on_apply", "periodic_tick", "on_expire", "unknown"}
_SURFACE_SHAPES = {
    "bare_noun", "possessive_phrase", "pronoun", "pre_punctuated_clause",
    "tagged_fragment", "unknown",
}
_APPLICABILITY = {"effect_absent", "unconditional", "unknown"}

_TOP_KEYS = {
    "schema_version", "registry_id", "numeric_claims", "reviewer_briefings",
    "runtime_compositions",
}
_CLAIM_KEYS = {
    "claim_id", "status", "string_key", "source_text", "target_text",
    "placeholder_index", "placeholder_token", "args_order", "quantity_kind",
    "source_explicitness", "target_explicitness", "scope",
    "explicitation_justified", "anchors",
    "decomposition", "target_assertions",
}
_ANCHOR_KEYS = {
    "component", "revision", "source_pinned", "path", "symbol", "line_hint",
    "placeholder_expression", "binding_reason", "required",
}
_DECOMPOSITION_KEYS = {
    "kind", "duration_turns", "tick_count", "components",
    "total_fraction_of_input", "applicability",
}
_COMPONENT_KEYS = {"phase", "fraction_of_input", "count"}
_FRACTION_KEYS = {"numerator", "denominator"}
_ASSERTION_KEYS = {"required", "forbidden"}
_BRIEFING_KEYS = {
    "briefing_id", "string_key", "source_text", "candidate_target",
    "placeholder_index", "placeholder_token", "args_order", "anchors", "read_budget",
}
_READ_BUDGET_KEYS = {"max_lines_per_anchor", "max_dependency_hops"}
_COMPOSITION_KEYS = {
    "case_id", "status", "string_key", "source_template", "target_template",
    "args_order", "placeholders", "renderings",
}
_PLACEHOLDER_KEYS = {"index", "runtime_source", "variants"}
_VARIANT_KEYS = {"variant_id", "surface_shape", "sample_value", "anchors"}
_RENDERING_KEYS = {"variant_ids", "rendered_sentence", "assertions"}


def _fail(where: str, message: str) -> None:
    raise ValidationError(f"{where}: {message}")


def _exact(value: Any, keys: set[str], where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(where, "expected object")
    actual = set(value)
    if actual != keys:
        missing = sorted(keys - actual)
        extra = sorted(actual - keys)
        _fail(where, f"exact keys required; missing={missing}, extra={extra}")
    return value


def _string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(where, "expected non-empty string")
    return value


def _integer(value: Any, where: str, *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        _fail(where, f"expected integer >= {minimum}")
    return value


def _boolean(value: Any, where: str) -> bool:
    if not isinstance(value, bool):
        _fail(where, "expected boolean")
    return value


def _enum(value: Any, allowed: set[str], where: str) -> str:
    result = _string(value, where)
    if result not in allowed:
        _fail(where, f"unknown enum {result!r}")
    return result


def _safe_path(value: Any, where: str) -> str:
    result = _string(value, where)
    if (
        "\x00" in result
        or "\\" in result
        or result.startswith("/")
        or re.match(r"^[A-Za-z]:", result)
        or any(part in {"", ".", ".."} for part in result.split("/"))
    ):
        _fail(where, "path must be a relative POSIX path")
    path = PurePosixPath(result)
    if any(part in {"", ".", ".."} for part in path.parts):
        _fail(where, "path contains an unsafe segment")
    return result


def _string_list(value: Any, where: str) -> list[str]:
    if not isinstance(value, list):
        _fail(where, "expected array")
    result = [_string(item, f"{where}[{index}]") for index, item in enumerate(value)]
    if len(result) != len(set(result)):
        _fail(where, "duplicate string assertion")
    return result


def _assertions(value: Any, where: str, rendered: str) -> None:
    obj = _exact(value, _ASSERTION_KEYS, where)
    required = _string_list(obj["required"], f"{where}.required")
    forbidden = _string_list(obj["forbidden"], f"{where}.forbidden")
    for fragment in required:
        if fragment not in rendered:
            _fail(where, f"required fragment absent: {fragment!r}")
    for fragment in forbidden:
        if fragment in rendered:
            _fail(where, f"forbidden fragment present: {fragment!r}")


def _anchor(value: Any, where: str) -> dict[str, Any]:
    obj = _exact(value, _ANCHOR_KEYS, where)
    _string(obj["component"], f"{where}.component")
    revision = _string(obj["revision"], f"{where}.revision")
    source_pinned = _boolean(obj["source_pinned"], f"{where}.source_pinned")
    if source_pinned and not (
        re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", revision)
        or re.fullmatch(r"manifest:[A-Za-z0-9._:-]+", revision)
    ):
        _fail(f"{where}.revision", "pinned anchor requires a commit hash or manifest identity")
    _safe_path(obj["path"], f"{where}.path")
    _string(obj["symbol"], f"{where}.symbol")
    _integer(obj["line_hint"], f"{where}.line_hint", minimum=1)
    _string(obj["placeholder_expression"], f"{where}.placeholder_expression")
    _string(obj["binding_reason"], f"{where}.binding_reason")
    _boolean(obj["required"], f"{where}.required")
    return obj


def _anchors(value: Any, where: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        _fail(where, "expected a non-empty anchor array")
    anchors = [_anchor(item, f"{where}[{index}]") for index, item in enumerate(value)]
    if not any(anchor["required"] for anchor in anchors):
        _fail(where, "at least one anchor must be required")
    return anchors


def _fraction(value: Any, where: str) -> Fraction:
    obj = _exact(value, _FRACTION_KEYS, where)
    numerator = _integer(obj["numerator"], f"{where}.numerator")
    denominator = _integer(obj["denominator"], f"{where}.denominator", minimum=1)
    if math.gcd(numerator, denominator) != 1:
        _fail(where, "fraction must be reduced")
    return Fraction(numerator, denominator)


def _unknown_or_integer(value: Any, where: str, *, minimum: int) -> int | str:
    if value == "unknown":
        return value
    return _integer(value, where, minimum=minimum)


def _decomposition(value: Any, where: str, scope: str) -> None:
    obj = _exact(value, _DECOMPOSITION_KEYS, where)
    kind = _enum(obj["kind"], {"fixed_fraction", "unknown"}, f"{where}.kind")
    applicability = _enum(obj["applicability"], _APPLICABILITY, f"{where}.applicability")
    duration = _unknown_or_integer(
        obj["duration_turns"], f"{where}.duration_turns", minimum=0
    )
    tick_count = _unknown_or_integer(
        obj["tick_count"], f"{where}.tick_count", minimum=0
    )
    if not isinstance(obj["components"], list):
        _fail(f"{where}.components", "expected array")
    if kind == "unknown":
        if obj["components"] or obj["total_fraction_of_input"] != "unknown":
            _fail(where, "unknown decomposition requires empty components and unknown total")
        if duration != "unknown" or tick_count != "unknown":
            _fail(where, "unknown decomposition requires unknown duration and tick count")
        if applicability != "unknown":
            _fail(where, "unknown decomposition requires unknown applicability")
        if scope != "unknown":
            _fail(where, "unknown decomposition requires unknown scope")
        return
    if duration == "unknown" or tick_count == "unknown":
        _fail(where, "fixed_fraction requires known duration_turns and tick_count")
    if not obj["components"]:
        _fail(f"{where}.components", "fixed_fraction requires components")
    total = Fraction(0, 1)
    periodic_count = 0
    phases: set[str] = set()
    for index, raw in enumerate(obj["components"]):
        item_where = f"{where}.components[{index}]"
        component = _exact(raw, _COMPONENT_KEYS, item_where)
        phase = _enum(component["phase"], _PHASES, f"{item_where}.phase")
        if phase == "unknown":
            _fail(item_where, "fixed_fraction component phase cannot be unknown")
        count = _integer(component["count"], f"{item_where}.count", minimum=1)
        fraction = _fraction(component["fraction_of_input"], f"{item_where}.fraction_of_input")
        total += fraction * count
        phases.add(phase)
        if phase == "periodic_tick":
            periodic_count += count
    expected_total = _fraction(obj["total_fraction_of_input"], f"{where}.total_fraction_of_input")
    if total != expected_total:
        _fail(where, f"component fractions sum to {total}, expected {expected_total}")
    if not periodic_count and tick_count != 0:
        _fail(where, "decomposition without periodic components requires tick_count 0")
    if periodic_count and tick_count <= 0:
        _fail(where, "periodic decomposition requires a positive tick_count")
    if periodic_count != tick_count:
        _fail(where, f"periodic component count {periodic_count} != tick_count {tick_count}")
    if phases == {"on_apply"}:
        if duration != 0:
            _fail(where, "pure on_apply decomposition requires duration_turns 0")
    elif duration <= 0:
        _fail(where, "on_expire or periodic decomposition requires positive duration_turns")
    if scope == "total_over_effect" and expected_total != Fraction(1, 1):
        _fail(where, "total_over_effect input must decompose to exactly 1")
    if scope == "on_apply" and phases != {"on_apply"}:
        _fail(where, "on_apply scope cannot contain other phases")
    if scope == "per_tick" and phases != {"periodic_tick"}:
        _fail(where, "per_tick scope cannot contain other phases")
    if scope == "on_expire" and phases != {"on_expire"}:
        _fail(where, "on_expire scope cannot contain other phases")
    if scope == "unknown":
        _fail(where, "fixed_fraction decomposition cannot use unknown scope")


def _format_tokens(text: str) -> list[str]:
    return [token.raw for token in extract_format_tokens(text)]


def _validate_placeholder(source: str, index: Any, token: Any, where: str) -> int:
    number = _integer(index, f"{where}.placeholder_index", minimum=1)
    actual = _format_tokens(source)
    if number > len(actual):
        _fail(where, f"placeholder index {number} exceeds {len(actual)} source placeholders")
    expected = _string(token, f"{where}.placeholder_token")
    if actual[number - 1] != expected:
        _fail(where, f"placeholder token mismatch: expected {actual[number - 1]!r}")
    return number


def _validate_token_permutation(
    source: str, target: str, args_order: Any, where: str
) -> list[int]:
    source_tokens = _format_tokens(source)
    target_tokens = _format_tokens(target)
    expected_indices = list(range(1, len(source_tokens) + 1))
    if args_order is None:
        order = expected_indices
    else:
        if not isinstance(args_order, list) or any(
            not isinstance(item, int) or isinstance(item, bool) for item in args_order
        ):
            _fail(f"{where}.args_order", "expected null or integer array")
        if sorted(args_order) != expected_indices:
            _fail(f"{where}.args_order", f"must be a permutation of {expected_indices}")
        order = args_order
    if [source_tokens[index - 1] for index in order] != target_tokens:
        _fail(where, "target format tokens do not match args_order")
    return order


def _validate_lua51_scanformat(tokens: list[Any], where: str) -> None:
    for index, token in enumerate(tokens):
        match = re.fullmatch(r"%([-+ #0]*)(\d*)(?:\.(\d*))?([cdeEfgGiouXxqs])", token.raw)
        if match is None:
            _fail(f"{where}[{index}]", f"invalid Lua 5.1 format token {token.raw!r}")
        flags, width, precision, _conversion = match.groups()
        if len(flags) > 5:
            _fail(f"{where}[{index}]", "Lua 5.1 permits at most five flag characters")
        if len(width) > 2:
            _fail(f"{where}[{index}]", "Lua 5.1 permits at most two width digits")
        if precision is not None and len(precision) > 2:
            _fail(f"{where}[{index}]", "Lua 5.1 permits at most two precision digits")


def _complete_format_tokens(template: str, where: str) -> list[Any]:
    """Return tokens only when every percent starts %% or one complete token."""
    tokens = list(extract_format_tokens(template))
    tokens_by_offset = {token.offset: token for token in tokens}
    cursor = 0
    while cursor < len(template):
        percent = template.find("%", cursor)
        if percent < 0:
            break
        if percent + 1 < len(template) and template[percent + 1] == "%":
            cursor = percent + 2
            continue
        token = tokens_by_offset.get(percent)
        if token is None:
            _fail(where, f"invalid percent sequence at offset {percent}")
        cursor = percent + len(token.raw)
    _validate_lua51_scanformat(tokens, f"{where}.tokens")
    return tokens


def _validate_runtime_composition_conversions(tokens: list[Any], where: str) -> None:
    for index, token in enumerate(tokens):
        if token.conversion not in {"s", "q"}:
            _fail(
                f"{where}[{index}]",
                "runtime composition v1 only supports %s and %q conversions",
            )
        if token.conversion == "s" and token.raw != "%s":
            _fail(
                f"{where}[{index}]",
                "runtime composition v1 only supports raw bare %s",
            )


def _validate_luajit_q_sample(value: str, where: str) -> None:
    for index, character in enumerate(value):
        codepoint = ord(character)
        if (codepoint < 0x20 and character != "\n") or codepoint == 0x7F:
            _fail(
                where,
                "LuaJIT-safe %q sample must not contain C0 controls except LF or DEL "
                f"(found U+{codepoint:04X} at index {index})",
            )


def _numeric_claim(value: Any, where: str) -> str:
    obj = _exact(value, _CLAIM_KEYS, where)
    claim_id = _string(obj["claim_id"], f"{where}.claim_id")
    status = _enum(obj["status"], _STATUS, f"{where}.status")
    _string(obj["string_key"], f"{where}.string_key")
    source = _string(obj["source_text"], f"{where}.source_text")
    target = _string(obj["target_text"], f"{where}.target_text")
    _validate_placeholder(source, obj["placeholder_index"], obj["placeholder_token"], where)
    _validate_token_permutation(source, target, obj["args_order"], where)
    _enum(obj["quantity_kind"], _QUANTITY_KINDS, f"{where}.quantity_kind")
    source_explicitness = _enum(
        obj["source_explicitness"], _EXPLICITNESS, f"{where}.source_explicitness"
    )
    target_explicitness = _enum(
        obj["target_explicitness"], _EXPLICITNESS, f"{where}.target_explicitness"
    )
    scope = _enum(obj["scope"], _SCOPES, f"{where}.scope")
    justified = _boolean(obj["explicitation_justified"], f"{where}.explicitation_justified")
    anchors = _anchors(obj["anchors"], f"{where}.anchors")
    if status == "confirmed" and any(
        anchor["required"] and not anchor["source_pinned"] for anchor in anchors
    ):
        _fail(where, "confirmed claim has an unpinned required anchor")
    increased_explicitness = (
        _EXPLICITNESS_ORDER[target_explicitness] > _EXPLICITNESS_ORDER[source_explicitness]
    )
    has_unpinned_required = any(
        anchor["required"] and not anchor["source_pinned"] for anchor in anchors
    )
    if increased_explicitness:
        if not justified:
            _fail(where, "increased target explicitness requires justification")
        if status == "pending" or has_unpinned_required:
            _fail(where, "pending or unpinned claim cannot increase target explicitness")
    elif justified:
        _fail(where, "explicitation_justified requires increased target explicitness")
    _decomposition(obj["decomposition"], f"{where}.decomposition", scope)
    _assertions(obj["target_assertions"], f"{where}.target_assertions", target)
    return claim_id


def _reviewer_briefing(value: Any, where: str) -> str:
    obj = _exact(value, _BRIEFING_KEYS, where)
    briefing_id = _string(obj["briefing_id"], f"{where}.briefing_id")
    _string(obj["string_key"], f"{where}.string_key")
    source = _string(obj["source_text"], f"{where}.source_text")
    target = _string(obj["candidate_target"], f"{where}.candidate_target")
    _validate_placeholder(source, obj["placeholder_index"], obj["placeholder_token"], where)
    _validate_token_permutation(source, target, obj["args_order"], where)
    _anchors(obj["anchors"], f"{where}.anchors")
    budget = _exact(obj["read_budget"], _READ_BUDGET_KEYS, f"{where}.read_budget")
    _integer(budget["max_lines_per_anchor"], f"{where}.read_budget.max_lines_per_anchor", minimum=1)
    _integer(budget["max_dependency_hops"], f"{where}.read_budget.max_dependency_hops", minimum=0)
    return briefing_id


def _render_printf(template: str, values: list[Any], where: str) -> str:
    tokens = extract_format_tokens(template)
    render_parts: list[str] = []
    render_values = list(values)
    cursor = 0
    for index, token in enumerate(tokens):
        render_parts.append(template[cursor:token.offset])
        value = render_values[index]
        if token.conversion not in {"s", "q"}:
            _fail(where, "runtime composition v1 only supports %s and %q conversions")
        if not isinstance(value, str):
            _fail(
                where,
                f"Lua %{token.conversion} rendering requires a string sample value",
            )
        if token.conversion == "q":
            _validate_luajit_q_sample(value, where)
            quoted = (
                value.replace("\\", "\\\\")
                .replace('"', '\\"')
                .replace("\n", "\\\n")
            )
            render_values[index] = f'"{quoted}"'
            # Lua 5.1 ignores syntactically valid flags, width, and precision for %q.
            render_parts.append("%s")
        else:
            render_parts.append(token.raw)
        cursor = token.offset + len(token.raw)
    render_parts.append(template[cursor:])
    render_template = "".join(render_parts)
    try:
        return render_template % tuple(render_values)
    except (TypeError, ValueError) as error:
        _fail(where, f"cannot render target template: {error}")
    raise AssertionError("unreachable")


def _runtime_composition(value: Any, where: str) -> str:
    obj = _exact(value, _COMPOSITION_KEYS, where)
    case_id = _string(obj["case_id"], f"{where}.case_id")
    status = _enum(obj["status"], _STATUS, f"{where}.status")
    _string(obj["string_key"], f"{where}.string_key")
    source_template = _string(obj["source_template"], f"{where}.source_template")
    target_template = _string(obj["target_template"], f"{where}.target_template")
    source_token_objects = _complete_format_tokens(
        source_template, f"{where}.source_template"
    )
    target_token_objects = _complete_format_tokens(
        target_template, f"{where}.target_template"
    )
    source_tokens = [token.raw for token in source_token_objects]
    target_tokens = [token.raw for token in target_token_objects]
    _validate_runtime_composition_conversions(
        source_token_objects, f"{where}.source_template.tokens"
    )
    _validate_runtime_composition_conversions(
        target_token_objects, f"{where}.target_template.tokens"
    )
    if not isinstance(obj["placeholders"], list) or not obj["placeholders"]:
        _fail(f"{where}.placeholders", "expected non-empty array")
    placeholders: list[dict[str, Any]] = []
    required_anchors: list[dict[str, Any]] = []
    for index, raw in enumerate(obj["placeholders"]):
        item_where = f"{where}.placeholders[{index}]"
        item = _exact(raw, _PLACEHOLDER_KEYS, item_where)
        number = _integer(item["index"], f"{item_where}.index", minimum=1)
        _string(item["runtime_source"], f"{item_where}.runtime_source")
        if not isinstance(item["variants"], list) or not item["variants"]:
            _fail(f"{item_where}.variants", "expected non-empty array")
        variants: list[dict[str, Any]] = []
        variant_ids: set[str] = set()
        for variant_index, raw_variant in enumerate(item["variants"]):
            variant_where = f"{item_where}.variants[{variant_index}]"
            variant = _exact(raw_variant, _VARIANT_KEYS, variant_where)
            variant_id = _string(variant["variant_id"], f"{variant_where}.variant_id")
            if variant_id in variant_ids:
                _fail(variant_where, f"duplicate variant ID {variant_id!r}")
            variant_ids.add(variant_id)
            _enum(
                variant["surface_shape"], _SURFACE_SHAPES,
                f"{variant_where}.surface_shape",
            )
            sample = _string(
                variant["sample_value"], f"{variant_where}.sample_value"
            )
            anchors = _anchors(variant["anchors"], f"{variant_where}.anchors")
            variants.append({**variant, "variant_id": variant_id})
            required_anchors.extend(anchor for anchor in anchors if anchor["required"])
        placeholders.append({**item, "index": number, "variants": variants})
    expected_indices = list(range(1, len(source_tokens) + 1))
    if sorted(item["index"] for item in placeholders) != expected_indices:
        _fail(where, f"placeholder indices must be exactly {expected_indices}")
    for placeholder_position, placeholder in enumerate(placeholders):
        if source_token_objects[placeholder["index"] - 1].conversion == "q":
            for variant_index, variant in enumerate(placeholder["variants"]):
                _validate_luajit_q_sample(
                    variant["sample_value"],
                    f"{where}.placeholders[{placeholder_position}].variants"
                    f"[{variant_index}].sample_value",
                )
    if len(target_tokens) != len(source_tokens):
        _fail(where, "source and target templates must have the same placeholder count")
    if status == "confirmed" and any(not anchor["source_pinned"] for anchor in required_anchors):
        _fail(where, "confirmed composition has an unpinned required anchor")
    order = _validate_token_permutation(
        source_template, target_template, obj["args_order"], where
    )

    by_index = {item["index"]: item for item in placeholders}
    expected_selections = {
        tuple(variant["variant_id"] for variant in combination)
        for combination in product(*(by_index[index]["variants"] for index in expected_indices))
    }
    if not isinstance(obj["renderings"], list) or not obj["renderings"]:
        _fail(f"{where}.renderings", "expected non-empty array")
    seen_selections: set[tuple[str, ...]] = set()
    variant_lookup = {
        index: {variant["variant_id"]: variant for variant in by_index[index]["variants"]}
        for index in expected_indices
    }
    for rendering_index, raw_rendering in enumerate(obj["renderings"]):
        rendering_where = f"{where}.renderings[{rendering_index}]"
        rendering = _exact(raw_rendering, _RENDERING_KEYS, rendering_where)
        variant_ids = rendering["variant_ids"]
        if not isinstance(variant_ids, list) or len(variant_ids) != len(expected_indices):
            _fail(f"{rendering_where}.variant_ids", "must select one variant per placeholder")
        selection = tuple(
            _string(variant_id, f"{rendering_where}.variant_ids[{index}]")
            for index, variant_id in enumerate(variant_ids)
        )
        if selection in seen_selections:
            _fail(rendering_where, f"duplicate variant selection {selection!r}")
        seen_selections.add(selection)
        try:
            selected_values = {
                index: variant_lookup[index][selection[index - 1]]["sample_value"]
                for index in expected_indices
            }
        except KeyError as error:
            _fail(rendering_where, f"unknown variant ID {error.args[0]!r}")
        rendered = _render_printf(
            target_template, [selected_values[index] for index in order], rendering_where
        )
        expected_rendered = _string(
            rendering["rendered_sentence"], f"{rendering_where}.rendered_sentence"
        )
        if rendered != expected_rendered:
            _fail(rendering_where, f"rendered sentence mismatch: got {rendered!r}")
        _assertions(rendering["assertions"], f"{rendering_where}.assertions", rendered)
    if seen_selections != expected_selections:
        missing = sorted(expected_selections - seen_selections)
        extra = sorted(seen_selections - expected_selections)
        _fail(where, f"renderings must cover every variant combination; missing={missing}, extra={extra}")
    return case_id


def validate_registry(value: Any) -> dict[str, int]:
    """Validate an already-decoded registry and return deterministic counts."""
    obj = _exact(value, _TOP_KEYS, "registry")
    schema_version = _integer(obj["schema_version"], "registry.schema_version", minimum=1)
    if schema_version != REGISTRY_SCHEMA_VERSION:
        _fail("registry.schema_version", f"expected {REGISTRY_SCHEMA_VERSION}")
    _string(obj["registry_id"], "registry.registry_id")
    collections = (
        ("numeric_claims", _numeric_claim),
        ("reviewer_briefings", _reviewer_briefing),
        ("runtime_compositions", _runtime_composition),
    )
    seen: set[str] = set()
    counts: dict[str, int] = {}
    for field, validator in collections:
        values = obj[field]
        if not isinstance(values, list) or not values:
            _fail(f"registry.{field}", "expected non-empty array")
        counts[field] = len(values)
        for index, item in enumerate(values):
            identifier = validator(item, f"registry.{field}[{index}]")
            if identifier in seen:
                _fail(f"registry.{field}[{index}]", f"duplicate ID {identifier!r}")
            seen.add(identifier)
    return counts


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"registry JSON: duplicate object key {key!r}")
        result[key] = value
    return result


def check_registry(path: Path, *, strict: bool = False) -> dict[str, Any]:
    """Load and validate one registry. Validation is fail-closed in every mode."""
    del strict  # Reserved for CLI compatibility; exact validation is never relaxed.
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValidationError(
            f"invalid semantic claim registry UTF-8: {path}: {error}"
        ) from error
    except OSError as error:
        raise ValidationError(f"cannot read semantic claim registry: {path}: {error}") from error
    try:
        value = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
    except ValidationError:
        raise
    except json.JSONDecodeError as error:
        raise ValidationError(f"invalid semantic claim registry JSON: {path}: {error}") from error
    counts = validate_registry(value)
    pending = sum(
        item["status"] == "pending"
        for field in ("numeric_claims", "runtime_compositions")
        for item in value[field]
    )
    return {
        "registry": str(path),
        "schema_version": REGISTRY_SCHEMA_VERSION,
        **counts,
        "pending": pending,
    }
