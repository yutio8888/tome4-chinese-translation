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
) -> tuple[int, list[str]]:
    """Stage affected files at ``commit``; returns (staged_count, deleted_paths).

    Files that no longer exist at ``commit`` (deleted in base..head) are
    skipped and reported instead of crashing on the missing blob (H2). A
    stage that ends up empty (only deletions) is a legitimate "nothing to
    recompute at head" state, not an error.
    """
    mounts = {source.git_path: source.mount for source in component.sources}
    count = 0
    deleted: list[str] = []
    for path in affected_source_paths:
        normalized = PurePosixPath(path).as_posix()
        matched = False
        for git_path, mount in mounts.items():
            prefix = git_path + "/"
            if normalized.startswith(prefix):
                relative = normalized[len(prefix):]
                target = stage.joinpath(mount, *PurePosixPath(relative).parts)
                blob = repository.read_blob_optional(commit, normalized)
                if blob is None:
                    # Genuinely absent at head: the file was deleted in the
                    # range. Other failures (git rc, ambiguous, non-regular,
                    # cat-file) propagate as ExtractionError - only a missing
                    # blob counts as a deletion (fail closed).
                    deleted.append(normalized)
                    matched = True
                    break
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(blob)
                count += 1
                matched = True
                break
        if not matched:
            raise ExtractionError(
                f"affected path does not belong to {component.id}: {normalized}"
            )
    return count, deleted


