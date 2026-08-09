#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""有界 diff 复审 bundle 生成：仅包含 origin/master..HEAD（或指定基线）改动的译文条目。

复用 tools/i18nlib/review.py 的 translation semantic v2 bundle schema，输出到
.artifacts/i18n/review-diff-*/。盲发现 bundle 不注入术语或 Facts。

用法：
  python3 -B tools/review_diff.py [--baseline origin/master] [--batch-size 10]
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
    REVIEW_INDEX_CONTRACT,
    REVIEW_INDEX_SCHEMA_VERSION,
    TOOL_VERSION,
    _bundle_id,
    _review_index_id,
    _translation_bundle_payload,
)
from i18nlib.runtime import LuaRuntime  # noqa: E402
from i18nlib.report import json_bytes  # noqa: E402
from i18nlib.translation_review import (  # noqa: E402
    DEFAULT_TRANSLATION_CHARACTER_BUDGET,
    MAX_TRANSLATION_CHARACTER_BUDGET,
    MAX_TRANSLATION_REVIEW_BATCH_SIZE,
    TRANSLATION_REVIEW_BUNDLE_CONTRACT,
    TRANSLATION_REVIEW_CHANNEL,
    TRANSLATION_REVIEW_SCHEMA_VERSION,
    build_translation_item,
    deduplicate_translation_revisions,
    load_translation_review_policy,
    partition_translation_items,
    translation_provider_message,
    translation_selection_sha256,
    write_translation_inventory,
)

MAX_REVIEW_BATCH_SIZE = MAX_TRANSLATION_REVIEW_BATCH_SIZE


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


def _review_character_budget(value: str) -> int:
    try:
        character_budget = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"invalid review character budget: {value!r}"
        ) from error
    if not 1 <= character_budget <= MAX_TRANSLATION_CHARACTER_BUDGET:
        raise argparse.ArgumentTypeError(
            "review character budget must be between 1 and "
            f"{MAX_TRANSLATION_CHARACTER_BUDGET}"
        )
    return character_budget


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
    *,
    version: str = DEFAULT_VERSION,
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
            build_translation_item(
                version=version,
                component=component,
                ordinal=ordinal,
                entry=entry,
            )
        )
    return deduplicate_translation_revisions(items)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_bytes(json_bytes(payload))


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
    character_budget: int,
    run_dir: Path,
) -> tuple[int, int, str]:
    """Load and validate every input, then publish the completed review run."""
    baseline_tree = _resolve_baseline_tree(ROOT, baseline)
    manifest = load_manifest(version=DEFAULT_VERSION)
    translations = _preflight_translation_paths(manifest)

    runtime = LuaRuntime(manifest=manifest)
    loader = LocaleLoader(runtime)
    _policy, policy_sha256 = load_translation_review_policy(manifest.root)
    manifest_sha256 = __import__("hashlib").sha256(manifest.raw_bytes).hexdigest()

    bundle_artifacts: list[tuple[Path, dict[str, Any]]] = []
    bundles: list[dict[str, Any]] = []
    changed_total = 0
    for component, rel, path in translations:
        base = _read_baseline_blob(ROOT, baseline_tree, rel)
        try:
            current_bytes = path.read_bytes()
        except OSError as error:
            raise ReviewDiffError(
                f"cannot read current translation path {rel!r}: {error}"
            ) from error
        doc_now = loader.load_bytes(current_bytes, logical_path=rel)
        doc_base = (
            None if base is None else loader.load_bytes(base, logical_path=rel)
        )
        items = _changed_translation_items(
            component,
            doc_now.translations,
            None if doc_base is None else doc_base.translations,
            version=manifest.version,
        )
        if not items:
            continue
        changed_total += len(items)
        selection_sha256 = translation_selection_sha256(items)
        translation_sha256 = __import__("hashlib").sha256(current_bytes).hexdigest()
        canonical_items = [
            build_translation_item(
                version=manifest.version,
                component=component,
                ordinal=ordinal,
                entry=entry,
            )
            for ordinal, entry in enumerate(doc_now.translations)
        ]
        inventory_sha256, inventory_membership = write_translation_inventory(
            root=manifest.root,
            tool_version=TOOL_VERSION,
            version=manifest.version,
            component=component,
            translation_sha256=translation_sha256,
            items=canonical_items,
        )
        for offset, batch, character_count, oversized in partition_translation_items(
            items, max_items=batch_size, character_budget=character_budget
        ):
            payload = _translation_bundle_payload(
                tool_version=TOOL_VERSION,
                version=manifest.version,
                manifest_sha256=manifest_sha256,
                component=component,
                translation_sha256=translation_sha256,
                offset=offset,
                total=len(items),
                batch=batch,
                character_count=character_count,
                character_budget=character_budget,
                oversized_single_item=oversized,
                policy_sha256=policy_sha256,
                inventory_sha256=inventory_sha256,
                selection_sha256=selection_sha256,
                membership=[inventory_membership[item["ordinal"]] for item in batch],
            )
            bundle_id = _bundle_id(payload)
            payload["bundle_id"] = bundle_id
            artifact_bytes = len(json_bytes(payload))
            payload_bytes = len(translation_provider_message(payload))
            relative_path = (
                Path("translations") / component / f"{bundle_id}.json"
            )
            bundle_artifacts.append((relative_path, payload))
            bundles.append(
                {
                    "bundle_id": bundle_id,
                    "schema_version": TRANSLATION_REVIEW_SCHEMA_VERSION,
                    "review_contract": TRANSLATION_REVIEW_BUNDLE_CONTRACT,
                    "channel": TRANSLATION_REVIEW_CHANNEL,
                    "kind": "translations",
                    "component": component,
                    "offset": offset,
                    "count": len(batch),
                    "total": len(items),
                    "selection_sha256": selection_sha256,
                    "item_character_count": character_count,
                    "item_character_budget": character_budget,
                    "artifact_bytes": artifact_bytes,
                    "payload_bytes": payload_bytes,
                    "oversized_single_item": oversized,
                    "path": str(run_dir / relative_path),
                }
            )

    index_payload = {
        "schema_version": REVIEW_INDEX_SCHEMA_VERSION,
        "review_contract": REVIEW_INDEX_CONTRACT,
        "tool_version": TOOL_VERSION,
        "version": manifest.version,
        "manifest_sha256": manifest_sha256,
        "scope": {
            "translations": True,
            "code": False,
            "protected_sources": False,
        },
        "redacted_absolute_path_count": 0,
        "baseline": baseline,
        "baseline_tree": baseline_tree,
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
        "--character-budget",
        type=_review_character_budget,
        default=DEFAULT_TRANSLATION_CHARACTER_BUDGET,
        help=(
            "maximum summed canonical JSON characters for translation items "
            "per bundle (default: 24000); the index also records actual payload bytes"
        ),
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
            character_budget=args.character_budget,
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
