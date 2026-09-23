#!/usr/bin/env python3
"""Build a consolidated human-review queue from the scattered campaign records.

Read-only over every source record. No semantic re-adjudication.

Primary queue records (the items a human must decide):
  human_review_md   HUMAN-REVIEW.md curated rows (batch-001..091); one record per row
  cross_092         reports/sol-092-01.md (batch-092 cross, not yet transcribed)
  batch_093         reports/gemini-093-01.md flagged entries (cross not dispatched)
  batch_094         reports/gemini-094-01.md flagged entries (cross not started)
  remaining_review  remaining-review-20260923/RESULTS.json (rem-* claims)

Attached reference: STATE.json cross_reviews[].recorded_cross_verdicts, matched to a
record by entry_id, so every curated row carries Sol's raw claim-level verdicts.

Outputs (regenerable, next to this script):
  human-review-queue-20260923/HUMAN-REVIEW-QUEUE.json
  human-review-queue-20260923/HUMAN-REVIEW-QUEUE.md
  human-review-queue-20260923/SUMMARY.json

Model status labels are copied verbatim. reconciled-20260923 canonical claims are NOT
merged here (separate experiment ledger).
"""
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "human-review-queue-20260923")

INVENTORY = os.path.join(HERE, "inventory.json")
STATE = os.path.join(HERE, "STATE.json")
HUMAN_REVIEW = os.path.join(HERE, "HUMAN-REVIEW.md")
REMAINING = os.path.join(HERE, "remaining-review-20260923", "RESULTS.json")
RECONCILED = os.path.join(HERE, "reconciled-20260923", "FINDINGS.json")

