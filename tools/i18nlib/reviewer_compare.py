"""Blind production-v2 reviewer comparison preparation and scoring.

The module never invokes a provider.  It freezes local candidates and Gold, emits
ordinary translation semantic v2 bundles, and validates externally produced results.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from . import TOOL_VERSION
from .errors import ConfigurationError, ValidationError
from .locale_model import LocaleLoader
from .quality import create_quality_run_directory
from .quality_contracts import canonical_sha256
from .report import write_json
from .review import _translation_bundle_payload, _translation_items_from_bytes
from .pi_review import _review_cache_key
from .translation_review import (
    TRANSLATION_REVIEW_ASSESSMENT_CONTRACT,
    TRANSLATION_REVIEW_BUNDLE_CONTRACT,
    TRANSLATION_REVIEW_NORMALIZER_CONTRACT,
    TRANSLATION_REVIEW_RUNNER_CONTRACT,
    deduplicate_translation_revisions,
    load_translation_review_policy,
    make_evaluator_identity,
    partition_translation_items,
    revalidate_translation_assessment,
    translation_provider_message,
    translation_selection_sha256,
    write_translation_inventory,
)


POLICY_PATH = Path("i18n/quality/reviewer-comparison-v2.json")
DATASET_REGISTRY_PATH = Path("i18n/quality/dataset-registry-v1.json")
PROMPT_PATH = Path("i18n/prompts/pi-translation-reviewer-v2.md")
COMPARISON_SCHEMA_PATHS = (
    Path("i18n/quality/schemas/reviewer-comparison-gold-v2.schema.json"),
    Path("i18n/quality/schemas/reviewer-comparison-preregistration-v2.schema.json"),
    Path("i18n/quality/schemas/reviewer-comparison-result-index-v2.schema.json"),
)
POLICY_CONTRACT = "tome4-reviewer-comparison-policy-v2"
POOL_CONTRACT = "tome4-reviewer-comparison-candidate-pool-v2"
GOLD_TEMPLATE_CONTRACT = "tome4-reviewer-comparison-gold-template-v2"
GOLD_CONTRACT = "tome4-reviewer-comparison-gold-v2"
PREREG_CONTRACT = "tome4-reviewer-comparison-preregistration-v2"
RESULT_INDEX_CONTRACT = "tome4-reviewer-comparison-result-index-v2"
VALIDATION_CONTRACT = "tome4-reviewer-comparison-validation-v2"
REPORT_CONTRACT = "tome4-reviewer-comparison-report-v2"
SHA256_HEX = frozenset("0123456789abcdef")
GOLD_SEVERITIES = frozenset({"major", "minor", "clean", "context-insufficient"})


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except OSError as error:
        raise ValidationError(f"cannot read {label}: {path}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid {label}: {path}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                if not line.strip():
                    continue
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValidationError(f"inventory line {line_number} is not an object")
                items.append(value)
    except OSError as error:
        raise ValidationError(f"cannot read quality inventory: {path}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid quality inventory: {path}: {error}") from error
    if not items:
        raise ValidationError("quality inventory is empty")
    return items


def _sha(value: Any) -> str:
    return canonical_sha256(value)


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= SHA256_HEX


def _implementation_sha256(root: Path) -> str:
    paths = (
        Path(__file__).resolve(),
        root / "tools" / "i18nlib" / "translation_review.py",
        root / "tools" / "i18nlib" / "pi_review.py",
        root / PROMPT_PATH,
        root / "i18n" / "review" / "translation-semantic-v2.json",
        root / POLICY_PATH,
        *(root / path for path in COMPARISON_SCHEMA_PATHS),
    )
    records = []
    for path in paths:
        try:
            payload = path.read_bytes()
        except OSError as error:
            raise ConfigurationError(f"cannot bind reviewer comparison implementation: {path}") from error
        records.append({
            "name": path.name,
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
    return _sha(records)


def load_comparison_policy(root: Path) -> tuple[dict[str, Any], str]:
    path = root / POLICY_PATH
    value = _read_json(path, "reviewer comparison policy")
    if value.get("contract") != POLICY_CONTRACT or value.get("schema_version") != 2:
        raise ConfigurationError("unsupported reviewer comparison policy")
    models = value.get("models")
    if not isinstance(models, list) or len(models) != 2:
        raise ConfigurationError("reviewer comparison policy must define two models")
    aliases = set()
    for model in models:
        if not isinstance(model, dict) or set(model) != {"alias", "provider", "model", "thinking"}:
            raise ConfigurationError("reviewer comparison model identity is invalid")
        if not all(isinstance(model[key], str) and model[key] for key in model):
            raise ConfigurationError("reviewer comparison model identity is invalid")
        aliases.add(model["alias"])
    if len(aliases) != 2:
        raise ConfigurationError("reviewer comparison model aliases must be unique")
    if models[0] != {
        "alias": "reviewer-a", "provider": "opencode-go",
        "model": "deepseek-v4-flash", "thinking": "max",
    } or models[1] != {
        "alias": "reviewer-b", "provider": "openai-codex",
        "model": "gpt-5.6-sol", "thinking": "medium",
    }:
        raise ConfigurationError("reviewer comparison model settings are not frozen")
    if value.get("max_items_per_bundle") != 2 or value.get("character_budget") != 16000:
        raise ConfigurationError("reviewer comparison bundle maximum is not frozen")
    minimum = value.get("minimum_gold_counts")
    if (
        not isinstance(minimum, dict)
        or type(minimum.get("no_substantive_difference")) is not int
        or type(minimum.get("context_insufficient")) is not int
        or type(minimum.get("accepted_difference")) is not int
    ):
        raise ConfigurationError("reviewer comparison semantic Gold minimum is invalid")
    if set(value.get("eligibility", {})) != {
        "schema_coverage",
        "structure_failures_max",
        "semantic_claim_jaccard_min",
        "item_flag_agreement_min",
        "context_state_accuracy_min",
        "no_difference_false_positive_rate_max",
    }:
        raise ConfigurationError("reviewer comparison eligibility fields are invalid")
    return value, hashlib.sha256(path.read_bytes()).hexdigest()


def _registered_revisions(root: Path) -> set[str]:
    registry = _read_json(root / DATASET_REGISTRY_PATH, "quality dataset registry")
    if registry.get("contract") != "tome4-quality-dataset-registry-v1":
        raise ConfigurationError("unsupported quality dataset registry")
    revisions: set[str] = set()
    for entry in registry.get("entries", []):
        if not isinstance(entry, dict):
            raise ConfigurationError("quality dataset registry entry is invalid")
        values = entry.get("revision_ids", [])
        if not isinstance(values, list) or not all(_is_sha(value) for value in values):
            raise ConfigurationError("quality dataset registry revisions are invalid")
        revisions.update(values)
    return revisions


def _risk_score(item: dict[str, Any]) -> int:
    flags = item.get("risk_flags", [])
    gates = item.get("gate_signals", {})
    score = 3 * len(flags) if isinstance(flags, list) else 0
    if isinstance(gates, dict):
        needs = gates.get("needs_review", [])
        score += 2 * len(needs) if isinstance(needs, list) else 0
        score += 4 * sum(gates.get(key) is False for key in (
            "format_shape_match", "format_signature_match", "markup_multiset_match",
            "at_token_multiset_match",
        ))
    source = item.get("source", "")
    if isinstance(source, str):
        score += min(len(source) // 120, 5)
        score += 2 * any(character.isdigit() for character in source)
    return score


def _candidate_projection(item: dict[str, Any], rank: int) -> dict[str, Any]:
    occurrence = (item.get("occurrences") or [{}])[0]
    return {
        "rank": rank,
        "revision_id": item["revision_id"],
        "unit_id": item.get("unit_id"),
        "component": item["component"],
        "section": item.get("section", ""),
        "source": item.get("source", ""),
        "target": item.get("target", ""),
        "source_tag": item.get("source_tag"),
        "ordinal": occurrence.get("ordinal"),
        "risk_score": _risk_score(item),
        "risk_flags": item.get("risk_flags", []),
        "gold": {
            "split": None,
            "gold_state": None,
            "semantic_state": None,
            "severity": None,
            "findings_exhaustive": None,
            "adjudication_rationale": None,
            "controlled": False,
            "findings": [],
        },
    }


def run_prepare(
    manifest: Any,
    *,
    inventory_path: Path,
    manual_include_revision_ids: tuple[str, ...] = (),
) -> dict[str, Any]:
    policy, policy_sha256 = load_comparison_policy(manifest.root)
    excluded = _registered_revisions(manifest.root)
    inventory = _read_jsonl(inventory_path)
    preferred = list(policy["preferred_components"])
    fallback = list(policy["fallback_components"])
    manifest_components = [component.id for component in manifest.components]
    component_order = preferred + fallback + [
        value for value in manifest_components if value not in preferred + fallback
    ]
    order_index = {value: index for index, value in enumerate(component_order)}
    eligible: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in inventory:
        revision = item.get("revision_id")
        component = item.get("component")
        if not _is_sha(revision) or revision in excluded or revision in seen:
            continue
        if component not in order_index:
            continue
        if not all(isinstance(item.get(key), str) for key in ("source", "target")):
            continue
        seen.add(revision)
        eligible.append(item)
    if (
        len(set(manual_include_revision_ids)) != len(manual_include_revision_ids)
        or not all(_is_sha(value) for value in manual_include_revision_ids)
    ):
        raise ValidationError("manual candidate inclusions must be unique revision SHA-256 values")
    eligible_by_revision = {item["revision_id"]: item for item in eligible}
    missing_inclusions = [
        revision for revision in manual_include_revision_ids
        if revision not in eligible_by_revision
    ]
    if missing_inclusions:
        raise ValidationError(
            "manual candidate inclusion is absent, ineligible, or already registered: "
            + ", ".join(missing_inclusions)
        )
    seed = policy["seed"]
    eligible.sort(key=lambda item: (
        order_index[item["component"]], -_risk_score(item),
        hashlib.sha256((seed + item["revision_id"]).encode()).hexdigest(),
    ))
    by_component: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in eligible:
        by_component[item["component"]].append(item)
    selected: list[dict[str, Any]] = [
        eligible_by_revision[revision] for revision in manual_include_revision_ids
    ]
    for values in by_component.values():
        values[:] = [
            item for item in values
            if item["revision_id"] not in set(manual_include_revision_ids)
        ]
    maximum = policy["candidate_pool_size"]
    tiers = [
        preferred,
        fallback,
        [value for value in component_order if value not in preferred + fallback],
    ]
    for tier in tiers:
        while len(selected) < maximum:
            progressed = False
            for component in tier:
                values = by_component[component]
                if values and len(selected) < maximum:
                    selected.append(values.pop(0))
                    progressed = True
            if not progressed:
                break
    candidates = [_candidate_projection(item, index + 1) for index, item in enumerate(selected)]
    pool_identity = {
        "contract": POOL_CONTRACT,
        "schema_version": 2,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "policy_sha256": policy_sha256,
        "implementation_sha256": _implementation_sha256(manifest.root),
        "inventory_sha256": hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
        "excluded_revision_ids_sha256": _sha(sorted(excluded)),
        "manual_include_revision_ids": list(manual_include_revision_ids),
        "fallback_order": policy["fallback_order"],
        "items": [{key: value for key, value in item.items() if key != "gold"} for item in candidates],
    }
    pool_identity["candidate_pool_id"] = _sha(pool_identity)
    template = {
        "contract": GOLD_TEMPLATE_CONTRACT,
        "schema_version": 2,
        "candidate_pool_id": pool_identity["candidate_pool_id"],
        "human_confirmed": False,
        "fallback_stage": "none",
        "instructions": (
            "Choose exactly 32 calibration and 32 holdout items; independently label "
            "semantic_state, acceptability severity, and whether findings are exhaustive; "
            "semantic_state describes only the observable bounded source-target relationship: "
            "an intentional or mechanics-justified adaptation remains substantive-difference "
            "with severity clean, and needing outside game-code verification for acceptability "
            "does not make the bounded observation context-insufficient; reserve "
            "no-substantive-difference for genuine proposition-level equivalence and reserve "
            "context-insufficient for absent referents, attachment, ellipsis, or deliberate "
            "ambiguity that prevents deciding the bounded proposition; "
            "record an adjudication rationale and list every accepted classification plus "
            "its equivalence rationale for each required claim; "
            "then set human_confirmed=true and change contract to " + GOLD_CONTRACT
        ),
        "items": candidates,
    }
    run_directory = create_quality_run_directory(manifest.root, "reviewer-comparison-prepare")
    pool_path = run_directory / "candidate-pool.json"
    template_path = run_directory / "gold-template.json"
    write_json(pool_path, pool_identity)
    write_json(template_path, template)
    summary = {
        "contract": "tome4-reviewer-comparison-prepare-report-v2",
        "candidate_pool_id": pool_identity["candidate_pool_id"],
        "candidate_count": len(candidates),
        "ready_for_gold_curation": len(candidates) >= 64,
        "fallback_required": (
            None if len(candidates) >= 64 else "unexposed-historical-revisions"
        ),
        "excluded_revision_count": len(excluded),
        "manual_include_count": len(manual_include_revision_ids),
        "component_counts": dict(sorted(Counter(item["component"] for item in candidates).items())),
        "candidate_pool": str(pool_path),
        "gold_template": str(template_path),
        "run_directory": str(run_directory),
    }
    write_json(run_directory / "prepare-report.json", summary)
    return summary


def _validate_gold_finding(finding: Any, item: dict[str, Any], where: str) -> dict[str, Any]:
    fields = {
        "phenomenon",
        "meaning_change",
        "accepted_classifications",
        "classification_rationale",
        "source_evidence",
        "target_evidence",
    }
    if not isinstance(finding, dict) or set(finding) != fields:
        raise ValidationError(f"{where} must contain exactly {sorted(fields)}")
    review_policy, _digest = load_translation_review_policy(item["root"])
    if finding["phenomenon"] not in review_policy["phenomena"]:
        raise ValidationError(f"{where}.phenomenon is invalid")
    if finding["meaning_change"] not in review_policy["phenomenon_meaning_changes"][finding["phenomenon"]]:
        raise ValidationError(f"{where} phenomenon/meaning_change is incompatible")
    if (
        not isinstance(finding["classification_rationale"], str)
        or not finding["classification_rationale"].strip()
        or len(finding["classification_rationale"]) > 12000
    ):
        raise ValidationError(f"{where}.classification_rationale is invalid")
    raw_classifications = finding["accepted_classifications"]
    if not isinstance(raw_classifications, list) or not raw_classifications:
        raise ValidationError(f"{where}.accepted_classifications must be a non-empty array")
    classifications: list[tuple[str, str]] = []
    for index, classification in enumerate(raw_classifications):
        classification_where = f"{where}.accepted_classifications[{index}]"
        if (
            not isinstance(classification, dict)
            or set(classification) != {"phenomenon", "meaning_change"}
        ):
            raise ValidationError(f"{classification_where} is invalid")
        phenomenon = classification["phenomenon"]
        meaning_change = classification["meaning_change"]
        if (
            phenomenon not in review_policy["phenomena"]
            or meaning_change not in review_policy["phenomenon_meaning_changes"][phenomenon]
        ):
            raise ValidationError(f"{classification_where} is incompatible")
        pair = (phenomenon, meaning_change)
        if pair in classifications:
            raise ValidationError(f"{where}.accepted_classifications contains a duplicate")
        classifications.append(pair)
    primary = (finding["phenomenon"], finding["meaning_change"])
    if primary not in classifications:
        raise ValidationError(f"{where}.accepted_classifications omits the primary classification")
    accepted_meanings = {meaning for _phenomenon, meaning in classifications}
    for evidence_name, text, allow_missing in (
        ("source_evidence", item["source"], "added" in accepted_meanings),
        ("target_evidence", item["target"], "omitted" in accepted_meanings),
    ):
        evidence = finding[evidence_name]
        if not isinstance(evidence, dict) or set(evidence) != {"quote", "occurrence"}:
            raise ValidationError(f"{where}.{evidence_name} is invalid")
        quote, occurrence = evidence["quote"], evidence["occurrence"]
        if not isinstance(quote, str) or type(occurrence) is not int:
            raise ValidationError(f"{where}.{evidence_name} is invalid")
        if not quote:
            if not allow_missing or occurrence != 0:
                raise ValidationError(f"{where}.{evidence_name} is invalid")
            continue
        if occurrence < 1 or text.count(quote) < occurrence:
            raise ValidationError(f"{where}.{evidence_name} is not exact evidence")
    if not finding["source_evidence"]["quote"] and not finding["target_evidence"]["quote"]:
        raise ValidationError(f"{where} cannot omit evidence on both sides")
    return finding


def _bundle_selected_items(manifest: Any, loader: LocaleLoader, selected: list[dict[str, Any]], run_directory: Path, policy: dict[str, Any]) -> list[dict[str, Any]]:
    manifest_sha256 = hashlib.sha256(manifest.raw_bytes).hexdigest()
    _review_policy, review_policy_sha256 = load_translation_review_policy(manifest.root)
    by_component: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in selected:
        by_component[item["component"]].append(item)
    descriptors: list[dict[str, Any]] = []
    for component, gold_items in sorted(by_component.items()):
        spec = manifest.component(component)
        translation_path = manifest.root / spec.translation
        translation_bytes = translation_path.read_bytes()
        canonical = _translation_items_from_bytes(manifest, loader, component, translation_bytes)
        canonical_by_revision = {item["revision_id"]: item for item in canonical}
        chosen = []
        for gold in gold_items:
            if gold["controlled"]:
                raise ValidationError(
                    "controlled variants cannot enter exact production-v2 canonical bundles; "
                    "use them only in a separately reported auxiliary experiment"
                )
            try:
                chosen.append(canonical_by_revision[gold["revision_id"]])
            except KeyError as error:
                raise ValidationError(
                    f"Gold revision is not current canonical content: {gold['revision_id']}"
                ) from error
        # Gold is curated in benchmark order, while production-v2 membership
        # proofs require the selected canonical records to remain in ordinal
        # order.  Restore that order before deduplication and partitioning.
        chosen.sort(key=lambda item: item["ordinal"])
        chosen = deduplicate_translation_revisions(chosen)
        selection_sha256 = translation_selection_sha256(chosen)
        inventory_sha256, membership = write_translation_inventory(
            root=manifest.root, tool_version=TOOL_VERSION, version=manifest.version,
            component=component,
            translation_sha256=hashlib.sha256(translation_bytes).hexdigest(), items=canonical,
        )
        for offset, batch, characters, oversized in partition_translation_items(
            chosen, max_items=policy["max_items_per_bundle"],
            character_budget=policy["character_budget"],
        ):
            payload = _translation_bundle_payload(
                tool_version=TOOL_VERSION, version=manifest.version,
                manifest_sha256=manifest_sha256, component=component,
                translation_sha256=hashlib.sha256(translation_bytes).hexdigest(),
                offset=offset, total=len(chosen), batch=batch,
                character_count=characters, character_budget=policy["character_budget"],
                oversized_single_item=oversized, policy_sha256=review_policy_sha256,
                inventory_sha256=inventory_sha256, selection_sha256=selection_sha256,
                membership=[membership[item["ordinal"]] for item in batch],
            )
            payload["bundle_id"] = _sha(payload)
            bundle_path = run_directory / "bundles" / gold_items[0]["split"] / component / f"{payload['bundle_id']}.json"
            write_json(bundle_path, payload)
            descriptors.append({
                "split": gold_items[0]["split"], "component": component,
                "bundle_id": payload["bundle_id"], "bundle_sha256": _sha(payload),
                "count": len(batch), "item_character_count": characters,
                "item_character_budget": policy["character_budget"],
                "artifact_bytes": bundle_path.stat().st_size,
                "payload_bytes": len(translation_provider_message(payload)),
                "path": str(bundle_path),
            })
    return descriptors


def run_freeze(manifest: Any, loader: LocaleLoader, *, pool_path: Path, gold_path: Path) -> dict[str, Any]:
    policy, policy_sha256 = load_comparison_policy(manifest.root)
    pool = _read_json(pool_path, "reviewer comparison candidate pool")
    gold = _read_json(gold_path, "reviewer comparison Gold")
    if pool.get("contract") != POOL_CONTRACT or pool.get("candidate_pool_id") != _sha({key: value for key, value in pool.items() if key != "candidate_pool_id"}):
        raise ValidationError("candidate pool identity is invalid")
    if gold.get("contract") != GOLD_CONTRACT or gold.get("schema_version") != 2 or gold.get("human_confirmed") is not True:
        raise ValidationError("Gold must be explicitly human-confirmed")
    if gold.get("candidate_pool_id") != pool["candidate_pool_id"]:
        raise ValidationError("Gold candidate pool identity does not match")
    fallback_stage = gold.get("fallback_stage")
    if fallback_stage not in {"none", *policy["fallback_order"]}:
        raise ValidationError("Gold fallback_stage is invalid")
    if fallback_stage == "stop-insufficient-evidence":
        raise ValidationError("insufficient-evidence Gold cannot be frozen for provider execution")
    raw_items = gold.get("items")
    if not isinstance(raw_items, list) or len(raw_items) != 64:
        raise ValidationError("Gold must select exactly 64 items")
    candidates = {item["revision_id"]: item for item in pool["items"]}
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_items):
        where = f"Gold items[{index}]"
        fields = {
            "revision_id",
            "split",
            "gold_state",
            "semantic_state",
            "severity",
            "findings_exhaustive",
            "adjudication_rationale",
            "controlled",
            "findings",
        }
        if not isinstance(raw, dict) or set(raw) != fields:
            raise ValidationError(f"{where} fields are invalid")
        revision = raw["revision_id"]
        if revision in seen or revision not in candidates:
            raise ValidationError(f"{where}.revision_id is duplicate or outside the pool")
        seen.add(revision)
        if raw["split"] not in {"calibration", "holdout"} or raw["severity"] not in GOLD_SEVERITIES:
            raise ValidationError(f"{where} split or severity is invalid")
        if (
            raw["gold_state"] not in {"assessed", "context-insufficient"}
            or raw["semantic_state"] not in {
                "no-substantive-difference",
                "substantive-difference",
                "context-insufficient",
            }
            or type(raw["findings_exhaustive"]) is not bool
            or not isinstance(raw["adjudication_rationale"], str)
            or not raw["adjudication_rationale"].strip()
            or len(raw["adjudication_rationale"]) > 12000
            or type(raw["controlled"]) is not bool
        ):
            raise ValidationError(f"{where} semantic state or marker is invalid")
        if not isinstance(raw["findings"], list):
            raise ValidationError(f"{where}.findings must be an array")
        if raw["semantic_state"] == "no-substantive-difference":
            if (
                raw["gold_state"] != "assessed"
                or raw["severity"] != "clean"
                or raw["findings_exhaustive"] is not True
                or raw["findings"]
            ):
                raise ValidationError(f"{where} no-difference labels disagree")
        elif raw["semantic_state"] == "substantive-difference":
            if (
                raw["gold_state"] != "assessed"
                or raw["severity"] not in {"major", "minor", "clean"}
                or not raw["findings"]
            ):
                raise ValidationError(f"{where} substantive-difference labels disagree")
        elif (
            raw["gold_state"] != "context-insufficient"
            or raw["severity"] != "context-insufficient"
            or raw["findings_exhaustive"] is not False
            or raw["findings"]
        ):
            raise ValidationError(f"{where} context-insufficient labels disagree")
        item = {**candidates[revision], **raw, "root": manifest.root}
        item["findings"] = [
            _validate_gold_finding(finding, item, f"{where}.findings[{position}]")
            for position, finding in enumerate(raw["findings"])
        ]
        item.pop("root")
        selected.append(item)
    required_fallback_index = -1
    for split, split_policy in policy["splits"].items():
        items = [item for item in selected if item["split"] == split]
        if len(items) != split_policy["size"]:
            raise ValidationError(f"{split} must contain exactly {split_policy['size']} items")
        counts = Counter(item["severity"] for item in items)
        substantive = counts["major"] + counts["minor"]
        minimum = policy["minimum_gold_counts"]
        no_difference = sum(
            item["semantic_state"] == "no-substantive-difference" for item in items
        )
        accepted_difference = sum(
            item["semantic_state"] == "substantive-difference"
            and item["severity"] == "clean"
            for item in items
        )
        if (
            counts["major"] < minimum["major"]
            or substantive < minimum["substantive_total"]
            or counts["clean"] < minimum["clean"]
            or counts["context-insufficient"] < minimum["context_insufficient"]
            or accepted_difference < minimum["accepted_difference"]
            or no_difference < minimum["no_substantive_difference"]
        ):
            raise ValidationError(f"{split} does not meet minimum Gold strata")
        components = Counter(item["component"] for item in items)
        if len(components) < policy["minimum_components_per_split"] or max(components.values()) > math.floor(len(items) * policy["component_max_fraction"]):
            raise ValidationError(f"{split} does not meet component diversity limits")
        if set(components) - set(policy["preferred_components"]):
            required_fallback_index = max(required_fallback_index, 0)
        if any(components.get(component, 0) != 8 for component in policy["preferred_components"]):
            required_fallback_index = max(required_fallback_index, 1)
        target = policy["target_gold_counts"]
        if any(counts[name] != expected for name, expected in target.items()):
            required_fallback_index = max(required_fallback_index, 3)
        controlled = sum(item["controlled"] for item in items)
        if controlled > math.floor(len(items) * policy["controlled_max_fraction"]):
            raise ValidationError(f"{split} exceeds the controlled-variant limit")
        if controlled:
            required_fallback_index = max(required_fallback_index, 4)
    actual_fallback_index = (
        -1 if fallback_stage == "none" else policy["fallback_order"].index(fallback_stage)
    )
    if actual_fallback_index < required_fallback_index:
        raise ValidationError(
            "Gold fallback_stage does not disclose the deepest sample fallback used"
        )
    run_directory = create_quality_run_directory(manifest.root, "reviewer-comparison-freeze")
    bundle_descriptors: list[dict[str, Any]] = []
    for split in ("calibration", "holdout"):
        bundle_descriptors.extend(_bundle_selected_items(
            manifest, loader, [item for item in selected if item["split"] == split],
            run_directory, policy,
        ))
    prompt = (manifest.root / PROMPT_PATH).read_text(encoding="utf-8")
    provider_prompt = prompt + "\nCurrent working directory: /private/tmp"
    prompt_sha256 = hashlib.sha256(provider_prompt.encode()).hexdigest()
    slots: list[dict[str, Any]] = []
    slot_number = 0
    for split in ("calibration", "holdout"):
        for run in range(1, policy["splits"][split]["runs"] + 1):
            for descriptor in [value for value in bundle_descriptors if value["split"] == split]:
                for model in policy["models"]:
                    slot_number += 1
                    slots.append({
                        "slot_id": f"slot-{slot_number:03d}", "split": split,
                        "round": run, "reviewer": model["alias"],
                        "provider": model["provider"], "model": model["model"],
                        "thinking": model["thinking"], "bundle_id": descriptor["bundle_id"],
                        "bundle": descriptor["path"], "cache": False,
                        "retry_transmission": policy["connection_failure_retry_limit"],
                        "command": [
                            "tools/pi-review", "--bundle", descriptor["path"],
                            "--expected-bundle-id", descriptor["bundle_id"],
                            "--provider", model["provider"], "--model", model["model"],
                            "--thinking", model["thinking"], "--timeout", "1200",
                            "--strict", "--no-cache",
                        ],
                    })
    frozen_gold = {
        "contract": GOLD_CONTRACT, "schema_version": 2,
        "candidate_pool_id": pool["candidate_pool_id"], "human_confirmed": True,
        "fallback_stage": fallback_stage,
        "items": [{key: value for key, value in item.items() if key not in {"rank", "unit_id", "section", "source", "target", "source_tag", "ordinal", "risk_score", "risk_flags", "component"}} for item in selected],
    }
    frozen_gold["gold_id"] = _sha(frozen_gold)
    gold_output = run_directory / "frozen-gold.json"
    write_json(gold_output, frozen_gold)
    prereg = {
        "contract": PREREG_CONTRACT, "schema_version": 2,
        "tool_version": TOOL_VERSION, "version": manifest.version,
        "policy_sha256": policy_sha256,
        "implementation_sha256": _implementation_sha256(manifest.root),
        "candidate_pool_id": pool["candidate_pool_id"], "gold_id": frozen_gold["gold_id"],
        "gold": str(gold_output),
        "fallback_stage": fallback_stage,
        "gold_sha256": hashlib.sha256(gold_output.read_bytes()).hexdigest(),
        "prompt_sha256": prompt_sha256,
        "translation_review_contract": TRANSLATION_REVIEW_BUNDLE_CONTRACT,
        "models": policy["models"], "bundles": bundle_descriptors, "slots": slots,
        "planned_content_slots": len(slots),
        "maximum_external_transfers": len(slots) * (1 + policy["connection_failure_retry_limit"]),
        "replace_content_failures": False,
        "holdout_sealed": True,
    }
    prereg["preregistration_id"] = _sha(prereg)
    prereg_path = run_directory / "preregistration.json"
    write_json(prereg_path, prereg)
    result_template = {
        "contract": RESULT_INDEX_CONTRACT, "schema_version": 2,
        "preregistration_id": prereg["preregistration_id"],
        "authorization_id": None,
        "authorized_at": None,
        "calibration_frozen_at": None,
        "holdout_cleared": False,
        "holdout_cleared_at": None,
        "results": [{"slot_id": slot["slot_id"], "status": "pending", "assessment": None, "run_report": None} for slot in slots],
    }
    write_json(run_directory / "result-index-template.json", result_template)
    summary = {
        "preregistration_id": prereg["preregistration_id"],
        "bundles": len(bundle_descriptors), "planned_content_slots": len(slots),
        "maximum_external_transfers": prereg["maximum_external_transfers"],
        "payload_bytes": sum(item["payload_bytes"] for item in bundle_descriptors),
        "preregistration": str(prereg_path), "gold": str(gold_output),
        "result_index_template": str(run_directory / "result-index-template.json"),
        "run_directory": str(run_directory),
    }
    write_json(run_directory / "freeze-report.json", summary)
    return summary


def _finding_span(evidence: dict[str, Any], text: str) -> tuple[int, int] | None:
    quote = evidence["quote"]
    if not quote:
        return None
    start = -1
    for _ in range(evidence["occurrence"]):
        start = text.find(quote, start + 1)
    return (start, start + len(quote)) if start >= 0 else None


def _overlap(left: tuple[int, int] | None, right: tuple[int, int] | None) -> bool:
    if left is None or right is None:
        return left is None and right is None
    return max(left[0], right[0]) < min(left[1], right[1])


def _evidence_matches(
    left: dict[str, Any],
    right: dict[str, Any],
    text: str,
    *,
    optional_missing_side: bool,
) -> tuple[bool, bool]:
    """Return whether one evidence side is compatible and whether it overlaps.

    Genuine additions and omissions have no literal counterpart on one side.  The
    missing side therefore acts as an explicit absence marker, not as a span that
    must overlap a curator's surrounding context anchor.
    """
    left_span = _finding_span(left, text)
    right_span = _finding_span(right, text)
    if optional_missing_side and (left_span is None or right_span is None):
        return True, False
    matched = _overlap(left_span, right_span)
    return matched, matched and left_span is not None and right_span is not None


def _finding_evidence_matches(
    left: dict[str, Any],
    right: dict[str, Any],
    *,
    source: str,
    target: str,
) -> bool:
    source_matches, source_overlaps = _evidence_matches(
        left["source_evidence"],
        right["source_evidence"],
        source,
        optional_missing_side=(
            left["meaning_change"] == "added" or right["meaning_change"] == "added"
        ),
    )
    target_matches, target_overlaps = _evidence_matches(
        left["target_evidence"],
        right["target_evidence"],
        target,
        optional_missing_side=(
            left["meaning_change"] == "omitted" or right["meaning_change"] == "omitted"
        ),
    )
    return source_matches and target_matches and (source_overlaps or target_overlaps)


def _accepted_classifications(finding: dict[str, Any]) -> set[tuple[str, str]]:
    values = finding.get("accepted_classifications")
    if not isinstance(values, list):
        return {(finding["phenomenon"], finding["meaning_change"])}
    return {
        (value["phenomenon"], value["meaning_change"])
        for value in values
        if isinstance(value, dict)
        and isinstance(value.get("phenomenon"), str)
        and isinstance(value.get("meaning_change"), str)
    }


def _gold_finding_matches(
    expected: dict[str, Any],
    observed: dict[str, Any],
    *,
    source: str,
    target: str,
) -> bool:
    if (observed["phenomenon"], observed["meaning_change"]) not in _accepted_classifications(expected):
        return False
    return _finding_evidence_matches(
        expected, observed, source=source, target=target
    )


def _semantic_findings_match(
    left: dict[str, Any],
    right: dict[str, Any],
    *,
    source: str,
    target: str,
) -> bool:
    # Phenomenon labels can legitimately differ for the same anchored claim, but
    # opposite directions (for example weakened vs strengthened) are not stable.
    if left["meaning_change"] != right["meaning_change"]:
        return False
    return _finding_evidence_matches(left, right, source=source, target=target)


def _maximum_matching_count(
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
    predicate: Any,
) -> int:
    """Compute deterministic maximum-cardinality matching for bounded finding lists."""
    matched_right: dict[int, int] = {}

    def augment(left_index: int, seen: set[int]) -> bool:
        for right_index in range(len(right)):
            if right_index in seen or not predicate(left[left_index], right[right_index]):
                continue
            seen.add(right_index)
            if right_index not in matched_right or augment(matched_right[right_index], seen):
                matched_right[right_index] = left_index
                return True
        return False

    return sum(augment(index, set()) for index in range(len(left)))


def _match_item(gold: dict[str, Any], observed: dict[str, Any]) -> tuple[int, int, int]:
    matched = _maximum_matching_count(
        gold["findings"],
        observed["findings"],
        lambda expected, finding: _gold_finding_matches(
            expected,
            finding,
            source=gold["source"],
            target=gold["target"],
        ),
    )
    return (
        matched,
        len(observed["findings"]) - matched,
        len(gold["findings"]) - matched,
    )


def _semantic_claim_jaccard(
    left: dict[str, dict[str, Any]],
    right: dict[str, dict[str, Any]],
    gold_items: list[dict[str, Any]],
) -> float:
    matched = left_total = right_total = 0
    gold_by_revision = {item["revision_id"]: item for item in gold_items}
    for revision_id in sorted(gold_by_revision):
        gold = gold_by_revision[revision_id]
        left_findings = left[revision_id]["findings"]
        right_findings = right[revision_id]["findings"]
        left_total += len(left_findings)
        right_total += len(right_findings)
        matched += _maximum_matching_count(
            left_findings,
            right_findings,
            lambda first, second: _semantic_findings_match(
                first,
                second,
                source=gold["source"],
                target=gold["target"],
            ),
        )
    union = left_total + right_total - matched
    return _ratio(matched, union) if union else 1.0


def _ratio(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 6) if denominator else None


def _metrics(gold_items: list[dict[str, Any]], observed: dict[str, dict[str, Any]]) -> dict[str, Any]:
    tp = fp = fn = major_found = no_difference_fp = unadjudicated = 0
    substantive_items = major_items = no_difference_items = exhaustive_items = 0
    accepted_difference_items = 0
    context_correct = context_total = 0
    for gold in gold_items:
        result = observed[gold["revision_id"]]
        semantic_state = gold["semantic_state"]
        if semantic_state == "substantive-difference":
            substantive_items += 1
            accepted_difference_items += gold["severity"] == "clean"
            if gold["severity"] == "major":
                major_items += 1
            item_tp, item_unmatched, item_fn = _match_item(gold, result)
            tp += item_tp
            fn += item_fn
            if gold["findings_exhaustive"]:
                exhaustive_items += 1
                fp += item_unmatched
            else:
                unadjudicated += item_unmatched
            if gold["severity"] == "major" and item_tp:
                major_found += 1
        elif semantic_state == "no-substantive-difference":
            no_difference_items += 1
            if result["findings"]:
                no_difference_fp += 1
                fp += len(result["findings"])
        else:
            context_total += 1
            context_correct += result["assessment_state"] == "context-insufficient"
            unadjudicated += len(result["findings"])
    precision = _ratio(tp, tp + fp)
    recall = _ratio(tp, tp + fn)
    return {
        "true_positive_findings": tp, "false_positive_findings": fp,
        "false_negative_findings": fn, "precision": precision, "recall": recall,
        "f1": _ratio(2 * tp, 2 * tp + fp + fn),
        "precision_complete": unadjudicated == 0,
        "unadjudicated_additional_findings": unadjudicated,
        "required_gold_findings": tp + fn,
        "exhaustive_substantive_items": exhaustive_items,
        "major_items": major_items, "major_items_found": major_found,
        "major_recall": _ratio(major_found, major_items),
        "substantive_items": substantive_items,
        "accepted_difference_items": accepted_difference_items,
        "no_difference_items": no_difference_items,
        "no_difference_false_positive_items": no_difference_fp,
        "no_difference_false_positive_rate": _ratio(
            no_difference_fp, no_difference_items
        ),
        "context_items": context_total,
        "context_state_accuracy": _ratio(context_correct, context_total),
        "manual_queue_per_100_items": round(100 * sum(len(value["findings"]) + (value["assessment_state"] == "context-insufficient" and not value["findings"]) for value in observed.values()) / len(gold_items), 6),
    }


def run_validate(manifest: Any, *, preregistration_path: Path, result_index_path: Path) -> dict[str, Any]:
    policy, policy_sha256 = load_comparison_policy(manifest.root)
    prereg = _read_json(preregistration_path, "reviewer comparison preregistration")
    if (
        prereg.get("contract") != PREREG_CONTRACT
        or prereg.get("schema_version") != 2
        or prereg.get("preregistration_id")
        != _sha({key: value for key, value in prereg.items() if key != "preregistration_id"})
    ):
        raise ValidationError("reviewer comparison preregistration identity is invalid")
    if prereg.get("policy_sha256") != policy_sha256:
        raise ValidationError("reviewer comparison policy is stale")
    if prereg.get("tool_version") != TOOL_VERSION or prereg.get("implementation_sha256") != _implementation_sha256(manifest.root):
        raise ValidationError("reviewer comparison implementation is stale")
    gold_path = Path(prereg.get("gold", ""))
    if not gold_path.is_file() or hashlib.sha256(gold_path.read_bytes()).hexdigest() != prereg.get("gold_sha256"):
        raise ValidationError("reviewer comparison Gold is unavailable or stale")
    result_index = _read_json(result_index_path, "reviewer comparison result index")
    if (
        result_index.get("contract") != RESULT_INDEX_CONTRACT
        or result_index.get("schema_version") != 2
        or result_index.get("preregistration_id") != prereg["preregistration_id"]
    ):
        raise ValidationError("result index identity is invalid")
    for field in ("authorization_id", "authorized_at", "calibration_frozen_at"):
        if not isinstance(result_index.get(field), str) or not result_index[field].strip():
            raise ValidationError(f"result index requires explicit {field}")
    holdout_cleared = result_index.get("holdout_cleared") is True
    if holdout_cleared:
        if not isinstance(result_index.get("holdout_cleared_at"), str) or not result_index["holdout_cleared_at"].strip():
            raise ValidationError("cleared holdout requires explicit holdout_cleared_at")
    elif result_index.get("holdout_cleared_at") is not None:
        raise ValidationError("sealed holdout must not have holdout_cleared_at")
    results = result_index.get("results")
    if not isinstance(results, list) or len(results) != len(prereg["slots"]):
        raise ValidationError("result index must cover every preregistered slot")
    by_slot = {item.get("slot_id"): item for item in results if isinstance(item, dict)}
    if set(by_slot) != {slot["slot_id"] for slot in prereg["slots"]}:
        raise ValidationError("result index slots are missing or duplicated")
    review_policy, review_policy_sha256 = load_translation_review_policy(manifest.root)
    observations: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    slot_reports = []
    structure_failures: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    from .review import validate_review_bundle
    for slot in prereg["slots"]:
        result = by_slot[slot["slot_id"]]
        status = result.get("status")
        if status not in {"pending", "success", "content-structure-failure"}:
            raise ValidationError(f"slot {slot['slot_id']} has invalid status")
        if status == "pending":
            if slot["split"] == "calibration" or holdout_cleared:
                raise ValidationError(f"required slot {slot['slot_id']} is still pending")
            if result.get("assessment") is not None or result.get("run_report") is not None:
                raise ValidationError(f"pending slot {slot['slot_id']} must not bind artifacts")
            continue
        if slot["split"] == "holdout" and not holdout_cleared:
            raise ValidationError("sealed holdout result is present before clearance")
        if not isinstance(result.get("run_report"), str):
            raise ValidationError(f"slot {slot['slot_id']} has no run report")
        bundle = validate_review_bundle(manifest, Path(slot["bundle"]))
        if bundle["bundle_id"] != slot["bundle_id"]:
            raise ValidationError(f"slot {slot['slot_id']} bundle identity is invalid")
        descriptor = next(
            (value for value in prereg["bundles"] if value["bundle_id"] == slot["bundle_id"]),
            None,
        )
        if descriptor is None or descriptor["bundle_sha256"] != _sha(bundle):
            raise ValidationError(f"slot {slot['slot_id']} bundle digest is invalid")
        run_report = _read_json(Path(result["run_report"]), "Pi run report")
        if any(run_report.get(key) != slot[key] for key in ("provider", "model", "thinking", "bundle_id")):
            raise ValidationError(f"slot {slot['slot_id']} run identity is invalid")
        provider_message = translation_provider_message(bundle)
        payload_sha256 = hashlib.sha256(provider_message).hexdigest()
        expected_cache_key = _review_cache_key(
            bundle_id=slot["bundle_id"],
            provider=slot["provider"],
            model=slot["model"],
            thinking=slot["thinking"],
            prompt_sha256=prereg["prompt_sha256"],
            strict=True,
            review_contract=TRANSLATION_REVIEW_ASSESSMENT_CONTRACT,
            policy_sha256=review_policy_sha256,
            normalizer_contract=TRANSLATION_REVIEW_NORMALIZER_CONTRACT,
            payload_sha256=payload_sha256,
            runner_contract=TRANSLATION_REVIEW_RUNNER_CONTRACT,
        )
        if (
            run_report.get("tool_version") != TOOL_VERSION
            or run_report.get("review_contract") != TRANSLATION_REVIEW_ASSESSMENT_CONTRACT
            or run_report.get("prompt_sha256") != prereg["prompt_sha256"]
            or run_report.get("runner_contract") != TRANSLATION_REVIEW_RUNNER_CONTRACT
            or run_report.get("payload_sha256") != payload_sha256
            or run_report.get("payload_bytes") != len(provider_message)
            or run_report.get("result_cache_key") != expected_cache_key
            or run_report.get("strict") is not True
        ):
            raise ValidationError(f"slot {slot['slot_id']} runner lineage is invalid")
        if run_report.get("cache_decision") != "disabled":
            raise ValidationError(f"slot {slot['slot_id']} must be a no-cache run")
        attempts = run_report.get("attempts")
        if type(attempts) is not int or not 1 <= attempts <= 1 + policy["connection_failure_retry_limit"]:
            raise ValidationError(f"slot {slot['slot_id']} attempts exceed preregistration")
        if status == "content-structure-failure":
            if result.get("assessment") is not None or run_report.get("ok") is not False:
                raise ValidationError(f"failed slot {slot['slot_id']} must bind no assessment and an unsuccessful report")
            if (
                run_report.get("failure_kind") != "content-structure"
                or run_report.get("pi_returncode") != 0
                or not _is_sha(run_report.get("raw_output_sha256"))
                or not isinstance(run_report.get("error"), str)
            ):
                raise ValidationError(f"failed slot {slot['slot_id']} lacks content-failure evidence")
            structure_failures[slot["split"]][slot["reviewer"]] += 1
            slot_reports.append({
                "slot_id": slot["slot_id"], "split": slot["split"], "reviewer": slot["reviewer"],
                "status": status, "attempts": attempts, "elapsed_seconds": run_report.get("elapsed_seconds"),
                "payload_bytes": run_report.get("payload_bytes"), "usage": run_report.get("usage"),
                "raw_output_sha256": run_report["raw_output_sha256"], "error": run_report["error"],
            })
            continue
        if not isinstance(result.get("assessment"), str) or run_report.get("ok") is not True:
            raise ValidationError(f"successful slot {slot['slot_id']} must bind a successful assessment")
        evaluator = make_evaluator_identity(
            provider=slot["provider"], model=slot["model"], thinking=slot["thinking"],
            prompt_sha256=prereg["prompt_sha256"], policy_sha256=review_policy_sha256,
            bundle=bundle,
        )
        assessment = _read_json(Path(result["assessment"]), "translation assessment")
        _summary, normalized = revalidate_translation_assessment(
            bundle=bundle, assessment=assessment, policy=review_policy,
            policy_sha256=review_policy_sha256, evaluator=evaluator,
        )
        key = f"{slot['split']}:{slot['round']}:{slot['reviewer']}"
        for item in normalized["items"]:
            if item["revision_id"] in observations[key]:
                raise ValidationError(f"slot {slot['slot_id']} duplicates a revision")
            observations[key][item["revision_id"]] = item
        usage = run_report.get("usage")
        if usage is not None and not isinstance(usage, dict):
            raise ValidationError(f"slot {slot['slot_id']} usage must be an object")
        slot_reports.append({
            "slot_id": slot["slot_id"], "split": slot["split"],
            "reviewer": slot["reviewer"], "status": status, "attempts": attempts,
            "elapsed_seconds": run_report.get("elapsed_seconds"),
            "payload_bytes": run_report.get("payload_bytes"),
            "usage": usage,
        })
    calibration_slots = [slot for slot in prereg["slots"] if slot["split"] == "calibration"]
    calibration_successes = sum(
        report["status"] == "success" for report in slot_reports if report["split"] == "calibration"
    )
    clearance_checks: dict[str, dict[str, Any]] = {}
    gold = _read_json(gold_path, "frozen comparison Gold")
    if (
        gold.get("contract") != GOLD_CONTRACT
        or gold.get("schema_version") != 2
        or gold.get("gold_id") != prereg.get("gold_id")
        or gold.get("gold_id")
        != _sha({key: value for key, value in gold.items() if key != "gold_id"})
    ):
        raise ValidationError("frozen comparison Gold identity is invalid")
    pool_candidates: dict[str, dict[str, Any]] = {}
    for descriptor in prereg["bundles"]:
        bundle = _read_json(Path(descriptor["path"]), "translation bundle")
        for item in bundle["items"]:
            pool_candidates[item["revision_id"]] = item
    calibration_gold = [
        {**pool_candidates[item["revision_id"]], **item}
        for item in gold["items"] if item["split"] == "calibration" and not item["controlled"]
    ]
    for model in policy["models"]:
        alias = model["alias"]
        failures = structure_failures["calibration"][alias]
        left = observations.get(f"calibration:1:{alias}")
        right = observations.get(f"calibration:2:{alias}")
        schema_coverage = _ratio(
            sum(report["status"] == "success" for report in slot_reports if report["split"] == "calibration" and report["reviewer"] == alias),
            sum(slot["reviewer"] == alias for slot in calibration_slots),
        )
        exact_claim_jaccard = semantic_claim_jaccard = None
        assessment_state_agreement = item_flag_agreement = None
        no_difference_false_positive_rate = context_state_accuracy = None
        if failures == 0 and isinstance(left, dict) and isinstance(right, dict):
            expected = {item["revision_id"] for item in calibration_gold}
            if set(left) == expected and set(right) == expected:
                left_claims = {finding["finding_key"] for item in left.values() for finding in item["findings"]}
                right_claims = {finding["finding_key"] for item in right.values() for finding in item["findings"]}
                union = left_claims | right_claims
                exact_claim_jaccard = (
                    _ratio(len(left_claims & right_claims), len(union)) if union else 1.0
                )
                semantic_claim_jaccard = _semantic_claim_jaccard(
                    left, right, calibration_gold
                )
                assessment_state_agreement = _ratio(
                    sum(
                        left[key]["assessment_state"] == right[key]["assessment_state"]
                        for key in left
                    ),
                    len(left),
                )
                item_flag_agreement = _ratio(
                    sum(bool(left[key]["findings"]) == bool(right[key]["findings"]) for key in left),
                    len(left),
                )
                left_metrics = _metrics(calibration_gold, left)
                right_metrics = _metrics(calibration_gold, right)
                no_difference_false_positive_rate = max(
                    left_metrics["no_difference_false_positive_rate"],
                    right_metrics["no_difference_false_positive_rate"],
                )
                context_state_accuracy = min(
                    left_metrics["context_state_accuracy"],
                    right_metrics["context_state_accuracy"],
                )
        passed = (
            schema_coverage == policy["eligibility"]["schema_coverage"]
            and failures <= policy["eligibility"]["structure_failures_max"]
            and semantic_claim_jaccard is not None
            and semantic_claim_jaccard >= policy["eligibility"]["semantic_claim_jaccard_min"]
            and item_flag_agreement is not None
            and item_flag_agreement >= policy["eligibility"]["item_flag_agreement_min"]
            and context_state_accuracy is not None
            and context_state_accuracy >= policy["eligibility"]["context_state_accuracy_min"]
            and no_difference_false_positive_rate is not None
            and no_difference_false_positive_rate
            <= policy["eligibility"]["no_difference_false_positive_rate_max"]
        )
        clearance_checks[alias] = {
            "schema_coverage": schema_coverage, "structure_failures": failures,
            "exact_claim_jaccard": exact_claim_jaccard,
            "semantic_claim_jaccard": semantic_claim_jaccard,
            "assessment_state_agreement": assessment_state_agreement,
            "item_flag_agreement": item_flag_agreement,
            "context_state_accuracy": context_state_accuracy,
            "no_difference_false_positive_rate": no_difference_false_positive_rate,
            "passed": passed,
        }
    calibration_clearance = "cleared" if all(value["passed"] for value in clearance_checks.values()) else "denied"
    if holdout_cleared and calibration_clearance != "cleared":
        raise ValidationError("holdout clearance contradicts frozen calibration eligibility")
    validation = {
        "contract": VALIDATION_CONTRACT, "schema_version": 2,
        "preregistration_id": prereg["preregistration_id"],
        "preregistration": str(preregistration_path.resolve()),
        "result_index": str(result_index_path.resolve()),
        "slot_reports": slot_reports,
        "holdout_cleared": holdout_cleared,
        "calibration_clearance": calibration_clearance,
        "calibration_checks": clearance_checks,
        "calibration_schema_coverage": _ratio(calibration_successes, len(calibration_slots)),
        "structure_failures": {split: dict(values) for split, values in structure_failures.items()},
        "observations": dict(observations),
    }
    validation["validation_id"] = _sha(validation)
    run_directory = create_quality_run_directory(manifest.root, "reviewer-comparison-validate")
    output = run_directory / "validation.json"
    write_json(output, validation)
    return {"validation_id": validation["validation_id"], "validation": str(output), "slots": len(slot_reports), "run_directory": str(run_directory)}


def run_report(*, validation_path: Path) -> dict[str, Any]:
    validation = _read_json(validation_path, "reviewer comparison validation")
    if validation.get("contract") != VALIDATION_CONTRACT or validation.get("validation_id") != _sha({key: value for key, value in validation.items() if key != "validation_id"}):
        raise ValidationError("reviewer comparison validation identity is invalid")
    prereg = _read_json(Path(validation["preregistration"]), "reviewer comparison preregistration")
    if (
        prereg.get("contract") != PREREG_CONTRACT
        or prereg.get("schema_version") != 2
        or validation.get("preregistration_id") != prereg.get("preregistration_id")
        or prereg.get("preregistration_id")
        != _sha({key: value for key, value in prereg.items() if key != "preregistration_id"})
    ):
        raise ValidationError("reviewer comparison preregistration identity is invalid")
    gold_path = Path(preregistration_gold_path(prereg))
    gold = _read_json(gold_path, "frozen comparison Gold")
    if hashlib.sha256(gold_path.read_bytes()).hexdigest() != prereg["gold_sha256"]:
        raise ValidationError("frozen comparison Gold bytes are stale")
    if (
        gold.get("contract") != GOLD_CONTRACT
        or gold.get("schema_version") != 2
        or gold.get("gold_id") != prereg["gold_id"]
        or gold.get("gold_id")
        != _sha({key: value for key, value in gold.items() if key != "gold_id"})
    ):
        raise ValidationError("frozen comparison Gold identity is invalid")
    bundle_path = Path(prereg["bundles"][0]["path"]).resolve()
    artifact_root = next(
        (path for path in (bundle_path, *bundle_path.parents) if path.name == ".artifacts"),
        None,
    )
    repository_root = artifact_root.parent if artifact_root is not None else Path.cwd()
    comparison_policy, policy_sha256 = load_comparison_policy(repository_root)
    if (
        prereg.get("policy_sha256") != policy_sha256
        or prereg.get("tool_version") != TOOL_VERSION
        or prereg.get("implementation_sha256") != _implementation_sha256(repository_root)
    ):
        raise ValidationError("reviewer comparison report implementation is stale")
    pool_candidates = {}
    for descriptor in prereg["bundles"]:
        bundle = _read_json(Path(descriptor["path"]), "translation bundle")
        for item in bundle["items"]:
            pool_candidates[item["revision_id"]] = item
    gold_items = []
    for item in gold["items"]:
        gold_items.append({**pool_candidates[item["revision_id"]], **item})
    if validation.get("holdout_cleared") is False:
        decision = f"calibration-{validation.get('calibration_clearance', 'invalid')}"
        report = {
            "contract": REPORT_CONTRACT, "schema_version": 2,
            "validation_id": validation["validation_id"],
            "stage": "calibration", "metrics": {}, "stability": {},
            "eligibility": {
                alias: values.get("passed")
                for alias, values in validation.get("calibration_checks", {}).items()
            },
            "calibration_checks": validation.get("calibration_checks", {}),
            "decision": decision,
            "operational": {},
            "notes": [
                "Holdout remained sealed; no holdout quality comparison was computed.",
                "Content/structure failures are retained as failed slots and are not normalized or replaced.",
                "Only no-substantive-difference items contribute to the false-positive gate.",
                "Additional findings on non-exhaustive Gold remain unadjudicated.",
            ],
        }
        report["report_id"] = _sha(report)
        output = validation_path.parent / "comparison-report.json"
        write_json(output, report)
        return {"report_id": report["report_id"], "decision": decision, "report": str(output)}
    metrics: dict[str, Any] = {}
    for split in ("calibration", "holdout"):
        split_gold = [item for item in gold_items if item["split"] == split and not item["controlled"]]
        for model in comparison_policy["models"]:
            runs = comparison_policy["splits"][split]["runs"]
            run_metrics = []
            for run in range(1, runs + 1):
                key = f"{split}:{run}:{model['alias']}"
                observed = validation["observations"].get(key)
                if not isinstance(observed, dict) or set(observed) != {item["revision_id"] for item in split_gold}:
                    raise ValidationError(f"observation coverage is incomplete for {key}")
                run_metrics.append(_metrics(split_gold, observed))
            metrics[f"{split}:{model['alias']}"] = run_metrics
    stability = {}
    calibration_gold = [
        item
        for item in gold_items
        if item["split"] == "calibration" and not item["controlled"]
    ]
    for model in comparison_policy["models"]:
        alias = model["alias"]
        left = validation["observations"][f"calibration:1:{alias}"]
        right = validation["observations"][f"calibration:2:{alias}"]
        left_claims = {finding["finding_key"] for item in left.values() for finding in item["findings"]}
        right_claims = {finding["finding_key"] for item in right.values() for finding in item["findings"]}
        union = left_claims | right_claims
        state_agreement = sum(left[key]["assessment_state"] == right[key]["assessment_state"] for key in left)
        flag_agreement = sum(
            bool(left[key]["findings"]) == bool(right[key]["findings"])
            for key in left
        )
        stability[alias] = {
            "exact_claim_jaccard": (
                _ratio(len(left_claims & right_claims), len(union)) if union else 1.0
            ),
            "semantic_claim_jaccard": _semantic_claim_jaccard(
                left, right, calibration_gold
            ),
            "assessment_state_agreement": _ratio(state_agreement, len(left)),
            "item_flag_agreement": _ratio(flag_agreement, len(left)),
        }
    eligibility = {}
    for model in comparison_policy["models"]:
        alias = model["alias"]
        holdout = metrics[f"holdout:{alias}"][0]
        eligibility[alias] = (
            stability[alias]["semantic_claim_jaccard"]
            >= comparison_policy["eligibility"]["semantic_claim_jaccard_min"]
            and stability[alias]["item_flag_agreement"]
            >= comparison_policy["eligibility"]["item_flag_agreement_min"]
            and holdout["context_state_accuracy"]
            >= comparison_policy["eligibility"]["context_state_accuracy_min"]
            and holdout["no_difference_false_positive_rate"]
            <= comparison_policy["eligibility"]["no_difference_false_positive_rate_max"]
        )
    operational = {}
    for model in comparison_policy["models"]:
        alias = model["alias"]
        values = [value for value in validation["slot_reports"] if value["reviewer"] == alias]
        usage_values = [value["usage"] for value in values if isinstance(value.get("usage"), dict)]
        operational[alias] = {
            "content_slots": len(values),
            "external_transfer_attempts": sum(value["attempts"] for value in values),
            "elapsed_seconds": round(sum(value["elapsed_seconds"] for value in values if isinstance(value.get("elapsed_seconds"), (int, float))), 6),
            "payload_bytes": sum(value["payload_bytes"] for value in values if type(value.get("payload_bytes")) is int),
            "usage_available_slots": len(usage_values),
            "input_tokens": sum(value.get("input_tokens", 0) for value in usage_values if type(value.get("input_tokens", 0)) is int),
            "output_tokens": sum(value.get("output_tokens", 0) for value in usage_values if type(value.get("output_tokens", 0)) is int),
            "estimated_cost_usd": round(sum(value.get("estimated_cost_usd", 0.0) for value in usage_values if isinstance(value.get("estimated_cost_usd", 0.0), (int, float))), 6),
        }
    a, b = [model["alias"] for model in comparison_policy["models"]]
    am = metrics[f"holdout:{a}"][0]; bm = metrics[f"holdout:{b}"][0]
    decision = "no-decisive-quality-winner-retain-deepseek"
    if eligibility[a] != eligibility[b]:
        decision = f"winner:{a if eligibility[a] else b}"
    elif not eligibility[a]:
        decision = "single-model-reviewer-insufficient"
    else:
        major_delta = bm["major_items_found"] - am["major_items_found"]
        no_difference_delta = (
            bm["no_difference_false_positive_items"]
            - am["no_difference_false_positive_items"]
        )
        threshold = comparison_policy["winner"]
        if abs(major_delta) >= threshold["additional_major_min"]:
            candidate = b if major_delta > 0 else a
            added_fp = (
                no_difference_delta if candidate == b else -no_difference_delta
            )
            if added_fp <= threshold["additional_no_difference_false_positives_max"]:
                decision = f"winner:{candidate}"
        if decision.startswith("no-decisive"):
            recall_delta = bm["true_positive_findings"] - am["true_positive_findings"]
            candidate = b if recall_delta > 0 else a
            winner_metrics = bm if candidate == b else am
            loser_metrics = am if candidate == b else bm
            precision_drop = 100 * ((loser_metrics["precision"] or 0) - (winner_metrics["precision"] or 0))
            if (
                am["precision_complete"]
                and bm["precision_complete"]
                and abs(recall_delta) >= threshold["additional_substantive_min"]
                and precision_drop <= threshold["precision_drop_percentage_points_max"]
            ):
                decision = f"winner:{candidate}"
    report = {
        "contract": REPORT_CONTRACT, "schema_version": 2,
        "validation_id": validation["validation_id"], "metrics": metrics,
        "stability": stability, "eligibility": eligibility, "decision": decision,
        "operational": operational,
        "notes": [
            "Natural canonical items only; controlled auxiliary results are excluded.",
            "Risk-enriched results do not estimate corpus prevalence.",
            "Only exhaustive Gold and no-substantive-difference items contribute false positives.",
            "Additional findings on non-exhaustive items remain unadjudicated.",
        ],
    }
    report["report_id"] = _sha(report)
    output = validation_path.parent / "comparison-report.json"
    write_json(output, report)
    return {"report_id": report["report_id"], "decision": decision, "report": str(output)}


def preregistration_gold_path(preregistration: dict[str, Any]) -> str:
    value = preregistration.get("gold")
    if not isinstance(value, str) or not value:
        raise ValidationError("reviewer comparison preregistration has no Gold path")
    return value
