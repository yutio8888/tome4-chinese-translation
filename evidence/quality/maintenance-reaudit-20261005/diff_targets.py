"""Independent expectation for the migration: per catalog file, compare loaded translation
records at BASE vs HEAD (same order, same source/section/tag) and list changed targets."""
import json, subprocess, sys
sys.path.insert(0, "tools")
from i18nlib.config import load_manifest
from i18nlib.runtime import LuaRuntime
from i18nlib.locale_model import LocaleLoader
BASE, HEAD = sys.argv[1], sys.argv[2]
cat = json.load(open("evidence/production-review-v2-lite/catalog/manifest.json"))
paths = sorted({json.loads(l)["normalized_path"] for l in open("evidence/production-review-v2-lite/catalog/entries.jsonl")})
loader = LocaleLoader(LuaRuntime(load_manifest(version="tome-1.7.6", manifest_path=None)))
out, summary = [], {}
for p in paths:
    a, b = (loader.load_bytes(subprocess.run(["git", "show", f"{c}:{p}"], capture_output=True, check=True).stdout, logical_path=p).translations for c in (BASE, HEAD))
    key = lambda r: (r.get("section"), r["source"], r.get("source_tag"))
    assert [key(r) for r in a] == [key(r) for r in b], f"record order/identity changed in {p}"
    n = 0
    for x, y in zip(a, b):
        if x["target"] != y["target"] or x.get("args_order") != y.get("args_order"):
            n += 1; out.append({"path": p, "section": y.get("section"), "source": y["source"], "source_tag": y.get("source_tag"), "old": x["target"], "new": y["target"]})
    summary[p] = n
json.dump({"base": BASE, "head": HEAD, "per_file": summary, "total": len(out), "changes": out}, open(".artifacts/i18n/reaudit-20261005/expected-changes.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(summary), "total", len(out))
