"""Rebuildable personal-scale SQLite projection for production-review WP2-Lite."""
from __future__ import annotations

import errno
import fcntl
import hashlib
import os
import sqlite3
import stat
import subprocess
import tempfile
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from . import production_review as wp1
from . import production_review_v2_lite as catalog
from . import production_review_v2_lite_evidence as evidence
from . import git_evidence_reader
import contextual_result_check as contextual_check

RUNTIME_RELATIVE = Path(".artifacts/i18n/production-review-v2-lite")
DATABASE_NAME = "queue.sqlite3"
LOCK_NAME = "repository.lock"
CHECKPOINT_NAME = "active-batch.json"
BATCH_PREFIX = "evidence/production-review-v2-lite/batches/"
MIGRATION_PREFIX = "evidence/production-review-v2-lite/migrations/"
QUEUE_SCHEMA_PATH = "i18n/quality/production-review-v2-lite/queue-v1.schema.sql"
DURABLE_STATES = frozenset({"done", "repair_required", "blocked"})
OVERRIDE_STATES = frozenset({"reserved", "screened", "deep_required", "repair_required", "done", "blocked"})
BUSINESS_STATES = frozenset({"queued", *OVERRIDE_STATES})

META_SQL = """CREATE TABLE meta(
  singleton INTEGER PRIMARY KEY CHECK(singleton=1),
  schema_version INTEGER NOT NULL CHECK(schema_version=1),
  catalog_id TEXT NOT NULL,
  evidence_head TEXT NOT NULL,
  rebuilt_at TEXT NOT NULL
)"""
STATE_SQL = """CREATE TABLE state_override(
  entry_revision_identity TEXT PRIMARY KEY,
  logical_entry_identity TEXT NOT NULL,
  state TEXT NOT NULL CHECK(state IN
    ('reserved','screened','deep_required','repair_required','done','blocked')),
  batch_id TEXT,
  attempt INTEGER NOT NULL CHECK(attempt>=0),
  result_sha256 TEXT,
  updated_at TEXT NOT NULL
)"""
RECONCILIATION_SQL = """CREATE TABLE reconciliation(
  old_logical_entry_identity TEXT NOT NULL,
  old_entry_revision_identity TEXT NOT NULL,
  new_logical_entry_identity TEXT,
  new_entry_revision_identity TEXT,
  disposition TEXT NOT NULL CHECK(disposition IN
    ('unchanged','revision_changed','logical_moved','removed','ambiguous','unmapped')),
  reason TEXT NOT NULL CHECK(reason IN
    ('unchanged','target_changed','source_changed','source_tag_changed',
     'call_locator_changed','fixed_source_changed','terminology_changed',
     'rules_changed','args_order_changed','removed','ambiguous','unmapped')),
  migration_id TEXT NOT NULL,
  PRIMARY KEY(migration_id,old_entry_revision_identity)
)"""
EXPECTED_SCHEMA = {"meta": META_SQL, "state_override": STATE_SQL, "reconciliation": RECONCILIATION_SQL}

BATCH_MANIFEST_KEYS = frozenset({"schema_version", "kind", "catalog_id", "policy_sha256", "base_commit",
    "batch_id", "attempt", "ordered_revisions", "ordered_revisions_sha256", "entry_snapshots_sha256",
    "adapter_refs", "results_sha256", "adjudications_sha256", "gates_sha256", "producer_task_ids",
    "recorded_at", "recorded_by"})
RESULT_KEYS = frozenset({"schema_version", "source", "target", "source_tag", "normalized_path", "call_locator",
    "logical_entry_identity", "entry_revision_identity", "surface_verdict", "surface_observation",
    "deep_verdict", "deep_observation", "input_sha256", "output_sha256", "final_state", "completion_level"})
ADJUDICATION_KEYS = frozenset({"schema_version", "entry_revision_identity", "observation_contract", "observation_identity", "observation_sha256", "disposition",
    "evidence_path", "evidence_commit", "evidence_snapshot", "conclusion", "repair_required"})
ADAPTER_REF_KEYS = frozenset({"contract", "input_path", "input_sha256", "output_path", "output_sha256",
                              "candidate_identity"})
ADAPTER_REF_WITH_GROUP_KEYS = ADAPTER_REF_KEYS | {"group_manifest_path", "group_manifest_sha256"}


def database_path(root: Path) -> Path:
    return root / RUNTIME_RELATIVE / DATABASE_NAME


def repository_lock_path(root: Path) -> Path:
    return root / RUNTIME_RELATIVE / LOCK_NAME


def checkpoint_path(root: Path) -> Path:
    return root / RUNTIME_RELATIVE / CHECKPOINT_NAME


def _error(message: str) -> wp1.ProductionReviewError:
    return wp1.ProductionReviewError(message)


def _git(root: Path, *args: str) -> bytes:
    try:
        return subprocess.run(["git", *args], cwd=root, check=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        detail = error.stderr.decode("utf-8", "replace").strip() if isinstance(error, subprocess.CalledProcessError) else str(error)
        raise _error(f"queue git operation failed: {detail}") from error


def _head(root: Path, treeish: str) -> str:
    value = _git(root, "rev-parse", "--verify", f"{treeish}^{{commit}}").decode("ascii").strip()
    if len(value) != 40:
        raise _error("queue treeish did not resolve to a commit")
    return value


def _tree(root: Path, treeish: str) -> dict[str, tuple[str, str, str]]:
    raw = git_evidence_reader.read(root, "tree", treeish, _git,
                                   "ls-tree", "-rz", "--full-tree", "-r")
    result: dict[str, tuple[str, str, str]] = {}
    try:
        records = raw.split(b"\0")
        if records[-1] != b"":
            raise ValueError("missing NUL terminator")
        for record in records[:-1]:
            metadata, path_raw = record.split(b"\t", 1)
            mode, kind, object_id = (part.decode("ascii") for part in metadata.split())
            path = path_raw.decode("utf-8")
            if path in result:
                raise ValueError("duplicate path")
            result[path] = (mode, kind, object_id)
    except (UnicodeDecodeError, ValueError) as error:
        raise _error(f"cannot parse queue Git tree: {error}") from error
    return result


def _blob(root: Path, object_id: str, label: str) -> bytes:
    try:
        return git_evidence_reader.read(root, "blob", object_id, _git, "cat-file", "blob")
    except wp1.ProductionReviewError as error:
        raise _error(f"cannot read {label}: {error}") from error


def _ordinary_blob(root: Path, tree: dict[str, tuple[str, str, str]], path: str) -> bytes:
    entry = tree.get(path)
    if entry is None:
        raise _error(f"tracked formal catalog/evidence file is missing: {path}")
    mode, kind, object_id = entry
    if mode not in {"100644", "100755"} or kind != "blob":
        raise _error(f"tracked formal catalog/evidence entry is not an ordinary file: {path}")
    return _blob(root, object_id, path)


def _exact(value: object, keys: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        present = set(value) if isinstance(value, dict) else set()
        raise _error(f"adjudications must exactly cover observations; {label} schema exact keys mismatch (missing={sorted(keys-present)}, extra={sorted(present-keys)})")
    return value


def _sha(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise _error(f"{label} must be a lowercase SHA-256")
    return value


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise _error(f"{label} must be a non-empty string")
    return value


def _schema_one(value: object, label: str) -> None:
    if type(value) is not int or value != 1:
        raise _error(f"{label} schema_version must be integer 1")


def _catalog_from_tree(root: Path, treeish: str) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, bytes]]:
    tree = _tree(root, treeish)
    catalog_paths = {path for path in tree if path.startswith(catalog.CATALOG_PREFIX + "/")}
    expected_catalog_paths = {path for path in catalog.CANDIDATE_FILES
                              if path.startswith(catalog.CATALOG_PREFIX + "/")}
    quality_prefix = "i18n/quality/production-review-v2-lite/"
    quality_paths = {path for path in tree if path.startswith(quality_prefix)}
    expected_quality_paths = ({path for path in catalog.CANDIDATE_FILES
                               if path.startswith(quality_prefix)} | {QUEUE_SCHEMA_PATH})
    if catalog_paths != expected_catalog_paths or not quality_paths.issubset(expected_quality_paths):
        raise _error(
            "formal catalog subtree or planned quality sibling set mismatch "
            f"(catalog_missing={sorted(expected_catalog_paths-catalog_paths)}, "
            f"catalog_extra={sorted(catalog_paths-expected_catalog_paths)}, "
            f"quality_extra={sorted(quality_paths-expected_quality_paths)})")
    files = {path: _ordinary_blob(root, tree, path) for path in catalog.CANDIDATE_FILES}
    manifest, entries, _exclusions = catalog.validate_catalog_files(files)
    return manifest, entries, files


def _clean_evidence(root: Path) -> None:
    raw = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--",
               "evidence/production-review-v2-lite")
    if raw:
        raise _error("tracked evidence worktree must be clean before queue rebuild")


