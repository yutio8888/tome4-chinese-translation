"""Stratified quality sample (2026-11-20, post-v0.3.15): component x length bin, fixed seed; writes sample.json."""
import collections
import json
import os
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import lite_review as L

SEED = 20261120
QUOTA = {
    "mod-tome.lua": 60,
    "tome-orcs.lua": 20,
    "tome-cults.lua": 15,
    "tome-ashes-urhrok.lua": 12,
    "engine.lua": 13,
}
SHARE = {"S": 0.35, "M": 0.45, "L": 0.20}
MAXLEN = 1500


def lbin(s: str) -> str:
    return "S" if len(s) <= 30 else "M" if len(s) <= 200 else "L"


def load_dead_keys():
    dead = set()
    p = ROOT / "evidence/quality/dead-key-scan-20261111/pairs.json"
    for pr in json.loads(p.read_text(encoding="utf-8")):
        x = pr["dead"]
        dead.add((x["file"], x["en"], str(x["tag"])))
    return dead


def is_dead(u, dead_set):
    o = u["occurrence"]
    if (o["translation_path"], o["source"], str(o["source_tag"])) in dead_set:
        return True
    return o["translation_path"] == "engine.lua" and o["source"].startswith("following chain")


def load_addon_locale_keys():
    """Return set of source keys shipped in v0.3.15 addon zh_hans.lua."""
    addon_locale = Path("/workspace/tome4-chn-mod/data/locales/zh_hans.lua")
    if not addon_locale.exists():
        return set()
    lua_code = """
local keys = {}
function locale() end
function section() end
function t(src, dst, tag)
  if type(src) == 'string' and type(dst) == 'string' then
    keys[src] = dst
  end
end
dofile(assert(os.getenv("ADDON_LOCALE")))
for k, _ in pairs(keys) do
  io.write(k:gsub("\\r", "\\\\r"):gsub("\\n", "\\\\n"), "\\n")
end
"""
    env = dict(os.environ, ADDON_LOCALE=str(addon_locale))
    res = subprocess.run(
        ["/usr/bin/luajit", "-e", lua_code],
        env=env,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=True,
    )
    return set(res.stdout.splitlines())


def main():
    us = L.units()
    dead_set = load_dead_keys()
    live = []
    dead_excluded = 0
    for u in us:
        if is_dead(u, dead_set):
            dead_excluded += 1
            continue
        live.append(u)

    addon_keys = load_addon_locale_keys()
    prev_1119_path = ROOT / "evidence/quality/sample-quality-20261119/sample.json"
    prev_1119_ids = set()
    if prev_1119_path.exists():
        prev_1119_ids = {x["unit_id"] for x in json.loads(prev_1119_path.read_text(encoding="utf-8"))["items"]}

    rng = random.Random(SEED)
    picked = []
    stratum_counts = {}
    for path, n in QUOTA.items():
        pool = sorted(
            (u for u in live if u["occurrence"]["translation_path"] == path),
            key=L.order_key,
        )
        for b, share in SHARE.items():
            cand = [
                u
                for u in pool
                if lbin(u["occurrence"]["source"]) == b
                and len(u["occurrence"]["source"]) <= MAXLEN
            ]
            k = min(len(cand), round(n * share))
            stratum_counts[f"{path}:{b}"] = {"pool": len(cand), "picked": k}
            picked += rng.sample(cand, k)

    items = []
    for i, u in enumerate(picked, 1):
        o = u["occurrence"]
        text, loc = L.source_text(o["section"])
        hits = L.locate(text, o["source"])
        ctx = None
        if hits:
            lines = text.splitlines()
            h = hits[0]
            ctx = "\n".join(
                f"{k}: {lines[k - 1][:240]}"
                for k in range(max(1, h - 5), min(len(lines), h + 5) + 1)
            )
        src_escaped = o["source"].replace("\r", "\\r").replace("\n", "\\n")
        in_addon = src_escaped in addon_keys
        entry = {
            "n": i,
            "unit_id": u["unit_id"][:12],
            "file": o["translation_path"],
            "length_bin": lbin(o["source"]),
            "in_addon_delta": in_addon,
            "section": o["section"],
            "source_tag": o["source_tag"],
            "source": o["source"],
            "target": o["target"],
            "source_location": f"{loc}:{hits[0]}" if hits else loc,
            "source_context": ctx,
        }
        if o.get("args_order"):
            entry["args_order"] = o["args_order"]
        items.append(entry)

    overlap = sum(1 for x in items if x["unit_id"] in prev_1119_ids)
    out = {
        "date": "2026-11-20",
        "release_version": "0.3.15",
        "source_commit": "f6e64afc0038ba9920233f4aa55250b484664a84",
        "seed": SEED,
        "quota": QUOTA,
        "share": SHARE,
        "maxlen": MAXLEN,
        "population_total": len(us),
        "dead_excluded": dead_excluded,
        "population_live": len(live),
        "overlap_with_20261119": overlap,
        "in_addon_delta_count": sum(1 for x in items if x["in_addon_delta"]),
        "stratum_counts": stratum_counts,
        "items": items,
    }
    (HERE / "sample.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(
        f"picked={len(items)} chars={sum(len(x['source']) for x in items)} "
        f"dead_excluded={dead_excluded} overlap_20261119={overlap} "
        f"in_addon_delta={out['in_addon_delta_count']}"
    )
    print("by_file:", dict(collections.Counter(x["file"] for x in items)))
    print("by_bin:", dict(collections.Counter(x["length_bin"] for x in items)))
    print("by_tag:", dict(collections.Counter(str(x["source_tag"]) for x in items).most_common(12)))


if __name__ == "__main__":
    main()
