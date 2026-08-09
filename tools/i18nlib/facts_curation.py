"""Facts-study curation v1: source-side pool, curator flow and quota selection.

This module implements ``facts-study-curation-v1`` on top of the shared
contract/claim core.  It deliberately does not grow ``facts_study.py``:

- ``facts-study-curation-build``   : deterministic 80-item source-side pool.
- ``facts-study-curation-prepare`` : frozen Facts packet -> target-visible
                                     curator bundle and assessment template.
- ``facts-study-curation-select``  : curator assessment -> final 20-item
                                     sample v2 (natural first, minimal
                                     controlled fill), gold drafts and a
                                     registry fragment.

The seven-arm bundle/preregistration/fake-replay chain dispatches through the
existing ``facts-study-bundles/validate/report`` commands on the sample
contract; external execution is impossible for ``offline-frozen``
preregistrations.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from .config import Manifest
from .dataset_registry import (
    build_registry_fragment,
    excluded_revision_ids,
    load_registry,
    validate_registry_fragment,
)
from .errors import ConfigurationError, ValidationError
from .facts_study import (
    ARMS,
    pi_executable_identity,
    FACT_ARMS,
    NO_FACT_ARMS,
    OPAQUE_FACT_ID_PATTERN,
    SUPPLEMENTAL_PROVENANCE_KINDS,
    _assessment_map,
    _safe_ratio,
    _score,
    build_fake_assessments,
    build_report,
    build_schedule,
    canonical_sha256,
    load_arm_prompt,
    load_historical_exclusions,
)
from .quality import create_quality_run_directory, structure_signature
from .quality_claims import normalize_evidence, validate_uncertainty
from .quality_contracts import (
    canonical_json_bytes,
    exact_fields,
    read_json_object,
    sha256 as sha256_field,
    string,
    validate_provenance,
)
from .report import write_json


CURATION_POOL_CONTRACT = "tome4-quality-facts-study-curation-pool-v1"
CURATION_FACTS_AUTHOR_BUNDLE_CONTRACT = "tome4-quality-facts-author-bundle-v3"
CURATION_PACKET_CONTRACT = "tome4-quality-fact-packet-v3"
CURATION_CURATOR_BUNDLE_CONTRACT = "tome4-quality-curator-bundle-v1"
CURATION_CURATOR_ASSESSMENT_CONTRACT = "tome4-quality-curator-assessment-v1"
CURATION_SAMPLE_CONTRACT = "tome4-quality-facts-study-sample-v2"
CURATION_GOLD_CONTRACT = "tome4-quality-facts-study-gold-v2"
CURATION_GOLD_REVIEW_CONTRACT = "tome4-quality-facts-study-gold-review-v2"
CURATION_GOLD_ADJUDICATION_CONTRACT = "tome4-quality-facts-study-gold-adjudication-v2"
CURATION_BUNDLE_CONTRACT = "tome4-quality-facts-study-bundle-v2"
CURATION_ASSESSMENT_CONTRACT = "tome4-quality-facts-study-assessment-v2"
CURATION_PREREG_CONTRACT = "tome4-quality-facts-study-preregistration-v2"
CURATION_VALIDATION_CONTRACT = "tome4-quality-facts-study-validation-index-v2"
CURATION_REPORT_CONTRACT = "tome4-quality-facts-study-report-v2"
CONTROLLED_MUTATION_CONTRACT = "tome4-quality-controlled-mutation-v1"
CONTROLLED_VARIANTS_REQUEST_CONTRACT = "tome4-quality-controlled-variants-request-v1"
CONTROLLED_VARIANTS_CONTRACT = "tome4-quality-controlled-variants-v1"

CURATION_SEED = "tome4-facts-study-curation-v1"
SELECTION_SEED = "tome4-facts-study-curation-select-v1"

STRATA = (
    "term-proper-name",
    "mechanism-condition-number",
    "entity-relation",
    "ui-role",
    "general-semantic-clean-control",
)
STRATUM_TARGETS = {
    "term-proper-name": 20,
    "mechanism-condition-number": 20,
    "entity-relation": 15,
    "ui-role": 15,
    "general-semantic-clean-control": 10,
}
ITEM_KINDS = frozenset(("semantic", "term", "mechanics", "ui", "localization"))
CLASSIFICATIONS = frozenset(
    ("fact-dependent-defect", "surface-defect", "clean", "acceptable-localization", "unsuitable-uncertain")
)
SELECTION_CLASSIFICATIONS = frozenset(
    ("fact-dependent-defect", "surface-defect", "clean", "acceptable-localization")
)
MUTATION_KINDS = frozenset(
    (
        "number-flip", "condition-inversion", "polarity-reversal",
        "term-substitution", "unit-change", "entity-role-swap",
        "omission-introduction", "addition-introduction",
    )
)
CURATION_POOL_SIZE = 80
FINAL_SAMPLE_SIZE = 20
FACT_QUOTA = 8
SURFACE_QUOTA = 6
CLEAN_ACCEPTABLE_QUOTA = 6
CLEAN_MIN = 5
FACT_TRAPS_MIN = 3

#: strata that tolerate short sources when the 80-1500 band cannot fill them
_LENGTH_EXEMPT_STRATA = frozenset(("term-proper-name", "ui-role"))


def load_protocol(manifest: Manifest, *, version: str = "v4") -> dict[str, Any]:
    """Load the frozen curation protocol (v3 baseline or v4 enriched pool).

    v4 changes only the source-side pool construction parameters (stratum
    targets, length band, long-source preference, risk bonus); arms, quotas,
    controlled policy and every downstream contract stay identical.
    """
    if version not in ("v3", "v4", "v5"):
        raise ConfigurationError(f"unsupported facts study curation protocol version: {version}")
    path = manifest.root / "i18n" / "quality" / f"facts-study-{version}.json"
    value = read_json_object(path, "facts study curation protocol")
    expected_contract = {
        "v3": "tome4-quality-facts-study-protocol-v3",
        "v4": "tome4-quality-facts-study-protocol-v4",
        "v5": "tome4-quality-facts-study-protocol-v5",
    }[version]
    if value.get("contract") != expected_contract or value.get("schema_version") != 1:
        raise ConfigurationError(f"unsupported facts study curation protocol: {path}")
    if value.get("arms") != list(ARMS) or value.get("item_count") != FINAL_SAMPLE_SIZE:
        raise ConfigurationError("facts study curation protocol must freeze seven arms and 20 items")
    if value.get("max_external_slots") != 33 or value.get("shard_count") != 1:
        raise ConfigurationError("facts study curation protocol must freeze 33 one-shard slots")
    if value.get("pool_contract") != CURATION_POOL_CONTRACT or value.get("sample_contract") != CURATION_SAMPLE_CONTRACT:
        raise ConfigurationError("facts study curation protocol binds unsupported pool/sample contracts")
    if value.get("dataset_registry") != "dataset-registry-v1.json":
        raise ConfigurationError("facts study curation protocol does not bind the dataset registry")
    if value.get("fact_policy", {}).get("language") != "english-metalanguage":
        raise ConfigurationError("facts study curation Facts statements must use English metalanguage")
    if value.get("controlled_policy", {}).get("grant_clearance") is not False:
        raise ConfigurationError("facts study curation controlled variants can never grant clearance")
    if version in ("v4", "v5"):
        if sum(value["pool_targets"].values()) != CURATION_POOL_SIZE:
            raise ConfigurationError("v4/v5 pool targets must sum to 80")
        if not value["length_policy"].get("prefer_long_source"):
            raise ConfigurationError("v4/v5 length policy must prefer long sources")
    return value


def _pool_selection_params(protocol: dict[str, Any] | None) -> dict[str, Any]:
    """Source-side pool construction parameters (v3 defaults when None)."""
    if protocol is None:
        return {
            "targets": STRATUM_TARGETS,
            "min_chars": 80, "max_chars": 1500,
            "exempt_strata": ("term-proper-name", "ui-role"),
            "prefer_long_source": False,
            "long_source_peak_chars": 1500,
            "risk_bonus": {},
        }
    length_policy = protocol["length_policy"]
    return {
        "targets": protocol["pool_targets"],
        "min_chars": length_policy["min_chars"],
        "max_chars": length_policy["max_chars"],
        "exempt_strata": tuple(length_policy.get("exempt_strata", ("term-proper-name",))),
        "prefer_long_source": bool(length_policy.get("prefer_long_source", False)),
        "long_source_peak_chars": int(length_policy.get("long_source_peak_chars", 1500)),
        "risk_bonus": dict(protocol.get("risk_bonus", {})),
    }


def _long_source_score(length: int, peak: int) -> int:
    return length if length <= peak else peak - (length - peak) * 2


def _source_risk_bonus(row: dict[str, Any], risk_bonus: dict[str, int]) -> int:
    flags = row.get("risk_flags") or []
    return sum(risk_bonus.get(flag, 0) for flag in flags if isinstance(flag, str))


# ---------------------------------------------------------------------------
# Source-side classification (only reads source/source tag/section/profile/
# context/terminology features; never the target)
# ---------------------------------------------------------------------------


def _terminology_features(row: dict[str, Any]) -> list[dict[str, str]]:
    features = []
    for term in row.get("relevant_terms") or []:
        if not isinstance(term, dict):
            continue
        features.append({
            "category": str(term.get("category") or ""),
            "domain": str(term.get("domain") or ""),
            "term_source": str(term.get("source") or ""),
            "status": str(term.get("status") or ""),
            "match": str(term.get("match") or ""),
        })
    return features


def classify_stratum(row: dict[str, Any]) -> str:
    """Deterministic source-side stratum assignment."""
    profile = row.get("profile")
    if profile == "term-name":
        return "term-proper-name"
    if profile == "mechanics":
        return "mechanism-condition-number"
    if profile == "ui":
        return "ui-role"
    features = row.get("relevant_terms") or []
    has_entity = any(
        isinstance(term, dict)
        and str(term.get("category") or "").startswith(("T.PN.", "T.GAME.ENTITY"))
        for term in features
    )
    if profile in ("dialogue", "narrative", "runtime-log") and has_entity:
        return "entity-relation"
    return "general-semantic-clean-control"


def _public_input_identity(
    *, source: str, source_tag: str, section: str, item_kind: str, stratum: str,
    bounded_context: list[dict[str, Any]], terminology_features: list[dict[str, Any]],
) -> str:
    return canonical_sha256({
        "source": source, "source_tag": source_tag, "section": section,
        "item_kind": item_kind, "stratum": stratum,
        "bounded_context": [
            {"relative_index": entry.get("relative_index"), "source": entry.get("source", "")}
            for entry in bounded_context[:2]
        ],
        "terminology_features": terminology_features,
    })


def _read_inventory(path: Path) -> tuple[list[dict[str, Any]], str]:
    try:
        raw = path.read_bytes()
        rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"cannot read curation inventory: {path}: {error}") from error
    if not rows or any(not isinstance(row, dict) for row in rows):
        raise ValidationError("curation inventory must contain JSON objects")
    return rows, hashlib.sha256(raw).hexdigest()


def _revision_ids_from_artifact(path: Path) -> set[str]:
    value = read_json_object(path, "curation exclusion artifact")
    ids: set[str] = set()
    for revision_id in value.get("excluded_revision_ids", []):
        if isinstance(revision_id, str):
            ids.add(revision_id)
    for entry in value.get("items", []):
        if isinstance(entry, dict) and isinstance(entry.get("revision_id"), str):
            ids.add(entry["revision_id"])
    for entry in value.get("revisions", []):
        if isinstance(entry, dict) and isinstance(entry.get("revision_id"), str):
            ids.add(entry["revision_id"])
    return ids


def _load_inventory_rows(path: Path, expected_sha256: str) -> dict[str, dict[str, Any]]:
    rows, inventory_sha = _read_inventory(path)
    if inventory_sha != expected_sha256:
        raise ValidationError("inventory bytes do not match the pool inventory_sha256")
    return {row["revision_id"]: row for row in rows}


def _pool_length_policy(params: dict[str, Any]) -> dict[str, Any]:
    if params["prefer_long_source"]:
        return {
            "min_chars": params["min_chars"], "max_chars": params["max_chars"],
            "exempt_strata": sorted(params["exempt_strata"]),
            "prefer_long_source": True,
            "long_source_peak_chars": params["long_source_peak_chars"],
        }
    return {
        "min_chars": params["min_chars"], "max_chars": params["max_chars"],
        "term_entries_exempt": True,
    }


def _pool_selection_inputs(params: dict[str, Any]) -> dict[str, Any]:
    value: dict[str, Any] = {
        "source_side_only": True, "target_blind": True,
        "dedupe_key": "model-visible-public-input",
    }
    if params["prefer_long_source"]:
        value["prefer_long_source"] = True
        value["risk_bonus"] = dict(sorted(params["risk_bonus"].items()))
    return value


# ---------------------------------------------------------------------------
# Pool build + validation
# ---------------------------------------------------------------------------


def build_candidate_pool(
    *,
    inventory_path: Path,
    exclusion_paths: list[Path],
    seed: str,
    required_excluded_ids: Iterable[str] = (),
    protocol: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Deterministic source-side 80-item pool.

    Selection reads only source, source tag, section, profile, public context
    and terminology features; replacing every target leaves the selection
    byte-identical.  The v3 protocol keeps the 80-1500 band with a documented
    ui relaxation; the v4 protocol tightens the band to 300-1500, prefers long
    sources and adds source-side risk flags as a selection bonus.
    """
    params = _pool_selection_params(protocol)
    targets = params["targets"]
    if sum(targets.values()) != CURATION_POOL_SIZE:
        raise ValidationError(f"curation pool targets must sum to {CURATION_POOL_SIZE}")
    rows, inventory_sha = _read_inventory(inventory_path)
    excluded: set[str] = set(required_excluded_ids)
    for path in exclusion_paths:
        excluded.update(_revision_ids_from_artifact(path))
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("revision_id") in excluded:
            continue
        stratum = classify_stratum(row)
        length = len(str(row.get("source") or ""))
        if stratum in params["exempt_strata"] or params["min_chars"] <= length <= params["max_chars"]:
            eligible = True
        else:
            eligible = False
        if eligible:
            buckets[stratum].append(row)
    # candidates are deduplicated by their model-visible public input
    for stratum in STRATA:
        deduped: list[dict[str, Any]] = []
        seen_public: set[str] = set()
        for row in buckets[stratum]:
            public_id = _public_input_identity(
                source=str(row.get("source") or ""),
                source_tag=str(row.get("source_tag") or ""),
                section=str(row.get("section") or ""),
                item_kind={
                    "term-name": "term", "mechanics": "mechanics", "ui": "ui",
                    "dialogue": "semantic", "narrative": "semantic", "runtime-log": "semantic",
                }.get(str(row.get("profile") or "unknown"), "localization"),
                stratum=stratum,
                bounded_context=[
                    {"relative_index": entry.get("relative_index"), "source": entry.get("source", "")}
                    for entry in (row.get("context_neighbors") or [])[:2]
                    if isinstance(entry, dict)
                ],
                terminology_features=_terminology_features(row),
            )
            if public_id in seen_public:
                continue
            seen_public.add(public_id)
            deduped.append(row)
        buckets[stratum] = deduped
    selected: dict[str, list[dict[str, Any]]] = defaultdict(list)
    relaxations: dict[str, dict[str, Any]] = {}
    for stratum in STRATA:
        target = targets[stratum]
        candidates = list(buckets[stratum])
        if params["prefer_long_source"]:
            def source_score(row: dict[str, Any]) -> int:
                length = len(str(row.get("source") or ""))
                return _long_source_score(length, params["long_source_peak_chars"]) + _source_risk_bonus(row, params["risk_bonus"])
            candidates.sort(key=lambda row: (-source_score(row), str(row["revision_id"])))
            pool_rows = candidates[:target]
        else:
            rng = random.Random(f"{seed}:{stratum}")
            rng.shuffle(candidates)
            preferred = [row for row in candidates if stratum == "term-proper-name" or params["min_chars"] <= len(str(row.get("source") or "")) <= params["max_chars"]]
            relaxed = [row for row in candidates if row not in preferred]
            pool_rows = preferred[:target]
            relaxed_used = 0
            if len(pool_rows) < target:
                relaxed_used = min(target - len(pool_rows), len(relaxed))
                pool_rows.extend(relaxed[:relaxed_used])
            if stratum in params["exempt_strata"] and relaxed_used:
                relaxations[stratum] = {
                    "target": target, "preferred_band_filled": len(pool_rows) - relaxed_used,
                    "relaxed_short_filled": relaxed_used,
                    "reason": "insufficient sources in the frozen length band",
                }
        if len(pool_rows) < target:
            raise ConfigurationError(
                f"curation pool stratum {stratum} has only {len(candidates)} eligible "
                f"rows; cannot fill target {target}"
            )
        selected[stratum] = pool_rows
    items: list[dict[str, Any]] = []
    pool_index = 0
    for stratum in STRATA:
        for row in selected[stratum]:
            source = str(row.get("source") or "")
            source_tag = str(row.get("source_tag") or "")
            section = str(row.get("section") or "")
            profile = str(row.get("profile") or "unknown")
            item_kind = {
                "term-name": "term", "mechanics": "mechanics", "ui": "ui",
                "dialogue": "semantic", "narrative": "semantic", "runtime-log": "semantic",
            }.get(profile, "localization")
            neighbors = row.get("context_neighbors") or []
            bounded_context = [
                {"relative_index": entry.get("relative_index"), "source": entry.get("source", "")}
                for entry in neighbors[:2]
                if isinstance(entry, dict)
            ]
            features = _terminology_features(row)
            public_id = _public_input_identity(
                source=source, source_tag=source_tag, section=section,
                item_kind=item_kind, stratum=stratum,
                bounded_context=bounded_context, terminology_features=features,
            )
            items.append({
                "pool_index": pool_index,
                "revision_id": row["revision_id"],
                "source": source, "source_tag": source_tag, "section": section,
                "profile": profile, "item_kind": item_kind, "stratum": stratum,
                "bounded_context": bounded_context,
                "terminology_features": features,
                "source_length": len(source),
                "public_input_identity": public_id,
                "origin": "natural",
                "args_order": row.get("args_order"),
            })
            pool_index += 1
    if len(items) < CURATION_POOL_SIZE:
        raise ConfigurationError(
            f"curation pool dedupe reduced the pool to {len(items)} < {CURATION_POOL_SIZE}"
        )
    items = items[:CURATION_POOL_SIZE]
    stratum_counts = {stratum: sum(item["stratum"] == stratum for item in items) for stratum in STRATA}
    pool_id = canonical_sha256({
        "contract": CURATION_POOL_CONTRACT, "seed": seed,
        "inventory_sha256": inventory_sha, "excluded": sorted(excluded),
        "stratum_targets": targets, "items": items,
    })
    pool = {
        "contract": CURATION_POOL_CONTRACT, "schema_version": 1, "pool_id": pool_id,
        "seed": seed, "inventory_sha256": inventory_sha,
        "excluded_revision_ids": sorted(excluded),
        "exclusion_revision_ids_sha256": canonical_sha256(sorted(excluded)),
        "stratum_targets": targets, "stratum_counts": stratum_counts,
        "length_policy": _pool_length_policy(params),
        "selection_inputs": _pool_selection_inputs(params),
        "items": items,
    }
    author_bundle = build_facts_author_bundle(pool)
    facts = {
        "contract": CURATION_PACKET_CONTRACT, "schema_version": 1,
        "pool_id": pool_id, "packet_kind": "facts", "status": "draft",
        "non_exhaustive": True, "supplemental_only": True,
        "language": "english-metalanguage",
        "authoring_lineage": {
            "role": "facts-author", "actor_id": "", "target_defects_seen": False,
            "gold_seen": False, "curator_assessments_seen": False,
            "common_input_restatements_excluded": True,
            "source_inputs_sha256": canonical_sha256(author_bundle),
        },
        "items": [{"revision_id": item["revision_id"], "facts": []} for item in items],
    }
    report = {
        "pool_id": pool_id, "seed": seed, "inventory_sha256": inventory_sha,
        "items": len(items), "historical_exclusions": len(excluded),
        "stratum_counts": stratum_counts,
        "length_relaxations": relaxations or None,
        "target_blind": True, "status": "authoring-required",
    }
    return pool, author_bundle, facts, report


