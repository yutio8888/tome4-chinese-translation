#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨组件同 (source, source_tag) 多运行时值扫描。

ToME4 翻译运行时按 (component, source, source_tag) 键匹配；同键多条目在
引擎加载多个 locale 文件时会发生覆盖（后加载者胜出）。组件内同键不同
运行时值已由 lint 的 runtime-collision（error）覆盖；本脚本补充扫描
**跨组件**同键多值，输出 JSON + Markdown 报告，供维护
docs/runtime-key-collisions.md 档案。

用法：python3 -B tools/scan_runtime_collisions.py [--out-dir .artifacts/i18n]
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from i18nlib.config import DEFAULT_VERSION, Manifest, load_manifest  # noqa: E402
from i18nlib.errors import I18nToolError, ValidationError  # noqa: E402
from i18nlib.locale_model import LocaleDocument, LocaleLoader  # noqa: E402
from i18nlib.runtime import LuaRuntime  # noqa: E402
from i18nlib.semantics import runtime_semantic_signature  # noqa: E402


@dataclass(frozen=True)
class TranslationLoadFailure:
    component: str
    path: Path
    detail: str


class RuntimeCollisionLoadError(ValidationError):
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


def load_translation_documents(
    manifest: Manifest, loader: LocaleLoader
) -> list[tuple[str, LocaleDocument]]:
    """Load every declared translation before allowing reports to be written."""
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
                    component.id, path, "translation path is not a regular file"
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
        raise RuntimeCollisionLoadError(failures)
    return documents


def run_runtime_collision_scan(
    *,
    manifest: Manifest | None = None,
    loader: LocaleLoader | None = None,
    output_dir: Path | None = None,
) -> dict[str, object]:
    manifest = manifest or load_manifest(version=DEFAULT_VERSION)
    if loader is None:
        runtime = LuaRuntime(manifest=manifest)
        loader = LocaleLoader(runtime)

    # Fail closed before creating or replacing either report.
    documents = load_translation_documents(manifest, loader)

    scanned_translations = 0
    by_key: dict[tuple[str, str | None], list[dict[str, object]]] = defaultdict(list)
    for component_id, document in documents:
        translations = document.translations
        scanned_translations += len(translations)
        for record in translations:
            source = record.get("source") or ""
            target = record.get("target") or ""
            semantic_target = record.get("target")
            tag = record.get("source_tag")
            semantic_signature = runtime_semantic_signature(
                record,
                label=(
                    f"translation {document.logical_path}:"
                    f"{record.get('line', '?')}"
                ),
            )
            by_key[(source, tag)].append(
                {
                    "component": component_id,
                    "target": target,
                    "semantic_target": semantic_target,
                    "args_order": record.get("args_order"),
                    "special": record.get("special"),
                    "semantic_signature": semantic_signature,
                    "section": record.get("section") or "",
                    "line": record.get("line"),
                }
            )

    collisions = []
    sorted_keys = sorted(
        by_key.items(),
        key=lambda item: (
            item[0][0],
            item[0][1] is not None,
            item[0][1] if item[0][1] is not None else "",
        ),
    )
    for (source, tag), entries in sorted_keys:
        components = {entry["component"] for entry in entries}
        targets = {entry["target"] for entry in entries}
        semantic_signatures = {
            entry["semantic_signature"] for entry in entries
        }
        if len(components) > 1 and len(semantic_signatures) > 1:
            variants: dict[object, set[object]] = {}
            semantic_variants: dict[object, dict[str, dict[str, object]]] = {}
            for entry in entries:
                variants.setdefault(entry["component"], set()).add(entry["target"])
                value = {
                    "target": entry["semantic_target"],
                    "args_order": entry["args_order"],
                    "special": entry["special"],
                }
                semantic_variants.setdefault(entry["component"], {})[
                    str(entry["semantic_signature"])
                ] = value
            values_by_signature: dict[str, dict[str, object]] = {}
            for component_values in semantic_variants.values():
                values_by_signature.update(component_values)
            collisions.append(
                {
                    "source": source,
                    "source_tag": tag,
                    "entry_count": len(entries),
                    "components": sorted(components),
                    "target_count": len(targets),
                    "targets": sorted(targets),
                    "semantic_value_count": len(semantic_signatures),
                    "semantic_values": [
                        {
                            **values_by_signature[signature],
                            "signature": signature,
                        }
                        for signature in sorted(values_by_signature)
                    ],
                    "variants": {
                        component: sorted(values)
                        for component, values in sorted(variants.items())
                    },
                    "semantic_variants": {
                        component: [
                            {**values[signature], "signature": signature}
                            for signature in sorted(values)
                        ]
                        for component, values in sorted(
                            semantic_variants.items()
                        )
                    },
                }
            )

    report = {
        "scanned_translations": scanned_translations,
        "collision_count": len(collisions),
        "collisions": collisions,
    }
    output_dir = output_dir or ROOT / ".artifacts" / "i18n"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "runtime-collisions.json"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    md = [
        "# 跨组件同 TAG 多运行时值扫描报告",
        "",
        f"扫描时间：{__import__('datetime').datetime.now().isoformat(timespec='seconds')}",
        f"译文条目：{report['scanned_translations']}；冲突：{report['collision_count']} 条",
        "",
    ]
    for item in collisions:
        md.append(
            f"## [{item['source_tag']}] {item['source']!r}"
            f"（{item['entry_count']} 条）"
        )
        for component, values_for_component in item[
            "semantic_variants"
        ].items():
            for value in values_for_component:
                displayed_value = {
                    field: value[field]
                    for field in ("target", "args_order", "special")
                }
                md.append(
                    f"- {component}："
                    + json.dumps(
                        displayed_value,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                        allow_nan=False,
                    )
                )
        md.append("")
    md_path = output_dir / "runtime-collisions.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"runtime collisions: {report['collision_count']}")
    print(f"  json: {json_path}")
    print(f"  md:   {md_path}")
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
        default=str(ROOT / ".artifacts" / "i18n"),
        help="report output directory",
    )

    signal.alarm(300)
    try:
        args = parser.parse_args(argv)
        try:
            report = run_runtime_collision_scan(
                manifest=manifest,
                loader=loader,
                output_dir=output_dir or Path(args.out_dir),
            )
        except I18nToolError as error:
            print(f"runtime collision scan failed: {error}", file=sys.stderr)
            return error.exit_code
        return 1 if report["collision_count"] else 0
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
