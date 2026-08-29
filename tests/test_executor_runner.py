#!/usr/bin/env python3
import base64
import contextlib
import errno
import hashlib
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
import executor_runner as module
from executor_runner import (
    BoundedExecutor,
    ENVELOPE_VERSION,
    JOURNAL_VERSION,
    compute_hash,
    load_json_strict,
    write_atomic_json,
)


def image(content: bytes, mode: int = 0o644) -> dict:
    return {"state": "file", "sha256": hashlib.sha256(content).hexdigest(), "mode": mode}


def edit(content: bytes, mode: int = 0o644) -> dict:
    return {"state": "file", "content_base64": base64.b64encode(content).decode("ascii"), "mode": mode}


class TestBoundedExecutor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        subprocess.check_call(["git", "init", "-q"], cwd=self.repo)
        subprocess.check_call(["git", "config", "user.email", "test@example.com"], cwd=self.repo)
        subprocess.check_call(["git", "config", "user.name", "Test"], cwd=self.repo)
        (self.repo / "init.txt").write_text("init", encoding="utf-8")
        subprocess.check_call(["git", "add", "init.txt"], cwd=self.repo)
        subprocess.check_call(["git", "commit", "-qm", "init"], cwd=self.repo)
        self.head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo, text=True).strip()
        self.target = self.repo / "target.txt"
        self.target.write_bytes(b"original")
        self.target.chmod(0o640)
        self.runner = BoundedExecutor(self.repo)

    def tearDown(self):
        self.temp_dir.cleanup()

    def seal(self, envelope: dict) -> dict:
        candidate = envelope["candidate"]
        candidate["candidate_id"] = compute_hash({k: v for k, v in candidate.items() if k != "candidate_id"})
        envelope["envelope_hash"] = compute_hash({k: v for k, v in envelope.items() if k != "envelope_hash"})
        return envelope

    def envelope(self, paths=None, *, dispatch="d1", retry_of=None) -> dict:
        paths = paths or ["target.txt"]
        old = {"target.txt": b"original", "target2.txt": b"second"}
        new = {"target.txt": b"new", "target2.txt": b"new-second"}
        envelope = {
            "envelope_version": ENVELOPE_VERSION,
            "task_id": "task-1",
            "dispatch_id": dispatch,
            "workspace_id": "workspace-1",
            "parent_lineage": ["root", "executor"],
            "base_revision": self.head,
            "candidate": {
                "candidate_id": "0" * 64,
                "author": {"role": "EXECUTOR", "dispatch_id": "author-1"},
                "allowed_paths": list(paths),
                "edits": {path: edit(new[path], 0o600) for path in paths},
                "invariants": ["target-bounded"],
            },
            "preimages": {path: image(old[path], 0o640) for path in paths},
            "postimages": {path: image(new[path], 0o600) for path in paths},
            "gates": ["focused-unit"],
            "retry_of": retry_of,
            "envelope_hash": "0" * 64,
        }
        return self.seal(envelope)

    def context(self, receipts=None) -> dict:
        return {
            "task_id": "task-1",
            "workspace_id": "workspace-1",
            "parent_lineage": ["root", "executor"],
            "base_revision": self.head,
            "archive_receipts": [] if receipts is None else receipts,
        }

    def journal(self, envelope: dict, status: str, applied: list[str]) -> dict:
        return {
            "schema_version": JOURNAL_VERSION,
            "workspace_id": envelope["workspace_id"],
            "dispatch_id": envelope["dispatch_id"],
            "envelope_hash": envelope["envelope_hash"],
            "candidate_id": envelope["candidate"]["candidate_id"],
            "status": status,
            "ordered_paths": envelope["candidate"]["allowed_paths"],
            "applied_paths": applied,
            "preimages": envelope["preimages"],
            "postimages": envelope["postimages"],
        }

    def prepare(self, envelope: dict, status="PREPARED", applied=None) -> Path:
        decoded = self.runner._decoded_edits(envelope)
        self.runner._prepare_artifacts(envelope, decoded)
        ledger = self.runner._ledger_path(envelope["workspace_id"], envelope["dispatch_id"])
        write_atomic_json(ledger, self.journal(envelope, status, [] if applied is None else applied))
        return ledger

    def assert_target(self, path: Path, content: bytes, mode: int) -> None:
        self.assertEqual(path.read_bytes(), content)
        self.assertEqual(path.stat().st_mode & 0o777, mode)

    def retarget(self, envelope: dict, path: str, old: bytes, new: bytes, *, pre_mode=0o640, post_mode=0o600) -> dict:
        envelope["candidate"]["allowed_paths"] = [path]
        envelope["candidate"]["edits"] = {path: edit(new, post_mode)}
        envelope["preimages"] = {path: image(old, pre_mode)}
        envelope["postimages"] = {path: image(new, post_mode)}
        return self.seal(envelope)

    def absent_paths_envelope(self, paths: list[str], *, dispatch: str) -> dict:
        envelope = self.envelope(dispatch=dispatch)
        envelope["candidate"]["allowed_paths"] = list(paths)
        envelope["candidate"]["edits"] = {path: edit(f"new:{path}".encode(), 0o600) for path in paths}
        envelope["preimages"] = {path: {"state": "absent"} for path in paths}
        envelope["postimages"] = {path: image(f"new:{path}".encode(), 0o600) for path in paths}
        return self.seal(envelope)

    @contextlib.contextmanager
    def ordinary_permission_semantics(self):
        real_open = os.open

        def guarded_open(path, flags, *args, **kwargs):
            candidate = Path(path)
            if (
                flags & os.O_ACCMODE == os.O_RDONLY
                and candidate.is_file()
                and not candidate.stat().st_mode & stat.S_IRUSR
            ):
                raise PermissionError(f"ordinary owner cannot read {candidate}")
            return real_open(path, flags, *args, **kwargs)

        with mock.patch.object(module.os, "open", side_effect=guarded_open):
            yield

    def test_success_and_idempotent_commit_use_contract_artifact_root(self):
        envelope = self.envelope()
        self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        self.assert_target(self.target, b"new", 0o600)
        ledger = self.runner.get_ledger("workspace-1", "d1")
        self.assertEqual(ledger["status"], "COMMITTED")
        self.assertEqual(ledger["applied_paths"], ["target.txt"])
        self.assertIn(".artifacts/paseo-bounded", self.runner._ledger_path("workspace-1", "d1").as_posix())
        self.assertEqual(self.runner.apply(envelope, self.context()), "already_committed")
        self.assert_target(self.target, b"new", 0o600)

    def test_candidate_and_envelope_hashes_are_non_circular_and_distinct(self):
        first = self.envelope()
        second = self.envelope(dispatch="d2")
        self.assertEqual(first["candidate"]["candidate_id"], second["candidate"]["candidate_id"])
        self.assertNotEqual(first["envelope_hash"], second["envelope_hash"])
        self.assertRegex(first["candidate"]["candidate_id"], r"^[0-9a-f]{64}$")
        self.assertRegex(first["envelope_hash"], r"^[0-9a-f]{64}$")

    def test_candidate_and_envelope_hash_fields_require_lowercase_hex(self):
        for field in ("candidate_id", "envelope_hash"):
            with self.subTest(field=field):
                envelope = self.envelope(dispatch=f"hash-{field}")
                if field == "candidate_id":
                    envelope["candidate"][field] = "A" * 64
                else:
                    envelope[field] = "A" * 64
                with self.assertRaisesRegex(ValueError, "lowercase hex"):
                    self.runner.apply(envelope, self.context())
                self.assert_target(self.target, b"original", 0o640)

    def test_orchestrator_candidate_author_is_accepted(self):
        envelope = self.envelope()
        envelope["candidate"]["author"]["role"] = "ORCHESTRATOR"
        self.seal(envelope)
        self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        self.assert_target(self.target, b"new", 0o600)
        self.assertEqual(self.runner.get_ledger("workspace-1", "d1")["status"], "COMMITTED")

    def test_executor_candidate_author_remains_accepted(self):
        envelope = self.envelope()
        self.assertEqual(envelope["candidate"]["author"]["role"], "EXECUTOR")
        self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        self.assert_target(self.target, b"new", 0o600)
        self.assertEqual(self.runner.get_ledger("workspace-1", "d1")["status"], "COMMITTED")

    def test_invalid_candidate_author_roles_fail_before_target_or_ledger_write(self):
        for index, role in enumerate(("REVIEWER", "orchestrator", "executor", 7)):
            with self.subTest(role=role):
                dispatch = f"invalid-author-{index}"
                envelope = self.envelope(dispatch=dispatch)
                envelope["candidate"]["author"]["role"] = role
                self.seal(envelope)
                with self.assertRaisesRegex(ValueError, "candidate author role"):
                    self.runner.apply(envelope, self.context())
                self.assert_target(self.target, b"original", 0o640)
                self.assertIsNone(self.runner.get_ledger("workspace-1", dispatch))
                self.assertFalse(self.runner._transaction_root("workspace-1", dispatch).exists())

    def test_postimage_mismatch_fails_before_journal_or_target_write(self):
        envelope = self.envelope()
        envelope["postimages"]["target.txt"] = image(b"different", 0o600)
        self.seal(envelope)
        with self.assertRaisesRegex(ValueError, "edit bytes/mode"):
            self.runner.apply(envelope, self.context())
        self.assert_target(self.target, b"original", 0o640)
        self.assertFalse(self.runner._transaction_root("workspace-1", "d1").exists())

    def test_mode_bool_negative_and_overflow_are_rejected_without_writes(self):
        for location, bad_mode in (("edits", True), ("preimages", -1), ("postimages", 0o1000)):
            with self.subTest(location=location, bad_mode=bad_mode):
                envelope = self.envelope(dispatch=f"d-{location}")
                container = envelope["candidate"][location] if location == "edits" else envelope[location]
                container["target.txt"]["mode"] = bad_mode
                self.seal(envelope)
                with self.assertRaisesRegex(ValueError, "0..0o777"):
                    self.runner.apply(envelope, self.context())
                self.assert_target(self.target, b"original", 0o640)
                self.assertIsNone(self.runner.get_ledger("workspace-1", f"d-{location}"))

    def test_privileged_target_namespaces_fail_before_any_transaction_write(self):
        for index, path in enumerate((".git/config", ".ai/task/x", ".artifacts/output.bin")):
            with self.subTest(path=path):
                dispatch = f"privileged-{index}"
                envelope = self.retarget(self.envelope(dispatch=dispatch), path, b"old", b"new")
                with self.assertRaisesRegex(ValueError, "privileged target namespace"):
                    self.runner.apply(envelope, self.context())
                self.assertFalse(self.runner._transaction_root("workspace-1", dispatch).exists())
                self.assert_target(self.target, b"original", 0o640)

    def test_ordinary_dot_prefixed_target_is_allowed(self):
        dotfile = self.repo / ".gitignore"
        dotfile.write_bytes(b"old\n")
        dotfile.chmod(0o640)
        envelope = self.retarget(self.envelope(), ".gitignore", b"old\n", b"new\n")
        self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        self.assert_target(dotfile, b"new\n", 0o600)

    def test_noncanonical_posix_paths_fail_before_any_write(self):
        for index, path in enumerate(("./target.txt", "target.txt/", "a//b", "a/./b", "a/../b")):
            with self.subTest(path=path):
                dispatch = f"noncanonical-{index}"
                envelope = self.retarget(self.envelope(dispatch=dispatch), path, b"original", b"new")
                with self.assertRaisesRegex(ValueError, "path components|canonical POSIX"):
                    self.runner.apply(envelope, self.context())
                self.assertFalse(self.runner._transaction_root("workspace-1", dispatch).exists())
                self.assert_target(self.target, b"original", 0o640)

    def test_path_alias_pair_fails_before_any_write(self):
        envelope = self.envelope(dispatch="path-alias-pair")
        aliases = ["target.txt", "target.txt/"]
        envelope["candidate"]["allowed_paths"] = aliases
        envelope["candidate"]["edits"] = {path: edit(b"new", 0o600) for path in aliases}
        envelope["preimages"] = {path: image(b"original", 0o640) for path in aliases}
        envelope["postimages"] = {path: image(b"new", 0o600) for path in aliases}
        self.seal(envelope)
        with self.assertRaisesRegex(ValueError, "path components"):
            self.runner.apply(envelope, self.context())
        self.assertFalse(self.runner._transaction_root("workspace-1", "path-alias-pair").exists())
        self.assert_target(self.target, b"original", 0o640)

    def test_ancestor_descendant_paths_fail_in_both_orders_before_any_write(self):
        for index, paths in enumerate((["newdir", "newdir/child.txt"], ["newdir/child.txt", "newdir"])):
            with self.subTest(paths=paths):
                dispatch = f"overlap-{index}"
                envelope = self.absent_paths_envelope(paths, dispatch=dispatch)
                with self.assertRaisesRegex(ValueError, "ancestor and descendant"):
                    self.runner.apply(envelope, self.context())
                self.assertFalse(self.runner._transaction_root("workspace-1", dispatch).exists())
                self.assertFalse((self.repo / "newdir").exists())
                self.assert_target(self.target, b"original", 0o640)

                journal = self.journal(envelope, "PREPARED", [])
                with self.assertRaisesRegex(ValueError, "ancestor and descendant"):
                    self.runner._validate_journal(journal)
                self.assertFalse(self.runner._transaction_root("workspace-1", dispatch).exists())
                self.assertFalse((self.repo / "newdir").exists())

    def test_sibling_paths_are_allowed(self):
        paths = ["a/x", "a/y"]
        envelope = self.absent_paths_envelope(paths, dispatch="siblings")
        self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        for path in paths:
            self.assert_target(self.repo / path, f"new:{path}".encode(), 0o600)
        self.assertEqual(self.runner.get_ledger("workspace-1", "siblings")["applied_paths"], paths)

    def test_recovery_journal_rejects_noncanonical_ordered_paths_without_write(self):
        for index, path in enumerate(("./target.txt", "target.txt/", "a//b", "a/./b", "a/../b")):
            with self.subTest(path=path):
                envelope = self.envelope(dispatch=f"journal-path-{index}")
                journal = self.journal(envelope, "PREPARED", [])
                journal["ordered_paths"] = [path]
                journal["preimages"] = {path: {"state": "absent"}}
                journal["postimages"] = {path: image(b"new", 0o600)}
                with self.assertRaisesRegex(ValueError, "path components|canonical POSIX"):
                    self.runner._validate_journal(journal)
                self.assertFalse(self.runner._transaction_root("workspace-1", envelope["dispatch_id"]).exists())
                self.assert_target(self.target, b"original", 0o640)

    def test_recovery_journal_rejects_privileged_ordered_paths(self):
        for index, path in enumerate((".git/config", ".ai/task/x", ".artifacts/output.bin")):
            with self.subTest(path=path):
                envelope = self.envelope(dispatch=f"journal-privileged-{index}")
                journal = self.journal(envelope, "PREPARED", [])
                journal["ordered_paths"] = [path]
                journal["preimages"] = {path: {"state": "absent"}}
                journal["postimages"] = {path: image(b"new", 0o600)}
                with self.assertRaisesRegex(ValueError, "privileged target namespace"):
                    self.runner._validate_journal(journal)
                self.assertFalse(self.runner._transaction_root("workspace-1", envelope["dispatch_id"]).exists())

    def test_ascii_identifiers_are_enforced_by_apply_and_artifact_helpers(self):
        envelope = self.envelope()
        envelope["workspace_id"] = "工作区"
        self.seal(envelope)
        with self.assertRaisesRegex(ValueError, "ASCII identifier"):
            self.runner.apply(envelope, self.context())
        for call in (
            lambda: self.runner.get_ledger("工作区", "d1"),
            lambda: self.runner._ledger_path("workspace-1", "派发"),
            lambda: self.runner._shadow_path("../escape", "d1"),
        ):
            with self.assertRaisesRegex(ValueError, "ASCII identifier"):
                call()
        self.assert_target(self.target, b"original", 0o640)

    def test_exact_envelope_candidate_and_list_schemas(self):
        mutations = {
            "version": lambda e: e.__setitem__("envelope_version", "1.0"),
            "author role": lambda e: e["candidate"]["author"].__setitem__("role", 7),
            "author dispatch": lambda e: e["candidate"]["author"].__setitem__("dispatch_id", "作者"),
            "allowed string": lambda e: e["candidate"].__setitem__("allowed_paths", [7]),
            "invariants": lambda e: e["candidate"].__setitem__("invariants", "not-list"),
            "gates": lambda e: e.__setitem__("gates", [7]),
            "extra": lambda e: e.__setitem__("extra", True),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                envelope = self.envelope(dispatch=f"d-{name.replace(' ', '-')}")
                mutate(envelope)
                # Some malformed bodies cannot be canonical-resealed only if keys are non-string; none here.
                self.seal(envelope)
                with self.assertRaises(ValueError):
                    self.runner.apply(envelope, self.context())
                self.assert_target(self.target, b"original", 0o640)

    def test_archive_receipts_are_exact_typed_trusted_host_facts(self):
        envelope = self.envelope(retry_of="old-dispatch")
        candidate_id = envelope["candidate"]["candidate_id"]
        valid = {"task_id": "task-1", "workspace_id": "workspace-1", "dispatch_id": "old-dispatch", "candidate_id": candidate_id, "archive_confirmed": True}
        for receipts in ("not-list", [dict(valid, archive_confirmed=1)], [dict(valid, candidate_id="A" * 64)], [dict(valid, extra=True)]):
            with self.subTest(receipts=receipts):
                with self.assertRaises(ValueError):
                    self.runner.apply(envelope, self.context(receipts))
                self.assert_target(self.target, b"original", 0o640)
                self.assertIsNone(self.runner.get_ledger("workspace-1", "d1"))
        self.assertEqual(self.runner.apply(envelope, self.context([valid])), "COMMITTED")
        self.assertEqual(self.runner.get_ledger("workspace-1", "d1")["status"], "COMMITTED")

    def test_duplicate_keys_rejected_by_cli_loader_and_journal_reader(self):
        duplicate = self.repo / "duplicate.json"
        duplicate.write_text('{"task_id":"a","task_id":"b"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            load_json_strict(duplicate)
        context_file = self.repo / "context.json"
        context_file.write_text(json.dumps(self.context()), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main(["executor_runner.py", str(duplicate), str(context_file)]), 1)
        self.assert_target(self.target, b"original", 0o640)

        envelope = self.envelope()
        ledger = self.prepare(envelope)
        raw = ledger.read_text(encoding="utf-8")
        ledger.write_text(raw[:-1] + ',"status":"COMMITTED"}', encoding="utf-8")
        before = self.target.read_bytes(), self.target.stat().st_mode & 0o777
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            self.runner.apply(envelope, self.context())
        self.assertEqual((self.target.read_bytes(), self.target.stat().st_mode & 0o777), before)

    def test_non_finite_json_and_non_string_journal_status_fail_closed(self):
        non_finite = self.repo / "nan.json"
        non_finite.write_text('{"value":NaN}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "non-finite"):
            load_json_strict(non_finite)
        envelope = self.envelope()
        ledger = self.prepare(envelope)
        journal = json.loads(ledger.read_text(encoding="utf-8"))
        journal["status"] = ["PREPARED"]
        ledger.write_text(json.dumps(journal), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "journal status"):
            self.runner.apply(envelope, self.context())
        self.assert_target(self.target, b"original", 0o640)

    def test_tampered_journal_schema_and_envelope_bindings_fail_closed(self):
        changes = {
            "extra": lambda j: j.__setitem__("extra", 1),
            "workspace": lambda j: j.__setitem__("workspace_id", "other"),
            "dispatch": lambda j: j.__setitem__("dispatch_id", "other"),
            "envelope": lambda j: j.__setitem__("envelope_hash", "2" * 64),
            "candidate": lambda j: j.__setitem__("candidate_id", "1" * 64),
            "ordered": lambda j: j.__setitem__("ordered_paths", ["other.txt"]),
            "preimages": lambda j: j.__setitem__("preimages", {"target.txt": {"state": "absent"}}),
            "postimages": lambda j: j.__setitem__("postimages", {"target.txt": {"state": "absent"}}),
            "applied type": lambda j: j.__setitem__("applied_paths", "target.txt"),
        }
        for name, mutate in changes.items():
            with self.subTest(name=name):
                envelope = self.envelope(dispatch=f"journal-{name.replace(' ', '-')}")
                ledger = self.prepare(envelope)
                journal = json.loads(ledger.read_text(encoding="utf-8"))
                mutate(journal)
                ledger.write_text(json.dumps(journal), encoding="utf-8")
                raw = ledger.read_bytes()
                with self.assertRaises(ValueError):
                    self.runner.apply(envelope, self.context())
                self.assertEqual(ledger.read_bytes(), raw)
                self.assert_target(self.target, b"original", 0o640)

    def test_tampered_post_shadow_fails_before_target_write(self):
        envelope = self.envelope()
        ledger = self.prepare(envelope)
        shadow = self.runner._artifact_path("workspace-1", "d1", "post", "target.txt")
        shadow.write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "post shadow"):
            self.runner.apply(envelope, self.context())
        self.assert_target(self.target, b"original", 0o640)
        self.assertEqual(load_json_strict(ledger)["status"], "PREPARED")

    def test_tampered_preimage_snapshot_fails_before_apply_or_rollback(self):
        envelope = self.envelope()
        ledger = self.prepare(envelope, "ROLLING_BACK", ["target.txt"])
        snapshot = self.runner._artifact_path("workspace-1", "d1", "pre", "target.txt")
        snapshot.chmod(0o777)
        self.target.write_bytes(b"new")
        self.target.chmod(0o600)
        with self.assertRaisesRegex(ValueError, "preimage snapshot"):
            self.runner.apply(envelope, self.context())
        self.assert_target(self.target, b"new", 0o600)
        self.assertEqual(load_json_strict(ledger)["status"], "ROLLING_BACK")

    def test_prepositioned_predictable_temp_symlinks_cannot_escape(self):
        outside = self.repo / "outside.txt"
        outside.write_bytes(b"outside")
        old_target_temp = self.repo / f"target.txt.tmp.{os.getpid()}"
        old_target_temp.symlink_to(outside)
        envelope = self.envelope()
        self.prepare(envelope)
        transaction = self.runner._transaction_root("workspace-1", "d1")
        old_journal_temp = transaction / f"journal.json.tmp.{os.getpid()}.0"
        old_journal_temp.symlink_to(outside)
        self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        self.assertEqual(outside.read_bytes(), b"outside")
        self.assertTrue(old_target_temp.is_symlink())
        self.assertTrue(old_journal_temp.is_symlink())
        self.assert_target(self.target, b"new", 0o600)
        self.assertEqual(self.runner.get_ledger("workspace-1", "d1")["status"], "COMMITTED")

    def test_symlinked_artifact_root_is_rejected_without_external_write(self):
        outside_dir = Path(self.temp_dir.name).parent / f"outside-{os.getpid()}"
        outside_dir.mkdir(exist_ok=True)
        try:
            (self.repo / ".artifacts").symlink_to(outside_dir)
            with self.assertRaisesRegex(ValueError, "symlink"):
                self.runner.apply(self.envelope(), self.context())
            self.assertEqual(list(outside_dir.iterdir()), [])
            self.assert_target(self.target, b"original", 0o640)
        finally:
            (self.repo / ".artifacts").unlink(missing_ok=True)
            outside_dir.rmdir()

    def test_target_and_journal_replace_fsync_parent_directories(self):
        seen = []
        real = module._fsync_directory

        def record(directory):
            seen.append(Path(directory).resolve())
            return real(directory)

        with mock.patch.object(module, "_fsync_directory", side_effect=record):
            self.assertEqual(self.runner.apply(self.envelope(), self.context()), "COMMITTED")
        ledger_parent = self.runner._ledger_path("workspace-1", "d1").parent.resolve()
        self.assertIn(self.repo.resolve(), seen)
        self.assertIn(ledger_parent, seen)
        self.assert_target(self.target, b"new", 0o600)
        self.assertEqual(self.runner.get_ledger("workspace-1", "d1")["status"], "COMMITTED")

    def test_journal_less_partial_artifacts_are_verified_completed_and_applied(self):
        envelope, target2 = self.two_target_envelope()
        failing_artifact = self.runner._artifact_path("workspace-1", "d1", "pre", "target2.txt")
        real = module._atomic_replace_bytes

        def fail_partway(path, content, mode):
            if Path(path) == failing_artifact:
                raise OSError("injected preparation crash")
            return real(path, content, mode)

        with mock.patch.object(module, "_atomic_replace_bytes", side_effect=fail_partway):
            with self.assertRaisesRegex(OSError, "preparation crash"):
                self.runner.apply(envelope, self.context())
        self.assert_target(self.target, b"original", 0o640)
        self.assert_target(target2, b"second", 0o640)
        self.assertFalse(self.runner._ledger_path("workspace-1", "d1").exists())

        self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        self.assert_target(self.target, b"new", 0o600)
        self.assert_target(target2, b"new-second", 0o600)

    def test_journal_less_complete_artifacts_resume_after_prepared_write_crash(self):
        envelope = self.envelope()
        with mock.patch.object(module, "write_atomic_json", side_effect=OSError("injected journal crash")):
            with self.assertRaisesRegex(OSError, "journal crash"):
                self.runner.apply(envelope, self.context())
        self.assertFalse(self.runner._ledger_path("workspace-1", "d1").exists())
        self.runner._verify_artifacts(envelope)
        self.assert_target(self.target, b"original", 0o640)

        self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        self.assert_target(self.target, b"new", 0o600)

    def test_journal_less_tampered_or_unknown_artifacts_fail_without_target_write(self):
        mutations = {
            "hash": lambda e: self.runner._artifact_path("workspace-1", e["dispatch_id"], "post", "target.txt").write_bytes(b"tampered"),
            "mode": lambda e: self.runner._artifact_path("workspace-1", e["dispatch_id"], "post", "target.txt").chmod(0o777),
            "unknown": lambda e: (self.runner._transaction_root("workspace-1", e["dispatch_id"]) / "unknown.bin").write_bytes(b"unknown"),
            "symlink": lambda e: (self.runner._transaction_root("workspace-1", e["dispatch_id"]) / "unknown-link").symlink_to(self.target),
        }
        for index, (name, mutate) in enumerate(mutations.items()):
            with self.subTest(name=name):
                dispatch = f"tampered-{index}"
                envelope = self.envelope(dispatch=dispatch)
                with mock.patch.object(module, "write_atomic_json", side_effect=OSError("injected journal crash")):
                    with self.assertRaises(OSError):
                        self.runner.apply(envelope, self.context())
                mutate(envelope)
                with self.assertRaises(ValueError):
                    self.runner.apply(envelope, self.context())
                self.assert_target(self.target, b"original", 0o640)
                self.assertFalse(self.runner._ledger_path("workspace-1", dispatch).exists())

    def test_journal_less_target_drift_fails_without_artifact_or_target_rewrite(self):
        envelope = self.envelope()
        with mock.patch.object(module, "write_atomic_json", side_effect=OSError("injected journal crash")):
            with self.assertRaises(OSError):
                self.runner.apply(envelope, self.context())
        artifact = self.runner._artifact_path("workspace-1", "d1", "post", "target.txt")
        before_artifact = artifact.read_bytes(), artifact.stat().st_mode & 0o777
        self.target.write_bytes(b"drift")
        self.target.chmod(0o644)

        with self.assertRaisesRegex(ValueError, "target preimage mismatch"):
            self.runner.apply(envelope, self.context())
        self.assert_target(self.target, b"drift", 0o644)
        self.assertEqual((artifact.read_bytes(), artifact.stat().st_mode & 0o777), before_artifact)
        self.assertFalse(self.runner._ledger_path("workspace-1", "d1").exists())

    def test_owner_unreadable_new_and_existing_files_apply_and_verify_without_root_bypass(self):
        new_path = self.repo / "new-unreadable.txt"
        new_envelope = self.retarget(self.envelope(dispatch="new-unreadable"), "new-unreadable.txt", b"", b"created", post_mode=0o000)
        new_envelope["preimages"]["new-unreadable.txt"] = {"state": "absent"}
        self.seal(new_envelope)
        with self.ordinary_permission_semantics():
            self.assertEqual(self.runner.apply(new_envelope, self.context()), "COMMITTED")
            self.assertEqual(self.runner.apply(new_envelope, self.context()), "already_committed")
        self.assertEqual(module._read_bytes_preserving_mode(new_path), b"created")
        self.assertEqual(new_path.stat().st_mode & 0o777, 0o000)

        self.target.chmod(0o200)
        existing = self.envelope(dispatch="existing-unreadable")
        existing["preimages"]["target.txt"]["mode"] = 0o200
        existing["candidate"]["edits"]["target.txt"]["mode"] = 0o000
        existing["postimages"]["target.txt"]["mode"] = 0o000
        self.seal(existing)
        with self.ordinary_permission_semantics():
            self.assertEqual(self.runner.apply(existing, self.context()), "COMMITTED")
            self.assertEqual(self.runner.apply(existing, self.context()), "already_committed")
        self.assertEqual(module._read_bytes_preserving_mode(self.target), b"new")
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o000)

    def test_read_failure_is_not_masked_by_double_close(self):
        real_fdopen = os.fdopen

        class FailingReadStream:
            def __init__(self, stream):
                self.stream = stream

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                self.stream.close()

            def read(self):
                raise OSError(errno.EIO, "injected read failure")

        def failing_fdopen(fd, *args, **kwargs):
            return FailingReadStream(real_fdopen(fd, *args, **kwargs))

        self.target.chmod(0o200)
        original_mode = self.target.stat().st_mode & 0o777
        with mock.patch.object(module.os, "fdopen", side_effect=failing_fdopen):
            with self.assertRaisesRegex(OSError, "injected read failure") as caught:
                module._read_bytes_preserving_mode(self.target)
        self.assertEqual(caught.exception.errno, errno.EIO)
        self.assertEqual(self.target.stat().st_mode & 0o777, original_mode)

    def test_owner_unreadable_apply_failure_rolls_back_exact_bytes_and_modes(self):
        envelope, target2 = self.two_target_envelope()
        self.target.chmod(0o200)
        envelope["preimages"]["target.txt"]["mode"] = 0o200
        envelope["candidate"]["edits"]["target.txt"]["mode"] = 0o000
        envelope["postimages"]["target.txt"]["mode"] = 0o000
        self.seal(envelope)
        real = module._atomic_replace_bytes

        def fail_second(path, content, mode):
            if Path(path) == target2 and content == b"new-second":
                raise OSError("injected replace failure")
            return real(path, content, mode)

        with self.ordinary_permission_semantics(), mock.patch.object(module, "_atomic_replace_bytes", side_effect=fail_second):
            with self.assertRaisesRegex(RuntimeError, "rolled back"):
                self.runner.apply(envelope, self.context())
        self.assertEqual(module._read_bytes_preserving_mode(self.target), b"original")
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o200)
        self.assert_target(target2, b"second", 0o640)
        self.assertEqual(self.runner.get_ledger("workspace-1", "d1")["status"], "ROLLED_BACK")

    def two_target_envelope(self) -> tuple[dict, Path]:
        target2 = self.repo / "target2.txt"
        target2.write_bytes(b"second")
        target2.chmod(0o640)
        return self.envelope(["target.txt", "target2.txt"]), target2

    def test_second_replace_failure_rolls_back_bytes_modes_and_journal(self):
        envelope, target2 = self.two_target_envelope()
        real = module._atomic_replace_bytes

        def fail_second(path, content, mode):
            if Path(path) == target2 and content == b"new-second":
                raise OSError("injected replace failure")
            return real(path, content, mode)

        with mock.patch.object(module, "_atomic_replace_bytes", side_effect=fail_second):
            with self.assertRaisesRegex(RuntimeError, "rolled back") as caught:
                self.runner.apply(envelope, self.context())
        self.assertIsInstance(caught.exception.__cause__, OSError)
        self.assert_target(self.target, b"original", 0o640)
        self.assert_target(target2, b"second", 0o640)
        ledger = self.runner.get_ledger("workspace-1", "d1")
        self.assertEqual(ledger["status"], "ROLLED_BACK")
        self.assertEqual(ledger["applied_paths"], [])

    def test_applying_crash_reconciles_actual_post_missing_from_applied(self):
        envelope, target2 = self.two_target_envelope()
        ledger = self.prepare(envelope, "APPLYING", [])
        self.target.write_bytes(b"new")
        self.target.chmod(0o600)
        self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        self.assert_target(self.target, b"new", 0o600)
        self.assert_target(target2, b"new-second", 0o600)
        journal = load_json_strict(ledger)
        self.assertEqual(journal["status"], "COMMITTED")
        self.assertEqual(journal["applied_paths"], ["target.txt", "target2.txt"])

    def test_non_first_postimage_recovery_keeps_every_journal_ordered_and_idempotent(self):
        envelope, target2 = self.two_target_envelope()
        ledger = self.prepare(envelope, "APPLYING", [])
        target2.write_bytes(b"new-second")
        target2.chmod(0o600)
        writes = []
        real_write = module.write_atomic_json

        def record_write(path, data):
            writes.append(json.loads(json.dumps(data)))
            return real_write(path, data)

        with mock.patch.object(module, "write_atomic_json", side_effect=record_write):
            self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")

        self.assert_target(self.target, b"new", 0o600)
        self.assert_target(target2, b"new-second", 0o600)
        applying = [journal for journal in writes if journal["status"] == "APPLYING"]
        self.assertTrue(applying)
        for journal in applying:
            self.runner._validate_journal(journal, envelope)
            self.assertEqual(
                journal["applied_paths"],
                [path for path in journal["ordered_paths"] if path in journal["applied_paths"]],
            )
        journal = load_json_strict(ledger)
        self.assertEqual(journal["status"], "COMMITTED")
        self.assertEqual(journal["applied_paths"], ["target.txt", "target2.txt"])
        self.assertEqual(self.runner.apply(envelope, self.context()), "already_committed")

        make_journal = self.runner._journal_factory(envelope)
        with self.assertRaisesRegex(ValueError, "duplicates"):
            make_journal("APPLYING", ["target.txt", "target.txt"])
        with self.assertRaisesRegex(ValueError, "unknown"):
            make_journal("APPLYING", ["unknown.txt"])

    def test_rolling_back_crash_removes_actual_pre_still_in_applied(self):
        envelope, target2 = self.two_target_envelope()
        ledger = self.prepare(envelope, "ROLLING_BACK", ["target.txt", "target2.txt"])
        target2.write_bytes(b"new-second")
        target2.chmod(0o600)
        self.assertEqual(self.runner.apply(envelope, self.context()), "ROLLED_BACK")
        self.assert_target(self.target, b"original", 0o640)
        self.assert_target(target2, b"second", 0o640)
        journal = load_json_strict(ledger)
        self.assertEqual(journal["status"], "ROLLED_BACK")
        self.assertEqual(journal["applied_paths"], [])

    def test_recovery_third_state_records_conflict_without_overwrite(self):
        envelope = self.envelope()
        ledger = self.prepare(envelope, "APPLYING", [])
        self.target.write_bytes(b"user-change")
        self.target.chmod(0o644)
        with self.assertRaisesRegex(RuntimeError, "neither"):
            self.runner.apply(envelope, self.context())
        self.assert_target(self.target, b"user-change", 0o644)
        journal = load_json_strict(ledger)
        self.assertEqual(journal["status"], "ROLLBACK_CONFLICT")
        self.assertEqual(journal["applied_paths"], [])

    def test_delete_apply_and_parent_fsync(self):
        envelope = self.envelope()
        envelope["candidate"]["edits"]["target.txt"] = {"state": "absent"}
        envelope["postimages"]["target.txt"] = {"state": "absent"}
        self.seal(envelope)
        seen = []
        real = module._fsync_directory
        with mock.patch.object(module, "_fsync_directory", side_effect=lambda p: (seen.append(Path(p).resolve()), real(p))[1]):
            self.assertEqual(self.runner.apply(envelope, self.context()), "COMMITTED")
        self.assertFalse(self.target.exists())
        self.assertIn(self.repo.resolve(), seen)
        self.assertEqual(self.runner.get_ledger("workspace-1", "d1")["status"], "COMMITTED")


if __name__ == "__main__":
    unittest.main()
