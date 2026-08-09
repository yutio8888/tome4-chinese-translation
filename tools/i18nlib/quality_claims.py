"""Shared claim semantics: evidence spans, signatures, compatibility, alignment.

This module is the claim core extracted for the offline closure round.  It
implements the exact legacy semantics of v2, v3 and Facts-study matching under
distinct profiles so historical contracts and artifacts stay byte-identical,
plus the new ``canonical-v1`` profile for curation and future v4 consumers.

Profiles:
- ``legacy-v2``    : evaluator-v2 policy-driven compatibility and matching.
- ``legacy-v3``    : evaluator-v3 normalized-phenomenon compatibility.
- ``legacy-facts`` : Facts-study exact-family/meaning matching with span overlap
                     scoring (symmetric maximum-weight alignment).
- ``canonical-v1`` : subject-bound compatible clustering; ``unknown`` may
                     participate in matching but always routes to manual;
                     ``evidence-invalid`` is rejected outright.
"""

from __future__ import annotations

from typing import Any

from .errors import ValidationError
from .quality_contracts import canonical_sha256, exact_fields, string


PROFILE_LEGACY_V2 = "legacy-v2"
PROFILE_LEGACY_V3 = "legacy-v3"
PROFILE_LEGACY_FACTS = "legacy-facts"
PROFILE_CANONICAL_V1 = "canonical-v1"
PROFILES = frozenset(
    (PROFILE_LEGACY_V2, PROFILE_LEGACY_V3, PROFILE_LEGACY_FACTS, PROFILE_CANONICAL_V1)
)

# ---------------------------------------------------------------------------
# Evidence normalization (identical legacy semantics)
# ---------------------------------------------------------------------------


def normalize_evidence(
    evidence: Any,
    text: str,
    *,
    where: str,
    allow_empty_omission: bool = False,
) -> dict[str, Any]:
    if not isinstance(evidence, dict):
        raise ValidationError(f"{where} must be an object")
    allowed = {"quote", "occurrence", "whole_item"}
    unknown = sorted(set(evidence) - allowed)
    if unknown:
        raise ValidationError(f"{where} has host-owned or unknown fields: {', '.join(unknown)}")
    if "quote" not in evidence or "occurrence" not in evidence:
        raise ValidationError(f"{where} requires quote and occurrence")
    quote = string(evidence["quote"], f"{where}.quote", empty=True)
    occurrence = evidence["occurrence"]
    if type(occurrence) is not int or occurrence < 0:
        raise ValidationError(f"{where}.occurrence must be an exact non-negative integer")
    if "whole_item" in evidence and evidence["whole_item"] is not True:
        raise ValidationError(f"{where}.whole_item must be true when present")
    whole_item = evidence.get("whole_item", False)
    if whole_item:
        if quote or occurrence != 0:
            raise ValidationError(f"{where} whole-item evidence requires empty quote and occurrence 0")
        return {"quote": "", "occurrence": 0, "whole_item": True, "state": "whole-item", "start": 0, "end": len(text)}
    if not quote:
        if allow_empty_omission and occurrence == 0:
            return {"quote": "", "occurrence": 0, "state": "missing", "start": None, "end": None}
        raise ValidationError(f"{where} empty quote requires whole_item or a legal omission")
    starts: list[int] = []
    position = 0
    while True:
        position = text.find(quote, position)
        if position < 0:
            break
        starts.append(position)
        position += max(1, len(quote))
    if occurrence == 0:
        return {"quote": quote, "occurrence": 0, "state": "ambiguous" if len(starts) > 1 else "missing", "start": None, "end": None}
    if occurrence > len(starts):
        return {"quote": quote, "occurrence": occurrence, "state": "missing", "start": None, "end": None}
    start = starts[occurrence - 1]
    return {"quote": quote, "occurrence": occurrence, "state": "exact", "start": start, "end": start + len(quote)}


# ---------------------------------------------------------------------------
# Span helpers
# ---------------------------------------------------------------------------


