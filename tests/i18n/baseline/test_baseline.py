"""Baseline contract tests (contract/0.1-rc3 §7): freeze/state/CI gate (G7),
the B1 evidence-identity rule (G11) and environment validation (§7.1)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.baseline import (  # noqa: E402
    BaselineState,
    ci_gate,
    compute_baseline_state,
    read_baseline,
    validate_baseline_environment,
    write_baseline,
)
from i18nlib.errors import ValidationError  # noqa: E402
from i18nlib.fingerprint import FindingRecord, finding_fingerprint  # noqa: E402
from i18nlib.lint import Issue  # noqa: E402

from tests.i18n.fingerprint.test_fingerprint import _record  # noqa: E402


def _sha(value: bytes) -> str:
    import hashlib

    return hashlib.sha256(value).hexdigest()


class BaselineLifecycleTests(unittest.TestCase):
    """G7: inject -> detect new -> freeze -> fix -> resolved."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-baseline-")
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _freeze(self, records, *, component: str = "tome", commit: str = "c1") -> None:
        write_baseline(
            manifest_root=self.root,
            component=component,
            translation_commit=commit,
            source_snapshot_sha256="snap-1",
            engine_commit="e" * 40,
            extractor_commit="x" * 40,
            rules_registry_sha256="r" * 64,
            slot_registry_sha256="s" * 64,
            records=records,
        )

    def test_g7_new_legacy_resolved(self) -> None:
        defect = _record(evidence_key="conv:d|", tu_uid="TU-DEFECT")
        clean = _record(evidence_key="conv:d|d", tu_uid="TU-CLEAN")
        self._freeze([defect, clean])

        # After freeze: everything is legacy, nothing new.
        baseline = read_baseline(self.root, component="tome", translation_commit="c1")
        state = compute_baseline_state(baseline, [defect, clean])
        self.assertEqual(len(state.new), 0)
        self.assertEqual(len(state.legacy), 2)
        self.assertEqual(len(state.resolved), 0)
        passed, gate = ci_gate(state)
        self.assertTrue(passed)
        self.assertEqual(gate["legacy_errors"], 2)

        # A newly injected defect is NEW.
        injected = _record(evidence_key="conv:s|s", tu_uid="TU-INJECTED")
        state = compute_baseline_state(baseline, [defect, clean, injected])
        passed, gate = ci_gate(state)
        self.assertFalse(passed)
        self.assertEqual(gate["new_errors"], 1)

        # Fixing the defect removes the finding entirely -> resolved.
        state = compute_baseline_state(baseline, [clean])
        passed, gate = ci_gate(state)
        self.assertTrue(passed)
        self.assertEqual(gate["resolved"], 1)

    def test_g11_b1_same_evidence_stays_legacy(self) -> None:
        defect = _record(evidence_key="conv:d|", tu_uid="TU-DEFECT")
        self._freeze([defect])
        baseline = read_baseline(self.root, component="tome", translation_commit="c1")
        # Translator rewrote the wording but did not fix the %d: the
        # evidence identity is unchanged -> same fingerprint -> legacy.
        reworded = _record(
            evidence_key="conv:d|",
            tu_uid="TU-DEFECT",
            issue=Issue("error", "format-mismatch", "rewritten", "p.lua", 1, "e"),
        )
        self.assertEqual(defect.fingerprint, reworded.fingerprint)
        state = compute_baseline_state(
            baseline, [reworded], touched_tu_uids={"TU-DEFECT"}
        )
        self.assertEqual(len(state.new), 0)
        self.assertEqual(len(state.legacy), 1)
        # B1 advisory: legacy finding on a touched TU is reported, not upgraded.
        self.assertEqual(state.legacy_on_touched_tu, (defect.fingerprint,))

    def test_environment_validation(self) -> None:
        self._freeze([])
        baseline = read_baseline(self.root, component="tome", translation_commit="c1")
        validate_baseline_environment(
            baseline,
            source_snapshot_sha256="snap-1",
            engine_commit="e" * 40,
            extractor_commit="x" * 40,
            rules_registry_sha256="r" * 64,
            slot_registry_sha256="s" * 64,
        )
        with self.assertRaises(ValidationError):
            validate_baseline_environment(
                baseline,
                source_snapshot_sha256="snap-OTHER",
                engine_commit="e" * 40,
                extractor_commit="x" * 40,
                rules_registry_sha256="r" * 64,
                slot_registry_sha256="s" * 64,
            )

    def test_duplicate_fingerprint_rejected(self) -> None:
        record = _record()
        with self.assertRaises(ValidationError):
            self._freeze([record, record])

    def test_baseline_bytes_deterministic(self) -> None:
        records = [_record(tu_uid="A"), _record(tu_uid="B")]
        self._freeze(records)
        baseline = read_baseline(self.root, component="tome", translation_commit="c1")
        self.assertEqual(len(baseline.entries), 2)
        fingerprints = list(baseline.entries)
        self.assertEqual(fingerprints, sorted(fingerprints))


if __name__ == "__main__":
    unittest.main()


class FrozenMetaFormatTests(unittest.TestCase):
    """§7.1: the frozen meta.json carries exactly the contract fields."""

    def test_meta_has_exact_contract_keys(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="tome4-i18n-meta-") as temporary:
            root = Path(temporary)
            write_baseline(
                manifest_root=root,
                component="tome",
                translation_commit="c1",
                source_snapshot_sha256="snap-1",
                engine_commit="e" * 40,
                extractor_commit="x" * 40,
                rules_registry_sha256="r" * 64,
                slot_registry_sha256="s" * 64,
                records=[],
            )
            import json

            meta = json.loads(
                (root / "i18n" / "baselines" / "tome-c1.meta.json").read_text()
            )
            self.assertEqual(
                set(meta),
                {
                    "schema_version",
                    "component",
                    "translation_commit",
                    "source_snapshot_sha256",
                    "engine_commit",
                    "extractor_commit",
                    "rules_registry_sha256",
                    "slot_registry_sha256",
                },
            )
            baseline = read_baseline(
                root, component="tome", translation_commit="c1"
            )
            self.assertEqual(len(baseline.sha256), 64)
            self.assertEqual(
                baseline.sha256,
                __import__("hashlib").sha256(
                    (root / "i18n" / "baselines" / "tome-c1.jsonl").read_bytes()
                ).hexdigest(),
            )
