"""Quiescent catalog migration and repair-preflight helpers for WP2-Lite.

This module deliberately keeps migration as a batch-boundary operation.  The
catalog and Git tree are the inputs, the existing SQLite projection is the only
mutable runtime state, and the migration JSON is only a prospective artifact
until a maintainer publishes it in the ordinary Git change.
"""
from __future__ import annotations

import hashlib
import os
import sqlite3
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from . import production_review as wp1
from . import production_review_v2_lite as catalog

MIGRATION_KIND = "production_review_v2_lite_migration_v1"
MIGRATION_PREFIX = "evidence/production-review-v2-lite/migrations/"
MIGRATION_SUFFIX = ".json"
REPAIR_KIND = "production_review_v2_lite_repair_workset_v1"
REPAIR_KEYS = frozenset({
    "schema_version", "kind", "batch_id", "evidence_commit", "catalog_id",
    "catalog_manifest_sha256", "policy_sha256", "items", "items_sha256",
    "recorded_at", "recorded_by",
})
REPAIR_ITEM_KEYS = frozenset({
    "entry_revision_identity", "logical_entry_identity", "component",
    "normalized_path", "section", "source", "target_preimage",
    "target_preimage_sha256", "source_tag", "call_locator",
    "fixed_source_identity", "terminology_snapshot_sha256", "rules_version",
    "winner_evidence", "proposed_successor_input",
})
ACTIVE_STATES = frozenset({"reserved", "screened", "deep_required"})
DISPOSITIONS = frozenset({"unchanged", "revision_changed", "logical_moved", "removed", "ambiguous", "unmapped"})
REASONS = frozenset({
    "unchanged", "target_changed", "source_changed", "source_tag_changed",
    "call_locator_changed", "fixed_source_changed", "terminology_changed",
    "args_order_changed", "rules_changed", "removed", "ambiguous", "unmapped",
})
CATALOG_COUNT_KEYS = frozenset({"occurrence_count", "entry_count", "exclusion_count"})
MAPPING_KEYS = frozenset({
    "old_logical_entry_identity", "old_entry_revision_identity",
    "new_logical_entry_identity", "new_entry_revision_identity",
    "disposition", "reason", "old_row_sha256", "new_row_sha256",
})
ROW_SNAPSHOT_KEYS = frozenset({
    "logical_entry_identity", "entry_revision_identity", "row_sha256",
})
MIGRATION_KEYS = frozenset({
    "schema_version", "kind", "migration_id", "base_commit", "base_tree",
    "target_path", "old_catalog_id", "old_manifest_sha256", "old_entries_sha256",
    "old_exclusions_sha256", "old_counts", "new_catalog_id", "new_manifest_sha256",
    "new_entries_sha256", "new_exclusions_sha256", "new_counts", "old_rows",
    "new_rows", "rows", "rows_sha256", "recorded_at", "recorded_by",
})


def _error(message: str) -> wp1.ProductionReviewError:
    return wp1.ProductionReviewError(message)


def _sha(value: object, label: str) -> str:
    if not isinstance(value, str) or not wp1.SHA256_RE.fullmatch(value):
        raise _error(f"{label} must be a lowercase SHA-256")
    return value


