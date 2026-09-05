"""Registration and handlers for identity commands."""

from __future__ import annotations
import argparse
from typing import Any, Iterable
from .config import ComponentSpec, Manifest
from .errors import ValidationError
from .git_source import GitRepository
from .locale_model import LocaleLoader
from .report import create_run_directory, write_json
from .runtime import LuaRuntime
from .cli_common import _add_common_arguments, _manifest, _print_json, _select_components


def register(subparsers: argparse._SubParsersAction) -> None:
    identity = subparsers.add_parser(
        "identity",
        help="TU/entity identity queries and audit (contract §4, §11)",
    )
    identity_subparsers = identity.add_subparsers(
        dest="identity_command", required=True
    )
    identity_show = identity_subparsers.add_parser(
        "show", help="show one TU's anchor/slot/revision/binding"
    )
    _add_common_arguments(identity_show)
    identity_show.add_argument("tu_uid", metavar="TU_UID")
    identity_audit = identity_subparsers.add_parser(
        "audit",
        help="UNKNOWN rate, conflicts and the rename queue between two runs",
    )
    _add_common_arguments(identity_audit)
    baseline = subparsers.add_parser(
        "baseline",
        help="frozen baseline snapshots and reports (contract §7)",
    )
    baseline_subparsers = baseline.add_subparsers(
        dest="baseline_command", required=True
    )
    baseline_freeze = baseline_subparsers.add_parser(
        "freeze", help="freeze the current findings as the baseline for a commit"
    )
    _add_common_arguments(baseline_freeze)
    baseline_freeze.add_argument(
        "--commit",
        required=True,
        metavar="COMMIT",
        help="translation repository commit this baseline belongs to",
    )
    baseline_report = baseline_subparsers.add_parser(
        "report", help="new / legacy / resolved statistics"
    )
    _add_common_arguments(baseline_report)
    baseline_report.add_argument(
        "--commit",
        required=True,
        metavar="COMMIT",
        help="translation repository commit to compare against",
    )
    identity.set_defaults(handler=dispatch)
    baseline.set_defaults(handler=dispatch)


def dispatch(arguments: argparse.Namespace) -> int:
    if arguments.command == "baseline":
        if arguments.baseline_command == "freeze":
            return _baseline_freeze(arguments)
        if arguments.baseline_command == "report":
            return _baseline_report(arguments)
        raise AssertionError(
            f"unhandled baseline command: {arguments.baseline_command}"
        )
    if arguments.command == "identity":
        if arguments.identity_command == "show":
            return _identity_show(arguments)
        if arguments.identity_command == "audit":
            return _identity_audit(arguments)
        raise AssertionError(
            f"unhandled identity command: {arguments.identity_command}"
        )
    raise AssertionError(f"unhandled command: {arguments.command}")


def _current_indexes_for(manifest: Manifest) -> dict[str, Any]:
    """Current identity indexes keyed by component.

    Shares the fail-closed scan with the extract path (V3/V10): a partial
    trio (entities/tu/identity) or a corrupt identity.json raises
    ValidationError instead of being silently skipped, so identity
    show/audit cannot read a half-written component index.
    """
    from .extract import _read_current_indexes

    current_root = manifest.root / ".artifacts" / "i18n" / "identity" / "current"
    if not current_root.is_dir():
        return {}
    return {
        index.component: index for index in _read_current_indexes(current_root)
    }


def _records_by_component(
    records: Iterable[Any],
    components: Iterable[ComponentSpec],
    *,
    indexes: dict[str, Any] | None = None,
) -> dict[str, list[Any]]:
    """Assign FindingRecords to components.

    Translation-path mapping is the primary owner signal, but entity-level
    findings (duplicate-talent-id / duplicate-effect-id) carry a source
    section as their Issue.logical_path, so they never match a translation
    file path. They are attributed through the identity evidence instead:
    the component index whose TUs contain the record's subject/participants
    (never string-matching the section text).
    """
    by_path: dict[str, str] = {}
    for component in components:
        by_path[component.translation] = component.id
        if component.copy_fragment:
            by_path[component.copy_fragment] = component.id
    indexes = indexes or {}

    def via_tu(record: Any) -> str | None:
        for component_id, index in indexes.items():
            if record.tu_uid in index.tus:
                return component_id
        for component_id, index in indexes.items():
            if any(participant in index.tus for participant in record.participants):
                return component_id
        return None

    grouped: dict[str, list[Any]] = {}
    for record in records:
        owner = by_path.get(record.issue.logical_path)
        if owner is None:
            owner = via_tu(record)
        if owner is None:
            continue
        grouped.setdefault(owner, []).append(record)
    return grouped


