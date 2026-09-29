"""Read-only guards and orchestration record updates for this research batch."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guards():
    base = read("BASELINE.json")
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == base["head"]
    assert all(sha(Path(p)) == h for p, h in base["locale_sha256"].items())
    assert sha(ROOT.parent.parent / "STATE.json") == base["campaign_state_sha256"]
    assert sha(ROOT.parent.parent / "inventory.json") == base["inventory_sha256"]
    previous = ROOT.parent / base["prior_experiment"]
    assert all(sha(previous / p) == h for p, h in base["prior_experiment_files_sha256"].items())
    assert all(sha(ROOT / p) == h for p, h in read("FREEZE.json")["files_sha256"].items())
    return True


def harvest(dispatch_id, snapshot_file):
    guards()
    state = read("STATE.json")
    child = next(c for c in state["child_dispatches"] if c["dispatch_id"] == dispatch_id)
    snapshot = read(snapshot_file)["structuredContent"]["snapshot"]
    assert snapshot["id"] == child["agent_id"] and not snapshot.get("activeTurn")
    report = (ROOT / "reports" / (dispatch_id + ".md")).read_text()
    ids = re.findall(r"^\|\s*(?:\*\*)?(entry-\d{5})(?:\*\*)?\s*\|", report, re.M)
    expected = [e["audit_id"] for e in read("entries.json")]
    child.update(lifecycle="terminal", terminal_observation=snapshot,
                 coverage=len(ids), table_coverage_valid=ids == expected,
                 report_sha256=hashlib.sha256(report.encode()).hexdigest())
    child["archive_attempts_started"] += 1
    assert child["archive_attempts_started"] <= 2
    write("STATE.json", state)
    print(json.dumps({"coverage": len(ids), "table_valid": ids == expected}))


def archive(dispatch_id, snapshot_file):
    state = read("STATE.json")
    child = next(c for c in state["child_dispatches"] if c["dispatch_id"] == dispatch_id)
    snapshot = read(snapshot_file)["structuredContent"]["snapshot"]
    assert snapshot["id"] == child["agent_id"] and snapshot.get("archivedAt")
    child.update(lifecycle="archived", archive_confirmed=True, archived_at=snapshot["archivedAt"])
    write("STATE.json", state)


if __name__ == "__main__":
    if sys.argv[1] == "guards":
        print("guards passed" if guards() else "failed")
    elif sys.argv[1] == "harvest":
        harvest(*sys.argv[2:])
    elif sys.argv[1] == "archive":
        archive(*sys.argv[2:])

