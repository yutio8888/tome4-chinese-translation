"""Publish the canonical translation overlay into the release addon repository.

Explicit install command (AGENTS.md: no canonical Lua or release repository is
ever rewritten without an explicit publish invocation).  Defaults to a dry run;
``--apply`` performs the actual write into the release repository.

The published file is the deterministic core addon artifact
(``build --profile addon --component tome --require-complete``) written to
``<addon-repo>/data/locales/zh_hans.lua``.  Everything else in the release
repository (lore/nullpack translation data, runtime hooks, superloads,
overloads, init.lua metadata) is left untouched.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from subprocess import SubprocessError
from typing import Any, Iterable

from .build import _render_addon_locale, build_addon_locale
from .config import Manifest
from .errors import ValidationError
from .git_source import GitRepository
from .locale_model import LocaleDocument, LocaleLoader
from .report import write_json

_LOCALE_RELATIVE = "data/locales/zh_hans.lua"
_INIT_RELATIVE = "init.lua"
_ADDON_VERSION_RE = re.compile(r"addon_version\s*=\s*\{(\d+),(\d+),(\d+)\}")


@dataclass(frozen=True)
class _FileSnapshot:
    data: bytes
    mode: int


def _read_file_snapshot(path: Path, *, label: str) -> _FileSnapshot:
    try:
        with path.open("rb") as stream:
            mode = stat.S_IMODE(os.fstat(stream.fileno()).st_mode)
            data = stream.read()
    except OSError as error:
        raise ValidationError(f"{label} failed for {path}: {error}") from error
    return _FileSnapshot(data=data, mode=mode)


def _atomic_replace_bytes(
    path: Path,
    data: bytes,
    mode: int,
    *,
    label: str,
) -> None:
    """Atomically replace *path* from a same-directory, mode-preserving file."""
    descriptor: int | None = None
    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
        )
        temporary_path = Path(temporary_name)
        stream = os.fdopen(descriptor, "wb")
        descriptor = None
        with stream:
            written = stream.write(data)
            if written != len(data):
                raise OSError(
                    f"short write: wrote {written} of {len(data)} bytes"
                )
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    except BaseException as error:
        cleanup_error: OSError | None = None
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError as close_error:
                cleanup_error = close_error
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError as unlink_error:
                cleanup_error = cleanup_error or unlink_error
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            if cleanup_error is not None:
                error.add_note(
                    "publish temporary-file cleanup failed: "
                    f"{cleanup_error}"
                )
            raise
        if isinstance(error, OSError) or cleanup_error is not None:
            detail = f"{label} failed for {path}: {error}"
            if cleanup_error is not None:
                detail += (
                    "; temporary-file cleanup also failed: "
                    f"{cleanup_error}"
                )
            raise ValidationError(detail) from error
        raise


def _verify_file_snapshot(
    path: Path,
    expected: _FileSnapshot,
    *,
    label: str,
) -> bytes:
    actual = _read_file_snapshot(path, label=label)
    if hashlib.sha256(actual.data).digest() != hashlib.sha256(expected.data).digest():
        raise ValidationError(f"{label} failed: written file hash mismatch")
    if actual.mode != expected.mode:
        raise ValidationError(
            f"{label} failed: written file mode "
            f"{oct(actual.mode)} != {oct(expected.mode)}"
        )
    return actual.data


def _rollback_files(
    paths: list[Path],
    snapshots: dict[Path, _FileSnapshot],
) -> list[str]:
    failures: list[str] = []
    for path in reversed(paths):
        snapshot = snapshots[path]
        try:
            _atomic_replace_bytes(
                path,
                snapshot.data,
                snapshot.mode,
                label="publish rollback",
            )
            _verify_file_snapshot(
                path,
                snapshot,
                label="publish rollback verification",
            )
        except Exception as error:
            failures.append(f"{path}: {error}")
    return failures


def _runtime_key(entry: dict[str, Any], *, label: str, index: int) -> tuple[str, str | None]:
    source = entry.get("source")
    source_tag = entry.get("source_tag")
    if not isinstance(source, str) or (
        source_tag is not None and not isinstance(source_tag, str)
    ):
        raise ValidationError(f"{label} entry {index} has an invalid runtime key")
    return source, source_tag


def _semantic_signature(entry: dict[str, Any], *, label: str, index: int) -> str:
    semantic = {
        "target": entry.get("target"),
        "args_order": entry.get("args_order"),
        "special": entry.get("special"),
    }
    try:
        return json.dumps(
            semantic,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise ValidationError(
            f"{label} entry {index} has non-canonical runtime semantics"
        ) from error


def _runtime_semantic_map(
    entries: Iterable[dict[str, Any]], *, label: str
) -> dict[tuple[str, str | None], str]:
    result: dict[tuple[str, str | None], str] = {}
    for index, entry in enumerate(entries):
        key = _runtime_key(entry, label=label, index=index)
        result[key] = _semantic_signature(entry, label=label, index=index)
    return result


def _sorted_runtime_keys(
    keys: Iterable[tuple[str, str | None]],
) -> list[tuple[str, str | None]]:
    return sorted(keys, key=lambda key: (key[0], key[1] is not None, key[1] or ""))


def _assert_publish_semantics(
    expected_entries: Iterable[dict[str, Any]],
    actual: LocaleDocument,
    *,
    label: str,
) -> None:
    expected = list(expected_entries)
    actual_entries = list(actual.translations)
    expected_map = _runtime_semantic_map(expected, label=f"{label} expected")
    actual_map = _runtime_semantic_map(actual_entries, label=f"{label} actual")
    missing = _sorted_runtime_keys(set(expected_map) - set(actual_map))
    unexpected = _sorted_runtime_keys(set(actual_map) - set(expected_map))
    mismatched = _sorted_runtime_keys(
        key
        for key in set(expected_map) & set(actual_map)
        if expected_map[key] != actual_map[key]
    )
    if (
        len(actual_entries) != len(expected)
        or missing
        or unexpected
        or mismatched
    ):
        raise ValidationError(
            f"{label} failed: entry_count={len(actual_entries)}/{len(expected)}, "
            f"missing={len(missing)} {missing!r}, "
            f"unexpected={len(unexpected)} {unexpected!r}, "
            f"mismatched={len(mismatched)} {mismatched!r}"
        )


def _count_entries(loader: LocaleLoader, path: Path) -> int:
    document = loader.load_path(path, logical_path=str(path))
    return len(document.translations)


def _bump_init_version(init_text: str) -> tuple[str, str]:
    match = _ADDON_VERSION_RE.search(init_text)
    if not match:
        raise ValidationError("release init.lua has no addon_version = {maj,min,pat}")
    major, minor, patch = (int(g) for g in match.groups())
    new_version = f"addon_version = {{{major},{minor},{patch + 1}}}"
    return _ADDON_VERSION_RE.sub(new_version, init_text, count=1), (
        f"{major}.{minor}.{patch + 1}"
    )


def _git_failure_detail(result: subprocess.CompletedProcess[str]) -> str:
    return (
        result.stderr.strip()
        or result.stdout.strip()
        or f"exit status {result.returncode}"
    )


def _assert_publish_targets_unstaged(
    addon_root: Path,
    published_paths: list[str],
) -> None:
    try:
        result = subprocess.run(
            [
                "git",
                "diff",
                "--cached",
                "--quiet",
                "--",
                *published_paths,
            ],
            cwd=addon_root,
            capture_output=True,
            text=True,
        )
    except (OSError, SubprocessError) as error:
        raise ValidationError(
            f"release git staged-state preflight failed to start: {error}"
        ) from error
    if result.returncode == 0:
        return
    if result.returncode == 1:
        raise ValidationError(
            "release git staged-state preflight refused: publish target "
            "paths have staged changes relative to HEAD: "
            + ", ".join(published_paths)
        )
    raise ValidationError(
        "release git staged-state preflight failed: "
        f"{_git_failure_detail(result)}"
    )


def _official_locale_keys(manifest: Manifest, loader: LocaleLoader) -> set[tuple[str, str | None]]:
    """(source, source_tag) keys of the official zh_hans locales (tome/engine/boot)."""
    repository = GitRepository(manifest.repository_path("engine"))
    commit = manifest.repositories["engine"].commit
    keys: set[tuple[str, str | None]] = set()
    for component_id in ("tome", "engine", "boot"):
        component = manifest.component(component_id)
        if not component.official_locale:
            continue
        document = loader.load_bytes(
            repository.read_blob(commit, component.official_locale),
            logical_path=f"{commit}:{component.official_locale}",
        )
        keys.update(
            (entry.get("source"), entry.get("source_tag"))
            for entry in document.translations
        )
    return keys


_DLC_COMPONENTS = ("ashes-urhrok", "cults", "orcs")


def _dlc_overlay_entries(
    manifest: Manifest,
    loader: LocaleLoader,
    official_keys: set[tuple[str, str | None]],
) -> list[dict[str, Any]]:
    """DLC entries whose runtime key is absent from the official locales.

    These are DLC-specific texts; entries that already exist in the official
    zh_hans locales are left to the core overlay/official inheritance so the
    DLC layer never shadows main-game strings.
    """
    entries: list[dict[str, Any]] = []
    seen: set[tuple[str, str | None]] = set()
    for component_id in _DLC_COMPONENTS:
        component = manifest.component(component_id)
        document = loader.load_path(
            manifest.root / component.translation, logical_path=component.translation
        )
        for entry in document.translations:
            key = (entry.get("source"), entry.get("source_tag"))
            if key in official_keys or key in seen:
                continue
            seen.add(key)
            rendered = dict(entry)
            rendered["section"] = component_id
            entries.append(rendered)
    return entries


def publish_addon(
    manifest: Manifest,
    loader: LocaleLoader,
    *,
    apply: bool,
    bump: bool,
    commit: bool,
) -> dict[str, Any]:
    if commit and not apply:
        raise ValidationError("commit=True requires apply=True")

    if "addon" not in manifest.repositories:
        raise ValidationError("manifest has no 'addon' release repository mapping")
    addon_root = manifest.repository_path("addon")
    if not addon_root.is_dir():
        raise ValidationError(f"release repository not found: {addon_root}")

    locale_path = addon_root / _LOCALE_RELATIVE
    init_path = addon_root / _INIT_RELATIVE
    if not locale_path.is_file() or not init_path.is_file():
        raise ValidationError(
            f"release repository layout mismatch (expected {_LOCALE_RELATIVE} "
            f"and {_INIT_RELATIVE} under {addon_root})"
        )
    if locale_path.is_symlink() or init_path.is_symlink():
        raise ValidationError(
            "release repository layout mismatch (publish files must be regular files, "
            "not symbolic links, so atomic rollback can restore their file state)"
        )

    published_paths = [_LOCALE_RELATIVE]
    if bump:
        published_paths.append(_INIT_RELATIVE)
    if commit:
        _assert_publish_targets_unstaged(addon_root, published_paths)

    components = [component for component in manifest.components if component.id == "tome"]
    if not components:
        raise ValidationError("manifest has no 'tome' component")
    build_report = build_addon_locale(
        manifest,
        loader,
        components,
        include_external_requirements=False,
    )
    # Merge DLC-specific entries (runtime keys absent from official locales)
    # into the same zh_hans.lua, in their own sections.
    official_keys = _official_locale_keys(manifest, loader)
    dlc_entries = _dlc_overlay_entries(manifest, loader, official_keys)
    merged_entries = list(build_report["delta_entries"]) + dlc_entries
    artifact_bytes = _render_addon_locale(manifest, merged_entries, skipped=[])
    new_entries = len(merged_entries)
    try:
        artifact_document = loader.load_bytes(
            artifact_bytes,
            logical_path="generated:publish/data/locales/zh_hans.lua",
        )
    except ValidationError as error:
        raise ValidationError(
            f"publish pre-write verification failed: {error}"
        ) from error
    _assert_publish_semantics(
        merged_entries,
        artifact_document,
        label="publish pre-write verification",
    )
    artifact_sha256 = hashlib.sha256(artifact_bytes).hexdigest()

    locale_snapshot = _read_file_snapshot(
        locale_path,
        label="release locale snapshot",
    )
    init_snapshot: _FileSnapshot | None = None
    snapshots = {locale_path: locale_snapshot}
    current_sha256 = hashlib.sha256(locale_snapshot.data).hexdigest()
    try:
        current_entries = _count_entries(loader, locale_path)
    except OSError as error:
        raise ValidationError(
            f"release locale verification failed for {locale_path}: {error}"
        ) from error
    dlc_entries_by_component = {
        component_id: sum(1 for e in dlc_entries if e.get("section") == component_id)
        for component_id in _DLC_COMPONENTS
    }

    old_version = None
    new_version = None
    new_init_bytes: bytes | None = None
    if bump:
        init_snapshot = _read_file_snapshot(
            init_path,
            label="release init snapshot",
        )
        snapshots[init_path] = init_snapshot
        try:
            init_text = init_snapshot.data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValidationError("release init.lua is not valid UTF-8") from error
        old_match = _ADDON_VERSION_RE.search(init_text)
        old_version = ".".join(old_match.groups()) if old_match else None
        new_init_text, new_version = _bump_init_version(init_text)
        new_init_bytes = new_init_text.encode("utf-8")
        verified_match = _ADDON_VERSION_RE.search(new_init_bytes.decode("utf-8"))
        if (
            verified_match is None
            or ".".join(verified_match.groups()) != new_version
        ):
            raise ValidationError("publish init.lua pre-write verification failed")

    report: dict[str, Any] = {
        "ok": True,
        "release_repository": str(addon_root),
        "locale_file": str(locale_path),
        "applied": apply,
        "commit": commit,
        "bump_addon_version": bump,
        "old_addon_version": old_version,
        "new_addon_version": new_version,
        "old_entries": current_entries,
        "new_entries": new_entries,
        "old_sha256": current_sha256,
        "new_sha256": artifact_sha256,
        "delta_runtime_keys": sum(
            c["delta_entries"] for c in build_report["components"]
        ),
        "dlc_entries": len(dlc_entries),
        "dlc_entries_by_component": dlc_entries_by_component,
        "override_entries": build_report["override_entries"],
        "new_entries_overlay": build_report["new_entries"],
        "verification": build_report["verification"],
    }

    if not apply:
        report["note"] = (
            "dry run: no file was written; re-run with --apply to publish"
        )
        return report

    touched_paths: list[Path] = []
    commit_completed = False
    try:
        touched_paths.append(locale_path)
        _atomic_replace_bytes(
            locale_path,
            artifact_bytes,
            locale_snapshot.mode,
            label="publish locale write",
        )

        # Verify the actual release file before changing init.lua or invoking git.
        written = _verify_file_snapshot(
            locale_path,
            _FileSnapshot(artifact_bytes, locale_snapshot.mode),
            label="publish verification",
        )
        if hashlib.sha256(written).hexdigest() != artifact_sha256:
            raise ValidationError(
                "publish verification failed: written file hash mismatch"
            )
        try:
            written_document = loader.load_path(
                locale_path,
                logical_path=str(locale_path),
            )
        except ValidationError as error:
            raise ValidationError(
                f"publish post-write verification failed: {error}"
            ) from error
        except OSError as error:
            raise ValidationError(
                f"publish post-write verification failed: {error}"
            ) from error
        _assert_publish_semantics(
            merged_entries,
            written_document,
            label="publish post-write verification",
        )
        report["verified_entries"] = len(written_document.translations)

        if bump:
            if new_init_bytes is None or init_snapshot is None:
                raise ValidationError(
                    "publish init.lua content was not prepared before apply"
                )
            touched_paths.append(init_path)
            _atomic_replace_bytes(
                init_path,
                new_init_bytes,
                init_snapshot.mode,
                label="publish init write",
            )
            _verify_file_snapshot(
                init_path,
                _FileSnapshot(new_init_bytes, init_snapshot.mode),
                label="publish init verification",
            )

        if commit:
            message = (
                f"publish: sync core zh_hans overlay from tools/i18n build "
                f"(sha256 {artifact_sha256[:16]}, {new_entries} entries"
                + (f", addon_version {new_version}" if new_version else "")
                + ")"
            )
            try:
                result = subprocess.run(
                    [
                        "git",
                        "commit",
                        "--only",
                        "-m",
                        message,
                        "--",
                        *published_paths,
                    ],
                    cwd=addon_root,
                    capture_output=True,
                    text=True,
                )
            except (OSError, SubprocessError) as error:
                raise ValidationError(
                    f"release git commit failed to start: {error}"
                ) from error
            if result.returncode != 0:
                raise ValidationError(
                    f"release git commit failed: {_git_failure_detail(result)}"
                )
            commit_completed = True
            report["commit_message"] = message
    except (KeyboardInterrupt, SystemExit) as error:
        if not commit_completed:
            rollback_failures = _rollback_files(touched_paths, snapshots)
            if rollback_failures:
                error.add_note(
                    "publish rollback failed: " + "; ".join(rollback_failures)
                )
        raise
    except Exception as error:
        if not commit_completed:
            rollback_failures = _rollback_files(touched_paths, snapshots)
            if rollback_failures:
                raise ValidationError(
                    "publish transaction rollback failed after "
                    f"{type(error).__name__}: "
                    + "; ".join(rollback_failures)
                ) from error
        if isinstance(error, (OSError, SubprocessError)):
            raise ValidationError(f"publish apply failed: {error}") from error
        raise

    if commit_completed:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=addon_root,
                capture_output=True,
                text=True,
            )
        except (OSError, SubprocessError):
            result = None
        if result is not None and result.returncode == 0:
            report["release_head"] = result.stdout.strip()

    return report
