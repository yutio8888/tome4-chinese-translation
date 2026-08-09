#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classify duplicate ``(component, source, source_tag)`` runtime keys.

Buckets are defined by the sections containing each occurrence:

- A: every occurrence is in a different section;
- B: every occurrence is in the same section;
- C: occurrences span sections and at least one section contains a repeat.

Reports are written to
``.artifacts/i18n/runtime-key-classification/`` only after every declared
translation has loaded and every duplicate key has been proven to use one
runtime semantic value (target/args_order/special).
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib.config import DEFAULT_VERSION, Manifest, load_manifest  # noqa: E402
from i18nlib.errors import I18nToolError, ValidationError  # noqa: E402
from i18nlib.locale_model import LocaleDocument, LocaleLoader  # noqa: E402
from i18nlib.runtime import LuaRuntime  # noqa: E402
from i18nlib.semantics import runtime_semantic_signature  # noqa: E402


DEFAULT_OUTPUT_DIR = (
    ROOT / ".artifacts" / "i18n" / "runtime-key-classification"
)
SECTION_DISPLAY_LIMIT = 6


@dataclass(frozen=True)
class TranslationLoadFailure:
    component: str
    path: Path
    detail: str


class RuntimeKeyClassificationLoadError(ValidationError):
    def __init__(self, failures: list[TranslationLoadFailure]) -> None:
        if not failures:
            raise ValueError("translation load failures must not be empty")
        self.failures = tuple(failures)
        noun = "component" if len(failures) == 1 else "components"
        details = "\n".join(
            f"  - {failure.component}: {failure.detail}: {failure.path}"
            for failure in failures
        )
        super().__init__(
            f"{len(failures)} declared translation {noun} failed to load:\n"
            f"{details}"
        )


@dataclass(frozen=True)
class TargetConflict:
    component: str
    source: str
    source_tag: str | None
    targets: tuple[str, ...]
    semantic_values: tuple[str, ...]


class RuntimeKeyTargetConflictError(ValidationError):
    def __init__(self, conflicts: list[TargetConflict]) -> None:
        if not conflicts:
            raise ValueError("runtime-key target conflicts must not be empty")
        self.conflicts = tuple(conflicts)
        noun = "key" if len(conflicts) == 1 else "keys"
        details = "\n".join(
            "  - "
            f"({conflict.component!r}, {conflict.source!r}, "
            f"{conflict.source_tag!r}): targets={list(conflict.targets)!r}; "
            f"runtime_values={list(conflict.semantic_values)!r}"
            for conflict in conflicts
        )
        super().__init__(
            f"{len(conflicts)} duplicate runtime {noun} resolve to multiple "
            f"targets or runtime semantic values:\n{details}"
        )


def _tag_sort_key(tag: str | None) -> tuple[bool, str]:
    return (tag is not None, tag if tag is not None else "")


def _runtime_key_sort_key(
    item: tuple[
        tuple[str, str, str | None],
        list[tuple[str, Any, Any, str, str]],
    ],
) -> tuple[str, str, bool, str]:
    component, source, source_tag = item[0]
    return (component, source, *_tag_sort_key(source_tag))


def _count_sort_key(item: tuple[Any, int]) -> tuple[Any, ...]:
    key, count = item
    if key is None or isinstance(key, str):
        return (-count, *_tag_sort_key(key))
    return (-count, str(key))


def load_translation_documents(
    manifest: Manifest, loader: LocaleLoader
) -> list[tuple[str, LocaleDocument]]:
    """Load every declared translation exactly once, aggregating failures."""
    documents: list[tuple[str, LocaleDocument]] = []
    failures: list[TranslationLoadFailure] = []
    for component in manifest.components:
        if not component.translation:
            continue
        path = manifest.root / component.translation
        if not path.exists():
            failures.append(
                TranslationLoadFailure(
                    component.id, path, "missing translation file"
                )
            )
            continue
        if not path.is_file():
            failures.append(
                TranslationLoadFailure(
                    component.id,
                    path,
                    "translation path is not a regular file",
                )
            )
            continue
        try:
            document = loader.load_path(
                path, logical_path=str(component.translation)
            )
        except I18nToolError as error:
            failures.append(
                TranslationLoadFailure(
                    component.id,
                    path,
                    f"load failed ({type(error).__name__}: {error})",
                )
            )
            continue
        documents.append((component.id, document))
    if failures:
        raise RuntimeKeyClassificationLoadError(failures)
    return documents


