"""Deterministic, self-contained production-review shadow calibration."""
from __future__ import annotations

import ctypes
import errno
import fcntl
import hashlib
import json
import os
import re
import shutil
import stat
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

TOOLS_DIR = str(Path(__file__).resolve().parents[1])
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
if "tools" in sys.modules:
    from tools import surface_screen_result_check as surface
    from tools import translation_review_ledger as ledger
else:
    import surface_screen_result_check as surface
    import translation_review_ledger as ledger

from .config import Manifest
from .locale_model import LocaleLoader
from .runtime import LuaRuntime


class ProductionReviewError(Exception):
    pass


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SOURCE_ID_RE = re.compile(r"^(?:commit:[0-9a-f]{40}|snapshot:[0-9a-f]{64})$")
MARKERS = {"authoritative": False, "dispatchable": False, "promotable": False}
FROZEN_RULES_VERSION = "production-shadow-rules-v1"
RULES_VERSION = FROZEN_RULES_VERSION
PRIORITY_VERSION = "production-shadow-priority-v1"
FEATURE_SCHEMA = "production-shadow-features-v1"
ELIGIBLE_PREDICATE = "catalog_entry_and_checkpoint_state_queued"
PRIORITY_TUPLE = ["format_risk_desc","component_group_size_desc","component_group_last_desc",
                  "component_ordinal_asc","entry_revision_identity_bytes_asc"]
DOMAINS = {name: f"tome4-production-{name}-v1\0".encode() for name in (
    "occurrence", "call-locator", "locator-snapshot", "catalog", "terminology-snapshot",
    "shadow-queue-policy", "journal-group", "journal-event", "journal-checkpoint",
    "shadow-batch", "ordered-set")}
OCCURRENCE_KEYS = frozenset({"schema_version", "component", "translation_path", "document_ordinal",
    "function_name", "section", "source", "target", "source_tag", "args_order", "special"})
ALLOCATION_KEYS = frozenset({"component", "translation_path", "function_name", "section", "source",
    "normalized_source_tag", "duplicate_index"})
LOCATOR_ROW_KEYS = frozenset({"schema_version", "occurrence_identity", "component", "translation_path",
    "function_name", "section", "source", "normalized_source_tag", "duplicate_index", "call_locator"})
RISK_KEYS = frozenset({"has_args_order", "has_special", "source_utf8_bytes", "target_utf8_bytes",
    "component_group_size", "component_group_last"})
CATALOG_ENTRY_KEYS = frozenset({"schema_version", "occurrence_identity", "logical_entry_identity",
    "entry_revision_identity", "component", "normalized_path", "call_locator", "source_sha256",
    "source_tag_sha256", "target_sha256", "fixed_source_identity", "terminology_snapshot_id",
    "rules_version", "risk"})
EXCLUSION_KEYS = frozenset({"schema_version", "occurrence_identity", "component", "reason_code"})
COMPONENT_ORDINAL_KEYS = frozenset({"component", "ordinal"})
LEDGER_RECORD_KEYS = frozenset(ledger.RECORD_KEYS)
JOURNAL_EVENT_KEYS = frozenset({"schema_version", "event_id", "group_id", "ordinal", "catalog_id",
    "shadow_policy_id", "attempt", "batch_id", "task_id", "handoff_id", "record", "previous_event_hash"})
IN_SCOPE_COMPONENTS = frozenset({"engine", "boot", "tome", "ashes-urhrok", "cults", "orcs"})
BUDGETS = {"locator": 32*1024*1024, "catalog": 32*1024*1024, "policy": 1024*1024,
           "journal": 48*1024*1024, "batch": 8*1024*1024, "total": 128*1024*1024}


def canonical_bytes(value: object) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                          allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise ProductionReviewError(f"value is not canonicalizable: {error}") from error


def production_hash(domain: str, core: bytes) -> str:
    if domain not in DOMAINS:
        raise ProductionReviewError(f"unknown production hash domain: {domain}")
    return hashlib.sha256(DOMAINS[domain] + len(core).to_bytes(8, "big") + core).hexdigest()


def object_id(domain: str, value: dict[str, Any], id_key: str) -> str:
    core = dict(value); core.pop(id_key, None)
    return production_hash(domain, canonical_bytes(core))


def ordered_set_hash(values: Iterable[str]) -> str:
    body = b"".join(len(v.encode("ascii")).to_bytes(8, "big") + v.encode("ascii") for v in values)
    return production_hash("ordered-set", body)


