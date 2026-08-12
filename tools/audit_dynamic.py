#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""术语表动态校对审计：术语 vs 30,308 条规范译文。
- S2.1 术语使用率：preferred 术语的 (source, source_tag) 在对应 scope 组件译文中是否存在、target 是否一致
- S2.2 高频未录候选：译文中高复用英文 source 未收录术语表
- S2.3 译文多译：同一英文 source 在译文中出现多译但术语表未记录语境区分
- r2 inventory：第二轮术语审核的候选全集、覆盖率与自动排除生成器（见 docs/terminology-review-round-2.md）
输出 JSON + MD 到 .artifacts/i18n/terminology-audit/，inventory 到 .artifacts/i18n/terminology-review-r2/。"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import signal
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from i18nlib import TOOL_VERSION  # noqa: E402
from i18nlib import terminology as terminology_store  # noqa: E402
from i18nlib.config import DEFAULT_VERSION, Manifest, load_manifest  # noqa: E402
from i18nlib.errors import I18nToolError, ValidationError  # noqa: E402
from i18nlib.lint import (  # noqa: E402
    TERMINOLOGY_FIELDS,
    TERMINOLOGY_REQUIRED_FIELDS,
)
from i18nlib.locale_model import LocaleDocument, LocaleLoader  # noqa: E402
from i18nlib.runtime import LuaRuntime  # noqa: E402
from i18nlib.workset import _scope_matches, _source_tag_matches  # noqa: E402

# ---------- r2 术语审核：候选全集与覆盖率生成器 ----------
# 契约见 docs/terminology-review-round-2.md 2.1/2.2/3/6/7.1。

INVENTORY_SCHEMA_VERSION = 1
S2_2_THRESHOLD = 15
AUTO_EXCLUSION_RULE_ID = "B-AUTO-1"
CHAT_TAG_PREFIX = "chat_"
PROJECTION_SCHEMA_VERSION = 1
# 机制关键标签：玩家直接可见的机制/成就/叙事标签，不参与自动排除（3.B）
MECHANISM_KEY_TAGS = frozenset({"talent name", "achievement name", "newLore category"})

# A 类：必须穷举登记的封闭词表（3.A）
A_CLASS_TAGS = frozenset(
    {
        "damage type",
        "effect subtype",
        "stat name",
        "stat short_name",
        "talent category",
        "talent type",
        "birth descriptor name",
        "faction name",
        "entity type",
        "entity subtype",
    }
)
# B 类：必须审核、按复用价值决定是否登记的开放词表（3.B）
B_CLASS_TAGS = frozenset(
    {
        "talent name",
        "entity name",
        "achievement name",
        "newLore category",
        "entity short_name",
        "ingredient name",
        "ingredient type",
        "gem name",
        "gem subtype",
        "alchemist gem",
        "birth facial category",
        "init.lua load_tips",
        "calendar allied",
        "calendar dwarf",
        "calendar orc",
        "say",
        "saySimple",
        "chat",
        "delayedLogMessage",
        "ft-illusory-castle branch name",
        "save name",
        "quest_lumberjack",
        "dialog_portal",
        "entity keyword",  # provisional：疑似源码注册封闭枚举，待源码核验后可能移入 A
    }
)
PROVISIONAL_CLASS_TAGS = frozenset({"entity keyword"})
# C 类：不生成候选单元，仅治理已登记行（3.A 运行时标签边界）
C_CLASS_TAGS = frozenset(
    {
        "_t",
        "tformat",
        "log",
        "logSeen",
        "logPlayer",
        "logCombat",
        "logMessage",
        "nil",
        "floorEffect desc",
        "entity on slot",
        "entity combat talented",
        "init.lua long_name",
        "init.lua description",
        "easing",
    }
)

BATCH_BY_TAG = {
    "damage type": "P0",
    "effect subtype": "P0",
    "stat name": "P0",
    "stat short_name": "P0",
    "talent category": "P1",
    "talent type": "P1",
    "birth descriptor name": "P1",
    "faction name": "P1",
    "entity type": "P1",
    "entity keyword": "P1",
    "talent name": "P2",
    "entity name": "P3",
    "entity subtype": "P3",
    "entity short_name": "P3",
    "ingredient name": "P3",
    "ingredient type": "P3",
    "gem name": "P3",
    "gem subtype": "P3",
    "alchemist gem": "P3",
    "birth facial category": "P3",
    "achievement name": "P4",
    "newLore category": "P4",
    "init.lua load_tips": "P4",
    "calendar allied": "P4",
    "calendar dwarf": "P4",
    "calendar orc": "P4",
    "say": "P4",
    "saySimple": "P4",
    "chat": "P4",
    "delayedLogMessage": "P4",
    "ft-illusory-castle branch name": "P4",
    "save name": "P4",
    "quest_lumberjack": "P4",
    "dialog_portal": "P4",
}