def _directory_pattern(section: str) -> str:
    parts = section.split("/")
    return "/".join(parts[1:3]) if len(parts) >= 3 else section


def _item(
    component: str,
    source: str,
    source_tag: str | None,
    entries: list[tuple[str, Any, Any, str, str]],
    *,
    truncate_sections: bool,
) -> dict[str, object]:
    sections = sorted({section for _, _, _, _, section in entries})
    displayed_sections = (
        sections[:SECTION_DISPLAY_LIMIT] if truncate_sections else sections
    )
    return {
        "component": component,
        "source": source,
        "source_tag": source_tag,
        "count": len(entries),
        "section_count": len(sections),
        "sections": displayed_sections,
        "target": entries[0][0],
        "args_order": entries[0][1],
        "special": entries[0][2],
        "semantic_value": {
            "target": entries[0][0],
            "args_order": entries[0][1],
            "special": entries[0][2],
        },
    }


def run_runtime_key_classification(
    *,
    manifest: Manifest | None = None,
    loader: LocaleLoader | None = None,
    output_dir: Path | None = None,
) -> dict[str, object]:
    manifest = manifest or load_manifest(version=DEFAULT_VERSION)
    if loader is None:
        runtime = LuaRuntime(manifest=manifest)
        loader = LocaleLoader(runtime)

    # This must finish before report paths are created or existing reports are
    # touched. It also ensures each locale is parsed only once.
    documents = load_translation_documents(manifest, loader)

    by_key: dict[
        tuple[str, str, str | None],
        list[tuple[str, Any, Any, str, str]],
    ] = defaultdict(list)
    for component_id, document in documents:
        for record in document.translations:
            source = record.get("source") or ""
            if not source:
                continue
            target = record.get("target") or ""
            section = record.get("section") or ""
            semantic_signature = runtime_semantic_signature(
                record,
                label=(
                    f"translation {document.logical_path}:"
                    f"{record.get('line', '?')}"
                ),
            )
            by_key[(component_id, source, record.get("source_tag"))].append(
                (
                    target,
                    record.get("args_order"),
                    record.get("special"),
                    semantic_signature,
                    section,
                )
            )

    duplicate_items = sorted(
        (
            (runtime_key, entries)
            for runtime_key, entries in by_key.items()
            if len(entries) > 1
        ),
        key=_runtime_key_sort_key,
    )

    conflicts: list[TargetConflict] = []
    for (component, source, source_tag), entries in duplicate_items:
        targets = tuple(sorted({entry[0] for entry in entries}))
        semantic_values = tuple(sorted({entry[3] for entry in entries}))
        if len(semantic_values) > 1:
            conflicts.append(
                TargetConflict(
                    component,
                    source,
                    source_tag,
                    targets,
                    semantic_values,
                )
            )
    if conflicts:
        raise RuntimeKeyTargetConflictError(conflicts)

    bucket_a: list[dict[str, object]] = []
    bucket_b: list[dict[str, object]] = []
    bucket_c: list[dict[str, object]] = []
    bucket_a_full_sections: list[tuple[str, ...]] = []
    for (component, source, source_tag), entries in duplicate_items:
        full_sections = tuple(sorted({entry[4] for entry in entries}))
        if len(full_sections) == len(entries):
            bucket_a.append(
                _item(
                    component,
                    source,
                    source_tag,
                    entries,
                    truncate_sections=True,
                )
            )
            bucket_a_full_sections.append(full_sections)
        elif len(full_sections) == 1:
            bucket_b.append(
                _item(
                    component,
                    source,
                    source_tag,
                    entries,
                    truncate_sections=False,
                )
            )
        else:
            bucket_c.append(
                _item(
                    component,
                    source,
                    source_tag,
                    entries,
                    truncate_sections=False,
                )
            )

    tag_distribution = Counter(item["source_tag"] for item in bucket_a)
    sorted_tag_distribution = dict(
        sorted(tag_distribution.items(), key=_count_sort_key)
    )

    # Deliberately use the complete section sets, not the six-entry display
    # projection stored in bucket A's JSON items.
    directory_distribution: Counter[str] = Counter()
    for sections in bucket_a_full_sections:
        for section in sections:
            directory_distribution[_directory_pattern(section)] += 1
    sorted_directory_distribution = dict(
        sorted(directory_distribution.items(), key=_count_sort_key)[:15]
    )

    report: dict[str, object] = {
        "total_duplicate_keys": len(duplicate_items),
        "all_duplicate_targets_identical": True,
        "all_duplicate_runtime_values_identical": True,
        "bucket_counts": {
            "A": len(bucket_a),
            "B": len(bucket_b),
            "C": len(bucket_c),
        },
        # Keep the original A/C field names for report consumers.
        "bucket_a_cross_file": bucket_a,
        "bucket_b_same_file_redundant": bucket_b,
        "bucket_c_same_file_mixed": bucket_c,
        "bucket_a_tag_distribution": sorted_tag_distribution,
        "bucket_a_dir_distribution": sorted_directory_distribution,
    }

    markdown = [
        "# 重复运行键分类报告",
        "",
        f"总重复键：{len(duplicate_items)}"
        "（全部运行时语义值相同：target/args_order/special；"
        "无运行时覆盖差异）",
        "",
        f"## 桶 A：所有 occurrence 分属不同 section（{len(bucket_a)}）",
        "",
        "各 section 独立声明同键同运行时值，未发现 section 内重复。",
        "",
        "tag 分布："
        + ", ".join(
            f"{tag}={count}"
            for tag, count in sorted_tag_distribution.items()
        ),
        "",
        "目录模式分布："
        + ", ".join(
            f"{directory}={count}"
            for directory, count in sorted_directory_distribution.items()
        ),
        "",
        f"## 桶 B：全部 occurrence 位于同一 section（{len(bucket_b)}）",
        "",
        "同一 section 内重复声明同键同运行时值，可人工确认是否合并：",
        "",
    ]
    for item in sorted(bucket_b, key=lambda value: (-value["count"], value["component"], value["source"], *_tag_sort_key(value["source_tag"]))):
        markdown.append(
            f"- [{item['component']}] ({item['count']}) "
            f"`{str(item['source'])[:50]}` [{item['source_tag']}] "
            f"section: {item['sections'][0]!r}"
        )
    markdown.extend(
        [
            "",
            f"## 桶 C：跨 section 且至少一个 section 内重复（{len(bucket_c)}）",
            "",
            "同时存在跨 section 声明和 section 内重复，需人工逐条确认：",
            "",
        ]
    )
    for item in sorted(bucket_c, key=lambda value: (-value["count"], value["component"], value["source"], *_tag_sort_key(value["source_tag"]))):
        markdown.append(
            f"- [{item['component']}] ({item['count']}) "
            f"`{str(item['source'])[:50]}` [{item['source_tag']}] "
            f"sections: {item['sections'][:4]}"
        )

    output_dir = output_dir or DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "classification.json"
    markdown_path = output_dir / "classification.md"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    markdown_path.write_text("\n".join(markdown) + "\n", encoding="utf-8")

    print(f"duplicate keys: {len(duplicate_items)}")
    print(f"桶 A 不同 section: {len(bucket_a)}")
    print(f"桶 B 同一 section: {len(bucket_b)}")
    print(f"桶 C 混合 section: {len(bucket_c)}")
    print("桶 A tag 分布:", sorted_tag_distribution)
    print("桶 A 目录模式分布:", sorted_directory_distribution)
    print("report written:", output_dir)
    return report


def main(
    argv: list[str] | None = None,
    *,
    manifest: Manifest | None = None,
    loader: LocaleLoader | None = None,
    output_dir: Path | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="report output directory",
    )

    signal.alarm(300)
    try:
        args = parser.parse_args(argv)
        try:
            run_runtime_key_classification(
                manifest=manifest,
                loader=loader,
                output_dir=output_dir or Path(args.out_dir),
            )
        except I18nToolError as error:
            print(f"runtime-key classification failed: {error}", file=sys.stderr)
            return error.exit_code
        return 0
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