def _empty_index(component_id: str) -> Any:
    """A head index with no definitions (deleted-only stage / empty diff)."""
    from .identity import ComponentIndex

    return ComponentIndex(
        component=component_id,
        source_snapshot_sha256="",
        entities={},
        tus={},
        editorial_to_tu={},
        conflicts=(),
        stats={"definitions": 0, "occurrences_bound": 0, "entities": 0,
               "tus": 0, "strong_tus": 0, "fallback_tus": 0,
               "unknown_fallback_occurrences": 0, "conflicts": 0},
    )


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
        return _empty_index(component.id)
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
    from .identity import (
        RULES_REGISTRY_RELATIVE_PATH,
        UNLOADED_SOURCES_RELATIVE_PATH,
        UnloadedSources,
    )
    from .pipeline import extract_enriched, lint_translation_documents

    registry = RuleRegistry.load(manifest.root / RULES_REGISTRY_RELATIVE_PATH)
    unloaded_sources = UnloadedSources.load(
        manifest.root / UNLOADED_SOURCES_RELATIVE_PATH
    )
    issues, contexts, metrics = lint_translation_documents(
        manifest, loader, component_list
    )

    def records_for_indexes(
        indexes: dict[str, Any], *, conflicts_indexes: dict[str, Any] | None = None
    ) -> tuple[list[FindingRecord], dict[str, Any]]:
        """Bind issues against ``indexes`` but take conflicts from
        ``conflicts_indexes`` (default: the same indexes). The conflict input
        must be equivalent to the full head (§8.4 / D4); the partial staged
        index cannot see duplicates across unchanged files."""
        bound_contexts = {
            name: FindingContext(
                component=context.component,
                entries=context.entries,
                index=indexes.get(context.component),
            )
            for name, context in contexts.items()
        }
        conflicts: list[Any] = []
        source = conflicts_indexes if conflicts_indexes is not None else indexes
        for index in source.values():
            conflicts.extend(index.conflicts)
        return build_finding_records(
            registry=registry,
            issues=issues,
            contexts=bound_contexts,
            conflicts=conflicts,
            unloaded_sources=unloaded_sources,
        )

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
    base_records, base_binding = records_for_indexes(base_indexes)

    # Affected TU set from the base indexes (includes TUs of deleted sections).
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
    deleted_files: list[str] = []
    staged_components: set[str] = set()
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
            staged_count, deleted = _stage_affected_files(
                engine_repository, head_commit, component, source_paths, stage
            )
            deleted_files.extend(deleted)
            if staged_count == 0:
                # Only deletions: nothing exists at head to re-extract.
                head_partial[component.id] = _empty_index(component.id)
                continue
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
                staged_components.add(component.id)
            except ExtractionError as error:
                # I1: unparseable diff -> the whole component is affected.
                widened[component.id] = str(error)
                head_partial[component.id] = None

    # H2: head-side affected TUs (new entities / new UIDs / same-file
    # renames) collected from the staged partial index.
    for component in component_list:
        index = head_partial.get(component.id)
        if index is not None and component.id in staged_components:
            affected_tus.update(index.tus)

    full_head_indexes: dict[str, Any] = {}
    for component in component_list:
        if head_partial.get(component.id) is None:
            # Widened component: full head extraction replaces the partial.
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
            break
    for component in component_list:
        if head_partial.get(component.id) is None:
            head_partial[component.id] = full_head_indexes[component.id]
            for tu in head_partial[component.id].tus.values():
                affected_tus.add(tu.tu_uid)

    # D4: conflict input equivalent to the full head. The partial staged
    # extraction cannot see a duplicate anchor formed between a changed file
    # and an unchanged file; only the full head identity index carries the
    # complete definition-site evidence. With self-check enabled the
    # self-check full extraction is reused (and also becomes the binding
    # index so incremental == full byte-wise); without self-check each
    # affected component is fully extracted at head and that full index is
    # used for binding/recompute as well (V8) - the partial index would
    # produce participants/fingerprints that differ from the full head.
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
        conflict_indexes = full_head_indexes
        # Bind and recompute against the full head so participants and
        # conflicts are consistent (cross-file duplicates included).
        head_indexes = full_head_indexes
        for component in component_list:
            sections = affected_by_component[component.id]
            index = full_head_indexes[component.id]
            affected_tus.update(
                tu.tu_uid
                for tu in index.tus.values()
                if set(tu.sections) & sections
            )
    else:
        conflict_indexes: dict[str, Any] = {}
        affected_components = [
            component
            for component in component_list
            if affected_by_component[component.id]
        ]
        for component in affected_components:
            if component.id in full_head_indexes:
                conflict_indexes[component.id] = full_head_indexes[component.id]
        missing = [
            component
            for component in affected_components
            if component.id not in conflict_indexes
        ]
        if missing:
            extracted, _ = extract_enriched(
                manifest,
                runtime,
                missing,
                timeout=timeout,
                commit_overrides={
                    component.source_repository: head_commit
                    for component in missing
                    if component.source_repository
                },
            )
            conflict_indexes.update(extracted)
        for component in component_list:
            conflict_indexes.setdefault(
                component.id, base_indexes[component.id]
            )
        # V8: affected components bind and recompute against their full head
        # index (participants include the unchanged file's TUs); unaffected
        # components reuse the base index (head == base there).
        head_indexes = conflict_indexes
        for component in affected_components:
            sections = affected_by_component[component.id]
            index = conflict_indexes[component.id]
            affected_tus.update(
                tu.tu_uid
                for tu in index.tus.values()
                if set(tu.sections) & sections
            )

    head_records, head_binding = records_for_indexes(
        head_indexes, conflicts_indexes=conflict_indexes
    )
    # H2/V8: recompute/kept are record-identity level, not merely TU-level.
    # The base and head record sets share the same lint Issues; a rename /
    # new-UID / deleted source changes where an Issue binds (base TU -> head
    # TU or fallback), so a record must be recomputed when its Issue was
    # attached to an affected TU on either side. Conflict-driven records
    # (duplicate-id) carry a regenerated Issue per binding, so they are
    # matched through their stable evidence key instead; a record whose
    # participants contain an affected TU is touched on both sides.
    def _record_touched(record: FindingRecord) -> bool:
        return record.tu_uid in affected_tus or any(
            participant in affected_tus for participant in record.participants
        )

    affected_issues = frozenset(
        record.issue.entry_id
        for record in [*base_records, *head_records]
        if record.issue.entry_id is not None and _record_touched(record)
    )
    affected_evidence = frozenset(
        record.evidence_key
        for record in [*base_records, *head_records]
        if _record_touched(record)
    )

    def _record_affected(record: FindingRecord) -> bool:
        return (
            _record_touched(record)
            or record.issue.entry_id in affected_issues
            or record.evidence_key in affected_evidence
        )

    recomputed = tuple(record for record in head_records if _record_affected(record))
    kept = tuple(record for record in base_records if not _record_affected(record))
    incremental_records = tuple(
        sorted([*kept, *recomputed], key=lambda record: record.fingerprint)
    )

    # H3: CI new-error semantics. Only recomputed errors whose fingerprint is
    # not in the base error fingerprints are NEW; legacy errors stay
    # technical debt and never fail the gate.
    base_error_fingerprints = frozenset(
        record.fingerprint
        for record in base_records
        if record.issue.severity == "error"
    )
    new_errors = tuple(
        record
        for record in recomputed
        if record.issue.severity == "error"
        and record.fingerprint not in base_error_fingerprints
    )
    legacy_errors = tuple(
        record
        for record in incremental_records
        if record.issue.severity == "error"
        and record.fingerprint in base_error_fingerprints
    )

    result: dict[str, Any] = {
        "domain": "source",
        "base_commit": base_commit,
        "head_commit": head_commit,
        "changed_paths": len(changed),
        "deleted_files": sorted(deleted_files),
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
        "ci": {
            "new_errors": len(new_errors),
            "legacy_errors": len(legacy_errors),
            "new_error_fingerprints": [
                record.fingerprint for record in new_errors
            ],
        },
        "binding": {
            "suppressed_conflicts": head_binding.get(
                "suppressed_conflicts", []
            ),
        },
        "self_check": None,
        "records": [record.to_dict() for record in incremental_records],
    }
    if self_check:
        full_records, _ = records_for_indexes(full_head_indexes)
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
