#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Persist the reviewer's returned JSON as the raw evidence file.

`paseo logs` renders a transcript (prompt echo, tool calls, thoughts, prose and
sometimes a fenced or heredoc copy of the answer), so the transcript itself is
not "the exact returned bytes" that v2 section 5 binds. This keeps the
transcript as `raw-<dispatch>.transcript.txt` for diagnostics and writes the
reviewer's contract/identity/coverage-exact JSON object - byte for byte as it
appears in the transcript - to `raw-<dispatch>.txt`, then rebinds
`raw_output_sha256`.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harvest_v2 as H  # noqa: E402

REPO = HERE.parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task_ids", nargs="+")
    ap.add_argument("--dispatch-id", default="full-01")
    args = ap.parse_args()
    ok = 0
    for tid in args.task_ids:
        reviews = REPO / ".ai" / "reviews" / tid
        raw = reviews / f"raw-{args.dispatch_id}.txt"
        env = REPO / ".ai" / "task" / tid / f"CONTEXTUAL-ENVELOPE-{args.dispatch_id}.json"
        record_path = reviews / f"{args.dispatch_id}.json"
        envelope = json.loads(env.read_text(encoding="utf-8"))
        text = raw.read_text(encoding="utf-8", errors="replace")
        # if the file already is a single valid object, only rebind the hash
        direct = H.validate(text.strip(), envelope)
        if direct is not None:
            blob = text.strip()
            print(f"ALREADY-CLEAN      {tid}")
        else:
            found = [v for v in (H.validate(o, envelope) for o in H.objects(text)) if v]
            if not found:
                print(f"INVALID            {tid}  (no contract/identity/coverage-exact object)")
                continue
            # recover the verbatim text of the first valid object
            match = None
            for candidate in H.objects(text):
                if H.validate(candidate, envelope) is not None:
                    match = candidate
                    break
            blob = match
            transcript = reviews / f"raw-{args.dispatch_id}.transcript.txt"
            if not transcript.exists():
                transcript.write_text(text, encoding="utf-8")
            raw.write_text(blob, encoding="utf-8")
            print(f"FINALIZED          {tid}  bytes={len(blob.encode('utf-8'))}")
        digest = hashlib.sha256(raw.read_bytes()).hexdigest()
        if record_path.exists():
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["raw_output_path"] = f".ai/reviews/{tid}/raw-{args.dispatch_id}.txt"
            record["raw_output_sha256"] = digest
            record_path.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  rebound            {tid} sha256={digest[:16]}")
        ok += 1
    print(f"\nfinalized {ok}/{len(args.task_ids)}")


if __name__ == "__main__":
    main()
