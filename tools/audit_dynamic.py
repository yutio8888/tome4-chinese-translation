#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""术语表动态校对审计：术语 vs 30,170 条规范译文。
- S2.1 术语使用率：preferred 术语的 (source, source_tag) 在对应 scope 组件译文中是否存在、target 是否一致
- S2.2 高频未录候选：译文中高复用英文 source 未收录术语表
- S2.3 译文多译：同一英文 source 在译文中出现多译但术语表未记录语境区分
输出 JSON + MD 到 .artifacts/i18n/terminology-audit/。"""
from __future__ import annotations

import csv
import json
import signal
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from i18nlib.config import DEFAULT_VERSION, Manifest, load_manifest  # noqa: E402
from i18nlib.errors import I18nToolError, ValidationError  # noqa: E402
from i18nlib.lint import (  # noqa: E402
    TERMINOLOGY_FIELDS,
    TERMINOLOGY_REQUIRED_FIELDS,
)
from i18nlib.locale_model import LocaleDocument, LocaleLoader  # noqa: E402
from i18nlib.runtime import LuaRuntime  # noqa: E402
from i18nlib.workset import _scope_matches, _source_tag_matches  # noqa: E402

OUT = ROOT / ".artifacts/i18n/terminology-audit"


@dataclass(frozen=True)
class TranslationLoadFailure:
    component: str
    path: Path
    detail: str


class DynamicAuditLoadError(ValidationError):
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
            f"{len(failures)} declared translation {noun} failed to load:\n{details}"
        )


def _tag_sort_key(tag: str | None) -> tuple[bool, str]:
    return (tag is not None, tag if tag is not None else "")


def _markdown_tag(tag: str | None) -> str:
    if tag is None:
        return "<nil>"
    if tag == "":
        return '""'
    return tag


def load_translation_documents(
    manifest: Manifest, loader: LocaleLoader
) -> dict[str, LocaleDocument]:
    """Load every declared translation before allowing the audit to proceed."""
    docs: dict[str, LocaleDocument] = {}
    failures: list[TranslationLoadFailure] = []
    for comp in manifest.components:
        if not comp.translation:
            continue
        path = manifest.root / comp.translation
        if not path.is_file():
            failures.append(
                TranslationLoadFailure(comp.id, path, "missing translation file")
            )
            continue
        try:
            docs[comp.id] = loader.load_path(
                path, logical_path=str(comp.translation)
            )
        except I18nToolError as exc:
            failures.append(
                TranslationLoadFailure(
                    comp.id,
                    path,
                    f"load failed ({type(exc).__name__}: {exc})",
                )
            )
    if failures:
        raise DynamicAuditLoadError(failures)
    return docs


def load_terminology_rows(path: Path) -> list[dict[str, object]]:
    """Read and structurally validate terminology without changing it."""
    rows: list[dict[str, object]] = []
    reader: csv.DictReader[str] | None = None
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t", strict=True)
            fieldnames = tuple(reader.fieldnames or ())
            if fieldnames != TERMINOLOGY_FIELDS:
                raise ValidationError(
                    f"invalid terminology TSV: {path}: line 1: "
                    f"expected fields {TERMINOLOGY_FIELDS!r}, got {fieldnames!r}"
                )
            for row in reader:
                line = max(reader.line_num, 2)
                missing = [
                    field
                    for field in TERMINOLOGY_REQUIRED_FIELDS
                    if field not in row or row[field] is None
                ]
                if missing:
                    raise ValidationError(
                        f"invalid terminology TSV: {path}: line {line}: "
                        f"missing required fields: {', '.join(missing)}"
                    )
                empty = [
                    field
                    for field in TERMINOLOGY_REQUIRED_FIELDS
                    if not row[field].strip()
                ]
                if empty:
                    raise ValidationError(
                        f"invalid terminology TSV: {path}: line {line}: "
                        f"empty required fields: {', '.join(empty)}"
                    )
                validated_row: dict[str, object] = dict(row)
                validated_row["_line"] = line
                rows.append(validated_row)
    except ValidationError:
        raise
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        line = max(reader.line_num if reader is not None else 1, 1)
        raise ValidationError(
            f"invalid terminology TSV: {path}: line {line}: {error}"
        ) from error
    return rows


def run_dynamic_audit(
    *,
    manifest: Manifest | None = None,
    loader: LocaleLoader | None = None,
    terminology_path: Path | None = None,
    output_dir: Path | None = None,
) -> dict[str, object]:
    manifest = manifest or load_manifest(version=DEFAULT_VERSION)
    if terminology_path is None:
        terminology_path = manifest.root / manifest.terminology
    if output_dir is None:
        output_dir = manifest.root / ".artifacts/i18n/terminology-audit"

    # 术语是纯文本输入，必须在创建 Lua runtime 或加载任何译文前完成预检。
    rows = load_terminology_rows(terminology_path)

    if loader is None:
        runtime = LuaRuntime(manifest=manifest)
        loader = LocaleLoader(runtime)

    # 全量加载是发布报告的前置条件，任何失败都先汇总并终止。
    docs = load_translation_documents(manifest, loader)

    # 聚合译文条目
    entries = []  # (component, source, source_tag, target)
    by_source = defaultdict(list)  # source -> [(comp, tag, target)]
    for comp, doc in docs.items():
        for rec in doc.translations:
            src = rec.get("source") or ""
            tgt = rec.get("target") or ""
            tag = rec.get("source_tag")
            if not src or not tgt:
                continue
            entries.append((comp, src, tag, tgt))
            by_source[src].append((comp, tag, tgt))

    terminology_targets_by_source = defaultdict(set)
    for row in rows:
        terminology_targets_by_source[row["source"]].add(row["target"])
    term_sources = set(terminology_targets_by_source)

    report = {"entries": len(entries), "components": sorted(docs.keys())}

    # ---------- S2.1 preferred 术语使用率 ----------
    unused = []
    mismatch = []
    for r in rows:
        if r["status"] != "preferred":
            continue
        source_entries = by_source.get(r["source"], ())
        # 精确匹配 (source, source_tag)，仅扫描同 source 的索引候选。
        hits = [
            entry
            for entry in source_entries
            if _scope_matches(r["scope"], entry[0])
            and _source_tag_matches(r["source_tag"], entry[1])
        ]
        if not hits:
            # source 都不存在：术语可能过时
            unused.append({"line": r["_line"], "source": r["source"], "target": r["target"],
                           "category": r["category"], "tag": r["source_tag"], "scope": r["scope"]})
            continue
        # target 一致性：术语 target 是否出现在译文 target 中（允许术语是条目 target 的子串或相等）
        tgt_set = {e[2] for e in hits}
        term_t = r["target"]
        if not any(term_t == t or (len(term_t) >= 4 and term_t in t) for t in tgt_set):
            mismatch.append({"line": r["_line"], "source": r["source"], "target": term_t,
                             "category": r["category"], "tag": r["source_tag"], "scope": r["scope"],
                             "found_targets": sorted(tgt_set)[:8]})
    report["s2_1"] = {
        "unused_count": len(unused), "unused": unused,
        "mismatch_count": len(mismatch), "mismatch": mismatch,
    }

    # ---------- S2.2 高频未录候选 ----------
    src_counts = Counter(e[1] for e in entries)
    candidates = []
    for src, n in src_counts.most_common():
        if n < 15:
            break
        if src in term_sources:
            continue
        if len(src) > 60 or len(src) < 3:
            continue
        tags = sorted(
            {source_tag for _, source_tag, _ in by_source[src]},
            key=_tag_sort_key,
        )[:4]
        targets = sorted({target for _, _, target in by_source[src]})[:3]
        candidates.append(
            {
                "source": src,
                "count": n,
                "tags": tags,
                "targets": targets,
            }
        )
    report["s2_2"] = {"count": len(candidates), "items": candidates}

    # ---------- S2.3 译文多译（术语表未记录） ----------
    multi = []
    for src, es in sorted(by_source.items()):
        variants = {}
        for comp, tag, tgt in es:
            variants.setdefault(tgt, []).append((comp, tag))
        if len(variants) >= 2:
            # 过滤：长句、数字/占位符为主
            if len(src) > 50:
                continue
            terminology_targets = terminology_targets_by_source.get(src, set())
            unrecorded_targets = set(variants) - terminology_targets
            if not unrecorded_targets:
                continue
            multi.append({
                "source": src, "count": len(es),
                "terminology_targets": sorted(terminology_targets),
                "unrecorded_targets": sorted(unrecorded_targets),
                "variants": [{"target": t, "places": sorted({f"{c}" for c, _ in v})[:6],
                              "tags": sorted({tag for _, tag in v}, key=_tag_sort_key)[:4]}
                             for t, v in sorted(variants.items())],
            })
    # 只保留最显著的前 200 条
    multi.sort(key=lambda x: -x["count"])
    report["s2_3"] = {"count": len(multi), "items": multi[:200]}

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "audit_dynamic.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    md = ["# 术语表动态校对审计报告", "",
          f"译文条目总数：{report['entries']}；组件：{', '.join(report['components'])}", "",
          "## S2.1 preferred 术语使用率", "",
          f"- 术语 source 在对应组件译文中完全不存在（可能过时）：{len(unused)} 条", ""]
    for it in unused:
        md.append(f"  - L{it['line']} `{it['source']}` → `{it['target']}` [{it['category']} @ {it['scope']}]")
    md += ["", f"- source 存在但译文 target 与术语 target 不一致：{len(mismatch)} 条", ""]
    for it in mismatch:
        md.append(f"  - L{it['line']} `{it['source']}` → 术语 `{it['target']}`；译文：{' / '.join(it['found_targets'][:4])}")
    md += ["", "## S2.2 高频未录候选（译文出现 ≥15 次）", f"共 {len(candidates)} 条", ""]
    for it in candidates:
        md.append(f"- ({it['count']}) `{it['source']}` → {' / '.join(it['targets'][:3])}")
    md += ["", "## S2.3 译文多译（术语表未记录语境区分）", f"共 {len(multi)} 条（显示前 200）", ""]
    for it in multi[:200]:
        vs = "；".join(
            f"`{v['target']}`[{','.join(_markdown_tag(tag) for tag in v['tags'])}]"
            for v in it["variants"]
        )
        md.append(f"- ({it['count']}) `{it['source']}` → {vs}")
    (output_dir / "audit_dynamic.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("dynamic audit done:", report["entries"], "entries")
    print("  unused:", len(unused), "| mismatch:", len(mismatch), "| candidates:", len(candidates), "| multi:", len(multi))
    return report


def main(
    *,
    manifest: Manifest | None = None,
    loader: LocaleLoader | None = None,
    terminology_path: Path | None = None,
    output_dir: Path | None = None,
) -> int:
    signal.alarm(300)
    try:
        run_dynamic_audit(
            manifest=manifest,
            loader=loader,
            terminology_path=terminology_path,
            output_dir=output_dir,
        )
    except I18nToolError as error:
        print(f"dynamic audit failed: {error}", file=sys.stderr)
        return error.exit_code
    finally:
        signal.alarm(0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
