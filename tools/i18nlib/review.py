"""Bounded, read-only review bundles for translations and public code changes."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

from . import TOOL_VERSION
from .config import Manifest
from .errors import ConfigurationError, ValidationError
from .locale_model import LocaleLoader
from .report import create_run_directory, write_json
from .runtime import LuaRuntime
from .workset import _relevant_terms, _terminology_rows


REVIEW_SCHEMA_VERSION = 1
REVIEW_CONTRACT = "tome4-review-v1"
DEFAULT_REVIEW_BATCH_SIZE = 50
MAX_REVIEW_BATCH_SIZE = 100
DEFAULT_REVIEW_TIMEOUT = 1200
REVIEW_KINDS = frozenset({"translations", "code"})
ABSOLUTE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_/:])/(?![\\\[\](){}])(?:[^\s`\"']+)"
)
PUBLIC_REVIEW_ROOTS = (".agents", ".codex", "docs", "i18n", "tools", "tests")
PUBLIC_REVIEW_FILES = (
    ".gitignore",
    "AGENTS.md",
    "handoff.md",
    "pi-agent-analysis.md",
    "TERMINOLOGY.md",
    "terminology.tsv",
)


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _relative_path(value: str) -> str:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValidationError(f"review bundle contains an unsafe path: {value!r}")
    return value.replace(os.sep, "/")


def _public_review_files(manifest: Manifest | None = None) -> tuple[str, ...]:
    files = list(PUBLIC_REVIEW_FILES)
    if manifest is not None:
        files.extend(
            component.copy_fragment
            for component in manifest.components
            if component.copy_fragment
        )
        files.extend(manifest.manual_definitions)
    normalized: list[str] = []
    for value in files:
        if not isinstance(value, str) or not value:
            raise ValidationError(
                f"review manifest contains an unsafe path: {value!r}"
            )
        path = _relative_path(value)
        if path not in normalized:
            normalized.append(path)
    return tuple(normalized)


def _redact_absolute_paths(value: str) -> tuple[str, int]:
    redactions = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal redactions
        if match.group(0) == "/dev/null":
            line_start = value.rfind("\n", 0, match.start()) + 1
            line_end = value.find("\n", match.end())
            if line_end == -1:
                line_end = len(value)
            if value[line_start:line_end].rstrip("\r") in {
                "--- /dev/null",
                "+++ /dev/null",
            }:
                return match.group(0)
        redactions += 1
        return "<redacted-absolute-path>"

    return ABSOLUTE_PATH_RE.sub(replace, value), redactions


def _entry_id(
    component: str, ordinal: int, entry: dict[str, Any]
) -> str:
    identity = {
        "component": component,
        "ordinal": ordinal,
        "section": entry.get("section"),
        "source": entry.get("source"),
        "source_tag": entry.get("source_tag"),
        "target": entry.get("target"),
        "args_order": entry.get("args_order"),
        "special": entry.get("special"),
    }
    return "translation-" + _canonical_sha256(identity)


def _translation_items(
    manifest: Manifest, loader: LocaleLoader, component: str
) -> list[dict[str, Any]]:
    spec = manifest.component(component)
    document = loader.load_path(
        manifest.root / spec.translation,
        logical_path=spec.translation,
    )
    items: list[dict[str, Any]] = []
    for ordinal, entry in enumerate(document.translations):
        source = entry.get("source")
        target = entry.get("target")
        section = entry.get("section")
        source_tag = entry.get("source_tag")
        if not all(isinstance(value, str) for value in (source, target, section)):
            raise ValidationError(
                f"invalid canonical translation entry in component {component}"
            )
        item = {
            "item_id": _entry_id(component, ordinal, entry),
            "component": component,
            "ordinal": ordinal,
            "section": section,
            "source": source,
            "target": target,
            "source_tag": source_tag,
            "args_order": entry.get("args_order"),
            "special": entry.get("special"),
            "line": entry.get("line"),
        }
        items.append(item)
    return items


def _git_status_paths(
    root: Path, manifest: Manifest | None = None
) -> list[tuple[str, str, str | None]]:
    pathspecs = [*_public_review_files(manifest), *PUBLIC_REVIEW_ROOTS]
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "status",
                "--porcelain=v1",
                "-z",
                "--untracked-files=all",
                "--",
                *pathspecs,
            ],
            cwd=root,
            env={
                key: value
                for key, value in os.environ.items()
                if not key.startswith("GIT_")
            },
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise ConfigurationError(f"cannot inspect public worktree changes: {error}") from error
    if result.returncode != 0:
        raise ConfigurationError(
            "cannot inspect public worktree changes: "
            + (os.fsdecode(result.stderr).strip() or "git status failed")
        )
    paths: list[tuple[str, str, str | None]] = []
    fields = result.stdout.split(b"\0")
    index = 0
    while index < len(fields):
        record = fields[index]
        index += 1
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            continue
        status_bytes = record[:2]
        path = _relative_path(os.fsdecode(record[3:]))
        source_path = None
        if b"R" in status_bytes or b"C" in status_bytes:
            # With ``-z``, rename/copy records contain the destination/current
            # path first and the source path in a second NUL-delimited field.
            if index >= len(fields) or not fields[index]:
                continue
            source_path = _relative_path(os.fsdecode(fields[index]))
            index += 1
        paths.append((os.fsdecode(status_bytes), path, source_path))
    return paths


def _is_public_review_path(
    path: str, manifest: Manifest | None = None
) -> bool:
    return path in _public_review_files(manifest) or any(
        path == root or path.startswith(root + "/") for root in PUBLIC_REVIEW_ROOTS
    )


def _git_diff(root: Path, path: str, *, untracked: bool = False) -> str:
    if untracked:
        file_path = root / path
        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError as error:
            if error.errno == 2:
                return ""
            raise ConfigurationError(
                f"cannot read public changed file {path}: {error}"
            ) from error
        return f"--- /dev/null\n+++ b/{path}\n@@ added file @@\n{content}"
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "diff",
                "--no-ext-diff",
                "--unified=80",
                "HEAD",
                "--",
                path,
            ],
            cwd=root,
            env={
                key: value
                for key, value in os.environ.items()
                if not key.startswith("GIT_")
            },
            capture_output=True,
            check=False,
            text=True,
        )
    except OSError as error:
        raise ConfigurationError(f"cannot read public code diff: {error}") from error
    if result.returncode != 0:
        raise ConfigurationError(
            f"cannot read public code diff for {path}: "
            + (result.stderr.strip() or "git diff failed")
        )
    return result.stdout


def _code_items(
    root: Path, manifest: Manifest | None = None
) -> tuple[list[dict[str, Any]], int]:
    items: list[dict[str, Any]] = []
    redactions = 0
    for status, path, source_path in _git_status_paths(root, manifest):
        changed_paths = [path]
        if source_path is not None and "R" in status:
            changed_paths.append(source_path)
        for changed_path in changed_paths:
            if not _is_public_review_path(changed_path, manifest):
                continue
            diff = _git_diff(root, changed_path, untracked=status == "??")
            if not diff:
                continue
            redacted, count = _redact_absolute_paths(diff)
            redactions += count
            items.append(
                {
                    "item_id": "code-"
                    + _canonical_sha256({"path": changed_path, "status": status}),
                    "path": changed_path,
                    "status": status,
                    "diff": redacted,
                }
            )
    return items, redactions


def _bundle_id(payload: dict[str, Any]) -> str:
    return _canonical_sha256(payload)


def _review_index_id(payload: dict[str, Any]) -> str:
    """Hash semantic review selection without run-local artifact paths."""
    bundles = payload.get("bundles", [])
    identity_bundles = [
        {
            key: item[key]
            for key in ("bundle_id", "kind", "component", "offset", "count", "total")
            if key in item
        }
        for item in bundles
        if isinstance(item, dict)
    ]
    identity_bundles.sort(
        key=lambda item: (
            str(item.get("kind", "")),
            str(item.get("component", "")),
            int(item.get("offset", 0)),
            str(item.get("bundle_id", "")),
        )
    )
    return _canonical_sha256(
        {
            "schema_version": payload.get("schema_version"),
            "review_contract": payload.get("review_contract"),
            "tool_version": payload.get("tool_version"),
            "version": payload.get("version"),
            "manifest_sha256": payload.get("manifest_sha256"),
            "scope": payload.get("scope"),
            "redacted_absolute_path_count": payload.get(
                "redacted_absolute_path_count"
            ),
            "bundles": identity_bundles,
        }
    )


def _write_translation_bundles(
    run_directory: Path,
    manifest: Manifest,
    loader: LocaleLoader,
    batch_size: int,
) -> list[dict[str, Any]]:
    bundles: list[dict[str, Any]] = []
    manifest_sha256 = hashlib.sha256(manifest.raw_bytes).hexdigest()
    terminology_rows, terminology_sha256 = _terminology_rows(
        manifest.root / manifest.terminology
    )
    components = [component.id for component in manifest.components]
    for component in components:
        items = _translation_items(manifest, loader, component)
        total = len(items)
        for offset in range(0, total, batch_size):
            batch = items[offset : offset + batch_size]
            payload = {
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "tool_version": TOOL_VERSION,
                "version": manifest.version,
                "manifest_sha256": manifest_sha256,
                "kind": "translations",
                "component": component,
                "selection": {
                    "offset": offset,
                    "count": len(batch),
                    "total": total,
                },
                "items": batch,
                "terminology_sha256": terminology_sha256,
                "terminology": _relevant_terms(terminology_rows, batch, component),
                "constraints": [
                    "Review only the supplied canonical translation entries.",
                    "Preserve source, source_tag, printf arguments, and control markers in any suggested fix.",
                    "Return findings only; do not rewrite files or invent missing game context.",
                ],
            }
            bundle_id = _bundle_id(payload)
            payload["bundle_id"] = bundle_id
            output = run_directory / "translations" / component / f"{bundle_id}.json"
            write_json(output, payload)
            bundles.append(
                {
                    "bundle_id": bundle_id,
                    "kind": "translations",
                    "component": component,
                    "offset": offset,
                    "count": len(batch),
                    "total": total,
                    "path": str(output),
                }
            )
    return bundles


def _write_code_bundles(
    run_directory: Path, manifest: Manifest, batch_size: int
) -> tuple[list[dict[str, Any]], int]:
    code_items, redactions = _code_items(manifest.root, manifest)
    if not code_items:
        return [], redactions
    bundles: list[dict[str, Any]] = []
    manifest_sha256 = hashlib.sha256(manifest.raw_bytes).hexdigest()
    for offset in range(0, len(code_items), batch_size):
        batch = code_items[offset : offset + batch_size]
        payload = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "tool_version": TOOL_VERSION,
            "version": manifest.version,
            "manifest_sha256": manifest_sha256,
            "kind": "code",
            "selection": {
                "offset": offset,
                "count": len(batch),
                "total": len(code_items),
            },
            "files": batch,
            "constraints": [
                "Review only the supplied public worktree diff.",
                "Do not assume access to repository files, tools, sessions, or external source.",
                "Return findings only; do not edit files or propose changes outside the supplied diff.",
            ],
        }
        bundle_id = _bundle_id(payload)
        payload["bundle_id"] = bundle_id
        output = run_directory / "code" / f"{bundle_id}.json"
        write_json(output, payload)
        bundles.append(
            {
                "bundle_id": bundle_id,
                "kind": "code",
                "offset": offset,
                "count": len(batch),
                "total": len(code_items),
                "path": str(output),
            }
        )
    return bundles, redactions


def create_review_index(
    manifest: Manifest,
    *,
    batch_size: int = DEFAULT_REVIEW_BATCH_SIZE,
    include_translations: bool,
    include_code: bool,
) -> dict[str, Any]:
    if type(batch_size) is not int:
        raise ValidationError("review batch size must be an integer")
    if not 1 <= batch_size <= MAX_REVIEW_BATCH_SIZE:
        raise ValidationError(
            f"review batch size must be between 1 and {MAX_REVIEW_BATCH_SIZE}"
        )
    if type(include_translations) is not bool:
        raise ValidationError("review include_translations must be a boolean")
    if type(include_code) is not bool:
        raise ValidationError("review include_code must be a boolean")
    if not include_translations and not include_code:
        raise ValidationError("review must include translations or code")
    run_directory = create_run_directory(manifest.root, "review")
    translation_bundles: list[dict[str, Any]] = []
    if include_translations:
        runtime = LuaRuntime(manifest)
        loader = LocaleLoader(runtime)
        translation_bundles = _write_translation_bundles(
            run_directory, manifest, loader, batch_size
        )
    code_bundles, redactions = (
        _write_code_bundles(run_directory, manifest, batch_size)
        if include_code
        else ([], 0)
    )
    bundles = translation_bundles + code_bundles
    index_payload = {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "review_contract": REVIEW_CONTRACT,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "manifest_sha256": hashlib.sha256(manifest.raw_bytes).hexdigest(),
        "scope": {
            "translations": include_translations,
            "code": include_code,
            "protected_sources": False,
        },
        "redacted_absolute_path_count": redactions,
        "bundles": bundles,
        "run_directory": str(run_directory),
    }
    index_path = run_directory / "review-index.json"
    index_payload["index"] = str(index_path)
    index_payload["review_id"] = _review_index_id(index_payload)
    write_json(index_path, index_payload)
    return index_payload


def _read_bundle(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except OSError as error:
        raise ValidationError(f"cannot read review bundle: {path}") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid review bundle: {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError("review bundle must be an object")
    return value


def validate_review_bundle(manifest: Manifest, path: Path) -> dict[str, Any]:
    bundle = _read_bundle(path)
    if (
        type(bundle.get("schema_version")) is not int
        or bundle.get("schema_version") != REVIEW_SCHEMA_VERSION
    ):
        raise ValidationError("unsupported review bundle schema")
    if bundle.get("review_contract") != REVIEW_CONTRACT:
        raise ValidationError("unsupported review contract")
    if bundle.get("tool_version") != TOOL_VERSION:
        raise ValidationError("review bundle was generated by a different tool version")
    if bundle.get("version") != manifest.version:
        raise ValidationError("review bundle version does not match the selected manifest")
    expected_manifest = hashlib.sha256(manifest.raw_bytes).hexdigest()
    if bundle.get("manifest_sha256") != expected_manifest:
        raise ValidationError("review bundle manifest digest is stale or invalid")
    kind = bundle.get("kind")
    if kind not in REVIEW_KINDS:
        raise ValidationError("review bundle kind is invalid")
    if bundle.get("bundle_id") != _bundle_id({key: value for key, value in bundle.items() if key != "bundle_id"}):
        raise ValidationError("review bundle id is invalid")
    if kind == "translations":
        component = bundle.get("component")
        if not isinstance(component, str):
            raise ValidationError("translation review bundle has no component")
        manifest.component(component)
        items = bundle.get("items")
        if not isinstance(items, list) or not items:
            raise ValidationError("translation review bundle items are invalid")
        for item in items:
            if not isinstance(item, dict):
                raise ValidationError("translation review item is invalid")
            if item.get("component") != component:
                raise ValidationError("translation review item has the wrong component")
            if not isinstance(item.get("item_id"), str):
                raise ValidationError("translation review item has no item_id")
            if not all(isinstance(item.get(key), str) for key in ("section", "source", "target")):
                raise ValidationError("translation review item has invalid text")
        if "terminology" in bundle:
            if not isinstance(bundle.get("terminology_sha256"), str):
                raise ValidationError("translation review terminology digest is invalid")
            terminology = bundle.get("terminology")
            if not isinstance(terminology, list):
                raise ValidationError("translation review terminology is invalid")
            for term in terminology:
                if not isinstance(term, dict) or not all(
                    isinstance(term.get(key), str)
                    for key in ("source", "target", "category", "source_tag", "status", "scope", "notes")
                ):
                    raise ValidationError("translation review terminology row is invalid")
    else:
        files = bundle.get("files")
        if not isinstance(files, list) or not files:
            raise ValidationError("code review bundle files are invalid")
        for item in files:
            if not isinstance(item, dict):
                raise ValidationError("code review file item is invalid")
            path_value = item.get("path")
            if not isinstance(path_value, str) or not _is_public_review_path(
                path_value, manifest
            ):
                raise ValidationError("code review contains a path outside the public review scope")
            if Path(path_value).is_absolute() or ".." in Path(path_value).parts:
                raise ValidationError("code review contains an unsafe path")
            if not isinstance(item.get("diff"), str):
                raise ValidationError("code review file has no diff")
    return bundle


def _validate_findings_for_remediation(
    bundle: dict[str, Any], review: dict[str, Any]
) -> None:
    if (
        type(review.get("schema_version")) is not int
        or review.get("schema_version") != REVIEW_SCHEMA_VERSION
    ):
        raise ValidationError("validated review has an unsupported schema")
    if review.get("review_contract") != REVIEW_CONTRACT:
        raise ValidationError("validated review has an unsupported contract")
    if review.get("bundle_id") != bundle.get("bundle_id"):
        raise ValidationError("validated review bundle_id does not match")
    findings = review.get("findings")
    if not isinstance(findings, list) or len(findings) > 200:
        raise ValidationError("validated review findings are invalid")
    if bundle.get("kind") == "translations":
        allowed = {
            item.get("item_id")
            for item in bundle.get("items", [])
            if isinstance(item, dict)
        }
    else:
        allowed = {
            item.get("item_id")
            for item in bundle.get("files", [])
            if isinstance(item, dict)
        }
    seen: set[str] = set()
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValidationError(f"validated review finding {index} is invalid")
        finding_id = finding.get("finding_id")
        if not isinstance(finding_id, str) or not finding_id or finding_id in seen:
            raise ValidationError(f"validated review finding {index} has an invalid id")
        if finding.get("item_id") not in allowed:
            raise ValidationError(f"validated review finding {index} references an unknown item")
        if not isinstance(finding.get("severity"), str) or not isinstance(finding.get("category"), str):
            raise ValidationError(f"validated review finding {index} has invalid classification")
        if not isinstance(finding.get("title"), str) or not finding["title"].strip():
            raise ValidationError(f"validated review finding {index} has no title")
        if not isinstance(finding.get("body"), str) or not finding["body"].strip():
            raise ValidationError(f"validated review finding {index} has no body")
        seen.add(finding_id)


def review_index_summary(index: dict[str, Any]) -> dict[str, Any]:
    bundles = index.get("bundles", [])
    return {
        "review_id": index.get("review_id"),
        "index": index.get("index"),
        "bundles": len(bundles) if isinstance(bundles, list) else 0,
        "translation_bundles": sum(
            item.get("kind") == "translations"
            for item in bundles
            if isinstance(item, dict)
        ),
        "code_bundles": sum(
            item.get("kind") == "code"
            for item in bundles
            if isinstance(item, dict)
        ),
        "protected_sources_included": False,
    }