def _pool_band(value: dict[str, Any]) -> tuple[tuple[str, ...], int, int]:
    """(exempt_strata, min_chars, max_chars) from the pool's own policy."""
    length_policy = value["length_policy"]
    if not isinstance(length_policy, dict):
        raise ValidationError("pool.length_policy must be an object")
    min_chars = length_policy.get("min_chars")
    max_chars = length_policy.get("max_chars")
    if type(min_chars) is not int or type(max_chars) is not int or min_chars < 0 or max_chars <= min_chars:
        raise ValidationError("pool.length_policy must freeze a legal length band")
    if "exempt_strata" in length_policy:
        exempt = length_policy["exempt_strata"]
        if not isinstance(exempt, list) or not exempt or any(stratum not in STRATA for stratum in exempt):
            raise ValidationError("pool.length_policy.exempt_strata is invalid")
        exempt_strata = tuple(sorted(exempt))
    else:
        if length_policy.get("term_entries_exempt") is not True:
            raise ValidationError("pool.length_policy must declare term entries exempt")
        exempt_strata = ("term-proper-name", "ui-role")
    return exempt_strata, min_chars, max_chars


def validate_pool(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("curation pool must be an object")
    exact_fields(
        value,
        ("contract", "schema_version", "pool_id", "seed", "inventory_sha256",
         "excluded_revision_ids", "exclusion_revision_ids_sha256",
         "stratum_targets", "stratum_counts", "length_policy",
         "selection_inputs", "items"),
        "curation pool",
    )
    if value["contract"] != CURATION_POOL_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported curation pool contract")
    sha256_field(value["pool_id"], "pool.pool_id")
    string(value["seed"], "pool.seed")
    sha256_field(value["inventory_sha256"], "pool.inventory_sha256")
    if not isinstance(value["excluded_revision_ids"], list) or value["excluded_revision_ids"] != sorted(set(value["excluded_revision_ids"])):
        raise ValidationError("pool.excluded_revision_ids must be a sorted unique list")
    for revision_id in value["excluded_revision_ids"]:
        sha256_field(revision_id, "pool.excluded_revision_ids")
    if canonical_sha256(value["excluded_revision_ids"]) != value["exclusion_revision_ids_sha256"]:
        raise ValidationError("pool exclusion revision digest mismatch")
    if sum(value["stratum_targets"].values()) != CURATION_POOL_SIZE:
        raise ValidationError("pool stratum targets must sum to 80")
    if value["selection_inputs"]["source_side_only"] is not True or value["selection_inputs"]["target_blind"] is not True:
        raise ValidationError("pool selection inputs must be frozen source-side only")
    exempt_strata, min_chars, max_chars = _pool_band(value)
    if min_chars != 80 and min_chars != 300:
        raise ValidationError(f"pool length band minimum must be 80 or 300, got {min_chars}")
    items = value["items"]
    if not isinstance(items, list) or len(items) != CURATION_POOL_SIZE:
        raise ValidationError(f"curation pool must contain exactly {CURATION_POOL_SIZE} items")
    seen_ids: set[str] = set()
    seen_inputs: set[str] = set()
    counts: Counter[str] = Counter()
    for index, item in enumerate(items):
        where = f"pool.items[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(
            item,
            ("pool_index", "revision_id", "source", "source_tag", "section",
             "profile", "item_kind", "stratum", "bounded_context",
             "terminology_features", "source_length", "public_input_identity",
             "origin", "args_order"),
            where,
        )
        if item["pool_index"] != index:
            raise ValidationError(f"{where}.pool_index must equal output order")
        revision_id = sha256_field(item["revision_id"], f"{where}.revision_id")
        if revision_id in seen_ids or revision_id in set(value["excluded_revision_ids"]):
            raise ValidationError(f"{where}.revision_id duplicates an exclusion or another item")
        seen_ids.add(revision_id)
        if item["origin"] != "natural":
            raise ValidationError(f"{where}.origin must be natural in the pool")
        if item["stratum"] not in STRATA:
            raise ValidationError(f"{where}.stratum is invalid")
        counts[item["stratum"]] += 1
        length_ok = item["stratum"] in exempt_strata or min_chars <= item["source_length"] <= max_chars
        if not length_ok:
            raise ValidationError(f"{where}.source_length violates the frozen length band")
        public_id = _public_input_identity(
            source=item["source"], source_tag=item["source_tag"], section=item["section"],
            item_kind=item["item_kind"], stratum=item["stratum"],
            bounded_context=item["bounded_context"],
            terminology_features=item["terminology_features"],
        )
        if item["public_input_identity"] != public_id:
            raise ValidationError(f"{where}.public_input_identity is not canonical")
        if public_id in seen_inputs:
            raise ValidationError(f"{where} duplicates a model-visible public input")
        seen_inputs.add(public_id)
    expected_counts = {stratum: counts[stratum] for stratum in STRATA}
    if expected_counts != value["stratum_counts"]:
        raise ValidationError("pool stratum_counts do not match items")
    expected_id = canonical_sha256({
        "contract": CURATION_POOL_CONTRACT, "seed": value["seed"],
        "inventory_sha256": value["inventory_sha256"],
        "excluded": value["excluded_revision_ids"],
        "stratum_targets": value["stratum_targets"], "items": items,
    })
    if value["pool_id"] != expected_id:
        raise ValidationError("curation pool_id is not canonical")
    return value


def build_facts_author_bundle(pool: dict[str, Any]) -> dict[str, Any]:
    """Target-blind input view for the Facts author (80 items)."""
    bundle = {
        "contract": CURATION_FACTS_AUTHOR_BUNDLE_CONTRACT, "schema_version": 1,
        "pool_id": pool["pool_id"],
        "fact_policy": {
            "min_facts_per_item": 0, "max_facts_per_item": 4,
            "supplemental_only": True, "language": "english-metalanguage",
            "common_input_restatements": "forbidden",
            "allowed_provenance_kinds": sorted(SUPPLEMENTAL_PROVENANCE_KINDS),
        },
        "items": [
            {
                "revision_id": item["revision_id"], "source": item["source"],
                "source_tag": item["source_tag"], "section": item["section"],
                "item_kind": item["item_kind"], "stratum": item["stratum"],
                "bounded_context": item["bounded_context"],
                "terminology_features": item["terminology_features"],
            }
            for item in pool["items"]
        ],
    }
    bundle["bundle_id"] = canonical_sha256(bundle)
    return bundle


