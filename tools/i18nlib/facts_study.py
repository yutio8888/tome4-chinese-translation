"""Isolated Facts causal-study harness using the supplemental-only v2 data contract.

This module is deliberately independent from evaluator v1-v3 and the v4
draft.  It builds blinded arm bundles, validates exhaustive research gold,
freezes an exact 33-slot schedule, validates assessments, constructs the
host-only B+F union, and reports preregistered causal contrasts.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import shutil
import stat
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from .config import Manifest
from .errors import ConfigurationError, ValidationError
from .quality import create_quality_run_directory
from .quality_v2 import canonical_sha256, normalize_evidence, read_json_object
from .report import write_json


SAMPLE_CONTRACT = "tome4-quality-facts-study-sample-v1"
PACKET_CONTRACT = "tome4-quality-fact-packet-v2"
LEGACY_PACKET_CONTRACT = "tome4-quality-fact-packet-v1"
FACTS_AUTHOR_BUNDLE_CONTRACT = "tome4-quality-facts-author-bundle-v2"
GOLD_CONTRACT = "tome4-quality-facts-study-gold-v1"
BUNDLE_CONTRACT = "tome4-quality-facts-study-bundle-v1"
ASSESSMENT_CONTRACT = "tome4-quality-facts-study-assessment-v1"
PREREG_CONTRACT = "tome4-quality-facts-study-preregistration-v1"
REPORT_CONTRACT = "tome4-quality-facts-study-report-v1"
PROTOCOL_CONTRACT = "tome4-quality-facts-study-protocol-v2"
HISTORICAL_EXCLUSIONS_CONTRACT = "tome4-quality-facts-study-exclusions-v1"

ARMS = ("A", "B", "C", "D", "N", "L", "F")
LUNA_ARMS = ARMS
DEEPSEEK_ARMS = ("B", "D", "L", "F")
FACT_ARMS = frozenset(("C", "D", "L", "F"))
NO_FACT_ARMS = frozenset(("A", "B", "N"))
CHECKLIST_ARMS = frozenset(("B", "D", "N", "L"))
FACT_TYPES = frozenset(
    ("term-authority", "mechanism", "condition", "entity-relation", "ui-role")
)
SUPPLEMENTAL_PROVENANCE_KINDS = frozenset(
    ("terminology", "public-source", "versioned-context")
)
OPAQUE_FACT_ID_PATTERN = re.compile(r"fact-[0-9a-f]{16}\Z")
ERROR_FAMILIES = frozenset(("semantic", "terminology", "ui"))
PHENOMENA = frozenset(
    (
        "number", "number-range", "unit", "condition", "polarity",
        "entity-role", "scope", "trigger-timing", "omission", "addition",
        "terminology", "proper-name", "ambiguity", "other",
    )
)
MEANING_CHANGES = frozenset(
    (
        "omitted", "added", "weakened", "strengthened", "reversed",
        "reassigned", "made-ambiguous", "unknown",
    )
)
ITEM_KINDS = frozenset(("semantic", "term", "mechanics", "ui", "localization"))
STRATA = frozenset(
    ("ordinary-semantic", "term-name", "condition-number-mechanism", "ui", "acceptable-localization")
)


def study_harness_identity() -> dict[str, str]:
    """Bind the complete repository-local Python runner implementation.

    Hashing every i18nlib module is intentionally conservative: the external
    runner calls shared command, environment, subprocess, decoding, artifact,
    and manifest helpers.  An unrelated helper change may invalidate a frozen
    preregistration, but no local execution-semantic change can remain hidden.
    """
    module_root = Path(__file__).parent
    tools_root = module_root.parent
    files = sorted(module_root.glob("*.py")) + [tools_root / "pi-quality-facts-study"]
    return {
        str(path.relative_to(tools_root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in files
    }


def study_harness_sha256() -> str:
    return canonical_sha256(study_harness_identity())


def _tree_identity(root: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    file_count = byte_count = 0
    for path in sorted(root.rglob("*"), key=lambda value: str(value.relative_to(root))):
        if path.is_dir() and not path.is_symlink():
            continue
        relative = str(path.relative_to(root)).encode("utf-8")
        link = os.readlink(path).encode("utf-8") if path.is_symlink() else b""
        resolved = path.resolve()
        if not resolved.is_file():
            raise ConfigurationError(f"runtime package contains a non-file link: {path}")
        content_digest = hashlib.sha256()
        size = 0
        with resolved.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                content_digest.update(chunk)
                size += len(chunk)
        mode = stat.S_IMODE(resolved.stat().st_mode)
        digest.update(relative + b"\0" + link + b"\0" + str(mode).encode() + b"\0")
        digest.update(str(size).encode() + b"\0" + content_digest.digest())
        file_count += 1
        byte_count += size
    return {"root": str(root), "sha256": digest.hexdigest(), "file_count": file_count, "byte_count": byte_count}


def _nearest_marker_root(path: Path, marker: str) -> Path:
    for parent in (path.parent, *path.parents):
        if (parent / marker).is_file():
            return parent
    raise ConfigurationError(f"cannot locate {marker} for runtime executable: {path}")


def _runtime_file_set_identity(paths: Iterable[Path], label: str) -> dict[str, Any]:
    """Hash an explicit runtime file closure without traversing unrelated OS trees."""
    files = sorted({path.resolve() for path in paths}, key=str)
    if not files:
        raise ConfigurationError(f"runtime file set is empty: {label}")
    digest = hashlib.sha256()
    byte_count = 0
    for path in files:
        if not path.is_file():
            raise ConfigurationError(f"runtime dependency is not a regular file: {path}")
        content_digest = hashlib.sha256()
        size = 0
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                content_digest.update(chunk)
                size += len(chunk)
        mode = stat.S_IMODE(path.stat().st_mode)
        digest.update(str(path).encode("utf-8") + b"\0")
        digest.update(str(mode).encode() + b"\0")
        digest.update(str(size).encode() + b"\0")
        digest.update(content_digest.digest())
        byte_count += size
    return {
        "root": label,
        "sha256": digest.hexdigest(),
        "file_count": len(files),
        "byte_count": byte_count,
    }


def _node_runtime_identity(node_path: Path) -> dict[str, Any]:
    """Bind Homebrew's package tree or Linux's exact dynamic-library closure."""
    try:
        return _tree_identity(_nearest_marker_root(node_path, "INSTALL_RECEIPT.json"))
    except ConfigurationError:
        ldd = shutil.which("ldd")
        if not ldd:
            raise ConfigurationError(
                f"cannot identify transitive Node runtime for executable: {node_path}"
            )
        result = subprocess.run(
            [ldd, str(node_path)], capture_output=True, text=True, check=False
        )
        if result.returncode != 0 or "not found" in result.stdout:
            raise ConfigurationError(
                f"cannot resolve transitive Node runtime for executable: {node_path}"
            )
        dependencies = {node_path}
        for raw_line in result.stdout.splitlines():
            line = raw_line.strip()
            if "=>" in line:
                candidate = line.split("=>", 1)[1].strip().split(" ", 1)[0]
            else:
                candidate = line.split(" ", 1)[0]
            if candidate.startswith("/"):
                dependencies.add(Path(candidate))
        return _runtime_file_set_identity(
            dependencies, f"ldd-runtime:{node_path}"
        )


def pi_executable_identity(executable: str | None = None) -> dict[str, Any]:
    candidate = executable or shutil.which("pi")
    if not candidate:
        raise ConfigurationError("pi is required to freeze a Facts-study preregistration")
    path = Path(candidate).expanduser().resolve()
    if not path.is_file():
        raise ConfigurationError(f"Pi executable is not a regular file: {path}")
    package_root = _nearest_marker_root(path, "package.json")
    node_candidate = shutil.which("node")
    if not node_candidate:
        raise ConfigurationError("node is required to freeze the Pi runtime identity")
    node_path = Path(node_candidate).resolve()
    return {
        "path": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "package_tree": _tree_identity(package_root),
        "node_path": str(node_path),
        "node_sha256": hashlib.sha256(node_path.read_bytes()).hexdigest(),
        "node_tree": _node_runtime_identity(node_path),
    }


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _exact(value: dict[str, Any], fields: Iterable[str], where: str) -> None:
    expected = set(fields)
    unknown = sorted(set(value) - expected)
    missing = sorted(expected - set(value))
    if unknown:
        raise ValidationError(f"{where} has unknown fields: {', '.join(unknown)}")
    if missing:
        raise ValidationError(f"{where} is missing fields: {', '.join(missing)}")


def _string(value: Any, where: str, *, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value):
        raise ValidationError(f"{where} must be a {'string' if empty else 'non-empty string'}")
    return value


def _sha(value: Any, where: str) -> str:
    text = _string(value, where)
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise ValidationError(f"{where} must be a lowercase SHA-256")
    return text


def _enum(value: Any, allowed: Iterable[str], where: str) -> str:
    if not isinstance(value, str) or value not in set(allowed):
        raise ValidationError(f"{where} must be one of: {', '.join(sorted(allowed))}")
    return value


def _id(value: Any, where: str) -> str:
    return _sha(value, where)


def load_protocol(manifest: Manifest) -> dict[str, Any]:
    path = manifest.root / "i18n" / "quality" / "facts-study-v2.json"
    value = read_json_object(path, "facts study protocol")
    if value.get("contract") != PROTOCOL_CONTRACT or value.get("schema_version") != 1:
        raise ConfigurationError(f"unsupported facts study protocol: {path}")
    if value.get("arms") != list(ARMS) or value.get("item_count") != 20:
        raise ConfigurationError("facts study protocol must freeze seven arms and 20 items")
    if value.get("max_external_slots") != 33 or value.get("shard_count") != 1:
        raise ConfigurationError("facts study protocol must freeze 33 one-shard slots")
    expected_policy = {
        "packet_contract": PACKET_CONTRACT,
        "facts_author_bundle_contract": FACTS_AUTHOR_BUNDLE_CONTRACT,
        "min_facts_per_item": 0,
        "max_facts_per_item": 4,
        "supplemental_only": True,
        "common_input_restatements": "forbidden",
        "allowed_provenance_kinds": sorted(SUPPLEMENTAL_PROVENANCE_KINDS),
        "addressed_definition": "claim-cites-directly-supporting-supplemental-fact",
    }
    if value.get("fact_policy") != expected_policy:
        raise ConfigurationError("facts study protocol has an unsupported supplemental Fact policy")
    if value.get("historical_exclusions") != "facts-study-exclusions-v1.json":
        raise ConfigurationError("facts study protocol does not bind the historical exclusion registry")
    return value


def load_historical_exclusions(manifest: Manifest) -> set[str]:
    path = manifest.root / "i18n" / "quality" / "facts-study-exclusions-v1.json"
    value = read_json_object(path, "facts study historical exclusions")
    _exact(value, ("contract", "schema_version", "lineages"), "facts study historical exclusions")
    if value["contract"] != HISTORICAL_EXCLUSIONS_CONTRACT or value["schema_version"] != 1:
        raise ConfigurationError(f"unsupported Facts study exclusion registry: {path}")
    if not isinstance(value["lineages"], list) or not value["lineages"]:
        raise ConfigurationError("Facts study exclusion registry must contain at least one lineage")
    revision_ids: set[str] = set()
    for index, lineage in enumerate(value["lineages"]):
        where = f"facts study historical exclusions.lineages[{index}]"
        _exact(lineage, ("study_id", "status", "reason", "revision_ids", "revision_ids_sha256"), where)
        _id(lineage["study_id"], f"{where}.study_id")
        _string(lineage["status"], f"{where}.status")
        _string(lineage["reason"], f"{where}.reason")
        ids = lineage["revision_ids"]
        if not isinstance(ids, list) or ids != sorted(set(ids)):
            raise ConfigurationError(f"{where}.revision_ids must be a sorted unique list")
        for rid in ids:
            _id(rid, f"{where}.revision_ids")
        if canonical_sha256(ids) != lineage["revision_ids_sha256"]:
            raise ConfigurationError(f"{where} revision digest mismatch")
        if revision_ids & set(ids):
            raise ConfigurationError("Facts study exclusion lineages must not overlap")
        revision_ids.update(ids)
    return revision_ids


def validate_historical_exclusions(manifest: Manifest, sample: dict[str, Any]) -> None:
    required = load_historical_exclusions(manifest)
    declared = set(sample["excluded_revision_ids"])
    selected = {item["revision_id"] for item in sample["items"]}
    if not required <= declared or required & selected:
        raise ValidationError(
            "Facts study sample does not bind every required historical pilot exclusion"
        )


def load_arm_prompt(manifest: Manifest, arm: str) -> str:
    _enum(arm, ARMS, "arm")
    path = manifest.root / "i18n" / "prompts" / f"pi-quality-facts-study-{arm.lower()}.md"
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ConfigurationError(f"cannot read facts study arm {arm} prompt: {path}") from error


def _public_item(raw: dict[str, Any], index: int) -> dict[str, Any]:
    profile = raw.get("profile")
    item_kind = {
        "term-name": "term", "mechanics": "mechanics", "ui": "ui",
        "dialogue": "semantic", "narrative": "semantic", "runtime-log": "semantic",
    }.get(profile, "localization")
    stratum = {
        "term": "term-name", "mechanics": "condition-number-mechanism",
        "ui": "ui", "localization": "acceptable-localization",
    }.get(item_kind, "ordinary-semantic")
    neighbors = raw.get("context_neighbors") or []
    bounded = [
        {"relative_index": entry.get("relative_index"), "source": entry.get("source", ""), "target": entry.get("target", "")}
        for entry in neighbors[:2]
        if isinstance(entry, dict)
    ]
    return {
        "index": index,
        "revision_id": raw["revision_id"],
        "source": raw["source"],
        "target": raw["target"],
        "item_kind": item_kind,
        "source_tag": raw.get("source_tag") or "",
        "bounded_context": bounded,
        "stratum": stratum,
    }


def _read_inventory(path: Path) -> tuple[list[dict[str, Any]], str]:
    try:
        raw = path.read_bytes()
        rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"cannot read facts study inventory: {path}: {error}") from error
    if not rows or any(not isinstance(row, dict) for row in rows):
        raise ValidationError("facts study inventory must contain JSON objects")
    return rows, hashlib.sha256(raw).hexdigest()


def _revision_ids_from_artifact(path: Path) -> set[str]:
    value = read_json_object(path, "facts study exclusion artifact")
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


def build_candidate_sample(
    *, inventory_path: Path, exclusion_paths: list[Path], seed: str,
    required_excluded_ids: Iterable[str] = (),
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rows, inventory_sha = _read_inventory(inventory_path)
    excluded: set[str] = set(required_excluded_ids)
    for path in exclusion_paths:
        excluded.update(_revision_ids_from_artifact(path))
    eligible = [row for row in rows if row.get("revision_id") not in excluded]
    if len(eligible) < 20:
        raise ValidationError("fewer than 20 inventory revisions remain after exclusions")
    rng = random.Random(seed)
    rng.shuffle(eligible)
    # A deterministic round-robin prevents a single profile from dominating the authoring pool.
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        groups[str(row.get("profile") or "other")].append(row)
    if seed.startswith("tome4-facts-study-v2-long-source-v1"):
        # Keep the profile round-robin, but make the selection intent encoded in
        # the frozen seed reproducible.  The score peaks at 1,500 characters so
        # a single book-length entry cannot consume most of the one-shard study.
        def long_source_score(row: dict[str, Any]) -> int:
            length = len(str(row.get("source") or ""))
            return length if length <= 1500 else 1500 - (length - 1500) * 2

        for entries in groups.values():
            entries.sort(key=long_source_score)
    selected: list[dict[str, Any]] = []
    selected_texts: set[tuple[str, str]] = set()
    keys = sorted(groups)
    while len(selected) < 20:
        progressed = False
        for key in keys:
            while groups[key] and len(selected) < 20:
                candidate = groups[key].pop()
                text_identity = (
                    str(candidate.get("source") or ""),
                    str(candidate.get("target") or ""),
                )
                if text_identity in selected_texts:
                    continue
                selected.append(candidate)
                selected_texts.add(text_identity)
                progressed = True
                break
        if not progressed:
            break
    items = [_public_item(row, index) for index, row in enumerate(selected)]
    study_id = canonical_sha256(
        {"contract": SAMPLE_CONTRACT, "seed": seed, "inventory_sha256": inventory_sha,
         "excluded": sorted(excluded), "items": items}
    )
    sample = {
        "contract": SAMPLE_CONTRACT, "schema_version": 1, "study_id": study_id,
        "seed": seed, "inventory_sha256": inventory_sha,
        "excluded_revision_ids": sorted(excluded),
        "exclusion_revision_ids_sha256": canonical_sha256(sorted(excluded)), "items": items,
    }
    facts = {
        "contract": PACKET_CONTRACT, "schema_version": 1, "study_id": study_id,
        "packet_kind": "facts", "status": "draft", "non_exhaustive": True,
        "supplemental_only": True,
        "authoring_lineage": {
            "role": "facts-author", "actor_id": "", "target_defects_seen": False,
            "gold_seen": False, "common_input_restatements_excluded": True,
            "source_inputs_sha256": "",
        },
        "items": [{"revision_id": item["revision_id"], "facts": []} for item in items],
    }
    gold = {
        "contract": GOLD_CONTRACT, "schema_version": 1, "study_id": study_id,
        "status": "draft", "review_lineage": {
            "reviewer_ids": ["", ""], "review_artifact_sha256s": ["", ""],
            "adjudicator_id": "", "adjudication_artifact_sha256": "",
        },
        "items": [
            {"revision_id": item["revision_id"], "clean": False, "fact_trap": False,
             "acceptable_localization": False, "claims": []}
            for item in items
        ],
    }
    return sample, facts, gold


def validate_sample(value: dict[str, Any]) -> dict[str, Any]:
    _exact(value, ("contract", "schema_version", "study_id", "seed", "inventory_sha256", "excluded_revision_ids", "exclusion_revision_ids_sha256", "items"), "facts study sample")
    if value["contract"] != SAMPLE_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported facts study sample contract")
    _id(value["study_id"], "sample.study_id")
    _string(value["seed"], "sample.seed")
    _sha(value["inventory_sha256"], "sample.inventory_sha256")
    _sha(value["exclusion_revision_ids_sha256"], "sample.exclusion_revision_ids_sha256")
    if not isinstance(value["excluded_revision_ids"], list) or value["excluded_revision_ids"] != sorted(set(value["excluded_revision_ids"])):
        raise ValidationError("sample.excluded_revision_ids must be a sorted unique list")
    for index, revision_id in enumerate(value["excluded_revision_ids"]):
        _id(revision_id, f"sample.excluded_revision_ids[{index}]")
    if canonical_sha256(value["excluded_revision_ids"]) != value["exclusion_revision_ids_sha256"]:
        raise ValidationError("sample exclusion revision digest mismatch")
    if not isinstance(value["items"], list) or len(value["items"]) != 20:
        raise ValidationError("facts study sample must contain exactly 20 items")
    seen: set[str] = set()
    for index, item in enumerate(value["items"]):
        where = f"sample.items[{index}]"
        if not isinstance(item, dict):
            raise ValidationError(f"{where} must be an object")
        _exact(item, ("index", "revision_id", "source", "target", "item_kind", "source_tag", "bounded_context", "stratum"), where)
        if item["index"] != index:
            raise ValidationError(f"{where}.index must equal output order")
        revision_id = _id(item["revision_id"], f"{where}.revision_id")
        if revision_id in seen:
            raise ValidationError("facts study sample revision IDs must be unique")
        if revision_id in set(value["excluded_revision_ids"]):
            raise ValidationError("facts study sample overlaps a frozen exclusion revision")
        seen.add(revision_id)
        _string(item["source"], f"{where}.source")
        _string(item["target"], f"{where}.target", empty=True)
        _enum(item["item_kind"], ITEM_KINDS, f"{where}.item_kind")
        _string(item["source_tag"], f"{where}.source_tag", empty=True)
        _enum(item["stratum"], STRATA, f"{where}.stratum")
        if not isinstance(item["bounded_context"], list) or len(item["bounded_context"]) > 2:
            raise ValidationError(f"{where}.bounded_context must contain at most two entries")
        for cindex, context in enumerate(item["bounded_context"]):
            _exact(context, ("relative_index", "source", "target"), f"{where}.bounded_context[{cindex}]")
            if type(context["relative_index"]) is not int:
                raise ValidationError(f"{where}.bounded_context[{cindex}].relative_index must be an integer")
            _string(context["source"], f"{where}.bounded_context[{cindex}].source", empty=True)
            _string(context["target"], f"{where}.bounded_context[{cindex}].target", empty=True)
    expected_study_id = canonical_sha256({
        "contract": SAMPLE_CONTRACT, "seed": value["seed"],
        "inventory_sha256": value["inventory_sha256"],
        "excluded": value["excluded_revision_ids"], "items": value["items"],
    })
    if value["study_id"] != expected_study_id:
        raise ValidationError("facts study sample study_id is not canonical")
    return value


def build_facts_author_bundle(sample: dict[str, Any]) -> dict[str, Any]:
    """Target-blind input view for the human Facts author."""
    bundle = {
        "contract": FACTS_AUTHOR_BUNDLE_CONTRACT, "schema_version": 1,
        "study_id": sample["study_id"],
        "fact_policy": {
            "min_facts_per_item": 0, "max_facts_per_item": 4,
            "supplemental_only": True,
            "common_input_restatements": "forbidden",
            "allowed_provenance_kinds": sorted(SUPPLEMENTAL_PROVENANCE_KINDS),
            "addressed_definition": "claim-cites-directly-supporting-supplemental-fact",
        },
        "items": [
            {
                "revision_id": item["revision_id"], "source": item["source"],
                "item_kind": item["item_kind"], "source_tag": item["source_tag"],
                "bounded_context": [
                    {"relative_index": context["relative_index"], "source": context["source"]}
                    for context in item["bounded_context"]
                ],
            }
            for item in sample["items"]
        ],
    }
    bundle["bundle_id"] = canonical_sha256(bundle)
    return bundle


def _validate_fact(fact: Any, *, neutral: bool, where: str) -> None:
    if not isinstance(fact, dict):
        raise ValidationError(f"{where} must be an object")
    _exact(fact, ("fact_id", "fact_type", "statement", "provenance"), where)
    _string(fact["fact_id"], f"{where}.fact_id")
    if OPAQUE_FACT_ID_PATTERN.fullmatch(fact["fact_id"]) is None:
        raise ValidationError(
            f"{where}.fact_id must be an opaque fact- followed by 16 lowercase hex characters"
        )
    if neutral:
        _string(fact["fact_type"], f"{where}.fact_type")
    else:
        _enum(fact["fact_type"], FACT_TYPES, f"{where}.fact_type")
    _string(fact["statement"], f"{where}.statement")
    provenance = fact["provenance"]
    if not isinstance(provenance, dict):
        raise ValidationError(f"{where}.provenance must be an object")
    _exact(provenance, ("kind", "reference", "sha256"), f"{where}.provenance")
    if neutral:
        _string(provenance["kind"], f"{where}.provenance.kind")
    else:
        _enum(provenance["kind"], SUPPLEMENTAL_PROVENANCE_KINDS, f"{where}.provenance.kind")
    _string(provenance["reference"], f"{where}.provenance.reference")
    if not neutral and any(
        marker in provenance["reference"].lower()
        for marker in ("facts-author-bundle", "sample.json")
    ):
        raise ValidationError(f"{where}.provenance.reference points to model-visible common input")
    _sha(provenance["sha256"], f"{where}.provenance.sha256")


def validate_packets(value: dict[str, Any], *, sample: dict[str, Any], expected_kind: str) -> dict[str, Any]:
    _exact(value, ("contract", "schema_version", "study_id", "packet_kind", "status", "non_exhaustive", "supplemental_only", "authoring_lineage", "items"), f"{expected_kind} packet")
    if value["contract"] != PACKET_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported fact packet contract")
    if value["study_id"] != sample["study_id"] or value["packet_kind"] != expected_kind:
        raise ValidationError(f"{expected_kind} packet identity does not match sample")
    if value["non_exhaustive"] is not True:
        raise ValidationError("fact packets must declare non_exhaustive=true")
    if value["supplemental_only"] is not True:
        raise ValidationError("fact packets must declare supplemental_only=true")
    if value["status"] != "frozen":
        raise ValidationError(f"{expected_kind} packet must be frozen")
    lineage = value["authoring_lineage"]
    if not isinstance(lineage, dict):
        raise ValidationError(f"{expected_kind}.authoring_lineage must be an object")
    _exact(lineage, ("role", "actor_id", "target_defects_seen", "gold_seen", "common_input_restatements_excluded", "source_inputs_sha256"), f"{expected_kind}.authoring_lineage")
    expected_role = "facts-author" if expected_kind == "facts" else "host-neutral-generator"
    if lineage["role"] != expected_role or not lineage["actor_id"]:
        raise ValidationError(f"{expected_kind} packet authoring role or actor is invalid")
    if lineage["target_defects_seen"] is not False or lineage["gold_seen"] is not False:
        raise ValidationError(f"{expected_kind} packet author must attest target defects and gold were unseen")
    if lineage["common_input_restatements_excluded"] is not True:
        raise ValidationError(f"{expected_kind} packet must attest common-input restatements were excluded")
    _sha(lineage["source_inputs_sha256"], f"{expected_kind}.authoring_lineage.source_inputs_sha256")
    if expected_kind == "facts":
        expected_source_hash = canonical_sha256(build_facts_author_bundle(sample))
        if lineage["source_inputs_sha256"] != expected_source_hash:
            raise ValidationError("facts packet does not bind the deterministic target-blind author bundle")
    if not isinstance(value["items"], list) or len(value["items"]) != 20:
        raise ValidationError(f"{expected_kind} packet must contain 20 items")
    seen_fact_ids: set[str] = set()
    neutral_fact_serial = 0
    for index, (entry, sample_item) in enumerate(zip(value["items"], sample["items"])):
        where = f"{expected_kind}.items[{index}]"
        _exact(entry, ("revision_id", "facts"), where)
        if entry["revision_id"] != sample_item["revision_id"]:
            raise ValidationError(f"{where}.revision_id is out of order")
        if not isinstance(entry["facts"], list) or len(entry["facts"]) > 4:
            raise ValidationError(f"{where}.facts must contain 0-4 supplemental entries")
        for fact_index, fact in enumerate(entry["facts"]):
            _validate_fact(fact, neutral=expected_kind == "neutral", where=f"{where}.facts[{fact_index}]")
            if expected_kind == "neutral":
                expected_id = f"fact-{neutral_fact_serial:016x}"
                if fact["fact_id"] != expected_id:
                    raise ValidationError(
                        f"{where}.facts[{fact_index}].fact_id must be the host-generated neutral ID {expected_id}"
                    )
                neutral_fact_serial += 1
            if fact["fact_id"] in seen_fact_ids:
                raise ValidationError(f"{where}.facts[{fact_index}].fact_id must be globally unique")
            seen_fact_ids.add(fact["fact_id"])
    return value


def build_neutral_packets(facts: dict[str, Any], *, sample: dict[str, Any]) -> dict[str, Any]:
    validate_packets(facts, sample=sample, expected_kind="facts")
    items = []
    fact_serial = 0
    for entry in facts["items"]:
        neutral_facts = []
        for fact in entry["facts"]:
            def fill(value: str, character: str = "x") -> str:
                # Match the bytes occupied by the JSON string payload, including
                # expansion caused by quotes, backslashes and control characters.
                encoded = json.dumps(value, ensure_ascii=False).encode("utf-8")
                return character * (len(encoded) - 2)
            neutral_facts.append({
                "fact_id": f"fact-{fact_serial:016x}",
                "fact_type": fill(fact["fact_type"]),
                "statement": fill(fact["statement"]),
                "provenance": {
                    "kind": fill(fact["provenance"]["kind"]),
                    "reference": fill(fact["provenance"]["reference"]),
                    "sha256": "0" * 64,
                },
            })
            fact_serial += 1
        if len(_canonical_bytes(neutral_facts)) != len(_canonical_bytes(entry["facts"])):
            raise AssertionError("neutral packet canonical byte matching failed")
        items.append({"revision_id": entry["revision_id"], "facts": neutral_facts})
    return {
        "contract": PACKET_CONTRACT, "schema_version": 1,
        "study_id": sample["study_id"], "packet_kind": "neutral", "status": "frozen",
        "non_exhaustive": True, "supplemental_only": True,
        "authoring_lineage": {
            "role": "host-neutral-generator", "actor_id": "facts-study-v2",
            "target_defects_seen": False, "gold_seen": False,
            "common_input_restatements_excluded": True,
            "source_inputs_sha256": canonical_sha256(facts),
        }, "items": items,
    }


def validate_neutral_equivalence(facts: dict[str, Any], neutral: dict[str, Any]) -> None:
    if neutral["authoring_lineage"]["source_inputs_sha256"] != canonical_sha256(facts):
        raise ValidationError("neutral packet does not bind the frozen Facts packet")
    fact_serial = 0
    for index, (left, right) in enumerate(zip(facts["items"], neutral["items"])):
        if len(_canonical_bytes(left["facts"])) != len(_canonical_bytes(right["facts"])):
            raise ValidationError(f"neutral item {index} does not match Facts canonical JSON byte length")
        if [set(f) for f in left["facts"]] != [set(f) for f in right["facts"]]:
            raise ValidationError(f"neutral item {index} does not match Facts JSON shape")
        for fact in right["facts"]:
            if fact["fact_id"] != f"fact-{fact_serial:016x}":
                raise ValidationError(f"neutral item {index} does not use host-generated opaque IDs")
            fact_serial += 1


def _validate_evidence(evidence: Any, text: str, where: str) -> dict[str, Any]:
    return normalize_evidence(evidence, text, where=where, allow_empty_omission=True)


def _require_valid_evidence(evidence: dict[str, Any], where: str) -> None:
    if evidence["state"] in ("exact", "whole-item"):
        return
    if evidence["state"] == "missing" and evidence["quote"] == "" and evidence["occurrence"] == 0:
        return
    raise ValidationError(f"{where} is ambiguous or does not resolve to the visible text")


def _validate_claim(claim: Any, sample_item: dict[str, Any], where: str, fact_ids: set[str]) -> dict[str, Any]:
    if not isinstance(claim, dict):
        raise ValidationError(f"{where} must be an object")
    _exact(claim, ("claim_id", "error_family", "phenomenon", "meaning_change", "source_evidence", "target_evidence", "fact_ids", "requires_manual"), where)
    _string(claim["claim_id"], f"{where}.claim_id")
    _enum(claim["error_family"], ERROR_FAMILIES, f"{where}.error_family")
    _enum(claim["phenomenon"], PHENOMENA, f"{where}.phenomenon")
    _enum(claim["meaning_change"], MEANING_CHANGES, f"{where}.meaning_change")
    source = _validate_evidence(claim["source_evidence"], sample_item["source"], f"{where}.source_evidence")
    target = _validate_evidence(claim["target_evidence"], sample_item["target"], f"{where}.target_evidence")
    _require_valid_evidence(source, f"{where}.source_evidence")
    _require_valid_evidence(target, f"{where}.target_evidence")
    if not isinstance(claim["fact_ids"], list) or any(fid not in fact_ids for fid in claim["fact_ids"]):
        raise ValidationError(f"{where}.fact_ids must reference this item's facts")
    if claim["requires_manual"] not in (True, False):
        raise ValidationError(f"{where}.requires_manual must be boolean")
    return {**claim, "source_evidence": source, "target_evidence": target}


def validate_gold(value: dict[str, Any], *, sample: dict[str, Any], facts: dict[str, Any], require_frozen: bool = True) -> dict[str, Any]:
    _exact(value, ("contract", "schema_version", "study_id", "status", "review_lineage", "items"), "facts study gold")
    if value["contract"] != GOLD_CONTRACT or value["schema_version"] != 1 or value["study_id"] != sample["study_id"]:
        raise ValidationError("facts study gold identity does not match sample")
    if value["status"] not in ("draft", "frozen") or (require_frozen and value["status"] != "frozen"):
        raise ValidationError("facts study gold must be frozen before preregistration")
    lineage = value["review_lineage"]
    _exact(lineage, ("reviewer_ids", "review_artifact_sha256s", "adjudicator_id", "adjudication_artifact_sha256"), "gold.review_lineage")
    if require_frozen:
        if not isinstance(lineage["reviewer_ids"], list) or len(lineage["reviewer_ids"]) != 2 or len(set(lineage["reviewer_ids"])) != 2 or any(not x for x in lineage["reviewer_ids"]):
            raise ValidationError("frozen gold requires two distinct non-empty reviewer IDs")
        if not isinstance(lineage["review_artifact_sha256s"], list) or len(lineage["review_artifact_sha256s"]) != 2:
            raise ValidationError("frozen gold requires two review artifact hashes")
        for index, digest in enumerate(lineage["review_artifact_sha256s"]):
            _sha(digest, f"gold.review_lineage.review_artifact_sha256s[{index}]")
        _string(lineage["adjudicator_id"], "gold.review_lineage.adjudicator_id")
        if lineage["adjudicator_id"] in set(lineage["reviewer_ids"]):
            raise ValidationError("gold adjudicator must be distinct from both reviewers")
        _sha(lineage["adjudication_artifact_sha256"], "gold.review_lineage.adjudication_artifact_sha256")
        fact_author = facts["authoring_lineage"]["actor_id"]
        if fact_author in set(lineage["reviewer_ids"]) | {lineage["adjudicator_id"]}:
            raise ValidationError("Facts author must be separate from gold reviewers and adjudicator")
    if not isinstance(value["items"], list) or len(value["items"]) != 20:
        raise ValidationError("facts study gold must contain 20 items")
    fact_map = {entry["revision_id"]: {fact["fact_id"] for fact in entry["facts"]} for entry in facts["items"]}
    normalized_items = []
    claim_ids: set[str] = set()
    for index, (entry, sample_item) in enumerate(zip(value["items"], sample["items"])):
        where = f"gold.items[{index}]"
        _exact(entry, ("revision_id", "clean", "fact_trap", "acceptable_localization", "claims"), where)
        if entry["revision_id"] != sample_item["revision_id"]:
            raise ValidationError(f"{where}.revision_id is out of order")
        for field in ("clean", "fact_trap", "acceptable_localization"):
            if entry[field] not in (True, False):
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
        if addressed < 8 or unaddressed < 8 or clean < 5 or traps < 3:
            raise ValidationError("frozen gold misses preregistered minima: 8 addressed, 8 unaddressed, 5 clean, 3 fact traps")
        required_strata = STRATA
        present = {item["stratum"] for item in sample["items"]}
        if not required_strata <= present:
            raise ValidationError("frozen sample does not cover every preregistered stratum")
    return {**value, "items": normalized_items}


def validate_gold_authoring_artifacts(
    *, review_paths: list[Path], adjudication_path: Path, gold: dict[str, Any],
    sample: dict[str, Any], facts: dict[str, Any],
) -> None:
    if len(review_paths) != 2:
        raise ValidationError("Facts study requires exactly two independent gold review artifacts")
    review_ids = []
    review_hashes = []
    for index, path in enumerate(review_paths):
        review = read_json_object(path, f"facts study gold review {index + 1}")
        _exact(review, ("contract", "schema_version", "study_id", "reviewer_id", "independent", "items"), f"gold review {index + 1}")
        if review["contract"] != "tome4-quality-facts-study-gold-review-v1" or review["schema_version"] != 1 or review["study_id"] != sample["study_id"] or review["independent"] is not True:
            raise ValidationError(f"gold review {index + 1} identity or independence attestation is invalid")
        review_ids.append(_string(review["reviewer_id"], f"gold review {index + 1}.reviewer_id"))
        review_hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
        validate_gold({
            "contract": GOLD_CONTRACT, "schema_version": 1, "study_id": sample["study_id"],
            "status": "draft", "review_lineage": {
                "reviewer_ids": ["", ""], "review_artifact_sha256s": ["", ""],
                "adjudicator_id": "", "adjudication_artifact_sha256": "",
            }, "items": review["items"],
        }, sample=sample, facts=facts, require_frozen=False)
    if len(set(review_ids)) != 2:
        raise ValidationError("gold review artifacts must have distinct reviewer IDs")
    adjudication = read_json_object(adjudication_path, "facts study gold adjudication")
    _exact(adjudication, ("contract", "schema_version", "study_id", "status", "adjudicator_id", "review_artifact_sha256s", "items"), "gold adjudication")
    if adjudication["contract"] != "tome4-quality-facts-study-gold-adjudication-v1" or adjudication["schema_version"] != 1 or adjudication["study_id"] != sample["study_id"] or adjudication["status"] != "frozen":
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


def _packet_map(packet: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {entry["revision_id"]: entry["facts"] for entry in packet["items"]}


def build_bundle(*, sample: dict[str, Any], facts: dict[str, Any], neutral: dict[str, Any], arm: str, prompt_sha256: str) -> dict[str, Any]:
    _enum(arm, ARMS, "bundle arm")
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
        "contract": BUNDLE_CONTRACT, "schema_version": 1, "study_id": sample["study_id"],
        "arm": arm, "prompt_sha256": prompt_sha256, "items": items, "bundle_id": "",
    }
    bundle["bundle_id"] = canonical_sha256({key: val for key, val in bundle.items() if key != "bundle_id"})
    return bundle


def validate_bundle(value: dict[str, Any], *, sample: dict[str, Any], facts: dict[str, Any], neutral: dict[str, Any], prompt_sha256: str) -> dict[str, Any]:
    _exact(value, ("contract", "schema_version", "study_id", "arm", "prompt_sha256", "items", "bundle_id"), "facts study bundle")
    if value["contract"] != BUNDLE_CONTRACT or value["schema_version"] != 1 or value["study_id"] != sample["study_id"]:
        raise ValidationError("facts study bundle identity mismatch")
    arm = _enum(value["arm"], ARMS, "bundle.arm")
    if value["prompt_sha256"] != prompt_sha256:
        raise ValidationError("facts study bundle prompt hash mismatch")
    expected = build_bundle(sample=sample, facts=facts, neutral=neutral, arm=arm, prompt_sha256=prompt_sha256)
    if value != expected:
        raise ValidationError("facts study bundle is not the deterministic expected view")
    return value


def build_schedule(protocol: dict[str, Any], bundles: dict[str, dict[str, Any]], prompts: dict[str, str]) -> list[dict[str, Any]]:
    slots = []
    providers = protocol["evaluators"]
    for evaluator_id, arms in (("luna", LUNA_ARMS), ("deepseek", DEEPSEEK_ARMS)):
        evaluator = providers[evaluator_id]
        for arm in arms:
            for replicate in range(1, 4):
                seed = canonical_sha256({"schedule_seed": protocol["schedule_seed"], "evaluator": evaluator_id, "arm": arm, "replicate": replicate})[:16]
                slot = {
                    "slot_id": f"{evaluator_id}-{arm.lower()}-{replicate}",
                    "ordinal": 0, "evaluator_id": evaluator_id, "provider": evaluator["provider"],
                    "model": evaluator["model"], "thinking": evaluator["thinking"],
                    "arm": arm, "replicate": replicate, "seed": seed,
                    "bundle_id": bundles[arm]["bundle_id"],
                    "bundle_sha256": canonical_sha256(bundles[arm]),
                    "prompt_sha256": hashlib.sha256(prompts[arm].encode("utf-8")).hexdigest(),
                    "shard_count": 1, "cache": "disabled", "retry_policy": "none",
                }
                slots.append(slot)
    rng = random.Random(protocol["execution_order_seed"])
    rng.shuffle(slots)
    for ordinal, slot in enumerate(slots, 1):
        slot["ordinal"] = ordinal
    if len(slots) != 33:
        raise AssertionError("facts study schedule must contain exactly 33 slots")
    return slots


def build_preregistration(*, protocol: dict[str, Any], sample: dict[str, Any], facts: dict[str, Any], neutral: dict[str, Any], gold: dict[str, Any], bundles: dict[str, dict[str, Any]], prompts: dict[str, str]) -> dict[str, Any]:
    validate_gold(gold, sample=sample, facts=facts, require_frozen=True)
    schedule = build_schedule(protocol, bundles, prompts)
    value = {
        "contract": PREREG_CONTRACT, "schema_version": 1, "study_id": sample["study_id"],
        "purpose": "facts-causal-study-only-no-holdout-clearance",
        "sample_sha256": canonical_sha256(sample), "facts_sha256": canonical_sha256(facts),
        "neutral_sha256": canonical_sha256(neutral), "gold_sha256": canonical_sha256(gold),
        "protocol_sha256": canonical_sha256(protocol),
        "harness_sha256": study_harness_sha256(),
        "pi_executable": pi_executable_identity(),
        "arm_prompt_sha256s": {arm: hashlib.sha256(prompts[arm].encode("utf-8")).hexdigest() for arm in ARMS},
        "item_order": [item["revision_id"] for item in sample["items"]],
        "schedule": schedule, "contrasts": protocol["contrasts"],
        "decision_rule": protocol["decision_rule"], "max_external_slots": 33,
        "cache_policy": "disabled", "replacement_policy": "forbidden", "preregistration_id": "",
    }
    value["preregistration_id"] = canonical_sha256({key: val for key, val in value.items() if key != "preregistration_id"})
    return value


def validate_preregistration(value: dict[str, Any], *, protocol: dict[str, Any], sample: dict[str, Any], facts: dict[str, Any], neutral: dict[str, Any], gold: dict[str, Any], bundles: dict[str, dict[str, Any]], prompts: dict[str, str]) -> dict[str, Any]:
    expected = build_preregistration(protocol=protocol, sample=sample, facts=facts, neutral=neutral, gold=gold, bundles=bundles, prompts=prompts)
    if value != expected:
        raise ValidationError("facts study preregistration is not the deterministic expected artifact")
    return value


def _normalize_finding(finding: Any, *, item: dict[str, Any], facts: set[str], arm: str, where: str) -> dict[str, Any]:
    if not isinstance(finding, dict):
        raise ValidationError(f"{where} must be an object")
    _exact(finding, ("error_family", "phenomenon", "meaning_change", "source_evidence", "target_evidence", "explanation", "supported_fact_ids", "requires_manual"), where)
    _enum(finding["error_family"], ERROR_FAMILIES, f"{where}.error_family")
    _enum(finding["phenomenon"], PHENOMENA, f"{where}.phenomenon")
    _enum(finding["meaning_change"], MEANING_CHANGES, f"{where}.meaning_change")
    source = _validate_evidence(finding["source_evidence"], item["source"], f"{where}.source_evidence")
    target = _validate_evidence(finding["target_evidence"], item["target"], f"{where}.target_evidence")
    _require_valid_evidence(source, f"{where}.source_evidence")
    _require_valid_evidence(target, f"{where}.target_evidence")
    _string(finding["explanation"], f"{where}.explanation")
    if not isinstance(finding["supported_fact_ids"], list) or len(finding["supported_fact_ids"]) != len(set(finding["supported_fact_ids"])):
        raise ValidationError(f"{where}.supported_fact_ids must be a unique list")
    if any(fid not in facts for fid in finding["supported_fact_ids"]):
        raise ValidationError(f"{where}.supported_fact_ids contains an unknown fact")
    if arm in NO_FACT_ARMS and finding["supported_fact_ids"]:
        raise ValidationError(f"arm {arm} cannot cite Facts")
    if arm == "F" and not finding["supported_fact_ids"]:
        raise ValidationError("Facts-only verifier findings must cite at least one fact_id")
    if finding["requires_manual"] not in (True, False):
        raise ValidationError(f"{where}.requires_manual must be boolean")
    return {**finding, "source_evidence": source, "target_evidence": target}


def validate_assessment(value: dict[str, Any], *, sample: dict[str, Any], facts: dict[str, Any], bundle: dict[str, Any], slot: dict[str, Any]) -> dict[str, Any]:
    _exact(value, ("contract", "schema_version", "study_id", "slot_id", "evaluator", "bundle_id", "bundle_sha256", "prompt_sha256", "assessment_state", "items"), "facts study assessment")
    if value["contract"] != ASSESSMENT_CONTRACT or value["schema_version"] != 1 or value["study_id"] != sample["study_id"] or value["slot_id"] != slot["slot_id"]:
        raise ValidationError("facts study assessment identity mismatch")
    expected_evaluator = {key: slot[key] for key in ("evaluator_id", "provider", "model", "thinking")}
    if value["evaluator"] != expected_evaluator:
        raise ValidationError("facts study assessment evaluator identity mismatch")
    if value["bundle_id"] != bundle["bundle_id"] or value["bundle_sha256"] != canonical_sha256(bundle) or value["prompt_sha256"] != slot["prompt_sha256"]:
        raise ValidationError("facts study assessment frozen input hashes mismatch")
    if value["assessment_state"] != "complete":
        raise ValidationError("facts study assessment must be complete")
    if not isinstance(value["items"], list) or len(value["items"]) != 20:
        raise ValidationError("facts study assessment must contain 20 items")
    fact_map = {entry["revision_id"]: {fact["fact_id"] for fact in entry["facts"]} for entry in facts["items"]}
    normalized_items = []
    for index, (entry, sample_item) in enumerate(zip(value["items"], sample["items"])):
        where = f"assessment.items[{index}]"
        _exact(entry, ("revision_id", "findings"), where)
        if entry["revision_id"] != sample_item["revision_id"] or not isinstance(entry["findings"], list):
            raise ValidationError(f"{where} is out of order or findings is not a list")
        findings = [_normalize_finding(finding, item=sample_item, facts=fact_map[entry["revision_id"]], arm=slot["arm"], where=f"{where}.findings[{findex}]") for findex, finding in enumerate(entry["findings"])]
        normalized_items.append({"revision_id": entry["revision_id"], "findings": findings})
    return {**value, "items": normalized_items}


def align_claims(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> list[tuple[int, int]]:
    """Shared symmetric maximum-weight alignment (see quality_claims)."""
    from .quality_claims import align_claims as _align_claims
    return _align_claims(left, right)


def union_and_dedupe(left: dict[str, Any], right: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Host-only symmetric B+F union (see quality_claims)."""
    from .quality_claims import union_findings
    return union_findings(left, right)


