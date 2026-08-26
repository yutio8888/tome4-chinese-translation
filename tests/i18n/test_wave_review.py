from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import wave_review


class WaveFixture:
    """A two-lane wave whose task records live in real detached Git worktrees."""

    wave_id = "p2-wave-phase1-test"
    wave_path = Path(".ai/waves/p2-wave-phase1-test/WAVE.json")
    integration_apply_agent_id = "integration-apply-agent"
    wave_evidence_agent_id = "integration-evidence-agent"

    def __init__(self, parent: Path) -> None:
        self.parent = parent
        self.root = parent / "integration"
        self.root.mkdir()
        self._git(self.root, "init", "-q")
        self._git(self.root, "config", "user.email", "fixture@example.invalid")
        self._git(self.root, "config", "user.name", "Wave Fixture")
        self.write_raw(".gitignore", b".ai/\n.artifacts/\n")
        self.write_raw("tools/lua/load_locale.lua", (TOOLS / "lua/load_locale.lua").read_bytes())
        manifest_raw = (
            ROOT / f"i18n/versions/{wave_review.DEFAULT_VERSION}.json"
        ).read_bytes()
        self.write_raw(
            f"i18n/versions/{wave_review.DEFAULT_VERSION}.json", manifest_raw
        )
        manifest_value = json.loads(manifest_raw)
        self.fixed_source_identity = (
            "commit:" + manifest_value["repositories"]["engine"]["commit"]
        )
        self.calls_by_lane = {
            "A": self._calls("A", "mod-tome/data/lore/fun.lua"),
            "B": self._calls("B", "mod-tome/data/lore/infinite-dungeon.lua"),
        }
        self.write_raw("mod-tome.lua", self._locale_bytes())
        self._git(
            self.root,
            "add",
            ".gitignore",
            "tools/lua/load_locale.lua",
            f"i18n/versions/{wave_review.DEFAULT_VERSION}.json",
            "mod-tome.lua",
        )
        self._git(self.root, "commit", "-q", "-m", "base")
        self.base = self._git(self.root, "rev-parse", "HEAD").stdout.strip()
        self.base_tree = self._git(
            self.root, "rev-parse", f"{self.base}^{{tree}}"
        ).stdout.strip()
        self.lane_roots = {
            "A": parent / "lane-A",
            "B": parent / "lane-B",
        }
        for lane_root in self.lane_roots.values():
            self._git(self.root, "worktree", "add", "--detach", "-q", str(lane_root), self.base)
        self.workspace_roots = {
            "root-workspace": self.root,
            "lane-workspace-A": self.lane_roots["A"],
            "lane-workspace-B": self.lane_roots["B"],
        }
        self.lanes: list[dict[str, object]] = []
        self.worksets: list[dict[str, object]] = []
        self.preflight_sets: list[dict[str, object]] = []
        self.patches: list[dict[str, object]] = []
        self.lane_envelopes: list[dict[str, object]] = []
        self._build_lanes()
        self._build_preflight()
        self._build_integration()
        self._build_wave_and_evidence()

    @staticmethod
    def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            text=True,
            capture_output=True,
            check=True,
        )

    @staticmethod
    def _calls(lane_id: str, section: str) -> list[dict[str, object]]:
        return [
            {
                "revision_key": f"{lane_id}-{index:02d}",
                "section": section,
                "source": f"{lane_id} source {index:02d}",
                "source_tag": "_t",
                "args_order": None,
                "special": None,
            }
            for index in range(2)
        ]

    def _locale_bytes(self) -> bytes:
        lines = ['locale "zh_CN"']
        for lane_id in ("A", "B"):
            calls = self.calls_by_lane[lane_id]
            lines.append(f'section "{calls[0]["section"]}"')
            for index, call in enumerate(calls):
                lines.append(
                    f't({json.dumps(call["source"])}, '
                    f'{json.dumps(f"{lane_id} target {index:02d}")}, "_t")'
                )
        return ("\n".join(lines) + "\n").encode()

    def workspace_root(self, workspace_id: str | None = None) -> Path:
        return self.root if workspace_id is None else self.workspace_roots[workspace_id]

    def path(self, relative: str | Path, *, workspace_id: str | None = None) -> Path:
        return self.workspace_root(workspace_id) / relative

    def write_raw(
        self,
        relative: str | Path,
        raw: bytes,
        *,
        workspace_id: str | None = None,
    ) -> None:
        path = self.path(relative, workspace_id=workspace_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def write(
        self,
        relative: str | Path,
        value: object,
        *,
        workspace_id: str | None = None,
    ) -> None:
        self.write_raw(
            relative,
            wave_review.canonical_bytes(value),
            workspace_id=workspace_id,
        )

    def read(
        self, relative: str | Path, *, workspace_id: str | None = None
    ) -> dict[str, object]:
        return json.loads(self.path(relative, workspace_id=workspace_id).read_text())

    @staticmethod
    def _target(lane_id: str, index: int) -> str:
        return f"{lane_id} target {index:02d}"

    def _envelope(
        self, calls: list[dict[str, object]], label: str
    ) -> tuple[dict[str, object], str]:
        keys = [str(item["revision_key"]) for item in calls]
        payload = {
            "contract": "translation_contextual_v1",
            "ordered_revision_keys": keys,
            "translation_snapshot": [
                {
                    "revision_key": item["revision_key"],
                    "source": item["source"],
                    "target": self._target(str(item["revision_key"])[0], index % 2),
                }
                for index, item in enumerate(calls)
            ],
            "fixed_source_identity": self.fixed_source_identity,
            "terminology_snapshot": f"{label} frozen terminology",
            "bounded_context": [
                {
                    "revision_key": item["revision_key"],
                    "context": f"{label} frozen context for {item['revision_key']}",
                }
                for item in calls
            ],
            "rendered_briefing": f"{label} full review",
        }
        identity = wave_review.canonical_sha256(payload)
        return {"candidate_identity": identity, "payload": payload}, identity

    def _state_and_review(
        self,
        *,
        task_id: str,
        workspace_id: str,
        identity: str,
        envelope_path: str,
        review_path: str,
        dispatch_id: str,
        agent_id: str,
        implement: bool,
        with_executor: bool = False,
    ) -> tuple[dict[str, object], dict[str, object]]:
        reviewer = {
            "dispatch_id": dispatch_id,
            "task_id": task_id,
            "role": "REVIEWER",
            "purpose": "translation_contextual_v1",
            "agent_id": agent_id,
            "parent_agent_id": "wave-orchestrator",
            "workspace_id": workspace_id,
            "candidate_identity": identity,
            "input_path": envelope_path,
            "lineage_verified": True,
            "lifecycle": "archived",
            "archive_confirmed": True,
        }
        children: list[dict[str, object]] = [reviewer]
        if with_executor:
            children[0:0] = [
                {
                    "dispatch_id": "integration-apply-exec",
                    "task_id": task_id,
                    "role": "EXECUTOR",
                    "purpose": "integration_apply",
                    "agent_id": self.integration_apply_agent_id,
                    "parent_agent_id": "wave-orchestrator",
                    "workspace_id": workspace_id,
                    "lineage_verified": True,
                    "lifecycle": "archived",
                    "archive_confirmed": True,
                },
                {
                    "dispatch_id": "integration-wave-evidence-exec",
                    "task_id": task_id,
                    "role": "EXECUTOR",
                    "purpose": "wave_evidence",
                    "agent_id": self.wave_evidence_agent_id,
                    "parent_agent_id": "wave-orchestrator",
                    "workspace_id": workspace_id,
                    "lineage_verified": True,
                    "wave_evidence_path": (
                        f"evidence/quality/p2-waves/{self.wave_id}-adjudication.json"
                    ),
                    "prospective_wave_identity": "0" * 64,
                    "lifecycle": "archived",
                    "archive_confirmed": True,
                },
            ]
        state = {
            "schema_version": 2,
            "task_id": task_id,
            "mode": "implement" if implement else "review_only",
            "review_contracts": ["translation_contextual_v1"],
            "state": "DONE",
            "review_phase": "FINAL_REVIEW",
            "pending_review_contracts": [],
            "completed_review_contracts": ["translation_contextual_v1"],
            "cycle": 0,
            "max_cycles": 5,
            "workspace_id": workspace_id,
            "orchestrator_agent_id": "wave-orchestrator",
            "orchestration_transport": "mcp",
            "child_dispatches": children,
            "open_accepted_findings": [],
            "deferred_findings": [],
            "review_records": [review_path],
            "senior_review_records": [],
            "wait": None,
            "last_error": None,
        }
        if implement:
            state["final_validation_passed"] = True
        review = {
            "task_id": task_id,
            "review_contract": "translation_contextual_v1",
            "review_phase": "FINAL_REVIEW",
            "cycle": 0,
            "attempt": 1,
            "reviewer_role": "REVIEWER",
            "purpose": "translation_contextual_v1",
            "agent_id": agent_id,
            "dispatch_id": dispatch_id,
            "status": "completed",
            "result": "PASS",
            "candidate_identity": identity,
            "input_path": envelope_path,
            "review_kind": "full",
        }
        return state, review

    def _build_lanes(self) -> None:
        for lane_id in ("A", "B"):
            task_id = f"lane-task-{lane_id}"
            workspace_id = f"lane-workspace-{lane_id}"
            calls = self.calls_by_lane[lane_id]
            workset = {
                "schema_id": "lane-workset/1",
                "schema_version": 1,
                "lane_id": lane_id,
                "task_id": task_id,
                "ordered_revision_keys": [item["revision_key"] for item in calls],
                "calls": calls,
                "primary_content_paths": ["mod-tome.lua"],
            }
            workset_path = f".ai/waves/{self.wave_id}/LANE-{lane_id}-WORKSET.json"
            self.write(workset_path, workset)
            spec_path = f".ai/task/{task_id}/SPEC.md"
            spec_raw = f"# Lane fixture\n{wave_review.COLLATERAL_FORBIDDEN_MARKER}\n".encode()
            self.write_raw(spec_path, spec_raw, workspace_id=workspace_id)
            scope_path = f".ai/task/{task_id}/SCOPE.json"
            scope = {
                "schema_id": "task-content-allowed-files/1",
                "schema_version": 1,
                "task_id": task_id,
                "wave_id": self.wave_id,
                "allowed_files": ["mod-tome.lua"],
                "translation_fix_paths": ["mod-tome.lua"],
                "wave_evidence_path": None,
            }
            self.write(scope_path, scope, workspace_id=workspace_id)
            envelope, identity = self._envelope(calls, lane_id)
            self.lane_envelopes.append(copy.deepcopy(envelope))
            envelope_path = f".ai/task/{task_id}/CONTEXTUAL-ENVELOPE-final.json"
            review_path = f".ai/reviews/{task_id}/review-final.json"
            self.write(envelope_path, envelope, workspace_id=workspace_id)
            state, review = self._state_and_review(
                task_id=task_id,
                workspace_id=workspace_id,
                identity=identity,
                envelope_path=envelope_path,
                review_path=review_path,
                dispatch_id=f"{lane_id}-review-final",
                agent_id=f"{lane_id}-reviewer-agent",
                implement=False,
            )
            self.write(review_path, review, workspace_id=workspace_id)
            state_path = f".ai/task/{task_id}/STATE.json"
            self.write(state_path, state, workspace_id=workspace_id)
            patch = {
                "schema_id": "target-patch/1",
                "schema_version": 1,
                "base_commit": self.base,
                "task_id": task_id,
                "candidate_identity": identity,
                "ordered_revision_keys": list(workset["ordered_revision_keys"]),
                "changes": [],
            }
            patch_path = f".ai/task/{task_id}/TARGET-PATCH.json"
            self.write(patch_path, patch, workspace_id=workspace_id)
            patch_identity = wave_review.canonical_sha256(patch)
            self.lanes.append(
                {
                    "lane_id": lane_id,
                    "task_id": task_id,
                    "workspace_id": workspace_id,
                    "state_path": state_path,
                    "spec_path": spec_path,
                    "workset_path": workset_path,
                    "workset_identity": wave_review.canonical_sha256(workset),
                    "collateral_empty": True,
                    "final_candidate_identity": identity,
                    "final_review_kind": "full",
                    "final_review_dispatch_id": f"{lane_id}-review-final",
                    "final_review_record": review_path,
                    "target_patch_path": patch_path,
                    "target_patch_identity": patch_identity,
                }
            )
            self.worksets.append(workset)
            self.patches.append(patch)

    def _build_preflight(self) -> None:
        for lane, workset in zip(self.lanes, self.worksets):
            lane_id = str(lane["lane_id"])
            task_id = str(lane["task_id"])
            workspace_id = str(lane["workspace_id"])
            call_set = {
                "schema_id": "call-set/1",
                "schema_version": 1,
                "lane_id": lane_id,
                "task_id": task_id,
                "items": copy.deepcopy(workset["calls"]),
            }
            runtime_set = {
                "schema_id": "runtime-key-set/1",
                "schema_version": 1,
                "lane_id": lane_id,
                "task_id": task_id,
                "items": [
                    {"runtime_key": item["source"], "source_tag": item["source_tag"]}
                    for item in workset["calls"]
                ],
            }
            term_set = {
                "schema_id": "term-narrative-set/1",
                "schema_version": 1,
                "lane_id": lane_id,
                "task_id": task_id,
                "items": [
                    {"kind": "narrative_closure", "key": key}
                    for key in workset["ordered_revision_keys"]
                ],
            }
            scope_path = f".ai/task/{task_id}/SCOPE.json"
            scope_raw = self.path(scope_path, workspace_id=workspace_id).read_bytes()
            collateral = {
                "schema_id": "collateral-authorization/1",
                "schema_version": 1,
                "lane_id": lane_id,
                "task_id": task_id,
                "spec_path": lane["spec_path"],
                "spec_identity": hashlib.sha256(
                    self.path(str(lane["spec_path"]), workspace_id=workspace_id).read_bytes()
                ).hexdigest(),
                "scope_path": scope_path,
                "scope_identity": hashlib.sha256(scope_raw).hexdigest(),
                "allowed_files_path": scope_path,
                "allowed_files_identity": hashlib.sha256(scope_raw).hexdigest(),
                "primary_content_paths": ["mod-tome.lua"],
                "ordinary_non_collateral_paths": [],
                "collateral_paths": [],
            }
            frozen = {
                "lane_id": lane_id,
                "task_id": task_id,
                "call_set": call_set,
                "call_set_identity": wave_review.canonical_sha256(call_set),
                "runtime_key_set": runtime_set,
                "runtime_key_set_identity": wave_review.canonical_sha256(runtime_set),
                "term_narrative_set": term_set,
                "term_narrative_set_identity": wave_review.canonical_sha256(term_set),
                "collateral_authorization": collateral,
                "collateral_authorization_identity": wave_review.canonical_sha256(collateral),
            }
            self.preflight_sets.append(frozen)
        self.preflight = {
            "schema_id": "conflict-preflight/1",
            "schema_version": 1,
            "wave_id": self.wave_id,
            "base_commit": self.base,
            "ordered_lane_ids": ["A", "B"],
            "sets": self.preflight_sets,
            "pairwise_intersections_empty": True,
            "result": "PASS",
        }
        self.preflight_path = f".ai/waves/{self.wave_id}/CONFLICT-PREFLIGHT.json"
        self.write(self.preflight_path, self.preflight)
        self.merge = {
            "schema_id": "merge-queue/1",
            "schema_version": 1,
            "wave_id": self.wave_id,
            "base_commit": self.base,
            "ordered_lane_ids": ["A", "B"],
            "items": [
                {
                    "lane_id": lane["lane_id"],
                    "task_id": lane["task_id"],
                    "target_patch_path": lane["target_patch_path"],
                    "target_patch_identity": lane["target_patch_identity"],
                    "candidate_identity": lane["final_candidate_identity"],
                }
                for lane in self.lanes
            ],
        }
        self.merge_path = f".ai/waves/{self.wave_id}/MERGE-QUEUE.json"
        self.write(self.merge_path, self.merge)

    def _build_integration(self) -> None:
        task_id = "integration-task"
        workspace_id = "root-workspace"
        evidence_path = f"evidence/quality/p2-waves/{self.wave_id}-adjudication.json"
        calls = self.calls_by_lane["A"] + self.calls_by_lane["B"]
        envelope, identity = self._envelope(calls, "integration")
        lane_payloads = [
            (lane_id, envelope_value["payload"])
            for lane_id, envelope_value in zip(("A", "B"), self.lane_envelopes)
        ]
        payload = envelope["payload"]
        payload["bounded_context"] = [
            copy.deepcopy(context)
            for _, lane_payload in lane_payloads
            for context in lane_payload["bounded_context"]
        ]
        payload["terminology_snapshot"] = (
            wave_review._render_integration_terminology_snapshot(lane_payloads)
        )
        payload["rendered_briefing"] = wave_review._render_integration_briefing(
            lane_payloads=lane_payloads,
            ordered_revision_keys=payload["ordered_revision_keys"],
            translation_snapshot=payload["translation_snapshot"],
            fixed_source_identity=payload["fixed_source_identity"],
            terminology_snapshot=payload["terminology_snapshot"],
            bounded_context=payload["bounded_context"],
        )
        identity = wave_review.canonical_sha256(payload)
        envelope["candidate_identity"] = identity
        envelope_path = f".ai/task/{task_id}/CONTEXTUAL-ENVELOPE-final.json"
        review_path = f".ai/reviews/{task_id}/review-final.json"
        self.write(envelope_path, envelope)
        state, review = self._state_and_review(
            task_id=task_id,
            workspace_id=workspace_id,
            identity=identity,
            envelope_path=envelope_path,
            review_path=review_path,
            dispatch_id="integration-review-final",
            agent_id="integration-reviewer-agent",
            implement=True,
            with_executor=True,
        )
        self.write(review_path, review)
        state_path = f".ai/task/{task_id}/STATE.json"
        self.write(state_path, state)
        spec_path = f".ai/task/{task_id}/SPEC.md"
        self.write_raw(spec_path, f"# Integration\nwave evidence: {evidence_path}\n".encode())
        self.integration_scope = {
            "schema_id": "task-content-allowed-files/1",
            "schema_version": 1,
            "task_id": task_id,
            "wave_id": self.wave_id,
            "allowed_files": [evidence_path, "mod-tome.lua"],
            "translation_fix_paths": ["mod-tome.lua"],
            "wave_evidence_path": evidence_path,
        }
        scope_path = f".ai/task/{task_id}/SCOPE.json"
        self.write(scope_path, self.integration_scope)
        self.content_diff = {
            "schema_id": "integration-content-diff/1",
            "schema_version": 1,
            "wave_id": self.wave_id,
            "task_id": task_id,
            "base_commit": self.base,
            "translation_paths": ["mod-tome.lua"],
            "changed_paths": [],
            "entries": [],
        }
        content_path = f".ai/task/{task_id}/INTEGRATION-CONTENT-DIFF.json"
        self.write(content_path, self.content_diff)
        self.integration = {
            "task_id": task_id,
            "workspace_id": workspace_id,
            "state_path": state_path,
            "spec_path": spec_path,
            "allowed_files_path": scope_path,
            "allowed_files_identity": wave_review.canonical_sha256(self.integration_scope),
            "combined_candidate_identity": identity,
            "content_diff_path": content_path,
            "content_diff_identity": wave_review.canonical_sha256(self.content_diff),
            "final_review_kind": "full",
            "final_review_dispatch_id": "integration-review-final",
            "final_review_record": review_path,
        }

    def _build_wave_and_evidence(self) -> None:
        evidence_path = f"evidence/quality/p2-waves/{self.wave_id}-adjudication.json"
        self.wave = {
            "schema_id": "wave/1",
            "schema_version": 1,
            "wave_id": self.wave_id,
            "state": "DONE",
            "base_commit": self.base,
            "orchestrator_agent_id": "wave-orchestrator",
            "root_workspace_id": "root-workspace",
            "ordered_lane_ids": ["A", "B"],
            "lanes": self.lanes,
            "integration": self.integration,
            "merge_queue_path": self.merge_path,
            "conflict_preflight_path": self.preflight_path,
            "conflict_preflight_identity": wave_review.canonical_sha256(self.preflight),
            "wave_evidence_path": evidence_path,
        }
        self.evidence = {
            "schema_id": "wave-evidence/1",
            "schema_version": 1,
            "wave_id": self.wave_id,
            "base_commit": self.base,
            "orchestrator_agent_id": "wave-orchestrator",
            "wave_record_identity": "0" * 64,
            "merge_queue_identity": wave_review.canonical_sha256(self.merge),
            "conflict_preflight_path": self.preflight_path,
            "conflict_preflight_identity": wave_review.canonical_sha256(self.preflight),
            "lanes": [
                {
                    "lane_id": lane["lane_id"],
                    "task_id": lane["task_id"],
                    "workspace_id": lane["workspace_id"],
                    "final_candidate_identity": lane["final_candidate_identity"],
                    "target_patch_identity": lane["target_patch_identity"],
                    "final_review_kind": "full",
                    "final_review_dispatch_id": lane["final_review_dispatch_id"],
                    "final_review_record": lane["final_review_record"],
                    "done_verified": True,
                }
                for lane in self.lanes
            ],
            "integration": {
                "task_id": self.integration["task_id"],
                "workspace_id": self.integration["workspace_id"],
                "executor_agent_id": self.wave_evidence_agent_id,
                "combined_candidate_identity": self.integration["combined_candidate_identity"],
                "content_diff_path": self.integration["content_diff_path"],
                "content_diff_identity": self.integration["content_diff_identity"],
                "final_review_kind": "full",
                "final_review_dispatch_id": self.integration["final_review_dispatch_id"],
                "final_review_record": self.integration["final_review_record"],
                "initial_git": {
                    "head_commit": self.base,
                    "index_tree": self.base_tree,
                    "worktree_tree": self.base_tree,
                },
                "done_verified": True,
            },
            "collateral_empty": True,
            "gates_result": "PASS",
        }
        self.sync_done_records()

    def sync_done_records(self) -> None:
        done_wave = copy.deepcopy(self.wave)
        done_wave["state"] = "DONE"
        self.prospective_path = f".ai/waves/{self.wave_id}/WAVE.DONE.prospective.json"
        self.write(self.prospective_path, done_wave)
        prospective_identity = wave_review.canonical_sha256(done_wave)
        self.evidence["wave_record_identity"] = prospective_identity
        integration_state = self.read(str(self.integration["state_path"]))
        evidence_dispatch = next(
            item
            for item in integration_state["child_dispatches"]
            if item.get("purpose") == "wave_evidence"
        )
        evidence_dispatch["wave_evidence_path"] = self.wave["wave_evidence_path"]
        evidence_dispatch["prospective_wave_identity"] = prospective_identity
        self.write(str(self.integration["state_path"]), integration_state)
        self.evidence["merge_queue_identity"] = wave_review.canonical_sha256(self.merge)
        self.evidence["conflict_preflight_identity"] = wave_review.canonical_sha256(self.preflight)
        self.write(str(self.wave["wave_evidence_path"]), self.evidence)
        self.write(self.wave_path, self.wave)

    def set_integrating(self) -> None:
        self.wave["state"] = "INTEGRATING"
        for field in (
            "combined_candidate_identity",
            "content_diff_path",
            "content_diff_identity",
            "final_review_kind",
            "final_review_dispatch_id",
            "final_review_record",
        ):
            self.wave["integration"][field] = None
        evidence_path = self.path(str(self.wave["wave_evidence_path"]))
        if evidence_path.exists():
            evidence_path.unlink()
        self.write(self.wave_path, self.wave)

    def set_gated(self) -> None:
        self.wave["integration"] = copy.deepcopy(self.integration)
        self.wave["state"] = "GATED"
        self.sync_done_records()

    def refresh_preflight(self) -> None:
        self.write(self.preflight_path, self.preflight)
        self.wave["conflict_preflight_identity"] = wave_review.canonical_sha256(self.preflight)
        self.sync_done_records()

    def refresh_patch(self, index: int) -> None:
        lane = self.lanes[index]
        identity = wave_review.canonical_sha256(self.patches[index])
        self.write(
            str(lane["target_patch_path"]),
            self.patches[index],
            workspace_id=str(lane["workspace_id"]),
        )
        lane["target_patch_identity"] = identity
        self.merge["items"][index]["target_patch_identity"] = identity
        self.evidence["lanes"][index]["target_patch_identity"] = identity
        self.write(self.merge_path, self.merge)
        self.sync_done_records()

    def refresh_content_diff(self) -> None:
        identity = wave_review.canonical_sha256(self.content_diff)
        self.write(str(self.integration["content_diff_path"]), self.content_diff)
        self.integration["content_diff_identity"] = identity
        self.wave["integration"]["content_diff_identity"] = identity
        self.evidence["integration"]["content_diff_identity"] = identity
        self.sync_done_records()

    def mutate_integration_envelope(self, mutate) -> None:
        workspace_id = "root-workspace"
        path = str(self.integration["final_review_record"])
        review = self.read(path, workspace_id=workspace_id)
        envelope_path = str(review["input_path"])
        envelope = self.read(envelope_path, workspace_id=workspace_id)
        mutate(envelope["payload"])
        identity = wave_review.canonical_sha256(envelope["payload"])
        envelope["candidate_identity"] = identity
        review["candidate_identity"] = identity
        state = self.read(str(self.integration["state_path"]), workspace_id=workspace_id)
        reviewer = next(
            item for item in state["child_dispatches"] if item["role"] == "REVIEWER"
        )
        reviewer["candidate_identity"] = identity
        self.integration["combined_candidate_identity"] = identity
        self.wave["integration"]["combined_candidate_identity"] = identity
        self.evidence["integration"]["combined_candidate_identity"] = identity
        self.write(envelope_path, envelope)
        self.write(path, review)
        self.write(str(self.integration["state_path"]), state)
        self.sync_done_records()


class WaveReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="wave-review-")
        self.addCleanup(self.temporary.cleanup)
        self.fixture = WaveFixture(Path(self.temporary.name))
        environment = mock.patch.dict(
            os.environ,
            {"PASEO_AGENT_ID": WaveFixture.integration_apply_agent_id},
        )
        environment.start()
        self.addCleanup(environment.stop)

    def call(self, function, *args):
        previous = Path.cwd()
        try:
            __import__("os").chdir(self.fixture.root)
            return function(*args, self.fixture.workspace_roots)
        finally:
            __import__("os").chdir(previous)

    def test_real_cross_worktree_preflight_and_no_root_shadow_reads(self) -> None:
        f = self.fixture
        common = WaveFixture._git(f.root, "rev-parse", "--git-common-dir").stdout
        for lane_root in f.lane_roots.values():
            self.assertNotEqual(lane_root, f.root)
            self.assertEqual(
                Path(WaveFixture._git(lane_root, "rev-parse", "--git-common-dir").stdout).resolve(),
                (f.root / common).resolve(),
            )
        for lane in f.lanes:
            f.write_raw(str(lane["state_path"]), b"root shadow is not JSON")
            f.write_raw(str(lane["spec_path"]), b"root shadow")
        result = self.call(wave_review.preflight, str(f.wave_path))
        self.assertEqual((result.outcome, result.exit_code), ("PASS", 0), result.detail)
        f.set_integrating()
        result = self.call(wave_review.verify_target_patch, str(f.wave_path), "A")
        self.assertEqual(result.exit_code, 0, result.detail)

    def test_workspace_map_is_exact_and_lane_symlink_fails_closed(self) -> None:
        f = self.fixture
        previous = Path.cwd()
        try:
            __import__("os").chdir(f.root)
            self.assertEqual(wave_review.preflight(str(f.wave_path)).exit_code, 2)
            bad = dict(f.workspace_roots)
            bad["lane-workspace-A"] = f.root
            self.assertEqual(wave_review.preflight(str(f.wave_path), bad).exit_code, 2)
        finally:
            __import__("os").chdir(previous)
        lane = f.lanes[0]
        state_path = f.path(str(lane["state_path"]), workspace_id="lane-workspace-A")
        backup = state_path.with_name("STATE-real.json")
        state_path.rename(backup)
        state_path.symlink_to(backup.name)
        f.set_integrating()
        result = self.call(wave_review.verify_target_patch, str(f.wave_path), "A")
        self.assertEqual(result.exit_code, 2)
        self.assertIn("symlink", result.detail)

    def test_schemas_and_workset_provenance_fail_closed(self) -> None:
        f = self.fixture
        values = [
            f.wave,
            f.merge,
            f.preflight,
            f.worksets[0],
            f.preflight_sets[0]["call_set"],
            f.preflight_sets[0]["runtime_key_set"],
            f.preflight_sets[0]["term_narrative_set"],
            f.preflight_sets[0]["collateral_authorization"],
            f.integration_scope,
            f.content_diff,
            f.evidence,
            f.patches[0],
        ]
        for value in values:
            mutated = copy.deepcopy(value)
            mutated["extra"] = True
            with self.assertRaises(wave_review.ContractError):
                wave_review.validate_schema(mutated)

        empty = copy.deepcopy(f.worksets[0])
        empty["ordered_revision_keys"] = []
        empty["calls"] = []
        with self.assertRaises(wave_review.ContractError):
            wave_review.validate_schema(empty)

        f.preflight_sets[0]["runtime_key_set"]["items"] = []
        f.preflight_sets[0]["runtime_key_set_identity"] = wave_review.canonical_sha256(
            f.preflight_sets[0]["runtime_key_set"]
        )
        f.refresh_preflight()
        result = self.call(wave_review.preflight, str(f.wave_path))
        self.assertEqual(result.exit_code, 1)
        self.assertIn("reconstructed", result.detail)

        forged_terms = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-review-empty-term-")))
        self.addCleanup(lambda: shutil.rmtree(forged_terms.parent, ignore_errors=True))
        forged_terms.preflight_sets[0]["term_narrative_set"]["items"] = []
        forged_terms.preflight_sets[0]["term_narrative_set_identity"] = (
            wave_review.canonical_sha256(
                forged_terms.preflight_sets[0]["term_narrative_set"]
            )
        )
        forged_terms.refresh_preflight()
        previous = Path.cwd()
        try:
            __import__("os").chdir(forged_terms.root)
            result = wave_review.preflight(
                str(forged_terms.wave_path), forged_terms.workspace_roots
            )
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("reconstructed", result.detail)

        other = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-review-missing-call-")))
        self.addCleanup(lambda: shutil.rmtree(other.parent, ignore_errors=True))
        other.worksets[0]["calls"][0]["source"] = "not in pinned locale"
        other.preflight_sets[0]["call_set"]["items"] = copy.deepcopy(other.worksets[0]["calls"])
        other.preflight_sets[0]["call_set_identity"] = wave_review.canonical_sha256(
            other.preflight_sets[0]["call_set"]
        )
        other.write(str(other.lanes[0]["workset_path"]), other.worksets[0])
        other.lanes[0]["workset_identity"] = wave_review.canonical_sha256(other.worksets[0])
        other.refresh_preflight()
        previous = Path.cwd()
        try:
            __import__("os").chdir(other.root)
            result = wave_review.preflight(str(other.wave_path), other.workspace_roots)
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("pinned Lua calls", result.detail)

    def test_empty_patch_never_discards_candidate_or_current_target_drift(self) -> None:
        f = self.fixture
        f.set_integrating()
        self.assertEqual(
            self.call(wave_review.verify_target_patch, str(f.wave_path), "A").exit_code,
            0,
        )
        lane_file = f.path("mod-tome.lua", workspace_id="lane-workspace-A")
        lane_file.write_text(
            lane_file.read_text().replace("A target 00", "changed current target", 1)
        )
        result = self.call(wave_review.verify_target_patch, str(f.wave_path), "A")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("differs bytewise from base_commit", result.detail)

        other = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-review-nonempty-")))
        self.addCleanup(lambda: shutil.rmtree(other.parent, ignore_errors=True))
        change = copy.deepcopy(other.worksets[0]["calls"][0])
        change.update({"call_index": None, "old_target": "A target 00", "new_target": "new"})
        other.patches[0]["changes"] = [change]
        other.refresh_patch(0)
        other.set_integrating()
        previous = Path.cwd()
        try:
            __import__("os").chdir(other.root)
            result = wave_review.verify_target_patch(
                str(other.wave_path), "A", other.workspace_roots
            )
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("does not support non-empty", result.detail)

    def test_lane_no_change_closure_rejects_workset_external_call_and_target_drift(self) -> None:
        for name, old, new in (
            ("call", "B source 00", "changed outside-workset source"),
            ("target", "B target 00", "changed outside-workset target"),
        ):
            with self.subTest(name=name):
                temporary = tempfile.TemporaryDirectory(prefix=f"wave-lane-{name}-")
                self.addCleanup(temporary.cleanup)
                fixture = WaveFixture(Path(temporary.name))
                lane_file = fixture.path(
                    "mod-tome.lua", workspace_id="lane-workspace-A"
                )
                lane_file.write_text(lane_file.read_text().replace(old, new, 1))
                fixture.set_integrating()
                previous = Path.cwd()
                try:
                    __import__("os").chdir(fixture.root)
                    result = wave_review.verify_target_patch(
                        str(fixture.wave_path), "A", fixture.workspace_roots
                    )
                finally:
                    __import__("os").chdir(previous)
                self.assertEqual(result.exit_code, 1)
                self.assertIn("differs bytewise from base_commit", result.detail)

    def test_integration_no_change_cannot_be_legitimized_by_recomputed_diff(self) -> None:
        f = self.fixture
        translation = f.path("mod-tome.lua")
        base_raw = translation.read_bytes()
        translation.write_bytes(base_raw + b"-- workset-external drift\n")
        current_raw = translation.read_bytes()
        f.content_diff["changed_paths"] = ["mod-tome.lua"]
        f.content_diff["entries"] = [
            {
                "path": "mod-tome.lua",
                "old_content_sha256": hashlib.sha256(base_raw).hexdigest(),
                "new_content_sha256": hashlib.sha256(current_raw).hexdigest(),
            }
        ]
        f.refresh_content_diff()
        result = self.call(wave_review.verify_content_diff, str(f.wave_path))
        self.assertEqual(result.exit_code, 1)
        self.assertIn("differs bytewise from base_commit", result.detail)

        other = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-content-nonempty-")))
        self.addCleanup(lambda: shutil.rmtree(other.parent, ignore_errors=True))
        digest = hashlib.sha256(other.path("mod-tome.lua").read_bytes()).hexdigest()
        other.content_diff["changed_paths"] = ["mod-tome.lua"]
        other.content_diff["entries"] = [
            {
                "path": "mod-tome.lua",
                "old_content_sha256": digest,
                "new_content_sha256": digest,
            }
        ]
        other.refresh_content_diff()
        previous = Path.cwd()
        try:
            __import__("os").chdir(other.root)
            result = wave_review.verify_content_diff(
                str(other.wave_path), other.workspace_roots
            )
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("changed_paths and entries must be empty", result.detail)

    def test_integration_envelope_requires_exact_queue_union_order_source_and_target(self) -> None:
        mutations = {
            "omission": lambda payload: (
                payload["ordered_revision_keys"].pop(),
                payload["translation_snapshot"].pop(),
                payload["bounded_context"].pop(),
            ),
            "order": lambda payload: (
                payload["ordered_revision_keys"].reverse(),
                payload["translation_snapshot"].reverse(),
                payload["bounded_context"].reverse(),
            ),
            "source": lambda payload: payload["translation_snapshot"][0].update(
                {"source": "drift"}
            ),
            "target": lambda payload: payload["translation_snapshot"][0].update(
                {"target": "drift"}
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                temporary = tempfile.TemporaryDirectory(prefix=f"wave-{name}-")
                self.addCleanup(temporary.cleanup)
                fixture = WaveFixture(Path(temporary.name))
                fixture.mutate_integration_envelope(mutation)
                previous = Path.cwd()
                try:
                    __import__("os").chdir(fixture.root)
                    result = wave_review.verify_content_diff(
                        str(fixture.wave_path), fixture.workspace_roots
                    )
                finally:
                    __import__("os").chdir(previous)
                self.assertEqual(result.exit_code, 1)
                self.assertIn("integration", result.detail)

    def test_apply_requires_integrating_and_completed_lane_state_and_review(self) -> None:
        f = self.fixture
        result = self.call(wave_review.apply_target_patch, str(f.wave_path))
        self.assertEqual(result.exit_code, 1)
        self.assertIn("INTEGRATING", result.detail)

        gated = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-early-gated-")))
        self.addCleanup(lambda: shutil.rmtree(gated.parent, ignore_errors=True))
        gated.set_gated()
        previous = Path.cwd()
        try:
            __import__("os").chdir(gated.root)
            result = wave_review.apply_target_patch(
                str(gated.wave_path), gated.workspace_roots
            )
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("INTEGRATING", result.detail)

        preflight = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-early-preflight-")))
        self.addCleanup(lambda: shutil.rmtree(preflight.parent, ignore_errors=True))
        preflight.wave["state"] = "PREFLIGHT"
        for lane in preflight.wave["lanes"]:
            for field in (
                "final_candidate_identity", "final_review_kind", "final_review_dispatch_id",
                "final_review_record", "target_patch_identity",
            ):
                lane[field] = None
        preflight.wave["integration"] = {key: None for key in wave_review.WAVE_INTEGRATION_KEYS}
        preflight.write(preflight.wave_path, preflight.wave)
        previous = Path.cwd()
        try:
            __import__("os").chdir(preflight.root)
            result = wave_review.apply_target_patch(
                str(preflight.wave_path), preflight.workspace_roots
            )
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("INTEGRATING", result.detail)

        f.set_integrating()
        result = self.call(wave_review.apply_target_patch, str(f.wave_path))
        self.assertEqual(result.exit_code, 0, result.detail)

        state_path = str(f.lanes[0]["state_path"])
        state = f.read(state_path, workspace_id="lane-workspace-A")
        state["state"] = "FINAL_VALIDATE"
        f.write(state_path, state, workspace_id="lane-workspace-A")
        result = self.call(wave_review.apply_target_patch, str(f.wave_path))
        self.assertEqual(result.exit_code, 1)
        self.assertIn("STATE.state=DONE", result.detail)

        f.path(state_path, workspace_id="lane-workspace-A").unlink()
        result = self.call(wave_review.apply_target_patch, str(f.wave_path))
        self.assertEqual(result.exit_code, 2)

    def test_apply_requires_integration_identity_scope_and_executor_provenance(self) -> None:
        mutations = {
            "task": lambda fixture, state: state.update({"task_id": "other-task"}),
            "workspace": lambda fixture, state: state.update(
                {"workspace_id": "other-workspace"}
            ),
            "orchestrator": lambda fixture, state: state.update(
                {"orchestrator_agent_id": "other-orchestrator"}
            ),
            "executor-purpose": lambda fixture, state: next(
                item for item in state["child_dispatches"] if item["role"] == "EXECUTOR"
            ).update({"purpose": "wave_evidence"}),
            "executor-parent": lambda fixture, state: next(
                item for item in state["child_dispatches"] if item["role"] == "EXECUTOR"
            ).update({"parent_agent_id": "other-orchestrator"}),
            "executor-agent": lambda fixture, state: next(
                item for item in state["child_dispatches"] if item["role"] == "EXECUTOR"
            ).update({"agent_id": "wave-orchestrator"}),
            "executor-ambiguous": lambda fixture, state: state[
                "child_dispatches"
            ].append(
                {
                    **copy.deepcopy(
                        next(
                            item
                            for item in state["child_dispatches"]
                            if item["role"] == "EXECUTOR"
                        )
                    ),
                    "dispatch_id": "integration-apply-copy",
                    "agent_id": "integration-executor-copy",
                }
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                temporary = tempfile.TemporaryDirectory(prefix=f"wave-apply-{name}-")
                self.addCleanup(temporary.cleanup)
                fixture = WaveFixture(Path(temporary.name))
                fixture.set_integrating()
                state_path = str(fixture.integration["state_path"])
                state = fixture.read(state_path)
                mutate(fixture, state)
                fixture.write(state_path, state)
                previous = Path.cwd()
                try:
                    __import__("os").chdir(fixture.root)
                    result = wave_review.apply_target_patch(
                        str(fixture.wave_path), fixture.workspace_roots
                    )
                finally:
                    __import__("os").chdir(previous)
                self.assertEqual(result.exit_code, 1)

        scope = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-apply-scope-")))
        self.addCleanup(lambda: shutil.rmtree(scope.parent, ignore_errors=True))
        scope.integration_scope["allowed_files"] = ["mod-tome.lua"]
        scope.write(str(scope.integration["allowed_files_path"]), scope.integration_scope)
        scope.wave["integration"]["allowed_files_identity"] = (
            wave_review.canonical_sha256(scope.integration_scope)
        )
        scope.set_integrating()
        previous = Path.cwd()
        try:
            __import__("os").chdir(scope.root)
            result = wave_review.apply_target_patch(
                str(scope.wave_path), scope.workspace_roots
            )
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("exact translation/evidence union", result.detail)

        spec = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-apply-spec-")))
        self.addCleanup(lambda: shutil.rmtree(spec.parent, ignore_errors=True))
        spec.write_raw(str(spec.integration["spec_path"]), b"# Integration\n")
        spec.set_integrating()
        previous = Path.cwd()
        try:
            __import__("os").chdir(spec.root)
            result = wave_review.apply_target_patch(
                str(spec.wave_path), spec.workspace_roots
            )
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("SPEC", result.detail)

    def test_apply_requires_actual_paseo_caller_identity_in_real_worktrees(self) -> None:
        f = self.fixture
        self.assertEqual(len(f.lane_roots), 2)
        self.assertTrue(all(root != f.root for root in f.lane_roots.values()))
        f.set_integrating()

        with mock.patch.dict(os.environ):
            os.environ.pop("PASEO_AGENT_ID", None)
            missing = self.call(wave_review.apply_target_patch, str(f.wave_path))
        self.assertEqual(missing.exit_code, 1)
        self.assertIn("PASEO_AGENT_ID", missing.detail)

        with mock.patch.dict(os.environ, {"PASEO_AGENT_ID": "wrong-executor"}):
            mismatch = self.call(wave_review.apply_target_patch, str(f.wave_path))
        self.assertEqual(mismatch.exit_code, 1)
        self.assertIn("unique integration_apply EXECUTOR", mismatch.detail)

    def test_final_review_must_be_unique_state_completion_not_shadow_record(self) -> None:
        f = self.fixture
        lane = f.lanes[0]
        workspace_id = str(lane["workspace_id"])
        original_path = str(lane["final_review_record"])
        shadow_path = original_path.replace("review-final.json", "shadow.json")
        f.write(shadow_path, f.read(original_path, workspace_id=workspace_id), workspace_id=workspace_id)
        lane["final_review_record"] = shadow_path
        f.evidence["lanes"][0]["final_review_record"] = shadow_path
        f.sync_done_records()
        result = self.call(wave_review.done, str(f.wave_path))
        self.assertEqual(result.exit_code, 1)
        self.assertIn("latest", result.detail)

        other = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-review-duplicate-")))
        self.addCleanup(lambda: shutil.rmtree(other.parent, ignore_errors=True))
        lane = other.lanes[0]
        workspace_id = str(lane["workspace_id"])
        duplicate_path = str(lane["final_review_record"]).replace("review-final.json", "review-copy.json")
        other.write(
            duplicate_path,
            other.read(str(lane["final_review_record"]), workspace_id=workspace_id),
            workspace_id=workspace_id,
        )
        state = other.read(str(lane["state_path"]), workspace_id=workspace_id)
        state["review_records"].append(duplicate_path)
        other.write(str(lane["state_path"]), state, workspace_id=workspace_id)
        previous = Path.cwd()
        try:
            __import__("os").chdir(other.root)
            result = wave_review.done(str(other.wave_path), other.workspace_roots)
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("ambiguous", result.detail)

    def test_final_review_must_bind_unique_maximum_cycle_attempt(self) -> None:
        f = self.fixture
        lane = f.lanes[0]
        workspace_id = str(lane["workspace_id"])
        old_path = str(lane["final_review_record"])
        later_path = old_path.replace("review-final.json", "review-later.json")
        later = f.read(old_path, workspace_id=workspace_id)
        later.update(
            {
                "cycle": 1,
                "attempt": 1,
                "dispatch_id": "A-review-later",
                "agent_id": "A-reviewer-later-agent",
            }
        )
        f.write(later_path, later, workspace_id=workspace_id)
        state = f.read(str(lane["state_path"]), workspace_id=workspace_id)
        state["review_records"].append(later_path)
        later_dispatch = copy.deepcopy(state["child_dispatches"][0])
        later_dispatch.update(
            {
                "dispatch_id": "A-review-later",
                "agent_id": "A-reviewer-later-agent",
            }
        )
        state["child_dispatches"].append(later_dispatch)
        f.write(str(lane["state_path"]), state, workspace_id=workspace_id)
        result = self.call(wave_review.done, str(f.wave_path))
        self.assertEqual(result.exit_code, 1)
        self.assertIn("not the latest", result.detail)

    def test_latest_full_completion_spans_both_state_arrays_and_legal_phases(self) -> None:
        for record_field in ("review_records", "senior_review_records"):
            for review_phase in ("FINAL_REVIEW", "RE_REVIEW"):
                with self.subTest(
                    record_field=record_field, review_phase=review_phase
                ):
                    temporary = tempfile.TemporaryDirectory(
                        prefix="wave-latest-completion-"
                    )
                    self.addCleanup(temporary.cleanup)
                    fixture = WaveFixture(Path(temporary.name))
                    lane = fixture.lanes[0]
                    workspace_id = str(lane["workspace_id"])
                    old_path = str(lane["final_review_record"])
                    later_path = old_path.replace(
                        "review-final.json",
                        f"review-{record_field}-{review_phase}.json",
                    )
                    later = fixture.read(old_path, workspace_id=workspace_id)
                    later.update(
                        {
                            "review_phase": review_phase,
                            "cycle": 1,
                            "attempt": 1,
                            "dispatch_id": "A-review-newer-changes",
                            "agent_id": "A-reviewer-newer-changes-agent",
                            "status": "completed_with_findings",
                            "result": "CHANGES_REQUIRED",
                        }
                    )
                    fixture.write(
                        later_path, later, workspace_id=workspace_id
                    )
                    state = fixture.read(
                        str(lane["state_path"]), workspace_id=workspace_id
                    )
                    state[record_field].append(later_path)
                    later_dispatch = copy.deepcopy(
                        next(
                            item
                            for item in state["child_dispatches"]
                            if item["role"] == "REVIEWER"
                        )
                    )
                    later_dispatch.update(
                        {
                            "dispatch_id": "A-review-newer-changes",
                            "agent_id": "A-reviewer-newer-changes-agent",
                        }
                    )
                    state["child_dispatches"].append(later_dispatch)
                    fixture.write(
                        str(lane["state_path"]), state, workspace_id=workspace_id
                    )
                    previous = Path.cwd()
                    try:
                        os.chdir(fixture.root)
                        result = wave_review.done(
                            str(fixture.wave_path), fixture.workspace_roots
                        )
                    finally:
                        os.chdir(previous)
                    self.assertEqual(result.exit_code, 1)
                    self.assertIn("not the latest", result.detail)

    def test_wave_evidence_requires_unique_fresh_bound_evidence_executor(self) -> None:
        mutations = {
            "apply-purpose": lambda dispatch, state: dispatch.update(
                {"purpose": "integration_apply"}
            ),
            "fix-purpose": lambda dispatch, state: dispatch.update(
                {"purpose": "integration_fix"}
            ),
            "evidence-path": lambda dispatch, state: dispatch.update(
                {"wave_evidence_path": "evidence/quality/p2-waves/wrong.json"}
            ),
            "prospective-identity": lambda dispatch, state: dispatch.update(
                {"prospective_wave_identity": "f" * 64}
            ),
            "not-fresh": lambda dispatch, state: state["child_dispatches"].append(
                {
                    **copy.deepcopy(dispatch),
                    "dispatch_id": "integration-wave-evidence-copy",
                    "agent_id": "integration-evidence-copy-agent",
                }
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                temporary = tempfile.TemporaryDirectory(
                    prefix=f"wave-evidence-{name}-"
                )
                self.addCleanup(temporary.cleanup)
                fixture = WaveFixture(Path(temporary.name))
                state_path = str(fixture.integration["state_path"])
                state = fixture.read(state_path)
                dispatch = next(
                    item
                    for item in state["child_dispatches"]
                    if item.get("purpose") == "wave_evidence"
                )
                mutate(dispatch, state)
                fixture.write(state_path, state)
                previous = Path.cwd()
                try:
                    os.chdir(fixture.root)
                    result = wave_review.done(
                        str(fixture.wave_path), fixture.workspace_roots
                    )
                finally:
                    os.chdir(previous)
                self.assertEqual(result.exit_code, 1)

    def test_contextual_provenance_rejects_rehashed_arbitrary_integration_fields(self) -> None:
        mutations = {
            "fixed-source": lambda payload: payload.update(
                {"fixed_source_identity": "commit:" + "f" * 40}
            ),
            "empty-context": lambda payload: payload.update(
                {
                    "bounded_context": [
                        {"revision_key": key, "context": ""}
                        for key in payload["ordered_revision_keys"]
                    ]
                }
            ),
            "empty-terminology": lambda payload: payload.update(
                {"terminology_snapshot": ""}
            ),
            "empty-briefing": lambda payload: payload.update(
                {"rendered_briefing": ""}
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                temporary = tempfile.TemporaryDirectory(
                    prefix=f"wave-context-{name}-"
                )
                self.addCleanup(temporary.cleanup)
                fixture = WaveFixture(Path(temporary.name))
                fixture.mutate_integration_envelope(mutation)
                previous = Path.cwd()
                try:
                    os.chdir(fixture.root)
                    result = wave_review.verify_content_diff(
                        str(fixture.wave_path), fixture.workspace_roots
                    )
                finally:
                    os.chdir(previous)
                self.assertEqual(result.exit_code, 1)

    def test_current_manifest_mutation_cannot_redefine_pinned_source_identity(self) -> None:
        f = self.fixture
        manifest_path = f.path(
            f"i18n/versions/{wave_review.DEFAULT_VERSION}.json"
        )
        manifest = json.loads(manifest_path.read_text())
        manifest["repositories"]["engine"]["commit"] = "f" * 40
        manifest_path.write_bytes(wave_review.canonical_bytes(manifest))
        result = self.call(wave_review.preflight, str(f.wave_path))
        self.assertEqual(result.exit_code, 1)
        self.assertIn("pinned base_commit bytes", result.detail)

    def test_prepare_publish_recovery_idempotence_and_postpublication_done(self) -> None:
        f = self.fixture
        f.set_gated()
        f.path(f.prospective_path).unlink()
        evidence_raw = f.path(str(f.wave["wave_evidence_path"])).read_bytes()
        f.path(str(f.wave["wave_evidence_path"])).unlink()
        prepared = self.call(wave_review.prepare_publication, str(f.wave_path))
        self.assertEqual(prepared.exit_code, 0, prepared.detail)
        prospective_raw = f.path(f.prospective_path).read_bytes()
        evidence = json.loads(evidence_raw)
        evidence["wave_record_identity"] = hashlib.sha256(prospective_raw).hexdigest()
        f.write(str(f.wave["wave_evidence_path"]), evidence)
        published = self.call(wave_review.publish, str(f.wave_path))
        self.assertEqual(published.exit_code, 0, published.detail)
        self.assertEqual(f.path(f.wave_path).read_bytes(), prospective_raw)
        repeated = self.call(wave_review.publish, str(f.wave_path))
        self.assertEqual(repeated.exit_code, 0, repeated.detail)
        done = self.call(wave_review.done, str(f.wave_path))
        self.assertEqual(done.exit_code, 0, done.detail)

    def test_publish_fails_closed_on_missing_evidence_and_identity_or_byte_drift(self) -> None:
        f = self.fixture
        f.set_gated()
        f.path(str(f.wave["wave_evidence_path"])).unlink()
        result = self.call(wave_review.publish, str(f.wave_path))
        self.assertEqual(result.exit_code, 2)

        other = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-publish-drift-")))
        self.addCleanup(lambda: shutil.rmtree(other.parent, ignore_errors=True))
        other.set_gated()
        other.evidence["wave_record_identity"] = "f" * 64
        other.write(str(other.wave["wave_evidence_path"]), other.evidence)
        previous = Path.cwd()
        try:
            __import__("os").chdir(other.root)
            result = wave_review.publish(str(other.wave_path), other.workspace_roots)
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("prospective", result.detail)

        published = WaveFixture(Path(tempfile.mkdtemp(prefix="wave-published-drift-")))
        self.addCleanup(lambda: shutil.rmtree(published.parent, ignore_errors=True))
        published.write_raw(published.prospective_path, b"{}")
        previous = Path.cwd()
        try:
            __import__("os").chdir(published.root)
            result = wave_review.publish(
                str(published.wave_path), published.workspace_roots
            )
        finally:
            __import__("os").chdir(previous)
        self.assertEqual(result.exit_code, 1)

    def test_cli_help_requires_workspace_map_and_exposes_publish(self) -> None:
        run = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "wave_review.py"), "--help"],
            cwd=self.fixture.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("publish", run.stdout)
        mapped_arguments: list[str] = []
        for workspace_id, root in self.fixture.workspace_roots.items():
            mapped_arguments.extend(("--workspace-root", f"{workspace_id}={root}"))
        positive = subprocess.run(
            [
                sys.executable,
                "-B",
                str(TOOLS / "wave_review.py"),
                "preflight",
                str(self.fixture.wave_path),
                *mapped_arguments,
            ],
            cwd=self.fixture.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(positive.returncode, 0, positive.stderr)
        self.assertTrue(positive.stdout.startswith("PASS:"), positive.stdout)
        usage = subprocess.run(
            [
                sys.executable,
                "-B",
                str(TOOLS / "wave_review.py"),
                "preflight",
                str(self.fixture.wave_path),
            ],
            cwd=self.fixture.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(usage.returncode, 2)
        self.assertTrue(usage.stderr.startswith("INPUT_ERROR:"), usage.stderr)


if __name__ == "__main__":
    unittest.main()
