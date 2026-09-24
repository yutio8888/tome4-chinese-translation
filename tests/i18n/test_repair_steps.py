from __future__ import annotations

import fcntl
import io
import os
import shutil
import sqlite3
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from tests.i18n import test_production_review_v2_lite_migration as migration_fixture
from tools.i18nlib import cli as tools_cli
from tools.i18nlib import cli_production
from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as catalog
from tools.i18nlib import production_review_v2_lite_migration as migration
from tools.i18nlib import production_review_v2_lite_queue as queue
from tools.orchestration import run_repair_steps as steps


STAMP = "2026-09-21T01:02:03Z"


class _CapturedStdout(io.StringIO):
    def __init__(self):
        super().__init__()
        self.buffer = io.BytesIO()

    def combined(self) -> str:
        return self.getvalue() + self.buffer.getvalue().decode("utf-8")


class RepairStepTests(migration_fixture.MigrationFixture):
    _publish_surface_batch = migration_fixture.MigrationTests._publish_surface_batch

    def _run(self, *argv):
        stdout, stderr = _CapturedStdout(), io.StringIO()
        with mock.patch.dict(os.environ, {"I18N_REPOSITORY_ROOT": str(self.root)}), \
                redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                code = steps.main(list(argv))
            except SystemExit as error:
                code = error.code if isinstance(error.code, int) else 1
                if not isinstance(error.code, int):
                    stderr.write(str(error.code))
        return code, stdout.combined(), stderr.getvalue()

    def _timing(self, path: Path) -> dict:
        return wp1.parse_canonical_object(path.read_bytes(), "repair timing")

    def _publish_two_repairs(self):
        self._publish_surface_batch(repair=True, entry_index=0, batch_name="repair-a")
        self._publish_surface_batch(repair=True, entry_index=1, batch_name="repair-b")

    def _runtime_snapshot(self):
        runtime = self.root / queue.RUNTIME_RELATIVE
        return {
            path.relative_to(runtime).as_posix(): path.read_bytes()
            for path in runtime.rglob("*") if path.is_file()
        }

    def test_preflight_rejects_every_mutable_state_output_before_cli(self):
        runtime = self.root / queue.RUNTIME_RELATIVE
        safe_timing = self.root / ".artifacts" / "safe-preflight-timing.json"
        targets = [
            queue.checkpoint_path(self.root),
            queue.database_path(self.root),
            runtime / (queue.DATABASE_NAME + "-wal"),
            queue.repository_lock_path(self.root),
        ]
        before = self._runtime_snapshot()
        for option in ("output", "timing-output"):
            for index, target in enumerate(targets):
                safe_output = safe_timing.with_name(f"safe-workset-{option}-{index}.json")
                safe_report = safe_timing.with_name(f"safe-timing-{option}-{index}.json")
                argv = [
                    "preflight", "--batch-id", "repair-a",
                    "--output", str(target if option == "output" else safe_output),
                    "--timing-output", str(target if option == "timing-output" else safe_report),
                ]
                with self.subTest(option=option, target=target.name), \
                        mock.patch.object(steps, "cli_main") as cli:
                    code, _stdout, stderr = self._run(*argv)
                    self.assertNotEqual(code, 0)
                    self.assertIn("production mutable state directory", stderr)
                    cli.assert_not_called()
                    self.assertEqual(self._runtime_snapshot(), before)

    def test_migration_chain_rejects_mutable_state_output_before_cli(self):
        candidate = self.candidate([
            self.replace(self.entries[0], target="state boundary target"), *self.entries[1:]])
        runtime = self.root / queue.RUNTIME_RELATIVE
        timing = runtime / "timing-sidecar.json"
        migration_output = self.root / ".artifacts" / "safe-migration.json"
        before = self._runtime_snapshot()
        with mock.patch.object(steps, "cli_main") as cli:
            code, _stdout, stderr = self._run(
                "migration-chain", "--candidate-catalog", str(candidate),
                "--migration-output", str(migration_output),
                "--timing-output", str(timing))
        self.assertNotEqual(code, 0)
        self.assertIn("production mutable state directory", stderr)
        cli.assert_not_called()
        self.assertFalse(migration_output.exists())
        self.assertEqual(self._runtime_snapshot(), before)

    def test_timing_write_failure_preserves_business_nonzero(self):
        planned = [("preflight:repair-a", ["synthetic"])]
        with mock.patch.object(steps, "_precheck", return_value=planned), \
                mock.patch.object(steps, "cli_main", return_value=7), \
                mock.patch.object(steps, "_write_timing", side_effect=RuntimeError("timing full")):
            code, _stdout, stderr = self._run(
                "preflight", "--batch-id", "repair-a", "--output", "unused.json",
                "--timing-output", "unused-timing.json")
        self.assertEqual(code, 7)
        self.assertIn("business steps completed: preflight:repair-a(exit=7)", stderr)
        self.assertIn("do not blindly rerun", stderr)

    def test_timing_write_failure_preserves_business_exception(self):
        planned = [("migration:apply", ["synthetic"])]
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, {"I18N_REPOSITORY_ROOT": str(self.root)}), \
                mock.patch.object(steps, "_precheck", return_value=planned), \
                mock.patch.object(steps, "cli_main", side_effect=LookupError("business exploded")), \
                mock.patch.object(steps, "_write_timing", side_effect=RuntimeError("timing full")), \
                redirect_stdout(_CapturedStdout()), redirect_stderr(stderr):
            with self.assertRaisesRegex(LookupError, "business exploded"):
                steps.main([
                    "migration-chain", "--candidate-catalog", "unused-candidate",
                    "--migration-output", "unused.json",
                    "--timing-output", "unused-timing.json",
                ])
        self.assertIn("business steps completed: migration:apply(exit=1)", stderr.getvalue())
        self.assertIn("do not blindly rerun", stderr.getvalue())

    def test_timing_write_failure_after_success_uses_dedicated_exit(self):
        planned = [("migration:apply", ["synthetic"])]
        with mock.patch.object(steps, "_precheck", return_value=planned), \
                mock.patch.object(steps, "cli_main", return_value=0), \
                mock.patch.object(steps, "_write_timing", side_effect=RuntimeError("timing full")):
            code, _stdout, stderr = self._run(
                "migration-chain", "--candidate-catalog", "unused-candidate",
                "--migration-output", "unused.json",
                "--timing-output", "unused-timing.json")
        self.assertEqual(code, steps.TIMING_WRITE_EXIT)
        self.assertIn("business steps completed: migration:apply(exit=0)", stderr)
        self.assertIn("may already exist", stderr)
        self.assertIn("do not blindly rerun", stderr)

    def test_two_preflights_match_standalone_bytes_and_replay_once(self):
        self._publish_two_repairs()
        direct = [self.root / ".artifacts" / f"direct-{name}.json"
                  for name in ("a", "b")]
        wrapped = [self.root / ".artifacts" / f"wrapped-{name}.json"
                   for name in ("a", "b")]
        timing = self.root / ".artifacts" / "preflight-timing.json"
        original = queue._projection
        direct_calls = []

        def counted(*args, **kwargs):
            direct_calls.append(1)
            return original(*args, **kwargs)

        with mock.patch.object(queue, "_projection", side_effect=counted), \
                mock.patch.object(migration, "_validate_live_repair_preimage"), \
                mock.patch.object(catalog, "utc_now", return_value=STAMP):
            migration.repair_preflight(self.root, "repair-a", output=direct[0])
            migration.repair_preflight(self.root, "repair-b", output=direct[1])
        self.assertEqual(len(direct_calls), 2)

        with mock.patch.object(migration, "_validate_live_repair_preimage"), \
                mock.patch.object(cli_production, "_manifest", return_value=None), \
                mock.patch.object(catalog, "utc_now", return_value=STAMP):
            code, _stdout, stderr = self._run(
                "preflight", "--batch-id", "repair-a", "--output", str(wrapped[0]),
                "--batch-id", "repair-b", "--output", str(wrapped[1]),
                "--timing-output", str(timing))
        self.assertEqual(code, 0, stderr)
        self.assertEqual([path.read_bytes() for path in wrapped],
                         [path.read_bytes() for path in direct])
        report = self._timing(timing)
        self.assertTrue(report["success"])
        self.assertEqual(report["projection_calls"], 1)
        self.assertEqual([row["step"] for row in report["steps"]],
                         ["preflight:repair-a", "preflight:repair-b"])
        self.assertTrue(all(row["elapsed_seconds"] >= 0 for row in report["steps"]))
        self.assertGreaterEqual(report["projection_elapsed_seconds"], 0)

    def test_preflight_validates_all_paths_before_running_and_rejects_lock(self):
        self._publish_two_repairs()
        output = self.root / ".artifacts" / "same.json"
        timing = self.root / ".artifacts" / "unused-timing.json"
        code, _stdout, stderr = self._run(
            "preflight", "--batch-id", "repair-a", "--output", str(output),
            "--batch-id", "repair-b", "--output", str(output),
            "--timing-output", str(timing))
        self.assertNotEqual(code, 0)
        self.assertIn("collision", stderr)
        self.assertFalse(output.exists())

        second = self.root / ".artifacts" / "second.json"
        first_is_second_temporary = second.with_name("." + second.name + ".tmp")
        temp_timing = self.root / ".artifacts" / "temp-collision-timing.json"
        code, _stdout, stderr = self._run(
            "preflight", "--batch-id", "repair-a", "--output",
            str(first_is_second_temporary), "--batch-id", "repair-b", "--output",
            str(second), "--timing-output", str(temp_timing))
        self.assertNotEqual(code, 0)
        self.assertIn("collision", stderr)
        self.assertFalse(first_is_second_temporary.exists())
        self.assertFalse(second.exists())
        self.assertFalse(temp_timing.exists())

        parent = self.root / ".artifacts" / "parent-output"
        nested = parent / "nested.json"
        hierarchy_timing = self.root / ".artifacts" / "hierarchy-timing.json"
        code, _stdout, stderr = self._run(
            "preflight", "--batch-id", "repair-a", "--output", str(parent),
            "--batch-id", "repair-b", "--output", str(nested),
            "--timing-output", str(hierarchy_timing))
        self.assertNotEqual(code, 0)
        self.assertIn("hierarchy collision", stderr)
        self.assertFalse(parent.exists())
        self.assertFalse(hierarchy_timing.exists())

        lock = queue.repository_lock_path(self.root)
        locked_output = self.root / ".artifacts" / "locked.json"
        locked_timing = self.root / ".artifacts" / "locked-timing.json"
        with lock.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            with mock.patch.object(migration, "_validate_live_repair_preimage"), \
                    mock.patch.object(cli_production, "_manifest", return_value=None):
                code, _stdout, stderr = self._run(
                    "preflight", "--batch-id", "repair-a", "--output", str(locked_output),
                    "--timing-output", str(locked_timing))
        self.assertNotEqual(code, 0)
        self.assertIn("lock", stderr.lower())
        self.assertFalse(locked_output.exists())
        self.assertEqual(self._timing(locked_timing)["projection_calls"], 0)

    def test_head_move_does_not_reuse_carried_projection(self):
        self._publish_two_repairs()
        outputs = [self.root / ".artifacts" / f"head-{index}.json" for index in range(2)]
        timing = self.root / ".artifacts" / "head-timing.json"
        actual = steps.cli_main
        calls = 0

        def moving(command):
            nonlocal calls
            code = actual(command)
            calls += 1
            if calls == 1:
                (self.root / "head-drift.txt").write_text("drift\n", encoding="utf-8")
                self.commit("move head between repair preflights")
            return code

        with mock.patch.object(steps, "cli_main", side_effect=moving), \
                mock.patch.object(migration, "_validate_live_repair_preimage"), \
                mock.patch.object(cli_production, "_manifest", return_value=None), \
                mock.patch.object(catalog, "utc_now", return_value=STAMP):
            code, _stdout, stderr = self._run(
                "preflight", "--batch-id", "repair-a", "--output", str(outputs[0]),
                "--batch-id", "repair-b", "--output", str(outputs[1]),
                "--timing-output", str(timing))
        self.assertNotEqual(code, 0)
        self.assertIn("remaining steps not run", stderr)
        report = self._timing(timing)
        self.assertEqual(report["projection_calls"], 2)
        self.assertEqual(report["failure_step"], "preflight:repair-b")
        self.assertTrue(outputs[0].is_file())
        self.assertFalse(outputs[1].exists())

    def test_migration_chain_matches_three_cli_steps_and_replays_once(self):
        candidate = self.candidate([
            self.replace(self.entries[0], target="repaired target"), *self.entries[1:]])
        direct_artifact = self.root / ".artifacts" / "direct-migration.json"
        wrapped_artifact = self.root / ".artifacts" / "wrapped-migration.json"
        timing = self.root / ".artifacts" / "migration-timing.json"
        database = queue.database_path(self.root)
        database_before = database.read_bytes()
        original = queue._projection
        direct_calls = []

        def counted(*args, **kwargs):
            direct_calls.append(1)
            return original(*args, **kwargs)

        commands = [
            ["production", "migration", "plan", "--candidate-catalog", str(candidate),
             "--output", str(direct_artifact), "--recorded-at", STAMP],
            ["production", "migration", "check", "--input", str(direct_artifact),
             "--candidate-catalog", str(candidate)],
            ["production", "migration", "apply", "--input", str(direct_artifact),
             "--candidate-catalog", str(candidate)],
        ]
        with mock.patch.dict(os.environ, {"I18N_REPOSITORY_ROOT": str(self.root)}), \
                mock.patch.object(queue, "_projection", side_effect=counted), \
                mock.patch.object(catalog, "utc_now", return_value=STAMP), \
                redirect_stdout(_CapturedStdout()), redirect_stderr(io.StringIO()):
            self.assertEqual([tools_cli.main(command) for command in commands], [0, 0, 0])
        direct_rows = queue.business_rows(database)
        direct_bytes = direct_artifact.read_bytes()
        self.assertEqual(len(direct_calls), 3)

        database.write_bytes(database_before)
        with mock.patch.object(catalog, "utc_now", return_value=STAMP):
            code, _stdout, stderr = self._run(
                "migration-chain", "--candidate-catalog", str(candidate),
                "--migration-output", str(wrapped_artifact),
                "--timing-output", str(timing), "--recorded-at", STAMP)
        self.assertEqual(code, 0, stderr)
        self.assertEqual(wrapped_artifact.read_bytes(), direct_bytes)
        self.assertEqual(queue.business_rows(database), direct_rows)
        report = self._timing(timing)
        self.assertTrue(report["success"])
        self.assertEqual(report["projection_calls"], 1)
        self.assertEqual([row["exit_code"] for row in report["steps"]], [0, 0, 0])

    def test_publish_chain_matches_rebuild_build_and_migration_and_replays_once(self):
        reference = self.candidate([
            self.replace(self.entries[0], target="published target"), *self.entries[1:]])
        files = {path.relative_to(reference).as_posix(): path.read_bytes()
                 for path in reference.rglob("*") if path.is_file()}
        published = self.root / ".artifacts" / "published-candidate"
        direct_artifact = self.root / ".artifacts" / "direct-migration.json"
        wrapped_artifact = self.root / ".artifacts" / "wrapped-migration.json"
        timing = self.root / ".artifacts" / "publish-timing.json"
        database = queue.database_path(self.root)
        database_before = database.read_bytes()

        # Standalone reference: the same candidate bytes at the same path,
        # followed by the three ordinary migration commands.
        catalog.write_candidate(files, published, repository_root=self.root)
        commands = [
            ["production", "migration", "plan", "--candidate-catalog", str(published),
             "--output", str(direct_artifact), "--recorded-at", STAMP],
            ["production", "migration", "check", "--input", str(direct_artifact),
             "--candidate-catalog", str(published)],
            ["production", "migration", "apply", "--input", str(direct_artifact),
             "--candidate-catalog", str(published)],
        ]
        with mock.patch.dict(os.environ, {"I18N_REPOSITORY_ROOT": str(self.root)}), \
                mock.patch.object(catalog, "utc_now", return_value=STAMP), \
                redirect_stdout(_CapturedStdout()), redirect_stderr(io.StringIO()):
            self.assertEqual([tools_cli.main(command) for command in commands], [0, 0, 0])
        direct_rows = queue.business_rows(database)
        direct_bytes = direct_artifact.read_bytes()

        shutil.rmtree(published)
        database.write_bytes(database_before)
        summary = {"catalog_id": "fixture", "occurrence_count": len(self.entries),
                   "entry_count": len(self.entries), "exclusion_count": 0}
        with mock.patch.object(cli_production, "_manifest", return_value=None), \
                mock.patch.object(catalog, "build_catalog", return_value=files) as build, \
                mock.patch.object(catalog, "check_catalog_tree", return_value=summary), \
                mock.patch.object(catalog, "utc_now", return_value=STAMP):
            code, _stdout, stderr = self._run(
                "publish-chain", "--candidate-catalog", str(published),
                "--migration-output", str(wrapped_artifact),
                "--timing-output", str(timing), "--recorded-at", STAMP,
                "--catalog-recorded-by", "fixture ORCHESTRATOR")
        self.assertEqual(code, 0, stderr)
        self.assertEqual(build.call_args.kwargs,
                         {"recorded_at": STAMP, "recorded_by": "fixture ORCHESTRATOR"})
        self.assertEqual({path.relative_to(published).as_posix(): path.read_bytes()
                          for path in published.rglob("*") if path.is_file()}, files)
        self.assertEqual(wrapped_artifact.read_bytes(), direct_bytes)
        self.assertEqual(queue.business_rows(database), direct_rows)
        report = self._timing(timing)
        self.assertTrue(report["success"])
        self.assertEqual(report["command"], "publish-chain")
        self.assertEqual(report["projection_calls"], 1)
        self.assertEqual([row["step"] for row in report["steps"]],
                         ["queue:rebuild", "catalog:build", "migration:plan",
                          "migration:check", "migration:apply"])

    def test_publish_chain_requires_a_fresh_candidate_before_cli(self):
        existing = self.write_catalog(self.entries, self.root / ".artifacts" / "existing-candidate")
        with mock.patch.object(steps, "cli_main") as cli:
            code, _stdout, stderr = self._run(
                "publish-chain", "--candidate-catalog", str(existing),
                "--migration-output", str(self.root / ".artifacts" / "m.json"),
                "--timing-output", str(self.root / ".artifacts" / "t.json"),
                "--catalog-recorded-by", "fixture")
        self.assertNotEqual(code, 0)
        self.assertIn("candidate-catalog must be fresh", stderr)
        cli.assert_not_called()

    def test_candidate_and_sqlite_drift_fail_before_apply_and_keep_artifact(self):
        for drift in ("candidate", "sqlite"):
            with self.subTest(drift=drift):
                candidate = self.candidate([
                    self.replace(self.entries[0], target=f"{drift} target"), *self.entries[1:]])
                artifact = self.root / ".artifacts" / f"{drift}-migration.json"
                timing = self.root / ".artifacts" / f"{drift}-timing.json"
                database = queue.database_path(self.root)
                before = queue.business_rows(database)
                actual = steps.cli_main
                labels = []

                def mutate_after_check(command):
                    code = actual(command)
                    labels.append(command[1:3])
                    if code == 0 and command[1:3] == ["migration", "check"]:
                        if drift == "candidate":
                            entries = candidate / catalog.CATALOG_PREFIX / "entries.jsonl"
                            entries.write_bytes(entries.read_bytes() + b"{}\n")
                        else:
                            with sqlite3.connect(database) as connection:
                                connection.execute("UPDATE meta SET catalog_id=? WHERE singleton=1",
                                                   ("f" * 64,))
                                connection.commit()
                    return code

                with mock.patch.object(steps, "cli_main", side_effect=mutate_after_check), \
                        mock.patch.object(catalog, "utc_now", return_value=STAMP):
                    code, _stdout, stderr = self._run(
                        "migration-chain", "--candidate-catalog", str(candidate),
                        "--migration-output", str(artifact),
                        "--timing-output", str(timing), "--recorded-at", STAMP)
                self.assertNotEqual(code, 0)
                self.assertIn("migration:apply failed", stderr)
                self.assertTrue(artifact.is_file())
                self.assertEqual(labels, [["migration", "plan"], ["migration", "check"],
                                          ["migration", "apply"]])
                report = self._timing(timing)
                self.assertEqual(report["failure_step"], "migration:apply")
                self.assertEqual(report["projection_calls"], 1)
                if drift == "candidate":
                    self.assertEqual(queue.business_rows(database), before)
                else:
                    # Apply rejected the drift rather than rewriting it.
                    self.assertEqual(queue.business_rows(database)[2][2], "f" * 64)
                    with sqlite3.connect(database) as connection:
                        connection.execute("UPDATE meta SET catalog_id=? WHERE singleton=1",
                                           (before[2][2],))
                        connection.commit()

    def test_migration_input_drift_stops_after_plan_and_preserves_recovery_file(self):
        candidate = self.candidate([
            self.replace(self.entries[0], target="input drift target"), *self.entries[1:]])
        artifact = self.root / ".artifacts" / "input-drift-migration.json"
        timing = self.root / ".artifacts" / "input-drift-timing.json"
        database_before = queue.business_rows(queue.database_path(self.root))
        actual = steps.cli_main
        labels = []

        def mutate_after_plan(command):
            code = actual(command)
            labels.append(command[1:3])
            if code == 0 and command[1:3] == ["migration", "plan"]:
                artifact.write_bytes(artifact.read_bytes() + b"\n")
            return code

        with mock.patch.object(steps, "cli_main", side_effect=mutate_after_plan), \
                mock.patch.object(catalog, "utc_now", return_value=STAMP):
            code, _stdout, stderr = self._run(
                "migration-chain", "--candidate-catalog", str(candidate),
                "--migration-output", str(artifact),
                "--timing-output", str(timing), "--recorded-at", STAMP)
        self.assertNotEqual(code, 0)
        self.assertIn("migration:check failed", stderr)
        self.assertEqual(labels, [["migration", "plan"], ["migration", "check"]])
        self.assertTrue(artifact.read_bytes().endswith(b"\n"))
        self.assertEqual(queue.business_rows(queue.database_path(self.root)), database_before)
        report = self._timing(timing)
        self.assertEqual(report["failure_step"], "migration:check")
        self.assertEqual(report["projection_calls"], 1)


if __name__ == "__main__":
    unittest.main()
