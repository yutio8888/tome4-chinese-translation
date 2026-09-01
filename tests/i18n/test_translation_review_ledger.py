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
import surface_screen_result_check as check
import translation_review_ledger as ledger


def identity(byte: str) -> str:
    return (byte * 64)


LOGICAL = identity("a")
REVISION_1 = identity("b")
REVISION_2 = identity("c")
OTHER_LOGICAL = identity("d")
OTHER_LOGICAL_REVISION = identity("e")
MIGRATED_LOGICAL = identity("f")
MIGRATED_REVISION = identity("0")
THIRD_LOGICAL = identity("9")


def record(
    to_state: str,
    *,
    from_state: str | None = None,
    logical: str = LOGICAL,
    revision: str = REVISION_1,
    parent: str | None = None,
    migration: str | None = None,
    reason_code: str = "revision_frozen",
    provenance_kind: str = "revision_freeze_record",
    provenance_sha256: str | None = None,
    recorded_by: str = "ORCHESTRATOR",
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "logical_entry_identity": logical,
        "entry_revision_identity": revision,
        "from_state": from_state,
        "to_state": to_state,
        "reason_code": reason_code,
        "provenance": {
            "kind": provenance_kind,
            "sha256": provenance_sha256 or ("2" * 64),
        },
        "recorded_by": recorded_by,
        "recorded_at": "2026-08-29T12:00:00Z",
        "parent_revision_identity": parent,
        "migration_from_logical_entry_identity": migration,
    }


HAPPY_PATH = [
    record("queued"),
    record("deterministic_pass", from_state="queued",
           reason_code="deterministic_layer_passed",
           provenance_kind="deterministic_layer"),
    record("screened", from_state="deterministic_pass",
           reason_code="surface_screen_completed", provenance_kind="surface_handoff"),
    record("deep_queued", from_state="screened",
           reason_code="surface_ok_selected", provenance_kind="surface_handoff"),
    record("deep_reviewed", from_state="deep_queued",
           reason_code="deep_review_completed", provenance_kind="deep_handoff"),
    record("revalidated", from_state="deep_reviewed",
           reason_code="deep_ok_revalidated", provenance_kind="revalidation_record"),
    record("closed", from_state="revalidated",
           reason_code="revision_closed", provenance_kind="revision_freeze_record"),
]


class TranslationReviewLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        (ROOT / ".artifacts" / "i18n").mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".artifacts" / "i18n")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def _write(self, records: list[dict[str, object]]) -> Path:
        path = self.root / "TRANSLATION-REVIEW-LEDGER.jsonl"
        path.write_bytes(b"".join(
            check.canonical_bytes(item) + b"\n" for item in records
        ))
        return path

    def test_happy_path_and_named_states(self) -> None:
        path = self._write(HAPPY_PATH)
        summary = ledger.summarize(ledger.parse_ledger_bytes(path.read_bytes()))
        self.assertEqual(summary["state_counts"], {"closed": 1})
        self.assertEqual(summary["deep_reviewed"], 1)
        self.assertEqual(summary["deferred_sampling_queued"], 0)

    def test_deferred_is_not_deep_reviewed(self) -> None:
        records = [
            record("queued"),
            record("deterministic_pass", from_state="queued",
                   reason_code="deterministic_layer_passed",
                   provenance_kind="deterministic_layer"),
            record("screened", from_state="deterministic_pass",
                   reason_code="surface_screen_completed", provenance_kind="surface_handoff"),
            record("sampling_queued", from_state="screened",
                   reason_code="surface_ok_deferred", provenance_kind="surface_handoff"),
        ]
        path = self._write(records)
        summary = ledger.summarize(ledger.parse_ledger_bytes(path.read_bytes()))
        self.assertEqual(summary["state_counts"], {"sampling_queued": 1})
        self.assertEqual(summary["deep_reviewed"], 0)
        self.assertEqual(summary["deferred_sampling_queued"], 1)
        self.assertTrue(summary["deferred_is_not_deep_reviewed"])

    def test_confirmed_repair_and_reopen_paths(self) -> None:
        records = [
            record("queued"),
            record("deterministic_pass", from_state="queued",
                   reason_code="deterministic_layer_passed",
                   provenance_kind="deterministic_layer"),
            record("screened", from_state="deterministic_pass",
                   reason_code="surface_screen_completed", provenance_kind="surface_handoff"),
            record("deep_queued", from_state="screened",
                   reason_code="surface_issue", provenance_kind="surface_handoff"),
            record("deep_reviewed", from_state="deep_queued",
                   reason_code="deep_review_completed", provenance_kind="deep_handoff"),
            record("finding_observed", from_state="deep_reviewed",
                   reason_code="deep_issue_observed", provenance_kind="deep_handoff"),
            record("adjudication", from_state="finding_observed",
                   reason_code="finding_observed", provenance_kind="adjudication_record"),
            record("adjudication", from_state="adjudication",
                   reason_code="re_adjudication_pending_evidence",
                   provenance_kind="adjudication_record"),
            record("fixed", from_state="adjudication",
                   reason_code="repair_confirmed_applied", provenance_kind="repair_handoff"),
            record("revalidated", from_state="fixed",
                   reason_code="repair_revalidated", provenance_kind="revalidation_record"),
            record("closed", from_state="revalidated",
                   reason_code="revision_closed", provenance_kind="revision_freeze_record"),
            record("reopened", from_state="closed",
                   reason_code="new_fidelity_evidence",
                   provenance_kind="reopen_evidence_record"),
            record("deep_queued", from_state="reopened",
                   reason_code="reopen_dispatched", provenance_kind="deep_handoff"),
        ]
        path = self._write(records)
        ledger.replay(ledger.parse_ledger_bytes(path.read_bytes()))

    def test_invalidation_creates_new_revision_with_lineage(self) -> None:
        records = HAPPY_PATH[:4] + [
            record("invalidated", from_state="deep_queued",
                   reason_code="source_changed", provenance_kind="identity_snapshot"),
            record("queued", revision=REVISION_2, parent=REVISION_1),
            record("deterministic_pass", from_state="queued", revision=REVISION_2,
                   reason_code="deterministic_layer_passed",
                   provenance_kind="deterministic_layer"),
            record("screened", from_state="deterministic_pass", revision=REVISION_2,
                   reason_code="surface_screen_completed", provenance_kind="surface_handoff"),
        ]
        path = self._write(records)
        ledger.replay(ledger.parse_ledger_bytes(path.read_bytes()))

    def test_closed_revision_identity_invalidation_spawns_new_revision(self) -> None:
        records = HAPPY_PATH + [
            record("invalidated", from_state="closed",
                   reason_code="terminology_snapshot_changed",
                   provenance_kind="identity_snapshot"),
            record("queued", revision=REVISION_2, parent=REVISION_1),
        ]
        path = self._write(records)
        ledger.replay(ledger.parse_ledger_bytes(path.read_bytes()))

    def test_preference_only_reopen_of_closed_revision_is_forbidden(self) -> None:
        # A free-text/preference reopen of a closed revision fails closed even
        # when dressed as a machine cause, because closed->reopened only
        # accepts named new-evidence codes.
        records = HAPPY_PATH + [
            record("reopened", from_state="closed", reason_code="new_fidelity_evidence",
                   provenance_kind="reopen_evidence_record"),
            record("deep_queued", from_state="reopened",
                   reason_code="reopen_dispatched", provenance_kind="deep_handoff"),
            record("closed", from_state="deep_queued", reason_code="revision_closed"),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(records)))
        preference = HAPPY_PATH + [
            record("reopened", from_state="closed", reason_code="surface_issue",
                   provenance_kind="reopen_evidence_record"),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(preference)))

    def test_migration_edge_for_new_logical_identity(self) -> None:
        # A migration edge must cite a logical-identity change cause.
        old = [
            record("queued", logical=OTHER_LOGICAL, revision=OTHER_LOGICAL_REVISION),
            record("invalidated", from_state="queued", logical=OTHER_LOGICAL,
                   revision=OTHER_LOGICAL_REVISION, reason_code="call_locator_changed",
                   provenance_kind="identity_snapshot"),
        ]
        records = old + [
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=OTHER_LOGICAL),
        ]
        path = self._write(records)
        ledger.replay(ledger.parse_ledger_bytes(path.read_bytes()))

    def test_migration_edge_requires_logical_cause(self) -> None:
        # C2-06: source_changed is a revision-level cause; the same logical
        # identity continues under a new revision, so it cannot back a
        # migration edge.
        records = [
            record("queued", logical=OTHER_LOGICAL, revision=OTHER_LOGICAL_REVISION),
            record("invalidated", from_state="queued", logical=OTHER_LOGICAL,
                   revision=OTHER_LOGICAL_REVISION, reason_code="source_changed",
                   provenance_kind="identity_snapshot"),
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=OTHER_LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(records)))

    def test_logical_migration_requires_adjacent_successor_edge(self) -> None:
        # C2-06: a logical-migration invalidation must be followed immediately
        # by the successor revision carrying its migration edge.
        def invalidation(logical: str, revision: str) -> dict[str, object]:
            return record("invalidated", from_state="queued", logical=logical,
                          revision=revision, reason_code="source_tag_changed",
                          provenance_kind="identity_snapshot")

        # Closed logical migration: invalidate then immediately migrate.
        closed = [
            record("queued", logical=OTHER_LOGICAL, revision=OTHER_LOGICAL_REVISION),
            invalidation(OTHER_LOGICAL, OTHER_LOGICAL_REVISION),
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=OTHER_LOGICAL),
        ]
        ledger.replay(json.loads(json.dumps(closed)))
        # Successor without the migration edge.
        without_edge = closed[:2] + [
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(without_edge)))
        # Any other record before the successor breaks adjacency.
        intervening = closed[:2] + [
            record("queued", logical=THIRD_LOGICAL, revision=identity("7")),
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=OTHER_LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(intervening)))
        # Edge must cite the pending migration, not another logical identity.
        wrong_target = closed[:2] + [
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=THIRD_LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(wrong_target)))

    def test_logical_migration_edge_is_single_consumption_and_fork_proof(self) -> None:
        # C3-04: a logical-migration invalidation opens exactly one
        # single-consumption pending edge.  After one successor consumes it,
        # the same source can never back another migration (fork) and a
        # logical identity that already migrated away cannot spawn further
        # revisions without consuming a new pending edge (resurrection).
        invalidation = [
            record("queued", logical=OTHER_LOGICAL, revision=OTHER_LOGICAL_REVISION),
            record("invalidated", from_state="queued", logical=OTHER_LOGICAL,
                   revision=OTHER_LOGICAL_REVISION, reason_code="call_locator_changed",
                   provenance_kind="identity_snapshot"),
        ]
        fork = invalidation + [
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=OTHER_LOGICAL),
            record("queued", logical=THIRD_LOGICAL, revision=identity("7"),
                   migration=OTHER_LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError) as caught:
            ledger.replay(json.loads(json.dumps(fork)))
        self.assertIn("already consumed", str(caught.exception))
        resurrection = invalidation + [
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=OTHER_LOGICAL),
            record("queued", logical=OTHER_LOGICAL, revision=identity("8"),
                   parent=OTHER_LOGICAL_REVISION),
        ]
        with self.assertRaises(ledger.LedgerError) as caught:
            ledger.replay(json.loads(json.dumps(resurrection)))
        self.assertIn("already migrated away", str(caught.exception))
        self_migration = invalidation + [
            record("queued", logical=OTHER_LOGICAL, revision=identity("7"),
                   parent=OTHER_LOGICAL_REVISION, migration=OTHER_LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(self_migration)))

    def test_truthful_migration_back_to_a_used_logical_identity_is_legal(self) -> None:
        # C3-04: a locator that reverts to a prior value truthfully migrates
        # back to the previously used logical identity; the revert revision
        # must be the adjacent successor carrying the different pending
        # migration source, and the resulting history stays single-active.
        original = [
            record("queued", logical=OTHER_LOGICAL, revision=OTHER_LOGICAL_REVISION),
            record("invalidated", from_state="queued", logical=OTHER_LOGICAL,
                   revision=OTHER_LOGICAL_REVISION, reason_code="call_locator_changed",
                   provenance_kind="identity_snapshot"),
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=OTHER_LOGICAL),
            record("invalidated", from_state="queued", logical=MIGRATED_LOGICAL,
                   revision=MIGRATED_REVISION, reason_code="call_locator_changed",
                   provenance_kind="identity_snapshot"),
            record("queued", logical=OTHER_LOGICAL, revision=identity("7"),
                   parent=OTHER_LOGICAL_REVISION, migration=MIGRATED_LOGICAL),
        ]
        revisions = ledger.replay(json.loads(json.dumps(original)))
        self.assertEqual(
            list(revisions[OTHER_LOGICAL].values()), ["invalidated", "queued"]
        )
        self.assertEqual(list(revisions[OTHER_LOGICAL])[-1], identity("7"))
        self.assertEqual(list(revisions[MIGRATED_LOGICAL].values()), ["invalidated"])
        # The consumed source can never back a later migration.
        fork_after_revert = original + [
            record("queued", logical=THIRD_LOGICAL, revision=identity("3"),
                   migration=MIGRATED_LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError) as caught:
            ledger.replay(json.loads(json.dumps(fork_after_revert)))
        self.assertIn("already consumed", str(caught.exception))
        # A revert edge is only legal adjacent to its pending source.
        non_adjacent_revert = original[:4] + [
            record("queued", logical=THIRD_LOGICAL, revision=identity("3")),
            record("queued", logical=OTHER_LOGICAL, revision=identity("7"),
                   parent=OTHER_LOGICAL_REVISION, migration=MIGRATED_LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(non_adjacent_revert)))

    def test_revival_clears_the_consumed_away_marker_for_later_bumps(self) -> None:
        # C4-04: after a truthful migration edge revives a previously used
        # logical identity, its consumed-away marker is cleared, so later
        # ordinary invalidations can spawn ordinary revision bumps under it,
        # and a later logical invalidation can back a fresh migration edge;
        # duplicate/fork citation of the consumed source stays rejected.
        revived = [
            record("queued", logical=OTHER_LOGICAL, revision=OTHER_LOGICAL_REVISION),
            record("invalidated", from_state="queued", logical=OTHER_LOGICAL,
                   revision=OTHER_LOGICAL_REVISION, reason_code="call_locator_changed",
                   provenance_kind="identity_snapshot"),
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=OTHER_LOGICAL),
            record("invalidated", from_state="queued", logical=MIGRATED_LOGICAL,
                   revision=MIGRATED_REVISION, reason_code="call_locator_changed",
                   provenance_kind="identity_snapshot"),
            record("queued", logical=OTHER_LOGICAL, revision=identity("7"),
                   parent=OTHER_LOGICAL_REVISION, migration=MIGRATED_LOGICAL),
            # Ordinary (non-logical) invalidation of the revived identity.
            record("invalidated", from_state="queued", logical=OTHER_LOGICAL,
                   revision=identity("7"), reason_code="source_changed",
                   provenance_kind="identity_snapshot"),
        ]
        # Before the fix this ordinary bump was rejected as a resurrection
        # fork even though the revival consumed a fresh pending edge.
        ordinary_bump = revived + [
            record("queued", logical=OTHER_LOGICAL, revision=identity("8"),
                   parent=identity("7")),
        ]
        revisions = ledger.replay(json.loads(json.dumps(ordinary_bump)))
        # OTHER_LOGICAL_REVISION: invalidated; identity("7"): revived queued,
        # then ordinarily invalidated; identity("8"): ordinary bump queued.
        self.assertEqual(
            list(revisions[OTHER_LOGICAL].values()),
            ["invalidated", "invalidated", "queued"],
        )
        self.assertEqual(list(revisions[OTHER_LOGICAL])[-1], identity("8"))
        # The still-consumed source stays fork/reuse-rejected.
        fork_after_revival = revived + [
            record("queued", logical=THIRD_LOGICAL, revision=identity("3"),
                   migration=MIGRATED_LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError) as caught:
            ledger.replay(json.loads(json.dumps(fork_after_revival)))
        self.assertIn("already consumed", str(caught.exception))
        resurrection_fork = revived + [
            record("queued", logical=MIGRATED_LOGICAL, revision=identity("4"),
                   parent=MIGRATED_REVISION),
        ]
        with self.assertRaises(ledger.LedgerError) as caught:
            ledger.replay(json.loads(json.dumps(resurrection_fork)))
        self.assertIn("fork", str(caught.exception))
        # A later logical invalidation of the revived identity can back a
        # fresh migration edge to a new logical identity.
        remarriage = revived + [
            record("queued", logical=OTHER_LOGICAL, revision=identity("8"),
                   parent=identity("7")),
            record("invalidated", from_state="queued", logical=OTHER_LOGICAL,
                   revision=identity("8"), reason_code="source_tag_changed",
                   provenance_kind="identity_snapshot"),
            record("queued", logical=THIRD_LOGICAL, revision=identity("3"),
                   migration=OTHER_LOGICAL),
        ]
        revisions = ledger.replay(json.loads(json.dumps(remarriage)))
        self.assertEqual(list(revisions[THIRD_LOGICAL].values()), ["queued"])

    def test_append_replays_malformed_history_before_idempotent_return(self) -> None:
        # C3-03: append_record must replay and validate the existing ledger
        # BEFORE the exact-last-line ALREADY_PRESENT return; malformed
        # existing history can never report success.
        broken = HAPPY_PATH[:3] + [
            record("closed", from_state="screened", reason_code="revision_closed"),
        ]
        path = self._write(broken)
        raw = path.read_bytes()
        with self.assertRaises(ledger.LedgerError) as caught:
            ledger.append_record(path, json.loads(json.dumps(broken[-1])))
        self.assertIn("is not a named migration", str(caught.exception))
        self.assertNotIn("ALREADY_PRESENT", str(caught.exception))
        # The malformed file is left untouched.
        self.assertEqual(path.read_bytes(), raw)

    def test_provenance_kind_is_transition_bound(self) -> None:
        # C2-06: each (from_state, to_state) migration binds its allowed
        # provenance kinds; a truthful kind for one transition is not
        # automatically truthful for another.
        def prefix(n: int) -> list[dict[str, object]]:
            return json.loads(json.dumps(HAPPY_PATH[:n]))

        adjudication_prefix = [
            record("queued"),
            record("deterministic_pass", from_state="queued",
                   reason_code="deterministic_layer_passed",
                   provenance_kind="deterministic_layer"),
            record("screened", from_state="deterministic_pass",
                   reason_code="surface_screen_completed", provenance_kind="surface_handoff"),
            record("deep_queued", from_state="screened",
                   reason_code="surface_ok_selected", provenance_kind="surface_handoff"),
            record("deep_reviewed", from_state="deep_queued",
                   reason_code="deep_review_completed", provenance_kind="deep_handoff"),
            record("finding_observed", from_state="deep_reviewed",
                   reason_code="deep_issue_observed", provenance_kind="deep_handoff"),
            record("adjudication", from_state="finding_observed",
                   reason_code="finding_observed", provenance_kind="adjudication_record"),
        ]
        wrong_kind_cases = [
            # Start with a non-freeze kind.
            [record("queued", provenance_kind="deterministic_layer")],
            # Deterministic pass cited by a surface handoff.
            prefix(1) + [record(
                "deterministic_pass", from_state="queued",
                reason_code="deterministic_layer_passed", provenance_kind="surface_handoff")],
            # Screened cited by an identity snapshot.
            prefix(2) + [record(
                "screened", from_state="deterministic_pass",
                reason_code="surface_screen_completed", provenance_kind="identity_snapshot")],
            # Deep review cited by a repair handoff.
            prefix(4) + [record(
                "deep_reviewed", from_state="deep_queued",
                reason_code="deep_review_completed", provenance_kind="repair_handoff")],
            # Closure cited by a deep handoff.
            prefix(6) + [record(
                "closed", from_state="revalidated",
                reason_code="revision_closed", provenance_kind="deep_handoff")],
            # Repair cited by an adjudication record.
            json.loads(json.dumps(adjudication_prefix)) + [record(
                "fixed", from_state="adjudication",
                reason_code="repair_confirmed_applied", provenance_kind="adjudication_record")],
        ]
        for sequence in wrong_kind_cases:
            with self.subTest(
                to=sequence[-1]["to_state"],
                kind=sequence[-1]["provenance"]["kind"],  # type: ignore[index]
            ):
                with self.assertRaises(ledger.LedgerError) as caught:
                    ledger.replay(sequence)
                self.assertIn("provenance kind", str(caught.exception))
        # The same kinds remain legal on their own named transitions.
        ledger.replay(json.loads(json.dumps(adjudication_prefix)) + [record(
            "fixed", from_state="adjudication",
            reason_code="repair_confirmed_applied", provenance_kind="repair_handoff")])

    def test_invalid_transition_matrix(self) -> None:
        base = HAPPY_PATH[:3]  # queued -> deterministic_pass -> screened
        invalid_sequences = [
            base + [record("closed", from_state="screened", reason_code="revision_closed")],
            base + [record("deep_reviewed", from_state="screened",
                           reason_code="deep_review_completed")],
            HAPPY_PATH[:4] + [record("deep_reviewed", from_state="sampling_queued",
                                     reason_code="deep_review_completed")],
            HAPPY_PATH[:4] + [record("queued", from_state="sampling_queued")],
            HAPPY_PATH + [record("queued", from_state="closed")],
            HAPPY_PATH[:1] + [record("screened", from_state="queued",
                                     reason_code="surface_screen_completed")],
            HAPPY_PATH[:2] + [record("deterministic_pass", from_state="deterministic_pass",
                                     reason_code="deterministic_layer_passed")],
            # Even a structurally named transition fails with a mismatched cause.
            base + [record("sampling_queued", from_state="screened",
                           reason_code="surface_issue")],
        ]
        for sequence in invalid_sequences:
            with self.subTest(to=sequence[-1]["to_state"]):
                with self.assertRaises(ledger.LedgerError):
                    ledger.replay(json.loads(json.dumps(sequence)))

    def test_lineage_and_duplication_failures(self) -> None:
        bad_new_revision_parent = HAPPY_PATH[:4] + [
            record("invalidated", from_state="deep_queued",
                   reason_code="source_changed", provenance_kind="identity_snapshot"),
            record("queued", revision=REVISION_2, parent=None),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(bad_new_revision_parent)))
        parent_not_latest = HAPPY_PATH[:4] + [
            record("invalidated", from_state="deep_queued",
                   reason_code="source_changed", provenance_kind="identity_snapshot"),
            record("queued", revision=REVISION_2, parent=OTHER_LOGICAL_REVISION),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(parent_not_latest)))
        migration_on_same_logical = HAPPY_PATH[:4] + [
            record("invalidated", from_state="deep_queued",
                   reason_code="source_changed", provenance_kind="identity_snapshot"),
            record("queued", revision=REVISION_2, parent=REVISION_1, migration=LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(migration_on_same_logical)))
        migration_target_not_invalidated = [
            record("queued", logical=OTHER_LOGICAL, revision=OTHER_LOGICAL_REVISION),
            record("queued", logical=MIGRATED_LOGICAL, revision=MIGRATED_REVISION,
                   migration=OTHER_LOGICAL),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(migration_target_not_invalidated)))
        two_active_revisions = HAPPY_PATH[:4] + [
            record("invalidated", from_state="deep_queued",
                   reason_code="source_changed", provenance_kind="identity_snapshot"),
            record("queued", revision=REVISION_2, parent=REVISION_1),
        ] + [record("deterministic_pass", from_state="queued", revision=REVISION_1,
                    reason_code="deterministic_layer_passed")]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(two_active_revisions)))
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(HAPPY_PATH + HAPPY_PATH[:1])))
        from_state_mismatch = HAPPY_PATH[:3] + [
            record("deep_queued", from_state="deterministic_pass",
                   reason_code="surface_ok_selected")
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(from_state_mismatch)))

    def test_entry_revision_identity_reuse_across_logicals_is_global(self) -> None:
        records = HAPPY_PATH + [
            # Same revision identity re-owned by a different logical identity.
            record("queued", logical=OTHER_LOGICAL, revision=REVISION_1),
        ]
        with self.assertRaises(ledger.LedgerError):
            ledger.replay(json.loads(json.dumps(records)))

    def test_formal_catalog_consumer_rejects_shadow_provenance(self) -> None:
        shadow = {
            "schema_version": 1,
            "kind": "production_catalog_shadow_v1",
            "markers": {"authoritative": False, "dispatchable": False, "promotable": False},
            "catalog_id": "1" * 64,
        }
        shadow_raw = check.canonical_bytes(shadow)
        harvested = record(
            "queued",
            provenance_sha256=__import__("hashlib").sha256(shadow_raw).hexdigest(),
        )
        # The exact eleven-key row remains structurally legal in isolation,
        # but the formal catalog/provenance consumer rejects its shadow parent.
        ledger.validate_record(harvested)
        with self.assertRaisesRegex(ledger.LedgerError, "formal catalog manifest"):
            ledger.replay_with_catalog([harvested], shadow_raw)

        # Rebranding and flipping markers cannot manufacture the missing WP2
        # schema/ID/domain/body/lineage validator.
        rebranded = {
            "schema_version": 1, "kind": "production_catalog_v1",
            "markers": {"authoritative": True, "dispatchable": True, "promotable": True},
            "catalog_id": "2" * 64,
        }
        rebranded_raw = check.canonical_bytes(rebranded)
        accepted = record("queued", provenance_sha256=__import__("hashlib").sha256(rebranded_raw).hexdigest())
        with self.assertRaisesRegex(ledger.LedgerError, "formal catalog manifest"):
            ledger.replay_with_catalog([accepted], rebranded_raw)

    def test_cli_formal_consumer_rejects_shadow_catalog(self) -> None:
        shadow = {
            "schema_version": 1,
            "kind": "production_catalog_shadow_v1",
            "markers": {"authoritative": False, "dispatchable": False, "promotable": False},
            "catalog_id": "1" * 64,
        }
        shadow_raw = check.canonical_bytes(shadow)
        path = self._write([record(
            "queued", provenance_sha256=__import__("hashlib").sha256(shadow_raw).hexdigest()
        )])
        catalog = self.root / "catalog.json"
        catalog.write_bytes(shadow_raw)
        completed = subprocess.run([
            sys.executable, "-B", str(TOOLS / "translation_review_ledger.py"),
            "check", path.name, "--root", str(self.root),
            "--catalog-manifest", catalog.name,
        ], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 1)
        self.assertIn("formal catalog manifest", completed.stdout)
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_cli_repository_shadow_barrier_survives_root_redirection(self) -> None:
        repository_catalog = next((ROOT / "evidence/production-review/catalogs").glob("*/manifest.json"))
        digest = __import__("hashlib").sha256(repository_catalog.read_bytes()).hexdigest()
        forbidden_record = record("queued", provenance_sha256=digest)
        ledger_path = self._write([forbidden_record])
        record_path = self.root / "record.json"
        record_path.write_bytes(check.canonical_bytes(forbidden_record))
        empty_path = self.root / "empty.jsonl"
        empty_path.write_bytes(b"")
        for command, arguments in (
            ("check", [ledger_path.name]),
            ("summary", [ledger_path.name]),
            ("append", [empty_path.name, str(record_path)]),
        ):
            with self.subTest(command=command):
                completed = subprocess.run([
                    sys.executable, "-B", str(TOOLS / "translation_review_ledger.py"),
                    command, *arguments, "--root", str(self.root),
                ], capture_output=True, text=True)
                self.assertEqual(completed.returncode, 1)
                self.assertIn("forbidden tracked WP1 shadow", completed.stdout)
                self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_shadow_catalog_children_fail_closed_when_malformed(self) -> None:
        catalogs = self.root / "evidence/production-review/catalogs"
        catalogs.mkdir(parents=True)
        cases = ("file-child", "missing-manifest", "malformed-manifest")
        for case in cases:
            with self.subTest(case=case):
                child = catalogs / case
                if case == "file-child":
                    child.write_bytes(b"not a directory")
                else:
                    child.mkdir()
                    if case == "malformed-manifest":
                        (child / "manifest.json").write_bytes(b'{}')
                with self.assertRaises(ledger.LedgerError):
                    ledger.forbidden_shadow_provenance(self.root)
                if child.is_dir():
                    for path in child.iterdir():
                        path.unlink()
                    child.rmdir()
                else:
                    child.unlink()

    def test_relabelled_shadow_catalog_fails_closed_for_default_cli(self) -> None:
        repository_catalog = next(
            (ROOT / "evidence/production-review/catalogs").glob("*/manifest.json")
        )
        original = check.strict_json_bytes(
            repository_catalog.read_bytes(), label="repository shadow catalog")
        original["recorded_by"] = "temporary exact-shape baseline"
        original["catalog_id"] = ledger._shadow_catalog_id(original)
        original_raw = check.canonical_bytes(original)
        original_digest = __import__("hashlib").sha256(original_raw).hexdigest()
        mutations = [
            ("kind", "production_catalog_v1"),
            ("authoritative", True),
            ("dispatchable", True),
            ("promotable", True),
        ]
        for field, replacement in mutations:
            with self.subTest(field=field):
                catalogs = self.root / "evidence/production-review/catalogs"
                child = catalogs / original["catalog_id"]
                child.mkdir(parents=True, exist_ok=True)
                relabelled = json.loads(json.dumps(original))
                if field == "kind":
                    relabelled["kind"] = replacement
                else:
                    relabelled["markers"][field] = replacement
                (child / "manifest.json").write_bytes(check.canonical_bytes(relabelled))
                records = [record("queued", provenance_sha256=original_digest)]
                ledger_path = self._write(records)
                record_path = self.root / "record.json"
                record_path.write_bytes(check.canonical_bytes(records[0]))
                empty_path = self.root / "empty.jsonl"
                empty_path.write_bytes(b"")
                for command, arguments in (
                    ("check", [ledger_path.name]),
                    ("summary", [ledger_path.name]),
                    ("append", [empty_path.name, str(record_path)]),
                ):
                    completed = subprocess.run([
                        sys.executable, "-B", str(TOOLS / "translation_review_ledger.py"),
                        command, *arguments, "--root", str(self.root),
                    ], capture_output=True, text=True)
                    self.assertEqual(completed.returncode, 1, completed.stdout)
                    self.assertIn("shadow catalog manifest", completed.stdout)
                    self.assertNotIn("Traceback", completed.stdout + completed.stderr)
                for path in child.iterdir():
                    path.unlink()
                child.rmdir()

    def test_default_cli_and_library_barrier_harvest_tracked_shadow(self) -> None:
        repository_catalog = next(
            (ROOT / "evidence/production-review/catalogs").glob("*/manifest.json")
        )
        shadow = check.strict_json_bytes(
            repository_catalog.read_bytes(), label="repository shadow catalog")
        shadow["recorded_by"] = "temporary exact-shape baseline"
        shadow["catalog_id"] = ledger._shadow_catalog_id(shadow)
        catalog_dir = (self.root / "evidence/production-review/catalogs"
                       / shadow["catalog_id"])
        catalog_dir.mkdir(parents=True)
        raw = check.canonical_bytes(shadow)
        (catalog_dir / "manifest.json").write_bytes(raw)
        digest = __import__("hashlib").sha256(raw).hexdigest()
        records = [record("queued", provenance_sha256=digest)]
        path = self._write(records)
        forbidden = ledger.forbidden_shadow_provenance(self.root)
        with self.assertRaisesRegex(ledger.LedgerError, "forbidden tracked WP1 shadow"):
            ledger.replay_production(records, forbidden_provenance=forbidden)
        completed = subprocess.run([
            sys.executable, "-B", str(TOOLS / "translation_review_ledger.py"),
            "check", path.name, "--root", str(self.root),
        ], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 1)
        self.assertIn("forbidden tracked WP1 shadow", completed.stdout)
        record_file = self.root / "record.json"
        record_file.write_bytes(check.canonical_bytes(records[0]))
        empty = self.root / "empty.jsonl"; empty.write_bytes(b"")
        appended = subprocess.run([
            sys.executable, "-B", str(TOOLS / "translation_review_ledger.py"),
            "append", empty.name, str(record_file), "--root", str(self.root),
        ], capture_output=True, text=True)
        self.assertEqual(appended.returncode, 1)
        self.assertNotIn("Traceback", completed.stdout + completed.stderr + appended.stdout + appended.stderr)

    def test_exact_record_shape_and_forbidden_provenance(self) -> None:
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_record({"schema_version": 1})
        provider_record = record("queued")
        provider_record["provider"] = "some-provider"
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_record(provider_record)
        model_record = record("queued")
        model_record["recorded_by"] = ""
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_record(model_record)
        bad_state = record("queued")
        bad_state["to_state"] = "done_i_guess"
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_record(bad_state)
        free_text = record("invalidated", from_state="queued", reason_code="just because")
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_record(free_text)
        bad_provenance = record("queued")
        bad_provenance["provenance"] = {"kind": "surface_handoff"}
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_record(bad_provenance)
        bad_kind = record("queued")
        bad_kind["provenance"]["kind"] = "gut_feeling"
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_record(bad_kind)
        bad_hash = record("queued")
        bad_hash["provenance"]["sha256"] = "NOTHEX"
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_record(bad_hash)
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_record(record("queued", reason_code="not_a_machine_cause"))
        # A closed-set code bound to the wrong transition is caught by replay.
        with self.assertRaises(ledger.LedgerError):
            ledger.replay([record("queued", reason_code="surface_issue")])

    def test_file_level_failures(self) -> None:
        path = self._write(HAPPY_PATH)
        raw = path.read_bytes()
        # Non-canonical line.
        pretty = json.dumps(HAPPY_PATH[0], ensure_ascii=False, indent=2).encode("utf-8")
        path.write_bytes(pretty + b"\n")
        with self.assertRaises(ledger.LedgerError):
            ledger.parse_ledger_bytes(path.read_bytes())
        # BOM.
        path.write_bytes(b"\xef\xbb\xbf" + raw)
        with self.assertRaises(ledger.LedgerError):
            ledger.parse_ledger_bytes(path.read_bytes())
        # Blank middle line.
        path.write_bytes(raw.split(b"\n", 1)[0] + b"\n\n" + raw.split(b"\n", 1)[1])
        with self.assertRaises(ledger.LedgerError):
            ledger.parse_ledger_bytes(path.read_bytes())
        # Missing trailing newline.
        path.write_bytes(raw.rstrip(b"\n"))
        with self.assertRaises(ledger.LedgerError):
            ledger.parse_ledger_bytes(path.read_bytes())
        # Duplicate immutable event.
        path.write_bytes(raw + raw.split(b"\n", 1)[0] + b"\n")
        with self.assertRaises(ledger.LedgerError):
            ledger.parse_ledger_bytes(path.read_bytes())
        # Non-last duplicate of an immutable event.
        first = check.canonical_bytes(HAPPY_PATH[0])
        later = b"".join(
            check.canonical_bytes(item) + b"\n" for item in HAPPY_PATH[1:3]
        )
        tail = b"".join(
            check.canonical_bytes(item) + b"\n" for item in HAPPY_PATH[3:]
        )
        path.write_bytes(first + b"\n" + first + b"\n" + later + tail)
        with self.assertRaises(ledger.LedgerError):
            ledger.parse_ledger_bytes(path.read_bytes())
        # Empty ledger is valid.
        path.write_bytes(b"")
        self.assertEqual(ledger.parse_ledger_bytes(path.read_bytes()), [])

    def test_append_rejects_intervening_logical_duplicate_reproduction(self) -> None:
        # C2-04: an exact duplicate of an earlier event whose from_state
        # matches the replayed state (here: the adjudication self-loop)
        # must be rejected even after an intervening logical identity,
        # because re-appending it would permanently corrupt the history.
        adjudication_loop = record(
            "adjudication", from_state="adjudication",
            reason_code="re_adjudication_pending_evidence",
            provenance_kind="adjudication_record",
        )
        history = [
            record("queued"),
            record("deterministic_pass", from_state="queued",
                   reason_code="deterministic_layer_passed",
                   provenance_kind="deterministic_layer"),
            record("screened", from_state="deterministic_pass",
                   reason_code="surface_screen_completed", provenance_kind="surface_handoff"),
            record("deep_queued", from_state="screened",
                   reason_code="surface_ok_selected", provenance_kind="surface_handoff"),
            record("deep_reviewed", from_state="deep_queued",
                   reason_code="deep_review_completed", provenance_kind="deep_handoff"),
            record("finding_observed", from_state="deep_reviewed",
                   reason_code="deep_issue_observed", provenance_kind="deep_handoff"),
            record("adjudication", from_state="finding_observed",
                   reason_code="finding_observed", provenance_kind="adjudication_record"),
            adjudication_loop,
            # Intervening logical identity so the duplicate is not the last
            # line and its from_state still matches the replayed state.
            record("queued", logical=OTHER_LOGICAL, revision=OTHER_LOGICAL_REVISION),
        ]
        path = self._write(history)
        with self.assertRaises(ledger.LedgerError) as caught:
            ledger.append_record(path, json.loads(json.dumps(adjudication_loop)))
        self.assertIn("duplicates an immutable event", str(caught.exception))
        # The file is untouched and still loads cleanly.
        self.assertEqual(len(ledger.load_ledger(path)), len(history))

    def test_append_is_idempotent_for_last_line_and_rejects_duplicates(self) -> None:
        path = self._write(HAPPY_PATH[:3])
        outcome = ledger.append_record(path, record(
            "deep_queued", from_state="screened",
            reason_code="surface_ok_selected", provenance_kind="surface_handoff",
        ))
        self.assertEqual(outcome, "APPENDED")
        self.assertEqual(len(ledger.load_ledger(path)), 4)
        outcome = ledger.append_record(path, record(
            "deep_queued", from_state="screened",
            reason_code="surface_ok_selected", provenance_kind="surface_handoff",
        ))
        self.assertEqual(outcome, "ALREADY_PRESENT")
        self.assertEqual(len(ledger.load_ledger(path)), 4)
        with self.assertRaises(ledger.LedgerError):
            ledger.append_record(path, record(
                "closed", from_state="deep_queued", reason_code="revision_closed"
            ))
        # A record duplicating a non-last immutable event is rejected.
        with self.assertRaises(ledger.LedgerError):
            ledger.append_record(path, HAPPY_PATH[0])
        with tempfile.TemporaryDirectory() as temporary:
            fresh = Path(temporary) / "nested" / "ledger.jsonl"
            fresh.parent.mkdir()
            outcome = ledger.append_record(fresh, record("queued"))
            self.assertEqual(outcome, "APPENDED")
            self.assertEqual(len(ledger.load_ledger(fresh)), 1)

    def test_append_rejects_illegal_first_record(self) -> None:
        # The first record must replay as a legal revision start: not an
        # arbitrary mid-machine transition.
        with tempfile.TemporaryDirectory() as temporary:
            fresh = Path(temporary) / "ledger.jsonl"
            for bad in (
                record("screened", from_state="deterministic_pass",
                       reason_code="surface_screen_completed"),
                record("deep_reviewed", from_state="deep_queued",
                       reason_code="deep_review_completed"),
                record("closed", from_state="revalidated",
                       reason_code="revision_closed"),
                record("queued", from_state="queued"),
            ):
                with self.subTest(to=bad["to_state"]):
                    with self.assertRaises(ledger.LedgerError):
                        ledger.append_record(fresh, bad)
                    self.assertFalse(fresh.exists())

    def test_cli_exit_codes(self) -> None:
        path = self._write(HAPPY_PATH)
        verified = subprocess.run([
            sys.executable, "-B", str(TOOLS / "translation_review_ledger.py"),
            "check", "TRANSLATION-REVIEW-LEDGER.jsonl", "--root", str(self.root),
        ], capture_output=True, text=True)
        self.assertEqual(verified.returncode, 0)
        self.assertIn("LEDGER_VERIFIED records=7", verified.stdout)
        record_file = self.root / "record.json"
        record_file.write_bytes(check.canonical_bytes(
            record("deep_queued", from_state="sampling_queued",
                   reason_code="deferred_sampled")
        ))
        appended = subprocess.run([
            sys.executable, "-B", str(TOOLS / "translation_review_ledger.py"),
            "append", "TRANSLATION-REVIEW-LEDGER.jsonl", str(record_file),
            "--root", str(self.root),
        ], capture_output=True, text=True)
        self.assertEqual(appended.returncode, 1)
        self.assertIn("LEDGER_FAILED:", appended.stdout)
        summary = subprocess.run([
            sys.executable, "-B", str(TOOLS / "translation_review_ledger.py"),
            "summary", "TRANSLATION-REVIEW-LEDGER.jsonl", "--root", str(self.root),
        ], capture_output=True, text=True)
        self.assertEqual(summary.returncode, 0)
        self.assertIn('"deferred_is_not_deep_reviewed":true', summary.stdout)
        escaped = subprocess.run([
            sys.executable, "-B", str(TOOLS / "translation_review_ledger.py"),
            "check", "../escape.jsonl", "--root", str(self.root),
        ], capture_output=True, text=True)
        self.assertEqual(escaped.returncode, 2)
        self.assertIn("INPUT_ERROR:", escaped.stdout)
        self.assertNotIn(
            "Traceback",
            verified.stdout + verified.stderr + appended.stdout + summary.stdout,
        )


if __name__ == "__main__":
    unittest.main()