def _no_checkpoint(root: Path) -> None:
    path = checkpoint_path(root)
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return
    except OSError as error:
        raise _error(f"cannot inspect active checkpoint: {error}") from error
    raise _error("queue rebuild requires no active checkpoint")


@contextmanager
def writer_lock(root: Path) -> Iterator[Any]:
    path = repository_lock_path(root)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = path.open("a+b")
    except OSError as error:
        raise _error(f"cannot open repository lock: {error}") from error
    try:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            if error.errno in (errno.EACCES, errno.EAGAIN):
                raise _error("repository lock is held by another writer") from error
            raise _error(f"cannot acquire repository lock: {error}") from error
        yield handle
    finally:
        handle.close()


def writer_active(root: Path) -> bool:
    path = repository_lock_path(root)
    try:
        handle = path.open("rb")
    except FileNotFoundError:
        return False
    except OSError as error:
        raise _error(f"cannot inspect repository lock: {error}") from error
    with handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            if error.errno in (errno.EACCES, errno.EAGAIN):
                return True
            raise _error(f"cannot inspect repository lock: {error}") from error
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return False


def _candidate_commits(root: Path, treeish: str, path: str) -> list[str]:
    raw = _git(root, "log", "--full-history", "--format=%H", "--diff-filter=AM", treeish, "--", path)
    commits = raw.decode("ascii").splitlines()
    if not commits:
        raise _error(f"cannot locate introduction/change commit for evidence: {path}")
    return commits


def _commit_parent(root: Path, commit: str) -> str:
    raw = _git(root, "rev-list", "--parents", "-n", "1", commit).decode("ascii").split()
    if len(raw) != 2:
        raise _error("durable batch commit must have exactly one parent")
    return raw[1]


def _publication_commit(root: Path, treeish: str, tree: dict[str, tuple[str, str, str]],
                        paths: set[str], base_commit: object) -> str:
    """Find the one publication of the current evidence bytes bound to base_commit."""
    base = _nonempty(base_commit, "batch base_commit")
    histories = [_candidate_commits(root, treeish, path) for path in sorted(paths)]
    common = set(histories[0]).intersection(*(set(history) for history in histories[1:]))
    current_entries = {path: tree[path] for path in paths}
    matches: list[str] = []
    for commit in histories[0]:
        if commit not in common:
            continue
        candidate_tree = _tree(root, commit)
        if not all(candidate_tree.get(path) == entry for path, entry in current_entries.items()):
            continue
        try:
            parent = _commit_parent(root, commit)
        except wp1.ProductionReviewError:
            continue
        if parent == base:
            matches.append(commit)
    if len(matches) != 1:
        raise _error("durable batch core/raw files were not published in one commit for current bytes and base_commit")
    return matches[0]


def _validate_ref(root: Path, tree: dict[str, tuple[str, str, str]], value: object, batch_root: str,
                  index: int) -> tuple[set[str], tuple[str, str], str, dict[str, tuple[str, str | None]]]:
    keys = ADAPTER_REF_WITH_GROUP_KEYS if isinstance(value, dict) and "group_manifest_path" in value else ADAPTER_REF_KEYS
    ref = _exact(value, keys, f"adapter ref {index}")
    contract = _nonempty(ref["contract"], "adapter ref contract")
    candidate_identity = _sha(ref["candidate_identity"], "adapter ref candidate_identity")
    raws: dict[str, bytes] = {}
    for path_key, hash_key in (("input_path", "input_sha256"), ("output_path", "output_sha256")):
        path = _nonempty(ref[path_key], f"adapter ref {path_key}")
        if not path.startswith(batch_root + "/raw/") or ".." in Path(path).parts:
            raise _error("adapter ref escapes its bounded raw evidence tree")
        raw = _ordinary_blob(root, tree, path)
        digest = _sha(ref[hash_key], f"adapter ref {hash_key}")
        if hashlib.sha256(raw).hexdigest() != digest:
            raise _error("adapter raw evidence hash mismatch")
        raws[path_key] = raw
    if "group_manifest_path" in ref:
        group_path = _nonempty(ref["group_manifest_path"], "adapter group manifest path")
        if not group_path.startswith(batch_root + "/raw/") or ".." in Path(group_path).parts:
            raise _error("adapter group manifest escapes its bounded raw evidence tree")
        group_raw = _ordinary_blob(root, tree, group_path)
        if hashlib.sha256(group_raw).hexdigest() != _sha(ref["group_manifest_sha256"], "adapter group manifest hash"):
            raise _error("adapter group manifest hash mismatch")
        raws["group_manifest_path"] = group_raw
    try:
        if contract == wp1.surface.CONTRACT:
            accepted = wp1.surface.validate_result_bytes(raws["input_path"], raws["output_path"])
        elif contract == "translation_contextual_v2":
            accepted = contextual_check.validate_result_bytes(raws["input_path"], raws["output_path"])
        else:
            raise _error("adapter ref contract is not a current accepted consumer")
    except (wp1.surface.InputError, wp1.surface.ContractError,
            contextual_check.InputError, contextual_check.ContractError) as error:
        raise _error(f"adapter raw evidence was rejected by current consumer: {error}") from error
    if accepted["candidate_identity"] != candidate_identity:
        raise _error("adapter ref candidate identity does not match accepted raw bytes")
    if contract == wp1.surface.CONTRACT:
        accepted_rows = {item["entry_revision_identity"]:
                         (item["verdict"], item.get("observation")) for item in accepted["results"]}
    else:
        accepted_rows = {item["revision_key"]:
                         (item["verdict"], item.get("observation")) for item in accepted["verdicts"]}
    referenced = {ref["input_path"], ref["output_path"]}
    if "group_manifest_path" in ref:
        referenced.add(ref["group_manifest_path"])
    return (referenced,
            (ref["input_sha256"], ref["output_sha256"]), contract, accepted_rows)


