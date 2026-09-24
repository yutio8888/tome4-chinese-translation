from pathlib import Path
import hashlib
import json
import re
import sys

sys.path.insert(0, "tools")
from i18nlib.config import load_manifest
from i18nlib.lint import AT_TOKEN_RE, MARKUP_RE
from i18nlib.locale_model import LocaleLoader
from i18nlib.runtime import LuaRuntime


ROOT = Path(__file__).resolve().parents[3]
TASK = ROOT / ".ai/task/repair-w27-20260924"
FILES = ("mod-tome.lua", "tome-ashes-urhrok.lua")
PLACEHOLDER_RE = re.compile(r"%[-+ #0]*\d*(?:\.\d+)?[cdeEfgGiouXxqs%]")
MUCUS_REVISION = "fdff442a1e55fecae18f6dd9bb4761bb6c0572059c4f4a1706ef5d06fa3ff2d2"
EPITAPH_REVISION = "fec0939b43c92583f4d00aeb244393a5348b9d4d9d20be01e6b3cb39ceaa0d35"
WRATH_REVISION = "295b84f066bb5e2610c84354d9f94de40a32ef9ded864d97373d29cbf3df47c5"
STONE_GOLEM_REVISION = "fff8487389cbed3c2897bfc85f6d3c264537cae71a0985cdbf5e67c64a34c076"


def without_line(record):
    return {key: value for key, value in record.items() if key != "line"}


def leading_tabs(value):
    return [len(line) - len(line.lstrip("\t")) for line in value.split("\n")]


loader = LocaleLoader(LuaRuntime(load_manifest()))
workset = json.loads((TASK / "WORKSET.json").read_text(encoding="utf-8"))["items"]
assert len(workset) == 28
allowed = {
    (item["normalized_path"], item["section"], item["source"], item["source_tag"]): item
    for item in workset
}
assert len(allowed) == 28

frozen_records = json.loads((TASK / "BASELINE-records.json").read_text(encoding="utf-8"))
changed = []
line_invariants = []
total_records = 0

for filename in FILES:
    baseline = loader.load_path(
        TASK / "baseline" / filename, logical_path=filename
    ).records
    current = loader.load_path(ROOT / filename, logical_path=filename).records
    assert len(baseline) == len(current), f"record count drift: {filename}"
    total_records += len(current)

    baseline_by_key = {
        (row.get("section"), row.get("source"), row.get("source_tag")): row
        for row in baseline
        if row.get("kind") == "translation"
    }
    for frozen in frozen_records[filename]:
        frozen_key = (frozen["section"], frozen["source"], frozen["source_tag"])
        assert baseline_by_key[frozen_key] == frozen, f"frozen record drift: {frozen_key}"

    for before, after in zip(baseline, current):
        left = without_line(before)
        right = without_line(after)
        if left == right:
            continue
        key = (filename, before.get("section"), before.get("source"), before.get("source_tag"))
        assert key in allowed, f"out-of-scope record changed: {key}"
        item = allowed[key]
        assert before["target"] == item["target_preimage"]
        assert {k: v for k, v in left.items() if k != "target"} == {
            k: v for k, v in right.items() if k != "target"
        }, f"non-target field drift: {item['entry_revision_identity']}"

        source = after["source"]
        target = after["target"]
        source_placeholders = PLACEHOLDER_RE.findall(source)
        target_placeholders = PLACEHOLDER_RE.findall(target)
        if item["entry_revision_identity"] == STONE_GOLEM_REVISION:
            assert source_placeholders == target_placeholders + ["%%", "%%"]
            assert target_placeholders == PLACEHOLDER_RE.findall(before["target"])
        else:
            assert source_placeholders == target_placeholders, (
                item["entry_revision_identity"],
                source_placeholders,
                target_placeholders,
            )
        assert MARKUP_RE.findall(source) == MARKUP_RE.findall(target), item[
            "entry_revision_identity"
        ]
        assert AT_TOKEN_RE.findall(source) == AT_TOKEN_RE.findall(target), item[
            "entry_revision_identity"
        ]

        revision = item["entry_revision_identity"]
        if revision == MUCUS_REVISION:
            assert target.count("\n") == source.count("\n") == 5
            assert target.count("\t") == source.count("\t") == 10
            assert leading_tabs(target) == leading_tabs(source)
        elif revision == WRATH_REVISION:
            assert target.count("\n") == source.count("\n") == 9
            assert target.count("\t") == source.count("\t") == 18
            assert leading_tabs(target) == leading_tabs(source)
            wrath_lines = target.splitlines()
            assert len(wrath_lines[3:]) == 7
            assert all(line.startswith("\t\t-") for line in wrath_lines[3:])
        else:
            assert target.count("\n") == source.count("\n"), revision
            assert leading_tabs(target) == leading_tabs(source), revision

        if revision == EPITAPH_REVISION:
            assert "在这光明的时代\n在崭新的冒险中\n你不会被遗忘" in target
        line_invariants.append(
            {
                "revision": revision,
                "source_lf": source.count("\n"),
                "target_lf": target.count("\n"),
                "target_leading_tabs": leading_tabs(target),
            }
        )
        changed.append(
            {
                "revision": revision,
                "file": filename,
                "line": after["line"],
                "before": before["target"],
                "after": target,
            }
        )

assert len(changed) == 28, len(changed)
assert {row["revision"] for row in changed} == {
    item["entry_revision_identity"] for item in workset
}

anchors = json.loads((TASK / "SOURCE-ANCHORS.json").read_text(encoding="utf-8"))
ashes_root = Path(anchors["ashes_checkout"])
assert anchors["ashes_repository_commit_pinned"] is False
checked_ashes = {}
for query in anchors["queries"]:
    if query["component"] != "ashes-urhrok":
        continue
    rel = query["public_source_path"]
    digest = hashlib.sha256((ashes_root / rel).read_bytes()).hexdigest()
    assert digest == query["file_sha256"], rel
    checked_ashes[rel] = digest

print(
    json.dumps(
        {
            "verified": True,
            "lua_loaded_files": list(FILES),
            "records": total_records,
            "changed_count": len(changed),
            "changed": changed,
            "line_invariants": line_invariants,
            "ashes_source_files": checked_ashes,
        },
        ensure_ascii=False,
        indent=2,
    )
)
