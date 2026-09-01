from __future__ import annotations

import fcntl
import hashlib
import os
import json
from collections import Counter
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import shutil
from contextlib import closing
from pathlib import Path
from unittest import mock

from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as catalog
from tools.i18nlib import production_review_v2_lite_queue as queue
from tools.i18nlib import production_review_v2_lite_batch as batch
import contextual_result_check

ROOT = Path(__file__).resolve().parents[2]
STAMP = "2026-09-02T01:02:03Z"


class QueueFixture(unittest.TestCase):
    def setUp(self):
        (ROOT / ".artifacts/i18n").mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".artifacts/i18n")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        (self.root / ".gitignore").write_text("/.artifacts/\n", encoding="utf-8")
        self.entries = [self._entry("1"), self._entry("2")]
        self._write_catalog()
        queue_schema = self.root / "i18n/quality/production-review-v2-lite/queue-v1.schema.sql"
        queue_schema.write_text("-- planned WP2-Lite queue schema fixture\n", encoding="utf-8")
        self._commit("catalog")

    def _entry(self, digit):
        source, target, fixed, terminology = "source " + digit, "target " + digit, "commit:" + "a" * 40, "b" * 64
        core = {"component": "tome", "duplicate_index": 0, "function_name": "t", "normalized_source_tag": "",
                "section": "fixture", "source": source, "translation_path": "tome.lua"}
        locator = catalog._plain_id(catalog.CALL_LOCATOR_KIND, "locator", core)
        logical = wp1.surface.logical_entry_identity(component="tome", normalized_path="tome.lua",
                                                      call_locator=locator, source_tag="")
        revision = wp1.surface.entry_revision_identity(logical_entry_identity=logical, source=source, target=target,
            fixed_source_identity=fixed, terminology_snapshot=terminology, rules_version=catalog.RULES_VERSION)
        return {"schema_version": 1, "component": "tome", "normalized_path": "tome.lua",
                "section": "fixture", "call_locator": locator, "logical_entry_identity": logical,
                "entry_revision_identity": revision, "source": source, "target": target, "source_tag": "",
                "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
                "target_sha256": hashlib.sha256(target.encode()).hexdigest(), "fixed_source_identity": fixed,
                "terminology_snapshot_sha256": terminology, "rules_version": catalog.RULES_VERSION,
                "risk": {"has_args_order": False, "has_special": False, "source_utf8_bytes": len(source.encode()),
                         "target_utf8_bytes": len(target.encode()), "component_group_size": 1, "component_group_last": True}}

    def _write_catalog(self):
        entries_raw = wp1._jsonl(sorted(self.entries, key=lambda row: row["entry_revision_identity"]))
        exclusions_raw = b""
        manifest = {"schema_version": 1, "kind": catalog.CATALOG_KIND, "catalog_id": "",
                    "rules_version": catalog.RULES_VERSION, "recorded_at": STAMP, "recorded_by": "fixture",
                    "manifest_sha256": "c" * 64, "loader_contract_path": "tools/i18nlib/locale_model.py",
                    "loader_contract_sha256": "d" * 64, "lua_runtime": "Lua 5.1",
                    "manifest_component_ordinals": [{"component": name, "ordinal": index} for index, name in
                        enumerate(["engine", "boot", "tome", "ashes-urhrok", "cults", "orcs"])],
                    "component_counts": {"ashes-urhrok": 0, "boot": 0, "cults": 0, "engine": 0,
                                                              "orcs": 0, "tome": len(self.entries)},
                    "occurrence_count": len(self.entries), "entry_count": len(self.entries), "exclusion_count": 0,
                    "entries_sha256": hashlib.sha256(entries_raw).hexdigest(),
                    "exclusions_sha256": hashlib.sha256(exclusions_raw).hexdigest(),
                    "terminology_snapshot_sha256": "b" * 64,
                    "source_identities": {name: "commit:" + "a" * 40 for name in
                                          ["engine", "boot", "tome", "ashes-urhrok", "cults", "orcs"]},
                    "policy_sha256": hashlib.sha256(catalog.POLICY_RAW).hexdigest()}
        manifest["catalog_id"] = catalog.catalog_id(manifest)
        files = {catalog.SCHEMA_PATH: catalog.SCHEMA_RAW, catalog.POLICY_PATH: catalog.POLICY_RAW,
                 f"{catalog.CATALOG_PREFIX}/manifest.json": wp1.canonical_bytes(manifest),
                 f"{catalog.CATALOG_PREFIX}/entries.jsonl": entries_raw,
                 f"{catalog.CATALOG_PREFIX}/exclusions.jsonl": exclusions_raw}
        for name, raw in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        self.catalog_id = manifest["catalog_id"]

    def _commit(self, message):
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=self.root, check=True)
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

    def _install_contextual_done_state(self, ref, output_raw):
        """Install a real v2 review-only DONE_VERIFIED fixture for this run."""
        fixture = ROOT / "tests/i18n/fixtures/paseo_state_v2/contextual_v2"
        task_id = ref["task_id"]
        task_dir = self.root / ".ai/task" / task_id
        task_dir.mkdir(parents=True, exist_ok=True)
        envelope_raw = Path(ref["input_path"]).read_bytes()
        envelope = json.loads(envelope_raw)
        input_path = task_dir / "CONTEXTUAL-ENVELOPE-final-full.json"
        raw_path = self.root / ".ai/reviews" / task_id / "raw-final-full.txt"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        input_path.write_bytes(envelope_raw)
        raw_path.write_bytes(output_raw)
        state = json.loads((fixture / "STATE.json").read_text(encoding="utf-8"))
        record = json.loads((fixture / "review-final-full.json").read_text(encoding="utf-8"))
        relative_input = input_path.relative_to(self.root).as_posix()
        relative_raw = raw_path.relative_to(self.root).as_posix()
        record.update({"task_id": task_id, "cycle": 0, "review_phase": "REVIEW",
                       "task_id": task_id, "candidate_identity": ref["candidate_identity"],
                       "input_path": relative_input, "raw_output_path": relative_raw,
                       "raw_output_sha256": hashlib.sha256(output_raw).hexdigest(),
                       "dispatch_id": "final-full", "agent_id": "agent-final-full"})
        record_path = task_dir / "review-final-full.json"
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        dispatch = {"dispatch_id": "final-full", "role": "REVIEWER",
                    "purpose": "translation_contextual_v2", "agent_id": "agent-final-full",
                    "parent_agent_id": "agent-orchestrator", "workspace_id": "fixture-workspace",
                    "lineage_verified": True, "lifecycle": "archived", "archive_confirmed": True,
                    "candidate_identity": ref["candidate_identity"], "input_path": relative_input,
                    "labels": {"task_id": task_id, "role": "reviewer", "purpose": "translation_contextual_v2",
                               "candidate_identity": ref["candidate_identity"], "dispatch_id": "final-full"}}
        state.update({"task_id": task_id, "cycle": 0, "state": "DONE", "mode": "review_only",
                      "change_class": "standard",
                      "contextual_reviewers": [{"role": "REVIEWER", "purpose": "translation_contextual_v2",
                          "candidate_identity": ref["candidate_identity"], "dispatch_id": "final-full",
                          "input_path": relative_input, "agent_id": "agent-final-full"}],
                      "child_dispatches": [dispatch],
                      "review_records": [record_path.relative_to(self.root).as_posix()],
                      "senior_review_records": []})
        state_path = task_dir / "STATE.json"
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        sys.path.insert(0, str(ROOT / "tools"))
        import ai_state_check
        checked = ai_state_check.check_state(state_path, target="DONE", workspace_root=self.root)
        if checked.outcome != "DONE_VERIFIED":
            raise AssertionError(f"fixture state rejected: {checked.detail}")

    def _batch(self, state="done", batch="batch-1", *, contract="surface", adapter_entry_index=0):
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        entry = self.entries[0]
        revision = entry["entry_revision_identity"]
        adapter_entry = self.entries[adapter_entry_index]
        adapter_revision = adapter_entry["entry_revision_identity"]
        if contract == "surface":
            contract_name = "translation_surface_screen_v1"
            surface_entry = {key: adapter_entry[key] for key in (
                "component", "normalized_path", "call_locator", "source_tag", "source", "target",
                "logical_entry_identity", "entry_revision_identity")}
            payload = {"contract": contract_name, "fixed_source_identity": adapter_entry["fixed_source_identity"],
                       "terminology_snapshot": adapter_entry["terminology_snapshot_sha256"],
                       "rules_version": adapter_entry["rules_version"], "rendered_briefing": "fixture",
                       "entries": [surface_entry]}
            adapter_output_value = {"contract": contract_name, "candidate_identity": "",
                                    "results": [{"entry_revision_identity": adapter_revision, "verdict": "OK"}]}
        elif contract == "contextual":
            contract_name = "translation_contextual_v2"
            payload = {"contract": contract_name, "ordered_revision_keys": [adapter_revision],
                       "translation_snapshot": [{"revision_key": adapter_revision,
                                                   "source": adapter_entry["source"],
                                                   "target": adapter_entry["target"]}],
                       "fixed_source_identity": adapter_entry["fixed_source_identity"],
                       "terminology_snapshot": adapter_entry["terminology_snapshot_sha256"],
                       "bounded_context": [{"revision_key": adapter_revision, "context": "fixture"}],
                       "rendered_briefing": "fixture"}
            adapter_output_value = {"contract": contract_name, "candidate_identity": "",
                                    "verdicts": [{"revision_key": adapter_revision, "verdict": "OK"}]}
        else:
            raise AssertionError(contract)
        candidate_identity = hashlib.sha256(wp1.surface.canonical_bytes(payload)).hexdigest()
        adapter_input = wp1.surface.canonical_bytes({"candidate_identity": candidate_identity, "payload": payload})
        adapter_output_value["candidate_identity"] = candidate_identity
        adapter_output = (wp1.surface.canonical_bytes(adapter_output_value) if contract == "surface" else
                          json.dumps(adapter_output_value, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8"))
        input_hash, output_hash = hashlib.sha256(adapter_input).hexdigest(), hashlib.sha256(adapter_output).hexdigest()
        row = {"schema_version": 1, "source": entry["source"], "target": entry["target"],
               "source_tag": "", "normalized_path": "tome.lua", "call_locator": entry["call_locator"],
               "logical_entry_identity": entry["logical_entry_identity"], "entry_revision_identity": revision,
               "surface_verdict": "OK" if contract == "surface" else None, "surface_observation": None,
               "deep_verdict": "OK" if contract == "contextual" else None, "deep_observation": None,
               "input_sha256": input_hash, "output_sha256": output_hash, "final_state": state,
               "completion_level": "surface_only" if contract == "surface" else "deep_reviewed"}
        results = wp1._jsonl([row])
        adjudications = b""
        gates = wp1.canonical_bytes({"schema_version": 1, "commands": []})
        manifest = {"schema_version": 1, "kind": "production_review_v2_lite_batch_v1",
                    "catalog_id": self.catalog_id, "policy_sha256": hashlib.sha256(catalog.POLICY_RAW).hexdigest(),
                    "base_commit": base, "batch_id": batch, "attempt": 1, "ordered_revisions": [revision],
                    "ordered_revisions_sha256": hashlib.sha256(wp1.canonical_bytes([revision])).hexdigest(),
                    "entry_snapshots_sha256": hashlib.sha256(wp1.canonical_bytes([entry])).hexdigest(),
                    "adapter_refs": [{"contract": contract_name,
                        "input_path": f"evidence/production-review-v2-lite/batches/{batch}/raw/{contract}/input.json",
                        "input_sha256": input_hash,
                        "output_path": f"evidence/production-review-v2-lite/batches/{batch}/raw/{contract}/output.json",
                        "output_sha256": output_hash, "candidate_identity": candidate_identity}],
                    "results_sha256": hashlib.sha256(results).hexdigest(),
                    "adjudications_sha256": hashlib.sha256(adjudications).hexdigest(),
                    "gates_sha256": hashlib.sha256(gates).hexdigest(), "producer_task_ids": ["fixture"],
                    "recorded_at": STAMP, "recorded_by": "fixture"}
        root = self.root / f"evidence/production-review-v2-lite/batches/{batch}"
        root.mkdir(parents=True)
        (root / "manifest.json").write_bytes(wp1.canonical_bytes(manifest))
        (root / "results.jsonl").write_bytes(results)
        (root / "adjudications.jsonl").write_bytes(adjudications)
        (root / "gates.json").write_bytes(gates)
        (root / f"raw/{contract}").mkdir(parents=True)
        (root / f"raw/{contract}/input.json").write_bytes(adapter_input)
        (root / f"raw/{contract}/output.json").write_bytes(adapter_output)
        return root

    def _add_overlapping_contract(self, root, contract):
        entry = self.entries[0]
        revision = entry["entry_revision_identity"]
        if contract == "surface":
            contract_name = "translation_surface_screen_v1"
            surface_entry = {key: entry[key] for key in (
                "component", "normalized_path", "call_locator", "source_tag", "source", "target",
                "logical_entry_identity", "entry_revision_identity")}
            payload = {"contract": contract_name, "fixed_source_identity": entry["fixed_source_identity"],
                       "terminology_snapshot": entry["terminology_snapshot_sha256"],
                       "rules_version": entry["rules_version"], "rendered_briefing": "fixture",
                       "entries": [surface_entry]}
            output_value = {"contract": contract_name, "candidate_identity": "",
                            "results": [{"entry_revision_identity": revision, "verdict": "OK"}]}
        elif contract == "contextual":
            contract_name = "translation_contextual_v2"
            payload = {"contract": contract_name, "ordered_revision_keys": [revision],
                       "translation_snapshot": [{"revision_key": revision, "source": entry["source"],
                                                  "target": entry["target"]}],
                       "fixed_source_identity": entry["fixed_source_identity"],
                       "terminology_snapshot": entry["terminology_snapshot_sha256"],
                       "bounded_context": [{"revision_key": revision, "context": "fixture"}],
                       "rendered_briefing": "fixture"}
            output_value = {"contract": contract_name, "candidate_identity": "",
                            "verdicts": [{"revision_key": revision, "verdict": "OK"}]}
        else:
            raise AssertionError(contract)
        candidate_identity = hashlib.sha256(wp1.surface.canonical_bytes(payload)).hexdigest()
        input_raw = wp1.surface.canonical_bytes({"candidate_identity": candidate_identity, "payload": payload})
        output_value["candidate_identity"] = candidate_identity
        output_raw = (wp1.surface.canonical_bytes(output_value) if contract == "surface" else
                      json.dumps(output_value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        raw_root = root / f"raw/{contract}"
        raw_root.mkdir(parents=True)
        (raw_root / "input.json").write_bytes(input_raw)
        (raw_root / "output.json").write_bytes(output_raw)
        manifest_path = root / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["adapter_refs"].append({
            "contract": contract_name,
            "input_path": (raw_root / "input.json").relative_to(self.root).as_posix(),
            "input_sha256": hashlib.sha256(input_raw).hexdigest(),
            "output_path": (raw_root / "output.json").relative_to(self.root).as_posix(),
            "output_sha256": hashlib.sha256(output_raw).hexdigest(),
            "candidate_identity": candidate_identity,
        })
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        results_path = root / "results.jsonl"
        row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
        prefix = "surface" if contract == "surface" else "deep"
        row[prefix + "_verdict"] = "OK"
        row[prefix + "_observation"] = None
        results_path.write_bytes(wp1._jsonl([row]))
        manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))

    def _rewrite_catalog(self, rows):
        rows = sorted(rows, key=lambda row: row["entry_revision_identity"])
        entries_path = self.root / catalog.CATALOG_PREFIX / "entries.jsonl"
        entries_path.write_bytes(wp1._jsonl(rows))
        manifest_path = self.root / catalog.CATALOG_PREFIX / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["entries_sha256"] = hashlib.sha256(entries_path.read_bytes()).hexdigest()
        for row in rows:
            manifest["source_identities"][row["component"]] = row["fixed_source_identity"]
        counts = Counter(row["component"] for row in rows)
        manifest["component_counts"] = {key: counts.get(key, 0) for key in manifest["component_counts"]}
        manifest["catalog_id"] = catalog.catalog_id(manifest)
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        self.catalog_id = manifest["catalog_id"]


class QueueTests(QueueFixture):
    def _resize_and_init(self, count):
        database = queue.database_path(self.root)
        queue.checkpoint_path(self.root).unlink(missing_ok=True)
        scratch = queue.checkpoint_path(self.root).parent / "surface"
        if scratch.exists():
            import shutil
            shutil.rmtree(scratch)
        for path in (database, Path(str(database) + "-wal"), Path(str(database) + "-shm")):
            path.unlink(missing_ok=True)
        self.entries = [self._entry(str(i)) for i in range(count)]
        self._write_catalog()
        self._commit(f"catalog {count}")
        queue.init(self.root)

    def _surface_outputs(self):
        checkpoint = batch.show(self.root)
        outputs = {}
        for index, ref in enumerate(checkpoint["surface"]):
            envelope = wp1.surface.strict_json_bytes(Path(ref["input_path"]).read_bytes(), label="surface envelope")
            outputs[str(index)] = wp1.surface.canonical_bytes({
                "contract": wp1.surface.CONTRACT,
                "candidate_identity": ref["candidate_identity"],
                "results": [{"entry_revision_identity": entry["entry_revision_identity"], "verdict": "OK"}
                            for entry in envelope["payload"]["entries"]],
            })
        return outputs

    def _blocked_batch(self, batch):
        root = self._batch(batch=batch)
        self._add_overlapping_contract(root, "contextual")
        # Surface ISSUE + contextual ISSUE + pending adjudication is the
        # exact durable blocked shape consumed by current replay.
        surface_out = root / "raw/surface/output.json"
        value = wp1.parse_canonical_object(surface_out.read_bytes(), "surface output")
        value["results"][0].update({"verdict": "ISSUE", "observation": "blocked fixture"})
        surface_out.write_bytes(wp1.canonical_bytes(value))
        contextual_out = root / "raw/contextual/output.json"
        contextual_value = json.loads(contextual_out.read_bytes())
        contextual_value["verdicts"][0].update({"verdict": "ISSUE", "observation": "contextual issue"})
        contextual_out.write_bytes(wp1.canonical_bytes(contextual_value))
        result_path = root / "results.jsonl"
        result = wp1.parse_jsonl(result_path.read_bytes(), "results")[0]
        result.update({"surface_verdict": "ISSUE", "surface_observation": "blocked fixture",
                       "deep_verdict": "ISSUE", "deep_observation": "contextual issue",
                       "completion_level": "deep_reviewed", "final_state": "blocked",
                       "input_sha256": hashlib.sha256((root / "raw/surface/input.json").read_bytes()).hexdigest(),
                       "output_sha256": hashlib.sha256(surface_out.read_bytes()).hexdigest()})
        result_path.write_bytes(wp1._jsonl([result]))
        adjud_path = root / "adjudications.jsonl"
        adjud_path.write_bytes(wp1._jsonl([{"schema_version": 1,
            "entry_revision_identity": result["entry_revision_identity"],
            "observation_sha256": hashlib.sha256(b"contextual issue").hexdigest(),
            "disposition": "pending", "evidence_path": None, "evidence_commit": None,
            "evidence_snapshot": None, "conclusion": "blocked fixture", "repair_required": False}]))
        manifest_path = root / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["results_sha256"] = hashlib.sha256(result_path.read_bytes()).hexdigest()
        manifest["adjudications_sha256"] = hashlib.sha256(adjud_path.read_bytes()).hexdigest()
        manifest["adapter_refs"][0]["output_sha256"] = hashlib.sha256(surface_out.read_bytes()).hexdigest()
        manifest["adapter_refs"][1]["output_sha256"] = hashlib.sha256(contextual_out.read_bytes()).hexdigest()
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        return root

    def test_c12_real_git_retry_blocked_abandon_restores_exact_committed_tuple(self):
        root = self._blocked_batch("blocked-winner")
        self._commit("blocked winner")
        queue.init(self.root)
        before = queue.business_rows(queue.database_path(self.root))[0][0]
        batch.start(self.root, limit=1, retry_blocked=True)
        batch.abandon(self.root)
        after = queue.business_rows(queue.database_path(self.root))[0][0]
        self.assertEqual(after, before)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"blocked": 1})

    def test_c21_sqlite_first_exact_winner_recover_then_abandon_is_byte_exact(self):
        self._blocked_batch("blocked-exact")
        self._commit("blocked exact winner")
        queue.init(self.root)
        winner = queue.business_rows(queue.database_path(self.root))[0][0]
        batch.start(self.root, limit=1, retry_blocked=True)
        with sqlite3.connect(queue.database_path(self.root)) as con:
            con.execute("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", winner)
            con.commit()
        batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][2], "reserved")
        batch.abandon(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0], winner)

    def test_c22_tampered_prior_state_rejects_before_sqlite_mutation(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        path = queue.checkpoint_path(self.root)
        value = batch._load(path)
        value["entry_snapshots"][0]["prior_effective_state"] = "blocked"
        batch._atomic(path, batch._checkpoint_bytes(value))
        before = queue.business_rows(queue.database_path(self.root))[0]
        with self.assertRaisesRegex(wp1.ProductionReviewError, "non-queued"):
            batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0], before)
        path.unlink()

    def test_c23_retry_attempt_and_batch_identity_are_deterministic(self):
        self._blocked_batch("blocked-attempt")
        self._commit("blocked attempt winner")
        queue.init(self.root)
        first = batch.start(self.root, limit=1, retry_blocked=True)
        checkpoint = batch.show(self.root)
        self.assertEqual(checkpoint["attempt"], 2)
        self.assertEqual(first["batch_id"], batch._batch_id("retry_blocked", checkpoint["selected"], 2))
        batch.abandon(self.root)
        second = batch.start(self.root, limit=1, retry_blocked=True)
        self.assertEqual(second["batch_id"], first["batch_id"])
        self.assertEqual(batch.show(self.root)["attempt"], 2)
        batch.abandon(self.root)

    def test_c23_checkpoint_attempt_tamper_is_rejected_before_sqlite_open(self):
        cases = (("queued", False), ("retry_blocked", True))
        for mode, retry_blocked in cases:
            with self.subTest(mode=mode):
                # Each mode is an independent transaction fixture.  In
                # particular, queue.init must not inherit the previous mode's
                # database, and SQLite's WAL/checkpoint bytes are not a stable
                # representation of the durable projection.
                for candidate in (queue.checkpoint_path(self.root), queue.database_path(self.root),
                                  Path(str(queue.database_path(self.root)) + "-wal"),
                                  Path(str(queue.database_path(self.root)) + "-shm")):
                    candidate.unlink(missing_ok=True)
                if retry_blocked:
                    self._blocked_batch("blocked-attempt-authority")
                    self._commit("blocked attempt authority")
                else:
                    self._resize_and_init(1)
                if retry_blocked:
                    queue.init(self.root)
                batch.start(self.root, limit=1, retry_blocked=retry_blocked)
                path = queue.checkpoint_path(self.root)
                value = batch._load(path)
                value["attempt"] = 9
                value["batch_id"] = batch._batch_id(mode, value["selected"], value["attempt"])
                batch._atomic(path, batch._checkpoint_bytes(value))
                database = queue.database_path(self.root)
                before = queue.business_rows(database)
                with mock.patch.object(queue, "_connect", side_effect=AssertionError("SQLite opened before checkpoint validation")):
                    with self.assertRaisesRegex(wp1.ProductionReviewError, "authoritative winners"):
                        batch.recover(self.root)
                self.assertEqual(queue.business_rows(database), before)
                path.unlink()
                for candidate in (database, Path(str(database) + "-wal"), Path(str(database) + "-shm")):
                    candidate.unlink(missing_ok=True)

    def test_c24_missing_reservation_rejects_canonical_replacement_before_sqlite(self):
        self._resize_and_init(2)
        batch.start(self.root, limit=1)
        path = queue.checkpoint_path(self.root)
        value = batch._load(path)
        selected_revision = value["selected"][0]
        replacement = next(entry for entry in self.entries
                           if entry["entry_revision_identity"] != selected_revision)
        value["selected"] = [replacement["entry_revision_identity"]]
        value["selected_sha256"] = batch._sha(wp1.canonical_bytes(value["selected"]))
        value["entry_snapshots"] = [{**replacement, "prior_effective_state": "queued",
                                      "row_sha256": batch._sha(wp1.canonical_bytes(replacement))}]
        value["batch_id"] = batch._batch_id("queued", value["selected"], value["attempt"])
        batch._atomic(path, batch._checkpoint_bytes(value))
        database = queue.database_path(self.root)
        with sqlite3.connect(database) as con:
            con.execute("DELETE FROM state_override")
            con.commit()
        before = {candidate: candidate.read_bytes() for candidate in
                  (database, Path(str(database) + "-wal"), Path(str(database) + "-shm"))
                  if candidate.exists()}
        with self.assertRaisesRegex(wp1.ProductionReviewError, "stable selection"):
            batch.recover(self.root)
        after = {candidate: candidate.read_bytes() for candidate in before}
        self.assertEqual(after, before)
        path.unlink()
        for candidate in (database, Path(str(database) + "-wal"), Path(str(database) + "-shm")):
            candidate.unlink(missing_ok=True)

    def test_c12_sqlite_first_abandon_crash_checkpoint_remaining_recovers_blocked(self):
        self._blocked_batch("blocked-crash")
        self._commit("blocked crash winner")
        queue.init(self.root)
        batch.start(self.root, limit=1, retry_blocked=True)
        with sqlite3.connect(queue.database_path(self.root)) as con:
            con.execute("DELETE FROM state_override")
            con.commit()
        batch.abandon(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"blocked": 1})
        self.assertFalse(batch.show(self.root)["active"])

    def test_c12_checkpoint_first_import_with_sqlite_lag_and_deleted_row_recovers(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        outputs = self._surface_outputs()
        with sqlite3.connect(queue.database_path(self.root)) as con:
            con.execute("DELETE FROM state_override")
            con.commit()
        imported = batch.surface_import(self.root, outputs)
        self.assertEqual(imported["imported"], 1)
        with sqlite3.connect(queue.database_path(self.root)) as con:
            con.execute("DELETE FROM state_override")
            con.commit()
        batch.recover(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"screened": 1})

    def test_c12_real_surface_full_and_lane_group_round_trip(self):
        for count, expected_lanes in ((1, 1), (4, 4)):
            with self.subTest(count=count):
                self._resize_and_init(count)
                batch.start(self.root, limit=count)
                exported = batch.surface_export(self.root)
                self.assertEqual(exported["runs"], 1)
                checkpoint = batch.show(self.root)
                self.assertEqual(len(checkpoint["surface"]), expected_lanes)
                if count == 4:
                    self.assertTrue(checkpoint["surface"][0]["group_manifest_path"])
                batch.surface_import(self.root, self._surface_outputs())
                self.assertEqual(queue.status(self.root)["explicit_overrides"], {"screened": count})
                batch.abandon(self.root, discard_uncommitted_results=True)
                runtime = queue.checkpoint_path(self.root).parent
                self.assertEqual(list(runtime.glob(".active-batch.json.tmp")), [])
                self.assertEqual(list((runtime / "surface").glob("*")) if (runtime / "surface").exists() else [], [])

    def test_c13_c16_integer_output_key_is_rejected_before_any_write(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        outputs = self._surface_outputs()
        with self.assertRaisesRegex(wp1.ProductionReviewError, "exact strings"):
            batch.surface_import(self.root, {0: outputs["0"]})
        self.assertIsNone(batch._load(queue.checkpoint_path(self.root))["surface"][0]["output_path"])
        batch.abandon(self.root)

    def test_c15_group_consumer_layout_never_touches_preexisting_workspace_task(self):
        self._resize_and_init(4)
        task_file = self.root / ".ai/task/preexisting/STATE.json"
        task_file.parent.mkdir(parents=True)
        task_file.write_bytes(b"keep me")
        batch.start(self.root, limit=4)
        batch.surface_export(self.root)
        self.assertEqual(task_file.read_bytes(), b"keep me")
        self.assertEqual([p.relative_to(self.root).as_posix() for p in self.root.glob(".ai/task/**/SURFACE-*")], [])
        batch.abandon(self.root)

    def test_c12_reimport_requires_exact_output_key_set_and_bytes(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        outputs = self._surface_outputs()
        with self.assertRaisesRegex(wp1.ProductionReviewError, "missing or extra"):
            batch.surface_import(self.root, {"0": outputs["0"], "extra": outputs["0"]})
        with self.assertRaisesRegex(wp1.ProductionReviewError, "rejected"):
            batch.surface_import(self.root, {"0": b"missing output"})
        batch.surface_import(self.root, outputs)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "changed"):
            batch.surface_import(self.root, {"0": outputs["0"][:-1] + b" "})
        batch.abandon(self.root, discard_uncommitted_results=True)

    def test_c12_stale_atomic_temp_is_controlled_and_removed(self):
        self._resize_and_init(1)
        runtime = queue.checkpoint_path(self.root).parent
        runtime.mkdir(parents=True, exist_ok=True)
        (runtime / ".active-batch.json.tmp").write_bytes(b"stale")
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        self.assertFalse((runtime / ".active-batch.json.tmp").exists())
        batch.abandon(self.root)
        residue = [p.name for p in runtime.iterdir()
                   if p.name not in {queue.LOCK_NAME, queue.DATABASE_NAME}]
        self.assertEqual(residue, [])

    def test_real_git_sqlite_batch_start_duplicate_and_abandon_restores_queue(self):
        queue.init(self.root)
        started = batch.start(self.root, limit=1)
        self.assertEqual(started["selected"], 1)
        checkpoint = batch.show(self.root)
        self.assertEqual(checkpoint["entry_snapshots"][0]["prior_effective_state"], "queued")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "active batch"):
            batch.start(self.root, limit=1)
        batch.abandon(self.root)
        self.assertFalse(batch.show(self.root)["active"])
        self.assertEqual(queue.status(self.root)["implicit_queued"], 2)

    def test_catalog_loader_allows_only_planned_quality_sibling(self):
        self.assertEqual(queue.init(self.root)["catalog_id"], self.catalog_id)
        extra = self.root / "i18n/quality/production-review-v2-lite/unplanned.txt"
        extra.write_text("unexpected\n", encoding="utf-8")
        self._commit("unplanned quality sibling")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "sibling|extra"):
            queue.rebuild(self.root)

    def test_implicit_queued_seven_state_schema_and_deterministic_rebuild(self):
        first = queue.init(self.root)
        self.assertEqual(first["implicit_queued"], 2)
        db = queue.database_path(self.root)
        with closing(sqlite3.connect(db)) as connection:
            tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertEqual(tables, {"meta", "state_override", "reconciliation"})
            self.assertEqual(queue.BUSINESS_STATES,
                             {"queued", "reserved", "screened", "deep_required", "repair_required", "done", "blocked"})
            for state in ("queued", "invalid"):
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute("INSERT INTO state_override VALUES (?,?,?,?,?,?,?)",
                                       ("f" * 64, "e" * 64, state, None, 0, None, STAMP))
        self._batch()
        self._commit("batch")
        queue.rebuild(self.root)
        before = queue.business_rows(db)
        db.unlink()
        queue.rebuild(self.root)
        self.assertEqual(queue.business_rows(db), before)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"done": 1})

    def test_failed_validation_preserves_old_database_and_dirty_evidence_is_rejected(self):
        queue.init(self.root)
        db = queue.database_path(self.root)
        old = db.read_bytes()
        root = self._batch()
        (root / "results.jsonl").write_bytes(b"{bad\n")
        self._commit("bad batch")
        with self.assertRaises(wp1.ProductionReviewError):
            queue.rebuild(self.root)
        self.assertEqual(db.read_bytes(), old)
        subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)
        dirty = self.root / "evidence/production-review-v2-lite/dirty"
        dirty.write_text("x")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "clean"):
            queue.rebuild(self.root)

    def test_evidence_rejects_duplicate_keys_invalid_utf8_and_extra_keys(self):
        queue.init(self.root)
        old = queue.database_path(self.root).read_bytes()
        for label in ("duplicate", "utf8", "extra"):
            with self.subTest(label=label):
                root = self._batch()
                path = root / "results.jsonl"
                if label == "duplicate":
                    path.write_bytes(b'{"schema_version":1,"schema_version":1}\n')
                elif label == "utf8":
                    path.write_bytes(b"\xff\n")
                else:
                    row = wp1.parse_jsonl(path.read_bytes(), "result")[0]
                    row["extra"] = True
                    path.write_bytes(wp1._jsonl([row]))
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                manifest["results_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("invalid " + label)
                with self.assertRaises(wp1.ProductionReviewError):
                    queue.rebuild(self.root)
                self.assertEqual(queue.database_path(self.root).read_bytes(), old)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_catalog_reuses_strict_traversal_duplicate_extra_and_nonliteral_checks(self):
        cases = ("traversal", "duplicate-logical", "extra-file", "nonliteral")
        for label in cases:
            with self.subTest(label=label):
                rows = [dict(row) for row in self.entries]
                if label == "traversal":
                    row = rows[0]; row["normalized_path"] = "../tome.lua"
                    core = {"component": row["component"], "duplicate_index": 0, "function_name": "t",
                            "normalized_source_tag": row["source_tag"], "section": row["section"],
                            "source": row["source"], "translation_path": row["normalized_path"]}
                    row["call_locator"] = catalog._plain_id(catalog.CALL_LOCATOR_KIND, "locator", core)
                    row["logical_entry_identity"] = wp1.surface.logical_entry_identity(
                        component=row["component"], normalized_path=row["normalized_path"],
                        call_locator=row["call_locator"], source_tag=row["source_tag"])
                    row["entry_revision_identity"] = wp1.surface.entry_revision_identity(
                        logical_entry_identity=row["logical_entry_identity"], source=row["source"], target=row["target"],
                        fixed_source_identity=row["fixed_source_identity"],
                        terminology_snapshot=row["terminology_snapshot_sha256"], rules_version=row["rules_version"])
                    self._rewrite_catalog(rows)
                elif label == "duplicate-logical":
                    first, row = rows
                    row.update({key: first[key] for key in ("source", "source_sha256", "normalized_path",
                                                            "call_locator", "logical_entry_identity")})
                    row["risk"] = dict(row["risk"]); row["risk"]["source_utf8_bytes"] = len(row["source"].encode())
                    row["entry_revision_identity"] = wp1.surface.entry_revision_identity(
                        logical_entry_identity=row["logical_entry_identity"], source=row["source"], target=row["target"],
                        fixed_source_identity=row["fixed_source_identity"],
                        terminology_snapshot=row["terminology_snapshot_sha256"], rules_version=row["rules_version"])
                    self._rewrite_catalog(rows)
                elif label == "extra-file":
                    extra = self.root / catalog.CATALOG_PREFIX / "extra.json"
                    extra.write_text("{}", encoding="utf-8")
                else:
                    rows[0]["source"] = ["not", "a", "literal"]
                    self._rewrite_catalog(rows)
                self._commit("invalid catalog " + label)
                with self.assertRaises(wp1.ProductionReviewError):
                    queue.init(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)
                self.entries = [self._entry("1"), self._entry("2")]
                self._write_catalog()

    def test_results_require_bound_validator_accepted_adapter_bytes(self):
        for label in ("empty", "unbound", "mismatched", "invalid-raw"):
            with self.subTest(label=label):
                root = self._batch(batch="batch-" + label)
                manifest_path, results_path = root / "manifest.json", root / "results.jsonl"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
                if label == "empty":
                    manifest["adapter_refs"] = []
                    for path in (root / "raw").rglob("*"):
                        if path.is_file(): path.unlink()
                elif label == "unbound":
                    row["input_sha256"] = "e" * 64
                elif label == "mismatched":
                    manifest["adapter_refs"][0]["output_sha256"] = "f" * 64
                else:
                    output = root / "raw/surface/output.json"
                    output.write_bytes(b'{"invalid":true}')
                    digest = hashlib.sha256(output.read_bytes()).hexdigest()
                    manifest["adapter_refs"][0]["output_sha256"] = digest
                    row["output_sha256"] = digest
                results_path.write_bytes(wp1._jsonl([row]))
                manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("invalid adapter " + label)
                with self.assertRaises(wp1.ProductionReviewError):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_results_reject_borrowed_run_for_wrong_revision_surface_and_contextual(self):
        for contract in ("surface", "contextual"):
            with self.subTest(contract=contract):
                self._batch(batch="batch-wrong-" + contract, contract=contract, adapter_entry_index=1)
                self._commit("wrong revision " + contract)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "revision|union|membership"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_results_match_accepted_contract_verdict_and_observation(self):
        for contract in ("surface", "contextual"):
            with self.subTest(contract=contract):
                root = self._batch(batch="batch-verdict-" + contract, contract=contract)
                results_path = root / "results.jsonl"
                row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
                prefix = "surface" if contract == "surface" else "deep"
                row[prefix + "_verdict"] = "ISSUE"
                row[prefix + "_observation"] = "forged observation"
                results_path.write_bytes(wp1._jsonl([row]))
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("forged verdict " + contract)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "verdict|observation|accepted"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_results_validate_matching_surface_contextual_overlap(self):
        root = self._batch(batch="batch-overlap", contract="surface")
        self._add_overlapping_contract(root, "contextual")
        self._commit("matching cross-contract overlap")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "surface ISSUE"):
            queue.rebuild(self.root)

    def test_results_require_null_fields_for_absent_contract(self):
        for contract, forged_prefix in (("surface", "deep"), ("contextual", "surface")):
            with self.subTest(absent=forged_prefix):
                root = self._batch(batch="batch-absent-" + forged_prefix, contract=contract)
                results_path = root / "results.jsonl"
                row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
                row[forged_prefix + "_verdict"] = "OK"
                results_path.write_bytes(wp1._jsonl([row]))
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("forged absent contract " + forged_prefix)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "verdict|observation|accepted"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_results_reject_cross_contract_mismatch_in_both_directions(self):
        for primary, overlapping, forged_prefix in (
                ("surface", "contextual", "deep"),
                ("contextual", "surface", "surface")):
            with self.subTest(forged=forged_prefix):
                root = self._batch(batch="batch-mismatch-" + forged_prefix, contract=primary)
                self._add_overlapping_contract(root, overlapping)
                results_path = root / "results.jsonl"
                row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
                row[forged_prefix + "_verdict"] = "ISSUE"
                row[forged_prefix + "_observation"] = "forged observation"
                results_path.write_bytes(wp1._jsonl([row]))
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("forged cross-contract " + forged_prefix)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "verdict|observation|accepted"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_durable_batch_schema_versions_reject_json_true(self):
        for boundary in ("manifest", "result", "adjudication", "gates"):
            with self.subTest(boundary=boundary):
                root = self._batch(batch="batch-bool-" + boundary)
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                if boundary == "manifest":
                    manifest["schema_version"] = True
                elif boundary == "result":
                    path = root / "results.jsonl"
                    row = wp1.parse_jsonl(path.read_bytes(), "result")[0]
                    row["schema_version"] = True
                    path.write_bytes(wp1._jsonl([row]))
                    manifest["results_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                elif boundary == "adjudication":
                    path = root / "adjudications.jsonl"
                    row = {"schema_version": True, "entry_revision_identity": self.entries[0]["entry_revision_identity"],
                           "observation_sha256": "a" * 64, "disposition": "advisory",
                           "evidence_path": None, "evidence_commit": None, "evidence_snapshot": None,
                           "conclusion": "fixture", "repair_required": False}
                    path.write_bytes(wp1._jsonl([row]))
                    manifest["adjudications_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                else:
                    path = root / "gates.json"
                    path.write_bytes(wp1.canonical_bytes({"schema_version": True, "commands": []}))
                    manifest["gates_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("boolean schema " + boundary)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "schema"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_split_raw_and_core_commits_are_rejected(self):
        queue.init(self.root)
        root = self._batch(batch="batch-split")
        subprocess.run(["git", "add", str(root / "raw")], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "raw before core"], cwd=self.root, check=True)
        raw_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        manifest_path = root / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["base_commit"] = raw_commit
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        self._commit("batch core after raw")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "raw.*one commit|one commit.*raw"):
            queue.rebuild(self.root)

    def test_merged_sibling_identical_publications_are_rejected_as_ambiguous(self):
        queue.init(self.root)
        base = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        self._batch(batch="batch-siblings")
        first = self._commit("first identical publication")

        subprocess.run(["git", "checkout", "-qb", "sibling-publication", base],
                       cwd=self.root, check=True)
        self._batch(batch="batch-siblings")
        self._commit("second identical publication")
        subprocess.run(["git", "merge", "-q", "--no-ff", first, "-m", "merge publications"],
                       cwd=self.root, check=True)

        with self.assertRaisesRegex(wp1.ProductionReviewError, "one commit"):
            queue.rebuild(self.root)

    def test_current_tree_only_and_same_commit_revert_deletion(self):
        queue.init(self.root)
        self._batch()
        committed = self._commit("batch")
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["implicit_queued"], 1)
        subprocess.run(["git", "revert", "--no-edit", committed], cwd=self.root,
                       check=True, stdout=subprocess.DEVNULL)
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["implicit_queued"], 2)
        queue.rebuild(self.root, treeish=committed)
        self.assertEqual(queue.status(self.root, treeish=committed)["implicit_queued"], 1)

    def test_same_path_replacement_revert_restores_prior_publication(self):
        queue.init(self.root)
        root = self._batch(batch="batch-replaced")
        original_commit = self._commit("original batch publication")
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"done": 1})

        input_path = root / "raw/surface/input.json"
        input_value = wp1.parse_canonical_object(input_path.read_bytes(), "surface input")
        input_value["payload"]["rendered_briefing"] = "replacement fixture"
        candidate_identity = hashlib.sha256(wp1.surface.canonical_bytes(input_value["payload"])).hexdigest()
        input_value["candidate_identity"] = candidate_identity
        input_path.write_bytes(wp1.surface.canonical_bytes(input_value))
        output_path = root / "raw/surface/output.json"
        output_value = wp1.parse_canonical_object(output_path.read_bytes(), "surface output")
        output_value["candidate_identity"] = candidate_identity
        output_path.write_bytes(wp1.surface.canonical_bytes(output_value))
        input_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
        output_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()

        results_path = root / "results.jsonl"
        result = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
        result.update({"input_sha256": input_hash, "output_sha256": output_hash,
                       "final_state": "blocked"})
        results_path.write_bytes(wp1._jsonl([result]))
        adjudications_path = root / "adjudications.jsonl"
        adjudications_path.write_bytes(wp1._jsonl([{
            "schema_version": 1, "entry_revision_identity": result["entry_revision_identity"],
            "observation_sha256": "a" * 64, "disposition": "advisory",
            "evidence_path": None, "evidence_commit": None, "evidence_snapshot": None,
            "conclusion": "replacement fixture", "repair_required": False}]))
        gates_path = root / "gates.json"
        gates_path.write_bytes(wp1.canonical_bytes({"schema_version": 1,
                                                     "commands": ["replacement fixture"]}))
        manifest_path = root / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["base_commit"] = original_commit
        manifest["adapter_refs"][0].update({
            "candidate_identity": candidate_identity, "input_sha256": input_hash,
            "output_sha256": output_hash})
        manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
        manifest["adjudications_sha256"] = hashlib.sha256(adjudications_path.read_bytes()).hexdigest()
        manifest["gates_sha256"] = hashlib.sha256(gates_path.read_bytes()).hexdigest()
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        replacement_commit = self._commit("same-path replacement publication")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "adjudications must exactly cover"):
            queue.rebuild(self.root)

        subprocess.run(["git", "revert", "--no-edit", replacement_commit], cwd=self.root,
                       check=True, stdout=subprocess.DEVNULL)
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"done": 1})

    def test_lock_is_nonblocking_and_readers_report_writer(self):
        lock = queue.repository_lock_path(self.root)
        lock.parent.mkdir(parents=True, exist_ok=True)
        with lock.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertTrue(queue.writer_active(self.root))
            with self.assertRaisesRegex(wp1.ProductionReviewError, "lock"):
                queue.init(self.root)
            self.assertTrue(queue.status(self.root)["active_writer"])
            self.assertTrue(queue.check(self.root)["active_writer"])
        self.assertFalse(queue.writer_active(self.root))

    def test_cli_check_exits_nonzero_for_drift_during_active_writer(self):
        queue.init(self.root)
        with closing(sqlite3.connect(queue.database_path(self.root))) as connection:
            connection.execute("UPDATE meta SET catalog_id=?", ("f" * 64,))
            connection.commit()
        lock = queue.repository_lock_path(self.root)
        command = """import argparse, sys
from pathlib import Path
from tools.i18nlib import cli
from tools.i18nlib import production_review_v2_lite_queue as queue
fixture = Path(sys.argv[1])
check = queue.check
cli.production_review_v2_lite_queue.check = lambda _root: check(fixture)
raise SystemExit(cli._production(argparse.Namespace(
    production_command='queue', production_action='check')))
"""
        with lock.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = subprocess.run([sys.executable, "-B", "-c", command, str(self.root)], cwd=ROOT,
                                    capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"active_writer": true', result.stdout)
        self.assertIn('"ok": false', result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_post_replace_check_failure_restores_old_database(self):
        queue.init(self.root)
        database = queue.database_path(self.root)
        old = database.read_bytes()
        original = queue._check_projection

        def fail_post_replace(*args, **kwargs):
            if kwargs.get("database") is None:
                raise wp1.ProductionReviewError("injected post-replace failure")
            return original(*args, **kwargs)

        with mock.patch.object(queue, "_check_projection", side_effect=fail_post_replace):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "injected"):
                queue.rebuild(self.root)
        self.assertEqual(database.read_bytes(), old)
        self.assertEqual(list(database.parent.glob(".queue.sqlite3.rollback.*")), [])

    def test_check_rejects_orphan_override(self):
        queue.init(self.root)
        with closing(sqlite3.connect(queue.database_path(self.root))) as connection:
            connection.execute("INSERT INTO state_override VALUES (?,?,?,?,?,?,?)",
                               ("f" * 64, "e" * 64, "done", None, 0, None, STAMP))
            connection.commit()
        with self.assertRaises(wp1.ProductionReviewError):
            queue.check(self.root)

    def test_missing_real_catalog_is_controlled_cli_failure(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/i18n"),
                                 "production", "queue", "status"], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stdout + result.stderr)