def validate_exact(value: object, keys: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or frozenset(value) != keys:
        actual = set(value) if isinstance(value, dict) else set()
        raise ProductionReviewError(f"{label} exact schema mismatch (missing={sorted(keys-actual)}, extra={sorted(actual-keys)})")
    return value


def _version_one(value: dict[str, Any], label: str) -> None:
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise ProductionReviewError(f"{label}.schema_version must be integer 1")


def _integer(value: object, label: str, *, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ProductionReviewError(f"{label} must be an integer >= {minimum}")
    return value


def _boolean(value: object, label: str) -> bool:
    if type(value) is not bool:
        raise ProductionReviewError(f"{label} must be a boolean")
    return value


def _markers(value: object, label: str = "markers") -> dict[str, bool]:
    row = validate_exact(value, frozenset(MARKERS), label)
    for key in MARKERS:
        _boolean(row[key], f"{label}.{key}")
    return row  # type: ignore[return-value]


def parse_canonical_object(raw: bytes, label: str) -> dict[str, Any]:
    """Parse one compact canonical JSON object. Top-level artifacts have no LF."""
    value = _parse_json(raw, label)
    if not isinstance(value, dict) or canonical_bytes(value) != raw:
        raise ProductionReviewError(f"{label} must be one canonical JSON object without trailing LF")
    return value


def _raw_object_sha(raw: bytes, value: dict[str, Any], label: str) -> str:
    if parse_canonical_object(raw, label) != value:
        raise ProductionReviewError(f"{label} bytes do not encode the supplied object")
    return hashlib.sha256(raw).hexdigest()


def strict_utc_seconds(value: object) -> str:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        raise ProductionReviewError("recorded_at must be strict UTC seconds (YYYY-MM-DDTHH:MM:SSZ)")
    try: datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error: raise ProductionReviewError("recorded_at is invalid") from error
    return value


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value: raise ProductionReviewError(f"{label} must be non-empty")
    return value


def _sha(value: object, label: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value): raise ProductionReviewError(f"{label} must be SHA-256")
    return value


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError(f"duplicate key {key!r}")
        result[key] = value
    return result


def _parse_json(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)),
                          object_pairs_hook=_unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ProductionReviewError(f"invalid {label} JSON: {error}") from error


def _jsonl(rows: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(row) + b"\n" for row in rows)


class VerifiedRows(list):
    """Canonical JSONL rows that carry the digest of their own exact line.

    The digests come from :func:`parse_jsonl`, taken at the moment it proves
    ``canonical_bytes(value) == line``.  They are therefore digests of each
    row's canonical bytes: exactly what re-serialising the row would produce,
    without re-serialising it.

    They live *on* the list rather than beside it.  Any plain list derived from
    these rows -- by sorting, filtering or slicing -- simply has no digests and
    falls back to recomputing, which is correct.  Pairing one catalog's digests
    with another catalog's rows would require deliberately constructing this
    type by hand.

    **There is no cheap runtime check that would catch such a mispairing.**
    Comparing key sets does not: a terminology-provenance change keeps the same
    revision identities while changing the row bytes, which is precisely the
    dangerous case.  Recomputing a sample is a symptom check, and recomputing
    all of them costs what this saves.  The safety here is structural, not
    verified at runtime -- do not add an assertion that pretends otherwise.
    """

    def __init__(self, rows: list[dict[str, Any]], digests: list[str]):
        super().__init__(rows)
        if len(digests) != len(rows):
            raise ProductionReviewError("verified rows and line digests are not aligned")
        self.digest_by_revision = {row["entry_revision_identity"]: digest
                                   for row, digest in zip(rows, digests)}
        if len(self.digest_by_revision) != len(rows):
            raise ProductionReviewError("verified rows do not have unique revision identities")


def parse_jsonl(raw: bytes, label: str, *, digests: list[str] | None = None) -> list[dict[str, Any]]:
    """Parse canonical JSONL, optionally collecting each line's SHA-256.

    ``digests`` receives one hex digest per row in file order.  The canonical
    check on the line immediately above makes that the digest of the row's
    canonical bytes, so a later consumer can use it instead of serialising the
    row again.
    """
    if raw and not raw.endswith(b"\n"): raise ProductionReviewError(f"{label} JSONL must end in LF")
    result = []
    for number, line in enumerate(raw.splitlines(), 1):
        value = _parse_json(line, f"{label} line {number}")
        if not isinstance(value, dict) or canonical_bytes(value) != line:
            raise ProductionReviewError(f"{label} line {number} is not canonical")
        result.append(value)
        if digests is not None:
            digests.append(hashlib.sha256(line).hexdigest())
    return result


def make_occurrence(component: str, translation_path: str, document_ordinal: int, record: dict[str, Any]) -> dict[str, Any]:
    value = {"schema_version": 1, "component": component, "translation_path": translation_path,
        "document_ordinal": document_ordinal, "function_name": record.get("function_name", "t"),
        "section": record.get("section", ""), "source": record.get("source"), "target": record.get("target"),
        "source_tag": record.get("source_tag"), "args_order": record.get("args_order"), "special": record.get("special")}
    return validate_occurrence(value)


def validate_occurrence(value: object) -> dict[str, Any]:
    row = validate_exact(value, OCCURRENCE_KEYS, "occurrence"); _version_one(row, "occurrence")
    if row["function_name"] != "t": raise ProductionReviewError("occurrence.function_name must be 't'")
    _integer(row["document_ordinal"], "occurrence.document_ordinal")
    for key in ("component", "translation_path", "function_name", "section", "source", "target"):
        if not isinstance(row[key], str): raise ProductionReviewError(f"occurrence.{key} must be a string")
    if row["source_tag"] is not None and not isinstance(row["source_tag"], str): raise ProductionReviewError("occurrence.source_tag must be string or null")
    args = row["args_order"]
    if args is not None and (not isinstance(args, list) or any(type(item) is not int or item < 1 for item in args)):
        raise ProductionReviewError("occurrence.args_order must be an integer array or null")
    if row["special"] is not None and not isinstance(row["special"], str):
        raise ProductionReviewError("occurrence.special must be string or null")
    return row


def _duplicate_index_zero(value: object, label: str) -> int:
    if type(value) is not int or value != 0:
        raise ProductionReviewError(f"{label} must be literal integer zero")
    return value


def make_allocation(occurrence: dict[str, Any], duplicate_index: int = 0) -> dict[str, Any]:
    validate_occurrence(occurrence)
    _duplicate_index_zero(duplicate_index, "WP1 duplicate_index")
    return {"component": occurrence["component"], "translation_path": occurrence["translation_path"],
        "function_name": occurrence["function_name"], "section": occurrence["section"], "source": occurrence["source"],
        "normalized_source_tag": occurrence["source_tag"] or "", "duplicate_index": 0}


def make_locator_row(occurrence: dict[str, Any], allocation: dict[str, Any]) -> dict[str, Any]:
    validate_occurrence(occurrence); validate_exact(allocation, ALLOCATION_KEYS, "allocation")
    _duplicate_index_zero(allocation["duplicate_index"], "allocation.duplicate_index")
    expected = make_allocation(occurrence, allocation["duplicate_index"])
    if allocation != expected: raise ProductionReviewError("allocation does not match occurrence")
    return {"schema_version": 1, "occurrence_identity": production_hash("occurrence", canonical_bytes(occurrence)),
        "component": occurrence["component"], "translation_path": occurrence["translation_path"],
        "function_name": occurrence["function_name"], "section": occurrence["section"], "source": occurrence["source"],
        "normalized_source_tag": occurrence["source_tag"] or "", "duplicate_index": allocation["duplicate_index"],
        "call_locator": production_hash("call-locator", canonical_bytes(allocation))}


def load_occurrences(manifest: Manifest) -> list[dict[str, Any]]:
    runtime = LuaRuntime(manifest); runtime.doctor(); loader = LocaleLoader(runtime); result = []
    for component in manifest.components:
        document = loader.load_path(manifest.root/component.translation, logical_path=component.translation)
        result.extend(make_occurrence(component.id, component.translation, i, row) for i, row in enumerate(document.translations))
    return result


def _validate_locator_row(value: object) -> dict[str, Any]:
    row = validate_exact(value, LOCATOR_ROW_KEYS, "locator row"); _version_one(row, "locator row")
    for key in ("occurrence_identity", "call_locator"):
        _sha(row[key], f"locator row.{key}")
    for key in ("component", "translation_path", "function_name", "section", "source", "normalized_source_tag"):
        if not isinstance(row[key], str): raise ProductionReviewError(f"locator row.{key} must be a string")
    _duplicate_index_zero(row["duplicate_index"], "locator row.duplicate_index")
    return row


def _validate_component_ordinals(value: object, label: str, *, contiguous: bool = False) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ProductionReviewError(f"{label} must be an ordered list")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    previous = -1
    for index, item in enumerate(value):
        row = validate_exact(item, COMPONENT_ORDINAL_KEYS, label)
        if not isinstance(row["component"], str): raise ProductionReviewError(f"{label}.component must be a string")
        component = _nonempty(row["component"], f"{label}.component")
        ordinal = row["ordinal"]
        if (type(ordinal) is not int or ordinal < 0 or ordinal <= previous or
                (contiguous and ordinal != index) or component in seen):
            raise ProductionReviewError(f"{label} order/ordinal binding invalid")
        seen.add(component); previous=ordinal; result.append({"component": component, "ordinal": ordinal})
    return result


def _component_ordinals(components: Iterable[str]) -> list[dict[str, Any]]:
    return _validate_component_ordinals(
        [{"component": component, "ordinal": ordinal} for ordinal, component in enumerate(components)],
        "manifest_component_ordinals",
    )


def build_locator_snapshot_from_occurrences(occurrences: list[dict[str, Any]], *, manifest_sha256: str,
        manifest_component_ordinals: list[dict[str, Any]], loader_contract_path: str,
        loader_contract_sha256: str, lua_runtime: str, lua_build: str,
        recorded_at: str, recorded_by: str) -> tuple[dict[str, Any], bytes, bytes]:
    strict_utc_seconds(recorded_at); _nonempty(recorded_by, "recorded_by"); _sha(manifest_sha256, "manifest_sha256")
    _sha(loader_contract_sha256, "loader_contract_sha256"); _nonempty(loader_contract_path, "loader_contract_path")
    _nonempty(lua_runtime, "lua_runtime"); _nonempty(lua_build, "lua_build")
    component_ordinals = _validate_component_ordinals(
        manifest_component_ordinals, "manifest_component_ordinals", contiguous=True)
    checked = [validate_occurrence(row) for row in occurrences]
    manifest_components = {row["component"] for row in component_ordinals}
    if any(row["component"] not in manifest_components for row in checked):
        raise ProductionReviewError("occurrence component is absent from manifest component ordinals")
    locators = [make_locator_row(row, make_allocation(row)) for row in checked]
    if len({r["call_locator"] for r in locators}) != len(locators): raise ProductionReviewError("locator collision")
    occurrence_raw, locator_raw = _jsonl(checked), _jsonl(locators)
    counts = dict(sorted(Counter(row["component"] for row in checked).items()))
    value = {"schema_version": 1, "locator_snapshot_id": "", "kind": "production_locator_snapshot_shadow_v1",
        "markers": MARKERS, "manifest_sha256": manifest_sha256,
        "manifest_component_ordinals": component_ordinals, "component_counts": counts,
        "occurrences_count": len(checked), "occurrences_sha256": hashlib.sha256(occurrence_raw).hexdigest(),
        "locators_count": len(locators), "locators_sha256": hashlib.sha256(locator_raw).hexdigest(),
        "loader_contract_path": loader_contract_path, "loader_contract_sha256": loader_contract_sha256,
        "lua_runtime": lua_runtime, "lua_build": lua_build, "recorded_at": recorded_at, "recorded_by": recorded_by}
    value["locator_snapshot_id"] = object_id("locator-snapshot", value, "locator_snapshot_id")
    return value, occurrence_raw, locator_raw


def build_locator_snapshot(manifest: Manifest, *, recorded_at: str, recorded_by: str) -> tuple[dict[str, Any], bytes, bytes]:
    runtime = LuaRuntime(manifest).doctor(); contract = manifest.root/"tools/i18nlib/locale_model.py"
    try: contract_raw = contract.read_bytes()
    except OSError as error: raise ProductionReviewError(f"cannot read loader contract: {error}") from error
    return build_locator_snapshot_from_occurrences(load_occurrences(manifest),
        manifest_sha256=hashlib.sha256(manifest.raw_bytes).hexdigest(),
        manifest_component_ordinals=_component_ordinals(component.id for component in manifest.components),
        loader_contract_path="tools/i18nlib/locale_model.py",
        loader_contract_sha256=hashlib.sha256(contract_raw).hexdigest(), lua_runtime=runtime["lua_version"],
        lua_build=runtime["luajit_version"], recorded_at=recorded_at, recorded_by=recorded_by)


def check_locator_snapshot(value: dict[str, Any], occurrences_raw: bytes, locators_raw: bytes) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    keys = frozenset({"schema_version", "locator_snapshot_id", "kind", "markers", "manifest_sha256",
        "manifest_component_ordinals", "component_counts", "occurrences_count", "occurrences_sha256",
        "locators_count", "locators_sha256", "loader_contract_path",
        "loader_contract_sha256", "lua_runtime", "lua_build", "recorded_at", "recorded_by"})
    validate_exact(value, keys, "locator manifest"); _version_one(value, "locator manifest")
    strict_utc_seconds(value["recorded_at"]); _nonempty(value["recorded_by"], "recorded_by")
    _sha(value["locator_snapshot_id"], "locator_snapshot_id"); _sha(value["manifest_sha256"], "manifest_sha256")
    _sha(value["occurrences_sha256"], "occurrences_sha256"); _sha(value["locators_sha256"], "locators_sha256")
    _sha(value["loader_contract_sha256"], "loader_contract_sha256")
    for key in ("kind", "loader_contract_path", "lua_runtime", "lua_build"):
        _nonempty(value[key], f"locator manifest.{key}")
    _markers(value["markers"])
    _integer(value["occurrences_count"], "occurrences_count"); _integer(value["locators_count"], "locators_count")
    if not isinstance(value["component_counts"], dict) or any(not isinstance(k, str) or type(v) is not int or v < 0 for k, v in value["component_counts"].items()):
        raise ProductionReviewError("component_counts must be string -> non-negative integer")
    component_ordinals = _validate_component_ordinals(
        value["manifest_component_ordinals"], "manifest_component_ordinals", contiguous=True)
    if value["markers"] != MARKERS or value["kind"] != "production_locator_snapshot_shadow_v1": raise ProductionReviewError("locator markers/kind invalid")
    if value["locator_snapshot_id"] != object_id("locator-snapshot", value, "locator_snapshot_id"): raise ProductionReviewError("locator snapshot ID mismatch")
    if hashlib.sha256(occurrences_raw).hexdigest() != value["occurrences_sha256"] or hashlib.sha256(locators_raw).hexdigest() != value["locators_sha256"]: raise ProductionReviewError("locator file hash mismatch")
    occurrences = [validate_occurrence(row) for row in parse_jsonl(occurrences_raw, "occurrences")]
    locators = [_validate_locator_row(row) for row in parse_jsonl(locators_raw, "locators")]
    if len(occurrences) != value["occurrences_count"] or len(locators) != value["locators_count"] or len(occurrences) != len(locators): raise ProductionReviewError("locator file count mismatch")
    if dict(sorted(Counter(o["component"] for o in occurrences).items())) != value["component_counts"]: raise ProductionReviewError("component counts mismatch")
    manifest_components = {row["component"] for row in component_ordinals}
    if any(o["component"] not in manifest_components for o in occurrences):
        raise ProductionReviewError("occurrence component is absent from manifest component ordinals")
    seen: set[str] = set()
    for occurrence, locator in zip(occurrences, locators):
        if locator != make_locator_row(occurrence, make_allocation(occurrence)) or locator["call_locator"] in seen: raise ProductionReviewError("locator identity/allocation mismatch")
        seen.add(locator["call_locator"])
    return occurrences, locators


def check_locator_snapshot_live(value: dict[str, Any], occurrences_raw: bytes,
                                locators_raw: bytes, manifest: Manifest) -> None:
    """Bind a frozen locator snapshot to this checkout's complete live inputs."""
    check_locator_snapshot(value, occurrences_raw, locators_raw)
    runtime = LuaRuntime(manifest).doctor()
    contract_path = manifest.root / "tools/i18nlib/locale_model.py"
    try:
        contract_raw = contract_path.read_bytes()
    except OSError as error:
        raise ProductionReviewError(f"cannot read loader contract: {error}") from error
    expected = {
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "manifest_component_ordinals": _component_ordinals(c.id for c in manifest.components),
        "loader_contract_path": "tools/i18nlib/locale_model.py",
        "loader_contract_sha256": hashlib.sha256(contract_raw).hexdigest(),
        "lua_runtime": runtime["lua_version"],
        "lua_build": runtime["luajit_version"],
    }
    for key, expected_value in expected.items():
        if value[key] != expected_value:
            raise ProductionReviewError(f"operational locator live binding drift: {key}")
    if _jsonl(load_occurrences(manifest)) != occurrences_raw:
        raise ProductionReviewError("operational locator live occurrence harvest drift")


def terminology_snapshot(root: Path) -> str:
    try:
        files = [root/"TERMINOLOGY.md"] + sorted((root/"terminology").rglob("*")); framed = bytearray()
        for path in files:
            if not path.is_file() or path.is_symlink(): continue
            rel, body = path.relative_to(root).as_posix().encode(), path.read_bytes()
            framed += len(rel).to_bytes(8,"big")+rel+len(body).to_bytes(8,"big")+body
        return production_hash("terminology-snapshot", bytes(framed))
    except OSError as error:
        raise ProductionReviewError(f"cannot read terminology snapshot inputs: {error}") from error


def source_identities_from_manifest(manifest: Manifest) -> dict[str, str]:
    result = {}
    for component in manifest.components:
        if component.source_baseline: result[component.id] = "snapshot:" + component.source_baseline.snapshot_sha256
        elif component.source_repository: result[component.id] = "commit:" + manifest.repositories[component.source_repository].commit
    return result


def _validate_source_identities(value: object) -> dict[str, str]:
    if not isinstance(value, dict) or any(not isinstance(k,str) or not isinstance(v,str) or not SOURCE_ID_RE.fullmatch(v) for k,v in value.items()):
        raise ProductionReviewError("source identities must be component -> typed source identity")
    return dict(sorted(value.items()))


def _eligible_component_ordinals(locator_manifest: dict[str, Any], sources: dict[str, str]) -> list[dict[str, Any]]:
    manifest_ordinals = _validate_component_ordinals(
        locator_manifest.get("manifest_component_ordinals"), "manifest_component_ordinals", contiguous=True)
    result = [row for row in manifest_ordinals if row["component"] in IN_SCOPE_COMPONENTS]
    if {row["component"] for row in result} != IN_SCOPE_COMPONENTS:
        raise ProductionReviewError("manifest component ordinals do not bind the exact eligible component set")
    if any(row["component"] not in sources for row in result):
        raise ProductionReviewError("eligible component ordinal lacks fixed source identity")
    return result


def build_catalog(locator_manifest: dict[str, Any], occurrences_raw: bytes, locators_raw: bytes, *, locator_manifest_raw: bytes,
        terminology_snapshot_id: str, source_identities: dict[str, str], recorded_at: str, recorded_by: str,
        rules_version: str | None = None) -> tuple[dict[str, Any], bytes, bytes]:
    occurrences, locators = check_locator_snapshot(locator_manifest, occurrences_raw, locators_raw)
    active_rules = RULES_VERSION if rules_version is None else _nonempty(rules_version, "rules_version")
    locator_manifest_sha256 = _raw_object_sha(locator_manifest_raw, locator_manifest, "locator manifest")
    _sha(terminology_snapshot_id, "terminology_snapshot_id"); sources = _validate_source_identities(source_identities)
    eligible_component_ordinals = _eligible_component_ordinals(locator_manifest, sources)
    strict_utc_seconds(recorded_at); _nonempty(recorded_by, "recorded_by")
    if (recorded_at, recorded_by) != (locator_manifest["recorded_at"], locator_manifest["recorded_by"]):
        raise ProductionReviewError("catalog metadata must match locator baseline")
    grouped = Counter((o["component"],o["source"],o["source_tag"] or "") for o in occurrences); seen = Counter()
    entries=[]; exclusions=[]
    for o,l in zip(occurrences,locators):
        reason = "outside_initial_six_component_scope" if o["component"] not in IN_SCOPE_COMPONENTS else ("empty_source" if not o["source"] else ("empty_target" if not o["target"] else None))
        if reason:
            exclusions.append({"schema_version":1,"occurrence_identity":l["occurrence_identity"],"component":o["component"],"reason_code":reason}); continue
        fixed = sources.get(o["component"])
        if not fixed: raise ProductionReviewError(f"missing fixed source identity for {o['component']}")
        tag=o["source_tag"] or ""; group=(o["component"],o["source"],tag); seen[group]+=1
        try:
            normalized_path = surface.normalize_relative_path(o["translation_path"])
        except surface.ContractError as error:
            raise ProductionReviewError(f"invalid catalog normalized_path: {error}") from error
        if normalized_path != o["translation_path"]:
            raise ProductionReviewError("translation_path must already equal normalized_path")
        logical=surface.logical_entry_identity(component=o["component"], normalized_path=normalized_path, call_locator=l["call_locator"], source_tag=tag)
        revision=surface.entry_revision_identity(logical_entry_identity=logical, source=o["source"], target=o["target"], fixed_source_identity=fixed,
            terminology_snapshot=terminology_snapshot_id, rules_version=active_rules)
        entries.append({"schema_version":1,"occurrence_identity":l["occurrence_identity"],"logical_entry_identity":logical,
            "entry_revision_identity":revision,"component":o["component"],"normalized_path":normalized_path,"call_locator":l["call_locator"],
            "source_sha256":hashlib.sha256(o["source"].encode()).hexdigest(),"source_tag_sha256":hashlib.sha256(tag.encode()).hexdigest(),
            "target_sha256":hashlib.sha256(o["target"].encode()).hexdigest(),"fixed_source_identity":fixed,
            "terminology_snapshot_id":terminology_snapshot_id,"rules_version":active_rules,
            "risk":{"has_args_order":o["args_order"] is not None,"has_special":o["special"] is not None,
                "source_utf8_bytes":len(o["source"].encode()),"target_utf8_bytes":len(o["target"].encode()),
                "component_group_size":grouped[group],"component_group_last":seen[group]==grouped[group]}})
    entries.sort(key=lambda e:e["logical_entry_identity"]); exclusions.sort(key=lambda e:e["occurrence_identity"])
    eb,xb=_jsonl(entries),_jsonl(exclusions)
    value={"schema_version":1,"catalog_id":"","kind":"production_catalog_shadow_v1","markers":MARKERS,
        "locator_snapshot_id":locator_manifest["locator_snapshot_id"],"locator_manifest_sha256":locator_manifest_sha256,
        "terminology_snapshot_id":terminology_snapshot_id,"source_identities":sources,
        "eligible_component_ordinals":eligible_component_ordinals,"rules_version":active_rules,
        "recorded_at":recorded_at,"recorded_by":recorded_by,"entry_count":len(entries),"exclusion_count":len(exclusions),
        "entries_sha256":hashlib.sha256(eb).hexdigest(),"exclusions_sha256":hashlib.sha256(xb).hexdigest()}
    value["catalog_id"]=object_id("catalog",value,"catalog_id")
    return value,eb,xb


def _validate_catalog_entry(entry: object) -> dict[str, Any]:
    row = validate_exact(entry, CATALOG_ENTRY_KEYS, "catalog entry"); _version_one(row, "catalog entry")
    for key in ("occurrence_identity", "logical_entry_identity", "entry_revision_identity", "call_locator", "source_sha256", "source_tag_sha256", "target_sha256", "terminology_snapshot_id"):
        _sha(row[key], f"catalog entry.{key}")
    for key in ("component", "normalized_path", "fixed_source_identity", "rules_version"):
        _nonempty(row[key], f"catalog entry.{key}")
    risk = validate_exact(row["risk"], RISK_KEYS, "catalog risk")
    _boolean(risk["has_args_order"], "catalog risk.has_args_order"); _boolean(risk["has_special"], "catalog risk.has_special")
    for key in ("source_utf8_bytes", "target_utf8_bytes", "component_group_size"):
        _integer(risk[key], f"catalog risk.{key}")
    _boolean(risk["component_group_last"], "catalog risk.component_group_last")
    return row


def _validate_exclusion(exclusion: object) -> dict[str, Any]:
    row = validate_exact(exclusion, EXCLUSION_KEYS, "catalog exclusion"); _version_one(row, "catalog exclusion")
    _sha(row["occurrence_identity"], "catalog exclusion.occurrence_identity")
    _nonempty(row["component"], "catalog exclusion.component"); _nonempty(row["reason_code"], "catalog exclusion.reason_code")
    return row


def check_catalog(value: dict[str, Any], entries_raw: bytes, exclusions_raw: bytes, *, locator_manifest: dict[str,Any],
        locator_manifest_raw: bytes, occurrences_raw: bytes, locators_raw: bytes,
        expected_terminology_snapshot_id: str | None = None,
        expected_source_identities: dict[str, str] | None = None,
        require_current_rules: bool = False) -> tuple[list[dict[str,Any]],list[dict[str,Any]]]:
    keys=frozenset({"schema_version","catalog_id","kind","markers","locator_snapshot_id","locator_manifest_sha256","terminology_snapshot_id","source_identities","eligible_component_ordinals","rules_version","recorded_at","recorded_by","entry_count","exclusion_count","entries_sha256","exclusions_sha256"})
    validate_exact(value,keys,"catalog manifest"); _version_one(value, "catalog manifest")
    strict_utc_seconds(value["recorded_at"]); _nonempty(value["recorded_by"],"recorded_by")
    for key in ("catalog_id", "locator_snapshot_id", "locator_manifest_sha256", "terminology_snapshot_id", "entries_sha256", "exclusions_sha256"):
        _sha(value[key], f"catalog manifest.{key}")
    _markers(value["markers"]); _nonempty(value["kind"], "catalog manifest.kind"); _nonempty(value["rules_version"], "catalog manifest.rules_version")
    _integer(value["entry_count"], "entry_count"); _integer(value["exclusion_count"], "exclusion_count")
    sources=_validate_source_identities(value["source_identities"])
    _validate_component_ordinals(value["eligible_component_ordinals"], "eligible_component_ordinals")
    if (value["recorded_at"], value["recorded_by"]) != (locator_manifest.get("recorded_at"), locator_manifest.get("recorded_by")):
        raise ProductionReviewError("catalog metadata must match locator baseline")
    if value["schema_version"] != 1 or value["kind"] != "production_catalog_shadow_v1" or value["catalog_id"]!=object_id("catalog",value,"catalog_id") or value["markers"]!=MARKERS or value["rules_version"]!=FROZEN_RULES_VERSION: raise ProductionReviewError("catalog identity/kind/markers/rules invalid")
    if require_current_rules and value["rules_version"] != RULES_VERSION:
        raise ProductionReviewError("catalog rules drift")
    if hashlib.sha256(entries_raw).hexdigest()!=value["entries_sha256"] or hashlib.sha256(exclusions_raw).hexdigest()!=value["exclusions_sha256"]: raise ProductionReviewError("catalog body hash mismatch")
    entries,exclusions=parse_jsonl(entries_raw,"catalog entries"),parse_jsonl(exclusions_raw,"catalog exclusions")
    if (len(entries),len(exclusions))!=(value["entry_count"],value["exclusion_count"]): raise ProductionReviewError("catalog counts mismatch")
    occs,locs=check_locator_snapshot(locator_manifest,occurrences_raw,locators_raw)
    locator_sha = _raw_object_sha(locator_manifest_raw, locator_manifest, "locator manifest")
    if value["locator_snapshot_id"]!=locator_manifest["locator_snapshot_id"] or value["locator_manifest_sha256"]!=locator_sha or value["eligible_component_ordinals"]!=_eligible_component_ordinals(locator_manifest,sources): raise ProductionReviewError("catalog locator binding mismatch")
    if expected_terminology_snapshot_id is not None and value["terminology_snapshot_id"] != expected_terminology_snapshot_id:
        raise ProductionReviewError("catalog terminology snapshot drift")
    if expected_source_identities is not None and sources != _validate_source_identities(expected_source_identities):
        raise ProductionReviewError("catalog source identities drift")
    previous=None; identities=set(); occurrence_ids=set()
    for entry in entries:
        _validate_catalog_entry(entry)
        if previous is not None and entry["logical_entry_identity"]<=previous: raise ProductionReviewError("catalog order invalid")
        previous=entry["logical_entry_identity"]
        try: normalized_path = surface.normalize_relative_path(entry["normalized_path"])
        except surface.ContractError as error: raise ProductionReviewError(f"catalog normalized_path invalid: {error}") from error
        if normalized_path != entry["normalized_path"] or entry["rules_version"]!=value["rules_version"] or entry["terminology_snapshot_id"]!=value["terminology_snapshot_id"] or not SOURCE_ID_RE.fullmatch(entry["fixed_source_identity"]): raise ProductionReviewError("catalog entry binding invalid")
        if entry["logical_entry_identity"] in identities or entry["occurrence_identity"] in occurrence_ids: raise ProductionReviewError("catalog duplicate identity")
        identities.add(entry["logical_entry_identity"]); occurrence_ids.add(entry["occurrence_identity"])
    for exclusion in exclusions:
        _validate_exclusion(exclusion)
        if exclusion["reason_code"] not in {"outside_initial_six_component_scope","empty_source","empty_target"} or exclusion["occurrence_identity"] in occurrence_ids: raise ProductionReviewError("catalog exclusion invalid")
        occurrence_ids.add(exclusion["occurrence_identity"])
    if occs is not None:
        expected=set(l["occurrence_identity"] for l in locs)
        if occurrence_ids!=expected: raise ProductionReviewError("catalog occurrence allocation is not total")
        rebuilt, rebuilt_entries, rebuilt_exclusions = build_catalog(
            locator_manifest, occurrences_raw, locators_raw, locator_manifest_raw=locator_manifest_raw,
            terminology_snapshot_id=value["terminology_snapshot_id"],
            source_identities=value["source_identities"], recorded_at=value["recorded_at"],
            recorded_by=value["recorded_by"], rules_version=value["rules_version"],
        )
        if value != rebuilt or entries_raw != rebuilt_entries or exclusions_raw != rebuilt_exclusions:
            raise ProductionReviewError("catalog does not exactly reconstruct from locator snapshot")
    return entries,exclusions


def build_shadow_policy(catalog: dict[str,Any], locator_manifest: dict[str,Any], *, catalog_manifest_raw: bytes,
        terminology_snapshot_id: str, source_identities: dict[str,str], recorded_at: str, recorded_by: str) -> dict[str,Any]:
    strict_utc_seconds(recorded_at); _nonempty(recorded_by,"recorded_by"); sources=_validate_source_identities(source_identities)
    eligible_component_ordinals=_eligible_component_ordinals(locator_manifest,sources)
    if catalog.get("locator_snapshot_id")!=locator_manifest.get("locator_snapshot_id") or catalog.get("terminology_snapshot_id")!=terminology_snapshot_id or catalog.get("source_identities")!=sources or catalog.get("eligible_component_ordinals")!=eligible_component_ordinals: raise ProductionReviewError("policy inputs disagree")
    if (catalog.get("recorded_at"),catalog.get("recorded_by")) != (recorded_at,recorded_by) or (locator_manifest.get("recorded_at"),locator_manifest.get("recorded_by")) != (recorded_at,recorded_by): raise ProductionReviewError("policy metadata must match locator/catalog baseline")
    catalog_sha = _raw_object_sha(catalog_manifest_raw, catalog, "catalog manifest")
    value={"schema_version":1,"shadow_policy_id":"","kind":"shadow_queue_policy_v1","markers":MARKERS,
        "catalog_id":catalog["catalog_id"],"catalog_manifest_sha256":catalog_sha,
        "locator_snapshot_id":locator_manifest["locator_snapshot_id"],"terminology_snapshot_id":terminology_snapshot_id,
        "source_identities":sources,"eligible_component_ordinals":eligible_component_ordinals,
        "rules_version":RULES_VERSION,"eligible_predicate":ELIGIBLE_PREDICATE,
        "feature_schema":FEATURE_SCHEMA,"priority_version":PRIORITY_VERSION,
        "priority_tuple":PRIORITY_TUPLE,
        "batch_size":80,"fixed_source_identities_typed":True,"recorded_at":recorded_at,"recorded_by":recorded_by}
    value["shadow_policy_id"]=object_id("shadow-queue-policy",value,"shadow_policy_id"); return value


def check_shadow_policy(value: dict[str,Any], *, catalog: dict[str,Any], catalog_manifest_raw: bytes,
        locator_manifest: dict[str,Any]) -> dict[str,Any]:
    keys=frozenset({"schema_version","shadow_policy_id","kind","markers","catalog_id","catalog_manifest_sha256","locator_snapshot_id","terminology_snapshot_id","source_identities","eligible_component_ordinals","rules_version","eligible_predicate","feature_schema","priority_version","priority_tuple","batch_size","fixed_source_identities_typed","recorded_at","recorded_by"})
    validate_exact(value,keys,"shadow policy"); _version_one(value, "shadow policy")
    strict_utc_seconds(value["recorded_at"]); _nonempty(value["recorded_by"],"recorded_by"); _markers(value["markers"])
    for key in ("shadow_policy_id", "catalog_id", "catalog_manifest_sha256", "locator_snapshot_id", "terminology_snapshot_id"):
        _sha(value[key], f"shadow policy.{key}")
    for key in ("kind", "rules_version", "eligible_predicate", "feature_schema", "priority_version"):
        _nonempty(value[key], f"shadow policy.{key}")
    _integer(value["batch_size"], "shadow policy.batch_size", minimum=1); _boolean(value["fixed_source_identities_typed"], "fixed_source_identities_typed")
    if not isinstance(value["priority_tuple"], list) or any(not isinstance(item, str) for item in value["priority_tuple"]): raise ProductionReviewError("priority_tuple must be a string array")
    if value["schema_version"]!=1 or value["shadow_policy_id"]!=object_id("shadow-queue-policy",value,"shadow_policy_id") or value["markers"]!=MARKERS or value["kind"]!="shadow_queue_policy_v1" or value["batch_size"]!=80 or value["rules_version"]!=FROZEN_RULES_VERSION or value["eligible_predicate"]!=ELIGIBLE_PREDICATE or value["feature_schema"]!=FEATURE_SCHEMA or value["priority_version"]!=PRIORITY_VERSION or value["priority_tuple"]!=PRIORITY_TUPLE or value["fixed_source_identities_typed"] is not True: raise ProductionReviewError("shadow policy semantics invalid")
    sources=_validate_source_identities(value["source_identities"])
    ordinals=_validate_component_ordinals(value["eligible_component_ordinals"], "eligible_component_ordinals")
    if (value["catalog_id"]!=catalog["catalog_id"] or value["catalog_manifest_sha256"]!=_raw_object_sha(catalog_manifest_raw, catalog, "catalog manifest") or value["terminology_snapshot_id"]!=catalog["terminology_snapshot_id"] or value["source_identities"]!=catalog["source_identities"] or ordinals!=catalog["eligible_component_ordinals"] or (value["recorded_at"],value["recorded_by"])!=(catalog["recorded_at"],catalog["recorded_by"])): raise ProductionReviewError("policy catalog binding mismatch")
    if (value["locator_snapshot_id"]!=locator_manifest["locator_snapshot_id"] or ordinals!=_eligible_component_ordinals(locator_manifest,sources) or (value["recorded_at"],value["recorded_by"])!=(locator_manifest["recorded_at"],locator_manifest["recorded_by"])): raise ProductionReviewError("policy locator binding mismatch")
    return value


def _ledger_record(entry: dict[str,Any], catalog_manifest_sha256: str, recorded_at: str, recorded_by: str) -> dict[str,Any]:
    _sha(catalog_manifest_sha256, "catalog manifest raw SHA-256")
    return {"schema_version":1,"logical_entry_identity":entry["logical_entry_identity"],"entry_revision_identity":entry["entry_revision_identity"],"from_state":None,"to_state":"queued","reason_code":"revision_frozen","provenance":{"kind":"revision_freeze_record","sha256":catalog_manifest_sha256},"recorded_by":recorded_by,"recorded_at":recorded_at,"parent_revision_identity":None,"migration_from_logical_entry_identity":None}


def build_shadow_journal(entries: list[dict[str,Any]], exclusions: list[dict[str,Any]], catalog: dict[str,Any], policy: dict[str,Any], *,
        catalog_manifest_raw: bytes, locator_manifest: dict[str, Any], recorded_at: str, recorded_by: str) -> tuple[dict[str,Any],list[dict[str,Any]],dict[str,Any]]:
    strict_utc_seconds(recorded_at); _nonempty(recorded_by,"recorded_by")
    check_shadow_policy(policy,catalog=catalog,catalog_manifest_raw=catalog_manifest_raw,locator_manifest=locator_manifest)
    catalog_manifest_sha256 = _raw_object_sha(catalog_manifest_raw, catalog, "catalog manifest")
    if (recorded_at,recorded_by)!=(policy["recorded_at"],policy["recorded_by"]): raise ProductionReviewError("journal metadata must match frozen baseline")
    group={"schema_version":1,"group_id":"","catalog_id":catalog["catalog_id"],"shadow_policy_id":policy["shadow_policy_id"],"event_count":len(entries),"recorded_at":recorded_at,"recorded_by":recorded_by}; group["group_id"]=object_id("journal-group",group,"group_id")
    events=[]; previous=None
    for ordinal,entry in enumerate(entries):
        event={"schema_version":1,"event_id":"","group_id":group["group_id"],"ordinal":ordinal,"catalog_id":catalog["catalog_id"],"shadow_policy_id":policy["shadow_policy_id"],"attempt":0,"batch_id":None,"task_id":None,"handoff_id":None,"record":_ledger_record(entry,catalog_manifest_sha256,recorded_at,recorded_by),"previous_event_hash":previous}; event["event_id"]=object_id("journal-event",event,"event_id"); previous=event["event_id"]; events.append(event)
    raw=_jsonl(events); checkpoint={"schema_version":1,"checkpoint_id":"","group_id":group["group_id"],"catalog_id":catalog["catalog_id"],"shadow_policy_id":policy["shadow_policy_id"],"events_sha256":hashlib.sha256(raw).hexdigest(),"event_count":len(events),"last_event_hash":previous,"recorded_at":recorded_at,"recorded_by":recorded_by,"state_counts":{"queued":len(events)}}; checkpoint["checkpoint_id"]=object_id("journal-checkpoint",checkpoint,"checkpoint_id")
    check_shadow_journal(group,raw,checkpoint,catalog=catalog,catalog_manifest_raw=catalog_manifest_raw,locator_manifest=locator_manifest,entries=entries,exclusions=exclusions,policy=policy); return group,events,checkpoint


def check_shadow_journal(group: dict[str,Any], events_raw: bytes, checkpoint: dict[str,Any], *, catalog: dict[str,Any],
        catalog_manifest_raw: bytes, locator_manifest: dict[str, Any], entries: list[dict[str,Any]], exclusions: list[dict[str,Any]], policy: dict[str,Any]) -> dict[str,Any]:
    gkeys=frozenset({"schema_version","group_id","catalog_id","shadow_policy_id","event_count","recorded_at","recorded_by"}); ckeys=frozenset({"schema_version","checkpoint_id","group_id","catalog_id","shadow_policy_id","events_sha256","event_count","last_event_hash","recorded_at","recorded_by","state_counts"})
    validate_exact(group,gkeys,"journal group"); validate_exact(checkpoint,ckeys,"journal checkpoint")
    _version_one(group, "journal group"); _version_one(checkpoint, "journal checkpoint")
    check_shadow_policy(policy,catalog=catalog,catalog_manifest_raw=catalog_manifest_raw,locator_manifest=locator_manifest)
    catalog_manifest_sha256 = _raw_object_sha(catalog_manifest_raw, catalog, "catalog manifest")
    for key in ("group_id", "catalog_id", "shadow_policy_id"):
        _sha(group[key], f"journal group.{key}")
    for key in ("checkpoint_id", "group_id", "catalog_id", "shadow_policy_id", "events_sha256"):
        _sha(checkpoint[key], f"journal checkpoint.{key}")
    _integer(group["event_count"], "journal group.event_count"); _integer(checkpoint["event_count"], "journal checkpoint.event_count")
    if checkpoint["last_event_hash"] is not None: _sha(checkpoint["last_event_hash"], "journal checkpoint.last_event_hash")
    if not isinstance(checkpoint["state_counts"], dict) or frozenset(checkpoint["state_counts"]) != {"queued"}: raise ProductionReviewError("checkpoint state_counts exact schema mismatch")
    _integer(checkpoint["state_counts"]["queued"], "checkpoint.state_counts.queued")
    if hashlib.sha256(_jsonl(entries)).hexdigest()!=catalog["entries_sha256"] or len(entries)!=catalog["entry_count"]: raise ProductionReviewError("journal catalog entries do not match catalog manifest")
    if hashlib.sha256(_jsonl(exclusions)).hexdigest()!=catalog["exclusions_sha256"] or len(exclusions)!=catalog["exclusion_count"]: raise ProductionReviewError("journal catalog exclusions do not match catalog manifest")
    if (group["recorded_at"],group["recorded_by"])!=(policy["recorded_at"],policy["recorded_by"]) or (checkpoint["recorded_at"],checkpoint["recorded_by"])!=(policy["recorded_at"],policy["recorded_by"]): raise ProductionReviewError("journal metadata binding mismatch")
    if group["group_id"]!=object_id("journal-group",group,"group_id") or checkpoint["checkpoint_id"]!=object_id("journal-checkpoint",checkpoint,"checkpoint_id"): raise ProductionReviewError("journal group/checkpoint ID mismatch")
    if hashlib.sha256(events_raw).hexdigest()!=checkpoint["events_sha256"]: raise ProductionReviewError("journal events raw hash mismatch")
    events=parse_jsonl(events_raw,"journal events")
    if len(events)!=group["event_count"] or len(events)!=checkpoint["event_count"]: raise ProductionReviewError("journal count mismatch")
    if group["catalog_id"]!=catalog["catalog_id"] or group["shadow_policy_id"]!=policy["shadow_policy_id"] or checkpoint["group_id"]!=group["group_id"] or checkpoint["catalog_id"]!=catalog["catalog_id"] or checkpoint["shadow_policy_id"]!=policy["shadow_policy_id"]: raise ProductionReviewError("journal binding mismatch")
    expected=[(e["logical_entry_identity"],e["entry_revision_identity"]) for e in entries]
    excluded={x["occurrence_identity"] for x in exclusions}; eligible_occurrences={e["occurrence_identity"] for e in entries}
    if excluded & eligible_occurrences or len(excluded)+len(eligible_occurrences)!=catalog["entry_count"]+catalog["exclusion_count"]: raise ProductionReviewError("journal catalog entry/exclusion partition invalid")
    actual=[]; previous=None; records=[]
    for ordinal,event in enumerate(events):
        validate_exact(event,JOURNAL_EVENT_KEYS,"journal event"); _version_one(event, "journal event")
        for key in ("event_id", "group_id", "catalog_id", "shadow_policy_id"):
            _sha(event[key], f"journal event.{key}")
        _integer(event["ordinal"], "journal event.ordinal"); _integer(event["attempt"], "journal event.attempt")
        if event["previous_event_hash"] is not None: _sha(event["previous_event_hash"], "journal event.previous_event_hash")
        for key in ("batch_id", "task_id", "handoff_id"):
            if event[key] is not None and not isinstance(event[key], str): raise ProductionReviewError(f"journal event.{key} must be string or null")
        if event["ordinal"]!=ordinal or event["group_id"]!=group["group_id"] or event["catalog_id"]!=catalog["catalog_id"] or event["shadow_policy_id"]!=policy["shadow_policy_id"] or event["previous_event_hash"]!=previous or event["event_id"]!=object_id("journal-event",event,"event_id") or event["attempt"]!=0 or any(event[k] is not None for k in ("batch_id","task_id","handoff_id")): raise ProductionReviewError("journal event envelope/order/hash invalid")
        record=validate_exact(event["record"],LEDGER_RECORD_KEYS,"embedded ledger record")
        if record["provenance"]!={"kind":"revision_freeze_record","sha256":catalog_manifest_sha256}: raise ProductionReviewError("journal catalog provenance invalid")
        expected_record = _ledger_record(entries[ordinal], catalog_manifest_sha256, group["recorded_at"], group["recorded_by"])
        if record != expected_record: raise ProductionReviewError("journal record does not exactly match catalog entry")
        actual.append((record["logical_entry_identity"],record["entry_revision_identity"])); records.append(record); previous=event["event_id"]
    if actual!=expected: raise ProductionReviewError("journal must match eligible catalog logical order exactly")
    try: view=ledger.replay(records)
    except ledger.LedgerError as error: raise ProductionReviewError(f"ledger replay failed: {error}") from error
    if checkpoint["last_event_hash"]!=previous or checkpoint["state_counts"]!={"queued":len(events)}: raise ProductionReviewError("checkpoint replay mismatch")
    return {"schema_version":1,"logical_entries":len(view),"state_counts":{"queued":len(events)},"queued_revisions":[r for _,r in actual]}


def _priority(entry: dict[str,Any], component_ordinals: dict[str, int]) -> tuple[Any,...]:
    risk=entry["risk"]; format_risk=bool(risk["has_args_order"] or risk["has_special"])
    if entry["component"] not in component_ordinals:
        raise ProductionReviewError("eligible entry component lacks frozen manifest ordinal")
    return (not format_risk,-risk["component_group_size"],not risk["component_group_last"],component_ordinals[entry["component"]],bytes.fromhex(entry["entry_revision_identity"]))


def build_shadow_batch(entries: list[dict[str,Any]], catalog: dict[str,Any], policy: dict[str,Any], group: dict[str,Any], events_raw: bytes, checkpoint: dict[str,Any], exclusions: list[dict[str,Any]], *, catalog_manifest_raw: bytes, locator_manifest: dict[str, Any]) -> dict[str,Any]:
    replay=check_shadow_journal(group,events_raw,checkpoint,catalog=catalog,catalog_manifest_raw=catalog_manifest_raw,locator_manifest=locator_manifest,entries=entries,exclusions=exclusions,policy=policy)
    queued=set(replay["queued_revisions"]); eligible_entries=[e for e in entries if e["entry_revision_identity"] in queued]
    component_ordinals={row["component"]:row["ordinal"] for row in _validate_component_ordinals(
        policy["eligible_component_ordinals"], "eligible_component_ordinals")}
    priority=[e["entry_revision_identity"] for e in sorted(eligible_entries,key=lambda e:_priority(e,component_ordinals))]
    selected=sorted(priority[:policy["batch_size"]]); carry=sorted(priority[policy["batch_size"]:]); eligible=sorted(priority)
    value={"schema_version":1,"shadow_batch_id":"","kind":"shadow_batch_draft_v1","markers":MARKERS,"catalog_id":catalog["catalog_id"],"shadow_policy_id":policy["shadow_policy_id"],"checkpoint_id":checkpoint["checkpoint_id"],"eligible":eligible,"batch_selected":selected,"carry_over":carry,"promotion_pool":[],"eligible_ordered_hash":ordered_set_hash(eligible),"priority_ordered_hash":ordered_set_hash(priority),"batch_selected_ordered_hash":ordered_set_hash(selected),"carry_over_ordered_hash":ordered_set_hash(carry),"promotion_pool_ordered_hash":ordered_set_hash([])}
    value["shadow_batch_id"]=object_id("shadow-batch",value,"shadow_batch_id"); return value


def validate_shadow_batch(value: dict[str,Any], *, entries: list[dict[str,Any]], exclusions: list[dict[str,Any]], catalog: dict[str,Any], policy: dict[str,Any], group: dict[str,Any], events_raw: bytes, checkpoint: dict[str,Any], catalog_manifest_raw: bytes, locator_manifest: dict[str, Any]) -> dict[str,Any]:
    keys=frozenset({"schema_version","shadow_batch_id","kind","markers","catalog_id","shadow_policy_id","checkpoint_id","eligible","batch_selected","carry_over","promotion_pool","eligible_ordered_hash","priority_ordered_hash","batch_selected_ordered_hash","carry_over_ordered_hash","promotion_pool_ordered_hash"}); validate_exact(value,keys,"shadow batch"); _version_one(value, "shadow batch")
    _markers(value["markers"]); _nonempty(value["kind"], "shadow batch.kind")
    for key in ("shadow_batch_id", "catalog_id", "shadow_policy_id", "checkpoint_id", "eligible_ordered_hash", "priority_ordered_hash", "batch_selected_ordered_hash", "carry_over_ordered_hash", "promotion_pool_ordered_hash"):
        _sha(value[key], f"shadow batch.{key}")
    if value["markers"]!=MARKERS or value["kind"]!="shadow_batch_draft_v1" or value["shadow_batch_id"]!=object_id("shadow-batch",value,"shadow_batch_id"): raise ProductionReviewError("batch identity/markers invalid")
    for key in ("eligible","batch_selected","carry_over","promotion_pool"):
        xs=value[key]
        if not isinstance(xs,list) or xs!=sorted(xs) or len(xs)!=len(set(xs)) or any(not isinstance(x,str) or not SHA256_RE.fullmatch(x) for x in xs): raise ProductionReviewError(f"batch {key} invalid")
    if set(value["eligible"])!=set(value["batch_selected"])|set(value["carry_over"]) or set(value["batch_selected"])&set(value["carry_over"]) or value["promotion_pool"] or len(value["batch_selected"])>80: raise ProductionReviewError("batch conservation invalid")
    for key,hkey in (("eligible","eligible_ordered_hash"),("batch_selected","batch_selected_ordered_hash"),("carry_over","carry_over_ordered_hash"),("promotion_pool","promotion_pool_ordered_hash")):
        if value[hkey]!=ordered_set_hash(value[key]): raise ProductionReviewError(f"batch {key} hash mismatch")
    expected=build_shadow_batch(entries,catalog,policy,group,events_raw,checkpoint,exclusions,catalog_manifest_raw=catalog_manifest_raw,locator_manifest=locator_manifest)
    if value!=expected: raise ProductionReviewError("batch does not equal checkpoint queued/catalog priority construction")
    return value


RECONCILIATION_BASE_KEYS = frozenset({"schema_version","ok","catalog_entries","catalog_exclusions",
    "journal_events","batch_eligible","batch_selected","carry_over","promotion_pool",
    "catalog_journal_conserved","catalog_batch_conserved","authoritative","dispatchable","promotable"})
RECONCILIATION_AXES = frozenset({"manifest_sha_and_order","loader_contract_sha_and_runtime","occurrences",
    "terminology_snapshot","source_identities","current_rules","fully_reconstructed_catalog"})
RECONCILIATION_ARTIFACT_KEYS = RECONCILIATION_BASE_KEYS | frozenset({"catalog_id","group_id",
    "shadow_batch_id","live_occurrences","drift_axes","drift","shadow_publication_blocked"})


def reconciliation_report(entries: list[dict[str,Any]], exclusions: list[dict[str,Any]], events: list[dict[str,Any]], batch: dict[str,Any]) -> dict[str,Any]:
    revisions={e["entry_revision_identity"] for e in entries}; journal={e["record"]["entry_revision_identity"] for e in events}; eligible=set(batch["eligible"]); ok=revisions==journal==eligible
    return {"schema_version":1,"ok":ok,"catalog_entries":len(entries),"catalog_exclusions":len(exclusions),"journal_events":len(events),"batch_eligible":len(eligible),"batch_selected":len(batch["batch_selected"]),"carry_over":len(batch["carry_over"]),"promotion_pool":0,"catalog_journal_conserved":revisions==journal,"catalog_batch_conserved":revisions==eligible,"authoritative":False,"dispatchable":False,"promotable":False}


def validate_reconciliation_artifact(value: object) -> dict[str, Any]:
    row = validate_exact(value, RECONCILIATION_ARTIFACT_KEYS, "reconciliation artifact")
    _version_one(row, "reconciliation artifact")
    for key in ("ok","catalog_journal_conserved","catalog_batch_conserved","drift","shadow_publication_blocked"):
        _boolean(row[key], f"reconciliation artifact.{key}")
    if any(row[key] is not False for key in ("authoritative","dispatchable","promotable")):
        raise ProductionReviewError("reconciliation false markers changed")
    for key in ("catalog_entries","catalog_exclusions","journal_events","batch_eligible","batch_selected","carry_over","promotion_pool","live_occurrences"):
        _integer(row[key], f"reconciliation artifact.{key}")
    if row["promotion_pool"] != 0:
        raise ProductionReviewError("reconciliation promotion_pool must be zero")
    for key in ("catalog_id","group_id","shadow_batch_id"):
        _sha(row[key], f"reconciliation artifact.{key}")
    axes = validate_exact(row["drift_axes"], RECONCILIATION_AXES, "reconciliation drift_axes")
    for key in axes: _boolean(axes[key], f"reconciliation drift_axes.{key}")
    if row["drift"] != (not all(axes.values())) or row["shadow_publication_blocked"] != row["drift"]:
        raise ProductionReviewError("reconciliation drift markers do not match axes")
    return row


def _tree_bytes(path: Path) -> dict[str,bytes]:
    if not path.is_dir() or path.is_symlink(): raise ProductionReviewError(f"artifact is not a regular directory: {path}")
    result={}
    for item in sorted(path.rglob("*")):
        if item.is_symlink() or (not item.is_file() and not item.is_dir()): raise ProductionReviewError("artifact tree contains unsupported entry")
        if item.is_file(): result[item.relative_to(path).as_posix()]=item.read_bytes()
    return result


def _tree_equals(path: Path, files: dict[str, bytes]) -> bool:
    if _tree_bytes(path) != dict(sorted(files.items())):
        return False
    actual_dirs = {item.relative_to(path).as_posix() for item in path.rglob("*") if item.is_dir()}
    expected_dirs = {parent.as_posix() for name in files for parent in Path(name).parents
                     if parent != Path(".")}
    return actual_dirs == expected_dirs


def _rename_directory_noreplace(source: Path, destination: Path) -> None:
    """Atomically publish a directory without replacing a racing destination."""
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(libc, "renameat2", None)
    if renameat2 is None:
        raise ProductionReviewError("atomic no-replace directory rename is unavailable")
    renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    renameat2.restype = ctypes.c_int
    if renameat2(-100, os.fsencode(source), -100, os.fsencode(destination), 1) != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise FileExistsError(code, os.strerror(code), destination)
        raise OSError(code, os.strerror(code), destination)


_PUBLICATION_STAGE_RE = re.compile(r"^\.production-review-stage-[0-9a-f]{64}$")
_MAX_STAGING_CLEANUP_ENTRIES = 4096


def _publication_stage_name(files: dict[str, bytes]) -> str:
    """Return the task-owned, content-addressed staging directory name."""
    digest = hashlib.sha256(b"production-review-directory-stage-v1\0")
    for name, data in sorted(files.items()):
        encoded = name.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return f".production-review-stage-{digest.hexdigest()}"


def _safe_staging_directory(path: Path) -> bool:
    """Recognize a bounded ordinary tree without following any symlink."""
    try:
        mode = path.lstat().st_mode
        if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
            return False
        pending = [path]
        seen = 0
        while pending:
            directory = pending.pop()
            for item in directory.iterdir():
                seen += 1
                if seen > _MAX_STAGING_CLEANUP_ENTRIES:
                    return False
                mode = item.lstat().st_mode
                if stat.S_ISLNK(mode):
                    return False
                if stat.S_ISDIR(mode):
                    pending.append(item)
                elif not stat.S_ISREG(mode):
                    return False
        return True
    except OSError as error:
        raise ProductionReviewError(f"cannot inspect publication staging residue: {error}") from error


def _cleanup_publication_stages(parent: Path) -> None:
    """Remove only bounded task-owned content-addressed staging directories."""
    removed = False
    for sibling in parent.iterdir():
        if (_PUBLICATION_STAGE_RE.fullmatch(sibling.name) and
                _safe_staging_directory(sibling)):
            shutil.rmtree(sibling)
            removed = True
    if removed:
        _fsync_directory(parent)


def _production_total(root: Path, pending: int) -> int:
    try:
        total = pending
        for rel in ("evidence/production-review", "i18n/quality/production-review"):
            base = root / rel
            if base.exists():
                total += sum(path.stat().st_size for path in base.rglob("*")
                             if path.is_file() and not path.is_symlink())
        return total
    except OSError as error:
        raise ProductionReviewError(f"cannot measure production-review occupancy: {error}") from error


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _lexical_publish_target(final_dir: Path, root: Path) -> Path:
    """Return an absolute lexical target without resolving its components."""
    final = Path(os.path.abspath(os.fspath(final_dir)))
    try:
        final.relative_to(root)
    except ValueError as error:
        raise ProductionReviewError("publish path escapes tracked root") from error
    if final == root:
        raise ProductionReviewError("publish target must be beneath tracked root")
    return final


def _reject_symlink_components(root: Path, path: Path) -> None:
    """Reject existing or dangling symlinks from root through path."""
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise ProductionReviewError("publish path escapes tracked root") from error
    current = root
    for component in relative.parts:
        current = current / component
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            continue
        except OSError as error:
            raise ProductionReviewError(
                f"cannot inspect publication target component {current}: {error}"
            ) from error
        if stat.S_ISLNK(mode):
            raise ProductionReviewError(
                f"publication target traverses a symlink: {current}"
            )


def _open_publication_lock(root: Path, lock_directory: Path):
    """Create/open the global lock through pinned, no-follow directory FDs."""
    try:
        relative = lock_directory.relative_to(root)
    except ValueError as error:
        raise ProductionReviewError("publication lock path escapes tracked root") from error
    if not relative.parts:
        raise ProductionReviewError("publication lock directory must be beneath tracked root")

    directory_flags = (os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                       getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0))
    current = os.open(root, directory_flags)
    try:
        for component in relative.parts:
            try:
                child = os.open(component, directory_flags, dir_fd=current)
            except FileNotFoundError:
                os.mkdir(component, mode=0o755, dir_fd=current)
                child = os.open(component, directory_flags, dir_fd=current)
            os.close(current)
            current = child
        lock_flags = (os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0) |
                      getattr(os, "O_CLOEXEC", 0))
        descriptor = os.open(".publish.lock", lock_flags, 0o600, dir_fd=current)
        return os.fdopen(descriptor, "a+b")
    finally:
        os.close(current)


