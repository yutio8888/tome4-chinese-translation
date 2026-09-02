"""Exact WP2-Lite catalog candidate and read-only WP1 retirement preflight."""
from __future__ import annotations

import hashlib
import os
import shutil
import stat
import subprocess
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from . import production_review as wp1
from .config import Manifest
from .runtime import LuaRuntime

FROZEN_RULES_VERSION = wp1.ledger.FORMAL_RULES_VERSION_V1
RULES_VERSION = wp1.ledger.FORMAL_RULES_VERSION_V2
SUPPORTED_RULES_VERSIONS = wp1.ledger.FORMAL_RULES_VERSIONS
CATALOG_KIND = "production_review_v2_lite_catalog_v1"
CALL_LOCATOR_KIND = "production_review_v2_lite_call_locator_v1"
OCCURRENCE_KIND = "production_review_v2_lite_occurrence_v1"
CURRENT_VECTOR = (30308, 29828, 480)
TRACKED_LIMIT = 134217728
BASELINE_HEAD = "a287652c344a3e37199fe0af2d8a6b4cdf25f0b2"
SCHEMA_PATH = "i18n/quality/production-review-v2-lite/catalog-v1.schema.json"
POLICY_PATH = "i18n/quality/production-review-v2-lite/policy-v1.json"
CATALOG_PREFIX = "evidence/production-review-v2-lite/catalog"
CANDIDATE_FILES = frozenset({SCHEMA_PATH, POLICY_PATH, f"{CATALOG_PREFIX}/manifest.json",
                             f"{CATALOG_PREFIX}/entries.jsonl", f"{CATALOG_PREFIX}/exclusions.jsonl"})
MANIFEST_KEYS = frozenset({"schema_version", "kind", "catalog_id", "rules_version", "recorded_at",
    "recorded_by", "manifest_sha256", "loader_contract_path", "loader_contract_sha256",
    "lua_runtime", "manifest_component_ordinals", "component_counts", "occurrence_count",
    "entry_count", "exclusion_count", "entries_sha256", "exclusions_sha256",
    "terminology_snapshot_sha256", "source_identities", "policy_sha256"})
ENTRY_KEYS = frozenset({"schema_version", "component", "normalized_path", "section", "call_locator",
    "logical_entry_identity", "entry_revision_identity", "source", "target", "source_tag",
    "source_sha256", "target_sha256", "fixed_source_identity", "terminology_snapshot_sha256",
    "rules_version", "risk"})
EXCLUSION_PRIORITY = ("outside_initial_six_component_scope", "empty_source", "empty_target")
SCHEMA_VALUE = {"schema_version": 1, "kind": "production_review_v2_lite_catalog_schema_v1",
    "catalog_kind": CATALOG_KIND, "manifest_keys": sorted(MANIFEST_KEYS),
    "entry_keys": sorted(ENTRY_KEYS), "exclusion_keys": sorted(wp1.EXCLUSION_KEYS),
    "risk_keys": sorted(wp1.RISK_KEYS),
    "entry_order": "entry_revision_identity_lowercase_ascii_strict",
    "exclusion_order": "occurrence_identity_lowercase_ascii_strict",
    "canonical_json": "utf8_sorted_keys_compact_no_nan", "jsonl_final_lf": True}
def _policy_value(rules_version: str) -> dict[str, Any]:
    return {"schema_version": 1, "kind": "production_review_v2_lite_policy_v1",
        "rules_version": rules_version, "call_locator_kind": CALL_LOCATOR_KIND,
        "occurrence_kind": OCCURRENCE_KIND, "eligible_components": sorted(wp1.IN_SCOPE_COMPONENTS),
        "exclusion_priority": list(EXCLUSION_PRIORITY), "current_version_vector": {
            "occurrence_count": CURRENT_VECTOR[0], "entry_count": CURRENT_VECTOR[1],
            "exclusion_count": CURRENT_VECTOR[2]}}

