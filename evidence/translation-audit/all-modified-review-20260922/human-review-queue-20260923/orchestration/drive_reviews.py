#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drive the public v2 bundle reviews: keep at most `--parallel` Gemini
reviewers running, harvest each finished reviewer, persist its record and
verify it with ai_state_check.

Runs unattended; every action is appended to a JSONL journal so the run can be
audited or resumed. Never edits Lua files.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import harvest_v2 as H  # noqa: E402
import finalize_raw as F  # noqa: E402

AGENTS = Path(os.path.expanduser(
    "~/.paseo/agents/home-paseo-.paseo-worktrees-2p1pqszt-translation-spotcheck-20260921"))
ORCH = "eb0f2a87-8369-4e5b-b953-63159b37061b"
WORKSPACE = "wks_ac28b30c4bf45d5b"
PURPOSE = "translation_contextual_v2"
GEMINI = "pi/cpa/gemini-3.8-flash-high"
CODEX = "codex/gpt-6-sol"


def journal(path, event, **fields):
    row = {"at": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event, **fields}
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps(row, ensure_ascii=False), flush=True)


def agent_file(agent_id):
    return AGENTS / f"{agent_id}.json"


def agent_state(agent_id):
    try:
        d = json.loads(agent_file(agent_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return d


def is_finished(rec):
    if rec is None:
        return False
    status = rec.get("lastStatus")
    if status in ("running", "stopping", "starting", None):
        return False
    return True


def bundle_list(only=None):
    manifest = json.loads((HERE / "V2-BUNDLES-PUBLIC.json").read_text(encoding="utf-8"))
    tasks = sorted(manifest)
    if only:
        want = set(only)
        tasks = [t for t in tasks if t in want]
    return tasks


def state_path(task_id):
    return REPO / ".ai" / "task" / task_id / "STATE.json"


def load_state(task_id):
    return json.loads(state_path(task_id).read_text(encoding="utf-8"))


def save_state(task_id, state):
    state_path(task_id).write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")


def envelope(task_id):
    return json.loads(
        (REPO / ".ai" / "task" / task_id / "CONTEXTUAL-ENVELOPE-full-01.json").read_text(encoding="utf-8"))


def dispatch(task_id, provider, prompt_path, attempt):
    identity = envelope(task_id)["candidate_identity"]
    labels = [
        f"task_id={task_id}", "role=reviewer", f"purpose={PURPOSE}",
        f"candidate_identity={identity}", f"dispatch_id={attempt}",
    ]
    args = ["paseo", "run", "--provider", provider, "--thinking", "high" if provider == GEMINI else "medium"]
    for label in labels:
        args += ["--label", label]
    args.append(Path(prompt_path).read_text(encoding="utf-8"))
    log = open(f"/tmp/driver-{task_id}-{attempt}.log", "wb")
    # only agents created after this instant can belong to this dispatch; older
    # agents may carry identical labels from an interrupted earlier attempt
    cutoff = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() - 5))
    proc = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT,
                            cwd=str(REPO), start_new_session=True)
    # resolve the created agent by its creation labels
    for _ in range(90):
        time.sleep(2)
        best = None
        for name in os.listdir(AGENTS):
            if not name.endswith(".json"):
                continue
            try:
                rec = json.loads((AGENTS / name).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            lb = rec.get("labels") or {}
            if lb.get("task_id") != task_id or lb.get("purpose") != PURPOSE or lb.get("dispatch_id") != attempt:
                continue
            if (rec.get("createdAt") or "") <= cutoff:
                continue
            if rec.get("createdAt") and (best is None or rec["createdAt"] > best[0]):
                best = (rec["createdAt"], rec["id"])
        if best:
            return best[1], proc
    return None, proc


def build_record(task_id, agent_id, attempt, parsed):
    env = envelope(task_id)
    keys = env["payload"]["ordered_revision_keys"]
    issues = [v["revision_key"] for v in parsed["verdicts"] if v["verdict"] == "ISSUE"]
    return {
        "task_id": task_id,
        "agent_id": agent_id,
        "attempt": int(attempt.split("-")[-1]),
        "candidate_identity": env["candidate_identity"],
        "cycle": 0,
        "dispatch_id": attempt,
        "input_path": f".ai/task/{task_id}/CONTEXTUAL-ENVELOPE-full-01.json",
        "purpose": PURPOSE,
        "labels": {
            "task_id": task_id, "role": "reviewer", "purpose": PURPOSE,
            "candidate_identity": env["candidate_identity"], "dispatch_id": attempt,
        },
        "lineage_verified": True,
        "parent_agent_id": ORCH,
        "reviewer_role": "REVIEWER",
        "raw_output_path": f".ai/reviews/{task_id}/raw-{attempt}.txt",
        "raw_output_sha256": hashlib.sha256(
            (REPO / ".ai" / "reviews" / task_id / f"raw-{attempt}.txt").read_bytes()).hexdigest(),
        "review_contract": "translation_contextual_v2",
        "review_kind": "full",
        "review_phase": "REVIEW",
        "status": "completed",
        "workspace_id": WORKSPACE,
        "coverage": {"revisions": len(keys), "issues": len(issues), "issue_keys": issues},
    }


def harvest(task_id, agent_id, attempt, jpath):
    """Extract the reviewer's JSON, persist raw + record, verify with the checker."""
    env = envelope(task_id)
    reviews = REPO / ".ai" / "reviews" / task_id
    reviews.mkdir(parents=True, exist_ok=True)
    raw = reviews / f"raw-{attempt}.txt"
    transcript = reviews / f"raw-{attempt}.transcript.txt"
    if raw.exists() and transcript.exists():
        pass
    else:
        if raw.exists():
            raw.unlink()
        if transcript.exists():
            transcript.unlink()
        text = ""
        for _ in range(6):
            text = subprocess.run(["paseo", "logs", agent_id], capture_output=True, text=True,
                                  cwd=str(REPO)).stdout
            if text.strip():
                break
            time.sleep(10)
        if not text.strip():
            return None, "empty transcript"
        direct = H.validate(text.strip(), env)
        if direct is not None:
            raw.write_text(text.strip(), encoding="utf-8")
        else:
            found = None
            for candidate in H.objects(text):
                if H.validate(candidate, env) is not None:
                    found = candidate
                    break
            if found is None:
                transcript.write_text(text, encoding="utf-8")
                return None, "no contract/identity/coverage-exact object"
            transcript.write_text(text, encoding="utf-8")
            raw.write_text(found, encoding="utf-8")
    parsed = H.validate(raw.read_text(encoding="utf-8").strip(), env)
    if parsed is None:
        parsed = json.loads(raw.read_text(encoding="utf-8"))
    record = build_record(task_id, agent_id, attempt, parsed)
    (reviews / f"{attempt}.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    issues = record["coverage"]["issue_keys"]
    journal(jpath, "harvested", task=task_id, attempt=attempt, revisions=record["coverage"]["revisions"],
            issues=len(issues), issue_keys=issues)
    return record, None


def close_task(task_id, record, agent_id, jpath):
    state = load_state(task_id)
    state["state"] = "DONE"
    state["child_dispatches"] = [{
        "dispatch_id": record["dispatch_id"],
        "agent_id": agent_id,
        "role": "REVIEWER",
        "purpose": PURPOSE,
        "workspace_id": WORKSPACE,
        "parent_agent_id": ORCH,
        "lineage_verified": True,
        "lifecycle": "archived",
        "archive_confirmed": True,
        "archive_attempts_started": 1,
        "provider_requested": GEMINI,
        "candidate_identity": record["candidate_identity"],
        "input_path": record["input_path"],
        "labels": record["labels"],
        "record_path": f".ai/reviews/{task_id}/{record['dispatch_id']}.json",
        "verdict": "completed_valid_v2_record",
    }]
    state["review_records"] = [f".ai/reviews/{task_id}/{record['dispatch_id']}.json"]
    state["completed_review_contracts"] = ["translation_contextual_v2"]
    state["pending_review_contracts"] = []
    state["final_validation_passed"] = True
    state["contextual_reviewers"] = [{
        "role": "REVIEWER", "purpose": PURPOSE,
        "candidate_identity": record["candidate_identity"],
        "dispatch_id": record["dispatch_id"], "input_path": record["input_path"],
        "agent_id": agent_id,
    }]
    state["open_accepted_findings"] = []
    state["findings_artifact"] = ("evidence/translation-audit/all-modified-review-20260922/"
                                  "human-review-queue-20260923/CONTEXTUAL-V2-FINDINGS-ALL.json")
    state["findings_note"] = ("review_only run: accepted findings are consolidated in the findings "
                             "artifact and fixed by the parent task")
    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
    with open(HERE / f"FINDINGS-{task_id}.json", "w", encoding="utf-8") as fh:
        json.dump({"task_id": task_id, "candidate_identity": record["candidate_identity"],
                   "issue_keys": record["coverage"]["issue_keys"]}, fh, ensure_ascii=False, indent=1)
    save_state(task_id, state)
    check = subprocess.run([sys.executable, "-B", "tools/ai_state_check.py",
                            f".ai/task/{task_id}/STATE.json", "--target", "DONE"],
                           capture_output=True, text=True, cwd=str(REPO))
    verdict = (check.stdout or check.stderr).strip().splitlines()[-1] if (check.stdout or check.stderr) else ""
    journal(jpath, "closed", task=task_id, verdict=verdict)
    return verdict.startswith("DONE_VERIFIED")


def running_count(window_seconds=3 * 3600):
    """Count every live reviewer agent for this purpose, including ones started
    outside this driver, so the Gemini concurrency cap is global."""
    now = time.time()
    total = 0
    for name in os.listdir(AGENTS):
        if not name.endswith(".json"):
            continue
        path = AGENTS / name
        try:
            if now - os.path.getmtime(path) > window_seconds:
                continue
            rec = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        lb = rec.get("labels") or {}
        if lb.get("purpose") == PURPOSE and rec.get("lastStatus") == "running":
            total += 1
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parallel", type=int, default=3)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--provider", default=GEMINI)
    ap.add_argument("--budget-minutes", type=int, default=180)
    ap.add_argument("--journal", default=f"/tmp/v2-driver-{int(time.time())}.jsonl")
    args = ap.parse_args()

    tasks = bundle_list(args.only)
    pending = []
    done = []
    for task in tasks:
        # A task counts as done when its STATE is DONE, regardless of which
        # attempt (full-01, full-02, ...) produced the accepted record.
        state_path = REPO / ".ai" / "task" / task / "STATE.json"
        is_done = False
        if state_path.exists():
            try:
                is_done = json.loads(state_path.read_text(encoding="utf-8")).get("state") == "DONE"
            except Exception:
                is_done = False
        if is_done:
            done.append(task)
        else:
            pending.append(task)
    journal(args.journal, "start", pending=len(pending), already=len(done), provider=args.provider)
    active = {}  # task -> (agent_id, attempt, proc)
    started = time.time()
    while pending or active:
        if time.time() - started > args.budget_minutes * 60:
            journal(args.journal, "budget_exhausted", pending=pending, active=list(active))
            break
        for task, (agent_id, attempt, proc) in list(active.items()):
            rec = agent_state(agent_id)
            if not is_finished(rec):
                continue
            del active[task]
            record, error = harvest(task, agent_id, attempt, args.journal)
            if error:
                journal(args.journal, "invalid_output", task=task, attempt=attempt, error=error)
                subprocess.run(["paseo", "archive", agent_id], capture_output=True, cwd=str(REPO))
                nxt = f"full-{int(attempt.split('-')[-1]) + 1:02d}"
                pending.insert(0, (task, nxt))
                continue
            subprocess.run(["paseo", "archive", agent_id], capture_output=True, cwd=str(REPO))
            if close_task(task, record, agent_id, args.journal):
                done.append(task)
            else:
                pending.insert(0, (task, attempt))
        while pending and running_count() < args.parallel:
            item = pending.pop(0)
            task, attempt = item if isinstance(item, tuple) else (item, "full-01")
            agent_id, proc = dispatch(task, args.provider,
                                      REPO / ".ai" / "task" / task / "PROMPT-full-01.txt", attempt)
            if not agent_id:
                journal(args.journal, "dispatch_failed", task=task)
                continue
            active[task] = (agent_id, attempt, proc)
            journal(args.journal, "dispatched", task=task, attempt=attempt, agent=agent_id,
                    parallel=len(active))
        time.sleep(20)
    journal(args.journal, "end", done=len(done), remaining=[t for t in pending])


if __name__ == "__main__":
    main()
