from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.i18nlib import production_review as p

STAMP = "2026-08-30T01:02:03Z"
BY = "tester"
ROOT = Path(__file__).resolve().parents[2]
MANIFEST_COMPONENTS = ["engine", "boot", "tome", "example", "example-realtime", "addon-dev",
                       "ashes-urhrok", "cults", "items-vault", "orcs", "possessors"]
SOURCES = {component: "commit:" + "4" * 40 for component in p.IN_SCOPE_COMPONENTS}


def occurrence(component="tome", source="Source", target="甲", ordinal=0):
    return p.make_occurrence(component, "mod.lua", ordinal, {
        "function_name": "t", "section": "s", "source": source, "target": target,
        "source_tag": None, "args_order": None, "special": None,
    })


def snapshot(occurrences=None):
    occs = occurrences or [occurrence(), occurrence("example", "Other", "乙")]
    return p.build_locator_snapshot_from_occurrences(
        occs, manifest_sha256="1" * 64,
        manifest_component_ordinals=p._component_ordinals(MANIFEST_COMPONENTS),
        loader_contract_path="tools/i18nlib/locale_model.py",
        loader_contract_sha256="2" * 64, lua_runtime="Lua 5.1",
        lua_build="LuaJIT 2.1", recorded_at=STAMP, recorded_by=BY,
    )


def chain(occurrences=None):
    lm, ob, lb = snapshot(occurrences)
    lm_raw = p.canonical_bytes(lm)
    cm, eb, xb = p.build_catalog(
        lm, ob, lb, locator_manifest_raw=lm_raw,
        terminology_snapshot_id="3" * 64, source_identities=SOURCES,
        recorded_at=STAMP, recorded_by=BY,
    )
    cm_raw = p.canonical_bytes(cm)
    entries, exclusions = p.check_catalog(
        cm, eb, xb, locator_manifest=lm, locator_manifest_raw=lm_raw,
        occurrences_raw=ob, locators_raw=lb,
        expected_terminology_snapshot_id="3" * 64,
        expected_source_identities=SOURCES,
    )
    policy = p.build_shadow_policy(
        cm, lm, catalog_manifest_raw=cm_raw,
        terminology_snapshot_id="3" * 64, source_identities=SOURCES,
        recorded_at=STAMP, recorded_by=BY,
    )
    group, events, checkpoint = p.build_shadow_journal(
        entries, exclusions, cm, policy, catalog_manifest_raw=cm_raw,
        locator_manifest=lm, recorded_at=STAMP, recorded_by=BY,
    )
    return {
        "lm": lm, "lm_raw": lm_raw, "ob": ob, "lb": lb,
        "cm": cm, "cm_raw": cm_raw, "eb": eb, "xb": xb,
        "entries": entries, "exclusions": exclusions, "policy": policy,
        "group": group, "events": events, "checkpoint": checkpoint,
    }


def check_journal(data, events=None, checkpoint=None):
    return p.check_shadow_journal(
        data["group"], p._jsonl(events if events is not None else data["events"]),
        checkpoint if checkpoint is not None else data["checkpoint"],
        catalog=data["cm"], catalog_manifest_raw=data["cm_raw"],
        locator_manifest=data["lm"], entries=data["entries"],
        exclusions=data["exclusions"], policy=data["policy"],
    )


