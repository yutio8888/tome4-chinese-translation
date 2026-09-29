#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create the review task scaffolding (dispatch prompt + STATE) for the
re-split public v2 bundles, and refresh V2-BUNDLES-PUBLIC.json.

One bundle = one review_only v2 task with a single `full` dispatch, because
`review_only v2 只允许单一 full` (contract section 5).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))

PROMPT = (
    "任务：审核 input_path 全部冻结 revision；仅报有证据的语义、机制、术语、关系或跨条一致性问题；否则判 OK。\n"
    "输入：candidate_identity={identity}；input_path={path}。全程只读；可读输入、引用内容及 "
    "docs/paseo-translation-context-review-v2-contract.md 第六、七节；可沿调用链补查固定版本的相关公开源码；"
    "禁读其他 .ai/task/、.ai/reviews/ 和先前 finding。\n"
    "输出：仅返回第六节单一紧凑 JSON；按冻结顺序覆盖全部 revision 并回显 identity；补查依据按第七节记录；"
    "首字节{、末字节}，无其他文字、Markdown 或围栏。"
)

WORKSPACE_ID = "wks_ac28b30c4bf45d5b"
ORCHESTRATOR = "eb0f2a87-8369-4e5b-b953-63159b37061b"
PREVIOUS_ORCHESTRATOR = "330b8a33-ca74-4ea2-b931-89133e5edad1"
FIXED = "commit:624a67329fe2ad440c5b344785a9c73fcf22ae63"


def prompt_for(task_id, identity):
    # the contract template contains literal braces, so substitute by hand
    return (PROMPT.replace("{identity}", identity)
            .replace("{path}", f".ai/task/{task_id}/CONTEXTUAL-ENVELOPE-full-01.json"))


def state_for(task_id, identity, count, baseline, index_suffix):
    return {
        "schema_version": 5,
        "task_id": task_id,
        "mode": "review_only",
        "change_class": "standard",
        "review_contracts": ["translation_contextual_v2"],
        "state": "REVIEW",
        "review_phase": "REVIEW",
        "pending_review_contracts": ["translation_contextual_v2"],
        "completed_review_contracts": [],
        "cycle": 0,
        "max_cycles": 3,
        "workspace_id": WORKSPACE_ID,
        "orchestrator_agent_id": ORCHESTRATOR,
        "orchestration_transport": "cli",
        "baseline": {"commit": baseline, "patch": None, "copies_dir": None},
        "candidate_author_agent_id": None,
        "child_dispatches": [],
        "open_accepted_findings": [],
        "deferred_findings": [],
        "review_records": [],
        "senior_review_records": [],
        "final_validation_passed": False,
        "wait": None,
        "last_error": None,
        "updated_at": "2026-09-24T00:00:00+00:00",
        "run_origin": {
            "parent_task": "human-review-adjudication-20260923",
            "run": "PUBLIC (engine/boot/tome)",
            "fixed_source_identity": FIXED,
            "bundle_index": index_suffix,
            "bundle_revisions": count,
            "split_reason": "v1 requires echoing frozen source/target per revision (infeasible at scale); "
                            "v2 returns revision_key+verdict. review_only v2 allows one full, so the bundle is the task. "
                            "Bundles 04..28 were re-split under a bounded source+target character budget because the "
                            "original 18-revision slices produced envelopes up to 529 KB (production bundles stay <= ~80 KB).",
            "orchestrator_session": ORCHESTRATOR,
            "previous_orchestrator_session": PREVIOUS_ORCHESTRATOR,
            "orchestrator_note": "the 2026-09-24 system restart started a continuation ORCHESTRATOR session; new "
                                 "dispatches are direct children of this session, so its id is recorded here",
        },
        "contextual_reviewers": [
            {
                "role": "REVIEWER",
                "purpose": "translation_contextual_v2",
                "candidate_identity": identity,
                "dispatch_id": "full-01",
                "input_path": f".ai/task/{task_id}/CONTEXTUAL-ENVELOPE-full-01.json",
                "agent_id": None,
            }
        ],
    }


def main():
    bundles = json.load(open(os.path.join(HERE, "V2-BUNDLES-PUBLIC-NEW.json"), encoding="utf-8"))
    frozen = json.load(open(os.path.join(HERE, "V2-BUNDLES-PUBLIC.json"), encoding="utf-8"))
    out = {}
    for task_id, info in sorted(frozen.items()):
        if task_id in ("ctx2-pub-01", "ctx2-pub-02", "ctx2-pub-03"):
            out[task_id] = info
    baseline = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                              text=True, check=True).stdout.strip()
    for task_id, info in sorted(bundles.items()):
        identity = info["candidate_identity"]
        task_dir = os.path.join(REPO, ".ai", "task", task_id)
        text = prompt_for(task_id, identity)
        assert len(text.encode("utf-8")) <= 800, (task_id, len(text.encode("utf-8")))
        with open(os.path.join(task_dir, "PROMPT-full-01.txt"), "w", encoding="utf-8") as fh:
            fh.write(text)
        info = dict(info)
        info["prompt_bytes"] = len(text.encode("utf-8"))
        out[task_id] = info
        suffix = task_id[len("ctx2-pub-"):]
        state = state_for(task_id, identity, info["count"], baseline, suffix)
        with open(os.path.join(task_dir, "STATE.json"), "w", encoding="utf-8") as fh:
            json.dump(state, fh, ensure_ascii=False, indent=1)
        print(f"{task_id}: n={info['count']} prompt={info['prompt_bytes']}B")
    with open(os.path.join(HERE, "V2-BUNDLES-PUBLIC.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"bundles recorded: {len(out)}  revisions: {sum(b['count'] for b in out.values())}")


if __name__ == "__main__":
    main()