def _batch_rows(root: Path, treeish: str, manifest_path: str, catalog_manifest: dict[str, Any],
                entries_by_revision: dict[str, dict[str, Any]]) -> tuple[str, list[tuple[Any, ...]]]:
    tree = _tree(root, treeish)
    batch_root = manifest_path.rsplit("/", 1)[0]
    required = {f"{batch_root}/{name}" for name in ("manifest.json", "results.jsonl", "adjudications.jsonl", "gates.json")}
    for path, (mode, kind, _object) in tree.items():
        if path.startswith(batch_root + "/") and (mode not in {"100644", "100755"} or kind != "blob"):
            raise _error(f"batch evidence contains symlink/special entry: {path}")
        if path.startswith(batch_root + "/") and path not in required and not path.startswith(batch_root + "/raw/"):
            raise _error(f"batch evidence contains unexpected file: {path}")
    raws = {path: _ordinary_blob(root, tree, path) for path in required}
    manifest_raw = raws[f"{batch_root}/manifest.json"]
    manifest = _exact(wp1.parse_canonical_object(manifest_raw, "batch manifest"), BATCH_MANIFEST_KEYS, "batch manifest")
    _schema_one(manifest["schema_version"], "batch manifest")
    if manifest["kind"] != "production_review_v2_lite_batch_v1":
        raise _error("batch manifest kind mismatch")
    if manifest["catalog_id"] != catalog_manifest["catalog_id"] or manifest["policy_sha256"] != catalog_manifest["policy_sha256"]:
        raise _error("batch catalog/policy identity mismatch")
    batch_id = _nonempty(manifest["batch_id"], "batch_id")
    if batch_root != f"{BATCH_PREFIX}{batch_id}":
        raise _error("batch ID/path mismatch")
    if not isinstance(manifest["attempt"], int) or isinstance(manifest["attempt"], bool) or manifest["attempt"] < 0:
        raise _error("batch attempt must be a nonnegative integer")
    wp1.strict_utc_seconds(manifest["recorded_at"])
    _nonempty(manifest["recorded_by"], "recorded_by")
    for name, key in (("results.jsonl", "results_sha256"), ("adjudications.jsonl", "adjudications_sha256"),
                      ("gates.json", "gates_sha256")):
        if hashlib.sha256(raws[f"{batch_root}/{name}"]).hexdigest() != _sha(manifest[key], key):
            raise _error(f"batch {name} hash mismatch")
    revisions = manifest["ordered_revisions"]
    if not isinstance(revisions, list) or not revisions or len(revisions) != len(set(revisions)):
        raise _error("batch ordered revisions must be a nonempty unique array")
    if hashlib.sha256(wp1.canonical_bytes(revisions)).hexdigest() != manifest["ordered_revisions_sha256"]:
        raise _error("batch ordered revisions hash mismatch")
    try:
        snapshots = [entries_by_revision[revision] for revision in revisions]
    except (KeyError, TypeError) as error:
        raise _error("batch ordered revision is not in the current catalog") from error
    if hashlib.sha256(wp1.canonical_bytes(snapshots)).hexdigest() != manifest["entry_snapshots_sha256"]:
        raise _error("batch entry snapshot hash mismatch")
    refs = manifest["adapter_refs"]
    if not isinstance(refs, list) or not refs:
        raise _error("batch adapter_refs must be a nonempty array")
    referenced_raw: set[str] = set()
    adapter_runs: dict[tuple[str, str], tuple[str, dict[str, tuple[str, str | None]]]] = {}
    accepted_by_contract: dict[str, dict[str, tuple[str, str | None]]] = {}
    for index, ref in enumerate(refs):
        paths, pair, contract, accepted_rows = _validate_ref(root, tree, ref, batch_root, index)
        if pair in adapter_runs:
            raise _error("batch adapter refs contain a duplicate input/output hash pair")
        contract_rows = accepted_by_contract.setdefault(contract, {})
        if contract_rows.keys() & accepted_rows.keys():
            raise _error("accepted adapter runs overlap within one contract")
        contract_rows.update(accepted_rows)
        referenced_raw.update(paths)
        adapter_runs[pair] = (contract, accepted_rows)
    present_raw = {path for path in tree if path.startswith(batch_root + "/raw/")}
    if present_raw != referenced_raw:
        raise _error("batch raw evidence set does not exactly match adapter refs")
    commit = _publication_commit(root, treeish, tree, required | referenced_raw,
                                 manifest["base_commit"])
    # Replay is a derivation, not a trust decision: surface is the ordered
    # authority for the batch, deep is exactly its ISSUE projection, and no
    # contextual-only or surface-OK-plus-blocked conclusion is representable.
    surface_rows = accepted_by_contract.get(wp1.surface.CONTRACT, {})
    deep_rows = accepted_by_contract.get("translation_contextual_v2", {})
    if set(surface_rows) != set(revisions):
        raise _error("accepted surface membership/verdict set does not exactly equal ordered revisions")
    expected_deep = [revision for revision in revisions if surface_rows[revision][0] == "ISSUE"]
    if set(deep_rows) != set(expected_deep):
        raise _error("accepted contextual membership/verdict set does not exactly equal surface ISSUE set")
    if set().union(*(rows.keys() for rows in accepted_by_contract.values())) != set(revisions):
        raise _error("accepted adapter run revision union does not equal ordered revisions")
    results = wp1.parse_jsonl(raws[f"{batch_root}/results.jsonl"], "batch results")
    if len(results) != len(revisions):
        raise _error("batch result/revision count mismatch")
    adjudications = wp1.parse_jsonl(raws[f"{batch_root}/adjudications.jsonl"], "batch adjudications")
    adjud_by_revision: dict[str, list[dict[str, Any]]] = {}
    adjud_by_observation: set[str] = set()
    legacy_adjudication_seen = False
    for index, value in enumerate(adjudications):
        # Read older contextual-only publications while requiring the same
        # exact observation binding in the normalized replay representation.
        legacy_compat = isinstance(value, dict) and "observation_identity" not in value
        legacy_adjudication_seen = legacy_adjudication_seen or legacy_compat
        if legacy_compat and set(value) == ADJUDICATION_KEYS - {"observation_identity", "observation_contract"}:
            revision_value = value.get("entry_revision_identity")
            accepted = accepted_by_contract.get("translation_contextual_v2", {}).get(revision_value)
            if accepted is not None:
                value = dict(value)
                value["observation_contract"] = "translation_contextual_v2"
                value["observation_identity"] = catalog.observation_identity(
                    "translation_contextual_v2", revision_value,
                    accepted[0], accepted[1])
        row = _exact(value, ADJUDICATION_KEYS, f"batch adjudication {index}")
        _schema_one(row["schema_version"], f"batch adjudication {index}")
        revision = _sha(row["entry_revision_identity"], "adjudication revision identity")
        if revision not in revisions:
            raise _error("adjudications must belong to this batch")
        contract = row["observation_contract"]
        if contract not in {wp1.surface.CONTRACT, "translation_contextual_v2"}:
            raise _error("adjudication observation contract is not accepted")
        accepted_value = accepted_by_contract.get(contract, {}).get(revision)
        if accepted_value is None:
            raise _error("adjudication has no accepted observation")
        expected_observation_identity = catalog.observation_identity(
            contract, revision, accepted_value[0], accepted_value[1])
        if row["observation_identity"] != expected_observation_identity or row["observation_identity"] in adjud_by_observation:
            raise _error("adjudication does not exactly bind a unique observation")
        adjud_by_observation.add(row["observation_identity"])
        accepted_observation = accepted_by_contract.get(contract, {}).get(revision)
        # The named contract is the observation authority.  A surface ISSUE
        # and a contextual ISSUE for one revision are distinct observations,
        # even when their text happens to be equal, and each must bind its own
        # value/hash pair.
        if (accepted_observation is None or accepted_observation[0] != "ISSUE" or
                row["observation_sha256"] != hashlib.sha256(
                    (accepted_observation[1] or "").encode("utf-8")).hexdigest()):
            raise _error("adjudication does not exactly bind its named contract ISSUE")
        if row["disposition"] not in {"confirmed", "pending", "advisory", "refuted"} or type(row["repair_required"]) is not bool:
            raise _error("invalid durable adjudication")
        if row["disposition"] != "confirmed" and row["repair_required"]:
            raise _error("only confirmed durable adjudications may require repair")
        if row["disposition"] == "confirmed":
            try:
                evidence.validate_source_evidence(root, row["evidence_path"],
                                                  row["evidence_commit"], row["evidence_snapshot"],
                                                  # Only the legacy row shape may
                                                  # carry a descriptive snapshot
                                                  # annotation.  Current named
                                                  # observations require bytes in
                                                  # both active import and replay.
                                                  allow_legacy_annotation=legacy_compat)
            except (wp1.ProductionReviewError, ValueError, TypeError) as error:
                raise _error(f"confirmed source evidence rejected: {error}") from error
        adjud_by_revision.setdefault(revision, []).append(row)
    observation_records: list[dict[str, Any]] = []
    expected_observations = set()
    for contract, values in accepted_by_contract.items():
        for revision, (verdict, observation) in values.items():
            if verdict == "ISSUE":
                identity = catalog.observation_identity(
                    contract, revision, verdict, observation)
                observation_records.append({
                    "contract": contract,
                    "entry_revision_identity": revision,
                    "verdict": verdict,
                    "observation": observation,
                    "observation_identity": identity,
                })
                expected_observations.add(identity)
    # The active producer always names every current-contract observation.
    # Only old durable rows may use the narrow contextual-only compatibility
    # path; normalize those rows before applying the shared fold.
    all_decisions = [row for rows in adjud_by_revision.values() for row in rows]
    if not legacy_adjudication_seen:
        required_observations = expected_observations
        fold_observations = observation_records
    else:
        required_observations = {
            row["observation_identity"] for row in all_decisions
            if row.get("observation_contract") == "translation_contextual_v2"}
        fold_observations = [observation for observation in observation_records
                             if observation["observation_identity"] in required_observations]
    if adjud_by_observation != required_observations:
        raise _error("adjudications must exactly cover every surface/contextual ISSUE observation")
    folded_states = catalog.fold_issue_observations(
        fold_observations, all_decisions)
    output: list[tuple[Any, ...]] = []
    observed: list[str] = []
    for index, value in enumerate(results):
        row = _exact(value, RESULT_KEYS, f"batch result {index}")
        _schema_one(row["schema_version"], f"batch result {index}")
        if row["final_state"] not in DURABLE_STATES:
            raise _error("batch result has nonterminal durable state")
        revision = _sha(row["entry_revision_identity"], "result revision identity")
        entry = entries_by_revision.get(revision)
        if entry is None:
            raise _error("batch result revision is not in current catalog")
        for result_key, entry_key in (("source", "source"), ("target", "target"), ("source_tag", "source_tag"),
                ("normalized_path", "normalized_path"), ("call_locator", "call_locator"),
                ("logical_entry_identity", "logical_entry_identity"), ("entry_revision_identity", "entry_revision_identity")):
            if row[result_key] != entry[entry_key]:
                raise _error(f"batch result catalog mismatch: {result_key}")
        result_pair = (_sha(row["input_sha256"], "result input hash"),
                       _sha(row["output_sha256"], "result output hash"))
        run = adapter_runs.get(result_pair)
        if run is None:
            raise _error("batch result input/output hashes are not bound to an accepted adapter ref")
        contract, accepted_rows = run
        if revision not in accepted_rows:
            raise _error("batch result revision is not a member of its accepted adapter run")
        contract_fields = (
            (wp1.surface.CONTRACT, "surface_verdict", "surface_observation"),
            ("translation_contextual_v2", "deep_verdict", "deep_observation"),
        )
        for field_contract, verdict_key, observation_key in contract_fields:
            accepted_result = accepted_by_contract.get(field_contract, {}).get(revision)
            durable_result = (row[verdict_key], row[observation_key])
            if accepted_result is None:
                if durable_result != (None, None):
                    raise _error("batch result has verdict/observation without an accepted contract run")
            elif durable_result != accepted_result:
                raise _error("batch result verdict/observation does not match accepted consumer result")
        expected_level = "deep_reviewed" if revision in deep_rows else "surface_only"
        if row["completion_level"] != expected_level:
            raise _error("batch result completion level is not derived from accepted authority")
        deep_value = accepted_by_contract.get("translation_contextual_v2", {}).get(revision)
        surface_value = accepted_by_contract.get(wp1.surface.CONTRACT, {}).get(revision)
        if surface_value and surface_value[0] == "ISSUE":
            # The surface observation remains authoritative even when the
            # contextual result for the same revision is OK.
            expected_state = folded_states.get(revision)
            if expected_state is None:
                raise _error("durable surface ISSUE lacks observation adjudication")
        elif deep_value and deep_value[0] == "OK":
            expected_state = "done"
        elif deep_value and deep_value[0] == "ISSUE":
            expected_state = folded_states.get(revision)
            if expected_state is None:
                raise _error("durable ISSUE lacks observation adjudication")
        elif surface_value and surface_value[0] == "OK":
            expected_state = "done"
        else:
            raise _error("durable result is not resolved by accepted observations")
        if row["final_state"] != expected_state:
            raise _error("durable final state is not derived from accepted observations/adjudication")
        observed.append(revision)
        output.append((revision, row["logical_entry_identity"], row["final_state"], batch_id,
                       manifest["attempt"], hashlib.sha256(wp1.canonical_bytes(row)).hexdigest(), manifest["recorded_at"]))
    if observed != revisions:
        raise _error("batch result order does not match ordered revisions")
    gates = wp1.parse_canonical_object(raws[f"{batch_root}/gates.json"], "batch gates")
    if isinstance(gates, dict) and type(gates.get("schema_version")) is int and gates["schema_version"] == 2:
        from . import gate_results
        if set(gates) != {"schema_version", "result", "prospective_bytes", "committed_bytes"}:
            raise _error("batch gates v2 exact schema mismatch")
        try:
            gate_results.validate_historical(gates["result"], selected=gate_results.candidate(
                manifest["batch_id"], manifest["catalog_id"], manifest["base_commit"],
                manifest["policy_sha256"], revisions))
        except ValueError as error:
            raise _error(f"batch gates v2 invalid: {error}") from error
        if any(type(gates[key]) is not int or not 0 <= gates[key] <= catalog.TRACKED_LIMIT
               for key in ("prospective_bytes", "committed_bytes")):
            raise _error("batch gates exceed the combined 128 MiB production budget")
    else:
        if not isinstance(gates, dict) or set(gates) not in ({"schema_version", "commands"}, {"schema_version", "commands", "prospective_bytes", "committed_bytes"}):
            raise _error("batch gates exact schema mismatch")
        _schema_one(gates["schema_version"], "batch gates")
        commands = gates["commands"]
        if not isinstance(commands, list):
            raise _error("batch gates commands must be an array")
        gate_keys = {"command", "version", "exit_code", "output_sha256"}
        if any(not isinstance(item, dict) or set(item) != gate_keys or
               not isinstance(item["command"], str) or not item["command"] or
               not isinstance(item["version"], str) or not item["version"] or
               type(item["exit_code"]) is not int or item["exit_code"] != 0 or
               not isinstance(item["output_sha256"], str) or
               not wp1.SHA256_RE.fullmatch(item["output_sha256"])
               for item in commands):
            raise _error("batch gates must contain successful recorded commands")
        # Older committed fixtures had no gate records and no occupancy fields;
        # retain that narrow replay compatibility.  Active producer output always
        # has at least one actual command and the budget fields.
        if "prospective_bytes" in gates and not commands:
            raise _error("active batch gates must record actual applicable commands")
        if "prospective_bytes" in gates:
            if (type(gates["prospective_bytes"]) is not int or
                    type(gates["committed_bytes"]) is not int or
                    gates["prospective_bytes"] < 0 or gates["committed_bytes"] < 0 or
                    gates["prospective_bytes"] > catalog.TRACKED_LIMIT or
                    gates["committed_bytes"] > catalog.TRACKED_LIMIT):
                raise _error("batch gates exceed the combined 128 MiB production budget")
            if "tools/ci-gates.sh" in tree:
                command_names = {item["command"] for item in commands}
                if not any("tools/ci-gates.sh" in command for command in command_names):
                    raise _error("active batch gates must record the full tools/ci-gates.sh gate")
                if all(path in tree for path in (
                        "tests/i18n/test_surface_screen_manifest.py",
                        "tests/i18n/test_surface_screen_result_check.py",
                        "tests/i18n/test_contextual_result_check.py")):
                    if not any("test_surface_screen_manifest.py" in command and
                               "test_surface_screen_result_check.py" in command and
                               "test_contextual_result_check.py" in command
                               for command in command_names):
                        raise _error("active batch gates must record current-consumer checks")
    return commit, output


