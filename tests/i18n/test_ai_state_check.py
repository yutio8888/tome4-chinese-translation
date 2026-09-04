from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
FIXTURES = ROOT / "tests" / "i18n" / "fixtures" / "paseo_state_v2"
EVIDENCE_FIXTURES = ROOT / "tests" / "i18n" / "fixtures" / "review_evidence"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import ai_state_check
import surface_screen_manifest
import surface_screen_result_check


class StateCheckerFixtureTests(unittest.TestCase):
    """File-backed coverage; tests never scan ignored .ai/task records."""

    def setUp(self) -> None:
        artifacts = ROOT / ".artifacts" / "i18n"
        artifacts.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-state-check-", dir=artifacts)
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        self.copy_index = 0

    @staticmethod
    def _read(path: Path) -> dict[str, object]:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _write(path: Path, value: object) -> None:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _copy_fixture(self, name: str) -> tuple[Path, dict[str, object], dict[str, object]]:
        self.copy_index += 1
        directory = self.work / f"{name}-{self.copy_index}"
        shutil.copytree(FIXTURES / name, directory)
        state_path, record_path = directory / "STATE.json", directory / "review.json"
        state, record = self._read(state_path), self._read(record_path)
        relative = directory.relative_to(ROOT)
        state["review_records"] = [str(relative / "review.json")]
        if name == "code":
            locator = record["candidate_locator"]
            assert isinstance(locator, dict)
            locator["spec_path"] = str(relative / "SPEC.md")
            locator["diff_path"] = str(relative / "CODE_DIFF-FINAL_REVIEW-0-1.patch")
        else:
            input_path = str(relative / "CONTEXTUAL-ENVELOPE-review-1.json")
            state["child_dispatches"][0]["input_path"] = input_path  # type: ignore[index]
            record["input_path"] = input_path
        self._write(record_path, record)
        self._write(state_path, state)
        return state_path, state, record

    def _copy_v2_fixture(self) -> tuple[Path, dict[str, object], Path, Path]:
        self.copy_index += 1
        workspace = self.work / f"v2-workspace-{self.copy_index}"
        shutil.copytree(FIXTURES / "contextual_v2", workspace)
        state_path = workspace / "STATE.json"
        return state_path, self._read(state_path), workspace, workspace

    def _check_v2(self, mutate=None) -> ai_state_check.CheckResult:
        state_path, state, directory, workspace = self._copy_v2_fixture()
        if mutate:
            mutate(state, directory)
        self._write(state_path, state)
        return ai_state_check.check_state(state_path, workspace_root=workspace)

    def test_contextual_v2_fixture_and_fail_closed_state_matrix(self) -> None:
        self.assertEqual(self._check_v2().outcome, "DONE_VERIFIED")

        def schema4(state, _): state["schema_version"] = 4
        def mixed_contracts(state, _):
            state["review_contracts"].append("translation_contextual_v1")
            state["completed_review_contracts"].append("translation_contextual_v1")
        def singular_pointer(state, _): state["contextual_reviewer"] = state.pop("contextual_reviewers")[0]
        def missing_lane(state, _):
            state["review_records"].pop(0)
            state["child_dispatches"].pop(0)
        def duplicate_agent(state, _): state["child_dispatches"][1]["agent_id"] = "agent-lane-1"
        def missing_parent_agent_id(state, _): state["child_dispatches"][0].pop("parent_agent_id")
        def missing_workspace_id(state, _): state["child_dispatches"][0].pop("workspace_id")
        def raw_hash_drift(_state, directory):
            raw = directory / ".ai/reviews/fixture-contextual-v2/raw-lane-1.txt"
            raw.write_bytes(raw.read_bytes() + b"drift")
        def raw_path_drift(_state, directory):
            record = self._read(directory / "review-lane-1.json")
            record["raw_output_path"] = ".ai/reviews/fixture-contextual-v2/raw-foreign.txt"
            self._write(directory / "review-lane-1.json", record)
        def mixed_stage(_state, directory):
            record = self._read(directory / "review-lane-2.json")
            record["review_kind"] = "full"; record.pop("lane")
            self._write(directory / "review-lane-2.json", record)
        def coordinate_conflict(_state, directory):
            record = self._read(directory / "review-lane-2.json")
            record["lane"]["index"] = 1
            self._write(directory / "review-lane-2.json", record)
        def final_review_lane(_state, directory):
            record = self._read(directory / "review-lane-1.json")
            record["review_phase"] = "FINAL_REVIEW"
            self._write(directory / "review-lane-1.json", record)
        def wrong_closure_parent(_state, directory):
            record = self._read(directory / "review-final-full.json")
            record.update({
                "review_phase": "RE_REVIEW", "review_kind": "closure",
                "parent_review_kind": "lane_group", "parent_coverage_identity": "0" * 64,
                "inclusion": [{"revision_key": key, "reasons": ["changed_target"]} for key in ("r1", "r2", "r3", "r4")],
            })
            self._write(directory / "review-final-full.json", record)

        for mutation in (
            schema4, mixed_contracts, singular_pointer, missing_lane, duplicate_agent,
            missing_parent_agent_id, missing_workspace_id,
            raw_hash_drift, raw_path_drift, mixed_stage, coordinate_conflict,
            final_review_lane, wrong_closure_parent,
        ):
            with self.subTest(mutation=mutation.__name__):
                self.assertNotEqual(self._check_v2(mutation).exit_code, 0)

    def test_contextual_v2_dispatch_prompt_is_gated_for_all_records(self) -> None:
        with patch.object(
            ai_state_check.contextual_lane_manifest,
            "render_dispatch_prompt",
            wraps=ai_state_check.contextual_lane_manifest.render_dispatch_prompt,
        ) as render:
            self.assertEqual(self._check_v2().outcome, "DONE_VERIFIED")
        identities = [call.args[0] for call in render.call_args_list]
        state_path, state, directory, _ = self._copy_v2_fixture()
        final_record = self._read(directory / "review-final-full.json")
        self.assertIn(final_record["candidate_identity"], identities)

    def test_contextual_v2_nested_shadow_artifacts_cannot_override_workspace_root(self) -> None:
        state_path, state, directory, workspace = self._copy_v2_fixture()
        shadow = workspace / "nested-shadow"
        shadow.mkdir()
        shutil.copytree(workspace / ".ai", shadow / ".ai")
        for record_name in (
            "review-lane-1.json", "review-lane-2.json", "review-lane-3.json",
            "review-lane-4.json", "review-final-full.json",
        ):
            shutil.copy2(workspace / record_name, shadow / record_name)
        state["review_records"] = [
            f"nested-shadow/{Path(path).name}" for path in state["review_records"]
        ]
        shadow_raw = shadow / ".ai/reviews/fixture-contextual-v2/raw-lane-1.txt"
        shadow_raw.write_bytes(shadow_raw.read_bytes() + b"shadow drift")
        self._write(state_path, state)

        result = ai_state_check.check_state(state_path, workspace_root=workspace)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_contextual_v2_public_cli_uses_explicit_workspace_root(self) -> None:
        state_path, _state, _directory, workspace = self._copy_v2_fixture()
        run = subprocess.run(
            [
                sys.executable, "-B", str(TOOLS / "ai_state_check.py"),
                "STATE.json", "--workspace-root", str(workspace),
            ],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("DONE_VERIFIED:", run.stdout)

    def test_contextual_v2_complete_lane_stage_cannot_be_latest(self) -> None:
        def complete_lane_latest(state, _directory):
            state["review_records"].pop()
            state["child_dispatches"].pop()
            state["contextual_reviewers"] = [
                {
                    "role": "REVIEWER",
                    "purpose": "translation_contextual_v2",
                    "candidate_identity": dispatch["candidate_identity"],
                    "dispatch_id": dispatch["dispatch_id"],
                    "input_path": dispatch["input_path"],
                    "agent_id": dispatch["agent_id"],
                    "lane_group_identity": dispatch["lane_group_identity"],
                    "lane_index": dispatch["lane_index"],
                }
                for dispatch in state["child_dispatches"]
            ]
            state["cycle"] = 0

        result = self._check_v2(complete_lane_latest)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("latest v2 stage must be a successful FINAL_REVIEW/full", result.detail)

    def test_contextual_v2_well_formed_closure_with_wrong_parent_is_rejected(self) -> None:
        def wrong_parent(state, directory):
            record = self._read(directory / "review-final-full.json")
            record.update({
                "review_phase": "RE_REVIEW",
                "review_kind": "closure",
                "parent_review_kind": "lane_group",
                "parent_coverage_identity": "0" * 64,
                "inclusion": [
                    {"revision_key": key, "reasons": ["changed_target"]}
                    for key in ("r1", "r2", "r3", "r4")
                ],
            })
            self._write(directory / "review-final-full.json", record)

        result = self._check_v2(wrong_parent)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("closure parent coverage binding mismatch", result.detail)

    def test_contextual_v2_rejects_each_group_identifier_reused_across_stages(self) -> None:
        first = ("group-a", "1" * 64, ".ai/task/t/CONTEXTUAL-LANE-GROUP-group-a.json")
        for index, label in enumerate(("group_id", "group_identity", "group_manifest_path")):
            with self.subTest(label=label):
                used_ids: set[str] = set()
                used_identities: set[str] = set()
                used_paths: set[str] = set()
                self.assertTrue(ai_state_check._claim_lane_group_identifiers(
                    *first,
                    used_group_ids=used_ids,
                    used_group_identities=used_identities,
                    used_group_manifest_paths=used_paths,
                )[0])
                second = ["group-b", "2" * 64, ".ai/task/t/CONTEXTUAL-LANE-GROUP-group-b.json"]
                second[index] = first[index]
                valid, detail = ai_state_check._claim_lane_group_identifiers(
                    *second,
                    used_group_ids=used_ids,
                    used_group_identities=used_identities,
                    used_group_manifest_paths=used_paths,
                )
                self.assertFalse(valid)
                self.assertIn(label, detail)

    def test_v1_canonical_payload_acceptance_is_unchanged(self) -> None:
        base = {
            "contract": "translation_contextual_v1",
            "ordered_revision_keys": [],
            "translation_snapshot": [],
            "fixed_source_identity": "commit:" + "1" * 40,
            "terminology_snapshot": "",
            "bounded_context": [],
            "rendered_briefing": "",
        }
        ai_state_check._canonical_payload_bytes(base)
        duplicate = json.loads(json.dumps(base))
        duplicate.update({
            "ordered_revision_keys": ["r1", "r1"],
            "translation_snapshot": [
                {"revision_key": "r1", "source": "", "target": ""},
                {"revision_key": "r1", "source": "", "target": ""},
            ],
            "bounded_context": [
                {"revision_key": "r1", "context": ""},
                {"revision_key": "r1", "context": ""},
            ],
        })
        ai_state_check._canonical_payload_bytes(duplicate)

    def _check_code(self, mutate=None, *, target: str | None = None) -> ai_state_check.CheckResult:
        state_path, state, record = self._copy_fixture("code")
        if mutate:
            mutate(state, record, state_path.parent)
        self._write(state_path.parent / "review.json", record)
        self._write(state_path, state)
        return ai_state_check.check_state(state_path, target=target)

    def _check_contextual(self, mutate=None, *, target: str | None = None) -> ai_state_check.CheckResult:
        state_path, state, record = self._copy_fixture("contextual")
        if mutate:
            mutate(state, record, state_path.parent)
        self._write(state_path.parent / "review.json", record)
        self._write(state_path, state)
        return ai_state_check.check_state(state_path, target=target)

    def _policy_state(self) -> tuple[Path, dict[str, object]]:
        state_path, state, _ = self._copy_fixture("contextual")
        state.update({
            "schema_version": 4,
            "mode": "implement",
            "change_class": "translation_workflow",
            "orchestrator_agent_id": "agent-orchestrator",
            "cycle": 2,
            "max_cycles": 3,
            "final_validation_passed": True,
            "child_dispatches": [],
            "review_records": [],
            "senior_review_records": [],
        })
        return state_path, state

    def _add_policy_contextual_record(
        self,
        state_path: Path,
        state: dict[str, object],
        *,
        dispatch_id: str,
        phase: str,
        cycle: int,
        attempt: int,
        review_kind: str,
        keys: list[str],
        sources: dict[str, str] | None = None,
        targets: dict[str, str] | None = None,
        result: str = "PASS",
        parent_candidate_identity: str | None = None,
        inclusion: list[dict[str, object]] | None = None,
        senior: bool = False,
    ) -> str:
        sources = sources or {key: f"Source {key}" for key in keys}
        targets = targets or {key: f"Target {key}" for key in keys}
        payload = {
            "contract": "translation_contextual_v1",
            "ordered_revision_keys": keys,
            "translation_snapshot": [
                {
                    "revision_key": key,
                    "source": sources[key],
                    "target": targets[key],
                }
                for key in keys
            ],
            "fixed_source_identity": "commit:61bb370c33e46c4df4b2bbfd56113a0de1822300",
            "terminology_snapshot": "fixture terminology",
            "bounded_context": [
                {"revision_key": key, "context": f"context {key}"}
                for key in keys
            ],
            "rendered_briefing": f"fixture {dispatch_id}",
        }
        identity = hashlib.sha256(ai_state_check._canonical_payload_bytes(payload)).hexdigest()
        directory = state_path.parent
        envelope_path = directory / f"CONTEXTUAL-ENVELOPE-{dispatch_id}.json"
        self._write(envelope_path, {"candidate_identity": identity, "payload": payload})
        input_path = str(envelope_path.relative_to(ROOT))
        agent_id = f"agent-{dispatch_id}"
        record: dict[str, object] = {
            "task_id": state["task_id"],
            "review_contract": "translation_contextual_v1",
            "review_phase": phase,
            "cycle": cycle,
            "attempt": attempt,
            "reviewer_role": "REVIEWER",
            "purpose": "translation_contextual_v1",
            "dispatch_id": dispatch_id,
            "agent_id": agent_id,
            "result": result,
            "candidate_identity": identity,
            "input_path": input_path,
            "review_kind": review_kind,
        }
        if review_kind == "closure":
            record["parent_candidate_identity"] = parent_candidate_identity
            record["inclusion"] = inclusion if inclusion is not None else [
                {"revision_key": key, "reasons": ["changed_target"]}
                for key in keys
            ]
        record_path = directory / f"{dispatch_id}.json"
        self._write(record_path, record)
        field = "senior_review_records" if senior else "review_records"
        state[field].append(str(record_path.relative_to(ROOT)))  # type: ignore[union-attr]
        state["child_dispatches"].append({  # type: ignore[union-attr]
            "dispatch_id": dispatch_id,
            "role": "REVIEWER",
            "purpose": "translation_contextual_v1",
            "agent_id": agent_id,
            "lineage_verified": True,
            "lifecycle": "archived",
            "archive_confirmed": True,
            "candidate_identity": identity,
            "input_path": input_path,
        })
        return identity

    def _finish_policy_state(
        self, state_path: Path, state: dict[str, object]
    ) -> ai_state_check.CheckResult:
        self._write(state_path, state)
        return ai_state_check.check_state(state_path)

    def _positive_policy_sequence(
        self, *, final_cycle: int = 2,
    ) -> tuple[Path, dict[str, object], str]:
        state_path, state = self._policy_state()
        state["cycle"] = final_cycle
        full_sources = {"r1": "Source r1", "r2": "Source r2", "r3": "Source r3"}
        initial_identity = self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="initial-full", phase="REVIEW", cycle=0, attempt=1,
            review_kind="full", keys=["r1", "r2", "r3"], sources=full_sources,
        )
        self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="closure-one", phase="RE_REVIEW", cycle=1, attempt=1,
            review_kind="closure", keys=["r2"], sources=full_sources,
            parent_candidate_identity=initial_identity,
        )
        self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="final-full", phase="FINAL_REVIEW", cycle=final_cycle, attempt=1,
            review_kind="full", keys=["r1", "r2", "r3"], sources=full_sources,
        )
        return state_path, state, initial_identity

    def _evidence_code(self) -> tuple[Path, dict[str, object], dict[str, object], Path]:
        directory = self.work / "evidence-code"
        shutil.copytree(FIXTURES / "code", directory)
        shutil.copytree(EVIDENCE_FIXTURES / ".ai", self.work / ".ai")
        state_path, record_path = directory / "STATE.json", directory / "review.json"
        state, record = self._read(state_path), self._read(record_path)
        state["task_id"] = "review-evidence-fixture"
        record["task_id"] = "review-evidence-fixture"
        relative = directory.relative_to(self.work)
        state["review_records"] = [str(relative / "review.json")]
        locator = record["candidate_locator"]
        assert isinstance(locator, dict)
        locator["spec_path"] = str(relative / "SPEC.md")
        locator["diff_path"] = str(relative / "CODE_DIFF-FINAL_REVIEW-0-1.patch")
        self._write(record_path, record)
        self._write(state_path, state)
        return state_path, state, record, directory

    @staticmethod
    def _new_file_patch(relative: str, content: bytes, *, duplicate: bool = False) -> bytes:
        lines = content.splitlines(keepends=True)
        if content and not lines:
            lines = [content]
        blocks: list[bytes] = []
        for _ in range(2 if duplicate else 1):
            block = [
                f"diff --git a/{relative} b/{relative}\n".encode(),
                b"new file mode 100644\n",
                b"--- /dev/null\n",
                f"+++ b/{relative}\n".encode(),
                f"@@ -0,0 +1,{len(lines)} @@\n".encode(),
            ]
            for line in lines:
                if line.endswith(b"\n"):
                    block.append(b"+" + line)
                else:
                    block.extend((b"+" + line + b"\n", b"\\ No newline at end of file\n"))
            blocks.append(b"".join(block))
        return b"".join(blocks)

    def _install_evidence_candidate(
        self, state: dict[str, object], record: dict[str, object], directory: Path,
        *, content: bytes | None = None, spec: bytes | None = None,
        duplicate: bool = False, diff_name: str = "CODE_DIFF-FINAL_REVIEW-0-1.patch",
    ) -> bytes:
        if content is None:
            content = (EVIDENCE_FIXTURES / "good-reconciliation.json").read_bytes()
        if spec is None:
            spec = b"# Fixture SPEC\n"
        sidecar = directory / "EVIDENCE-RECONCILIATION.json"
        sidecar.write_bytes(content)
        spec_path = directory / "SPEC.md"
        spec_path.write_bytes(spec)
        diff_path = directory / diff_name
        relative_sidecar = (directory.relative_to(self.work) / sidecar.name).as_posix()
        completed = subprocess.run(
            ["git", "diff", "--no-index", "--", "/dev/null", relative_sidecar],
            cwd=self.work,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1, completed.stderr.decode())
        diff = completed.stdout
        if duplicate:
            diff += diff
        diff_path.write_bytes(diff)
        locator = record["candidate_locator"]
        assert isinstance(locator, dict)
        locator["spec_path"] = str(spec_path.relative_to(self.work))
        locator["diff_path"] = str(diff_path.relative_to(self.work))
        record["candidate_ref"] = ai_state_check.candidate_ref(spec, diff)
        return diff

    def test_new_file_parser_ignores_rename_only_patch_without_sidecar(self) -> None:
        rename = (
            b"diff --git a/x b/archive/x\n"
            b"similarity index 100%\n"
            b"rename from x\n"
            b"rename to archive/x\n"
        )
        self.assertIsNone(
            ai_state_check._new_file_entry_bytes(rename, "evidence-code/EVIDENCE-RECONCILIATION.json")
        )

    def test_new_file_parser_rejects_truncation_crlf_bad_index_and_modification(self) -> None:
        content = (EVIDENCE_FIXTURES / "good-reconciliation.json").read_bytes()
        directory = self.work / "parser"
        directory.mkdir()
        sidecar = directory / "EVIDENCE-RECONCILIATION.json"
        sidecar.write_bytes(content)
        completed = subprocess.run(
            ["git", "diff", "--no-index", "--", "/dev/null", "parser/EVIDENCE-RECONCILIATION.json"],
            cwd=self.work,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1, completed.stderr.decode())
        positive = completed.stdout
        self.assertEqual(
            ai_state_check._new_file_entry_bytes(
                positive, "parser/EVIDENCE-RECONCILIATION.json"
            ),
            content,
        )
        bad_index = positive.replace(b"index 0000000..", b"index invalid..", 1)
        self.assertNotEqual(bad_index, positive)
        cases = {
            "truncated": positive[:-1],
            "crlf": positive.replace(b"\n", b"\r\n"),
            "bad_index": bad_index,
            "modification": positive.replace(
                b"new file mode 100644\n", b"", 1
            ).replace(b"--- /dev/null\n", b"--- a/parser/EVIDENCE-RECONCILIATION.json\n", 1),
        }
        for name, patch in cases.items():
            with self.subTest(case=name):
                with self.assertRaises(ai_state_check.ContractError):
                    ai_state_check._new_file_entry_bytes(
                        patch, "parser/EVIDENCE-RECONCILIATION.json"
                    )

    def test_new_file_parser_reconstructs_real_git_patch_with_12_digit_index(self) -> None:
        content = (EVIDENCE_FIXTURES / "good-reconciliation.json").read_bytes()
        directory = self.work / "parser-full-index"
        directory.mkdir()
        sidecar = directory / "EVIDENCE-RECONCILIATION.json"
        sidecar.write_bytes(content)
        completed = subprocess.run(
            [
                "git", "-c", "core.abbrev=12", "diff", "--no-index", "--",
                "/dev/null", "parser-full-index/EVIDENCE-RECONCILIATION.json",
            ],
            cwd=self.work,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1, completed.stderr.decode())
        self.assertIn(b"index 000000000000..", completed.stdout)
        self.assertEqual(
            ai_state_check._new_file_entry_bytes(
                completed.stdout, "parser-full-index/EVIDENCE-RECONCILIATION.json"
            ),
            content,
        )

    def _check_evidence_state(self, state_path: Path) -> ai_state_check.CheckResult:
        with patch.object(ai_state_check, "ROOT", self.work):
            return ai_state_check.check_state(state_path)

    def test_evidence_e1_no_bound_record_fails_existing_closure_predicate(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        state.update({"schema_version": 3, "mode": "review_only", "change_class": "infrastructure", "review_records": []})
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("no bound completion record", result.detail)

    def test_evidence_e2_required_for_v3_review_only_infrastructure(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        state.update({"schema_version": 3, "mode": "review_only", "change_class": "infrastructure"})
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))
        self.assertIn("evidence_reconciliation_required", result.detail)

    def test_evidence_surface_colisting_never_waives_code_records(self) -> None:
        # C2-05: when a surface task is co-listed with a real code record,
        # the surface terminal never waives the code sidecar reconciliation.
        state_path, state, record, directory = self._evidence_code()
        task_id = str(state["task_id"])
        state.update({
            "schema_version": 5,
            "mode": "review_only",
            "change_class": "translation_workflow",
            "review_contracts": ["code_legacy_v1", "translation_surface_screen_v1"],
            "completed_review_contracts": ["code_legacy_v1", "translation_surface_screen_v1"],
        })
        zero = surface_screen_manifest.build_zero_payload(task_id=task_id)
        zero_path = surface_screen_manifest.zero_artifact_path(task_id)
        zero_file = self.work / zero_path
        zero_file.parent.mkdir(parents=True, exist_ok=True)
        zero_file.write_bytes(surface_screen_result_check.canonical_bytes(zero))
        state["surface_zero_path"] = zero_path
        draft_path = f".ai/task/{task_id}/SURFACE-SCREEN-INPUT-DRAFT.json"
        (self.work / draft_path).parent.mkdir(parents=True, exist_ok=True)
        (self.work / draft_path).write_bytes(surface_screen_result_check.canonical_bytes({
            "contract": "translation_surface_screen_v1",
            "fixed_source_identity": "commit:" + "3" * 40,
            "terminology_snapshot": "surface terms",
            "rules_version": "surface-rules/1",
            "rendered_briefing": "lane neutral",
            "entries": [],
        }))
        state["surface_screen_input_path"] = draft_path
        state["surface_evidence_binding"] = {
            "algorithm": "surface-evidence-binding/1",
            "task_id": task_id,
            "terminal": "zero",
            "artifact_sha256": {
                locator: hashlib.sha256((self.work / locator).read_bytes()).hexdigest()
                for locator in (zero_path, draft_path)
            },
        }
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))
        self.assertIn("evidence_reconciliation_required", result.detail)

    def test_evidence_e3_reviewer_must_not_be_orchestrator(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        state.update({"schema_version": 3, "mode": "review_only", "change_class": "infrastructure", "orchestrator_agent_id": "agent-review-1"})
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("agent_id must differ", result.detail)

    def test_evidence_f_is_candidate_bound_and_on_disk_sidecar_is_checked(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        self._install_evidence_candidate(state, record, directory)
        self._write(directory / "review.json", record)
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual((result.outcome, result.exit_code), ("DONE_VERIFIED", 0), result)

        directory.joinpath("EVIDENCE-RECONCILIATION.json").write_bytes(b"different\n")
        result = self._check_evidence_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("on-disk sidecar", result.detail)

    def test_evidence_sidecar_task_id_must_match_state(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        content = json.loads((EVIDENCE_FIXTURES / "good-reconciliation.json").read_text(encoding="utf-8"))
        content["task_id"] = "different-task"
        self._install_evidence_candidate(
            state, record, directory,
            content=(json.dumps(content, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        )
        self._write(directory / "review.json", record)
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("task_id", result.detail)

    def test_evidence_binding_rejects_duplicate_new_file_and_handles_no_newline_marker(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        content = (EVIDENCE_FIXTURES / "good-reconciliation.json").read_bytes().rstrip(b"\n")
        self._install_evidence_candidate(state, record, directory, content=content)
        self._write(directory / "review.json", record)
        self._write(state_path, state)
        self.assertEqual(self._check_evidence_state(state_path).outcome, "DONE_VERIFIED")

        self._install_evidence_candidate(state, record, directory, duplicate=True)
        self._write(directory / "review.json", record)
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("duplicate new-file entries", result.detail)

    def test_evidence_binding_accepts_two_attempts_when_disk_is_latest(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        first = self._install_evidence_candidate(state, record, directory)
        self._write(directory / "review.json", record)
        second = dict(record)
        second["dispatch_id"] = "review-2"
        second["agent_id"] = "agent-review-2"
        second["attempt"] = 2
        second_diff = directory / "CODE_DIFF-FINAL_REVIEW-0-2.patch"
        second_content = bytearray((EVIDENCE_FIXTURES / "good-reconciliation.json").read_bytes())
        second_content.extend(b"\n")
        (directory / "EVIDENCE-RECONCILIATION.json").write_bytes(bytes(second_content))
        completed = subprocess.run(
            ["git", "diff", "--no-index", "--", "/dev/null", "evidence-code/EVIDENCE-RECONCILIATION.json"],
            cwd=self.work,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        second_diff.write_bytes(completed.stdout)
        second["candidate_locator"] = {
            "spec_path": "evidence-code/SPEC.md",
            "diff_path": "evidence-code/CODE_DIFF-FINAL_REVIEW-0-2.patch",
        }
        second["candidate_ref"] = ai_state_check.candidate_ref(
            (directory / "SPEC.md").read_bytes(), second_diff.read_bytes()
        )
        second_path = directory / "review-2.json"
        self._write(second_path, second)
        state["review_records"].append("evidence-code/review-2.json")  # type: ignore[union-attr]
        state["child_dispatches"].append({  # type: ignore[union-attr]
            "dispatch_id": "review-2", "role": "REVIEWER", "purpose": "normal_review",
            "agent_id": "agent-review-2", "lineage_verified": True,
            "lifecycle": "archived", "archive_confirmed": True,
        })
        directory.joinpath("EVIDENCE-RECONCILIATION.json").write_bytes(bytes(second_content))
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual((result.outcome, result.exit_code), ("DONE_VERIFIED", 0), result)

    def test_evidence_latest_paired_records_must_have_identical_embedded_sidecar(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        self._install_evidence_candidate(state, record, directory)
        self._write(directory / "review.json", record)

        cross_directory = directory / "cross"
        cross_directory.mkdir()
        second_content = (EVIDENCE_FIXTURES / "good-reconciliation.json").read_bytes() + b"\n"
        second_diff = cross_directory / "CODE_DIFF-FINAL_REVIEW-0-1.patch"
        cross_sidecar = directory / "EVIDENCE-RECONCILIATION.json"
        completed = subprocess.run(
            ["git", "diff", "--no-index", "--", "/dev/null", "evidence-code/EVIDENCE-RECONCILIATION.json"],
            cwd=self.work,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        # The second embedded candidate is deliberately distinct but still a valid sidecar.
        cross_sidecar.write_bytes(second_content)
        completed = subprocess.run(
            ["git", "diff", "--no-index", "--", "/dev/null", "evidence-code/EVIDENCE-RECONCILIATION.json"],
            cwd=self.work,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        second_diff.write_bytes(completed.stdout)
        cross_sidecar.write_bytes((EVIDENCE_FIXTURES / "good-reconciliation.json").read_bytes())

        second = dict(record)
        second.update({"dispatch_id": "review-2", "agent_id": "agent-review-2"})
        second["candidate_locator"] = {
            "spec_path": "evidence-code/SPEC.md",
            "diff_path": "evidence-code/cross/CODE_DIFF-FINAL_REVIEW-0-1.patch",
        }
        second["candidate_ref"] = ai_state_check.candidate_ref(
            (directory / "SPEC.md").read_bytes(), second_diff.read_bytes()
        )
        self._write(directory / "review-2.json", second)
        state["review_records"].append("evidence-code/review-2.json")  # type: ignore[union-attr]
        state["child_dispatches"].append({  # type: ignore[union-attr]
            "dispatch_id": "review-2", "role": "REVIEWER", "purpose": "normal_review",
            "agent_id": "agent-review-2", "lineage_verified": True,
            "lifecycle": "archived", "archive_confirmed": True,
        })
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("disagree", result.detail)

    def test_evidence_latest_tied_records_must_derive_one_sidecar_path(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        self._install_evidence_candidate(state, record, directory)
        self._write(directory / "review.json", record)

        other_directory = self.work / "evidence-code-other"
        other_directory.mkdir()
        other_sidecar = other_directory / "EVIDENCE-RECONCILIATION.json"
        other_sidecar.write_bytes((EVIDENCE_FIXTURES / "good-reconciliation.json").read_bytes())
        other_spec = other_directory / "SPEC.md"
        other_spec.write_bytes(b"# Fixture SPEC\n")
        completed = subprocess.run(
            [
                "git", "diff", "--no-index", "--", "/dev/null",
                "evidence-code-other/EVIDENCE-RECONCILIATION.json",
            ],
            cwd=self.work,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1, completed.stderr.decode())
        other_diff = other_directory / "CODE_DIFF-FINAL_REVIEW-0-1.patch"
        other_diff.write_bytes(completed.stdout)

        second = dict(record)
        second.update({"dispatch_id": "review-2", "agent_id": "agent-review-2"})
        second["candidate_locator"] = {
            "spec_path": "evidence-code-other/SPEC.md",
            "diff_path": "evidence-code-other/CODE_DIFF-FINAL_REVIEW-0-1.patch",
        }
        second["candidate_ref"] = ai_state_check.candidate_ref(
            other_spec.read_bytes(), other_diff.read_bytes()
        )
        second_path = directory / "review-2.json"
        self._write(second_path, second)
        state["review_records"].append("evidence-code/review-2.json")  # type: ignore[union-attr]
        state["child_dispatches"].append({  # type: ignore[union-attr]
            "dispatch_id": "review-2", "role": "REVIEWER", "purpose": "normal_review",
            "agent_id": "agent-review-2", "lineage_verified": True,
            "lifecycle": "archived", "archive_confirmed": True,
        })
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("different sidecar paths", result.detail)

    def test_evidence_citation_consistency_rejects_uncited_exact_review_path(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        extra = self.work / ".ai" / "reviews" / "review-evidence-fixture" / "review-03.json"
        self._write(extra, {"task_id": "extra", "findings": [{"id": "Z1"}]})
        self._install_evidence_candidate(
            state, record, directory,
            spec=b"# Fixture SPEC cites .ai/reviews/review-evidence-fixture/review-03.json\n",
        )
        self._write(directory / "review.json", record)
        self._write(state_path, state)
        result = self._check_evidence_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("citation", result.detail)

    def test_evidence_schema_2_compatibility_and_implement_validate_if_present(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        state.update({"schema_version": 2, "mode": "review_only", "change_class": "infrastructure"})
        self._write(state_path, state)
        self.assertEqual(self._check_evidence_state(state_path).outcome, "DONE_VERIFIED")

        state["schema_version"] = 3
        state["mode"] = "implement"
        self._write(state_path, state)
        self.assertEqual(self._check_evidence_state(state_path).outcome, "DONE_VERIFIED")

    def test_evidence_schema_3_requires_valid_change_class_and_code_record(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        for change_class in (None, "invalid"):
            with self.subTest(change_class=change_class):
                state.update({"schema_version": 3, "mode": "review_only"})
                if change_class is None:
                    state.pop("change_class", None)
                else:
                    state["change_class"] = change_class
                self._write(state_path, state)
                result = self._check_evidence_state(state_path)
                self.assertEqual(result.exit_code, 1)
                self.assertIn("change_class", result.detail)

        state_path, state, record = self._copy_fixture("contextual")
        state.update({
            "schema_version": 3,
            "change_class": "infrastructure",
            "orchestrator_agent_id": "agent-orchestrator",
        })
        self._write(state_path.parent / "review.json", record)
        self._write(state_path, state)
        result = ai_state_check.check_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("evidence_reconciliation_required", result.detail)

    def test_evidence_scope_audit_is_checked_when_present_in_schema_3(self) -> None:
        state_path, state, record, directory = self._evidence_code()
        audit_path = self.work / "evidence-code" / "scope-audit.json"
        shutil.copy2(EVIDENCE_FIXTURES / "scope-audit.json", audit_path)
        state.update({"schema_version": 3, "change_class": "standard", "senior_review_records": ["evidence-code/scope-audit.json"]})
        self._write(state_path, state)
        self.assertEqual(self._check_evidence_state(state_path).outcome, "DONE_VERIFIED")
        audit = self._read(audit_path)
        audit["calibration"] = {"F1": "keep"}
        self._write(audit_path, audit)
        result = self._check_evidence_state(state_path)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("scope_audit", result.detail)

    def test_production_code_and_contextual_fixtures_are_done_verified(self) -> None:
        self.assertEqual(ai_state_check.check_state(FIXTURES / "code" / "STATE.json").outcome, "DONE_VERIFIED")
        state_path, state, record = self._copy_fixture("contextual")
        self._write(state_path.parent / "review.json", record)
        self._write(state_path, state)
        self.assertEqual(ai_state_check.check_state(state_path).outcome, "DONE_VERIFIED")

    def test_schema4_translation_full_closure_final_full_can_close(self) -> None:
        state_path, state, _ = self._positive_policy_sequence()
        result = self._finish_policy_state(state_path, state)
        self.assertEqual((result.outcome, result.exit_code), ("DONE_VERIFIED", 0), result)

    def test_schema4_translation_failed_final_repair_successful_final_can_close(self) -> None:
        state_path, state = self._policy_state()
        self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="initial-full", phase="REVIEW", cycle=0, attempt=1,
            review_kind="full", keys=["r1", "r2", "r3"],
        )
        self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="failed-final", phase="FINAL_REVIEW", cycle=1, attempt=1,
            review_kind="full", keys=["r1", "r2", "r3"],
            result="CHANGES_REQUIRED",
        )
        self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="repair-full", phase="RE_REVIEW", cycle=2, attempt=1,
            review_kind="full", keys=["r1", "r2", "r3"],
        )
        self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="successful-final", phase="FINAL_REVIEW", cycle=3, attempt=1,
            review_kind="full", keys=["r1", "r2", "r3"],
        )
        state["cycle"] = 3
        result = self._finish_policy_state(state_path, state)
        self.assertEqual((result.outcome, result.exit_code), ("DONE_VERIFIED", 0), result)

    def test_schema4_translation_adjudicated_pass_overrides_producer_status(self) -> None:
        state_path, state, _ = self._positive_policy_sequence()
        final_path = state_path.parent / "final-full.json"
        final = self._read(final_path)
        final["status"] = "completed_with_findings"
        self._write(final_path, final)
        result = self._finish_policy_state(state_path, state)
        self.assertEqual((result.outcome, result.exit_code), ("DONE_VERIFIED", 0), result)

    def test_schema4_translation_closure_cannot_finish(self) -> None:
        state_path, state, _ = self._positive_policy_sequence()
        state["review_records"].pop()  # type: ignore[union-attr]
        state["child_dispatches"].pop()  # type: ignore[union-attr]
        state["cycle"] = 1
        result = self._finish_policy_state(state_path, state)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("FINAL_REVIEW/full", result.detail)

    def test_schema4_translation_stale_pass_cannot_hide_newer_failure(self) -> None:
        state_path, state, _ = self._positive_policy_sequence(final_cycle=3)
        final_path = state_path.parent / "final-full.json"
        final = self._read(final_path)
        final["status"] = "completed"
        final["result"] = "CHANGES_REQUIRED"
        self._write(final_path, final)
        result = self._finish_policy_state(state_path, state)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("successful FINAL_REVIEW/full", result.detail)

    def test_schema4_translation_stale_final_cannot_close_newer_state_cycle(self) -> None:
        state_path, state, _ = self._positive_policy_sequence()
        state["cycle"] = 3
        result = self._finish_policy_state(state_path, state)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("FINAL_REVIEW/full cycle must equal STATE.cycle", result.detail)

    def test_schema4_translation_record_cycles_are_state_and_limit_bounded(self) -> None:
        cases = (
            (3, "STATE.cycle"),
            (99, "max_cycles"),
        )
        for record_cycle, expected in cases:
            with self.subTest(record_cycle=record_cycle):
                state_path, state, _ = self._positive_policy_sequence()
                self._add_policy_contextual_record(
                    state_path, state,
                    dispatch_id=f"future-{record_cycle}",
                    phase="FINAL_REVIEW",
                    cycle=record_cycle,
                    attempt=1,
                    review_kind="full",
                    keys=["r1", "r2", "r3"],
                )
                result = self._finish_policy_state(state_path, state)
                self.assertEqual(result.exit_code, 1)
                self.assertIn(expected, result.detail)

    def test_schema4_translation_terminal_phases_must_be_ordered(self) -> None:
        cases = (
            ("initial-full.json", {"review_phase": "RE_REVIEW"}, "earliest"),
            (
                "closure-one.json",
                {"review_phase": "REVIEW", "review_kind": "full"},
                "intervening",
            ),
            ("final-full.json", {"review_phase": "RE_REVIEW"}, "latest"),
        )
        for record_name, mutation, expected in cases:
            with self.subTest(record=record_name):
                state_path, state, _ = self._positive_policy_sequence()
                record_path = state_path.parent / record_name
                record = self._read(record_path)
                record.update(mutation)
                self._write(record_path, record)
                result = self._finish_policy_state(state_path, state)
                self.assertEqual(result.exit_code, 1)
                self.assertIn(expected, result.detail)

    def test_schema4_translation_closure_key_source_and_parent_drift_fail(self) -> None:
        cases = (
            ("keys", ["r2"], {"r2": "Source r2"}, [
                {"revision_key": "r1", "reasons": ["changed_target"]}
            ], None, "closure keys"),
            ("source", ["r2"], {"r2": "Drifted source"}, None, None, "sources drift"),
            ("parent", ["r2"], {"r2": "Source r2"}, None, "0" * 64, "parent_candidate_identity"),
            ("order", ["r2", "r1"], {"r1": "Source r1", "r2": "Source r2"}, None, None, "ordered subset"),
        )
        for name, keys, sources, inclusion, parent_override, expected in cases:
            with self.subTest(case=name):
                state_path, state = self._policy_state()
                initial_identity = self._add_policy_contextual_record(
                    state_path, state,
                    dispatch_id=f"initial-{name}", phase="REVIEW", cycle=0, attempt=1,
                    review_kind="full", keys=["r1", "r2", "r3"],
                )
                self._add_policy_contextual_record(
                    state_path, state,
                    dispatch_id=f"closure-{name}", phase="RE_REVIEW", cycle=1, attempt=1,
                    review_kind="closure", keys=keys, sources=sources,
                    parent_candidate_identity=parent_override or initial_identity,
                    inclusion=inclusion,
                )
                self._add_policy_contextual_record(
                    state_path, state,
                    dispatch_id=f"final-{name}", phase="FINAL_REVIEW", cycle=2, attempt=1,
                    review_kind="full", keys=["r1", "r2", "r3"],
                )
                result = self._finish_policy_state(state_path, state)
                self.assertEqual(result.exit_code, 1)
                self.assertIn(expected, result.detail)

    def test_schema4_translation_closure_parent_must_be_latest_earlier_full(self) -> None:
        state_path, state = self._policy_state()
        initial_identity = self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="initial-parent", phase="REVIEW", cycle=0, attempt=1,
            review_kind="full", keys=["r1", "r2"],
        )
        self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="fallback-full", phase="RE_REVIEW", cycle=1, attempt=1,
            review_kind="full", keys=["r1", "r2"],
        )
        self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="stale-parent", phase="RE_REVIEW", cycle=2, attempt=1,
            review_kind="closure", keys=["r2"],
            parent_candidate_identity=initial_identity,
        )
        self._add_policy_contextual_record(
            state_path, state,
            dispatch_id="final-parent", phase="FINAL_REVIEW", cycle=3, attempt=1,
            review_kind="full", keys=["r1", "r2"],
        )
        state["cycle"] = 3
        result = self._finish_policy_state(state_path, state)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("latest earlier full", result.detail)

    def test_schema4_translation_max_cycles_default_and_authorization(self) -> None:
        state_path, state, _ = self._positive_policy_sequence(final_cycle=3)
        state.pop("max_cycles")
        result = self._finish_policy_state(state_path, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED", result)

        state_path, state, _ = self._positive_policy_sequence(final_cycle=4)
        state.pop("max_cycles")
        result = self._finish_policy_state(state_path, state)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("cycle must not exceed max_cycles", result.detail)

        state["max_cycles"] = 4
        result = self._finish_policy_state(state_path, state)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("max_cycles_user_authorized", result.detail)

        state["max_cycles_user_authorized"] = True
        result = self._finish_policy_state(state_path, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED", result)

    def test_schema3_translation_implement_record_remains_compatible(self) -> None:
        def schema3_implement(state, record, directory):
            state.update({
                "schema_version": 3,
                "mode": "implement",
                "change_class": "translation_workflow",
                "orchestrator_agent_id": "agent-orchestrator",
                "cycle": 99,
                "max_cycles": 1,
                "final_validation_passed": True,
            })

        result = self._check_contextual(schema3_implement)
        self.assertEqual((result.outcome, result.exit_code), ("DONE_VERIFIED", 0), result)

    def test_nul_candidate_vector_is_exact_and_not_the_obsolete_separator(self) -> None:
        spec = (FIXTURES / "code" / "SPEC.md").read_bytes()
        diff = (FIXTURES / "code" / "CODE_DIFF-FINAL_REVIEW-0-1.patch").read_bytes()
        self.assertEqual(ai_state_check.candidate_ref(spec, diff), "2c2efd1b4d0184dfdcc93c30349501a3076f7639c05c9a09ab2afca909da85e8")
        self.assertNotEqual(ai_state_check.candidate_ref(spec, diff), hashlib.sha256(spec + b"\n--diff--\n" + diff).hexdigest())

    def test_done_predicate_fails_closed_for_each_load_bearing_relationship(self) -> None:
        def dispatch(state: dict[str, object]) -> dict[str, object]:
            return state["child_dispatches"][0]  # type: ignore[index]

        def missing_dispatch(state, record, directory): record.pop("dispatch_id")
        def unknown_dispatch(state, record, directory): record["dispatch_id"] = "missing"
        def missing_child_dispatch_id(state, record, directory): dispatch(state).pop("dispatch_id")
        def missing_child_agent_id(state, record, directory): dispatch(state).pop("agent_id")
        def invalid_child_purpose(state, record, directory): dispatch(state)["purpose"] = []
        def wrong_role(state, record, directory): dispatch(state)["role"] = "SCOUT"
        def wrong_agent(state, record, directory): dispatch(state)["agent_id"] = "another"
        def not_archived(state, record, directory): dispatch(state)["archive_confirmed"] = False
        def false_lineage(state, record, directory): dispatch(state)["lineage_verified"] = False
        def missing_lineage(state, record, directory): dispatch(state).pop("lineage_verified")
        def unrelated_false_lineage(state, record, directory):
            state["child_dispatches"].append({  # type: ignore[union-attr]
                "dispatch_id": "unrelated-scout",
                "role": "SCOUT",
                "purpose": "source_scout",
                "agent_id": "agent-scout",
                "lineage_verified": False,
                "lifecycle": "archived",
                "archive_confirmed": True,
            })
        def missing_locator(state, record, directory): record.pop("candidate_locator")
        def bad_attempt(state, record, directory): record["attempt"] = 2
        def malformed_diff_name(state, record, directory):
            bad = directory / "not-a-code-diff.patch"
            bad.write_bytes((directory / "CODE_DIFF-FINAL_REVIEW-0-1.patch").read_bytes())
            record["candidate_locator"]["diff_path"] = str(bad.relative_to(ROOT))  # type: ignore[index]
        def changed_diff(state, record, directory): (directory / "CODE_DIFF-FINAL_REVIEW-0-1.patch").write_bytes(b"changed\n")
        def mismatched_task(state, record, directory): record["task_id"] = "different-task"
        def no_final_validation(state, record, directory): state.pop("final_validation_passed")
        def open_findings(state, record, directory): state["open_accepted_findings"] = ["f"]
        def deferred(state, record, directory): state["deferred_findings"] = ["f"]
        def empty_children(state, record, directory): state["child_dispatches"] = []
        def dual_lifecycle(state, record, directory): dispatch(state)["status"] = "archived"
        def unknown_role(state, record, directory): dispatch(state)["role"] = "AUTHOR"
        def traversal(state, record, directory): record["candidate_locator"]["spec_path"] = "../outside"  # type: ignore[index]
        def missing_candidate_path(state, record, directory): record["candidate_locator"]["spec_path"] = "missing/SPEC.md"  # type: ignore[index]
        def absolute_candidate_path(state, record, directory): record["candidate_locator"]["spec_path"] = "/tmp/SPEC.md"  # type: ignore[index]
        def missing_review_path(state, record, directory): state["review_records"] = ["missing/review.json"]
        def absolute_review_path(state, record, directory): state["review_records"] = ["/tmp/review.json"]
        def traversal_review_path(state, record, directory): state["review_records"] = ["../review.json"]

        cases = (
            (missing_dispatch, 1),
            (unknown_dispatch, 1),
            (missing_child_dispatch_id, 1),
            (missing_child_agent_id, 1),
            (invalid_child_purpose, 1),
            (wrong_role, 1),
            (wrong_agent, 1),
            (not_archived, 1),
            (false_lineage, 1),
            (missing_lineage, 1),
            (unrelated_false_lineage, 0),
            (missing_locator, 1),
            (bad_attempt, 1),
            (malformed_diff_name, 1),
            (changed_diff, 1),
            (mismatched_task, 1),
            (no_final_validation, 1),
            (open_findings, 1),
            (deferred, 1),
            (empty_children, 1),
            (dual_lifecycle, 1),
            (unknown_role, 1),
            (traversal, 2),
            (missing_candidate_path, 2),
            (absolute_candidate_path, 2),
            (missing_review_path, 2),
            (absolute_review_path, 2),
            (traversal_review_path, 2),
        )
        for mutation, expected in cases:
            with self.subTest(mutation=mutation.__name__):
                result = self._check_code(mutation)
                self.assertEqual(result.exit_code, expected, result)

    def test_valid_record_plus_orphan_record_only_counts_the_valid_binding(self) -> None:
        def valid_plus_orphan(state, record, directory):
            orphan = dict(record)
            orphan["dispatch_id"] = "orphan-dispatch"
            orphan_path = directory / "orphan.json"
            self._write(orphan_path, orphan)
            state["review_records"].append(str(orphan_path.relative_to(ROOT)))

        self.assertEqual(self._check_code(valid_plus_orphan).outcome, "DONE_VERIFIED")

        def orphan_only(state, record, directory):
            orphan = dict(record)
            orphan["dispatch_id"] = "orphan-dispatch"
            orphan_path = directory / "orphan.json"
            self._write(orphan_path, orphan)
            state["review_records"] = [str(orphan_path.relative_to(ROOT))]

        self.assertEqual(self._check_code(orphan_only).outcome, "NEW_CONTRACT_FAILED")

    def test_explicit_role_and_lifecycle_alias_matrix_is_reader_compatible(self) -> None:
        roles = ("EXECUTOR", "executor", "REVIEWER", "reviewer", "SCOUT", "scout", "senior-reviewer", "SENIOR_REVIEWER")
        for index, role in enumerate(roles):
            def add_unrelated(state, record, directory, role=role, index=index):
                state["child_dispatches"].append({  # type: ignore[union-attr]
                    "dispatch_id": f"alias-{index}",
                    "role": role,
                    "purpose": "source_scout",
                    "agent_id": f"agent-alias-{index}",
                    "lineage_verified": False,
                    "lifecycle": "archived",
                    "archive_confirmed": True,
                })
            with self.subTest(role=role):
                self.assertEqual(self._check_code(add_unrelated).outcome, "DONE_VERIFIED")

        def canonical_lifecycle(state, record, directory):
            state["child_dispatches"][0]["lifecycle"] = "archived"  # type: ignore[index]

        def legacy_lifecycle(state, record, directory):
            item = state["child_dispatches"][0]  # type: ignore[index]
            item["status"] = item.pop("lifecycle")

        self.assertEqual(self._check_code(canonical_lifecycle).outcome, "DONE_VERIFIED")
        self.assertEqual(self._check_code(legacy_lifecycle).outcome, "DONE_VERIFIED")

    def test_two_independent_attempts_recompute_distinct_candidates(self) -> None:
        state_path, state, record = self._copy_fixture("code")
        directory = state_path.parent
        second_diff = directory / "CODE_DIFF-FINAL_REVIEW-0-2.patch"
        second_diff.write_bytes(b"second candidate\n")
        second = dict(record)
        second["review_contract"] = "code_legacy_v1"
        second["dispatch_id"] = "review-2"
        second["agent_id"] = "agent-review-2"
        second["attempt"] = 2
        second["candidate_locator"] = {
            "spec_path": str((directory / "SPEC.md").relative_to(ROOT)),
            "diff_path": str(second_diff.relative_to(ROOT)),
        }
        second["candidate_ref"] = ai_state_check.candidate_ref(
            (directory / "SPEC.md").read_bytes(), second_diff.read_bytes()
        )
        second_path = directory / "review-2.json"
        self._write(second_path, second)
        state["review_records"].append(str(second_path.relative_to(ROOT)))
        state["child_dispatches"].append({  # type: ignore[union-attr]
            "dispatch_id": "review-2",
            "role": "REVIEWER",
            "purpose": "normal_review",
            "agent_id": "agent-review-2",
            "lineage_verified": True,
            "lifecycle": "archived",
            "archive_confirmed": True,
        })
        self._write(state_path, state)
        self.assertEqual(ai_state_check.check_state(state_path).outcome, "DONE_VERIFIED")

    def test_reader_aliases_and_legacy_record_mapping_remain_compatible(self) -> None:
        def aliases(state, record, directory):
            item = state["child_dispatches"][0]  # type: ignore[index]
            item["role"] = "reviewer"
            item["status"] = item.pop("lifecycle")
            state["review_records"] = {"normal-review": state["review_records"][0]}
        self.assertEqual(self._check_code(aliases).outcome, "DONE_VERIFIED")

    def test_contextual_binding_checks_record_dispatch_envelope_and_payload(self) -> None:
        state_path, state, record = self._copy_fixture("contextual")
        record["candidate_identity"] = "0" * 64
        self._write(state_path.parent / "review.json", record)
        self._write(state_path, state)
        self.assertEqual(ai_state_check.check_state(state_path).exit_code, 1)

        state_path, state, record = self._copy_fixture("contextual")
        envelope_path = state_path.parent / "CONTEXTUAL-ENVELOPE-review-1.json"
        envelope = self._read(envelope_path)
        envelope["payload"]["extra"] = "not canonical"  # type: ignore[index]
        self._write(envelope_path, envelope)
        self._write(state_path.parent / "review.json", record)
        self._write(state_path, state)
        result = ai_state_check.check_state(state_path)
        self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

    def test_completion_binding_checks_reviewer_purpose_and_identity_types(self) -> None:
        def wrong_reviewer_role(state, record, directory): record["reviewer_role"] = "senior-reviewer"
        def wrong_dispatch_purpose(state, record, directory): dispatch = state["child_dispatches"][0]; dispatch["purpose"] = "cross_review"  # type: ignore[index]
        def matching_non_string_agents(state, record, directory):
            record["agent_id"] = []
            state["child_dispatches"][0]["agent_id"] = []  # type: ignore[index]

        for mutation in (wrong_reviewer_role, wrong_dispatch_purpose, matching_non_string_agents):
            with self.subTest(mutation=mutation.__name__):
                result = self._check_code(mutation)
                self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

        def omitted_optional_purpose(state, record, directory):
            state["child_dispatches"].append({  # type: ignore[union-attr]
                "dispatch_id": "unrelated-no-purpose",
                "role": "SCOUT",
                "agent_id": "agent-no-purpose",
                "lineage_verified": False,
                "lifecycle": "archived",
                "archive_confirmed": True,
            })
        self.assertEqual(self._check_code(omitted_optional_purpose).outcome, "DONE_VERIFIED")

    def test_contextual_metadata_types_are_checked_before_candidate_branch(self) -> None:
        cases = (
            ("review_phase", True),
            ("cycle", False),
            ("attempt", 1.0),
        )
        for field, value in cases:
            def mutate(state, record, directory, field=field, value=value): record[field] = value
            with self.subTest(field=field, value=value):
                result = self._check_contextual(mutate)
                self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

    def test_persisted_state_marker_is_required_and_canonical(self) -> None:
        cases = (
            ("missing", lambda state, record, directory: state.pop("state")),
            ("non_string", lambda state, record, directory: state.update({"state": []})),
            ("unknown", lambda state, record, directory: state.update({"state": "NOT_A_STATE"})),
            ("obsolete_implementation_validate", lambda state, record, directory: state.update({"state": "IMPLEMENTATION_VALIDATE"})),
            ("obsolete_test", lambda state, record, directory: state.update({"state": "TEST"})),
        )
        for name, mutation in cases:
            with self.subTest(state=name):
                result = self._check_code(mutation, target="DONE")
                self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

        for marker in ("PLAN", "VALIDATE", "FINAL_VALIDATE"):
            with self.subTest(state=marker):
                result = self._check_code(lambda state, record, directory, marker=marker: state.update({"state": marker}), target="DONE")
                self.assertEqual((result.outcome, result.exit_code), ("DONE_VERIFIED", 0))

    def test_completion_markers_use_the_terminal_vocabulary(self) -> None:
        for field, value in (("status", "pending"), ("result", "pending"), ("status", []), ("result", {})):
            def mutate(state, record, directory, field=field, value=value):
                record[field] = value
            with self.subTest(field=field, value=value):
                result = self._check_code(mutate)
                self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

        def both_allowed(state, record, directory):
            record["status"] = "completed"
            record["result"] = "CHANGES_REQUIRED"

        self.assertEqual(self._check_code(both_allowed).outcome, "DONE_VERIFIED")

        def result_only_allowed(state, record, directory):
            record.pop("status", None)
            record["result"] = "CHANGES_REQUIRED"

        self.assertEqual(self._check_code(result_only_allowed).outcome, "DONE_VERIFIED")

    def test_filename_binding_requires_exact_json_types(self) -> None:
        cases = (
            ("cycle", False),
            ("attempt", 1.0),
        )
        for field, value in cases:
            def mutate(state, record, directory, field=field, value=value):
                record[field] = value

            with self.subTest(field=field, value=value):
                result = self._check_code(mutate)
                self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

    def test_candidate_byte_read_errors_are_input_errors(self) -> None:
        original_read_bytes = Path.read_bytes
        for field, filename in (
            ("spec", "SPEC.md"),
            ("diff", "CODE_DIFF-FINAL_REVIEW-0-1.patch"),
        ):
            def fail_candidate_read(path, filename=filename):
                if path.name == filename:
                    raise OSError("mock candidate read failure")
                return original_read_bytes(path)

            with self.subTest(field=field), patch.object(Path, "read_bytes", new=fail_candidate_read):
                result = self._check_code()
                self.assertEqual((result.outcome, result.exit_code), ("INPUT_ERROR", 2))

    def test_review_contracts_bind_to_purpose_before_candidate_validation(self) -> None:
        cases = (
            ("code_legacy_v1", "translation_contextual_v1"),
            ("translation_contextual_v1", "normal_review"),
            ("code_legacy_v1", "scope_audit"),
            ("unknown_contract", "normal_review"),
        )
        for contract, purpose in cases:
            def mutate(state, record, directory, contract=contract, purpose=purpose):
                state["review_contracts"] = [contract]
                state["completed_review_contracts"] = [contract]
                record["review_contract"] = contract
                record["purpose"] = purpose
            with self.subTest(contract=contract, purpose=purpose):
                result = self._check_code(mutate)
                self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

    def test_malformed_json_values_return_structured_results(self) -> None:
        cases = (
            lambda state, record, directory: record.update({"candidate_ref": {}}),
            lambda state, record, directory: record.update({"review_phase": []}),
            lambda state, record, directory: state.update({"mode": {}}),
            lambda state, record, directory: state["child_dispatches"][0].update({"role": []}),
        )
        for mutate in cases:
            with self.subTest(mutation=mutate):
                result = self._check_code(mutate)
                self.assertIsInstance(result, ai_state_check.CheckResult)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
                self.assertEqual(result.exit_code, 1)

        state_path, state, record = self._copy_fixture("contextual")
        envelope_path = state_path.parent / "CONTEXTUAL-ENVELOPE-review-1.json"
        envelope = self._read(envelope_path)
        envelope["payload"]["rendered_briefing"] = []  # type: ignore[index]
        self._write(envelope_path, envelope)
        self._write(state_path.parent / "review.json", record)
        self._write(state_path, state)
        result = ai_state_check.check_state(state_path)
        self.assertIsInstance(result, ai_state_check.CheckResult)
        self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

    @staticmethod
    def _runtime_observation() -> dict[str, object]:
        return {
            "schema_version": 1,
            "source": "live_agent_metadata",
            "captured_at": "2026-08-27T17:30:00Z",
            "capture_status": "captured",
            "provider": {"presence": "present", "value": "raw-provider"},
            "model": {"presence": "present", "value": None},
            "mode": {"presence": "present", "value": {"raw": [1, True]}},
            "thinking": {"presence": "missing"},
        }

    def test_runtime_observation_is_optional_and_completion_neutral(self) -> None:
        self.assertEqual(self._check_code().outcome, "DONE_VERIFIED")

        def add_observation(state, record, directory):
            state["child_dispatches"][0]["runtime_observation"] = self._runtime_observation()

        self.assertEqual(self._check_code(add_observation).outcome, "DONE_VERIFIED")

        def add_observation_to_stop(state, record, directory):
            state["state"] = "STOP"
            state["child_dispatches"][0]["runtime_observation"] = self._runtime_observation()

        self.assertEqual(
            self._check_code(add_observation_to_stop, target="STOP").outcome,
            "STOP_VERIFIED",
        )

        def raw_value_contains_ordinary_same_name(state, record, directory):
            observation = self._runtime_observation()
            observation["provider"] = {
                "presence": "present",
                "value": {"runtime_observation": {"ordinary": "raw metadata"}},
            }
            state["child_dispatches"][0]["runtime_observation"] = observation

        self.assertEqual(
            self._check_code(raw_value_contains_ordinary_same_name).outcome,
            "DONE_VERIFIED",
        )

    def test_runtime_observation_exact_schema_and_placement(self) -> None:
        invalid: list[object] = [None, [], {"schema_version": 1}]
        for field, value in (
            ("schema_version", True),
            ("schema_version", 2),
            ("source", "profile"),
            ("captured_at", ""),
            ("captured_at", None),
            ("capture_status", "partial"),
        ):
            observation = self._runtime_observation()
            observation[field] = value
            invalid.append(observation)
        extra = self._runtime_observation()
        extra["extra"] = True
        invalid.append(extra)
        for field_value in (
            {"presence": "missing", "value": None},
            {"presence": "present"},
            {"presence": "present", "value": "x", "extra": True},
            {"presence": "unknown"},
            [],
        ):
            observation = self._runtime_observation()
            observation["provider"] = field_value
            invalid.append(observation)
        non_json = self._runtime_observation()
        non_json["provider"] = {"presence": "present", "value": float("nan")}
        invalid.append(non_json)

        for value in invalid:
            def mutate(state, record, directory, value=value):
                state["child_dispatches"][0]["runtime_observation"] = value

            with self.subTest(value=value):
                result = self._check_code(mutate)
                self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

        placements = (
            lambda state, record, directory: state.update(
                {"runtime_observation": self._runtime_observation()}
            ),
            lambda state, record, directory: state.update(
                {"executor": {"runtime_observation": self._runtime_observation()}}
            ),
            lambda state, record, directory: state.update(
                {"baseline": {"runtime_observation": self._runtime_observation()}}
            ),
            lambda state, record, directory: state.update(
                {"wait": {"runtime_observation": self._runtime_observation()}}
            ),
            lambda state, record, directory: state["child_dispatches"][0].update(
                {"nested": {"runtime_observation": self._runtime_observation()}}
            ),
        )
        for mutate in placements:
            with self.subTest(placement=mutate):
                self.assertEqual(self._check_code(mutate).exit_code, 1)

        def nested_review_record(state, record, directory):
            record["evidence"] = [{"runtime_observation": self._runtime_observation()}]

        self.assertEqual(self._check_code(nested_review_record).exit_code, 1)

        def nested_review_record_stop(state, record, directory):
            state["state"] = "STOP"
            record["evidence"] = [{"runtime_observation": self._runtime_observation()}]

        self.assertEqual(
            self._check_code(nested_review_record_stop, target="STOP").exit_code,
            1,
        )

    def test_stop_ignores_unavailable_or_non_object_review_records(self) -> None:
        def unavailable_records(state, record, directory):
            state["state"] = "STOP"
            invalid_json = directory / "invalid-review.json"
            invalid_json.write_text("{", encoding="utf-8")
            non_object = directory / "non-object-review.json"
            self._write(non_object, [{"ordinary": "value"}])
            relative = directory.relative_to(ROOT)
            state["review_records"] = [
                str(relative / "missing-review.json"),
                str(invalid_json.relative_to(ROOT)),
                str(non_object.relative_to(ROOT)),
            ]

        self.assertEqual(
            self._check_code(unavailable_records, target="STOP").outcome,
            "STOP_VERIFIED",
        )

    def test_review_only_does_not_require_final_validation_and_stop_is_narrow(self) -> None:
        state_path, state, record = self._copy_fixture("contextual")
        self.assertNotIn("final_validation_passed", state)
        self._write(state_path.parent / "review.json", record)
        self._write(state_path, state)
        self.assertEqual(ai_state_check.check_state(state_path).outcome, "DONE_VERIFIED")

        result = self._check_code(lambda state, record, directory: state.update({"state": "STOP"}), target="STOP")
        self.assertEqual(result.outcome, "STOP_VERIFIED")
        result = self._check_code(lambda state, record, directory: (state.update({"state": "STOP"}), state.update({"child_dispatches": []})), target="STOP")
        self.assertEqual(result.outcome, "STOP_VERIFIED")

        def lifecycle_archived_stop(state, record, directory):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            state["state"] = "STOP"
            dispatch["lifecycle"] = "archived"
            dispatch["archive_confirmed"] = True

        def status_archived_stop(state, record, directory):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            state["state"] = "STOP"
            dispatch["status"] = dispatch.pop("lifecycle")
            dispatch["archive_confirmed"] = True

        def active_confirmed_stop(state, record, directory):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            state["state"] = "STOP"
            dispatch["lifecycle"] = "active"
            dispatch["archive_confirmed"] = True

        def stopping_confirmed_stop(state, record, directory):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            state["state"] = "STOP"
            dispatch["lifecycle"] = "stopping"
            dispatch["archive_confirmed"] = True

        def dual_fields_stop(state, record, directory):
            state["state"] = "STOP"
            state["child_dispatches"][0]["status"] = "archived"  # type: ignore[index]

        self.assertEqual(self._check_code(lifecycle_archived_stop, target="STOP").outcome, "STOP_VERIFIED")
        self.assertEqual(self._check_code(status_archived_stop, target="STOP").outcome, "STOP_VERIFIED")
        self.assertEqual(self._check_code(active_confirmed_stop, target="STOP").exit_code, 1)
        self.assertEqual(self._check_code(stopping_confirmed_stop, target="STOP").exit_code, 1)
        self.assertEqual(self._check_code(dual_fields_stop, target="STOP").exit_code, 1)

    def test_preflight_needs_target_and_cli_emits_structured_outcomes(self) -> None:
        result = self._check_code(lambda state, record, directory: state.update({"state": "FINAL_VALIDATE"}))
        self.assertEqual((result.outcome, result.exit_code), ("INPUT_ERROR", 2))
        result = self._check_code(lambda state, record, directory: state.update({"state": "FINAL_VALIDATE"}), target="DONE")
        self.assertEqual(result.outcome, "DONE_VERIFIED")
        run = subprocess.run([sys.executable, "-B", str(TOOLS / "ai_state_check.py"), str(FIXTURES / "code" / "STATE.json")], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("DONE_VERIFIED:", run.stdout)

    def test_cli_reports_every_stable_outcome_and_exit_code(self) -> None:
        done = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "ai_state_check.py"),
             str(FIXTURES / "code" / "STATE.json")],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual((done.returncode, done.stdout.split(":", 1)[0]), (0, "DONE_VERIFIED"))

        stop_path, stop_state, stop_record = self._copy_fixture("code")
        stop_state["state"] = "STOP"
        self._write(stop_path, stop_state)
        stop = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "ai_state_check.py"), str(stop_path), "--target", "STOP"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual((stop.returncode, stop.stdout.split(":", 1)[0]), (0, "STOP_VERIFIED"))

        failed_path, failed_state, failed_record = self._copy_fixture("code")
        failed_state["open_accepted_findings"] = ["VAL-001"]
        self._write(failed_path, failed_state)
        failed = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "ai_state_check.py"), str(failed_path)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual((failed.returncode, failed.stdout.split(":", 1)[0]), (1, "NEW_CONTRACT_FAILED"))

        invalid_manifest = self.work / "invalid-manifest.json"
        invalid_manifest.write_text(json.dumps({"schema_version": 1, "unsupported_tasks": ["z", "a"]}), encoding="utf-8")
        manifest_result = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "ai_state_check.py"), str(FIXTURES / "code" / "STATE.json"), "--manifest", str(invalid_manifest)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual((manifest_result.returncode, manifest_result.stdout.split(":", 1)[0]), (1, "MANIFEST_INVALID"))

        preflight_path, preflight_state, preflight_record = self._copy_fixture("code")
        preflight_state["state"] = "FINAL_VALIDATE"
        self._write(preflight_path, preflight_state)
        preflight = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "ai_state_check.py"), str(preflight_path)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual((preflight.returncode, preflight.stdout.split(":", 1)[0]), (2, "INPUT_ERROR"))

        legacy_state = self.work / "legacy-STATE.json"
        legacy_state.write_text(json.dumps({"task_id": "legacy-task", "state": "DONE"}), encoding="utf-8")
        legacy_manifest = self.work / "legacy-manifest.json"
        legacy_manifest.write_text(json.dumps({"schema_version": 1, "unsupported_tasks": ["legacy-task"]}), encoding="utf-8")
        legacy = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "ai_state_check.py"), str(legacy_state), "--manifest", str(legacy_manifest)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual((legacy.returncode, legacy.stdout.split(":", 1)[0]), (3, "UNSUPPORTED_LEGACY"))

        for arguments in ((), (str(FIXTURES / "code" / "STATE.json"), "--target", "BAD"), ("--unknown",)):
            with self.subTest(arguments=arguments):
                usage = subprocess.run(
                    [sys.executable, "-B", str(TOOLS / "ai_state_check.py"), *arguments],
                    cwd=ROOT, text=True, capture_output=True, check=False,
                )
                self.assertEqual(usage.returncode, 2)
                self.assertTrue(usage.stdout.startswith("INPUT_ERROR:"), usage)

    def test_managed_wave_context_is_opt_in_and_workspace_bound(self) -> None:
        state_path, state, record = self._copy_fixture("code")
        self.assertEqual(ai_state_check.check_state(state_path).outcome, "DONE_VERIFIED")
        state.update({"workspace_id": "lane-workspace", "orchestrator_agent_id": "wave-orchestrator"})
        state["child_dispatches"][0].update({  # type: ignore[index]
            "workspace_id": "lane-workspace",
            "task_id": state["task_id"],
            "parent_agent_id": "wave-orchestrator",
            "lineage_verified": True,
            "runtime_observation": self._runtime_observation(),
        })
        self._write(state_path, state)
        result = ai_state_check.check_wave_state_context(
            state_path,
            task_id=state["task_id"],  # type: ignore[arg-type]
            workspace_id="lane-workspace",
            orchestrator_agent_id="wave-orchestrator",
            workspace_root=ROOT,
        )
        self.assertEqual((result.outcome, result.exit_code), ("DONE_VERIFIED", 0))

        for field, value in (
            ("workspace_id", "other-workspace"),
            ("task_id", "other-task"),
            ("parent_agent_id", "other-parent"),
            ("purpose", ""),
            ("lineage_verified", False),
            ("role", "orchestrator"),
            ("agent_id", "wave-orchestrator"),
        ):
            with self.subTest(field=field):
                mutated = json.loads(json.dumps(state))
                mutated["child_dispatches"][0][field] = value
                self._write(state_path, mutated)
                result = ai_state_check.check_wave_state_context(
                    state_path,
                    task_id=state["task_id"],  # type: ignore[arg-type]
                    workspace_id="lane-workspace",
                    orchestrator_agent_id="wave-orchestrator",
                    workspace_root=ROOT,
                )
                self.assertEqual(result.exit_code, 1)


class AdoptionBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-state-manifest-", dir=ROOT / ".artifacts" / "i18n")
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)

    def _manifest(self, payload: object) -> Path:
        path = self.work / "manifest.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_tracked_manifest_is_strict_future_only_boundary(self) -> None:
        manifest = json.loads((ROOT / ".ai" / "legacy-cohort-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest), {"schema_version", "unsupported_tasks"})
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["unsupported_tasks"], sorted(manifest["unsupported_tasks"]))
        self.assertEqual(len(manifest["unsupported_tasks"]), len(set(manifest["unsupported_tasks"])))
        self.assertNotIn("paseo-ai-state-checker-001", manifest["unsupported_tasks"])

    def test_listed_tasks_are_informational_only_and_unlisted_deficient_tasks_fail_contract(self) -> None:
        state = self.work / "STATE.json"
        state.write_text(json.dumps({"task_id": "old-task", "state": "DONE"}), encoding="utf-8")
        manifest = self._manifest({"schema_version": 1, "unsupported_tasks": ["old-task"]})
        result = ai_state_check.check_state(state, manifest_path=manifest)
        self.assertEqual((result.outcome, result.exit_code), ("UNSUPPORTED_LEGACY", 3))

        state.write_text(json.dumps({"task_id": "new-task", "state": "DONE"}), encoding="utf-8")
        result = ai_state_check.check_state(state, manifest_path=manifest)
        self.assertEqual((result.outcome, result.exit_code), ("NEW_CONTRACT_FAILED", 1))

    def test_manifest_schema_failures_are_contract_failures(self) -> None:
        state = FIXTURES / "code" / "STATE.json"
        for payload in (
            {"schema_version": 1, "unsupported_tasks": [], "extra": True},
            {"schema_version": 1, "unsupported_tasks": ["z", "a"]},
            {"schema_version": 1, "unsupported_tasks": ["a", "a"]},
            {"schema_version": 2, "unsupported_tasks": []},
            {"schema_version": True, "unsupported_tasks": []},
            {"schema_version": 1.0, "unsupported_tasks": []},
            {"schema_version": 1, "unsupported_tasks": "old-task"},
            {"schema_version": 1, "unsupported_tasks": [""]},
            {"schema_version": 1, "unsupported_tasks": [1]},
        ):
            with self.subTest(payload=payload):
                self.assertEqual(ai_state_check.check_state(state, manifest_path=self._manifest(payload)).exit_code, 1)


SURFACE_TASK = "fixture-surface-screen"
SURFACE_SCALARS = {
    "fixed_source_identity": "commit:" + "3" * 40,
    "terminology_snapshot": "surface terms",
    "rules_version": "surface-rules/1",
}


def _surface_entry(index: int) -> dict[str, str]:
    logical = surface_screen_result_check.logical_entry_identity(
        component="tome", normalized_path="lua/mod.lua",
        call_locator=f"section/call-{index:04d}", source_tag=f"tag-{index}",
    )
    return {
        "component": "tome", "normalized_path": "lua/mod.lua",
        "call_locator": f"section/call-{index:04d}", "source_tag": f"tag-{index}",
        "source": f"Source {index}", "target": f"Target {index}",
        "logical_entry_identity": logical,
        "entry_revision_identity": surface_screen_result_check.entry_revision_identity(
            logical_entry_identity=logical, source=f"Source {index}",
            target=f"Target {index}", **SURFACE_SCALARS,
        ),
    }


def _surface_payload(count: int) -> dict[str, object]:
    entries = sorted(
        (_surface_entry(i) for i in range(1, count + 1)),
        key=lambda entry: entry["entry_revision_identity"],
    )
    return {
        "contract": "translation_surface_screen_v1", **SURFACE_SCALARS,
        "rendered_briefing": "lane neutral", "entries": entries,
    }


def _surface_zero_draft() -> dict[str, object]:
    """The actual frozen n=0 input draft a zero terminal must bind."""
    return {
        "contract": "translation_surface_screen_v1", **SURFACE_SCALARS,
        "rendered_briefing": "lane neutral", "entries": [],
    }


SURFACE_DRAFT_PATH = f".ai/task/{SURFACE_TASK}/SURFACE-SCREEN-INPUT-DRAFT.json"


class SurfaceScreenContractTests(unittest.TestCase):
    """File-backed coverage for the translation_surface_screen_v1 integration."""

    def setUp(self) -> None:
        artifacts = ROOT / ".artifacts" / "i18n"
        artifacts.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="surface-check-", dir=artifacts)
        self.addCleanup(self.temporary.cleanup)
        self.counter = 0

    def _write(self, path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(surface_screen_result_check.canonical_bytes(value))

    def _workspace(self) -> tuple[Path, dict[str, object], Path]:
        self.counter += 1
        workspace = Path(self.temporary.name) / f"surface-{self.counter}"
        workspace.mkdir(parents=True)
        state: dict[str, object] = {
            "schema_version": 5,
            "task_id": SURFACE_TASK,
            "mode": "review_only",
            "change_class": "translation_workflow",
            "state": "DONE",
            "cycle": 0,
            "max_cycles": 3,
            "workspace_id": "surface-workspace",
            "orchestrator_agent_id": "agent-orchestrator",
            "review_contracts": ["translation_surface_screen_v1"],
            "pending_review_contracts": [],
            "completed_review_contracts": ["translation_surface_screen_v1"],
            "open_accepted_findings": [],
            "deferred_findings": [],
            "child_dispatches": [],
            "review_records": [],
            "senior_review_records": [],
        }
        return workspace, state, workspace / "STATE.json"

    def _bind_whole_screen(
        self, workspace: Path, state: dict[str, object],
        records: list[dict[str, object]],
    ) -> None:
        binding = state.get("surface_evidence_binding")
        if not isinstance(binding, dict):
            binding = {
                "algorithm": "surface-evidence-binding/1",
                "task_id": SURFACE_TASK,
                "terminal": "whole_screen",
                "artifact_sha256": {},
            }
            state["surface_evidence_binding"] = binding
        locators: list[str] = []
        for record in records:
            locators.extend((record["input_path"], record["raw_output_path"]))  # type: ignore[arg-type]
        for key in ("surface_screen_input_path", "surface_carry_over_path"):
            locator = state.get(key)
            if isinstance(locator, str):
                locators.append(locator)
        hashes = binding["artifact_sha256"]  # type: ignore[index]
        for locator in locators:
            hashes[locator] = hashlib.sha256(  # type: ignore[index]
                (workspace / str(locator)).read_bytes()
            ).hexdigest()

    def _bind_zero(self, workspace: Path, state: dict[str, object]) -> None:
        locators = [surface_screen_manifest.zero_artifact_path(SURFACE_TASK)]
        draft_locator = state.get("surface_screen_input_path")
        if isinstance(draft_locator, str):
            locators.append(draft_locator)
        state["surface_evidence_binding"] = {
            "algorithm": "surface-evidence-binding/1",
            "task_id": SURFACE_TASK,
            "terminal": "zero",
            "artifact_sha256": {
                locator: hashlib.sha256((workspace / locator).read_bytes()).hexdigest()
                for locator in locators
            },
        }

    def _install_zero_terminal(self, workspace: Path, state: dict[str, object]) -> str:
        """Write the zero artifact plus its actual empty frozen input draft,
        bind both paths, and record the unified draft binding (C3-02)."""
        zero = surface_screen_manifest.build_zero_payload(task_id=SURFACE_TASK)
        zero_path = surface_screen_manifest.zero_artifact_path(SURFACE_TASK)
        self._write(workspace / zero_path, zero)
        state["surface_zero_path"] = zero_path
        self._write(workspace / SURFACE_DRAFT_PATH, _surface_zero_draft())
        state["surface_screen_input_path"] = SURFACE_DRAFT_PATH
        self._bind_zero(workspace, state)
        return zero_path

    def _add_surface_stage(
        self,
        workspace: Path,
        state: dict[str, object],
        *,
        phase: str,
        cycle: int,
        attempt: int,
        count: int,
        result: str = "PASS",
    ) -> list[dict[str, object]]:
        payload = _surface_payload(count)
        stage = f"{phase.lower().replace('_', '-')}-{cycle}-{attempt}"
        # C3-02: every whole-screen terminal binds one unified actual frozen
        # input draft; the stage coverage is later compared against it.
        if state.get("surface_screen_input_path") is None:
            self._write(workspace / SURFACE_DRAFT_PATH, payload)
            state["surface_screen_input_path"] = SURFACE_DRAFT_PATH
        records: list[dict[str, object]] = []
        if count <= 3:
            envelope, path, _ = surface_screen_manifest.build_full(
                payload, task_id=SURFACE_TASK, dispatch_id=stage,
            )
            members = [(stage, envelope, path, None)]
        else:
            group, group_path, envelopes = surface_screen_manifest.build_group(
                payload, task_id=SURFACE_TASK, group_id=f"group-{cycle}-{attempt}",
                review_phase=phase, cycle=cycle, attempt=attempt,
                dispatch_ids=[f"lane-{cycle}-{attempt}-{index}" for index in range(1, 5)],
            )
            self._write(workspace / group_path, group)
            boundaries = group["payload"]["lane_boundaries"]
            members = [
                (
                    lane["dispatch_id"], envelope, lane["input_path"],
                    {
                        "group_id": group["payload"]["group_id"],
                        "group_identity": group["group_identity"],
                        "group_manifest_path": group_path,
                        "index": boundary["index"], "count": 4,
                        "offset": boundary["offset"], "length": boundary["length"],
                    },
                )
                for lane, boundary, (_, envelope) in zip(
                    group["payload"]["lanes"], boundaries, envelopes
                )
            ]
        for dispatch_id, envelope, input_path, lane in members:
            self._write(workspace / input_path, envelope)
            lane_entries = envelope["payload"]["entries"]
            raw = {
                "contract": "translation_surface_screen_v1",
                "candidate_identity": envelope["candidate_identity"],
                "results": [
                    {"entry_revision_identity": entry["entry_revision_identity"], "verdict": "OK"}
                    for entry in lane_entries
                ],
            }
            raw_path = f".ai/reviews/{SURFACE_TASK}/raw-{dispatch_id}.txt"
            self._write(workspace / raw_path, raw)
            record: dict[str, object] = {
                "task_id": SURFACE_TASK,
                "review_contract": "translation_surface_screen_v1",
                "review_phase": phase,
                "cycle": cycle,
                "attempt": attempt,
                "reviewer_role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "dispatch_id": dispatch_id,
                "agent_id": f"agent-{dispatch_id}",
                "workspace_id": "surface-workspace",
                "parent_agent_id": "agent-orchestrator",
                "lineage_verified": True,
                "result": result,
                "review_kind": "lane" if lane else "full",
                "candidate_identity": envelope["candidate_identity"],
                "input_path": input_path,
                "raw_output_path": raw_path,
                "raw_output_sha256": hashlib.sha256(
                    surface_screen_result_check.canonical_bytes(raw)
                ).hexdigest(),
            }
            dispatch: dict[str, object] = {
                "dispatch_id": dispatch_id,
                "role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "agent_id": f"agent-{dispatch_id}",
                "parent_agent_id": "agent-orchestrator",
                "workspace_id": "surface-workspace",
                "lineage_verified": True,
                "lifecycle": "archived",
                "archive_confirmed": True,
                "candidate_identity": envelope["candidate_identity"],
                "input_path": input_path,
                "labels": {
                    "task_id": SURFACE_TASK,
                    "role": "reviewer",
                    "purpose": "translation_surface_screen_v1",
                    "candidate_identity": envelope["candidate_identity"],
                    "dispatch_id": dispatch_id,
                },
            }
            if lane is not None:
                record["lane"] = lane
                dispatch["lane_group_identity"] = lane["group_identity"]
                dispatch["lane_index"] = lane["index"]
                dispatch["labels"]["lane_group_identity"] = lane["group_identity"]
                dispatch["labels"]["lane_index"] = lane["index"]
            record_file = workspace / f"{dispatch_id}.json"
            self._write(record_file, record)
            state["review_records"].append(str(record_file.relative_to(workspace)))  # type: ignore[union-attr]
            state["child_dispatches"].append(dispatch)  # type: ignore[union-attr]
            records.append(record)
        self._bind_whole_screen(workspace, state, records)
        return records

    def _verify(self, workspace: Path, state: dict[str, object], mutate=None) -> ai_state_check.CheckResult:
        state_path = workspace / "STATE.json"
        if mutate:
            mutate(workspace, state)
        self._write(state_path, state)
        return ai_state_check.check_state(state_path, workspace_root=workspace)

    def test_review_only_single_full_is_done_verified(self) -> None:
        workspace, state, state_path = self._workspace()
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_review_only_complete_lane_group_is_done_verified(self) -> None:
        workspace, state, _ = self._workspace()
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=5)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_review_only_translation_workflow_surface_is_done_verified_without_code_terminal(self) -> None:
        # CF-13: surface is translation_workflow under the active definition;
        # evidence reconciliation adapts honestly via the surface-specific
        # binding instead of requiring or fabricating a code/contextual
        # completion terminal.
        workspace, state, _ = self._workspace()
        self.assertEqual(state["change_class"], "translation_workflow")
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_review_only_rejects_partial_lane_publication(self) -> None:
        workspace, state, _ = self._workspace()
        records = self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=5)
        dropped = records[3]
        state["review_records"].remove(f"{dropped['dispatch_id']}.json")  # type: ignore[attr-defined]
        state["child_dispatches"] = [
            dispatch for dispatch in state["child_dispatches"]  # type: ignore[union-attr]
            if dispatch["dispatch_id"] != dropped["dispatch_id"]
        ]
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("surface lane stage must contain exactly members 1..4", result.detail)

    def test_surface_rejects_borrowed_implement_convergence(self) -> None:
        # CF-03: surface is review_only; the contextual implement convergence
        # (RE_REVIEW/FINAL_REVIEW escalation) is not part of this contract.
        workspace, state, _ = self._workspace()
        state["mode"] = "implement"
        state["final_validation_passed"] = True
        state["cycle"] = 1
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("review_only", result.detail)

    def test_review_only_rejects_second_stage(self) -> None:
        workspace, state, _ = self._workspace()
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=2, count=2)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("exactly one whole-screen stage", result.detail)

    def test_zero_no_dispatch_artifact_is_done_verified(self) -> None:
        workspace, state, _ = self._workspace()
        self._install_zero_terminal(workspace, state)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_zero_artifact_negative_matrix(self) -> None:
        def zero_with_dispatch(workspace, state):
            self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)

        def drifted_zero(workspace, state):
            path = workspace / surface_screen_manifest.zero_artifact_path(SURFACE_TASK)
            value = json.loads(path.read_text(encoding="utf-8"))
            value["proves_no_surface_dispatch"] = False
            self._write(path, value)

        def wrong_path(workspace, state):
            state["surface_zero_path"] = f".ai/task/{SURFACE_TASK}/SURFACE-SCREEN-ZERO-copy.json"
            self._write(
                workspace / str(state["surface_zero_path"]),
                surface_screen_manifest.build_zero_payload(task_id=SURFACE_TASK),
            )

        def nonzero_zero(workspace, state):
            path = workspace / surface_screen_manifest.zero_artifact_path(SURFACE_TASK)
            value = json.loads(path.read_text(encoding="utf-8"))
            value["screen_count"] = 3
            self._write(path, value)

        def missing_artifact(workspace, state):
            state["surface_zero_path"] = surface_screen_manifest.zero_artifact_path(SURFACE_TASK)
            (workspace / state["surface_zero_path"]).unlink()

        def dispatch_without_terminal(workspace, state):
            # A declared zero terminal must not coexist with dispatches.
            state["child_dispatches"] = [{
                "dispatch_id": "ghost-1", "role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "agent_id": "agent-ghost-1", "parent_agent_id": "agent-orchestrator",
                "workspace_id": "surface-workspace", "lineage_verified": True,
                "lifecycle": "archived", "archive_confirmed": True,
            }]

        for mutate in (
            zero_with_dispatch, drifted_zero, wrong_path, nonzero_zero,
            missing_artifact, dispatch_without_terminal,
        ):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._install_zero_terminal(workspace, state)
                result = self._verify(workspace, state, mutate=mutate)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")

    def test_zero_artifact_binds_recomputable_empty_workset_identity(self) -> None:
        # C2-03: the zero artifact must bind the canonical recomputable
        # empty workset/input snapshot identity and algorithm version, and
        # DONE must rederive it.
        zero = surface_screen_manifest.build_zero_payload(task_id=SURFACE_TASK)
        surface_screen_manifest.validate_zero_payload(zero)
        self.assertEqual(zero["algorithm"], "surface-zero-workset/1")
        self.assertEqual(
            zero["workset_identity"],
            surface_screen_manifest.build_zero_workset_identity(),
        )

        def tampered_workset_identity(workspace, state):
            path = workspace / surface_screen_manifest.zero_artifact_path(SURFACE_TASK)
            value = json.loads(path.read_text(encoding="utf-8"))
            value["workset_identity"] = "0" * 64
            self._write(path, value)

        def wrong_algorithm(workspace, state):
            path = workspace / surface_screen_manifest.zero_artifact_path(SURFACE_TASK)
            value = json.loads(path.read_text(encoding="utf-8"))
            value["algorithm"] = "surface-zero-workset/2"
            self._write(path, value)

        def dropped_workset_identity(workspace, state):
            path = workspace / surface_screen_manifest.zero_artifact_path(SURFACE_TASK)
            value = json.loads(path.read_text(encoding="utf-8"))
            del value["workset_identity"]
            self._write(path, value)

        def bound_carry_over(workspace, state):
            state["surface_carry_over_path"] = surface_screen_manifest.carry_over_artifact_path(SURFACE_TASK)

        for mutate in (
            tampered_workset_identity, wrong_algorithm,
            dropped_workset_identity, bound_carry_over,
        ):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._install_zero_terminal(workspace, state)
                result = self._verify(workspace, state, mutate=mutate)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")

    def test_surface_n_zero_build_rejects_dispatch_inputs(self) -> None:
        # C2-03: the n=0 CLI must require no dispatch/group/cycle/attempt
        # inputs at all.
        draft = self.temporary.name + "/zero-draft.json"
        Path(draft).write_bytes(surface_screen_result_check.canonical_bytes({
            "contract": "translation_surface_screen_v1",
            "fixed_source_identity": "commit:" + "3" * 40,
            "terminology_snapshot": "surface terms",
            "rules_version": "surface-rules/1",
            "rendered_briefing": "lane neutral",
            "entries": [],
        }))
        for extra in (
            [], ["--dispatch-id", "full-0"], ["--group-id", "group-0"],
            ["--cycle", "0"], ["--attempt", "1"], ["--review-phase", "REVIEW", "--cycle", "0"],
        ):
            with self.subTest(extra=extra):
                completed = subprocess.run(
                    [sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                     "build", draft, "--task-id", SURFACE_TASK, *extra,
                     "--root", self.temporary.name],
                    capture_output=True, text=True,
                )
                if extra:
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertIn("MANIFEST_FAILED", completed.stdout + completed.stderr)
                else:
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    self.assertIn("ZERO_RECORDED", completed.stdout)

    def _carry_over_fixture(
        self, workspace: Path, state: dict[str, object],
    ) -> tuple[dict[str, object], dict[str, object]]:
        """Build an n>80 carry-over artifact, bind its original frozen workset
        draft via surface_screen_input_path, and add a lane stage covering
        exactly the first-80 screen set with the evidence binding."""
        payload = _surface_payload(85)
        carry = surface_screen_manifest.build_carry_over_payload(payload, task_id=SURFACE_TASK)
        carry_path = surface_screen_manifest.carry_over_artifact_path(SURFACE_TASK)
        self._write(workspace / carry_path, carry)
        draft_path = f".ai/task/{SURFACE_TASK}/SURFACE-SCREEN-DRAFT.json"
        self._write(workspace / draft_path, payload)
        state["surface_carry_over_path"] = carry_path
        state["surface_screen_input_path"] = draft_path
        screen_payload = dict(payload)
        screen_payload["entries"] = payload["entries"][:80]
        group, group_path, envelopes = surface_screen_manifest.build_group(
            screen_payload, task_id=SURFACE_TASK, group_id="group-carry",
            review_phase="REVIEW", cycle=0, attempt=1,
            dispatch_ids=[f"carry-lane-{index}" for index in range(1, 5)],
        )
        self._write(workspace / group_path, group)
        records: list[dict[str, object]] = []
        boundaries = group["payload"]["lane_boundaries"]
        for lane, boundary, (_, envelope) in zip(
            group["payload"]["lanes"], boundaries, envelopes
        ):
            input_path = lane["input_path"]
            self._write(workspace / input_path, envelope)
            lane_entries = envelope["payload"]["entries"]
            raw = {
                "contract": "translation_surface_screen_v1",
                "candidate_identity": envelope["candidate_identity"],
                "results": [
                    {"entry_revision_identity": entry["entry_revision_identity"], "verdict": "OK"}
                    for entry in lane_entries
                ],
            }
            raw_path = f".ai/reviews/{SURFACE_TASK}/raw-{lane['dispatch_id']}.txt"
            self._write(workspace / raw_path, raw)
            record: dict[str, object] = {
                "task_id": SURFACE_TASK,
                "review_contract": "translation_surface_screen_v1",
                "review_phase": "REVIEW", "cycle": 0, "attempt": 1,
                "reviewer_role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "dispatch_id": lane["dispatch_id"],
                "agent_id": f"agent-{lane['dispatch_id']}",
                "workspace_id": "surface-workspace",
                "parent_agent_id": "agent-orchestrator",
                "lineage_verified": True,
                "result": "PASS", "review_kind": "lane",
                "candidate_identity": envelope["candidate_identity"],
                "input_path": input_path,
                "raw_output_path": raw_path,
                "raw_output_sha256": hashlib.sha256(
                    surface_screen_result_check.canonical_bytes(raw)
                ).hexdigest(),
                "lane": {
                    "group_id": group["payload"]["group_id"],
                    "group_identity": group["group_identity"],
                    "group_manifest_path": group_path,
                    "index": boundary["index"], "count": 4,
                    "offset": boundary["offset"], "length": boundary["length"],
                },
            }
            dispatch: dict[str, object] = {
                "dispatch_id": lane["dispatch_id"], "role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "agent_id": f"agent-{lane['dispatch_id']}",
                "parent_agent_id": "agent-orchestrator",
                "workspace_id": "surface-workspace", "lineage_verified": True,
                "lifecycle": "archived", "archive_confirmed": True,
                "candidate_identity": envelope["candidate_identity"],
                "input_path": input_path,
                "lane_group_identity": group["group_identity"],
                "lane_index": boundary["index"],
                "labels": {
                    "task_id": SURFACE_TASK, "role": "reviewer",
                    "purpose": "translation_surface_screen_v1",
                    "candidate_identity": envelope["candidate_identity"],
                    "dispatch_id": lane["dispatch_id"],
                    "lane_group_identity": group["group_identity"],
                    "lane_index": boundary["index"],
                },
            }
            record_file = workspace / f"{lane['dispatch_id']}.json"
            self._write(record_file, record)
            state["review_records"].append(str(record_file.relative_to(workspace)))  # type: ignore[union-attr]
            state["child_dispatches"].append(dispatch)  # type: ignore[union-attr]
            records.append(record)
        self._bind_whole_screen(workspace, state, records)
        return payload, carry

    def test_carry_over_binding_covers_first_eighty_only(self) -> None:
        workspace, state, _ = self._workspace()
        payload, carry = self._carry_over_fixture(workspace, state)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_carry_over_artifact_binds_complete_original_workset(self) -> None:
        # C2-02: malformed counts, overlap, omissions and extras — plus a
        # missing original-workset binding — must all fail closed.
        def omitted_carry_entry(workspace, state, carry):
            carry["ordered_carry_over_entry_revision_identities"] = \
                carry["ordered_carry_over_entry_revision_identities"][:-1]
            carry["carry_over_count"] = len(carry["ordered_carry_over_entry_revision_identities"])
            carry["original_count"] = 80 + carry["carry_over_count"]

        def extra_carry_entry(workspace, state, carry):
            carry["ordered_carry_over_entry_revision_identities"].append(
                carry["ordered_screen_entry_revision_identities"][0]
            )
            carry["carry_over_count"] = len(carry["ordered_carry_over_entry_revision_identities"])
            carry["original_count"] = 80 + carry["carry_over_count"]

        def overlapping_sets(workspace, state, carry):
            carry["ordered_carry_over_entry_revision_identities"][0] = \
                carry["ordered_screen_entry_revision_identities"][0]

        def wrong_counts(workspace, state, carry):
            carry["original_count"] = 84

        def wrong_task_id(workspace, state, carry):
            carry["task_id"] = "other-task"

        def missing_draft_binding(workspace, state, carry):
            del state["surface_screen_input_path"]  # type: ignore[arg-type]

        def draft_drift(workspace, state, carry):
            draft_path = workspace / str(state["surface_screen_input_path"])  # type: ignore[arg-type]
            draft = json.loads(draft_path.read_text(encoding="utf-8"))
            draft["entries"] = draft["entries"][:-1]
            draft_path.write_bytes(surface_screen_result_check.canonical_bytes(draft))

        def deleted_carry_binding(workspace, state, carry):
            # C3-02: deleting the carry binding must never reclassify the
            # n=85 workset as a whole n=80 screen.
            del state["surface_carry_over_path"]  # type: ignore[arg-type]
            binding = state["surface_evidence_binding"]  # type: ignore[index]
            del binding["artifact_sha256"][
                surface_screen_manifest.carry_over_artifact_path(SURFACE_TASK)
            ]

        for mutate in (
            omitted_carry_entry, extra_carry_entry, overlapping_sets,
            wrong_counts, wrong_task_id, missing_draft_binding, draft_drift,
            deleted_carry_binding,
        ):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                payload, carry = self._carry_over_fixture(workspace, state)
                mutate(workspace, state, carry)
                if mutate.__name__ not in {"missing_draft_binding", "deleted_carry_binding"}:
                    carry_path = surface_screen_manifest.carry_over_artifact_path(SURFACE_TASK)
                    self._write(workspace / carry_path, carry)
                result = self._verify(workspace, state)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")

    def test_carry_over_drift_is_rejected(self) -> None:
        workspace, state, _ = self._workspace()
        # Screen a set that is NOT the recorded first-80 slice.
        payload = _surface_payload(85)
        carry = surface_screen_manifest.build_carry_over_payload(payload, task_id=SURFACE_TASK)
        carry_path = surface_screen_manifest.carry_over_artifact_path(SURFACE_TASK)
        self._write(workspace / carry_path, carry)
        draft_path = f".ai/task/{SURFACE_TASK}/SURFACE-SCREEN-DRAFT.json"
        self._write(workspace / draft_path, payload)
        state["surface_carry_over_path"] = carry_path
        state["surface_screen_input_path"] = draft_path
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=5)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("does not cover exactly the recorded first-80 screen set", result.detail)

    def test_surface_manifest_binding_and_terminal_matrix(self) -> None:
        def stale_candidate(workspace, state):
            envelope_path = workspace / ".ai/task" / SURFACE_TASK / "SURFACE-SCREEN-ENVELOPE-review-0-1.json"
            envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
            envelope["payload"]["terminology_snapshot"] = "drifted"
            envelope_path.write_bytes(surface_screen_result_check.canonical_bytes(envelope))

        def raw_truncation(workspace, state):
            raw_path = workspace / ".ai/reviews" / SURFACE_TASK / "raw-review-0-1.txt"
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            raw["results"] = raw["results"][:1]
            raw_path.write_bytes(surface_screen_result_check.canonical_bytes(raw))

        def raw_hash_drift(workspace, state):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            record_path = workspace / f"{dispatch['dispatch_id']}.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["raw_output_sha256"] = "0" * 64
            record_path.write_bytes(surface_screen_result_check.canonical_bytes(record))

        def label_drift(workspace, state):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            dispatch["labels"]["candidate_identity"] = "0" * 64

        def parent_drift(workspace, state):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            dispatch["parent_agent_id"] = "agent-other"

        def record_parent_drift(workspace, state):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            record_path = workspace / f"{dispatch['dispatch_id']}.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["parent_agent_id"] = "agent-other"
            record_path.write_bytes(surface_screen_result_check.canonical_bytes(record))

        def record_workspace_drift(workspace, state):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            record_path = workspace / f"{dispatch['dispatch_id']}.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["workspace_id"] = "other-workspace"
            record_path.write_bytes(surface_screen_result_check.canonical_bytes(record))

        def record_lineage_missing(workspace, state):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            record_path = workspace / f"{dispatch['dispatch_id']}.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            del record["lineage_verified"]
            record_path.write_bytes(surface_screen_result_check.canonical_bytes(record))

        def unsafe_dispatch_id(workspace, state):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            record_path = workspace / f"{dispatch['dispatch_id']}.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["dispatch_id"] = "../ESCAPED"
            record_path.write_bytes(surface_screen_result_check.canonical_bytes(record))

        def failed_completion(workspace, state):
            dispatch = state["child_dispatches"][0]  # type: ignore[index]
            record_path = workspace / f"{dispatch['dispatch_id']}.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["result"] = "CHANGES_REQUIRED"
            record_path.write_bytes(surface_screen_result_check.canonical_bytes(record))

        for mutate in (
            stale_candidate, raw_truncation, raw_hash_drift, label_drift,
            parent_drift, record_parent_drift, record_workspace_drift,
            record_lineage_missing, unsafe_dispatch_id, failed_completion,
        ):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
                result = self._verify(workspace, state, mutate=mutate)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")

    def test_change_class_matrix_for_review_only_surface(self) -> None:
        # C2-05: surface review_only tasks must use
        # change_class=translation_workflow; standard and infrastructure fail.
        for change_class, expected in (
            ("translation_workflow", "DONE_VERIFIED"),
            ("standard", "NEW_CONTRACT_FAILED"),
            ("infrastructure", "NEW_CONTRACT_FAILED"),
            (None, "NEW_CONTRACT_FAILED"),
        ):
            with self.subTest(change_class=change_class):
                workspace, state, _ = self._workspace()
                state["change_class"] = change_class
                self._add_surface_stage(
                    workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2,
                )
                result = self._verify(workspace, state)
                self.assertEqual(result.outcome, expected)

    def test_surface_stop_rejects_dispatched_screen(self) -> None:
        workspace, state, state_path = self._workspace()
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
        state["state"] = "STOP"
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("STOP cannot close a dispatched surface screen", result.detail)
        # STOP remains available for a surface task that never dispatched.
        fresh_workspace, fresh_state, fresh_path = self._workspace()
        fresh_state["state"] = "STOP"
        result = self._verify(fresh_workspace, fresh_state)
        self.assertEqual(result.outcome, "STOP_VERIFIED")

    def test_surface_stop_uses_the_all_source_activity_predicate(self) -> None:
        # C4-03: STOP must apply the same persisted all-source surface
        # activity predicate as DONE: relabeling or deleting child_dispatches
        # cannot close persisted surface records, terminal bindings, or
        # artifacts.
        def relabel_children(workspace: Path, state: dict[str, object]) -> None:
            for dispatch in state["child_dispatches"]:  # type: ignore[type-var, union-attr]
                dispatch["purpose"] = "translation_contextual_v1"  # type: ignore[index]
                dispatch["labels"]["purpose"] = "translation_contextual_v1"  # type: ignore[index]

        def delete_children(workspace: Path, state: dict[str, object]) -> None:
            state["child_dispatches"] = []

        for mutate in (relabel_children, delete_children):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._add_surface_stage(
                    workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2,
                )
                state["state"] = "STOP"
                result = self._verify(workspace, state, mutate=mutate)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
                self.assertIn("STOP cannot close a dispatched surface screen", result.detail)
        # A bound zero terminal is also persisted surface activity: STOP
        # cannot close it; DONE remains its terminal.
        workspace, state, _ = self._workspace()
        self._install_zero_terminal(workspace, state)
        state["state"] = "STOP"
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("STOP cannot close a dispatched surface screen", result.detail)

    def test_surface_cannot_mix_with_contextual_contracts_or_low_schema(self) -> None:
        def mixed_contracts(workspace, state):
            state["review_contracts"] = ["translation_surface_screen_v1", "translation_contextual_v2"]

        def low_schema(workspace, state):
            state["schema_version"] = 4

        for mutate in (mixed_contracts, low_schema):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
                result = self._verify(workspace, state, mutate=mutate)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")

    def test_surface_requires_a_bound_completion_record(self) -> None:
        workspace, state, _ = self._workspace()
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("no bound completion record for contract 'translation_surface_screen_v1'", result.detail)

    def _add_forged_full_stage(
        self, workspace: Path, state: dict[str, object], *, count: int,
    ) -> None:
        """Hand-forge an internally valid full stage envelope bypassing the
        builder cardinality check (the malicious C2-01 probe)."""
        payload = _surface_payload(count)
        identity = hashlib.sha256(
            surface_screen_result_check.canonical_payload_bytes(payload)
        ).hexdigest()
        envelope = {"candidate_identity": identity, "payload": payload}
        stage = "review-0-1"
        input_path = surface_screen_manifest._envelope_path(SURFACE_TASK, stage)
        self._write(workspace / input_path, envelope)
        raw = {
            "contract": "translation_surface_screen_v1",
            "candidate_identity": identity,
            "results": [
                {"entry_revision_identity": entry["entry_revision_identity"], "verdict": "OK"}
                for entry in payload["entries"]
            ],
        }
        raw_path = f".ai/reviews/{SURFACE_TASK}/raw-{stage}.txt"
        self._write(workspace / raw_path, raw)
        record: dict[str, object] = {
            "task_id": SURFACE_TASK,
            "review_contract": "translation_surface_screen_v1",
            "review_phase": "REVIEW", "cycle": 0, "attempt": 1,
            "reviewer_role": "REVIEWER",
            "purpose": "translation_surface_screen_v1",
            "dispatch_id": stage, "agent_id": f"agent-{stage}",
            "workspace_id": "surface-workspace",
            "parent_agent_id": "agent-orchestrator",
            "lineage_verified": True, "result": "PASS",
            "review_kind": "full", "candidate_identity": identity,
            "input_path": input_path, "raw_output_path": raw_path,
            "raw_output_sha256": hashlib.sha256(
                surface_screen_result_check.canonical_bytes(raw)
            ).hexdigest(),
        }
        dispatch: dict[str, object] = {
            "dispatch_id": stage, "role": "REVIEWER",
            "purpose": "translation_surface_screen_v1",
            "agent_id": f"agent-{stage}",
            "parent_agent_id": "agent-orchestrator",
            "workspace_id": "surface-workspace", "lineage_verified": True,
            "lifecycle": "archived", "archive_confirmed": True,
            "candidate_identity": identity, "input_path": input_path,
            "labels": {
                "task_id": SURFACE_TASK, "role": "reviewer",
                "purpose": "translation_surface_screen_v1",
                "candidate_identity": identity, "dispatch_id": stage,
            },
        }
        self._write(workspace / f"{stage}.json", record)
        state["review_records"].append(f"{stage}.json")  # type: ignore[union-attr]
        state["child_dispatches"].append(dispatch)  # type: ignore[union-attr]
        self._write(workspace / SURFACE_DRAFT_PATH, payload)
        state["surface_screen_input_path"] = SURFACE_DRAFT_PATH
        self._bind_whole_screen(workspace, state, [record])

    def test_surface_full_stage_cardinality_is_enforced(self) -> None:
        # C2-01: a forged full stage outside n=1..3 (here 40 and 200 entries)
        # must fail closed even when its envelope bytes are internally valid.
        for count in (40, 200):
            with self.subTest(count=count):
                workspace, state, _ = self._workspace()
                self._add_forged_full_stage(workspace, state, count=count)
                result = self._verify(workspace, state)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
                self.assertIn(
                    "full surface stage must cover between 1 and 3 entries",
                    result.detail,
                )

    def test_surface_lane_manifest_rejects_whole_stage_over_screen_limit(self) -> None:
        # C2-01: any whole stage over SCREEN_LIMIT (80) fails closed at the
        # manifest validator, even with hand-made balanced-looking boundaries.
        payload = _surface_payload(200)
        workset = {
            "entries": payload["entries"],
            "fixed_source_identity": payload["fixed_source_identity"],
            "terminology_snapshot": payload["terminology_snapshot"],
            "rules_version": payload["rules_version"],
            "rendered_briefing": payload["rendered_briefing"],
        }
        boundaries = [
            {"index": index, "offset": (index - 1) * 50, "length": 50}
            for index in range(1, 5)
        ]
        group_payload = {
            "contract": surface_screen_result_check.LANE_GROUP_CONTRACT,
            "task_id": SURFACE_TASK, "group_id": "group-over",
            "review_phase": "REVIEW", "cycle": 0, "attempt": 1,
            "lane_count": 4, "workset": workset,
            "lane_boundaries": boundaries, "lanes": [],
        }
        manifest = {
            "group_identity": hashlib.sha256(
                surface_screen_result_check.canonical_bytes(group_payload)
            ).hexdigest(),
            "payload": group_payload,
        }
        with self.assertRaises(surface_screen_result_check.ContractError):
            surface_screen_manifest.validate_group_manifest(manifest)

    def test_surface_evidence_binding_is_required_and_recomputed(self) -> None:
        # C2-05: the immutable surface evidence reconciliation binding is
        # mandatory, terminal-bound, and rederived from current bytes.
        def no_binding(workspace, state):
            del state["surface_evidence_binding"]  # type: ignore[arg-type]

        def wrong_algorithm(workspace, state):
            state["surface_evidence_binding"]["algorithm"] = "surface-evidence-binding/2"  # type: ignore[index]

        def wrong_terminal(workspace, state):
            state["surface_evidence_binding"]["terminal"] = "zero"  # type: ignore[index]

        def wrong_task_id(workspace, state):
            state["surface_evidence_binding"]["task_id"] = "other-task"  # type: ignore[index]

        def extra_artifact(workspace, state):
            state["surface_evidence_binding"]["artifact_sha256"][".ai/reviews/extra.txt"] = "0" * 64  # type: ignore[index]

        def omitted_artifact(workspace, state):
            binding = state["surface_evidence_binding"]  # type: ignore[index]
            first_locator = next(iter(binding["artifact_sha256"]))
            del binding["artifact_sha256"][first_locator]

        for mutate in (
            no_binding, wrong_algorithm, wrong_terminal, wrong_task_id,
            extra_artifact, omitted_artifact,
        ):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
                result = self._verify(workspace, state, mutate=mutate)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")

    def test_surface_evidence_binding_drift_fails_closed(self) -> None:
        # C2-05: any drift of the bound terminal artifact bytes fails.
        def envelope_drift(workspace, state):
            path = workspace / ".ai/task" / SURFACE_TASK / "SURFACE-SCREEN-ENVELOPE-review-0-1.json"
            envelope = json.loads(path.read_text(encoding="utf-8"))
            envelope["payload"]["rendered_briefing"] = "drifted briefing"
            path.write_bytes(surface_screen_result_check.canonical_bytes(envelope))

        def raw_drift(workspace, state):
            path = workspace / ".ai/reviews" / SURFACE_TASK / "raw-review-0-1.txt"
            raw = json.loads(path.read_text(encoding="utf-8"))
            raw["results"][0]["verdict"] = "ISSUE"
            path.write_bytes(surface_screen_result_check.canonical_bytes(raw))

        for mutate in (envelope_drift, raw_drift):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
                result = self._verify(workspace, state, mutate=mutate)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")

    def test_surface_stop_rejects_dispatched_screen_despite_tampering(self) -> None:
        # C2-08: STOP must reject whenever any child dispatch carries the
        # surface purpose, regardless of review_contracts removal or a
        # schema_version downgrade.
        for mutate in (
            lambda state: state.update({
                "schema_version": 4,
                "review_contracts": ["translation_contextual_v2"],
                "completed_review_contracts": ["translation_contextual_v2"],
            }),
            lambda state: state.update({
                "review_contracts": ["code_legacy_v1"],
                "completed_review_contracts": ["code_legacy_v1"],
            }),
        ):
            with self.subTest():
                workspace, state, _ = self._workspace()
                self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
                mutate(state)  # type: ignore[arg-type]
                state["state"] = "STOP"
                result = self._verify(workspace, state)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
                self.assertIn("STOP cannot close a dispatched surface screen", result.detail)

    def test_surface_group_phase_only_allows_review(self) -> None:
        # C2-07: surface manifest/group artifacts allow only REVIEW; a fresh
        # retry increases attempt with fresh IDs and never emits RE_REVIEW.
        self.assertEqual(surface_screen_manifest.PHASES, frozenset({"REVIEW"}))
        workspace, state, _ = self._workspace()
        payload = _surface_payload(5)
        with self.assertRaises(surface_screen_result_check.ContractError):
            surface_screen_manifest.build_group(
                payload, task_id=SURFACE_TASK, group_id="group-re-review",
                review_phase="RE_REVIEW", cycle=0, attempt=1,
                dispatch_ids=[f"re-lane-{index}" for index in range(1, 5)],
            )
        completed = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
             "build", "--help"], capture_output=True, text=True,
        )
        self.assertNotIn("RE_REVIEW", completed.stdout)

    def test_surface_convergence_fails_closed_without_contract_activation(self) -> None:
        # C3-01: the surface predicate must activate from any persisted
        # surface activity — a surface dispatch, completion record, or
        # terminal binding — even when review_contracts no longer lists the
        # surface contract or schema_version was downgraded.
        workspace, state, _ = self._workspace()
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
        loaded = ai_state_check._load_records(state, root=workspace)
        completed = ai_state_check._completion_records(state, loaded)
        self.assertTrue(ai_state_check._translation_surface_convergence_valid(
            state, loaded, completed, root=workspace)[0])
        for mutate in (
            lambda s: s.update({"review_contracts": ["code_legacy_v1"]}),
            lambda s: s.update({"schema_version": 4}),
        ):
            with self.subTest(mutate=mutate.__name__ if hasattr(mutate, "__name__") else "mutate"):
                mutated = json.loads(json.dumps(state))
                mutate(mutated)
                outcome = ai_state_check._translation_surface_convergence_valid(
                    mutated, loaded, completed, root=workspace)
                self.assertFalse(outcome[0])
                self.assertIn("DONE fails closed", outcome[1])
        # A surface dispatch alone (no completion records) also activates
        # the fail-closed guard.
        dispatch_only = json.loads(json.dumps(state))
        dispatch_only["review_contracts"] = ["code_legacy_v1"]
        dispatch_only["review_records"] = []
        dispatch_only["child_dispatches"] = state["child_dispatches"]
        outcome = ai_state_check._translation_surface_convergence_valid(
            dispatch_only, [], [], root=workspace)
        self.assertFalse(outcome[0])
        self.assertIn("DONE fails closed", outcome[1])

    def test_zero_terminal_requires_actual_empty_input_draft(self) -> None:
        # C3-02: the zero terminal binds its actual frozen input draft by
        # real bytes; a missing binding or a non-empty draft fails closed.
        def no_draft_binding(workspace, state):
            del state["surface_screen_input_path"]  # type: ignore[arg-type]
            binding = state["surface_evidence_binding"]  # type: ignore[index]
            del binding["artifact_sha256"][SURFACE_DRAFT_PATH]  # type: ignore[index]

        def nonempty_draft(workspace, state):
            self._write(workspace / SURFACE_DRAFT_PATH, _surface_payload(2))
            binding = state["surface_evidence_binding"]  # type: ignore[index]
            binding["artifact_sha256"][SURFACE_DRAFT_PATH] = hashlib.sha256(  # type: ignore[index]
                (workspace / SURFACE_DRAFT_PATH).read_bytes()
            ).hexdigest()

        def draft_bytes_drift(workspace, state):
            # Tampering with the bound draft bytes drifts the evidence
            # binding even when the artifact set is otherwise intact.
            path = workspace / SURFACE_DRAFT_PATH
            draft = json.loads(path.read_text(encoding="utf-8"))
            draft["rendered_briefing"] = "drifted"
            path.write_bytes(surface_screen_result_check.canonical_bytes(draft))

        for mutate in (no_draft_binding, nonempty_draft, draft_bytes_drift):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._install_zero_terminal(workspace, state)
                result = self._verify(workspace, state, mutate=mutate)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")

    def test_whole_screen_terminal_must_cover_the_bound_draft_exactly(self) -> None:
        # C3-02: for n<=80 the stage coverage must equal the unified frozen
        # input draft exactly; rebinding to a different draft fails closed.
        def rebound_draft(workspace, state):
            self._write(workspace / SURFACE_DRAFT_PATH, _surface_payload(2))
            binding = state["surface_evidence_binding"]  # type: ignore[index]
            binding["artifact_sha256"][SURFACE_DRAFT_PATH] = hashlib.sha256(  # type: ignore[index]
                (workspace / SURFACE_DRAFT_PATH).read_bytes()
            ).hexdigest()

        workspace, state, _ = self._workspace()
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=3)
        result = self._verify(workspace, state, mutate=rebound_draft)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("does not cover exactly the frozen input draft workset", result.detail)

    def _drift_draft_briefing(self, workspace: Path, state: dict[str, object]) -> None:
        # C4-01 mutation: drift the only shared scalar that is not bound into
        # entry_revision_identity (rendered_briefing), then rebind the
        # evidence hash so only the payload-semantics comparison can catch it.
        draft = json.loads((workspace / SURFACE_DRAFT_PATH).read_text(encoding="utf-8"))
        draft["rendered_briefing"] = "drifted briefing"
        self._write(workspace / SURFACE_DRAFT_PATH, draft)
        binding = state["surface_evidence_binding"]  # type: ignore[index]
        binding["artifact_sha256"][SURFACE_DRAFT_PATH] = hashlib.sha256(  # type: ignore[index]
            (workspace / SURFACE_DRAFT_PATH).read_bytes()
        ).hexdigest()

    def test_full_terminal_binds_complete_draft_payload_semantics(self) -> None:
        # C4-01: a full stage's envelope payload must equal the whole frozen
        # input draft, not only its entry identity keys.
        workspace, state, _ = self._workspace()
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2)
        result = self._verify(workspace, state, mutate=self._drift_draft_briefing)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn(
            "full surface envelope payload does not equal the frozen input draft",
            result.detail,
        )

    def test_lane_terminal_binds_whole_workset_draft_projection(self) -> None:
        # C4-01: a lane stage's manifest whole workset must equal the frozen
        # input draft, including all shared scalars and the briefing.
        workspace, state, _ = self._workspace()
        self._add_surface_stage(workspace, state, phase="REVIEW", cycle=0, attempt=1, count=5)
        result = self._verify(workspace, state, mutate=self._drift_draft_briefing)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn(
            "lane group whole workset does not equal the frozen input draft",
            result.detail,
        )

    def test_carry_terminal_binds_first80_projection_payload_semantics(self) -> None:
        # C4-01: an n>80 stage must equal the exact canonical first-80
        # projection of the frozen draft, including scalars and briefing.
        workspace, state, _ = self._workspace()
        full = _surface_payload(85)
        screen, _ = surface_screen_manifest.split_carry_over(full["entries"])
        stage_payload = {
            "contract": "translation_surface_screen_v1", **SURFACE_SCALARS,
            "rendered_briefing": "lane neutral", "entries": screen,
        }
        group, group_path, envelopes = surface_screen_manifest.build_group(
            stage_payload, task_id=SURFACE_TASK, group_id="group-0-1",
            review_phase="REVIEW", cycle=0, attempt=1,
            dispatch_ids=[f"lane-0-1-{index}" for index in range(1, 5)],
        )
        self._write(workspace / group_path, group)
        binding: dict[str, object] = {
            "algorithm": "surface-evidence-binding/1",
            "task_id": SURFACE_TASK,
            "terminal": "whole_screen",
            "artifact_sha256": {},
        }
        state["surface_evidence_binding"] = binding
        locators: list[str] = []
        for lane, boundary, (_, envelope) in zip(
            group["payload"]["lanes"], group["payload"]["lane_boundaries"], envelopes,
        ):
            self._write(workspace / lane["input_path"], envelope)
            raw = {
                "contract": "translation_surface_screen_v1",
                "candidate_identity": envelope["candidate_identity"],
                "results": [
                    {"entry_revision_identity": entry["entry_revision_identity"], "verdict": "OK"}
                    for entry in envelope["payload"]["entries"]
                ],
            }
            raw_path = f".ai/reviews/{SURFACE_TASK}/raw-{lane['dispatch_id']}.txt"
            self._write(workspace / raw_path, raw)
            lane_obj = {
                "group_id": group["payload"]["group_id"],
                "group_identity": group["group_identity"],
                "group_manifest_path": group_path,
                "index": boundary["index"], "count": 4,
                "offset": boundary["offset"], "length": boundary["length"],
            }
            record: dict[str, object] = {
                "task_id": SURFACE_TASK,
                "review_contract": "translation_surface_screen_v1",
                "review_phase": "REVIEW", "cycle": 0, "attempt": 1,
                "reviewer_role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "dispatch_id": lane["dispatch_id"],
                "agent_id": f"agent-{lane['dispatch_id']}",
                "workspace_id": "surface-workspace",
                "parent_agent_id": "agent-orchestrator",
                "lineage_verified": True,
                "result": "PASS", "review_kind": "lane",
                "candidate_identity": envelope["candidate_identity"],
                "input_path": lane["input_path"], "raw_output_path": raw_path,
                "raw_output_sha256": hashlib.sha256(
                    surface_screen_result_check.canonical_bytes(raw)
                ).hexdigest(),
                "lane": lane_obj,
            }
            dispatch: dict[str, object] = {
                "dispatch_id": lane["dispatch_id"], "role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "agent_id": f"agent-{lane['dispatch_id']}",
                "parent_agent_id": "agent-orchestrator",
                "workspace_id": "surface-workspace", "lineage_verified": True,
                "lifecycle": "archived", "archive_confirmed": True,
                "candidate_identity": envelope["candidate_identity"],
                "input_path": lane["input_path"],
                "lane_group_identity": lane_obj["group_identity"],
                "lane_index": lane_obj["index"],
                "labels": {
                    "task_id": SURFACE_TASK, "role": "reviewer",
                    "purpose": "translation_surface_screen_v1",
                    "candidate_identity": envelope["candidate_identity"],
                    "dispatch_id": lane["dispatch_id"],
                    "lane_group_identity": lane_obj["group_identity"],
                    "lane_index": lane_obj["index"],
                },
            }
            self._write(workspace / f"{lane['dispatch_id']}.json", record)
            state["review_records"].append(f"{lane['dispatch_id']}.json")  # type: ignore[union-attr]
            state["child_dispatches"].append(dispatch)  # type: ignore[union-attr]
            locators.extend((lane["input_path"], raw_path))
        self._write(workspace / SURFACE_DRAFT_PATH, full)
        state["surface_screen_input_path"] = SURFACE_DRAFT_PATH
        carry = surface_screen_manifest.build_carry_over_payload(
            full, task_id=SURFACE_TASK)
        carry_path = surface_screen_manifest.carry_over_artifact_path(SURFACE_TASK)
        self._write(workspace / carry_path, carry)
        state["surface_carry_over_path"] = carry_path
        locators.extend((SURFACE_DRAFT_PATH, carry_path))
        hashes = binding["artifact_sha256"]  # type: ignore[index]
        for locator in locators:
            hashes[locator] = hashlib.sha256(  # type: ignore[index]
                (workspace / locator).read_bytes()
            ).hexdigest()
        result = self._verify(workspace, state, mutate=self._drift_draft_briefing)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn(
            "lane group whole workset does not equal the frozen input draft",
            result.detail,
        )

    def test_surface_retry_history_failed_then_success_is_done_verified(self) -> None:
        # C3-05: a failed attempt followed by a fresh, higher-attempt
        # successful stage is an honest terminal.
        workspace, state, _ = self._workspace()
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2,
            result="FINDINGS",
        )
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=2, count=2,
            result="PASS",
        )
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_surface_retry_attempts_must_be_monotonic_and_precede_success(self) -> None:
        # C3-05: attempts must increase monotonically across the retry
        # history, and every failed attempt must precede the successful
        # stage.  Same attempt number at a higher cycle is not a fresh retry.
        workspace, state, _ = self._workspace()
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2,
            result="FINDINGS",
        )
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=1, attempt=1, count=2,
            result="PASS",
        )
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("monotonically", result.detail)

        workspace, state, _ = self._workspace()
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=2, count=2,
            result="FINDINGS",
        )
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2,
            result="PASS",
        )
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("must precede the successful stage", result.detail)

    def _add_orphan_lane_group(
        self,
        workspace: Path,
        state: dict[str, object],
        *,
        cycle: int,
        attempt: int,
        group_id: str,
    ) -> tuple[str, str]:
        """Persist one failed lane attempt as orphan children: the group
        manifest and lane envelopes exist, the four children are archived
        surface dispatches, but no completion record was ever published and
        nothing enters the terminal evidence binding (C4-02)."""
        group, group_path, envelopes = surface_screen_manifest.build_group(
            _surface_payload(5), task_id=SURFACE_TASK, group_id=group_id,
            review_phase="REVIEW", cycle=cycle, attempt=attempt,
            dispatch_ids=[f"lane-{cycle}-{attempt}-{index}" for index in range(1, 5)],
        )
        self._write(workspace / group_path, group)
        for lane, (_, envelope) in zip(group["payload"]["lanes"], envelopes):
            self._write(workspace / lane["input_path"], envelope)
            dispatch: dict[str, object] = {
                "dispatch_id": lane["dispatch_id"], "role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "agent_id": f"agent-{lane['dispatch_id']}",
                "parent_agent_id": "agent-orchestrator",
                "workspace_id": "surface-workspace", "lineage_verified": True,
                "lifecycle": "archived", "archive_confirmed": True,
                "candidate_identity": envelope["candidate_identity"],
                "input_path": lane["input_path"],
                "lane_group_identity": group["group_identity"],
                "lane_index": lane["index"],
                "labels": {
                    "task_id": SURFACE_TASK, "role": "reviewer",
                    "purpose": "translation_surface_screen_v1",
                    "candidate_identity": envelope["candidate_identity"],
                    "dispatch_id": lane["dispatch_id"],
                    "lane_group_identity": group["group_identity"],
                    "lane_index": lane["index"],
                },
            }
            state["child_dispatches"].append(dispatch)  # type: ignore[union-attr]
        return group["group_identity"], group_path

    def test_surface_orphan_failed_children_join_retry_history(self) -> None:
        # C4-02: orphan failed surface children (dispatched, archived, no
        # completion record) are part of the retry history.  A legal fresh
        # retry after an orphaned attempt still verifies.
        workspace, state, _ = self._workspace()
        self._add_orphan_lane_group(
            workspace, state, cycle=0, attempt=1, group_id="group-0-1",
        )
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=2, count=5,
        )
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_surface_orphan_identity_reuse_fails_closed(self) -> None:
        # C4-02: the successful stage must not reuse an orphan failed
        # child's agent identity.
        workspace, state, _ = self._workspace()
        self._add_orphan_lane_group(
            workspace, state, cycle=0, attempt=1, group_id="group-0-1",
        )
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=2, count=2,
        )
        record_path = workspace / "review-0-2.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        orphan_agent = "agent-lane-0-1-1"
        record["agent_id"] = orphan_agent
        self._write(record_path, record)
        dispatch = state["child_dispatches"][-1]  # type: ignore[index]
        dispatch["agent_id"] = orphan_agent
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn(
            "must not reuse a failed attempt's dispatch/agent identity",
            result.detail,
        )

    def test_surface_orphan_group_manifest_path_reuse_fails_closed(self) -> None:
        # C4-02: reusing an orphan attempt's group_id (hence its group
        # manifest path) destroys the manifest bound by the orphan's
        # lane_group_identity and must fail closed.
        workspace, state, _ = self._workspace()
        group_identity, group_path = self._add_orphan_lane_group(
            workspace, state, cycle=0, attempt=1, group_id="group-0-1",
        )
        payload = _surface_payload(5)
        rewritten, rewritten_path, envelopes = surface_screen_manifest.build_group(
            payload, task_id=SURFACE_TASK, group_id="group-0-1",
            review_phase="REVIEW", cycle=0, attempt=2,
            dispatch_ids=[f"lane-0-2-{index}" for index in range(1, 5)],
        )
        self.assertEqual(rewritten_path, group_path)
        self.assertNotEqual(rewritten["group_identity"], group_identity)
        self._write(workspace / rewritten_path, rewritten)
        self._write(workspace / SURFACE_DRAFT_PATH, payload)
        state["surface_screen_input_path"] = SURFACE_DRAFT_PATH
        state["surface_evidence_binding"] = {
            "algorithm": "surface-evidence-binding/1",
            "task_id": SURFACE_TASK,
            "terminal": "whole_screen",
            "artifact_sha256": {
                SURFACE_DRAFT_PATH: hashlib.sha256(
                    (workspace / SURFACE_DRAFT_PATH).read_bytes()
                ).hexdigest(),
            },
        }
        for lane, boundary, (_, envelope) in zip(
            rewritten["payload"]["lanes"], rewritten["payload"]["lane_boundaries"], envelopes,
        ):
            self._write(workspace / lane["input_path"], envelope)
            raw = {
                "contract": "translation_surface_screen_v1",
                "candidate_identity": envelope["candidate_identity"],
                "results": [
                    {"entry_revision_identity": entry["entry_revision_identity"], "verdict": "OK"}
                    for entry in envelope["payload"]["entries"]
                ],
            }
            raw_path = f".ai/reviews/{SURFACE_TASK}/raw-{lane['dispatch_id']}.txt"
            self._write(workspace / raw_path, raw)
            lane_obj = {
                "group_id": rewritten["payload"]["group_id"],
                "group_identity": rewritten["group_identity"],
                "group_manifest_path": rewritten_path,
                "index": boundary["index"], "count": 4,
                "offset": boundary["offset"], "length": boundary["length"],
            }
            record: dict[str, object] = {
                "task_id": SURFACE_TASK,
                "review_contract": "translation_surface_screen_v1",
                "review_phase": "REVIEW", "cycle": 0, "attempt": 2,
                "reviewer_role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "dispatch_id": lane["dispatch_id"],
                "agent_id": f"agent-{lane['dispatch_id']}",
                "workspace_id": "surface-workspace",
                "parent_agent_id": "agent-orchestrator",
                "lineage_verified": True,
                "result": "PASS", "review_kind": "lane",
                "candidate_identity": envelope["candidate_identity"],
                "input_path": lane["input_path"], "raw_output_path": raw_path,
                "raw_output_sha256": hashlib.sha256(
                    surface_screen_result_check.canonical_bytes(raw)
                ).hexdigest(),
                "lane": lane_obj,
            }
            dispatch: dict[str, object] = {
                "dispatch_id": lane["dispatch_id"], "role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "agent_id": f"agent-{lane['dispatch_id']}",
                "parent_agent_id": "agent-orchestrator",
                "workspace_id": "surface-workspace", "lineage_verified": True,
                "lifecycle": "archived", "archive_confirmed": True,
                "candidate_identity": envelope["candidate_identity"],
                "input_path": lane["input_path"],
                "lane_group_identity": lane_obj["group_identity"],
                "lane_index": lane_obj["index"],
                "labels": {
                    "task_id": SURFACE_TASK, "role": "reviewer",
                    "purpose": "translation_surface_screen_v1",
                    "candidate_identity": envelope["candidate_identity"],
                    "dispatch_id": lane["dispatch_id"],
                    "lane_group_identity": lane_obj["group_identity"],
                    "lane_index": lane_obj["index"],
                },
            }
            self._write(workspace / f"{lane['dispatch_id']}.json", record)
            state["review_records"].append(f"{lane['dispatch_id']}.json")  # type: ignore[union-attr]
            state["child_dispatches"].append(dispatch)  # type: ignore[union-attr]
            state["surface_evidence_binding"]["artifact_sha256"][lane["input_path"]] = hashlib.sha256(  # type: ignore[index]
                (workspace / str(lane["input_path"])).read_bytes()
            ).hexdigest()
            state["surface_evidence_binding"]["artifact_sha256"][raw_path] = hashlib.sha256(  # type: ignore[index]
                (workspace / raw_path).read_bytes()
            ).hexdigest()
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("cannot be located by its bound lane_group_identity", result.detail)

    def test_surface_orphan_attempt_must_precede_success(self) -> None:
        # C4-02: an orphan attempt numbered above the successful stage is a
        # non-monotonic retry history and fails closed.
        workspace, state, _ = self._workspace()
        self._add_orphan_lane_group(
            workspace, state, cycle=0, attempt=2, group_id="group-0-2",
        )
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=1, count=5,
        )
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("must precede the successful stage", result.detail)

    def test_surface_retry_all_failed_history_cannot_close(self) -> None:
        workspace, state, _ = self._workspace()
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2,
            result="FINDINGS",
        )
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn("without a successful terminal stage", result.detail)

    def test_surface_retry_identity_freshness_predicate(self) -> None:
        # C3-05: unit probe of the retry-history predicate — no failed child
        # identity (dispatch, agent, group) may be reused.
        def retry_record(result, attempt, dispatch, agent, lane=None):
            record = {
                "result": result, "cycle": 0, "attempt": attempt,
                "dispatch_id": dispatch, "agent_id": agent,
            }
            if lane is not None:
                record["lane"] = lane
            return record

        def bind(items):
            return [(record, {}, Path("record.json")) for record in items]

        lane_failed = {
            "group_id": "group-a", "group_identity": "identity-a",
            "group_manifest_path": ".ai/task/t/SURFACE-SCREEN-GROUP-group-a.json",
            "index": 1, "count": 4, "offset": 0, "length": 1,
        }
        lane_success_same_group = {
            **lane_failed, "group_identity": "identity-b",
            "group_manifest_path": ".ai/task/t/SURFACE-SCREEN-GROUP-group-b.json",
        }
        failed = [retry_record("CHANGES_REQUIRED", 1, "dispatch-1", "agent-1")]
        success = [retry_record("PASS", 2, "dispatch-2", "agent-2")]
        ok = ai_state_check._surface_retry_history_valid(
            {}, bind(failed), bind(success))
        self.assertTrue(ok[0])
        reused_dispatch = [retry_record("PASS", 2, "dispatch-1", "agent-2")]
        outcome = ai_state_check._surface_retry_history_valid(
            {}, bind(failed), bind(reused_dispatch))
        self.assertIn("must not reuse a failed attempt's", outcome[1])
        reused_agent = [retry_record("PASS", 2, "dispatch-2", "agent-1")]
        outcome = ai_state_check._surface_retry_history_valid(
            {}, bind(failed), bind(reused_agent))
        self.assertIn("must not reuse a failed attempt's", outcome[1])
        failed_lane = [retry_record("CHANGES_REQUIRED", 1, "dispatch-1", "agent-1", lane=lane_failed)]
        success_lane = [retry_record("PASS", 2, "dispatch-2", "agent-2", lane=lane_success_same_group)]
        outcome = ai_state_check._surface_retry_history_valid(
            {}, bind(failed_lane), bind(success_lane))
        self.assertIn("must not reuse a failed attempt's lane group", outcome[1])
        duplicate_failed = [
            retry_record("CHANGES_REQUIRED", 1, "dispatch-1", "agent-1"),
            retry_record("FINDINGS", 2, "dispatch-2", "agent-1"),
        ]
        fresh_success = [retry_record("PASS", 3, "dispatch-3", "agent-3")]
        outcome = ai_state_check._surface_retry_history_valid(
            {}, bind(duplicate_failed), bind(fresh_success))
        self.assertIn("fresh dispatch/agent identities", outcome[1])
        failed_after_success = [retry_record("CHANGES_REQUIRED", 3, "dispatch-3", "agent-3")]
        outcome = ai_state_check._surface_retry_history_valid(
            {}, bind(success + failed_after_success), bind(success))
        self.assertIn("must precede the successful stage", outcome[1])

    def test_surface_retry_failed_lane_stage_members_share_one_group_tuple(self):
        # C5-01 (positive half): the four members of one failed lane stage
        # may share one group tuple; a fresh successful stage still closes.
        def retry_record(result, attempt, dispatch, agent, lane=None):
            record = {
                "result": result, "cycle": 0, "attempt": attempt,
                "dispatch_id": dispatch, "agent_id": agent,
            }
            if lane is not None:
                record["lane"] = lane
            return record

        def bind(items):
            return [(record, {}, Path("record.json")) for record in items]

        group_tuple = {
            "group_id": "group-a", "group_identity": "identity-a",
            "group_manifest_path": ".ai/task/t/SURFACE-SCREEN-GROUP-group-a.json",
        }
        failed_stage = [
            retry_record("FINDINGS", 1, f"dispatch-1-{index}", f"agent-1-{index}",
                         lane={**group_tuple, "index": index, "count": 4,
                              "offset": index - 1, "length": 1})
            for index in range(1, 5)
        ]
        success = [retry_record("PASS", 2, "dispatch-2", "agent-2")]
        ok = ai_state_check._surface_retry_history_valid(
            {}, bind(failed_stage), bind(success))
        self.assertTrue(ok[0])

    def test_surface_retry_failed_stage_group_reuse_is_rejected(self):
        # C5-01 (negative half): group_id, group_identity, and
        # group_manifest_path must each stay fresh between two distinct
        # failed stages; reusing any one of them fails closed.
        def retry_record(result, attempt, dispatch, agent, lane=None):
            record = {
                "result": result, "cycle": 0, "attempt": attempt,
                "dispatch_id": dispatch, "agent_id": agent,
            }
            if lane is not None:
                record["lane"] = lane
            return record

        def bind(items):
            return [(record, {}, Path("record.json")) for record in items]

        stage_one_tuple = {
            "group_id": "group-a", "group_identity": "identity-a",
            "group_manifest_path": ".ai/task/t/SURFACE-SCREEN-GROUP-group-a.json",
        }
        stage_one = [
            retry_record("FINDINGS", 1, f"dispatch-1-{index}", f"agent-1-{index}",
                         lane={**stage_one_tuple, "index": index, "count": 4,
                               "offset": index - 1, "length": 1})
            for index in range(1, 5)
        ]
        success = [retry_record("PASS", 3, "dispatch-3", "agent-3")]
        for reused_key in ("group_id", "group_identity", "group_manifest_path"):
            stage_two_tuple = {
                "group_id": "group-b", "group_identity": "identity-b",
                "group_manifest_path": ".ai/task/t/SURFACE-SCREEN-GROUP-group-b.json",
            }
            stage_two_tuple[reused_key] = stage_one_tuple[reused_key]
            stage_two = [
                retry_record("CHANGES_REQUIRED", 2, f"dispatch-2-{index}",
                             f"agent-2-{index}",
                             lane={**stage_two_tuple, "index": index, "count": 4,
                                   "offset": index - 1, "length": 1})
                for index in range(1, 5)
            ]
            with self.subTest(reused_key=reused_key):
                outcome = ai_state_check._surface_retry_history_valid(
                    {}, bind(stage_one + stage_two), bind(success))
                self.assertFalse(outcome[0])
                self.assertIn(
                    "must not reuse an earlier failed attempt's lane group",
                    outcome[1],
                )

    def test_surface_failed_stage_group_reuse_fails_closed(self):
        # C5-01 (file-backed): two distinct failed lane stages reusing one
        # group tuple fail closed even though a fresh successful stage
        # follows; sharing within one failed stage stays legal.
        workspace, state, _ = self._workspace()
        first = self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=1, count=5,
            result="FINDINGS",
        )
        second = self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=2, count=5,
            result="FINDINGS",
        )
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=3, count=5,
            result="PASS",
        )
        first_lane = first[0]["lane"]
        assert isinstance(first_lane, dict)
        for record in second:
            lane = record["lane"]
            assert isinstance(lane, dict)
            lane["group_id"] = first_lane["group_id"]
            lane["group_identity"] = first_lane["group_identity"]
            lane["group_manifest_path"] = first_lane["group_manifest_path"]
            self._write(workspace / f"{record['dispatch_id']}.json", record)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn(
            "must not reuse an earlier failed attempt's lane group", result.detail,
        )

    def test_surface_failed_stage_reusing_orphan_group_fails_closed(self):
        # C5-01: a failed record stage must not reuse an orphan failed
        # attempt's group_id/group_identity/group manifest path either.
        workspace, state, _ = self._workspace()
        group_identity, group_path = self._add_orphan_lane_group(
            workspace, state, cycle=0, attempt=1, group_id="group-0-1",
        )
        second = self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=2, count=5,
            result="FINDINGS",
        )
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=3, count=5,
            result="PASS",
        )
        for record in second:
            lane = record["lane"]
            assert isinstance(lane, dict)
            lane["group_id"] = "group-0-1"
            lane["group_identity"] = group_identity
            lane["group_manifest_path"] = group_path
            self._write(workspace / f"{record['dispatch_id']}.json", record)
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
        self.assertIn(
            "must not reuse an earlier failed attempt's lane group", result.detail,
        )

    def test_surface_partially_orphaned_failed_stage_then_success(self):
        # SR-01 regression: one legal failed stage (cycle 0, attempt 1) whose
        # four members share one group tuple but split across the
        # orphan/record boundary — three FINDINGS records plus one orphan
        # lane child — followed by a fresh successful stage must verify.
        # The orphan and record-bound members claim their shared group tuple
        # in one per-stage map; treating them as two distinct stages (and so
        # rejecting the legal stage as cross-stage group reuse) fails closed
        # is the bug this test pins.
        workspace, state, _ = self._workspace()
        group_identity, group_path = self._add_orphan_lane_group(
            workspace, state, cycle=0, attempt=1, group_id="group-0-1",
        )
        manifest = json.loads((workspace / group_path).read_text(encoding="utf-8"))
        boundaries = manifest["payload"]["lane_boundaries"]
        failed_records: list[dict[str, object]] = []
        for lane in manifest["payload"]["lanes"][:3]:
            envelope = json.loads(
                (workspace / str(lane["input_path"])).read_text(encoding="utf-8")
            )
            boundary = next(b for b in boundaries if b["index"] == lane["index"])
            lane_obj = {
                "group_id": manifest["payload"]["group_id"],
                "group_identity": group_identity,
                "group_manifest_path": group_path,
                "index": boundary["index"], "count": 4,
                "offset": boundary["offset"], "length": boundary["length"],
            }
            raw = {
                "contract": "translation_surface_screen_v1",
                "candidate_identity": envelope["candidate_identity"],
                "results": [
                    {"entry_revision_identity": entry["entry_revision_identity"], "verdict": "OK"}
                    for entry in envelope["payload"]["entries"]
                ],
            }
            raw_path = f".ai/reviews/{SURFACE_TASK}/raw-{lane['dispatch_id']}.txt"
            self._write(workspace / raw_path, raw)
            record: dict[str, object] = {
                "task_id": SURFACE_TASK,
                "review_contract": "translation_surface_screen_v1",
                "review_phase": "REVIEW", "cycle": 0, "attempt": 1,
                "reviewer_role": "REVIEWER",
                "purpose": "translation_surface_screen_v1",
                "dispatch_id": lane["dispatch_id"],
                "agent_id": f"agent-{lane['dispatch_id']}",
                "workspace_id": "surface-workspace",
                "parent_agent_id": "agent-orchestrator",
                "lineage_verified": True,
                "result": "FINDINGS", "review_kind": "lane",
                "candidate_identity": envelope["candidate_identity"],
                "input_path": lane["input_path"], "raw_output_path": raw_path,
                "raw_output_sha256": hashlib.sha256(
                    surface_screen_result_check.canonical_bytes(raw)
                ).hexdigest(),
                "lane": lane_obj,
            }
            record_file = workspace / f"{lane['dispatch_id']}.json"
            self._write(record_file, record)
            state["review_records"].append(  # type: ignore[union-attr]
                str(record_file.relative_to(workspace))
            )
            failed_records.append(record)
        # The exact whole-screen evidence map covers every dispatch-bound
        # record (failed and successful); the orphan member has no record and
        # stays out of the binding.
        self._bind_whole_screen(workspace, state, failed_records)
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=2, count=5,
        )
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_surface_purpose_relabeling_cannot_hide_orphan_children(self):
        # C5-02: deleting or relabeling an orphan surface child's purpose
        # cannot remove it from the retry history: the persisted
        # lane_group_identity, or the canonical task-derived SURFACE-SCREEN
        # input path, still identifies it, so identity reuse fails closed.
        def relabel_children(workspace: Path, state: dict[str, object]) -> None:
            for dispatch in state["child_dispatches"]:  # type: ignore[type-var, union-attr]
                if str(dispatch["dispatch_id"]).startswith("lane-0-1-"):
                    dispatch["purpose"] = "translation_contextual_v1"  # type: ignore[index]

        def strip_children(workspace: Path, state: dict[str, object]) -> None:
            for dispatch in state["child_dispatches"]:  # type: ignore[type-var, union-attr]
                if str(dispatch["dispatch_id"]).startswith("lane-0-1-"):
                    dispatch.pop("purpose", None)
                    dispatch.pop("lane_group_identity", None)
                    labels = dispatch["labels"]
                    assert isinstance(labels, dict)
                    labels.pop("purpose", None)
                    labels.pop("lane_group_identity", None)
                    labels.pop("lane_index", None)

        for mutate in (relabel_children, strip_children):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._add_orphan_lane_group(
                    workspace, state, cycle=0, attempt=1, group_id="group-0-1",
                )
                self._add_surface_stage(
                    workspace, state, phase="REVIEW", cycle=0, attempt=2, count=5,
                )
                mutate(workspace, state)
                orphan_agent = "agent-lane-0-1-1"
                record_path = workspace / "lane-0-2-1.json"
                record = json.loads(record_path.read_text(encoding="utf-8"))
                record["agent_id"] = orphan_agent
                self._write(record_path, record)
                dispatch = next(
                    item for item in state["child_dispatches"]  # type: ignore[union-attr]
                    if item["dispatch_id"] == "lane-0-2-1"  # type: ignore[index]
                )
                dispatch["agent_id"] = orphan_agent
                result = self._verify(workspace, state)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
                self.assertIn(
                    "must not reuse a failed attempt's dispatch/agent identity",
                    result.detail,
                )

    def test_surface_orphan_inference_stays_bounded(self):
        # C5-02: the orphan inference never becomes a generalized heuristic —
        # a purpose-less child with a non-canonical input path and no
        # persisted lane_group_identity is not a surface orphan.
        workspace, state, _ = self._workspace()
        self._add_surface_stage(
            workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2,
        )
        state["child_dispatches"].append({  # type: ignore[union-attr]
            "dispatch_id": "unrelated-1", "role": "REVIEWER",
            "agent_id": "agent-unrelated-1",
            "parent_agent_id": "agent-orchestrator",
            "workspace_id": "surface-workspace", "lineage_verified": True,
            "lifecycle": "archived", "archive_confirmed": True,
            "input_path": ".ai/task/other-task/SURFACE-SCREEN-ENVELOPE-unrelated-1.json",
        })
        result = self._verify(workspace, state)
        self.assertEqual(result.outcome, "DONE_VERIFIED")

    def test_stop_record_loader_handles_each_path_independently(self):
        # C5-03: unit probe of the tolerant STOP loader — one unavailable,
        # malformed, or non-object locator must not discard the other
        # records; every valid record is retained.
        workspace, state, _ = self._workspace()
        good = workspace / "good.json"
        self._write(good, {"purpose": "translation_surface_screen_v1"})
        broken = workspace / "broken.json"
        broken.write_text("{", encoding="utf-8")
        non_object = workspace / "non-object.json"
        self._write(non_object, [{"ordinary": "value"}])
        state["review_records"] = [
            "missing.json",
            str(broken.relative_to(workspace)),
            str(good.relative_to(workspace)),
            str(non_object.relative_to(workspace)),
        ]
        state["senior_review_records"] = ["also-missing.json"]
        loaded = ai_state_check._load_records_for_stop(state, root=workspace)
        self.assertEqual(
            [record.get("purpose") for record, _ in loaded],
            ["translation_surface_screen_v1"],
        )

    def test_stop_bad_record_path_cannot_hide_surface_records(self):
        # C5-03 (file-backed): with every non-record surface signal removed
        # (relabeled children, no terminal bindings), the persisted surface
        # completion records are the only surface activity left — a broken
        # unrelated record path before them must not let STOP close.
        def broken_paths_first(workspace: Path, state: dict[str, object]) -> None:
            broken = Path("broken-records")
            (workspace / broken).mkdir(exist_ok=True)
            (workspace / broken / "invalid.json").write_text("{", encoding="utf-8")
            (workspace / broken / "non-object.json").write_bytes(
                surface_screen_result_check.canonical_bytes(["list"])
            )
            records = state["review_records"]
            assert isinstance(records, list)
            state["review_records"] = [
                str(broken / "missing.json"),
                str(broken / "invalid.json"),
                str(broken / "non-object.json"),
                *records,
            ]

        def broken_paths_last(workspace: Path, state: dict[str, object]) -> None:
            broken = Path("broken-records")
            (workspace / broken).mkdir(exist_ok=True)
            (workspace / broken / "invalid.json").write_text("{", encoding="utf-8")
            records = state["review_records"]
            assert isinstance(records, list)
            state["review_records"] = [
                *records,
                str(broken / "missing.json"),
                str(broken / "invalid.json"),
            ]

        for mutate in (broken_paths_first, broken_paths_last):
            with self.subTest(mutate=mutate.__name__):
                workspace, state, _ = self._workspace()
                self._add_surface_stage(
                    workspace, state, phase="REVIEW", cycle=0, attempt=1, count=2,
                )
                state["state"] = "STOP"
                for dispatch in state["child_dispatches"]:  # type: ignore[type-var, union-attr]
                    dispatch["purpose"] = "translation_contextual_v1"  # type: ignore[index]
                    labels = dispatch["labels"]
                    assert isinstance(labels, dict)
                    labels["purpose"] = "translation_contextual_v1"
                state.pop("surface_screen_input_path")
                state.pop("surface_evidence_binding")
                mutate(workspace, state)
                result = self._verify(workspace, state)
                self.assertEqual(result.outcome, "NEW_CONTRACT_FAILED")
                self.assertIn(
                    "STOP cannot close a dispatched surface screen", result.detail,
                )


def load_tests(loader, tests, pattern):
    """Keep the v2 validator modules in the established contract-suite entry."""
    from tests.i18n import test_contextual_lane_manifest, test_contextual_result_check

    tests.addTests(loader.loadTestsFromModule(test_contextual_result_check))
    tests.addTests(loader.loadTestsFromModule(test_contextual_lane_manifest))
    return tests


if __name__ == "__main__":
    unittest.main()
