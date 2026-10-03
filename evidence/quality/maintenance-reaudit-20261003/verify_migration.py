"""CATALOG-CHANGE-VERIFICATION: every migration row is a target change on an unchanged logical entry,
and the multiset of (path, section, source, tag, old, new) equals the independent BASE..HEAD diff."""
import json, subprocess, collections, sys
W = ".artifacts/i18n/reaudit-20261003"
m = json.load(open(f"{W}/migration.json"))
old = {json.loads(l)["entry_revision_identity"]: json.loads(l) for l in subprocess.run(["git", "show", "HEAD:evidence/production-review-v2-lite/catalog/entries.jsonl"], capture_output=True, text=True, check=True).stdout.splitlines()}
new = {json.loads(l)["entry_revision_identity"]: json.loads(l) for l in open("evidence/production-review-v2-lite/catalog/entries.jsonl")}
exp = json.load(open(f"{W}/expected-changes.json"))
disp = collections.Counter(r["disposition"] for r in m["rows"]); reasons = collections.Counter(r.get("reason") for r in m["rows"])
got = collections.Counter()
for r in m["rows"]:
    assert r["disposition"] == "revision_changed", r
    a, b = old[r["old_entry_revision_identity"]], new[r["new_entry_revision_identity"]]
    assert r["old_logical_entry_identity"] == r["new_logical_entry_identity"] == a["logical_entry_identity"] == b["logical_entry_identity"]
    for k in ("normalized_path", "section", "source", "source_tag", "component"): assert a[k] == b[k], k
    assert a["target"] != b["target"] or a["risk"]["args_order"] != b["risk"]["args_order"]
    got[(b["normalized_path"], b["section"], b["source"], b["source_tag"], a["target"], b["target"])] += 1
want = collections.Counter((c["path"], c["section"], c["source"], c["source_tag"], c["old"], c["new"]) for c in exp["changes"])
res = {"verified": got == want, "migration_id": m["migration_id"], "old_catalog_id": m["old_catalog_id"], "new_catalog_id": m["new_catalog_id"],
       "base_commit": m["base_commit"], "dispositions": dict(disp), "reasons": dict(reasons), "revision_changed": sum(got.values()),
       "expected_from_lua_diff": {"base": exp["base"], "head": exp["head"], "total": exp["total"], "per_file": exp["per_file"]},
       "only_in_migration": len(got - want), "only_in_lua_diff": len(want - got),
       "entries": {"old": len(old), "new": len(new)}, "outside_catalog": {"tome-possessors.lua": "not in catalog files", "tome-items-vault.lua": "not in catalog files"}}
print(json.dumps(res, ensure_ascii=False, indent=2))
sys.exit(0 if res["verified"] else 1)