# ---------- 长文本投影（5.3 高精度低召回策略） ----------

# 英文短语最短长度；中文译法最短长度
PROJECTION_MIN_TERM_LEN = 4
PROJECTION_MIN_TARGET_LEN = 2
# 运行时键空间不参与投影（键名不是自然语言）
PROJECTION_EXCLUDED_ENTRY_TAGS = frozenset({"_t"})
# 通用词黑名单：投影命中但几乎不携带术语信息，先排除控制噪音
PROJECTION_BLACKLIST = frozenset(
    {
        "master",
        "wall",
        "fire",
        "light",
        "dark",
        "cold",
        "hot",
        "slow",
        "fast",
        "strong",
        "weak",
        "small",
        "large",
        "heavy",
        "light",
        "power",
        "speed",
        "armor",
        "damage",
        "health",
        "mana",
        "gold",
        "level",
        "range",
        "powerful",
        "greater",
        "lesser",
    }
)

_MARKUP_RE = re.compile(r"#[^#\n]+#|@[^@\n]+@")


def _markup_stripped(text: str) -> str:
    return _MARKUP_RE.sub("", text)


def _term_pattern(term: str) -> tuple[re.Pattern[str], str]:
    """按术语大小写特征生成匹配模式。

    首字母大写（专名特征）用大小写敏感匹配，其余 IGNORECASE。
    """
    if term[:1].isupper():
        return re.compile(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])"), "case-sensitive"
    return re.compile(
        rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])", re.IGNORECASE
    ), "ignorecase"


def _projection_term_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """投影对象：仅 preferred，且满足长度与黑名单门槛。"""
    terms: list[dict[str, object]] = []
    for row in rows:
        if row["status"] != "preferred":
            continue
        src = row["source"]
        tgt = row["target"]
        if len(src) < PROJECTION_MIN_TERM_LEN:
            continue
        if len(tgt) < PROJECTION_MIN_TARGET_LEN:
            continue
        if src.lower() in PROJECTION_BLACKLIST:
            continue
        terms.append(row)
    return terms


def run_projection(
    *,
    docs: dict[str, LocaleDocument],
    rows: list[dict[str, object]],
) -> dict[str, object]:
    """长文本投影：术语短语在英文 source 中出现时，中文 target 是否采用规范译法。

    输出全部为“候选不一致”进入 triage，不直接成为 finding；只有经源码核验的
    确认漂移才进入 findings（docs/terminology-review-round-2.md 5.3）。
    """
    terms = _projection_term_rows(rows)
    patterns: list[tuple[re.Pattern[str], dict[str, object], str]] = []
    for term in terms:
        pattern, mode = _term_pattern(term["source"])
        patterns.append((pattern, term, mode))

    candidates: list[dict[str, object]] = []
    matched_count = 0
    scanned = 0
    by_tag: Counter = Counter()
    for comp, doc in docs.items():
        for rec in doc.translations:
            src = rec.get("source") or ""
            if not src:
                continue
            tag = rec.get("source_tag")
            if tag in PROJECTION_EXCLUDED_ENTRY_TAGS:
                continue
            scanned += 1
            lowered = src.lower()
            tgt = rec.get("target") or ""
            stripped_tgt = _markup_stripped(tgt)
            for pattern, term, _mode in patterns:
                term_src = term["source"]
                if term_src.lower() not in lowered:
                    continue
                match = pattern.search(src)
                if match is None:
                    continue
                matched_count += 1
                term_tgt = term["target"]
                if len(term_tgt) >= PROJECTION_MIN_TARGET_LEN and term_tgt in stripped_tgt:
                    continue  # 一致，不算候选
                candidates.append(
                    {
                        "component": comp,
                        "section": rec.get("section") or "",
                        "line": rec.get("line"),
                        "entry_source": src,
                        "entry_target": tgt,
                        "term_source": term_src,
                        "term_target": term_tgt,
                        "term_line": term["_line"],
                        "term_scope": term["scope"],
                        "term_category": term["category"],
                        "term_domain": term["domain"],
                        "matched": match.group(0),
                    }
                )
                by_tag[term["source_tag"]] += 1
    candidates.sort(
        key=lambda c: (
            c["component"],
            c["section"],
            c["line"] if isinstance(c["line"], int) else 0,
        )
    )
    return {
        "schema_version": PROJECTION_SCHEMA_VERSION,
        "terms": len(terms),
        "scanned_entries": scanned,
        "matched_occurrences": matched_count,
        "candidate_count": len(candidates),
        "candidates_by_term_tag": dict(by_tag),
        "candidates": candidates,
    }


