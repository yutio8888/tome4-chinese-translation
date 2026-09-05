"""Shared CLI configuration, component selection and environment helpers."""

from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from typing import Any, Iterable
from .config import ComponentSpec, Manifest, load_manifest


_PUBLIC_DLC_ROOT = Path("/Users/yun/projects/tome4-dlcs")

_PUBLIC_DLC_PATHS = {
    "TOME_DLC_ASHES_ROOT": "ashes-urhrok/tome-ashes-urhrok",
    "TOME_DLC_CULTS_ROOT": "cults/tome-cults",
    "TOME_DLC_ORCS_ROOT": "orcs/tome-orcs",
}


def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--version-manifest",
        default="tome-1.7.6",
        metavar="VERSION",
        help="version manifest name (default: tome-1.7.6)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="explicit manifest path for the selected --version-manifest",
    )
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")


def _manifest(arguments: argparse.Namespace) -> Manifest:
    return load_manifest(
        version=arguments.version_manifest,
        manifest_path=arguments.manifest,
    )


def _select_components(
    manifest: Manifest,
    identifiers: Iterable[str],
    *,
    default: str,
) -> list[ComponentSpec]:
    requested = list(identifiers)
    if requested:
        return [
            manifest.component(identifier)
            for identifier in dict.fromkeys(requested)
        ]
    if default == "extract":
        return [component for component in manifest.components if component.extract_by_default]
    if default == "status":
        return [
            component
            for component in manifest.components
            if component.official_locale is not None
        ]
    return list(manifest.components)


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def _public_dlc_root() -> Path:
    """Resolve the public DLC root portably (contract AC-9).

    Priority: TOME_PUBLIC_DLC_ROOT env override (if a directory), then
    ~/projects/tome4-dlcs (POSIX home), then the legacy macOS default
    /Users/yun/projects/tome4-dlcs. The last candidate is also the final
    fallback, so behavior on the original machine is unchanged.
    """
    configured = os.environ.get("TOME_PUBLIC_DLC_ROOT")
    candidates = []
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.append(Path.home() / "projects" / "tome4-dlcs")
    candidates.append(_PUBLIC_DLC_ROOT)
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return candidates[-1]


def _inject_public_dlc_env() -> None:
    """Point DLC extraction at the public GPL v3 release when the env is unset.

    The official DLC sources are GPL v3 public (see AGENTS.md). The public
    release under _public_dlc_root() is the canonical extraction input; the
    legacy TOME_DLC_*_ROOT values (if set by the user) still take precedence.
    """
    public_dlc_root = _public_dlc_root()
    if not public_dlc_root.is_dir():
        return
    for env_name, relative in _PUBLIC_DLC_PATHS.items():
        if env_name in os.environ:
            continue
        candidate = public_dlc_root / relative
        if candidate.is_dir():
            os.environ[env_name] = str(candidate)
