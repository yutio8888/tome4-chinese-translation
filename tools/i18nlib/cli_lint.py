"""Registration and handlers for lint commands."""

from __future__ import annotations
import argparse
import json
from collections import Counter, defaultdict
from typing import Any, Iterable
from .config import ComponentSpec, Manifest
from .errors import I18nToolError, ValidationError
from .git_source import GitRepository
from .lint import Issue, lint_documents, lint_terminology, load_policy
from .locale_model import LocaleLoader
from .report import create_run_directory, write_json
from .runtime import LuaRuntime
from .cli_common import _add_common_arguments, _manifest, _print_json, _select_components
from .cli_identity import _load_required_baselines, _records_by_component, _resolve_translation_commit


def register(subparsers: argparse._SubParsersAction) -> None:
    lint = subparsers.add_parser("lint", help="validate canonical translations")
    _add_common_arguments(lint)
    lint.add_argument(
        "--component", action="append", default=[], metavar="ID", help="component to lint"
    )
    lint.add_argument(
        "--strict", action="store_true", help="treat warnings as blocking failures"
    )
    lint.add_argument(
        "--baseline",
        metavar="COMMIT",
        help="compare against the frozen baseline for this translation commit",
    )
    lint.add_argument(
        "--incremental",
        metavar="BASE..HEAD",
        help="incremental invalidation over a commit range (contract §8)",
    )
    lint.add_argument(
        "--domain",
        choices=("source", "translation", "rule"),
        default="source",
        help="incremental domain (default: source)",
    )
    lint.add_argument(
        "--self-check",
        action="store_true",
        help="run the whole-set canonical self-check (exit 2 on mismatch)",
    )
    lint.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: new ERROR findings fail with exit code 1",
    )
    lint.add_argument(
        "--legacy-report",
        action="store_true",
        help="expand the folded legacy technical-debt report",
    )
    lint.set_defaults(handler=dispatch)


def dispatch(arguments: argparse.Namespace) -> int:
    if arguments.command == "lint":
        return _lint(arguments)
    raise AssertionError(f"unhandled command: {arguments.command}")


def _issue_line(issue: Issue) -> str:
    location = issue.logical_path
    if issue.line is not None:
        location += f":{issue.line}"
    return f"{issue.severity.upper():7} {issue.code:24} {location}  {issue.message}"


def _lint(arguments: argparse.Namespace) -> int:
    if arguments.baseline or arguments.incremental:
        return _lint_identity_mode(arguments)
    manifest = _manifest(arguments)
    components = _select_components(manifest, arguments.component, default="lint")
    policy = load_policy(manifest)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    documents = []
    copy_fragment_documents = []
    for component in components:
        if component.copy_fragment:
            copy_fragment_documents.append(
                (
                    component.id,
                    loader.load_path(
                        manifest.root / component.copy_fragment,
                        logical_path=component.copy_fragment,
                    ),
                )
            )
        documents.append(
            (
                component.id,
                loader.load_path(
                    manifest.root / component.translation,
                    logical_path=component.translation,
                ),
            )
        )
    issues, metrics = lint_documents(documents, policy, require_nonempty=True)
    copy_fragment_issues, copy_fragment_metrics = lint_documents(
        copy_fragment_documents,
        policy,
        require_nonempty=False,
    )
    issues.extend(copy_fragment_issues)
    metrics["copy_fragment_translations"] = copy_fragment_metrics["translations"]
    metrics["copy_fragment_components"] = copy_fragment_metrics["components"]
    metrics["copy_fragment_duplicate_runtime_keys"] = copy_fragment_metrics[
        "duplicate_runtime_keys"
    ]
    terminology_issues, terminology_metrics = lint_terminology(
        manifest.root / manifest.terminology
    )
    issues.extend(terminology_issues)
    metrics["errors"] = sum(issue.severity == "error" for issue in issues)
    metrics["warnings"] = sum(issue.severity == "warning" for issue in issues)
    metrics["terminology"] = terminology_metrics
    report = {
        "ok": metrics["errors"] == 0
        and (not arguments.strict or metrics["warnings"] == 0),
        "version": manifest.version,
        "strict": arguments.strict,
        "metrics": metrics,
        "issues": [issue.to_dict() for issue in issues],
    }
    run_directory = create_run_directory(manifest.root, "lint")
    report["run_directory"] = str(run_directory)
    write_json(run_directory / "lint.json", report)
    if arguments.json:
        _print_json(report)
    else:
        limit = 80
        for issue in issues[:limit]:
            print(_issue_line(issue))
        if len(issues) > limit:
            print(f"... {len(issues) - limit} additional issues are in the JSON report")
        print(
            f"Checked {metrics['translations']} translations: "
            f"{metrics['errors']} errors, {metrics['warnings']} warnings"
        )
        print(f"Report: {run_directory / 'lint.json'}")
    if not report["ok"]:
        raise ValidationError(
            f"lint failed with {metrics['errors']} errors and {metrics['warnings']} warnings"
        )
    return 0


