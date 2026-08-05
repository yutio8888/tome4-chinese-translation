"""Command-line interface for the localization toolchain."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterable

from . import TOOL_VERSION
from .build import build_addon_locale, build_full_locales
from .config import ComponentSpec, Manifest, load_manifest
from .context import resolve_context, validate_context_options
from .errors import I18nToolError, ValidationError
from .extract import extract_components, probe_protected_component
from .git_source import GitRepository
from .lint import Issue, lint_documents, lint_terminology, load_policy
from .locale_model import LocaleLoader
from .merge import run_merge
from .proposal import validate_proposal
from .publish import publish_addon
from .quality import (
    create_quality_run_directory,
    load_taxonomy,
    run_dry_run as quality_run_dry_run,
    run_inventory as quality_run_inventory,
    run_report as quality_run_report,
    run_sample as quality_run_sample,
    run_validation as quality_run_validation,
)
from .quality_v2 import (
    adjudicate_v2,
    build_disputes_v2,
    build_report_v2,
    canonical_sha256,
    load_anchors,
    load_impact_rules,
    load_policy_v2,
    match_assessments_v2,
    read_json_object,
    run_calibration_v2,
    run_evaluator_bundles_v2,
    validate_assessment_v2,
    validate_sample_v2,
)
from .report import create_run_directory, write_json
from .review import create_review_index, review_index_summary
from .runtime import LuaRuntime
from .status import status_report
from .workset import create_workset


def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--version-manifest",
        default="tome-1.7.6",
        metavar="VERSION",
        help="version manifest name (default: tome-1.7.6)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="explicit manifest path for the selected --version-manifest",
    )
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tools/i18n",
        description="ToME4 Chinese localization toolchain",
    )
    parser.add_argument("--tool-version", action="version", version=TOOL_VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="validate the pinned toolchain")
    _add_common_arguments(doctor)

    extract = subparsers.add_parser(
        "extract",
        help="extract source strings from pinned Git objects or protected Lua-only inputs",
    )
    _add_common_arguments(extract)
    extract.add_argument(
        "--component",
        action="append",
        default=[],
        metavar="ID",
        help="component to extract; may be repeated",
    )
    extract.add_argument(
        "--all",
        action="store_true",
        help="extract every component with a public or protected source mapping",
    )
    extract.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="per-component extractor timeout in seconds (default: 900)",
    )

    lint = subparsers.add_parser("lint", help="validate canonical translations")
    _add_common_arguments(lint)
    lint.add_argument(
        "--component", action="append", default=[], metavar="ID", help="component to lint"
    )
    lint.add_argument(
        "--strict", action="store_true", help="treat warnings as blocking failures"
    )

    status = subparsers.add_parser(
        "status", help="compare canonical translations with pinned official locales"
    )
    _add_common_arguments(status)
    status.add_argument(
        "--component", action="append", default=[], metavar="ID", help="component to compare"
    )

    build = subparsers.add_parser(
        "build", help="build deterministic full or addon locale artifacts"
    )
    _add_common_arguments(build)
    build.add_argument(
        "--profile",
        required=True,
        choices=("full", "addon"),
        help="artifact profile to build",
    )
    build.add_argument(
        "--component",
        action="append",
        default=[],
        metavar="ID",
        help=(
            "component to build; may be repeated. For addon builds, an explicit "
            "selection is an independently checkable minimal overlay"
        ),
    )
    build.add_argument(
        "--require-complete",
        action="store_true",
        help="fail an addon build when any required component/layer is unavailable",
    )

    publish = subparsers.add_parser(
        "publish",
        help=(
            "publish the core addon overlay into the release addon repository "
            "(dry run by default; use --apply to write)"
        ),
    )
    _add_common_arguments(publish)
    publish.add_argument(
        "--apply",
        action="store_true",
        help="write the artifact into the release repository (default: dry run)",
    )
    publish.add_argument(
        "--bump",
        action="store_true",
        help="bump addon_version patch in release init.lua",
    )
    publish.add_argument(
        "--commit",
        action="store_true",
        help="git add/commit the published files in the release repository",
    )

    merge = subparsers.add_parser(
        "merge", help="classify a snapshot and generate a non-destructive candidate"
    )
    _add_common_arguments(merge)
    merge.add_argument("--component", required=True, metavar="ID")
    merge.add_argument(
        "--snapshot",
        required=True,
        type=Path,
        help="new normalized extraction snapshot.jsonl",
    )
    merge.add_argument(
        "--base-snapshot",
        type=Path,
        help="previous accepted snapshot; omit for bootstrap coverage mode",
    )

    workset = subparsers.add_parser(
        "workset", help="create a bounded translation workset from a merge report"
    )
    _add_common_arguments(workset)
    workset.add_argument("--merge-report", required=True, type=Path)
    workset.add_argument("--limit", type=int, default=50)
    workset.add_argument(
        "--section",
        dest="section_prefix",
        help="only include sections with this prefix",
    )
    workset.add_argument(
        "--classification",
        choices=("all", "added", "untranslated-existing", "source-changed"),
        default="all",
    )

    context = subparsers.add_parser(
        "context", help="resolve bounded canonical translation and terminology context"
    )
    _add_common_arguments(context)
    context.add_argument("--component", required=True, metavar="ID")
    context.add_argument("--section", dest="section_prefix")
    context.add_argument("--query")
    context.add_argument("--limit", type=int, default=50)

    review = subparsers.add_parser(
        "review", help="create bounded Pi review bundles for an explicit scope"
    )
    _add_common_arguments(review)
    review.add_argument("--batch-size", type=int, default=50)
    review.add_argument(
        "--scope",
        action="append",
        choices=("translations", "code"),
        required=True,
        help="review scope; repeat to include both translations and code",
    )

    proposal = subparsers.add_parser(
        "proposal", help="validate a structured proposal against its workset"
    )
    _add_common_arguments(proposal)
    proposal.add_argument("--workset", required=True, type=Path)
    proposal.add_argument("--proposal", required=True, type=Path)
    proposal.add_argument("--allow-partial", action="store_true")
    proposal.add_argument("--strict", action="store_true")

    quality = subparsers.add_parser(
        "quality",
        help=(
            "translation quality: current-revision inventory, deterministic "
            "pilot sampling, strict assessment/adjudication validation and "
            "consistency reports"
        ),
    )
    quality_subparsers = quality.add_subparsers(dest="quality_command", required=True)
    quality_inventory = quality_subparsers.add_parser(
        "inventory",
        help="build the current revision inventory with deterministic gate/risk facts",
    )
    _add_common_arguments(quality_inventory)
    quality_sample = quality_subparsers.add_parser(
        "sample",
        help="deterministic stratified pilot sample and assessment templates",
    )
    _add_common_arguments(quality_sample)
    quality_sample.add_argument(
        "--inventory",
        required=True,
        type=Path,
        help="inventory.jsonl produced by 'quality inventory'",
    )
    quality_sample.add_argument(
        "--size",
        type=int,
        default=None,
        help="sample size (default: policy pilot size 120)",
    )
    quality_sample.add_argument(
        "--seed",
        default=None,
        help="deterministic sampling seed (default: policy seed)",
    )
    quality_sample.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "build the 12-item rubric try-out bundle that never enters the "
            "official pilot sample (size/seed come from policy dry_run)"
        ),
    )
    quality_validate = quality_subparsers.add_parser(
        "validate",
        help=(
            "strictly validate sample, assessments and adjudication against "
            "taxonomy/policy and revision identity"
        ),
    )
    _add_common_arguments(quality_validate)
    quality_validate.add_argument("--sample", required=True, type=Path)
    quality_validate.add_argument(
        "--assessment",
        action="append",
        default=[],
        type=Path,
        metavar="ASSESSMENT",
        help="assessment JSON; may be repeated (pilot: exactly two)",
    )
    quality_validate.add_argument(
        "--adjudication",
        type=Path,
        help="adjudication JSON (required for the official pilot sample)",
    )
    quality_validate.add_argument(
        "--dry-run",
        action="store_true",
        help="validate a dry-run sample; adjudication is optional",
    )
    quality_validate.add_argument("--strict", action="store_true")
    quality_report = quality_subparsers.add_parser(
        "report",
        help="build the consistency and calibration report from a validation run",
    )
    _add_common_arguments(quality_report)
    quality_report.add_argument("--validation", required=True, type=Path)
    quality_calibration = quality_subparsers.add_parser(
        "calibration", help="generate mutually-exclusive evaluator-v2 calibration and holdout datasets",
    )
    _add_common_arguments(quality_calibration)
    quality_calibration.add_argument("--inventory", required=True, type=Path)
    quality_calibration.add_argument("--calibration-size", type=int, default=32)
    quality_calibration.add_argument("--holdout-size", type=int, default=32)
    quality_bundles = quality_subparsers.add_parser(
        "evaluator-bundles", help="build offline evaluator-v2 shards without calling a provider",
    )
    _add_common_arguments(quality_bundles)
    quality_bundles.add_argument("--sample", required=True, type=Path)
    quality_bundles.add_argument("--evaluator", required=True)
    quality_bundles.add_argument("--max-items", type=int, default=20)
    quality_match = quality_subparsers.add_parser(
        "match", help="normalize and match two complete evaluator-v2 assessments",
    )
    _add_common_arguments(quality_match)
    quality_match.add_argument("--sample", required=True, type=Path)
    quality_match.add_argument("--assessment", action="append", required=True, type=Path)
    quality_disputes = quality_subparsers.add_parser(
        "disputes", help="build an anonymous dispute bundle and separate identity mapping",
    )
    _add_common_arguments(quality_disputes)
    quality_disputes.add_argument("--match", required=True, type=Path)
    quality_disputes.add_argument("--sample", required=True, type=Path)
    quality_disputes.add_argument("--assessment", action="append", required=True, type=Path)
    quality_disputes.add_argument("--seed", default="tome4-quality-disputes-v2")
    quality_adjudicate = quality_subparsers.add_parser(
        "adjudicate-v2", help="validate human fact adjudication and recompute severity",
    )
    _add_common_arguments(quality_adjudicate)
    quality_adjudicate.add_argument("--match", required=True, type=Path)
    quality_adjudicate.add_argument("--adjudication", required=True, type=Path)
    quality_adjudicate.add_argument("--strict", action="store_true")
    quality_report_v2 = quality_subparsers.add_parser(
        "report-v2", help="build evaluator-v2 item, issue, fact, severity and burden metrics",
    )
    _add_common_arguments(quality_report_v2)
    quality_report_v2.add_argument("--match", required=True, type=Path)
    quality_report_v2.add_argument("--adjudication-validation", type=Path)
    return parser


def _manifest(arguments: argparse.Namespace) -> Manifest:
    return load_manifest(
        version=arguments.version_manifest,
        manifest_path=arguments.manifest,
    )


def _select_components(
    manifest: Manifest,
    identifiers: Iterable[str],
    *,
    default: str,
) -> list[ComponentSpec]:
    requested = list(identifiers)
    if requested:
        return [
            manifest.component(identifier)
            for identifier in dict.fromkeys(requested)
        ]
    if default == "extract":
        return [component for component in manifest.components if component.extract_by_default]
    if default == "status":
        return [
            component
            for component in manifest.components
            if component.official_locale is not None
        ]
    return list(manifest.components)


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def _doctor(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    required_files = [
        manifest.root / manifest.terminology,
        manifest.root / manifest.policy,
        *(manifest.root / component.translation for component in manifest.components),
        *(
            manifest.root / component.copy_fragment
            for component in manifest.components
            if component.copy_fragment is not None
        ),
        *(manifest.root / path for path in manifest.manual_definitions),
    ]
    missing = []
    not_regular = []
    for path in required_files:
        if path.is_file():
            continue
        if path.exists():
            not_regular.append(str(path))
        else:
            missing.append(str(path))
    if missing or not_regular:
        problems = []
        if missing:
            problems.append("missing: " + ", ".join(missing))
        if not_regular:
            problems.append("not regular files: " + ", ".join(not_regular))
        raise ValidationError(
            "required localization files are invalid: " + "; ".join(problems)
        )

    runtime = LuaRuntime(manifest)
    runtime_report = runtime.doctor()
    repositories: dict[str, Any] = {}
    warnings: list[str] = []
    for name, spec in manifest.repositories.items():
        path = spec.resolve(manifest.root)
        if not path.exists() and not spec.required:
            warnings.append(f"optional repository is absent: {name}: {path}")
            repositories[name] = {"path": str(path), "available": False}
            continue
        repository = GitRepository(path)
        check_worktree = name not in manifest.protected_repositories
        report = repository.validate(
            spec.commit, check_worktree=check_worktree
        )
        report["available"] = True
        if report["clean"] is False:
            warnings.append(f"repository has worktree changes: {name}: {path}")
        if not check_worktree:
            warnings.append(
                f"repository worktree scan skipped because it contains a protected source: {name}"
            )
        repositories[name] = report

    extractor_repository = GitRepository(
        manifest.repository_path(manifest.extractor.repository)
    )
    extractor_repository.validate(
        manifest.extractor.commit, check_worktree=False
    )

    protected_sources: dict[str, Any] = {}
    for component in manifest.components:
        if component.protected_source is None:
            continue
        available = probe_protected_component(manifest, runtime, component)
        protected_sources[component.id] = {
            "available": available,
            "access": "lua-extractor-only",
        }
        if not available:
            warnings.append(
                f"declared protected source is unavailable: {component.id}"
            )

    report = {
        "ok": True,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "manifest": str(manifest.path),
        "runtime": runtime_report,
        "repositories": repositories,
        "protected_sources": protected_sources,
        "extractor_commit": manifest.extractor.commit,
        "warnings": warnings,
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  manifest       {manifest.version}")
        print(
            "OK  runtime        "
            f"{runtime_report['lua_version']} / {runtime_report['luajit_version']}"
        )
        print(
            "OK  LPeg           "
            f"{runtime_report['lpeg_rock_version']} ({runtime_report['lpeg_runtime_version']})"
        )
        for name, repository in repositories.items():
            availability = "OK" if repository.get("available") else "SKIP"
            detail = repository.get("path")
            print(f"{availability:<5}repository      {name}: {detail}")
        for component, protected in protected_sources.items():
            availability = "OK" if protected["available"] else "SKIP"
            print(
                f"{availability:<5}protected source {component}: "
                f"{protected['access']}"
            )
        for warning in warnings:
            print(f"WARN              {warning}")
    return 0


def _extract(arguments: argparse.Namespace) -> int:
    if arguments.timeout < 1:
        raise ValidationError("--timeout must be a positive integer")
    manifest = _manifest(arguments)
    components = _select_components(
        manifest, arguments.component, default="extract"
    )
    if arguments.all:
        components = [
            component
            for component in manifest.components
            if (
                component.source_repository is not None and component.sources
            )
            or component.protected_source is not None
        ]
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    report = extract_components(
        manifest,
        runtime,
        components,
        timeout=arguments.timeout,
    )
    if arguments.json:
        _print_json(report)
    else:
        for item in report["components"]:
            print(
                f"OK  {item['component']:<16} "
                f"{item['tdef_count']:>7} tDef  {item['snapshot_sha256'][:16]}"
            )
        print(f"Artifacts: {report['run_directory']}")
    return 0


def _issue_line(issue: Issue) -> str:
    location = issue.logical_path
    if issue.line is not None:
        location += f":{issue.line}"
    return f"{issue.severity.upper():7} {issue.code:24} {location}  {issue.message}"


def _lint(arguments: argparse.Namespace) -> int:
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


def _status(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    components = _select_components(manifest, arguments.component, default="status")
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    report = status_report(manifest, loader, components)
    run_directory = create_run_directory(manifest.root, "status")
    report["run_directory"] = str(run_directory)
    write_json(run_directory / "status.json", report)
    if arguments.json:
        _print_json(report)
    else:
        for item in report["components"]:
            if not item["official_available"]:
                print(
                    f"SKIP {item['component']:<16} no pinned official locale "
                    f"({item['canonical_entries']} canonical entries)"
                )
                continue
            print(
                f"OK   {item['component']:<16} "
                f"same={item['identical']} changed={item['changed']} "
                f"new={item['canonical_only']} official-only={item['official_only']}"
            )
        print(f"Report: {run_directory / 'status.json'}")
    return 0


def _build(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    if arguments.component:
        components = _select_components(
            manifest, arguments.component, default="build"
        )
        if arguments.profile == "full":
            missing_outputs = [
                component.id
                for component in components
                if component.full_output is None
            ]
            if missing_outputs:
                label = "component" if len(missing_outputs) == 1 else "components"
                verb = "has" if len(missing_outputs) == 1 else "have"
                raise ValidationError(
                    f"{label} {', '.join(repr(value) for value in missing_outputs)} "
                    f"{verb} no full_output mapping"
                )
        else:
            non_eligible = [
                component.id for component in components if not component.addon_eligible
            ]
            if non_eligible:
                raise ValidationError(
                    "addon build requires addon-eligible components; not eligible: "
                    + ", ".join(non_eligible)
                )
    elif arguments.profile == "full":
        components = [
            component
            for component in manifest.components
            if component.full_output is not None
        ]
    else:
        components = [
            component for component in manifest.components if component.addon_eligible
        ]
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    if arguments.profile == "full":
        report = build_full_locales(manifest, loader, components)
    else:
        report = build_addon_locale(
            manifest,
            loader,
            components,
            include_external_requirements=not bool(arguments.component),
        )
    if arguments.json:
        _print_json(report)
    elif arguments.profile == "full":
        for item in report["components"]:
            print(
                f"OK  {item['component']:<16} {item['translation_entries']:>7} entries  "
                f"{item['sha256'][:16]}"
            )
        print(f"Artifacts: {report['run_directory']}")
    else:
        for item in report["components"]:
            print(
                f"OK  {item['component']:<16} delta={item['delta_entries']} "
                f"inherited={item['inherited_entries']} "
                f"override={item['override_entries']} new={item['new_entries']}"
            )
        for item in report["skipped"]:
            print(f"SKIP {item['component']:<16} {item['reason']}")
        completeness = "complete" if report["complete"] else "INCOMPLETE"
        print(
            f"Addon artifact: {completeness}, "
            f"{report['verification']['patch_runtime_keys']} runtime keys, "
            f"{report['sha256'][:16]}"
        )
        print(f"Output: {report['output']}")
    if (
        arguments.profile == "addon"
        and arguments.require_complete
        and not report["complete"]
    ):
        raise ValidationError(
            "addon artifact is incomplete; see "
            f"{Path(report['run_directory']) / 'build.json'}"
        )
    return 0


def _merge(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    component = manifest.component(arguments.component)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    report = run_merge(
        manifest,
        loader,
        component,
        new_snapshot_path=arguments.snapshot,
        base_snapshot_path=arguments.base_snapshot,
    )
    if arguments.json:
        _print_json(report)
    else:
        counts = report["counts"]
        print(
            f"OK  {component.id:<16} candidate={counts['candidate_translations']} "
            f"exact={counts['exact_editorial']} moved={counts['moved_section']}"
        )
        print(
            f"    untranslated={counts['untranslated']} "
            f"source-changed={counts['source_changed_suggestions']} "
            f"obsolete/unextracted={counts['obsolete_or_unextracted']}"
        )
        safety = "SAFE" if report["safe_to_apply"] else "REVIEW REQUIRED"
        print(f"Candidate: {safety}  {report['candidate']}")
        print(f"Report: {report['report']}")
    return 0


def _workset(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    workset = create_workset(
        manifest,
        merge_report_path=arguments.merge_report,
        limit=arguments.limit,
        section_prefix=arguments.section_prefix,
        classification=arguments.classification,
    )
    if arguments.json:
        _print_json(workset)
    else:
        selection = workset["selection"]
        print(
            f"OK  workset {workset['workset_id'][:16]}  "
            f"selected={selection['selected']}/"
            f"{selection['available_after_filter']} terms={len(workset['terminology'])}"
        )
        print(f"Output: {workset['output']}")
        print(f"Proposal template: {workset['proposal_template']}")
    return 0


def _context(arguments: argparse.Namespace) -> int:
    validate_context_options(
        section_prefix=arguments.section_prefix,
        query=arguments.query,
        limit=arguments.limit,
    )
    manifest = _manifest(arguments)
    component = manifest.component(arguments.component)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    result = resolve_context(
        manifest,
        loader,
        component,
        section_prefix=arguments.section_prefix,
        query=arguments.query,
        limit=arguments.limit,
    )
    if arguments.json:
        _print_json(result)
    else:
        selection = result["selection"]
        print(
            f"OK  context {result['context_id'][:16]}  "
            f"selected={selection['selected']}/{selection['available']} "
            f"terms={len(result['terminology'])}"
        )
        print(f"Output: {result['output']}")
    return 0


def _review(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    scopes = frozenset(arguments.scope)
    index = create_review_index(
        manifest,
        batch_size=arguments.batch_size,
        include_translations="translations" in scopes,
        include_code="code" in scopes,
    )
    if arguments.json:
        _print_json(index)
    else:
        summary = review_index_summary(index)
        print(
            f"OK  review {summary['review_id'][:16]}  "
            f"bundles={summary['bundles']} "
            f"translations={summary['translation_bundles']} "
            f"code={summary['code_bundles']}"
        )
        print(f"Index: {summary['index']}")
        if index.get("redacted_absolute_path_count"):
            print(
                "Redacted absolute paths: "
                f"{index['redacted_absolute_path_count']}"
            )
    return 0


def _proposal(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = validate_proposal(
        manifest,
        workset_path=arguments.workset,
        proposal_path=arguments.proposal,
        allow_partial=arguments.allow_partial,
        strict=arguments.strict,
    )
    if arguments.json:
        _print_json(report)
    else:
        coverage = report["coverage"]
        print(
            f"{'OK' if report['ok'] else 'FAIL'} proposal "
            f"{report['proposal_id'][:16]}  "
            f"coverage={coverage['proposed']}/{coverage['workset_items']} "
            f"errors={report['errors']} warnings={report['warnings']}"
        )
        print(f"Report: {report['report']}")
        if report.get("validated_proposal"):
            print(f"Validated: {report['validated_proposal']}")
    if not report["ok"]:
        raise ValidationError(
            f"proposal validation failed with {report['errors']} errors and "
            f"{report['warnings']} warnings"
        )
    return 0


def _publish(arguments: argparse.Namespace) -> int:
    if arguments.commit and not arguments.apply:
        raise ValidationError("publish --commit requires --apply")

    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    report = publish_addon(
        manifest,
        loader,
        apply=arguments.apply,
        bump=arguments.bump,
        commit=arguments.commit,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(f"Release repository: {report['release_repository']}")
        print(f"Locale file:        {report['locale_file']}")
        print(
            f"Entries:            {report['old_entries']} -> {report['new_entries']} "
            f"(delta {report['delta_runtime_keys']} runtime keys)"
        )
        print(f"SHA-256:            {report['old_sha256'][:16]} -> {report['new_sha256'][:16]}")
        if report.get("bump_addon_version"):
            print(
                f"addon_version:      {report['old_addon_version']} -> "
                f"{report['new_addon_version']}"
            )
        if report["applied"]:
            print(
                f"Applied:            OK (verified {report['verified_entries']} entries)"
            )
            if report.get("release_head"):
                print(f"Release HEAD:       {report['release_head']}")
        else:
            print("Applied:            dry run (re-run with --apply to publish)")
    return 0


_PUBLIC_DLC_ROOT = Path("/Users/yun/projects/tome4-dlcs")
_PUBLIC_DLC_PATHS = {
    "TOME_DLC_ASHES_ROOT": "ashes-urhrok/tome-ashes-urhrok",
    "TOME_DLC_CULTS_ROOT": "cults/tome-cults",
    "TOME_DLC_ORCS_ROOT": "orcs/tome-orcs",
}


def _inject_public_dlc_env() -> None:
    """Point DLC extraction at the public GPL v3 release when the env is unset.

    The official DLC sources are GPL v3 public (see AGENTS.md). The public
    release under _PUBLIC_DLC_ROOT is the canonical extraction input; the
    legacy TOME_DLC_*_ROOT values (if set by the user) still take precedence.
    """
    if not _PUBLIC_DLC_ROOT.is_dir():
        return
    for env_name, relative in _PUBLIC_DLC_PATHS.items():
        if env_name in os.environ:
            continue
        candidate = _PUBLIC_DLC_ROOT / relative
        if candidate.is_dir():
            os.environ[env_name] = str(candidate)


def _quality_inventory(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    report = quality_run_inventory(manifest, loader)
    if arguments.json:
        _print_json(report)
    else:
        summary = report["summary"]
        print(
            f"OK  quality inventory {report['version']}  "
            f"entries={summary['entries']} occurrences={summary['occurrences']}"
        )
        print(f"    sha256={report['inventory_sha256'][:16]}")
        print(f"    profiles={summary['profiles']}")
        print(f"    risk flags={summary['risk_flags']}")
        print(f"Output: {report['inventory']}")
    return 0


def _quality_sample(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    if arguments.dry_run:
        if arguments.size is not None or arguments.seed is not None:
            raise ValidationError(
                "--dry-run uses the policy dry_run size/seed; "
                "--size/--seed cannot be combined with --dry-run"
            )
        report = quality_run_dry_run(
            manifest,
            inventory_path=arguments.inventory,
        )
        if arguments.json:
            _print_json(report)
        else:
            print(
                f"OK  quality dry-run {report['sample_id'][:16]}  "
                f"size={report['size']} "
                f"official={report['official_sample_id'][:16]}"
            )
            if report["unmet_constraints"]:
                for unmet in report["unmet_constraints"]:
                    print(
                        f"    UNMET {unmet['id']}: "
                        f"{unmet.get('value', '')} "
                        f"{unmet['actual']}/{unmet['target_min']}"
                    )
            print(f"Output: {report['dry_run_path']}")
        return 0
    report = quality_run_sample(
        manifest,
        inventory_path=arguments.inventory,
        size=arguments.size,
        seed=arguments.seed,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"OK  quality sample {report['sample_id'][:16]}  "
            f"size={report['size']} buckets={report['bucket_counts']}"
        )
        print(f"    coverage={report['coverage']}")
        if report["unmet_constraints"]:
            for unmet in report["unmet_constraints"]:
                print(f"    UNMET {unmet['id']}: {unmet['actual']}/{unmet['target_min']}")
        print(f"Output: {report['sample_path']}")
    return 0


def _quality_validate(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    if not arguments.dry_run and arguments.adjudication is None:
        raise ValidationError(
            "quality validate requires --adjudication for the official "
            "pilot sample (or pass --dry-run)"
        )
    report = quality_run_validation(
        manifest,
        sample_path=arguments.sample,
        assessment_paths=arguments.assessment,
        adjudication_path=arguments.adjudication,
        strict=arguments.strict or None,
        dry_run=arguments.dry_run,
    )
    if arguments.json:
        _print_json(report)
    else:
        status = "OK" if report["ok"] else "FAIL"
        print(f"{status} quality validate {report['sample_id'][:16]}")
        for error in report["errors"]:
            print(f"    ERROR {error}")
        for warning in report["warnings"]:
            print(f"    WARN  {warning}")
        for assessment in report["assessments"]:
            print(
                f"    {assessment['evaluator_id']}: {assessment['items']} items"
            )
        print(f"Output: {report['validation_path']}")
    if not report["ok"]:
        raise ValidationError(
            "quality validation failed: "
            + "; ".join(report["errors"][:5])
        )
    return 0


def _quality_report(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    report = quality_run_report(
        manifest,
        validation_path=arguments.validation,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality report {report['sample_id'][:16]}")
        for assessment in report.get("assessments", []):
            print(
                f"    {assessment['evaluator_id']}: items={assessment['items']} "
                f"findings={assessment['findings']}"
            )
        agreement = report.get("agreement", {})
        if "note" not in agreement:
            print(
                f"    context agreement={agreement.get('context_sufficient_agreement')} "
                f"defect agreement={agreement.get('defect_presence_agreement')}"
            )
            print(
                f"    major agreement={agreement.get('major_or_worse_agreement')} "
                f"kappa={agreement.get('severity_weighted_kappa')}"
            )
        print(f"Output: {report['report_md']}")
    return 0


def _quality_calibration_v2(arguments: argparse.Namespace) -> int:
    if arguments.calibration_size != 32 or arguments.holdout_size != 32:
        raise ValidationError("quality v2 calibration and holdout sizes are frozen at 32")
    report = run_calibration_v2(_manifest(arguments), arguments.inventory)
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"OK  quality v2 datasets calibration={report['calibration_id'][:16]} "
            f"holdout={report['holdout_id'][:16]} inventory={report['inventory_entries']}"
        )
        print(f"Manifest: {report['manifest']}")
    return 0


def _quality_evaluator_bundles_v2(arguments: argparse.Namespace) -> int:
    report = run_evaluator_bundles_v2(
        _manifest(arguments), sample_path=arguments.sample,
        evaluator_id=arguments.evaluator, max_items=arguments.max_items,
    )
    if arguments.json:
        _print_json(report)
    else:
        print(
            f"OK  quality v2 shards evaluator={report['evaluator_id']} "
            f"shards={report['shard_count']} max-items={report['max_items']}"
        )
        print(f"Index: {report['index']}")
    return 0


def _quality_v2_inputs(arguments: argparse.Namespace) -> tuple[
    Manifest, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    manifest = _manifest(arguments)
    policy = load_policy_v2(manifest)
    rules = load_impact_rules(manifest, policy)
    anchors = load_anchors(manifest)
    taxonomy = load_taxonomy(manifest)
    return manifest, policy, rules, anchors, taxonomy


def _validated_v2_assessments(
    paths: list[Path], *, sample: dict[str, Any], policy: dict[str, Any],
    rules: dict[str, Any], anchors: dict[str, Any], taxonomy: dict[str, Any],
) -> list[dict[str, Any]]:
    if len(paths) != 2:
        raise ValidationError("quality v2 requires exactly two assessments")
    normalized = []
    expected_rules = canonical_sha256(rules)
    expected_anchors = canonical_sha256(anchors)
    for path in paths:
        value = read_json_object(path, "quality v2 assessment")
        if value.get("evaluator", {}).get("rules_sha256") != expected_rules:
            raise ValidationError("quality v2 assessment rules hash does not match")
        if value.get("evaluator", {}).get("anchors_sha256") != expected_anchors:
            raise ValidationError("quality v2 assessment anchors hash does not match")
        normalized.append(
            validate_assessment_v2(
                value, sample=sample, policy=policy, rules=rules,
                anchors=anchors, taxonomy=taxonomy,
            )
        )
    if [item["evaluator"]["id"] for item in normalized] != policy["evaluator_ids"]:
        raise ValidationError("quality v2 assessments must be reviewer-a then reviewer-b")
    return normalized


def _quality_match_v2(arguments: argparse.Namespace) -> int:
    manifest, policy, rules, anchors, taxonomy = _quality_v2_inputs(arguments)
    sample = validate_sample_v2(read_json_object(arguments.sample, "quality v2 sample"))
    assessments = _validated_v2_assessments(
        arguments.assessment, sample=sample, policy=policy, rules=rules,
        anchors=anchors, taxonomy=taxonomy,
    )
    match = match_assessments_v2(
        sample=sample, left_assessment=assessments[0],
        right_assessment=assessments[1], policy=policy,
    )
    run_directory = create_quality_run_directory(manifest.root, "issue-match-v2")
    path = run_directory / "issue-match.json"
    write_json(path, match)
    report = {
        "match_id": match["match_id"], "issues": len(match["issues"]),
        "manual_queue": len(match["manual_queue"]), "match": str(path),
        "run_directory": str(run_directory),
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality v2 match issues={report['issues']} manual={report['manual_queue']}")
        print(f"Match: {path}")
    return 0


def _quality_disputes_v2(arguments: argparse.Namespace) -> int:
    manifest, policy, rules, anchors, taxonomy = _quality_v2_inputs(arguments)
    sample = validate_sample_v2(read_json_object(arguments.sample, "quality v2 sample"))
    assessments = _validated_v2_assessments(
        arguments.assessment, sample=sample, policy=policy, rules=rules,
        anchors=anchors, taxonomy=taxonomy,
    )
    match = read_json_object(arguments.match, "quality v2 issue match")
    dispute, identity = build_disputes_v2(
        match=match, sample=sample, assessments=(assessments[0], assessments[1]),
        seed=arguments.seed,
    )
    run_directory = create_quality_run_directory(manifest.root, "disputes-v2")
    dispute_path = run_directory / "dispute.json"
    identity_path = run_directory / "dispute-identity.json"
    write_json(dispute_path, dispute)
    write_json(identity_path, identity)
    report = {
        "dispute_id": dispute["dispute_id"], "items": len(dispute["items"]),
        "dispute": str(dispute_path), "identity_mapping": str(identity_path),
        "run_directory": str(run_directory),
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality v2 disputes items={report['items']}")
        print(f"Dispute: {dispute_path}")
        print(f"Identity: {identity_path}")
    return 0


def _quality_adjudicate_v2(arguments: argparse.Namespace) -> int:
    manifest, policy, rules, anchors, _ = _quality_v2_inputs(arguments)
    match = read_json_object(arguments.match, "quality v2 issue match")
    adjudication = read_json_object(arguments.adjudication, "quality v2 adjudication")
    validation = adjudicate_v2(
        match=match, adjudication=adjudication, policy=policy, rules=rules,
        anchors=anchors, strict=arguments.strict,
    )
    run_directory = create_quality_run_directory(manifest.root, "adjudication-v2")
    path = run_directory / "adjudication-validation.json"
    write_json(path, validation)
    report = {
        "validation_id": validation["validation_id"], "items": len(validation["items"]),
        "validation": str(path), "run_directory": str(run_directory),
    }
    if arguments.json:
        _print_json(report)
    else:
        print(f"OK  quality v2 adjudication items={report['items']}")
        print(f"Validation: {path}")
    return 0


def _quality_report_v2(arguments: argparse.Namespace) -> int:
    manifest = _manifest(arguments)
    match = read_json_object(arguments.match, "quality v2 issue match")
    validation = (
        read_json_object(arguments.adjudication_validation, "quality v2 adjudication validation")
        if arguments.adjudication_validation else None
    )
    report = build_report_v2(match=match, adjudication_validation=validation)
    run_directory = create_quality_run_directory(manifest.root, "report-v2")
    path = run_directory / "report.json"
    write_json(path, report)
    summary = {**report, "report": str(path), "run_directory": str(run_directory)}
    if arguments.json:
        _print_json(summary)
    else:
        print(
            f"OK  quality v2 report issues={report['issue_metrics']['issue_union']} "
            f"manual={report['human_burden']['issues_requiring_adjudication']}"
        )
        print(f"Report: {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    _inject_public_dlc_env()
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "doctor":
            return _doctor(arguments)
        if arguments.command == "extract":
            return _extract(arguments)
        if arguments.command == "lint":
            return _lint(arguments)
        if arguments.command == "status":
            return _status(arguments)
        if arguments.command == "build":
            return _build(arguments)
        if arguments.command == "publish":
            return _publish(arguments)
        if arguments.command == "merge":
            return _merge(arguments)
        if arguments.command == "workset":
            return _workset(arguments)
        if arguments.command == "context":
            return _context(arguments)
        if arguments.command == "review":
            return _review(arguments)
        if arguments.command == "proposal":
            return _proposal(arguments)
        if arguments.command == "quality":
            if arguments.quality_command == "inventory":
                return _quality_inventory(arguments)
            if arguments.quality_command == "sample":
                return _quality_sample(arguments)
            if arguments.quality_command == "validate":
                return _quality_validate(arguments)
            if arguments.quality_command == "report":
                return _quality_report(arguments)
            if arguments.quality_command == "calibration":
                return _quality_calibration_v2(arguments)
            if arguments.quality_command == "evaluator-bundles":
                return _quality_evaluator_bundles_v2(arguments)
            if arguments.quality_command == "match":
                return _quality_match_v2(arguments)
            if arguments.quality_command == "disputes":
                return _quality_disputes_v2(arguments)
            if arguments.quality_command == "adjudicate-v2":
                return _quality_adjudicate_v2(arguments)
            if arguments.quality_command == "report-v2":
                return _quality_report_v2(arguments)
            raise AssertionError(
                f"unhandled quality command: {arguments.quality_command}"
            )
        raise AssertionError(f"unhandled command: {arguments.command}")
    except I18nToolError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return error.exit_code