def _identity_show(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    tu_uid = arguments.tu_uid
    indexes = _current_indexes_for(manifest)
    match = None
    owner = None
    for component, index in indexes.items():
        tu = index.tus.get(tu_uid)
        if tu is not None:
            match = tu
            owner = component
            break
    if match is None:
        raise ValidationError(
            f"TU {tu_uid} not found in the current identity indexes; "
            "run extract --enrich first"
        )
    entity = None
    if match.entity_uid is not None:
        entity = indexes[owner].entities.get(match.entity_uid)
    report = {
        "tu": match.to_dict(),
        "entity": entity.to_dict() if entity is not None else None,
        "component": owner,
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"TU      {match.tu_uid}")
        print(f"binding {match.identity_binding}  component={match.component}")
        print(
            f"entity  {match.entity_uid or '-'}  kind={match.kind}  "
            f"anchor={match.anchor_key or '-'}"
        )
        print(f"slot    {match.semantic_slot}  discriminator={match.discriminator}")
        print(f"sections {', '.join(match.sections[:5])}")
        for revision in match.revisions:
            print(
                f"rev     {revision.revision_uid[:16]}  "
                f"source={revision.source!r}"
            )
    return 0


def _identity_audit(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    components = _select_components(manifest, [], default="extract")
    from .identity import diff_indexes
    from .pipeline import extract_enriched

    previous = _current_indexes_for(manifest)
    current, extract_report = extract_enriched(manifest, runtime, components)
    events: list[dict[str, Any]] = []
    for component in components:
        if component.id not in current:
            continue
        new_index = current[component.id]
        old_index = previous.get(component.id)
        if old_index is not None:
            events.extend(
                event.to_dict()
                for event in diff_indexes(base=old_index, new=new_index)
            )
        else:
            for uid, entity in new_index.entities.items():
                events.append(
                    {
                        "kind": "created",
                        "component": component.id,
                        "entity_kind": entity.kind,
                        "section": (
                            sorted(entity.sections)[0] if entity.sections else None
                        ),
                        "old_anchor_key": None,
                        "new_anchor_key": entity.anchor_key,
                        "old_entity_uid": None,
                        "new_entity_uid": uid,
                        "similarity": None,
                    }
                )
    summary: dict[str, int] = {}
    for event in events:
        kind = event.get("kind")
        summary[kind] = summary.get(kind, 0) + 1
    rename_queue = [
        event
        for event in events
        if event.get("kind") in ("rename_candidate", "ambiguous", "hint")
    ]
    report = {
        "ok": True,
        "events": events,
        "rename_queue": rename_queue,
        "summary": summary,
        "components": {
            component.id: current[component.id].stats
            for component in components
            if component.id in current
        },
        "extract_run_directory": extract_report.get("run_directory"),
    }
    run_directory = create_run_directory(manifest.root, "identity-audit")
    write_json(run_directory / "audit.json", report)
    report["run_directory"] = str(run_directory)
    if arguments.json:
        _print_json(report)
    else:
        for component in components:
            if component.id not in current:
                continue
            stats = current[component.id].stats
            print(
                f"OK  {component.id:<16} tus={stats['tus']} "
                f"strong={stats['strong_tus']} "
                f"unknown_fallback={stats['unknown_fallback_occurrences']} "
                f"conflicts={stats['conflicts']}"
            )
        print(
            f"Events: unchanged={summary.get('unchanged', 0)} "
            f"created={summary.get('created', 0)} "
            f"deleted={summary.get('deleted', 0)} "
            f"rename_candidate={summary.get('rename_candidate', 0)} "
            f"ambiguous={summary.get('ambiguous', 0)} "
            f"hint={summary.get('hint', 0)}"
        )
        if rename_queue:
            print(f"Rename queue: {len(rename_queue)} entries (see audit.json)")
        print(f"Report: {run_directory / 'audit.json'}")
    return 0


def _verify_freeze_provenance(manifest: Manifest, requested_commit: str) -> str:
    """Bind a `baseline freeze --commit` label to the translation repo HEAD.

    Contract §7.1: the commit in the baseline filename is the translation
    repository commit this baseline was generated from, and a baseline whose
    generation environment cannot be rebuilt is invalid for CI. To keep that
    honest for a personal project, the caller-supplied commit must resolve to
    exactly the current HEAD and the tracked/index worktree must be clean, so a
    dirty worktree can never masquerade as a frozen commit.
    """
    from .errors import ContractError

    repository = GitRepository(manifest.root)
    resolved = repository.resolve_commit(requested_commit)
    head = repository.resolve_commit("HEAD")
    if resolved != head:
        raise ContractError(
            f"baseline freeze --commit {requested_commit!r} resolves to "
            f"{resolved[:12]} but the translation repository HEAD is "
            f"{head[:12]}; a frozen baseline must be generated from the "
            "current HEAD (commit your changes first)"
        )
    status = repository.worktree_porcelain()
    if status.strip():
        raise ContractError(
            "translation repository worktree is not clean; a baseline must be "
            "frozen from a committed tree (stash or commit your changes first):\n"
            + status.rstrip()
        )
    return resolved


def _baseline_freeze(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    components = _select_components(manifest, [], default="lint")
    from .baseline import write_baseline
    from .pipeline import run_enriched_lint

    frozen_commit = _verify_freeze_provenance(manifest, arguments.commit)
    pipeline = run_enriched_lint(manifest, runtime, loader, components)
    extractable_ids = set(pipeline["indexes"])
    records_by_component = _records_by_component(
        pipeline["records"], components, indexes=pipeline["indexes"]
    )

    frozen: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for component in components:
        if component.id not in extractable_ids:
            skipped.append(
                {
                    "component": component.id,
                    "reason": "no reproducible source extraction",
                    "findings": len(records_by_component.get(component.id, [])),
                }
            )
            continue
        records = records_by_component.get(component.id, [])
        snapshot_sha = next(
            (
                item["snapshot_sha256"]
                for item in pipeline["extract"].get("components", [])
                if item["component"] == component.id
            ),
            "",
        )
        engine_commit = (
            manifest.repositories[component.source_repository].commit
            if component.source_repository
            else ""
        )
        baseline = write_baseline(
            manifest_root=manifest.root,
            component=component.id,
            translation_commit=frozen_commit,
            source_snapshot_sha256=snapshot_sha,
            engine_commit=engine_commit,
            extractor_commit=manifest.extractor.commit,
            rules_registry_sha256=pipeline["registries"]["rules_registry_sha256"],
            slot_registry_sha256=pipeline["registries"]["slot_registry_sha256"],
            records=records,
        )
        frozen.append(
            {
                "component": component.id,
                "entries": len(baseline.entries),
                "baseline": str(baseline.path),
                "sha256": baseline.sha256,
            }
        )
    report = {
        "ok": True,
        "translation_commit": frozen_commit,
        "components": frozen,
        "skipped": skipped,
        "metrics": pipeline["metrics"],
        "binding": pipeline["binding"],
    }
    if arguments.json:
        _print_json(report)
    else:
        for item in frozen:
            print(f"OK  {item['component']:<16} baseline={item['entries']} findings")
        for item in skipped:
            print(
                f"SKIP {item['component']:<16} {item['reason']} "
                f"({item['findings']} findings unbaselined)"
            )
        print(f"Baselines frozen for translation commit {frozen_commit}")
    return 0


def _resolve_translation_commit(manifest: Manifest, requested: str) -> str:
    """Resolve a `--commit` label to a full translation-repository commit OID.

    Baselines are keyed and named by the full OID (§7.1); a short sha or rev
    expression from the operator is canonicalized here so freeze/report/lint
    all address the same on-disk artifact. An unresolvable label is a
    contract-level failure.
    """
    repository = GitRepository(manifest.root)
    return repository.resolve_commit(requested)


def _load_required_baselines(
    manifest: Manifest,
    *,
    components: list[ComponentSpec],
    indexes: dict[str, Any],
    commit: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load baselines for the components that have reproducible extraction.

    Fail-closed (§7.1): every component present in ``indexes`` (i.e. with a
    reproducible source extraction this run) MUST have a loadable, intact
    baseline; a missing or corrupt one is a ValidationError, never a silent
    skip. Components without reproducible extraction are the only legitimate
    absence and are returned explicitly as ``skipped``. An empty required
    set (no component demands a baseline) is also a failure: a CI gate over
    no valid baseline cannot return success.
    """
    from .baseline import read_baseline

    required = [component for component in components if component.id in indexes]
    skipped = [
        {
            "component": component.id,
            "reason": "no reproducible source extraction",
        }
        for component in components
        if component.id not in indexes
    ]
    if not required:
        raise ValidationError(
            f"no reproducible-extraction component demands a baseline for "
            f"commit {commit}; a CI gate over an empty valid set cannot pass"
        )
    baselines: dict[str, Any] = {}
    load_errors: list[tuple[str, str]] = []
    for component in required:
        try:
            baselines[component.id] = read_baseline(
                manifest.root,
                component=component.id,
                translation_commit=commit,
            )
        except ValidationError as error:
            load_errors.append((component.id, str(error)))
    if load_errors:
        details = "; ".join(f"{cid}: {msg}" for cid, msg in load_errors)
        raise ValidationError(
            f"missing or corrupt baselines for commit {commit}; refusing CI "
            f"judgement (fail-closed): {details}"
        )
    return baselines, skipped


def _baseline_report(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    components = _select_components(manifest, [], default="lint")
    from .baseline import ci_gate, compute_baseline_state
    from .pipeline import run_enriched_lint, validate_baselines

    pipeline = run_enriched_lint(manifest, runtime, loader, components)
    records_by_component = _records_by_component(
        pipeline["records"], components, indexes=pipeline["indexes"]
    )

    resolved_commit = _resolve_translation_commit(manifest, arguments.commit)
    baselines, skipped = _load_required_baselines(
        manifest,
        components=components,
        indexes=pipeline["indexes"],
        commit=resolved_commit,
    )
    validate_baselines(
        manifest,
        baselines=baselines,
        extract_report=pipeline["extract"],
        registries=pipeline["registries"],
    )
    states: dict[str, dict[str, Any]] = {}
    total_gate: dict[str, int] = {
        "new_errors": 0,
        "new_warnings": 0,
        "legacy_errors": 0,
        "legacy_warnings": 0,
        "resolved": 0,
    }
    for component_id, baseline in baselines.items():
        state = compute_baseline_state(
            baseline, records_by_component.get(component_id, [])
        )
        passed, gate = ci_gate(state)
        for key in total_gate:
            total_gate[key] += gate[key]
        states[component_id] = {
            "passed": passed,
            "gate": gate,
            "new": [record.to_dict() for record in state.new],
            "legacy": [record.to_dict() for record in state.legacy],
            "resolved": [entry.to_dict() for entry in state.resolved],
            "legacy_on_touched_tu": list(state.legacy_on_touched_tu),
        }
    report = {
        "ok": bool(baselines) and all(state["passed"] for state in states.values()),
        "translation_commit": resolved_commit,
        "components": states,
        "skipped": skipped,
        "totals": total_gate,
        "binding": pipeline["binding"],
    }
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"baseline report vs {resolved_commit}: "
            f"new_errors={total_gate['new_errors']} "
            f"new_warnings={total_gate['new_warnings']} "
            f"legacy_errors={total_gate['legacy_errors']} "
            f"legacy_warnings={total_gate['legacy_warnings']} "
            f"resolved={total_gate['resolved']}"
        )
        for component_id, state in states.items():
            for record in state["new"][:20]:
                print(
                    f"NEW  {component_id:<16} {record['code']:24} "
                    f"{record['message'][:100]}"
                )
    if not report["ok"]:
        raise ValidationError(
            f"baseline gate failed: {total_gate['new_errors']} new errors"
        )
    return 0
