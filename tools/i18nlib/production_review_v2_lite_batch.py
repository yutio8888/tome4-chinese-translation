"""Single active batch and exact current surface adapter for WP2-Lite."""
from __future__ import annotations
import copy
import hashlib, os, shutil, sqlite3, json, subprocess, stat
from collections import defaultdict
from pathlib import Path
from typing import Any
from . import production_review as wp1
from . import production_review_v2_lite as catalog
from . import production_review_v2_lite_queue as queue
from . import production_review_v2_lite_evidence as evidence
from . import gate_results
import surface_screen_result_check as surface
import surface_screen_manifest as surface_manifest
import contextual_result_check as contextual

MAX_BATCH = 80
# WP2L-3 owns only the reservation and surface adapter phases.  Later
# contextual/adjudication/commit phases belong to WP2L-4 and must fail closed.
PHASES = frozenset({"reserved", "surface_ready", "surface_collected", "deep_ready", "deep_collected", "adjudicated", "commit_ready"})
SAFE = frozenset({"reserved", "before_result_import", "before_commit"})
CONTEXTUAL_REF_KEYS = frozenset({"run_index", "contract", "input_path", "input_sha256", "output_path", "output_sha256", "validator_status", "candidate_identity", "parent_indexes", "task_id", "task_state_path", "intended_state_updates"})
CHECKPOINT_KEYS = frozenset({"schema_version", "kind", "batch_id", "catalog_id", "base_commit", "policy_sha256", "created_at", "created_by", "attempt", "selection_mode", "phase", "selected", "selected_sha256", "entry_snapshots", "surface", "contextual", "adjudications", "repair_candidates", "gates", "last_safe_boundary"})
SNAPSHOT_KEYS = frozenset(catalog.ENTRY_KEYS) | {"prior_effective_state", "row_sha256"}
SURFACE_REF_KEYS = frozenset({"run_index", "lane_index", "contract", "input_path", "input_sha256", "output_path", "output_sha256", "validator_status", "candidate_identity", "parent_indexes", "intended_state_updates", "group_manifest_path", "group_manifest_sha256"})

def _observation_identity(contract, revision, verdict, observation):
    return catalog.observation_identity(contract, revision, verdict, observation)

def _accepted_observations(checkpoint):
    """Return all ISSUE observations, including multiple observations per revision."""
    found = []
    for ref in (checkpoint.get("surface") or []):
        if ref.get("output_path"):
            result = surface.validate_result_bytes(Path(ref["input_path"]).read_bytes(), Path(ref["output_path"]).read_bytes())
            found.extend({"contract": surface.CONTRACT, "entry_revision_identity": item["entry_revision_identity"],
                          "verdict": item["verdict"], "observation": item.get("observation")} for item in result["results"] if item["verdict"] == "ISSUE")
    for ref in (checkpoint.get("contextual") or []):
        if ref.get("output_path"):
            result = contextual.validate_result_bytes(Path(ref["input_path"]).read_bytes(), Path(ref["output_path"]).read_bytes())
            found.extend({"contract": "translation_contextual_v2", "entry_revision_identity": item["revision_key"],
                          "verdict": item["verdict"], "observation": item.get("observation")} for item in result["verdicts"] if item["verdict"] == "ISSUE")
    for item in found:
        item["observation_identity"] = _observation_identity(item["contract"], item["entry_revision_identity"], item["verdict"], item["observation"])
    return found

def _err(message): return wp1.ProductionReviewError(message)
def _sha(raw): return hashlib.sha256(raw).hexdigest()
def _checkpoint_bytes(value): return wp1.canonical_bytes(value) + b"\n"


def _batch_relative(*parts):
    """Use the shared batch-relative constructor for every durable path."""
    return evidence.batch_relative_path(*parts)


def _raw_evidence_name(number, key):
    """Return the one stable filename used by raw copies and their temps."""
    stems = {"input_path": "input_path", "output_path": "output_path",
             "group_manifest_path": "group"}
    if type(number) is not int or number < 0 or key not in stems:
        raise _err("invalid raw evidence filename components")
    return f"{number:03d}-{stems[key]}.json"


def _prospective_batch_path(root, batch_id):
    relative = _batch_relative(batch_id)
    return queue.checkpoint_path(root).parent / "prospective" / Path(relative)


def _batch_id(selection_mode, selected, attempt):
    """Identity includes the retry axis, not just the selected catalog rows."""
    return "batch-" + _sha(wp1.canonical_bytes({
        "schema": "production_review_v2_lite_active_batch_v1",
        "selection_mode": selection_mode,
        "selected": selected,
        "attempt": attempt,
    }))[:20]

