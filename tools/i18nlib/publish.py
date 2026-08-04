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
import re
import subprocess
from pathlib import Path
from typing import Any

from .build import _render_addon_locale, build_addon_locale
from .config import Manifest
from .errors import ValidationError
from .git_source import GitRepository
from .locale_model import LocaleLoader, runtime_map
from .report import write_json

_LOCALE_RELATIVE = "data/locales/zh_hans.lua"
_INIT_RELATIVE = "init.lua"
_ADDON_VERSION_RE = re.compile(r"addon_version\s*=\s*\{(\d+),(\d+),(\d+)\}")


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
    if "addon" not in manifest.repositories:
        raise ValidationError("manifest has no 'addon' release repository mapping")
    addon_root = manifest.repository_path("addon")
    if not addon_root.is_dir():
        raise ValidationError(f"release repository not found: {addon_root}")

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
    artifact_sha256 = hashlib.sha256(artifact_bytes).hexdigest()

    locale_path = addon_root / _LOCALE_RELATIVE
    init_path = addon_root / _INIT_RELATIVE
    if not locale_path.is_file() or not init_path.is_file():
        raise ValidationError(
            f"release repository layout mismatch (expected {_LOCALE_RELATIVE} "
            f"and {_INIT_RELATIVE} under {addon_root})"
        )

    current_bytes = locale_path.read_bytes()
    current_sha256 = hashlib.sha256(current_bytes).hexdigest()
    current_entries = _count_entries(loader, locale_path)
    new_entries = len(merged_entries)
    dlc_entries_by_component = {
        component_id: sum(1 for e in dlc_entries if e.get("section") == component_id)
        for component_id in _DLC_COMPONENTS
    }

    old_version = None
    new_version = None
    if bump:
        init_text = init_path.read_text(encoding="utf-8")
        old_match = _ADDON_VERSION_RE.search(init_text)
        old_version = (
            ".".join(old_match.groups()) if old_match else None
        )
        _, new_version = _bump_init_version(init_text)

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

    locale_path.write_bytes(artifact_bytes)

    if bump:
        init_bytes = init_path.read_bytes()
        init_text = init_bytes.decode("utf-8")  # keep \r\n line endings
        new_init_text, _ = _bump_init_version(init_text)
        init_path.write_bytes(new_init_text.encode("utf-8"))

    if commit:
        message = (
            f"publish: sync core zh_hans overlay from tools/i18n build "
            f"(sha256 {artifact_sha256[:16]}, {new_entries} entries"
            + (f", addon_version {new_version}" if new_version else "")
            + ")"
        )
        result = subprocess.run(
            ["git", "add", _LOCALE_RELATIVE]
            + ([_INIT_RELATIVE] if bump else []),
            cwd=addon_root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise ValidationError(f"release git add failed: {result.stderr.strip()}")
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=addon_root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise ValidationError(f"release git commit failed: {result.stderr.strip()}")
        report["commit_message"] = message

    # verify the written file parses and matches the artifact
    written = locale_path.read_bytes()
    if hashlib.sha256(written).hexdigest() != artifact_sha256:
        raise ValidationError("publish verification failed: written file hash mismatch")
    written_entries = _count_entries(loader, locale_path)
    if written_entries != new_entries:
        raise ValidationError(
            f"publish verification failed: entry count {written_entries} != {new_entries}"
        )
    report["verified_entries"] = written_entries

    if commit:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=addon_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            report["release_head"] = result.stdout.strip()

    return report
