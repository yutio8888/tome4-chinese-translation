from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as v2
from tools import translation_review_ledger as ledger

ROOT = Path(__file__).resolve().parents[2]
STAMP = "2026-09-01T01:02:03Z"
COMPONENTS = ["engine", "boot", "tome", "example", "example-realtime", "addon-dev",
              "ashes-urhrok", "cults", "items-vault", "orcs", "possessors"]
SOURCES = {name: "commit:" + "4" * 40 for name in wp1.IN_SCOPE_COMPONENTS}


def occurrences():
    return [wp1.make_occurrence(name, f"{name}.lua", index, {
        "function_name": "t", "section": "section", "source": f"Source {name}",
        "target": f"目标 {name}", "source_tag": None, "args_order": None, "special": None,
    }) for index, name in enumerate(COMPONENTS)]


def ledger_record(digest: str):
    return {"schema_version": 1, "logical_entry_identity": "a" * 64,
            "entry_revision_identity": "b" * 64, "from_state": None, "to_state": "queued",
            "reason_code": "revision_frozen", "provenance": {"kind": "revision_freeze_record", "sha256": digest},
            "recorded_by": "tester", "recorded_at": STAMP, "parent_revision_identity": None,
            "migration_from_logical_entry_identity": None}


class ProductionReviewV2LiteTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".artifacts/i18n").mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".artifacts/i18n")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "tools/i18nlib").mkdir(parents=True)
        (self.root / "tools/i18nlib/locale_model.py").write_bytes(b"loader")
        self.manifest = SimpleNamespace(root=self.root, raw_bytes=b"manifest",
            components=[SimpleNamespace(id=name) for name in COMPONENTS])
        runtime = mock.Mock(); runtime.doctor.return_value = {"lua_version": "Lua 5.1", "luajit_version": "LuaJIT"}
        self.patches = [mock.patch.object(v2, "LuaRuntime", return_value=runtime),
            mock.patch.object(wp1, "load_occurrences", return_value=occurrences()),
            mock.patch.object(wp1, "terminology_snapshot", return_value="3" * 64),
            mock.patch.object(wp1, "source_identities_from_manifest", return_value=SOURCES)]
        for patch in self.patches: patch.start(); self.addCleanup(patch.stop)

    def candidate(self):
        files = v2.build_catalog(self.manifest, recorded_at=STAMP, recorded_by="tester",
                                 require_current_vector=False)
        output = self.root / "candidate"
        v2.write_candidate(files, output, repository_root=ROOT)
        return output, files

    def historical_v1_files(self):
        files = v2.build_catalog(self.manifest, recorded_at=STAMP, recorded_by="tester",
                                 require_current_vector=False)
        entries, exclusions = v2.formal_rows(
            occurrences(), terminology="3" * 64, sources=SOURCES,
            rules_version=v2.FROZEN_RULES_VERSION)
        entries_raw, exclusions_raw = wp1._jsonl(entries), wp1._jsonl(exclusions)
        path = f"{v2.CATALOG_PREFIX}/manifest.json"
        manifest = wp1.parse_canonical_object(files[path], "manifest")
        manifest.update({
            "rules_version": v2.FROZEN_RULES_VERSION,
            "entries_sha256": hashlib.sha256(entries_raw).hexdigest(),
            "exclusions_sha256": hashlib.sha256(exclusions_raw).hexdigest(),
            "policy_sha256": hashlib.sha256(v2.FROZEN_POLICY_RAW).hexdigest(),
        })
        manifest["catalog_id"] = v2.catalog_id(manifest)
        files[v2.POLICY_PATH] = v2.FROZEN_POLICY_RAW
        files[path] = wp1.canonical_bytes(manifest)
        files[f"{v2.CATALOG_PREFIX}/entries.jsonl"] = entries_raw
        files[f"{v2.CATALOG_PREFIX}/exclusions.jsonl"] = exclusions_raw
        return files

    def test_exact_formal_catalog_reconstructs_and_uses_fresh_identity(self):
        output, files = self.candidate()
        value = v2.check_catalog_tree(output, self.manifest, require_current_vector=False)
        self.assertEqual((value["occurrence_count"], value["entry_count"], value["exclusion_count"]), (11, 6, 5))
        self.assertEqual(sum(value["component_counts"].values()), 11)
        entries = wp1.parse_jsonl(files[f"{v2.CATALOG_PREFIX}/entries.jsonl"], "entries")
        self.assertEqual(set(entries[0]), v2.ENTRY_KEYS)
        self.assertEqual([row["entry_revision_identity"] for row in entries],
                         sorted(row["entry_revision_identity"] for row in entries))
        wp1_locator = wp1.make_locator_row(occurrences()[0], wp1.make_allocation(occurrences()[0]))["call_locator"]
        self.assertNotIn(wp1_locator, {row["call_locator"] for row in entries})

    def test_candidate_rejects_noncanonical_duplicate_invalid_and_extra(self):
        output, _ = self.candidate(); manifest_path = output / v2.CATALOG_PREFIX / "manifest.json"
        original = manifest_path.read_bytes()
        mutations = [json.dumps(json.loads(original), indent=2).encode(), b'{"a":1,"a":2}', b"\xff"]
        for raw in mutations:
            with self.subTest(raw=raw[:10]):
                manifest_path.write_bytes(raw)
                with self.assertRaises((wp1.ProductionReviewError, ledger.LedgerError)):
                    v2.check_catalog_tree(output, self.manifest, require_current_vector=False)
                manifest_path.write_bytes(original)
        (output / "extra").write_bytes(b"x")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "exact tree"):
            v2.check_catalog_tree(output, self.manifest, require_current_vector=False)

    def test_candidate_rejects_symlink_and_live_drift(self):
        output, _ = self.candidate(); entries = output / v2.CATALOG_PREFIX / "entries.jsonl"
        body = entries.read_bytes(); entries.unlink(); entries.symlink_to(output / v2.POLICY_PATH)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "symlink"):
            v2.check_catalog_tree(output, self.manifest, require_current_vector=False)
        entries.unlink(); entries.write_bytes(body)
        with mock.patch.object(wp1, "load_occurrences", return_value=occurrences()[:-1]):
            with self.assertRaises((wp1.ProductionReviewError, ledger.LedgerError)):
                v2.check_catalog_tree(output, self.manifest, require_current_vector=False)

    def test_formal_ledger_consumer_accepts_only_exact_manifest_and_provenance(self):
        _, files = self.candidate()
        v2.validate_catalog_files(files)
        raw = files[f"{v2.CATALOG_PREFIX}/manifest.json"]
        digest = hashlib.sha256(raw).hexdigest()
        value = ledger.validate_authoritative_catalog(raw, expected_sha256=digest)
        self.assertEqual(value["kind"], v2.CATALOG_KIND)
        self.assertEqual(value["rules_version"], v2.RULES_VERSION)
        ledger.replay_with_catalog([ledger_record(digest)], raw)
        with self.assertRaisesRegex(ledger.LedgerError, "does not bind"):
            ledger.replay_with_catalog([ledger_record("0" * 64)], raw)
        changed = copy.deepcopy(value); changed["catalog_id"] = "0" * 64
        with self.assertRaisesRegex(ledger.LedgerError, "self-ID"):
            ledger.validate_authoritative_catalog(wp1.canonical_bytes(changed))
        shadow = {"schema_version": 1, "kind": "production_catalog_shadow_v1"}
        with self.assertRaisesRegex(ledger.LedgerError, "exact schema"):
            ledger.validate_authoritative_catalog(wp1.canonical_bytes(shadow))
        non_padded = copy.deepcopy(value)
        non_padded["recorded_at"] = "2026-9-1T01:02:03Z"
        non_padded["catalog_id"] = v2.catalog_id(non_padded)
        with self.assertRaisesRegex(ledger.LedgerError, "strict UTC seconds"):
            ledger.validate_authoritative_catalog(wp1.canonical_bytes(non_padded))

    def test_current_v2_and_historical_v1_catalogs_validate_exactly(self):
        _, current = self.candidate()
        historical = self.historical_v1_files()
        for label, files, rules in (
            ("current", current, v2.RULES_VERSION),
            ("historical", historical, v2.FROZEN_RULES_VERSION),
        ):
            with self.subTest(label=label):
                manifest, entries, _ = v2.validate_catalog_files(files)
                raw = files[f"{v2.CATALOG_PREFIX}/manifest.json"]
                digest = hashlib.sha256(raw).hexdigest()
                self.assertEqual(manifest["rules_version"], rules)
                self.assertTrue(all(row["rules_version"] == rules for row in entries))
                ledger.validate_authoritative_catalog(raw, expected_sha256=digest)
                ledger.replay_with_catalog([ledger_record(digest)], raw)

                ledger_path = self.root / f"{label}-ledger.jsonl"
                ledger_path.write_bytes(wp1.canonical_bytes(ledger_record(digest)) + b"\n")
                catalog_path = self.root / f"{label}-manifest.json"
                catalog_path.write_bytes(raw)
                with mock.patch.object(ledger, "ROOT", self.root):
                    self.assertEqual(ledger.main([
                        "check", ledger_path.name, "--catalog-manifest", catalog_path.name,
                        "--root", str(self.root),
                    ]), 0)

    def test_unknown_and_mixed_formal_rules_are_rejected(self):
        _, current = self.candidate()
        manifest_path = f"{v2.CATALOG_PREFIX}/manifest.json"
        unknown_manifest = wp1.parse_canonical_object(current[manifest_path], "manifest")
        unknown_manifest["rules_version"] = "production-review-v2-lite-rules-v3"
        unknown_manifest["catalog_id"] = v2.catalog_id(unknown_manifest)
        with self.assertRaisesRegex(ledger.LedgerError, "kind/rules mismatch"):
            ledger.validate_authoritative_catalog(wp1.canonical_bytes(unknown_manifest))

        mixed = dict(current)
        rows = wp1.parse_jsonl(mixed[f"{v2.CATALOG_PREFIX}/entries.jsonl"], "entries")
        rows[0]["rules_version"] = v2.FROZEN_RULES_VERSION
        mixed[f"{v2.CATALOG_PREFIX}/entries.jsonl"] = wp1._jsonl(rows)
        manifest = wp1.parse_canonical_object(mixed[manifest_path], "manifest")
        manifest["entries_sha256"] = hashlib.sha256(
            mixed[f"{v2.CATALOG_PREFIX}/entries.jsonl"]
        ).hexdigest()
        manifest["catalog_id"] = v2.catalog_id(manifest)
        mixed[manifest_path] = wp1.canonical_bytes(manifest)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "rules mismatch"):
            v2.validate_catalog_files(mixed)

    def test_formal_catalog_schema_versions_reject_json_true(self):
        _, original = self.candidate()
        for boundary in ("schema", "policy", "manifest", "entry", "exclusion"):
            with self.subTest(boundary=boundary):
                files = dict(original)
                if boundary == "schema":
                    value = dict(v2.SCHEMA_VALUE); value["schema_version"] = True
                    files[v2.SCHEMA_PATH] = wp1.canonical_bytes(value)
                elif boundary == "policy":
                    value = dict(v2.POLICY_VALUE); value["schema_version"] = True
                    files[v2.POLICY_PATH] = wp1.canonical_bytes(value)
                else:
                    manifest_path = f"{v2.CATALOG_PREFIX}/manifest.json"
                    manifest = wp1.parse_canonical_object(files[manifest_path], "manifest")
                    if boundary == "manifest":
                        manifest["schema_version"] = True
                    else:
                        name = "entries.jsonl" if boundary == "entry" else "exclusions.jsonl"
                        path = f"{v2.CATALOG_PREFIX}/{name}"
                        rows = wp1.parse_jsonl(files[path], boundary)
                        rows[0]["schema_version"] = True
                        files[path] = wp1._jsonl(rows)
                        manifest["entries_sha256" if boundary == "entry" else "exclusions_sha256"] = \
                            hashlib.sha256(files[path]).hexdigest()
                    manifest["catalog_id"] = v2.catalog_id(manifest)
                    files[manifest_path] = wp1.canonical_bytes(manifest)
                with self.assertRaises((wp1.ProductionReviewError, ledger.LedgerError)):
                    v2.validate_catalog_files(files)

    def _git_fixture(self):
        root = self.root / "git-fixture"
        root.mkdir()
        fixture = {"evidence/production-review/a": hashlib.sha256(b"a").hexdigest(),
                   "i18n/quality/production-review/b": hashlib.sha256(b"b").hexdigest()}
        for path, body in zip(fixture, (b"a", b"b")):
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "baseline"], cwd=root, check=True)
        baseline = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        return root, fixture, baseline

    def test_retirement_preimage_accepts_descendant_implementation_commit(self):
        root, fixture, baseline = self._git_fixture()
        (root / "implementation.py").write_text("candidate\n", encoding="utf-8")
        subprocess.run(["git", "add", "implementation.py"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "candidate implementation"], cwd=root, check=True)
        with mock.patch.dict(v2.WP1_FILES, fixture, clear=True), \
                mock.patch.object(v2, "BASELINE_HEAD", baseline):
            v2.verify_wp1_preimage(root)

    def test_retirement_preimage_rejects_committed_wp1_extra_but_allows_v2_lite(self):
        root, fixture, baseline = self._git_fixture()
        v2_path = root / "evidence/production-review-v2-lite/catalog/allowed.json"
        v2_path.parent.mkdir(parents=True)
        v2_path.write_bytes(b"v2")
        subprocess.run(["git", "add", str(v2_path.relative_to(root))], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "allowed v2-lite"], cwd=root, check=True)
        with mock.patch.dict(v2.WP1_FILES, fixture, clear=True), \
                mock.patch.object(v2, "BASELINE_HEAD", baseline):
            v2.verify_wp1_preimage(root)
            extra = root / "evidence/production-review/committed-extra.json"
            extra.write_bytes(b"extra")
            subprocess.run(["git", "add", str(extra.relative_to(root))], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "extra WP1 child"], cwd=root, check=True)
            with self.assertRaisesRegex(wp1.ProductionReviewError, "current HEAD.*extra"):
                v2.verify_wp1_preimage(root)

    def test_retirement_preimage_rejects_missing_changed_and_symlink(self):
        root, fixture, baseline = self._git_fixture()
        first = root / next(iter(fixture))
        second = root / list(fixture)[1]
        with mock.patch.dict(v2.WP1_FILES, fixture, clear=True), \
                mock.patch.object(v2, "BASELINE_HEAD", baseline):
            v2.verify_wp1_preimage(root)
            first.write_bytes(b"changed")
            with self.assertRaisesRegex(wp1.ProductionReviewError, "SHA-256"):
                v2.verify_wp1_preimage(root)
            first.write_bytes(b"a")
            second.unlink()
            with self.assertRaisesRegex(wp1.ProductionReviewError, "cannot read"):
                v2.verify_wp1_preimage(root)
            second.symlink_to(first)
            with self.assertRaisesRegex(wp1.ProductionReviewError, "symlink"):
                v2.verify_wp1_preimage(root)

    def test_retirement_rejects_staged_extra_and_committed_gitlink(self):
        root, fixture, baseline = self._git_fixture()
        candidate = {path: b"x" for path in v2.CANDIDATE_FILES}
        value = {"catalog_id": "c" * 64}
        extra = root / "evidence/production-review-v2-lite/staged.json"
        extra.parent.mkdir(parents=True)
        extra.write_bytes(b"staged")
        subprocess.run(["git", "add", str(extra.relative_to(root))], cwd=root, check=True)
        with mock.patch.dict(v2.WP1_FILES, fixture, clear=True), \
                mock.patch.object(v2, "BASELINE_HEAD", baseline), \
                mock.patch.object(v2, "check_catalog_tree", return_value=value), \
                mock.patch.object(v2, "ordinary_tree", return_value=candidate):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "staged|index|worktree"):
                v2.retirement_preflight(root, self.root / "candidate", self.manifest)
        subprocess.run(["git", "reset", "--hard", "-q"], cwd=root, check=True)
        subprocess.run(["git", "update-index", "--add", "--cacheinfo",
                        f"160000,{baseline},evidence/production-review-v2-lite/gitlink"],
                       cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "gitlink"], cwd=root, check=True)
        with mock.patch.dict(v2.WP1_FILES, fixture, clear=True), \
                mock.patch.object(v2, "BASELINE_HEAD", baseline), \
                mock.patch.object(v2, "check_catalog_tree", return_value=value), \
                mock.patch.object(v2, "ordinary_tree", return_value=candidate):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "ordinary 100644 blob"):
                v2.retirement_preflight(root, self.root / "candidate", self.manifest)

    def test_candidate_paths_reject_symlink_ancestors_for_read_and_write(self):
        real = self.root / "real"
        real.mkdir()
        link = self.root / "link"
        link.symlink_to(real, target_is_directory=True)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "symlink ancestor"):
            v2.ordinary_tree(link / "candidate")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "symlink ancestor"):
            v2.write_candidate({"file": b"x"}, link / "output", repository_root=ROOT)
        self.assertFalse((real / "output").exists())

    def test_prospective_budget_and_collision_are_exact(self):
        candidate = {path: b"x" for path in v2.CANDIDATE_FILES}
        self.assertEqual(v2.prospective_occupancy(dict.fromkeys(v2.WP1_FILES, 1), candidate), len(candidate))
        path = next(iter(candidate))
        for tracked in (path, path + "/child", path.rsplit("/", 1)[0]):
            with self.subTest(tracked=tracked), \
                    self.assertRaisesRegex(wp1.ProductionReviewError, "collides"):
                v2.prospective_occupancy({tracked: 1}, candidate)
        for tracked in (path + "-sibling", path.rsplit("/", 1)[0] + "-prefix/child"):
            with self.subTest(tracked=tracked):
                self.assertEqual(v2.prospective_occupancy({tracked: 1}, candidate), len(candidate) + 1)
        with mock.patch.object(v2, "TRACKED_LIMIT", 4):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "128 MiB"):
                v2.prospective_occupancy({}, candidate)

    def test_wp1_preimage_is_absent_after_publication(self):
        self.assertEqual(len(v2.WP1_RETIREMENT_ROOTS), 6)
        self.assertEqual(len(v2.WP1_FILES), 12)
        for path in v2.WP1_FILES:
            self.assertFalse((ROOT / path).exists(), path)
        with self.assertRaises(wp1.ProductionReviewError):
            v2.verify_wp1_preimage(ROOT)

    def test_real_cli_vector_preflight_and_controlled_failure(self):
        output = self.root / "real-candidate"
        built = subprocess.run([sys.executable, "-B", str(ROOT / "tools/i18n"), "production",
            "authoritative-catalog", "build", "--output", str(output), "--recorded-at", STAMP,
            "--recorded-by", "real-vector-test"], capture_output=True, text=True, timeout=300)
        self.assertEqual(built.returncode, 0, built.stderr)
        report = json.loads(built.stdout)
        self.assertEqual((report["occurrences"], report["entries"], report["exclusions"]), v2.CURRENT_VECTOR)
        preflight = subprocess.run([sys.executable, "-B", str(ROOT / "tools/i18n"), "production",
            "wp1-retirement", "preflight", "--candidate-catalog", str(output)],
            capture_output=True, text=True, timeout=300)
        self.assertNotEqual(preflight.returncode, 0)
        self.assertIn("WP1", preflight.stderr)
        self.assertTrue(all(not (ROOT / path).exists() for path in v2.WP1_FILES))
        manifest_path = output / v2.CATALOG_PREFIX / "manifest.json"
        manifest_path.write_bytes(b'{"kind":"production_review_v2_lite_catalog_v1","kind":"duplicate"}')
        failed = subprocess.run([sys.executable, "-B", str(ROOT / "tools/i18n"), "production",
            "authoritative-catalog", "check", "--candidate-catalog", str(output)],
            capture_output=True, text=True, timeout=60)
        self.assertNotEqual(failed.returncode, 0)
        self.assertNotIn("Traceback", failed.stdout + failed.stderr)


if __name__ == "__main__":
    unittest.main()