def spans_related(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Legacy-v2 span relatedness (exact/whole-item/missing semantics)."""
    if left["state"] == "whole-item" or right["state"] == "whole-item":
        return left["state"] == right["state"]
    if left["state"] != "exact" or right["state"] != "exact":
        return False
    return left["start"] <= right["end"] and right["start"] <= left["end"]


def spans_identical(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return (
        left["state"] == right["state"]
        and left.get("start") == right.get("start")
        and left.get("end") == right.get("end")
    )


def span_overlap_ratio(left: dict[str, Any], right: dict[str, Any]) -> float:
    """Legacy-Facts span overlap in [0, 1]; 1.0 for paired omissions."""
    if left["state"] == right["state"] == "missing":
        return 1.0
    if left["state"] not in ("exact", "whole-item") or right["state"] not in ("exact", "whole-item"):
        return 0.0
    intersection = max(0, min(left["end"], right["end"]) - max(left["start"], right["start"]))
    union = max(left["end"], right["end"]) - min(left["start"], right["start"])
    return intersection / union if union else 1.0


def spans_intersect(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Non-empty span intersection; paired empty omissions count as related."""
    if left["state"] == right["state"] == "missing":
        return not left.get("quote") and not right.get("quote")
    if left["state"] not in ("exact", "whole-item") or right["state"] not in ("exact", "whole-item"):
        return False
    return max(left["start"], right["start"]) < min(left["end"], right["end"])


def _span_payload(evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "state": evidence.get("state"),
        "start": evidence.get("start"),
        "end": evidence.get("end"),
    }


def claim_view(claim: dict[str, Any]) -> dict[str, Any]:
    """Map legacy and canonical claim shapes onto one common view."""
    source = claim.get("normalized_source_evidence")
    if source is None:
        source = claim.get("source_evidence")
    target = claim.get("normalized_target_evidence")
    if target is None:
        target = claim.get("target_evidence")
    meaning = claim.get("normalized_meaning_change", claim.get("meaning_change"))
    if isinstance(meaning, dict):
        meaning = meaning.get("type")
    return {
        "source": source,
        "target": target,
        "error_family": claim.get("error_family"),
        "phenomenon": claim.get("normalized_phenomenon", claim.get("phenomenon")),
        "meaning_change": meaning,
        "subject": claim.get("subject"),
    }


def claim_signature(claim: dict[str, Any], *, include_subject: bool = True) -> str:
    """Exact identity: subject, error family, phenomenon, meaning change and
    normalized source/target evidence spans."""
    view = claim_view(claim)
    if view["source"] is None or view["target"] is None:
        raise ValidationError("claim_signature requires normalized source/target evidence")
    if "state" not in view["source"] or "state" not in view["target"]:
        raise ValidationError("claim_signature requires normalized evidence with a state")
    payload: dict[str, Any] = {
        "error_family": view["error_family"],
        "phenomenon": view["phenomenon"],
        "meaning_change": view["meaning_change"],
        "source": _span_payload(view["source"]),
        "target": _span_payload(view["target"]),
    }
    if include_subject and view["subject"] is not None:
        payload["subject"] = view["subject"]
    return canonical_sha256(payload)


# ---------------------------------------------------------------------------
# Meaning-change compatibility
# ---------------------------------------------------------------------------

_V2_CONTRADICTIONS = frozenset(
    (
        frozenset(("omitted", "added")),
        frozenset(("weakened", "strengthened")),
        frozenset(("none", "reversed")),
        frozenset(("none", "omitted")),
        frozenset(("none", "added")),
        frozenset(("presentation-only", "reversed")),
        frozenset(("presentation-only", "omitted")),
        frozenset(("presentation-only", "added")),
    )
)

#: canonical-v1 contradictions: only true semantic opposites.  Everything else
#: is compatible (clustering) but ``unknown``/uncertain claims always route to
#: manual adjudication.
_CANONICAL_CONTRADICTIONS = frozenset(
    (
        frozenset(("omitted", "added")),
        frozenset(("weakened", "strengthened")),
        frozenset(("reversed", "weakened")),
        frozenset(("reversed", "strengthened")),
    )
)

_CANONICAL_MERGEABLE_PHENOMENA = frozenset(
    (
        frozenset(("number", "number-range")),
        frozenset(("terminology", "proper-name")),
        frozenset(("omission", "unit")),
        frozenset(("ambiguity", "other")),
    )
)


def meaning_changes_compatible(left: str, right: str, *, legacy: bool = False) -> bool:
    if left == right or "unknown" in {left, right}:
        return True
    contradictions = _V2_CONTRADICTIONS if legacy else _CANONICAL_CONTRADICTIONS
    return frozenset((left, right)) not in contradictions


def meaning_compatibility_decision(
    left: str, right: str, *, legacy: bool = False
) -> dict[str, Any]:
    """Compatibility with routing: unknown or uncertain pairs are compatible
    for clustering but never silently derive an automatic minor."""
    compatible = meaning_changes_compatible(left, right, legacy=legacy)
    requires_manual = "unknown" in {left, right} or not compatible
    reason = (
        "meaning-change-unknown"
        if "unknown" in {left, right}
        else ("meaning-change-contradiction" if not compatible else "none")
    )
    return {
        "compatible": compatible,
        "requires_manual": requires_manual,
        "reason": reason,
    }


def phenomena_compatible(left: str, right: str, *, policy: dict[str, Any] | None = None, legacy: bool = False) -> bool:
    if left == right:
        return True
    if legacy:
        if policy is None:
            return False
        declared = {tuple(sorted(item)) for item in policy["mergeable_phenomena"]}
        return tuple(sorted((left, right))) in declared
    return frozenset((left, right)) in _CANONICAL_MERGEABLE_PHENOMENA


# ---------------------------------------------------------------------------
# Legacy-v2 profile
# ---------------------------------------------------------------------------


def legacy_v2_phenomenon_compatible(left: dict[str, Any], right: dict[str, Any], policy: dict[str, Any]) -> bool:
    """Byte-identical re-implementation of quality_v2._phenomenon_compatible."""
    left_value = left["phenomenon"]
    right_value = right["phenomenon"]
    if left_value == right_value:
        return True
    pair = tuple(sorted((left_value, right_value)))
    declared = {tuple(sorted(item)) for item in policy["mergeable_phenomena"]}
    if pair not in declared:
        return False
    if pair == ("ambiguity", "fluency"):
        return spans_identical(
            left["normalized_source_evidence"], right["normalized_source_evidence"]
        ) and spans_identical(
            left["normalized_target_evidence"], right["normalized_target_evidence"]
        )
    if pair == ("omission", "unit"):
        return (
            left["meaning_change"]["type"] == "omitted"
            and right["meaning_change"]["type"] == "omitted"
            and spans_identical(
                left["normalized_source_evidence"], right["normalized_source_evidence"]
            )
            and spans_identical(
                left["normalized_target_evidence"], right["normalized_target_evidence"]
            )
        )
    return True


def legacy_v2_findings_match(
    left: dict[str, Any], right: dict[str, Any], policy: dict[str, Any]
) -> bool:
    """Byte-identical re-implementation of quality_v2.findings_match."""
    if not spans_related(
        left["normalized_source_evidence"], right["normalized_source_evidence"]
    ):
        return False
    left_target = left["normalized_target_evidence"]
    right_target = right["normalized_target_evidence"]
    if left_target["state"] == "missing" and right_target["state"] == "missing":
        target_related = not left_target.get("quote") and not right_target.get("quote")
    else:
        target_related = spans_related(left_target, right_target)
    if not target_related:
        return False
    if not legacy_v2_phenomenon_compatible(left, right, policy):
        return False
    return meaning_changes_compatible(
        left["meaning_change"]["type"], right["meaning_change"]["type"], legacy=True
    )


# ---------------------------------------------------------------------------
# Legacy-v3 profile
# ---------------------------------------------------------------------------


def legacy_v3_spans_related(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Byte-identical re-implementation of quality_v3._spans_related."""
    for side in ("normalized_source_evidence", "normalized_target_evidence"):
        a, b = left[side], right[side]
        if a["state"] not in {"exact", "whole-item"} or b["state"] not in {"exact", "whole-item"}:
            if a["state"] == b["state"] == "missing" and not a.get("quote") and not b.get("quote"):
                continue
            return False
        if max(a["start"], b["start"]) >= min(a["end"], b["end"]):
            return False
    return True


def legacy_v3_findings_compatible(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Byte-identical re-implementation of quality_v3._findings_compatible."""
    if not legacy_v3_spans_related(left, right):
        return False
    lp, rp = left["normalized_phenomenon"], right["normalized_phenomenon"]
    compatible = lp == rp or frozenset((lp, rp)) in {
        frozenset(("number", "number-range")),
        frozenset(("terminology", "proper-name")),
        frozenset(("omission", "unit")),
        frozenset(("ambiguity", "other")),
    }
    return compatible


# ---------------------------------------------------------------------------
# Legacy-Facts profile: symmetric maximum-weight alignment
# ---------------------------------------------------------------------------


def _facts_claim_key(claim: dict[str, Any]) -> str:
    return canonical_sha256({
        "error_family": claim["error_family"], "phenomenon": claim["phenomenon"],
        "meaning_change": claim["meaning_change"],
        "source": {key: claim["source_evidence"].get(key) for key in ("state", "start", "end")},
        "target": {key: claim["target_evidence"].get(key) for key in ("state", "start", "end")},
    })


def _facts_edge_score(left: dict[str, Any], right: dict[str, Any]) -> int:
    if (
        left["error_family"] != right["error_family"]
        or left["phenomenon"] != right["phenomenon"]
        or left["meaning_change"] != right["meaning_change"]
    ):
        return -1
    source = span_overlap_ratio(left["source_evidence"], right["source_evidence"])
    target = span_overlap_ratio(left["target_evidence"], right["target_evidence"])
    if source == 0 or target == 0:
        return -1
    return int(1000 * (source + target))


def _facts_collection_key(claims: list[dict[str, Any]]) -> tuple[tuple[str, str], ...]:
    return tuple(sorted((_facts_claim_key(claim), canonical_sha256(claim)) for claim in claims))


def _align_canonical_sides(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> list[tuple[int, int]]:
    left_order = sorted(range(len(left)), key=lambda index: (_facts_claim_key(left[index]), canonical_sha256(left[index])))
    right_order = sorted(range(len(right)), key=lambda index: (_facts_claim_key(right[index]), canonical_sha256(right[index])))
    ordered_left = [left[index] for index in left_order]
    ordered_right = [right[index] for index in right_order]
    memo: dict[tuple[int, int], tuple[int, tuple[tuple[int, int], ...]]] = {}

    def solve(index: int, mask: int) -> tuple[int, tuple[tuple[int, int], ...]]:
        key = (index, mask)
        if key in memo:
            return memo[key]
        if index == len(ordered_left):
            return (0, ())
        best = solve(index + 1, mask)
        for rindex, candidate in enumerate(ordered_right):
            if mask & (1 << rindex):
                continue
            score = _facts_edge_score(ordered_left[index], candidate)
            if score < 0:
                continue
            tail_score, tail_pairs = solve(index + 1, mask | (1 << rindex))
            option = (score + tail_score, ((index, rindex),) + tail_pairs)
            if option[0] > best[0] or (option[0] == best[0] and option[1] < best[1]):
                best = option
        memo[key] = best
        return best

    return sorted((left_order[lindex], right_order[rindex]) for lindex, rindex in solve(0, 0)[1])


def align_claims(
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
    profile: str = PROFILE_LEGACY_FACTS,
) -> list[tuple[int, int]]:
    """Deterministic, direction-independent maximum-weight one-to-one alignment."""
    if profile not in PROFILES:
        raise ValidationError(f"unknown claim compatibility profile: {profile}")
    if profile != PROFILE_LEGACY_FACTS:
        raise ValidationError(f"align_claims only implements the {PROFILE_LEGACY_FACTS} profile")
    left_key, right_key = _facts_collection_key(left), _facts_collection_key(right)
    if right_key < left_key:
        return sorted((right_index, left_index) for left_index, right_index in _align_canonical_sides(right, left))
    return _align_canonical_sides(left, right)


def union_findings(left: dict[str, Any], right: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Host-only, symmetric B+F union; no assessment is exposed to a model.

    Byte-identical to the legacy Facts-study implementation.
    """
    left_map = {entry["revision_id"]: entry["findings"] for entry in left["items"]}
    right_map = {entry["revision_id"]: entry["findings"] for entry in right["items"]}
    result: dict[str, list[dict[str, Any]]] = {}
    for revision_id in sorted(set(left_map) | set(right_map)):
        lfindings = left_map.get(revision_id, [])
        rfindings = right_map.get(revision_id, [])
        pairs = align_claims(lfindings, rfindings)
        used_l, used_r = {a for a, _ in pairs}, {b for _, b in pairs}
        merged = []
        for lindex, rindex in pairs:
            candidates = sorted(
                (lfindings[lindex], rfindings[rindex]),
                key=lambda finding: (_facts_claim_key(finding), canonical_sha256(finding)),
            )
            base = dict(candidates[0])
            base["supported_fact_ids"] = sorted(set(lfindings[lindex]["supported_fact_ids"]) | set(rfindings[rindex]["supported_fact_ids"]))
            base["requires_manual"] = lfindings[lindex]["requires_manual"] or rfindings[rindex]["requires_manual"]
            merged.append(base)
        merged.extend(finding for index, finding in enumerate(lfindings) if index not in used_l)
        merged.extend(finding for index, finding in enumerate(rfindings) if index not in used_r)
        result[revision_id] = sorted(
            merged, key=lambda finding: (_facts_claim_key(finding), canonical_sha256(finding))
        )
    return result


# ---------------------------------------------------------------------------
# canonical-v1: subject-bound compatible clustering
# ---------------------------------------------------------------------------


def _canonical_compatible(left: dict[str, Any], right: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    """Compatibility decision for canonical-v1 clustering.

    Requirements: same subject (when both declare one), intersecting evidence
    on both sides (or paired omissions), category-compatible phenomenon and
    non-contradictory meaning change.
    """
    lview, rview = claim_view(left), claim_view(right)
    if lview["source"] is None or lview["target"] is None or rview["source"] is None or rview["target"] is None:
        return False, {"reason": "missing-normalized-evidence"}
    if lview["subject"] is not None and rview["subject"] is not None and lview["subject"] != rview["subject"]:
        return False, {"reason": "subject-mismatch"}
    if not spans_intersect(lview["source"], rview["source"]):
        return False, {"reason": "source-span-disjoint"}
    if not spans_intersect(lview["target"], rview["target"]):
        return False, {"reason": "target-span-disjoint"}
    if lview["error_family"] is not None and rview["error_family"] is not None and lview["error_family"] != rview["error_family"]:
        return False, {"reason": "error-family-mismatch"}
    if not phenomena_compatible(lview["phenomenon"], rview["phenomenon"]):
        return False, {"reason": "phenomenon-incompatible"}
    decision = meaning_compatibility_decision(lview["meaning_change"], rview["meaning_change"])
    if not decision["compatible"]:
        return False, {"reason": decision["reason"]}
    return True, {"reason": "compatible", "requires_manual": decision["requires_manual"]}


def claims_compatible(
    left: dict[str, Any],
    right: dict[str, Any],
    profile: str = PROFILE_CANONICAL_V1,
    policy: dict[str, Any] | None = None,
) -> bool:
    """Profile-specific claim compatibility predicate."""
    if profile == PROFILE_LEGACY_V2:
        return legacy_v2_findings_match(left, right, policy)
    if profile == PROFILE_LEGACY_V3:
        return legacy_v3_findings_compatible(left, right)
    if profile == PROFILE_LEGACY_FACTS:
        return _facts_edge_score(left, right) >= 0
    if profile == PROFILE_CANONICAL_V1:
        compatible, _ = _canonical_compatible(left, right)
        return compatible
    raise ValidationError(f"unknown claim compatibility profile: {profile}")


def cluster_claims(
    claims: list[dict[str, Any]],
    profile: str = PROFILE_CANONICAL_V1,
    policy: dict[str, Any] | None = None,
) -> list[list[int]]:
    """Stable transitive clustering of pairwise-compatible claims.

    Returns clusters as lists of claim indices in input order; cluster order
    follows the first member index.  Compatible matching is symmetric, so the
    result is direction independent.
    """
    parent = list(range(len(claims)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for left in range(len(claims)):
        for right in range(left + 1, len(claims)):
            if claims_compatible(claims[left], claims[right], profile=profile, policy=policy):
                left_root, right_root = find(left), find(right)
                if left_root != right_root:
                    parent[max(left_root, right_root)] = min(left_root, right_root)
    buckets: dict[int, list[int]] = {}
    for index in range(len(claims)):
        buckets.setdefault(find(index), []).append(index)
    return [buckets[key] for key in sorted(buckets)]


# ---------------------------------------------------------------------------
# Independent uncertainty states and routing
# ---------------------------------------------------------------------------

UNCERTAINTY_STATES = frozenset(
    (
        "none",
        "unknown",
        "other",
        "taxonomy-unknown",
        "context-insufficient",
        "evidence-invalid",
    )
)

_ROUTING = {
    "none": ("normal", False),
    "unknown": ("manual", True),
    "other": ("manual", True),
    "taxonomy-unknown": ("manual", True),
    "context-insufficient": ("manual", True),
    "evidence-invalid": ("rejected", True),
}

_ROUTING_REASONS = {
    "unknown": "unknown claims may match but must be routed to manual adjudication",
    "other": "uncategorized claims stay in the other state and require manual routing",
    "taxonomy-unknown": "taxonomy-unknown claims require manual routing and never auto-derive minor",
    "context-insufficient": "context-insufficient claims require manual routing and never auto-derive minor",
    "evidence-invalid": "evidence-invalid claims are rejected outright and never downgraded",
}


def route_uncertainty(state: str) -> dict[str, Any]:
    """Independent uncertainty routing; no state silently becomes minor."""
    if state not in UNCERTAINTY_STATES:
        raise ValidationError(f"unknown uncertainty state: {state}")
    routing, requires_manual = _ROUTING[state]
    return {
        "state": state,
        "routing": routing,
        "requires_manual": requires_manual,
        "auto_minor": False,
        "reason": _ROUTING_REASONS.get(state, "no uncertainty"),
    }


def validate_uncertainty(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(value, ("state", "routing", "requires_manual", "auto_minor", "reason"), where)
    state = value["state"]
    if state not in UNCERTAINTY_STATES:
        raise ValidationError(f"{where}.state must be one of: {', '.join(sorted(UNCERTAINTY_STATES))}")
    expected = route_uncertainty(state)
    for field in ("routing", "requires_manual", "auto_minor"):
        if value[field] != expected[field]:
            raise ValidationError(f"{where}.{field} is inconsistent with state {state}")
    if value["reason"] != expected["reason"] and not value["reason"].startswith(expected["reason"] + "; "):
        raise ValidationError(f"{where}.reason is inconsistent with state {state}")
    return dict(value)


def make_uncertainty(state: str, *, reason: str | None = None) -> dict[str, Any]:
    if state not in UNCERTAINTY_STATES:
        raise ValidationError(f"unknown uncertainty state: {state}")
    result = route_uncertainty(state)
    if reason:
        result["reason"] = f"{result['reason']}; {reason}"
    return result
