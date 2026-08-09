"""Pinned-source extraction using the historical ToME4 Lua parser."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .config import ComponentSpec, ExtractorSpec, Manifest
from .errors import ExtractionError, ValidationError
from .git_source import GitRepository
from .locale_model import LocaleLoader
from .report import atomic_write_bytes, create_run_directory, write_json
from .runtime import LuaRuntime


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
KNOWN_PARSE_FAILURES = (
    "too many pending calls/choices",
    "empty loop in rule 'functioncall'",
)


def _patch_extractor(extractor_root: Path, spec: ExtractorSpec) -> dict[str, Any]:
    parser_path = extractor_root / "luafish" / "parser.lua"
    extractor_path = extractor_root / "i18n_extractor.lua"
    try:
        parser = parser_path.read_text(encoding="utf-8")
        extractor = extractor_path.read_text(encoding="utf-8")
    except OSError as error:
        raise ExtractionError(f"cannot read staged extractor: {error}") from error

    require_line = "local lpeg = require 'lpeg'\n"
    if parser.count(require_line) != 1:
        raise ExtractionError("cannot locate unique LPeg import in staged parser")
    parser = parser.replace(
        require_line,
        require_line + f"lpeg.setmaxstack({spec.max_stack})\n",
        1,
    )
    parser_path.write_text(parser, encoding="utf-8", newline="\n")

    duplicate_patch_applied = False
    if spec.preserve_duplicate_occurrences:
        locale_declaration = "local locales = {}\n"
        if extractor.count(locale_declaration) != 1:
            raise ExtractionError("cannot locate locale table in staged extractor")
        bucket_helper = """local locales = {}