def _safe_ratio(numerator: int, denominator: int) -> dict[str, Any]:
    return {"state": "applicable" if denominator else "not-applicable", "numerator": numerator, "denominator": denominator, "value": numerator / denominator if denominator else None}


def _score(findings_by_revision: dict[str, list[dict[str, Any]]], gold: dict[str, Any], sample: dict[str, Any] | None = None) -> dict[str, Any]:
    gold_map = {entry["revision_id"]: entry for entry in gold["items"]}
    stratum_map = {item["revision_id"]: item["stratum"] for item in sample["items"]} if sample else {}
    tp = fp = fn = addressed_hit = addressed_total = unaddressed_hit = unaddressed_total = trap_fp = clean_fp = manual = 0
    clean_items = trap_items = clean_items_with_fp = trap_items_with_fp = 0
    by_family: dict[str, Counter[str]] = defaultdict(Counter)
    by_stratum: dict[str, Counter[str]] = defaultdict(Counter)
    for revision_id, gold_item in gold_map.items():
        findings = findings_by_revision.get(revision_id, [])
        claims = gold_item["claims"]
        pairs = align_claims(findings, claims)
        matched_findings = {a for a, _ in pairs}
        matched_claims = {b for _, b in pairs}
        tp += len(pairs); fp += len(findings) - len(pairs); fn += len(claims) - len(pairs)
        manual += sum(finding["requires_manual"] for finding in findings)
        if gold_item["clean"]:
            clean_fp += len(findings)
            clean_items += 1
            clean_items_with_fp += bool(findings)
        if gold_item["fact_trap"]:
            trap_fp += len(findings)
            trap_items += 1
            trap_items_with_fp += bool(findings)
        for cindex, claim in enumerate(claims):
            addressed = bool(claim["fact_ids"])
            addressed_total += addressed; unaddressed_total += not addressed
            addressed_hit += addressed and cindex in matched_claims
            unaddressed_hit += (not addressed) and cindex in matched_claims
            bucket = by_family[claim["error_family"]]
            bucket["gold"] += 1; bucket["matched"] += cindex in matched_claims
            if revision_id in stratum_map:
                sbucket = by_stratum[stratum_map[revision_id]]
                sbucket["gold"] += 1; sbucket["matched"] += cindex in matched_claims
        for findex, finding in enumerate(findings):
            if findex not in matched_findings:
                by_family[finding["error_family"]]["false_positive"] += 1
                if revision_id in stratum_map:
                    by_stratum[stratum_map[revision_id]]["false_positive"] += 1
    precision = _safe_ratio(tp, tp + fp); recall = _safe_ratio(tp, tp + fn)
    p, r = precision["value"], recall["value"]
    f1 = None if p is None or r is None or p + r == 0 else 2 * p * r / (p + r)
    def summarize_buckets(values: dict[str, Counter[str]]) -> dict[str, Any]:
        result = {}
        for key, value in sorted(values.items()):
            matched = value["matched"]
            false_positive = value["false_positive"]
            false_negative = value["gold"] - matched
            result[key] = {
                "counts": {"true_positive": matched, "false_positive": false_positive, "false_negative": false_negative},
                "precision": _safe_ratio(matched, matched + false_positive),
                "recall": _safe_ratio(matched, matched + false_negative),
            }
        return result

    return {
        "counts": {"true_positive": tp, "false_positive": fp, "false_negative": fn},
        "precision": precision, "recall": recall,
        "f1": {"state": "applicable" if f1 is not None else "not-applicable", "value": f1},
        "fact_addressed_recall": _safe_ratio(addressed_hit, addressed_total),
        "fact_unaddressed_recall": _safe_ratio(unaddressed_hit, unaddressed_total),
        "clean_false_findings": clean_fp, "fact_trap_false_findings": trap_fp,
        "clean_item_false_positive_rate": _safe_ratio(clean_items_with_fp, clean_items),
        "fact_trap_item_false_positive_rate": _safe_ratio(trap_items_with_fp, trap_items),
        "manual_queue_findings": manual,
        "error_family": summarize_buckets(by_family),
        "sample_stratum": summarize_buckets(by_stratum),
    }


