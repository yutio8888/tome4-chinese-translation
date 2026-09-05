"""Registration and handlers for production commands."""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any
from .errors import I18nToolError
from . import production_review
from . import production_review_v2_lite
from . import production_review_v2_lite_queue
from . import production_review_v2_lite_batch
from . import production_review_v2_lite_migration
from .runtime import LuaRuntime
from .cli_common import _add_common_arguments, _manifest, _print_json


def register(subparsers: argparse._SubParsersAction) -> None:
    production = subparsers.add_parser(
        "production", help="non-authoritative production-review shadow calibration",
    )
    production_sub = production.add_subparsers(dest="production_command", required=True)
    authoritative = production_sub.add_parser("authoritative-catalog", help="formal WP2-Lite catalog candidate")
    authoritative_sub = authoritative.add_subparsers(dest="production_action", required=True)
    authoritative_build = authoritative_sub.add_parser("build")
    _add_common_arguments(authoritative_build)
    authoritative_build.add_argument("--output", required=True, type=Path)
    authoritative_build.add_argument("--recorded-at")
    authoritative_build.add_argument("--recorded-by", default="WP2L-1 EXECUTOR")
    authoritative_check = authoritative_sub.add_parser("check")
    _add_common_arguments(authoritative_check)
    authoritative_check.add_argument("--candidate-catalog", required=True, type=Path)
    retirement = production_sub.add_parser("wp1-retirement", help="read-only exact WP1 retirement preflight")
    retirement_sub = retirement.add_subparsers(dest="production_action", required=True)
    retirement_preflight = retirement_sub.add_parser("preflight")
    _add_common_arguments(retirement_preflight)
    retirement_preflight.add_argument("--candidate-catalog", required=True, type=Path)
    queue = production_sub.add_parser("queue", help="rebuildable WP2-Lite SQLite projection")
    queue_sub = queue.add_subparsers(dest="production_action", required=True)
    queue_sub.add_parser("init")
    queue_rebuild = queue_sub.add_parser("rebuild")
    queue_rebuild.add_argument("--treeish", default="HEAD")
    queue_sub.add_parser("check")
    queue_status = queue_sub.add_parser("status")
    queue_status.add_argument("--json", action="store_true")
    batch = production_sub.add_parser("batch", help="single WP2-Lite active batch")
    batch_sub = batch.add_subparsers(dest="production_action", required=True)
    batch_start = batch_sub.add_parser("start")
    batch_start.add_argument("--limit", type=int, default=80)
    batch_start.add_argument("--retry-blocked", action="store_true")
    batch_sub.add_parser("show")
    batch_abandon = batch_sub.add_parser("abandon")
    batch_abandon.add_argument("--discard-uncommitted-results", action="store_true")
    batch_abandon.add_argument("--restore-evidence", action="store_true")
    recover = batch_sub.add_parser("recover")
    recover.add_argument("--from-head", action="store_true")
    batch_sub.add_parser("surface-export")
    batch_import = batch_sub.add_parser("surface-import")
    batch_import.add_argument("--input", required=True, type=Path)
    batch_sub.add_parser("contextual-export")
    contextual_import = batch_sub.add_parser("contextual-import")
    contextual_import.add_argument("--input", required=True, type=Path)
    adjudicate = batch_sub.add_parser("adjudicate")
    adjudicate.add_argument("--input", required=True, type=Path)
    batch_sub.add_parser("prepare-evidence")
    finalize = batch_sub.add_parser("finalize")
    finalize.add_argument("--commit", required=True)
    batch_sub.add_parser("recover-from-head")
    migration = production_sub.add_parser("migration", help="quiescent catalog migration")
    migration_sub = migration.add_subparsers(dest="production_action", required=True)
    migration_plan = migration_sub.add_parser("plan")
    migration_plan.add_argument("--candidate-catalog", required=True, type=Path)
    migration_plan.add_argument("--output", type=Path)
    migration_plan.add_argument("--recorded-at")
    migration_plan.add_argument("--recorded-by", default="WP2L-5 EXECUTOR")
    migration_check = migration_sub.add_parser("check")
    migration_check.add_argument("--input", required=True, type=Path)
    migration_check.add_argument("--candidate-catalog", required=True, type=Path)
    migration_apply = migration_sub.add_parser("apply")
    migration_apply.add_argument("--input", required=True, type=Path)
    migration_apply.add_argument("--candidate-catalog", required=True, type=Path)
    repair = production_sub.add_parser("repair", help="committed repair preflight")
    repair_sub = repair.add_subparsers(dest="production_action", required=True)
    repair_preflight = repair_sub.add_parser("preflight")
    _add_common_arguments(repair_preflight)
    repair_preflight.add_argument("--batch-id", required=True)
    repair_preflight.add_argument("--output", type=Path)
    locator = production_sub.add_parser("locator", help="production locator snapshot")
    locator_sub = locator.add_subparsers(dest="production_action", required=True)
    locator_bootstrap = locator_sub.add_parser("bootstrap")
    _add_common_arguments(locator_bootstrap)
    locator_bootstrap.add_argument("--recorded-at", required=True)
    locator_bootstrap.add_argument("--recorded-by", required=True)
    locator_check = locator_sub.add_parser("check")
    locator_check.add_argument("--snapshot", required=True, type=Path)
    locator_check.add_argument("--occurrences", required=True, type=Path)
    locator_check.add_argument("--locators", required=True, type=Path)
    catalog = production_sub.add_parser("catalog", help="production catalog shadow snapshot")
    catalog_sub = catalog.add_subparsers(dest="production_action", required=True)
    catalog_build = catalog_sub.add_parser("build")
    catalog_check = catalog_sub.add_parser("check")
    _add_common_arguments(catalog_build)
    _add_common_arguments(catalog_check)
    for item in (catalog_build, catalog_check):
        item.add_argument("--locator-snapshot", required=True, type=Path)
        item.add_argument("--occurrences", required=True, type=Path)
        item.add_argument("--locators", required=True, type=Path)
        if item is catalog_build:
            item.add_argument("--recorded-at", required=True)
            item.add_argument("--recorded-by", required=True)
        else:
            item.add_argument("--catalog", required=True, type=Path)
            item.add_argument("--entries", required=True, type=Path)
            item.add_argument("--exclusions", required=True, type=Path)
    policy = production_sub.add_parser("shadow-policy", help="shadow queue policy")
    policy_sub = policy.add_subparsers(dest="production_action", required=True)
    policy_build = policy_sub.add_parser("build")
    policy_check = policy_sub.add_parser("check")
    for item in (policy_build, policy_check):
        for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions"):
            item.add_argument(f"--{flag}", required=True, type=Path)
        item.add_argument("--manifest", type=Path)
        item.add_argument("--version-manifest", default="tome-1.7.6")
        if item is policy_check: item.add_argument("--policy", required=True, type=Path)
    journal = production_sub.add_parser("shadow-journal", help="one-shot shadow journal")
    journal_sub = journal.add_subparsers(dest="production_action", required=True)
    journal_bootstrap = journal_sub.add_parser("bootstrap")
    journal_check = journal_sub.add_parser("check")
    for item in (journal_bootstrap, journal_check):
        for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions", "policy"):
            item.add_argument(f"--{flag}", required=True, type=Path)
        item.add_argument("--manifest", type=Path); item.add_argument("--version-manifest", default="tome-1.7.6")
        if item is journal_bootstrap:
            item.add_argument("--recorded-at", required=True)
            item.add_argument("--recorded-by", required=True)
        else:
            for flag in ("group", "events", "checkpoint"):
                item.add_argument(f"--{flag}", required=True, type=Path)
    replay = production_sub.add_parser("replay", help="replay shadow journal")
    for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions", "policy", "group", "events", "checkpoint"):
        replay.add_argument(f"--{flag}", required=True, type=Path)
    replay.add_argument("--manifest", type=Path)
    replay.add_argument("--version-manifest", default="tome-1.7.6")
    replay.add_argument("--detail", action="store_true", help="include queued revision IDs")
    batch = production_sub.add_parser("batch-draft", help="build a non-dispatchable shadow draft")
    batch.add_argument("--shadow", action="store_true", required=True)
    for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions", "policy", "group", "events", "checkpoint"):
        batch.add_argument(f"--{flag}", required=True, type=Path)
    batch.add_argument("--manifest", type=Path)
    batch.add_argument("--version-manifest", default="tome-1.7.6")
    reconcile = production_sub.add_parser("reconciliation", help="shadow conservation and live-drift report")
    _add_common_arguments(reconcile)
    reconcile.add_argument("action", choices=("report",))
    for flag in ("locator-snapshot", "occurrences", "locators", "catalog", "entries", "exclusions",
                 "policy", "group", "events", "checkpoint", "batch"):
        reconcile.add_argument(f"--{flag}", required=True, type=Path)
    production.set_defaults(handler=dispatch)


