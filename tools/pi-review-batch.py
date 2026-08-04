#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""并行批量 Pi 审核驱动：并发执行 tools/pi-review，失败自动重试，进度汇报。

用法：
  python3 -B tools/pi-review-batch.py --index <review-index.json> [--workers 4] [--limit N] [--skip M] [--retries 2]

- 并发 worker 数量由 --workers 控制（默认 4；provider 限速时降低）。
- 每个 bundle 单独调用 tools/pi-review（--timeout 1200 保持不变）。
- 非零退出或空响应自动重试 --retries 次（间隔递增）。
- 已完成的 bundle（runs/*-pi-review/review.json 存在且 bundle_id 匹配）自动跳过。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

signal.alarm(3600 * 4)

ROOT = Path(__file__).resolve().parents[1]
PI_REVIEW = ROOT / "tools" / "pi-review"
RUNS_GLOB = str(ROOT / ".artifacts" / "i18n" / "runs" / "*pi-review" / "review.json")

import queue  # noqa: E402

class Progress:
    def __init__(self, total: int) -> None:
        self.total = total
        self.done = 0
        self.ok = 0
        self.failed = 0
        self._lock = queue.SimpleQueue()

    def tick(self, ok: bool) -> None:
        self._lock.put(ok)

    def pump(self) -> None:
        while not self._lock.empty():
            ok = self._lock.get()
            self.done += 1
            if ok:
                self.ok += 1
            else:
                self.failed += 1


def already_done(bundle_id: str) -> bool:
    for rj in glob.glob(RUNS_GLOB):
        try:
            with open(rj, encoding="utf-8") as h:
                data = json.load(h)
            if data.get("bundle_id") == bundle_id:
                return True
        except (OSError, json.JSONDecodeError):
            continue
    return False


def run_one(bundle_path: str, retries: int, progress: Progress, force: bool = False) -> tuple[str, bool]:
    bundle_id = Path(bundle_path).stem
    if not force and already_done(bundle_id):
        progress.tick(True)
        return bundle_id, True
    delay = 10
    cmd = [str(PI_REVIEW), "--bundle", bundle_path]
    if force:
        cmd.append("--force")
    for attempt in range(retries + 1):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1250,
            )
            if result.returncode == 0:
                progress.tick(True)
                return bundle_id, True
            err = (result.stderr or result.stdout or "").strip()
            if "empty response" in err or "validation failed" in err:
                print(f"  retry {bundle_id[:12]} (attempt {attempt + 1}): {err[:80]}")
                time.sleep(delay)
                delay *= 2
                continue
        except subprocess.TimeoutExpired:
            print(f"  timeout {bundle_id[:12]} (attempt {attempt + 1})")
            time.sleep(delay)
            delay *= 2
            continue
        except OSError as exc:
            print(f"  error {bundle_id[:12]}: {exc}")
            break
    progress.tick(False)
    return bundle_id, False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--skip", type=int, default=0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--force", action="store_true",
                        help="bypass cache and force fresh Pi review for every bundle")
    args = parser.parse_args()

    index = json.loads(args.index.read_text(encoding="utf-8"))
    bundles = [b for b in index["bundles"] if b.get("path")]
    bundles = bundles[args.skip:]
    if args.limit:
        bundles = bundles[: args.limit]
    total = len(bundles)
    if total == 0:
        print("no bundles to review")
        return 0

    print(f"batch: {total} bundles, workers={args.workers}, retries={args.retries}")
    progress = Progress(total)
    results: dict[str, bool] = {}
    started = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run_one, b["path"], args.retries, progress, args.force): b["bundle_id"]
            for b in bundles
        }
        for future in as_completed(futures):
            bundle_id, ok = future.result()
            results[bundle_id] = ok
            progress.pump()
            elapsed = time.time() - started
            rate = progress.done / elapsed if elapsed > 0 else 0
            print(
                f"[{progress.done}/{total}] ok={progress.ok} fail={progress.failed} "
                f"rate={rate:.2f}/s ({bundle_id[:12]} {'OK' if ok else 'FAIL'})"
            )

    failed = [bid for bid, ok in results.items() if not ok]
    print(f"\n完成: {progress.done}/{total}，成功 {progress.ok}，失败 {len(failed)}")
    for bid in failed:
        print(f"  FAILED: {bid}")
    summary = {
        "index": str(args.index),
        "total": total,
        "ok": progress.ok,
        "failed": failed,
    }
    out = ROOT / ".artifacts" / "i18n" / "pi-batch-summary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"summary: {out}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
