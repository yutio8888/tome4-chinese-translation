#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""有界 diff 复审 bundle 生成：仅包含 origin/master..HEAD（或指定基线）改动的译文条目。

复用 tools/i18nlib/review.py 的 bundle schema（kind=translations、item_id、
terminology context、constraints），输出到 .artifacts/i18n/review-diff-*/。

用法：
  python3 -B tools/review_diff.py [--baseline origin/master] [--batch-size 50]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib.config import DEFAULT_VERSION, Manifest, load_manifest  # noqa: E402
from i18nlib.errors import I18nToolError  # noqa: E402
from i18nlib.locale_model import LocaleLoader  # noqa: E402
from i18nlib.review import (  # noqa: E402
    DEFAULT_REVIEW_BATCH_SIZE,
    MAX_REVIEW_BATCH_SIZE,
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    TOOL_VERSION,
    _bundle_id,
    _entry_id,
    _relevant_terms,
    _review_index_id,
    _terminology_rows,
)
from i18nlib.runtime import LuaRuntime  # noqa: E402


class ReviewDiffError(RuntimeError):
    """A fatal review-diff input error."""


def _review_batch_size(value: str) -> int:
    try:
        batch_size = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"invalid review batch size: {value!r}"
        ) from error
    if not 1 <= batch_size <= MAX_REVIEW_BATCH_SIZE:
        raise argparse.ArgumentTypeError(
            f"review batch size must be between 1 and {MAX_REVIEW_BATCH_SIZE}"
        )
    return batch_size


def _run_git(root: Path, arguments: Sequence[str], *, operation: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments],
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
        raise ReviewDiffError(f"{operation}: {error}") from error
    if result.returncode != 0:
        detail = (
            result.stderr.decode("utf-8", errors="replace").strip()
            or result.stdout.decode("utf-8", errors="replace").strip()
            or f"git exited with status {result.returncode}"
        )
        raise ReviewDiffError(f"{operation}: {detail}")
    return result.stdout


def _resolve_baseline_tree(root: Path, baseline: str) -> str:
    output = _run_git(
        root,
        ["rev-parse", "--verify", "--end-of-options", f"{baseline}^{{tree}}"],
        operation=f"cannot resolve baseline {baseline!r} as a commit or tree",
    )
    try:
        tree = output.strip().decode("ascii")
    except UnicodeDecodeError as error:
        raise ReviewDiffError(
            f"cannot resolve baseline {baseline!r}: git returned a malformed tree ID"
        ) from error
    if len(tree) not in {40, 64} or any(
        character not in "0123456789abcdef" for character in tree
    ):
        raise ReviewDiffError(
            f"cannot resolve baseline {baseline!r}: git returned a malformed tree ID"
        )
    return tree


def _preflight_translation_paths(
    manifest: Manifest,
) -> list[tuple[str, str, Path]]:
    translations: list[tuple[str, str, Path]] = []
    invalid: list[tuple[str, str]] = []
    for component in manifest.components:
        if not component.translation:
            continue
        logical_path = component.translation
        path = manifest.root / logical_path
        if path.is_file():
            translations.append((component.id, logical_path, path))
        else:
            invalid.append((component.id, logical_path))
    if invalid:
        details = "\n".join(
            f"  - component {component!r}: {logical_path}"
            for component, logical_path in invalid
        )
        raise ReviewDiffError(
            "manifest translation files are missing or not regular files:\n"
            f"{details}"
        )
    return translations