def _projection(root: Path, treeish: str) -> tuple[str, dict[str, Any], list[dict[str, Any]], list[tuple[Any, ...]], list[tuple[Any, ...]]]:
    with git_evidence_reader.projection_scope(root):
        return _projection_contents(root, treeish)


def _projection_contents(root: Path, treeish: str) -> tuple[str, dict[str, Any], list[dict[str, Any]], list[tuple[Any, ...]], list[tuple[Any, ...]]]:
    evidence_head = _head(root, treeish)
    manifest, entries, _files = _catalog_from_tree(root, evidence_head)
    tree = _tree(root, evidence_head)
    batch_paths = sorted(path for path in tree if path.startswith(BATCH_PREFIX))
    batch_roots = {"/".join(path.split("/")[:4]) for path in batch_paths}
    all_manifests = sorted(f"{batch_root}/manifest.json" for batch_root in batch_roots)
    if any(path not in tree for path in all_manifests):
        raise _error("batch evidence tree has files without a manifest")
    # A catalog boundary leaves old, committed batches in Git for diagnosis.
    # They remain valid evidence, but only an exact unchanged mapping may
    # carry a durable state to the current revision.  Validate every current
    # migration against the catalog bytes at its publication boundary before
    # composing the unique linear chain used for historical batches.
    from . import production_review_v2_lite_migration as migration
    migration_edges = _validated_migration_edges(root, tree, evidence_head)
    matching_edges = [edge for edge in migration_edges
                      if edge["value"]["new_catalog_id"] == manifest["catalog_id"]]
    if len(matching_edges) > 1:
        raise _error("more than one migration boundary targets the current catalog")
    reconciliation = migration.reconciliation_rows_for_tree(root, tree, manifest, entries)
    batch_records: list[tuple[str, dict[str, Any], dict[str, Any], list[dict[str, Any]]]] = []
    for path in all_manifests:
        batch_root = path.rsplit("/", 1)[0]
        required = {f"{batch_root}/{name}" for name in
                    ("manifest.json", "results.jsonl", "adjudications.jsonl", "gates.json")}
        for candidate_path, (mode, kind, _object) in tree.items():
            if not candidate_path.startswith(batch_root + "/"):
                continue
            if mode not in {"100644", "100755"} or kind != "blob":
                raise _error(f"batch evidence contains symlink/special entry: {candidate_path}")
            if candidate_path not in required and not candidate_path.startswith(batch_root + "/raw/"):
                raise _error(f"batch evidence contains unexpected file: {candidate_path}")
        value = _exact(wp1.parse_canonical_object(_ordinary_blob(root, tree, path), "batch manifest"),
                       BATCH_MANIFEST_KEYS, "batch manifest")
        _schema_one(value["schema_version"], "historical batch manifest")
        if value["kind"] != "production_review_v2_lite_batch_v1":
            raise _error("historical batch manifest kind mismatch")
        if not isinstance(value.get("catalog_id"), str) or not value["catalog_id"]:
            raise _error("historical batch manifest has no catalog identity")
        if value.get("batch_id") != batch_root.rsplit("/", 1)[-1]:
            raise _error("historical batch ID/path mismatch")
        for name, key in (("results.jsonl", "results_sha256"),
                          ("adjudications.jsonl", "adjudications_sha256"),
                          ("gates.json", "gates_sha256")):
            raw = _ordinary_blob(root, tree, f"{batch_root}/{name}")
            if hashlib.sha256(raw).hexdigest() != _sha(value[key], key):
                raise _error(f"historical batch {name} hash mismatch")
        try:
            # Always validate the batch against the catalog at its own
            # base_commit.  The current catalog may be a later boundary, and
            # parsing old result rows against it can silently manufacture or
            # discard durable conclusions.
            source_manifest, source_entries, _source_files = _catalog_from_tree(root, value["base_commit"])
        except wp1.ProductionReviewError as error:
            raise _error(f"cannot validate historical batch catalog: {error}") from error
        if source_manifest["catalog_id"] != value["catalog_id"]:
            raise _error("historical batch base commit does not name its catalog")
        batch_records.append((path, value, source_manifest, source_entries))
    topo = _git(root, "rev-list", "--topo-order", "--reverse", evidence_head).decode("ascii").splitlines()
    order = {commit: index for index, commit in enumerate(topo)}
    candidates: list[tuple[int, bytes, str, tuple[Any, ...]]] = []
    by_revision = {row["entry_revision_identity"]: row for row in entries}
    for path, batch_manifest, source_manifest, source_entries in batch_records:
        source_by_revision = {row["entry_revision_identity"]: row for row in source_entries}
        commit, source_rows = _batch_rows(root, evidence_head, path, source_manifest, source_by_revision)
        chain = _migration_chain(root, migration_edges, source_manifest["catalog_id"],
                                 manifest["catalog_id"])
        # A changed/ambiguous/unmapped row is deliberately not carried across
        # the chain.  Its current successor remains implicit queued; no
        # durable state is guessed from an old revision.
        rows = _unchanged_rows_through_chain(source_rows, chain, set(by_revision))
        for row in rows:
            if row[0] not in by_revision:
                raise _error("historical durable result mapped outside the current catalog")
            candidates.append((order[commit], path.encode("utf-8").lower(), commit, row))
    candidates.sort(key=lambda item: (item[0], item[1]))
    winners: dict[str, tuple[int, bytes, str, tuple[Any, ...]]] = {}
    for candidate in candidates:
        revision = candidate[3][0]
        prior = winners.get(revision)
        if prior is not None and prior[0:2] == candidate[0:2] and prior[3] != candidate[3]:
            raise _error("incompatible duplicate durable conclusions")
        winners[revision] = candidate
    overrides = [item[3] for item in sorted(winners.values(), key=lambda item: item[3][0])]
    return evidence_head, manifest, entries, overrides, reconciliation