def _assessment_map(assessment: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {entry["revision_id"]: entry["findings"] for entry in assessment["items"]}


def _matched_gold_ids(findings_by_revision: dict[str, list[dict[str, Any]]], gold: dict[str, Any]) -> set[str]:
    result = set()
    for item in gold["items"]:
        findings = findings_by_revision.get(item["revision_id"], [])
        for _, gold_index in align_claims(findings, item["claims"]):
            result.add(item["claims"][gold_index]["claim_id"])
    return result


def _revision_counts(findings_by_revision: dict[str, list[dict[str, Any]]], gold: dict[str, Any]) -> dict[str, tuple[int, int, int]]:
    result = {}
    for item in gold["items"]:
        findings = findings_by_revision.get(item["revision_id"], [])
        pairs = align_claims(findings, item["claims"])
        result[item["revision_id"]] = (len(pairs), len(findings) - len(pairs), len(item["claims"]) - len(pairs))
    return result


def _metric_from_counts(counts: tuple[int, int, int], metric: str) -> float:
    tp, fp, fn = counts
    if metric == "precision": return tp / (tp + fp) if tp + fp else 1.0
    if metric == "recall": return tp / (tp + fn) if tp + fn else 1.0
    raise AssertionError(metric)


def _paired_bootstrap(
    left: dict[str, list[dict[str, Any]]], right: dict[str, list[dict[str, Any]]],
    gold: dict[str, Any], *, seed: str, replicates: int,
) -> dict[str, Any]:
    """Paired item bootstrap for left-minus-right metric differences."""
    left_counts, right_counts = _revision_counts(left, gold), _revision_counts(right, gold)
    return _paired_bootstrap_counts(left_counts, right_counts, seed=seed, replicates=replicates)


def _paired_bootstrap_counts(
    left_counts: dict[str, tuple[int, int, int]],
    right_counts: dict[str, tuple[int, int, int]], *, seed: str, replicates: int,
) -> dict[str, Any]:
    revisions = sorted(left_counts)
    rng = random.Random(seed)
    samples: dict[str, list[float]] = {"precision": [], "recall": []}
    for _ in range(replicates):
        picked = [rng.choice(revisions) for _ in revisions]
        lsum = tuple(sum(left_counts[r][index] for r in picked) for index in range(3))
        rsum = tuple(sum(right_counts[r][index] for r in picked) for index in range(3))
        for metric in samples:
            samples[metric].append(_metric_from_counts(lsum, metric) - _metric_from_counts(rsum, metric))
    result = {}
    for metric, values in samples.items():
        values.sort()
        low = values[max(0, math.floor(0.025 * replicates))]
        high = values[min(replicates - 1, math.ceil(0.975 * replicates) - 1)]
        result[metric] = {"lower": low, "upper": high, "level": 0.95, "replicates": replicates}
    return result


def _interaction_bootstrap_counts(
    d_counts: dict[str, tuple[int, int, int]], c_counts: dict[str, tuple[int, int, int]],
    b_counts: dict[str, tuple[int, int, int]], a_counts: dict[str, tuple[int, int, int]],
    *, seed: str, replicates: int,
) -> dict[str, Any]:
    revisions = sorted(d_counts)
    rng = random.Random(seed)
    samples: dict[str, list[float]] = {"precision": [], "recall": []}
    for _ in range(replicates):
        picked = [rng.choice(revisions) for _ in revisions]
        totals = []
        for counts in (d_counts, c_counts, b_counts, a_counts):
            totals.append(tuple(sum(counts[revision][index] for revision in picked) for index in range(3)))
        for metric in samples:
            dvalue, cvalue, bvalue, avalue = (_metric_from_counts(total, metric) for total in totals)
            samples[metric].append((dvalue - cvalue) - (bvalue - avalue))
    result = {}
    for metric, values in samples.items():
        values.sort()
        result[metric] = {
            "lower": values[max(0, math.floor(0.025 * replicates))],
            "upper": values[min(replicates - 1, math.ceil(0.975 * replicates) - 1)],
            "level": 0.95, "replicates": replicates,
        }
    return result


def build_report(*, preregistration: dict[str, Any], gold: dict[str, Any], assessments: dict[str, dict[str, Any]], sample: dict[str, Any] | None = None, protocol: dict[str, Any] | None = None, evidence_mode: str = "offline-fake-replay") -> dict[str, Any]:
    if evidence_mode not in ("offline-fake-replay", "external-assessments"):
        raise ValidationError("facts study report evidence mode is invalid")
    slot_by_id = {slot["slot_id"]: slot for slot in preregistration["schedule"]}
    if set(assessments) != set(slot_by_id):
        missing = sorted(set(slot_by_id) - set(assessments))
        extra = sorted(set(assessments) - set(slot_by_id))
        raise ValidationError(f"facts study report requires exactly all 33 slots; missing={missing}, extra={extra}")
    run_metrics: dict[str, Any] = {}
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for slot_id, assessment in assessments.items():
        slot = slot_by_id[slot_id]
        metrics = _score(_assessment_map(assessment), gold, sample)
        run_metrics[slot_id] = metrics
        grouped[(slot["evaluator_id"], slot["arm"])].append(metrics)
    t_metrics: dict[str, Any] = {}
    t_composition: dict[str, Any] = {}
    for evaluator_id in ("luna", "deepseek"):
        for replicate in range(1, 4):
            left = assessments[f"{evaluator_id}-b-{replicate}"]
            right = assessments[f"{evaluator_id}-f-{replicate}"]
            union = union_and_dedupe(left, right)
            key = f"{evaluator_id}-t-{replicate}"
            t_metrics[key] = _score(union, gold, sample)
            left_count = sum(len(item["findings"]) for item in left["items"])
            right_count = sum(len(item["findings"]) for item in right["items"])
            union_count = sum(len(findings) for findings in union.values())
            t_composition[key] = {
                "open_findings": left_count, "facts_findings": right_count,
                "union_findings": union_count,
                "duplicates_removed": left_count + right_count - union_count,
            }

    def pooled(evaluator_id: str, arm: str) -> dict[str, Any]:
        metrics = [run_metrics[f"{evaluator_id}-{arm.lower()}-{rep}"] for rep in range(1, 4)] if arm != "T" else [t_metrics[f"{evaluator_id}-t-{rep}"] for rep in range(1, 4)]
        counts = Counter()
        for metric in metrics:
            counts.update(metric["counts"])
        p = _safe_ratio(counts["true_positive"], counts["true_positive"] + counts["false_positive"])
        r = _safe_ratio(counts["true_positive"], counts["true_positive"] + counts["false_negative"])
        pvalue, rvalue = p["value"], r["value"]
        f1 = None if pvalue is None or rvalue is None or pvalue + rvalue == 0 else 2 * pvalue * rvalue / (pvalue + rvalue)
        return {
            "counts": dict(counts), "precision": p, "recall": r,
            "f1": {"state": "applicable" if f1 is not None else "not-applicable", "value": f1},
            "fact_addressed_recall": sum(m["fact_addressed_recall"]["value"] or 0 for m in metrics) / 3,
            "fact_unaddressed_recall": sum(m["fact_unaddressed_recall"]["value"] or 0 for m in metrics) / 3,
            "fact_trap_false_findings_per_run": sum(m["fact_trap_false_findings"] for m in metrics) / 3,
            "manual_queue_findings_per_run": sum(m["manual_queue_findings"] for m in metrics) / 3,
        }

    pooled_metrics = {}
    for evaluator_id, arms in (("luna", ARMS + ("T",)), ("deepseek", DEEPSEEK_ARMS + ("T",))):
        pooled_metrics[evaluator_id] = {arm: pooled(evaluator_id, arm) for arm in arms}

    def delta(evaluator: str, left: str, right: str, field: str) -> float | None:
        lval = pooled_metrics[evaluator][left][field]
        rval = pooled_metrics[evaluator][right][field]
        if isinstance(lval, dict): lval = lval["value"]
        if isinstance(rval, dict): rval = rval["value"]
        return None if lval is None or rval is None else lval - rval

    contrasts = {
        "luna": {
            "B-A": {"recall": delta("luna", "B", "A", "recall")},
            "C-A": {"recall": delta("luna", "C", "A", "recall")},
            "D-B": {"recall": delta("luna", "D", "B", "recall")},
            "interaction": {"recall": (delta("luna", "D", "C", "recall") or 0) - (delta("luna", "B", "A", "recall") or 0)},
            "N-B": {"recall": delta("luna", "N", "B", "recall")},
            "L-D": {"recall": delta("luna", "L", "D", "recall")},
            "T-B": {"recall": delta("luna", "T", "B", "recall"), "precision": delta("luna", "T", "B", "precision")},
        },
        "deepseek": {"T-B": {"recall": delta("deepseek", "T", "B", "recall"), "precision": delta("deepseek", "T", "B", "precision")}},
    }
    bootstrap = {}
    if protocol is not None:
        contrast_pairs = {
            "B-A": ("B", "A"), "C-A": ("C", "A"), "D-B": ("D", "B"),
            "N-B": ("N", "B"), "L-D": ("L", "D"), "T-B": ("T", "B"),
        }
        for evaluator_id, allowed in (("luna", set(contrast_pairs)), ("deepseek", {"T-B"})):
            bootstrap[evaluator_id] = {}
            for name in sorted(allowed):
                left_arm, right_arm = contrast_pairs[name]
                per_round = []
                left_round_counts = []
                right_round_counts = []
                for replicate in range(1, 4):
                    left_map = union_and_dedupe(
                        assessments[f"{evaluator_id}-b-{replicate}"], assessments[f"{evaluator_id}-f-{replicate}"]
                    ) if left_arm == "T" else _assessment_map(assessments[f"{evaluator_id}-{left_arm.lower()}-{replicate}"])
                    right_map = _assessment_map(assessments[f"{evaluator_id}-{right_arm.lower()}-{replicate}"])
                    left_round_counts.append(_revision_counts(left_map, gold))
                    right_round_counts.append(_revision_counts(right_map, gold))
                    per_round.append(_paired_bootstrap(
                        left_map, right_map, gold,
                        seed=f"{protocol['bootstrap_seed']}:{evaluator_id}:{name}:{replicate}",
                        replicates=protocol["bootstrap_replicates"],
                    ))
                pooled_left = {
                    revision_id: tuple(sum(round_counts[revision_id][index] for round_counts in left_round_counts) for index in range(3))
                    for revision_id in left_round_counts[0]
                }
                pooled_right = {
                    revision_id: tuple(sum(round_counts[revision_id][index] for round_counts in right_round_counts) for index in range(3))
                    for revision_id in right_round_counts[0]
                }
                bootstrap[evaluator_id][name] = {
                    "per_run": per_round,
                    "pooled": _paired_bootstrap_counts(
                        pooled_left, pooled_right,
                        seed=f"{protocol['bootstrap_seed']}:{evaluator_id}:{name}:pooled",
                        replicates=protocol["bootstrap_replicates"],
                    ),
                }
        interaction_round_counts = []
        interaction_per_run = []
        for replicate in range(1, 4):
            counts = tuple(
                _revision_counts(_assessment_map(assessments[f"luna-{arm.lower()}-{replicate}"]), gold)
                for arm in ("D", "C", "B", "A")
            )
            interaction_round_counts.append(counts)
            interaction_per_run.append(_interaction_bootstrap_counts(
                *counts, seed=f"{protocol['bootstrap_seed']}:luna:interaction:{replicate}",
                replicates=protocol["bootstrap_replicates"],
            ))
        pooled_interaction = []
        for arm_index in range(4):
            pooled_interaction.append({
                revision_id: tuple(
                    sum(interaction_round_counts[replicate][arm_index][revision_id][field] for replicate in range(3))
                    for field in range(3)
                )
                for revision_id in interaction_round_counts[0][arm_index]
            })
        bootstrap["luna"]["interaction"] = {
            "per_run": interaction_per_run,
            "pooled": _interaction_bootstrap_counts(
                *pooled_interaction, seed=f"{protocol['bootstrap_seed']}:luna:interaction:pooled",
                replicates=protocol["bootstrap_replicates"],
            ),
        }

    claim_frequencies = {}
    gold_claim_by_id = {claim["claim_id"]: claim for item in gold["items"] for claim in item["claims"]}
    for evaluator_id in ("luna", "deepseek"):
        frequencies = {}
        for arm in ("B", "T"):
            counts: Counter[str] = Counter()
            for replicate in range(1, 4):
                finding_map = union_and_dedupe(
                    assessments[f"{evaluator_id}-b-{replicate}"], assessments[f"{evaluator_id}-f-{replicate}"]
                ) if arm == "T" else _assessment_map(assessments[f"{evaluator_id}-b-{replicate}"])
                counts.update(_matched_gold_ids(finding_map, gold))
            frequencies[arm] = dict(sorted(counts.items()))
        claim_frequencies[evaluator_id] = frequencies

    luna_b, luna_t = pooled_metrics["luna"]["B"], pooled_metrics["luna"]["T"]
    deep_b, deep_t = pooled_metrics["deepseek"]["B"], pooled_metrics["deepseek"]["T"]
    luna_stable_added = sorted(claim_id for claim_id, count in claim_frequencies["luna"]["T"].items() if count >= 2 and claim_frequencies["luna"]["B"].get(claim_id, 0) == 0)
    deep_stable_addressed = sorted(claim_id for claim_id, count in claim_frequencies["deepseek"]["T"].items() if count >= 2 and claim_frequencies["deepseek"]["B"].get(claim_id, 0) == 0 and gold_claim_by_id[claim_id]["fact_ids"])
    luna_trap_round_ok = all(
        t_metrics[f"luna-t-{rep}"]["fact_trap_false_findings"] <= run_metrics[f"luna-b-{rep}"]["fact_trap_false_findings"] + 1
        for rep in range(1, 4)
    )
    criteria = {
        "luna_adds_two_true_claims": len(luna_stable_added) >= 2,
        "luna_precision_drop_at_most_3pp": (luna_t["precision"]["value"] or 0) >= (luna_b["precision"]["value"] or 0) - 0.03,
        "luna_fact_trap_increase_at_most_one_each_run": luna_trap_round_ok,
        "luna_unaddressed_recall_not_lower": luna_t["fact_unaddressed_recall"] >= luna_b["fact_unaddressed_recall"],
        "deepseek_direction_consistent": (deep_t["recall"]["value"] or 0) >= (deep_b["recall"]["value"] or 0),
        "deepseek_adds_one_stable_fact_addressed_claim": len(deep_stable_addressed) >= 1,
        "structure_and_evidence_validity": True,
    }
    decision = "promote-two-stage-to-v4-draft3" if all(criteria.values()) else "do-not-promote-facts-channel"
    if decision.startswith("promote") and protocol is not None:
        margin = protocol["decision_rule"]["single_pass_equivalence_margin"]
        candidates = []
        for arm in ("D", "L"):
            if all(
                (pooled_metrics[evaluator][arm][metric]["value"] or 0) >= (pooled_metrics[evaluator]["T"][metric]["value"] or 0) - margin
                for evaluator in ("luna", "deepseek") for metric in ("precision", "recall")
            ) and all(pooled_metrics[evaluator][arm]["manual_queue_findings_per_run"] < pooled_metrics[evaluator]["T"]["manual_queue_findings_per_run"] for evaluator in ("luna", "deepseek")):
                candidates.append(arm)
        if candidates:
            decision = f"consider-single-pass-{'-or-'.join(candidates)}-otherwise-two-stage"
    if evidence_mode != "external-assessments":
        decision = "non-evidentiary-offline-replay"
    report = {
        "contract": REPORT_CONTRACT, "schema_version": 1,
        "study_id": preregistration["study_id"], "preregistration_id": preregistration["preregistration_id"],
        "holdout_clearance": False, "run_metrics": run_metrics, "two_stage_metrics": t_metrics,
        "evidence_mode": evidence_mode,
        "external_evidence": evidence_mode == "external-assessments",
        "schema_validity": {"numerator": 33, "denominator": 33, "value": 1.0},
        "evidence_validity": {"numerator": 33, "denominator": 33, "value": 1.0},
        "two_stage_composition": t_composition,
        "pooled_metrics": pooled_metrics, "contrasts": contrasts,
        "paired_item_bootstrap": bootstrap,
        "claim_detection_frequencies": claim_frequencies,
        "incremental_true_claims": {"luna_stable": luna_stable_added, "deepseek_stable_fact_addressed": deep_stable_addressed},
        "decision": {"result": decision, "criteria": criteria}, "report_id": "",
    }
    report["report_id"] = canonical_sha256({key: value for key, value in report.items() if key != "report_id"})
    return report


def build_fake_assessments(*, preregistration: dict[str, Any], sample: dict[str, Any], gold: dict[str, Any], bundles: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Offline identity/metric replay. It is never valid evidence about a provider."""
    gold_map = {entry["revision_id"]: entry["claims"] for entry in gold["items"]}
    result = {}
    for slot in preregistration["schedule"]:
        arm = slot["arm"]
        items = []
        for item in sample["items"]:
            findings = []
            for claim in gold_map[item["revision_id"]]:
                addressed = bool(claim["fact_ids"])
                include = (arm in ("B", "D", "L") and not addressed) or (arm in ("C", "D", "L", "F") and addressed)
                if arm == "A": include = not addressed and int(claim["claim_id"][-1], 16) % 2 == 0
                if arm == "N": include = not addressed
                if include:
                    findings.append({
                        "error_family": claim["error_family"], "phenomenon": claim["phenomenon"],
                        "meaning_change": claim["meaning_change"],
                        "source_evidence": {key: claim["source_evidence"][key] for key in ("quote", "occurrence", "whole_item") if key in claim["source_evidence"]},
                        "target_evidence": {key: claim["target_evidence"][key] for key in ("quote", "occurrence", "whole_item") if key in claim["target_evidence"]},
                        "explanation": "offline fake-runner replay",
                        "supported_fact_ids": claim["fact_ids"] if arm in FACT_ARMS else [],
                        "requires_manual": claim["requires_manual"],
                    })
            items.append({"revision_id": item["revision_id"], "findings": findings})
        evaluator = {key: slot[key] for key in ("evaluator_id", "provider", "model", "thinking")}
        result[slot["slot_id"]] = {
            "contract": ASSESSMENT_CONTRACT, "schema_version": 1, "study_id": sample["study_id"],
            "slot_id": slot["slot_id"], "evaluator": evaluator,
            "bundle_id": bundles[arm]["bundle_id"], "bundle_sha256": canonical_sha256(bundles[arm]),
            "prompt_sha256": slot["prompt_sha256"], "assessment_state": "complete", "items": items,
        }
    return result


def run_build(manifest: Manifest, *, inventory: Path, exclusions: list[Path], seed: str) -> dict[str, Any]:
    historical_exclusions = load_historical_exclusions(manifest)
    sample, facts, gold = build_candidate_sample(
        inventory_path=inventory, exclusion_paths=exclusions, seed=seed,
        required_excluded_ids=historical_exclusions,
    )
    run = create_quality_run_directory(manifest.root, "facts-study-build")
    author_bundle = build_facts_author_bundle(sample)
    facts["authoring_lineage"]["source_inputs_sha256"] = canonical_sha256(author_bundle)
    write_json(run / "sample.json", sample)
    write_json(run / "facts-author-bundle.json", author_bundle)
    write_json(run / "fact-packets.draft.json", facts)
    write_json(run / "gold.draft.json", gold)
    review_template = {
        "contract": "tome4-quality-facts-study-gold-review-v1", "schema_version": 1,
        "study_id": sample["study_id"], "reviewer_id": "", "independent": True,
        "items": gold["items"],
    }
    adjudication_template = {
        "contract": "tome4-quality-facts-study-gold-adjudication-v1", "schema_version": 1,
        "study_id": sample["study_id"], "status": "draft", "adjudicator_id": "",
        "review_artifact_sha256s": ["", ""], "items": gold["items"],
    }
    write_json(run / "gold-review-a.template.json", review_template)
    write_json(run / "gold-review-b.template.json", review_template)
    write_json(run / "gold-adjudication.template.json", adjudication_template)
    report = {"study_id": sample["study_id"], "status": "authoring-required", "items": 20, "historical_exclusions": len(historical_exclusions), "sample": str(run / "sample.json"), "facts_author_bundle": str(run / "facts-author-bundle.json"), "facts": str(run / "fact-packets.draft.json"), "gold": str(run / "gold.draft.json"), "gold_reviews": [str(run / "gold-review-a.template.json"), str(run / "gold-review-b.template.json")], "gold_adjudication": str(run / "gold-adjudication.template.json"), "run_directory": str(run)}
    write_json(run / "build-report.json", report)
    return report


def run_bundles(manifest: Manifest, *, sample_path: Path, facts_path: Path, gold_path: Path, gold_review_paths: list[Path], gold_adjudication_path: Path) -> dict[str, Any]:
    protocol = load_protocol(manifest)
    sample = validate_sample(read_json_object(sample_path, "facts study sample"))
    validate_historical_exclusions(manifest, sample)
    facts = validate_packets(read_json_object(facts_path, "facts packet"), sample=sample, expected_kind="facts")
    neutral = build_neutral_packets(facts, sample=sample)
    validate_packets(neutral, sample=sample, expected_kind="neutral")
    validate_neutral_equivalence(facts, neutral)
    raw_gold = read_json_object(gold_path, "facts study gold")
    validate_gold(raw_gold, sample=sample, facts=facts, require_frozen=True)
    validate_gold_authoring_artifacts(
        review_paths=gold_review_paths, adjudication_path=gold_adjudication_path,
        gold=raw_gold, sample=sample, facts=facts,
    )
    prompts = {arm: load_arm_prompt(manifest, arm) for arm in ARMS}
    bundles = {arm: build_bundle(sample=sample, facts=facts, neutral=neutral, arm=arm, prompt_sha256=hashlib.sha256(prompts[arm].encode()).hexdigest()) for arm in ARMS}
    prereg = build_preregistration(protocol=protocol, sample=sample, facts=facts, neutral=neutral, gold=raw_gold, bundles=bundles, prompts=prompts)
    run = create_quality_run_directory(manifest.root, "facts-study-bundles")
    write_json(run / "neutral-packets.json", neutral)
    for arm, bundle in bundles.items(): write_json(run / f"bundle-{arm.lower()}.json", bundle)
    write_json(run / "preregistration.json", prereg)
    index = {"study_id": sample["study_id"], "preregistration_id": prereg["preregistration_id"], "slots": 33, "shards": 1, "bundles": {arm: str(run / f"bundle-{arm.lower()}.json") for arm in ARMS}, "neutral": str(run / "neutral-packets.json"), "preregistration": str(run / "preregistration.json"), "run_directory": str(run)}
    write_json(run / "index.json", index)
    return index


def load_study_inputs(manifest: Manifest, *, sample_path: Path, facts_path: Path, neutral_path: Path, gold_path: Path, prereg_path: Path, bundle_paths: list[Path]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    protocol = load_protocol(manifest)
    sample = validate_sample(read_json_object(sample_path, "facts study sample"))
    validate_historical_exclusions(manifest, sample)
    facts = validate_packets(read_json_object(facts_path, "facts packet"), sample=sample, expected_kind="facts")
    neutral = validate_packets(read_json_object(neutral_path, "neutral packet"), sample=sample, expected_kind="neutral")
    validate_neutral_equivalence(facts, neutral)
    raw_gold = read_json_object(gold_path, "facts study gold")
    gold = validate_gold(raw_gold, sample=sample, facts=facts, require_frozen=True)
    prompts = {arm: load_arm_prompt(manifest, arm) for arm in ARMS}
    bundles = {}
    for path in bundle_paths:
        raw = read_json_object(path, "facts study bundle")
        arm = raw.get("arm")
        if arm in bundles: raise ValidationError(f"duplicate facts study bundle arm: {arm}")
        prompt_sha = hashlib.sha256(prompts.get(arm, "").encode()).hexdigest()
        bundles[arm] = validate_bundle(raw, sample=sample, facts=facts, neutral=neutral, prompt_sha256=prompt_sha)
    if set(bundles) != set(ARMS): raise ValidationError("exactly one bundle for each of seven arms is required")
    prereg = validate_preregistration(read_json_object(prereg_path, "facts study preregistration"), protocol=protocol, sample=sample, facts=facts, neutral=neutral, gold=raw_gold, bundles=bundles, prompts=prompts)
    return sample, facts, neutral, gold, prereg, bundles


def validate_external_run_lineage(
    manifest: Manifest, *, prereg: dict[str, Any],
    assessment_paths_by_slot: dict[str, Path], runner_report_paths: list[Path],
) -> dict[str, str]:
    if len(runner_report_paths) != 33:
        raise ValidationError("external Facts study validation requires exactly 33 runner reports")
    slots = {slot["slot_id"]: slot for slot in prereg["schedule"]}
    reports: dict[str, str] = {}
    execution_ids: set[str] = set()
    authorization_hashes: set[str] = set()
    campaign = (
        manifest.root / ".artifacts" / "i18n" / "quality" / "facts-study-campaigns"
        / prereg["preregistration_id"]
    )
    expected_report_fields = {
        "contract", "ok", "study_id", "preregistration_id", "slot_id", "ordinal",
        "arm", "seed", "execution_id", "provider", "model", "thinking",
        "harness_sha256", "pi_executable",
        "cache_decision", "replacement_policy", "attempts",
        "charged_or_possible_transfers", "shards", "blind_inputs", "report",
        "run_directory", "runner_report_id", "assessment", "normalization",
        "assessment_sha256", "raw_output_sha256", "findings", "elapsed_seconds",
    }
    for path in runner_report_paths:
        report = read_json_object(path, "facts study runner report")
        _exact(report, expected_report_fields, "facts study runner report")
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
        if report["cache_decision"] != "disabled" or report["replacement_policy"] != "forbidden" or report["attempts"] != 1 or report["charged_or_possible_transfers"] != 1 or report["shards"] != 1:
            raise ValidationError(f"runner report transfer semantics mismatch: {slot_id}")
        if report["blind_inputs"] != {"gold": False, "other_assessments": False, "anchors": False, "holdout": False}:
            raise ValidationError(f"runner report blindness declaration mismatch: {slot_id}")
        expected_report_id = canonical_sha256({key: value for key, value in report.items() if key not in ("runner_report_id", "report", "run_directory", "elapsed_seconds")})
        if report["runner_report_id"] != expected_report_id:
            raise ValidationError(f"runner report ID is not canonical: {slot_id}")
        if Path(report["report"]).resolve() != path.resolve():
            raise ValidationError(f"runner report path does not bind the supplied file: {slot_id}")
        assessment_path = assessment_paths_by_slot.get(slot_id)
        if assessment_path is None or hashlib.sha256(assessment_path.read_bytes()).hexdigest() != report["assessment_sha256"]:
            raise ValidationError(f"runner report does not bind the supplied assessment bytes: {slot_id}")
        execution_id = _sha(report["execution_id"], f"runner report {slot_id}.execution_id")
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
        authorization_hashes.add(_sha(ledger.get("authorization_sha256"), f"slot ledger {slot_id}.authorization_sha256"))
        reports[slot_id] = str(path)
    if set(reports) != set(slots):
        raise ValidationError("runner report membership does not match all 33 preregistered slots")
    if len(authorization_hashes) != 1:
        raise ValidationError("all 33 Facts study slots must bind the same explicit authorization")
    return reports


def run_validate(
    manifest: Manifest, *, sample_path: Path, facts_path: Path, neutral_path: Path,
    gold_path: Path, prereg_path: Path, bundle_paths: list[Path],
    assessment_paths: list[Path], runner_report_paths: list[Path], fake_runner: bool,
) -> dict[str, Any]:
    sample, facts, _, gold, prereg, bundles = load_study_inputs(
        manifest, sample_path=sample_path, facts_path=facts_path,
        neutral_path=neutral_path, gold_path=gold_path, prereg_path=prereg_path,
        bundle_paths=bundle_paths,
    )
    slot_by_id = {slot["slot_id"]: slot for slot in prereg["schedule"]}
    if fake_runner:
        if assessment_paths or runner_report_paths:
            raise ValidationError("--fake-runner cannot be combined with assessments or runner reports")
        raw_assessments = build_fake_assessments(
            preregistration=prereg, sample=sample, gold=gold, bundles=bundles
        )
    else:
        if len(assessment_paths) != 33:
            raise ValidationError("facts-study-validate requires exactly 33 assessments")
        raw_assessments = {}
        original_assessment_paths = {}
        for path in assessment_paths:
            raw = read_json_object(path, "facts study assessment")
            slot_id = raw.get("slot_id")
            if slot_id in raw_assessments:
                raise ValidationError(f"duplicate facts study slot: {slot_id}")
            raw_assessments[slot_id] = raw
            original_assessment_paths[slot_id] = path
        validate_external_run_lineage(
            manifest, prereg=prereg,
            assessment_paths_by_slot=original_assessment_paths,
            runner_report_paths=runner_report_paths,
        )
    if set(raw_assessments) != set(slot_by_id):
        raise ValidationError("assessment slot membership does not match the frozen 33-slot schedule")
    normalized = {}
    for slot_id, raw in raw_assessments.items():
        slot = slot_by_id[slot_id]
        normalized[slot_id] = validate_assessment(
            raw, sample=sample, facts=facts, bundle=bundles[slot["arm"]], slot=slot
        )
    run = create_quality_run_directory(manifest.root, "facts-study-fake" if fake_runner else "facts-study-validate")
    paths = {}
    for slot_id in sorted(normalized):
        path = run / "assessments" / f"{slot_id}.json"
        # Persist the model-owned form. Normalized evidence contains host-only
        # offsets and must be recomputed by every downstream consumer.
        write_json(path, raw_assessments[slot_id])
        paths[slot_id] = str(path)
    index = {
        "contract": "tome4-quality-facts-study-validation-index-v1",
        "schema_version": 1, "study_id": sample["study_id"],
        "preregistration_id": prereg["preregistration_id"],
        "mode": "offline-fake-replay" if fake_runner else "external-assessments",
        "structure_validity": {"numerator": 33, "denominator": 33, "value": 1.0},
        "evidence_validity": {"numerator": 33, "denominator": 33, "value": 1.0},
        "inputs": {
            "sample": str(sample_path), "facts": str(facts_path),
            "neutral": str(neutral_path), "gold": str(gold_path),
            "preregistration": str(prereg_path),
            "bundles": [str(path) for path in bundle_paths],
        },
        "assessments": paths, "run_directory": str(run), "validation_id": "",
        "runner_reports": {} if fake_runner else {
            read_json_object(path, "facts study runner report")["slot_id"]: str(path)
            for path in runner_report_paths
        },
    }
    index["validation_id"] = canonical_sha256({key: val for key, val in index.items() if key not in ("validation_id", "run_directory")})
    path = run / "validation-index.json"
    write_json(path, index)
    return {**index, "validation": str(path)}


def run_report(manifest: Manifest, *, validation_path: Path) -> dict[str, Any]:
    validation = read_json_object(validation_path, "facts study validation index")
    if validation.get("contract") != "tome4-quality-facts-study-validation-index-v1":
        raise ValidationError("unsupported facts study validation index")
    expected_validation_id = canonical_sha256({key: value for key, value in validation.items() if key not in ("validation_id", "run_directory")})
    if validation.get("validation_id") != expected_validation_id:
        raise ValidationError("facts study validation_id is not canonical")
    if validation.get("mode") not in ("offline-fake-replay", "external-assessments"):
        raise ValidationError("facts study validation mode is invalid")
    inputs = validation.get("inputs")
    if not isinstance(inputs, dict):
        raise ValidationError("facts study validation index is missing inputs")
    sample, facts, _, gold, prereg, bundles = load_study_inputs(
        manifest, sample_path=Path(inputs["sample"]), facts_path=Path(inputs["facts"]),
        neutral_path=Path(inputs["neutral"]), gold_path=Path(inputs["gold"]),
        prereg_path=Path(inputs["preregistration"]),
        bundle_paths=[Path(path) for path in inputs["bundles"]],
    )
    assessments = {}
    slot_by_id = {slot["slot_id"]: slot for slot in prereg["schedule"]}
    for slot_id, path in validation.get("assessments", {}).items():
        slot = slot_by_id.get(slot_id)
        if slot is None:
            raise ValidationError(f"validation index contains unknown slot: {slot_id}")
        assessments[slot_id] = validate_assessment(
            read_json_object(Path(path), "facts study assessment"), sample=sample,
            facts=facts, bundle=bundles[slot["arm"]], slot=slot,
        )
    if validation["mode"] == "external-assessments":
        validate_external_run_lineage(
            manifest, prereg=prereg,
            assessment_paths_by_slot={slot_id: Path(path) for slot_id, path in validation["assessments"].items()},
            runner_report_paths=[Path(path) for path in validation.get("runner_reports", {}).values()],
        )
    report = build_report(
        preregistration=prereg, gold=gold, assessments=assessments, sample=sample,
        protocol=load_protocol(manifest), evidence_mode=validation["mode"],
    )
    if validation["mode"] == "offline-fake-replay":
        report["decision"] = {
            "result": "non-evidentiary-offline-replay",
            "criteria": {},
        }
    report["report_id"] = canonical_sha256({key: value for key, value in report.items() if key != "report_id"})
    run = create_quality_run_directory(manifest.root, "facts-study-report")
    path = run / "report.json"
    write_json(path, report)
    return {**report, "report": str(path), "run_directory": str(run)}


EXECUTION_MANIFEST_CONTRACT = "tome4-quality-facts-study-execution-manifest-v1"


def build_execution_manifest(
    *, preregistration: dict[str, Any], authorization_id: str,
    granted_at: str, granted_by: str = "user",
    execution_mode: str = "sequential", concurrency: int = 1,
    transmission_failure_max_retries: int = 0,
) -> dict[str, Any]:
    """Authorized execution manifest for an offline-frozen preregistration.

    The offline-frozen preregistration itself can never be executed; a future
    external phase is only possible through this manifest, which binds the
    user authorization record to the frozen prereg bytes and the exact
    33-slot schedule.
    """
    if not authorization_id.strip():
        raise ValidationError("execution manifest requires a non-empty authorization_id")
    if not granted_at.strip():
        raise ValidationError("execution manifest requires a granted_at timestamp")
    if execution_mode not in ("sequential", "parallel"):
        raise ValidationError("execution manifest mode must be sequential or parallel")
    if type(concurrency) is not int or concurrency < 1 or concurrency > 33:
        raise ValidationError("execution manifest concurrency must be an integer in 1..33")
    if type(transmission_failure_max_retries) is not int or transmission_failure_max_retries < 0 or transmission_failure_max_retries > 3:
        raise ValidationError("execution manifest transmission retries must be 0..3")
    prereg_sha = canonical_sha256(preregistration)
    providers: dict[str, Any] = {}
    for slot in preregistration["schedule"]:
        evaluator = slot["evaluator_id"]
        providers.setdefault(evaluator, {
            "provider": slot["provider"], "model": slot["model"], "thinking": slot["thinking"], "slots": 0,
        })
        providers[evaluator]["slots"] += 1
    value = {
        "contract": EXECUTION_MANIFEST_CONTRACT, "schema_version": 1,
        "preregistration_id": preregistration["preregistration_id"],
        "preregistration_sha256": prereg_sha,
        "authorization": {
            "authorization_id": authorization_id,
            "granted_by": granted_by, "granted_at": granted_at,
            "scope": "external-facts-study-campaign",
            "providers": providers,
            "item_count": len(preregistration["item_order"]),
            "shard_count": preregistration["shard_count"],
            "max_external_slots": preregistration["max_external_slots"],
            "cache": preregistration["cache_policy"],
            "replacement": preregistration["replacement_policy"],
            "failure_policy": "no-retry-no-replacement",
        },
        "execution": {
            "mode": execution_mode, "concurrency": concurrency,
            "order_policy": "ordinal-submission" if execution_mode == "sequential" else "parallel-all-slots-unique-non-replaceable",
            "retry": {
                "transmission_failure_max_retries": transmission_failure_max_retries,
                "content_failure_retries": 0,
            },
        },
        "schedule": preregistration["schedule"],
        "manifest_id": "",
    }
    value["manifest_id"] = canonical_sha256(
        {key: val for key, val in value.items() if key != "manifest_id"}
    )
    return value


def validate_execution_manifest(value: dict[str, Any], *, preregistration: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError("execution manifest must be an object")
    _exact(value, ("contract", "schema_version", "preregistration_id", "preregistration_sha256", "authorization", "execution", "schedule", "manifest_id"), "execution manifest")
    if value["contract"] != EXECUTION_MANIFEST_CONTRACT or value["schema_version"] != 1:
        raise ValidationError("unsupported execution manifest contract")
    if value["preregistration_id"] != preregistration["preregistration_id"]:
        raise ValidationError("execution manifest does not bind this preregistration")
    if value["preregistration_sha256"] != canonical_sha256(preregistration):
        raise ValidationError("execution manifest does not bind the frozen preregistration bytes")
    expected = build_execution_manifest(
        preregistration=preregistration,
        authorization_id=value["authorization"]["authorization_id"],
        granted_at=value["authorization"]["granted_at"],
        granted_by=value["authorization"].get("granted_by", "user"),
        execution_mode=value["execution"]["mode"],
        concurrency=value["execution"]["concurrency"],
        transmission_failure_max_retries=value["execution"]["retry"]["transmission_failure_max_retries"],
    )
    if value != expected:
        raise ValidationError("execution manifest is not the deterministic expected artifact")
    if value["schedule"] != preregistration["schedule"]:
        raise ValidationError("execution manifest schedule must equal the preregistered schedule")
    return value
