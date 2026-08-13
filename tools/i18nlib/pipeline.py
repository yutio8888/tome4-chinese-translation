"""Shared enriched-lint pipeline for baseline / incremental commands.

Order (contract §7, §8): pinned extraction with the enrichment sidecar,
TU index build, translation lint, FindingRecord assembly with identity
bindings. Default command paths are untouched (extract/lint byte-stability).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Iterable

from .baseline import Baseline, read_baseline, validate_baseline_environment
from .config import ComponentSpec, Manifest
from .errors import ValidationError
from .extract import extract_components
from .fingerprint import RuleRegistry
from .findings import FindingContext, build_finding_records
from .identity import (
    RULES_REGISTRY_RELATIVE_PATH,
    SLOT_REGISTRY_RELATIVE_PATH,
    UNLOADED_SOURCES_RELATIVE_PATH,
    ComponentIndex,
    UnloadedSources,
    read_index_files,
)
from .lint import Issue, lint_documents, load_policy
from .locale_model import LocaleLoader
from .runtime import LuaRuntime


def _registry_sha256(manifest_root: Path, relative: str) -> str:
    path = manifest_root / relative
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        raise ValidationError(f"cannot hash registry {path}: {error}") from error


def extract_enriched(
    manifest: Manifest,
    runtime: LuaRuntime,
    components: Iterable[ComponentSpec],
    *,
    timeout: int = 900,
    commit_overrides: dict[str, str] | None = None,
) -> tuple[dict[str, ComponentIndex], dict[str, Any]]:
    extractable = [
        component
        for component in components
        if (
            component.source_repository is not None and component.sources
        )
        or component.protected_source is not None
    ]
    report: dict[str, Any] = {}
    if extractable:
        report = extract_components(
            manifest,
            runtime,
            extractable,
            timeout=timeout,
            enrich=True,
            commit_overrides=commit_overrides,
        )
    indexes: dict[str, ComponentIndex] = {}
    current_root = manifest.root / ".artifacts" / "i18n" / "identity" / "current"
    for component in extractable:
        entities_path = current_root / component.id / "entities.jsonl"
        tu_index_path = current_root / component.id / "tu_index.jsonl"
        if not entities_path.is_file() or not tu_index_path.is_file():
            raise ValidationError(
                f"identity index missing for {component.id}; "
                "run extract --enrich first"
            )
        indexes[component.id] = read_index_files(
            component=component.id,
            entities_path=entities_path,
            tu_index_path=tu_index_path,
            conflicts_path=current_root / component.id / "identity.json",
        )
    return indexes, report


def load_translation_documents(
    manifest: Manifest,
    loader: LocaleLoader,
    components: Iterable[ComponentSpec],
) -> list[tuple[str, Any, bool]]:
    """Load (component_id, LocaleDocument, is_copy_fragment) specs."""
    specs: list[tuple[str, Any, bool]] = []
    for component in components:
        document = loader.load_path(
            manifest.root / component.translation,
            logical_path=component.translation,
        )
        specs.append((component.id, document, False))
        if component.copy_fragment:
            copy_document = loader.load_path(
                manifest.root / component.copy_fragment,
                logical_path=component.copy_fragment,
            )
            specs.append((component.id, copy_document, True))
    return specs


def lint_documents_specs(
    manifest: Manifest,
    documents_specs: Iterable[tuple[str, Any, bool]],
    *,
    policy: Any | None = None,
) -> tuple[list[Issue], dict[str, FindingContext], dict[str, Any]]:
    """Lint (component_id, LocaleDocument, is_copy_fragment) specs."""
    if policy is None:
        policy = load_policy(manifest)
    documents: list[tuple[str, Any]] = []
    contexts: dict[str, FindingContext] = {}
    for component_id, document, is_copy_fragment in documents_specs:
        documents.append((component_id, document))
        suffix = ":copy-fragment" if is_copy_fragment else ""
        contexts[component_id + suffix] = FindingContext(
            component=component_id,
            entries=tuple(document.translations),
            index=None,
        )
    issues, metrics = lint_documents(
        documents, policy, require_nonempty=True
    )
    return issues, contexts, metrics


def lint_translation_documents(
    manifest: Manifest,
    loader: LocaleLoader,
    components: Iterable[ComponentSpec],
) -> tuple[list[Issue], dict[str, FindingContext], dict[str, Any]]:
    specs = load_translation_documents(manifest, loader, components)
    return lint_documents_specs(manifest, specs)


def run_enriched_lint(
    manifest: Manifest,
    runtime: LuaRuntime,
    loader: LocaleLoader,
    components: Iterable[ComponentSpec],
    *,
    timeout: int = 900,
) -> dict[str, Any]:
    """Full pipeline: extract --enrich, lint, assemble FindingRecords."""
    component_list = list(components)
    indexes, extract_report = extract_enriched(
        manifest, runtime, component_list, timeout=timeout
    )
    issues, contexts, metrics = lint_translation_documents(
        manifest, loader, component_list
    )
    for name, context in contexts.items():
        contexts[name] = FindingContext(
            component=context.component,
            entries=context.entries,
            index=indexes.get(context.component),
        )
    registry = RuleRegistry.load(manifest.root / RULES_REGISTRY_RELATIVE_PATH)
    unloaded_sources = UnloadedSources.load(
        manifest.root / UNLOADED_SOURCES_RELATIVE_PATH
    )
    conflicts: list[Any] = []
    for index in indexes.values():
        conflicts.extend(index.conflicts)
    records, binding_report = build_finding_records(
        registry=registry,
        issues=issues,
        contexts=contexts,
        conflicts=conflicts,
        unloaded_sources=unloaded_sources,
    )
    from .storage import store_findings

    store_findings(manifest.root, records)
    return {
        "records": records,
        "issues": issues,
        "metrics": metrics,
        "indexes": indexes,
        "extract": extract_report,
        "binding": binding_report,
        "registries": {
            "rules_registry_sha256": _registry_sha256(
                manifest.root, RULES_REGISTRY_RELATIVE_PATH
            ),
            "slot_registry_sha256": _registry_sha256(
                manifest.root, SLOT_REGISTRY_RELATIVE_PATH
            ),
        },
    }


def baseline_for(
    manifest: Manifest,
    *,
    component: str,
    translation_commit: str,
) -> Baseline:
    return read_baseline(
        manifest.root,
        component=component,
        translation_commit=translation_commit,
    )


def validate_baselines(
    manifest: Manifest,
    *,
    baselines: dict[str, Baseline],
    extract_report: dict[str, Any],
    registries: dict[str, str],
) -> None:
    for component_id, baseline in baselines.items():
        component = manifest.component(component_id)
        snapshot_sha = next(
            (
                item["snapshot_sha256"]
                for item in extract_report.get("components", [])
                if item["component"] == component_id
            ),
            None,
        )
        if snapshot_sha is None:
            raise ValidationError(
                f"baseline {component_id} has no reproducible source snapshot "
                "in this run"
            )
        engine_commit = manifest.repositories[
            component.source_repository
        ].commit if component.source_repository else ""
        validate_baseline_environment(
            baseline,
            source_snapshot_sha256=snapshot_sha,
            engine_commit=engine_commit,
            extractor_commit=manifest.extractor.commit,
            rules_registry_sha256=registries["rules_registry_sha256"],
            slot_registry_sha256=registries["slot_registry_sha256"],
        )
