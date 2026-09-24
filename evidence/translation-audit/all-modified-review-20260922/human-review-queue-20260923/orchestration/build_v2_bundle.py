#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a translation_contextual_v2 full envelope for one bounded bundle.

review_only v2 allows a single `full` per task, so each bundle becomes its own
task with one whole-workset envelope. Read-only over the Lua files.
"""
import argparse
import collections
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))
import contextual_anchor_preflight as P  # noqa: E402

SOURCE_MAP = {
    "engine/": "game/engines/default/engine/",
    "engine/data/": "game/engines/default/data/",
    "mod-boot/": "game/engines/default/modules/boot/",
    "mod-tome/": "game/modules/tome/",
}
BRIEFING = (
    "有界译文语境审核。按冻结顺序逐条比对 source 与 target，结合本文件给出的术语子集、"
    "同 section 邻近译文与固定版本公开源码证据，只报有证据的语义、机制、术语、关系或跨条一致性"
    "问题；无问题判 OK。DLC（tome-orcs/tome-possessors）源码未固定，引用时须注明。"
)


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def public_source(section):
    for prefix, mapped in SOURCE_MAP.items():
        if section.startswith(prefix):
            return mapped + section[len(prefix):]
    return None


def scan_file(path):
    text = open(path, encoding="utf-8").read()
    sections, calls = P._scan_lua(text)
    per_section = collections.defaultdict(list)
    for section in sections:
        nxt = min((s.start for s in sections if s.start > section.start), default=len(text))
        members = [c for c in calls if section.start < c.start < nxt]
        for ordinal, call in enumerate(members):
            cursor = text.find("(", call.start)
            cursor = P._skip_space_and_comments(text, cursor + 1)
            if text[cursor] in ("'", '"'):
                src, cursor = P._decode_lua_string(text, cursor)
            else:
                src, cursor = P._decode_lua_long_bracket(text, cursor)
            cursor = P._skip_space_and_comments(text, cursor)
            if cursor >= len(text) or text[cursor] != ",":
                continue
            cursor = P._skip_space_and_comments(text, cursor + 1)
            if text[cursor] in ("'", '"'):
                tgt, cursor = P._decode_lua_string(text, cursor)
            else:
                tgt, cursor = P._decode_lua_long_bracket(text, cursor)
            cursor = P._skip_space_and_comments(text, cursor)
            tag = ""
            if cursor < len(text) and text[cursor] == ",":
                cursor = P._skip_space_and_comments(text, cursor + 1)
                if cursor < len(text) and text[cursor] in ("'", '"'):
                    tag, _ = P._decode_lua_string(text, cursor)
            per_section[section.path].append(
                {"ordinal": ordinal, "source": src, "target": tgt, "tag": tag, "args_order": call.args_order}
            )
    return per_section


def render_terminology(rows):
    lines = [
        f"- {t['source']} => {t['target']} [{t['category']}/{t['source_tag']}/{t['status']}/{t['scope']}]"
        + (f" 注：{t['notes']}" if t.get("notes") else "")
        for t in rows
    ]
    return "适用术语子集：\n" + ("\n".join(lines) if lines else "（本 bundle 无以原文字形直接命中的术语条目）")


def build(packet_path, task_dir, dispatch_id, fixed_identity, terminology_dir, out_prefix):
    packet = json.load(open(packet_path, encoding="utf-8"))
    revisions = packet["revisions"]
    files = sorted({r["file"] for r in revisions})
    cache = {f: scan_file(os.path.join(REPO, f)) for f in files}

    blob_parts = []
    for rev in revisions:
        blob_parts.append(rev["source"])
        for entry in cache[rev["file"]].get(rev["section"], []):
            if entry["source"] == rev["source"]:
                blob_parts.append(entry["target"])
    blob = "\n".join(blob_parts)

    terms = []
    for name in sorted(os.listdir(terminology_dir)):
        if not name.endswith(".tsv"):
            continue
        with open(os.path.join(terminology_dir, name), encoding="utf-8") as fh:
            header = fh.readline().rstrip("\n").split("\t")
            for line in fh:
                line = line.rstrip("\n")
                if not line:
                    continue
                cells = line.split("\t")
                if len(cells) < len(header):
                    cells += [""] * (len(header) - len(cells))
                row = dict(zip(header, cells))
                if row["source"] and row["source"] in blob:
                    terms.append(row)

    keys, snapshot, contexts, problems = [], [], [], []
    for rev in revisions:
        entries = cache[rev["file"]].get(rev["section"], [])
        hits = [e for e in entries if e["source"] == rev["source"]]
        if not hits:
            problems.append(f"{rev['revision_key']}: source not found in {rev['section']}")
            continue
        targets = {h["target"] for h in hits}
        if len(targets) != 1:
            problems.append(f"{rev['revision_key']}: {len(targets)} distinct targets in window")
            continue
        orders = {h["args_order"] for h in hits}
        if len(orders) != 1:
            problems.append(f"{rev['revision_key']}: differing args_order")
            continue
        args_order = next(iter(orders))
        key = rev["revision_key"]
        keys.append(key)
        snapshot.append({"revision_key": key, "source": rev["source"], "target": next(iter(targets))})
        ordinal = hits[0]["ordinal"]
        near = [f"{e['source']!r}->{e['target']!r}" for e in entries if abs(e["ordinal"] - ordinal) <= 2 and e["ordinal"] != ordinal]
        src_path = public_source(rev["section"])
        carriers = [f"{h['tag'] or '_t'}" for h in hits]
        ctx = (
            f"{rev['file']}; section={rev['section']}; source_tag={hits[0]['tag']}; "
            f"组件={rev['component']}; 固定源码路径={src_path or '未映射（DLC 源码未固定）'}"
            f"; 同源载体数={len(hits)}（tags: {','.join(carriers)}）"
            + (f"; 邻近译文={' , '.join(near)}" if near else "")
        )
        if args_order is not None:
            ctx += f"; args_order={args_order}"
        contexts.append({"revision_key": key, "context": ctx})

    if problems:
        for p in problems:
            print("PROBLEM:", p, file=sys.stderr)
        raise SystemExit(2)

    payload = {
        "contract": "translation_contextual_v2",
        "ordered_revision_keys": keys,
        "translation_snapshot": snapshot,
        "fixed_source_identity": fixed_identity,
        "terminology_snapshot": render_terminology(terms),
        "bounded_context": contexts,
        "rendered_briefing": BRIEFING,
    }
    identity = hashlib.sha256(canonical(payload)).hexdigest()
    envelope = {"candidate_identity": identity, "payload": payload}
    os.makedirs(task_dir, exist_ok=True)
    with open(os.path.join(task_dir, f"{out_prefix}-PAYLOAD-{dispatch_id}.json"), "wb") as fh:
        fh.write(canonical(payload))
    with open(os.path.join(task_dir, f"{out_prefix}-ENVELOPE-{dispatch_id}.json"), "wb") as fh:
        fh.write(canonical(envelope))
    anchors = [{"file": f, "section_path": s, "ordered_titles": []} for f in files for s in sorted(cache[f])]
    with open(os.path.join(task_dir, f"{out_prefix}-SCOPE-{dispatch_id}.json"), "w", encoding="utf-8") as fh:
        json.dump({"schema_version": 1, "allowed_files": files, "anchor_scopes": anchors}, fh, ensure_ascii=False, indent=1)
    return identity, len(keys), len(terms), len(files), len(anchors)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet", required=True)
    ap.add_argument("--task-dir", required=True)
    ap.add_argument("--dispatch-id", required=True)
    ap.add_argument("--fixed-source-identity", required=True)
    ap.add_argument("--terminology", default=os.path.join(REPO, "terminology"))
    ap.add_argument("--out-prefix", default="CONTEXTUAL")
    args = ap.parse_args()
    identity, n, t, f, a = build(args.packet, args.task_dir, args.dispatch_id, args.fixed_source_identity, args.terminology, args.out_prefix)
    print(f"revisions={n} terminology_rows={t} files={f} anchors={a}")
    print(f"candidate_identity={identity}")