def _validate_publication_occupancy(root: Path, final: Path, category: str | None,
                                    family: int, *, already_present: bool) -> None:
    if category in {"locator", "catalog"}:
        siblings = [path for path in final.parent.iterdir()
                    if path.is_dir() and not path.is_symlink()]
        allowed = [final] if already_present else []
        if siblings != allowed:
            raise ProductionReviewError(f"WP1 permits only one {category} baseline")
    occupied = _production_total(root, 0)
    pending = 0 if already_present else family
    if occupied + pending > BUDGETS["total"]:
        raise ProductionReviewError(
            "production-review tracked total exceeds 128 MiB "
            f"(occupied={occupied}, pending={pending}, limit={BUDGETS['total']})"
        )


def atomic_publish_directory(files: dict[str, bytes], final_dir: Path, *, root: Path,
                             budget: int, category: str | None = None) -> str:
    """Publish one immutable artifact family under the production-wide lock.

    The lock covers occupancy measurement, family/total budget checks, rename,
    and durability fsync, so two independently valid publishers cannot race the
    128 MiB ceiling.  ``category`` is mandatory for repository publications;
    tests using an isolated root may pass an explicit ad-hoc budget without it.
    """
    root = root.resolve()
    final = _lexical_publish_target(final_dir, root)
    _reject_symlink_components(root, final)
    repository_root = Path(__file__).resolve().parents[2]
    if root == repository_root and category is None:
        raise ProductionReviewError("repository production publication requires a category")
    if not files or any(
        not name or Path(name).is_absolute() or ".." in Path(name).parts
        for name in files
    ):
        raise ProductionReviewError("invalid directory publication mapping")
    if any(not isinstance(data, bytes) for data in files.values()):
        raise ProductionReviewError("publication bodies must be bytes")
    family = sum(len(data) for data in files.values())
    if category is not None:
        if category not in BUDGETS or category == "total":
            raise ProductionReviewError(f"unknown production-review category: {category}")
        if budget != BUDGETS[category]:
            raise ProductionReviewError("publication category/budget mismatch")
    if family > budget:
        raise ProductionReviewError(
            f"artifact family bytes={family} exceeds {category or 'provided'} budget={budget}"
        )

    lock_directory = root / ".artifacts/i18n/production-review"
    lock_path = lock_directory / ".publish.lock"
    try:
        # This lexical/lstat pass rejects pre-existing and dangling links before
        # any lock-directory creation or lock-file open.  The fd-relative walk
        # then closes the check/use race without following swapped components.
        _reject_symlink_components(root, lock_directory)
        _reject_symlink_components(root, lock_path)
        lock_handle = _open_publication_lock(root, lock_directory)
    except ProductionReviewError:
        raise
    except OSError as error:
        raise ProductionReviewError(f"publication lock I/O failed: {error}") from error
    with lock_handle as lock:
      try:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        _reject_symlink_components(root, final)
        final.parent.mkdir(parents=True, exist_ok=True)
        _reject_symlink_components(root, final)
        _cleanup_publication_stages(final.parent)
        if final.exists():
            _reject_symlink_components(root, final)
            if not _tree_equals(final, files):
                raise ProductionReviewError(f"immutable artifact tree drift: {final}")
            _validate_publication_occupancy(
                root, final, category, family, already_present=True)
            _fsync_directory(final.parent)
            return "ALREADY_PRESENT"
        _validate_publication_occupancy(
            root, final, category, family, already_present=False)

        temp = final.parent / _publication_stage_name(files)
        temp.mkdir(mode=0o700)
        outcome = "PUBLISHED"
        try:
            for name, data in sorted(files.items()):
                path = temp / name
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("xb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
            directories = sorted(
                (path for path in temp.rglob("*") if path.is_dir()),
                key=lambda path: len(path.parts), reverse=True,
            )
            for directory in [*directories, temp]:
                _fsync_directory(directory)
            try:
                _reject_symlink_components(root, final)
                _rename_directory_noreplace(temp, final)
            except FileExistsError:
                _reject_symlink_components(root, final)
                if temp.exists():
                    shutil.rmtree(temp)
                    _fsync_directory(final.parent)
                if not _tree_equals(final, files):
                    raise ProductionReviewError(f"immutable artifact tree drift: {final}")
                _validate_publication_occupancy(
                    root, final, category, family, already_present=True)
                outcome = "ALREADY_PRESENT"
            _reject_symlink_components(root, final)
            _fsync_directory(final.parent)
        finally:
            if temp.exists():
                shutil.rmtree(temp)
        return outcome
      except ProductionReviewError:
        raise
      except OSError as error:
        raise ProductionReviewError(f"production publication I/O failed: {error}") from error