def _commit(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise _error(f"{label} must be a lowercase Git commit")
    return value


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise _error(f"{label} must be non-empty")
    return value


def _exact(value: object, keys: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        actual = set(value) if isinstance(value, dict) else set()
        raise _error(f"{label} exact keys mismatch (missing={sorted(keys-actual)}, extra={sorted(actual-keys)})")
    return value


def _git(root: Path, *args: str) -> bytes:
    try:
        return subprocess.run(["git", *args], cwd=root, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        detail = error.stderr.decode("utf-8", "replace").strip() if isinstance(error, subprocess.CalledProcessError) else str(error)
        raise _error(f"migration Git operation failed: {detail}") from error


def _head(root: Path, treeish: str = "HEAD") -> str:
    value = _git(root, "rev-parse", "--verify", f"{treeish}^{{commit}}").decode("ascii").strip()
    return _commit(value, "base_commit")


def _tree_id(root: Path, commit: str) -> str:
    value = _git(root, "rev-parse", f"{commit}^{{tree}}").decode("ascii").strip()
    if len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise _error("base_tree must be a lowercase Git tree")
    return value


def _raw_sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _summary(manifest: dict[str, Any], files: dict[str, bytes]) -> dict[str, Any]:
    manifest_path = f"{catalog.CATALOG_PREFIX}/manifest.json"
    entries_path = f"{catalog.CATALOG_PREFIX}/entries.jsonl"
    exclusions_path = f"{catalog.CATALOG_PREFIX}/exclusions.jsonl"
    return {
        "catalog_id": _sha(manifest.get("catalog_id"), "catalog_id"),
        "manifest_sha256": _raw_sha(files[manifest_path]),
        "entries_sha256": _sha(manifest.get("entries_sha256"), "entries_sha256"),
        "exclusions_sha256": _sha(manifest.get("exclusions_sha256"), "exclusions_sha256"),
        "counts": {
            "occurrence_count": manifest.get("occurrence_count"),
            "entry_count": manifest.get("entry_count"),
            "exclusion_count": manifest.get("exclusion_count"),
        },
    }


def _validate_bundle(files: dict[str, bytes], label: str) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    try:
        manifest, entries, _exclusions = catalog.validate_catalog_files(files)
    except (wp1.ProductionReviewError, KeyError, TypeError, ValueError) as error:
        raise _error(f"{label} catalog is not an exact validated catalog: {error}") from error
    for path, raw in files.items():
        if path.endswith(".json"):
            value = wp1.parse_canonical_object(raw, f"{label} {path}")
            if wp1.canonical_bytes(value) != raw:
                raise _error(f"{label} {path} is not canonical")
    if catalog.catalog_id(manifest) != manifest["catalog_id"]:
        raise _error(f"{label} catalog_id does not bind its manifest")
    if not isinstance(manifest.get("rules_version"), str) or not manifest["rules_version"]:
        raise _error(f"{label} rules_version is invalid")
    if any(row.get("rules_version") != manifest["rules_version"] for row in entries):
        raise _error(f"{label} entry rules_version does not match its manifest")
    if any(type(manifest[key]) is not int or manifest[key] < 0
           for key in ("occurrence_count", "entry_count", "exclusion_count")):
        raise _error(f"{label} catalog counts are invalid")
    summary = _summary(manifest, files)
    if any(not isinstance(value, int) for value in summary["counts"].values()):
        raise _error(f"{label} catalog counts are not integers")
    if summary["counts"]["occurrence_count"] != summary["counts"]["entry_count"] + summary["counts"]["exclusion_count"]:
        raise _error(f"{label} catalog conservation mismatch")
    return manifest, entries, summary


def _current_bundle(root: Path, treeish: str) -> tuple[str, str, dict[str, Any], list[dict[str, Any]], dict[str, bytes], dict[str, Any]]:
    from . import production_review_v2_lite_queue as queue
    commit = _head(root, treeish)
    manifest, entries, files = queue._catalog_from_tree(root, commit)
    _manifest, _entries, summary = _validate_bundle(files, f"current {commit}")
    return commit, _tree_id(root, commit), manifest, entries, files, summary


def _candidate_bundle(root: Path, candidate_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, bytes], dict[str, Any]]:
    try:
        files = catalog.ordinary_tree(candidate_root)
    except (OSError, wp1.ProductionReviewError) as error:
        raise _error(f"candidate catalog cannot be read: {error}") from error
    manifest, entries, summary = _validate_bundle(files, "candidate")
    return manifest, entries, files, summary


def _row_sha(row: dict[str, Any]) -> str:
    return _raw_sha(wp1.canonical_bytes(row))


def _snapshots(entries: Iterable[dict[str, Any]]) -> list[dict[str, str]]:
    result = [{
        "logical_entry_identity": row["logical_entry_identity"],
        "entry_revision_identity": row["entry_revision_identity"],
        "row_sha256": _row_sha(row),
    } for row in entries]
    result.sort(key=lambda row: row["entry_revision_identity"].encode("ascii"))
    return result


def _validate_snapshots(value: object, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise _error(f"{label} must be an array")
    result: list[dict[str, str]] = []
    previous = ""
    seen_revisions: set[str] = set()
    seen_logicals: set[str] = set()
    for index, item in enumerate(value):
        row = _exact(item, ROW_SNAPSHOT_KEYS, f"{label} row {index}")
        logical = _sha(row["logical_entry_identity"], f"{label} logical identity")
        revision = _sha(row["entry_revision_identity"], f"{label} revision identity")
        digest = _sha(row["row_sha256"], f"{label} row hash")
        if revision <= previous or revision in seen_revisions or logical in seen_logicals:
            raise _error(f"{label} is not strictly ordered and unique")
        previous = revision
        seen_revisions.add(revision)
        seen_logicals.add(logical)
        result.append({"logical_entry_identity": logical, "entry_revision_identity": revision, "row_sha256": digest})
    return result


def _counts(value: object, label: str) -> dict[str, int]:
    row = _exact(value, CATALOG_COUNT_KEYS, label)
    if any(type(row[key]) is not int or row[key] < 0 for key in CATALOG_COUNT_KEYS):
        raise _error(f"{label} contains invalid counts")
    return {key: row[key] for key in sorted(CATALOG_COUNT_KEYS)}


def _summary_matches(value: dict[str, Any], summary: dict[str, Any], label: str) -> None:
    for key in ("catalog_id", "manifest_sha256", "entries_sha256", "exclusions_sha256"):
        if value[key] != summary[key]:
            raise _error(f"{label} {key} drift")
    if value["counts"] != summary["counts"]:
        raise _error(f"{label} counts drift")


def _reason_changed(old: dict[str, Any], new: dict[str, Any]) -> str:
    fields = (
        ("target", "target_changed"), ("source", "source_changed"),
        ("source_tag", "source_tag_changed"), ("call_locator", "call_locator_changed"),
        ("fixed_source_identity", "fixed_source_changed"),
    )
    for field, reason in fields:
        if old.get(field) != new.get(field):
            return reason
    # In rules-v2 terminology is provenance only, while args_order is part of
    # the revision identity.  Give the identity input its own reason whenever
    # both rows are v2 so a provenance refresh cannot mask this change.
    old_args = old.get("risk", {}).get("args_order")
    new_args = new.get("risk", {}).get("args_order")
    if (old.get("rules_version") == catalog.RULES_VERSION and
            new.get("rules_version") == catalog.RULES_VERSION and
            old_args != new_args):
        return "args_order_changed"
    for field, reason in (("terminology_snapshot_sha256", "terminology_changed"),
                          ("rules_version", "rules_changed")):
        if old.get(field) != new.get(field):
            return reason
    raise _error("revision identity changed without an identity input change")


def _structure(row: dict[str, Any]) -> tuple[str, str, str, str]:
    # Formal catalog rows use the loader's t(...) call.  Test/adaptor rows may
    # expose the same fixed function explicitly; neither form uses a line
    # number or fuzzy textual feature.
    return (row["component"], row["normalized_path"], row["section"],
            row.get("function_name", "t"))


def _mapping_row(old: dict[str, Any], new: dict[str, Any] | None, disposition: str, reason: str) -> dict[str, Any]:
    if disposition not in DISPOSITIONS or reason not in REASONS:
        raise _error("invalid migration classification")
    if new is None:
        new_logical = new_revision = new_hash = None
    else:
        new_logical = new["logical_entry_identity"]
        new_revision = new["entry_revision_identity"]
        new_hash = _row_sha(new)
    return {
        "old_logical_entry_identity": old["logical_entry_identity"],
        "old_entry_revision_identity": old["entry_revision_identity"],
        "new_logical_entry_identity": new_logical,
        "new_entry_revision_identity": new_revision,
        "disposition": disposition,
        "reason": reason,
        "old_row_sha256": _row_sha(old),
        "new_row_sha256": new_hash,
    }


def reconcile(old_entries: list[dict[str, Any]], new_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Classify every old row using only exact identity and structure inputs."""
    new_by_logical = {row["logical_entry_identity"]: row for row in new_entries}
    new_by_revision = {row["entry_revision_identity"]: row for row in new_entries}
    # The formal v2-lite entry schema has no loader-order field (args_order is
    # semantic formatting metadata, not call adjacency). Revision identities
    # are content hashes, so their byte order is not evidence of source
    # adjacency. Until exact loader-order data is part of a catalog boundary,
    # changed logical identities are conservatively unmapped rather than
    # guessed from hash order.
    used_new: set[str] = set()
    result: list[dict[str, Any]] = []
    exact_rows: dict[str, dict[str, Any]] = {}
    changed_rows: dict[str, dict[str, Any]] = {}

    # Consume every exact logical/revision match before looking for moves.  A
    # later unchanged row must not be mistaken for a second move candidate.
    for old in old_entries:
        revision = old["entry_revision_identity"]
        exact = new_by_revision.get(revision)
        if exact is not None and exact["logical_entry_identity"] == old["logical_entry_identity"]:
            used_new.add(revision)
            exact_rows[revision] = exact
            continue
        logical = new_by_logical.get(old["logical_entry_identity"])
        if logical is not None:
            used_new.add(logical["entry_revision_identity"])
            changed_rows[revision] = logical
    for old in old_entries:
        revision = old["entry_revision_identity"]
        if revision in exact_rows:
            result.append(_mapping_row(old, exact_rows[revision], "unchanged", "unchanged"))
            continue
        if revision in changed_rows:
            logical = changed_rows[revision]
            result.append(_mapping_row(old, logical, "revision_changed", _reason_changed(old, logical)))
            continue
        structural = [row for row in new_entries
                      if row["entry_revision_identity"] not in used_new
                      and _structure(row) == _structure(old)]
        if len(structural) > 1:
            result.append(_mapping_row(old, None, "ambiguous", "ambiguous"))
            continue
        if not structural:
            result.append(_mapping_row(old, None, "removed", "removed"))
            continue
        # A unique structural candidate is still insufficient: the list order
        # of validated catalog rows is revision-hash order, not loader call
        # order.  Without an exact adjacency binding this is intentionally an
        # unmapped move and apply must stop for user adjudication.
        result.append(_mapping_row(old, None, "unmapped", "unmapped"))
    result.sort(key=lambda row: row["old_entry_revision_identity"].encode("ascii"))
    if len(result) != len(old_entries):
        raise _error("migration does not conserve old catalog rows")
    return result


def _identity_core(value: dict[str, Any]) -> dict[str, Any]:
    return {key: value[key] for key in sorted(MIGRATION_KEYS - {"migration_id", "target_path", "recorded_at", "recorded_by"})}


def _migration_id(value: dict[str, Any]) -> str:
    return _raw_sha(wp1.canonical_bytes(_identity_core(value)))


def _build_migration(base_commit: str, base_tree: str, old_summary: dict[str, Any], old_entries: list[dict[str, Any]],
                     new_summary: dict[str, Any], new_entries: list[dict[str, Any]], *, recorded_at: str,
                     recorded_by: str) -> dict[str, Any]:
    wp1.strict_utc_seconds(recorded_at)
    _nonempty(recorded_by, "recorded_by")
    rows = reconcile(old_entries, new_entries)
    value: dict[str, Any] = {
        "schema_version": 1,
        "kind": MIGRATION_KIND,
        "migration_id": "",
        "base_commit": base_commit,
        "base_tree": base_tree,
        "target_path": "",
        "old_catalog_id": old_summary["catalog_id"],
        "old_manifest_sha256": old_summary["manifest_sha256"],
        "old_entries_sha256": old_summary["entries_sha256"],
        "old_exclusions_sha256": old_summary["exclusions_sha256"],
        "old_counts": old_summary["counts"],
        "new_catalog_id": new_summary["catalog_id"],
        "new_manifest_sha256": new_summary["manifest_sha256"],
        "new_entries_sha256": new_summary["entries_sha256"],
        "new_exclusions_sha256": new_summary["exclusions_sha256"],
        "new_counts": new_summary["counts"],
        "old_rows": _snapshots(old_entries),
        "new_rows": _snapshots(new_entries),
        "rows": rows,
        "rows_sha256": _raw_sha(wp1.canonical_bytes(rows)),
        "recorded_at": recorded_at,
        "recorded_by": recorded_by,
    }
    value["migration_id"] = _migration_id(value)
    value["target_path"] = f"{MIGRATION_PREFIX}{value['migration_id']}{MIGRATION_SUFFIX}"
    return value


def validate_migration(value: object, *, target_path: str | None = None,
                       expected_new_entries: list[dict[str, Any]] | None = None,
                       expected_old_entries: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    row = _exact(value, MIGRATION_KEYS, "migration")
    if type(row["schema_version"]) is not int or row["schema_version"] != 1 or row["kind"] != MIGRATION_KIND:
        raise _error("migration schema or kind mismatch")
    migration_id = _sha(row["migration_id"], "migration_id")
    base_commit = _commit(row["base_commit"], "base_commit")
    if (not isinstance(row["base_tree"], str) or len(row["base_tree"]) != 40
            or any(c not in "0123456789abcdef" for c in row["base_tree"] or "")):
        raise _error("base_tree must be a lowercase Git tree")
    expected_target = f"{MIGRATION_PREFIX}{migration_id}{MIGRATION_SUFFIX}"
    if row["target_path"] != expected_target or (target_path is not None and row["target_path"] != target_path):
        raise _error("migration target path is not canonical")
    for key in ("old_catalog_id", "old_manifest_sha256", "old_entries_sha256", "old_exclusions_sha256",
                "new_catalog_id", "new_manifest_sha256", "new_entries_sha256", "new_exclusions_sha256"):
        _sha(row[key], key)
    old_counts = _counts(row["old_counts"], "old_counts")
    new_counts = _counts(row["new_counts"], "new_counts")
    old_rows = _validate_snapshots(row["old_rows"], "old_rows")
    new_rows = _validate_snapshots(row["new_rows"], "new_rows")
    if old_counts["entry_count"] != len(old_rows) or new_counts["entry_count"] != len(new_rows):
        raise _error("migration row/count mismatch")
    rows_value = row["rows"]
    if not isinstance(rows_value, list) or len(rows_value) != len(old_rows):
        raise _error("migration mapping rows do not conserve the old catalog")
    previous = ""
    seen: set[str] = set()
    old_by_revision = {item["entry_revision_identity"]: item for item in old_rows}
    new_by_revision = {item["entry_revision_identity"]: item for item in new_rows}
    mapped_new_revisions: set[str] = set()
    for index, item in enumerate(rows_value):
        mapping = _exact(item, MAPPING_KEYS, f"migration mapping row {index}")
        old_revision = _sha(mapping["old_entry_revision_identity"], "mapping old revision")
        old_logical = _sha(mapping["old_logical_entry_identity"], "mapping old logical")
        if old_revision <= previous or old_revision in seen:
            raise _error("migration mapping rows are not strictly ordered and unique")
        snapshot = old_by_revision.get(old_revision)
        if snapshot is None or snapshot["logical_entry_identity"] != old_logical:
            raise _error("migration mapping old row is not in old_rows")
        if mapping["old_row_sha256"] != snapshot["row_sha256"]:
            raise _error("migration old row hash drift")
        previous = old_revision
        seen.add(old_revision)
        disposition = mapping["disposition"]
        reason = mapping["reason"]
        if disposition not in DISPOSITIONS or reason not in REASONS:
            raise _error("migration disposition/reason is invalid")
        new_revision = mapping["new_entry_revision_identity"]
        new_logical = mapping["new_logical_entry_identity"]
        new_hash = mapping["new_row_sha256"]
        missing_target = new_revision is None or new_logical is None or new_hash is None
        if missing_target:
            if not (new_revision is None and new_logical is None and new_hash is None):
                raise _error("migration target must be all-null or fully bound")
            if disposition not in {"removed", "ambiguous", "unmapped"} or reason not in {"removed", "ambiguous", "unmapped"}:
                raise _error("migration target is missing for a mapped disposition")
        else:
            new_revision = _sha(new_revision, "mapping new revision")
            new_logical = _sha(new_logical, "mapping new logical")
            new_hash = _sha(new_hash, "mapping new row hash")
            snapshot = new_by_revision.get(new_revision)
            if snapshot is None or snapshot["logical_entry_identity"] != new_logical or snapshot["row_sha256"] != new_hash:
                raise _error("migration new row hash or identity drift")
            if new_revision in mapped_new_revisions:
                raise _error("migration maps more than one old row to a new revision")
            mapped_new_revisions.add(new_revision)
        if disposition == "unchanged":
            if reason != "unchanged" or new_revision != old_revision or new_logical != old_logical:
                raise _error("unchanged migration row is not exact")
        elif disposition == "revision_changed":
            if new_logical != old_logical or new_revision == old_revision or reason not in {
                    "target_changed", "source_changed", "fixed_source_changed", "terminology_changed",
                    "args_order_changed", "rules_changed"}:
                raise _error("revision_changed migration row is not exact")
        elif disposition == "logical_moved":
            if new_logical == old_logical or reason not in {"source_changed", "source_tag_changed", "call_locator_changed"}:
                raise _error("logical_moved migration row is not exact")
        elif disposition in {"removed", "ambiguous", "unmapped"}:
            if new_revision is not None or new_logical is not None or new_hash is not None or reason != disposition:
                raise _error(f"{disposition} migration row has an unexpected target")
    if seen != set(old_by_revision):
        raise _error("migration mapping rows do not exactly cover old_rows")
    if _raw_sha(wp1.canonical_bytes(rows_value)) != _sha(row["rows_sha256"], "rows_sha256"):
        raise _error("migration rows hash drift")
    if _migration_id(row) != migration_id:
        raise _error("migration_id does not bind migration inputs")
    if expected_old_entries is not None and _snapshots(expected_old_entries) != old_rows:
        raise _error("migration old catalog rows drift")
    if expected_new_entries is not None and _snapshots(expected_new_entries) != new_rows:
        raise _error("migration new catalog rows drift")
    if expected_old_entries is not None and expected_new_entries is not None:
        if reconcile(expected_old_entries, expected_new_entries) != rows_value:
            raise _error("migration classifications do not match the validated catalogs")
    _commit(row["base_commit"], "base_commit")
    wp1.strict_utc_seconds(row["recorded_at"])
    _nonempty(row["recorded_by"], "recorded_by")
    return row


def validate_migration_bytes(raw: bytes, *, target_path: str | None = None,
                             expected_new_entries: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    try:
        value = wp1.parse_canonical_object(raw, "migration")
    except wp1.ProductionReviewError:
        raise
    return validate_migration(value, target_path=target_path, expected_new_entries=expected_new_entries)


def _status_scope_clean(root: Path) -> None:
    raw = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--",
               "evidence/production-review-v2-lite", "i18n/quality/production-review-v2-lite")
    if raw:
        raise _error("migration requires clean tracked catalog/evidence worktree and index")


def _no_active_rows(root: Path, *, require_database: bool = False) -> None:
    from . import production_review_v2_lite_queue as queue
    database = queue.database_path(root)
    if not database.exists() or database.is_symlink():
        if require_database:
            raise _error("migration apply requires the existing SQLite queue")
        return
    try:
        connection = queue._connect(database)
        try:
            queue._schema_check(connection)
            active = connection.execute(
                "SELECT entry_revision_identity,state FROM state_override "
                "WHERE state IN ('reserved','screened','deep_required') ORDER BY entry_revision_identity").fetchall()
        finally:
            connection.close()
    except (OSError, sqlite3.Error, wp1.ProductionReviewError) as error:
        raise _error(f"cannot inspect queue for quiescence: {error}") from error
    if active:
        raise _error("migration requires no reserved/screened/deep_required queue rows")


def _quiescent(root: Path, *, require_database: bool = False) -> None:
    from . import production_review_v2_lite_queue as queue
    queue._no_checkpoint(root)
    _status_scope_clean(root)
    _no_active_rows(root, require_database=require_database)


def _safe_output(root: Path, output: Path) -> Path:
    absolute = catalog._reject_symlink_ancestors(
        Path(os.path.abspath(os.fspath(output))), label="migration output")
    current = Path(os.path.abspath(os.fspath(root)))
    if absolute == current:
        raise _error("migration output must be a file")
    try:
        relative = absolute.relative_to(current)
    except ValueError:
        relative = None
    if relative is not None:
        try:
            ignored = subprocess.run(["git", "check-ignore", "-q", "--no-index", str(relative)], cwd=root).returncode == 0
        except OSError as error:
            raise _error(f"cannot inspect migration output: {error}") from error
        if not ignored:
            raise _error("migration output inside the repository must be ignored")
    return absolute


def _write_output(root: Path, output: Path, raw: bytes) -> Path:
    destination = _safe_output(root, output)
    temporary: Path | None = None
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name("." + destination.name + ".tmp")
        if temporary.exists() or temporary.is_symlink():
            if temporary.is_symlink() or not temporary.is_file():
                raise _error("migration output temporary path is not an ordinary file")
            temporary.unlink()
        with temporary.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        wp1._fsync_directory(destination.parent)
    except (OSError, wp1.ProductionReviewError) as error:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
        if isinstance(error, wp1.ProductionReviewError):
            raise
        raise _error(f"cannot write migration artifact: {error}") from error
    return destination


def _report(value: dict[str, Any], *, path: Path | None = None) -> dict[str, Any]:
    counts = Counter(row["disposition"] for row in value["rows"])
    report: dict[str, Any] = {
        "migration_id": value["migration_id"],
        "target_path": value["target_path"],
        "old_catalog_id": value["old_catalog_id"],
        "new_catalog_id": value["new_catalog_id"],
        "base_commit": value["base_commit"],
        "old_counts": value["old_counts"],
        "new_counts": value["new_counts"],
        "dispositions": dict(sorted(counts.items())),
        "ambiguous": counts.get("ambiguous", 0),
        "unmapped": counts.get("unmapped", 0),
        "ok": not counts.get("ambiguous", 0) and not counts.get("unmapped", 0),
    }
    if path is not None:
        report["artifact"] = str(path)
    return report


def plan(root: Path, candidate_catalog: Path, *, treeish: str = "HEAD", recorded_at: str | None = None,
         recorded_by: str = "WP2L-5 EXECUTOR", output: Path | None = None) -> dict[str, Any]:
    from . import production_review_v2_lite_queue as queue
    with queue.writer_lock(root):
        _quiescent(root)
        commit, tree, _old_manifest, old_entries, _old_files, old_summary = _current_bundle(root, treeish)
        if queue.database_path(root).exists():
            queue.strict_check(root)
        _new_manifest, new_entries, _new_files, new_summary = _candidate_bundle(root, candidate_catalog)
        value = _build_migration(commit, tree, old_summary, old_entries, new_summary, new_entries,
                                 recorded_at=recorded_at or catalog.utc_now(), recorded_by=recorded_by)
        validate_migration(value, target_path=value["target_path"],
                           expected_old_entries=old_entries, expected_new_entries=new_entries)
        raw = wp1.canonical_bytes(value)
        destination = output or root / ".artifacts/i18n/production-review-v2-lite" / f"migration-{value['migration_id']}.json"
        path = _write_output(root, destination, raw)
        return _report(value, path=path)


def _load_input(root: Path, input_path: Path) -> dict[str, Any]:
    try:
        if input_path.is_symlink() or not input_path.is_file():
            raise _error("migration input is not an ordinary file")
        raw = input_path.read_bytes()
        value = wp1.parse_canonical_object(raw, "migration input")
    except (OSError, wp1.ProductionReviewError) as error:
        if isinstance(error, wp1.ProductionReviewError):
            raise
        raise _error(f"cannot read migration input: {error}") from error
    return validate_migration(value)


def _assert_old(value: dict[str, Any], root: Path) -> tuple[str, dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    commit, _tree, manifest, entries, files, summary = _current_bundle(root, "HEAD")
    if commit != value["base_commit"] or _tree_id(root, commit) != value["base_tree"]:
        raise _error("migration base commit/tree no longer names the current checkout")
    _summary_matches({
        "catalog_id": value["old_catalog_id"], "manifest_sha256": value["old_manifest_sha256"],
        "entries_sha256": value["old_entries_sha256"], "exclusions_sha256": value["old_exclusions_sha256"],
        "counts": value["old_counts"],
    }, summary, "old catalog")
    if _snapshots(entries) != value["old_rows"]:
        raise _error("migration old catalog rows no longer match the planned boundary")
    return commit, manifest, entries, summary


def _assert_new(root: Path, value: dict[str, Any], candidate_catalog: Path,
                old_entries: list[dict[str, Any]], *, label: str = "new catalog") -> list[dict[str, Any]]:
    """Re-read and validate the exact prospective boundary at the call site."""
    _manifest, entries, _files, summary = _candidate_bundle(root, candidate_catalog)
    _summary_matches({
        "catalog_id": value["new_catalog_id"], "manifest_sha256": value["new_manifest_sha256"],
        "entries_sha256": value["new_entries_sha256"], "exclusions_sha256": value["new_exclusions_sha256"],
        "counts": value["new_counts"],
    }, summary, label)
    if _snapshots(entries) != value["new_rows"]:
        raise _error(f"{label} rows no longer match the planned boundary")
    if reconcile(old_entries, entries) != value["rows"]:
        raise _error(f"migration classifications no longer match the planned boundary")
    return entries


def check(root: Path, input_path: Path, *, candidate_catalog: Path | None = None) -> dict[str, Any]:
    from . import production_review_v2_lite_queue as queue
    if candidate_catalog is None:
        raise _error("migration check requires the exact candidate catalog")
    with queue.writer_lock(root):
        _quiescent(root)
        value = _load_input(root, input_path)
        _commit, _manifest_old, old_entries, _summary_old = _assert_old(value, root)
        if queue.database_path(root).exists():
            queue.strict_check(root)
        _assert_new(root, value, candidate_catalog, old_entries)
        return _report(value, path=input_path)


def _migration_rows(value: dict[str, Any]) -> list[tuple[Any, ...]]:
    return [(row["old_logical_entry_identity"], row["old_entry_revision_identity"],
             row["new_logical_entry_identity"], row["new_entry_revision_identity"],
             row["disposition"], row["reason"], value["migration_id"])
            for row in value["rows"]]


def apply(root: Path, input_path: Path, *, candidate_catalog: Path | None = None) -> dict[str, Any]:
    from . import production_review_v2_lite_queue as queue
    if candidate_catalog is None:
        raise _error("migration apply requires the exact candidate catalog")
    with queue.writer_lock(root):
        _quiescent(root, require_database=True)
        value = _load_input(root, input_path)
        if any(row["disposition"] in {"ambiguous", "unmapped"} for row in value["rows"]):
            raise _error("migration contains ambiguous/unmapped rows; apply requires user adjudication")
        _commit_id, _manifest, old_entries, old_summary = _assert_old(value, root)
        _assert_new(root, value, candidate_catalog, old_entries)
        queue.strict_check(root)
        database = queue.database_path(root)
        connection: sqlite3.Connection | None = None
        try:
            connection = queue._connect(database)
            queue._schema_check(connection)
            meta = connection.execute("SELECT singleton,schema_version,catalog_id,evidence_head FROM meta").fetchone()
            if meta is None or tuple(meta[0:4]) != (1, 1, old_summary["catalog_id"], value["base_commit"]):
                raise _error("queue meta does not name the migration old boundary")
            actual = connection.execute("SELECT * FROM state_override ORDER BY entry_revision_identity").fetchall()
            old_ids = {row["entry_revision_identity"] for row in old_entries}
            if any(row[0] not in old_ids for row in actual):
                raise _error("queue contains an override outside the old catalog")
            by_old = {row[0]: row for row in actual}
            preserved = [by_old[row["old_entry_revision_identity"]]
                         for row in value["rows"]
                         if row["disposition"] == "unchanged" and row["old_entry_revision_identity"] in by_old]
            # The candidate is a prospective boundary and is not protected by
            # the repository lock.  Re-read it immediately before BEGIN so the
            # one transaction can never apply a boundary validated earlier.
            _assert_new(root, value, candidate_catalog, old_entries,
                        label="new catalog immediately before transaction")
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("DELETE FROM state_override")
            connection.execute("DELETE FROM reconciliation")
            connection.executemany("INSERT INTO state_override VALUES (?,?,?,?,?,?,?)", preserved)
            connection.executemany("INSERT INTO reconciliation VALUES (?,?,?,?,?,?,?)", _migration_rows(value))
            connection.execute("UPDATE meta SET catalog_id=?, evidence_head=?, rebuilt_at=? WHERE singleton=1",
                               (value["new_catalog_id"], value["base_commit"], catalog.utc_now()))
            connection.commit()
        except (sqlite3.Error, OSError, wp1.ProductionReviewError) as error:
            if connection is not None:
                try:
                    connection.rollback()
                except sqlite3.Error:
                    pass
            if isinstance(error, wp1.ProductionReviewError):
                raise
            raise _error(f"migration SQLite transaction rolled back: {error}") from error
        finally:
            if connection is not None:
                connection.close()
        try:
            with database.open("rb") as handle:
                os.fsync(handle.fileno())
        except OSError as error:
            raise _error(f"cannot fsync migrated queue: {error}") from error
        report = _report(value)
        report.update({"applied": True, "queued_successors": value["new_counts"]["entry_count"] - sum(
            1 for row in value["rows"] if row["disposition"] == "unchanged"), "ok": True})
        return report


def validate_repair_workset(value: object) -> dict[str, Any]:
    row = _exact(value, REPAIR_KEYS, "repair workset")
    if type(row["schema_version"]) is not int or row["schema_version"] != 1 or row["kind"] != REPAIR_KIND:
        raise _error("repair workset schema or kind mismatch")
    _batch_id(row["batch_id"])
    _commit(row["evidence_commit"], "repair evidence_commit")
    _sha(row["catalog_id"], "repair catalog_id")
    _sha(row["catalog_manifest_sha256"], "repair catalog manifest hash")
    _sha(row["policy_sha256"], "repair policy hash")
    items = row["items"]
    if not isinstance(items, list) or not items or len(items) > 80:
        raise _error("repair workset items must contain one to 80 rows")
    revisions: set[str] = set()
    for index, item in enumerate(items):
        item = _exact(item, REPAIR_ITEM_KEYS, f"repair workset item {index}")
        revision = _sha(item["entry_revision_identity"], "repair item revision")
        _sha(item["logical_entry_identity"], "repair item logical")
        preimage_hash = _sha(item["target_preimage_sha256"], "repair target preimage hash")
        if preimage_hash != _raw_sha(item["target_preimage"].encode("utf-8")):
            raise _error("repair target preimage hash drift")
        if revision in revisions:
            raise _error("repair workset contains duplicate revisions")
        revisions.add(revision)
        if any(not isinstance(item[key], str) for key in
               ("component", "normalized_path", "section", "source", "target_preimage",
                "source_tag", "call_locator", "fixed_source_identity",
                "terminology_snapshot_sha256", "rules_version")):
            raise _error("repair workset item contains a non-string source identity")
        winner = item["winner_evidence"]
        if not isinstance(winner, dict):
            raise _error("repair workset item lacks winner evidence")
        _sha(winner.get("observation_identity"), "repair winner observation identity")
        proposed = item["proposed_successor_input"]
        if not isinstance(proposed, dict) or proposed.get("parent_entry_revision_identity") != revision:
            raise _error("repair workset successor input is not bound to its parent")
    if _raw_sha(wp1.canonical_bytes(items)) != _sha(row["items_sha256"], "repair items hash"):
        raise _error("repair workset items hash drift")
    wp1.strict_utc_seconds(row["recorded_at"])
    _nonempty(row["recorded_by"], "repair workset recorded_by")
    return row


def _batch_id(value: object) -> str:
    if (not isinstance(value, str) or not value or value in {".", ".."}
            or "/" in value or "\\" in value or value != Path(value).name):
        raise _error("batch_id is not a canonical path component")
    return value


def _validate_live_repair_preimage(root: Path, expected_manifest: dict[str, Any],
                                   expected_entries: list[dict[str, Any]],
                                   expected_exclusions: list[dict[str, Any]],
                                   manifest: Any | None) -> None:
    """Re-harvest the live locale before producing a repair workset.

    The repair workset is deliberately created before the maintainer edits a
    translation.  It therefore binds the committed catalog target as a
    preimage, but also proves that the current loader still sees the same call,
    source/tag/path and target.  A later dirty translation is allowed only
    after this function has completed.
    """
    if manifest is None:
        from .config import load_manifest
        try:
            manifest = load_manifest()
        except Exception as error:
            raise _error(f"repair preflight cannot load the live version manifest: {error}") from error
    try:
        live_root = Path(manifest.root).resolve()
    except (AttributeError, OSError, TypeError) as error:
        raise _error(f"repair preflight live manifest has no usable repository root: {error}") from error
    if live_root != root.resolve():
        raise _error("repair preflight live manifest root does not match the current repository")
    try:
        if hashlib.sha256(manifest.raw_bytes).hexdigest() != expected_manifest["manifest_sha256"]:
            raise _error("repair preflight live version manifest identity drift")
        sources = wp1.source_identities_from_manifest(manifest)
        if sources != expected_manifest["source_identities"]:
            raise _error("repair preflight live source identity drift")
        terminology = wp1.terminology_snapshot(root)
        if terminology != expected_manifest["terminology_snapshot_sha256"]:
            raise _error("repair preflight live terminology identity drift")
        contract_path = root / expected_manifest["loader_contract_path"]
        contract_raw = contract_path.read_bytes()
        if hashlib.sha256(contract_raw).hexdigest() != expected_manifest["loader_contract_sha256"]:
            raise _error("repair preflight live loader contract drift")
        runtime = catalog.LuaRuntime(manifest).doctor()
        if runtime.get("lua_version") != expected_manifest["lua_runtime"]:
            raise _error("repair preflight live Lua runtime identity drift")
        occurrences = wp1.load_occurrences(manifest)
        live_entries, live_exclusions = catalog.formal_rows(
            occurrences, terminology=terminology, sources=sources,
            rules_version=expected_manifest["rules_version"])
    except wp1.ProductionReviewError:
        raise
    except Exception as error:
        raise _error(f"repair preflight live translation harvest failed: {error}") from error
    if live_entries != expected_entries or live_exclusions != expected_exclusions:
        raise _error("repair preflight live translation call/preimage/identity drift")


def _repair_workset(root: Path, batch_id: str, *, manifest: Any | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    from . import production_review_v2_lite_queue as queue
    batch_id = _batch_id(batch_id)
    commit = _head(root, "HEAD")
    catalog_manifest, entries, files = queue._catalog_from_tree(root, commit)
    exclusions = wp1.parse_jsonl(files[f"{catalog.CATALOG_PREFIX}/exclusions.jsonl"], "catalog exclusions")
    tree = queue._tree(root, commit)
    batch_root = f"{queue.BATCH_PREFIX}{batch_id}"
    manifest_path = f"{batch_root}/manifest.json"
    if manifest_path not in tree:
        raise _error("repair preflight requires a committed batch manifest")
    # Validate the named batch against the catalog that was current at its own
    # base commit before consulting the live current catalog.  This preserves
    # the historical row identity needed to compare it with today's winner.
    batch_manifest = queue._exact(
        wp1.parse_canonical_object(queue._ordinary_blob(root, tree, manifest_path), "repair batch manifest"),
        queue.BATCH_MANIFEST_KEYS, "repair batch manifest")
    source_manifest, source_entries, _source_files = queue._catalog_from_tree(
        root, batch_manifest["base_commit"])
    if source_manifest["catalog_id"] != batch_manifest["catalog_id"]:
        raise _error("repair batch base commit does not name its catalog")
    publication, tuples = queue._batch_rows(
        root, commit, manifest_path, source_manifest,
        {row["entry_revision_identity"]: row for row in source_entries})
    # A named batch is usable for repair only while every repair row remains
    # the current durable winner.  In particular, a later done/blocked batch
    # must not be hidden by asking for the older batch by name.
    current_projection = queue._projection(root, commit)
    current_winners = {row[0]: row for row in current_projection[3]}
    repair_tuples = [row for row in tuples if row[2] == "repair_required" and row[3] == batch_id]
    for winner in repair_tuples:
        current = current_winners.get(winner[0])
        if current != winner:
            raise _error("named repair batch rows are not the current durable winners")
    if not repair_tuples:
        raise _error("requested batch has no committed repair_required winner")
    # Only after the historical batch and current durable winner agree do we
    # validate the live current unchanged preimage.
    _validate_live_repair_preimage(root, catalog_manifest, entries, exclusions, manifest)
    if publication != commit:
        # The current tree is the durable source; a descendant publication is
        # allowed by replay, but its exact publication commit is the evidence
        # anchor returned by _batch_rows.
        evidence_commit = publication
    else:
        evidence_commit = commit
    results_raw = queue._ordinary_blob(root, tree, f"{batch_root}/results.jsonl")
    adjudications_raw = queue._ordinary_blob(root, tree, f"{batch_root}/adjudications.jsonl")
    results = wp1.parse_jsonl(results_raw, "repair batch results")
    adjudications = wp1.parse_jsonl(adjudications_raw, "repair batch adjudications")
    by_revision = {row["entry_revision_identity"]: row for row in results}
    by_adjud_revision: dict[str, list[dict[str, Any]]] = {}
    for row in adjudications:
        if row.get("repair_required") is True:
            by_adjud_revision.setdefault(row.get("entry_revision_identity"), []).append(row)
    entries_by_revision = {row["entry_revision_identity"]: row for row in entries}
    items: list[dict[str, Any]] = []
    for override in sorted(repair_tuples, key=lambda row: row[0].encode("ascii")):
        revision, logical, _state, _batch, _attempt, result_hash, _updated = override
        result = by_revision.get(revision)
        entry = entries_by_revision.get(revision)
        if result is None or entry is None or result.get("final_state") != "repair_required":
            raise _error("repair winner result is missing or no longer a repair row")
        if result_hash != _raw_sha(wp1.canonical_bytes(result)):
            raise _error("repair winner result hash drift")
        repair_rows = by_adjud_revision.get(revision)
        if not repair_rows:
            raise _error("repair winner lacks committed repair adjudication")
        winner = sorted(repair_rows, key=lambda row: row.get("observation_identity", ""))[0]
        if winner.get("disposition") != "confirmed" or winner.get("repair_required") is not True:
            raise _error("repair winner adjudication is not confirmed")
        if entry["logical_entry_identity"] != logical:
            raise _error("repair queue logical identity drift")
        items.append({
            "entry_revision_identity": revision,
            "logical_entry_identity": logical,
            "component": entry["component"],
            "normalized_path": entry["normalized_path"],
            "section": entry["section"],
            "source": entry["source"],
            "target_preimage": entry["target"],
            "target_preimage_sha256": entry["target_sha256"],
            "source_tag": entry["source_tag"],
            "call_locator": entry["call_locator"],
            "fixed_source_identity": entry["fixed_source_identity"],
            "terminology_snapshot_sha256": entry["terminology_snapshot_sha256"],
            "rules_version": entry["rules_version"],
            "winner_evidence": {
                "batch_id": batch_id,
                "publication_commit": evidence_commit,
                "manifest_path": manifest_path,
                "results_path": f"{batch_root}/results.jsonl",
                "adjudications_path": f"{batch_root}/adjudications.jsonl",
                "result_sha256": result_hash,
                "observation_identity": winner.get("observation_identity"),
                "evidence_path": winner.get("evidence_path"),
                "evidence_commit": winner.get("evidence_commit"),
            },
            "proposed_successor_input": {
                "parent_entry_revision_identity": revision,
                "logical_entry_identity": logical,
                "component": entry["component"],
                "normalized_path": entry["normalized_path"],
                "section": entry["section"],
                "source": entry["source"],
                "source_tag": entry["source_tag"],
                "call_locator": entry["call_locator"],
                "fixed_source_identity": entry["fixed_source_identity"],
                "terminology_snapshot_sha256": entry["terminology_snapshot_sha256"],
                "rules_version": entry["rules_version"],
                "target_preimage_sha256": entry["target_sha256"],
            },
        })
    workset = {
        "schema_version": 1,
        "kind": REPAIR_KIND,
        "batch_id": batch_id,
        "evidence_commit": evidence_commit,
        "catalog_id": catalog_manifest["catalog_id"],
        "catalog_manifest_sha256": _raw_sha(queue._ordinary_blob(root, tree, f"{catalog.CATALOG_PREFIX}/manifest.json")),
        "policy_sha256": catalog_manifest["policy_sha256"],
        "items": items,
        "items_sha256": _raw_sha(wp1.canonical_bytes(items)),
        "recorded_at": catalog.utc_now(),
        "recorded_by": "WP2L-5 EXECUTOR",
    }
    validate_repair_workset(workset)
    return workset, items


def repair_preflight(root: Path, batch_id: str, *, output: Path | None = None,
                     manifest: Any | None = None) -> dict[str, Any]:
    from . import production_review_v2_lite_queue as queue
    with queue.writer_lock(root):
        _quiescent(root, require_database=True)
        queue.strict_check(root)
        workset, items = _repair_workset(root, batch_id, manifest=manifest)
        raw = wp1.canonical_bytes(workset)
        destination = output or root / ".artifacts/i18n/production-review-v2-lite" / f"repair-preflight-{_batch_id(batch_id)}.json"
        path = _write_output(root, destination, raw)
        return {"batch_id": batch_id, "items": len(items), "workset": str(path),
                "catalog_id": workset["catalog_id"], "evidence_commit": workset["evidence_commit"], "ok": True}


def reconciliation_rows_for_tree(root: Path, tree: dict[str, tuple[str, str, str]],
                                 manifest: dict[str, Any], entries: list[dict[str, Any]]) -> list[tuple[Any, ...]]:
    """Return the most recent boundary rows for queue projection replay."""
    candidates: list[dict[str, Any]] = []
    from . import production_review_v2_lite_queue as queue
    for path in sorted(tree):
        if not path.startswith(MIGRATION_PREFIX) or not path.endswith(MIGRATION_SUFFIX):
            continue
        relative = path[len(MIGRATION_PREFIX):]
        if not relative or "/" in relative:
            raise _error("migration evidence path is not a direct canonical file")
        raw = queue._ordinary_blob(root, tree, path)
        value = validate_migration_bytes(raw, target_path=path)
        candidates.append(value)
    matching = [value for value in candidates if value["new_catalog_id"] == manifest["catalog_id"]]
    if len(matching) > 1:
        raise _error("more than one migration boundary targets the current catalog")
    if not matching:
        return []
    value = matching[0]
    # Revalidate the actual boundary from Git, not just the artifact's row
    # snapshots.  This makes a committed artifact's semantic classifications
    # fail closed even after the candidate directory has disappeared.
    old_manifest, old_entries, old_files = queue._catalog_from_tree(root, value["base_commit"])
    if (old_manifest["catalog_id"] != value["old_catalog_id"] or
            _raw_sha(old_files[f"{catalog.CATALOG_PREFIX}/manifest.json"]) != value["old_manifest_sha256"] or
            old_manifest["entries_sha256"] != value["old_entries_sha256"] or
            old_manifest["exclusions_sha256"] != value["old_exclusions_sha256"]):
        raise _error("migration base catalog no longer matches its Git boundary")
    validate_migration(value, expected_old_entries=old_entries, expected_new_entries=entries)
    return _migration_rows(value)
