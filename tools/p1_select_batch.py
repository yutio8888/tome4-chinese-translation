#!/usr/bin/env python3
"""Freeze a bounded P1 quality-check batch from a current revision inventory.

The batch is selected deterministically from `tools/i18n quality inventory`
output, which is treated as a read-only ordering source. This script makes no
quality judgement: risk flags only decide which revisions get looked at, never
whether a revision is defective. It never touches canonical Lua and never calls
a provider.

See docs/p1-execution-plan.md sections 3 and 4.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
QUALITY_RUNS = REPO_ROOT / ".artifacts" / "i18n" / "quality" / "runs"
OUT_DIR = REPO_ROOT / ".artifacts" / "i18n" / "p1-batches"

ITEM_FIELDS = (
    "revision_id",
    "revision_uid",
    "tu_uid",
    "section",
    "source_tag",
    "source",
    "target",
    "args_order",
    "profile",
    "risk_flags",
)


def latest_inventory_dir() -> pathlib.Path:
    candidates = sorted(QUALITY_RUNS.glob("*-inventory"))
    if not candidates:
        raise SystemExit(
            "no inventory run found; run `python3 -B tools/i18n quality inventory` first"
        )
    return candidates[-1]


def load_manifest(run_dir: pathlib.Path) -> dict:
    path = run_dir / "inventory-manifest.json"
    if not path.exists():
        raise SystemExit(f"missing inventory manifest: {path}")
    return json.loads(path.read_text())


def pinned_commit(version: str) -> str:
    path = REPO_ROOT / "i18n" / "versions" / f"{version}.json"
    if not path.exists():
        raise SystemExit(f"missing version manifest: {path}")
    manifest = json.loads(path.read_text())
    try:
        return manifest["repositories"]["engine"]["commit"]
    except (KeyError, TypeError):
        raise SystemExit(f"{path} has no repositories.engine.commit")


def matches(entry: dict, args: argparse.Namespace) -> bool:
    if entry.get("component") != args.component:
        return False
    if args.profile and entry.get("profile") != args.profile:
        return False
    flags = set(entry.get("risk_flags") or ())
    if not flags & set(args.risk_flag):
        return False
    if flags & set(args.exclude_risk_flag or ()):
        return False
    if len(entry.get("source") or "") < args.min_source_len:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", default="p1-b1-mechanics-numeric")
    parser.add_argument(
        "--inventory-dir",
        type=pathlib.Path,
        help="inventory run directory (default: newest under .artifacts/i18n/quality/runs)",
    )
    parser.add_argument("--component", default="tome")
    parser.add_argument("--profile", default="mechanics")
    parser.add_argument(
        "--risk-flag",
        action="append",
        default=None,
        help="risk flag to require; repeatable, matched as OR "
        "(default: source-has-number-or-unit)",
    )
    parser.add_argument(
        "--exclude-risk-flag",
        action="append",
        default=None,
        help="risk flag that disqualifies an entry; repeatable. Use this to isolate a "
        "dimension from one it co-occurs with, so a batch tests that dimension rather "
        "than the overlap.",
    )
    parser.add_argument("--min-source-len", type=int, default=40)
    parser.add_argument("--size", type=int, default=24)
    parser.add_argument(
        "--seed-label",
        default="tome4-p1-b1",
        help="seed prefix; combined with inventory and source identity",
    )
    parser.add_argument("--out", type=pathlib.Path)
    args = parser.parse_args()

    if args.risk_flag is None:
        args.risk_flag = ["source-has-number-or-unit"]

    run_dir = args.inventory_dir or latest_inventory_dir()
    manifest = load_manifest(run_dir)
    inventory_sha256 = manifest["inventory_sha256"]
    version = manifest["version"]
    source_commit = pinned_commit(version)

    inventory_path = run_dir / "inventory.jsonl"
    pool = []
    with inventory_path.open(encoding="utf-8") as handle:
        for line in handle:
            entry = json.loads(line)
            if matches(entry, args):
                pool.append(entry)

    if len(pool) < args.size:
        raise SystemExit(
            f"pool has only {len(pool)} entries, cannot select {args.size}"
        )

    # Deterministic and Python-version independent: order the pool by
    # revision_id, then take the entries whose seeded digest sorts lowest.
    pool.sort(key=lambda e: e["revision_id"])
    seed_str = f"{args.seed_label}|{inventory_sha256}|{source_commit}"

    def digest(entry: dict) -> str:
        payload = f"{seed_str}|{entry['revision_id']}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    selected = sorted(pool, key=lambda e: (digest(e), e["revision_id"]))[: args.size]
    selected.sort(key=lambda e: (e["section"], e["revision_id"]))

    batch = {
        "batch_id": args.batch_id,
        "plan": "docs/p1-execution-plan.md",
        "purpose": "bounded quality check over already-translated revisions",
        "note": (
            "Risk flags only order candidates for review. No entry in this batch "
            "is asserted to be defective; host source verification decides."
        ),
        "version": version,
        "source_commit": source_commit,
        "inventory_run": str(run_dir.relative_to(REPO_ROOT)),
        "inventory_sha256": inventory_sha256,
        "manifest_sha256": manifest["manifest_sha256"],
        "risk_rule_version": manifest["risk_rule_version"],
        "profile_classifier_version": manifest["profile_classifier_version"],
        "filter": {
            "component": args.component,
            "profile": args.profile,
            "risk_flags_any": sorted(args.risk_flag),
            "risk_flags_excluded": sorted(args.exclude_risk_flag or ()),
            "min_source_len": args.min_source_len,
        },
        "pool_size": len(pool),
        "size": args.size,
        "sort_key": "revision_id",
        "selection": "sha256(seed_str|revision_id) ascending",
        "seed_str": seed_str,
        "items": [
            {field: entry.get(field) for field in ITEM_FIELDS} for entry in selected
        ],
    }

    out_path = args.out or (OUT_DIR / f"{args.batch_id}.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(batch, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )

    print(f"OK  batch {args.batch_id}  pool={len(pool)}  selected={len(selected)}")
    print(f"    version={version}  source_commit={source_commit[:12]}")
    print(f"    inventory_sha256={inventory_sha256[:16]}")
    print(f"Output: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