def _lint_identity_mode(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    if arguments.baseline:
        components = _select_components(manifest, arguments.component, default="lint")
        from .baseline import ci_gate, compute_baseline_state
        from .pipeline import run_enriched_lint, validate_baselines

        pipeline = run_enriched_lint(manifest, runtime, loader, components)
        records_by_component = _records_by_component(
            pipeline["records"], components, indexes=pipeline["indexes"]
        )
        resolved_commit = _resolve_translation_commit(
            manifest, arguments.baseline
        )
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
        new_errors = 0
        report_states: dict[str, dict[str, Any]] = {}
        for component_id, baseline in baselines.items():
            records = records_by_component.get(component_id, [])
            state = compute_baseline_state(baseline, records)
            passed, gate = ci_gate(state)
            new_errors += gate["new_errors"]
            report_states[component_id] = {
                "passed": passed,
                "gate": gate,
                "new": [record.to_dict() for record in state.new],
                "legacy": [record.to_dict() for record in state.legacy],
                "resolved": [entry.to_dict() for entry in state.resolved],
            }
        report = {
            "ok": bool(baselines) and new_errors == 0,
            "mode": "baseline",
            "translation_commit": resolved_commit,
            "components": report_states,
            "skipped": skipped,
            "binding": pipeline["binding"],
        }
        run_directory = create_run_directory(manifest.root, "lint-baseline")
        write_json(run_directory / "lint.json", report)
        report["run_directory"] = str(run_directory)
        if arguments.json:
            _print_json(report)
        else:
            print(
                f"baseline {resolved_commit}: new errors={new_errors} "
                f"({'OK' if new_errors == 0 else 'FAIL'})"
            )
            for component_id, state in report_states.items():
                gate = state["gate"]
                print(
                    f"  {component_id:<16} new_err={gate['new_errors']} "
                    f"new_warn={gate['new_warnings']} "
                    f"legacy_err={gate['legacy_errors']} "
                    f"legacy_warn={gate['legacy_warnings']} "
                    f"resolved={gate['resolved']}"
                )
                if arguments.legacy_report:
                    for record in state["legacy"][:50]:
                        print(
                            f"    LEGACY {record['code']:24} "
                            f"{record['message'][:80]}"
                        )
        if arguments.ci and new_errors > 0:
            from .errors import I18nToolError

            raise I18nToolError(
                f"baseline CI gate failed: {new_errors} new errors"
            )
        return 0

    # --incremental
    base, head = arguments.incremental.split("..", 1)
    if not base or not head:
        raise ValidationError("--incremental expects BASE..HEAD")
    if arguments.domain == "source":
        from .git_source import GitRepository
        from .incremental import incremental_source_flow

        repository_name = manifest.repositories["engine"].name
        engine_repository = GitRepository(manifest.repository_path(repository_name))
        base = engine_repository.resolve_commit(base)
        head = engine_repository.resolve_commit(head)
        components = _select_components(manifest, arguments.component, default="lint")
        artifact_directory = (
            create_run_directory(manifest.root, "lint-incremental")
            if arguments.self_check
            else None
        )
        result = incremental_source_flow(
            manifest=manifest,
            runtime=runtime,
            loader=loader,
            components=components,
            engine_repository=engine_repository,
            base_commit=base,
            head_commit=head,
            self_check=arguments.self_check,
            artifact_directory=artifact_directory,
        )
        report = dict(result)
        report["ok"] = True
        # Keep the self-check verdict separate from the aggregated ok: the
        # exception dispatch must follow the actual gate that failed, not the
        # render-only aggregate (FR2 regression fix: --self-check --ci with a
        # passed self-check and new ERRORs must raise I18nToolError/exit 1,
        # not IncrementalCheckError/exit 2; a failed self-check keeps exit 2
        # priority). The aggregated ok still expresses ANY enabled gate
        # failure for the JSON/text render.
        self_check_failed = False
        if arguments.self_check and result.get("self_check") is not None:
            self_check_failed = not result["self_check"]["passed"]
            report["ok"] = result["self_check"]["passed"]
        # FR2: the JSON/text ok must agree with the CI gate. The flow already
        # reports new_errors; when --ci is passed a non-zero count flips ok
        # to False BEFORE any render (the raise below keeps the established
        # exit code and fingerprint message). Without --ci the counts never
        # influence ok (V7).
        ci = result.get("ci") or {}
        new_error_count = ci.get("new_errors", 0)
        if arguments.ci and new_error_count > 0:
            report["ok"] = False
        if arguments.json:
            _print_json(report)
        else:
            findings = result["findings"]
            print(
                f"incremental {arguments.incremental} domain=source: "
                f"affected_tus={result['affected_tus']} "
                f"previous={findings['previous']} kept={findings['kept']} "
                f"recomputed={findings['recomputed']} "
                f"incremental={findings['incremental']}"
            )
            if result.get("deleted_files"):
                print(f"deleted_files: {len(result['deleted_files'])}")
            if result.get("widened_components"):
                print(f"widened: {sorted(result['widened_components'])}")
            ci = result.get("ci") or {}
            print(
                f"ci: new_errors={ci.get('new_errors', 0)} "
                f"legacy_errors={ci.get('legacy_errors', 0)}"
            )
            if result.get("self_check") is not None:
                check = result["self_check"]
                print(
                    f"self-check: {'PASS' if check['passed'] else 'MISMATCH'} "
                    f"(full={check['full_findings']})"
                )
        if arguments.self_check and self_check_failed:
            from .errors import IncrementalCheckError

            raise IncrementalCheckError(
                "incremental self-check failed: canonical forms differ"
            )
        if arguments.ci:
            from .errors import I18nToolError

            # §7.4/§11: only NEW ERROR findings (recomputed errors whose
            # fingerprint is absent from the base error fingerprints) fail
            # the gate; legacy ERROR stays technical debt (H3). The flow
            # reports new_errors directly so the CLI never miscounts from
            # the final full records set.
            first_fingerprint = (ci.get("new_error_fingerprints") or [""])[0]
            if new_error_count:
                detail = (
                    f" (first fingerprint: {first_fingerprint})"
                    if first_fingerprint
                    else ""
                )
                raise I18nToolError(
                    "incremental CI gate failed: "
                    f"{new_error_count} new ERROR findings{detail}"
                )
        return 0
    if arguments.domain == "rule":
        return _lint_incremental_rule(arguments, manifest, runtime, loader)
    if arguments.domain == "translation":
        return _lint_incremental_translation(arguments, manifest, runtime, loader)
    raise AssertionError(f"unhandled domain: {arguments.domain}")


def _changed_editorial_keys(
    base_entries: Iterable[dict[str, Any]],
    head_entries: Iterable[dict[str, Any]],
    semantic: Any,
) -> set[tuple[str, str, str | None]]:
    """H4/D5/R5/R8: bidirectional added / deleted / semantically-changed keys.

    Each (section, source, source_tag) key carries a multiset of occurrence
    identities - (semantic payload, line) - because the same key can
    legitimately repeat; a key is affected when its base and head multisets
    differ. A dict that keeps only the last occurrence would fold a
    duplicated defective occurrence into invisibility (R5); the occurrence
    line is part of the identity so a pure reorder of duplicated occurrences
    still recomputes the record against the head document (R8: the kept
    base record would otherwise carry stale issue metadata and diverge from
    the full-head canonical form).
    """
    base_by_key: dict[
        tuple[str, str, str | None], Counter[tuple[Any, Any]]
    ] = defaultdict(Counter)
    head_by_key: dict[
        tuple[str, str, str | None], Counter[tuple[Any, Any]]
    ] = defaultdict(Counter)
    for entry in base_entries:
        base_by_key[
            (entry.get("section"), entry.get("source"), entry.get("source_tag"))
        ][(semantic(entry), entry.get("line"))] += 1
    for entry in head_entries:
        head_by_key[
            (entry.get("section"), entry.get("source"), entry.get("source_tag"))
        ][(semantic(entry), entry.get("line"))] += 1
    return {
        key
        for key in set(base_by_key) | set(head_by_key)
        if base_by_key.get(key, Counter()) != head_by_key.get(key, Counter())
    }


def _rule_signature(rule: Any) -> tuple[Any, ...]:
    """H4: the full semantic signature of a rule entry.

    schema_version / severity / evidence_key_spec changes alter the frozen
    fingerprint (§6.1), so they must drive recomputation even when the
    rule_id set is unchanged."""
    return (
        rule.rule_id,
        rule.schema_version,
        rule.severity,
        rule.evidence_key_spec,
    )


def affected_rule_ids(
    base_registry: Any, head_registry: Any
) -> frozenset[str]:
    """Rule IDs whose semantic signature differs between two registries."""
    base_signatures = {_rule_signature(rule) for rule in base_registry.rules.values()}
    head_signatures = {_rule_signature(rule) for rule in head_registry.rules.values()}
    return frozenset(signature[0] for signature in base_signatures ^ head_signatures)


def _lint_incremental_rule(
    arguments: argparse.Namespace,
    manifest: Manifest,
    runtime: LuaRuntime,
    loader: LocaleLoader,
) -> int:
    from .errors import ContractError
    from .fingerprint import RuleRegistry
    from .findings import FindingContext, build_finding_records
    from .git_source import GitRepository
    from .identity import (
        RULES_REGISTRY_RELATIVE_PATH,
        UnloadedSources,
    )
    from .lint import parse_policy
    from .pipeline import extract_enriched, lint_documents_specs

    repository = GitRepository(manifest.root)
    base, head = arguments.incremental.split("..", 1)
    base = repository.resolve_commit(base)
    head = repository.resolve_commit(head)
    changed = repository.changed_paths(base, head)
    registry_path = "i18n/quality/rules-registry-v1.json"
    policy_path = "i18n/policy.json"
    unloaded_path = "i18n/quality/unloaded-sources-v1.json"
    registry_changed = registry_path in changed
    policy_changed = policy_path in changed
    unloaded_changed = unloaded_path in changed

    # H4/V4: the head registry/policy come from the resolved head commit
    # blob (required, fail-closed) - uncommitted worktree content can never
    # masquerade as head. The base side comes from the base blob when the
    # file changed in the range, otherwise it equals head. Every read is
    # strict: corrupt/missing JSON aborts instead of silently falling back.
    head_registry_data = _read_commit_json(
        repository, head, registry_path, "rule registry"
    )
    head_registry = RuleRegistry.from_dict(
        head_registry_data, label=f"rule registry@{head[:12]}"
    )
    if registry_changed:
        base_registry = RuleRegistry.from_dict(
            _read_commit_json(repository, base, registry_path, "rule registry"),
            label=f"rule registry@{base[:12]}",
        )
    else:
        base_registry = head_registry

    affected_rules: set[str] = set()
    if registry_changed:
        affected_rules |= set(
            affected_rule_ids(base_registry, head_registry)
        )
    head_policy_data = _read_commit_json(
        repository, head, policy_path, "lint policy"
    )
    head_policy = parse_policy(head_policy_data, label=f"lint policy@{head[:12]}")
    if policy_changed:
        base_policy = parse_policy(
            _read_commit_json(repository, base, policy_path, "lint policy"),
            label=f"lint policy@{base[:12]}",
        )
        # D3: the three policy allowlists are consumed only by these four
        # rules (lint.py _format_issue/_format_shape_issue/empty-target/
        # runtime-collision), so a policy change recomputes exactly them.
        affected_rules |= {
            "format-mismatch",
            "format-shape-difference",
            "empty-target",
            "runtime-collision",
        }
    else:
        base_policy = head_policy
    # R4: the unloaded-sources registry is a rule-domain dependency: an
    # exemption change toggles duplicate-talent-id / duplicate-effect-id
    # ERROR findings. Loaded strictly from base/head blobs (fail-closed);
    # the head side is always required, so a corrupt/missing active registry
    # aborts even when nothing else changed.
    head_unloaded = UnloadedSources.from_dict(
        _read_commit_json(
            repository, head, unloaded_path, "unloaded-sources registry"
        ),
        label=f"unloaded-sources registry@{head[:12]}",
    )
    if unloaded_changed:
        base_unloaded = UnloadedSources.from_dict(
            _read_commit_json(
                repository, base, unloaded_path, "unloaded-sources registry"
            ),
            label=f"unloaded-sources registry@{base[:12]}",
        )
        affected_rules |= {"duplicate-talent-id", "duplicate-effect-id"}
    else:
        base_unloaded = head_unloaded
    if not affected_rules:
        # No rule/policy semantic change: F_new == F_previous, so both flags
        # hold trivially; they are reported explicitly, never silently
        # dropped. The active registry was validated above (fail-closed).
        report = {
            "domain": "rule",
            "base": base,
            "head": head,
            "registry_changed": registry_changed,
            "policy_changed": policy_changed,
            "unloaded_changed": unloaded_changed,
            "affected_rules": [],
            "findings": 0,
            "ok": True,
        }
        if arguments.self_check:
            report["self_check"] = {"passed": True, "full_findings": 0}
        report["ci"] = {"new_errors": 0, "legacy_errors": 0}
        if arguments.json:
            _print_json(report)
        else:
            print(f"rule domain: no rule change in {base}..{head}")
        return 0
    components = _select_components(manifest, arguments.component, default="lint")
    indexes, _ = extract_enriched(manifest, runtime, components)
    # V4: translation documents come from the resolved head commit blobs
    # (never the worktree).
    specs, _ = _document_specs_at_commit(repository, loader, components, head)

    def records_for(
        issues: Any, contexts: Any, registry: Any, unloaded: Any
    ) -> list[Any]:
        bound = {
            name: FindingContext(
                component=context.component,
                entries=context.entries,
                index=indexes.get(context.component),
            )
            for name, context in contexts.items()
        }
        conflicts: list[Any] = []
        for index in indexes.values():
            conflicts.extend(index.conflicts)
        records, _ = build_finding_records(
            registry=registry,
            issues=issues,
            contexts=bound,
            conflicts=conflicts,
            unloaded_sources=unloaded,
        )
        return records

    issues_head, contexts_head, _ = lint_documents_specs(
        manifest, specs, policy=head_policy
    )
    issues_base, contexts_base, _ = lint_documents_specs(
        manifest, specs, policy=base_policy
    )
    # R4: base records use the base unloaded registry, head records the head
    # one (an exemption change alters which duplicate ERRORs are emitted).
    head_records = records_for(
        issues_head, contexts_head, head_registry, head_unloaded
    )
    base_records = records_for(
        issues_base, contexts_base, base_registry, base_unloaded
    )
    # F_new = (F_previous - findings(affected)) + recompute(affected)
    f_new = tuple(
        sorted(
            [
                *[record for record in base_records if record.rule_id not in affected_rules],
                *[record for record in head_records if record.rule_id in affected_rules],
            ],
            key=lambda record: record.fingerprint,
        )
    )
    base_error_fingerprints = frozenset(
        record.fingerprint
        for record in base_records
        if record.issue.severity == "error"
    )
    new_error_count = sum(
        1
        for record in f_new
        if record.issue.severity == "error"
        and record.fingerprint not in base_error_fingerprints
    )
    legacy_error_count = sum(
        1
        for record in f_new
        if record.issue.severity == "error"
        and record.fingerprint in base_error_fingerprints
    )
    report = {
        "domain": "rule",
        "base": base,
        "head": head,
        "registry_changed": registry_changed,
        "policy_changed": policy_changed,
        "unloaded_changed": unloaded_changed,
        "affected_rules": sorted(affected_rules),
        "findings": {
            "previous": len(base_records),
            "incremental": len(f_new),
        },
        "records": [record.to_dict() for record in f_new],
        "ok": True,
    }
    if arguments.self_check:
        from .invalidation import self_check as canonical_self_check

        passed = canonical_self_check(incremental=f_new, full=head_records)
        report["self_check"] = {
            "passed": passed,
            "full_findings": len(head_records),
        }
        report["ok"] = report["ok"] and passed
    # V6/V7: counts are always reported; only --ci turns them into a gate.
    report["ci"] = {
        "new_errors": new_error_count,
        "legacy_errors": legacy_error_count,
    }
    if arguments.ci:
        report["ok"] = report["ok"] and new_error_count == 0
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"rule domain: affected rules={sorted(affected_rules)} "
            f"previous={len(base_records)} incremental={len(f_new)}"
        )
        if report.get("self_check") is not None:
            print(
                f"self-check: "
                f"{'PASS' if report['self_check']['passed'] else 'MISMATCH'}"
            )
        if report.get("ci") is not None:
            print(f"ci: new_errors={report['ci']['new_errors']}")
    if arguments.self_check and report["self_check"]["passed"] is False:
        from .errors import IncrementalCheckError

        raise IncrementalCheckError(
            "incremental self-check failed: canonical forms differ"
        )
    if arguments.ci and new_error_count > 0:
        from .errors import I18nToolError

        raise I18nToolError(
            f"incremental CI gate failed: {new_error_count} new ERROR findings"
        )
    return 0