class PublicApiFlowTests(QueueTests):
    def _surface_bytes(self, ref, verdict="OK"):
        raw = Path(ref["input_path"]).read_bytes()
        envelope = wp1.surface.strict_json_bytes(raw, label="surface envelope")
        payload, candidate = wp1.surface.validate_envelope(envelope)
        results = []
        for entry in payload["entries"]:
            item = {"entry_revision_identity": entry["entry_revision_identity"], "verdict": verdict}
            if verdict == "ISSUE":
                item["observation"] = "review issue"
            results.append(item)
        return wp1.surface.canonical_bytes({"contract": wp1.surface.CONTRACT,
            "candidate_identity": candidate, "results": results})

    def _contextual_bytes(self, ref, verdict="OK"):
        raw = Path(ref["input_path"]).read_bytes()
        envelope = contextual_result_check.strict_json_bytes(raw, label="contextual envelope")
        payload, candidate = contextual_result_check.validate_envelope(envelope)
        verdicts = []
        for position, revision in enumerate(payload["ordered_revision_keys"]):
            item_verdict = verdict if position == 0 else "OK"
            item = {"revision_key": revision, "verdict": item_verdict}
            if item_verdict == "ISSUE":
                item["observation"] = "contextual issue"
            verdicts.append(item)
        return wp1.canonical_bytes({"contract": "translation_contextual_v2",
            "candidate_identity": candidate, "verdicts": verdicts})

    def _decision(self, observation, *, disposition="advisory", path=None,
                  commit=None, snapshot=None, repair_required=False):
        return {"entry_revision_identity": observation["entry_revision_identity"],
                "observation_contract": observation["contract"],
                "observation_identity": observation["observation_identity"],
                "observation_sha256": hashlib.sha256(
                    (observation["observation"] or "").encode()).hexdigest(),
                "disposition": disposition, "evidence_path": path,
                "evidence_commit": commit, "evidence_snapshot": snapshot,
                "conclusion": "current producer fixture",
                "repair_required": repair_required}

    def _publish_generated(self, batch_root):
        destination = self.root / "evidence/production-review-v2-lite/batches" / batch_root.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copytree(batch_root, destination)
        self._commit("publish generated evidence")
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

    def test_public_api_all_surface_ok_full_n_1_4_80_and_commit_same_tree(self):
        for count in (1, 4, 80):
            with self.subTest(count=count):
                self._resize_and_init(count)
                batch.start(self.root, limit=count)
                batch.surface_export(self.root)
                checkpoint = batch.show(self.root)
                outputs = {str(i): self._surface_bytes(ref) for i, ref in enumerate(checkpoint["surface"])}
                batch.surface_import(self.root, outputs)
                empty = self.root / "empty-adjudication.json"
                empty.write_bytes(wp1.canonical_bytes({"batch_id": checkpoint["batch_id"], "decisions": []}))
                batch.adjudicate(self.root, empty)
                prepared = batch.prepare_evidence(self.root)
                if count == 80:
                    commit = self._publish_generated(Path(prepared["prospective"]))
                    batch.finalize(self.root, commit)
                else:
                    batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
                self.assertFalse(queue.checkpoint_path(self.root).exists())
                if count == 80:
                    queue.rebuild(self.root)
                self.assertTrue(queue.check(self.root)["ok"])

    def _mixed_identity_entries(self):
        variants = []
        for digit, component, fixed, terminology in (
                ("0", "tome", "commit:" + "a" * 40, "b" * 64),
                ("1", "tome", "commit:" + "a" * 40, "b" * 64),
                ("2", "boot", "commit:" + "d" * 40, "b" * 64),
                ("3", "boot", "commit:" + "d" * 40, "b" * 64)):
            entry = self._entry(digit)
            entry["component"] = component
            entry["fixed_source_identity"] = fixed
            entry["terminology_snapshot_sha256"] = terminology
            core = {"component": component, "duplicate_index": 0, "function_name": "t",
                    "normalized_source_tag": "", "section": "fixture", "source": entry["source"],
                    "translation_path": "tome.lua"}
            entry["call_locator"] = catalog._plain_id(catalog.CALL_LOCATOR_KIND, "locator", core)
            entry["logical_entry_identity"] = wp1.surface.logical_entry_identity(
                component=component, normalized_path="tome.lua", call_locator=entry["call_locator"], source_tag="")
            entry["entry_revision_identity"] = wp1.surface.entry_revision_identity(
                logical_entry_identity=entry["logical_entry_identity"], source=entry["source"], target=entry["target"],
                fixed_source_identity=fixed, terminology_snapshot=terminology, rules_version=catalog.RULES_VERSION)
            variants.append(entry)
        return variants

    def test_public_api_contextual_e2e_mixed_identity_commit_rebuild_revert(self):
        self._resize_and_init(1)
        self.entries = self._mixed_identity_entries()
        self._write_catalog()
        self._rewrite_catalog(self.entries)
        self._commit("mixed identity catalog")
        (self.root / "src.lua").write_text("-- verified public source fixture\\n", encoding="utf-8")
        source_commit = self._commit("public source fixture")
        queue.rebuild(self.root)

        started = batch.start(self.root, limit=4)
        self.assertEqual(started["selected"], 4)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        surface_runs = batch.partition_surface_entries(checkpoint["entry_snapshots"])
        self.assertEqual([min(run["parent_indexes"]) for run in surface_runs], [0, 2])
        self.assertEqual(len({run["identity"] for run in surface_runs}), 2)
        surface_outputs = {str(i): self._surface_bytes(ref, "ISSUE")
                           for i, ref in enumerate(checkpoint["surface"])}
        batch.surface_import(self.root, surface_outputs)

        exported = batch.contextual_export(self.root)
        self.assertEqual(exported["runs"], 2)
        checkpoint = batch.show(self.root)
        runs = batch.partition_contextual_entries(checkpoint)
        self.assertEqual([min(run["parent_indexes"]) for run in runs], [0, 2])
        self.assertEqual(len({run["identity"] for run in runs}), 2)
        deep_indexes = sorted(i for run in runs for i in run["parent_indexes"])
        self.assertEqual(deep_indexes, [0, 1, 2, 3])
        self.assertEqual(sum(len(run["parent_indexes"]) for run in runs), len(set(deep_indexes)))
        for run in runs:
            self.assertEqual(len({(row["fixed_source_identity"], row["terminology_snapshot_sha256"],
                                   row["rules_version"]) for row in run["entries"]}), 1)

        contextual_outputs = {str(i): self._contextual_bytes(ref, "ISSUE")
                              for i, ref in enumerate(checkpoint["contextual"])}
        for ref, raw in zip(checkpoint["contextual"], contextual_outputs.values()):
            self._install_contextual_done_state(ref, raw)
        import_report = batch.contextual_import(self.root, contextual_outputs)
        self.assertEqual(import_report["imported"], 4)
        checkpoint = batch.show(self.root)
        for ref in checkpoint["contextual"]:
            accepted = contextual_result_check.validate_result_bytes(
                Path(ref["input_path"]).read_bytes(), Path(ref["output_path"]).read_bytes())
            expected = [checkpoint["entry_snapshots"][i]["entry_revision_identity"]
                        for i in ref["parent_indexes"]]
            self.assertEqual([item["revision_key"] for item in accepted["verdicts"]], expected)

        decisions = [self._decision(item, disposition="advisory")
                     for item in batch._accepted_observations(batch.show(self.root))]
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": checkpoint["batch_id"], "decisions": decisions}))
        self.assertEqual(batch.adjudicate(self.root, adjudication)["adjudicated"], 4)
        prepared = batch.prepare_evidence(self.root)
        prospective = Path(prepared["prospective"])
        raw_files = sorted(p for p in prospective.rglob("*") if p.is_file())
        self.assertEqual(len(raw_files), 4 + 2 * len(checkpoint["surface"] + checkpoint["contextual"]))
        destination = self.root / "evidence/production-review-v2-lite/batches" / prospective.name
        import shutil
        shutil.copytree(prospective, destination)
        subprocess.run(["git", "add", str(destination.relative_to(self.root))], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "publish mixed identity review evidence"],
                       cwd=self.root, check=True)
        publication = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        changed = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", publication],
                                          cwd=self.root, text=True).splitlines()
        self.assertEqual(len(changed), len(raw_files))
        self.assertTrue(all(path.startswith("evidence/production-review-v2-lite/batches/") for path in changed))
        self.assertEqual(batch.finalize(self.root, publication)["commit"], publication)
        self.assertFalse(queue.checkpoint_path(self.root).exists())
        overrides, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[2] for row in overrides}, {"done"})

        database = queue.database_path(self.root)
        database.unlink()
        Path(str(database) + "-wal").unlink(missing_ok=True)
        Path(str(database) + "-shm").unlink(missing_ok=True)
        queue.rebuild(self.root)
        overrides, _reconciliation, _meta = queue.business_rows(database)
        self.assertEqual({row[2] for row in overrides}, {"done"})
        subprocess.run(["git", "revert", "--no-edit", publication], cwd=self.root, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        queue.rebuild(self.root)
        overrides, _reconciliation, _meta = queue.business_rows(database)
        self.assertEqual(overrides, [])
        self.assertTrue(queue.check(self.root)["ok"])

    def test_public_api_contextual_review_only_mixed_identities_and_unique_outcomes(self):
        self._resize_and_init(4)
        (self.root / "src.lua").write_text("-- public source fixture\n", encoding="utf-8")
        self._commit("public source fixture")
        queue.rebuild(self.root)
        batch.start(self.root, limit=4)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        surface_outputs = {str(i): self._surface_bytes(ref, "ISSUE") for i, ref in enumerate(checkpoint["surface"])}
        batch.surface_import(self.root, surface_outputs)
        exported = batch.contextual_export(self.root)
        self.assertEqual(exported["runs"], 1)
        checkpoint = batch.show(self.root)
        # The real checker is exercised for rejection; acceptance is explicitly
        # supplied only after that fail-closed result, using the public API.
        bad = self.root / "bad-state.json"
        bad.write_text("{}", encoding="utf-8")
        sys.path.insert(0, str(ROOT / "tools"))
        import ai_state_check
        self.assertNotEqual(ai_state_check.check_state(bad, target="DONE", workspace_root=self.root).outcome,
                            "DONE_VERIFIED")
        contextual_outputs = {str(i): self._contextual_bytes(ref, "ISSUE") for i, ref in enumerate(checkpoint["contextual"])}
        for ref, raw in zip(batch.show(self.root)["contextual"], contextual_outputs.values()):
            self._install_contextual_done_state(ref, raw)
        batch.contextual_import(self.root, contextual_outputs)
        input_path = self.root / "adjudication.json"
        issues = [self._decision(item, disposition="advisory")
            for item in batch._accepted_observations(batch.show(self.root))]
        input_path.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"], "decisions": issues}))
        report = batch.adjudicate(self.root, input_path)
        self.assertEqual(report["adjudicated"], len(set(item["entry_revision_identity"] for item in issues)))
        self.assertEqual(len(set(item["entry_revision_identity"] for item in issues)), 4)

    def test_public_api_contextual_n_1_and_80_real_done_verified(self):
        for count in (1, 80):
            with self.subTest(count=count):
                self._resize_and_init(count)
                batch.start(self.root, limit=count)
                batch.surface_export(self.root)
                checkpoint = batch.show(self.root)
                surface_outputs = {str(i): self._surface_bytes(ref, "ISSUE")
                                   for i, ref in enumerate(checkpoint["surface"])}
                batch.surface_import(self.root, surface_outputs)
                exported = batch.contextual_export(self.root)
                checkpoint = batch.show(self.root)
                contextual_outputs = {str(i): self._contextual_bytes(ref, "ISSUE")
                                      for i, ref in enumerate(checkpoint["contextual"])}
                for ref, raw in zip(checkpoint["contextual"], contextual_outputs.values()):
                    self._install_contextual_done_state(ref, raw)
                batch.contextual_import(self.root, contextual_outputs)
                accepted = contextual_result_check.validate_result_bytes(
                    Path(checkpoint["contextual"][0]["input_path"]).read_bytes(),
                    contextual_outputs["0"])
                issue = next(item for item in accepted["verdicts"] if item["verdict"] == "ISSUE")
                adjudication = self.root / "adjudication.json"
                decisions = [self._decision(item, disposition="advisory")
                             for item in batch._accepted_observations(batch.show(self.root))]
                adjudication.write_bytes(wp1.canonical_bytes({"batch_id": checkpoint["batch_id"], "decisions": decisions}))
                report = batch.adjudicate(self.root, adjudication)
                self.assertEqual(report["adjudicated"], len(set(item["entry_revision_identity"] for item in decisions)))
                batch.abandon(self.root, discard_uncommitted_results=True)
                self.assertFalse(queue.checkpoint_path(self.root).exists())

    def test_public_api_checkpoint_first_recovery_delete_rebuild_revert_and_forged_adjudication(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        checkpoint = queue.checkpoint_path(self.root)
        database = queue.database_path(self.root)
        database.unlink()
        batch.recover(self.root)
        self.assertTrue(database.exists())
        batch.surface_import(self.root, {"0": self._surface_bytes(batch.show(self.root)["surface"][0])})
        empty = self.root / "empty.json"
        empty.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"], "decisions": []}))
        batch.adjudicate(self.root, empty)
        batch.prepare_evidence(self.root)
        value = batch.show(self.root)
        forged = self.root / "forged.json"
        forged.write_bytes(wp1.canonical_bytes({"batch_id": value["batch_id"], "decisions": [{"bad": True}]}))
        with self.assertRaises(wp1.ProductionReviewError):
            batch.adjudicate(self.root, forged)
        self.assertTrue(checkpoint.exists())
        batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
        self.assertFalse(checkpoint.exists())
        queue.rebuild(self.root)
        self.assertTrue(queue.check(self.root)["ok"])


class C31PublicApiTests(PublicApiFlowTests):
    def _contextual_issue_ready(self, count=1, *, surface_verdict="ISSUE", source_before=False):
        self._resize_and_init(count)
        if source_before:
            (self.root / "source.lua").write_text("-- C31 public source\n", encoding="utf-8")
            self._commit("C31 source")
            queue.rebuild(self.root)
        batch.start(self.root, limit=count)
        batch.surface_export(self.root)
        batch.surface_import(self.root, {str(i): self._surface_bytes(ref, surface_verdict)
                                         for i, ref in enumerate(batch.show(self.root)["surface"])})
        batch.contextual_export(self.root)
        ref = batch.show(self.root)["contextual"][0]
        output = self._contextual_bytes(ref, "ISSUE")
        return ref, output

    def _install_and_import_contextual(self, ref, output):
        self._install_contextual_done_state(ref, output)
        return batch.contextual_import(self.root, {"0": output})

    def _legacy_decision(self, observation, *, disposition="advisory", path=None,
                         commit=None, snapshot=None, repair_required=False):
        # Keep the historical helper name for older test call sites while
        # emitting the current producer's exact contract binding.  A textual
        # legacy snapshot is upgraded to the exact named Git blob.
        if commit is not None and path is not None and snapshot is not None:
            commit_id = commit[7:] if commit.startswith("commit:") else commit
            raw = subprocess.check_output(
                ["git", "cat-file", "blob", f"{commit_id}:{path}"],
                cwd=self.root)
            snapshot = {"sha256": hashlib.sha256(raw).hexdigest(),
                        "content_base64": __import__("base64").b64encode(raw).decode("ascii")}
        return self._decision(observation, disposition=disposition, path=path,
                              commit=commit, snapshot=snapshot,
                              repair_required=repair_required)

    def _decision(self, observation, *, disposition="advisory", path=None,
                  commit=None, snapshot=None, repair_required=False):
        return {"entry_revision_identity": observation["entry_revision_identity"],
                "observation_contract": observation["contract"],
                "observation_identity": observation["observation_identity"],
                "observation_sha256": hashlib.sha256(
                    (observation["observation"] or "").encode()).hexdigest(),
                "disposition": disposition, "evidence_path": path,
                "evidence_commit": commit, "evidence_snapshot": snapshot,
                "conclusion": "C31 fixture", "repair_required": repair_required}

    def test_c31_contextual_full_n4_publish(self):
        ref, output = self._contextual_issue_ready(4, source_before=True)
        # A full run must be bound to the exact producer output, not merely to
        # a validator-accepted result.  The predecessor accepts this forged
        # but contract-valid alternate verdict.
        self._install_contextual_done_state(ref, output)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "DONE_VERIFIED"):
            batch.contextual_import(self.root, {"0": self._contextual_bytes(ref, "OK")})
        self._install_and_import_contextual(ref, output)
        observations = batch._accepted_observations(batch.show(self.root))
        self.assertEqual(len(observations), 5)  # four surface + one contextual ISSUE
        source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        decisions = []
        for item in observations:
            if item["contract"] == "translation_contextual_v2":
                decisions.append(self._legacy_decision(
                    item, disposition="confirmed", path="source.lua",
                    commit="commit:" + source_commit, snapshot="source"))
            else:
                decisions.append(self._legacy_decision(item, disposition="advisory"))
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                       "decisions": decisions}))
        self.assertEqual(batch.adjudicate(self.root, adjudication)["adjudicated"], 4)
        prepared = batch.prepare_evidence(self.root)
        published = self._publish_generated(Path(prepared["prospective"]))
        self.assertEqual(batch.finalize(self.root, published)["commit"], published)
        self.assertFalse(queue.checkpoint_path(self.root).exists())
        self.assertTrue(queue.check(self.root)["ok"])

    def test_c31_fresh_contextual_import_without_done_verified_fails(self):
        ref, output = self._contextual_issue_ready()
        with self.assertRaisesRegex(wp1.ProductionReviewError, "DONE_VERIFIED"):
            batch.contextual_import(self.root, {"0": output})
        self.assertIsNone(batch.show(self.root)["contextual"][0]["output_path"])
        batch.abandon(self.root, discard_uncommitted_results=True)

    def test_c31_unrelated_task_candidate_input_and_output_done_fail(self):
        cases = ("task", "candidate", "input", "output")
        for kind in cases:
            with self.subTest(kind=kind):
                shutil.rmtree(self.root / ".ai", ignore_errors=True)
                ref, output = self._contextual_issue_ready(1 if kind in {"task", "input"} else 2)
                self._install_contextual_done_state(ref, output)
                checkpoint = batch._load(queue.checkpoint_path(self.root))
                if kind == "task":
                    checkpoint["contextual"][0]["task_id"] = "unrelated-task"
                elif kind == "candidate":
                    checkpoint["contextual"][0]["candidate_identity"] = "0" * 64
                elif kind == "input":
                    Path(ref["input_path"]).write_bytes(Path(ref["input_path"]).read_bytes() + b" ")
                else:
                    output = output[:-1] + b" "
                if kind in {"task", "candidate"}:
                    batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
                with self.assertRaises(wp1.ProductionReviewError):
                    batch.contextual_import(self.root, {"0": output})
                shutil.rmtree(self.root / ".ai", ignore_errors=True)

    def test_c31_two_observations_same_revision_keep_two_adjudications_and_fold_state(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        observations = batch._accepted_observations(batch.show(self.root))
        same_revision = [item for item in observations
                         if item["entry_revision_identity"] == observations[0]["entry_revision_identity"]]
        self.assertEqual(len(same_revision), 2)
        adjudication = self.root / "adjudication.json"
        evidence = {"sha256": hashlib.sha256(b"C31 source snapshot").hexdigest(),
                    "content": "C31 source snapshot"}
        decisions = [self._decision(item, disposition=("confirmed" if index == 0 else "advisory"),
                                     snapshot=(evidence if index == 0 else None),
                                     repair_required=(index == 0))
                     for index, item in enumerate(same_revision)]
        adjudication.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"], "decisions": decisions}))
        self.assertEqual(batch.adjudicate(self.root, adjudication)["repair_required"], 1)
        checkpoint = batch.show(self.root)
        self.assertEqual(len(checkpoint["adjudications"]), 2)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"repair_required": 1})

    def test_c31_free_form_snapshot_and_absolute_path_are_rejected(self):
        for forged in ((None, None, "not-a-snapshot"), ("/tmp/forged.lua", None, None)):
            with self.subTest(forged=forged):
                ref, output = self._contextual_issue_ready()
                self._install_and_import_contextual(ref, output)
                observations = batch._accepted_observations(batch.show(self.root))
                path, commit, snapshot = forged
                decisions = [self._legacy_decision(item) for item in observations]
                decisions[0] = self._legacy_decision(observations[0], disposition="confirmed", path=path,
                                                     commit=commit, snapshot=snapshot)
                input_path = self.root / "adjudication.json"
                input_path.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                            "decisions": decisions}))
                with self.assertRaises(wp1.ProductionReviewError):
                    batch.adjudicate(self.root, input_path)
                batch.abandon(self.root, discard_uncommitted_results=True)
        # A normalized path is part of the current source-evidence contract.
        # The predecessor's existence-only check accepts this equivalent path.
        ref, output = self._contextual_issue_ready(1, source_before=True)
        self._install_and_import_contextual(ref, output)
        source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        tree = subprocess.check_output(["git", "rev-parse", f"{source_commit}^{{tree}}"], cwd=self.root, text=True).strip()
        observations = batch._accepted_observations(batch.show(self.root))
        decisions = [self._decision(item, disposition="confirmed", path="source.lua",
                                     commit="commit:" + tree, snapshot=None)
                     for item in observations]
        input_path = self.root / "adjudication.json"
        input_path.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                    "decisions": decisions}))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "public-source path"):
            batch.adjudicate(self.root, input_path)
        batch.abandon(self.root, discard_uncommitted_results=True)

    def test_c31_checkpoint_first_postimage_mismatch_keeps_checkpoint_then_restores(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                       "decisions": [self._legacy_decision(item) for item in
                                                                      batch._accepted_observations(batch.show(self.root))]}))
        batch.adjudicate(self.root, adjudication)
        prepared = batch.prepare_evidence(self.root)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        self.assertIsInstance(checkpoint["gates"]["prospective"], dict)
        self.assertEqual(set(checkpoint["gates"]), {"commands", "prospective", "preimage_absent",
                                                     "prospective_bytes", "committed_bytes"})
        prospective = Path(prepared["prospective"])
        target = next(path for path in prospective.rglob("*") if path.is_file())
        original = target.read_bytes()
        target.write_bytes(original + b"tamper")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "postimages"):
            batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
        self.assertTrue(queue.checkpoint_path(self.root).exists())
        # The checkpoint remains the recovery authority until a later
        # operator retry; this test intentionally leaves its scratch tree to
        # TemporaryDirectory cleanup.

    def test_c31_committed_overbudget_and_gate_mismatch_fail_closed(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                       "decisions": [self._legacy_decision(item) for item in
                                                                      batch._accepted_observations(batch.show(self.root))]}))
        batch.adjudicate(self.root, adjudication)
        prepared = batch.prepare_evidence(self.root)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        self.assertIsInstance(checkpoint["gates"]["prospective"], dict)
        prospective = Path(prepared["prospective"])
        published = self._publish_generated(prospective)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        checkpoint["gates"]["committed_bytes"] = 0
        batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
        with mock.patch.object(catalog, "TRACKED_LIMIT", 0):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "128 MiB"):
                batch.finalize(self.root, published)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        checkpoint["gates"]["committed_bytes"] = batch._committed_production_bytes(self.root, published) + 1
        batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "occupancy"):
            batch.finalize(self.root, published)

    def test_c39_named_dual_observations_publish_and_rebuild(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        observations = batch._accepted_observations(batch.show(self.root))
        decisions = [{"entry_revision_identity": item["entry_revision_identity"],
                      "observation_contract": item["contract"],
                      "observation_identity": item["observation_identity"],
                      "observation_sha256": hashlib.sha256(
                          (item["observation"] or "").encode()).hexdigest(),
                      "disposition": "advisory", "evidence_path": None,
                      "evidence_commit": None, "evidence_snapshot": None,
                      "conclusion": "C39 named dual observation", "repair_required": False}
                     for item in observations]
        input_path = self.root / "c39-adjudication.json"
        input_path.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"], "decisions": decisions}))
        self.assertEqual(batch.adjudicate(self.root, input_path)["adjudicated"], 1)
        prepared = batch.prepare_evidence(self.root)
        published = self._publish_generated(Path(prepared["prospective"]))
        self.assertEqual(batch.finalize(self.root, published)["commit"], published)
        queue.rebuild(self.root)
        overrides, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[2] for row in overrides}, {"done"})

    def test_c40_repeated_recovery_accepts_exact_previous_and_desired_tuples(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        reserved = queue.business_rows(queue.database_path(self.root))[0][0]
        surface_ref = batch.show(self.root)["surface"][0]
        batch.surface_import(self.root, {"0": self._surface_bytes(surface_ref, "ISSUE")})
        surface_complete = queue.business_rows(queue.database_path(self.root))[0][0]
        with sqlite3.connect(queue.database_path(self.root)) as connection:
            connection.execute("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", reserved)
            connection.commit()
        batch.recover(self.root)
        batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][:6], surface_complete[:6])
        batch.contextual_export(self.root)
        checkpoint = batch.show(self.root)
        contextual_output = self._contextual_bytes(checkpoint["contextual"][0], "ISSUE")
        self._install_contextual_done_state(checkpoint["contextual"][0], contextual_output)
        batch.contextual_import(self.root, {"0": contextual_output})
        contextual_complete = queue.business_rows(queue.database_path(self.root))[0][0]
        with sqlite3.connect(queue.database_path(self.root)) as connection:
            connection.execute("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", surface_complete)
            connection.commit()
        batch.recover(self.root)
        batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][:6], contextual_complete[:6])
        observations = batch._accepted_observations(batch.show(self.root))
        adjudication = self.root / "c40-adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"],
            "decisions": [self._legacy_decision(item) for item in observations]}))
        batch.adjudicate(self.root, adjudication)
        final_complete = queue.business_rows(queue.database_path(self.root))[0][0]
        with sqlite3.connect(queue.database_path(self.root)) as connection:
            connection.execute("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", contextual_complete)
            connection.commit()
        batch.recover(self.root)
        batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][:6], final_complete[:6])

    def _run_c45_surface_issue_contextual_ok(self, disposition, expected_state):
        ref, output = self._contextual_issue_ready()
        output = self._contextual_bytes(ref, "OK")
        self._install_and_import_contextual(ref, output)
        observations = batch._accepted_observations(batch.show(self.root))
        self.assertEqual({item["contract"] for item in observations},
                         {"translation_surface_screen_v1"})
        snapshot = {"sha256": hashlib.sha256(b"C45 source").hexdigest(),
                    "content": "C45 source"}
        decisions = [self._decision(
            item, disposition=disposition,
            snapshot=snapshot if disposition == "confirmed" else None,
            repair_required=disposition == "confirmed")
            for item in observations]
        adjudication = self.root / "c45-adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"],
            "decisions": decisions}))
        batch.adjudicate(self.root, adjudication)
        self.assertEqual(queue.status(self.root)["explicit_overrides"],
                         {expected_state: 1})
        prepared = batch.prepare_evidence(self.root)
        published = self._publish_generated(Path(prepared["prospective"]))
        if disposition == "confirmed":
            batch.finalize(self.root, published)
        else:
            # Exercise committed-before-finalize recovery for the pending
            # fold, then rebuild from the durable Git tree.
            batch.recover(self.root)
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"],
                         {expected_state: 1})

    def test_c45_surface_issue_contextual_ok_confirmed_repair(self):
        self._run_c45_surface_issue_contextual_ok("confirmed", "repair_required")

    def test_c45_surface_issue_contextual_ok_pending_blocked(self):
        self._run_c45_surface_issue_contextual_ok("pending", "blocked")

    def test_c46_exact_prospective_temps_resume_and_abandon_is_mutation_free(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        batch.surface_import(self.root, {"0": self._surface_bytes(
            checkpoint["surface"][0], "OK")})
        empty = self.root / "c46-empty.json"
        empty.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"], "decisions": []}))
        batch.adjudicate(self.root, empty)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        declared = batch._prospective_declared_paths(checkpoint)
        checkpoint["gates"] = {
            "commands": [],
            "prospective": {path: None for path in sorted(declared)},
            "preimage_absent": sorted(declared),
            "prospective_bytes": 0,
            "committed_bytes": 0,
        }
        batch._atomic(queue.checkpoint_path(self.root),
                      batch._checkpoint_bytes(checkpoint))
        runtime = batch._prospective_batch_path(self.root, checkpoint["batch_id"])
        core = runtime / "manifest.json"
        raw = runtime / "raw/surface/000-input_path.json"
        output = runtime / "raw/surface/000-output_path.json"
        core.parent.mkdir(parents=True, exist_ok=True)
        raw.parent.mkdir(parents=True, exist_ok=True)
        (core.with_name("." + core.name + ".tmp")).write_bytes(b"partial core")
        # These are the exact destinations used by _write_fsynced below;
        # recovery must remove their atomic temp targets before retrying.
        (raw.with_name("." + raw.name + ".tmp")).write_bytes(b"partial raw")
        (output.with_name("." + output.name + ".tmp")).write_bytes(b"partial output")
        script = self.root / "tools/ci-gates.sh"
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text("#!/bin/sh\nexit 9\n", encoding="utf-8")
        script.chmod(0o755)
        with mock.patch.dict(os.environ, {"I18N_CI_GATES_FROM_PRODUCTION": "1"}):
            prepared = batch.prepare_evidence(self.root)
        self.assertFalse((core.with_name("." + core.name + ".tmp")).exists())
        self.assertFalse((raw.with_name("." + raw.name + ".tmp")).exists())
        self.assertFalse((output.with_name("." + output.name + ".tmp")).exists())
        self.assertFalse(any("tools/ci-gates.sh" in command
                             for command in batch.show(self.root)["gates"]["commands"]))
        manifest = wp1.parse_canonical_object(
            (Path(prepared["prospective"]) / "manifest.json").read_bytes(), "manifest")
        self.assertEqual(manifest["adapter_refs"][0]["input_path"].split("/")[-1],
                         batch._raw_evidence_name(0, "input_path"))
        self.assertEqual(manifest["adapter_refs"][0]["output_path"].split("/")[-1],
                         batch._raw_evidence_name(0, "output_path"))
        database = queue.database_path(self.root)
        before_db = database.read_bytes()
        checkpoint_path = queue.checkpoint_path(self.root)
        before_checkpoint = checkpoint_path.read_bytes()
        unexpected = Path(prepared["prospective"]) / "unexpected.tmp"
        unexpected.write_bytes(b"not generated")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "undeclared"):
            batch.abandon(self.root, discard_uncommitted_results=True,
                          restore_evidence=True)
        self.assertEqual(database.read_bytes(), before_db)
        self.assertEqual(checkpoint_path.read_bytes(), before_checkpoint)
        self.assertTrue(checkpoint_path.exists())
        unexpected.unlink()
        batch.abandon(self.root, discard_uncommitted_results=True,
                      restore_evidence=True)
        self.assertFalse(checkpoint_path.exists())
        self.assertFalse(Path(prepared["prospective"]).exists())

    def test_c47_gate_records_include_current_consumers_full_ci_and_failures(self):
        script = self.root / "tools/ci-gates.sh"
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text("#!/bin/sh\nprintf 'build gate\\n'\n", encoding="utf-8")
        script.chmod(0o755)
        for name in ("test_surface_screen_manifest.py",
                     "test_surface_screen_result_check.py",
                     "test_contextual_result_check.py"):
            (self.root / "tests/i18n" / name).parent.mkdir(parents=True, exist_ok=True)
            (self.root / "tests/i18n" / name).write_text(
                "import unittest\nclass TestConsumer(unittest.TestCase):\n"
                "    def test_placeholder(self):\n        pass\n",
                encoding="utf-8")
        # The fake outer call must be tested with the recursion marker absent,
        # even when the real full gate invokes this test with the marker set.
        with mock.patch.dict(os.environ):
            os.environ.pop("I18N_CI_GATES_FROM_PRODUCTION", None)
            records = batch._actual_gate_records(self.root)
            commands = [record["command"] for record in records]
            consumer_command = next(command for command in commands
                                    if "test_surface_screen_manifest.py" in command)
            self.assertIn("test_contextual_result_check.py", consumer_command)
            self.assertTrue(any("tools/ci-gates.sh" in command for command in commands))
            script.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
            with self.assertRaisesRegex(wp1.ProductionReviewError, "gate command failed"):
                batch._actual_gate_records(self.root)

        # A nested prepare/full-gate context omits only the recursive full CI;
        # current-consumer checks remain applicable and are still recorded.
        script.write_text("#!/bin/sh\nprintf 'nested full gate must not run\\n'\n", encoding="utf-8")
        with mock.patch.dict(os.environ, {"I18N_CI_GATES_FROM_PRODUCTION": "1"}):
            nested = batch._actual_gate_records(self.root)
        nested_commands = [record["command"] for record in nested]
        nested_consumer = next(command for command in nested_commands
                               if "test_surface_screen_manifest.py" in command)
        self.assertIn("test_contextual_result_check.py", nested_consumer)
        self.assertFalse(any("tools/ci-gates.sh" in command for command in nested_commands))

    def test_c48_public_cli_recovery_aliases_rebuild_temp_sqlite_idempotently(self):
        self._batch(batch="c48-cli")
        self._commit("C48 durable evidence")
        queue.init(self.root)
        database = queue.database_path(self.root)
        database.unlink()
        Path(str(database) + "-wal").unlink(missing_ok=True)
        Path(str(database) + "-shm").unlink(missing_ok=True)
        environment = os.environ.copy()
        environment["I18N_REPOSITORY_ROOT"] = str(self.root)
        command = [sys.executable, "-B", str(ROOT / "tools/i18n"),
                   "production", "batch"]
        reports = []
        first_rows = None
        for action in (("recover", "--from-head"), ("recover-from-head",)):
            result = subprocess.run(command + list(action), cwd=ROOT,
                                    env=environment, capture_output=True,
                                    text=True)
            self.assertEqual(result.returncode, 0,
                             result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertTrue(report["ok"])
            reports.append(report)
            current_rows = queue.business_rows(database)[0]
            if first_rows is None:
                first_rows = current_rows
            else:
                self.assertEqual(first_rows, current_rows)
        self.assertTrue(database.exists())
        self.assertTrue(all(report["recovered"] for report in reports))

    def test_c42_interrupted_prepare_reuses_canonical_inventory_and_can_abandon(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        batch.surface_import(self.root, {"0": self._surface_bytes(
            checkpoint["surface"][0], "OK")})
        empty = self.root / "c42-empty.json"
        empty.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"], "decisions": []}))
        batch.adjudicate(self.root, empty)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        declared = batch._prospective_declared_paths(checkpoint)
        checkpoint["gates"] = {"commands": [],
                                "prospective": {path: None for path in sorted(declared)},
                                "preimage_absent": sorted(declared),
                                "prospective_bytes": 0, "committed_bytes": 0}
        batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
        runtime = batch._prospective_batch_path(self.root, checkpoint["batch_id"])
        (runtime / "manifest.json").parent.mkdir(parents=True, exist_ok=True)
        (runtime / "manifest.json").write_bytes(b"partial prepare")
        batch.prepare_evidence(self.root)
        batch.abandon(self.root, discard_uncommitted_results=True,
                      restore_evidence=True)
        self.assertFalse(queue.checkpoint_path(self.root).exists())
        self.assertFalse(runtime.exists())

    def test_c31_wal_rollback_preserves_old_logical_projection(self):
        queue.init(self.root)
        database = queue.database_path(self.root)
        with sqlite3.connect(database) as connection:
            connection.execute("UPDATE meta SET catalog_id=?", ("e" * 64,))
            connection.commit()
        before = queue.business_rows(database)
        original = queue._check_projection
        def fail_after_replace(*args, **kwargs):
            if kwargs.get("database") is None:
                raise wp1.ProductionReviewError("C31 injected failure")
            return original(*args, **kwargs)
        with mock.patch.object(queue, "_check_projection", side_effect=fail_after_replace):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "C31 injected"):
                queue.rebuild(self.root)
        self.assertEqual(queue.business_rows(database), before)

    def test_c44_direct_cli_forms_cover_active_batch_actions(self):
        from tools.i18nlib import cli
        parser = cli._parser()
        cases = (
            (["production", "batch", "start", "--limit", "1"], "start"),
            (["production", "batch", "show"], "show"),
            (["production", "batch", "abandon", "--discard-uncommitted-results", "--restore-evidence"], "abandon"),
            (["production", "batch", "recover", "--from-head"], "recover"),
            (["production", "batch", "surface-export"], "surface-export"),
            (["production", "batch", "surface-import", "--input", "result.json"], "surface-import"),
            (["production", "batch", "contextual-export"], "contextual-export"),
            (["production", "batch", "contextual-import", "--input", "result.json"], "contextual-import"),
            (["production", "batch", "adjudicate", "--input", "adjudications.json"], "adjudicate"),
            (["production", "batch", "prepare-evidence"], "prepare-evidence"),
            (["production", "batch", "finalize", "--commit", "HEAD"], "finalize"),
            (["production", "batch", "recover-from-head"], "recover-from-head"),
        )
        for argv, expected in cases:
            with self.subTest(argv=argv):
                self.assertEqual(parser.parse_args(argv).production_action, expected)

    def test_c31_recover_from_head_cli_alias_no_checkpoint_missing_db_is_idempotent(self):
        from tools.i18nlib import cli
        parser = cli._parser()
        self.assertEqual(parser.parse_args(["production", "batch", "recover", "--from-head"]).production_action, "recover")
        self.assertEqual(parser.parse_args(["production", "batch", "recover-from-head"]).production_action, "recover-from-head")
        queue.init(self.root)
        database = queue.database_path(self.root)
        database.unlink()
        self.assertTrue(batch.recover(self.root)["ok"])
        first = batch.finalize(self.root, queue._head(self.root, "HEAD"))
        second = batch.finalize(self.root, queue._head(self.root, "HEAD"))
        self.assertEqual(first, {"active": False, "ok": True})
        self.assertEqual(second, first)
        self.assertTrue(database.exists())


if __name__ == "__main__":
    unittest.main()
