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


class MetaIdentityFailClosedTests(unittest.TestCase):
    """read_baseline validates meta identity (§7.1): fail-closed on a corrupt,
    misfiled, or half-set baseline so it can never reach a CI judgement."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-meta-id-")
        self.root = Path(self.temporary.name)
        write_baseline(
            manifest_root=self.root,
            component="tome",
            translation_commit="c1",
            source_snapshot_sha256="snap-1",
            engine_commit="e" * 40,
            extractor_commit="x" * 40,
            rules_registry_sha256="r" * 64,
            slot_registry_sha256="s" * 64,
            records=[],
        )
        self.jsonl = self.root / "i18n" / "baselines" / "tome-c1.jsonl"
        self.meta = self.root / "i18n" / "baselines" / "tome-c1.meta.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_component_mismatch_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            read_baseline(self.root, component="ashes", translation_commit="c1")

    def test_translation_commit_mismatch_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            read_baseline(self.root, component="tome", translation_commit="c2")

    def _rewrite_meta(self, patched: dict) -> None:
        import json

        self.meta.write_text(
            json.dumps(patched, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        )

    def test_bad_schema_version_rejected(self) -> None:
        import json

        meta = json.loads(self.meta.read_text())
        meta["schema_version"] = 2
        self._rewrite_meta(meta)
        with self.assertRaises(ValidationError):
            read_baseline(self.root, component="tome", translation_commit="c1")

    def test_extra_meta_key_rejected(self) -> None:
        import json

        meta = json.loads(self.meta.read_text())
        meta["rogue_field"] = "x"
        self._rewrite_meta(meta)
        with self.assertRaises(ValidationError):
            read_baseline(self.root, component="tome", translation_commit="c1")

    def test_missing_meta_key_rejected(self) -> None:
        import json

        meta = json.loads(self.meta.read_text())
        del meta["source_snapshot_sha256"]
        self._rewrite_meta(meta)
        with self.assertRaises(ValidationError):
            read_baseline(self.root, component="tome", translation_commit="c1")

    def test_half_set_missing_meta_rejected(self) -> None:
        self.meta.unlink()
        with self.assertRaises(ValidationError):
            read_baseline(self.root, component="tome", translation_commit="c1")

    def test_half_set_missing_jsonl_rejected(self) -> None:
        self.jsonl.unlink()
        with self.assertRaises(ValidationError):
            read_baseline(self.root, component="tome", translation_commit="c1")


class NoClobberFreezeTests(unittest.TestCase):
    """§7.1 no-clobber: a frozen baseline is never overwritten. A re-freeze
    with byte-identical content is idempotent; differing content is rejected."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-noclobber-")
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

    def test_identical_refreeze_is_idempotent(self) -> None:
        record = _record(tu_uid="A")
        self._freeze([record])
        first = (self.root / "i18n" / "baselines" / "tome-c1.jsonl").read_bytes()
        # Re-freeze identical content: must not raise and must not rewrite.
        self._freeze([record])
        second = (self.root / "i18n" / "baselines" / "tome-c1.jsonl").read_bytes()
        self.assertEqual(first, second)
        baseline = read_baseline(self.root, component="tome", translation_commit="c1")
        self.assertEqual(len(baseline.entries), 1)

    def test_differing_refreeze_rejected(self) -> None:
        self._freeze([_record(tu_uid="A")])
        with self.assertRaises(ValidationError):
            self._freeze(
                [_record(evidence_key="conv:d|d", tu_uid="B")]
            )

    def test_half_set_existing_rejected_as_corrupt(self) -> None:
        self._freeze([_record(tu_uid="A")])
        # Leave only the meta file (simulate a half-written state).
        (self.root / "i18n" / "baselines" / "tome-c1.jsonl").unlink()
        with self.assertRaises(ValidationError):
            self._freeze([_record(tu_uid="A")])


def _make_git_repo() -> tuple[tempfile.TemporaryDirectory, Path, str]:
    import subprocess

    temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-prov-")
    repository = Path(temporary.name)
    subprocess.run(["git", "init", "-q", str(repository)], check=True)
    subprocess.run(
        ["git", "-C", str(repository), "config", "user.name", "test"], check=True
    )
    subprocess.run(
        ["git", "-C", str(repository), "config", "user.email", "t@x.invalid"],
        check=True,
    )
    (repository / "f.txt").write_text("v1\n")
    subprocess.run(["git", "-C", str(repository), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(repository), "commit", "-q", "-m", "first"], check=True
    )
    head = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return temporary, repository, head