def _load_document_at(
    repository: GitRepository,
    loader: LocaleLoader,
    commit: str,
    logical_path: str,
) -> Any | None:
    """Load a logical translation document at ``commit``; None only when the
    file is genuinely absent there. Git failures and Lua loader errors
    propagate (fail closed): a corrupt document is never treated as missing
    and an absent one is never mistaken for a broken repository."""
    blob = repository.read_blob_optional(commit, logical_path)
    if blob is None:
        return None
    return loader.load_bytes(blob, logical_path=logical_path)


def _document_specs_at_commit(
    repository: GitRepository,
    loader: LocaleLoader,
    components: Iterable[ComponentSpec],
    commit: str,
) -> tuple[list[tuple[str, Any, bool]], dict[tuple[str, str], Any | None]]:
    """Load main + copy documents of every component at ``commit``.

    Returns (specs, docs_by_file) where docs_by_file maps (component_id,
    logical_path) to the document or None when the file is absent at that
    commit. The logical path stays identical across commits so identical
    entries produce identical Issue logical_paths (self-check parity).
    """
    specs: list[tuple[str, Any, bool]] = []
    docs: dict[tuple[str, str], Any | None] = {}
    for component in components:
        main = _load_document_at(repository, loader, commit, component.translation)
        docs[(component.id, component.translation)] = main
        if main is not None:
            specs.append((component.id, main, False))
        if component.copy_fragment:
            copy = _load_document_at(
                repository, loader, commit, component.copy_fragment
            )
            docs[(component.id, component.copy_fragment)] = copy
            if copy is not None:
                specs.append((component.id, copy, True))
    return specs, docs


