import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "review_usage", ROOT / "tools/orchestration/review_usage.py")
usage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(usage)


def record(request_id, role="CHILD", *, batch="batch-1", phase="review",
           counter_scope="request", input_tokens=100, cached=None, output_tokens=10,
           start="2026-09-19T00:00:00Z", end="2026-09-19T00:00:10Z"):
    return {
        "request_id": request_id,
        "role": role,
        "batch": batch,
        "phase": phase,
        "counter_scope": counter_scope,
        "usage": {"input_tokens": input_tokens, "cached_input": cached,
                  "output_tokens": output_tokens},
        "interval": None if start is None else {"started_at": start, "ended_at": end},
    }


def document(*records):
    return {"schema": usage.SCHEMA, "records": list(records)}


class ReviewUsageTests(unittest.TestCase):
    def test_groups_orchestrator_and_all_children_by_batch_phase(self):
        records = usage.validate(document(
            record("o", "ORCHESTRATOR", input_tokens=20),
            record("c1", phase="surface", input_tokens=30),
            record("c2", phase="contextual", input_tokens=40)))
        result = usage.report(records)
        self.assertEqual(result["role_groups"]["ORCHESTRATOR"]["records"], 1)
        self.assertEqual(result["role_groups"]["CHILDREN"]["records"], 2)
        self.assertEqual([(item["batch"], item["phase"]) for item in result["scopes"]],
                         [("batch-1", "contextual"), ("batch-1", "review"),
                          ("batch-1", "surface")])

    def test_duplicate_request_identity_is_rejected(self):
        with self.assertRaisesRegex(usage.UsageError, "duplicate request_id"):
            usage.validate(document(record("same"), record("same", "ORCHESTRATOR")))

    def test_missing_counters_remain_unknown_not_zero(self):
        result = usage.report(usage.validate(document(
            record("unknown", input_tokens=None, output_tokens=None, cached=None))))
        measured = result["role_groups"]["CHILDREN"]["measurements"]["request"]
        self.assertEqual(measured["input_tokens"],
                         {"known_sum": None, "known_records": 0, "unknown_records": 1})
        self.assertIsNone(measured["output_tokens"]["known_sum"])
        self.assertEqual(measured["cached_input_tokens"]["unknown_records"], 1)

    def test_invalid_bool_and_negative_counters_are_rejected(self):
        for value in (True, False, -1):
            with self.subTest(value=value), self.assertRaises(usage.UsageError):
                usage.validate(document(record("bad", input_tokens=value)))
        with self.assertRaises(usage.UsageError):
            usage.validate(document(record("bad-cache", cached={
                "tokens": True, "relationship": "subset_of_input"})))

    def test_cached_subset_and_separate_measurement_stay_distinct(self):
        result = usage.report(usage.validate(document(
            record("subset", input_tokens=100,
                   cached={"tokens": 40, "relationship": "subset_of_input"}),
            record("separate", input_tokens=80,
                   cached={"tokens": 90, "relationship": "separately_measured"}))))
        measured = result["role_groups"]["CHILDREN"]["measurements"]["request"]
        self.assertEqual(measured["cached_input_tokens"]["subset_of_input"]["known_sum"], 40)
        self.assertEqual(measured["cached_input_tokens"]["separately_measured"]["known_sum"], 90)
        self.assertEqual(measured["input_excluding_cached_subset_tokens"]["known_sum"], 60)
        self.assertEqual(measured["input_excluding_cached_subset_tokens"]["unknown_records"], 1)
        with self.assertRaisesRegex(usage.UsageError, "subset exceeds"):
            usage.validate(document(record("impossible", input_tokens=10,
                cached={"tokens": 11, "relationship": "subset_of_input"})))

    def test_overlapping_child_intervals_use_span_not_sum(self):
        result = usage.report(usage.validate(document(
            record("a", start="2026-09-19T00:00:00Z", end="2026-09-19T00:00:10Z"),
            record("b", start="2026-09-19T00:00:05Z", end="2026-09-19T00:00:15Z"))))
        elapsed = result["role_groups"]["CHILDREN"]["elapsed"]
        self.assertEqual(elapsed["observed_span_ms"], 15000)
        self.assertNotEqual(elapsed["observed_span_ms"], 20000)

    def test_last_usage_snapshot_is_separate_and_cli_is_stdout_only(self):
        doc = document(record("snapshot", counter_scope="last_usage_snapshot"))
        result = usage.report(usage.validate(doc))
        group = result["role_groups"]["CHILDREN"]["measurements"]
        self.assertEqual(group["request"]["records"], 0)
        self.assertEqual(group["last_usage_snapshot"]["records"], 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "explicit.json"
            path.write_text(json.dumps(doc), encoding="utf-8")
            before = path.read_bytes()
            process = subprocess.run(
                [sys.executable, "-B", str(ROOT / "tools/orchestration/review_usage.py"), str(path)],
                capture_output=True, text=True, timeout=10)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(json.loads(process.stdout)["records"], 1)

    def test_loader_rejects_nonregular_and_reads_with_actual_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.json"
            target.write_text(json.dumps(document()), encoding="utf-8")
            link = root / "link.json"
            link.symlink_to(target)
            with self.assertRaisesRegex(usage.UsageError, "regular file"):
                usage.load(link)
            oversized = root / "oversized.json"
            oversized.write_bytes(b"12345")
            with patch.object(usage, "MAX_BYTES", 4), self.assertRaisesRegex(
                    usage.UsageError, "exceeds"):
                usage.load(oversized)


if __name__ == "__main__":
    unittest.main()