def _git(repo: Path, *arguments: str):
    import subprocess

    return subprocess.run(
        ["git", "-C", str(repo), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


class FreezeProvenanceTests(unittest.TestCase):
    """`baseline freeze` binds --commit to the translation repo HEAD and
    requires a clean tracked/index worktree (contract §7.1 provenance)."""

    def setUp(self) -> None:
        from types import SimpleNamespace

        from i18nlib.cli import _verify_freeze_provenance  # noqa: F401

        self.temporary, self.repository, self.head = _make_git_repo()
        self.manifest = SimpleNamespace(root=self.repository)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_head_commit_accepted(self) -> None:
        from i18nlib.cli import _verify_freeze_provenance

        self.assertEqual(
            _verify_freeze_provenance(self.manifest, self.head), self.head
        )

    def test_short_sha_canonicalized_to_head(self) -> None:
        from i18nlib.cli import _verify_freeze_provenance

        self.assertEqual(
            _verify_freeze_provenance(self.manifest, self.head[:12]), self.head
        )

    def test_non_head_commit_rejected(self) -> None:
        from i18nlib.errors import ContractError

        from i18nlib.cli import _verify_freeze_provenance

        # Create a second commit so the parent is no longer HEAD.
        (self.repository / "f.txt").write_text("v2\n")
        _git(self.repository, "add", "-A")
        _git(self.repository, "commit", "-q", "-m", "second")
        parent = _git(self.repository, "rev-parse", "HEAD~1").stdout.strip()
        with self.assertRaises(ContractError):
            _verify_freeze_provenance(self.manifest, parent)

    def test_dirty_worktree_rejected(self) -> None:
        from i18nlib.errors import ContractError

        from i18nlib.cli import _verify_freeze_provenance

        (self.repository / "f.txt").write_text("dirty\n")
        with self.assertRaises(ContractError):
            _verify_freeze_provenance(self.manifest, self.head)

    def test_unresolvable_commit_rejected(self) -> None:
        from i18nlib.errors import ContractError

        from i18nlib.cli import _verify_freeze_provenance

        with self.assertRaises(ContractError):
            _verify_freeze_provenance(self.manifest, "no-such-commit")


class RequiredBaselinesLoaderTests(unittest.TestCase):
    """_load_required_baselines: only indexable components must have a
    baseline; missing/corrupt is fail-closed; an empty valid set fails."""

    def setUp(self) -> None:
        from types import SimpleNamespace

        self.temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-loader-")
        self.root = Path(self.temporary.name)
        write_baseline(
            manifest_root=self.root,
            component="tome",
            translation_commit="c1",
            source_snapshot_sha256="snap-1",
            engine_commit="e" * 40,
            extractor_commit="x" * 40,
            rules_registry_sha256="r" * 64,
            slot_registry_sha256="s" * 64,
            records=[],
        )
        self.manifest = SimpleNamespace(root=self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _comp(self, component_id):
        from types import SimpleNamespace

        return SimpleNamespace(id=component_id)

    def test_indexed_component_loaded(self) -> None:
        from i18nlib.cli import _load_required_baselines

        baselines, skipped = _load_required_baselines(
            self.manifest,
            components=[self._comp("tome")],
            indexes={"tome": object()},
            commit="c1",
        )
        self.assertIn("tome", baselines)
        self.assertEqual(skipped, [])

    def test_non_indexed_component_allowed_as_skipped(self) -> None:
        from i18nlib.cli import _load_required_baselines

        baselines, skipped = _load_required_baselines(
            self.manifest,
            components=[self._comp("tome"), self._comp("noroot")],
            indexes={"tome": object()},
            commit="c1",
        )
        self.assertEqual(set(baselines), {"tome"})
        self.assertEqual([item["component"] for item in skipped], ["noroot"])

    def test_empty_required_set_rejected(self) -> None:
        from i18nlib.cli import _load_required_baselines

        with self.assertRaises(ValidationError):
            _load_required_baselines(
                self.manifest,
                components=[self._comp("noroot")],
                indexes={},
                commit="c1",
            )

    def test_indexed_but_missing_baseline_fail_closed(self) -> None:
        from i18nlib.cli import _load_required_baselines

        with self.assertRaises(ValidationError):
            _load_required_baselines(
                self.manifest,
                components=[self._comp("tome")],
                indexes={"tome": object()},
                commit="never-frozen",
            )

    def test_indexed_but_corrupt_baseline_fail_closed(self) -> None:
        from i18nlib.cli import _load_required_baselines

        (self.root / "i18n" / "baselines" / "tome-c1.jsonl").unlink()
        with self.assertRaises(ValidationError):
            _load_required_baselines(
                self.manifest,
                components=[self._comp("tome")],
                indexes={"tome": object()},
                commit="c1",
            )