FROZEN_POLICY_VALUE = _policy_value(FROZEN_RULES_VERSION)
POLICY_VALUE = _policy_value(RULES_VERSION)
SCHEMA_RAW = wp1.canonical_bytes(SCHEMA_VALUE)
FROZEN_POLICY_RAW = wp1.canonical_bytes(FROZEN_POLICY_VALUE)
POLICY_RAW = wp1.canonical_bytes(POLICY_VALUE)
POLICY_RAW_BY_RULES = {
    FROZEN_RULES_VERSION: FROZEN_POLICY_RAW,
    RULES_VERSION: POLICY_RAW,
}
WP1_RETIREMENT_ROOTS = frozenset({
    "evidence/production-review/batches/35eee018cacf0048ebcad2c5de01423dce900777a92d52a7b4c89e0085862306",
    "evidence/production-review/catalogs/1001066b5d575524a5c2966d462e03b3a06b38c3232c098eaa459de1e0a29567",
    "evidence/production-review/locator-snapshots/ea8e0f5bf078e63d4411ed5518f79950960bf9aa7b36ea621ae14ead6dadcec5",
    "evidence/production-review/shadow-journals/705606c15ec0fc1526cf40345c23f7b79205b992007e2cc873fa3c0cb272184c",
    "i18n/quality/production-review/schemas-v1.json",
    "i18n/quality/production-review/shadow-policies/a177ad59ed744a00b98af91b3fbcd989db4097b631bd46c1fc23ddb3f5d8af58",
})
WP1_FAMILY_PREFIXES = ("evidence/production-review/", "i18n/quality/production-review/")
WP1_FILES = {
"evidence/production-review/batches/35eee018cacf0048ebcad2c5de01423dce900777a92d52a7b4c89e0085862306/manifest.json":"018970f667b3ee1093e5175ed59936b85dd8a29ee4641c76247761a2dd7c77d5",
"evidence/production-review/catalogs/1001066b5d575524a5c2966d462e03b3a06b38c3232c098eaa459de1e0a29567/entries.jsonl":"1c69eb09dba94e8f7879af60e2ec05e430429e7028340d4d608e38acfccd2621",
"evidence/production-review/catalogs/1001066b5d575524a5c2966d462e03b3a06b38c3232c098eaa459de1e0a29567/exclusions.jsonl":"35b161d41302e493cb6d45d2be946ca0122c92012ca1edd50d94b99d88231e43",
"evidence/production-review/catalogs/1001066b5d575524a5c2966d462e03b3a06b38c3232c098eaa459de1e0a29567/manifest.json":"e579e48c4095bb1565f28d01fff6ed2cf4c5713f675d813c14307336f73d02e3",
"evidence/production-review/locator-snapshots/ea8e0f5bf078e63d4411ed5518f79950960bf9aa7b36ea621ae14ead6dadcec5/locators.jsonl":"f6a2d8ac1a5500d466a9c32ddaa6d76311d6817516754be4e499e69163e968ef",
"evidence/production-review/locator-snapshots/ea8e0f5bf078e63d4411ed5518f79950960bf9aa7b36ea621ae14ead6dadcec5/manifest.json":"dae1b2bed19b168f9a4dc98eb7ed30edeea4a3b21f3b0832e887c70b02f277f2",
"evidence/production-review/locator-snapshots/ea8e0f5bf078e63d4411ed5518f79950960bf9aa7b36ea621ae14ead6dadcec5/occurrences.jsonl":"cfb3e83c043cfe419ab6f0d7ffdf000e2ea01406db3adf61ae713dc7fa216ab4",
"evidence/production-review/shadow-journals/705606c15ec0fc1526cf40345c23f7b79205b992007e2cc873fa3c0cb272184c/checkpoint.json":"9916bfc9fb66f9ff006b7ec4a59693045db7a8d9939d0b4b1ab9fb302911d9c8",
"evidence/production-review/shadow-journals/705606c15ec0fc1526cf40345c23f7b79205b992007e2cc873fa3c0cb272184c/events.jsonl":"7001ac7d4458c37f6e3d91c44b75169ad05db4118cee555ad2a9159828ba5e39",
"evidence/production-review/shadow-journals/705606c15ec0fc1526cf40345c23f7b79205b992007e2cc873fa3c0cb272184c/group.json":"8ff3e7123801fe5e08e329a372aedc86b34b66ce4253939d8fcb8698f528f4fd",
"i18n/quality/production-review/schemas-v1.json":"7881ce527032927b34dcc6b7ec050be6669e2f76f70b0a3ccd1f72666e7390fd",
"i18n/quality/production-review/shadow-policies/a177ad59ed744a00b98af91b3fbcd989db4097b631bd46c1fc23ddb3f5d8af58/policy.json":"b2e2bc0f67e6376baea3243aa7e9a15c16543512c9d5af48baae1819f24413fd"}


def observation_identity(contract: object, revision: object,
                         verdict: object, observation: object) -> str:
    """Return the identity of one current-consumer observation."""
    if (not isinstance(contract, str) or not contract or
            not isinstance(revision, str) or not revision or
            verdict != "ISSUE"):
        raise wp1.ProductionReviewError("observation identity has invalid contract/revision/verdict")
    return hashlib.sha256(wp1.canonical_bytes({
        "contract": contract,
        "entry_revision_identity": revision,
        "verdict": verdict,
        "observation": observation,
    })).hexdigest()


def fold_issue_observations(observations: Iterable[dict[str, Any]],
                            decisions: Iterable[dict[str, Any]], *,
                            require_complete: bool = True) -> dict[str, str]:
    """Fold all ISSUE decisions for each revision into one durable state.

    This is intentionally shared by the active checkpoint projection and the
    Git-tree replay.  A surface ISSUE and a contextual ISSUE are separate
    observations, while a surface ISSUE remains authoritative even when its
    contextual run later reports OK.  ``decisions`` is current producer input;
    legacy durable rows are normalized by the reader before calling here.
    """
    issue_by_identity: dict[str, dict[str, Any]] = {}
    for observation in observations:
        if not isinstance(observation, dict) or observation.get("verdict") != "ISSUE":
            continue
        contract = observation.get("contract")
        revision = observation.get("entry_revision_identity")
        identity = observation.get("observation_identity")
        expected = observation_identity(contract, revision, "ISSUE",
                                        observation.get("observation"))
        if identity is None:
            identity = expected
        if identity != expected or identity in issue_by_identity:
            raise wp1.ProductionReviewError("ISSUE observation identity is duplicated or not current")
        issue_by_identity[identity] = observation

    decision_by_identity: dict[str, dict[str, Any]] = {}
    for decision in decisions:
        if not isinstance(decision, dict):
            raise wp1.ProductionReviewError("observation decision must be an object")
        identity = decision.get("observation_identity")
        if (not isinstance(identity, str) or identity not in issue_by_identity or
                identity in decision_by_identity):
            raise wp1.ProductionReviewError("observation decision does not name one current ISSUE")
        observation = issue_by_identity[identity]
        if (decision.get("entry_revision_identity") != observation["entry_revision_identity"] or
                decision.get("observation_contract") != observation["contract"]):
            raise wp1.ProductionReviewError("observation decision contract/revision mismatch")
        disposition = decision.get("disposition")
        repair_required = decision.get("repair_required")
        if (disposition not in {"confirmed", "pending", "advisory", "refuted"} or
                type(repair_required) is not bool or
                (disposition != "confirmed" and repair_required)):
            raise wp1.ProductionReviewError("observation decision disposition is invalid")
        decision_by_identity[identity] = decision

    if require_complete and set(decision_by_identity) != set(issue_by_identity):
        raise wp1.ProductionReviewError("observation decisions do not exactly cover current ISSUE observations")

    priority = {"done": 0, "blocked": 1, "repair_required": 2}
    folded: dict[str, str] = {}
    for identity, observation in issue_by_identity.items():
        decision = decision_by_identity.get(identity)
        if decision is None:
            continue
        if decision["disposition"] == "confirmed" and decision["repair_required"]:
            state = "repair_required"
        elif decision["disposition"] == "pending":
            state = "blocked"
        else:
            state = "done"
        revision = observation["entry_revision_identity"]
        if priority[state] > priority.get(folded.get(revision), -1):
            folded[revision] = state
    return folded