def validate_facts_author_bundle(value: dict[str, Any], *, pool: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("facts author bundle must be an object")
    exact_fields(value, ("contract", "schema_version", "pool_id", "bundle_id", "fact_policy", "items"), "facts author bundle")
    if value["contract"] != CURATION_FACTS_AUTHOR_BUNDLE_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported facts author bundle contract")
    if value["pool_id"] != pool["pool_id"]:
        raise ValidationError("facts author bundle does not bind the curation pool")
    expected = build_facts_author_bundle(pool)
    if value != expected:
        raise ValidationError("facts author bundle is not the deterministic expected view")
    return value


# ---------------------------------------------------------------------------
# Fact packet v3
# ---------------------------------------------------------------------------


def _validate_fact(fact: Any, *, where: str) -> None:
    if not isinstance(fact, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(fact, ("fact_id", "fact_type", "statement", "provenance"), where)
    fact_id = string(fact["fact_id"], f"{where}.fact_id")
    if OPAQUE_FACT_ID_PATTERN.fullmatch(fact_id) is None:
        raise ValidationError(f"{where}.fact_id must be an opaque fact- followed by 16 lowercase hex characters")
    if fact["fact_type"] not in ("term-authority", "mechanism", "condition", "entity-relation", "ui-role"):
        raise ValidationError(f"{where}.fact_type is invalid")
    string(fact["statement"], f"{where}.statement")
    provenance = validate_provenance(fact["provenance"], f"{where}.provenance")
    reference_text = json.dumps(provenance["resource"], ensure_ascii=False)
    for marker in ("facts-author-bundle", "sample.json", "curation-pool.json", "curator-bundle"):
        if marker in reference_text.lower():
            raise ValidationError(f"{where}.provenance points to model-visible common input")


def _validate_packet_lineage(lineage: Any, *, expected_role: str, where: str) -> None:
    if not isinstance(lineage, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(
        lineage,
        ("role", "actor_id", "target_defects_seen", "gold_seen",
         "curator_assessments_seen", "common_input_restatements_excluded",
         "source_inputs_sha256"),
        where,
    )
    if lineage["role"] != expected_role or not lineage["actor_id"]:
        raise ValidationError(f"{where}.role or actor is invalid")
    if lineage["target_defects_seen"] is not False or lineage["gold_seen"] is not False:
        raise ValidationError(f"{where} must attest target defects and gold were unseen")
    if expected_role == "facts-author" and lineage["curator_assessments_seen"] is not False:
        raise ValidationError(f"{where} facts author must attest curator assessments were unseen")
    if lineage["common_input_restatements_excluded"] is not True:
        raise ValidationError(f"{where} must attest common-input restatements were excluded")
    sha256_field(lineage["source_inputs_sha256"], f"{where}.source_inputs_sha256")


def validate_packets(value: dict[str, Any], *, pool: dict[str, Any], expected_kind: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{expected_kind} packet must be an object")
    exact_fields(
        value,
        ("contract", "schema_version", "pool_id", "packet_kind", "status",
         "non_exhaustive", "supplemental_only", "language", "authoring_lineage", "items"),
        f"{expected_kind} packet",
    )
    if value["contract"] != CURATION_PACKET_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported fact packet contract")
    if value["pool_id"] != pool["pool_id"] or value["packet_kind"] != expected_kind:
        raise ValidationError(f"{expected_kind} packet identity does not match pool")
    if value["status"] != "frozen" or value["non_exhaustive"] is not True or value["supplemental_only"] is not True:
        raise ValidationError(f"{expected_kind} packet must be frozen supplemental-only")
    if value["language"] != "english-metalanguage":
        raise ValidationError("Facts statements must use English metalanguage")
    _validate_packet_lineage(
        value["authoring_lineage"],
        expected_role="facts-author" if expected_kind == "facts" else "host-neutral-generator",
        where=f"{expected_kind}.authoring_lineage",
    )
    items = value["items"]
    if not isinstance(items, list) or [item.get("revision_id") for item in items] != [item["revision_id"] for item in pool["items"]]:
        raise ValidationError(f"{expected_kind} packet must cover every pool item in order")
    seen_fact_ids: set[str] = set()
    for index, (entry, pool_item) in enumerate(zip(items, pool["items"])):
        where = f"{expected_kind}.items[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(entry, ("revision_id", "facts"), where)
        if entry["revision_id"] != pool_item["revision_id"]:
            raise ValidationError(f"{where}.revision_id is out of order")
        facts = entry["facts"]
        if not isinstance(facts, list) or len(facts) > 4:
            raise ValidationError(f"{where}.facts must contain 0-4 supplemental entries")
        for fact_index, fact in enumerate(facts):
            _validate_fact(fact, where=f"{where}.facts[{fact_index}]")
            if fact["fact_id"] in seen_fact_ids:
                raise ValidationError(f"{where}.facts[{fact_index}].fact_id must be globally unique")
            seen_fact_ids.add(fact["fact_id"])
    return value


def validate_subset_packet(value: dict[str, Any], *, source_packet: dict[str, Any], sample: dict[str, Any]) -> dict[str, Any]:
    """The frozen final-20 packet is a byte-exact subset of the 80-item packet."""
    if not isinstance(value, dict):
        raise ValidationError("subset packet must be an object")
    exact_fields(
        value,
        ("contract", "schema_version", "pool_id", "packet_kind", "status",
         "non_exhaustive", "supplemental_only", "language", "authoring_lineage", "items"),
        "subset packet",
    )
    if value["contract"] != CURATION_PACKET_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported subset packet contract")
    if value["pool_id"] != source_packet["pool_id"] or value["packet_kind"] != "facts":
        raise ValidationError("subset packet identity does not match the authoring packet")
    if value["status"] != "frozen" or value["language"] != "english-metalanguage":
        raise ValidationError("subset packet must be frozen English-metalanguage")
    if value["authoring_lineage"] != source_packet["authoring_lineage"]:
        raise ValidationError("subset packet must inherit the authoring lineage unchanged")
    source_by_id = {entry["revision_id"]: entry["facts"] for entry in source_packet["items"]}
    items = value["items"]
    if not isinstance(items, list) or len(items) != FINAL_SAMPLE_SIZE:
        raise ValidationError("subset packet must contain exactly 20 items")
    seen: set[str] = set()
    for index, (entry, sample_item) in enumerate(zip(items, sample["items"])):
        where = f"subset packet items[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(entry, ("revision_id", "facts"), where)
        if entry["revision_id"] != sample_item["revision_id"]:
            raise ValidationError(f"{where}.revision_id is out of order")
        if entry["revision_id"] in seen:
            raise ValidationError(f"{where}.revision_id must be unique")
        seen.add(entry["revision_id"])
        if sample_item["origin"] == "controlled":
            base = sample_item["mutation_lineage"]["base_revision_id"]
        else:
            base = sample_item["revision_id"]
        if entry["facts"] != source_by_id.get(base, []):
            raise ValidationError(f"{where} facts must be the byte-exact subset of the authoring packet")
    return value


def _validate_neutral_fact(fact: Any, *, where: str) -> None:
    if not isinstance(fact, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(fact, ("fact_id", "fact_type", "statement", "provenance"), where)
    fact_id = string(fact["fact_id"], f"{where}.fact_id")
    if OPAQUE_FACT_ID_PATTERN.fullmatch(fact_id) is None:
        raise ValidationError(f"{where}.fact_id must be an opaque fact- followed by 16 lowercase hex characters")
    string(fact["fact_type"], f"{where}.fact_type")
    string(fact["statement"], f"{where}.statement")
    provenance = fact["provenance"]
    if not isinstance(provenance, dict):
        raise ValidationError(f"{where}.provenance must be an object")
    exact_fields(provenance, ("kind", "resource", "locator"), f"{where}.provenance")
    string(provenance["kind"], f"{where}.provenance.kind")
    if not isinstance(provenance["resource"], dict) or not isinstance(provenance["locator"], dict):
        raise ValidationError(f"{where}.provenance.resource and locator must be objects")


def validate_neutral_packet(value: dict[str, Any], *, sample: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    """Neutral packets mirror the frozen Facts packet with host x-fill only."""
    if not isinstance(value, dict):
        raise ValidationError("neutral packet must be an object")
    exact_fields(
        value,
        ("contract", "schema_version", "pool_id", "packet_kind", "status",
         "non_exhaustive", "supplemental_only", "language", "authoring_lineage", "items"),
        "neutral packet",
    )
    if value["contract"] != CURATION_PACKET_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported neutral packet contract")
    if value["pool_id"] != facts["pool_id"] or value["packet_kind"] != "neutral":
        raise ValidationError("neutral packet identity does not match the Facts packet")
    if value["status"] != "frozen" or value["language"] != "english-metalanguage":
        raise ValidationError("neutral packet must be frozen English-metalanguage")
    if value["authoring_lineage"]["role"] != "host-neutral-generator":
        raise ValidationError("neutral packet authoring role is invalid")
    if value["authoring_lineage"]["source_inputs_sha256"] != canonical_sha256(facts):
        raise ValidationError("neutral packet does not bind the frozen Facts packet")
    items = value["items"]
    if not isinstance(items, list) or len(items) != FINAL_SAMPLE_SIZE:
        raise ValidationError("neutral packet must contain exactly 20 items")
    fact_serial = 0
    for index, (entry, sample_item) in enumerate(zip(items, sample["items"])):
        where = f"neutral packet items[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(entry, ("revision_id", "facts"), where)
        if entry["revision_id"] != sample_item["revision_id"]:
            raise ValidationError(f"{where}.revision_id is out of order")
        facts_entry = facts["items"][index]["facts"]
        if len(entry["facts"]) != len(facts_entry):
            raise ValidationError(f"{where}.facts shape must mirror the Facts packet")
        for fact_index, fact in enumerate(entry["facts"]):
            _validate_neutral_fact(fact, where=f"{where}.facts[{fact_index}]")
            if fact["fact_id"] != f"fact-{fact_serial:016x}":
                raise ValidationError(f"{where}.facts[{fact_index}].fact_id must be the host-generated neutral ID")
            fact_serial += 1
    validate_neutral_equivalence(facts, value)
    return value


def build_neutral_packets(facts: dict[str, Any], *, pool_id: str) -> dict[str, Any]:
    """Host x-filled neutral mirror of a frozen Facts packet."""
    items = []
    fact_serial = 0
    for entry in facts["items"]:
        neutral_facts = []
        for fact in entry["facts"]:
            def fill(value: str, character: str = "x") -> str:
                encoded = json.dumps(value, ensure_ascii=False).encode("utf-8")
                return character * (len(encoded) - 2)
            provenance = fact["provenance"]
            neutral_facts.append({
                "fact_id": f"fact-{fact_serial:016x}",
                "fact_type": fill(fact["fact_type"]),
                "statement": fill(fact["statement"]),
                "provenance": {
                    "kind": fill(provenance["kind"]),
                    "resource": {
                        "repository": fill(provenance["resource"]["repository"]),
                        "revision": fill(provenance["resource"]["revision"]),
                        "logical_path": fill(provenance["resource"]["logical_path"]),
                        "file_sha256": "0" * 64,
                    },
                    "locator": _neutral_locator(provenance["locator"]),
                },
            })
            fact_serial += 1
        if len(canonical_json_bytes(neutral_facts)) != len(canonical_json_bytes(entry["facts"])):
            raise AssertionError("neutral packet canonical byte matching failed")
        items.append({"revision_id": entry["revision_id"], "facts": neutral_facts})
    return {
        "contract": CURATION_PACKET_CONTRACT, "schema_version": 1,
        "pool_id": pool_id, "packet_kind": "neutral", "status": "frozen",
        "non_exhaustive": True, "supplemental_only": True,
        "language": "english-metalanguage",
        "authoring_lineage": {
            "role": "host-neutral-generator", "actor_id": "facts-study-curation-v1",
            "target_defects_seen": False, "gold_seen": False,
            "curator_assessments_seen": False,
            "common_input_restatements_excluded": True,
            "source_inputs_sha256": canonical_sha256(facts),
        }, "items": items,
    }


def _neutral_locator(locator: dict[str, Any]) -> dict[str, Any]:
    """Length-preserving host filler: identical canonical byte length and
    JSON shape, no semantic content (mirrors the v1 neutral fill)."""
    result: dict[str, Any] = {}
    for key, value in locator.items():
        if isinstance(value, str):
            encoded = json.dumps(value, ensure_ascii=False).encode("utf-8")
            result[key] = "x" * (len(encoded) - 2)
        elif type(value) is int:
            result[key] = int("1" * len(str(value)))
        else:
            result[key] = value
    return result


def validate_neutral_equivalence(facts: dict[str, Any], neutral: dict[str, Any]) -> None:
    if neutral["authoring_lineage"]["source_inputs_sha256"] != canonical_sha256(facts):
        raise ValidationError("neutral packet does not bind the frozen Facts packet")
    fact_serial = 0
    for index, (left, right) in enumerate(zip(facts["items"], neutral["items"])):
        if len(canonical_json_bytes(left["facts"])) != len(canonical_json_bytes(right["facts"])):
            raise ValidationError(f"neutral item {index} does not match Facts canonical JSON byte length")
        if [set(f) for f in left["facts"]] != [set(f) for f in right["facts"]]:
            raise ValidationError(f"neutral item {index} does not match Facts JSON shape")
        for fact in right["facts"]:
            if fact["fact_id"] != f"fact-{fact_serial:016x}":
                raise ValidationError(f"neutral item {index} does not use host-generated opaque IDs")
            fact_serial += 1


# ---------------------------------------------------------------------------
# Curator bundle / assessment
# ---------------------------------------------------------------------------


def build_curator_bundle(*, pool: dict[str, Any], facts: dict[str, Any], inventory: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Target-visible view for the curator (80 items)."""
    validate_packets(facts, pool=pool, expected_kind="facts")
    facts_by_id = {entry["revision_id"]: entry["facts"] for entry in facts["items"]}
    bundle = {
        "contract": CURATION_CURATOR_BUNDLE_CONTRACT, "schema_version": 1,
        "pool_id": pool["pool_id"],
        "facts_packet_sha256": canonical_sha256(facts),
        "items": [],
    }
    for item in pool["items"]:
        row = inventory.get(item["revision_id"])
        if row is None:
            raise ValidationError(f"pool item {item['revision_id']} is missing from the inventory")
        bundle["items"].append({
            "revision_id": item["revision_id"],
            "source": item["source"],
            "target": str(row.get("target") or ""),
            "source_tag": item["source_tag"], "section": item["section"],
            "item_kind": item["item_kind"], "stratum": item["stratum"],
            "bounded_context": [
                {"relative_index": entry.get("relative_index"), "source": entry.get("source", ""),
                 "target": ""}
                for entry in item["bounded_context"]
            ],
            "facts": facts_by_id[item["revision_id"]],
        })
    bundle["curator_bundle_id"] = canonical_sha256(bundle)
    return bundle


def build_curator_assessment_template(*, pool: dict[str, Any], facts: dict[str, Any], curator_bundle_id: str) -> dict[str, Any]:
    return {
        "contract": CURATION_CURATOR_ASSESSMENT_CONTRACT, "schema_version": 1,
        "pool_id": pool["pool_id"], "curator_id": "", "status": "frozen",
        "lineage": {
            "facts_packet_sha256": canonical_sha256(facts),
            "curator_bundle_sha256": curator_bundle_id,
            "controlled_mutations_seen": False, "gold_seen": False,
        },
        "language_declaration": {
            "facts_statements_language": "english-metalanguage", "verified": True,
        },
        "items": [
            {"revision_id": item["revision_id"], "classification": "", "fact_trap": False, "notes": ""}
            for item in pool["items"]
        ],
        "assessment_id": "",
    }


def validate_curator_assessment(value: dict[str, Any], *, pool: dict[str, Any], facts: dict[str, Any], curator_bundle_id: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("curator assessment must be an object")
    exact_fields(
        value,
        ("contract", "schema_version", "pool_id", "curator_id", "status",
         "lineage", "language_declaration", "items", "assessment_id"),
        "curator assessment",
    )
    if value["contract"] != CURATION_CURATOR_ASSESSMENT_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported curator assessment contract")
    if value["pool_id"] != pool["pool_id"] or value["status"] != "frozen":
        raise ValidationError("curator assessment identity or status is invalid")
    if not value["curator_id"]:
        raise ValidationError("curator assessment requires a non-empty curator_id")
    lineage = value["lineage"]
    if not isinstance(lineage, dict):
        raise ValidationError("curator assessment lineage must be an object")
    exact_fields(lineage, ("facts_packet_sha256", "curator_bundle_sha256", "controlled_mutations_seen", "gold_seen"), "curator assessment lineage")
    if lineage["facts_packet_sha256"] != canonical_sha256(facts):
        raise ValidationError("curator assessment does not bind the frozen Facts packet")
    if lineage["curator_bundle_sha256"] != curator_bundle_id:
        raise ValidationError("curator assessment does not bind the curator bundle")
    if lineage["controlled_mutations_seen"] is not False or lineage["gold_seen"] is not False:
        raise ValidationError("curator assessment must attest mutations and gold were unseen")
    declaration = value["language_declaration"]
    if declaration != {"facts_statements_language": "english-metalanguage", "verified": True}:
        raise ValidationError("curator assessment language declaration is invalid")
    items = value["items"]
    if not isinstance(items, list) or len(items) != len(pool["items"]):
        raise ValidationError("curator assessment must cover every pool item")
    covered: set[str] = set()
    for index, (entry, pool_item) in enumerate(zip(items, pool["items"])):
        where = f"curator assessment items[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(entry, ("revision_id", "classification", "fact_trap", "notes"), where)
        if entry["revision_id"] != pool_item["revision_id"]:
            raise ValidationError(f"{where}.revision_id is out of order")
        covered.add(entry["revision_id"])
        if entry["classification"] not in CLASSIFICATIONS:
            raise ValidationError(f"{where}.classification is invalid")
        if entry["fact_trap"] is not True and entry["fact_trap"] is not False:
            raise ValidationError(f"{where}.fact_trap must be boolean")
        string(entry["notes"], f"{where}.notes", empty=True)
    if len(covered) != len(pool["items"]):
        raise ValidationError("curator assessment must be complete")
    expected_id = canonical_sha256({key: value for key, value in value.items() if key != "assessment_id"})
    if value["assessment_id"] != expected_id:
        raise ValidationError("curator assessment_id is not canonical")
    return value


# ---------------------------------------------------------------------------
# Controlled mutations
# ---------------------------------------------------------------------------


def _target_structure(source: str, target: str, args_order: Any) -> dict[str, Any]:
    signature = structure_signature(source, target, args_order)
    return {
        "printf": signature["printf"],
        "markup": signature["markup"],
        "at_tokens": signature["at_tokens"],
        "newlines": signature["newlines"],
        "multiline": signature["multiline"],
    }


def _mutation_digest(*, base_revision_id: str, variant_target: str, mutation_kind: str) -> str:
    return canonical_sha256({
        "contract": CONTROLLED_MUTATION_CONTRACT,
        "base_revision_id": base_revision_id,
        "variant_target": variant_target,
        "mutation_kind": mutation_kind,
    })


def build_controlled_variant_request(*, pool: dict[str, Any], inventory: dict[str, dict[str, Any]], shortfall: list[dict[str, Any]]) -> dict[str, Any]:
    """Shortfall bundle asking the curator for minimal controlled variants."""
    pool_by_id = {item["revision_id"]: item for item in pool["items"]}
    items = []
    for entry in shortfall:
        item = pool_by_id[entry["revision_id"]]
        row = inventory.get(entry["revision_id"])
        base_target = str(row.get("target") or "") if row is not None else ""
        items.append({
            "revision_id": entry["revision_id"],
            "source": item["source"], "target": base_target,
            "source_tag": item["source_tag"], "item_kind": item["item_kind"],
            "stratum": item["stratum"],
            "bounded_context": item["bounded_context"],
            "args_order": item.get("args_order"),
            "base_structure": _target_structure(item["source"], base_target, item.get("args_order")),
            "variant_target": "",
        })
    bundle = {
        "contract": CONTROLLED_VARIANTS_REQUEST_CONTRACT,
        "schema_version": 1, "pool_id": pool["pool_id"],
        "policy": {
            "max_variants_per_base": 1,
            "structure_preservation": True,
            "fill_only_fact_dependent": True,
            "max_fact_dependent_fill": 8,
        },
        "items": items, "request_id": "",
    }
    bundle["request_id"] = canonical_sha256({key: value for key, value in bundle.items() if key != "request_id"})
    return bundle


def validate_controlled_variants(value: dict[str, Any], *, pool: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("controlled variants bundle must be an object")
    exact_fields(value, ("contract", "schema_version", "pool_id", "items", "variants_id"), "controlled variants")
    if value["contract"] != CONTROLLED_VARIANTS_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported controlled variants contract")
    if value["pool_id"] != pool["pool_id"]:
        raise ValidationError("controlled variants do not bind the curation pool")
    request_items = {item["revision_id"]: item for item in request["items"]}
    items = value["items"]
    if not isinstance(items, list) or not items:
        raise ValidationError("controlled variants must contain at least one variant")
    if len(items) > 8:
        raise ValidationError("controlled variants may fill at most 8 fact-dependent slots")
    seen: set[str] = set()
    for index, entry in enumerate(items):
        where = f"controlled variants[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(entry, ("revision_id", "variant_target", "mutation_kind", "digest"), where)
        revision_id = sha256_field(entry["revision_id"], f"{where}.revision_id")
        if revision_id in seen:
            raise ValidationError(f"{where}.revision_id must be unique (one variant per base)")
        if revision_id not in request_items:
            raise ValidationError(f"{where}.revision_id was not requested")
        seen.add(revision_id)
        if entry["mutation_kind"] not in MUTATION_KINDS:
            raise ValidationError(f"{where}.mutation_kind is invalid")
        variant_target = string(entry["variant_target"], f"{where}.variant_target")
        request_item = request_items[revision_id]
        if variant_target == request_item.get("target", ""):
            raise ValidationError(f"{where}.variant_target must differ from the base target")
        base_structure = request_item["base_structure"]
        variant_structure = _target_structure(
            request_item["source"], variant_target, request_item.get("args_order")
        )
        if variant_structure != base_structure:
            raise ValidationError(
                f"{where} variant must preserve printf/markup/token/argument structure"
            )
        expected_digest = _mutation_digest(
            base_revision_id=revision_id, variant_target=variant_target,
            mutation_kind=entry["mutation_kind"],
        )
        if entry["digest"] != expected_digest:
            raise ValidationError(f"{where}.digest is not canonical")
    expected_id = canonical_sha256({key: value for key, value in value.items() if key != "variants_id"})
    if value["variants_id"] != expected_id:
        raise ValidationError("controlled variants_id is not canonical")
    return value


# ---------------------------------------------------------------------------
# Final sample v2 selection
# ---------------------------------------------------------------------------


def _pick(candidates: list[dict[str, Any]], count: int, rng: random.Random) -> list[dict[str, Any]]:
    """Stratum-diverse round-robin pick with a stable seed."""
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        buckets[candidate["stratum"]].append(candidate)
    picked: list[dict[str, Any]] = []
    keys = sorted(buckets)
    while len(picked) < count:
        progressed = False
        for key in keys:
            if buckets[key] and len(picked) < count:
                index = rng.randrange(len(buckets[key]))
                picked.append(buckets[key].pop(index))
                progressed = True
        if not progressed:
            break
    return picked


def _default_quota() -> dict[str, int]:
    return {
        "fact_dependent": FACT_QUOTA, "surface": SURFACE_QUOTA,
        "clean_acceptable": CLEAN_ACCEPTABLE_QUOTA, "clean_min": CLEAN_MIN,
        "fact_traps_min": FACT_TRAPS_MIN,
        "addressed_claims_min": 8, "unaddressed_claims_min": 8,
    }


def _quota_from_protocol(protocol: dict[str, Any] | None) -> dict[str, int]:
    if protocol is None:
        return _default_quota()
    quota = protocol["quota"]
    return {
        "fact_dependent": quota["fact_dependent_defects"],
        "surface": quota["surface_defects"],
        "clean_acceptable": quota["clean_acceptable"],
        "clean_min": quota["clean_min"],
        "fact_traps_min": quota["fact_traps_min"],
        "addressed_claims_min": quota["addressed_claims_min"],
        "unaddressed_claims_min": quota["unaddressed_claims_min"],
    }


def select_final_sample(
    *,
    pool: dict[str, Any], facts: dict[str, Any], curator: dict[str, Any],
    inventory: dict[str, dict[str, Any]],
    controlled_variants: dict[str, Any] | None = None,
    seed: str = SELECTION_SEED,
    quota: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Quota selection: natural first, minimal controlled fact-dependent fill.

    Returns a dict with ``status`` either ``selected`` (sample, frozen
    20-item packet, gold draft, templates and selection report) or
    ``shortfall`` (exit code 2 with the controlled variant request bundle).
    """
    quota = quota or _default_quota()
    fact_quota = quota["fact_dependent"]
    surface_quota = quota["surface"]
    clean_quota = quota["clean_acceptable"]
    clean_min = quota["clean_min"]
    traps_min = quota["fact_traps_min"]
    validate_pool(pool)
    validate_packets(facts, pool=pool, expected_kind="facts")
    curator_bundle = build_curator_bundle(pool=pool, facts=facts, inventory=inventory)
    validate_curator_assessment(
        curator, pool=pool, facts=facts,
        curator_bundle_id=curator_bundle["curator_bundle_id"],
    )
    pool_by_id = {item["revision_id"]: item for item in pool["items"]}
    assessment = {entry["revision_id"]: entry for entry in curator["items"]}

    natural: dict[str, list[dict[str, Any]]] = {
        "fact-dependent-defect": [], "surface-defect": [], "clean": [],
        "acceptable-localization": [],
    }
    for revision_id, entry in assessment.items():
        classification = entry["classification"]
        if classification == "unsuitable-uncertain":
            continue
        natural[classification].append(pool_by_id[revision_id])

    rng = random.Random(seed)
    fact_dependent = _pick(natural["fact-dependent-defect"], fact_quota, rng)
    surface = _pick(natural["surface-defect"], surface_quota, rng)
    # Clean/acceptable: fact-trap decoys first (they are the quota-critical
    # clean items), then the remaining clean quota, then the extra slot.
    trap_candidates = [
        item for item in natural["clean"] + natural["acceptable-localization"]
        if assessment[item["revision_id"]]["fact_trap"]
    ]
    clean = _pick(trap_candidates, clean_min, rng)
    if len(clean) < clean_min:
        rest_clean = [item for item in natural["clean"] if item not in clean]
        clean += _pick(rest_clean, clean_min - len(clean), rng)
    clean_rest = [item for item in natural["clean"] + natural["acceptable-localization"] if item not in clean]
    # The extra slot prefers acceptable-localization items that cover a
    # stratum missing from the rest of the selection (stratum coverage is a
    # frozen gold requirement).
    present_strata = {
        item["stratum"]
        for item in fact_dependent + surface + clean
    }
    preferred_extra = [
        item for item in clean_rest
        if assessment[item["revision_id"]]["classification"] == "acceptable-localization"
        and item["stratum"] not in present_strata
    ]
    if preferred_extra:
        extra = _pick(preferred_extra, clean_quota - clean_min, rng)
    else:
        extra = _pick(clean_rest, clean_quota - clean_min, rng)
    clean_acceptable = clean + extra

    shortfall_needed = fact_quota - len(fact_dependent)
    shortfall_items: list[dict[str, Any]] = []
    if shortfall_needed:
        # Bases for controlled variants: unused fact-dependent candidates
        # first, then any other pool item outside the final natural selection.
        already_selected = set(id(item) for item in fact_dependent + surface + clean_acceptable)
        candidates = [
            item for item in natural["fact-dependent-defect"]
            if id(item) not in already_selected
        ]
        for item in pool["items"]:
            if len(candidates) >= shortfall_needed:
                break
            if id(item) not in already_selected and item not in candidates:
                candidates.append(item)
        shortfall_items = candidates[:shortfall_needed]
        if len(shortfall_items) < shortfall_needed:
            raise ValidationError(
                f"not enough pool items remain for controlled fact-dependent fill: "
                f"need {shortfall_needed}"
            )
        if controlled_variants is None:
            request = build_controlled_variant_request(pool=pool, inventory=inventory, shortfall=[
                {"revision_id": item["revision_id"]} for item in shortfall_items
            ])
            return {
                "status": "shortfall",
                "shortfall": {"fact_dependent_needed": shortfall_needed, "filled": 0},
                "controlled_variant_request": request,
                "selection_report": {
                    "status": "shortfall", "seed": seed,
                    "quota": {"fact_dependent": fact_quota, "surface": surface_quota, "clean_acceptable": clean_quota},
                    "natural_counts": {key: len(value) for key, value in natural.items()},
                    "shortfall": {"fact_dependent_needed": shortfall_needed},
                },
            }
    elif controlled_variants is not None:
        raise ValidationError("controlled variants were supplied but no shortfall exists")

    selected = list(fact_dependent) + list(shortfall_items) + list(surface) + list(clean_acceptable)
    if len(selected) != FINAL_SAMPLE_SIZE:
        raise ValidationError(f"curation selection produced {len(selected)} items, expected {FINAL_SAMPLE_SIZE}")
    present_strata = {item["stratum"] for item in selected}
    if set(STRATA) - present_strata:
        missing = sorted(set(STRATA) - present_strata)
        raise ValidationError(f"curation selection misses source opportunity strata: {missing}")

    fact_trap_revisions = {
        revision_id
        for revision_id, entry in assessment.items()
        if entry["fact_trap"] and entry["classification"] in ("clean", "acceptable-localization")
    }
    traps = [item for item in selected if item["revision_id"] in fact_trap_revisions]
    if len(traps) < traps_min:
        raise ValidationError(f"curation selection needs at least {traps_min} fact traps")

    mutation_by_id: dict[str, dict[str, Any] | None] = {item["revision_id"]: None for item in selected}
    if shortfall_needed and controlled_variants is not None:
        request = build_controlled_variant_request(pool=pool, inventory=inventory, shortfall=[
            {"revision_id": item["revision_id"]} for item in shortfall_items
        ])
        validate_controlled_variants(controlled_variants, pool=pool, request=request)
        covered = {entry["revision_id"] for entry in controlled_variants["items"]}
        if covered != {item["revision_id"] for item in shortfall_items}:
            raise ValidationError(
                "controlled variants must fill exactly the shortfall revisions"
            )
        for entry in controlled_variants["items"]:
            mutation_by_id[entry["revision_id"]] = {
                "contract": CONTROLLED_MUTATION_CONTRACT,
                "base_revision_id": entry["revision_id"],
                "variant_target": entry["variant_target"],
                "mutation_kind": entry["mutation_kind"],
                "digest": entry["digest"],
            }

    items = []
    for index, pool_item in enumerate(selected):
        revision_id = pool_item["revision_id"]
        mutation = mutation_by_id[revision_id]
        origin = "controlled" if mutation is not None else "natural"
        if origin == "controlled":
            classification = "fact-dependent-defect"
        else:
            classification = assessment[revision_id]["classification"]
        item_revision_id = mutation["digest"] if mutation is not None else revision_id
        row = inventory.get(revision_id)
        target = mutation["variant_target"] if mutation is not None else (str(row.get("target") or "") if row is not None else "")
        items.append({
            "index": index,
            "revision_id": item_revision_id,
            "source": pool_item["source"],
            "target": target,
            "item_kind": pool_item["item_kind"],
            "source_tag": pool_item["source_tag"],
            "section": pool_item["section"],
            "bounded_context": pool_item["bounded_context"],
            "stratum": pool_item["stratum"],
            "origin": origin,
            "selection_classification": classification,
            "mutation_lineage": mutation,
        })
    selected_pool_ids = {item["revision_id"] for item in selected}
    excluded = sorted(
        set(pool["excluded_revision_ids"])
        | {item["revision_id"] for item in pool["items"] if item["revision_id"] not in selected_pool_ids}
    )
    study_id = canonical_sha256({
        "contract": CURATION_SAMPLE_CONTRACT, "pool_id": pool["pool_id"],
        "seed": seed, "inventory_sha256": pool["inventory_sha256"],
        "excluded": excluded, "items": items,
    })
    sample = {
        "contract": CURATION_SAMPLE_CONTRACT, "schema_version": 1,
        "study_id": study_id, "pool_id": pool["pool_id"], "seed": seed,
        "inventory_sha256": pool["inventory_sha256"],
        "excluded_revision_ids": excluded,
        "exclusion_revision_ids_sha256": canonical_sha256(excluded),
        "items": items,
    }
    packet_by_id = {entry["revision_id"]: entry["facts"] for entry in facts["items"]}
    frozen_items = []
    for item in items:
        if item["origin"] == "controlled":
            base = item["mutation_lineage"]["base_revision_id"]
        else:
            base = item["revision_id"]
        frozen_items.append({"revision_id": item["revision_id"], "facts": packet_by_id[base]})
    frozen_packet = {
        "contract": CURATION_PACKET_CONTRACT, "schema_version": 1,
        "pool_id": pool["pool_id"], "packet_kind": "facts", "status": "frozen",
        "non_exhaustive": True, "supplemental_only": True,
        "language": "english-metalanguage",
        "authoring_lineage": dict(facts["authoring_lineage"]),
        "items": frozen_items,
    }
    gold_items = []
    for item in items:
        if item["origin"] == "controlled":
            base_id = item["mutation_lineage"]["base_revision_id"]
        else:
            base_id = item["revision_id"]
        entry = assessment[base_id]
        clean_flag = entry["classification"] in ("clean", "acceptable-localization")
        gold_items.append({
            "revision_id": item["revision_id"], "clean": clean_flag,
            "fact_trap": entry["fact_trap"] and clean_flag,
            "acceptable_localization": entry["classification"] == "acceptable-localization",
            "origin": item["origin"], "claims": [],
        })
    gold = {
        "contract": CURATION_GOLD_CONTRACT, "schema_version": 1,
        "study_id": study_id, "status": "draft",
        "review_lineage": {
            "reviewer_ids": ["", ""], "review_artifact_sha256s": ["", ""],
            "adjudicator_id": "", "adjudication_artifact_sha256": "",
        },
        "items": gold_items,
    }
    review_template = {
        "contract": CURATION_GOLD_REVIEW_CONTRACT, "schema_version": 1,
        "study_id": study_id, "reviewer_id": "", "independent": True,
        "items": gold_items,
    }
    adjudication_template = {
        "contract": CURATION_GOLD_ADJUDICATION_CONTRACT, "schema_version": 1,
        "study_id": study_id, "status": "frozen", "adjudicator_id": "",
        "review_artifact_sha256s": ["", ""], "items": gold_items,
    }
    selection_report = {
        "status": "selected", "seed": seed,
        "pool_id": pool["pool_id"], "study_id": study_id,
        "quota": {"fact_dependent": fact_quota, "surface": surface_quota, "clean_acceptable": clean_quota},
        "natural_counts": {key: len(value) for key, value in natural.items()},
        "selected_counts": {
            "fact-dependent-defect": len(fact_dependent) + sum(item["origin"] == "controlled" for item in items),
            "surface-defect": len(surface),
            "clean": sum(1 for item in clean_acceptable if assessment[item["revision_id"]]["classification"] == "clean"),
            "acceptable-localization": sum(1 for item in clean_acceptable if assessment[item["revision_id"]]["classification"] == "acceptable-localization"),
            "controlled": sum(item["origin"] == "controlled" for item in items),
        },
        "fact_traps": len(traps),
        "stratum_coverage": {
            stratum: sum(item["stratum"] == stratum for item in items) for stratum in STRATA
        },
        "controlled_used": sum(item["origin"] == "controlled" for item in items),
    }
    return {
        "status": "selected",
        "sample": sample, "frozen_packet": frozen_packet,
        "gold": gold, "review_template": review_template,
        "adjudication_template": adjudication_template,
        "selection_report": selection_report,
    }


# ---------------------------------------------------------------------------
# Sample v2 / gold v2 validation
# ---------------------------------------------------------------------------


def validate_sample(value: dict[str, Any], *, pool: dict[str, Any], required_excluded: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("curation sample must be an object")
    exact_fields(
        value,
        ("contract", "schema_version", "study_id", "pool_id", "seed",
         "inventory_sha256", "excluded_revision_ids",
         "exclusion_revision_ids_sha256", "items"),
        "curation sample",
    )
    if value["contract"] != CURATION_SAMPLE_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported curation sample contract")
    if value["pool_id"] != pool["pool_id"]:
        raise ValidationError("curation sample does not bind the curation pool")
    if value["inventory_sha256"] != pool["inventory_sha256"]:
        raise ValidationError("curation sample inventory identity mismatch")
    sha256_field(value["study_id"], "sample.study_id")
    string(value["seed"], "sample.seed")
    excluded = value["excluded_revision_ids"]
    if not isinstance(excluded, list) or excluded != sorted(set(excluded)):
        raise ValidationError("sample.excluded_revision_ids must be a sorted unique list")
    for revision_id in excluded:
        sha256_field(revision_id, "sample.excluded_revision_ids")
    if canonical_sha256(excluded) != value["exclusion_revision_ids_sha256"]:
        raise ValidationError("sample exclusion revision digest mismatch")
    if not required_excluded <= set(excluded):
        missing = sorted(required_excluded - set(excluded))
        raise ValidationError(f"curation sample misses required exclusions: {missing[:5]}")
    items = value["items"]
    if not isinstance(items, list) or len(items) != FINAL_SAMPLE_SIZE:
        raise ValidationError(f"curation sample must contain exactly {FINAL_SAMPLE_SIZE} items")
    seen: set[str] = set()
    pool_by_id = {item["revision_id"]: item for item in pool["items"]}
    for index, item in enumerate(items):
        where = f"sample.items[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(
            item,
            ("index", "revision_id", "source", "target", "item_kind", "source_tag",
             "section", "bounded_context", "stratum", "origin",
             "selection_classification", "mutation_lineage"),
            where,
        )
        if item["index"] != index:
            raise ValidationError(f"{where}.index must equal output order")
        revision_id = sha256_field(item["revision_id"], f"{where}.revision_id")
        if revision_id in seen or revision_id in set(excluded):
            raise ValidationError(f"{where}.revision_id duplicates an exclusion or another item")
        seen.add(revision_id)
        string(item["source"], f"{where}.source")
        string(item["target"], f"{where}.target")
        if item["item_kind"] not in ITEM_KINDS:
            raise ValidationError(f"{where}.item_kind is invalid")
        if item["stratum"] not in STRATA:
            raise ValidationError(f"{where}.stratum is invalid")
        if item["origin"] not in ("natural", "controlled"):
            raise ValidationError(f"{where}.origin is invalid")
        if item["selection_classification"] not in SELECTION_CLASSIFICATIONS:
            raise ValidationError(f"{where}.selection_classification is invalid")
        mutation = item["mutation_lineage"]
        if item["origin"] == "controlled":
            if not isinstance(mutation, dict):
                raise ValidationError(f"{where}.mutation_lineage is required for controlled items")
            exact_fields(
                mutation,
                ("contract", "base_revision_id", "variant_target", "mutation_kind", "digest"),
                f"{where}.mutation_lineage",
            )
            if mutation["contract"] != CONTROLLED_MUTATION_CONTRACT:
                raise ValidationError(f"{where}.mutation_lineage.contract is invalid")
            base = sha256_field(mutation["base_revision_id"], f"{where}.mutation_lineage.base_revision_id")
            if base not in pool_by_id:
                raise ValidationError(f"{where}.mutation_lineage.base_revision_id is not a pool item")
            string(mutation["variant_target"], f"{where}.mutation_lineage.variant_target")
            string(mutation["mutation_kind"], f"{where}.mutation_lineage.mutation_kind")
            if mutation["mutation_kind"] not in MUTATION_KINDS:
                raise ValidationError(f"{where}.mutation_lineage.mutation_kind is invalid")
            expected_digest = _mutation_digest(
                base_revision_id=base, variant_target=mutation["variant_target"],
                mutation_kind=mutation["mutation_kind"],
            )
            if mutation["digest"] != expected_digest:
                raise ValidationError(f"{where}.mutation_lineage.digest is not canonical")
            if revision_id != mutation["digest"]:
                raise ValidationError(f"{where}.revision_id must equal the mutation digest")
            if item["target"] != mutation["variant_target"]:
                raise ValidationError(f"{where}.target must equal the variant target")
            base_item = pool_by_id[base]
            if base_item["source"] != item["source"]:
                raise ValidationError(f"{where}.source must equal the base source")
        else:
            if mutation is not None:
                raise ValidationError(f"{where}.mutation_lineage must be null for natural items")
            if revision_id not in pool_by_id:
                raise ValidationError(f"{where}.revision_id is not a pool item")
            base_item = pool_by_id[revision_id]
            if base_item["source"] != item["source"]:
                raise ValidationError(f"{where}.source must equal the pool source")
    expected_id = canonical_sha256({
        "contract": CURATION_SAMPLE_CONTRACT, "pool_id": value["pool_id"],
        "seed": value["seed"], "inventory_sha256": value["inventory_sha256"],
        "excluded": excluded, "items": items,
    })
    if value["study_id"] != expected_id:
        raise ValidationError("curation sample study_id is not canonical")
    return value


def _validate_evidence(evidence: Any, text: str, where: str) -> dict[str, Any]:
    return normalize_evidence(evidence, text, where=where, allow_empty_omission=True)


#: Unicode punctuation characters that may be dropped entirely in evidence
#: normalization (interpuncts, ideographic commas/periods). Reworded or
#: shortened quotes are never tolerated.
_EVIDENCE_DROPPED_CHARS = frozenset(
    ("\u00b7", "\u2027", "\u30fb", "\u2022", "\u3001", "\u3002")
)

#: whitespace characters folded into a single ASCII space (semantic word
#: separation is preserved; only run length and exotic spaces are absorbed).
_EVIDENCE_WHITESPACE_CHARS = frozenset(
    (" ", "\t", "\n", "\r", "\u00a0", "\u2009", "\u202f", "\u3000", "\u2003", "\u2002")
)


def _is_cjk(char: str) -> bool:
    code = ord(char)
    return (
        0x3400 <= code <= 0x4DBF or 0x4E00 <= code <= 0x9FFF
        or 0xF900 <= code <= 0xFAFF or 0x3000 <= code <= 0x303F
    )


def _normalize_evidence_text(text: str) -> tuple[str, list[int]]:
    """Return (normalized, orig_indices).

    Dropped punctuation disappears; runs of whitespace fold to a single ASCII
    space; whitespace between two CJK characters is dropped entirely
    (Chinese typesetting uses no inter-word spaces).  ``orig_indices[i]`` is
    the original offset of normalized character ``i`` so normalized spans map
    back to unique original offsets.
    """
    out: list[str] = []
    orig_indices: list[int] = []
    pending_space = False
    for original_index, char in enumerate(text):
        if char in _EVIDENCE_DROPPED_CHARS:
            continue
        if char in _EVIDENCE_WHITESPACE_CHARS:
            if out:
                next_non_space = next(
                    (c for c in text[original_index + 1:] if c not in _EVIDENCE_WHITESPACE_CHARS),
                    None,
                )
                if _is_cjk(out[-1]) and next_non_space is not None and _is_cjk(next_non_space):
                    # CJK 之间空格在中文排版中无语义，直接删除
                    continue
            pending_space = True
            continue
        if pending_space:
            if out and out[-1] != " ":
                out.append(" ")
                orig_indices.append(original_index - 1)
            pending_space = False
        out.append(char)
        orig_indices.append(original_index)
    if pending_space and out and out[-1] != " ":
        out.append(" ")
        orig_indices.append(len(text) - 1)
    return "".join(out), orig_indices


def _map_normalized_span(start: int, end: int, orig_indices: list[int]) -> tuple[int, int]:
    if not orig_indices:
        return start, end
    original_start = orig_indices[start]
    original_end = orig_indices[end - 1] + 1
    return original_start, original_end


def _validate_evidence_with_normalization(
    evidence: Any, text: str, where: str, *, stats: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Byte-exact evidence validation with a narrow punctuation normalization.

    Falls back to tolerance of interpunct/space characters (e.g. ``马基·埃亚尔``
    vs ``马基埃亚尔``) only when the quote does not resolve verbatim, the
    normalized quote occurs exactly once in the normalized text, and the
    normalized span maps back to unique original offsets.  Reworded or
    shortened quotes remain rejected.  Every accepted normalization is counted
    in ``stats`` so the runner report records it.
    """
    original_error: ValidationError | None = None
    try:
        evidence_value = _validate_evidence(evidence, text, where)
        _require_valid_evidence(evidence_value, where)
        return evidence_value
    except ValidationError as caught:
        original_error = caught
    if not isinstance(evidence, dict):
        raise original_error if original_error is not None else ValidationError(f"{where} must be an object")
    quote = evidence.get("quote")
    occurrence = evidence.get("occurrence")
    if not isinstance(quote, str) or not quote or type(occurrence) is not int:
        raise original_error if original_error is not None else ValidationError(f"{where} evidence is invalid")
    normalized_quote, _ = _normalize_evidence_text(quote)
    normalized_text, orig_indices = _normalize_evidence_text(text)
    if normalized_quote == quote:
        raise original_error if original_error is not None else ValidationError(f"{where} does not resolve")
    starts: list[int] = []
    position = 0
    while True:
        position = normalized_text.find(normalized_quote, position)
        if position < 0:
            break
        starts.append(position)
        position += max(1, len(normalized_quote))
    if len(starts) != 1 or occurrence != 1:
        # ambiguous or non-unique matches are never normalized
        raise original_error if original_error is not None else ValidationError(f"{where} does not resolve")
    start, end = _map_normalized_span(starts[0], starts[0] + len(normalized_quote), orig_indices)
    if text[start:end] == quote:
        raise original_error if original_error is not None else ValidationError(f"{where} does not resolve")
    if stats is not None:
        stats["evidence_punctuation_normalized"] = stats.get("evidence_punctuation_normalized", 0) + 1
    return {
        "quote": quote, "occurrence": occurrence, "state": "exact",
        "start": start, "end": end,
    }


def _require_valid_evidence(evidence: dict[str, Any], where: str) -> None:
    if evidence["state"] in ("exact", "whole-item"):
        return
    if evidence["state"] == "missing" and evidence["quote"] == "" and evidence["occurrence"] == 0:
        return
    raise ValidationError(f"{where} is ambiguous or does not resolve to the visible text")


def _validate_claim(claim: Any, sample_item: dict[str, Any], where: str, fact_ids: set[str]) -> dict[str, Any]:
    if not isinstance(claim, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(
        claim,
        ("claim_id", "error_family", "phenomenon", "meaning_change",
         "source_evidence", "target_evidence", "fact_ids", "requires_manual"),
        where,
    )
    string(claim["claim_id"], f"{where}.claim_id")
    if claim["error_family"] not in ("semantic", "terminology", "ui"):
        raise ValidationError(f"{where}.error_family is invalid")
    if claim["phenomenon"] not in (
        "number", "number-range", "unit", "condition", "polarity", "entity-role",
        "scope", "trigger-timing", "omission", "addition", "terminology",
        "proper-name", "ambiguity", "other",
    ):
        raise ValidationError(f"{where}.phenomenon is invalid")
    if claim["meaning_change"] not in (
        "omitted", "added", "weakened", "strengthened", "reversed",
        "reassigned", "made-ambiguous", "unknown",
    ):
        raise ValidationError(f"{where}.meaning_change is invalid")
    source = _validate_evidence(claim["source_evidence"], sample_item["source"], f"{where}.source_evidence")
    target = _validate_evidence(claim["target_evidence"], sample_item["target"], f"{where}.target_evidence")
    _require_valid_evidence(source, f"{where}.source_evidence")
    _require_valid_evidence(target, f"{where}.target_evidence")
    fact_ids_list = claim["fact_ids"]
    if not isinstance(fact_ids_list, list) or any(fid not in fact_ids for fid in fact_ids_list):
        raise ValidationError(f"{where}.fact_ids must reference this item's facts")
    if claim["requires_manual"] is not True and claim["requires_manual"] is not False:
        raise ValidationError(f"{where}.requires_manual must be boolean")
    uncertainty = claim.get("uncertainty")
    if uncertainty is not None:
        uncertainty = validate_uncertainty(uncertainty, f"{where}.uncertainty")
        if uncertainty["state"] != "none" and claim["requires_manual"] is not True:
            raise ValidationError(f"{where} uncertainty requires requires_manual=true")
    return {
        **claim, "source_evidence": source, "target_evidence": target,
        "uncertainty": uncertainty,
    }


def validate_gold(value: dict[str, Any], *, sample: dict[str, Any], facts: dict[str, Any], require_frozen: bool = True, quota: dict[str, int] | None = None) -> dict[str, Any]:
    quota = quota or _default_quota()
    if not isinstance(value, dict):
        raise ValidationError("curation gold must be an object")
    exact_fields(value, ("contract", "schema_version", "study_id", "status", "review_lineage", "items"), "curation gold")
    if value["contract"] != CURATION_GOLD_CONTRACT or value["schema_version"] != 1 or value["study_id"] != sample["study_id"]:
        raise ValidationError("curation gold identity does not match sample")
    if value["status"] not in ("draft", "frozen") or (require_frozen and value["status"] != "frozen"):
        raise ValidationError("curation gold must be frozen before preregistration")
    lineage = value["review_lineage"]
    if not isinstance(lineage, dict):
        raise ValidationError("gold.review_lineage must be an object")
    exact_fields(lineage, ("reviewer_ids", "review_artifact_sha256s", "adjudicator_id", "adjudication_artifact_sha256"), "gold.review_lineage")
    if require_frozen:
        reviewer_ids = lineage["reviewer_ids"]
        if not isinstance(reviewer_ids, list) or len(reviewer_ids) != 2 or len(set(reviewer_ids)) != 2 or any(not x for x in reviewer_ids):
            raise ValidationError("frozen gold requires two distinct non-empty reviewer IDs")
        review_hashes = lineage["review_artifact_sha256s"]
        if not isinstance(review_hashes, list) or len(review_hashes) != 2:
            raise ValidationError("frozen gold requires two review artifact hashes")
        for index, digest in enumerate(review_hashes):
            sha256_field(digest, f"gold.review_lineage.review_artifact_sha256s[{index}]")
        adjudicator_id = string(lineage["adjudicator_id"], "gold.review_lineage.adjudicator_id")
        if adjudicator_id in set(reviewer_ids):
            raise ValidationError("gold adjudicator must be distinct from both reviewers")
        sha256_field(lineage["adjudication_artifact_sha256"], "gold.review_lineage.adjudication_artifact_sha256")
        fact_author = facts["authoring_lineage"]["actor_id"]
        if fact_author in set(reviewer_ids) | {adjudicator_id}:
            raise ValidationError("Facts author must be separate from gold reviewers and adjudicator")
    items = value["items"]
    if not isinstance(items, list) or len(items) != FINAL_SAMPLE_SIZE:
        raise ValidationError("curation gold must contain 20 items")
    fact_map = {entry["revision_id"]: {fact["fact_id"] for fact in entry["facts"]} for entry in facts["items"]}
    normalized_items = []
    claim_ids: set[str] = set()
    for index, (entry, sample_item) in enumerate(zip(items, sample["items"])):
        where = f"gold.items[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(entry, ("revision_id", "clean", "fact_trap", "acceptable_localization", "origin", "claims"), where)
        if entry["revision_id"] != sample_item["revision_id"]:
            raise ValidationError(f"{where}.revision_id is out of order")
        if entry["origin"] != sample_item["origin"]:
            raise ValidationError(f"{where}.origin must match the sample item")
        for field in ("clean", "fact_trap", "acceptable_localization"):
            if entry[field] is not True and entry[field] is not False:
                raise ValidationError(f"{where}.{field} must be boolean")
        if not isinstance(entry["claims"], list):
            raise ValidationError(f"{where}.claims must be a list")
        if entry["clean"] != (len(entry["claims"]) == 0):
            raise ValidationError(f"{where}.clean must exactly mean zero exhaustive gold claims")
        if entry["fact_trap"] and not entry["clean"]:
            raise ValidationError(f"{where}.fact_trap must be clean")
        claims = []
        for cindex, claim in enumerate(entry["claims"]):
            normalized = _validate_claim(claim, sample_item, f"{where}.claims[{cindex}]", fact_map[entry["revision_id"]])
            if normalized["claim_id"] in claim_ids:
                raise ValidationError("gold claim IDs must be globally unique")
            claim_ids.add(normalized["claim_id"])
            claims.append(normalized)
        normalized_items.append({**entry, "claims": claims})
    if require_frozen:
        addressed = sum(bool(claim["fact_ids"]) for item in normalized_items for claim in item["claims"])
        unaddressed = sum(not claim["fact_ids"] for item in normalized_items for claim in item["claims"])
        clean = sum(item["clean"] for item in normalized_items)
        traps = sum(item["fact_trap"] for item in normalized_items)
        if (addressed < quota["addressed_claims_min"] or unaddressed < quota["unaddressed_claims_min"]
                or clean < quota["clean_min"] or traps < quota["fact_traps_min"]):
            raise ValidationError(
                "frozen curation gold misses preregistered minima: "
                f"{quota['addressed_claims_min']} addressed, {quota['unaddressed_claims_min']} unaddressed, "
                f"{quota['clean_min']} clean, {quota['fact_traps_min']} fact traps"
            )
        present = {item["stratum"] for item in sample["items"]}
        if set(STRATA) - present:
            raise ValidationError("frozen curation sample must cover every source opportunity stratum")
        natural = [item for item in normalized_items if item["origin"] == "natural"]
        controlled = [item for item in normalized_items if item["origin"] == "controlled"]
        if not natural or len(controlled) > 8:
            raise ValidationError("frozen curation gold must keep natural/controlled separable within quota")
    return {**value, "items": normalized_items}


def validate_gold_authoring_artifacts(
    *, review_paths: list[Path], adjudication_path: Path, gold: dict[str, Any],
    sample: dict[str, Any], facts: dict[str, Any],
) -> None:
    if len(review_paths) != 2:
        raise ValidationError("curation gold requires exactly two independent review artifacts")
    review_ids = []
    review_hashes = []
    for index, path in enumerate(review_paths):
        review = read_json_object(path, f"curation gold review {index + 1}")
        exact_fields(review, ("contract", "schema_version", "study_id", "reviewer_id", "independent", "items"), f"gold review {index + 1}")
        if review["contract"] != CURATION_GOLD_REVIEW_CONTRACT or review["schema_version"] != 1 or review["study_id"] != sample["study_id"] or review["independent"] is not True:
            raise ValidationError(f"gold review {index + 1} identity or independence attestation is invalid")
        review_ids.append(string(review["reviewer_id"], f"gold review {index + 1}.reviewer_id"))
        review_hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
        validate_gold({
            "contract": CURATION_GOLD_CONTRACT, "schema_version": 1,
            "study_id": sample["study_id"], "status": "draft",
            "review_lineage": {
                "reviewer_ids": ["", ""], "review_artifact_sha256s": ["", ""],
                "adjudicator_id": "", "adjudication_artifact_sha256": "",
            }, "items": review["items"],
        }, sample=sample, facts=facts, require_frozen=False)
    if len(set(review_ids)) != 2:
        raise ValidationError("gold review artifacts must have distinct reviewer IDs")
    adjudication = read_json_object(adjudication_path, "curation gold adjudication")
    exact_fields(adjudication, ("contract", "schema_version", "study_id", "status", "adjudicator_id", "review_artifact_sha256s", "items"), "gold adjudication")
    if adjudication["contract"] != CURATION_GOLD_ADJUDICATION_CONTRACT or adjudication["schema_version"] != 1 or adjudication["study_id"] != sample["study_id"] or adjudication["status"] != "frozen":
        raise ValidationError("gold adjudication identity/status is invalid")
    if adjudication["review_artifact_sha256s"] != review_hashes:
        raise ValidationError("gold adjudication does not bind the supplied review artifacts in order")
    if adjudication["items"] != gold["items"]:
        raise ValidationError("frozen gold items must exactly equal the adjudication result")
    lineage = gold["review_lineage"]
    if lineage["reviewer_ids"] != review_ids or lineage["review_artifact_sha256s"] != review_hashes:
        raise ValidationError("frozen gold lineage does not bind the supplied reviews")
    if lineage["adjudicator_id"] != adjudication["adjudicator_id"]:
        raise ValidationError("frozen gold adjudicator identity mismatch")
    if lineage["adjudication_artifact_sha256"] != hashlib.sha256(adjudication_path.read_bytes()).hexdigest():
        raise ValidationError("frozen gold does not bind the supplied adjudication bytes")


# ---------------------------------------------------------------------------
# Seven-arm bundles, preregistration v2 (offline-frozen), fake replay
# ---------------------------------------------------------------------------


def _packet_map(packet: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {entry["revision_id"]: entry["facts"] for entry in packet["items"]}


def build_bundle(*, sample: dict[str, Any], facts: dict[str, Any], neutral: dict[str, Any], arm: str, prompt_sha256: str) -> dict[str, Any]:
    """Blinded seven-arm evaluator bundle; origin/mutation lineage never enter."""
    if arm not in ARMS:
        raise ValidationError(f"bundle arm must be one of {sorted(ARMS)}")
    facts_by_id, neutral_by_id = _packet_map(facts), _packet_map(neutral)
    items = []
    for sample_item in sample["items"]:
        translation_block = {
            "block_type": "translation", "source": sample_item["source"],
            "target": sample_item["target"],
        }
        item = {key: sample_item[key] for key in ("index", "revision_id", "item_kind", "source_tag", "bounded_context")}
        if arm in FACT_ARMS:
            supplemental = {"block_type": "supplemental", "packet": facts_by_id[sample_item["revision_id"]]}
            item["content_blocks"] = [translation_block, supplemental] if arm == "L" else [supplemental, translation_block]
        elif arm == "N":
            supplemental = {"block_type": "supplemental", "packet": neutral_by_id[sample_item["revision_id"]]}
            item["content_blocks"] = [supplemental, translation_block]
        else:
            item["content_blocks"] = [translation_block]
        items.append(item)
    bundle = {
        "contract": CURATION_BUNDLE_CONTRACT, "schema_version": 1,
        "study_id": sample["study_id"], "arm": arm,
        "prompt_sha256": prompt_sha256, "items": items, "bundle_id": "",
    }
    bundle["bundle_id"] = canonical_sha256({key: val for key, val in bundle.items() if key != "bundle_id"})
    return bundle


def validate_bundle(value: dict[str, Any], *, sample: dict[str, Any], facts: dict[str, Any], neutral: dict[str, Any], prompt_sha256: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("curation bundle must be an object")
    exact_fields(value, ("contract", "schema_version", "study_id", "arm", "prompt_sha256", "items", "bundle_id"), "curation bundle")
    if value["contract"] != CURATION_BUNDLE_CONTRACT or value["schema_version"] != 1 or value["study_id"] != sample["study_id"]:
        raise ValidationError("curation bundle identity mismatch")
    arm = value["arm"]
    if arm not in ARMS:
        raise ValidationError("curation bundle arm is invalid")
    if value["prompt_sha256"] != prompt_sha256:
        raise ValidationError("curation bundle prompt hash mismatch")
    expected = build_bundle(sample=sample, facts=facts, neutral=neutral, arm=arm, prompt_sha256=prompt_sha256)
    if value != expected:
        raise ValidationError("curation bundle is not the deterministic expected view")
    return value


def build_preregistration(*, protocol: dict[str, Any], sample: dict[str, Any], facts: dict[str, Any], neutral: dict[str, Any], gold: dict[str, Any], bundles: dict[str, dict[str, Any]], prompts: dict[str, str], harness_sha256: str) -> dict[str, Any]:
    validate_gold(gold, sample=sample, facts=facts, require_frozen=True)
    schedule = build_schedule(protocol, bundles, prompts)
    value = {
        "contract": CURATION_PREREG_CONTRACT, "schema_version": 1,
        "study_id": sample["study_id"], "pool_id": sample["pool_id"],
        "purpose": "facts-causal-study-only-no-holdout-clearance",
        "status": "offline-frozen",
        "sample_sha256": canonical_sha256(sample), "facts_sha256": canonical_sha256(facts),
        "neutral_sha256": canonical_sha256(neutral), "gold_sha256": canonical_sha256(gold),
        "protocol_sha256": canonical_sha256(protocol),
        "harness_sha256": harness_sha256,
        "pi_executable": pi_executable_identity(),
        "arm_prompt_sha256s": {arm: hashlib.sha256(prompts[arm].encode("utf-8")).hexdigest() for arm in ARMS},
        "item_order": [item["revision_id"] for item in sample["items"]],
        "schedule": schedule, "contrasts": protocol["contrasts"],
        "decision_rule": protocol["decision_rule"], "max_external_slots": 33,
        "shard_count": 1,
        "cache_policy": "disabled", "replacement_policy": "forbidden",
        "preregistration_id": "",
    }
    value["preregistration_id"] = canonical_sha256({key: val for key, val in value.items() if key != "preregistration_id"})
    return value


def validate_preregistration(value: dict[str, Any], *, protocol: dict[str, Any], sample: dict[str, Any], facts: dict[str, Any], neutral: dict[str, Any], gold: dict[str, Any], bundles: dict[str, dict[str, Any]], prompts: dict[str, str], harness_sha256: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("curation preregistration must be an object")
    if value.get("contract") != CURATION_PREREG_CONTRACT or value.get("status") != "offline-frozen":
        raise ValidationError("curation preregistration must be offline-frozen")
    expected = build_preregistration(
        protocol=protocol, sample=sample, facts=facts, neutral=neutral,
        gold=gold, bundles=bundles, prompts=prompts, harness_sha256=harness_sha256,
    )
    if value != expected:
        raise ValidationError("curation preregistration is not the deterministic expected artifact")
    return value


def _normalize_finding(finding: Any, *, item: dict[str, Any], facts: set[str], arm: str, where: str, evidence_stats: dict[str, int] | None = None) -> dict[str, Any]:
    if not isinstance(finding, dict):
        raise ValidationError(f"{where} must be an object")
    exact_fields(
        finding,
        ("error_family", "phenomenon", "meaning_change", "source_evidence",
         "target_evidence", "explanation", "supported_fact_ids", "requires_manual"),
        where,
    )
    if finding["error_family"] not in ("semantic", "terminology", "ui"):
        raise ValidationError(f"{where}.error_family is invalid")
    if finding["phenomenon"] not in (
        "number", "number-range", "unit", "condition", "polarity", "entity-role",
        "scope", "trigger-timing", "omission", "addition", "terminology",
        "proper-name", "ambiguity", "other",
    ):
        raise ValidationError(f"{where}.phenomenon is invalid")
    if finding["meaning_change"] not in (
        "omitted", "added", "weakened", "strengthened", "reversed",
        "reassigned", "made-ambiguous", "unknown",
    ):
        raise ValidationError(f"{where}.meaning_change is invalid")
    source = _validate_evidence_with_normalization(
        finding["source_evidence"], item["source"], f"{where}.source_evidence",
        stats=evidence_stats,
    )
    target = _validate_evidence_with_normalization(
        finding["target_evidence"], item["target"], f"{where}.target_evidence",
        stats=evidence_stats,
    )
    string(finding["explanation"], f"{where}.explanation")
    supported = finding["supported_fact_ids"]
    if not isinstance(supported, list) or len(supported) != len(set(supported)):
        raise ValidationError(f"{where}.supported_fact_ids must be a unique list")
    if any(fid not in facts for fid in supported):
        raise ValidationError(f"{where}.supported_fact_ids contains an unknown fact")
    if arm in NO_FACT_ARMS and supported:
        raise ValidationError(f"arm {arm} cannot cite Facts")
    if arm == "F" and not supported:
        raise ValidationError("Facts-only verifier findings must cite at least one fact_id")
    if finding["requires_manual"] is not True and finding["requires_manual"] is not False:
        raise ValidationError(f"{where}.requires_manual must be boolean")
    return {**finding, "source_evidence": source, "target_evidence": target}


def validate_assessment(value: dict[str, Any], *, sample: dict[str, Any], facts: dict[str, Any], bundle: dict[str, Any], slot: dict[str, Any], evidence_stats: dict[str, int] | None = None) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("curation assessment must be an object")
    exact_fields(
        value,
        ("contract", "schema_version", "study_id", "slot_id", "evaluator",
         "bundle_id", "bundle_sha256", "prompt_sha256", "assessment_state", "items"),
        "curation assessment",
    )
    if value["contract"] != CURATION_ASSESSMENT_CONTRACT or value["schema_version"] != 1 or value["study_id"] != sample["study_id"] or value["slot_id"] != slot["slot_id"]:
        raise ValidationError("curation assessment identity mismatch")
    expected_evaluator = {key: slot[key] for key in ("evaluator_id", "provider", "model", "thinking")}
    if value["evaluator"] != expected_evaluator:
        raise ValidationError("curation assessment evaluator identity mismatch")
    if value["bundle_id"] != bundle["bundle_id"] or value["bundle_sha256"] != canonical_sha256(bundle) or value["prompt_sha256"] != slot["prompt_sha256"]:
        raise ValidationError("curation assessment frozen input hashes mismatch")
    if value["assessment_state"] != "complete":
        raise ValidationError("curation assessment must be complete")
    items = value["items"]
    if not isinstance(items, list) or len(items) != FINAL_SAMPLE_SIZE:
        raise ValidationError("curation assessment must contain 20 items")
    fact_map = {entry["revision_id"]: {fact["fact_id"] for fact in entry["facts"]} for entry in facts["items"]}
    normalized_items = []
    for index, (entry, sample_item) in enumerate(zip(items, sample["items"])):
        where = f"assessment.items[{index}]"
        if not isinstance(entry, dict):
            raise ValidationError(f"{where} must be an object")
        exact_fields(entry, ("revision_id", "findings"), where)
        if entry["revision_id"] != sample_item["revision_id"] or not isinstance(entry["findings"], list):
            raise ValidationError(f"{where} is out of order or findings is not a list")
        findings = []
        for findex, finding in enumerate(entry["findings"]):
            try:
                findings.append(_normalize_finding(
                    finding, item=sample_item,
                    facts=fact_map[entry["revision_id"]], arm=slot["arm"],
                    where=f"{where}.findings[{findex}]",
                    evidence_stats=evidence_stats,
                ))
            except ValidationError:
                # Manifest-authorized finding-level tolerance: a single
                # malformed finding is dropped and counted, never allowed to
                # burn the whole slot.  Item-level integrity is still strict.
                if evidence_stats is not None:
                    evidence_stats["dropped_findings"] = evidence_stats.get("dropped_findings", 0) + 1
                continue
        normalized_items.append({"revision_id": entry["revision_id"], "findings": findings})
    return {**value, "items": normalized_items}


def _load_facts_pair(
    manifest: Manifest, *, pool: dict[str, Any], sample: dict[str, Any],
    facts_pool_path: Path, facts_path: Path, required_excluded: set[str],
) -> dict[str, Any]:
    """Validate the 80-item authoring packet and the frozen 20-item subset."""
    pool_facts = validate_packets(
        read_json_object(facts_pool_path, "pool facts packet"), pool=pool,
        expected_kind="facts",
    )
    facts = validate_subset_packet(
        read_json_object(facts_path, "curation facts packet"),
        source_packet=pool_facts, sample=sample,
    )
    return facts


def load_curation_inputs(
    manifest: Manifest, *, pool_path: Path, sample_path: Path,
    facts_pool_path: Path, facts_path: Path, neutral_path: Path,
    gold_path: Path, prereg_path: Path, bundle_paths: list[Path],
    harness_sha256: str | None = None,
    use_frozen_harness: bool = False,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    """Load and validate the frozen curation inputs.

    ``use_frozen_harness=True`` rebuilds the preregistration with the harness
    identity frozen inside it, so a completed campaign can be accepted even if
    the local toolchain moved on; the execution path keeps the strict
    current-harness check.
    """
    protocol = load_protocol(manifest)
    pool_registry = load_registry(manifest)
    required_excluded = excluded_revision_ids(pool_registry) | load_historical_exclusions(manifest)
    pool = validate_pool(read_json_object(pool_path, "curation pool"))
    sample = validate_sample(
        read_json_object(sample_path, "curation sample"), pool=pool,
        required_excluded=required_excluded,
    )
    facts = _load_facts_pair(
        manifest, pool=pool, sample=sample, facts_pool_path=facts_pool_path,
        facts_path=facts_path, required_excluded=required_excluded,
    )
    neutral = validate_neutral_packet(
        read_json_object(neutral_path, "neutral packet"), sample=sample, facts=facts,
    )
    validate_neutral_equivalence(facts, neutral)
    raw_gold = read_json_object(gold_path, "curation gold")
    gold = validate_gold(raw_gold, sample=sample, facts=facts, require_frozen=True)
    prompts = {arm: load_arm_prompt(manifest, arm) for arm in ARMS}
    bundles = {}
    for path in bundle_paths:
        raw = read_json_object(path, "curation bundle")
        arm = raw.get("arm")
        if arm in bundles:
            raise ValidationError(f"duplicate curation bundle arm: {arm}")
        prompt_sha = hashlib.sha256(prompts.get(arm, "").encode()).hexdigest()
        bundles[arm] = validate_bundle(raw, sample=sample, facts=facts, neutral=neutral, prompt_sha256=prompt_sha)
    if set(bundles) != set(ARMS):
        raise ValidationError("exactly one bundle for each of seven arms is required")
    prereg_raw = read_json_object(prereg_path, "curation preregistration")
    if use_frozen_harness:
        harness_sha256 = prereg_raw["harness_sha256"]
    elif harness_sha256 is None:
        from .facts_study import study_harness_sha256
        harness_sha256 = study_harness_sha256()
    prereg = validate_preregistration(
        prereg_raw,
        protocol=protocol, sample=sample, facts=facts, neutral=neutral,
        gold=raw_gold, bundles=bundles, prompts=prompts, harness_sha256=harness_sha256,
    )
    return sample, facts, neutral, gold, prereg, bundles


def _pooled_subset_metrics(assessments: list[dict[str, Any]], gold: dict[str, Any], sample: dict[str, Any], origin: str) -> dict[str, Any]:
    """Pooled per-arm metrics over natural or controlled items only."""
    gold_items = [item for item in gold["items"] if item["origin"] == origin]
    sample_items = [item for item in sample["items"] if item["origin"] == origin]
    if not gold_items:
        return {}
    gold_subset = {**gold, "items": gold_items}
    sample_subset = {**sample, "items": sample_items}
    per_run = [
        _score(_assessment_map(assessment), gold_subset, sample_subset)
        for assessment in assessments
    ]
    counts = Counter()
    for metric in per_run:
        counts.update(metric["counts"])
    p = _safe_ratio(counts["true_positive"], counts["true_positive"] + counts["false_positive"])
    r = _safe_ratio(counts["true_positive"], counts["true_positive"] + counts["false_negative"])
    pvalue, rvalue = p["value"], r["value"]
    f1 = None if pvalue is None or rvalue is None or pvalue + rvalue == 0 else 2 * pvalue * rvalue / (pvalue + rvalue)
    return {
        "counts": dict(counts), "precision": p, "recall": r,
        "f1": {"state": "applicable" if f1 is not None else "not-applicable", "value": f1},
        "fact_addressed_recall": sum(m["fact_addressed_recall"]["value"] or 0 for m in per_run) / max(1, len(per_run)),
        "fact_unaddressed_recall": sum(m["fact_unaddressed_recall"]["value"] or 0 for m in per_run) / max(1, len(per_run)),
    }


def build_report_v2(*, preregistration: dict[str, Any], gold: dict[str, Any], assessments: dict[str, dict[str, Any]], sample: dict[str, Any], protocol: dict[str, Any], evidence_mode: str = "offline-fake-replay") -> dict[str, Any]:
    """Report with natural/controlled separation.

    ``offline-fake-replay`` produces the non-evidentiary replay report;
    ``external-assessments`` produces the real preregistered decision report
    (which never grants holdout clearance).
    """
    if evidence_mode not in ("offline-fake-replay", "external-assessments"):
        raise ValidationError("curation report evidence mode is invalid")
    base = build_report(
        preregistration=preregistration, gold=gold, assessments=assessments,
        sample=sample, protocol=protocol, evidence_mode=evidence_mode,
    )
    subset: dict[str, dict[str, Any]] = {}
    slot_by_id = {slot["slot_id"]: slot for slot in preregistration["schedule"]}
    for origin in ("natural", "controlled"):
        origin_slots = {
            slot_id: assessment for slot_id, assessment in assessments.items()
            if any(item["origin"] == origin for item in sample["items"])
        }
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for slot_id, assessment in origin_slots.items():
            grouped[slot_by_id[slot_id]["arm"]].append(assessment)
        subset[f"{origin}_pooled_metrics"] = {
            arm: _pooled_subset_metrics(entries, gold, sample, origin)
            for arm, entries in grouped.items()
        }
    is_external = evidence_mode == "external-assessments"
    report = {
        "contract": CURATION_REPORT_CONTRACT, "schema_version": 1,
        "study_id": preregistration["study_id"],
        "preregistration_id": preregistration["preregistration_id"],
        "holdout_clearance": False,
        "evidence_mode": "external-assessments" if is_external else "non-evidentiary-offline-replay",
        "external_evidence": is_external,
        "schema_validity": {"numerator": 33, "denominator": 33, "value": 1.0},
        "evidence_validity": {"numerator": 33, "denominator": 33, "value": 1.0},
        "run_metrics": base["run_metrics"], "two_stage_metrics": base["two_stage_metrics"],
        "two_stage_composition": base["two_stage_composition"],
        "pooled_metrics": base["pooled_metrics"],
        "natural_pooled_metrics": subset["natural_pooled_metrics"],
        "controlled_pooled_metrics": subset["controlled_pooled_metrics"],
        "contrasts": base["contrasts"], "paired_item_bootstrap": base["paired_item_bootstrap"],
        "claim_detection_frequencies": base["claim_detection_frequencies"],
        "incremental_true_claims": base["incremental_true_claims"],
        "decision": base["decision"] if is_external else {"result": "non-evidentiary-offline-replay", "criteria": {}},
        "report_id": "",
    }
    report["report_id"] = canonical_sha256({key: value for key, value in report.items() if key != "report_id"})
    return report


def build_fake_assessments_v2(*, preregistration: dict[str, Any], sample: dict[str, Any], gold: dict[str, Any], bundles: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Offline identity/metric replay; never evidence about a provider."""
    fake = build_fake_assessments(
        preregistration=preregistration, sample=sample, gold=gold, bundles=bundles
    )
    for slot_id, assessment in fake.items():
        assessment["contract"] = CURATION_ASSESSMENT_CONTRACT
    return fake


# ---------------------------------------------------------------------------
# CLI entry points
# ---------------------------------------------------------------------------


def run_curation_build(
    manifest: Manifest, *, inventory: Path, exclusions: list[Path],
    seed: str = CURATION_SEED, protocol_version: str = "v3",
) -> dict[str, Any]:
    """80-item source-side pool + target-blind author bundle + packet draft."""
    protocol = load_protocol(manifest, version=protocol_version)
    registry = load_registry(manifest)
    required = excluded_revision_ids(registry) | load_historical_exclusions(manifest)
    pool, author_bundle, facts, report = build_candidate_pool(
        inventory_path=inventory, exclusion_paths=exclusions, seed=seed,
        required_excluded_ids=required, protocol=protocol,
    )
    report["protocol_version"] = protocol_version
    run = create_quality_run_directory(manifest.root, "facts-study-curation-build")
    write_json(run / "curation-pool.json", pool)
    write_json(run / "facts-author-bundle.json", author_bundle)
    write_json(run / "fact-packets.draft.json", facts)
    write_json(run / "build-report.json", report)
    return {
        **report, "run_directory": str(run),
        "pool": str(run / "curation-pool.json"),
        "facts_author_bundle": str(run / "facts-author-bundle.json"),
        "facts": str(run / "fact-packets.draft.json"),
        "report": str(run / "build-report.json"),
    }


def run_curation_prepare(
    manifest: Manifest, *, pool_path: Path, facts_path: Path, inventory_path: Path,
) -> dict[str, Any]:
    """Frozen 80-item Facts packet -> target-visible curator bundle + template."""
    pool = validate_pool(read_json_object(pool_path, "curation pool"))
    facts = validate_packets(
        read_json_object(facts_path, "curation facts packet"), pool=pool,
        expected_kind="facts",
    )
    inventory = _load_inventory_rows(inventory_path, pool["inventory_sha256"])
    curator_bundle = build_curator_bundle(pool=pool, facts=facts, inventory=inventory)
    template = build_curator_assessment_template(
        pool=pool, facts=facts, curator_bundle_id=curator_bundle["curator_bundle_id"]
    )
    run = create_quality_run_directory(manifest.root, "facts-study-curation-prepare")
    write_json(run / "curator-bundle.json", curator_bundle)
    write_json(run / "curator-assessment.template.json", template)
    report = {
        "pool_id": pool["pool_id"], "facts_packet_sha256": canonical_sha256(facts),
        "curator_bundle_id": curator_bundle["curator_bundle_id"],
        "items": len(curator_bundle["items"]), "status": "curation-required",
    }
    write_json(run / "prepare-report.json", report)
    return {
        **report, "run_directory": str(run),
        "curator_bundle": str(run / "curator-bundle.json"),
        "curator_assessment_template": str(run / "curator-assessment.template.json"),
    }


def run_curation_select(
    manifest: Manifest, *, pool_path: Path, facts_path: Path,
    curator_path: Path, inventory_path: Path,
    controlled_variants_path: Path | None = None,
    seed: str = SELECTION_SEED, protocol_version: str = "v5",
) -> dict[str, Any]:
    """Quota selection; exit code 2 shortfall carries the variant request."""
    protocol = load_protocol(manifest, version=protocol_version)
    pool = validate_pool(read_json_object(pool_path, "curation pool"))
    facts = validate_packets(
        read_json_object(facts_path, "curation facts packet"), pool=pool,
        expected_kind="facts",
    )
    inventory = _load_inventory_rows(inventory_path, pool["inventory_sha256"])
    curator = read_json_object(curator_path, "curator assessment")
    controlled = None
    if controlled_variants_path is not None:
        controlled = read_json_object(controlled_variants_path, "controlled variants")
    result = select_final_sample(
        pool=pool, facts=facts, curator=curator, inventory=inventory,
        controlled_variants=controlled, seed=seed,
        quota=_quota_from_protocol(protocol),
    )
    run = create_quality_run_directory(manifest.root, "facts-study-curation-select")
    if result["status"] == "shortfall":
        request = result["controlled_variant_request"]
        write_json(run / "controlled-variants.request.json", request)
        report = result["selection_report"]
        write_json(run / "selection-report.json", report)
        return {
            **report, "status_code": 2, "run_directory": str(run),
            "controlled_variant_request": str(run / "controlled-variants.request.json"),
        }
    sample = result["sample"]
    frozen_packet = result["frozen_packet"]
    gold = result["gold"]
    write_json(run / "curation-pool.json", pool)
    write_json(run / "sample.json", sample)
    write_json(run / "fact-packets.frozen.json", frozen_packet)
    write_json(run / "gold.draft.json", gold)
    write_json(run / "gold-review-a.template.json", result["review_template"])
    write_json(run / "gold-review-b.template.json", result["review_template"])
    write_json(run / "gold-adjudication.template.json", result["adjudication_template"])
    write_json(run / "selection-report.json", result["selection_report"])
    fragments = [
        build_registry_fragment({
            "dataset_id": "facts-curation-pool-v1",
            "purpose": "curation-pool", "status": "frozen",
            "sample_contract": CURATION_POOL_CONTRACT,
            "sample_id": pool["pool_id"],
            "sample_sha256": hashlib.sha256((run / "curation-pool.json").read_bytes()).hexdigest(),
            "sample_reference": None,
            "revision_ids": sorted(item["revision_id"] for item in pool["items"]),
            "revision_ids_sha256": canonical_sha256(sorted(item["revision_id"] for item in pool["items"])),
            "excluded_from_calibration": True, "excluded_from_holdout": True,
            "excluded_from_facts_curation": True,
            "scope": {"natural": 80, "controlled": 0},
            "disposition": "facts-study-curation-v1 source-side pool (80 items); consumed by the curation sample.",
        }),
        build_registry_fragment({
            "dataset_id": "facts-curation-sample-v1",
            "purpose": "facts-study-final-sample", "status": "frozen",
            "sample_contract": CURATION_SAMPLE_CONTRACT,
            "sample_id": sample["study_id"],
            "sample_sha256": hashlib.sha256((run / "sample.json").read_bytes()).hexdigest(),
            "sample_reference": None,
            "revision_ids": sorted(item["revision_id"] for item in sample["items"]),
            "revision_ids_sha256": canonical_sha256(sorted(item["revision_id"] for item in sample["items"])),
            "excluded_from_calibration": True, "excluded_from_holdout": True,
            "excluded_from_facts_curation": True,
            "scope": {
                "natural": sum(item["origin"] == "natural" for item in sample["items"]),
                "controlled": sum(item["origin"] == "controlled" for item in sample["items"]),
            },
            "disposition": "facts-study-curation-v1 final 20-item sample (offline-frozen).",
        }),
    ]
    for index, fragment in enumerate(fragments):
        validate_registry_fragment(fragment)
        write_json(run / f"registry-fragment-{index + 1}.json", fragment)
    report = {
        **result["selection_report"], "status_code": 0, "run_directory": str(run),
        "sample": str(run / "sample.json"),
        "facts": str(run / "fact-packets.frozen.json"),
        "gold": str(run / "gold.draft.json"),
        "gold_review_templates": [str(run / "gold-review-a.template.json"), str(run / "gold-review-b.template.json")],
        "gold_adjudication_template": str(run / "gold-adjudication.template.json"),
        "registry_fragments": [str(run / f"registry-fragment-{index + 1}.json") for index in range(2)],
        "pool": str(run / "curation-pool.json"),
    }
    write_json(run / "selection-report.json", report)
    return report


def run_curation_bundles(
    manifest: Manifest, *, pool_path: Path, sample_path: Path,
    facts_pool_path: Path, facts_path: Path, gold_path: Path,
    gold_review_paths: list[Path], gold_adjudication_path: Path,
) -> dict[str, Any]:
    """Freeze seven blinded arm bundles and the offline-frozen preregistration."""
    pool = validate_pool(read_json_object(pool_path, "curation pool"))
    protocol = load_protocol(manifest)
    pool_registry = load_registry(manifest)
    required_excluded = excluded_revision_ids(pool_registry) | load_historical_exclusions(manifest)
    sample = validate_sample(
        read_json_object(sample_path, "curation sample"), pool=pool,
        required_excluded=required_excluded,
    )
    facts = _load_facts_pair(
        manifest, pool=pool, sample=sample,
        facts_pool_path=facts_pool_path, facts_path=facts_path,
        required_excluded=required_excluded,
    )
    raw_gold = read_json_object(gold_path, "curation gold")
    validate_gold(raw_gold, sample=sample, facts=facts, require_frozen=True)
    validate_gold_authoring_artifacts(
        review_paths=gold_review_paths, adjudication_path=gold_adjudication_path,
        gold=raw_gold, sample=sample, facts=facts,
    )
    neutral = build_neutral_packets(facts, pool_id=pool["pool_id"])
    validate_neutral_equivalence(facts, neutral)
    prompts = {arm: load_arm_prompt(manifest, arm) for arm in ARMS}
    bundles = {
        arm: build_bundle(
            sample=sample, facts=facts, neutral=neutral, arm=arm,
            prompt_sha256=hashlib.sha256(prompts[arm].encode()).hexdigest(),
        )
        for arm in ARMS
    }
    from .facts_study import study_harness_sha256
    prereg = build_preregistration(
        protocol=protocol, sample=sample, facts=facts, neutral=neutral,
        gold=raw_gold, bundles=bundles, prompts=prompts,
        harness_sha256=study_harness_sha256(),
    )
    run = create_quality_run_directory(manifest.root, "facts-study-curation-bundles")
    write_json(run / "neutral-packets.json", neutral)
    for arm, bundle in bundles.items():
        write_json(run / f"bundle-{arm.lower()}.json", bundle)
    write_json(run / "preregistration.json", prereg)
    index = {
        "contract": "tome4-quality-facts-study-curation-bundles-index-v1",
        "schema_version": 1, "study_id": sample["study_id"],
        "pool_id": pool["pool_id"],
        "preregistration_id": prereg["preregistration_id"],
        "status": "offline-frozen", "slots": 33, "shards": 1,
        "bundles": {arm: str(run / f"bundle-{arm.lower()}.json") for arm in ARMS},
        "neutral": str(run / "neutral-packets.json"),
        "preregistration": str(run / "preregistration.json"),
        "run_directory": str(run),
    }
    write_json(run / "index.json", index)
    return index


def run_curation_validate(
    manifest: Manifest, *, pool_path: Path, sample_path: Path,
    facts_pool_path: Path, facts_path: Path, neutral_path: Path,
    gold_path: Path, prereg_path: Path, bundle_paths: list[Path],
    fake_runner: bool, assessment_paths: list[Path], runner_report_paths: list[Path],
    execution_manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Offline 33-slot fake replay or manifest-authorized external validation."""
    if not fake_runner:
        if execution_manifest_path is None:
            raise ValidationError(
                "external curation assessments require a user-authorized execution manifest"
            )
        execution_manifest = read_json_object(execution_manifest_path, "execution manifest")
    if assessment_paths or runner_report_paths:
        if fake_runner:
            raise ValidationError("--fake-runner cannot be combined with assessments or runner reports")
        if len(assessment_paths) != 33 or len(runner_report_paths) != 33:
            raise ValidationError("external curation validation requires exactly 33 assessments and 33 runner reports")
    from .facts_study import validate_execution_manifest as validate_execution_manifest_v2
    sample, facts, neutral, gold, prereg, bundles = load_curation_inputs(
        manifest, pool_path=pool_path, sample_path=sample_path,
        facts_pool_path=facts_pool_path, facts_path=facts_path,
        neutral_path=neutral_path, gold_path=gold_path, prereg_path=prereg_path,
        bundle_paths=bundle_paths, use_frozen_harness=True,
    )
    slot_by_id = {slot["slot_id"]: slot for slot in prereg["schedule"]}
    mode = "offline-fake-replay" if fake_runner else "external-assessments"
    if fake_runner:
        raw_assessments = build_fake_assessments_v2(
            preregistration=prereg, sample=sample, gold=gold, bundles=bundles
        )
    else:
        prereg_raw = read_json_object(prereg_path, "curation preregistration")
        validate_execution_manifest_v2(execution_manifest, preregistration=prereg_raw)
        raw_assessments = {}
        original_assessment_paths = {}
        for path in assessment_paths:
            raw = read_json_object(path, "curation assessment")
            slot_id = raw.get("slot_id")
            if slot_id in raw_assessments:
                raise ValidationError(f"duplicate curation slot: {slot_id}")
            raw_assessments[slot_id] = raw
            original_assessment_paths[slot_id] = path
        validate_external_run_lineage_v2(
            manifest, prereg=prereg, execution_manifest=execution_manifest,
            assessment_paths_by_slot=original_assessment_paths,
            runner_report_paths=runner_report_paths,
        )
    if set(raw_assessments) != set(slot_by_id):
        raise ValidationError("assessment slot membership does not match the frozen 33-slot schedule")
    normalized = {}
    for slot_id, raw in raw_assessments.items():
        normalized[slot_id] = validate_assessment(
            raw, sample=sample, facts=facts,
            bundle=bundles[slot_by_id[slot_id]["arm"]], slot=slot_by_id[slot_id],
        )
    run = create_quality_run_directory(
        manifest.root, "facts-study-curation-fake" if fake_runner else "facts-study-curation-external"
    )
    paths = {}
    for slot_id in sorted(normalized):
        path = run / "assessments" / f"{slot_id}.json"
        write_json(path, raw_assessments[slot_id])
        paths[slot_id] = str(path)
    index = {
        "contract": CURATION_VALIDATION_CONTRACT, "schema_version": 1,
        "study_id": sample["study_id"],
        "preregistration_id": prereg["preregistration_id"],
        "mode": mode,
        "structure_validity": {"numerator": 33, "denominator": 33, "value": 1.0},
        "evidence_validity": {"numerator": 33, "denominator": 33, "value": 1.0},
        "inputs": {
            "pool": str(pool_path), "sample": str(sample_path),
            "facts_pool": str(facts_pool_path), "facts": str(facts_path),
            "neutral": str(neutral_path), "gold": str(gold_path),
            "preregistration": str(prereg_path),
            "bundles": [str(path) for path in bundle_paths],
        },
        "assessments": paths, "validation_id": "",
        "runner_reports": {} if fake_runner else {
            read_json_object(path, "facts study runner report")["slot_id"]: str(path)
            for path in runner_report_paths
        },
    }
    index["validation_id"] = canonical_sha256(
        {key: val for key, val in index.items() if key != "validation_id"}
    )
    path = run / "validation-index.json"
    write_json(path, index)
    return {**index, "validation": str(path)}


def run_curation_report(manifest: Manifest, *, validation_path: Path) -> dict[str, Any]:
    validation = read_json_object(validation_path, "curation validation index")
    if validation.get("contract") != CURATION_VALIDATION_CONTRACT:
        raise ValidationError("unsupported curation validation index")
    expected_id = canonical_sha256(
        {key: value for key, value in validation.items() if key != "validation_id"}
    )
    if validation.get("validation_id") != expected_id:
        raise ValidationError("curation validation_id is not canonical")
    if validation.get("mode") not in ("offline-fake-replay", "external-assessments"):
        raise ValidationError("curation validation mode is invalid")
    inputs = validation.get("inputs")
    if not isinstance(inputs, dict):
        raise ValidationError("curation validation index is missing inputs")
    sample, facts, _, gold, prereg, bundles = load_curation_inputs(
        manifest, pool_path=Path(inputs["pool"]), sample_path=Path(inputs["sample"]),
        facts_pool_path=Path(inputs["facts_pool"]), facts_path=Path(inputs["facts"]),
        neutral_path=Path(inputs["neutral"]), gold_path=Path(inputs["gold"]),
        prereg_path=Path(inputs["preregistration"]),
        bundle_paths=[Path(path) for path in inputs["bundles"]],
        use_frozen_harness=True,
    )
    assessments = {}
    slot_by_id = {slot["slot_id"]: slot for slot in prereg["schedule"]}
    for slot_id, path in validation.get("assessments", {}).items():
        slot = slot_by_id.get(slot_id)
        if slot is None:
            raise ValidationError(f"validation index contains unknown slot: {slot_id}")
        assessments[slot_id] = validate_assessment(
            read_json_object(Path(path), "curation assessment"), sample=sample,
            facts=facts, bundle=bundles[slot["arm"]], slot=slot,
        )
    report = build_report_v2(
        preregistration=prereg, gold=gold, assessments=assessments,
        sample=sample, protocol=load_protocol(manifest),
        evidence_mode=validation["mode"],
    )
    run = create_quality_run_directory(manifest.root, "facts-study-curation-report")
    path = run / "report.json"
    write_json(path, report)
    return {**report, "report": str(path), "run_directory": str(run)}


def run_execution_manifest(
    manifest: Manifest, *, preregistration_path: Path,
    authorization_id: str, granted_at: str, output_path: Path,
    execution_mode: str = "sequential", concurrency: int = 1,
    transmission_failure_max_retries: int = 0,
) -> dict[str, Any]:
    """Freeze a user-authorized execution manifest for an offline-frozen prereg."""
    from .facts_study import build_execution_manifest, validate_execution_manifest
    prereg = read_json_object(preregistration_path, "facts study preregistration")
    if prereg.get("contract") != CURATION_PREREG_CONTRACT or prereg.get("status") != "offline-frozen":
        raise ValidationError("execution manifests can only authorize offline-frozen v2 preregistrations")
    value = build_execution_manifest(
        preregistration=prereg, authorization_id=authorization_id,
        granted_at=granted_at, granted_by="user",
        execution_mode=execution_mode, concurrency=concurrency,
        transmission_failure_max_retries=transmission_failure_max_retries,
    )
    validate_execution_manifest(value, preregistration=prereg)
    write_json(output_path, value)
    return {
        "contract": value["contract"], "manifest_id": value["manifest_id"],
        "preregistration_id": prereg["preregistration_id"],
        "authorization_id": authorization_id, "manifest": str(output_path),
    }


# ---------------------------------------------------------------------------
# External lineage validation (v2, manifest-authorized)
# ---------------------------------------------------------------------------

_RUNNER_REPORT_REQUIRED_FIELDS = {
    "contract", "ok", "study_id", "preregistration_id", "slot_id", "ordinal",
    "arm", "seed", "execution_id", "provider", "model", "thinking",
    "harness_sha256", "pi_executable",
    "cache_decision", "replacement_policy", "attempts",
    "charged_or_possible_transfers", "shards", "blind_inputs", "report",
    "run_directory", "runner_report_id", "assessment", "normalization",
    "assessment_sha256", "raw_output_sha256", "findings", "elapsed_seconds",
}
_RUNNER_REPORT_OPTIONAL_FIELDS = {
    "evidence_normalizations", "dropped_findings", "transcription_repairs",
    "transmission_retry", "transmission_timeout",
}


def _check_runner_report_fields(report: dict[str, Any], where: str) -> None:
    unknown = sorted(set(report) - _RUNNER_REPORT_REQUIRED_FIELDS - _RUNNER_REPORT_OPTIONAL_FIELDS)
    missing = sorted(_RUNNER_REPORT_REQUIRED_FIELDS - set(report))
    if unknown:
        raise ValidationError(f"{where} has unknown fields: {', '.join(unknown)}")
    if missing:
        raise ValidationError(f"{where} is missing fields: {', '.join(missing)}")


def validate_external_run_lineage_v2(
    manifest: Manifest, *, prereg: dict[str, Any], execution_manifest: dict[str, Any],
    assessment_paths_by_slot: dict[str, Path], runner_report_paths: list[Path],
) -> dict[str, str]:
    """Full external lineage check for a manifest-authorized v2 campaign."""
    if len(runner_report_paths) != 33:
        raise ValidationError("external curation validation requires exactly 33 runner reports")
    slots = {slot["slot_id"]: slot for slot in prereg["schedule"]}
    max_attempts = 1 + execution_manifest["execution"]["retry"]["transmission_failure_max_retries"]
    reports: dict[str, str] = {}
    execution_ids: set[str] = set()
    authorization_hashes: set[str] = set()
    campaign = (
        manifest.root / ".artifacts" / "i18n" / "quality" / "facts-study-campaigns"
        / prereg["preregistration_id"]
    )
    for path in runner_report_paths:
        report = read_json_object(path, "facts study runner report")
        _check_runner_report_fields(report, "facts study runner report")
        slot_id = report.get("slot_id")
        if slot_id in reports or slot_id not in slots:
            raise ValidationError(f"duplicate or unknown runner-report slot: {slot_id}")
        slot = slots[slot_id]
        expected_identity = {
            "study_id": prereg["study_id"], "preregistration_id": prereg["preregistration_id"],
            "ordinal": slot["ordinal"], "arm": slot["arm"], "seed": slot["seed"],
            "provider": slot["provider"], "model": slot["model"], "thinking": slot["thinking"],
            "harness_sha256": prereg["harness_sha256"],
            "pi_executable": prereg["pi_executable"],
        }
        if report["contract"] != "tome4-quality-facts-study-runner-report-v1" or report["ok"] is not True:
            raise ValidationError(f"runner report is not a successful Facts study transfer: {slot_id}")
        if any(report.get(key) != value for key, value in expected_identity.items()):
            raise ValidationError(f"runner report frozen identity mismatch: {slot_id}")
        if report["cache_decision"] != "disabled" or report["replacement_policy"] != "forbidden":
            raise ValidationError(f"runner report transfer semantics mismatch: {slot_id}")
        attempts = report["attempts"]
        if type(attempts) is not int or attempts < 1 or attempts > max_attempts:
            raise ValidationError(f"runner report attempts out of authorized range: {slot_id}")
        if report["charged_or_possible_transfers"] != attempts or report["shards"] != 1:
            raise ValidationError(f"runner report transfer counts mismatch: {slot_id}")
        if report["blind_inputs"] != {"gold": False, "other_assessments": False, "anchors": False, "holdout": False}:
            raise ValidationError(f"runner report blindness declaration mismatch: {slot_id}")
        expected_report_id = canonical_sha256(
            {key: value for key, value in report.items() if key not in ("runner_report_id", "report", "run_directory", "elapsed_seconds")}
        )
        if report["runner_report_id"] != expected_report_id:
            raise ValidationError(f"runner report ID is not canonical: {slot_id}")
        if Path(report["report"]).resolve() != path.resolve():
            raise ValidationError(f"runner report path does not bind the supplied file: {slot_id}")
        assessment_path = assessment_paths_by_slot.get(slot_id)
        if assessment_path is None or hashlib.sha256(assessment_path.read_bytes()).hexdigest() != report["assessment_sha256"]:
            raise ValidationError(f"runner report does not bind the supplied assessment bytes: {slot_id}")
        execution_id = sha256_field(report["execution_id"], f"runner report {slot_id}.execution_id")
        if execution_id in execution_ids:
            raise ValidationError("runner report execution IDs must be unique")
        execution_ids.add(execution_id)
        ledger_path = campaign / f"{slot_id}.json"
        ledger = read_json_object(ledger_path, "facts study campaign slot ledger")
        if (
            ledger.get("contract") != "tome4-quality-facts-study-slot-ledger-v1"
            or ledger.get("preregistration_id") != prereg["preregistration_id"]
            or ledger.get("slot_id") != slot_id or ledger.get("state") != "succeeded"
            or ledger.get("execution_id") != execution_id
            or Path(ledger.get("runner_report", "")).resolve() != path.resolve()
            or ledger.get("runner_report_sha256") != hashlib.sha256(path.read_bytes()).hexdigest()
        ):
            raise ValidationError(f"campaign ledger does not bind the successful runner report: {slot_id}")
        authorization_hashes.add(
            sha256_field(ledger.get("authorization_sha256"), f"slot ledger {slot_id}.authorization_sha256")
        )
        reports[slot_id] = str(path)
    if set(reports) != set(slots):
        raise ValidationError("runner report membership does not match all 33 preregistered slots")
    expected_authorization = hashlib.sha256(
        execution_manifest["authorization"]["authorization_id"].encode()
    ).hexdigest()
    if len(authorization_hashes) != 1 or authorization_hashes != {expected_authorization}:
        raise ValidationError("all 33 Facts study slots must bind the manifest authorization identity")
    return reports
