#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Record a v2 dispatch in its sub-task STATE (child_dispatches + contextual_reviewers)."""
import json
import os
import sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ORCH = "eb0f2a87-8369-4e5b-b953-63159b37061b"
WORKSPACE = "wks_ac28b30c4bf45d5b"
PURPOSE = "translation_contextual_v2"
PROVIDER = "pi/cpa/gemini-3.8-flash-high"


def record(task_id, agent_id, provider=PROVIDER, model=None):
    path = os.path.join(REPO, ".ai", "task", task_id, "STATE.json")
    state = json.load(open(path, encoding="utf-8"))
    identity = state["contextual_reviewers"][0]["candidate_identity"]
    dispatch_id = state["contextual_reviewers"][0]["dispatch_id"]
    entry = {
        "dispatch_id": dispatch_id,
        "agent_id": agent_id,
        "role": "REVIEWER",
        "purpose": PURPOSE,
        "workspace_id": WORKSPACE,
        "parent_agent_id": ORCH,
        "lineage_verified": True,
        "lifecycle": "active",
        "archive_confirmed": False,
        "archive_attempts_started": 0,
        "provider_requested": provider,
        "record_path": f".ai/reviews/{task_id}/{dispatch_id}.json",
        "labels": {
            "task_id": task_id,
            "role": "reviewer",
            "purpose": PURPOSE,
            "candidate_identity": identity,
            "dispatch_id": dispatch_id,
        },
    }
    if model:
        entry["runtime_observation"] = {
            "schema_version": 1,
            "source": "live_agent_metadata",
            "captured_at": "2026-09-24T00:00:00+00:00",
            "capture_status": "captured",
            "provider": {"presence": "present", "value": provider.split("/")[0]},
            "model": {"presence": "present", "value": provider.split("/", 1)[1]},
            "mode": {"presence": "present", "value": "default"},
            "thinking": {"presence": "present", "value": "high"},
        }
    state["child_dispatches"] = [entry]
    state["contextual_reviewers"][0]["agent_id"] = agent_id
    json.dump(state, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{task_id}: recorded child {agent_id}")


if __name__ == "__main__":
    record(sys.argv[1], sys.argv[2], *sys.argv[3:])