def _read_baseline_blob(root: Path, tree: str, path: str) -> bytes | None:
    listing = _run_git(
        root,
        ["ls-tree", "-z", "--full-tree", tree, "--", f":(literal){path}"],
        operation=f"cannot inspect baseline path {path!r}",
    )
    records = [record for record in listing.split(b"\0") if record]
    if not records:
        return None
    if len(records) != 1:
        raise ReviewDiffError(
            f"cannot inspect baseline path {path!r}: git returned multiple entries"
        )
    metadata, separator, listed_path = records[0].partition(b"\t")
    fields = metadata.split(b" ")
    if not separator or len(fields) != 3:
        raise ReviewDiffError(
            f"cannot inspect baseline path {path!r}: git returned malformed metadata"
        )
    mode, object_type, object_id = fields
    if listed_path != os.fsencode(path):
        raise ReviewDiffError(
            f"cannot inspect baseline path {path!r}: git returned a different path"
        )
    if object_type != b"blob" or mode not in {b"100644", b"100755"}:
        kind = object_type.decode("ascii", errors="replace")
        raise ReviewDiffError(
            f"cannot read baseline path {path!r}: expected a regular blob, "
            f"found {kind} with mode {mode.decode('ascii', errors='replace')}"
        )
    try:
        object_name = object_id.decode("ascii")
    except UnicodeDecodeError as error:
        raise ReviewDiffError(
            f"cannot inspect baseline path {path!r}: git returned a malformed object ID"
        ) from error
    if len(object_name) not in {40, 64} or any(
        character not in "0123456789abcdef" for character in object_name
    ):
        raise ReviewDiffError(
            f"cannot inspect baseline path {path!r}: git returned a malformed object ID"
        )
    return _run_git(
        root,
        ["cat-file", "blob", object_name],
        operation=f"cannot read baseline path {path!r}",
    )


