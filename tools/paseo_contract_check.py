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
    "docs/paseo-translation-context-review-v2-contract.md",
    "docs/paseo-translation-surface-screen-v1-contract.md",
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

RUNTIME_OBSERVATION_MARKERS = (
    "每个新 child dispatch 在身份／lineage 已无歧义且首次取得可核验 live agent metadata 后",
    "禁止从 profile、title、memory、其他字段或其他 dispatch 推断",
    "完成谓词、wave 判定或 model diversity proof",
    "顶层 STATE 与任何 review record 禁止 `runtime_observation`。",
    "`capture_status` 精确为 `captured`",
    "present 形式必须",
    "missing 形式必须",
    "与 missing 保持可区分",
    "旧 STATE 可以没有该字段；有效观测不改变 DONE／STOP、wave、candidate",
    "并允许第 19 条 exact-schema `runtime_observation` 审计例外",
)

ROLE_CLAUSE_REFERENCES = {
    ".ai/roles/executor.md": (
        "P2-SINGLE-WRITER", "P2-DIRECT-LINEAGE", "P2-FRESH-RETRY", "P2-STOP-CLOSED",
    ),
    ".ai/roles/orchestrator.md": (
        "P2-SINGLE-WRITER", "P2-DIRECT-LINEAGE", "P2-LIVE-ROUTING",
        "P2-RUNTIME-OBSERVATION", "P2-CANDIDATE-FREEZE",
        "P2-REVIEW-INDEPENDENCE", "P2-AUTHOR-PROVENANCE",
        "P2-MODEL-DIVERSITY", "P2-HARVEST-ARCHIVE", "P2-FRESH-RETRY",
        "P2-RECOVERY", "P2-STOP-CLOSED",
        "P2-TRANSLATION-CONVERGENCE",
        "P2-TRANSLATION-CONTEXT-V2",
        "P2-TRANSLATION-SURFACE-V1",
    ),
    ".ai/roles/reviewer.md": (
        "P2-READ-ONLY", "P2-CANDIDATE-FREEZE", "P2-REVIEW-INDEPENDENCE",
        "P2-STOP-CLOSED",
    ),
    ".ai/roles/scout.md": (
        "P2-READ-ONLY", "P2-DIRECT-LINEAGE", "P2-HARVEST-ARCHIVE",
    ),
    ".ai/roles/senior-reviewer.md": (
        "P2-READ-ONLY", "P2-CANDIDATE-FREEZE", "P2-REVIEW-INDEPENDENCE",
        "P2-STOP-CLOSED",
    ),
}

ROLE_CONTRACT_PATH = "docs/paseo-orchestration-v2-contract.md"

ROLE_OUTPUT_MARKERS = {
    ".ai/roles/reviewer.md": (
        "Severity: blocker | high | medium | low",
        "缺字段、额外字段或 enum 外取值均使输出无效。",
        "canonical sorted compact bytes",
        "surface 结果只是 `OK|ISSUE` observation，不得升级为",
    ),
    ".ai/roles/scout.md": (
        "`context`（非空字符串）",
        "`files_retrieved`、`risks`、`open_questions` 必须是字符串数组",
        "`key_code`、`architecture`、`start_here` 必须是字符串。",
        "七字段不得缺失或新增，类型不符即输出无效。",
    ),
    ".ai/roles/senior-reviewer.md": (
        "Severity: blocker | high | medium | low",
        "Assessment: keep | narrow | downgrade | reject | defer_to_user",
        "任一分支缺字段、额外字段或 enum 外取值均使输出无效。",
    ),
}