def write_projection_report(
    report: dict[str, object], output_dir: Path
) -> None:
    """写 projection-candidates.json 与 md 摘要。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "projection-candidates.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    candidates = report["candidates"]
    md = [
        "# 长文本投影候选（triage）",
        "",
        f"术语：{report['terms']} 条 preferred；扫描条目：{report['scanned_entries']}；"
        f"命中：{report['matched_occurrences']}；候选不一致：{report['candidate_count']}",
        "",
        "候选不直接成为 finding；按 5.3 分类：确认漂移 / 合法语境差异 / 误匹配 / 待源码核验。",
        "",
        f"按术语标签：{json.dumps(report['candidates_by_term_tag'], ensure_ascii=False)}",
        "",
        "## 候选（前 100）",
        "",
    ]
    for item in candidates[:100]:
        md.append(
            f"- [{item['component']}] L{item['line']} `{item['matched']}` "
            f"（术语 `{item['term_source']}`→`{item['term_target']}`）\n"
            f"  source: {item['entry_source'][:120]}\n"
            f"  target: {item['entry_target'][:120]}"
        )
    (output_dir / "projection-candidates.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8"
    )

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
    """Read and structurally validate terminology without changing it.

    Delegates to the shared terminology store loader, which accepts either a
    single TSV file or the domain directory (``terminology/``).
    """
    return terminology_store.load_terminology_rows(path)


def _tag_repr(tag: object) -> str:
    return "<null>" if tag is None else str(tag)


def _unit_class_and_batch(tag: object) -> tuple[str, str, bool]:
    """按 source_tag 判定候选类别、批次与 provisional 标记。"""
    trepr = _tag_repr(tag)
    if trepr in A_CLASS_TAGS:
        return "A", BATCH_BY_TAG[trepr], False
    if trepr in B_CLASS_TAGS or trepr.startswith(CHAT_TAG_PREFIX):
        return (
            "B",
            BATCH_BY_TAG.get(trepr, "P4"),
            trepr in PROVISIONAL_CLASS_TAGS,
        )
    if trepr in C_CLASS_TAGS or trepr == "<null>":
        return "C", "P4", False
    return "UNCLASSIFIED", "P4", False


def _row_batch(tag: str) -> str:
    """TSV 行按标签归属批次（用于现有行复核分母）。"""
    if tag in BATCH_BY_TAG:
        return BATCH_BY_TAG[tag]
    if tag in C_CLASS_TAGS or tag.startswith(CHAT_TAG_PREFIX):
        return "P4"
    return "UNASSIGNED"


def build_candidate_units(
    docs: dict[str, LocaleDocument],
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    """从已加载译文构建 (组件, source, source_tag) 候选单元与跨语料索引。

    单元去重口径固定为 (component, source, source_tag)；corpus 索引覆盖全部
    译文条目（含 C 类标签），用于跨组件、频次与词族变体判定。
    """
    units_by_key: dict[tuple[str, str, str], dict[str, object]] = {}
    corpus: dict[str, dict[str, object]] = defaultdict(
        lambda: {
            "occurrences": 0,
            "components": set(),
            "tags": set(),
            "targets": set(),
        }
    )
    for comp, doc in docs.items():
        for rec in doc.translations:
            src = rec.get("source") or ""
            if not src:
                continue
            tag = rec.get("source_tag")
            tgt = rec.get("target") or ""
            section = rec.get("section") or ""
            info = corpus[src]
            info["occurrences"] += 1
            info["components"].add(comp)
            if tag is not None:
                info["tags"].add(tag)
            if tgt:
                info["targets"].add(tgt)
            key = (comp, src, _tag_repr(tag))
            unit = units_by_key.get(key)
            if unit is None:
                unit = {
                    "component": comp,
                    "source": src,
                    "source_tag": tag,
                    "occurrences": 0,
                    "sections": set(),
                    "targets": set(),
                }
                units_by_key[key] = unit
            unit["occurrences"] += 1
            if section:
                unit["sections"].add(section)
            if tgt:
                unit["targets"].add(tgt)

    sources = list(corpus)
    lowered: dict[str, list[str]] = defaultdict(list)
    for src in sources:
        lowered[src.lower()].append(src)
    lowered_set = set(lowered)
    for src in sources:
        info = corpus[src]
        info["case_variants"] = len(lowered[src.lower()]) - 1
        base = src.lower()
        info["plural_variants"] = sum(
            candidate in lowered_set for candidate in (base + "s", base + "es")
        )
        info["components"] = sorted(info["components"])
        info["tags"] = sorted(info["tags"], key=_tag_sort_key)
        info["targets"] = sorted(info["targets"])

    units: list[dict[str, object]] = []
    for unit in units_by_key.values():
        unit["sections"] = sorted(unit["sections"])
        unit["targets"] = sorted(unit["targets"])
        unit["cross_component_count"] = len(corpus[unit["source"]]["components"])
        units.append(unit)
    units.sort(
        key=lambda unit: (unit["component"], _tag_repr(unit["source_tag"]), unit["source"])
    )
    return units, corpus


def annotate_units(
    units: list[dict[str, object]],
    corpus: dict[str, dict[str, object]],
    rows: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    """为候选单元填充类别、批次、登记状态与自动排除（B-AUTO-1）。

    登记判定复用 workset._scope_matches / _source_tag_matches 语义；
    自动排除规则见 docs/terminology-review-round-2.md 3.B。
    """
    row_index: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        row_index[row["source"]].append(row)

    a_class_sources: set[str] = set()
    for unit in units:
        cls, batch, provisional = _unit_class_and_batch(unit["source_tag"])
        unit["class"] = cls
        unit["class_provisional"] = provisional
        unit["batch"] = batch
        if cls == "A":
            a_class_sources.add(unit["source"])

    for unit in units:
        src = unit["source"]
        info = corpus[src]
        matched = [
            row
            for row in row_index.get(src, ())
            if _source_tag_matches(row["source_tag"], unit["source_tag"])
            and _scope_matches(row["scope"], unit["component"])
        ]
        unit["registered"] = bool(matched)
        unit["term_rows"] = [
            {
                "line": row["_line"],
                "status": row["status"],
                "scope": row["scope"],
                "notes": bool((row.get("notes") or "").strip()),
            }
            for row in matched
        ]
        unit["corpus_occurrences"] = info["occurrences"]
        unit["force_manual"] = info["occurrences"] >= S2_2_THRESHOLD
        excluded = False
        if (
            unit["class"] == "B"
            and _tag_repr(unit["source_tag"]) not in MECHANISM_KEY_TAGS
            and not unit["registered"]
            and not unit["force_manual"]
            and info["occurrences"] == 1
            and len(info["components"]) == 1
            and len(info["targets"]) == 1
            and info["case_variants"] == 0
            and info["plural_variants"] == 0
            and src not in a_class_sources
            and src not in row_index
            and src.strip() == src
        ):
            excluded = True
        unit["auto_excluded"] = excluded
        unit["exclusion_rule"] = AUTO_EXCLUSION_RULE_ID if excluded else None
    return row_index


def _coverage_totals(
    units: list[dict[str, object]],
    predicate: Callable[[dict[str, object]], bool] | None = None,
) -> dict[str, object]:
    units_n = registered = auto_excluded = 0
    for unit in units:
        if predicate is not None and not predicate(unit):
            continue
        units_n += 1
        if unit["registered"]:
            registered += 1
        elif unit["auto_excluded"]:
            auto_excluded += 1
    missing = units_n - registered
    return {
        "units": units_n,
        "registered": registered,
        "missing": missing,
        "auto_excluded": auto_excluded,
        "manual_remaining": missing - auto_excluded,
        "coverage": round(registered / units_n, 4) if units_n else 0.0,
    }


def run_terminology_inventory(
    *,
    manifest: Manifest,
    docs: dict[str, LocaleDocument],
    rows: list[dict[str, object]],
    output_dir: Path,
) -> dict[str, object]:
    """生成 r2 审核基线：baseline / candidate-inventory / coverage / exclusions。

    全部输出只写忽略目录；每个文件绑定输入快照（TSV 与组件文件 SHA-256、
    版本清单与生成器版本），供内容寻址核对。
    """
    units, corpus = build_candidate_units(docs)
    annotate_units(units, corpus, rows)
    candidates = [u for u in units if u["class"] in ("A", "B", "UNCLASSIFIED")]

    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    tsv_path = manifest.root / manifest.terminology
    components_snapshot = []
    for comp in manifest.components:
        if comp.id not in docs:
            continue
        path = manifest.root / comp.translation
        components_snapshot.append(
            {
                "id": comp.id,
                "path": comp.translation,
                "sha256": _sha256(path),
                "entries": len(docs[comp.id].translations),
            }
        )
    components_snapshot.sort(key=lambda item: item["id"])

    # 现有术语行复核分母（与候选单元正交）
    by_status = Counter(row["status"] for row in rows)
    no_notes = sum(1 for row in rows if not (row.get("notes") or "").strip())
    c_rows = [row for row in rows if _unit_class_and_batch(row["source_tag"])[0] == "C"]
    row_batches = Counter(_row_batch(str(row["source_tag"])) for row in rows)

    by_tag: dict[str, dict[str, object]] = {}
    tag_units: dict[str, list[dict[str, object]]] = defaultdict(list)
    for unit in candidates:
        tag_units[_tag_repr(unit["source_tag"])].append(unit)
    for trepr in sorted(tag_units):
        by_tag[trepr] = _coverage_totals(tag_units[trepr])

    by_batch = {
        batch: _coverage_totals(candidates, lambda u, b=batch: u["batch"] == b)
        for batch in ("P0", "P1", "P2", "P3", "P4")
    }
    by_component = {
        comp: _coverage_totals(candidates, lambda u, c=comp: u["component"] == c)
        for comp in sorted(docs)
    }
    by_class = {
        cls: _coverage_totals(candidates, lambda u, c=cls: u["class"] == c)
        for cls in ("A", "B", "UNCLASSIFIED")
    }
    c_units_by_tag = Counter(
        _tag_repr(unit["source_tag"]) for unit in units if unit["class"] == "C"
    )
    unclassified_tags = sorted(
        trepr
        for trepr in tag_units
        if trepr not in A_CLASS_TAGS
        and trepr not in B_CLASS_TAGS
        and not trepr.startswith(CHAT_TAG_PREFIX)
    )

    excluded_units = [u for u in candidates if u["auto_excluded"]]
    force_manual = [u for u in candidates if u["force_manual"] and not u["registered"]]

    inputs = {
        "manifest": str(manifest.path),
        "version": manifest.version,
        "repositories": {
            name: spec.commit for name, spec in sorted(manifest.repositories.items())
        },
        "extractor_commit": manifest.extractor.commit,
        "terminology": {
            "path": str(tsv_path),
            "sha256": terminology_store.terminology_store_sha256(tsv_path),
            "rows": len(rows),
        },
        "components": components_snapshot,
    }
    summary = {
        "entries": sum(len(doc.translations) for doc in docs.values()),
        "components": sorted(docs),
        "tsv_rows_review": {
            "total": len(rows),
            "by_status": dict(by_status),
            "no_notes": no_notes,
            "c_class_rows": len(c_rows),
            "c_class_existing": sum(1 for row in c_rows if row["status"] == "existing"),
            "by_batch": dict(row_batches),
        },
        "candidates": by_class,
        "candidates_by_batch": by_batch,
        "c_units_by_tag": dict(c_units_by_tag),
        "unclassified_tags": unclassified_tags,
        "auto_excluded": len(excluded_units),
        "force_manual_unregistered": len(force_manual),
    }

    baseline = {
        "schema_version": INVENTORY_SCHEMA_VERSION,
        "generator": {
            "name": "tools/audit_dynamic.py:run_terminology_inventory",
            "tool_version": TOOL_VERSION,
            "schema_version": INVENTORY_SCHEMA_VERSION,
            "source_sha256": _sha256(Path(__file__)),
        },
        "inputs": inputs,
        "summary": summary,
    }
    coverage = {
        "schema_version": INVENTORY_SCHEMA_VERSION,
        "by_source_tag": by_tag,
        "by_batch": by_batch,
        "by_component": by_component,
        "by_class": by_class,
        "unclassified_tags": unclassified_tags,
    }
    inventory = {
        "schema_version": INVENTORY_SCHEMA_VERSION,
        "inputs": {
            "terminology_sha256": inputs["terminology"]["sha256"],
            "component_sha256": {
                item["id"]: item["sha256"] for item in components_snapshot
            },
            "version": manifest.version,
        },
        "count": len(candidates),
        "items": candidates,
    }
    exclusions = {
        "schema_version": INVENTORY_SCHEMA_VERSION,
        "rule": {
            "id": AUTO_EXCLUSION_RULE_ID,
            "conditions": [
                "class == B",
                "tag not in MECHANISM_KEY_TAGS (talent name / achievement name / newLore category)",
                "unregistered",
                "corpus_occurrences == 1",
                "single component",
                "single target",
                "no case/plural variants",
                "not an A-class source",
                "no terminology row for the source",
                "source has no leading/trailing whitespace",
                "corpus_occurrences < 15 (not force_manual)",
            ],
        },
        "count": len(excluded_units),
        "by_batch": dict(
            Counter(unit["batch"] for unit in excluded_units)  # type: ignore[arg-type]
        ),
        "items": [
            {
                "component": unit["component"],
                "source": unit["source"],
                "source_tag": unit["source_tag"],
                "batch": unit["batch"],
                "sections": unit["sections"],
                "targets": unit["targets"],
            }
            for unit in excluded_units
        ],
    }

    def _canonical_sha256(value: object) -> str:
        return hashlib.sha256(
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    p1_units = [unit for unit in candidates if unit["batch"] == "P1"]
    p1_manual = [
        unit
        for unit in p1_units
        if not unit["registered"] and not unit["auto_excluded"]
    ]
    p1_excluded = [unit for unit in p1_units if unit["auto_excluded"]]
    sample_size = min(len(p1_excluded), max(20, (len(p1_excluded) + 19) // 20))
    p1_exclusion_sample = sorted(
        p1_excluded,
        key=lambda unit: hashlib.sha256(
            json.dumps(
                [unit["component"], unit["source"], unit["source_tag"]],
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest(),
    )[:sample_size]
    p1_rows = [row for row in rows if _row_batch(str(row["source_tag"])) == "P1"]
    p1_workset = {
        "schema_version": 1,
        "contract": "tome4-terminology-review-workset-v1",
        "batch": "P1",
        "title": "角色结构",
        "inputs": {
            "version": manifest.version,
            "baseline_sha256": _canonical_sha256(baseline),
            "inventory_sha256": _canonical_sha256(inventory),
            "exclusions_sha256": _canonical_sha256(exclusions),
            "terminology_sha256": inputs["terminology"]["sha256"],
            "component_sha256": inventory["inputs"]["component_sha256"],
        },
        "summary": {
            **by_batch["P1"],
            "terminology_rows": len(p1_rows),
            "provisional_units": sum(
                1 for unit in p1_units if unit["class_provisional"]
            ),
            "exclusion_sample_size": sample_size,
        },
        "manual_candidates": p1_manual,
        "terminology_rows": p1_rows,
        "provisional_candidates": [
            unit for unit in p1_units if unit["class_provisional"]
        ],
        "auto_exclusion_sample": p1_exclusion_sample,
        "sampling": {
            "population": len(p1_excluded),
            "minimum": "max(5%, 20)",
            "method": "ascending sha256(component, source, source_tag)",
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    workset_dir = output_dir / "worksets"
    workset_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in (
        ("baseline.json", baseline),
        ("candidate-inventory.json", inventory),
        ("coverage.json", coverage),
        ("exclusions.json", exclusions),
    ):
        (output_dir / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
        )
    (workset_dir / "P1-role-structure-v1.json").write_text(
        json.dumps(p1_workset, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(
        f"terminology inventory done: {len(candidates)} candidates "
        f"(A={by_class['A']['units']}, B={by_class['B']['units']}, "
        f"UNCLASSIFIED={by_class['UNCLASSIFIED']['units']}); "
        f"missing={sum(v['missing'] for v in by_class.values())}, "
        f"auto_excluded={len(excluded_units)}, force_manual={len(force_manual)}"
    )
    return baseline


def run_dynamic_audit(
    *,
    manifest: Manifest | None = None,
    loader: LocaleLoader | None = None,
    terminology_path: Path | None = None,
    output_dir: Path | None = None,
    inventory_dir: Path | None = None,
) -> dict[str, object]:
    manifest = manifest or load_manifest(version=DEFAULT_VERSION)
    if terminology_path is None:
        terminology_path = manifest.root / manifest.terminology
    if output_dir is None:
        output_dir = manifest.root / ".artifacts/i18n/terminology-audit"
    if inventory_dir is None:
        inventory_dir = manifest.root / ".artifacts/i18n/terminology-review-r2"

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
    run_terminology_inventory(
        manifest=manifest, docs=docs, rows=rows, output_dir=inventory_dir
    )
    write_projection_report(run_projection(docs=docs, rows=rows), inventory_dir)
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
