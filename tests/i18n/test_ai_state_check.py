from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import ai_state_check
from ai_state_check import validate

# A valid state document, shaped like the real .ai/task/STATE.json.
VALID = {
    "task_id": "orchestration-dryrun-001",
    "mode": "implement",
    "baseline": {
        "type": "snapshot",
        "ref": "worktree-2026-08-12T23-58Z",
        "files": {},
    },
    "state": "IMPLEMENT",
    "cycle": 0,
    "max_cycles": 2,
    "step": 2,
    "plan_rev": 0,
    "executor": {
        "provider": "pi",
        "model_id": "opencode-go/deepseek-v4-flash",
        "agent_id": None,
    },
    "reviewer": {
        "provider": "codex",
        "model_id": "gpt-5.6-sol",
        "agent_id": None,
    },
    "accepted_findings": [],
    "rejected_findings": [],
    "deferred_findings": [],
    "last_action": "PLAN->IMPLEMENT",
    "last_error": "",
    "retry_count": 0,
    "updated_at": "2026-08-12T23:59:00Z",
    "history": [
        {"from": None, "to": "PLAN", "step": 1, "at": "2026-08-12T23:58:00Z"},
        {"from": "PLAN", "to": "IMPLEMENT", "step": 2, "at": "2026-08-12T23:59:00Z"},
    ],
}

MINIMAL = {key: value for key, value in VALID.items() if key != "history"}

EXPECTED_TRANSITIONS = {
    "PLAN": ("REVIEW", "IMPLEMENT"),
    "IMPLEMENT": ("IMPLEMENTATION_VALIDATE",),
    "IMPLEMENTATION_VALIDATE": ("REVIEW", "FIX", "STOP"),
    "REVIEW": ("ADJUDICATE",),
    "ADJUDICATE": ("FIX", "WAIT_USER", "FINAL_REVIEW"),
    "FIX": ("TEST",),
    "TEST": ("RE_REVIEW",),
    "RE_REVIEW": ("ADJUDICATE",),
    "FINAL_REVIEW": ("FINAL_VALIDATE", "FIX", "STOP"),
    "FINAL_VALIDATE": ("DONE", "FIX", "STOP"),
    "WAIT_USER": ("ADJUDICATE", "STOP"),
    "STOP": (),
    "DONE": (),
}


def write_json(payload: object) -> str:
    """Write payload to a temp file and return its path (cleaned up by the test)."""
    path = Path(tempfile.mkstemp(suffix=".json")[1])
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return str(path)


class SchemaTests(unittest.TestCase):
    def test_valid_minimal(self):
        code, message = validate(write_json(MINIMAL))
        self.assertEqual(code, 0, message)

    def test_valid_with_history(self):
        code, message = validate(write_json(VALID))
        self.assertEqual(code, 0, message)

    def test_valid_review_only_mode(self):
        payload = dict(MINIMAL, mode="review_only")
        code, message = validate(write_json(payload))
        self.assertEqual(code, 0, message)

    def test_missing_each_required_field(self):
        for field in ai_state_check.REQUIRED_FIELDS:
            payload = {key: value for key, value in MINIMAL.items() if key != field}
            with self.subTest(field=field):
                code, message = validate(write_json(payload))
                self.assertEqual(code, 1, message)
                self.assertIn(field, message)

    def test_invalid_state(self):
        payload = dict(MINIMAL, state="NOT_A_STATE")
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("NOT_A_STATE", message)

    def test_invalid_mode(self):
        payload = dict(MINIMAL, mode="implementing")
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("mode", message)

    def test_field_type_errors(self):
        cases = [
            ("task_id", 123),
            ("task_id", ""),
            ("mode", 1),
            ("baseline", []),
            ("state", []),
            ("cycle", "0"),
            ("cycle", True),
            ("max_cycles", 0),
            ("max_cycles", True),
            ("step", 0),
            ("plan_rev", -1),
            ("executor", "pi"),
            ("reviewer", []),
            ("accepted_findings", {}),
            ("rejected_findings", "x"),
            ("deferred_findings", 3),
            ("last_action", None),
            ("last_error", 3),
            ("retry_count", -1),
            ("updated_at", 1),
        ]
        for field, value in cases:
            payload = dict(MINIMAL)
            payload[field] = value
            with self.subTest(field=field, value=value):
                code, message = validate(write_json(payload))
                self.assertEqual(code, 1, message)
                self.assertIn(field, message)

    def test_cycle_exceeds_max_cycles(self):
        payload = dict(MINIMAL, cycle=3, max_cycles=2)
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("cycle", message)

    def test_cycle_equal_to_max_cycles_is_valid(self):
        payload = dict(MINIMAL, cycle=2, max_cycles=2)
        code, message = validate(write_json(payload))
        self.assertEqual(code, 0, message)

    def test_role_missing_fields(self):
        for role in ("executor", "reviewer"):
            payload = dict(MINIMAL)
            payload[role] = {"provider": "pi"}
            with self.subTest(role=role):
                code, message = validate(write_json(payload))
                self.assertEqual(code, 1, message)
                self.assertIn("model_id", message)

    def test_agent_id_must_be_str_or_null(self):
        payload = dict(MINIMAL)
        payload["executor"] = {
            "provider": "pi",
            "model_id": "deepseek-v4-flash",
            "agent_id": 7,
        }
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("agent_id", message)

    def test_extra_unknown_fields_allowed(self):
        payload = dict(MINIMAL, future_field={"anything": 1})
        code, message = validate(write_json(payload))
        self.assertEqual(code, 0, message)