def _atomic(path, raw):
    """The protocol has one temp name; stale temps are not a second store."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name("." + path.name + ".tmp")
        if temporary.exists() or temporary.is_symlink():
            if temporary.is_symlink() or not temporary.is_file():
                raise OSError("atomic temporary is not an ordinary file")
            temporary.unlink()
        with temporary.open("xb") as handle:
            handle.write(raw); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, path); wp1._fsync_directory(path.parent)
    except OSError as error:
        raise _err(f"atomic checkpoint/output write failed: {error}") from error

def _load(path):
    try:
        raw = path.read_bytes()
        if not raw.endswith(b"\n") or raw != _checkpoint_bytes(wp1.parse_canonical_object(raw[:-1], "active batch checkpoint")):
            raise ValueError("checkpoint must be canonical JSON with one LF terminator")
        value = wp1.parse_canonical_object(raw[:-1], "active batch checkpoint")
    except (OSError, ValueError, UnicodeError, TypeError) as error:
        raise _err(f"invalid active batch checkpoint: {error}") from error
    if not isinstance(value, dict) or set(value) != CHECKPOINT_KEYS:
        raise _err("active batch checkpoint exact schema mismatch")
    if type(value.get("schema_version")) is not int or value["schema_version"] != 1 or value.get("kind") != "production_review_v2_lite_active_batch_v1":
        raise _err("active batch checkpoint schema/version mismatch")
    for key in ("batch_id", "catalog_id", "base_commit", "policy_sha256", "created_at", "created_by"):
        if not isinstance(value.get(key), str) or not value[key]:
            raise _err(f"active batch checkpoint {key} must be a non-empty string")
    for key in ("catalog_id", "policy_sha256", "selected_sha256"):
        if value.get(key) is not None and (not isinstance(value[key], str) or
                                           not wp1.SHA256_RE.fullmatch(value[key])):
            raise _err(f"active batch checkpoint {key} must be lowercase SHA-256")
    if not isinstance(value["base_commit"], str) or len(value["base_commit"]) != 40 or any(c not in "0123456789abcdef" for c in value["base_commit"]):
        raise _err("active batch checkpoint base_commit must be a Git commit")
    if type(value.get("attempt")) is not int or value["attempt"] < 1:
        raise _err("active batch checkpoint attempt must be positive integer")
    if value.get("selection_mode") not in {"queued", "retry_blocked"} or value.get("phase") not in PHASES or value.get("last_safe_boundary") not in SAFE:
        raise _err("active batch checkpoint phase/mode/boundary mismatch")
    expected_boundary = {"reserved": "reserved", "surface_ready": "before_result_import",
                         "surface_collected": "before_result_import", "deep_ready": "before_result_import",
                         "deep_collected": "before_result_import", "adjudicated": "before_commit",
                         "commit_ready": "before_commit"}[value["phase"]]
    if value["last_safe_boundary"] != expected_boundary:
        raise _err("active batch checkpoint phase/boundary combination is not legal")
    if any(value[key] is not None for key in ("adjudications", "repair_candidates", "gates")) and value["phase"] in {"reserved", "surface_ready", "surface_collected", "deep_ready", "deep_collected"}:
        raise _err("future checkpoint sections must be null before adjudication")
    selected = value["selected"]
    if (not isinstance(selected, list) or not 0 < len(selected) <= MAX_BATCH or
            any(not isinstance(x, str) or not wp1.SHA256_RE.fullmatch(x) for x in selected) or
            selected != list(dict.fromkeys(selected))):
        raise _err("active batch selected set must contain 1..80 unique identities")
    if _sha(wp1.canonical_bytes(selected)) != value["selected_sha256"]:
        raise _err("active batch selected hash mismatch")
    if value["batch_id"] != _batch_id(value["selection_mode"], selected, value["attempt"]):
        raise _err("active batch batch_id recomputation mismatch")
    snapshots = value["entry_snapshots"]
    if not isinstance(snapshots, list) or len(snapshots) != len(selected):
        raise _err("active batch entry snapshot count mismatch")
    for index, snapshot in enumerate(snapshots):
        if not isinstance(snapshot, dict) or set(snapshot) != SNAPSHOT_KEYS or snapshot.get("entry_revision_identity") != selected[index]:
            raise _err("active batch entry snapshot exact schema/order mismatch")
        if snapshot.get("prior_effective_state") not in {"queued", "blocked"}:
            raise _err("active batch prior_effective_state must be queued or blocked")
        row = {key: snapshot[key] for key in catalog.ENTRY_KEYS}
        if _sha(wp1.canonical_bytes(row)) != snapshot["row_sha256"]:
            raise _err("active batch entry snapshot row hash mismatch")
        if type(snapshot["schema_version"]) is not int or snapshot["schema_version"] != 1:
            raise _err("active batch snapshot schema_version mismatch")
    if value["phase"] == "reserved" and (value["surface"] is not None or value["contextual"] is not None):
        raise _err("reserved checkpoint must have null adapter sections")
    if value["surface"] is not None:
        if not isinstance(value["surface"], list) or not value["surface"]:
            raise _err("surface section must be a non-empty array or null")
        for index, ref in enumerate(value["surface"]): _validate_surface_ref(ref, index)
    elif value["phase"] in {"surface_ready", "surface_collected", "deep_ready", "deep_collected", "adjudicated", "commit_ready"}:
        raise _err("active phase requires a non-empty surface section")
    if value["contextual"] is not None:
        if not isinstance(value["contextual"], list) or not value["contextual"]:
            raise _err("contextual section must be a non-empty array or null")
        for index, ref in enumerate(value["contextual"]):
            if not isinstance(ref, dict) or set(ref) != CONTEXTUAL_REF_KEYS:
                raise _err(f"contextual ref {index} exact schema mismatch")
            if ref["contract"] != "translation_contextual_v2" or type(ref["run_index"]) is not int:
                raise _err("contextual ref contract/index mismatch")
            for key in ("input_sha256", "candidate_identity"):
                if not isinstance(ref[key], str) or not wp1.SHA256_RE.fullmatch(ref[key]):
                    raise _err("contextual ref hash mismatch")
            for key in ("output_sha256",):
                if ref[key] is not None and (not isinstance(ref[key], str) or not wp1.SHA256_RE.fullmatch(ref[key])):
                    raise _err("contextual ref output hash mismatch")
            if not isinstance(ref["parent_indexes"], list) or any(type(i) is not int or i < 0 for i in ref["parent_indexes"]):
                raise _err("contextual parent mapping mismatch")
            if not isinstance(ref["task_id"], str) or not ref["task_id"] or not isinstance(ref["task_state_path"], str) or not ref["task_state_path"]:
                raise _err("contextual task binding mismatch")
            if ref["output_path"] is not None and not isinstance(ref["output_path"], str):
                raise _err("contextual output path mismatch")
            if ref["validator_status"] not in {"prepared", "accepted"}:
                raise _err("contextual validator status mismatch")
    for key in ("surface", "contextual", "adjudications", "repair_candidates", "gates"):
        if value[key] is not None and not isinstance(value[key], (list, dict)):
            raise _err(f"active batch {key} has invalid value")
    return value

def _entries(root):
    manifest, rows, _ = queue._catalog_from_tree(root, "HEAD")
    return manifest, rows

def _effective_rows(root):
    manifest, rows = _entries(root)
    try:
        with sqlite3.connect(queue.database_path(root)) as con:
            overrides = {r[0]: r[1] for r in con.execute("SELECT entry_revision_identity,state FROM state_override")}
    except (sqlite3.Error, OSError, TypeError, ValueError) as error: raise _err(f"cannot read queue projection: {error}") from error
    return manifest, rows, overrides

def _risk(row):
    risk = row["risk"]
    ordinal = {"engine": 0, "boot": 1, "tome": 2, "example": 3, "example-realtime": 4, "addon-dev": 5, "ashes-urhrok": 6, "cults": 7, "items-vault": 8, "orcs": 9, "possessors": 10}
    return (-int(bool(risk["has_args_order"] or risk["has_special"])), -risk["component_group_size"], -int(bool(risk["component_group_last"])), ordinal.get(row["component"], 999), row["entry_revision_identity"])

def stable_selection(rows, overrides, *, retry_blocked=False, limit=MAX_BATCH):
    if not isinstance(limit, int) or isinstance(limit, bool) or not 0 <= limit <= MAX_BATCH: raise _err("batch limit must be between 0 and 80")
    candidates = [r for r in rows if overrides.get(r["entry_revision_identity"]) == "blocked"] if retry_blocked else [r for r in rows if r["entry_revision_identity"] not in overrides]
    return sorted(candidates, key=_risk)[:limit]

def _surface_entry(row):
    """Project one catalog row into the version-selected surface entry shape."""
    rules_version = row["rules_version"]
    keys = surface.entry_keys_for_rules(rules_version)
    entry = {key: row[key] for key in surface.ENTRY_KEYS}
    if rules_version == surface.IDENTITY_RULES_V2:
        risk = row.get("risk")
        if not isinstance(risk, dict) or "args_order" not in risk:
            raise _err("rules-v2 catalog row lacks its exact risk.args_order")
        entry["args_order"] = risk["args_order"]
    if set(entry) != keys:
        raise _err("surface entry projection does not match its rules-versioned shape")
    return entry

def _validate_surface_ref(ref, index):
    if not isinstance(ref, dict) or set(ref) != SURFACE_REF_KEYS:
        raise _err(f"surface ref {index} exact schema mismatch")
    if ref["contract"] != surface.CONTRACT or type(ref["run_index"]) is not int or type(ref["lane_index"]) is not int:
        raise _err("surface ref type/contract mismatch")
    for key in ("input_sha256", "candidate_identity"):
        if not isinstance(ref[key], str) or not wp1.SHA256_RE.fullmatch(ref[key]):
            raise _err("surface ref hash mismatch")
    for key in ("output_sha256", "group_manifest_sha256"):
        if ref[key] is not None and (not isinstance(ref[key], str) or not wp1.SHA256_RE.fullmatch(ref[key])):
            raise _err("surface ref hash mismatch")
    if not isinstance(ref["parent_indexes"], list) or any(type(i) is not int or i < 0 for i in ref["parent_indexes"]):
        raise _err("surface parent index mapping mismatch")
    if not isinstance(ref["input_path"], str) or not ref["input_path"]:
        raise _err("surface input path must be non-empty")
    if ref["output_path"] is not None and (not isinstance(ref["output_path"], str) or not ref["output_path"]):
        raise _err("surface output path must be a non-empty string or null")
    if ref["group_manifest_path"] is not None and (not isinstance(ref["group_manifest_path"], str) or
                                                     not ref["group_manifest_path"]):
        raise _err("surface group manifest path must be a non-empty string or null")
    updates = ref["intended_state_updates"]
    if updates is not None:
        if not isinstance(updates, dict):
            raise _err("surface intended state updates must be an object or null")
        for revision, state in updates.items():
            if (not isinstance(revision, str) or not wp1.SHA256_RE.fullmatch(revision) or
                    state not in {"screened", "deep_required"}):
                raise _err("surface intended state update has invalid identity or state")


def _validate_surface_projection(root, checkpoint, *, require_outputs):
    """Rebuild the expected runs/lanes/remap and compare every stored field."""
    snapshots = checkpoint["entry_snapshots"]
    expected_runs = partition_surface_entries(snapshots)
    refs = checkpoint.get("surface")
    if not isinstance(refs, list) or not refs:
        raise _err("surface phase requires non-empty prepared runs")
    expected_refs = []
    for run in expected_runs:
        count = len(run["entries"])
        lane_count = 1 if count <= 3 else 4
        for lane in range(lane_count):
            expected_refs.append((run["run_index"], lane, run["parent_indexes"] if lane_count == 1 else None))
    if len(refs) != len(expected_refs):
        raise _err("surface run/lane count drift")
    seen_indexes = []
    checked_groups = set()
    refs_by_run = defaultdict(list)
    for ref in refs:
        refs_by_run[ref["run_index"]].append(ref)
    for run_index, run_refs in refs_by_run.items():
        lane_count = 1 if len(expected_runs[run_index]["entries"]) <= 3 else 4
        if lane_count == 1:
            if any(ref["group_manifest_path"] is not None or ref["group_manifest_sha256"] is not None for ref in run_refs):
                raise _err("full surface refs must have null group manifest fields")
        else:
            bindings = {(ref["group_manifest_path"], ref["group_manifest_sha256"]) for ref in run_refs}
            if len(run_refs) != 4 or len(bindings) != 1 or next(iter(bindings))[0] is None:
                raise _err("four-lane surface refs require one non-null group manifest binding")
    for index, (ref, (run_index, lane_index, whole)) in enumerate(zip(refs, expected_refs)):
        _validate_surface_ref(ref, index)
        if (ref["run_index"], ref["lane_index"]) != (run_index, lane_index):
            raise _err("surface run/lane ordering drift")
        run = expected_runs[run_index]
        if whole is not None:
            expected_indexes = whole
        else:
            boundaries = surface_manifest.partition(len(run["entries"]))
            boundary = boundaries[lane_index]
            start, end = boundary["offset"], boundary["offset"] + boundary["length"]
            expected_indexes = run["parent_indexes"][start:end]
        if ref["parent_indexes"] != expected_indexes:
            raise _err("surface parent-index remap drift or duplicate lane membership")
        seen_indexes.extend(ref["parent_indexes"])
        if ref["group_manifest_path"] is not None and ref["group_manifest_path"] not in checked_groups:
            checked_groups.add(ref["group_manifest_path"])
            try:
                group_raw = Path(ref["group_manifest_path"]).read_bytes()
                if _sha(group_raw) != ref["group_manifest_sha256"]:
                    raise ValueError("surface group manifest hash drift")
                group = surface.strict_json_bytes(group_raw, label="surface group manifest")
                group_value = surface_manifest.validate_group_manifest
                # Recreate the consumer-relative .ai/task layout under the
                # ignored runtime root so the current validator can recheck
                # every lane, without touching a workspace task artifact.
                consumer_root = queue.checkpoint_path(root).parent / "consumer-recheck"
                lanes = group["payload"]["lanes"]
                group_refs = [item for item in refs if item["group_manifest_path"] == ref["group_manifest_path"]]
                for lane, lane_ref in zip(lanes, sorted(group_refs, key=lambda item: item["lane_index"])):
                    destination = consumer_root / lane["input_path"]
                    _atomic(destination, Path(lane_ref["input_path"]).read_bytes())
                payload = group["payload"]
                expected_manifest_path = f".ai/task/{payload['task_id']}/SURFACE-SCREEN-GROUP-{payload['group_id']}.json"
                group_value(group, root=consumer_root, manifest_path=expected_manifest_path)
            except (OSError, ValueError, TypeError, UnicodeError, KeyError, surface.InputError, surface.ContractError) as error:
                raise _err(f"surface group failed current validation: {error}") from error
            finally:
                shutil.rmtree(queue.checkpoint_path(root).parent / "consumer-recheck", ignore_errors=True)
        if require_outputs:
            if ref["validator_status"] != "accepted" or ref["output_path"] is None or ref["output_sha256"] is None:
                raise _err("surface_collected requires accepted non-empty output refs")
            try:
                input_raw, output_raw = Path(ref["input_path"]).read_bytes(), Path(ref["output_path"]).read_bytes()
                if _sha(input_raw) != ref["input_sha256"] or _sha(output_raw) != ref["output_sha256"]:
                    raise ValueError("surface raw hash drift")
                accepted = surface.validate_result_bytes(input_raw, output_raw)
            except (OSError, ValueError, TypeError, UnicodeError, surface.InputError, surface.ContractError) as error:
                raise _err(f"surface stored result failed current validation: {error}") from error
            if accepted["candidate_identity"] != ref["candidate_identity"]:
                raise _err("surface result candidate identity drift")
            expected_revisions = {snapshots[parent]["entry_revision_identity"] for parent in ref["parent_indexes"]}
            derived = {item["entry_revision_identity"]: ("screened" if item["verdict"] == "OK" else "deep_required") for item in accepted["results"]}
            if set(derived) != expected_revisions:
                raise _err("surface result membership does not match its lane remap")
            if not derived or ref["intended_state_updates"] != dict(sorted(derived.items())):
                raise _err("surface intended updates are not byte-exactly rederived")
        else:
            if (ref["validator_status"] != "prepared" or ref["output_path"] is not None or
                    ref["output_sha256"] is not None or ref["intended_state_updates"] is not None):
                raise _err("surface_ready requires prepared refs with null outputs and updates")
    if sorted(seen_indexes) != list(range(len(snapshots))) or len(seen_indexes) != len(set(seen_indexes)):
        raise _err("surface lane parent-index union is not exact")
    return expected_runs

def partition_surface_entries(rows):
    groups = defaultdict(list)
    for index, row in enumerate(rows): groups[(row["fixed_source_identity"], row["terminology_snapshot_sha256"], row["rules_version"])].append((index, row))
    result = []
    for ordinal, (identity, members) in enumerate(sorted(groups.items(), key=lambda item: min(x[0] for x in item[1]))):
        ordered = sorted(members, key=lambda x: x[1]["entry_revision_identity"])
        result.append({"run_index": ordinal, "identity": identity, "parent_indexes": [i for i, _ in ordered], "entries": [_surface_entry(row) for _, row in ordered]})
    if sorted(i for run in result for i in run["parent_indexes"]) != list(range(len(rows))): raise _err("surface partition is not an exact selected-set conservation")
    return result

def _payload(run):
    fixed, terminology, rules = run["identity"]
    return {"contract": surface.CONTRACT, "fixed_source_identity": fixed, "terminology_snapshot": terminology, "rules_version": rules, "rendered_briefing": "WP2-Lite surface screen; review only", "entries": run["entries"]}

def surface_payloads(checkpoint): return [_payload(run) for run in partition_surface_entries(checkpoint["entry_snapshots"])]

def surface_export(root):
    """Freeze exact full or four-lane current-consumer envelopes."""
    with queue.writer_lock(root):
        checkpoint = preflight(root)
        if checkpoint is None:
            raise _err("no active batch")
        if checkpoint["phase"] not in {"reserved", "surface_ready"}:
            raise _err("surface export is only valid before result import")
        runs = partition_surface_entries(checkpoint["entry_snapshots"])
        if checkpoint["phase"] == "surface_ready":
            # preflight validated the stored projection; preserve frozen historical
            # task paths and bytes instead of migrating an already exported batch.
            return {"batch_id": checkpoint["batch_id"], "runs": len(runs), "selected": len(checkpoint["selected"]), "ok": True}
        refs = []
        runtime = queue.checkpoint_path(root).parent / "surface"
        batch_task_id = checkpoint["batch_id"].replace("_", "-")
        for run in runs:
            # A review-only consumer task permits exactly one whole-screen stage.
            task_id = (batch_task_id if len(runs) == 1 else
                       f"{batch_task_id}-surface-{run['run_index']:03d}")
            payload = _payload(run)
            try:
                if len(run["entries"]) <= 3:
                    envelope, path_name, _ = surface_manifest.build_full(
                        payload, task_id=task_id, dispatch_id=f"full-{run['run_index']:03d}")
                    envelopes = [(path_name, envelope)]
                else:
                    _group, _group_path, envelopes = surface_manifest.build_group(
                        payload, task_id=task_id, group_id=f"group-{run['run_index']:03d}",
                        review_phase="REVIEW", cycle=0, attempt=checkpoint["attempt"],
                        dispatch_ids=[f"lane-{run['run_index']:03d}-{i}" for i in range(4)])
                group_path = group_hash = None
                if len(envelopes) > 1:
                    group_raw = surface.canonical_bytes(_group)
                    # Validate the group against the current consumer, including
                    # its exact lane paths, before freezing it in the checkpoint.
                    temporary_lane_paths = []
                    # The current consumer insists on its historical relative
                    # names.  Materialize that exact layout below our ignored
                    # runtime scratch root, never below workspace .ai/task.
                    consumer_root = runtime / "consumer"
                    try:
                        for consumer_path, envelope in envelopes:
                            expected = consumer_root / consumer_path
                            _atomic(expected, surface.canonical_bytes(envelope))
                            temporary_lane_paths.append(expected)
                        surface_manifest.validate_group_manifest(
                            _group, root=consumer_root, manifest_path=_group_path)
                    finally:
                        for expected in temporary_lane_paths:
                            expected.unlink(missing_ok=True)
                        for parent in {path.parent for path in temporary_lane_paths}:
                            while parent != root and parent.exists() and not any(parent.iterdir()):
                                parent.rmdir(); parent = parent.parent
                    group_path = runtime / f"run-{run['run_index']:03d}-group.json"
                    _atomic(group_path, group_raw)
                    group_hash = _sha(group_raw)
                for lane_index, (consumer_path, envelope) in enumerate(envelopes):
                    raw = surface.canonical_bytes(envelope)
                    path = runtime / f"run-{run['run_index']:03d}-lane-{lane_index:02d}.json"
                    _payload_value, candidate = surface.validate_envelope(
                        surface.strict_json_bytes(raw, label="surface envelope"))
                    if len(envelopes) == 1:
                        start, end = 0, len(run["entries"])
                    else:
                        boundary = surface_manifest.partition(len(run["entries"]))[lane_index]
                        start, end = boundary["offset"], boundary["offset"] + boundary["length"]
                    _atomic(path, raw)
                    refs.append({"run_index": run["run_index"], "lane_index": lane_index,
                                 "contract": surface.CONTRACT, "input_path": str(path),
                                 "input_sha256": _sha(raw), "output_path": None, "output_sha256": None,
                                 "validator_status": "prepared", "candidate_identity": candidate,
                                 "parent_indexes": run["parent_indexes"][start:end], "intended_state_updates": None,
                                 "group_manifest_path": str(group_path) if group_path else None,
                                 "group_manifest_sha256": group_hash})
            except (surface.InputError, surface.ContractError, OSError, ValueError, TypeError) as error:
                raise _err(f"surface export failed: {error}") from error
        checkpoint["surface"] = refs
        checkpoint["phase"] = "surface_ready"
        checkpoint["last_safe_boundary"] = "before_result_import"
        _atomic(queue.checkpoint_path(root), _checkpoint_bytes(checkpoint))
        return {"batch_id": checkpoint["batch_id"], "runs": len(runs), "selected": len(checkpoint["selected"]), "ok": True}

def surface_import(root, outputs):
    """Validate accepted result bytes and checkpoint intended state updates first."""
    with queue.writer_lock(root):
        checkpoint = preflight(root)
        if checkpoint is None: raise _err("no active batch")
        if checkpoint["phase"] not in {"surface_ready", "surface_collected"}:
            raise _err("surface import requires an exported surface batch")
        if not isinstance(outputs, dict): raise _err("surface outputs must be a mapping of run/lane index to bytes")
        refs = checkpoint.get("surface") or []
        expected_keys = {str(i) for i in range(len(refs))}
        if any(type(key) is not str for key in outputs) or set(outputs) != expected_keys:
            raise _err("surface result keys must be exact strings with no missing or extra keys")
        _validate_surface_projection(root, checkpoint, require_outputs=checkpoint["phase"] == "surface_collected")
        updates = {}; validated = []
        for number, ref in enumerate(refs):
            _validate_surface_ref(ref, number)
            raw = outputs[str(number)]
            if isinstance(raw, (bytearray, memoryview)): raw = bytes(raw)
            if not isinstance(raw, bytes): raise _err("surface result must be bytes")
            if checkpoint["phase"] == "surface_collected":
                if ref["output_sha256"] != _sha(raw): raise _err("changed surface result re-import rejected")
                validated.append((ref, raw, None)); continue
            try:
                input_raw = Path(ref["input_path"]).read_bytes()
                accepted = surface.validate_result_bytes(input_raw, raw)
            except (OSError, surface.InputError, surface.ContractError, ValueError, TypeError, UnicodeError) as error:
                raise _err(f"surface result rejected by current consumer: {error}") from error
            if accepted["candidate_identity"] != ref["candidate_identity"]: raise _err("surface candidate identity drift")
            for result in accepted["results"]:
                revision = result["entry_revision_identity"]
                if revision in updates: raise _err("surface result union contains a duplicate identity")
                updates[revision] = "screened" if result["verdict"] == "OK" else "deep_required"
            validated.append((ref, raw, accepted))
        if checkpoint["phase"] == "surface_collected":
            return {"batch_id": checkpoint["batch_id"], "imported": 0, "ok": True}
        if set(updates) != set(checkpoint["selected"]): raise _err("surface result union does not equal selected identities")
        # Keep the original checkpoint untouched until all bytes and the full
        # next SQLite tuple have been validated.
        candidate = copy.deepcopy(checkpoint)
        created_outputs = []
        for number, (ref, raw, _accepted) in enumerate(validated):
            output_path = queue.checkpoint_path(root).parent / "surface" / f"run-{number:03d}-output.json"
            _atomic(output_path, raw)
            created_outputs.append(output_path)
            candidate["surface"][number].update({
                "output_path": str(output_path), "output_sha256": _sha(raw),
                "validator_status": "accepted"})
        for ref in candidate["surface"]:
            members = {candidate["selected"][i] for i in ref["parent_indexes"]}
            ref["intended_state_updates"] = {
                revision: updates[revision] for revision in sorted(members)}
        candidate["phase"] = "surface_collected"
        candidate["last_safe_boundary"] = "before_result_import"
        try:
            _validate_phase_desired_tuple(candidate)
        except Exception:
            for output_path in created_outputs:
                output_path.unlink(missing_ok=True)
            raise
        checkpoint = candidate
        _atomic(queue.checkpoint_path(root), _checkpoint_bytes(checkpoint))
        with sqlite3.connect(queue.database_path(root)) as con:
            con.executemany("UPDATE state_override SET state=?,result_sha256=? WHERE entry_revision_identity=? AND batch_id=?", [(state, _result_hash(checkpoint, revision), revision, checkpoint["batch_id"]) for revision, state in updates.items()])
            con.commit()
        return {"batch_id": checkpoint["batch_id"], "imported": len(updates), "ok": True}

def _deep_rows(checkpoint):
    return [(index, row) for index, row in enumerate(checkpoint["entry_snapshots"])
            if (checkpoint.get("surface") and any(index in ref.get("parent_indexes", []) and
               (ref.get("intended_state_updates") or {}).get(row["entry_revision_identity"]) == "deep_required"
               for ref in checkpoint["surface"]))]


def _contextual_bound_context(row):
    """Keep v1 context bytes unchanged and disclose v2 remapping metadata."""
    context = row["section"]
    if row["rules_version"] != catalog.RULES_VERSION:
        return context
    risk = row.get("risk")
    if not isinstance(risk, dict) or "args_order" not in risk:
        raise _err("rules-v2 catalog row lacks its exact risk.args_order")
    try:
        args_order = surface.validate_args_order(
            risk["args_order"], source=row["source"], label="contextual risk.args_order")
    except surface.ContractError as error:
        raise _err(str(error)) from error
    if risk.get("has_args_order") != (args_order is not None):
        raise _err("contextual risk args_order flag mismatch")
    # The absence of a fourth t(...) argument is the historical null form;
    # only a runtime remapping needs an args_order= disclosure token.  This is
    # also the exact token consumed by the existing contextual preflight.
    if args_order is None:
        return context
    return f"{context} args_order={{{','.join(str(index) for index in args_order)}}}"


def _contextual_payload(run):
    entries = run["entries"]
    keys = [row["entry_revision_identity"] for row in entries]
    payload = {"contract": "translation_contextual_v2", "ordered_revision_keys": keys,
               "translation_snapshot": [{"revision_key": row["entry_revision_identity"], "source": row["source"], "target": row["target"]} for row in entries],
               "fixed_source_identity": run["identity"][0],
               "terminology_snapshot": run["identity"][1],
               "bounded_context": [{"revision_key": row["entry_revision_identity"], "context": _contextual_bound_context(row)} for row in entries],
               "rendered_briefing": "WP2-Lite contextual review; review only"}
    contextual.canonical_payload_bytes(payload)
    return payload


def partition_contextual_entries(checkpoint):
    deep = _deep_rows(checkpoint)
    groups = defaultdict(list)
    for index, row in deep:
        groups[(row["fixed_source_identity"], row["terminology_snapshot_sha256"], row["rules_version"])].append((index, row))
    result = []
    for ordinal, (identity, members) in enumerate(sorted(groups.items(), key=lambda item: min(x[0] for x in item[1]))):
        ordered = [row for _, row in members]  # contextual order is frozen key order, not revision sorting
        result.append({"run_index": ordinal, "identity": identity, "parent_indexes": [i for i, _ in members], "entries": ordered})
    if sorted(i for run in result for i in run["parent_indexes"]) != [i for i, _ in deep]:
        raise _err("contextual deep-set union is not exact")
    return result


def contextual_export(root, *, task_ids=None):
    with queue.writer_lock(root):
        checkpoint = preflight(root)
        if checkpoint is None or checkpoint["phase"] not in {"surface_collected", "deep_ready"}:
            raise _err("contextual export requires collected surface results")
        runs = partition_contextual_entries(checkpoint)
        if not runs:
            raise _err("there are no deep_required entries")
        runtime = queue.checkpoint_path(root).parent / "contextual"
        task_ids = task_ids or {}
        refs = []
        for run in runs:
            payload = _contextual_payload(run)
            raw = contextual.canonical_payload_bytes(payload)
            identity = _sha(raw)
            envelope = {"candidate_identity": identity, "payload": payload}
            input_raw = json.dumps(envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
            path = runtime / f"run-{run['run_index']:03d}-input.json"
            task_id = task_ids.get(run["run_index"], f"{checkpoint['batch_id']}-contextual-{run['run_index']:03d}")
            state_path = f".ai/task/{task_id}/STATE.json"
            _atomic(path, input_raw)
            refs.append({"run_index": run["run_index"], "contract": "translation_contextual_v2",
                         "input_path": str(path), "input_sha256": _sha(input_raw), "output_path": None,
                         "output_sha256": None, "validator_status": "prepared", "candidate_identity": identity,
                         "parent_indexes": run["parent_indexes"], "task_id": task_id, "task_state_path": state_path,
                         "intended_state_updates": None})
        checkpoint["contextual"] = refs
        checkpoint["phase"] = "deep_ready"
        checkpoint["last_safe_boundary"] = "before_result_import"
        _atomic(queue.checkpoint_path(root), _checkpoint_bytes(checkpoint))
        return {"batch_id": checkpoint["batch_id"], "runs": len(refs), "entries": sum(len(r["parent_indexes"]) for r in refs), "ok": True}


def _contextual_done_verified(root, ref, input_raw=None, output_raw=None):
    """Verify the current terminal predicate and its exact producer bytes.

    ``STATE.json`` is only the terminal predicate.  The producer record is the
    binding authority for this import: it must name this task/candidate and the
    exact input and output bytes currently being imported.
    """
    try:
        import ai_state_check
        state_path = Path(ref["task_state_path"])
        if not state_path.is_absolute():
            state_path = root / state_path
        state = json.loads(state_path.read_bytes())
        if state.get("task_id") != ref["task_id"]:
            return False
        result = ai_state_check.check_state(state_path, target="DONE", workspace_root=root)
        if result.outcome != "DONE_VERIFIED":
            return False
        expected_input = _sha(input_raw) if input_raw is not None else None
        expected_output = _sha(output_raw) if output_raw is not None else None
        records = []
        for name in state.get("review_records", []):
            record_path = Path(name)
            if not record_path.is_absolute():
                record_path = root / record_path
            if record_path.is_file() and not record_path.is_symlink():
                record = json.loads(record_path.read_bytes())
                if (record.get("task_id") == ref["task_id"] and
                    record.get("review_contract") == "translation_contextual_v2" and
                    record.get("review_kind") == "full" and
                    record.get("review_phase") in {"REVIEW", "FINAL_REVIEW"} and
                    record.get("candidate_identity") == ref["candidate_identity"]):
                    records.append(record)
        if len(records) != 1:
            return False
        record = records[0]
        if record.get("input_path") != ref["task_state_path"].replace("STATE.json", "CONTEXTUAL-ENVELOPE-final-full.json"):
            # Accept the task's recorded path, but never an unbound path.
            input_path = record.get("input_path")
            if not isinstance(input_path, str):
                return False
        if expected_input is not None:
            input_path = root / record["input_path"] if not Path(record["input_path"]).is_absolute() else Path(record["input_path"])
            if not input_path.is_file() or _sha(input_path.read_bytes()) != expected_input:
                return False
        if expected_output is not None:
            output_path = root / record["raw_output_path"] if not Path(record["raw_output_path"]).is_absolute() else Path(record["raw_output_path"])
            if (record.get("raw_output_sha256") != expected_output or not output_path.is_file() or
                    _sha(output_path.read_bytes()) != expected_output):
                return False
        return True
    except (ImportError, OSError, TypeError, ValueError, KeyError, json.JSONDecodeError):
        return False


def contextual_import(root, outputs):
    with queue.writer_lock(root):
        checkpoint = preflight(root)
        if checkpoint is None or checkpoint["phase"] not in {"deep_ready", "deep_collected"}:
            raise _err("contextual import requires contextual export")
        refs = checkpoint.get("contextual") or []
        if not isinstance(outputs, dict) or set(outputs) != {str(i) for i in range(len(refs))}:
            raise _err("contextual result keys must be exact strings")
        updates = {}
        accepted_runs = []
        for number, ref in enumerate(refs):
            raw = outputs[str(number)]
            if isinstance(raw, (bytearray, memoryview)): raw = bytes(raw)
            if not isinstance(raw, bytes): raise _err("contextual result must be bytes")
            if checkpoint["phase"] == "deep_collected":
                if ref["output_sha256"] != _sha(raw): raise _err("changed contextual result re-import rejected")
                continue
            try:
                input_raw = Path(ref["input_path"]).read_bytes()
                accepted = contextual.validate_result_bytes(input_raw, raw)
            except (OSError, ValueError, TypeError, UnicodeError, contextual.InputError, contextual.ContractError) as error:
                raise _err(f"contextual result rejected: {error}") from error
            if accepted["candidate_identity"] != ref["candidate_identity"]: raise _err("contextual candidate identity drift")
            if not _contextual_done_verified(root, ref, input_raw, raw):
                raise _err("contextual task is not current DONE_VERIFIED bound to exact task/candidate/input/output")
            keys = [item["revision_key"] for item in accepted["verdicts"]]
            expected = [checkpoint["entry_snapshots"][i]["entry_revision_identity"] for i in ref["parent_indexes"]]
            if keys != expected: raise _err("contextual result membership/order mismatch")
            for item in accepted["verdicts"]:
                if item["revision_key"] in updates:
                    raise _err("contextual result union contains a duplicate identity")
                updates[item["revision_key"]] = item["verdict"]
            accepted_runs.append((number, ref, raw, accepted))
        if checkpoint["phase"] == "deep_collected":
            return {"batch_id": checkpoint["batch_id"], "imported": 0, "ok": True}
        expected_deep = {checkpoint["entry_snapshots"][i]["entry_revision_identity"]
                         for ref in refs for i in ref["parent_indexes"]}
        if set(updates) != expected_deep:
            raise _err("contextual result union does not equal deep_required set")
        candidate = copy.deepcopy(checkpoint)
        created_outputs = []
        for number, ref, raw, accepted in accepted_runs:
            output_path = queue.checkpoint_path(root).parent / "contextual" / f"run-{number:03d}-output.json"
            _atomic(output_path, raw)
            created_outputs.append(output_path)
            candidate["contextual"][number].update({
                "output_path": str(output_path), "output_sha256": _sha(raw),
                "validator_status": "accepted",
                "intended_state_updates": {
                    item["revision_key"]: item["verdict"]
                    for item in accepted["verdicts"]}})
        candidate["phase"] = "deep_collected"
        candidate["last_safe_boundary"] = "before_result_import"
        try:
            _validate_phase_desired_tuple(candidate)
        except Exception:
            for output_path in created_outputs:
                output_path.unlink(missing_ok=True)
            raise
        checkpoint = candidate
        _atomic(queue.checkpoint_path(root), _checkpoint_bytes(checkpoint))
        desired = _validate_phase_desired_tuple(checkpoint)
        with sqlite3.connect(queue.database_path(root)) as con:
            con.executemany("UPDATE state_override SET state=?,result_sha256=? WHERE entry_revision_identity=? AND batch_id=?",
                            [(desired[revision][1], _result_hash(checkpoint, revision), revision, checkpoint["batch_id"]) for revision in checkpoint["selected"]])
            con.commit()
        return {"batch_id": checkpoint["batch_id"], "imported": len(updates), "ok": True}


def _result_hash(checkpoint, revision):
    # Contextual output is the applicable final authority for deep rows.
    for ref in (checkpoint.get("contextual") or []) + (checkpoint.get("surface") or []):
        if revision in {checkpoint["entry_snapshots"][i]["entry_revision_identity"] for i in ref.get("parent_indexes", [])} and ref.get("output_sha256"):
            return ref["output_sha256"]
    return None

def _desired_state_overlay(checkpoint):
    """Derive one complete desired state map from accepted observations.

    This is deliberately an in-memory projection: the checkpoint is the sole
    authority while a batch is active and SQLite is only its rebuildable
    projection.  Every writer path consumes this same map.
    """
    selected = set(checkpoint["selected"])
    desired = {revision: "reserved" for revision in selected}
    for section in (checkpoint.get("surface") or []):
        for revision, state in (section.get("intended_state_updates") or {}).items():
            if revision not in selected or revision in desired and desired[revision] != "reserved":
                raise _err("desired-state overlay has duplicate surface identity")
            desired[revision] = state
    for section in (checkpoint.get("contextual") or []):
        for revision, verdict in (section.get("intended_state_updates") or {}).items():
            if revision not in selected or revision in desired and desired[revision] not in {"deep_required", "reserved"}:
                raise _err("desired-state overlay has duplicate contextual identity")
            desired[revision] = "done" if verdict == "OK" else "deep_required"
    # Once adjudications are present, the same cross-contract fold is the
    # authority for every ISSUE.  In particular, a surface ISSUE is not
    # erased by a later contextual OK for that revision.
    if checkpoint.get("adjudications") is not None:
        observations = _accepted_observations(checkpoint)
        decision_states = catalog.fold_issue_observations(
            observations, checkpoint.get("adjudications") or [])
        for revision, state in decision_states.items():
            if revision not in selected:
                raise _err("desired-state overlay adjudication identity is outside selection")
            desired[revision] = state
    if checkpoint.get("phase") in {"adjudicated", "commit_ready"}:
        # ``screened`` is an active-batch intermediate; evidence preparation
        # closes a clean surface-only row as durable ``done``.
        desired = {revision: ("done" if state == "screened" else state)
                   for revision, state in desired.items()}
    if set(desired) != selected:
        raise _err("desired-state overlay does not cover selected identities")
    return desired


def _validate_mode_prior(root, value, current):
    """Bind the frozen prior state to the durable winner, before mutation."""
    committed = {row[0]: row for row in current[3]}
    snapshots = {row["entry_revision_identity"]: row for row in value["entry_snapshots"]}
    if value["selection_mode"] == "queued":
        if any(row["prior_effective_state"] != "queued" for row in snapshots.values()):
            raise _err("queued batch contains a non-queued frozen prior state")
        if any(revision in committed for revision in snapshots):
            raise _err("queued batch contains a committed winner")
        return
    if any(row["prior_effective_state"] != "blocked" for row in snapshots.values()):
        raise _err("retry_blocked batch contains a non-blocked frozen prior state")
    for revision, snapshot in snapshots.items():
        winner = committed.get(revision)
        if winner is None or winner[2] != "blocked" or winner[1] != snapshot["logical_entry_identity"]:
            raise _err("retry_blocked batch lacks its exact current committed blocked winner")


def _new_checkpoint(root, manifest, rows, *, mode, attempt, created_by):
    selected = [r["entry_revision_identity"] for r in rows]
    snapshots = []
    for row in rows:
        snapshot = dict(row)
        snapshot["prior_effective_state"] = "blocked" if mode == "retry_blocked" else "queued"
        snapshot["row_sha256"] = _sha(wp1.canonical_bytes(row))
        snapshots.append(snapshot)
    value = {"schema_version": 1, "kind": "production_review_v2_lite_active_batch_v1", "batch_id": _batch_id(mode, selected, attempt), "catalog_id": manifest["catalog_id"], "base_commit": queue._head(root, "HEAD"), "policy_sha256": manifest["policy_sha256"], "created_at": catalog.utc_now(), "created_by": created_by, "attempt": attempt, "selection_mode": mode, "phase": "reserved", "selected": selected, "selected_sha256": _sha(wp1.canonical_bytes(selected)), "entry_snapshots": snapshots, "surface": None, "contextual": None, "adjudications": None, "repair_candidates": None, "gates": None, "last_safe_boundary": "reserved"}
    return value

def _restore_orphans(root, *, projection=None):
    """Reconcile reserved rows left by a crash before checkpoint replace.

    A committed blocked winner is authoritative; all other orphan reservations
    represent implicit queued rows.  Never reset an imported terminal/intermediate row.

    ``projection`` is a replay the caller already holds for HEAD.  It is reused
    only after re-resolving that commit and finding it unchanged; any other
    answer replays, exactly as an omitted argument does.
    """
    db = queue.database_path(root)
    try:
        if projection is None or projection[0] != queue._head(root, "HEAD"):
            projection = queue.projection_for(root, "HEAD")
        blocked = {row[0] for row in projection[3] if row[2] == "blocked"}
        with sqlite3.connect(db) as con:
            blocked_rows = {row[0]: row for row in projection[3] if row[2] == "blocked"}
            orphan = con.execute("SELECT * FROM state_override WHERE state='reserved'").fetchall()
            for existing in orphan:
                revision = existing[0]
                if revision in blocked_rows:
                    # Restore the complete committed winner tuple, not merely its state.
                    con.execute("UPDATE state_override SET logical_entry_identity=?,state=?,batch_id=?,attempt=?,result_sha256=?,updated_at=? WHERE entry_revision_identity=?",
                                (*blocked_rows[revision][1:], revision))
                else:
                    con.execute("DELETE FROM state_override WHERE entry_revision_identity=?", (revision,))
            con.commit()
    except (sqlite3.Error, OSError, KeyError, TypeError, ValueError) as error:
        raise _err(f"reservation reconciliation failed: {error}") from error


def _accepted_phase_maps(checkpoint):
    """Return state/hash maps for each completed adapter contract."""
    surface_states, surface_hashes = {}, {}
    contextual_states, contextual_hashes = {}, {}
    for ref in checkpoint.get("surface") or []:
        if ref.get("validator_status") != "accepted" or not ref.get("output_path"):
            continue
        try:
            input_raw, output_raw = Path(ref["input_path"]).read_bytes(), Path(ref["output_path"]).read_bytes()
            accepted = surface.validate_result_bytes(input_raw, output_raw)
        except (OSError, ValueError, TypeError, UnicodeError, surface.InputError, surface.ContractError) as error:
            raise _err(f"surface phase tuple cannot be reconstructed: {error}") from error
        for item in accepted["results"]:
            revision = item["entry_revision_identity"]
            state = "screened" if item["verdict"] == "OK" else "deep_required"
            if revision in surface_states:
                raise _err("surface phase tuple has duplicate identity")
            surface_states[revision] = state
            surface_hashes[revision] = ref["output_sha256"]
    for ref in checkpoint.get("contextual") or []:
        if ref.get("validator_status") != "accepted" or not ref.get("output_path"):
            continue
        try:
            input_raw, output_raw = Path(ref["input_path"]).read_bytes(), Path(ref["output_path"]).read_bytes()
            accepted = contextual.validate_result_bytes(input_raw, output_raw)
        except (OSError, ValueError, TypeError, UnicodeError, contextual.InputError, contextual.ContractError) as error:
            raise _err(f"contextual phase tuple cannot be reconstructed: {error}") from error
        for item in accepted["verdicts"]:
            revision = item["revision_key"]
            state = "done" if item["verdict"] == "OK" else "deep_required"
            if revision in contextual_states:
                raise _err("contextual phase tuple has duplicate identity")
            contextual_states[revision] = state
            contextual_hashes[revision] = ref["output_sha256"]
    return surface_states, surface_hashes, contextual_states, contextual_hashes


def _phase_tuple_maps(checkpoint):
    """Build the exact prior and desired SQLite tuple for every selected row."""
    surface_states, surface_hashes, contextual_states, contextual_hashes = _accepted_phase_maps(checkpoint)
    selected = checkpoint["selected"]
    by_revision = {row["entry_revision_identity"]: row for row in checkpoint["entry_snapshots"]}
    phase = checkpoint["phase"]
    if phase in {"surface_collected", "deep_ready", "deep_collected", "adjudicated", "commit_ready"}:
        if set(surface_states) != set(selected):
            raise _err("completed surface phase does not cover the selected set")
    deep_revisions = {revision for revision, state in surface_states.items() if state == "deep_required"}
    if phase in {"deep_collected", "adjudicated", "commit_ready"}:
        if deep_revisions and set(contextual_states) != deep_revisions:
            raise _err("completed contextual phase does not cover the surface ISSUE set")
    reservation = {
        revision: (by_revision[revision]["logical_entry_identity"], "reserved",
                   checkpoint["batch_id"], checkpoint["attempt"], None)
        for revision in selected
    }
    surface = {
        revision: (by_revision[revision]["logical_entry_identity"], surface_states[revision],
                   checkpoint["batch_id"], checkpoint["attempt"], surface_hashes[revision])
        for revision in selected
    } if set(surface_states) == set(selected) else reservation
    contextual = dict(surface)
    if phase in {"deep_collected", "adjudicated", "commit_ready"}:
        for revision in deep_revisions:
            contextual[revision] = (by_revision[revision]["logical_entry_identity"], contextual_states[revision],
                                    checkpoint["batch_id"], checkpoint["attempt"], contextual_hashes[revision])
    final_states = _desired_state_overlay(checkpoint) if phase in {"adjudicated", "commit_ready"} else None
    final = dict(contextual)
    if final_states is not None:
        for revision, state in final_states.items():
            if revision in deep_revisions:
                final[revision] = (by_revision[revision]["logical_entry_identity"], state,
                                   checkpoint["batch_id"], checkpoint["attempt"], contextual_hashes[revision])
            elif revision in surface:
                final[revision] = (by_revision[revision]["logical_entry_identity"], state,
                                   checkpoint["batch_id"], checkpoint["attempt"], surface_hashes[revision])
    if phase in {"reserved", "surface_ready"}:
        return reservation, reservation
    if phase == "surface_collected":
        return reservation, surface
    if phase == "deep_ready":
        return surface, surface
    if phase == "deep_collected":
        return surface, contextual
    return contextual, final


def _validate_phase_desired_tuple(checkpoint):
    """Validate the complete selected-row tuple before checkpoint replace."""
    _prior, desired = _phase_tuple_maps(checkpoint)
    selected = set(checkpoint["selected"])
    if set(desired) != selected:
        raise _err("phase desired tuple does not cover the selected set")
    for revision, value in desired.items():
        if (not isinstance(value, tuple) or len(value) != 5 or
                value[0] != checkpoint["entry_snapshots"][
                    checkpoint["selected"].index(revision)]["logical_entry_identity"] or
                value[2] != checkpoint["batch_id"] or value[3] != checkpoint["attempt"]):
            raise _err("phase desired tuple is not fully bound to the checkpoint")
    return desired


def _tuple_matches(row, expected):
    return tuple(row[1:6]) == tuple(expected)


def _reconcile_phase_tuples(root, checkpoint, current_projection):
    """Atomically advance only from an exact phase predecessor or desired tuple."""
    prior, desired = _phase_tuple_maps(checkpoint)
    committed = {row[0]: row for row in current_projection[3]}
    selected = set(checkpoint["selected"])
    by_revision = {row["entry_revision_identity"]: row for row in checkpoint["entry_snapshots"]}
    database = queue.database_path(root)
    try:
        with sqlite3.connect(database) as con:
            all_rows = {row[0]: row for row in con.execute("SELECT * FROM state_override")}
            if set(all_rows) - (set(committed) | selected):
                raise _err("active batch projection contains an unrelated override")
            for revision, expected in committed.items():
                if revision not in selected and all_rows.get(revision) != expected:
                    raise _err("active batch changed a non-selected committed override")
            mutations = []
            inserts = []
            for revision in checkpoint["selected"]:
                actual = all_rows.get(revision)
                acceptable = {prior[revision], desired[revision]}
                # A retry checkpoint may be written after the checkpoint but
                # before the reservation transaction; the exact committed
                # blocked winner is the only additional predecessor accepted.
                if (checkpoint["selection_mode"] == "retry_blocked" and
                        revision in committed and committed[revision][2] == "blocked"):
                    winner = committed[revision]
                    acceptable.add(tuple(winner[1:6]))
                if actual is None:
                    inserts.append((revision, by_revision[revision]["logical_entry_identity"],
                                    *desired[revision][1:], catalog.utc_now()))
                elif tuple(actual[1:6]) not in acceptable:
                    raise _err("SQLite row is not the exact previous or desired phase tuple")
                elif tuple(actual[1:6]) != tuple(desired[revision]):
                    mutations.append((revision, desired[revision]))
            timestamp = catalog.utc_now()
            con.executemany(
                "UPDATE state_override SET logical_entry_identity=?,state=?,batch_id=?,attempt=?,result_sha256=?,updated_at=? WHERE entry_revision_identity=?",
                [(logical, state, batch_id, attempt, result_hash, timestamp, revision)
                 for revision, (logical, state, batch_id, attempt, result_hash) in mutations])
            con.executemany("INSERT INTO state_override VALUES (?,?,?,?,?,?,?)", inserts)
            con.commit()
    except sqlite3.Error as error:
        raise _err(f"phase tuple reconciliation failed: {error}") from error

    # Validate the complete active projection after the one transaction.  This
    # is deliberately after all comparison/mutation planning, so a mismatch
    # cannot leave a partially advanced batch.
    with sqlite3.connect(database) as con:
        actual = {row[0]: row for row in con.execute("SELECT * FROM state_override")}
    for revision in selected:
        row = actual.get(revision)
        if row is None or not _tuple_matches(row, desired[revision]):
            raise _err("active batch phase tuple was not atomically advanced")
    # This replay was already produced for the same evidence commit before any
    # SQLite was opened; only the database changed since.  strict_check still
    # re-resolves the commit and replays if it moved.
    queue.strict_check(root, projection=current_projection)


def _reconcile_checkpoint(root, value):
    # Rebuild all checkpoint identity inputs from the authoritative Git
    # projection before opening SQLite.  This covers both the normal
    # reservation-present path and the missing-reservation recovery path.
    current_projection = queue.projection_for(root, "HEAD")
    _validate_mode_prior(root, value, current_projection)
    manifest, rows = _entries(root)
    committed = {row[0]: row for row in current_projection[3]}
    committed_states = {revision: row[2] for revision, row in committed.items()}
    expected_selected = stable_selection(
        rows, committed_states,
        retry_blocked=value["selection_mode"] == "retry_blocked",
        limit=len(value["selected"]),
    )
    expected_revisions = [row["entry_revision_identity"] for row in expected_selected]
    if value["selected"] != expected_revisions:
        raise _err("active batch selected identities differ from current stable selection")
    expected_attempt = 1
    if value["selection_mode"] == "retry_blocked":
        # _validate_mode_prior already established that every selected row is
        # an exact current blocked winner; derive the retry number from those
        # winners rather than trusting checkpoint/SQLite reservation fields.
        expected_attempt = 1 + max(committed[revision][4] for revision in expected_revisions)
    if value["attempt"] != expected_attempt:
        raise _err("active batch attempt differs from current authoritative winners")
    expected_batch_id = _batch_id(value["selection_mode"], expected_revisions, expected_attempt)
    if value["batch_id"] != expected_batch_id:
        raise _err("active batch identity differs from current authoritative selection")
    if value["catalog_id"] != manifest["catalog_id"] or value["base_commit"] != queue._head(root, "HEAD"):
        raise _err("active batch catalog/base commit drift")
    current = {row["entry_revision_identity"]: row for row in rows}
    for snapshot in value["entry_snapshots"]:
        revision = snapshot["entry_revision_identity"]
        if revision not in current or any(snapshot[key] != current[revision][key] for key in catalog.ENTRY_KEYS):
            raise _err("active batch catalog row drift")
    if value["phase"] == "surface_ready":
        _validate_surface_projection(root, value, require_outputs=False)
    elif value["phase"] in {"surface_collected", "deep_ready", "deep_collected",
                              "adjudicated", "commit_ready"}:
        _validate_surface_projection(root, value, require_outputs=True)
    for index, ref in enumerate(value.get("surface") or []):
        _validate_surface_ref(ref, index)
        try:
            input_raw = Path(ref["input_path"]).read_bytes()
            if _sha(input_raw) != ref["input_sha256"]: raise ValueError("surface input hash drift")
            _payload_value, candidate = surface.validate_envelope(surface.strict_json_bytes(input_raw, label="surface envelope"))
            if candidate != ref["candidate_identity"]: raise ValueError("surface candidate drift")
            if ref["output_path"] is not None:
                output_raw = Path(ref["output_path"]).read_bytes()
                if _sha(output_raw) != ref["output_sha256"]: raise ValueError("surface output hash drift")
                surface.validate_result_bytes(input_raw, output_raw)
            if ref["group_manifest_path"] is not None:
                group_raw = Path(ref["group_manifest_path"]).read_bytes()
                if _sha(group_raw) != ref["group_manifest_sha256"]: raise ValueError("surface group manifest hash drift")
                # Group structure was accepted during export; the lane files
                # are intentionally checkpoint-owned scratch and may be absent
                # while a writer is reopening the checkpoint.
        except (OSError, ValueError, TypeError, surface.InputError, surface.ContractError) as error:
            raise _err(f"stored surface raw preflight failed: {error}") from error
    for index, ref in enumerate(value.get("contextual") or []):
        if ref.get("validator_status") == "accepted":
            try:
                input_raw = Path(ref["input_path"]).read_bytes()
                output_raw = Path(ref["output_path"]).read_bytes()
            except OSError as error:
                raise _err(f"contextual accepted raw is unavailable during writer preflight: {error}") from error
            if not _contextual_done_verified(root, ref, input_raw, output_raw):
                raise _err("contextual task is not current DONE_VERIFIED bound to exact bytes during writer preflight")
        try:
            input_raw = Path(ref["input_path"]).read_bytes()
            if _sha(input_raw) != ref["input_sha256"]: raise ValueError("contextual input hash drift")
            _payload_value, candidate = contextual.validate_envelope(contextual.strict_json_bytes(input_raw, label="contextual envelope"))
            if candidate != ref["candidate_identity"]: raise ValueError("contextual candidate drift")
            if ref.get("output_path"):
                output_raw = Path(ref["output_path"]).read_bytes()
                if _sha(output_raw) != ref["output_sha256"]: raise ValueError("contextual output hash drift")
                accepted = contextual.validate_result_bytes(input_raw, output_raw)
                expected_revisions = [value["entry_snapshots"][i]["entry_revision_identity"]
                                      for i in ref["parent_indexes"]]
                if [item["revision_key"] for item in accepted["verdicts"]] != expected_revisions:
                    raise ValueError("contextual result membership/order drift")
                derived = {item["revision_key"]: item["verdict"]
                           for item in accepted["verdicts"]}
                if ref.get("intended_state_updates") != dict(sorted(derived.items())):
                    raise ValueError("contextual intended updates drift")
        except (OSError, ValueError, TypeError, contextual.InputError, contextual.ContractError) as error:
            raise _err(f"stored contextual raw preflight failed: {error}") from error
    _reconcile_phase_tuples(root, value, current_projection)
    return value

    # Retained below only as a source-compatible historical reference; the
    # phase-tuple reconciler above is the sole active implementation.
    selected = set(value["selected"])
    by_revision = {row["entry_revision_identity"]: row for row in value["entry_snapshots"]}
    try:
        with sqlite3.connect(queue.database_path(root)) as con:
            all_rows = {row[0]: row for row in con.execute("SELECT * FROM state_override")}
            actual_rows = {revision: row for revision, row in all_rows.items() if row[3] == value["batch_id"]}
            actual = {revision: row[2] for revision, row in actual_rows.items()}
            desired_states = _desired_state_overlay(value)
            committed = {row[0]: row for row in current_projection[3]}
            # SQLite-first abandon can leave the exact durable winner in place
            # while the checkpoint still says retry_blocked.  It is compatible
            # lag, so replace it with the active reservation in this transaction;
            # foreign ownership is never accepted.
            if value["selection_mode"] == "retry_blocked":
                for revision in selected:
                    winner = committed.get(revision)
                    row = all_rows.get(revision)
                    if row is not None and winner is not None and row == winner:
                        actual_rows[revision] = row
                        actual[revision] = row[2]
            if any(state not in {"reserved", "screened", "deep_required", "repair_required", "done", "blocked"}
                   for state in desired_states.values()):
                raise _err("desired-state overlay contains an invalid state")

            # Validate the complete mutation plan before issuing *any* SQLite
            # write.  A row may be absent, still reserved, or exactly desired;
            # all other drift (including screened <-> deep_required) fails
            # closed and leaves the database untouched.
            planned_updates = []
            planned_inserts = []
            for revision in value["selected"]:
                desired = desired_states[revision]
                current_row = actual_rows.get(revision)
                if current_row is None:
                    # A primary-key row outside this active batch is not a
                    # missing reservation and must never be replaced.
                    if revision in all_rows:
                        raise _err("incompatible active batch SQLite row ownership drift")
                    planned_inserts.append((revision, desired, _result_hash(value, revision)))
                    continue
                compatible_winner = (value["selection_mode"] == "retry_blocked" and
                                     revision in committed and current_row[2] == "blocked" and
                                     current_row[1] == committed[revision][1])
                expected_result_hash = _result_hash(value, revision)
                if (current_row[1] != by_revision[revision]["logical_entry_identity"] or
                        (not compatible_winner and current_row[4] != value["attempt"]) or
                        # A checkpoint-first crash leaves the exact reserved
                        # pre-transaction tuple (including NULL result hash).
                        (not compatible_winner and current_row[5] != expected_result_hash and
                         not (current_row[2] == "reserved" and current_row[5] is None)) or
                        (current_row[3] != value["batch_id"] and not compatible_winner) or
                        (current_row[2] not in {"reserved", desired} and not compatible_winner)):
                    raise _err("incompatible active batch SQLite state drift")
                if current_row[2] != desired:
                    planned_updates.append((revision, desired, expected_result_hash))
            timestamp = catalog.utc_now()
            con.executemany("UPDATE state_override SET state=?,result_sha256=?,batch_id=?,attempt=?,updated_at=? WHERE entry_revision_identity=?",
                            [(state, result_hash, value["batch_id"], value["attempt"], timestamp, revision)
                             for revision, state, result_hash in planned_updates])
            con.executemany("INSERT INTO state_override VALUES (?,?,?,?,?,?,?)",
                            [(revision, by_revision[revision]["logical_entry_identity"], desired,
                              value["batch_id"], value["attempt"], result_hash, timestamp)
                             for revision, desired, result_hash in planned_inserts])
            con.commit()
    except sqlite3.Error as error:
        raise _err(f"checkpoint reservation reconciliation failed: {error}") from error
    # The active projection may differ from committed evidence only for the
    # selected batch.  Reject unrelated overrides and then run the strict
    # queue checker; queue.check's concurrent-writer fallback is never enough
    # for a writer preflight.
    try:
        _evidence_head, _manifest, committed_entries, committed, _recon = queue._projection(root, "HEAD")
        committed_by_revision = {row[0]: row for row in committed}
        selected = set(value["selected"])
        desired = _desired_state_overlay(value)
        with sqlite3.connect(queue.database_path(root)) as con:
            actual = {row[0]: row for row in con.execute("SELECT * FROM state_override")}
        if set(actual) - (set(committed_by_revision) | selected):
            raise _err("active batch projection contains an unrelated override")
        for revision, expected in committed_by_revision.items():
            if revision not in selected and actual.get(revision) != expected:
                raise _err("active batch changed a non-selected committed override")
        for revision in selected:
            row = actual.get(revision)
            if row is None or row[1] != by_revision[revision]["logical_entry_identity"] or row[3] != value["batch_id"] or row[2] != desired.get(revision, "reserved"):
                raise _err("active batch reservation/update projection mismatch")
        queue.strict_check(root)
    except wp1.ProductionReviewError:
        raise
    except (sqlite3.Error, OSError, TypeError, ValueError, KeyError) as error:
        raise _err(f"active batch projection validation failed: {error}") from error
    return value


def preflight(root, *, projection_out=None):
    """Validate the active batch state; optionally hand back the one HEAD replay.

    The no-checkpoint path used to replay the same evidence commit twice here
    and a third time in `start`.  One replay now serves the orphan reconciler,
    the strict check, and — through ``projection_out`` — the caller continuing
    in this process.  Each consumer still re-resolves the commit before reuse.
    """
    try:
        path = queue.checkpoint_path(root)
        if path.exists():
            return _reconcile_checkpoint(root, _load(path))
        db = queue.database_path(root)
        if not db.exists(): raise _err("queue database is missing; run queue init")
        projection = queue.projection_for(root, "HEAD")
        if projection_out is not None:
            projection_out.append(projection)
        _restore_orphans(root, projection=projection)
        queue.strict_check(root, projection=projection)
        return None
    except wp1.ProductionReviewError:
        raise
    except Exception as error:
        raise _err(f"batch preflight failed: {error}") from error

def start(root, *, limit=MAX_BATCH, retry_blocked=False, created_by="WP2L-3 EXECUTOR"):
    with queue.writer_lock(root):
        carried = []
        current = preflight(root, projection_out=carried)
        if current is not None: raise _err("an active batch already exists; recover or abandon it")
        projection = carried[0] if carried else None
        queue.strict_check(root, projection=projection)
        manifest, rows, overrides = _effective_rows(root)
        selected = stable_selection(rows, overrides, retry_blocked=retry_blocked, limit=limit)
        if not selected: return {"selected": 0, "active": False, "ok": True}
        mode = "retry_blocked" if retry_blocked else "queued"
        attempt = 1
        if mode == "retry_blocked":
            if projection is None or projection[0] != queue._head(root, "HEAD"):
                projection = queue.projection_for(root, "HEAD")
            winners = {row[0]: row for row in projection[3]}
            if any(winners.get(row["entry_revision_identity"], (None, None, None))[2] != "blocked" for row in selected):
                raise _err("retry selection is not backed by current committed blocked winners")
            attempt = 1 + max(winners[row["entry_revision_identity"]][4] for row in selected)
        value = _new_checkpoint(root, manifest, selected, mode=mode, attempt=attempt, created_by=created_by)
        with sqlite3.connect(queue.database_path(root)) as con:
            con.executemany("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", [(r["entry_revision_identity"], r["logical_entry_identity"], "reserved", value["batch_id"], attempt, None, catalog.utc_now()) for r in selected]); con.commit()
        _atomic(queue.checkpoint_path(root), _checkpoint_bytes(value))
        return {"batch_id": value["batch_id"], "selected": len(selected), "selection_mode": value["selection_mode"], "ok": True}

def show(root):
    path = queue.checkpoint_path(root)
    return {"active": False, "ok": True} if not path.exists() else {"active": True, **_load(path)}

def abandon(root, *, discard_uncommitted_results=False, restore_evidence=False):
    with queue.writer_lock(root):
        # Validate the checkpoint-owned prospective tree before preflight can
        # reconcile any SQLite lag.  A failed authorization is therefore
        # mutation-free for the durable projection.
        checkpoint_path = queue.checkpoint_path(root)
        if not checkpoint_path.exists():
            raise _err("no active batch")
        value = _load(checkpoint_path)
        prospective = _prospective_batch_path(root, value["batch_id"])
        if prospective.exists() or prospective.is_symlink():
            if not restore_evidence:
                raise _err("prepared evidence requires --restore-evidence")
            declared = _prospective_declared_paths(value)
            _remove_generated_prospective_temps(prospective, value["batch_id"], declared)
            _validate_abandon_prospective(value, prospective)
        value = preflight(root)
        if value is None:
            raise _err("no active batch")
        has_accepted = any(ref.get("validator_status") == "accepted" for ref in (value.get("surface") or []) + (value.get("contextual") or []))
        if has_accepted and not discard_uncommitted_results: raise _err("accepted results require --discard-uncommitted-results")
        blocked_winners = {row[0]: row for row in queue._projection(root, "HEAD")[3] if row[2] == "blocked"}
        with sqlite3.connect(queue.database_path(root)) as con:
            for row in value["entry_snapshots"]:
                revision = row["entry_revision_identity"]
                if row["prior_effective_state"] == "blocked" and revision in blocked_winners:
                    winner = blocked_winners[revision]
                    con.execute("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", winner)
                elif row["prior_effective_state"] == "queued":
                    con.execute("DELETE FROM state_override WHERE entry_revision_identity=? AND batch_id=?", (revision, value["batch_id"]))
            con.commit()
        # Validate every removable scratch tree before changing SQLite or the
        # checkpoint.  A failed restore therefore remains retryable and does
        # not leave an orphaned prospective publication.
        for scratch_name in ("surface", "contextual"):
            scratch = queue.checkpoint_path(root).parent / scratch_name
            if scratch.exists() or scratch.is_symlink():
                if scratch.is_symlink():
                    scratch.unlink()
                else:
                    shutil.rmtree(scratch)
        if prospective.exists():
            shutil.rmtree(prospective)
            wp1._fsync_directory(prospective.parent)
        queue.checkpoint_path(root).unlink(); wp1._fsync_directory(queue.checkpoint_path(root).parent)
        database = queue.database_path(root)
        with sqlite3.connect(database) as cleanup_db:
            cleanup_db.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        for sidecar in (database.with_name("queue.sqlite3-wal"), database.with_name("queue.sqlite3-shm")):
            sidecar.unlink(missing_ok=True)
        wp1._fsync_directory(queue.checkpoint_path(root).parent)
        return {"abandoned": value["batch_id"], "ok": True}

def adjudicate(root, input_path):
    with queue.writer_lock(root):
        checkpoint = preflight(root)
        if checkpoint is None or checkpoint["phase"] not in {"surface_collected", "deep_collected"}:
            raise _err("adjudication requires collected review results")
        # A clean surface-only batch has no contextual observations to
        # adjudicate.  It still needs the same durable transition and can
        # proceed directly to evidence preparation.
        if checkpoint["phase"] == "surface_collected" and not _accepted_observations(checkpoint):
            try:
                raw = Path(input_path).read_bytes()
                value = wp1.parse_canonical_object(raw, "adjudication input")
            except (OSError, ValueError, UnicodeError, TypeError) as error:
                raise _err(f"invalid adjudication input: {error}") from error
            if (wp1.canonical_bytes(value) != raw or not isinstance(value, dict) or
                    set(value) != {"batch_id", "decisions"} or value["batch_id"] != checkpoint["batch_id"] or
                    value["decisions"] != []):
                raise _err("surface-only adjudication must contain an empty decisions array")
            candidate = copy.deepcopy(checkpoint)
            candidate["adjudications"] = []
            candidate["repair_candidates"] = []
            candidate["phase"] = "adjudicated"
            candidate["last_safe_boundary"] = "before_commit"
            desired = _validate_phase_desired_tuple(candidate)
            if any(desired[revision][1] not in queue.DURABLE_STATES
                   for revision in candidate["selected"]):
                raise _err("surface-only desired tuple contains a nonterminal state")
            checkpoint = candidate
            _atomic(queue.checkpoint_path(root), _checkpoint_bytes(checkpoint))
            with sqlite3.connect(queue.database_path(root)) as con:
                con.executemany("UPDATE state_override SET state=? WHERE entry_revision_identity=? AND batch_id=?", [(desired[revision][1], revision, checkpoint["batch_id"]) for revision in checkpoint["selected"]]); con.commit()
            return {"batch_id": checkpoint["batch_id"], "adjudicated": 0, "repair_required": 0, "ok": True}
        try: raw = Path(input_path).read_bytes(); value = wp1.parse_canonical_object(raw, "adjudication input")
        except (OSError, ValueError, UnicodeError, TypeError) as error: raise _err(f"invalid adjudication input: {error}") from error
        if wp1.canonical_bytes(value) != raw or not isinstance(value, dict) or set(value) != {"batch_id", "decisions"} or value["batch_id"] != checkpoint["batch_id"]:
            raise _err("adjudication input must be canonical and bind the active batch")
        decisions = value["decisions"]
        if not isinstance(decisions, list): raise _err("adjudication decisions must be an array")
        observations = _accepted_observations(checkpoint)
        by_identity = {item["observation_identity"]: item for item in observations}
        if (any(not isinstance(decision, dict) for decision in decisions) or
                len(decisions) != len(by_identity) or
                {decision.get("observation_identity") for decision in decisions} != set(by_identity)):
            raise _err("adjudications must cover exactly every surface/contextual observation")
        normalized = []
        seen = set()
        for index, decision in enumerate(decisions):
            required = {"entry_revision_identity", "observation_contract", "observation_identity", "observation_sha256", "disposition", "evidence_path", "evidence_commit", "evidence_snapshot", "conclusion", "repair_required"}
            if not isinstance(decision, dict) or set(decision) != required:
                raise _err(f"adjudication {index} exact schema mismatch")
            identity = decision["observation_identity"]
            observation = by_identity.get(identity)
            if observation is None or identity in seen or decision["entry_revision_identity"] != observation["entry_revision_identity"] or decision["observation_contract"] != observation["contract"]:
                raise _err("adjudication observation identity mismatch")
            seen.add(identity)
            if decision["observation_sha256"] != _sha((observation["observation"] or "").encode("utf-8")):
                raise _err("adjudication observation hash mismatch")
            if decision["disposition"] not in {"confirmed", "pending", "advisory", "refuted"} or type(decision["repair_required"]) is not bool:
                raise _err("invalid adjudication disposition")
            if decision["disposition"] != "confirmed" and decision["repair_required"]:
                raise _err("only confirmed observations may require repair")
            if decision["disposition"] == "confirmed":
                try:
                    evidence.validate_source_evidence(root, decision["evidence_path"],
                                                      decision["evidence_commit"], decision["evidence_snapshot"],
                                                      allow_legacy_annotation=False)
                except (wp1.ProductionReviewError, ValueError, TypeError) as error:
                    raise _err(f"confirmed public-source path/snapshot evidence rejected: {error}") from error
            normalized_row = dict(decision)
            normalized_row["schema_version"] = 1
            normalized_row.update({"observation_contract": observation["contract"],
                                   "observation_identity": observation["observation_identity"]})
            normalized.append(normalized_row)
        # Validate the shared fold against a candidate checkpoint before its
        # first atomic replace.  This also validates a complete desired SQLite
        # tuple, so an invalid cross-contract decision cannot leave a durable
        # checkpoint behind.
        states = catalog.fold_issue_observations(observations, normalized)
        candidate = copy.deepcopy(checkpoint)
        candidate["adjudications"] = normalized
        candidate["repair_candidates"] = sorted(
            revision for revision, state in states.items()
            if state == "repair_required")
        candidate["phase"] = "adjudicated"
        candidate["last_safe_boundary"] = "before_commit"
        desired = _validate_phase_desired_tuple(candidate)
        if any(desired[revision][1] not in queue.DURABLE_STATES
               for revision in candidate["selected"]):
            raise _err("adjudication desired tuple contains a nonterminal state")
        checkpoint = candidate
        _atomic(queue.checkpoint_path(root), _checkpoint_bytes(checkpoint))
        with sqlite3.connect(queue.database_path(root)) as con:
            con.executemany("UPDATE state_override SET state=? WHERE entry_revision_identity=? AND batch_id=?", [(desired[revision][1], revision, checkpoint["batch_id"]) for revision in checkpoint["selected"]]); con.commit()
        return {"batch_id": checkpoint["batch_id"], "adjudicated": len(states), "repair_required": len(checkpoint["repair_candidates"]), "ok": True}


def _evidence_rows(checkpoint):
    by = {row["entry_revision_identity"]: row for row in checkpoint["entry_snapshots"]}
    surface_results = {}; deep_results = {}
    for ref in checkpoint.get("surface") or []:
        if ref.get("output_path"):
            accepted = surface.validate_result_bytes(Path(ref["input_path"]).read_bytes(), Path(ref["output_path"]).read_bytes())
            surface_results.update({x["entry_revision_identity"]: x for x in accepted["results"]})
    for ref in checkpoint.get("contextual") or []:
        if ref.get("output_path"):
            accepted = contextual.validate_result_bytes(Path(ref["input_path"]).read_bytes(), Path(ref["output_path"]).read_bytes())
            deep_results.update({x["revision_key"]: x for x in accepted["verdicts"]})
    accepted_observations = _accepted_observations(checkpoint)
    decision_states = catalog.fold_issue_observations(
        accepted_observations, checkpoint.get("adjudications") or [],
        require_complete=checkpoint.get("adjudications") is not None)
    desired = _desired_state_overlay(checkpoint)
    final = {}
    for revision, row in by.items():
        deep = deep_results.get(revision); surf = surface_results.get(revision)
        if surf and surf["verdict"] == "ISSUE":
            # A surface ISSUE remains part of the fold even when contextual
            # review later reports OK.
            state = decision_states.get(revision)
            if state is None:
                raise _err("surface ISSUE lacks complete observation adjudication")
            level = "deep_reviewed" if deep else "surface_only"
        elif deep and deep["verdict"] == "OK":
            state, level = "done", "deep_reviewed"
        elif deep and deep["verdict"] == "ISSUE":
            state = decision_states.get(revision)
            if state is None:
                raise _err("deep ISSUE lacks complete observation adjudication")
            level = "deep_reviewed"
        elif surf and surf["verdict"] == "OK":
            state, level = "done", "surface_only"
        else:
            raise _err("selected row is not durably resolved")
        if state != desired[revision]:
            raise _err("evidence row state does not match the complete desired tuple")
        adapter = next((ref for ref in (checkpoint.get("surface") or []) + (checkpoint.get("contextual") or [])
                        if revision in {checkpoint["entry_snapshots"][i]["entry_revision_identity"] for i in ref.get("parent_indexes", [])}), None)
        final[revision] = {"schema_version": 1, "source": row["source"], "target": row["target"], "source_tag": row["source_tag"], "normalized_path": row["normalized_path"], "call_locator": row["call_locator"], "logical_entry_identity": row["logical_entry_identity"], "entry_revision_identity": revision, "surface_verdict": surf["verdict"] if surf else None, "surface_observation": surf.get("observation") if surf else None, "deep_verdict": deep["verdict"] if deep else None, "deep_observation": deep.get("observation") if deep else None, "input_sha256": adapter.get("input_sha256") if adapter else None, "output_sha256": adapter.get("output_sha256") if adapter else None, "final_state": state, "completion_level": level}
    return [final[r] for r in checkpoint["selected"]]


def _gate_candidate(checkpoint):
    return gate_results.candidate(checkpoint["batch_id"], checkpoint["catalog_id"],
                                  checkpoint["base_commit"], checkpoint["policy_sha256"],
                                  checkpoint["selected"])


def _actual_gate_records(root, selected):
    result = gate_results.run(root, selected)
    try:
        gate_results.validate(result, selected=selected,
                              expected_binding=gate_results.binding(root, selected), root=root)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        raise _err(f"applicable gate command failed: {error}") from error
    return result


def _prospective_declared_paths(checkpoint):
    """Return the exact repository-relative prepare inventory."""
    batch_id = checkpoint["batch_id"]
    declared = {_batch_relative(batch_id, name) for name in evidence.CORE_FILES}
    for number, section in enumerate((checkpoint.get("surface") or []) +
                                      (checkpoint.get("contextual") or [])):
        if not section.get("output_path"):
            continue
        kind = "contextual" if section["contract"] == "translation_contextual_v2" else "surface"
        for key in ("input_path", "output_path"):
            declared.add(_batch_relative(batch_id, "raw", kind,
                                         _raw_evidence_name(number, key)))
        if section.get("group_manifest_path"):
            declared.add(_batch_relative(batch_id, "raw", kind,
                                         _raw_evidence_name(number, "group_manifest_path")))
    return declared


def _prospective_inventory(runtime, batch_id):
    """Hash an existing prospective tree without accepting unknown entries."""
    if not (runtime.exists() or runtime.is_symlink()):
        return {}
    files = evidence.ordinary_files(runtime)
    return {_batch_relative(batch_id, *Path(relative).parts): _sha(raw)
            for relative, raw in files.items()}


def _remove_generated_prospective_temps(runtime, batch_id, declared):
    """Remove only the atomic temp names our prospective writer generates."""
    if not (runtime.exists() or runtime.is_symlink()):
        return
    prefix = _batch_relative(batch_id) + "/"
    for durable in sorted(declared):
        if not durable.startswith(prefix):
            raise _err("prospective inventory path is outside the active batch")
        relative = durable[len(prefix):]
        target = runtime / Path(*relative.split("/"))
        temporary = target.with_name("." + target.name + ".tmp")
        try:
            mode = temporary.lstat().st_mode
        except FileNotFoundError:
            continue
        except OSError as error:
            raise _err(f"cannot inspect prospective temporary path: {error}") from error
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            raise _err("prospective temporary path is not an ordinary generated file")
        temporary.unlink()
        wp1._fsync_directory(temporary.parent)


def _validate_prepare_resume(checkpoint, runtime, declared):
    """Validate an interrupted prepare before any prospective overwrite."""
    actual = _prospective_inventory(runtime, checkpoint["batch_id"])
    unknown = set(actual) - declared
    if unknown:
        raise _err("prospective evidence contains undeclared paths")
    previous = (checkpoint.get("gates") or {}).get("prospective")
    if previous is None:
        if actual:
            raise _err("prospective evidence exists without a checkpoint inventory")
        return actual
    if not isinstance(previous, dict) or set(previous) != declared:
        raise _err("prospective checkpoint inventory does not match canonical paths")
    for path, digest in previous.items():
        if digest is not None and (not isinstance(digest, str) or
                                   not wp1.SHA256_RE.fullmatch(digest) or
                                   actual.get(path) != digest):
            raise _err("prospective evidence does not match checkpoint postimages")
    return actual


def _validate_abandon_prospective(checkpoint, runtime):
    """Authorize the exact prospective inventory before touching SQLite."""
    gates = checkpoint.get("gates")
    declared = gates.get("prospective") if isinstance(gates, dict) else None
    preimage_absent = gates.get("preimage_absent") if isinstance(gates, dict) else None
    if (not isinstance(declared, dict) or
            not isinstance(preimage_absent, list) or
            set(preimage_absent) != set(declared)):
        raise _err("cannot restore evidence: checkpoint lacks a complete prospective authorization")
    actual = _prospective_inventory(runtime, checkpoint["batch_id"])
    if set(actual) - set(declared):
        raise _err("cannot restore evidence: prospective tree contains an undeclared file")
    # Before the first prospective postimage is complete, the checkpoint
    # deliberately carries a declared path inventory with null hashes.  The
    # explicit discard/restore authorization can remove that bounded partial
    # tree; once any postimage hash is present, every present file must match
    # its exact recorded hash.
    if all(declared.get(path) is None for path in declared):
        return
    if actual != declared:
        raise _err("cannot restore evidence: prospective bytes differ from checkpoint postimages")


def _write_fsynced(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name("." + path.name + ".tmp")
    if temporary.exists() or temporary.is_symlink():
        if temporary.is_symlink() or not temporary.is_file():
            raise _err("evidence temporary path is not an ordinary file")
        temporary.unlink()
    with temporary.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    wp1._fsync_directory(path.parent)


def prepare_evidence(root):
    with queue.writer_lock(root):
        checkpoint = preflight(root)
        if checkpoint is None or checkpoint["phase"] != "adjudicated": raise _err("evidence preparation requires adjudicated batch")
        rows = _evidence_rows(checkpoint)
        # Record real checks before changing the checkpoint.  A clean status
        # listing is intentionally not a gate.
        selected = _gate_candidate(checkpoint)
        gate_result = _actual_gate_records(root, selected)
        gate_records = gate_result["checks"]
        destination = root / Path(_batch_relative(checkpoint["batch_id"]))
        # The prospective tree is scratch, but the destination collision is a
        # real repository concern (including an untracked directory).
        if destination.exists() or destination.is_symlink():
            raise _err("actual evidence batch destination already exists; refusing a path collision")
        runtime = _prospective_batch_path(root, checkpoint["batch_id"])
        if runtime.is_symlink() or (runtime.exists() and not runtime.is_dir()):
            raise _err("prospective evidence batch is not an ordinary directory")
        # Freeze the complete path inventory before the first prospective
        # write.  Hashes are filled with exact postimages below; None marks an
        # interrupted prepare that is safe to resume, not a second store.
        declared_paths = _prospective_declared_paths(checkpoint)
        _remove_generated_prospective_temps(runtime, checkpoint["batch_id"], declared_paths)
        _validate_prepare_resume(checkpoint, runtime, declared_paths)
        checkpoint["gates"] = {"commands": gate_records, "prospective": {path: None for path in sorted(declared_paths)},
                                "preimage_absent": sorted(declared_paths), "prospective_bytes": 0, "committed_bytes": 0}
        _atomic(queue.checkpoint_path(root), _checkpoint_bytes(checkpoint))
        runtime.mkdir(parents=True, exist_ok=True)
        raw_root = runtime / "raw"
        refs = []
        for number, section in enumerate((checkpoint.get("surface") or []) + (checkpoint.get("contextual") or [])):
            if not section.get("output_path"): continue
            kind = "contextual" if section["contract"] == "translation_contextual_v2" else "surface"
            copied = {}
            for key in ("input_path", "output_path"):
                name = _raw_evidence_name(number, key)
                src = Path(section[key]); dest = raw_root / kind / name
                raw = src.read_bytes(); _write_fsynced(dest, raw)
                copied[key] = (_batch_relative(checkpoint["batch_id"], "raw", kind, name), _sha(raw))
            ref = {"contract": section["contract"], "input_path": copied["input_path"][0], "input_sha256": copied["input_path"][1], "output_path": copied["output_path"][0], "output_sha256": copied["output_path"][1], "candidate_identity": section["candidate_identity"]}
            if section.get("group_manifest_path"):
                name = _raw_evidence_name(number, "group_manifest_path")
                src = Path(section["group_manifest_path"]); dest = raw_root / kind / name
                raw = src.read_bytes(); _write_fsynced(dest, raw)
                ref.update({"group_manifest_path": _batch_relative(checkpoint["batch_id"], "raw", kind, name), "group_manifest_sha256": _sha(raw)})
            refs.append(ref)
        def jsonl(values): return b"".join(wp1.canonical_bytes(v) + b"\n" for v in values)
        adjud_raw = jsonl(checkpoint.get("adjudications") or [])
        gates_raw = wp1.canonical_bytes({"schema_version": 2, "result": gate_result, "prospective_bytes": 0, "committed_bytes": 0})
        # Bind every durable result to the generated raw bytes before the
        # prospective tree is published; the checkpoint paths are absolute
        # scratch paths while the manifest refs are repository-relative.
        for row in rows:
            revision = row["entry_revision_identity"]
            for section in (checkpoint.get("contextual") or []) + (checkpoint.get("surface") or []):
                if not section.get("output_path"):
                    continue
                try:
                    if section["contract"] == "translation_contextual_v2":
                        accepted = contextual.validate_result_bytes(Path(section["input_path"]).read_bytes(), Path(section["output_path"]).read_bytes())
                        members = {item["revision_key"] for item in accepted["verdicts"]}
                    else:
                        accepted = surface.validate_result_bytes(Path(section["input_path"]).read_bytes(), Path(section["output_path"]).read_bytes())
                        members = {item["entry_revision_identity"] for item in accepted["results"]}
                    if revision in members:
                        row["input_sha256"], row["output_sha256"] = section["input_sha256"], section["output_sha256"]
                        break
                except (OSError, ValueError, TypeError, UnicodeError):
                    continue
            if row["input_sha256"] is None:
                raise _err("selected row has no generated adapter byte binding")
        results_raw = jsonl(rows)
        manifest = {"schema_version": 1, "kind": "production_review_v2_lite_batch_v1", "catalog_id": checkpoint["catalog_id"], "policy_sha256": checkpoint["policy_sha256"], "base_commit": checkpoint["base_commit"], "batch_id": checkpoint["batch_id"], "attempt": checkpoint["attempt"], "ordered_revisions": checkpoint["selected"], "ordered_revisions_sha256": _sha(wp1.canonical_bytes(checkpoint["selected"])), "entry_snapshots_sha256": _sha(wp1.canonical_bytes([{key: snapshot[key] for key in catalog.ENTRY_KEYS} for snapshot in checkpoint["entry_snapshots"]])), "adapter_refs": refs, "results_sha256": _sha(results_raw), "adjudications_sha256": _sha(adjud_raw), "gates_sha256": _sha(gates_raw), "producer_task_ids": [r["task_id"] for r in checkpoint.get("contextual") or []], "recorded_at": catalog.utc_now(), "recorded_by": checkpoint["created_by"]}
        batch_root = runtime
        _write_fsynced(batch_root / "results.jsonl", results_raw)
        _write_fsynced(batch_root / "adjudications.jsonl", adjud_raw)
        _write_fsynced(batch_root / "gates.json", gates_raw)
        _write_fsynced(batch_root / "manifest.json", wp1.canonical_bytes(manifest))
        for directory in sorted((p for p in batch_root.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            wp1._fsync_directory(directory)
        wp1._fsync_directory(batch_root)
        try:
            prospective_total = evidence.prospective_tracked_bytes(root, batch_root)
        except Exception:
            shutil.rmtree(batch_root, ignore_errors=True)
            wp1._fsync_directory(batch_root.parent)
            raise
        # The gates section also records the exact prospective occupancy.  Its
        # decimal value changes the gate file's own size, so converge the
        # small self-referential measurement before freezing postimages.
        # Reuse only this call's receipt after re-reading the checkpoint and live inputs.
        try:
            gate_results.validate(gate_result, selected=_gate_candidate(show(root)),
                                  expected_binding=gate_results.binding(root, selected), root=root)
        except (ValueError, OSError, subprocess.SubprocessError) as error:
            raise _err(f"gate reuse rejected: {error}") from error
        gates_value = {"schema_version": 2, "result": gate_result,
                       "prospective_bytes": prospective_total,
                       "committed_bytes": prospective_total}
        for _ in range(4):
            gates_raw = wp1.canonical_bytes(gates_value)
            _write_fsynced(batch_root / "gates.json", gates_raw)
            manifest["gates_sha256"] = _sha(gates_raw)
            _write_fsynced(batch_root / "manifest.json", wp1.canonical_bytes(manifest))
            measured = evidence.prospective_tracked_bytes(root, batch_root)
            if measured == prospective_total:
                break
            prospective_total = measured
            gates_value["prospective_bytes"] = measured
            gates_value["committed_bytes"] = measured
        else:
            raise _err("prospective occupancy did not converge")
        prospective_total = evidence.prospective_tracked_bytes(root, batch_root)
        if gates_value["prospective_bytes"] != prospective_total:
            raise _err("prospective occupancy changed after gate measurement")
        # Re-emit the final bytes after convergence so the checkpoint hashes
        # exactly the files that can be abandoned or published.
        gates_raw = wp1.canonical_bytes(gates_value)
        _write_fsynced(batch_root / "gates.json", gates_raw)
        manifest["gates_sha256"] = _sha(gates_raw)
        manifest_raw = wp1.canonical_bytes(manifest)
        _write_fsynced(batch_root / "manifest.json", manifest_raw)
        if evidence.prospective_tracked_bytes(root, batch_root) != prospective_total:
            raise _err("prospective occupancy changed after final postimage")
        prospective_files = {_batch_relative(checkpoint["batch_id"], *item.relative_to(batch_root).parts): _sha(item.read_bytes()) for item in sorted(p for p in batch_root.rglob("*") if p.is_file())}
        checkpoint["gates"] = {"commands": gate_result["checks"], "prospective": prospective_files, "preimage_absent": sorted(prospective_files), "prospective_bytes": prospective_total, "committed_bytes": prospective_total}
        checkpoint["phase"] = "commit_ready"; checkpoint["last_safe_boundary"] = "before_commit"; _atomic(queue.checkpoint_path(root), _checkpoint_bytes(checkpoint))
        return {"batch_id": checkpoint["batch_id"], "prospective": str(batch_root), "results": len(rows), "ok": True}


def _committed_production_bytes(root, commit):
    tree = queue._tree(root, commit)
    total = 0
    for path, (mode, kind, object_id) in tree.items():
        if any(path.startswith(prefix) for prefix in evidence.PRODUCTION_PREFIXES):
            if mode not in {"100644", "100755"} or kind != "blob":
                raise _err("committed production evidence contains a non-ordinary entry")
            total += len(queue._blob(root, object_id, path))
    if total > catalog.TRACKED_LIMIT:
        raise _err("committed production evidence exceeds the combined 128 MiB budget")
    return total


def finalize(root, commit):
    with queue.writer_lock(root):
        path = queue.checkpoint_path(root)
        if not path.exists(): return {"active": False, "ok": True}
        checkpoint = _load(path)
        if checkpoint["phase"] != "commit_ready": raise _err("finalize requires commit_ready batch")
        # Finalize is another writer path: accepted contextual authority must
        # still be terminal at the moment the publication is consumed.
        for ref in checkpoint.get("contextual") or []:
            if ref.get("validator_status") == "accepted":
                try:
                    input_raw = Path(ref["input_path"]).read_bytes()
                    output_raw = Path(ref["output_path"]).read_bytes()
                except OSError as error:
                    raise _err(f"accepted contextual raw is unavailable during finalize: {error}") from error
                if not _contextual_done_verified(root, ref, input_raw, output_raw):
                    raise _err("accepted contextual task is no longer current DONE_VERIFIED bound to exact bytes")
        if not isinstance(commit, str) or len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit): raise _err("finalize commit must be a Git commit")
        parent = queue._commit_parent(root, commit)
        if parent != checkpoint["base_commit"]: raise _err("finalize commit parent does not equal batch base_commit")
        tree = queue._tree(root, commit); prefix = queue.BATCH_PREFIX + checkpoint["batch_id"] + "/"
        if prefix + "manifest.json" not in tree: raise _err("reviewed commit does not contain this batch evidence")
        committed_total = _committed_production_bytes(root, commit)
        declared = (checkpoint.get("gates") or {}).get("committed_bytes")
        if declared is not None and declared != committed_total:
            raise _err("committed production-tree occupancy does not match the successful gate")
        # Existing queue replay is the authoritative current-tree validator.
        projection = queue._projection(root, commit)
        queue._replace(root, projection)
        path.unlink(); wp1._fsync_directory(path.parent)
        return {"batch_id": checkpoint["batch_id"], "commit": commit, "ok": True}


def _recover_committed_checkpoint(root, checkpoint):
    """Consume a commit-ready checkpoint whose publication reached HEAD."""
    if checkpoint["phase"] != "commit_ready":
        return None
    head = queue._head(root, "HEAD")
    tree = queue._tree(root, head)
    prefix = queue.BATCH_PREFIX + checkpoint["batch_id"] + "/"
    if prefix + "manifest.json" not in tree:
        return None
    if queue._commit_parent(root, head) != checkpoint["base_commit"]:
        return None
    # _projection invokes the durable evidence validator, including exact raw
    # bytes, observation contracts, gates and one-publication ancestry.
    projection = queue._projection(root, head)
    _committed_production_bytes(root, head)
    queue._replace(root, projection)
    path = queue.checkpoint_path(root)
    path.unlink()
    wp1._fsync_directory(path.parent)
    return {"batch_id": checkpoint["batch_id"], "commit": head,
            "recovered": True, "finalized": True, "ok": True}


def recover_from_head(root):
    """Direct CLI recovery alias: rebuild or finalize the current HEAD."""
    with queue.writer_lock(root):
        checkpoint = queue.checkpoint_path(root)
        database = queue.database_path(root)
        if not checkpoint.exists() and not database.exists():
            projection = queue._projection(root, "HEAD")
            return queue._replace(root, projection) | {"recovered": True}
    return recover(root)


def recover(root):
    with queue.writer_lock(root):
        database = queue.database_path(root)
        checkpoint = queue.checkpoint_path(root)
        if checkpoint.exists():
            committed = _recover_committed_checkpoint(root, _load(checkpoint))
            if committed is not None:
                return committed
        # Git is the durable publication authority.  A crash can happen after
        # commit and before checkpoint removal, or after the checkpoint itself
        # is lost; both cases must rebuild the one SQLite projection from HEAD.
        if not checkpoint.exists():
            # Checkpointless recovery is the only path allowed to rebuild the
            # projection.  An active checkpoint with a missing database is an
            # incomplete reservation transaction and must fail closed before
            # any replacement can mutate bytes.
            queue._replace(root, queue._projection(root, "HEAD"))
        elif not database.exists():
            # Validate checkpoint authority from Git before rebuilding a lost
            # projection; this keeps forged attempt/selection data fail-closed.
            value = _load(checkpoint)
            projection = queue._projection(root, "HEAD")
            _validate_mode_prior(root, value, projection)
            if value["selection_mode"] == "retry_blocked":
                winners = {row[0]: row for row in projection[3]}
                expected_attempt = 1 + max(winners[revision][4] for revision in value["selected"])
            else:
                expected_attempt = 1
            if value["attempt"] != expected_attempt:
                raise _err("checkpoint attempt is not backed by authoritative winners")
            queue._replace(root, projection)
        value = preflight(root)
        if value is None:
            return {"active": False, "recovered": True, "ok": True}
        return {"batch_id": value["batch_id"], "recovered": True, "phase": value["phase"], "ok": True}