TRANSLATION_CONVERGENCE_MARKERS = (
    '`"schema_version": 4`',
    '`"max_cycles": 3`',
    "max_cycles_user_authorized=true",
    "REVIEW/full",
    "RE_REVIEW/full",
    "RE_REVIEW/closure",
    "FINAL_REVIEW/full",
    "correctness backstop",
    "schema 3 及更早任务保持 compatibility",
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
    "The preflight also accepts the whole-section form for sections without actual chapter-title t(...) calls.",
    "An anchor scope may instead declare ordered_titles: [] only when its section contains no actual chapter-title t(...) calls; a titled section with [] fails closed and must declare explicit anchors.",
    "For ordered_titles: [], the window is the whole section from its section marker to the earliest later section marker or EOF.",
    "The same source proof applies to a whole-section window, and the preflight adds no payload or identity fields.",
    "The preflight requires each translation_snapshot entry whose matching in-window t(...) call has args_order to disclose the exact canonical token args_order={i,j,...} in bounded_context.context, rejects any args_order= token when the call has none, and fails closed when matching calls disagree.",
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
    ".ai/roles/executor.md": ("role=executor", ROLE_CONTRACT_PATH, *ROLE_CLAUSE_REFERENCES[".ai/roles/executor.md"]),
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
        "同一 provider 的另一个 profile 只能是复杂度升级，不能在该 provider 已不可用时充当 availability fallback。",
        "reviewer 尽量避开候选作者的 provider",
        "候选作者属于主要订阅 provider 且 `author_provider_resolution=verified` 时，预算例外才允许同 provider 审核。",
        "精确 model identity",
        "candidate binding",
        "fresh child",
        "WAIT_USER",
        "EXECUTOR`、`REVIEWER`、`SCOUT`、`senior-reviewer",
        "candidate_author_agent_id",
        "author_provider_resolution",
        "model_diversity_verified=true",
        "ParentAgentId",
        ROLE_CONTRACT_PATH,
        *CONTEXTUAL_ANCHOR_PREFLIGHT_MARKERS,
        *TRANSLATION_CONVERGENCE_MARKERS,
        *ROLE_CLAUSE_REFERENCES[".ai/roles/orchestrator.md"],
    ),
    ".ai/roles/reviewer.md": ("role=reviewer", "purpose", "translation_contextual_v2", ROLE_CONTRACT_PATH, *ROLE_OUTPUT_MARKERS[".ai/roles/reviewer.md"], *ROLE_CLAUSE_REFERENCES[".ai/roles/reviewer.md"]),
    ".ai/roles/scout.md": ("role=scout", ROLE_CONTRACT_PATH, *ROLE_OUTPUT_MARKERS[".ai/roles/scout.md"], *ROLE_CLAUSE_REFERENCES[".ai/roles/scout.md"]),
    ".ai/roles/senior-reviewer.md": ("role=senior-reviewer", "purpose", ROLE_CONTRACT_PATH, *ROLE_OUTPUT_MARKERS[".ai/roles/senior-reviewer.md"], *ROLE_CLAUSE_REFERENCES[".ai/roles/senior-reviewer.md"]),
    "docs/paseo-orchestration-v2-contract.md": (
        "purpose=normal_review",
        "purpose=translation_contextual_v1",
        "translation_contextual_v2",
        "translation_surface_screen_v1",
        "P2-TRANSLATION-CONTEXT-V2",
        "P2-TRANSLATION-SURFACE-V1",
        "SURFACE-SCREEN-GROUP-<group_id>.json",
        "SURFACE-SCREEN-ZERO.json",
        "SURFACE-SCREEN-CARRY-OVER.json",
        "proves_no_surface_dispatch=true",
        "paseo-orchestration/2.25-draft",
        "append-only",
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
        *RUNTIME_OBSERVATION_MARKERS,
        *tuple(dict.fromkeys(
            clause
            for clauses in ROLE_CLAUSE_REFERENCES.values()
            for clause in clauses
        )),
    ),
    "docs/paseo-translation-context-review-v1-contract.md": (
        "role=reviewer",
        "purpose=translation_contextual_v1",
        "candidate_identity",
        "dispatch_id",
    ),
    "docs/paseo-translation-context-review-v2-contract.md": (
        "translation-contextual/2.0",
        "role=reviewer",
        "purpose=translation_contextual_v2",
        "fb95fa08bd65b4f626bb1b5f0f5a2035a72ef359d584cb088c30609f3fa94067",
        "raw_output_sha256",
        "lane_count=4",
        "parent_coverage_identity",
        "FINAL_REVIEW/full",
    ),
    "docs/paseo-translation-surface-screen-v1-contract.md": (
        "translation-surface-screen/1.0",
        "role=reviewer",
        "purpose=translation_surface_screen_v1",
        "translation_surface_screen_v1_lane_group",
        "logical_entry_identity = SHA-256",
        "entry_revision_identity = SHA-256",
        "call_locator",
        "normalized_path",
        "n=0",
        "carry-over",
        "split_carry_over",
        "SURFACE-SCREEN-ZERO.json",
        "SURFACE-SCREEN-CARRY-OVER.json",
        "proves_no_surface_dispatch=true",
        "surface-carry-over/1",
        "lane_count=4",
        "raw_output_sha256",
        "REVIEW/full",
        "OK|ISSUE",
        "不得升级为 adjudicated finding 或修复指令",
        "reason_code",
        "docs/paseo-translation-surface-screen-v1-contract.md 第六节",
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
        text = "".join(texts.get(relative, "").split())
        for marker in markers:
            normalized_marker = "".join(marker.split())
            if normalized_marker not in text:
                errors.append(f"{relative}: missing required marker {marker!r}")

    # Keep the bounded EXECUTOR contract clauses load-bearing without adding a
    # second marker family to REQUIRED_MARKERS' migration-owner index.
    relative = "docs/paseo-orchestration-v2-contract.md"
    text = "".join(texts.get(relative, "").split())
    for marker in (
        "禁止 `git reset --hard`、`git checkout` 或任何整树清理",
        "允许非目标路径存在未提交的 dirty changes",
        "对目标路径必须使用 `allowed_paths` 声明的 required preimage state/hash/mode 进行 fail-closed 检查",
        "实现 shadow output 与持久化事务日志",
        "必须写入已忽略的 `.artifacts/paseo-bounded/<workspace_id>/<dispatch_id>/`",
        "任何既非明确 pre 也非明确 post 的第三种状态必须记录冲突且不得覆盖目标",
        "不得声称多文件 OS 原子，只保证基于日志的可恢复事务",
        "拆分 candidate_id 与 envelope_hash",
        "同 dispatch 不同 hash 硬失败",
        "`bounded_apply_v1`",
        "`bounded_apply_journal_v1`",
        "author 必须是精确的 `{role, dispatch_id}` object，其中 `role` 必须是精确字符串 `ORCHESTRATOR` 或 `EXECUTOR`，`dispatch_id` 必须是 ASCII identifier",
        "host 注入、精确绑定 task/workspace/prior dispatch/candidate 的可信 `archive_receipts`",
        "`gates` 只进入 envelope identity，runner 不执行 gate",
        "APPLYING 恢复时实际 post 但未记入 `applied_paths` 的目标必须补入",
        "ROLLING_BACK 恢复时实际 pre 但仍在列表中的目标必须移除",
        "replace 或 unlink 后必须 `fsync` 目标父目录",
        "首路径组件为 `.git`、`.ai` 或 `.artifacts` 的 privileged namespace",
        "`allowed_paths` 与恢复 journal 的 `ordered_paths` 使用同一原始 POSIX 路径集合校验",
        "任一路径为另一条路径严格祖先的祖先／后代重叠（与声明顺序无关）",
        "任何 journal 写入都必须先拒绝未知或重复的 applied path，再将 `applied_paths` 按 `ordered_paths` 唯一重排为 ordered subset",
        "读取异常不得被重复 close 的 `EBADF` 掩盖",
        "首个 PREPARED journal 尚未持久化时",
        "file mode `0o000`、`0o200` 等 owner-unreadable 值仍是有效声明",
    ):
        if "".join(marker.split()) not in text:
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
