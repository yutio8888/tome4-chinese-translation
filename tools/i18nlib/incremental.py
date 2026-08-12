"""lint --incremental orchestration (contract/0.1-rc3 §8).

Domain 'source': diff base..head of the engine repository, stage only the
affected files at head, recompute findings for affected TUs, and optionally
run the whole-set canonical self-check (G8). I1 widens to the full component
when a changed file fails to parse; I2 keeps GitRepository as the only git
channel.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .config import ComponentSpec, Manifest
from .errors import ExtractionError, ValidationError
from .extract import (
    _clean_log_lines,
    _minimal_mounts,
    _normalized_definitions,
    _patch_extractor,
    KNOWN_PARSE_FAILURES,
    parse_enrichment_records,
)
from .fingerprint import FindingRecord, canonical_findings_form
from .git_source import GitRepository
from .identity import (
    SLOT_REGISTRY_RELATIVE_PATH,
    SlotRegistry,
    build_component_index,
)
from .invalidation import (
    affected_for_source_domain,
    section_to_source_git_path,
)
from .locale_model import LocaleLoader
from .runtime import LuaRuntime
from .snapshot import read_snapshot


def _stage_affected_files(
    repository: GitRepository,
    commit: str,
    component: ComponentSpec,
    affected_source_paths: Iterable[str],
    stage: Path,
) -> int:
    mounts = {source.git_path: source.mount for source in component.sources}
    count = 0
    for path in affected_source_paths:
        normalized = PurePosixPath(path).as_posix()
        matched = False
        for git_path, mount in mounts.items():
            prefix = git_path + "/"
            if normalized.startswith(prefix):
                relative = normalized[len(prefix):]
                target = stage.joinpath(mount, *PurePosixPath(relative).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(repository.read_blob(commit, normalized))
                count += 1
                matched = True
                break
        if not matched:
            raise ExtractionError(
                f"affected path does not belong to {component.id}: {normalized}"
            )
    return count


def _run_staged_extractor(
    *,
    manifest: Manifest,
    runtime: LuaRuntime,
    loader: LocaleLoader,
    component: ComponentSpec,
    stage: Path,
    timeout: int,
) -> None:
    """Run the patched extractor on an already-staged tree (enrich mode).

    Outputs i18n_list.lua + i18n_enrichment.jsonl into the stage directory.
    Raises ExtractionError on parse failure (caller widens per I1).
    """
    extractor_repository = GitRepository(
        manifest.repository_path(manifest.extractor.repository)
    )
    extractor_repository.validate(manifest.extractor.commit, check_worktree=False)
    tool_stage = stage.parent / f"{stage.name}-tool"
    extractor_repository.materialize_lua_tree(
        manifest.extractor.commit,
        manifest.extractor.git_path,
        tool_stage,
        mount="i18n_tools",
    )
    extractor_root = tool_stage / "i18n_tools"
    _patch_extractor(extractor_root, manifest.extractor, enrich=True)
    mounts = _minimal_mounts(component)
    result = runtime.run(
        [extractor_root / "i18n_extractor.lua", *mounts],
        cwd=stage,
        lua_paths=[extractor_root],
        timeout=timeout,
        extra_env={"I18N_ENRICHMENT": "i18n_enrichment.jsonl"},
    )
    combined_log = result.stdout
    if result.stderr:
        combined_log += (
            "\n" if combined_log and not combined_log.endswith("\n") else ""
        ) + result.stderr
    clean_lines = _clean_log_lines(combined_log)
    parse_failures = [
        line for line in clean_lines if line.startswith("In file ")
    ]
    known_failures = [
        line
        for line in clean_lines
        if any(marker in line for marker in KNOWN_PARSE_FAILURES)
    ]
    if result.returncode != 0 or parse_failures or known_failures:
        sample = (parse_failures + known_failures)[:10] or [result.stderr.strip()]
        raise ExtractionError(
            f"staged extraction failed for {component.id}: " + " | ".join(sample)
        )
    output_file = stage / "i18n_list.lua"
    if not output_file.is_file():
        raise ExtractionError(f"no i18n_list.lua produced for {component.id}")
    if not (stage / "i18n_enrichment.jsonl").is_file():
        raise ExtractionError(f"no enrichment sidecar produced for {component.id}")


def _build_partial_index(
    *,
    manifest: Manifest,
    loader: LocaleLoader,
    component: ComponentSpec,
    stage: Path,
) -> Any:
    extracted_document = loader.load_path(
        stage / "i18n_list.lua",
        logical_path=f"generated:incremental/{component.id}/i18n_list.lua",
    )
    definitions = _normalized_definitions(
        component=component.id,
        records=extracted_document.records,
        origin_kind="extracted",
    )
    snapshot_data = b"".join(
        (
            json.dumps(
                definition,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
            + b"\n"
        )
        for definition in definitions
    )
    snapshot_path = stage / "snapshot.jsonl"
    snapshot_path.write_bytes(snapshot_data)
    if not definitions:
        # Affected files with no captured entries: nothing to recompute.
        from .identity import ComponentIndex

        return ComponentIndex(
            component=component.id,
            source_snapshot_sha256="",
            entities={},
            tus={},
            editorial_to_tu={},
            conflicts=(),
            stats={"definitions": 0, "occurrences_bound": 0, "entities": 0,
                   "tus": 0, "strong_tus": 0, "fallback_tus": 0,
                   "unknown_fallback_occurrences": 0, "conflicts": 0},
        )
    snapshot = read_snapshot(snapshot_path, expected_component=component.id)
    sidecar = [
        json.loads(line)
        for line in (stage / "i18n_enrichment.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line
    ]
    return build_component_index(
        component=component.id,
        snapshot=snapshot,
        enrichment_records=parse_enrichment_records(
            sidecar, source_label=f"incremental:{component.id}"
        ),
        slot_registry=SlotRegistry.load(
            manifest.root / SLOT_REGISTRY_RELATIVE_PATH
        ),
    )


def incremental_source_flow(
    *,
    manifest: Manifest,
    runtime: LuaRuntime,
    loader: LocaleLoader,
    components: Iterable[ComponentSpec],
    engine_repository: GitRepository,
    base_commit: str,
    head_commit: str,
    timeout: int = 900,
    self_check: bool = False,
    artifact_directory: Path | None = None,
) -> dict[str, Any]:
    component_list = [
        component
        for component in components
        if component.source_repository is not None and component.sources
    ]
    if not component_list:
        raise ValidationError("source domain requires public source components")
    if any(component.source_baseline is not None for component in component_list):
        raise ValidationError("incremental source domain excludes protected sources")
    engine_repository.validate(base_commit, check_worktree=False)
    engine_repository.validate(head_commit, check_worktree=False)
    changed = engine_repository.changed_paths(base_commit, head_commit)

    affected_by_component: dict[str, frozenset[str]] = {}
    mapped_lua_paths: set[str] = set()
    for component in component_list:
        affected = affected_for_source_domain(component, changed)
        for section in affected.sections:
            source = section_to_source_git_path(component, section)
            if source is not None:
                mapped_lua_paths.add(source)
        affected_by_component[component.id] = affected.sections
    unmapped = {
        path
        for path in changed
        if path.endswith(".lua") and path not in mapped_lua_paths
    }
    if unmapped:
        raise ValidationError(
            "cannot map changed Lua paths to any component: "
            + ", ".join(sorted(unmapped))[:500]
        )

    from .findings import FindingContext, build_finding_records
    from .fingerprint import RuleRegistry
    from .identity import RULES_REGISTRY_RELATIVE_PATH
    from .pipeline import extract_enriched, lint_translation_documents

    registry = RuleRegistry.load(manifest.root / RULES_REGISTRY_RELATIVE_PATH)
    issues, contexts, metrics = lint_translation_documents(
        manifest, loader, component_list
    )

    def records_for_indexes(indexes: dict[str, Any]) -> list[FindingRecord]:
        bound_contexts = {
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
            contexts=bound_contexts,
            conflicts=conflicts,
        )
        return records

    # F_previous: full extraction at base.
    base_indexes, _ = extract_enriched(
        manifest,
        runtime,
        component_list,
        timeout=timeout,
        commit_overrides={
            component.source_repository: base_commit
            for component in component_list
            if component.source_repository
        },
    )
    base_records = records_for_indexes(base_indexes)

    # Affected TU set from the base indexes.
    affected_tus: set[str] = set()
    for component in component_list:
        sections = affected_by_component[component.id]
        index = base_indexes[component.id]
        for tu in index.tus.values():
            if set(tu.sections) & sections:
                affected_tus.add(tu.tu_uid)

    # Partial recompute at head (I1 widens on parse failure).
    head_partial: dict[str, Any] = {}
    widened: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="tome4-i18n-incremental-") as temporary:
        temporary_root = Path(temporary)
        for component in component_list:
            sections = affected_by_component[component.id]
            source_paths = sorted(
                {
                    source
                    for section in sections
                    for source in [section_to_source_git_path(component, section)]
                    if source is not None
                }
            )
            if not source_paths:
                # No Lua files affected: reuse the base index unchanged.
                head_partial[component.id] = base_indexes[component.id]
                continue
            stage = temporary_root / f"component-{component.id}"
            stage.mkdir(parents=True)
            _stage_affected_files(
                engine_repository, head_commit, component, source_paths, stage
            )
            try:
                _run_staged_extractor(
                    manifest=manifest,
                    runtime=runtime,
                    loader=loader,
                    component=component,
                    stage=stage,
                    timeout=timeout,
                )
                head_partial[component.id] = _build_partial_index(
                    manifest=manifest,
                    loader=loader,
                    component=component,
                    stage=stage,
                )
            except ExtractionError as error:
                # I1: unparseable diff -> the whole component is affected.
                widened[component.id] = str(error)
                head_partial[component.id] = None

    full_head_indexes: dict[str, Any] = {}
    for component in component_list:
        if head_partial.get(component.id) is None:
            # Widened component: full head extraction replaces the partial.
            widened_override = {
                component.source_repository: head_commit
                for component in component_list
                if component.source_repository
            }
            full_head_indexes, _ = extract_enriched(
                manifest,
                runtime,
                component_list,
                timeout=timeout,
                commit_overrides=widened_override,
            )
            break
    for component in component_list:
        if head_partial.get(component.id) is None:
            head_partial[component.id] = full_head_indexes[component.id]
            for tu in head_partial[component.id].tus.values():
                affected_tus.add(tu.tu_uid)

    head_records = records_for_indexes(head_partial)
    recomputed = tuple(
        record for record in head_records if record.tu_uid in affected_tus
    )
    kept = tuple(
        record for record in base_records if record.tu_uid not in affected_tus
    )
    incremental_records = tuple(
        sorted([*kept, *recomputed], key=lambda record: record.fingerprint)
    )

    result: dict[str, Any] = {
        "domain": "source",
        "base_commit": base_commit,
        "head_commit": head_commit,
        "changed_paths": len(changed),
        "affected_sections": {
            component.id: sorted(affected_by_component[component.id])
            for component in component_list
        },
        "affected_tus": len(affected_tus),
        "widened_components": widened,
        "findings": {
            "previous": len(base_records),
            "kept": len(kept),
            "recomputed": len(recomputed),
            "incremental": len(incremental_records),
        },
        "self_check": None,
        "records": [record.to_dict() for record in incremental_records],
    }
    if self_check:
        if not full_head_indexes:
            full_head_indexes, _ = extract_enriched(
                manifest,
                runtime,
                component_list,
                timeout=timeout,
                commit_overrides={
                    component.source_repository: head_commit
                    for component in component_list
                    if component.source_repository
                },
            )
        full_records = records_for_indexes(full_head_indexes)
        from .invalidation import self_check as canonical_self_check

        passed = canonical_self_check(
            incremental=incremental_records,
            full=full_records,
            artifact_directory=artifact_directory,
        )
        result["self_check"] = {
            "passed": passed,
            "full_findings": len(full_records),
            "artifacts": str(artifact_directory) if artifact_directory else None,
        }
    return result