local function new_locale_bucket()
\treturn setmetatable({}, {
\t\t__newindex = function(bucket, key, value)
\t\t\tif type(key) == \"string\" and type(value) == \"table\" then
\t\t\t\tvalue.__i18n_source = key
\t\t\t\trawset(bucket, #bucket + 1, value)
\t\t\telse
\t\t\t\trawset(bucket, key, value)
\t\t\tend
\t\tend,
\t})
end
"""
        extractor = extractor.replace(locale_declaration, bucket_helper, 1)
        old_initializer = "locales[file] = locales[file] or {}"
        initializer_count = extractor.count(old_initializer)
        if initializer_count < 1:
            raise ExtractionError("cannot locate locale buckets in staged extractor")
        extractor = extractor.replace(
            old_initializer, "locales[file] = locales[file] or new_locale_bucket()"
        )
        old_output = """\tlocal list = {}
\tfor k, v in pairs(locales[section]) do
\t\tif type(k) == \"string\" then
\t\t\tlist[#list+1] = {text=k, line=v.line, type=v.type}
\t\tend
\tend
"""
        new_output = """\tlocal list = {}
\tfor _, v in ipairs(locales[section]) do
\t\tif type(v) == \"table\" and type(v.__i18n_source) == \"string\" then
\t\t\tlist[#list+1] = {text=v.__i18n_source, line=v.line, type=v.type}
\t\tend
\tend
"""
        if extractor.count(old_output) != 1:
            raise ExtractionError("cannot locate extractor output loop")
        extractor = extractor.replace(old_output, new_output, 1)
        extractor_path.write_text(extractor, encoding="utf-8", newline="\n")
        duplicate_patch_applied = True

    return {
        "max_stack": spec.max_stack,
        "duplicate_occurrences_preserved": duplicate_patch_applied,
        "parser_sha256": hashlib.sha256(parser_path.read_bytes()).hexdigest(),
        "extractor_sha256": hashlib.sha256(extractor_path.read_bytes()).hexdigest(),
    }


def _minimal_mounts(component: ComponentSpec) -> list[str]:
    mounts = sorted(
        {PurePosixPath(source.mount) for source in component.sources},
        key=lambda value: (len(value.parts), value.as_posix()),
    )
    selected: list[PurePosixPath] = []
    for mount in mounts:
        if any(parent == mount or parent in mount.parents for parent in selected):
            continue
        selected.append(mount)
    return [mount.as_posix() for mount in selected]


def _clean_log_lines(log: str) -> list[str]:
    return [ANSI_RE.sub("", line).rstrip() for line in log.splitlines()]


def _protected_source_candidates(
    manifest: Manifest, component: ComponentSpec
) -> list[Path]:
    protected = component.protected_source
    if protected is None:
        raise ExtractionError(f"component {component.id!r} is not protected")
    configured = os.environ.get(protected.path_env)
    if configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_absolute():
            raise ExtractionError(f"{protected.path_env} must be an absolute path")
        return [Path(os.path.normpath(str(candidate)))]
    root = manifest.protected_root_path(protected.root)
    return [root / candidate for candidate in protected.directory_candidates]


def _run_protected_extractor(
    manifest: Manifest,
    runtime: LuaRuntime,
    component: ComponentSpec,
    *,
    extractor_root: Path,
    stage: Path,
    timeout: int,
) -> tuple[Path, list[str]]:
    protected = component.protected_source
    if protected is None:
        raise ExtractionError(f"component {component.id!r} is not protected")
    broker = manifest.root / "tools" / "lua" / "protected_extract.lua"
    output_file = stage / "protected_i18n_list.lua"
    result = runtime.run_protected(
        [
            broker,
            "extract",
            extractor_root / "i18n_extractor.lua",
            output_file,
            protected.mount,
            *_protected_source_candidates(manifest, component),
        ],
        cwd=stage,
        lua_paths=[extractor_root],
        timeout=timeout,
    )
    failures = {
        10: "declared protected source is unavailable",
        11: "protected extractor contract is invalid",
        20: "protected Lua extraction failed",
        21: "protected Lua parser reported a source parse failure",
        22: "protected extractor produced no valid text artifact",
        23: "protected extractor could not redact its source path",
    }
    if result.returncode != 0:
        reason = failures.get(result.returncode, "protected Lua extraction failed")
        raise ExtractionError(f"{component.id}: {reason}")
    if not output_file.is_file():
        raise ExtractionError(
            f"{component.id}: protected extractor produced no text artifact"
        )
    return output_file, [protected.mount]


def probe_protected_component(
    manifest: Manifest, runtime: LuaRuntime, component: ComponentSpec
) -> bool:
    if component.protected_source is None:
        raise ExtractionError(f"component {component.id!r} is not protected")
    broker = manifest.root / "tools" / "lua" / "protected_extract.lua"
    with tempfile.TemporaryDirectory(prefix="tome4-i18n-protected-probe-") as temporary:
        result = runtime.run_protected(
            [
                broker,
                "probe",
                *_protected_source_candidates(manifest, component),
            ],
            cwd=Path(temporary),
            timeout=30,
        )
    if result.returncode == 0:
        return True
    if result.returncode == 10:
        return False
    raise ExtractionError(
        f"{component.id}: protected source probe failed closed"
    )


def _normalized_definitions(
    *,
    component: str,
    records: Iterable[Any],
    origin_kind: str,
) -> list[dict[str, Any]]:
    if not isinstance(component, str) or not component:
        raise ExtractionError(
            "extraction field 'component' must be a non-empty string"
        )
    if (
        not isinstance(origin_kind, str)
        or origin_kind not in ("extracted", "manual")
    ):
        raise ExtractionError(
            "extraction field 'origin_kind' must be 'extracted' or 'manual'"
        )

    normalized: list[dict[str, Any]] = []
    for position, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ExtractionError(
                f"extraction record {position} must be an object"
            )
        if record.get("kind") != "definition":
            continue

        section = record.get("section")
        if not isinstance(section, str) or not section:
            raise ExtractionError(
                f"extraction record {position} field 'section' must be a "
                "non-empty string"
            )
        source = record.get("source")
        if not isinstance(source, str):
            raise ExtractionError(
                f"extraction record {position} field 'source' must be a "
                "string"
            )
        if not source and origin_kind == "manual":
            raise ExtractionError(
                f"extraction record {position} field 'source' must be a "
                "non-empty string for manual definitions"
            )
        # The historical extractor emits real records for _t"" and similar
        # placeholders. Keep them in raw snapshots so frozen hashes remain stable.
        source_tag = record.get("source_tag")
        if source_tag is not None and not isinstance(source_tag, str):
            raise ExtractionError(
                f"extraction record {position} field 'source_tag' must be a "
                "string or null"
            )
        source_line = record.get("source_line")
        if type(source_line) is not int:
            raise ExtractionError(
                f"extraction record {position} field 'source_line' must be an "
                "exact integer"
            )
        if source_line < 1:
            if origin_kind == "manual" and source_line == 0:
                origin_line = None
            else:
                sentinel_note = (
                    "manual definitions may use only 0 as the "
                    "unknown-line sentinel"
                    if origin_kind == "manual"
                    else "only manual definitions may use 0 as the "
                    "unknown-line sentinel"
                )
                raise ExtractionError(
                    f"extraction record {position} field 'source_line' must be "
                    f"greater than or equal to 1; {sentinel_note}"
                )
        else:
            origin_line = source_line
        logical_path = record.get("logical_path")
        if logical_path is not None and not isinstance(logical_path, str):
            raise ExtractionError(
                f"extraction record {position} field 'logical_path' must be a "
                "string or null"
            )

        normalized.append(
            {
                "component": component,
                "section": section,
                "source": source,
                "source_tag": source_tag,
                "origin_line": origin_line,
                "origin_kind": origin_kind,
                "origin_document": logical_path,
            }
        )
    return normalized


def extract_components(
    manifest: Manifest,
    runtime: LuaRuntime,
    components: Iterable[ComponentSpec],
    *,
    timeout: int,
) -> dict[str, Any]:
    if type(timeout) is not int or timeout < 1:
        raise ExtractionError("timeout must be a positive integer")

    selected: list[ComponentSpec] = []
    seen_ids: set[str] = set()
    for component in components:
        if component.id in seen_ids:
            continue
        seen_ids.add(component.id)
        selected.append(component)
    if not selected:
        raise ExtractionError("no extractable components selected")
    for component in selected:
        has_public_source = (
            component.source_repository is not None and bool(component.sources)
        )
        if not has_public_source and component.protected_source is None:
            raise ExtractionError(
                f"component {component.id!r} has no pinned source mapping"
            )

    extractor_repo_path = manifest.repository_path(manifest.extractor.repository)
    extractor_repository = GitRepository(extractor_repo_path)
    extractor_repository.validate(manifest.extractor.commit, check_worktree=False)
    loader = LocaleLoader(runtime)
    run_directory = create_run_directory(manifest.root, "extract")
    component_reports: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="tome4-i18n-extract-") as temporary:
        temporary_root = Path(temporary)
        tool_stage = temporary_root / "tool"
        extractor_repository.materialize_lua_tree(
            manifest.extractor.commit,
            manifest.extractor.git_path,
            tool_stage,
            mount="i18n_tools",
        )
        extractor_root = tool_stage / "i18n_tools"
        patch_report = _patch_extractor(extractor_root, manifest.extractor)

        for component in selected:
            stage = temporary_root / f"component-{component.id}"
            stage.mkdir(parents=True)
            protected_access = component.protected_source is not None
            combined_log: str | None = None
            repository_name: str | None = None
            source_commit: str | None = None
            source_file_count: int | None = None
            if protected_access:
                output_file, mounts = _run_protected_extractor(
                    manifest,
                    runtime,
                    component,
                    extractor_root=extractor_root,
                    stage=stage,
                    timeout=timeout,
                )
            else:
                repository_name = component.source_repository
                assert repository_name is not None
                repository_spec = manifest.repositories[repository_name]
                source_commit = repository_spec.commit
                repository = GitRepository(manifest.repository_path(repository_name))
                repository.validate(repository_spec.commit, check_worktree=False)
                source_file_count = 0
                for source in component.sources:
                    source_file_count += repository.materialize_lua_tree(
                        repository_spec.commit,
                        source.git_path,
                        stage,
                        mount=source.mount,
                    )
                mounts = _minimal_mounts(component)
                extractor_result = runtime.run(
                    [extractor_root / "i18n_extractor.lua", *mounts],
                    cwd=stage,
                    lua_paths=[extractor_root],
                    timeout=timeout,
                )
                combined_log = extractor_result.stdout
                if extractor_result.stderr:
                    combined_log += (
                        "\n"
                        if combined_log and not combined_log.endswith("\n")
                        else ""
                    ) + extractor_result.stderr
                clean_lines = _clean_log_lines(combined_log)
                parse_failures = [
                    line for line in clean_lines if line.startswith("In file ")
                ]
                known_failures = [
                    line
                    for line in clean_lines
                    if any(marker in line for marker in KNOWN_PARSE_FAILURES)
                ]
                output_file = stage / "i18n_list.lua"
                if extractor_result.returncode != 0:
                    raise ExtractionError(
                        f"extractor failed for {component.id} with exit code "
                        f"{extractor_result.returncode}: "
                        f"{extractor_result.stderr.strip() or extractor_result.stdout[-2000:]}"
                    )
                if parse_failures or known_failures:
                    sample = (parse_failures + known_failures)[:10]
                    raise ExtractionError(
                        f"extractor reported parse failures for {component.id}: "
                        + " | ".join(sample)
                    )
                if not output_file.is_file():
                    raise ExtractionError(
                        f"extractor produced no i18n_list.lua for {component.id}"
                    )
            try:
                extracted_document = loader.load_path(
                    output_file,
                    logical_path=f"generated:{component.id}/i18n_list.lua",
                )
            except ValidationError as error:
                raise ExtractionError(str(error)) from error
            definitions = _normalized_definitions(
                component=component.id,
                records=extracted_document.records,
                origin_kind="extracted",
            )
            if not definitions:
                raise ExtractionError(
                    f"extractor produced zero tDef entries for {component.id}"
                )

            extracted_tdef_count = len(definitions)
            manual_tdef_count = 0
            if component.id == "engine":
                for manual_path in manifest.manual_definitions:
                    manual_document = loader.load_path(
                        manifest.root / manual_path,
                        logical_path=manual_path,
                    )
                    manual_definitions = _normalized_definitions(
                        component=component.id,
                        records=manual_document.records,
                        origin_kind="manual",
                    )
                    definitions.extend(manual_definitions)
                    manual_tdef_count += len(manual_definitions)

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
            snapshot_sha256 = hashlib.sha256(snapshot_data).hexdigest()
            if component.source_baseline is not None:
                baseline = component.source_baseline
                if snapshot_sha256 != baseline.snapshot_sha256:
                    raise ExtractionError(
                        f"protected baseline snapshot mismatch for {component.id}: "
                        f"{snapshot_sha256} != {baseline.snapshot_sha256}"
                    )
                if len(definitions) != baseline.tdef_count:
                    raise ExtractionError(
                        f"protected baseline count mismatch for {component.id}: "
                        f"{len(definitions)} != {baseline.tdef_count}"
                    )
            component_directory = run_directory / component.id
            atomic_write_bytes(component_directory / "snapshot.jsonl", snapshot_data)
            atomic_write_bytes(
                component_directory / "i18n_list.lua", output_file.read_bytes()
            )
            component_report = {
                "component": component.id,
                "source_access": (
                    "lua-extractor-only" if protected_access else "pinned-git-object"
                ),
                "source_repository": repository_name,
                "source_commit": source_commit,
                "source_lua_files": source_file_count,
                "mounts": mounts,
                "tdef_count": len(definitions),
                "extracted_tdef_count": extracted_tdef_count,
                "manual_tdef_count": manual_tdef_count,
                "snapshot_sha256": snapshot_sha256,
                "snapshot": str(component_directory / "snapshot.jsonl"),
                "raw_i18n_list": str(component_directory / "i18n_list.lua"),
                "log": None,
            }
            if combined_log is not None:
                log_path = component_directory / "extract.log"
                atomic_write_bytes(log_path, combined_log.encode("utf-8"))
                component_report["log"] = str(log_path)
            write_json(component_directory / "metadata.json", component_report)
            component_reports.append(component_report)

    report = {
        "ok": True,
        "version": manifest.version,
        "manifest": str(manifest.path),
        "extractor": {
            "repository": str(extractor_repo_path),
            "commit": manifest.extractor.commit,
            **patch_report,
        },
        "components": component_reports,
        "run_directory": str(run_directory),
    }
    write_json(run_directory / "summary.json", report)
    return report
