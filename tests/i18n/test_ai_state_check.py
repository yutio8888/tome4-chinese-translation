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
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import ai_state_check


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

    def test_production_code_and_contextual_fixtures_are_done_verified(self) -> None:
        self.assertEqual(ai_state_check.check_state(FIXTURES / "code" / "STATE.json").outcome, "DONE_VERIFIED")
        state_path, state, record = self._copy_fixture("contextual")
        self._write(state_path.parent / "review.json", record)
        self._write(state_path, state)
        self.assertEqual(ai_state_check.check_state(state_path).outcome, "DONE_VERIFIED")

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


if __name__ == "__main__":
    unittest.main()