class HistoryTests(unittest.TestCase):
    def test_history_empty(self):
        payload = dict(MINIMAL, history=[])
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("history", message)

    def test_history_not_a_list(self):
        payload = dict(MINIMAL, history={})
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)

    def test_history_missing_fields(self):
        payload = dict(MINIMAL, history=[{"from": None, "to": "PLAN"}])
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("step", message)
        self.assertIn("at", message)

    def test_history_illegal_transition(self):
        payload = dict(
            MINIMAL,
            state="FIX",
            history=[
                {"from": None, "to": "PLAN", "step": 1, "at": "t"},
                {"from": "PLAN", "to": "FIX", "step": 2, "at": "t"},
            ],
        )
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("illegal transition", message)

    def test_history_last_to_mismatch_state(self):
        payload = dict(
            MINIMAL,
            state="IMPLEMENT",
            history=[
                {"from": None, "to": "PLAN", "step": 1, "at": "t"},
                {"from": "PLAN", "to": "IMPLEMENTATION_VALIDATE", "step": 2, "at": "t"},
            ],
        )
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("does not match", message)

    def test_history_step_not_monotonic(self):
        payload = dict(
            MINIMAL,
            history=[
                {"from": None, "to": "PLAN", "step": 1, "at": "t"},
                {"from": "PLAN", "to": "IMPLEMENT", "step": 1, "at": "t"},
            ],
        )
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("step", message)

    def test_history_adjacency_violation(self):
        payload = dict(
            MINIMAL,
            history=[
                {"from": None, "to": "PLAN", "step": 1, "at": "t"},
                {"from": "REVIEW", "to": "ADJUDICATE", "step": 2, "at": "t"},
            ],
        )
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("does not match", message)

    def test_history_invalid_state_value(self):
        payload = dict(
            MINIMAL,
            history=[{"from": None, "to": "BOGUS", "step": 1, "at": "t"}],
        )
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("BOGUS", message)

    def test_terminal_state_has_no_outgoing(self):
        payload = dict(
            MINIMAL,
            state="DONE",
            history=[
                {"from": None, "to": "DONE", "step": 1, "at": "t"},
                {"from": "DONE", "to": "STOP", "step": 2, "at": "t"},
            ],
        )
        code, message = validate(write_json(payload))
        self.assertEqual(code, 1)
        self.assertIn("illegal transition", message)

    def test_full_cycle_history_is_valid(self):
        payload = dict(
            MINIMAL,
            state="DONE",
            history=[
                {"from": None, "to": "PLAN", "step": 1, "at": "t"},
                {"from": "PLAN", "to": "IMPLEMENT", "step": 2, "at": "t"},
                {"from": "IMPLEMENT", "to": "IMPLEMENTATION_VALIDATE", "step": 3, "at": "t"},
                {"from": "IMPLEMENTATION_VALIDATE", "to": "REVIEW", "step": 4, "at": "t"},
                {"from": "REVIEW", "to": "ADJUDICATE", "step": 5, "at": "t"},
                {"from": "ADJUDICATE", "to": "FINAL_REVIEW", "step": 6, "at": "t"},
                {"from": "FINAL_REVIEW", "to": "FINAL_VALIDATE", "step": 7, "at": "t"},
                {"from": "FINAL_VALIDATE", "to": "DONE", "step": 8, "at": "t"},
            ],
        )
        code, message = validate(write_json(payload))
        self.assertEqual(code, 0, message)