def _plain_id(kind: str, key: str, value: object) -> str:
    return hashlib.sha256(wp1.canonical_bytes({"kind": kind, key: value})).hexdigest()


def catalog_id(value: dict[str, Any]) -> str:
    core = dict(value)
    for key in ("catalog_id", "recorded_at", "recorded_by"): core.pop(key, None)
    return hashlib.sha256(wp1.canonical_bytes(core)).hexdigest()


def _reason(row: dict[str, Any]) -> str | None:
    if row["component"] not in wp1.IN_SCOPE_COMPONENTS: return EXCLUSION_PRIORITY[0]
    if not row["source"]: return EXCLUSION_PRIORITY[1]
    if not row["target"]: return EXCLUSION_PRIORITY[2]
    return None


def formal_rows(occurrences: Iterable[dict[str, Any]], *, terminology: str,
                sources: dict[str, str], rules_version: str = RULES_VERSION,
                ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if rules_version not in SUPPORTED_RULES_VERSIONS:
        raise wp1.ProductionReviewError("unsupported formal catalog rules version")
    rows = [wp1.validate_occurrence(row) for row in occurrences]
    grouped = Counter((r["component"], r["source"], r["source_tag"] or "") for r in rows)
    seen: Counter[tuple[str, str, str]] = Counter(); entries=[]; exclusions=[]; locators=set()
    for row in rows:
        tag=row["source_tag"] or ""
        core={"component":row["component"],"duplicate_index":0,"function_name":row["function_name"],
              "normalized_source_tag":tag,"section":row["section"],"source":row["source"],
              "translation_path":row["translation_path"]}
        locator=_plain_id(CALL_LOCATOR_KIND,"locator",core)
        if locator in locators: raise wp1.ProductionReviewError("formal call locator collision")
        locators.add(locator); occurrence_id=_plain_id(OCCURRENCE_KIND,"occurrence",row); reason=_reason(row)
        if reason:
            exclusions.append({"schema_version":1,"occurrence_identity":occurrence_id,
                               "component":row["component"],"reason_code":reason}); continue
        fixed=sources.get(row["component"])
        if not fixed: raise wp1.ProductionReviewError(f"missing fixed source identity for {row['component']}")
        try: normalized=wp1.surface.normalize_relative_path(row["translation_path"])
        except wp1.surface.ContractError as error: raise wp1.ProductionReviewError(f"invalid formal path: {error}") from error
        if normalized != row["translation_path"]: raise wp1.ProductionReviewError("translation_path is not normalized")
        logical=wp1.surface.logical_entry_identity(component=row["component"],normalized_path=normalized,
                                                    call_locator=locator,source_tag=tag)
        revision=wp1.surface.entry_revision_identity(logical_entry_identity=logical,source=row["source"],
            target=row["target"],fixed_source_identity=fixed,terminology_snapshot=terminology,rules_version=rules_version)
        group=(row["component"],row["source"],tag); seen[group]+=1
        entries.append({"schema_version":1,"component":row["component"],"normalized_path":normalized,
            "section":row["section"],"call_locator":locator,"logical_entry_identity":logical,
            "entry_revision_identity":revision,"source":row["source"],"target":row["target"],"source_tag":tag,
            "source_sha256":hashlib.sha256(row["source"].encode()).hexdigest(),
            "target_sha256":hashlib.sha256(row["target"].encode()).hexdigest(),"fixed_source_identity":fixed,
            "terminology_snapshot_sha256":terminology,"rules_version":rules_version,
            "risk":{"has_args_order":row["args_order"] is not None,"has_special":row["special"] is not None,
                "source_utf8_bytes":len(row["source"].encode()),"target_utf8_bytes":len(row["target"].encode()),
                "component_group_size":grouped[group],"component_group_last":seen[group]==grouped[group]}})
    entries.sort(key=lambda r:r["entry_revision_identity"].encode("ascii"))
    exclusions.sort(key=lambda r:r["occurrence_identity"].encode("ascii"))
    for key in ("entry_revision_identity","logical_entry_identity"):
        if len({r[key] for r in entries}) != len(entries): raise wp1.ProductionReviewError(f"formal {key} collision")
    return entries, exclusions


def build_catalog(manifest: Manifest, *, recorded_at: str, recorded_by: str,
                  require_current_vector: bool=True) -> dict[str, bytes]:
    wp1.strict_utc_seconds(recorded_at); wp1._nonempty(recorded_by,"recorded_by")
    runtime=LuaRuntime(manifest).doctor(); occurrences=wp1.load_occurrences(manifest)
    terminology=wp1.terminology_snapshot(manifest.root); sources=wp1.source_identities_from_manifest(manifest)
    entries,exclusions=formal_rows(occurrences,terminology=terminology,sources=sources)
    observed=(len(occurrences),len(entries),len(exclusions))
    if require_current_vector and observed != CURRENT_VECTOR:
        raise wp1.ProductionReviewError(f"formal current version vector drift: observed={observed} expected={CURRENT_VECTOR}")
    entries_raw,exclusions_raw=wp1._jsonl(entries),wp1._jsonl(exclusions)
    contract=manifest.root/"tools/i18nlib/locale_model.py"
    try: contract_raw=contract.read_bytes()
    except OSError as error: raise wp1.ProductionReviewError(f"cannot read loader contract: {error}") from error
    value={"schema_version":1,"kind":CATALOG_KIND,"catalog_id":"","rules_version":RULES_VERSION,
        "recorded_at":recorded_at,"recorded_by":recorded_by,
        "manifest_sha256":hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "loader_contract_path":"tools/i18nlib/locale_model.py","loader_contract_sha256":hashlib.sha256(contract_raw).hexdigest(),
        "lua_runtime":runtime["lua_version"],"manifest_component_ordinals":wp1._component_ordinals(c.id for c in manifest.components),
        "component_counts":dict(sorted(Counter(r["component"] for r in occurrences).items())),
        "occurrence_count":len(occurrences),"entry_count":len(entries),"exclusion_count":len(exclusions),
        "entries_sha256":hashlib.sha256(entries_raw).hexdigest(),"exclusions_sha256":hashlib.sha256(exclusions_raw).hexdigest(),
        "terminology_snapshot_sha256":terminology,"source_identities":dict(sorted(sources.items())),
        "policy_sha256":hashlib.sha256(POLICY_RAW).hexdigest()}
    value["catalog_id"]=catalog_id(value); manifest_raw=wp1.canonical_bytes(value)
    _validate_formal_manifest(manifest_raw)
    _validate_migration_manifest(value, POLICY_RAW)
    return {SCHEMA_PATH:SCHEMA_RAW,POLICY_PATH:POLICY_RAW,f"{CATALOG_PREFIX}/manifest.json":manifest_raw,
            f"{CATALOG_PREFIX}/entries.jsonl":entries_raw,f"{CATALOG_PREFIX}/exclusions.jsonl":exclusions_raw}


def _validate_migration_policy(raw: bytes) -> dict[str, Any]:
    """Validate exact frozen-v1 or current-v2 policy bytes."""
    value = wp1.parse_canonical_object(raw, "prospective migration policy")
    if raw not in POLICY_RAW_BY_RULES.values():
        raise wp1.ProductionReviewError("prospective migration policy bytes are not a supported exact policy")
    if set(value) != set(POLICY_VALUE):
        raise wp1.ProductionReviewError("prospective migration policy exact keys mismatch")
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise wp1.ProductionReviewError("prospective migration policy schema_version must be integer 1")
    for key, expected in POLICY_VALUE.items():
        if key != "rules_version" and value[key] != expected:
            raise wp1.ProductionReviewError(f"prospective migration policy {key} drift")
    if value["rules_version"] not in SUPPORTED_RULES_VERSIONS:
        raise wp1.ProductionReviewError("prospective migration policy rules_version is unsupported")
    return value


def _validate_formal_manifest(raw: bytes) -> dict[str, Any]:
    """Run the existing formal ledger catalog consumer on exact manifest bytes."""
    try:
        return wp1.ledger.validate_authoritative_catalog(
            raw, expected_sha256=hashlib.sha256(raw).hexdigest())
    except wp1.ledger.LedgerError as error:
        raise wp1.ProductionReviewError(f"invalid formal catalog manifest: {error}") from error


def _validate_migration_manifest(value: object, policy_raw: bytes) -> dict[str, Any]:
    """Validate the exact policy binding shared by ordinary and migration paths."""
    if not isinstance(value, dict) or set(value) != set(MANIFEST_KEYS):
        raise wp1.ProductionReviewError("prospective migration manifest exact keys mismatch")
    row = value
    if type(row["schema_version"]) is not int or row["schema_version"] != 1:
        raise wp1.ProductionReviewError("prospective migration manifest schema_version must be integer 1")
    if row["kind"] != CATALOG_KIND or not isinstance(row["rules_version"], str) or not row["rules_version"]:
        raise wp1.ProductionReviewError("prospective migration manifest kind/rules mismatch")
    for key in ("catalog_id", "manifest_sha256", "loader_contract_sha256", "entries_sha256",
                "exclusions_sha256", "terminology_snapshot_sha256", "policy_sha256"):
        if not isinstance(row[key], str) or not wp1.SHA256_RE.fullmatch(row[key]):
            raise wp1.ProductionReviewError(f"prospective migration manifest {key} must be a lowercase SHA-256")
    for key in ("recorded_at", "recorded_by", "loader_contract_path", "lua_runtime"):
        if not isinstance(row[key], str) or not row[key]:
            raise wp1.ProductionReviewError(f"prospective migration manifest {key} must be non-empty")
    wp1.strict_utc_seconds(row["recorded_at"])
    if row["loader_contract_path"] != "tools/i18nlib/locale_model.py":
        raise wp1.ProductionReviewError("prospective migration loader contract path mismatch")
    for key in ("occurrence_count", "entry_count", "exclusion_count"):
        if type(row[key]) is not int or row[key] < 0:
            raise wp1.ProductionReviewError(f"prospective migration manifest {key} is invalid")
    if row["occurrence_count"] != row["entry_count"] + row["exclusion_count"]:
        raise wp1.ProductionReviewError("prospective migration manifest conservation mismatch")
    counts = row["component_counts"]
    if (not isinstance(counts, dict) or not counts or
            any(not isinstance(key, str) or not key or type(number) is not int or number < 0
                for key, number in counts.items()) or
            sum(counts.values()) != row["occurrence_count"]):
        raise wp1.ProductionReviewError("prospective migration component counts mismatch")
    ordinals = row["manifest_component_ordinals"]
    if not isinstance(ordinals, list) or not ordinals:
        raise wp1.ProductionReviewError("prospective migration component ordinals are invalid")
    components = []
    for index, ordinal in enumerate(ordinals):
        if (not isinstance(ordinal, dict) or set(ordinal) != {"component", "ordinal"} or
                not isinstance(ordinal["component"], str) or not ordinal["component"] or
                type(ordinal["ordinal"]) is not int or ordinal["ordinal"] != index):
            raise wp1.ProductionReviewError("prospective migration component ordinal binding mismatch")
        components.append(ordinal["component"])
    if len(set(components)) != len(components) or set(counts) != set(components):
        raise wp1.ProductionReviewError("prospective migration component set mismatch")
    sources = row["source_identities"]
    required = set(wp1.IN_SCOPE_COMPONENTS)
    if (not isinstance(sources, dict) or not required.issubset(sources) or
            not set(sources).issubset(components) or
            any(not isinstance(key, str) or not isinstance(source, str) or
                not wp1.SOURCE_ID_RE.fullmatch(source)
                for key, source in sources.items())):
        raise wp1.ProductionReviewError("prospective migration source identities mismatch")
    policy = _validate_migration_policy(policy_raw)
    if row["rules_version"] != policy["rules_version"]:
        raise wp1.ProductionReviewError("prospective migration manifest/policy rules mismatch")
    if row["policy_sha256"] != hashlib.sha256(policy_raw).hexdigest():
        raise wp1.ProductionReviewError("prospective migration policy hash mismatch")
    core = dict(row)
    for key in ("catalog_id", "recorded_at", "recorded_by"):
        core.pop(key)
    if row["catalog_id"] != hashlib.sha256(wp1.canonical_bytes(core)).hexdigest():
        raise wp1.ProductionReviewError("prospective migration catalog self-ID mismatch")
    return row


def validate_catalog_files(files: dict[str, bytes]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate exact frozen-v1 or current-v2 catalog bytes."""
    def exact(value: object, keys: frozenset[str], label: str) -> dict[str, Any]:
        if not isinstance(value, dict) or set(value) != keys:
            raise wp1.ProductionReviewError(f"{label} exact keys mismatch")
        return value

    def sha(value: object, label: str) -> str:
        if not isinstance(value, str) or not wp1.SHA256_RE.fullmatch(value):
            raise wp1.ProductionReviewError(f"{label} must be a lowercase SHA-256")
        return value

    def schema_one(value: object, label: str) -> None:
        if type(value) is not int or value != 1:
            raise wp1.ProductionReviewError(f"{label} schema_version must be integer 1")

    try:
        if set(files) != set(CANDIDATE_FILES):
            raise wp1.ProductionReviewError(
                f"formal catalog exact file set mismatch (missing={sorted(CANDIDATE_FILES-set(files))}, "
                f"extra={sorted(set(files)-CANDIDATE_FILES)})")
        if files[SCHEMA_PATH] != SCHEMA_RAW:
            raise wp1.ProductionReviewError("formal catalog schema bytes mismatch")
        if files[POLICY_PATH] not in POLICY_RAW_BY_RULES.values():
            raise wp1.ProductionReviewError("formal catalog policy bytes mismatch")
        manifest_raw = files[f"{CATALOG_PREFIX}/manifest.json"]
        manifest = _validate_formal_manifest(manifest_raw)
        _validate_migration_manifest(manifest, files[POLICY_PATH])
        entries_raw = files[f"{CATALOG_PREFIX}/entries.jsonl"]
        exclusions_raw = files[f"{CATALOG_PREFIX}/exclusions.jsonl"]
        entries = wp1.parse_jsonl(entries_raw, "formal catalog entries")
        exclusions = wp1.parse_jsonl(exclusions_raw, "formal catalog exclusions")
        previous = ""
        seen_revisions: set[str] = set()
        seen_logical: set[str] = set()
        for index, item in enumerate(entries):
            row = exact(item, ENTRY_KEYS, f"formal catalog entry {index}")
            risk = exact(row["risk"], wp1.RISK_KEYS, f"formal catalog entry {index} risk")
            schema_one(row["schema_version"], f"formal catalog entry {index}")
            if row["rules_version"] not in SUPPORTED_RULES_VERSIONS or row["rules_version"] != manifest["rules_version"]:
                raise wp1.ProductionReviewError(f"formal catalog entry {index} rules mismatch")
            for key in ("component", "normalized_path", "section", "call_locator", "logical_entry_identity",
                        "entry_revision_identity", "source", "target", "source_tag", "source_sha256",
                        "target_sha256", "fixed_source_identity", "terminology_snapshot_sha256", "rules_version"):
                if not isinstance(row[key], str):
                    raise wp1.ProductionReviewError(f"formal catalog entry {index} {key} must be a string")
            normalized = wp1.surface.normalize_relative_path(row["normalized_path"])
            if normalized != row["normalized_path"]:
                raise wp1.ProductionReviewError("formal catalog normalized path drift")
            wp1.surface.validate_call_locator(row["call_locator"])
            revision = sha(row["entry_revision_identity"], "formal entry revision identity")
            logical = sha(row["logical_entry_identity"], "formal logical entry identity")
            if revision <= previous or revision in seen_revisions:
                raise wp1.ProductionReviewError("formal catalog entries are not strictly ordered and unique")
            if logical in seen_logical:
                raise wp1.ProductionReviewError("formal catalog entries contain duplicate logical identities")
            previous = revision
            seen_revisions.add(revision)
            seen_logical.add(logical)
            if not all(isinstance(risk[key], bool) for key in ("has_args_order", "has_special", "component_group_last")):
                raise wp1.ProductionReviewError("formal catalog risk boolean mismatch")
            for key in ("source_utf8_bytes", "target_utf8_bytes", "component_group_size"):
                if not isinstance(risk[key], int) or isinstance(risk[key], bool) or risk[key] < 0:
                    raise wp1.ProductionReviewError("formal catalog risk integer mismatch")
            source_raw, target_raw = row["source"].encode("utf-8"), row["target"].encode("utf-8")
            if hashlib.sha256(source_raw).hexdigest() != sha(row["source_sha256"], "formal source hash") or \
                    hashlib.sha256(target_raw).hexdigest() != sha(row["target_sha256"], "formal target hash"):
                raise wp1.ProductionReviewError("formal catalog source/target hash mismatch")
            if risk["source_utf8_bytes"] != len(source_raw) or risk["target_utf8_bytes"] != len(target_raw):
                raise wp1.ProductionReviewError("formal catalog UTF-8 risk length mismatch")
            fixed = manifest["source_identities"].get(row["component"])
            if fixed != row["fixed_source_identity"] or row["terminology_snapshot_sha256"] != manifest["terminology_snapshot_sha256"]:
                raise wp1.ProductionReviewError("formal catalog source/terminology identity mismatch")
            core = {"component": row["component"], "duplicate_index": 0, "function_name": "t",
                    "normalized_source_tag": row["source_tag"], "section": row["section"],
                    "source": row["source"], "translation_path": row["normalized_path"]}
            if _plain_id(CALL_LOCATOR_KIND, "locator", core) != row["call_locator"]:
                raise wp1.ProductionReviewError("formal catalog call locator identity mismatch")
            expected_logical = wp1.surface.logical_entry_identity(
                component=row["component"], normalized_path=normalized, call_locator=row["call_locator"],
                source_tag=row["source_tag"])
            expected_revision = wp1.surface.entry_revision_identity(
                logical_entry_identity=expected_logical, source=row["source"], target=row["target"],
                fixed_source_identity=fixed, terminology_snapshot=manifest["terminology_snapshot_sha256"],
                rules_version=row["rules_version"])
            if expected_logical != logical or expected_revision != revision:
                raise wp1.ProductionReviewError("formal catalog logical/revision identity mismatch")
        exclusion_previous = ""
        for index, item in enumerate(exclusions):
            row = exact(item, wp1.EXCLUSION_KEYS, f"formal catalog exclusion {index}")
            schema_one(row["schema_version"], f"formal catalog exclusion {index}")
            if row["reason_code"] not in EXCLUSION_PRIORITY or not isinstance(row["component"], str):
                raise wp1.ProductionReviewError("formal catalog exclusion reason mismatch")
            identity = sha(row["occurrence_identity"], "formal exclusion occurrence identity")
            if identity <= exclusion_previous:
                raise wp1.ProductionReviewError("formal catalog exclusions are not strictly ordered and unique")
            exclusion_previous = identity
        counts = Counter(row["component"] for row in entries)
        counts.update(row["component"] for row in exclusions)
        if {key: counts[key] for key in manifest["component_counts"]} != manifest["component_counts"] or \
                any(key not in manifest["component_counts"] for key in counts):
            raise wp1.ProductionReviewError("formal catalog component counts mismatch")
        if hashlib.sha256(entries_raw).hexdigest() != manifest["entries_sha256"] or \
                hashlib.sha256(exclusions_raw).hexdigest() != manifest["exclusions_sha256"]:
            raise wp1.ProductionReviewError("formal catalog entries/exclusions hash mismatch")
        if len(entries) != manifest["entry_count"] or len(exclusions) != manifest["exclusion_count"] or \
                manifest["occurrence_count"] != len(entries) + len(exclusions):
            raise wp1.ProductionReviewError("formal catalog conservation mismatch")
        expected_policy_sha = hashlib.sha256(files[POLICY_PATH]).hexdigest()
        if manifest["policy_sha256"] != expected_policy_sha:
            raise wp1.ProductionReviewError("formal catalog policy identity mismatch")
        if manifest["rules_version"] != _validate_migration_policy(files[POLICY_PATH])["rules_version"]:
            raise wp1.ProductionReviewError("formal catalog prospective rules identity mismatch")
        return manifest, entries, exclusions
    except wp1.ProductionReviewError:
        raise
    except (wp1.surface.ContractError, AttributeError, KeyError, TypeError, UnicodeError, ValueError) as error:
        raise wp1.ProductionReviewError(f"invalid formal catalog value: {error}") from error


def _reject_symlink_ancestors(path: Path, *, label: str) -> Path:
    """Reject every existing symlink in a lexical path, including outside the repo."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            continue
        except OSError as error:
            raise wp1.ProductionReviewError(f"cannot inspect {label} ancestor {current}: {error}") from error
        if stat.S_ISLNK(mode):
            raise wp1.ProductionReviewError(f"{label} traverses a symlink ancestor: {current}")
    return absolute


def ordinary_tree(root: Path) -> dict[str, bytes]:
    root = _reject_symlink_ancestors(root, label="candidate catalog")
    try: mode=root.lstat().st_mode
    except OSError as error: raise wp1.ProductionReviewError(f"candidate catalog unavailable: {error}") from error
    if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode): raise wp1.ProductionReviewError("candidate catalog is not an ordinary directory")
    result={}
    try:
        for path in sorted(root.rglob("*")):
            mode=path.lstat().st_mode
            if stat.S_ISLNK(mode) or not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                raise wp1.ProductionReviewError(f"candidate contains symlink/special entry: {path}")
            if stat.S_ISREG(mode): result[path.relative_to(root).as_posix()]=path.read_bytes()
    except wp1.ProductionReviewError:
        raise
    except OSError as error:
        raise wp1.ProductionReviewError(f"cannot read candidate catalog tree: {error}") from error
    if set(result)!=set(CANDIDATE_FILES):
        raise wp1.ProductionReviewError(f"candidate exact tree mismatch (missing={sorted(CANDIDATE_FILES-set(result))}, extra={sorted(set(result)-CANDIDATE_FILES)})")
    return result


def check_catalog_tree(root: Path, manifest: Manifest, *, require_current_vector: bool=True) -> dict[str, Any]:
    files=ordinary_tree(root)
    if files[SCHEMA_PATH]!=SCHEMA_RAW or files[POLICY_PATH]!=POLICY_RAW:
        raise wp1.ProductionReviewError("candidate formal schema/policy bytes mismatch")
    manifest_path=f"{CATALOG_PREFIX}/manifest.json"; raw=files[manifest_path]
    value, _entries, _exclusions = validate_catalog_files(files)
    expected=build_catalog(manifest,recorded_at=value["recorded_at"],recorded_by=value["recorded_by"],
                           require_current_vector=require_current_vector)
    if files!=expected: raise wp1.ProductionReviewError("formal catalog does not exactly reconstruct from live input")
    if value["occurrence_count"]!=value["entry_count"]+value["exclusion_count"] or sum(value["component_counts"].values())!=value["occurrence_count"]:
        raise wp1.ProductionReviewError("formal catalog conservation mismatch")
    return value


def write_candidate(files: dict[str,bytes], output: Path, *, repository_root: Path) -> None:
    destination=_reject_symlink_ancestors(output, label="candidate output"); repo=repository_root.resolve()
    if destination==repo or destination.exists(): raise wp1.ProductionReviewError("candidate output must be a new directory")
    try: relative=destination.relative_to(repo)
    except ValueError: relative=None
    if relative is not None:
        if subprocess.run(["git","check-ignore","-q","--no-index",str(destination)],cwd=repo).returncode:
            raise wp1.ProductionReviewError("candidate output inside repository must be ignored")
    stage = None
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        _reject_symlink_ancestors(destination.parent, label="candidate output")
        stage = Path(tempfile.mkdtemp(prefix=".production-review-v2-lite-stage-",
                                      dir=destination.parent))
        for name,raw in sorted(files.items()):
            path=stage/name; path.parent.mkdir(parents=True,exist_ok=True)
            with path.open("xb") as handle: handle.write(raw); handle.flush(); os.fsync(handle.fileno())
        for directory in sorted((p for p in stage.rglob("*") if p.is_dir()),key=lambda p:len(p.parts),reverse=True): wp1._fsync_directory(directory)
        wp1._fsync_directory(stage)
        wp1._rename_directory_noreplace(stage, destination)
        stage = None
        wp1._fsync_directory(destination.parent)
    except (OSError, wp1.ProductionReviewError) as error:
        if stage is not None and stage.exists(): shutil.rmtree(stage)
        if isinstance(error, wp1.ProductionReviewError): raise
        raise wp1.ProductionReviewError(f"cannot write candidate: {error}") from error


def _git(root:Path,*args:str)->bytes:
    try: return subprocess.run(["git",*args],cwd=root,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
    except subprocess.CalledProcessError as error: raise wp1.ProductionReviewError(f"git preflight failed: {error.stderr.decode('utf-8','replace').strip()}") from error


def is_production_path(path:str)->bool:
    return path.startswith("evidence/production-review") or path.startswith("i18n/quality/production-review")


def prospective_occupancy(tracked_sizes:dict[str,int],candidate:dict[str,bytes])->int:
    surviving = set(tracked_sizes) - set(WP1_FILES)
    collisions = sorted((tracked, proposed) for tracked in surviving for proposed in candidate
                        if tracked == proposed or tracked.startswith(proposed + "/")
                        or proposed.startswith(tracked + "/"))
    if collisions: raise wp1.ProductionReviewError(f"candidate collides with tracked paths: {collisions}")
    total=sum(size for path,size in tracked_sizes.items() if is_production_path(path) and path not in WP1_FILES)+sum(map(len,candidate.values()))
    if total>TRACKED_LIMIT: raise wp1.ProductionReviewError(f"prospective tracked total exceeds 128 MiB (bytes={total}, limit={TRACKED_LIMIT})")
    return total


def _tree_entries(root: Path, revision: str) -> dict[str, tuple[str, str, str, int | None]]:
    raw = _git(root, "ls-tree", "-rz", "-l", "--full-tree", revision)
    result: dict[str, tuple[str, str, str, int | None]] = {}
    try:
        records = raw.split(b"\0")
        if records[-1] != b"":
            raise ValueError("missing NUL terminator")
        for record in records[:-1]:
            metadata, path_raw = record.split(b"\t", 1)
            mode_raw, kind_raw, object_raw, size_raw = metadata.split()
            path = path_raw.decode("utf-8")
            if is_production_path(path):
                if path in result:
                    raise ValueError("duplicate path")
                result[path] = (mode_raw.decode("ascii"), kind_raw.decode("ascii"),
                                object_raw.decode("ascii"),
                                None if size_raw == b"-" else int(size_raw))
    except (UnicodeDecodeError, UnicodeEncodeError, ValueError) as error:
        raise wp1.ProductionReviewError(f"cannot parse production tree {revision}: {error}") from error
    return result


def _blob_sha256(root: Path, object_id: str) -> str:
    raw = _git(root, "cat-file", "blob", object_id)
    return hashlib.sha256(raw).hexdigest()


def _verify_production_state_matches_head(root: Path) -> None:
    raw = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    fields = raw.split(b"\0")
    index = 0
    changed: list[str] = []
    try:
        while index < len(fields) and fields[index]:
            record = fields[index]
            if len(record) < 4 or record[2:3] != b" ":
                raise ValueError("malformed porcelain record")
            status = record[:2]
            paths = [record[3:].decode("utf-8")]
            index += 1
            if b"R" in status or b"C" in status:
                if index >= len(fields) or not fields[index]:
                    raise ValueError("missing rename/copy source")
                paths.append(fields[index].decode("utf-8"))
                index += 1
            if any(is_production_path(path) for path in paths):
                changed.extend(paths)
        if index != len(fields) - 1:
            raise ValueError("malformed NUL termination")
    except (UnicodeDecodeError, ValueError) as error:
        raise wp1.ProductionReviewError(f"cannot parse production index/worktree state: {error}") from error
    if changed:
        raise wp1.ProductionReviewError(
            f"production-review index/worktree must exactly match HEAD (staged, unmerged, dirty, or untracked paths={changed})")


def verify_wp1_preimage(root:Path)->None:
    head=_git(root,"rev-parse","HEAD").decode().strip()
    _git(root, "merge-base", "--is-ancestor", BASELINE_HEAD, head)
    baseline = _tree_entries(root, BASELINE_HEAD)
    if set(baseline) != set(WP1_FILES):
        raise wp1.ProductionReviewError(
            f"WP1 exact baseline tree mismatch (missing={sorted(set(WP1_FILES)-set(baseline))}, "
            f"extra={sorted(set(baseline)-set(WP1_FILES))})")
    current = _tree_entries(root, head)
    current_wp1 = {path for path in current if path.startswith(WP1_FAMILY_PREFIXES)}
    if current_wp1 != set(WP1_FILES):
        raise wp1.ProductionReviewError(
            f"WP1 current HEAD tree mismatch (missing={sorted(set(WP1_FILES)-current_wp1)}, "
            f"extra={sorted(current_wp1-set(WP1_FILES))})")
    for path,expected in WP1_FILES.items():
        for label, tree in (("baseline", baseline), ("current HEAD", current)):
            entry = tree.get(path)
            if entry is None:
                raise wp1.ProductionReviewError(f"WP1 preimage missing from {label}: {path}")
            mode, kind, object_id, _size = entry
            if mode != "100644" or kind != "blob":
                raise wp1.ProductionReviewError(f"WP1 preimage is not an ordinary 100644 blob in {label}: {path}")
            if _blob_sha256(root, object_id) != expected:
                raise wp1.ProductionReviewError(f"WP1 preimage SHA-256 mismatch in {label}: {path}")
        file=root/path
        _reject_symlink_ancestors(file, label="WP1 preimage")
        try: mode=file.lstat().st_mode; raw=file.read_bytes()
        except OSError as error: raise wp1.ProductionReviewError(f"cannot read WP1 preimage {path}: {error}") from error
        if not stat.S_ISREG(mode) or stat.S_ISLNK(mode): raise wp1.ProductionReviewError(f"WP1 preimage is symlink/special: {path}")
        if hashlib.sha256(raw).hexdigest()!=expected: raise wp1.ProductionReviewError(f"WP1 preimage SHA-256 mismatch: {path}")


def retirement_preflight(root:Path,candidate_root:Path,manifest:Manifest)->dict[str,Any]:
    verify_wp1_preimage(root)
    head = _git(root, "rev-parse", "HEAD").decode().strip()
    source_tree = _tree_entries(root, head)
    for path, (mode, kind, _object, size) in source_tree.items():
        if mode != "100644" or kind != "blob" or size is None:
            raise wp1.ProductionReviewError(f"tracked production entry is not an ordinary 100644 blob: {path}")
    _verify_production_state_matches_head(root)
    value=check_catalog_tree(candidate_root,manifest); candidate=ordinary_tree(candidate_root)
    tracked={path: size for path, (_mode, _kind, _object, size) in source_tree.items()
             if size is not None}
    total=prospective_occupancy(tracked,candidate)
    return {"catalog_id":value["catalog_id"],"wp1_files":len(WP1_FILES),"prospective_tracked_bytes":total,"limit":TRACKED_LIMIT,"ok":True}


def utc_now()->str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
