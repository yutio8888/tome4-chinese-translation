#!/usr/bin/env python3
"""Run the lightweight guard for active, runtime-neutral Paseo contracts."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ROLE_FILES = (
    ".ai/roles/executor.md",
    ".ai/roles/orchestrator.md",
    ".ai/roles/reviewer.md",
    ".ai/roles/scout.md",
    ".ai/roles/senior-reviewer.md",
)
CONTRACT_FILES = (
    "docs/paseo-orchestration-v2-contract.md",
    "docs/paseo-translation-context-review-v1-contract.md",
)
ACTIVE_FILES = ("AGENTS.md", *ROLE_FILES, *CONTRACT_FILES)

# These complete normative clauses keep the recovery contract load-bearing.
# They are intentionally shared only by the three documents that define
# orchestration behavior; field-name presence or a free-standing label is not
# sufficient coverage.
ROUTING_PROVENANCE_MARKERS = (
    "Before selecting any reviewer profile, ORCHESTRATOR must freeze the implementation candidate, re-enumerate the task's allowed changed paths, and persist candidate_author_agent_id in the task-scoped `.ai/task/<task_id>/STATE.json` at that freeze/path-re-enumeration event.",
    "The persisted candidate_author_agent_id must point to the latest accepted output that was produced or materially changed by the current task's lineage-verified EXECUTOR, not to an author inferred from another task's STATE.",
    "When the candidate changes, ORCHESTRATOR must recompute candidate_author_agent_id before the new review dispatch; it is immutable within a freeze, and ORCHESTRATOR must not traverse another task's STATE to invent it.",
    "candidate_author_agent_id is null for review-only work and for an implement candidate that predates any managed EXECUTOR.",
    "The immutable per-dispatch author pointer is copied to every candidate-bound reviewer dispatch and cannot be rewritten within that dispatch; it is excluded from candidate_ref, candidate_identity, review JSON, and review-contract identity.",
    "After ambiguous-create reconciliation or recovery, ORCHESTRATOR must re-resolve author_provider_resolution before using the dispatch, and a temporarily missing enum alone must not force WAIT_USER.",
    "not_applicable is used for review-only work, implement candidates predating any managed EXECUTOR, and scope_audit with no frozen code candidate.",
    "Only the corresponding reviewer entry in STATE child_dispatches records author_provider_resolution=verified|unavailable|not_applicable; review JSON excludes this enum, which is recorded only after unambiguous child creation or adoption and re-resolved before using a recovered reviewer dispatch.",
    "Before consuming the transport's explicit provider, ORCHESTRATOR must query live Paseo metadata including archived agents and verify the author agent id, workspace, task/role labels, parent lineage, and EXECUTOR role.",
    "The same-provider budget exception is allowed only when the author-provider resolution is verified; unavailable resolution remains a soft preference failure.",
    "If the author record is missing, any of the author agent id, workspace, task/role labels, parent lineage, or EXECUTOR role checks fails, or the explicit provider is missing or differently represented, retry the lookup once, then record author_provider_resolution=unavailable without inferring a provider.",
    "Operational author_provider_resolution and model_diversity_verified fields are excluded from runtime tuples, candidate identity, review-contract identity, review JSON, and offline STATE-checker closure predicates.",
    "At creation of the second reviewer, ORCHESTRATOR must obtain both live exact model identities, verify exact inequality, and only then persist literal `true` for model_diversity_verified on both reviewer dispatch entries.",
    "When paired reviewer exact model identities collide, archive the second child before creating a fresh retry child, preserving the role, purpose, workspace, lineage, and candidate binding.",
    "If either exact model identity remains unavailable after one retry, enter `WAIT_USER` and do not infer identity from provider, profile, title, memory, or enum.",
    "If a second reviewer exists or was unambiguously adopted but either `model_diversity_verified` proof is missing or partial, re-resolve both exact model identities once; persist literal `true` on both entries when they differ, archive the second child and fresh-retry on collision, and enter `WAIT_USER` if either identity remains unavailable.",
)

STOP_ARCHIVE_MARKERS = (
    "A child counts as archived only when its normalized lifecycle is `archived` and `archive_confirmed` is literal `true`.",
)

# Contextual anchor provenance is an ORCHESTRATOR-only input preflight. These
# complete clauses deliberately live outside the reviewer-visible seven-key
# contextual contract.
CONTEXTUAL_ANCHOR_PREFLIGHT_MARKERS = (
    "Before freezing or hashing a translation_contextual_v1 payload, ORCHESTRATOR must run the deterministic offline contextual-anchor preflight with the task-scoped `.ai/task/<task_id>/SCOPE.json` and the exact seven-key draft payload.",
    "The task-scoped SCOPE.json must declare only workspace-relative ordinary allowed files plus file, section_path, and ordered actual chapter-title anchors; unsafe, duplicate, missing, or ambiguous declarations fail closed.",
    "Each declared anchor window begins at its actual chapter-title t(...) call and ends at the earliest later actual chapter title, later section marker, or EOF, so undeclared titles still bound the window.",
    "ORCHESTRATOR may freeze the payload only after every translation_snapshot source is proven to be the decoded first argument of a real t(...) call inside a declared anchor window; the preflight adds nothing to the payload, candidate_identity, review JSON, or STATE closure identity.",
)

REQUIRED_MARKERS = {
    "AGENTS.md": (
        "role",
        "purpose",
        "WAIT_USER",
        "child_dispatches",
        "archive_confirmed",
        "明确回退",
        "archive_confirmed=true",
        "WAIT_USER",
    ),
    ".ai/roles/executor.md": ("role=executor",),
    ".ai/roles/orchestrator.md": (
        "ORCHESTRATOR",
        "PASEO_AGENT_ID",
        "child_dispatches",
        "archive_confirmed",
        "archive_pending",
        "archive_attempts_started",
        "明确回退",
        "archive_confirmed=true",
        "lifecycle",
        "NUL",
        "每次 child 调度前，ORCHESTRATOR 必须读取实时 `list_profiles`",
        "同一 provider 的另一个 profile 只能是复杂度升级，不能在该 provider 已不可用时充当 availability fallback",
        "reviewer 尽量避开候选作者的 provider",
        "候选作者属于主要订阅 provider 且 `author_provider_resolution=verified` 时，预算例外才允许同 provider 审核",
        "精确 model identity",
        "candidate binding",
        "fresh child",
        "WAIT_USER",
        "EXECUTOR`、`REVIEWER`、`SCOUT`、`senior-reviewer",
        "candidate_author_agent_id",
        "author_provider_resolution",
        "model_diversity_verified=true",
        "not_applicable",
        "archived agent",
        "unavailable",
        "derived operational provenance",
        "明确删除的复杂度",
        ".ai/task/<task_id>/STATE.json",
        *ROUTING_PROVENANCE_MARKERS,
        *STOP_ARCHIVE_MARKERS,
        *CONTEXTUAL_ANCHOR_PREFLIGHT_MARKERS,
        "ParentAgentId",
    ),
    ".ai/roles/reviewer.md": ("role=reviewer", "purpose"),
    ".ai/roles/scout.md": ("role=scout",),
    ".ai/roles/senior-reviewer.md": ("role=senior-reviewer", "purpose"),
    "docs/paseo-orchestration-v2-contract.md": (
        "purpose=normal_review",
        "purpose=translation_contextual_v1",
        "candidate_ref",
        "orchestration_transport",
        "child_dispatches",
        "archive_confirmed",
        "archive_pending",
        "archive_attempts_started",
        "明确回退",
        "archive_confirmed=true",
        "lifecycle",
        "NUL",
        "每次 child 调度前，ORCHESTRATOR 必须读取实时 `list_profiles`",
        "同一 provider 的另一个 profile 只能是复杂度升级，不能在该 provider 已不可用时充当 availability fallback",
        "reviewer 尽量避开候选作者的 provider",
        "候选作者属于主要订阅 provider 且 `author_provider_resolution=verified` 时，预算例外才允许同 provider 审核",
        "精确 model identity",
        "candidate binding",
        "fresh child",
        "WAIT_USER",
        "EXECUTOR`、`REVIEWER`、`SCOUT`、`senior-reviewer",
        "candidate_author_agent_id",
        "author_provider_resolution",
        "model_diversity_verified=true",
        "not_applicable",
        "archived agent",
        "unavailable",
        "derived operational provenance",
        "明确删除的复杂度",
        ".ai/task/<task_id>/STATE.json",
        *ROUTING_PROVENANCE_MARKERS,
        *STOP_ARCHIVE_MARKERS,
        *CONTEXTUAL_ANCHOR_PREFLIGHT_MARKERS,
    ),
    "docs/paseo-translation-context-review-v1-contract.md": (
        "role=reviewer",
        "purpose=translation_contextual_v1",
        "candidate_identity",
        "dispatch_id",
    ),
}

# These are runtime identities or routing fields. Generic words such as
# "provider" and "model" remain allowed when describing the external API.
FORBIDDEN_RUNTIME_MARKERS = (
    "command-code-goat/",
    "opencode-go/",
    "openai-codex/",
    "gpt-5.6-",
    "claude-opus-",
    "runtime_tuple",
    "thinkingOptionId",
    "fallback_reason",
)


def main() -> int:
    errors: list[str] = []
    texts: dict[str, str] = {}

    for relative in ACTIVE_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing active file: {relative}")
            continue
        texts[relative] = path.read_text(encoding="utf-8")

    for relative, markers in REQUIRED_MARKERS.items():
        text = texts.get(relative, "")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative}: missing required marker {marker!r}")

    for relative, text in texts.items():
        for marker in FORBIDDEN_RUNTIME_MARKERS:
            if marker in text:
                errors.append(f"{relative}: fixed runtime marker {marker!r}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {len(texts)} active Paseo documents are role-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