class TransitionTableTests(unittest.TestCase):
    def test_transition_table_matches_spec(self):
        self.assertEqual(ai_state_check.TRANSITIONS, EXPECTED_TRANSITIONS)

    def test_transition_table_consistent_with_states(self):
        self.assertEqual(
            frozenset(ai_state_check.STATES),
            frozenset(ai_state_check.TRANSITIONS),
        )
        for src, dsts in ai_state_check.TRANSITIONS.items():
            self.assertIn(src, ai_state_check.STATES)
            for dst in dsts:
                self.assertIn(dst, ai_state_check.STATES)

    def test_every_non_terminal_state_has_at_least_one_exit(self):
        for src, dsts in ai_state_check.TRANSITIONS.items():
            if src in ("STOP", "DONE"):
                self.assertEqual(dsts, ())
            else:
                self.assertTrue(dsts, f"{src} must have outgoing transitions")


class ExitCodeTwoTests(unittest.TestCase):
    def test_non_json_content(self):
        path = Path(tempfile.mkstemp(suffix=".json")[1])
        path.write_text("{ this is not json", encoding="utf-8")
        code, message = validate(str(path))
        self.assertEqual(code, 2)
        self.assertIn("JSON", message)

    def test_missing_file(self):
        code, message = validate("/nonexistent/path/STATE.json")
        self.assertEqual(code, 2)
        self.assertIn("cannot read", message)

    def test_json_not_an_object(self):
        code, message = validate(write_json([1, 2, 3]))
        self.assertEqual(code, 1)
        self.assertIn("object", message)


class CliTests(unittest.TestCase):
    TOOL = str(ROOT / "tools" / "ai_state_check.py")

    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, self.TOOL, *args],
            capture_output=True,
            text=True,
        )

    def test_list_transitions(self):
        result = self.run_cli("--list-transitions")
        self.assertEqual(result.returncode, 0)
        for state in ai_state_check.STATES:
            self.assertIn(state, result.stdout)
        self.assertIn("PLAN ->", result.stdout)
        self.assertIn("IMPLEMENTATION_VALIDATE -> REVIEW, FIX, STOP", result.stdout)
        self.assertIn("STOP ->", result.stdout)
        self.assertIn("DONE ->", result.stdout)

    def test_cli_valid_file(self):
        result = self.run_cli(write_json(MINIMAL))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cli_missing_field_on_stderr(self):
        result = self.run_cli(write_json({}))
        self.assertEqual(result.returncode, 1)
        self.assertIn("task_id", result.stderr)

    def test_cli_non_json_exit_code(self):
        path = Path(tempfile.mkstemp(suffix=".json")[1])
        path.write_text("not json at all", encoding="utf-8")
        result = self.run_cli(str(path))
        self.assertEqual(result.returncode, 2)

    def test_cli_requires_state_file(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)

    def test_repo_state_json_is_valid(self):
        state_path = ROOT / ".ai" / "task" / "STATE.json"
        if not state_path.exists():
            self.skipTest("repo STATE.json not present")
        code, message = validate(str(state_path))
        self.assertEqual(code, 0, message)


if __name__ == "__main__":
    unittest.main()