ENTRY_RE = re.compile(r"entry-\d{5}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def rel(path):
    return os.path.relpath(path, HERE)


def batch_file(cross_id):
    m = re.match(r"cross-batch-(\d{3})", cross_id or "")
    if not m:
        return None
    p = os.path.join(HERE, "batches", f"batch-{m.group(1)}.md")
    return rel(p) if os.path.exists(p) else None


def cross_evidence(cross):
    ev = {
        "cross_id": cross["cross_id"],
        "verdict_author": cross.get("verdict_author"),
        "input_path": cross.get("input_path"),
        "human_review_file": rel(HUMAN_REVIEW),
        "batch_file": batch_file(cross["cross_id"]),
    }
    src = cross.get("source_dispatch_id")
    if src:
        ev["gemini_report"] = rel(os.path.join(HERE, "reports", src + ".md"))
    for d in cross.get("dispatches") or []:
        ev.setdefault("sol_reports", []).append(rel(os.path.join(HERE, "reports", d + ".md")))
    return ev


def entry_ref(entry):
    if not entry:
        return None
    return {
        "component": entry.get("component"),
        "logical_path": entry.get("logical_path"),
        "line": entry.get("line"),
        "section": entry.get("section"),
        "source": entry.get("source"),
        "target": entry.get("target"),
        "source_tag": entry.get("source_tag"),
        "snapshot_sha256": entry.get("snapshot_sha256"),
    }


# ---------------------------------------------------------------- HUMAN-REVIEW

def section_cross_id(title, state_crosses):
    m = re.search(r"batch-(\d{3})", title)
    if m:
        n = m.group(1)
        if n == "005":
            if "前三处" in title:
                return "cross-batch-005-partial"
            if "其余" in title:
                return "cross-batch-005-rest"
        return f"cross-batch-{n}"
    if "003/004" in title:
        return "cross-batch-003-004"
    if "当前两批" in title:
        return None  # batch-001 + batch-002, resolved per record
    return None


def extract_entry_ids(cell):
    """Entry ids from a curated cell, including ranges (entry-00393–00400)
    and bare continuations (entry-01706 / 01709 / 01711)."""
    ids = ENTRY_RE.findall(cell)
    for a, b in re.findall(r"entry-(\d{5})\s*[–—~-]\s*(\d{5})", cell):
        lo, hi = int(a), int(b)
        if 0 <= hi - lo <= 200:
            ids += [f"entry-{n:05d}" for n in range(lo, hi + 1)]
    if "entry-" in cell:
        for n in re.findall(r"/\s*(\d{5})\b", cell):
            ids.append(f"entry-{n}")
    return list(dict.fromkeys(ids))


def parse_human_review(state_crosses):
    with open(HUMAN_REVIEW, "r", encoding="utf-8") as fh:
        text = fh.read()
    sections = []
    cur_title, cur_lines = "", []
    for ln in text.splitlines():
        if ln.startswith("## "):
            sections.append((cur_title, cur_lines))
            cur_title, cur_lines = ln[3:].strip(), []
        else:
            cur_lines.append(ln)
    sections.append((cur_title, cur_lines))

    records = []
    for title, lines in sections:
        cross_id = section_cross_id(title, state_crosses)
        title_ids = extract_entry_ids(title)
        table_rows = []
        note_lines = []
        for ln in lines:
            s = ln.strip()
            if s.startswith("|") and s.endswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if not cells or all(set(c) <= set("-: ") for c in cells):
                    continue
                if any("条目" in c for c in cells[:1]):
                    continue
                table_rows.append(cells)
            elif s:
                note_lines.append(s)
        note = " ".join(note_lines)
        covered_ids = set()
        for cells in table_rows:
            if len(cells) < 2:
                continue
            entry_ids = extract_entry_ids(cells[0])
            if not entry_ids:
                continue
            covered_ids.update(entry_ids)
            sol_summary = " ｜ ".join(c for c in cells[1:-1] if c) if len(cells) > 2 else (cells[1] if len(cells) == 2 else "")
            human_hint = cells[-1] if len(cells) > 2 else ""
            records.append({
                "source_layer": "human_review_md",
                "section": title,
                "cross_id": cross_id,
                "entry_ids": entry_ids,
                "entry_id": entry_ids[0],
                "claim_id": None,
                "sol_summary": sol_summary,
                "human_hint": human_hint,
                "status": _dominant_status(sol_summary or human_hint),
                "detail": None,
                "reported_source": None,
                "reported_target": None,
                "section_note": note,
                "evidence": {},
            })
        # sections that carry their finding in the title/prose instead of a table row
        for eid in title_ids:
            if eid in covered_ids:
                continue
            hint = next((l for l in note_lines if "人工待决" in l), "")
            records.append({
                "source_layer": "human_review_md",
                "section": title,
                "cross_id": cross_id,
                "entry_ids": [eid],
                "entry_id": eid,
                "claim_id": None,
                "sol_summary": "",
                "human_hint": hint,
                "status": _dominant_status(note),
                "detail": "\n".join(lines).strip(),
                "reported_source": None,
                "reported_target": None,
                "section_note": note,
                "evidence": {},
            })
    return records


STATUS_ORDER = ["confirmed", "pending", "advisory", "refuted"]


def _dominant_status(text):
    low = (text or "").lower()
    # strongest signal present, in the campaign's own precedence
    if "confirmed" in low:
        return "confirmed"
    if "pending" in low:
        return "pending"
    if "advisory" in low:
        return "advisory"
    if "refuted" in low:
        return "refuted"
    return None


# ---------------------------------------------------------------- primary reports

ENTRY_HEAD_RE = re.compile(r"^#{3,4}\s+(entry-\d{5})\s*$")
FIELD_RE = re.compile(r"^[-*]\s*\*\*(原文|译文|结论|复核结论|依据|核验依据|位置|编号)\*\*：\s*(.*)$")


def _parse_blocks(text):
    lines = text.splitlines()
    cur, buf = None, []
    for ln in lines:
        m = ENTRY_HEAD_RE.match(ln)
        if m:
            if cur:
                yield cur, "\n".join(buf).strip()
            cur, buf = m.group(1), []
        elif cur:
            buf.append(ln)
    if cur:
        yield cur, "\n".join(buf).strip()


def _parse_fields(block):
    fields, lines, i, cur = {}, block.splitlines(), 0, None
    while i < len(lines):
        m = FIELD_RE.match(lines[i].strip())
        if m:
            key, val = m.group(1), m.group(2)
            if val.strip() in ("", "```text", "```"):
                collected, j = [], i + 1
                while j < len(lines) and not FIELD_RE.match(lines[j].strip()):
                    collected.append(lines[j]); j += 1
                t = "\n".join(collected).strip()
                t = re.sub(r"^```[a-z]*\n?", "", t)
                t = re.sub(r"\n?```$", "", t)
                fields[key] = t.strip(); i = j; continue
            fields[key] = val.strip(); cur = key; i += 1; continue
        i += 1
    return fields


def flagged_primary(report_path, layer, batch_id):
    with open(report_path, "r", encoding="utf-8") as fh:
        text = fh.read()
    out = []
    for entry_id, block in _parse_blocks(text):
        f = _parse_fields(block)
        conclusion = f.get("结论") or f.get("复核结论")
        if not conclusion or "未发现问题" in conclusion:
            continue
        prompt = os.path.join(HERE, f"cross-batch-{batch_id}.md")
        out.append({
            "source_layer": layer,
            "section": None,
            "cross_id": None,
            "entry_ids": [entry_id],
            "entry_id": entry_id,
            "claim_id": None,
            "sol_summary": None,
            "human_hint": None,
            "status": conclusion,
            "detail": block,
            "reported_source": f.get("原文"),
            "reported_target": f.get("译文"),
            "section_note": None,
            "evidence": {
                "gemini_report": rel(report_path),
                "batch_file": batch_file(f"cross-batch-{batch_id}"),
                "cross_prompt": rel(prompt) if os.path.exists(prompt) else None,
                "cross_status": "awaiting_cross",
            },
        })
    return out


CLAIM_HEAD_RE = re.compile(r"^#{3,4}\s+Claim\s+(\d+(?:\.\d+)?)\s*[:：]?\s*(.*)$")
SOL_CONCL_RE = re.compile(r"\*\*结论[:：]\s*(confirmed|refuted|pending|advisory)\*\*", re.I)


def parse_sol_claim_report(report_path, layer, cross_id):
    with open(report_path, "r", encoding="utf-8") as fh:
        text = fh.read()
    out, cur_entry, no, title, buf = [], None, None, None, []

    def flush():
        if no is None or cur_entry is None:
            return
        block = "\n".join(buf).strip()
        m = SOL_CONCL_RE.search(block)
        out.append({
            "source_layer": layer,
            "section": None,
            "cross_id": cross_id,
            "entry_ids": [cur_entry],
            "entry_id": cur_entry,
            "claim_id": f"Claim {no}",
            "sol_summary": (title or "").strip(),
            "human_hint": None,
            "status": m.group(1).lower() if m else "unknown",
            "detail": block,
            "reported_source": None,
            "reported_target": None,
            "section_note": None,
            "evidence": {
                "sol_reports": [rel(report_path)],
                "cross_prompt": rel(os.path.join(HERE, "cross-batch-" + cross_id[-3:] + ".md")),
                "cross_status": "crossed_not_transcribed",
            },
        })

    for ln in text.splitlines():
        em = re.match(r"^##\s+(entry-\d{5})\s*$", ln)
        if em:
            flush(); buf = []; no = title = None; cur_entry = em.group(1); continue
        cm = CLAIM_HEAD_RE.match(ln)
        if cm:
            flush(); buf = []; no, title = cm.group(1), cm.group(2); continue
        if no is not None:
            buf.append(ln)
    flush()
    return out


def build_remaining():
    d = load_json(REMAINING)
    obs = {x["observation_id"]: x for x in d.get("raw_observations", [])}
    out = []
    for c in d.get("claims", []):
        g = obs.get(c.get("gemini_observation"), {})
        s = obs.get(c.get("sol_observation"), {})
        out.append({
            "source_layer": "remaining_review",
            "section": None,
            "cross_id": None,
            "entry_ids": [c.get("entry_id")],
            "entry_id": c.get("entry_id"),
            "claim_id": c.get("claim_id"),
            "sol_summary": None,
            "human_hint": None,
            "status": c.get("current_status"),
            "detail": (s.get("original_text") or g.get("original_text") or "").strip(),
            "reported_source": None,
            "reported_target": None,
            "section_note": None,
            "evidence": {
                "results_json": rel(REMAINING),
                "findings_md": rel(os.path.join(HERE, "remaining-review-20260923", "FINDINGS.md")),
                "gemini_report": g.get("source"),
                "sol_report": s.get("source"),
                "cross_status": "crossed",
            },
        })
    return out


def main():
    inv = {e["audit_id"]: e for e in load_json(INVENTORY)["entries"]}
    state = load_json(STATE)
    crosses = state.get("cross_reviews", [])
    by_cross = {c["cross_id"]: c for c in crosses}

    # raw verdicts, indexed by entry_id
    raw_by_entry = {}
    raw_campaign = []
    for c in crosses:
        if c["cross_id"] in ("cross-batch-092", "cross-batch-093"):
            continue
        ev = cross_evidence(c)
        for v in c.get("recorded_cross_verdicts") or []:
            eid = v.get("entry_id")
            if not eid:
                ids = c.get("entry_ids") or []
                eid = ids[0] if len(ids) == 1 else None
            rec = {
                "cross_id": c["cross_id"], "entry_id": eid,
                "claim": v.get("claim"), "verdict": v.get("verdict"),
                "impact": v.get("impact"), "evidence": ev,
            }
            raw_campaign.append(rec)
            if eid:
                raw_by_entry.setdefault(eid, []).append(rec)

    records = []
    records += parse_human_review(by_cross)
    if os.path.exists(os.path.join(HERE, "reports", "sol-092-01.md")):
        records += parse_sol_claim_report(
            os.path.join(HERE, "reports", "sol-092-01.md"), "cross_092", "cross-batch-092")
    records += flagged_primary(os.path.join(HERE, "reports", "gemini-093-01.md"), "batch_093", "093")
    records += flagged_primary(os.path.join(HERE, "reports", "gemini-094-01.md"), "batch_094", "094")
    records += build_remaining()

    # Safety net: raw Sol verdicts whose entry was never transcribed into any curated row.
    covered_ids = {eid for r in records for eid in r["entry_ids"] if eid}
    untracked_crosses = set()
    seen_untracked = set()
    for rec in raw_campaign:
        eid = rec["entry_id"]
        if not eid or eid in covered_ids or eid in seen_untracked:
            continue
        seen_untracked.add(eid)
        untracked_crosses.add(rec["cross_id"])
        c = by_cross.get(rec["cross_id"], {})
        records.append({
            "source_layer": "campaign_state_untracked",
            "section": None,
            "cross_id": rec["cross_id"],
            "entry_ids": [eid],
            "entry_id": eid,
            "claim_id": None,
            "sol_summary": None,
            "human_hint": "HUMAN-REVIEW 未转录；来自 STATE 原始 verdict",
            "status": rec["verdict"],
            "detail": "；".join(
                f"{v['claim']}→{v['verdict']}" for v in raw_by_entry.get(eid, [])),
            "reported_source": None,
            "reported_target": None,
            "section_note": "HUMAN-REVIEW.md 未收录该 entry 的交叉结论，此处由 STATE.json raw verdict 补齐。",
            "evidence": cross_evidence(c) if c else {},
        })

    # resolve cross ids per curated row when the section merges batches
    for r in records:
        if r["source_layer"] == "human_review_md" and not r["cross_id"]:
            for eid in r["entry_ids"]:
                for cid, c in by_cross.items():
                    if eid in (c.get("entry_ids") or []):
                        r["cross_id"] = cid
                        break
                if r["cross_id"]:
                    break
        if r["source_layer"] == "human_review_md":
            c = by_cross.get(r["cross_id"])
            if c:
                r["evidence"] = cross_evidence(c)
        # attach raw Sol verdict detail
        r["sol_claims"] = []
        for eid in r["entry_ids"]:
            r["sol_claims"].extend(raw_by_entry.get(eid, []))

    records.sort(key=lambda r: (r.get("entry_id") or "zzz",
                                {"human_review_md": 0, "cross_092": 1, "batch_093": 2,
                                 "batch_094": 3, "remaining_review": 4,
                                 "campaign_state_untracked": 5}.get(r["source_layer"], 9),
                                str(r.get("claim_id") or r.get("sol_summary") or "")))
    for i, r in enumerate(records, 1):
        r["queue_id"] = f"hrq-{i:05d}"
        r["entry"] = entry_ref(inv.get(r.get("entry_id")))
        r["human_decision"] = None
        r["human_note"] = None
        r["human_decided_at"] = None

    apply_decisions(records)

    layers = {}
    for r in records:
        L = layers.setdefault(r["source_layer"], {"records": 0, "entries": set(), "status": {}})
        L["records"] += 1
        if r.get("entry_id"):
            L["entries"].add(r["entry_id"])
        L["status"][r.get("status")] = L["status"].get(r.get("status"), 0) + 1

    summary = {
        "generated_from": {
            "inventory.json": sha256(INVENTORY),
            "STATE.json": sha256(STATE),
            "HUMAN-REVIEW.md": sha256(HUMAN_REVIEW),
            "remaining-review-20260923/RESULTS.json": sha256(REMAINING),
            "reconciled-20260923/FINDINGS.json": sha256(RECONCILED),
            "reports/sol-092-01.md": sha256(os.path.join(HERE, "reports", "sol-092-01.md")),
            "reports/gemini-093-01.md": sha256(os.path.join(HERE, "reports", "gemini-093-01.md")),
            "reports/gemini-094-01.md": sha256(os.path.join(HERE, "reports", "gemini-094-01.md")),
        },
        "note": ("Curated human-decision rows from HUMAN-REVIEW.md plus the sources missing "
                 "from it (batch-092 cross, batch-093/094 primary, remaining-review). "
                 "Sol status labels copied verbatim; no semantic adjudication. "
                 "reconciled-20260923 canonical claims are not merged (separate experiment ledger)."),
        "schema_version": 1,
        "total_records": len(records),
        "decided_records": sum(1 for r in records if r.get("human_decision")),
        "distinct_entries": len({r["entry_id"] for r in records if r.get("entry_id")}),
        "records_missing_entry": sum(1 for r in records if not r.get("entry_id")),
        "raw_campaign_verdict_count": len(raw_campaign),
        "untracked_crosses_without_transcription": sorted(untracked_crosses),
        "layers": {k: {"records": v["records"], "distinct_entries": len(v["entries"]),
                       "status_counts": v["status"]}
                   for k, v in sorted(layers.items())},
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "HUMAN-REVIEW-QUEUE.json"), "w", encoding="utf-8") as fh:
        json.dump({"schema_version": 1, "summary": summary, "records": records,
                   "raw_campaign_verdicts": raw_campaign}, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    with open(os.path.join(OUT_DIR, "SUMMARY.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    write_md(records, summary)

    # checks
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


def apply_decisions(records):
    """Overlay durable human decisions from HUMAN-DECISIONS.jsonl (keyed by queue_id,
    with claim_id/entry_id as fallback identity)."""
    path = os.path.join(OUT_DIR, "HUMAN-DECISIONS.jsonl")
    if not os.path.exists(path):
        return
    by_qid, by_claim = {}, {}
    with open(path, "r", encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            try:
                d = json.loads(ln)
            except json.JSONDecodeError:
                continue
            if d.get("queue_id"):
                by_qid[d["queue_id"]] = d
            if d.get("claim_id"):
                by_claim[d["claim_id"]] = d
    for r in records:
        d = by_qid.get(r["queue_id"]) or (by_claim.get(r.get("claim_id")) if r.get("claim_id") else None)
        if not d:
            continue
        r["human_decision"] = d.get("decision")
        r["human_note"] = d.get("note")
        r["human_decided_at"] = d.get("decided_at")


LAYER_LABEL = {
    "human_review_md": "HUMAN-REVIEW",
    "cross_092": "cross-092",
    "batch_093": "batch-093(待交叉)",
    "batch_094": "batch-094(待交叉)",
    "remaining_review": "remaining",
    "campaign_state_untracked": "STATE补录",
}


def cell(text, limit=240):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", str(text)).strip()
    if len(text) > limit:
        text = text[: limit - 1] + "…"
    return text.replace("|", "\\|").replace("\n", " ")


def write_md(records, summary):
    by_entry = {}
    for r in records:
        by_entry.setdefault(r.get("entry_id") or "(no-entry)", []).append(r)
    order = sorted(by_entry.keys(), key=lambda e: (e == "(no-entry)", e))

    L = []
    L.append("# 统一人工批阅队列（合并索引）")
    L.append("")
    L.append("由 `build_human_review_queue.py` 合并 campaign 各来源生成：只做索引、原文/译文关联、")
    L.append("Sol 原始 verdict 挂接，不新增语义裁决。每条的模型状态原样保留。")
    L.append("`human_decision` 默认空，等待人工填写；填写后写回 JSON 同名字段。")
    L.append("")
    L.append("完整模型原文与全部 raw verdict 见 [HUMAN-REVIEW-QUEUE.json](HUMAN-REVIEW-QUEUE.json)；来源哈希见 [SUMMARY.json](SUMMARY.json)。")
    L.append("")
    L.append("## 统计")
    L.append("")
    L.append(f"- 待办记录：**{summary['total_records']}**；涉及 entry：**{summary['distinct_entries']}**。")
    for layer, info in summary["layers"].items():
        st = "、".join(f"{k}={v}" for k, v in sorted(info["status_counts"].items(), key=lambda x: str(x[0])))
        L.append(f"- `{layer}`：{info['records']} 条 / {info['distinct_entries']} entry；{st}")
    L.append(f"- 挂接的 Sol 原始 verdict 参考记录：{summary['raw_campaign_verdict_count']} 条（见 JSON `raw_campaign_verdicts`）。")
    ut = summary.get("untracked_crosses_without_transcription") or []
    if ut:
        L.append(f"- STATE 有 verdict 但 HUMAN-REVIEW 未转录的 cross（已用 `STATE补录` 补齐）：{', '.join(ut)}。")
    L.append("")
    L.append("说明：多 entry 行（如 `entry-01706 / 01709 / …`）按首个 entry 归组，行内列出全部 entry。")
    L.append("")
    L.append("> 未合并：`reconciled-20260923/FINDINGS.json` 的 714 canonical claims（实验台账，另有自身 ledger）及其 3050 条未映射 observation。")
    L.append("")
    L.append("---")
    L.append("")

    for entry_id in order:
        recs = by_entry[entry_id]
        ref = recs[0].get("entry")
        L.append(f"## {entry_id}")
        L.append("")
        if ref:
            L.append(f"- 位置：`{ref.get('logical_path')}:{ref.get('line')}`（{ref.get('component')}）｜section：`{ref.get('section')}`｜source_tag：`{ref.get('source_tag')}`")
            L.append(f"- 原文：`{ref.get('source')}`")
            L.append(f"- 现译：`{ref.get('target')}`")
        L.append("")
        L.append("| queue_id | 来源 | cross/claim | 状态 | 要点 / 人工待决 | 译名全文比对 | 决定 |")
        L.append("|---|---|---|---|---|---|---|")
        for r in recs:
            tag = r.get("cross_id") or r.get("claim_id") or ""
            if len(r.get("entry_ids") or []) > 1:
                tag = (tag + " " + ",".join(r["entry_ids"])).strip()
            key = r.get("human_hint") or r.get("sol_summary") or ""
            L.append(
                f"| {r['queue_id']} | {LAYER_LABEL.get(r['source_layer'], r['source_layer'])} "
                f"| {cell(tag, 28)} | {cell(r.get('status'), 24)} "
                f"| {cell(key, 300)} |  | {cell(r.get('human_decision'), 40)} |")
        L.append("")
        for r in recs:
            extras = []
            if r.get("sol_summary") and r.get("human_hint"):
                extras.append(f"Sol 分档：{r['sol_summary']}")
            if r.get("detail"):
                extras.append(r["detail"])
            if r.get("sol_claims"):
                claims = "; ".join(f"{c['claim']}→{c['verdict']}" for c in r["sol_claims"])
                extras.append(f"raw verdict: {claims}")
            if r.get("section_note"):
                extras.append(f"段末说明：{r['section_note']}")
            if not extras:
                continue
            L.append(f"<details><summary>{r['queue_id']} · {LAYER_LABEL.get(r['source_layer'], r['source_layer'])} 详情</summary>")
            L.append("")
            for e in extras:
                L.append("```")
                L.append(str(e)[:4000])
                L.append("```")
            L.append("</details>")
            L.append("")

    with open(os.path.join(OUT_DIR, "HUMAN-REVIEW-QUEUE.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L).rstrip() + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
