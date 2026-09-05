"""Registration and handlers for doctor commands."""

from __future__ import annotations
import argparse
from typing import Any
from . import TOOL_VERSION
from .errors import ValidationError
from .extract import probe_protected_component
from .git_source import GitRepository
from .runtime import LuaRuntime
from .cli_common import _add_common_arguments, _manifest, _print_json


def register(subparsers: argparse._SubParsersAction) -> None:
    doctor = subparsers.add_parser("doctor", help="validate the pinned toolchain")
    _add_common_arguments(doctor)
    doctor.set_defaults(handler=dispatch)


def dispatch(arguments: argparse.Namespace) -> int:
    if arguments.command == "doctor":
        return _doctor(arguments)
    raise AssertionError(f"unhandled command: {arguments.command}")


def _attributes(spec: Any) -> dict[str, Any]:
    return {"visibility": spec.visibility, "extraction_mode": spec.extraction_mode,
            "source_pinning": spec.source_pinning, "scan_allowlist": list(spec.scan_allowlist)}


def _attribute_text(report: dict[str, Any]) -> str:
    return (f"visibility={report['visibility']} extraction_mode={report['extraction_mode']} "
            f"source_pinning={report['source_pinning']} scan_allowlist={report['scan_allowlist']!r}")


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
    terminology_path = manifest.root / manifest.terminology
    terminology_ok = terminology_path.is_dir() or terminology_path.is_file()
    if not terminology_ok:
        if terminology_path.exists():
            not_regular.append(str(terminology_path))
        else:
            missing.append(str(terminology_path))
    for path in required_files[1:]:
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
            repositories[name] = {"path": str(path), "available": False, **_attributes(spec)}
            continue
        repository = GitRepository(path)
        report = repository.validate(
            spec.commit, scan_allowlist=spec.scan_allowlist
        )
        report.update(_attributes(spec))
        report["available"] = True
        if report["clean"] is False:
            warnings.append(f"repository has worktree changes: {name}: {path}")
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
            **_attributes(component.protected_source),
        }
        warnings.append(
            f"source-unpinned: {component.id}: source repository/commit unknown; "
            "extraction snapshot is not a source pin"
        )
        if not available:
            warnings.append(
                f"declared source is unavailable: {component.id}"
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
            print(f"{availability:<5}repository      {name}: {detail}; {_attribute_text(repository)}")
        for component, protected in protected_sources.items():
            availability = "OK" if protected["available"] else "SKIP"
            print(
                f"{availability:<5}source          {component}: "
                f"{_attribute_text(protected)}"
            )
        for warning in warnings:
            print(f"WARN              {warning}")
    return 0