class ProductionReviewUnitTests(unittest.TestCase):
    def test_snapshot_is_self_contained_and_exact(self):
        manifest, occurrences, locators = snapshot()
        with mock.patch.object(p, "load_occurrences", side_effect=AssertionError("live loader read")):
            checked_occ, checked_loc = p.check_locator_snapshot(manifest, occurrences, locators)
        self.assertEqual((len(checked_occ), len(checked_loc)), (2, 2))
        self.assertEqual(set(checked_occ[0]), p.OCCURRENCE_KEYS)
        self.assertEqual(set(checked_loc[0]), p.LOCATOR_ROW_KEYS)
        self.assertEqual([row["component"] for row in manifest["manifest_component_ordinals"]],
                         MANIFEST_COMPONENTS)
        for raw_name, raw in (("occurrences", occurrences), ("locators", locators)):
            rows = p.parse_jsonl(raw, raw_name)
            rows[0]["extra"] = True
            changed = p._jsonl(rows)
            bad = dict(manifest)
            bad[f"{raw_name}_sha256"] = hashlib.sha256(changed).hexdigest()
            bad["locator_snapshot_id"] = p.object_id("locator-snapshot", bad, "locator_snapshot_id")
            with self.assertRaises(p.ProductionReviewError):
                p.check_locator_snapshot(bad, changed if raw_name == "occurrences" else occurrences,
                                         changed if raw_name == "locators" else locators)

    def test_canonical_object_and_jsonl_fail_closed(self):
        self.assertEqual(p.parse_canonical_object(b'{"a":1}', "object"), {"a": 1})
        for raw in (b'{"a":1}\n', b'{"a":1,"a":1}', b'{"a":NaN}', b'\xff',
                    b'{"a":"\\ud800"}'):
            with self.subTest(raw=raw), self.assertRaises(p.ProductionReviewError):
                p.parse_canonical_object(raw, "object")
        self.assertEqual(p.parse_jsonl(b'{"a":1}\n', "rows"), [{"a": 1}])
        for raw in (b'{"a":1}', b'{"a": 1}\n', b'{"a":1}\n\n'):
            with self.subTest(raw=raw), self.assertRaises(p.ProductionReviewError):
                p.parse_jsonl(raw, "rows")

    def test_allocation_aliases_rejected(self):
        allocation = p.make_allocation(occurrence())
        alias = dict(allocation)
        alias["path"] = alias.pop("translation_path")
        alias["function"] = alias.pop("function_name")
        with self.assertRaises(p.ProductionReviewError):
            p.make_locator_row(occurrence(), alias)

    def test_catalog_exact_shapes_live_inputs_and_raw_parent(self):
        data = chain()
        self.assertEqual(set(data["entries"][0]), p.CATALOG_ENTRY_KEYS)
        self.assertEqual(data["exclusions"][0]["reason_code"],
                         "outside_initial_six_component_scope")
        self.assertEqual(data["cm"]["locator_manifest_sha256"],
                         hashlib.sha256(data["lm_raw"]).hexdigest())
        bad = copy.deepcopy(data["exclusions"])
        bad[0]["detail"] = "x"
        with self.assertRaises(p.ProductionReviewError):
            p.check_catalog(data["cm"], data["eb"], p._jsonl(bad),
                            locator_manifest=data["lm"], locator_manifest_raw=data["lm_raw"],
                            occurrences_raw=data["ob"], locators_raw=data["lb"])
        with self.assertRaisesRegex(p.ProductionReviewError, "terminology snapshot drift"):
            p.check_catalog(data["cm"], data["eb"], data["xb"],
                            locator_manifest=data["lm"], locator_manifest_raw=data["lm_raw"],
                            occurrences_raw=data["ob"], locators_raw=data["lb"],
                            expected_terminology_snapshot_id="0" * 64)
        pretty = json.dumps(data["lm"], sort_keys=True).encode()
        with self.assertRaises(p.ProductionReviewError):
            p.check_catalog(data["cm"], data["eb"], data["xb"],
                            locator_manifest=data["lm"], locator_manifest_raw=pretty,
                            occurrences_raw=data["ob"], locators_raw=data["lb"])

    def test_catalog_metadata_must_match_locator_before_publication_or_check(self):
        lm, ob, lb = snapshot()
        lm_raw = p.canonical_bytes(lm)
        with self.assertRaisesRegex(p.ProductionReviewError, "metadata must match"):
            p.build_catalog(lm, ob, lb, locator_manifest_raw=lm_raw,
                terminology_snapshot_id="3" * 64, source_identities=SOURCES,
                recorded_at="2026-08-30T01:02:04Z", recorded_by=BY)
        data = chain()
        bad = dict(data["cm"], recorded_by="other")
        bad["catalog_id"] = p.object_id("catalog", bad, "catalog_id")
        with self.assertRaisesRegex(p.ProductionReviewError, "metadata must match"):
            p.check_catalog(bad, data["eb"], data["xb"],
                locator_manifest=data["lm"], locator_manifest_raw=data["lm_raw"],
                occurrences_raw=data["ob"], locators_raw=data["lb"])

    def test_policy_binds_exact_catalog_manifest_bytes(self):
        data = chain()
        p.check_shadow_policy(data["policy"], catalog=data["cm"],
                              catalog_manifest_raw=data["cm_raw"],
                              locator_manifest=data["lm"])
        self.assertEqual(data["policy"]["catalog_manifest_sha256"],
                         hashlib.sha256(data["cm_raw"]).hexdigest())
        for change in ({"catalog_id": "0" * 64}, {"priority_tuple": []},
                       {"batch_size": 81}, {"recorded_by": "other"}):
            bad = dict(data["policy"], **change)
            bad["shadow_policy_id"] = p.object_id("shadow-queue-policy", bad,
                                                   "shadow_policy_id")
            with self.assertRaises(p.ProductionReviewError):
                p.check_shadow_policy(bad, catalog=data["cm"],
                                      catalog_manifest_raw=data["cm_raw"],
                                      locator_manifest=data["lm"])

    def test_journal_replays_through_real_ledger_and_summary_can_be_small(self):
        data = chain()
        with mock.patch("tools.translation_review_ledger.replay", wraps=p.ledger.replay) as replay:
            result = check_journal(data)
            replay.assert_called()
        self.assertEqual(result["state_counts"], {"queued": 1})
        self.assertEqual(len(result["queued_revisions"]), 1)

    def test_multi_event_semantic_mutations_survive_raw_hash_rebinding(self):
        data = chain([occurrence("tome", f"Source {i}", "甲", i) for i in range(3)])

        def rebound(mutator, *, forged_genesis=False):
            events = copy.deepcopy(data["events"])
            mutator(events)
            previous = "0" * 64 if forged_genesis else None
            for event in events:
                event["previous_event_hash"] = previous
                event["event_id"] = p.object_id("journal-event", event, "event_id")
                previous = event["event_id"]
            raw = p._jsonl(events)
            cp = copy.deepcopy(data["checkpoint"])
            cp["events_sha256"] = hashlib.sha256(raw).hexdigest()
            cp["last_event_hash"] = previous
            cp["checkpoint_id"] = p.object_id("journal-checkpoint", cp, "checkpoint_id")
            return events, cp

        mutations = [
            (lambda events: events[1].__setitem__("attempt", 1), False),
            (lambda events: events[1].__setitem__("batch_id", "not-null"), False),
            (lambda events: None, True),
            (lambda events: events[1]["record"].__setitem__("from_state", "queued"), False),
            (lambda events: events[1]["record"].__setitem__("logical_entry_identity", "0" * 64), False),
        ]
        for mutation, forged_genesis in mutations:
            events, cp = rebound(mutation, forged_genesis=forged_genesis)
            with self.subTest(mutation=mutation), self.assertRaises(p.ProductionReviewError):
                check_journal(data, events, cp)

    def test_batch_checkpoint_priority_and_conservation(self):
        occurrences = [occurrence("engine", f"Engine {i}", "甲", i) for i in range(80)]
        occurrences.append(occurrence("boot", "Boot", "乙", 80))
        data = chain(occurrences)
        batch = p.build_shadow_batch(
            data["entries"], data["cm"], data["policy"], data["group"],
            p._jsonl(data["events"]), data["checkpoint"], data["exclusions"],
            catalog_manifest_raw=data["cm_raw"], locator_manifest=data["lm"],
        )
        p.validate_shadow_batch(
            batch, entries=data["entries"], exclusions=data["exclusions"],
            catalog=data["cm"], policy=data["policy"], group=data["group"],
            events_raw=p._jsonl(data["events"]), checkpoint=data["checkpoint"],
            catalog_manifest_raw=data["cm_raw"], locator_manifest=data["lm"],
        )
        by_revision = {entry["entry_revision_identity"]: entry for entry in data["entries"]}
        self.assertEqual({by_revision[item]["component"] for item in batch["batch_selected"]},
                         {"engine"})
        self.assertEqual({by_revision[item]["component"] for item in batch["carry_over"]},
                         {"boot"})
        self.assertEqual((len(batch["batch_selected"]), len(batch["carry_over"])), (80, 1))

    def test_exclusion_partition_compares_occurrence_identities(self):
        data = chain()
        exclusion = copy.deepcopy(data["exclusions"])
        exclusion[0]["occurrence_identity"] = data["entries"][0]["logical_entry_identity"]
        with self.assertRaises(p.ProductionReviewError):
            p.check_catalog(data["cm"], data["eb"], p._jsonl(exclusion),
                            locator_manifest=data["lm"], locator_manifest_raw=data["lm_raw"],
                            occurrences_raw=data["ob"], locators_raw=data["lb"])

    def test_reconciliation_conservation_is_independent_of_live_drift(self):
        data = chain()
        batch = p.build_shadow_batch(
            data["entries"], data["cm"], data["policy"], data["group"],
            p._jsonl(data["events"]), data["checkpoint"], data["exclusions"],
            catalog_manifest_raw=data["cm_raw"], locator_manifest=data["lm"],
        )
        report = p.reconciliation_report(data["entries"], data["exclusions"],
                                         data["events"], batch)
        self.assertTrue(report["ok"])
        self.assertFalse(report["authoritative"])
        self.assertFalse(report["dispatchable"])
        self.assertFalse(report["promotable"])

    def test_atomic_directory_collision_durability_and_budgets(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final = root / "family" / "id"
            with mock.patch.object(p, "_fsync_directory", wraps=p._fsync_directory) as fsync_dir:
                self.assertEqual(p.atomic_publish_directory(
                    {"a": b"1", "b": b"2"}, final, root=root, budget=2), "PUBLISHED")
                self.assertGreaterEqual(fsync_dir.call_count, 2)
            self.assertEqual(p.atomic_publish_directory(
                {"a": b"1", "b": b"2"}, final, root=root, budget=2), "ALREADY_PRESENT")
            with self.assertRaisesRegex(p.ProductionReviewError, "drift"):
                p.atomic_publish_directory({"a": b"1"}, final, root=root, budget=2)
            with self.assertRaisesRegex(p.ProductionReviewError, "bytes=3"):
                p.atomic_publish_directory({"x": b"123"}, root / "too-large",
                                           root=root, budget=2)
            with self.assertRaisesRegex(p.ProductionReviewError, "category/budget"):
                p.atomic_publish_directory({"x": b"1"}, root / "bad-category",
                                           root=root, budget=2, category="policy")
            with mock.patch.object(p, "_rename_directory_noreplace", side_effect=OSError("stop")):
                with self.assertRaisesRegex(p.ProductionReviewError, "publication I/O"):
                    p.atomic_publish_directory({"x": b"1"}, root / "partial",
                                               root=root, budget=2)
            self.assertFalse((root / "partial").exists())
            with mock.patch.object(p, "_production_total", return_value=p.BUDGETS["total"]):
                with self.assertRaisesRegex(p.ProductionReviewError, "occupied="):
                    p.atomic_publish_directory({"x": b"1"}, root / "over-total",
                                               root=root, budget=2)

    def test_atomic_directory_rejects_symlinked_target_components(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside = root.parent / f"{root.name}-outside"
            outside.mkdir()
            self.addCleanup(lambda: outside.rmdir() if outside.exists() else None)
            (root / "linked").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(p.ProductionReviewError, "symlink"):
                p.atomic_publish_directory(
                    {"x": b"1"}, root / "linked" / "id", root=root, budget=1)
            self.assertFalse((outside / "id").exists())

            dangling = root / "dangling"
            dangling.symlink_to(root / "missing", target_is_directory=True)
            with self.assertRaisesRegex(p.ProductionReviewError, "symlink"):
                p.atomic_publish_directory(
                    {"x": b"1"}, dangling, root=root, budget=1)

            existing = root / "existing"
            existing.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(p.ProductionReviewError, "symlink"):
                p.atomic_publish_directory(
                    {"x": b"1"}, existing, root=root, budget=1)

    def test_atomic_directory_rejects_adversarial_lock_paths(self):
        with tempfile.TemporaryDirectory() as temporary, \
             tempfile.TemporaryDirectory() as outside_temporary:
            root = Path(temporary)
            outside = Path(outside_temporary)
            (root / ".artifacts").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(p.ProductionReviewError, "symlink"):
                p.atomic_publish_directory(
                    {"x": b"1"}, root / "family" / "id", root=root, budget=1)
            self.assertFalse((outside / "i18n/production-review/.publish.lock").exists())

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".artifacts").mkdir()
            (root / ".artifacts/i18n").symlink_to(
                root / "missing-lock-parent", target_is_directory=True)
            with self.assertRaisesRegex(p.ProductionReviewError, "symlink"):
                p.atomic_publish_directory(
                    {"x": b"1"}, root / "family" / "id", root=root, budget=1)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            lock_directory = root / ".artifacts/i18n/production-review"
            lock_directory.mkdir(parents=True)
            outside_lock = root / "outside-lock"
            outside_lock.write_bytes(b"unchanged")
            (lock_directory / ".publish.lock").symlink_to(outside_lock)
            with self.assertRaisesRegex(p.ProductionReviewError, "symlink|lock I/O"):
                p.atomic_publish_directory(
                    {"x": b"1"}, root / "family" / "id", root=root, budget=1)
            self.assertEqual(outside_lock.read_bytes(), b"unchanged")

    def test_atomic_directory_lock_open_resists_component_swap(self):
        with tempfile.TemporaryDirectory() as temporary, \
             tempfile.TemporaryDirectory() as outside_temporary:
            root = Path(temporary)
            artifacts = root / ".artifacts"
            artifacts.mkdir()
            outside = Path(outside_temporary)
            real_open = p.os.open
            swapped = False

            def swap_before_open(path, flags, *args, **kwargs):
                nonlocal swapped
                if path == ".artifacts" and kwargs.get("dir_fd") is not None and not swapped:
                    swapped = True
                    artifacts.rename(root / ".artifacts-original")
                    artifacts.symlink_to(outside, target_is_directory=True)
                return real_open(path, flags, *args, **kwargs)

            with mock.patch.object(p.os, "open", side_effect=swap_before_open):
                with self.assertRaisesRegex(p.ProductionReviewError, "lock I/O|symlink"):
                    p.atomic_publish_directory(
                        {"x": b"1"}, root / "family" / "id", root=root, budget=1)
            self.assertTrue(swapped)
            self.assertFalse((outside / "i18n/production-review/.publish.lock").exists())

    def test_rename_noreplace_rejects_real_empty_destination_collision(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            destination.mkdir()
            try:
                with self.assertRaises(FileExistsError):
                    p._rename_directory_noreplace(source, destination)
            except p.ProductionReviewError as error:
                if "unavailable" in str(error):
                    self.skipTest(str(error))
                raise
            self.assertTrue(source.is_dir())
            self.assertTrue(destination.is_dir())

    def test_live_locator_binding_rejects_detached_snapshot(self):
        manifest, occurrences, locators = snapshot()
        fake = mock.Mock()
        fake.raw_bytes = b"live manifest"
        fake.root = Path(".")
        fake.components = [mock.Mock(id=name) for name in MANIFEST_COMPONENTS]
        runtime = mock.Mock(); runtime.doctor.return_value={"lua_version":"Lua 5.1","luajit_version":"LuaJIT 2.1"}
        with mock.patch.object(p, "LuaRuntime", return_value=runtime), \
             mock.patch.object(p, "load_occurrences", return_value=p.parse_jsonl(occurrences, "occurrences")):
            with self.assertRaisesRegex(p.ProductionReviewError, "manifest_sha256"):
                p.check_locator_snapshot_live(manifest, occurrences, locators, fake)

    def test_live_locator_binding_rejects_occurrence_harvest_drift(self):
        manifest, occurrences, locators = snapshot()
        fake = mock.Mock()
        fake.raw_bytes = b"live manifest"
        fake.root = ROOT
        fake.components = [mock.Mock(id=name) for name in MANIFEST_COMPONENTS]
        runtime = mock.Mock()
        runtime.doctor.return_value = {
            "lua_version": "Lua 5.1", "luajit_version": "LuaJIT 2.1",
        }
        live_bound = dict(
            manifest,
            manifest_sha256=hashlib.sha256(fake.raw_bytes).hexdigest(),
            loader_contract_sha256=hashlib.sha256(
                (ROOT / "tools/i18nlib/locale_model.py").read_bytes()
            ).hexdigest(),
        )
        live_bound["locator_snapshot_id"] = p.object_id(
            "locator-snapshot", live_bound, "locator_snapshot_id")
        changed = p.parse_jsonl(occurrences, "occurrences")
        changed[0] = occurrence(source="Live drift")
        with mock.patch.object(p, "LuaRuntime", return_value=runtime), \
             mock.patch.object(p, "load_occurrences", return_value=changed):
            with self.assertRaisesRegex(
                    p.ProductionReviewError, "live occurrence harvest drift"):
                p.check_locator_snapshot_live(
                    live_bound, occurrences, locators, fake)

    def test_detached_catalog_cli_fails_without_traceback(self):
        manifest, occurrences, locators = snapshot()
        (ROOT / ".artifacts/i18n").mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / ".artifacts/i18n") as temporary:
            root = Path(temporary)
            lm=root/"locator.json"; ob=root/"occurrences.jsonl"; lb=root/"locators.jsonl"
            lm.write_bytes(p.canonical_bytes(manifest)); ob.write_bytes(occurrences); lb.write_bytes(locators)
            dummy=root/"dummy"; dummy.write_bytes(b"{}")
            completed=subprocess.run([sys.executable,"-B",str(ROOT/"tools/i18n"),"production","catalog","check",
                "--locator-snapshot",str(lm),"--occurrences",str(ob),"--locators",str(lb),
                "--catalog",str(dummy),"--entries",str(dummy),"--exclusions",str(dummy)],
                capture_output=True,text=True)
            self.assertNotEqual(completed.returncode,0)
            self.assertIn("operational locator live binding drift",completed.stderr)
            self.assertNotIn("Traceback",completed.stdout+completed.stderr)

    def test_frozen_chain_survives_current_rules_drift_for_reconciliation(self):
        data = chain()
        with mock.patch.object(p, "RULES_VERSION", "production-shadow-rules-v2"):
            # Frozen validation uses the frozen v1 contract, while a fresh live
            # reconstruction carries v2 and therefore becomes a false axis.
            entries, exclusions = p.check_catalog(data["cm"], data["eb"], data["xb"],
                locator_manifest=data["lm"], locator_manifest_raw=data["lm_raw"],
                occurrences_raw=data["ob"], locators_raw=data["lb"])
            with self.assertRaisesRegex(p.ProductionReviewError, "catalog rules drift"):
                p.check_catalog(data["cm"], data["eb"], data["xb"],
                    locator_manifest=data["lm"], locator_manifest_raw=data["lm_raw"],
                    occurrences_raw=data["ob"], locators_raw=data["lb"],
                    require_current_rules=True)
            rebuilt, rebuilt_entries, rebuilt_exclusions = p.build_catalog(data["lm"], data["ob"], data["lb"],
                locator_manifest_raw=data["lm_raw"], terminology_snapshot_id="3"*64,
                source_identities=SOURCES, recorded_at=STAMP, recorded_by=BY)
            self.assertEqual((len(entries),len(exclusions)),(1,1))
            self.assertNotEqual((rebuilt,rebuilt_entries,rebuilt_exclusions),(data["cm"],data["eb"],data["xb"]))

    def test_reconciliation_cli_uses_frozen_chain_when_live_manifest_is_missing(self):
        locator_dir = next((ROOT / "evidence/production-review/locator-snapshots").iterdir())
        catalog_dir = next((ROOT / "evidence/production-review/catalogs").iterdir())
        journal_dir = next((ROOT / "evidence/production-review/shadow-journals").iterdir())
        batch_dir = next((ROOT / "evidence/production-review/batches").iterdir())
        policy_dir = next((ROOT / "i18n/quality/production-review/shadow-policies").iterdir())
        missing = ROOT / ".artifacts/i18n/definitely-missing-production-manifest.json"
        completed = subprocess.run([sys.executable, "-B", str(ROOT / "tools/i18n"),
            "production", "reconciliation", "report", "--manifest", str(missing),
            "--locator-snapshot", str(locator_dir / "manifest.json"),
            "--occurrences", str(locator_dir / "occurrences.jsonl"),
            "--locators", str(locator_dir / "locators.jsonl"),
            "--catalog", str(catalog_dir / "manifest.json"),
            "--entries", str(catalog_dir / "entries.jsonl"),
            "--exclusions", str(catalog_dir / "exclusions.jsonl"),
            "--policy", str(policy_dir / "policy.json"),
            "--group", str(journal_dir / "group.json"),
            "--events", str(journal_dir / "events.jsonl"),
            "--checkpoint", str(journal_dir / "checkpoint.json"),
            "--batch", str(batch_dir / "manifest.json")], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = p.parse_canonical_object(
            (ROOT / ".artifacts/i18n/production-review/reconciliation.json").read_bytes(), "report")
        self.assertTrue(report["ok"])
        self.assertTrue(report["drift"])
        self.assertTrue(report["shadow_publication_blocked"])
        self.assertEqual(report["live_occurrences"], 0)
        self.assertEqual(report["drift_axes"], {key: False for key in p.RECONCILIATION_AXES})

    def test_reconciliation_artifact_exact_bytes_and_drift(self):
        data = chain()
        batch = p.build_shadow_batch(data["entries"], data["cm"], data["policy"], data["group"],
            p._jsonl(data["events"]), data["checkpoint"], data["exclusions"],
            catalog_manifest_raw=data["cm_raw"], locator_manifest=data["lm"])
        report = p.reconciliation_report(data["entries"], data["exclusions"], data["events"], batch)
        report.update({"catalog_id":data["cm"]["catalog_id"], "group_id":data["group"]["group_id"],
            "shadow_batch_id":batch["shadow_batch_id"], "live_occurrences":0,
            "drift_axes":{key: False for key in p.RECONCILIATION_AXES}, "drift":True,
            "shadow_publication_blocked":True})
        self.assertEqual(p.parse_canonical_object(p.canonical_bytes(p.validate_reconciliation_artifact(report)), "report"), report)
        with self.assertRaises(p.ProductionReviewError):
            p.validate_reconciliation_artifact(dict(report, extra=True))

    def test_publication_retry_race_residue_and_single_baseline(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); final = root / "family" / "id"; files={"x":b"1"}
            real_fsync = p._fsync_directory
            calls = 0
            def fail_parent_once(path):
                nonlocal calls
                calls += 1
                if path == final.parent and calls > 1:
                    raise OSError("durability")
                return real_fsync(path)
            with mock.patch.object(p, "_fsync_directory", side_effect=fail_parent_once):
                with self.assertRaisesRegex(p.ProductionReviewError, "publication I/O"):
                    p.atomic_publish_directory(files, final, root=root, budget=1)
            self.assertEqual(p.atomic_publish_directory(files, final, root=root, budget=1), "ALREADY_PRESENT")

            raced = root / "race" / "id"
            race_events = []
            def race(source, destination):
                race_events.append("rename")
                destination.mkdir(parents=True); (destination/"x").write_bytes(b"1")
                raise FileExistsError()
            def record_fsync(path):
                if path == raced.parent:
                    race_events.append("parent_fsync")
                return real_fsync(path)
            with mock.patch.object(p, "_rename_directory_noreplace", side_effect=race), \
                 mock.patch.object(p, "_fsync_directory", side_effect=record_fsync):
                self.assertEqual(p.atomic_publish_directory(files, raced, root=root, budget=1), "ALREADY_PRESENT")
            self.assertLess(race_events.index("rename"), race_events.index("parent_fsync"))

            drifted = root / "race-drift" / "id"
            def differing_race(source, destination):
                destination.mkdir(parents=True); (destination/"x").write_bytes(b"2")
                raise FileExistsError()
            with mock.patch.object(p, "_rename_directory_noreplace", side_effect=differing_race):
                with self.assertRaisesRegex(p.ProductionReviewError,
                                            "immutable artifact tree drift"):
                    p.atomic_publish_directory(files, drifted, root=root, budget=1)

            residue_final = root / "residue" / "id"
            residue = residue_final.parent / p._publication_stage_name({"waste": b"waste"})
            residue.mkdir(parents=True); (residue/"waste").write_bytes(b"waste")
            self.assertEqual(p.atomic_publish_directory(files, residue_final, root=root, budget=1), "PUBLISHED")
            self.assertFalse(residue.exists())

            locator_parent = root / "evidence/production-review/locator-snapshots"
            p.atomic_publish_directory(files, locator_parent/"one", root=root, budget=1, category=None)
            # Category-enforced WP1 callers reject a second baseline.
            with self.assertRaisesRegex(p.ProductionReviewError, "only one locator"):
                p.atomic_publish_directory(files, locator_parent/"two", root=root,
                                           budget=p.BUDGETS["locator"], category="locator")

    def test_publication_retry_revalidates_baselines_and_total_budget(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final = root / "evidence/production-review/locator-snapshots/one"
            files = {"x": b"1"}
            self.assertEqual(p.atomic_publish_directory(
                files, final, root=root, budget=p.BUDGETS["locator"],
                category="locator"), "PUBLISHED")

            # The identical artifact is already included in occupied bytes, so
            # a valid retry at the exact ceiling must not add its family again.
            with mock.patch.object(p, "_production_total", return_value=p.BUDGETS["total"]), \
                 mock.patch.object(p, "_fsync_directory",
                                   wraps=p._fsync_directory) as fsync_dir:
                self.assertEqual(p.atomic_publish_directory(
                    files, final, root=root, budget=p.BUDGETS["locator"],
                    category="locator"), "ALREADY_PRESENT")
            self.assertIn(mock.call(final.parent), fsync_dir.call_args_list)

            with mock.patch.object(p, "_production_total", return_value=p.BUDGETS["total"] + 1):
                with self.assertRaisesRegex(p.ProductionReviewError, "tracked total"):
                    p.atomic_publish_directory(
                        files, final, root=root, budget=p.BUDGETS["locator"],
                        category="locator")

            sibling = final.parent / "two"
            sibling.mkdir()
            (sibling / "x").write_bytes(b"1")
            with self.assertRaisesRegex(p.ProductionReviewError, "only one locator"):
                p.atomic_publish_directory(
                    files, final, root=root, budget=p.BUDGETS["locator"],
                    category="locator")

    def test_collision_retry_ignores_its_stage_but_not_a_real_baseline(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final = root / "evidence/production-review/locator-snapshots/one"
            files = {"x": b"1"}

            def identical_race(source, destination):
                destination.mkdir(parents=True)
                (destination / "x").write_bytes(b"1")
                raise FileExistsError()

            with mock.patch.object(p, "_rename_directory_noreplace",
                                   side_effect=identical_race), \
                 mock.patch.dict(p.BUDGETS, {"total": 1}):
                self.assertEqual(p.atomic_publish_directory(
                    files, final, root=root, budget=p.BUDGETS["locator"],
                    category="locator"), "ALREADY_PRESENT")

            with tempfile.TemporaryDirectory() as collision_temporary:
                collision_root = Path(collision_temporary)
                collision_final = (
                    collision_root
                    / "evidence/production-review/locator-snapshots/one"
                )

                def occupied_identical_race(source, destination):
                    destination.mkdir(parents=True)
                    (destination / "x").write_bytes(b"1")
                    second = destination.parent / "two"
                    second.mkdir()
                    (second / "x").write_bytes(b"1")
                    raise FileExistsError()

                with mock.patch.object(
                        p, "_rename_directory_noreplace",
                        side_effect=occupied_identical_race):
                    with self.assertRaisesRegex(
                            p.ProductionReviewError, "only one locator"):
                        p.atomic_publish_directory(
                            files, collision_final, root=collision_root,
                            budget=p.BUDGETS["locator"], category="locator")

            extra = final.parent / "two"
            extra.mkdir()
            (extra / "x").write_bytes(b"1")
            with self.assertRaisesRegex(p.ProductionReviewError, "only one locator"):
                p.atomic_publish_directory(
                    files, final, root=root, budget=p.BUDGETS["locator"],
                    category="locator")

    def test_cross_id_content_addressed_stage_residue_is_recovered(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            parent = root / "evidence/production-review/catalogs"
            parent.mkdir(parents=True)
            residue = parent / p._publication_stage_name({"old": b"residue"})
            residue.mkdir()
            (residue / "partial").write_bytes(b"crash residue")
            unrelated = parent / ".production-review-stage-not-owned"
            unrelated.write_bytes(b"unrelated")
            symlink_target = root / "outside-stage"
            symlink_target.mkdir()
            symlink_residue = parent / p._publication_stage_name({"link": b"residue"})
            symlink_residue.symlink_to(symlink_target, target_is_directory=True)

            final = parent / "new-id"
            self.assertEqual(p.atomic_publish_directory(
                {"new": b"artifact"}, final, root=root,
                budget=p.BUDGETS["catalog"], category="catalog"), "PUBLISHED")
            self.assertFalse(residue.exists())
            self.assertEqual(unrelated.read_bytes(), b"unrelated")
            self.assertTrue(symlink_residue.is_symlink())

    def test_duplicate_index_requires_exact_integer_zero(self):
        row = occurrence()
        for alias in (False, 0.0):
            with self.subTest(alias=alias):
                with self.assertRaisesRegex(p.ProductionReviewError,
                                            "duplicate_index.*integer zero"):
                    p.make_allocation(row, alias)

                allocation = p.make_allocation(row)
                allocation["duplicate_index"] = alias
                with self.assertRaisesRegex(p.ProductionReviewError,
                                            "duplicate_index.*integer zero"):
                    p.make_locator_row(row, allocation)

                locator = p.make_locator_row(row, p.make_allocation(row))
                locator["duplicate_index"] = alias
                with self.assertRaisesRegex(p.ProductionReviewError,
                                            "duplicate_index.*integer zero"):
                    p._validate_locator_row(locator)

    def test_tracked_schema_declares_wp1_duplicate_index_literal_zero(self):
        schema = json.loads(
            (ROOT / "i18n/quality/production-review/schemas-v1.json").read_text())
        shapes = schema["exact_shapes"]
        self.assertEqual(shapes["allocation"]["duplicate_index"], "integer:0")
        self.assertEqual(shapes["locator_row"]["duplicate_index"], "integer:0")

    def test_malformed_locator_types_fail_without_traceback(self):
        manifest, occurrences, locators = snapshot()
        rows = p.parse_jsonl(occurrences, "occurrences")
        rows[0]["component"] = []
        malformed = p._jsonl(rows)
        bad_manifest = dict(manifest, occurrences_sha256=hashlib.sha256(malformed).hexdigest())
        bad_manifest["locator_snapshot_id"] = p.object_id(
            "locator-snapshot", bad_manifest, "locator_snapshot_id")
        with self.assertRaises(p.ProductionReviewError):
            p.check_locator_snapshot(bad_manifest, malformed, locators)
        (ROOT / ".artifacts/i18n").mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / ".artifacts/i18n") as temporary:
            work = Path(temporary)
            manifest_path = work / "manifest.json"
            occurrences_path = work / "occurrences.jsonl"
            locators_path = work / "locators.jsonl"
            manifest_path.write_bytes(p.canonical_bytes(bad_manifest))
            occurrences_path.write_bytes(malformed)
            locators_path.write_bytes(locators)
            completed = subprocess.run([sys.executable, "-B", str(ROOT / "tools/i18n"),
                "production", "locator", "check", "--snapshot", str(manifest_path),
                "--occurrences", str(occurrences_path), "--locators", str(locators_path)],
                capture_output=True, text=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_timestamp_and_schema_version_are_exact(self):
        with self.assertRaises(p.ProductionReviewError):
            p.build_locator_snapshot_from_occurrences(
                [], manifest_sha256="1" * 64,
                manifest_component_ordinals=p._component_ordinals(MANIFEST_COMPONENTS),
                loader_contract_path="x", loader_contract_sha256="2" * 64,
                lua_runtime="Lua", lua_build="JIT", recorded_at=STAMP, recorded_by="")
        manifest, occurrences, locators = snapshot()
        bad = dict(manifest, schema_version=True)
        with self.assertRaises(p.ProductionReviewError):
            p.check_locator_snapshot(bad, occurrences, locators)


if __name__ == "__main__":
    unittest.main()
