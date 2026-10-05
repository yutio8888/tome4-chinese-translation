"""STAGE-BREAKDOWN: catalog-file target changes per commit interval (LuaJIT load at both ends)."""
import json, subprocess, sys
sys.path.insert(0, "tools")
from i18nlib.config import load_manifest
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
paths = sorted({json.loads(l)["normalized_path"] for l in open("evidence/production-review-v2-lite/catalog/entries.jsonl")})
loader = LocaleLoader(LuaRuntime(load_manifest(version="tome-1.7.6", manifest_path=None)))
def load(c, p): return loader.load_bytes(subprocess.run(["git", "show", f"{c}:{p}"], capture_output=True, check=True).stdout, logical_path=p).translations
stages = [("9079821a", "a1d40dfc", "生硬描述 C 档修复包 12–16"), ("a1d40dfc", "e255bdfc", "C 档交叉复核修正"), ("e255bdfc", "aea17710", "C 档搁置项处理")]
out, union = [], {}
for a, b, label in stages:
    n, per = 0, {}
    for p in paths:
        x, y = load(a, p), load(b, p)
        k = 0
        for i, (r1, r2) in enumerate(zip(x, y)):
            if r1["target"] != r2["target"]:
                k += 1; union[(p, i)] = 1
        per[p] = k; n += k
    out.append({"from": a, "to": b, "content": label, "catalog_changes": n, "per_file": per})
res = {"stages": out, "sum_of_stages": sum(s["catalog_changes"] for s in out), "distinct_entries": len(union),
       "note": "Entries changed in more than one stage are counted once in distinct_entries. tome-items-vault.lua and tome-possessors.lua are outside the catalog."}
json.dump(res, open("evidence/quality/maintenance-reaudit-20261005/STAGE-BREAKDOWN.json", "w"), ensure_ascii=False, indent=1)
print([(s["content"], s["catalog_changes"]) for s in out], res["sum_of_stages"], res["distinct_entries"])
