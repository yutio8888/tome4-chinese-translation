from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
FIXTURES = ROOT / "tests" / "i18n" / "fixtures" / "review_evidence"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import review_evidence


class ReviewEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        artifacts = ROOT / ".artifacts" / "i18n"
        artifacts.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="review-evidence-", dir=artifacts)
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        shutil.copytree(FIXTURES / ".ai", self.work / ".ai")
        self.good = json.loads((FIXTURES / "good-reconciliation.json").read_text(encoding="utf-8"))
        self.good_path = self.work / "good-reconciliation.json"
        self._write(self.good_path, self.good)

    @staticmethod
    def _write(path: Path, value: object) -> None:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _check(self, value: object) -> review_evidence.CheckResult:
        return review_evidence.check_reconciliation(value, root=self.work)

    def _entries(self) -> list[dict[str, object]]:
        return self.good["findings"]  # type: ignore[return-value]

    def test_good_sidecar_and_composite_collision_pass(self) -> None:
        result = self._check(self.good)
        self.assertEqual((result.outcome, result.exit_code), ("RECONCILIATION_VERIFIED", 0))

    def test_a_omission_is_reported_as_missing_composite_disposition(self) -> None:
        value = json.loads(json.dumps(self.good))
        value["findings"] = [entry for entry in value["findings"] if entry["id"] != "F2"]
        result = self._check(value)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("missing disposition", result.detail)
        self.assertIn("review-01.json/F2", result.detail)

    def test_a_prime_launder_by_include_requires_claim(self) -> None:
        value = json.loads(json.dumps(self.good))
        next(entry for entry in value["findings"] if entry["id"] == "F2")["claims"] = []
        result = self._check(value)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("non-empty claims", result.detail)

    def test_b_split_is_allowed_but_render_exposes_two_claims(self) -> None:
        value = json.loads(json.dumps(self.good))
        f1 = next(entry for entry in value["findings"] if entry["id"] == "F1" and entry["review"].endswith("review-01.json"))
        f1["claims"] = ["C1", "C2"]
        result = self._check(value)
        self.assertEqual(result.exit_code, 0)
        rendered = review_evidence.render(value, root=self.work)
        self.assertIn("review-01.json | F1", rendered)
        self.assertIn("C1, C2", rendered)

        omitted = json.loads(json.dumps(value))
        omitted["findings"] = [entry for entry in omitted["findings"] if entry["id"] != "F2"]
        self.assertEqual(self._check(omitted).exit_code, 1)

    def test_c_counts_are_derived_and_stored_counts_are_rejected(self) -> None:
        rendered = review_evidence.render(self.good, root=self.work)
        self.assertIn("cycle 0: 3 findings", rendered)
        self.assertIn("cycle 1: 2 findings", rendered)
        value = json.loads(json.dumps(self.good))
        value["counts"] = {"cycle0": 99}
        result = self._check(value)
        self.assertEqual(result.exit_code, 1)
        self.assertIn("exactly", result.detail)

    def test_d_duplicate_requires_reason_and_included_composite_target(self) -> None:
        cases = []
        no_reason = json.loads(json.dumps(self.good))
        duplicate = next(entry for entry in no_reason["findings"] if entry["disposition"] == "duplicate_of")
        duplicate.pop("reason")
        cases.append(("reason", no_reason))

        excluded_target = json.loads(json.dumps(self.good))
        duplicate = next(entry for entry in excluded_target["findings"] if entry["disposition"] == "duplicate_of")
        duplicate["duplicate_of"] = {"review": duplicate["review"].replace("review-02", "review-01"), "id": "F3"}
        cases.append(("excluded", excluded_target))

        unknown_target = json.loads(json.dumps(self.good))
        duplicate = next(entry for entry in unknown_target["findings"] if entry["disposition"] == "duplicate_of")
        duplicate["duplicate_of"]["id"] = "UNKNOWN"
        cases.append(("unknown", unknown_target))

        self_target = json.loads(json.dumps(self.good))
        duplicate = next(entry for entry in self_target["findings"] if entry["disposition"] == "duplicate_of")
        duplicate["duplicate_of"] = {"review": duplicate["review"], "id": duplicate["id"]}
        cases.append(("self", self_target))

        chain = json.loads(json.dumps(self.good))
        duplicate = next(entry for entry in chain["findings"] if entry["disposition"] == "duplicate_of")
        duplicate["duplicate_of"] = {"review": duplicate["review"].replace("review-02", "review-01"), "id": "F2"}
        f2 = next(entry for entry in chain["findings"] if entry["review"].endswith("review-01.json") and entry["id"] == "F2")
        f2["disposition"] = "duplicate_of"
        f2.pop("claims")
        f2["duplicate_of"] = {"review": f2["review"], "id": "F1"}
        f2["reason"] = "chain"
        cases.append(("chain", chain))

        for name, value in cases:
            with self.subTest(case=name):
                result = self._check(value)
                self.assertEqual(result.exit_code, 1)

        bare_id = json.loads(json.dumps(self.good))
        duplicate = next(entry for entry in bare_id["findings"] if entry["disposition"] == "duplicate_of")
        duplicate["duplicate_of"] = {"id": "F1"}
        self.assertEqual(self._check(bare_id).exit_code, 1)

    def test_empty_map_is_the_only_valid_empty_source_case(self) -> None:
        empty = {
            "schema_version": 1,
            "task_id": "empty",
            "source_reviews": [],
            "claims": [],
            "findings": [],
        }
        self.assertEqual(self._check(empty).exit_code, 0)
        nonempty = json.loads(json.dumps(empty))
        nonempty["claims"] = [{"id": "C1", "text": "orphan"}]
        self.assertEqual(self._check(nonempty).exit_code, 1)

    def test_inventory_preserves_raw_metadata_and_handles_old_record(self) -> None:
        old_path = self.work / ".ai" / "reviews" / "review-evidence-fixture" / "old.json"
        self._write(old_path, {"task_id": "old-record"})
        items = review_evidence.inventory([
            ".ai/reviews/review-evidence-fixture/review-01.json",
            old_path,
        ], root=self.work)
        self.assertEqual(items[0]["finding_count"], 3)
        self.assertEqual(items[0]["findings"][0]["reported_severity_raw"], "high")
        self.assertFalse(items[1]["has_findings_array"])
        self.assertEqual(items[1]["finding_count"], 0)
        self.assertIn("findings", items[1]["missing_fields"])

    def test_source_path_must_be_beneath_ai_reviews(self) -> None:
        value = json.loads(json.dumps(self.good))
        value["source_reviews"][0] = "good-reconciliation.json"
        result = self._check(value)
        self.assertEqual(result.exit_code, 1 if result.outcome == "NEW_CONTRACT_FAILED" else 2)

    def test_scope_audit_requires_composite_resolving_keys(self) -> None:
        audit = json.loads((FIXTURES / "scope-audit.json").read_text(encoding="utf-8"))
        self.assertEqual(review_evidence.check_audit(audit, root=self.work).exit_code, 0)
        bare = json.loads(json.dumps(audit))
        bare["calibration"] = {"F1": "keep"}
        self.assertEqual(review_evidence.check_audit(bare, root=self.work).exit_code, 1)
        unknown = json.loads(json.dumps(audit))
        unknown["calibration"] = {".ai/reviews/review-evidence-fixture/review-01.json / UNKNOWN": "keep"}
        self.assertEqual(review_evidence.check_audit(unknown, root=self.work).exit_code, 1)

    def test_cli_inventory_check_and_render_are_read_only_and_structured(self) -> None:
        source = self.work / ".ai" / "reviews" / "review-evidence-fixture" / "review-01.json"
        inventory = subprocess.run(
            [sys.executable, "-B", str(TOOLS / "review_evidence.py"), "inventory", str(source), "--root", str(self.work)],
            cwd=self.work, text=True, capture_output=True, check=False,
        )
        self.assertEqual(inventory.returncode, 0, inventory.stderr)
        self.assertEqual(json.loads(inventory.stdout)[0]["finding_count"], 3)
        check = subprocess.run(
            [
                sys.executable, "-B", str(TOOLS / "review_evidence.py"), "check",
                str(self.good_path), "--root", str(self.work),
            ],
            cwd=self.work, text=True, capture_output=True, check=False,
        )
        self.assertEqual(check.returncode, 0, check.stderr)

        bad = json.loads(json.dumps(self.good))
        bad["findings"] = [entry for entry in bad["findings"] if entry["id"] != "F2"]
        bad_path = self.work / "bad-reconciliation.json"
        self._write(bad_path, bad)
        failure = subprocess.run(
            [
                sys.executable, "-B", str(TOOLS / "review_evidence.py"), "check",
                str(bad_path), "--root", str(self.work),
            ],
            cwd=self.work, text=True, capture_output=True, check=False,
        )
        self.assertEqual(failure.returncode, 1, failure.stderr)

        rendered = subprocess.run(
            [
                sys.executable, "-B", str(TOOLS / "review_evidence.py"), "render",
                str(self.good_path), "--root", str(self.work),
            ],
            cwd=self.work, text=True, capture_output=True, check=False,
        )
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        self.assertIn("# Evidence reconciliation", rendered.stdout)


if __name__ == "__main__":
    unittest.main()
