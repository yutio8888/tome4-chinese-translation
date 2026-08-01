"""Command-line interface for the localization toolchain."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

from . import TOOL_VERSION
from .build import build_addon_locale, build_full_locales
from .config import ComponentSpec, Manifest, load_manifest
from .context import resolve_context
from .errors import I18nToolError, ValidationError
from .extract import extract_components, probe_protected_component
from .git_source import GitRepository
from .lint import Issue, lint_documents, lint_terminology, load_policy
from .locale_model import LocaleLoader
from .merge import run_merge
from .proposal import validate_proposal
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
        return [manifest.component(identifier) for identifier in requested]
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

    required_files = [
        manifest.root / manifest.terminology,
        manifest.root / manifest.policy,
        *(manifest.root / component.translation for component in manifest.components),
        *(manifest.root / path for path in manifest.manual_definitions),
    ]
    missing = [str(path) for path in required_files if not path.is_file()]
    if missing:
        raise ValidationError("required localization files are missing: " + ", ".join(missing))

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
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    policy = load_policy(manifest)
    components = _select_components(manifest, arguments.component, default="lint")
    documents = []
    for component in components:
        if component.copy_fragment:
            documents.append(
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
    issues, metrics = lint_documents(documents, policy)
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
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    components = _select_components(manifest, arguments.component, default="status")
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
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    if arguments.component:
        components = [manifest.component(value) for value in arguments.component]
        if arguments.profile == "addon":
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
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    component = manifest.component(arguments.component)
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
    manifest = _manifest(arguments)
    runtime = LuaRuntime(manifest)
    runtime.doctor()
    loader = LocaleLoader(runtime)
    component = manifest.component(arguments.component)
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


def main(argv: list[str] | None = None) -> int:
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
        raise AssertionError(f"unhandled command: {arguments.command}")
    except I18nToolError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return error.exit_code
