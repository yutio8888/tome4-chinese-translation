from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as catalog
from tools.i18nlib import production_review_v2_lite_migration as migration
from tools.i18nlib import production_review_v2_lite_queue as queue


class MigrationFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=self.root, check=True)
        (self.root / ".gitignore").write_text("/.artifacts/\n", encoding="utf-8")
        self.entries = [self.entry(str(index)) for index in range(3)]
        self.write_catalog(self.entries)
        (self.root / catalog.SCHEMA_PATH).write_bytes(catalog.SCHEMA_RAW_BY_RULES[catalog.RULES_VERSION])
        (self.root / catalog.POLICY_PATH).write_bytes(catalog.POLICY_RAW)
        self.commit("old catalog")
        queue.init(self.root)

    def entry(self, suffix: str, *, source: str | None = None, target: str | None = None,
              source_tag: str = "", section: str = "fixture", fixed: str | None = None,
              terminology: str = "b" * 64, rules: str = catalog.RULES_VERSION,
              path: str = "tome.lua", args_order: object = None) -> dict:
        source = source or "source " + suffix
        target = target or "target " + suffix
        fixed = fixed or "commit:" + "a" * 40
        core = {"component": "tome", "duplicate_index": 0, "function_name": "t",
                "normalized_source_tag": source_tag, "section": section, "source": source,
                "translation_path": path}
        locator = catalog._plain_id(catalog.CALL_LOCATOR_KIND, "locator", core)
        logical = wp1.surface.logical_entry_identity(component="tome", normalized_path=path,
                                                      call_locator=locator, source_tag=source_tag)
        revision = wp1.surface.entry_revision_identity(logical_entry_identity=logical,
            source=source, target=target, fixed_source_identity=fixed,
            terminology_snapshot=terminology, rules_version=rules,
            args_order=args_order if rules == catalog.RULES_VERSION else None)
        return {"schema_version": 1, "component": "tome", "normalized_path": path,
                "section": section, "call_locator": locator,
                "logical_entry_identity": logical, "entry_revision_identity": revision,
                "source": source, "target": target, "source_tag": source_tag,
                "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
                "target_sha256": hashlib.sha256(target.encode()).hexdigest(),
                "fixed_source_identity": fixed,
                "terminology_snapshot_sha256": terminology, "rules_version": rules,
                "risk": {"has_args_order": args_order is not None, "has_special": False,
                         "source_utf8_bytes": len(source.encode()),
                         "target_utf8_bytes": len(target.encode()),
                         "component_group_size": 3, "component_group_last": False,
                         **({"args_order": args_order} if rules == catalog.RULES_VERSION else {})}}

    def commit(self, message: str) -> str:
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=self.root, check=True)
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

    def write_catalog(self, entries: list[dict], destination: Path | None = None,
                      *, rules: str | None = None, terminology: str | None = None,
                      fixed: str | None = None) -> Path:
        destination = destination or self.root
        destination.mkdir(parents=True, exist_ok=True)
        rows = sorted(copy.deepcopy(entries), key=lambda row: row["entry_revision_identity"])
        entries_raw = wp1._jsonl(rows)
        exclusions_raw = b""
        rules = rules or (rows[0]["rules_version"] if rows else catalog.RULES_VERSION)
        policy_raw = catalog.POLICY_RAW_BY_RULES[rules]
        terminology = terminology or (rows[0]["terminology_snapshot_sha256"] if rows else "b" * 64)
        fixed = fixed or (rows[0]["fixed_source_identity"] if rows else "commit:" + "a" * 40)
        manifest = {"schema_version": 1, "kind": catalog.CATALOG_KIND, "catalog_id": "",
                    "rules_version": rules, "recorded_at": "2026-09-02T01:02:03Z",
                    "recorded_by": "fixture", "manifest_sha256": "c" * 64,
                    "loader_contract_path": "tools/i18nlib/locale_model.py",
                    "loader_contract_sha256": "d" * 64, "lua_runtime": "Lua 5.1",
                    "manifest_component_ordinals": [{"component": name, "ordinal": index}
                        for index, name in enumerate(["engine", "boot", "tome", "ashes-urhrok", "cults", "orcs"])],
                    "component_counts": {name: (len(rows) if name == "tome" else 0)
                                         for name in ["engine", "boot", "tome", "ashes-urhrok", "cults", "orcs"]},
                    "occurrence_count": len(rows), "entry_count": len(rows), "exclusion_count": 0,
                    "entries_sha256": hashlib.sha256(entries_raw).hexdigest(),
                    "exclusions_sha256": hashlib.sha256(exclusions_raw).hexdigest(),
                    "terminology_snapshot_sha256": terminology,
                    "source_identities": {name: (fixed if name == "tome" else "commit:" + "a" * 40)
                                          for name in ["engine", "boot", "tome", "ashes-urhrok", "cults", "orcs"]},
                    "policy_sha256": hashlib.sha256(policy_raw).hexdigest()}
        manifest["catalog_id"] = catalog.catalog_id(manifest)
        if destination == self.root:
            self.catalog_id = manifest["catalog_id"]
        files = {catalog.SCHEMA_PATH: catalog.SCHEMA_RAW_BY_RULES[rules], catalog.POLICY_PATH: policy_raw,
                 f"{catalog.CATALOG_PREFIX}/manifest.json": wp1.canonical_bytes(manifest),
                 f"{catalog.CATALOG_PREFIX}/entries.jsonl": entries_raw,
                 f"{catalog.CATALOG_PREFIX}/exclusions.jsonl": exclusions_raw}
        for name, raw in files.items():
            path = destination / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        return destination

    def candidate(self, entries: list[dict], **kwargs) -> Path:
        candidate = self.root / "candidate"
        if candidate.exists():
            shutil.rmtree(candidate)
        self.write_catalog(entries, candidate, **kwargs)
        return candidate

    def replace(self, row: dict, **changes) -> dict:
        result = copy.deepcopy(row)
        result.update(changes)
        if "args_order" in changes:
            result["risk"]["args_order"] = changes["args_order"]
        if result["rules_version"] == catalog.RULES_VERSION:
            result["risk"].setdefault("args_order", None)
        else:
            result["risk"].pop("args_order", None)
        source = result["source"]
        target = result["target"]
        path = result["normalized_path"]
        tag = result["source_tag"]
        core = {"component": result["component"], "duplicate_index": 0,
                "function_name": "t", "normalized_source_tag": tag,
                "section": result["section"], "source": source,
                "translation_path": path}
        result["call_locator"] = catalog._plain_id(catalog.CALL_LOCATOR_KIND, "locator", core)
        result["logical_entry_identity"] = wp1.surface.logical_entry_identity(
            component=result["component"], normalized_path=path,
            call_locator=result["call_locator"], source_tag=tag)
        result["entry_revision_identity"] = wp1.surface.entry_revision_identity(
            logical_entry_identity=result["logical_entry_identity"], source=source,
            target=target, fixed_source_identity=result["fixed_source_identity"],
            terminology_snapshot=result["terminology_snapshot_sha256"],
            rules_version=result["rules_version"],
            args_order=result["risk"].get("args_order"))
        result["source_sha256"] = hashlib.sha256(source.encode()).hexdigest()
        result["target_sha256"] = hashlib.sha256(target.encode()).hexdigest()
        result["risk"]["source_utf8_bytes"] = len(source.encode())
        result["risk"]["target_utf8_bytes"] = len(target.encode())
        return result