def _connect(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute("PRAGMA busy_timeout=0")
    return connection


def _create_database(path: Path, evidence_head: str, manifest: dict[str, Any], overrides: list[tuple[Any, ...]],
                     reconciliation: list[tuple[Any, ...]]) -> None:
    connection = None
    try:
        connection = _connect(path)
        with connection:
            mode = connection.execute("PRAGMA journal_mode=WAL").fetchone()[0]
            if str(mode).lower() != "wal":
                raise _error("SQLite WAL mode could not be enabled")
            connection.execute(META_SQL); connection.execute(STATE_SQL); connection.execute(RECONCILIATION_SQL)
            connection.execute("INSERT INTO meta VALUES (1,1,?,?,?)",
                               (manifest["catalog_id"], evidence_head, catalog.utc_now()))
            connection.executemany("INSERT INTO state_override VALUES (?,?,?,?,?,?,?)", overrides)
            connection.executemany("INSERT INTO reconciliation VALUES (?,?,?,?,?,?,?)", reconciliation)
        connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    except (OSError, sqlite3.Error) as error:
        raise _error(f"cannot build queue database: {error}") from error
    finally:
        if connection is not None:
            connection.close()
    try:
        with path.open("rb") as handle:
            os.fsync(handle.fileno())
    except OSError as error:
        raise _error(f"cannot fsync queue database: {error}") from error


def _schema_check(connection: sqlite3.Connection) -> None:
    objects = connection.execute("SELECT type,name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
    observed = {(name, sql) for kind, name, sql in objects if kind == "table"}
    if observed != set(EXPECTED_SCHEMA.items()) or any(kind != "table" for kind, _name, _sql in objects):
        raise _error("queue database schema drift")
    if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        raise _error("queue database foreign keys are disabled")
    if str(connection.execute("PRAGMA journal_mode").fetchone()[0]).lower() != "wal":
        raise _error("queue database is not in WAL mode")
    if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok" or \
            connection.execute("PRAGMA foreign_key_check").fetchall():
        raise _error("queue database integrity check failed")


def _check_projection(root: Path, treeish: str,
                      expected: tuple[str, dict[str, Any], list[dict[str, Any]], list[tuple[Any, ...]], list[tuple[Any, ...]]] | None = None,
                      *, database: Path | None = None, active_writer: bool | None = None) -> dict[str, Any]:
    evidence_head, manifest, entries, overrides, reconciliation = expected or _projection(root, treeish)
    path = database or database_path(root)
    connection = None
    try:
        if path.is_symlink() or not stat.S_ISREG(path.lstat().st_mode):
            raise _error("queue database is missing or not an ordinary file")
        connection = _connect(path)
        _schema_check(connection)
        meta = connection.execute("SELECT * FROM meta").fetchall()
        if len(meta) != 1 or meta[0][0:4] != (1, 1, manifest["catalog_id"], evidence_head):
            raise _error("queue database meta/catalog/evidence-head drift")
        wp1.strict_utc_seconds(meta[0][4])
        actual_overrides = connection.execute("SELECT * FROM state_override ORDER BY entry_revision_identity").fetchall()
        actual_reconciliation = connection.execute("SELECT * FROM reconciliation ORDER BY migration_id,old_entry_revision_identity").fetchall()
    except FileNotFoundError as error:
        raise _error("queue database is missing; run queue init or rebuild") from error
    except sqlite3.Error as error:
        raise _error(f"cannot check queue database: {error}") from error
    finally:
        if connection is not None:
            connection.close()
    catalog_ids = {row["entry_revision_identity"] for row in entries}
    if any(row[0] not in catalog_ids for row in actual_overrides):
        raise _error("queue database contains override not present in current catalog")
    if actual_overrides != overrides or actual_reconciliation != reconciliation:
        # An active batch intentionally projects uncommitted reservations or
        # accepted surface results into SQLite before Git evidence exists.
        # Validate that projection structurally belongs to the current catalog;
        # the active checkpoint owns the detailed reconciliation.
        checkpoint = checkpoint_path(root)
        if not checkpoint.exists() or any(row[3] is None for row in actual_overrides):
            raise _error("queue database state/evidence projection drift")
    counts = dict(sorted(Counter(row[2] for row in actual_overrides).items()))
    return {"catalog_id": manifest["catalog_id"], "evidence_head": evidence_head,
            "explicit_overrides": counts, "implicit_queued": len(entries) - len(actual_overrides),
            "reconciliation_count": len(actual_reconciliation),
            "active_writer": writer_active(root) if active_writer is None else active_writer, "ok": True}


def _fallback_report(root: Path,
                     projection: tuple[str, dict[str, Any], list[dict[str, Any]], list[tuple[Any, ...]], list[tuple[Any, ...]]],
                     *, active_writer: bool) -> dict[str, Any]:
    evidence_head, manifest, entries, overrides, reconciliation = projection
    path = database_path(root)
    try:
        database_present = stat.S_ISREG(path.lstat().st_mode) and not path.is_symlink()
    except FileNotFoundError:
        database_present = False
    except OSError as error:
        raise _error(f"cannot inspect queue database: {error}") from error
    return {"catalog_id": manifest["catalog_id"], "evidence_head": evidence_head,
            "explicit_overrides": dict(sorted(Counter(row[2] for row in overrides).items())),
            "implicit_queued": len(entries) - len(overrides), "reconciliation_count": len(reconciliation),
            "active_writer": active_writer, "database_present": database_present, "ok": False}


def _replace(root: Path, projection: tuple[str, dict[str, Any], list[dict[str, Any]], list[tuple[Any, ...]], list[tuple[Any, ...]]]) -> dict[str, Any]:
    evidence_head, manifest, _entries, overrides, reconciliation = projection
    destination = database_path(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=".queue.sqlite3.", dir=destination.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    rollback: Path | None = None
    rollback_sidecars: dict[Path, Path] = {}
    replaced = False
    try:
        temporary.unlink()
        _create_database(temporary, evidence_head, manifest, overrides, reconciliation)
        _check_projection(root, evidence_head, projection, database=temporary)
        Path(str(temporary) + "-wal").unlink(missing_ok=True)
        Path(str(temporary) + "-shm").unlink(missing_ok=True)
        if destination.exists() or destination.is_symlink():
            # Preserve the old inode and its WAL/SHM as one rollback unit.
            # Deleting sidecars before the replacement can destroy committed
            # state that is still visible only through WAL.
            for sidecar in (Path(str(destination) + "-wal"), Path(str(destination) + "-shm")):
                if sidecar.exists() or sidecar.is_symlink():
                    backup = sidecar.with_name(sidecar.name + ".rollback")
                    backup.unlink(missing_ok=True)
                    os.replace(sidecar, backup)
                    rollback_sidecars[sidecar] = backup
            rollback_fd, rollback_name = tempfile.mkstemp(prefix=".queue.sqlite3.rollback.", dir=destination.parent)
            os.close(rollback_fd)
            rollback = Path(rollback_name)
            rollback.unlink()
            os.replace(destination, rollback)
        os.replace(temporary, destination)
        replaced = True
        wp1._fsync_directory(destination.parent)
        report = _check_projection(root, evidence_head, projection)
        if rollback is not None:
            rollback.unlink()
            rollback = None
            for backup in rollback_sidecars.values():
                backup.unlink(missing_ok=True)
            rollback_sidecars.clear()
            wp1._fsync_directory(destination.parent)
        return report
    except Exception as original:
        try:
            temporary.unlink(missing_ok=True)
            Path(str(temporary) + "-wal").unlink(missing_ok=True)
            Path(str(temporary) + "-shm").unlink(missing_ok=True)
            if rollback is not None and (rollback.exists() or rollback.is_symlink()):
                if replaced:
                    destination.unlink(missing_ok=True)
                    Path(str(destination) + "-wal").unlink(missing_ok=True)
                    Path(str(destination) + "-shm").unlink(missing_ok=True)
                os.replace(rollback, destination)
                rollback = None
                for sidecar, backup in rollback_sidecars.items():
                    sidecar.unlink(missing_ok=True)
                    if backup.exists() or backup.is_symlink():
                        os.replace(backup, sidecar)
                rollback_sidecars.clear()
                wp1._fsync_directory(destination.parent)
            elif replaced:
                destination.unlink(missing_ok=True)
                wp1._fsync_directory(destination.parent)
        except OSError as rollback_error:
            raise _error(f"queue rollback failed after {type(original).__name__}: {rollback_error}") from rollback_error
        raise


def init(root: Path) -> dict[str, Any]:
    with writer_lock(root):
        if database_path(root).exists() or database_path(root).is_symlink():
            raise _error("queue database already exists; use queue rebuild")
        _no_checkpoint(root); _clean_evidence(root)
        projection = _projection(root, "HEAD")
        return _replace(root, projection)


def rebuild(root: Path, *, treeish: str = "HEAD") -> dict[str, Any]:
    with writer_lock(root):
        _no_checkpoint(root); _clean_evidence(root)
        projection = _projection(root, treeish)
        return _replace(root, projection)


def strict_check(root: Path, *, treeish: str = "HEAD") -> dict[str, Any]:
    """Check the exact projection; never turn a failure into an active-writer report.

    Writer preflight uses this entry point while holding the lock.  The public
    read-only check may still report a concurrent writer, but a writer must
    never proceed on that degraded answer.
    """
    _clean_evidence(root)
    projection = _projection(root, treeish)
    return _check_projection(root, treeish, projection, active_writer=True)


def check(root: Path, *, treeish: str = "HEAD") -> dict[str, Any]:
    active = writer_active(root)
    _clean_evidence(root)
    projection = _projection(root, treeish)
    try:
        return _check_projection(root, treeish, projection, active_writer=active)
    except wp1.ProductionReviewError:
        if not active:
            raise
        return _fallback_report(root, projection, active_writer=True)


def status(root: Path, *, treeish: str = "HEAD", allow_missing: bool = False) -> dict[str, Any]:
    active = writer_active(root)
    _clean_evidence(root)
    projection = _projection(root, treeish)
    try:
        return _check_projection(root, treeish, projection, active_writer=active)
    except wp1.ProductionReviewError:
        if not (allow_missing or active):
            raise
        return _fallback_report(root, projection, active_writer=active)


def _tree_id(root: Path, commit: str) -> str:
    value = _git(root, "rev-parse", f"{commit}^{{tree}}").decode("ascii").strip()
    if len(value) != 40 or any(ch not in "0123456789abcdef" for ch in value):
        raise _error("queue Git tree is not a lowercase Git tree")
    return value


def _is_ancestor(root: Path, ancestor: str, descendant: str) -> None:
    try:
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except OSError as error:
        raise _error(f"cannot validate migration ancestry: {error}") from error
    if result.returncode != 0:
        raise _error("migration boundaries are not on one linear Git history")


def _migration_publication_commit(root: Path, tree: dict[str, tuple[str, str, str]],
                                  treeish: str, path: str, value: dict[str, Any]) -> str:
    """Locate the one commit publishing the current migration blob.

    A migration's ``base_commit`` is the parent of its publication commit.
    Requiring both the current blob and that parent prevents a copied or
    replayed artifact from silently acting as a different boundary.
    """
    current_entry = tree.get(path)
    if current_entry is None:
        raise _error(f"migration artifact disappeared from the current Git tree: {path}")
    try:
        raw = _git(root, "log", "--full-history", "--format=%H", "--diff-filter=AM",
                   treeish, "--", path)
        commits = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise _error(f"cannot parse migration publication history for {path}") from error
    matches: list[str] = []
    for commit in commits:
        candidate_tree = _tree(root, commit)
        if candidate_tree.get(path) != current_entry:
            continue
        try:
            parent = _commit_parent(root, commit)
        except wp1.ProductionReviewError:
            continue
        if parent == value["base_commit"]:
            matches.append(commit)
    if len(matches) != 1:
        raise _error("migration artifact does not have one committed publication boundary")
    return matches[0]


def _validated_migration_edges(root: Path, tree: dict[str, tuple[str, str, str]],
                               treeish: str) -> list[dict[str, Any]]:
    """Validate every current migration and bind it to its Git boundary."""
    from . import production_review_v2_lite_migration as migration

    edges: list[dict[str, Any]] = []
    for path in sorted(tree):
        if not path.startswith(MIGRATION_PREFIX) or not path.endswith(".json"):
            continue
        relative = path[len(MIGRATION_PREFIX):]
        if not relative or "/" in relative:
            raise _error("migration evidence path is not a direct canonical file")
        raw = _ordinary_blob(root, tree, path)
        value = migration._validate_migration_record(
            wp1.parse_canonical_object(raw, "migration"), target_path=path)
        old_manifest, old_entries, old_files = _catalog_from_tree(root, value["base_commit"])
        if _tree_id(root, value["base_commit"]) != value["base_tree"]:
            raise _error("migration base tree no longer names its base commit")
        if old_manifest["catalog_id"] != value["old_catalog_id"]:
            raise _error("migration base catalog identity drift")
        if hashlib.sha256(old_files[f"{catalog.CATALOG_PREFIX}/manifest.json"]).hexdigest() != value["old_manifest_sha256"]:
            raise _error("migration base catalog manifest hash drift")
        if old_manifest["entries_sha256"] != value["old_entries_sha256"]:
            raise _error("migration base catalog entries hash drift")
        if old_manifest["exclusions_sha256"] != value["old_exclusions_sha256"]:
            raise _error("migration base catalog exclusions hash drift")

        publication_commit = _migration_publication_commit(root, tree, treeish, path, value)
        new_manifest, new_entries, new_files = _catalog_from_tree(root, publication_commit)
        if new_manifest["catalog_id"] != value["new_catalog_id"]:
            raise _error("migration publication catalog identity drift")
        if hashlib.sha256(new_files[f"{catalog.CATALOG_PREFIX}/manifest.json"]).hexdigest() != value["new_manifest_sha256"]:
            raise _error("migration publication catalog manifest hash drift")
        if new_manifest["entries_sha256"] != value["new_entries_sha256"]:
            raise _error("migration publication catalog entries hash drift")
        if new_manifest["exclusions_sha256"] != value["new_exclusions_sha256"]:
            raise _error("migration publication catalog exclusions hash drift")
        normalized = migration.validate_migration(
            value, expected_old_entries=old_entries, expected_new_entries=new_entries)
        edges.append({"value": normalized, "path": path,
                      "publication_commit": publication_commit,
                      "old_manifest": old_manifest, "old_entries": old_entries,
                      "new_manifest": new_manifest, "new_entries": new_entries,
                      "rows_by_old": {row["old_entry_revision_identity"]: row
                                      for row in normalized["rows"]}})
    return edges


def _migration_chain(root: Path, edges: list[dict[str, Any]], source_catalog_id: str,
                     current_catalog_id: str) -> list[dict[str, Any]]:
    """Return the unique exact catalog path, or fail closed."""
    if source_catalog_id == current_catalog_id:
        return []
    by_old: dict[str, list[dict[str, Any]]] = {}
    for edge in edges:
        value = edge["value"]
        by_old.setdefault(value["old_catalog_id"], []).append(edge)
    chain: list[dict[str, Any]] = []
    visited = {source_catalog_id}
    current = source_catalog_id
    while current != current_catalog_id:
        choices = by_old.get(current, [])
        if not choices:
            raise _error("missing committed migration link to the current catalog")
        if len(choices) != 1:
            raise _error("forked or ambiguous committed migration link")
        edge = choices[0]
        value = edge["value"]
        next_catalog = value["new_catalog_id"]
        if next_catalog in visited:
            raise _error("committed migration chain contains a catalog cycle")
        if chain:
            _is_ancestor(root, chain[-1]["publication_commit"], value["base_commit"])
        chain.append(edge)
        visited.add(next_catalog)
        current = next_catalog
    return chain


def _unchanged_rows_through_chain(source_rows: list[tuple[Any, ...]],
                                  chain: list[dict[str, Any]],
                                  current_revisions: set[str]) -> list[tuple[Any, ...]]:
    """Carry durable rows only across exact unchanged identity links."""
    if not chain:
        return [row for row in source_rows if row[0] in current_revisions]
    result: list[tuple[Any, ...]] = []
    for source_row in source_rows:
        revision, logical = source_row[0], source_row[1]
        retain = True
        for edge in chain:
            mapping = edge["rows_by_old"].get(revision)
            if (mapping is None or mapping["old_logical_entry_identity"] != logical or
                    mapping["disposition"] != "unchanged" or
                    mapping["new_logical_entry_identity"] != logical or
                    mapping["new_entry_revision_identity"] != revision):
                retain = False
                break
        if retain:
            if revision not in current_revisions:
                raise _error("unchanged migration row is absent from the current catalog")
            result.append(source_row)
    return result


def business_rows(path: Path) -> tuple[list[tuple[Any, ...]], list[tuple[Any, ...]], tuple[Any, ...]]:
    connection = _connect(path)
    try:
        overrides = connection.execute("SELECT * FROM state_override ORDER BY entry_revision_identity").fetchall()
        reconciliation = connection.execute("SELECT * FROM reconciliation ORDER BY migration_id,old_entry_revision_identity").fetchall()
        meta = connection.execute("SELECT singleton,schema_version,catalog_id,evidence_head FROM meta").fetchone()
        return overrides, reconciliation, meta
    finally:
        connection.close()