def _revision_semantics(entry: dict[str, Any]) -> str:
    """Return the canonical target-side fields used by revision identity."""
    return json.dumps(
        {
            "target": entry.get("target"),
            "args_order": entry.get("args_order"),
            "special": entry.get("special"),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _changed_translation_items(
    component: str,
    current_entries: Sequence[dict[str, Any]],
    baseline_entries: Sequence[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    baseline_revisions = Counter(
        (
            (
                entry.get("section"),
                entry.get("source"),
                entry.get("source_tag"),
            ),
            _revision_semantics(entry),
        )
        for entry in baseline_entries or ()
    )
    items: list[dict[str, Any]] = []
    for ordinal, entry in enumerate(current_entries):
        revision = (
            (
                entry.get("section"),
                entry.get("source"),
                entry.get("source_tag"),
            ),
            _revision_semantics(entry),
        )
        if baseline_revisions[revision] > 0:
            baseline_revisions[revision] -= 1
            continue
        items.append(
            {
                "item_id": _entry_id(component, ordinal, entry),
                "component": component,
                "ordinal": ordinal,
                "section": entry.get("section"),
                "source": entry.get("source"),
                "target": entry.get("target"),
                "source_tag": entry.get("source_tag"),
                "args_order": entry.get("args_order"),
                "special": entry.get("special"),
                "line": entry.get("line"),
            }
        )
    return items


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )


def _publish_artifacts(
    run_dir: Path,
    bundle_artifacts: Sequence[tuple[Path, dict[str, Any]]],
    index_payload: dict[str, Any],
) -> None:
    """Write a complete run beside its destination, then publish it atomically."""
    if os.path.lexists(run_dir):
        raise ReviewDiffError(
            f"output path already exists; refusing to overwrite: {run_dir}"
        )

    parent = run_dir.parent
    parent.mkdir(parents=True, exist_ok=True)
    if os.path.lexists(run_dir):
        raise ReviewDiffError(
            f"output path already exists; refusing to overwrite: {run_dir}"
        )

    staging_dir = Path(
        tempfile.mkdtemp(
            prefix=f".{run_dir.name}.staging-",
            dir=parent,
        )
    )
    try:
        for relative_path, payload in bundle_artifacts:
            staged_path = staging_dir / relative_path
            staged_path.parent.mkdir(parents=True, exist_ok=True)
            _write_json(staged_path, payload)
        _write_json(staging_dir / "review-index.json", index_payload)

        if os.path.lexists(run_dir):
            raise ReviewDiffError(
                f"output path already exists; refusing to overwrite: {run_dir}"
            )
        staging_dir.replace(run_dir)
        staging_dir = None
    finally:
        if staging_dir is not None and os.path.lexists(staging_dir):
            shutil.rmtree(staging_dir)


def _generate_review(
    *,
    baseline: str,
    batch_size: int,
    run_dir: Path,
) -> tuple[int, int, str]:
    """Load and validate every input, then publish the completed review run."""
    baseline_tree = _resolve_baseline_tree(ROOT, baseline)
    manifest = load_manifest(version=DEFAULT_VERSION)
    translations = _preflight_translation_paths(manifest)

    runtime = LuaRuntime(manifest=manifest)
    loader = LocaleLoader(runtime)
    terminology_rows, terminology_sha256 = _terminology_rows(
        manifest.root / manifest.terminology
    )
    manifest_sha256 = __import__("hashlib").sha256(manifest.raw_bytes).hexdigest()

    bundle_artifacts: list[tuple[Path, dict[str, Any]]] = []
    bundles: list[dict[str, Any]] = []
    changed_total = 0
    for component, rel, path in translations:
        base = _read_baseline_blob(ROOT, baseline_tree, rel)
        doc_now = loader.load_path(path, logical_path=rel)
        doc_base = (
            None if base is None else loader.load_bytes(base, logical_path=rel)
        )
        items = _changed_translation_items(
            component,
            doc_now.translations,
            None if doc_base is None else doc_base.translations,
        )
        if not items:
            continue
        changed_total += len(items)
        for offset in range(0, len(items), batch_size):
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
                    "total": len(items),
                },
                "items": batch,
                "terminology_sha256": terminology_sha256,
                "terminology": _relevant_terms(
                    terminology_rows, batch, component
                ),
                "constraints": [
                    "Review only the supplied canonical translation entries.",
                    "Preserve source, source_tag, printf arguments, and control markers in any suggested fix.",
                    "Return findings only; do not rewrite files or invent missing game context.",
                ],
            }
            bundle_id = _bundle_id(payload)
            payload["bundle_id"] = bundle_id
            relative_path = (
                Path("translations") / component / f"{bundle_id}.json"
            )
            bundle_artifacts.append((relative_path, payload))
            bundles.append(
                {
                    "bundle_id": bundle_id,
                    "kind": "translations",
                    "component": component,
                    "offset": offset,
                    "count": len(batch),
                    "total": len(items),
                    "path": str(run_dir / relative_path),
                }
            )

    index_payload = {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "review_contract": REVIEW_CONTRACT,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "manifest_sha256": manifest_sha256,
        "scope": {"translations": True, "code": False},
        "redacted_absolute_path_count": 0,
        "baseline": baseline,
        "bundles": bundles,
    }
    review_id = _review_index_id(index_payload)
    index_payload["review_id"] = review_id

    _publish_artifacts(run_dir, bundle_artifacts, index_payload)
    return changed_total, len(bundles), review_id


def _run(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default="origin/master",
                        help="git baseline revision (default: origin/master)")
    parser.add_argument(
        "--batch-size",
        type=_review_batch_size,
        default=DEFAULT_REVIEW_BATCH_SIZE,
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="explicit new output directory (must not already exist)",
    )
    args = parser.parse_args(argv)

    run_dir = Path(args.out_dir) if args.out_dir else (
        ROOT / ".artifacts" / "i18n" / (
            "review-diff-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
    )

    try:
        changed_total, bundle_count, review_id = _generate_review(
            baseline=args.baseline,
            batch_size=args.batch_size,
            run_dir=run_dir,
        )
    except (I18nToolError, ReviewDiffError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(f"baseline: {args.baseline}")
    print(f"changed entries: {changed_total}, bundles: {bundle_count}")
    print(f"review_id: {review_id}")
    print(f"run_dir: {run_dir}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    signal.alarm(600)
    try:
        return _run(argv)
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
