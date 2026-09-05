"""Registration and handlers for localization commands."""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from .build import build_addon_locale, build_full_locales
from .errors import ValidationError
from .extract import extract_components
from .locale_model import LocaleLoader
from .merge import run_merge
from .publish import publish_addon
from .report import create_run_directory, write_json
from .runtime import LuaRuntime
from .status import status_report
from .cli_common import _add_common_arguments, _manifest, _print_json, _select_components


def register(subparsers: argparse._SubParsersAction) -> None:
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
    extract.add_argument(
        "--enrich",
        action="store_true",
        help=(
            "produce the enrichment sidecar from the same AST traversal and "
            "build the TU identity index (contract §4.3)"
        ),
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
    merge.add_argument(
        "--base-tu-index",
        type=Path,
        help="optional base tu_index.jsonl for L1-L5 identity matching",
    )
    merge.add_argument(
        "--new-tu-index",
        type=Path,
        help="optional new tu_index.jsonl for L1-L5 identity matching",
    )
    extract.set_defaults(handler=dispatch)
    status.set_defaults(handler=dispatch)
    build.set_defaults(handler=dispatch)
    publish.set_defaults(handler=dispatch)
    merge.set_defaults(handler=dispatch)


def dispatch(arguments: argparse.Namespace) -> int:
    if arguments.command == "extract":
        return _extract(arguments)
    if arguments.command == "status":
        return _status(arguments)
    if arguments.command == "build":
        return _build(arguments)
    if arguments.command == "publish":
        return _publish(arguments)
    if arguments.command == "merge":
        return _merge(arguments)
    raise AssertionError(f"unhandled command: {arguments.command}")


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
        enrich=arguments.enrich,
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
    base_index = None
    new_index = None
    if arguments.base_tu_index or arguments.new_tu_index:
        if not (arguments.base_tu_index and arguments.new_tu_index):
            raise ValidationError(
                "identity matching requires both --base-tu-index and "
                "--new-tu-index"
            )
        from .identity import read_index_files

        entities_base = arguments.base_tu_index.parent / "entities.jsonl"
        entities_new = arguments.new_tu_index.parent / "entities.jsonl"
        base_index = read_index_files(
            component=component.id,
            entities_path=entities_base,
            tu_index_path=arguments.base_tu_index,
        )
        new_index = read_index_files(
            component=component.id,
            entities_path=entities_new,
            tu_index_path=arguments.new_tu_index,
        )
    merge_kwargs: dict[str, Any] = {}
    if base_index is not None and new_index is not None:
        merge_kwargs = {"base_index": base_index, "new_index": new_index}
    report = run_merge(
        manifest,
        loader,
        component,
        new_snapshot_path=arguments.snapshot,
        base_snapshot_path=arguments.base_snapshot,
        **merge_kwargs,
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
