#!/usr/bin/env python3
"""P2 talent-name blind semantic discovery: run pi-review over all bundles."""
import json
import subprocess
import sys
import time
from pathlib import Path

MANIFEST = Path(".artifacts/i18n/runs/P2-talents-review/bundle-manifest.json")
OUT = Path(".artifacts/i18n/runs/P2-talents-review/progress.jsonl")
START = int(sys.argv[1]) if len(sys.argv) > 1 else 0
END = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9

manifest = json.loads(MANIFEST.read_text())
bundles = manifest["bundles"]

results = {}
if OUT.exists():
    for line in OUT.read_text().splitlines():
        rec = json.loads(line)
        results[rec["bundle_id"]] = rec

for b in bundles[START:END]:
    if b["bundle_id"] in results:
        continue
    rec = {"bundle_id": b["bundle_id"], "component": b["component"], "count": b["count"]}
    t0 = time.time()
    try:
        p = subprocess.run(
            ["python3", "tools/pi-review", "--bundle", b["path"]],
            capture_output=True, text=True, timeout=1300,
        )
        rec["elapsed"] = round(time.time() - t0, 1)
        if p.returncode == 0:
            rec["status"] = "ok"
        else:
            # 一次重试
            p2 = subprocess.run(
                ["python3", "tools/pi-review", "--force", "--bundle", b["path"]],
                capture_output=True, text=True, timeout=1300,
            )
            rec["elapsed_retry"] = round(time.time() - t0, 1)
            rec["status"] = "ok" if p2.returncode == 0 else "fail"
            if p2.returncode != 0:
                rec["error"] = (p2.stdout + p2.stderr)[-400:]
    except subprocess.TimeoutExpired:
        rec["status"] = "timeout"
    results[b["bundle_id"]] = rec
    with OUT.open("a") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    done = sum(1 for r in results.values() if r.get("status") == "ok")
    print(f"[{done}/{len(bundles)}] {b['bundle_id'][:12]} {rec['status']} "
          f"{rec.get('elapsed', rec.get('elapsed_retry','?'))}s", flush=True)

ok = sum(1 for r in results.values() if r.get("status") == "ok")
fail = [r for r in results.values() if r.get("status") != "ok"]
print(f"progress: ok={ok} fail={len(fail)} total={len(results)}")
for f in fail:
    print("FAIL:", f["bundle_id"], f.get("error", f.get("status")))
