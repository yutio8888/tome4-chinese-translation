"""Semantic drift reports against the pinned official locales."""

from __future__ import annotations

from typing import Any, Iterable

from .config import ComponentSpec, Manifest
from .git_source import GitRepository
from .locale_model import LocaleLoader, runtime_map
from .semantics import runtime_semantic_signature


def _semantic_value(entry: dict[str, Any]) -> str:
    return runtime_semantic_signature(entry)


def component_status(
    manifest: Manifest,
    loader: LocaleLoader,
    component: ComponentSpec,
) -> dict[str, Any]:
    canonical = loader.load_path(
        manifest.root / component.translation,
        logical_path=component.translation,
    )
    result: dict[str, Any] = {
        "component": component.id,
        "translation": component.translation,
        "canonical_entries": len(canonical.translations),
        "official_available": False,
    }
    if component.source_repository is None or component.official_locale is None:
        return result

    repository_spec = manifest.repositories[component.source_repository]
    repository = GitRepository(manifest.repository_path(component.source_repository))
    official_bytes = repository.read_blob(
        repository_spec.commit, component.official_locale
    )
    official = loader.load_bytes(
        official_bytes,
        logical_path=f"{repository_spec.commit}:{component.official_locale}",
    )
    canonical_map = runtime_map([canonical])
    official_map = runtime_map([official])
    canonical_keys = set(canonical_map)
    official_keys = set(official_map)
    shared = canonical_keys & official_keys
    identical = sum(
        _semantic_value(canonical_map[key]) == _semantic_value(official_map[key])
        for key in shared
    )
    result.update(
        {
            "official_available": True,
            "official_entries": len(official.translations),
            "runtime_canonical_keys": len(canonical_map),
            "runtime_official_keys": len(official_map),
            "identical": identical,
            "changed": len(shared) - identical,
            "canonical_only": len(canonical_keys - official_keys),
            "official_only": len(official_keys - canonical_keys),
        }
    )
    return result


def status_report(
    manifest: Manifest,
    loader: LocaleLoader,
    components: Iterable[ComponentSpec],
) -> dict[str, Any]:
    reports = [component_status(manifest, loader, component) for component in components]
    return {
        "version": manifest.version,
        "components": reports,
        "totals": {
            "canonical_entries": sum(item["canonical_entries"] for item in reports),
            "changed": sum(item.get("changed", 0) for item in reports),
            "canonical_only": sum(item.get("canonical_only", 0) for item in reports),
            "official_only": sum(item.get("official_only", 0) for item in reports),
        },
    }