def dispatch(arguments: argparse.Namespace) -> int:
    if arguments.command == "production":
        return _production(arguments)
    raise AssertionError(f"unhandled command: {arguments.command}")


def _production_bytes(path: Path, label: str) -> bytes:
    try:
        if not path.is_file() or path.is_symlink():
            raise production_review.ProductionReviewError(f"{label} is not an ordinary file: {path}")
        return path.read_bytes()
    except OSError as error:
        raise production_review.ProductionReviewError(f"cannot read {label}: {path}: {error}") from error


def _production_read(path: Path, label: str = "artifact") -> Any:
    return production_review.parse_canonical_object(_production_bytes(path, label), label)


def _production(arguments: argparse.Namespace) -> int:
    configured_root = os.environ.get("I18N_REPOSITORY_ROOT")
    root = (Path(configured_root).resolve() if configured_root else
            Path(__file__).resolve().parents[2])
    if not root.is_dir():
        raise production_review.ProductionReviewError(
            f"repository root is not an ordinary directory: {root}")
    evidence = root / "evidence" / "production-review"
    quality = root / "i18n" / "quality" / "production-review"
    command, action = arguments.production_command, getattr(arguments, "production_action", None)

    def snapshot_inputs(*, operational: bool = True) -> tuple[dict[str, Any], bytes, bytes, bytes]:
        manifest_raw = _production_bytes(arguments.locator_snapshot, "locator manifest")
        value = production_review.parse_canonical_object(manifest_raw, "locator manifest")
        occurrences = _production_bytes(arguments.occurrences, "occurrences")
        locators = _production_bytes(arguments.locators, "locators")
        production_review.check_locator_snapshot(value, occurrences, locators)
        if operational:
            production_review.check_locator_snapshot_live(value, occurrences, locators, _manifest(arguments))
        return value, manifest_raw, occurrences, locators

    def catalog_inputs(*, operational: bool = True) -> tuple[dict[str, Any], bytes, list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
        locator, locator_raw, occurrences, locators = snapshot_inputs(operational=operational)
        expected_terminology = None
        expected_sources = None
        if operational:
            manifest = _manifest(arguments)
            expected_terminology = production_review.terminology_snapshot(root)
            expected_sources = production_review.source_identities_from_manifest(manifest)
        raw = _production_bytes(arguments.catalog, "catalog manifest")
        value = production_review.parse_canonical_object(raw, "catalog manifest")
        entries, exclusions = production_review.check_catalog(
            value, _production_bytes(arguments.entries, "catalog entries"),
            _production_bytes(arguments.exclusions, "catalog exclusions"),
            locator_manifest=locator, locator_manifest_raw=locator_raw,
            occurrences_raw=occurrences, locators_raw=locators,
            expected_terminology_snapshot_id=expected_terminology,
            expected_source_identities=expected_sources,
            require_current_rules=operational)
        return value, raw, entries, exclusions, locator

    def policy_input(catalog: dict[str, Any], catalog_raw: bytes, locator: dict[str, Any]) -> dict[str, Any]:
        return production_review.check_shadow_policy(
            _production_read(arguments.policy, "shadow policy"), catalog=catalog,
            catalog_manifest_raw=catalog_raw, locator_manifest=locator)

    def journal_inputs(catalog: dict[str, Any], catalog_raw: bytes, entries: list[dict[str, Any]],
                       exclusions: list[dict[str, Any]], policy: dict[str, Any], locator: dict[str, Any]):
        group = _production_read(arguments.group, "journal group")
        raw = _production_bytes(arguments.events, "journal events")
        checkpoint = _production_read(arguments.checkpoint, "journal checkpoint")
        replayed = production_review.check_shadow_journal(
            group, raw, checkpoint, catalog=catalog, catalog_manifest_raw=catalog_raw,
            locator_manifest=locator, entries=entries, exclusions=exclusions, policy=policy)
        return group, raw, checkpoint, replayed

    if command == "authoritative-catalog" and action == "build":
        manifest = _manifest(arguments)
        files = production_review_v2_lite.build_catalog(
            manifest, recorded_at=arguments.recorded_at or production_review_v2_lite.utc_now(),
            recorded_by=arguments.recorded_by)
        production_review_v2_lite.write_candidate(files, arguments.output, repository_root=root)
        value = production_review_v2_lite.check_catalog_tree(arguments.output, manifest)
        report = {"catalog_id": value["catalog_id"], "occurrences": value["occurrence_count"],
                  "entries": value["entry_count"], "exclusions": value["exclusion_count"],
                  "directory": str(arguments.output), "bytes": sum(map(len, files.values()))}
    elif command == "authoritative-catalog" and action == "check":
        value = production_review_v2_lite.check_catalog_tree(arguments.candidate_catalog, _manifest(arguments))
        report = {"catalog_id": value["catalog_id"], "occurrences": value["occurrence_count"],
                  "entries": value["entry_count"], "exclusions": value["exclusion_count"], "ok": True}
    elif command == "wp1-retirement" and action == "preflight":
        report = production_review_v2_lite.retirement_preflight(
            root, arguments.candidate_catalog, _manifest(arguments))
    elif command == "queue":
        if action == "init":
            report = production_review_v2_lite_queue.init(root)
        elif action == "rebuild":
            report = production_review_v2_lite_queue.rebuild(root, treeish=arguments.treeish)
        elif action == "check":
            report = production_review_v2_lite_queue.check(root)
        elif action == "status":
            report = production_review_v2_lite_queue.status(root)
        else:
            raise AssertionError(f"unhandled queue action: {action}")
    elif command == "batch":
        if action == "start":
            report = production_review_v2_lite_batch.start(root, limit=arguments.limit, retry_blocked=arguments.retry_blocked)
        elif action == "show":
            report = production_review_v2_lite_batch.show(root)
        elif action == "abandon":
            report = production_review_v2_lite_batch.abandon(root, discard_uncommitted_results=arguments.discard_uncommitted_results, restore_evidence=arguments.restore_evidence)
        elif action == "recover":
            report = (production_review_v2_lite_batch.recover_from_head(root)
                      if arguments.from_head else production_review_v2_lite_batch.recover(root))
        elif action == "surface-export":
            report = production_review_v2_lite_batch.surface_export(root)
        elif action == "surface-import":
            try:
                values = json.loads(arguments.input.read_text(encoding="utf-8"))
                if not isinstance(values, dict):
                    raise ValueError("surface import index must be an object")
                outputs = {key: (Path(value).read_bytes() if isinstance(value, str) and Path(value).is_file() else value) for key, value in values.items()}
            except (OSError, UnicodeError, ValueError, TypeError) as error:
                raise production_review.ProductionReviewError(f"invalid surface import input: {error}") from error
            report = production_review_v2_lite_batch.surface_import(root, outputs)
        elif action == "contextual-export":
            report = production_review_v2_lite_batch.contextual_export(root)
        elif action == "contextual-import":
            try:
                values = json.loads(arguments.input.read_text(encoding="utf-8"))
                outputs = {key: (Path(value).read_bytes() if isinstance(value, str) and Path(value).is_file() else value) for key, value in values.items()}
            except (OSError, UnicodeError, ValueError, TypeError) as error:
                raise production_review.ProductionReviewError(f"invalid contextual import input: {error}") from error
            report = production_review_v2_lite_batch.contextual_import(root, outputs)
        elif action == "adjudicate":
            report = production_review_v2_lite_batch.adjudicate(root, arguments.input)
        elif action == "prepare-evidence":
            report = production_review_v2_lite_batch.prepare_evidence(root)
        elif action == "finalize":
            report = production_review_v2_lite_batch.finalize(root, arguments.commit)
        elif action == "recover-from-head":
            report = production_review_v2_lite_batch.recover_from_head(root)
        else:
            raise AssertionError(f"unhandled batch action: {action}")
    elif command == "migration" and action == "plan":
        report = production_review_v2_lite_migration.plan(
            root, arguments.candidate_catalog, recorded_at=arguments.recorded_at,
            recorded_by=arguments.recorded_by, output=arguments.output)
    elif command == "migration" and action == "check":
        report = production_review_v2_lite_migration.check(
            root, arguments.input, candidate_catalog=arguments.candidate_catalog)
    elif command == "migration" and action == "apply":
        report = production_review_v2_lite_migration.apply(
            root, arguments.input, candidate_catalog=arguments.candidate_catalog)
    elif command == "repair" and action == "preflight":
        report = production_review_v2_lite_migration.repair_preflight(
            root, arguments.batch_id, output=arguments.output, manifest=_manifest(arguments))
    elif command == "locator" and action == "bootstrap":
        manifest = _manifest(arguments)
        value, occurrences, locators = production_review.build_locator_snapshot(
            manifest, recorded_at=arguments.recorded_at, recorded_by=arguments.recorded_by)
        directory = evidence / "locator-snapshots" / value["locator_snapshot_id"]
        production_review.atomic_publish_directory({"manifest.json": production_review.canonical_bytes(value),
            "occurrences.jsonl": occurrences, "locators.jsonl": locators}, directory,
            root=root, budget=production_review.BUDGETS["locator"], category="locator")
        report = {"locator_snapshot_id": value["locator_snapshot_id"], "occurrences": value["occurrences_count"],
            "locators": value["locators_count"], "directory": str(directory),
            "bytes": len(occurrences)+len(locators)+len(production_review.canonical_bytes(value))}
    elif command == "locator" and action == "check":
        value = _production_read(arguments.snapshot, "locator manifest")
        occurrences, locators = production_review.check_locator_snapshot(
            value, _production_bytes(arguments.occurrences, "occurrences"), _production_bytes(arguments.locators, "locators"))
        report = {"locator_snapshot_id": value["locator_snapshot_id"], "occurrences": len(occurrences),
            "locators": len(locators), "ok": True}
    elif command == "catalog" and action == "build":
        locator_manifest, locator_manifest_raw, occurrences, locators = snapshot_inputs()
        value, entries_raw, exclusions_raw = production_review.build_catalog(locator_manifest,
            occurrences, locators, locator_manifest_raw=locator_manifest_raw,
            terminology_snapshot_id=production_review.terminology_snapshot(root),
            source_identities=production_review.source_identities_from_manifest(_manifest(arguments)),
            recorded_at=arguments.recorded_at, recorded_by=arguments.recorded_by)
        directory = evidence / "catalogs" / value["catalog_id"]
        production_review.atomic_publish_directory({"manifest.json": production_review.canonical_bytes(value),
            "entries.jsonl": entries_raw, "exclusions.jsonl": exclusions_raw}, directory,
            root=root, budget=production_review.BUDGETS["catalog"], category="catalog")
        report = {"catalog_id": value["catalog_id"], "entries": value["entry_count"],
            "exclusions": value["exclusion_count"], "directory": str(directory),
            "bytes": len(entries_raw)+len(exclusions_raw)+len(production_review.canonical_bytes(value))}
    elif command == "catalog" and action == "check":
        locator_manifest, locator_manifest_raw, occurrences, locators = snapshot_inputs()
        manifest = _manifest(arguments)
        value = _production_read(arguments.catalog, "catalog manifest")
        entries, exclusions = production_review.check_catalog(value, _production_bytes(arguments.entries, "catalog entries"),
            _production_bytes(arguments.exclusions, "catalog exclusions"), locator_manifest=locator_manifest,
            locator_manifest_raw=locator_manifest_raw, occurrences_raw=occurrences, locators_raw=locators,
            expected_terminology_snapshot_id=production_review.terminology_snapshot(root),
            expected_source_identities=production_review.source_identities_from_manifest(manifest),
            require_current_rules=True)
        report = {"catalog_id": value["catalog_id"], "entries": len(entries), "exclusions": len(exclusions), "ok": True}
    elif command == "shadow-policy":
        catalog, catalog_raw, entries, exclusions, locator_manifest = catalog_inputs()
        if action == "build":
            value = production_review.build_shadow_policy(catalog, locator_manifest,
                catalog_manifest_raw=catalog_raw, terminology_snapshot_id=catalog["terminology_snapshot_id"],
                source_identities=catalog["source_identities"], recorded_at=catalog["recorded_at"],
                recorded_by=catalog["recorded_by"])
            directory = quality / "shadow-policies" / value["shadow_policy_id"]
            production_review.atomic_publish_directory({"policy.json": production_review.canonical_bytes(value)},
                directory, root=root, budget=production_review.BUDGETS["policy"], category="policy")
            report = {"shadow_policy_id": value["shadow_policy_id"], "directory": str(directory),
                "bytes": len(production_review.canonical_bytes(value))}
        else:
            value = production_review.check_shadow_policy(_production_read(arguments.policy, "shadow policy"), catalog=catalog,
                catalog_manifest_raw=catalog_raw, locator_manifest=locator_manifest)
            report = {"shadow_policy_id": value["shadow_policy_id"], "ok": True}
    elif command in ("shadow-journal", "replay"):
        catalog, catalog_raw, entries, exclusions, locator_manifest = catalog_inputs()
        policy = policy_input(catalog, catalog_raw, locator_manifest)
        if command == "shadow-journal" and action == "bootstrap":
            group, events, checkpoint = production_review.build_shadow_journal(entries, exclusions, catalog,
                policy, catalog_manifest_raw=catalog_raw, locator_manifest=locator_manifest,
                recorded_at=arguments.recorded_at, recorded_by=arguments.recorded_by)
            raw = production_review._jsonl(events); directory = evidence / "shadow-journals" / group["group_id"]
            production_review.atomic_publish_directory({"group.json": production_review.canonical_bytes(group),
                "events.jsonl": raw, "checkpoint.json": production_review.canonical_bytes(checkpoint)},
                directory, root=root, budget=production_review.BUDGETS["journal"], category="journal")
            report = {"group_id": group["group_id"], "checkpoint_id": checkpoint["checkpoint_id"],
                "events": len(events), "directory": str(directory),
                "bytes": len(raw)+len(production_review.canonical_bytes(group))+len(production_review.canonical_bytes(checkpoint))}
        else:
            group, raw, checkpoint, report = journal_inputs(catalog, catalog_raw, entries, exclusions, policy, locator_manifest)
            if not getattr(arguments, "detail", False): report.pop("queued_revisions", None)
            report.update({"group_id": group["group_id"], "checkpoint_id": checkpoint["checkpoint_id"], "ok": True})
    elif command == "batch-draft":
        catalog, catalog_raw, entries, exclusions, locator_manifest = catalog_inputs()
        policy = policy_input(catalog, catalog_raw, locator_manifest)
        group, raw, checkpoint, _ = journal_inputs(catalog, catalog_raw, entries, exclusions, policy, locator_manifest)
        value = production_review.build_shadow_batch(entries, catalog, policy, group, raw, checkpoint, exclusions,
            catalog_manifest_raw=catalog_raw, locator_manifest=locator_manifest)
        directory = evidence / "batches" / value["shadow_batch_id"]
        production_review.atomic_publish_directory({"manifest.json": production_review.canonical_bytes(value)},
            directory, root=root, budget=production_review.BUDGETS["batch"], category="batch")
        report = {"shadow_batch_id": value["shadow_batch_id"], "eligible": len(value["eligible"]),
            "batch_selected": len(value["batch_selected"]), "carry_over": len(value["carry_over"]),
            "directory": str(directory), "bytes": len(production_review.canonical_bytes(value))}
    elif command == "reconciliation":
        # Validate the complete frozen chain before independently measuring drift.
        locator_manifest, locator_raw, frozen_occurrences_raw, frozen_locators_raw = snapshot_inputs(operational=False)
        catalog, catalog_raw, entries, exclusions, locator_manifest = catalog_inputs(operational=False)
        policy = policy_input(catalog, catalog_raw, locator_manifest)
        group, raw, checkpoint, _ = journal_inputs(catalog, catalog_raw, entries, exclusions, policy, locator_manifest)
        batch = production_review.validate_shadow_batch(_production_read(arguments.batch, "shadow batch"), entries=entries,
            exclusions=exclusions, catalog=catalog, policy=policy, group=group, events_raw=raw, checkpoint=checkpoint,
            catalog_manifest_raw=catalog_raw, locator_manifest=locator_manifest)
        events = production_review.parse_jsonl(raw, "journal events")
        report = production_review.reconciliation_report(entries, exclusions, events, batch)
        try:
            manifest = _manifest(arguments); runtime_info = LuaRuntime(manifest).doctor()
            live_occurrences = production_review.load_occurrences(manifest)
            live_occurrences_raw = production_review._jsonl(live_occurrences)
            current_manifest_sha = hashlib.sha256(manifest.raw_bytes).hexdigest()
            current_ordinals = production_review._component_ordinals(c.id for c in manifest.components)
            current_loader_sha = hashlib.sha256(_production_bytes(root / "tools/i18nlib/locale_model.py", "loader contract")).hexdigest()
            current_terminology = production_review.terminology_snapshot(root)
            current_sources = production_review.source_identities_from_manifest(manifest)
            axes = {
                "manifest_sha_and_order": locator_manifest["manifest_sha256"] == current_manifest_sha and locator_manifest["manifest_component_ordinals"] == current_ordinals,
                "loader_contract_sha_and_runtime": locator_manifest["loader_contract_path"] == "tools/i18nlib/locale_model.py" and locator_manifest["loader_contract_sha256"] == current_loader_sha and locator_manifest["lua_runtime"] == runtime_info["lua_version"] and locator_manifest["lua_build"] == runtime_info["luajit_version"],
                "occurrences": live_occurrences_raw == frozen_occurrences_raw,
                "terminology_snapshot": catalog["terminology_snapshot_id"] == current_terminology,
                "source_identities": catalog["source_identities"] == current_sources,
                "current_rules": catalog["rules_version"] == production_review.RULES_VERSION and policy["rules_version"] == production_review.RULES_VERSION,
                "fully_reconstructed_catalog": False,
            }
            try:
                live_locator, live_locator_raw, live_locators_raw = production_review.build_locator_snapshot_from_occurrences(
                    live_occurrences, manifest_sha256=current_manifest_sha, manifest_component_ordinals=current_ordinals,
                    loader_contract_path="tools/i18nlib/locale_model.py", loader_contract_sha256=current_loader_sha,
                    lua_runtime=runtime_info["lua_version"], lua_build=runtime_info["luajit_version"],
                    recorded_at=locator_manifest["recorded_at"], recorded_by=locator_manifest["recorded_by"])
                rebuilt, rebuilt_entries, rebuilt_exclusions = production_review.build_catalog(
                    live_locator, live_locator_raw, live_locators_raw, locator_manifest_raw=production_review.canonical_bytes(live_locator),
                    terminology_snapshot_id=current_terminology, source_identities=current_sources,
                    recorded_at=catalog["recorded_at"], recorded_by=catalog["recorded_by"])
                axes["fully_reconstructed_catalog"] = (rebuilt == catalog and rebuilt_entries == _production_bytes(arguments.entries, "catalog entries") and rebuilt_exclusions == _production_bytes(arguments.exclusions, "catalog exclusions"))
            except production_review.ProductionReviewError:
                pass
        except (production_review.ProductionReviewError, I18nToolError, OSError):
            live_occurrences = []
            axes = {key: False for key in production_review.RECONCILIATION_AXES}
        drift = not all(axes.values())
        report.update({"catalog_id":catalog["catalog_id"], "group_id":group["group_id"],
                       "shadow_batch_id":batch["shadow_batch_id"], "live_occurrences":len(live_occurrences),
                       "drift_axes":axes, "drift":drift, "shadow_publication_blocked":drift})
        production_review.validate_reconciliation_artifact(report)
        artifact = root / ".artifacts/i18n/production-review/reconciliation.json"
        try:
            artifact.parent.mkdir(parents=True, exist_ok=True)
            with artifact.open("wb") as handle:
                handle.write(production_review.canonical_bytes(report)); handle.flush(); os.fsync(handle.fileno())
            production_review._fsync_directory(artifact.parent)
        except OSError as error:
            raise production_review.ProductionReviewError(f"cannot publish reconciliation artifact: {error}") from error
        report["artifact"] = str(artifact)
        if not report["ok"]: raise production_review.ProductionReviewError("shadow reconciliation conservation failed")
    else:
        raise AssertionError(f"unhandled production command: {command}/{action}")
    if command in {"migration", "repair"}:
        sys.stdout.buffer.write(production_review.canonical_bytes(report))
        return 0 if report.get("ok", True) else 1
    if command == "queue" and action == "status":
        if arguments.json:
            sys.stdout.buffer.write(production_review.canonical_bytes(report))
        else:
            print(f"catalog {report['catalog_id']}")
            print(f"evidence HEAD {report['evidence_head']}")
            states = ", ".join(f"{key}={value}" for key, value in report["explicit_overrides"].items()) or "none"
            print(f"raw state codes ({report['override_basis']}) {states}; queued={report['implicit_queued']}; reconciliation={report['reconciliation_count']}")
            progress = report["progress"]
            print(f"committed evidence progress; eligible={progress['eligible']}; independent metrics (overlap allowed)")
            for name, metric in progress["metrics"].items():
                print(f"{name}={metric['count']}/{metric['denominator']}")
            levels = progress["committed_done_by_completion_level"]
            print(f"committed done state levels: surface_only={levels['surface_only']}; deep_reviewed={levels['deep_reviewed']}")
            print(f"invalidated_without_current_review={progress['invalidated_without_current_review']}")
            print(f"active writer {'yes' if report['active_writer'] else 'no'}")
    else:
        _print_json(report)
    if command == "queue" and action == "check" and not report["ok"]:
        return 1
    return 0