def _read_commit_json(
    repository: GitRepository,
    commit: str,
    relative: str,
    label: str,
) -> dict[str, Any]:
    """Read and parse a required JSON artifact at ``commit`` (fail closed)."""
    from .errors import ContractError

    blob = repository.read_blob_optional(commit, relative)
    if blob is None:
        raise ContractError(f"{label} is missing at {commit[:12]}")
    try:
        data = json.loads(blob.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError(
            f"{label}@{commit[:12]} is not valid JSON: {error}"
        ) from error
    if not isinstance(data, dict):
        raise ContractError(f"{label}@{commit[:12]} must be an object")
    return data


def _bind_identity_contexts(
    contexts: dict[str, Any], indexes: dict[str, Any]
) -> dict[str, Any]:
    """FR1: ensure a component-key identity context exists for every indexed
    component.

    Entity-conflict participants are resolved through ``contexts.get(component)``
    in build_finding_records; when a translation document is absent at a
    commit (head-only main/copy), that context would be missing and the
    conflict would fall back to a synthetic participant TU - producing a
    different fingerprint than the side where the document exists. The
    identity binding therefore never depends on document presence: an
    existing main context keeps its entries and gets the index bound, a
    missing one becomes an identity-only context (empty entries, index
    bound). Translation-entry lookups are unaffected (empty entries add no
    groups; _bind still walks every context including the copy fragment).
    """
    from .findings import FindingContext

    bound = dict(contexts)
    for component_id, index in indexes.items():
        existing = bound.get(component_id)
        if existing is not None:
            bound[component_id] = FindingContext(
                component=component_id,
                entries=existing.entries,
                index=index,
            )
        else:
            bound[component_id] = FindingContext(
                component=component_id, entries=(), index=index
            )
    return bound


def _lint_incremental_translation(
    arguments: argparse.Namespace,
    manifest: Manifest,
    runtime: LuaRuntime,
    loader: LocaleLoader,
) -> int:
    from .errors import I18nToolError
    from .fingerprint import RuleRegistry
    from .findings import FindingContext, build_finding_records
    from .git_source import GitRepository
    from .identity import (
        RULES_REGISTRY_RELATIVE_PATH,
        UNLOADED_SOURCES_RELATIVE_PATH,
        UnloadedSources,
        tu_uid_fallback,
    )
    from .lint import parse_policy, stable_entry_id
    from .pipeline import extract_enriched, lint_documents_specs

    repository = GitRepository(manifest.root)
    base, head = arguments.incremental.split("..", 1)
    base = repository.resolve_commit(base)
    head = repository.resolve_commit(head)
    changed = repository.changed_paths(base, head)
    components = _select_components(manifest, arguments.component, default="lint")
    affected_components = [
        component
        for component in components
        if component.translation in changed
        or (
            component.copy_fragment is not None
            and component.copy_fragment in changed
        )
    ]
    if not affected_components:
        # No translation changed: F_new == F_previous, both flags hold
        # trivially; they are reported explicitly, never silently dropped.
        report = {
            "domain": "translation",
            "base": base,
            "head": head,
            "affected_components": [],
            "affected_tus": 0,
            "ok": True,
        }
        if arguments.self_check:
            report["self_check"] = {"passed": True, "full_findings": 0}
        report["ci"] = {"new_errors": 0, "legacy_errors": 0}
        if arguments.json:
            _print_json(report)
        else:
            print("translation domain: no translation files changed in the range")
        return 0
    indexes, _ = extract_enriched(manifest, runtime, components)
    # H4/V4: the rules registry, unloaded-sources registry and lint policy
    # all come from the resolved head commit blobs (never the worktree), so
    # uncommitted content cannot masquerade as head. Reads are fail-closed.
    head_registry = RuleRegistry.from_dict(
        _read_commit_json(repository, head, RULES_REGISTRY_RELATIVE_PATH, "rule registry"),
        label=f"rule registry@{head[:12]}",
    )
    unloaded_sources = UnloadedSources.from_dict(
        _read_commit_json(
            repository, head, UNLOADED_SOURCES_RELATIVE_PATH, "unloaded-sources registry"
        ),
        label=f"unloaded-sources registry@{head[:12]}",
    )
    head_policy = parse_policy(
        _read_commit_json(repository, head, manifest.policy, "lint policy"),
        label=f"lint policy@{head[:12]}",
    )

    def semantic(entry: dict[str, Any]) -> str:
        import json as _json

        return _json.dumps(
            [entry.get("target"), entry.get("args_order"), entry.get("special")],
            ensure_ascii=False,
            sort_keys=True,
        )

    # H4/D5/V4: the main translation and the copy fragment are independent
    # logical documents; each is loaded from the resolved base and head
    # commit blobs (never the worktree) so base records represent the true
    # base (including copy-fragment findings) and added / deleted /
    # semantically-changed entries are collected bidirectionally. A
    # genuinely absent file on either side compares as the empty side;
    # loader errors fail closed.
    specs_head, head_docs = _document_specs_at_commit(
        repository, loader, components, head
    )
    specs_base, base_docs = _document_specs_at_commit(
        repository, loader, components, base
    )
    logical_files: list[tuple[str, str, bool]] = []
    for component in components:
        logical_files.append((component.id, component.translation, False))
        if component.copy_fragment:
            logical_files.append((component.id, component.copy_fragment, True))

    affected_tus: set[str] = set()

    def add_editorial(
        component_id: str, section: str, source: str, source_tag: str | None
    ) -> None:
        editorial_id = stable_entry_id(component_id, section, source, source_tag)
        component_index = indexes.get(component_id)
        candidates = (
            component_index.editorial_to_tu.get(editorial_id, ())
            if component_index is not None
            else ()
        )
        if candidates:
            affected_tus.update(candidates)
        else:
            # No index mapping: use the frozen fallback TU, exactly like
            # build_finding_records::_bind (D5).
            affected_tus.add(tu_uid_fallback(editorial_id))

    def collect_changes(
        component_id: str, base_doc: Any | None, head_doc: Any | None
    ) -> None:
        base_entries = (
            list(base_doc.translations) if base_doc is not None else []
        )
        head_entries = (
            list(head_doc.translations) if head_doc is not None else []
        )
        if not base_entries and not head_entries:
            return
        if base_doc is None or head_doc is None:
            # Head-only or base-only logical file: every entry that exists
            # on either side changed (added or deleted).
            changed_keys = {
                (
                    entry.get("section"),
                    entry.get("source"),
                    entry.get("source_tag"),
                )
                for entry in [*base_entries, *head_entries]
            }
        else:
            changed_keys = _changed_editorial_keys(
                base_entries, head_entries, semantic
            )
        for section, source, source_tag in changed_keys:
            add_editorial(
                component_id, section or "", source or "", source_tag
            )

    for component_id, path, _is_copy in logical_files:
        collect_changes(
            component_id,
            base_docs.get((component_id, path)),
            head_docs.get((component_id, path)),
        )

    issues_head, contexts_head, _ = lint_documents_specs(
        manifest, specs_head, policy=head_policy
    )
    issues_base, contexts_base, _ = lint_documents_specs(
        manifest, specs_base, policy=head_policy
    )
    conflicts: list[Any] = []
    for index in indexes.values():
        conflicts.extend(index.conflicts)

    def records_for(issues: Any, contexts: Any) -> list[Any]:
        bound = {
            name: FindingContext(
                component=context.component,
                entries=context.entries,
                index=indexes.get(context.component),
            )
            for name, context in contexts.items()
        }
        # FR1: the identity binding must not depend on whether the component
        # document exists at this commit.
        bound = _bind_identity_contexts(bound, indexes)
        records, _ = build_finding_records(
            registry=head_registry,
            issues=issues,
            contexts=bound,
            conflicts=conflicts,
            unloaded_sources=unloaded_sources,
        )
        return records

    head_records = records_for(issues_head, contexts_head)
    base_records = records_for(issues_base, contexts_base)

    # R2 (cycle 3): recompute/kept are participant-aware, and runtime
    # collision records are correlated across the base/head sides through a
    # stable family key. The subject of a runtime-collision record is the
    # collision-id fallback TU while the actual editorial TUs live in
    # participants; a touched participant forces recompute on the head side
    # and out of kept on the base side. Because the collision_id (issue
    # entry_id) is a hash of component/source/source_tag, both sides of the
    # same collision share one family key: when ANY member of the family is
    # directly touched (e.g. base A+B already collides and head adds C, with
    # only C affected), the base member must leave kept and the head member
    # must be recomputed - otherwise the stale A+B record would linger next
    # to the correct A+B+C record.
    def _touched(record: Any) -> bool:
        return record.tu_uid in affected_tus or any(
            participant in affected_tus for participant in record.participants
        )

    def _family_key(record: Any) -> tuple[Any, ...] | None:
        if record.rule_id == "runtime-collision" and record.issue.entry_id is not None:
            return ("runtime-collision", record.issue.entry_id)
        return None

    touched_families = frozenset(
        key
        for record in [*base_records, *head_records]
        for key in [(_family_key(record) if _touched(record) else None)]
        if key is not None
    )

    def _record_affected(record: Any) -> bool:
        if _touched(record):
            return True
        key = _family_key(record)
        return key is not None and key in touched_families

    recomputed = tuple(record for record in head_records if _record_affected(record))
    kept = tuple(record for record in base_records if not _record_affected(record))
    incremental_records = tuple(
        sorted([*kept, *recomputed], key=lambda record: record.fingerprint)
    )
    report: dict[str, Any] = {
        "domain": "translation",
        "base": base,
        "head": head,
        "affected_components": [component.id for component in affected_components],
        "affected_tus": len(affected_tus),
        "affected_tu_uids": sorted(affected_tus),
        "findings": {
            "previous": len(base_records),
            "kept": len(kept),
            "recomputed": len(recomputed),
            "incremental": len(incremental_records),
        },
        "records": [record.to_dict() for record in incremental_records],
        "ok": True,
    }
    if arguments.self_check:
        from .invalidation import self_check as canonical_self_check

        passed = canonical_self_check(
            incremental=incremental_records, full=head_records
        )
        report["self_check"] = {
            "passed": passed,
            "full_findings": len(head_records),
        }
        report["ok"] = report["ok"] and passed
    # H4/D5: report new/legacy error counts regardless of --ci; the gate only
    # fails when --ci is passed (legacy ERROR stays technical debt).
    previous_error_fingerprints = {
        record.fingerprint
        for record in base_records
        if record.issue.severity == "error"
    }
    new_errors = sum(
        1
        for record in incremental_records
        if record.issue.severity == "error"
        and record.fingerprint not in previous_error_fingerprints
    )
    legacy_errors = sum(
        1
        for record in incremental_records
        if record.issue.severity == "error"
        and record.fingerprint in previous_error_fingerprints
    )
    report["ci"] = {"new_errors": new_errors, "legacy_errors": legacy_errors}
    if arguments.ci:
        # The CI gate is opt-in: counts are always reported, but new_errors
        # only influences ok/exit when --ci is passed (legacy CLI semantics).
        report["ok"] = report["ok"] and new_errors == 0
    if arguments.json:
        _print_json(report)
    else:
        findings = report["findings"]
        print(
            f"incremental translation {base}..{head}: "
            f"affected_tus={len(affected_tus)} "
            f"previous={findings['previous']} kept={findings['kept']} "
            f"recomputed={findings['recomputed']} "
            f"incremental={findings['incremental']}"
        )
        if report.get("ci") is not None:
            print(f"ci: new_errors={report['ci']['new_errors']}")
    if arguments.self_check and report["self_check"]["passed"] is False:
        from .errors import IncrementalCheckError

        raise IncrementalCheckError(
            "incremental self-check failed: canonical forms differ"
        )
    if arguments.ci and report["ci"]["new_errors"] > 0:
        raise I18nToolError(
            "incremental CI gate failed: "
            f"{report['ci']['new_errors']} new ERROR findings"
        )
    return 0