class MigrationTests(MigrationFixture):
    def _summary_for_rows(self, entries, catalog_id):
        entries_raw = wp1._jsonl(entries)
        return {"catalog_id": catalog_id, "manifest_sha256": "c" * 64,
                "entries_sha256": hashlib.sha256(entries_raw).hexdigest(),
                "exclusions_sha256": "d" * 64,
                "counts": {"occurrence_count": len(entries),
                           "entry_count": len(entries), "exclusion_count": 0}}

    def _rehash_migration(self, value):
        value["rows_sha256"] = hashlib.sha256(wp1.canonical_bytes(value["rows"])).hexdigest()
        value["migration_id"] = migration._migration_id(value)
        value["target_path"] = f"{migration.MIGRATION_PREFIX}{value['migration_id']}.json"
        return value

    def test_v2_sparse_representation_and_catalog_bound_expansion(self):
        changed = [self.replace(self.entries[0], target="new target"), *self.entries[1:]]
        value = migration._build_migration(
            "a" * 40, "b" * 40,
            self._summary_for_rows(self.entries, "a" * 64), self.entries,
            self._summary_for_rows(changed, "b" * 64), changed,
            recorded_at="2026-09-02T01:02:03Z", recorded_by="fixture")
        self.assertEqual(value["schema_version"], 2)
        self.assertNotIn("old_rows", value)
        self.assertNotIn("new_rows", value)
        self.assertEqual(len(value["rows"]), 1)
        self.assertEqual(value["rows"][0]["disposition"], "revision_changed")
        normalized = migration.validate_migration(
            value, expected_old_entries=self.entries, expected_new_entries=changed)
        self.assertEqual(len(normalized["rows"]), len(self.entries))
        self.assertEqual(sum(row["disposition"] == "unchanged" for row in normalized["rows"]), 2)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "catalog-bound"):
            migration.validate_migration(value)
        with self.assertRaises(wp1.ProductionReviewError):
            migration.validate_migration(
                value, expected_old_entries=changed, expected_new_entries=changed)

    def test_v2_sparse_rows_fail_closed_on_omission_extra_unchanged_and_misclassification(self):
        changed = [self.replace(self.entries[0], target="new target"), *self.entries[1:]]
        original = migration._build_migration(
            "a" * 40, "b" * 40,
            self._summary_for_rows(self.entries, "a" * 64), self.entries,
            self._summary_for_rows(changed, "b" * 64), changed,
            recorded_at="2026-09-02T01:02:03Z", recorded_by="fixture")
        unchanged = migration.reconcile(self.entries, changed)[1]
        mutations = []
        omitted = copy.deepcopy(original); omitted["rows"] = []; mutations.append(omitted)
        extra = copy.deepcopy(original); extra["rows"].append(copy.deepcopy(unchanged)); mutations.append(extra)
        misclassified = copy.deepcopy(original); misclassified["rows"][0]["reason"] = "fixed_source_changed"; mutations.append(misclassified)
        duplicated = copy.deepcopy(original); duplicated["rows"].append(copy.deepcopy(duplicated["rows"][0])); mutations.append(duplicated)
        reordered = copy.deepcopy(original); reordered["rows"] = list(reversed([copy.deepcopy(unchanged), *reordered["rows"]])); mutations.append(reordered)
        for value in mutations:
            with self.subTest(rows=value["rows"]):
                self._rehash_migration(value)
                with self.assertRaises(wp1.ProductionReviewError):
                    migration.validate_migration(
                        value, expected_old_entries=self.entries, expected_new_entries=changed)

    def test_v1_full_record_stays_exact_and_truncation_is_not_sparse(self):
        value = migration._build_migration(
            "a" * 40, "b" * 40,
            self._summary_for_rows(self.entries, "a" * 64), self.entries,
            self._summary_for_rows(self.entries, "b" * 64), self.entries,
            recorded_at="2026-09-02T01:02:03Z", recorded_by="fixture", schema_version=1)
        self.assertEqual(value["schema_version"], 1)
        self.assertIn("old_rows", value)
        self.assertIn("new_rows", value)
        self.assertEqual(migration.validate_migration(value), value)
        truncated = copy.deepcopy(value)
        truncated.pop("old_rows")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "exact keys"):
            migration.validate_migration(truncated)

    def test_current_rules_boundary_uses_exact_policy_in_ordinary_and_migration_validation(self):
        candidate = self.candidate(self.entries)
        artifact = self.root / ".artifacts" / "current-rules.json"
        report = migration.plan(self.root, candidate, output=artifact)
        self.assertEqual(report["dispositions"], {"unchanged": 3})
        migration.check(self.root, artifact, candidate_catalog=candidate)
        catalog.validate_catalog_files(catalog.ordinary_tree(candidate))
        applied = migration.apply(self.root, artifact, candidate_catalog=candidate)
        self.assertTrue(applied["applied"])
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[2][2], report["new_catalog_id"])

        policy_path = candidate / catalog.POLICY_PATH
        policy = wp1.parse_canonical_object(policy_path.read_bytes(), "unsupported policy")
        policy["rules_version"] = "production-review-v2-lite-rules-v3"
        policy_path.write_bytes(wp1.canonical_bytes(policy))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "supported exact policy|policy bytes"):
            catalog.validate_catalog_files(catalog.ordinary_tree(candidate))

    def test_check_and_apply_require_the_exact_candidate_catalog_api(self):
        candidate = self.candidate([self.replace(self.entries[0], target="new target"), *self.entries[1:]])
        artifact = self.root / ".artifacts" / "candidate-required.json"
        migration.plan(self.root, candidate, output=artifact)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "candidate catalog"):
            migration.check(self.root, artifact)
        before = queue.business_rows(queue.database_path(self.root))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "candidate catalog"):
            migration.apply(self.root, artifact)
        self.assertEqual(before, queue.business_rows(queue.database_path(self.root)))

    def test_all_exact_revision_reasons_and_removed(self):
        old = self.entries[0]
        cases = [
            (self.replace(old, target="new target"), "revision_changed", "target_changed"),
            (self.replace(old, source="new source"), "logical_moved", "source_changed"),
            (self.replace(old, source_tag="new-tag"), "logical_moved", "source_tag_changed"),
            (self.replace(old, fixed_source_identity="commit:" + "e" * 40), "revision_changed", "fixed_source_changed"),
            (self.replace(old, terminology_snapshot_sha256="f" * 64), "unchanged", "unchanged"),
            (self.replace(old, rules_version=catalog.FROZEN_RULES_VERSION), "revision_changed", "rules_changed"),
        ]
        # A single-row move has no exact local neighbour and is therefore
        # fail-closed; the full move proof is exercised below with neighbours.
        for candidate, disposition, reason in cases[:1] + cases[3:]:
            rows = migration.reconcile([old], [candidate])
            self.assertEqual((rows[0]["disposition"], rows[0]["reason"]), (disposition, reason))
        rows = migration.reconcile([old], [])
        self.assertEqual((rows[0]["disposition"], rows[0]["reason"]), ("removed", "removed"))

    def test_args_order_reason_is_validated_and_not_masked_by_terminology(self):
        old = self.entry("args", source="%s has %d", target="%s belongs to %d", args_order=[1, 2])
        changed = self.replace(old, args_order=[2, 1], terminology="f" * 64)
        rows = migration.reconcile([old], [changed])
        self.assertEqual((rows[0]["disposition"], rows[0]["reason"]),
                         ("revision_changed", "args_order_changed"))

        def summary(entries, catalog_id):
            entries_raw = wp1._jsonl(entries)
            return {"catalog_id": catalog_id, "manifest_sha256": "c" * 64,
                    "entries_sha256": hashlib.sha256(entries_raw).hexdigest(),
                    "exclusions_sha256": "d" * 64,
                    "counts": {"occurrence_count": len(entries),
                               "entry_count": len(entries), "exclusion_count": 0}}

        value = migration._build_migration(
            "a" * 40, "b" * 40, summary([old], "a" * 64), [old],
            summary([changed], "b" * 64), [changed],
            recorded_at="2026-09-02T01:02:03Z", recorded_by="fixture")
        self.assertEqual(value["rows"], rows)
        validated = migration.validate_migration(
            value, expected_old_entries=[old], expected_new_entries=[changed])
        self.assertEqual(validated["rows"], rows)

    def test_unique_move_requires_exact_local_adjacency_and_ambiguous_unmapped(self):
        old = self.entries
        moved = [copy.deepcopy(row) for row in old]
        moved[1] = self.replace(moved[1], source="moved source")
        result = migration.reconcile(old, moved)
        moved_row = next(row for row in result if row["old_entry_revision_identity"] == old[1]["entry_revision_identity"])
        self.assertEqual((moved_row["disposition"], moved_row["reason"]), ("unmapped", "unmapped"))

        locator_changed = [copy.deepcopy(row) for row in old]
        locator_changed[1]["call_locator"] = "e" * 64
        locator_changed[1]["logical_entry_identity"] = wp1.surface.logical_entry_identity(
            component="tome", normalized_path="tome.lua", call_locator="e" * 64,
            source_tag="")
        locator_changed[1]["entry_revision_identity"] = wp1.surface.entry_revision_identity(
            logical_entry_identity=locator_changed[1]["logical_entry_identity"],
            source=locator_changed[1]["source"], target=locator_changed[1]["target"],
            fixed_source_identity=locator_changed[1]["fixed_source_identity"],
            terminology_snapshot=locator_changed[1]["terminology_snapshot_sha256"],
            rules_version=locator_changed[1]["rules_version"])
        result = migration.reconcile(old, locator_changed)
        locator_row = next(row for row in result if row["old_entry_revision_identity"] == old[1]["entry_revision_identity"])
        self.assertEqual((locator_row["disposition"], locator_row["reason"]), ("unmapped", "unmapped"))

        ambiguous = [copy.deepcopy(row) for row in old]
        ambiguous[1] = self.replace(ambiguous[1], source="candidate one")
        ambiguous.append(self.replace(old[1], source="candidate two"))
        result = migration.reconcile(old[1:2], ambiguous)
        self.assertEqual((result[0]["disposition"], result[0]["reason"]), ("ambiguous", "ambiguous"))

        unrelated = [self.replace(old[1], source="not adjacent", section="other")]
        result = migration.reconcile(old[1:2], unrelated)
        self.assertEqual((result[0]["disposition"], result[0]["reason"]), ("removed", "removed"))
        no_adjacency = [self.replace(old[1], source="same group")]
        result = migration.reconcile(old[1:2], no_adjacency)
        self.assertEqual((result[0]["disposition"], result[0]["reason"]), ("unmapped", "unmapped"))

    def test_plan_check_apply_successor_queue_and_parent_state_noninheritance(self):
        # Exact target drift preserves the logical identity but creates a new
        # revision.  The prospective catalog is never copied into the repo.
        candidate_rows = [self.replace(self.entries[0], target="repaired target"), self.entries[1], self.entries[2]]
        candidate = self.candidate(candidate_rows)
        artifact = self.root / ".artifacts" / "migration.json"
        report = migration.plan(self.root, candidate, output=artifact)
        self.assertTrue(report["ok"])
        self.assertEqual(report["dispositions"], {"revision_changed": 1, "unchanged": 2})
        checked = migration.check(self.root, artifact, candidate_catalog=candidate)
        self.assertEqual(checked["migration_id"], report["migration_id"])
        before = queue.business_rows(queue.database_path(self.root))[0]
        # A queued-only old projection is enough to prove the successor is not
        # manufactured as an override; unchanged rows remain implicit too.
        applied = migration.apply(self.root, artifact, candidate_catalog=candidate)
        self.assertTrue(applied["applied"])
        overrides, reconciliation, meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual(overrides, [])
        self.assertEqual(meta[2], report["new_catalog_id"])
        changed = next(row for row in reconciliation if row[4] == "revision_changed")
        self.assertEqual(changed[4], "revision_changed")
        self.assertEqual(before, [])

    def test_active_checkpoint_and_dirty_relevant_paths_reject_plan(self):
        candidate = self.candidate([self.replace(self.entries[0], target="new target"), *self.entries[1:]])
        # batch.start creates the one active checkpoint and reserved rows.
        from tools.i18nlib import production_review_v2_lite_batch as batch
        batch.start(self.root, limit=1)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "checkpoint|reserved"):
            migration.plan(self.root, candidate)
        batch.abandon(self.root)
        dirty = self.root / "evidence/production-review-v2-lite/catalog/dirty"
        dirty.parent.mkdir(parents=True, exist_ok=True)
        dirty.write_text("dirty", encoding="utf-8")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "clean"):
            migration.plan(self.root, candidate)

    def test_ambiguous_plan_is_canonical_but_apply_stops_before_db_mutation(self):
        # Direct reconciliation is deterministic; a plan with ambiguous rows
        # is still useful for user adjudication, while apply remains fail-closed.
        old = self.entries[1]
        first = self.replace(old, source="first")
        second = self.replace(old, source="second")
        candidate = self.candidate([self.entries[0], first, second])
        artifact = self.root / ".artifacts" / "ambiguous.json"
        report = migration.plan(self.root, candidate, output=artifact)
        self.assertFalse(report["ok"])
        before = queue.business_rows(queue.database_path(self.root))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "ambiguous/unmapped"):
            migration.apply(self.root, artifact, candidate_catalog=candidate)
        self.assertEqual(before, queue.business_rows(queue.database_path(self.root)))

    def test_transaction_rollback_preserves_projection(self):
        candidate = self.candidate([self.replace(self.entries[0], target="new target"), *self.entries[1:]])
        artifact = self.root / ".artifacts" / "rollback.json"
        migration.plan(self.root, candidate, output=artifact)
        before = queue.business_rows(queue.database_path(self.root))
        with sqlite3.connect(queue.database_path(self.root)) as connection:
            connection.execute("CREATE TRIGGER fixture_abort BEFORE INSERT ON reconciliation "
                               "BEGIN SELECT RAISE(ABORT, 'fixture rollback'); END")
        # The trigger makes the real SQLite transaction abort.  The schema
        # check is patched only for this negative fixture because the trigger
        # is intentionally not part of the three-table production schema.
        with mock.patch.object(queue, "_schema_check", return_value=None):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "rolled back|fixture rollback"):
                migration.apply(self.root, artifact, candidate_catalog=candidate)
        self.assertEqual(before, queue.business_rows(queue.database_path(self.root)))

    def _publish_surface_batch(self, *, repair: bool, blocked: bool = False,
                                entry_index: int = 0, batch_name: str | None = None) -> str:
        """Create one real, current-consumer batch publication in the fixture."""
        if repair and blocked:
            raise AssertionError("repair and blocked are mutually exclusive")
        source_path = self.root / "source-evidence.txt"
        source_path.write_text("public source evidence", encoding="utf-8")
        if subprocess.check_output(["git", "status", "--porcelain"], cwd=self.root, text=True):
            self.commit("source evidence")
        queue.rebuild(self.root)
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        entry = self.entries[entry_index]
        revision = entry["entry_revision_identity"]
        batch_id = batch_name or ("repair" if repair else "done")
        surface_entry = {key: entry[key] for key in wp1.surface.ENTRY_KEYS}
        if entry["rules_version"] == wp1.surface.IDENTITY_RULES_V2:
            surface_entry["args_order"] = entry["risk"]["args_order"]
        payload = {"contract": wp1.surface.CONTRACT,
                   "fixed_source_identity": entry["fixed_source_identity"],
                   "terminology_snapshot": entry["terminology_snapshot_sha256"],
                   "rules_version": entry["rules_version"], "rendered_briefing": "fixture",
                   "entries": [surface_entry]}
        candidate_identity = hashlib.sha256(wp1.surface.canonical_bytes(payload)).hexdigest()
        input_raw = wp1.surface.canonical_bytes({"candidate_identity": candidate_identity, "payload": payload})
        verdict = "ISSUE" if repair or blocked else "OK"
        output_value = {"contract": wp1.surface.CONTRACT, "candidate_identity": candidate_identity,
                        "results": [{"entry_revision_identity": revision, "verdict": verdict}]}
        if repair or blocked:
            output_value["results"][0]["observation"] = "repair fixture" if repair else "blocked fixture"
        output_raw = wp1.surface.canonical_bytes(output_value)
        input_hash, output_hash = hashlib.sha256(input_raw).hexdigest(), hashlib.sha256(output_raw).hexdigest()
        deep_payload = {"contract": "translation_contextual_v2", "ordered_revision_keys": [revision],
                        "translation_snapshot": [{"revision_key": revision, "source": entry["source"],
                                                   "target": entry["target"]}],
                        "fixed_source_identity": entry["fixed_source_identity"],
                        "terminology_snapshot": entry["terminology_snapshot_sha256"],
                        "bounded_context": [{"revision_key": revision, "context": "fixture"}],
                        "rendered_briefing": "fixture"}
        deep_identity = hashlib.sha256(wp1.surface.canonical_bytes(deep_payload)).hexdigest()
        deep_input_raw = wp1.surface.canonical_bytes({"candidate_identity": deep_identity,
                                                       "payload": deep_payload})
        deep_output_value = {"contract": "translation_contextual_v2",
            "candidate_identity": deep_identity,
            "verdicts": [{"revision_key": revision,
                          "verdict": "ISSUE" if blocked else "OK"}]}
        if blocked:
            deep_output_value["verdicts"][0]["observation"] = "blocked deep fixture"
        deep_output_raw = wp1.surface.canonical_bytes(deep_output_value)
        deep_input_hash = hashlib.sha256(deep_input_raw).hexdigest()
        deep_output_hash = hashlib.sha256(deep_output_raw).hexdigest()
        result = {"schema_version": 1, "source": entry["source"], "target": entry["target"],
                  "source_tag": entry["source_tag"], "normalized_path": entry["normalized_path"],
                  "call_locator": entry["call_locator"], "logical_entry_identity": entry["logical_entry_identity"],
                  "entry_revision_identity": revision,
                  "surface_verdict": verdict,
                  "surface_observation": "repair fixture" if repair else ("blocked fixture" if blocked else None),
                  "deep_verdict": "ISSUE" if blocked else ("OK" if repair else None),
                  "deep_observation": "blocked deep fixture" if blocked else None,
                  "input_sha256": input_hash, "output_sha256": output_hash,
                  "final_state": "repair_required" if repair else ("blocked" if blocked else "done"),
                  "completion_level": "deep_reviewed" if repair or blocked else "surface_only"}
        results_raw = wp1._jsonl([result])
        if repair or blocked:
            observation_text = "repair fixture" if repair else "blocked fixture"
            observation_identity = catalog.observation_identity(wp1.surface.CONTRACT, revision, verdict,
                                                                  observation_text)
            snapshot_raw = source_path.read_bytes()
            decision = {"schema_version": 1, "entry_revision_identity": revision,
                        "observation_contract": wp1.surface.CONTRACT,
                        "observation_identity": observation_identity,
                        "observation_sha256": hashlib.sha256(observation_text.encode()).hexdigest(),
                        "disposition": "confirmed" if repair else "pending", "evidence_path": "source-evidence.txt",
                        "evidence_commit": base if repair else None,
                        "evidence_snapshot": {"sha256": hashlib.sha256(snapshot_raw).hexdigest(),
                                               "content": snapshot_raw.decode("utf-8")} if repair else None,
                        "conclusion": "fixture repair" if repair else "fixture blocked",
                        "repair_required": repair}
            decisions = [decision]
            if blocked:
                deep_observation = "blocked deep fixture"
                deep_decision = dict(decision)
                deep_decision.update({
                    "observation_contract": "translation_contextual_v2",
                    "observation_identity": catalog.observation_identity(
                        "translation_contextual_v2", revision, "ISSUE", deep_observation),
                    "observation_sha256": hashlib.sha256(deep_observation.encode()).hexdigest()})
                decisions.append(deep_decision)
            adjudications_raw = wp1._jsonl(decisions)
        else:
            adjudications_raw = b""
        gates_raw = wp1.canonical_bytes({"schema_version": 1, "commands": []})
        batch_root = self.root / f"evidence/production-review-v2-lite/batches/{batch_id}"
        raw_root = batch_root / "raw/translation_surface_screen_v1"
        deep_root = batch_root / "raw/translation_contextual_v2"
        raw_root.mkdir(parents=True, exist_ok=True)
        deep_root.mkdir(parents=True, exist_ok=True)
        (raw_root / "input.json").write_bytes(input_raw)
        (raw_root / "output.json").write_bytes(output_raw)
        if repair or blocked:
            (deep_root / "input.json").write_bytes(deep_input_raw)
            (deep_root / "output.json").write_bytes(deep_output_raw)
        adapter_refs = [{"contract": wp1.surface.CONTRACT,
            "input_path": f"evidence/production-review-v2-lite/batches/{batch_id}/raw/translation_surface_screen_v1/input.json",
            "input_sha256": input_hash, "output_path": f"evidence/production-review-v2-lite/batches/{batch_id}/raw/translation_surface_screen_v1/output.json",
            "output_sha256": output_hash, "candidate_identity": candidate_identity}]
        if repair or blocked:
            adapter_refs.append({"contract": "translation_contextual_v2",
                "input_path": f"evidence/production-review-v2-lite/batches/{batch_id}/raw/translation_contextual_v2/input.json",
                "input_sha256": deep_input_hash, "output_path": f"evidence/production-review-v2-lite/batches/{batch_id}/raw/translation_contextual_v2/output.json",
                "output_sha256": deep_output_hash, "candidate_identity": deep_identity})
        batch_manifest = {"schema_version": 1, "kind": "production_review_v2_lite_batch_v1",
                          "catalog_id": self.catalog_id,
                          "policy_sha256": hashlib.sha256(
                              (self.root / catalog.POLICY_PATH).read_bytes()).hexdigest(),
                          "base_commit": base, "batch_id": batch_id, "attempt": 1,
                          "ordered_revisions": [revision],
                          "ordered_revisions_sha256": hashlib.sha256(wp1.canonical_bytes([revision])).hexdigest(),
                          "entry_snapshots_sha256": hashlib.sha256(wp1.canonical_bytes([entry])).hexdigest(),
                          "adapter_refs": adapter_refs,
                          "results_sha256": hashlib.sha256(results_raw).hexdigest(),
                          "adjudications_sha256": hashlib.sha256(adjudications_raw).hexdigest(),
                          "gates_sha256": hashlib.sha256(gates_raw).hexdigest(),
                          "producer_task_ids": ["fixture"], "recorded_at": "2026-09-02T01:02:03Z",
                          "recorded_by": "fixture"}
        (batch_root / "results.jsonl").write_bytes(results_raw)
        (batch_root / "adjudications.jsonl").write_bytes(adjudications_raw)
        (batch_root / "gates.json").write_bytes(gates_raw)
        (batch_root / "manifest.json").write_bytes(wp1.canonical_bytes(batch_manifest))
        publication = self.commit("repair evidence" if repair else ("blocked evidence" if blocked else "done evidence"))
        queue.rebuild(self.root)
        return publication

    def test_v1_to_v2_boundary_revalidates_once_without_inheriting_durable_state(self):
        def publish_candidate(candidate: Path, artifact: Path, report: dict, message: str) -> str:
            candidate_files = catalog.ordinary_tree(candidate)
            shutil.rmtree(candidate)
            for relative, raw in candidate_files.items():
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            migration_path = self.root / report["target_path"]
            migration_path.parent.mkdir(parents=True, exist_ok=True)
            migration_path.write_bytes(artifact.read_bytes())
            return self.commit(message)

        # Establish exact historical v1 as the current catalog, then commit a
        # durable result against it before crossing the one-time rules boundary.
        v1_entries = [self.replace(row, rules_version=catalog.FROZEN_RULES_VERSION)
                      for row in self.entries]
        v1_candidate = self.candidate(v1_entries, rules=catalog.FROZEN_RULES_VERSION)
        v1_artifact = self.root / ".artifacts" / "to-v1.json"
        v1_report = migration.plan(self.root, v1_candidate, output=v1_artifact)
        migration.apply(self.root, v1_artifact, candidate_catalog=v1_candidate)
        publish_candidate(v1_candidate, v1_artifact, v1_report, "historical v1 boundary")
        self.entries = v1_entries
        self.catalog_id = v1_report["new_catalog_id"]
        queue.rebuild(self.root)
        self._publish_surface_batch(repair=False, entry_index=0, batch_name="v1-done")
        durable_revision = self.entries[0]["entry_revision_identity"]
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][2], "done")

        v2_entries = [self.replace(row, rules_version=catalog.RULES_VERSION)
                      for row in self.entries]
        v2_candidate = self.candidate(v2_entries, rules=catalog.RULES_VERSION)
        v2_artifact = self.root / ".artifacts" / "v1-to-v2.json"
        report = migration.plan(self.root, v2_candidate, output=v2_artifact)
        self.assertEqual(report["dispositions"], {"revision_changed": len(self.entries)})
        planned = wp1.parse_canonical_object(v2_artifact.read_bytes(), "v1-to-v2 migration")
        self.assertTrue(all(
            row["disposition"] == "revision_changed" and row["reason"] == "rules_changed"
            for row in planned["rows"]
        ))
        migration.apply(self.root, v2_artifact, candidate_catalog=v2_candidate)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0], [])
        publication = publish_candidate(
            v2_candidate, v2_artifact, report, "one-time v1 to v2 revalidation")

        queue.rebuild(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0], [])
        queue.database_path(self.root).unlink()
        queue.rebuild(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0], [])

        subprocess.run(["git", "revert", "--no-edit", publication], cwd=self.root, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        queue.rebuild(self.root)
        reverted, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[0]: row[2] for row in reverted}, {durable_revision: "done"})

    def test_progress_changed_reverted_successor_requires_actual_new_review(self):
        self._publish_surface_batch(repair=False, entry_index=0, batch_name="original-review")
        original = copy.deepcopy(self.entries)
        changed = [self.replace(original[0], target="changed target"), *original[1:]]
        # Returning the entry target while changing provenance keeps catalog
        # identities distinct: this is a migration chain, not git revert.
        reverted = [self.replace(row, terminology_snapshot_sha256="f" * 64) for row in original]
        for index, entries in enumerate((changed, reverted)):
            candidate = self.candidate(entries)
            artifact = self.root / ".artifacts" / f"progress-{index}.json"
            planned = migration.plan(self.root, candidate, output=artifact)
            migration.apply(self.root, artifact, candidate_catalog=candidate)
            files = catalog.ordinary_tree(candidate)
            shutil.rmtree(candidate)
            for relative, raw in files.items():
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            path = self.root / planned["target_path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(artifact.read_bytes())
            self.commit(f"progress boundary {index}")
            self.entries = entries
            self.catalog_id = queue._catalog_from_tree(self.root, "HEAD")[0]["catalog_id"]
            progress = queue.rebuild(self.root)["progress"]
            self.assertEqual(progress["metrics"]["surface_covered"]["count"], 0)
            self.assertEqual(progress["metrics"]["historical_revision_invalidated"]["count"], 1)
            self.assertEqual(progress["invalidated_without_current_review"], 1)
        self.assertEqual(self.entries[0]["entry_revision_identity"], original[0]["entry_revision_identity"])
        self._publish_surface_batch(repair=False, entry_index=0, batch_name="new-review")
        progress = queue.rebuild(self.root)["progress"]
        self.assertEqual(progress["metrics"]["surface_covered"]["count"], 1)
        self.assertEqual(progress["metrics"]["historical_revision_invalidated"]["count"], 1)
        self.assertEqual(progress["invalidated_without_current_review"], 0)

    def test_rebuild_retains_unchanged_done_repair_blocked_across_boundary_delete_revert(self):
        self._publish_surface_batch(repair=False, entry_index=0, batch_name="done-state")
        self._publish_surface_batch(repair=True, entry_index=1, batch_name="repair-state")
        self._publish_surface_batch(repair=False, blocked=True, entry_index=2, batch_name="blocked-state")
        terminology = "f" * 64
        term_only_entries = [self.replace(row, terminology_snapshot_sha256=terminology)
                             for row in self.entries]
        self.assertEqual([row["entry_revision_identity"] for row in term_only_entries],
                         [row["entry_revision_identity"] for row in self.entries])
        candidate = self.candidate(term_only_entries, terminology=terminology)
        artifact = self.root / ".artifacts" / "terminology-only-states.json"
        report = migration.plan(self.root, candidate, output=artifact)
        migration.apply(self.root, artifact, candidate_catalog=candidate)
        candidate_files = catalog.ordinary_tree(candidate)
        shutil.rmtree(candidate)
        for relative, raw in candidate_files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        migration_path = self.root / report["target_path"]
        migration_path.parent.mkdir(parents=True, exist_ok=True)
        migration_path.write_bytes(artifact.read_bytes())
        publication = self.commit("terminology-only states catalog boundary")
        queue.rebuild(self.root)
        expected_states = {
            self.entries[0]["entry_revision_identity"]: "done",
            self.entries[1]["entry_revision_identity"]: "repair_required",
            self.entries[2]["entry_revision_identity"]: "blocked",
        }
        overrides, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[0]: row[2] for row in overrides}, expected_states)
        queue.database_path(self.root).unlink()
        queue.rebuild(self.root)
        rebuilt, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[0]: row[2] for row in rebuilt}, expected_states)
        subprocess.run(["git", "revert", "--no-edit", publication], cwd=self.root, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        queue.rebuild(self.root)
        reverted, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[0]: row[2] for row in reverted}, expected_states)

    def test_two_successive_unchanged_boundaries_preserve_all_states_on_rebuild_delete_and_revert(self):
        self._publish_surface_batch(repair=False, entry_index=0, batch_name="history-done")
        self._publish_surface_batch(repair=True, entry_index=1, batch_name="history-repair")
        self._publish_surface_batch(repair=False, blocked=True, entry_index=2, batch_name="history-blocked")

        def publish_boundary(extra_suffix: str, message: str, *, schema_version: int = 2) -> tuple[dict, str]:
            rows = [*self.entries, self.entry(extra_suffix, section=extra_suffix)]
            candidate = self.candidate(rows)
            artifact = self.root / ".artifacts" / f"{extra_suffix}-migration.json"
            report = migration.plan(self.root, candidate, output=artifact)
            if schema_version == 1:
                stored = wp1.parse_canonical_object(artifact.read_bytes(), "planned sparse migration")
                old_summary = {"catalog_id": stored["old_catalog_id"],
                    "manifest_sha256": stored["old_manifest_sha256"],
                    "entries_sha256": stored["old_entries_sha256"],
                    "exclusions_sha256": stored["old_exclusions_sha256"], "counts": stored["old_counts"]}
                new_summary = {"catalog_id": stored["new_catalog_id"],
                    "manifest_sha256": stored["new_manifest_sha256"],
                    "entries_sha256": stored["new_entries_sha256"],
                    "exclusions_sha256": stored["new_exclusions_sha256"], "counts": stored["new_counts"]}
                stored = migration._build_migration(
                    stored["base_commit"], stored["base_tree"], old_summary, self.entries,
                    new_summary, rows, recorded_at=stored["recorded_at"],
                    recorded_by=stored["recorded_by"], schema_version=1)
                artifact.write_bytes(wp1.canonical_bytes(stored))
                report = migration._report(stored, path=artifact)
            migration.apply(self.root, artifact, candidate_catalog=candidate)
            candidate_files = catalog.ordinary_tree(candidate)
            shutil.rmtree(candidate)
            for relative, raw in candidate_files.items():
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            migration_path = self.root / report["target_path"]
            migration_path.parent.mkdir(parents=True, exist_ok=True)
            migration_path.write_bytes(artifact.read_bytes())
            publication = self.commit(message)
            self.catalog_id = report["new_catalog_id"]
            return report, publication

        first, _first_publication = publish_boundary(
            "first-generation", "first historical-full unchanged boundary", schema_version=1)
        queue.rebuild(self.root)
        with mock.patch.object(migration, "_validate_live_repair_preimage"):
            repair = migration.repair_preflight(self.root, "history-repair")
        self.assertTrue(repair["ok"])
        # A second batch is based on the first successor catalog, so the
        # second boundary has a real descendant evidence history to replay.
        self._publish_surface_batch(repair=False, entry_index=0, batch_name="successor-done")
        second, second_publication = publish_boundary("second-generation", "second unchanged boundary")

        expected_states = {
            self.entries[0]["entry_revision_identity"]: "done",
            self.entries[1]["entry_revision_identity"]: "repair_required",
            self.entries[2]["entry_revision_identity"]: "blocked",
        }
        queue.rebuild(self.root)
        rebuilt, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[0]: row[2] for row in rebuilt}, expected_states)
        self.assertEqual(first["new_catalog_id"], second["old_catalog_id"])

        queue.database_path(self.root).unlink()
        queue.rebuild(self.root)
        deleted_rebuild, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[0]: row[2] for row in deleted_rebuild}, expected_states)

        subprocess.run(["git", "revert", "--no-edit", second_publication], cwd=self.root,
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        queue.rebuild(self.root)
        reverted, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[0]: row[2] for row in reverted}, expected_states)

    def test_rebuild_retains_unchanged_committed_done_across_apply_delete_and_revert(self):
        self._publish_surface_batch(repair=False)
        candidate = self.candidate([self.entries[0], self.replace(self.entries[1], target="revised target"), self.entries[2]])
        artifact = self.root / ".artifacts" / "unchanged-done.json"
        report = migration.plan(self.root, candidate, output=artifact)
        migration.apply(self.root, artifact, candidate_catalog=candidate)
        before = queue.business_rows(queue.database_path(self.root))[0]
        self.assertEqual(before[0][0], self.entries[0]["entry_revision_identity"])
        self.assertEqual(before[0][2], "done")
        candidate_files = catalog.ordinary_tree(candidate)
        shutil.rmtree(candidate)
        for relative, raw in candidate_files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        migration_path = self.root / report["target_path"]
        migration_path.parent.mkdir(parents=True, exist_ok=True)
        migration_path.write_bytes(artifact.read_bytes())
        publication = self.commit("unchanged catalog boundary")
        queue.rebuild(self.root)
        overrides, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual(overrides[0][0], self.entries[0]["entry_revision_identity"])
        self.assertEqual(overrides[0][2], "done")
        self.assertEqual(overrides[0][3], "done")
        self.assertEqual(publication, subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip())
        subprocess.run(["git", "revert", "--no-edit", publication], cwd=self.root, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        queue.rebuild(self.root)
        reverted, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual(reverted[0][0], self.entries[0]["entry_revision_identity"])
        self.assertEqual(reverted[0][2], "done")

    def _live_preimage_fixture(self):
        expected = copy.deepcopy(self._catalog_manifest())
        live_manifest_raw = b"live fixture manifest"
        expected["manifest_sha256"] = hashlib.sha256(live_manifest_raw).hexdigest()
        contract = self.root / "tools/i18nlib/locale_model.py"
        contract.parent.mkdir(parents=True, exist_ok=True)
        contract.write_bytes(b"live loader")
        expected["loader_contract_sha256"] = hashlib.sha256(b"live loader").hexdigest()
        manifest = SimpleNamespace(root=self.root, raw_bytes=live_manifest_raw)
        occurrences = [wp1.make_occurrence("tome", "tome.lua", index, {
            "function_name": "t", "section": row["section"], "source": row["source"],
            "target": row["target"], "source_tag": row["source_tag"], "args_order": None,
            "special": None}) for index, row in enumerate(self.entries)]
        live_entries, live_exclusions = catalog.formal_rows(
            occurrences, terminology=expected["terminology_snapshot_sha256"],
            sources=expected["source_identities"])
        return expected, live_entries, live_exclusions, manifest, occurrences

    def _catalog_manifest(self):
        manifest_raw = (self.root / f"{catalog.CATALOG_PREFIX}/manifest.json").read_bytes()
        return wp1.parse_canonical_object(manifest_raw, "catalog manifest")

    def test_live_repair_preimage_rejects_missing_call_and_target_drift(self):
        expected, entries, exclusions, manifest, occurrences = self._live_preimage_fixture()
        runtime = mock.Mock(); runtime.doctor.return_value = {"lua_version": expected["lua_runtime"]}
        patches = [
            mock.patch.object(migration.catalog, "LuaRuntime", return_value=runtime),
            mock.patch.object(migration.wp1, "source_identities_from_manifest",
                              return_value=expected["source_identities"]),
            mock.patch.object(migration.wp1, "terminology_snapshot",
                              return_value=expected["terminology_snapshot_sha256"]),
        ]
        for patch in patches: patch.start()
        self.addCleanup(lambda: [patch.stop() for patch in patches])
        with mock.patch.object(migration.wp1, "load_occurrences", return_value=occurrences[:-1]):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "call/preimage/identity drift"):
                migration._validate_live_repair_preimage(self.root, expected, entries, exclusions, manifest)
        drifted = list(occurrences)
        drifted[0] = wp1.make_occurrence("tome", "tome.lua", 0, {
            "function_name": "t", "section": occurrences[0]["section"], "source": occurrences[0]["source"],
            "target": "uncommitted drift", "source_tag": occurrences[0]["source_tag"],
            "args_order": None, "special": None})
        with mock.patch.object(migration.wp1, "load_occurrences", return_value=drifted):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "call/preimage/identity drift"):
                migration._validate_live_repair_preimage(self.root, expected, entries, exclusions, manifest)

    def test_repair_preflight_rejects_later_done_winner_for_named_old_batch(self):
        self._publish_surface_batch(repair=True)
        self._publish_surface_batch(repair=False)
        with mock.patch.object(migration, "_validate_live_repair_preimage"):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "current durable winners"):
                migration.repair_preflight(self.root, "repair")

    def test_rebuild_reads_latest_reconciliation_and_git_revert_restores_old_projection(self):
        candidate = self.candidate([self.replace(self.entries[0], target="revised target"), *self.entries[1:]])
        artifact = self.root / ".artifacts" / "boundary.json"
        report = migration.plan(self.root, candidate, output=artifact)
        migration.apply(self.root, artifact, candidate_catalog=candidate)
        candidate_files = catalog.ordinary_tree(candidate)
        shutil.rmtree(candidate)
        for relative, raw in candidate_files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        migration_path = self.root / report["target_path"]
        migration_path.parent.mkdir(parents=True, exist_ok=True)
        migration_path.write_bytes(artifact.read_bytes())
        publication = self.commit("catalog boundary")
        queue.rebuild(self.root)
        overrides, reconciliation, meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual(publication, subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip())
        self.assertEqual(overrides, [])
        self.assertEqual(meta[2], report["new_catalog_id"])
        self.assertEqual(len(reconciliation), len(self.entries))
        self.assertEqual(sum(row[4] == "revision_changed" for row in reconciliation), 1)
        subprocess.run(["git", "revert", "--no-edit", publication], cwd=self.root, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        queue.rebuild(self.root)
        _overrides, reverted_reconciliation, reverted_meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual(reverted_meta[2], self.catalog_id)
        self.assertEqual(reverted_reconciliation, [])

    def test_done_parent_is_not_inherited_by_revision_successor(self):
        self._publish_surface_batch(repair=False)
        candidate = self.candidate([self.replace(self.entries[0], target="new target"), *self.entries[1:]])
        artifact = self.root / ".artifacts" / "done-parent.json"
        migration.plan(self.root, candidate, output=artifact)
        old_revision = self.entries[0]["entry_revision_identity"]
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][0], old_revision)
        migration.apply(self.root, artifact, candidate_catalog=candidate)
        overrides, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertFalse(any(row[0] == old_revision or row[2] == "done" for row in overrides))

    def test_repair_preflight_binds_committed_winner_and_rejects_preimage_drift(self):
        publication = self._publish_surface_batch(repair=True)
        # This fixture has no real version manifest/Lua bridge; the dedicated
        # live-preimage tests below exercise that gate with the existing loader
        # seam.  Keep this test focused on committed evidence/workset binding.
        with mock.patch.object(migration, "_validate_live_repair_preimage"):
            report = migration.repair_preflight(self.root, "repair")
        self.assertTrue(report["ok"])
        workset = wp1.parse_canonical_object(Path(report["workset"]).read_bytes(), "repair workset")
        self.assertEqual(workset["evidence_commit"], publication)
        self.assertEqual(len(workset["items"]), 1)
        item = workset["items"][0]
        self.assertEqual(item["target_preimage_sha256"], self.entries[0]["target_sha256"])
        self.assertEqual(item["proposed_successor_input"]["parent_entry_revision_identity"],
                         self.entries[0]["entry_revision_identity"])
        entries_path = self.root / catalog.CATALOG_PREFIX / "entries.jsonl"
        entries_path.write_bytes(entries_path.read_bytes().replace(b"target 0", b"drifted target 0", 1))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "clean|preimage"):
            migration.repair_preflight(self.root, "repair")

    def test_rebuild_queues_repaired_successor_without_replaying_old_batch(self):
        self._publish_surface_batch(repair=True)
        candidate = self.candidate([self.replace(self.entries[0], target="repaired target"), *self.entries[1:]])
        artifact = self.root / ".artifacts" / "successor.json"
        report = migration.plan(self.root, candidate, output=artifact)
        migration.apply(self.root, artifact, candidate_catalog=candidate)
        candidate_files = catalog.ordinary_tree(candidate)
        shutil.rmtree(candidate)
        for relative, raw in candidate_files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        migration_path = self.root / report["target_path"]
        migration_path.parent.mkdir(parents=True, exist_ok=True)
        migration_path.write_bytes(artifact.read_bytes())
        self.commit("repaired catalog")
        queue.rebuild(self.root)
        overrides, reconciliation, meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual(overrides, [])
        self.assertEqual(meta[2], report["new_catalog_id"])
        changed = next(row for row in reconciliation if row[1] == self.entries[0]["entry_revision_identity"])
        self.assertEqual((changed[4], changed[5]), ("revision_changed", "target_changed"))


if __name__ == "__main__":
    unittest.main()
