"""Stage-2 same-commit projection cache: exact reuse, isolation and fallback.

The reference is always the original ``queue._projection`` run in the same
fixture with the cache disabled.  A hit must equal it completely (every row,
tuple and type, VerifiedRows digests, complete progress); every doubt must be
a miss that replays; an original replay error must still surface; and entries
outside the ordinary read list must never read a persisted replay.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import shutil
import sqlite3
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

from tests.i18n import test_production_review_v2_lite_migration as migration_tests
from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite_queue as queue
from tools.i18nlib import projection_cache as cache
from tools.i18nlib import git_evidence_reader as reader

REPO = Path(__file__).resolve().parents[2]
ON = {cache.MODE_ENV: "on"}


def _reset_process_state() -> None:
    cache.events.clear()
    cache._frozen.clear()
    cache._poisoned.clear()


def _oracle(root: Path) -> tuple[tuple, dict]:
    progress: dict = {}
    with cache.disabled():
        projection = queue._projection(root, "HEAD", progress=progress)
    return projection, progress


class _Fixture(migration_tests.MigrationFixture):
    _publish_surface_batch = migration_tests.MigrationTests._publish_surface_batch

    def setUp(self):
        super().setUp()
        _reset_process_state()
        self.addCleanup(_reset_process_state)
        self._publish_surface_batch(repair=False, entry_index=1, batch_name="done")
        # Confirmed source evidence: the replay reads commit:path directly.
        self._publish_surface_batch(repair=True, entry_index=0, batch_name="repair")
        self.head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root,
                                            text=True).strip()

    def store(self, root: Path | None = None) -> tuple[tuple, dict, set[str]]:
        root = root or self.root
        progress: dict = {}
        settings = cache.replay_settings(root)
        with mock.patch.dict(os.environ, ON), reader.recording() as objects:
            projection = queue._projection(root, "HEAD", progress=progress)
        with mock.patch.dict(os.environ, ON):
            self.assertTrue(cache.store(root, projection, progress, objects, settings=settings,
                                        environment_ok=queue._publication_git_environment),
                            cache.events)
        return projection, progress, objects

    def load(self, root: Path | None = None, entry: tuple[str, str] = ("batch", "start")):
        root = root or self.root
        with mock.patch.dict(os.environ, ON), cache.entry_scope(*entry):
            return cache.load(root, queue._head(root, "HEAD"),
                              environment_ok=queue._publication_git_environment)

    def cached_file(self, root: Path | None = None) -> Path:
        files = sorted(cache.cache_directory(root or self.root).glob("v1-*.json"))
        self.assertEqual(len(files), 1, files)
        return files[0]

    def assert_equal_projection(self, left: tuple, right: tuple) -> None:
        self.assertEqual(left[0], right[0])
        self.assertEqual(left[1], right[1])
        self.assertEqual(repr(list(left[2])), repr(list(right[2])))
        self.assertIs(type(left[2]), wp1.VerifiedRows)
        self.assertEqual(left[2].digest_by_revision, right[2].digest_by_revision)
        self.assertEqual(left[3], right[3])
        self.assertEqual(left[4], right[4])
        self.assertTrue(all(type(row) is tuple for row in left[3] + left[4]))
        self.assertEqual(repr(left), repr(right))

    def last_reason(self) -> str:
        return cache.events[-1]["reason"]

    def rewrite_payload(self, path: Path, change) -> None:
        """Change the payload and re-sign it, so only strict parsing can refuse."""
        raw = path.read_bytes()
        header_raw, body = raw.split(b"\n", 1)
        header = json.loads(header_raw)
        body = change(body)
        header["payload_bytes"] = len(body)
        header["payload_sha256"] = hashlib.sha256(body).hexdigest()
        path.write_bytes(cache._canonical(header) + b"\n" + body)


class HitEquivalenceTests(_Fixture):
    def test_hit_equals_the_independent_replay_completely(self):
        stored, stored_progress, objects = self.store()
        oracle, oracle_progress = _oracle(self.root)
        self.assert_equal_projection(stored, oracle)
        self.assertEqual(stored_progress, oracle_progress)
        hit = self.load()
        self.assertIsNotNone(hit, cache.events)
        self.assert_equal_projection(hit[0], oracle)
        self.assertEqual(hit[1], oracle_progress)
        self.assertEqual(cache.events[-1]["event"], "hit")
        # Source evidence is named even though the replay read it outside the reader.
        evidence = [name for name in objects if name.endswith(":source-evidence.txt")]
        self.assertEqual(len(evidence), 1, objects)
        self.assertIn(evidence[0].split(":")[0], objects)
        self.assertNotIn(reader.INCOMPLETE, objects)

    def test_projection_for_uses_hit_and_carry_without_replaying(self):
        self.store()
        oracle, oracle_progress = _oracle(self.root)
        with mock.patch.dict(os.environ, ON), cache.entry_scope("batch", "surface-export"), \
                mock.patch.object(queue, "_projection", wraps=queue._projection) as replay, \
                queue.carry_projection():
            projection = queue.projection_for(self.root, "HEAD")
            again, progress = queue.projection_and_progress_for(self.root, "HEAD")
        self.assertEqual(replay.call_count, 0)
        self.assert_equal_projection(projection, oracle)
        self.assert_equal_projection(again, oracle)
        self.assertEqual(progress, oracle_progress)

    def test_cross_process_hit(self):
        script = (
            "import hashlib, json, os, sys\n"
            "from pathlib import Path\n"
            f"sys.path.insert(0, {str(REPO)!r})\n"
            "from tools.i18nlib import production_review_v2_lite_queue as q, projection_cache as c\n"
            "calls = []\n"
            "original = q._projection\n"
            "def spy(*a, **k):\n"
            "    calls.append(1)\n"
            "    return original(*a, **k)\n"
            "q._projection = spy\n"
            "with c.entry_scope('batch', 'start'):\n"
            "    p, progress = q.projection_and_progress_for(Path(sys.argv[1]), 'HEAD')\n"
            "print(json.dumps({'calls': len(calls), 'events': c.events,\n"
            "    'digest': hashlib.sha256(repr(p).encode()).hexdigest(), 'progress': progress}))\n")
        environment = {**os.environ, **ON}
        environment.pop(cache.TRACE_ENV, None)

        def run() -> dict:
            output = subprocess.run([sys.executable, "-B", "-c", script, str(self.root)],
                                    check=True, stdout=subprocess.PIPE, env=environment,
                                    cwd=REPO, timeout=300).stdout
            return json.loads(output)

        cold, warm = run(), run()
        oracle, oracle_progress = _oracle(self.root)
        digest = hashlib.sha256(repr(oracle).encode()).hexdigest()
        self.assertEqual((cold["calls"], warm["calls"]), (1, 0), (cold["events"], warm["events"]))
        self.assertEqual([event["event"] for event in cold["events"]], ["miss", "stored"])
        self.assertEqual([event["event"] for event in warm["events"]], ["hit"])
        self.assertEqual({cold["digest"], warm["digest"]}, {digest})
        self.assertEqual(cold["progress"], oracle_progress)
        self.assertEqual(warm["progress"], oracle_progress)

    def test_trace_prints_one_minimal_line(self):
        self.store()
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, {cache.TRACE_ENV: "1"}), contextlib.redirect_stderr(stderr):
            self.assertIsNotNone(self.load())
        self.assertEqual(stderr.getvalue(), "projection-cache: hit exact key and objects verified\n")


class SwitchAndEntryTests(_Fixture):
    def test_off_never_reads_writes_or_creates(self):
        for value in (None, "off", "ON", "1", ""):
            with self.subTest(value=value), mock.patch.dict(os.environ):
                os.environ.pop(cache.MODE_ENV, None)
                if value is not None:
                    os.environ[cache.MODE_ENV] = value
                self.assertFalse(cache.enabled())
                with cache.entry_scope("batch", "start"), queue.carry_projection():
                    queue.projection_for(self.root, "HEAD")
                queue.rebuild(self.root)
                self.assertFalse(cache.cache_directory(self.root).exists())
                self.assertEqual(cache.events, [])
        self.store()
        with mock.patch.dict(os.environ, ON), cache.disabled(), cache.entry_scope("batch", "start"):
            self.assertFalse(cache.reads_allowed())
            self.assertIsNone(cache.load(self.root, self.head,
                                         environment_ok=queue._publication_git_environment))
            self.assertFalse(cache.store(self.root, *_oracle(self.root), set(),
                                         settings=cache.replay_settings(self.root),
                                         environment_ok=queue._publication_git_environment))

    def test_non_listed_entries_never_read(self):
        self.store()
        entries = {("queue", "init"), ("queue", "rebuild"), ("queue", "check"), ("queue", "status"),
                   ("batch", "show"), ("batch", "abandon"), ("batch", "recover"),
                   ("batch", "finalize"), ("batch", "recover-from-head"), ("batch", "host-block"),
                   ("migration", "plan"), ("migration", "check"), ("migration", "apply"),
                   ("repair", "unknown")}
        self.assertFalse(entries & cache.READ_ENTRIES)
        for entry in entries:
            with self.subTest(entry=entry), mock.patch.dict(os.environ, ON), \
                    cache.entry_scope("batch", "start"), cache.entry_scope(*entry):
                self.assertFalse(cache.reads_allowed())
        for entry in cache.READ_ENTRIES:
            with mock.patch.dict(os.environ, ON), cache.entry_scope(*entry):
                self.assertTrue(cache.reads_allowed())

    def test_queue_commands_replay_independently_even_with_a_valid_cache(self):
        self.store()
        for name, call in (("rebuild", lambda: queue.rebuild(self.root)),
                           ("check", lambda: queue.check(self.root)),
                           ("status", lambda: queue.status(self.root))):
            with self.subTest(name=name), mock.patch.dict(os.environ, ON), \
                    cache.entry_scope("batch", "start"), \
                    mock.patch.object(cache, "load", wraps=cache.load) as load, \
                    mock.patch.object(queue, "_projection", wraps=queue._projection) as replay:
                report = call()
            self.assertEqual(load.call_count, 0)
            self.assertEqual(replay.call_count, 1)
            self.assertEqual(report["progress"], _oracle(self.root)[1])

    def test_recovery_and_closing_entries_pin_independent_replay(self):
        from tools.i18nlib import production_review_v2_lite_batch as batch
        self.store()
        seen: list[bool] = []
        missing = self.root / "no-such-checkpoint.json"

        def checkpoint_path(_root):
            seen.append(cache.reads_allowed())
            return missing

        calls = ((batch.finalize, (self.root, "0" * 40)), (batch.recover, (self.root,)),
                 (batch.recover_from_head, (self.root,)), (batch.abandon, (self.root,)))
        for function, arguments in calls:
            with self.subTest(function=function.__name__), mock.patch.dict(os.environ, ON), \
                    cache.entry_scope("batch", "start"), \
                    mock.patch.object(queue, "checkpoint_path", side_effect=checkpoint_path), \
                    mock.patch.object(cache, "load", wraps=cache.load) as load:
                with contextlib.suppress(wp1.ProductionReviewError):
                    function(*arguments)
                self.assertEqual(load.call_count, 0)
        self.assertTrue(seen)
        self.assertFalse(any(seen))
        # Recovery still replays in full and matches the oracle.
        with mock.patch.dict(os.environ, ON), cache.entry_scope("batch", "start"), \
                mock.patch.object(queue, "_projection", wraps=queue._projection) as replay:
            batch.recover(self.root)
        self.assertGreaterEqual(replay.call_count, 1)

    def test_cli_scope_reads_only_for_listed_actions(self):
        from tools.i18nlib import cli
        self.store()
        environment = {**ON, "I18N_REPOSITORY_ROOT": str(self.root)}
        with mock.patch.dict(os.environ, environment), \
                mock.patch.object(queue, "_projection", wraps=queue._projection) as replay, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["production", "queue", "check"]), 0)
            self.assertEqual(replay.call_count, 1)
            self.assertEqual(cli.main(["production", "batch", "start", "--limit", "1"]), 0)
            self.assertEqual(replay.call_count, 1)
        self.assertEqual(cache.events[-1]["event"], "hit")


class RealEntryTests(_Fixture):
    """``python3 -B tools/i18n`` itself: its ``__main__`` has no ``.py`` suffix."""

    def _code_copy(self) -> Path:
        code = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, code, True)
        shutil.copytree(REPO / "tools", code / "tools",
                        ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(REPO / "i18n" / "quality", code / "i18n" / "quality")
        InputIdentityTests._age(code)
        return code

    def _cli(self, code: Path, root: Path, mode: str, *action: str) -> tuple[str, list[str]]:
        environment = {**os.environ, cache.MODE_ENV: mode, cache.TRACE_ENV: "1",
                       "I18N_REPOSITORY_ROOT": str(root)}
        result = subprocess.run([sys.executable, "-B", "tools/i18n", "production", "batch", *action],
                                cwd=code, env=environment, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, timeout=300)
        self.assertEqual(result.returncode, 0, result.stderr)
        trace = [line for line in result.stderr.splitlines() if line.startswith("projection-cache: ")]
        return result.stdout, trace

    def _start(self, code: Path, root: Path, mode: str) -> tuple[str, list[str]]:
        return self._cli(code, root, mode, "start", "--limit", "1")

    def _abandon(self, code: Path, root: Path) -> None:
        _stdout, trace = self._cli(code, root, "on", "abandon")
        self.assertFalse([line for line in trace if " hit " in line], trace)
        self.assertFalse(queue.checkpoint_path(root).exists())

    def _state(self, root: Path) -> tuple[str, str]:
        return (queue._head(root, "HEAD"),
                subprocess.check_output(["git", "status", "--porcelain", "--ignored"], cwd=root,
                                        text=True))

    def test_standard_entry_cold_warm_off_and_entry_bytes_change(self):
        code = self._code_copy()
        twin = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, twin, True)
        shutil.copytree(self.root, twin, symlinks=True, dirs_exist_ok=True)
        directory = cache.cache_directory(self.root)

        cold, cold_trace = self._start(code, self.root, "on")
        self.assertIn("projection-cache: stored complete replay published", cold_trace)
        self.assertFalse([line for line in cold_trace if " hit " in line], cold_trace)
        files = sorted(directory.glob("v1-*.json"))
        self.assertEqual(len(files), 1, cold_trace)
        after_cold = self._state(self.root)
        self._abandon(code, self.root)

        warm, warm_trace = self._start(code, self.root, "on")
        self.assertIn("projection-cache: hit exact key and objects verified", warm_trace)
        self.assertFalse([line for line in warm_trace if " miss " in line], warm_trace)
        self.assertEqual(warm, cold)
        self.assertEqual(self._state(self.root), after_cold)

        off, off_trace = self._start(code, twin, "off")
        self.assertEqual(off_trace, [])
        self.assertFalse(cache.cache_directory(twin).exists())
        self.assertEqual(off, cold)
        self.assertEqual(self._state(twin)[0], after_cold[0])

        # Entry bytes change with HEAD unchanged: a new key, never the old file.
        self._abandon(code, self.root)
        with (code / "tools" / "i18n").open("a") as handle:
            handle.write("# entry changed\n")
        InputIdentityTests._age(code)
        changed, changed_trace = self._start(code, self.root, "on")
        self.assertIn("projection-cache: miss no cache file for this key", changed_trace)
        self.assertFalse([line for line in changed_trace if " hit " in line], changed_trace)
        self.assertEqual(changed, cold)
        self.assertEqual(len(sorted(directory.glob("v1-*.json"))), 2)

    def test_only_the_known_entry_is_accepted_as_an_extensionless_module(self):
        code = self._code_copy()
        now = time.time_ns()
        entry = mock.Mock(__file__=str(code / "tools" / "i18n"))
        other = mock.Mock(__file__=str(code / "tools" / "pi-review"))
        with mock.patch.dict(sys.modules, {"__main__": entry}):
            cache._loaded_modules(code, now)
        with mock.patch.dict(sys.modules, {"__main__": other}), self.assertRaises(cache._Skip):
            cache._loaded_modules(code, now)
        before = cache._code_digest(code, now)
        (code / "tools" / "pi-review").write_text("changed\n")
        InputIdentityTests._age(code)
        self.assertEqual(cache._code_digest(code, now), before)
        (code / "tools" / "i18n").write_text("changed\n")
        InputIdentityTests._age(code)
        self.assertNotEqual(cache._code_digest(code, now), before)


class ActiveStateStillCheckedTests(_Fixture):
    def _run_start(self, root: Path, environment: dict) -> tuple[int, str, str]:
        from tools.i18nlib import cli
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, {**environment, "I18N_REPOSITORY_ROOT": str(root)}), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = cli.main(["production", "batch", "start", "--limit", "1"])
            except wp1.ProductionReviewError as error:
                return 1, "", str(error)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_sqlite_drift_is_rejected_on_a_hit(self):
        self.store()
        with sqlite3.connect(queue.database_path(self.root)) as connection:
            connection.execute("DELETE FROM state_override")
        with mock.patch.object(queue, "_projection", wraps=queue._projection) as replay:
            code, _stdout, error = self._run_start(self.root, ON)
        self.assertEqual(replay.call_count, 0)
        self.assertNotEqual(code, 0)
        self.assertIn("drift", error)
        self.assertFalse(queue.checkpoint_path(self.root).exists())

    def test_on_and_off_start_produce_the_same_business_state(self):
        twin = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, twin, True)
        shutil.copytree(self.root, twin, symlinks=True, dirs_exist_ok=True)
        self.store()
        with mock.patch.object(queue, "_projection", wraps=queue._projection) as replay:
            on = self._run_start(self.root, ON)
            on_calls = replay.call_count
            off = self._run_start(twin, {cache.MODE_ENV: "off"})
        self.assertEqual((on_calls, replay.call_count), (0, 1))
        self.assertEqual(on[0], 0)
        self.assertEqual(on[:2], off[:2])

        def business(root: Path):
            overrides, reconciliation, meta = queue.business_rows(queue.database_path(root))
            checkpoint = json.loads(queue.checkpoint_path(root).read_bytes())
            checkpoint.pop("created_at")
            return ([row[:6] for row in overrides], reconciliation, meta, checkpoint)

        self.assertEqual(business(self.root), business(twin))


class MissAndFallbackTests(_Fixture):
    def test_cache_faults_are_misses_and_replay_still_matches(self):
        self.store()
        path = self.cached_file()
        original = path.read_bytes()
        faults = {
            "truncated": lambda: path.write_bytes(original[: len(original) // 2]),
            "flipped": lambda: path.write_bytes(original[:-5] + bytes([original[-5] ^ 1]) + original[-4:]),
            "empty": lambda: path.write_bytes(b""),
            "duplicate key": lambda: self.rewrite_payload(
                path, lambda body: b'{"progress":{},' + body[1:]),
            "wrong type": lambda: self.rewrite_payload(
                path, lambda body: _edit(body, lambda payload: payload.update(
                    evidence_head=[payload["evidence_head"]]))),
            "row as object": lambda: self.rewrite_payload(
                path, lambda body: _edit(body, lambda payload: payload["overrides"].__setitem__(
                    0, {str(index): value for index, value in enumerate(payload["overrides"][0])}))),
            "misaligned digests": lambda: self.rewrite_payload(
                path, lambda body: _edit(body, lambda payload: payload["entry_digests"].pop())),
            "override bool": lambda: self.rewrite_payload(
                path, lambda body: _edit(body, lambda payload: payload["overrides"][0].__setitem__(4, True))),
            "other key": lambda: self.rewrite_payload(
                path, lambda body: _edit(body, lambda payload: payload["key"].update(commit="0" * 40))),
            "non-finite": lambda: self.rewrite_payload(
                path, lambda body: body.replace(b'"ratio":', b'"ratio":NaN,"x":', 1)),
            "symlink": lambda: (path.unlink(), path.symlink_to(self.root / "elsewhere.json"),
                                (self.root / "elsewhere.json").write_bytes(original)),
        }
        oracle, oracle_progress = _oracle(self.root)
        for name, damage in faults.items():
            with self.subTest(fault=name):
                path.unlink(missing_ok=True)
                path.write_bytes(original)
                self.assertIsNotNone(self.load())
                damage()
                self.assertIsNone(self.load())
                self.assertEqual(cache.events[-1]["event"], "miss")
                with mock.patch.dict(os.environ, ON), cache.entry_scope("batch", "start"), \
                        mock.patch.object(queue, "_projection", wraps=queue._projection) as replay:
                    value, progress = queue.projection_and_progress_for(self.root, "HEAD")
                self.assertEqual(replay.call_count, 1)
                self.assert_equal_projection(value, oracle)
                self.assertEqual(progress, oracle_progress)
                (self.root / "elsewhere.json").unlink(missing_ok=True)

    def test_oversize_and_unwritable_only_lose_speed(self):
        with mock.patch.object(cache, "MAX_TOTAL_BYTES", 1024), mock.patch.dict(os.environ, ON):
            report = queue.rebuild(self.root)
        self.assertEqual(self.last_reason(), "oversize")
        self.assertTrue(report["ok"])
        self.assertFalse(cache.cache_directory(self.root).exists())
        self.store()
        directory = cache.cache_directory(self.root)
        self.cached_file().unlink()
        directory.chmod(0o500)
        self.addCleanup(directory.chmod, 0o700)
        if os.access(directory, os.W_OK):
            self.skipTest("running with privileges that ignore directory modes")
        with mock.patch.dict(os.environ, ON):
            report = queue.rebuild(self.root)
        self.assertTrue(report["ok"])
        self.assertEqual(cache.events[-1]["event"], "store-skipped")
        self.assertEqual(os.listdir(directory), [])

    def test_symlinked_cache_directory_is_never_used(self):
        outside = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, outside, True)
        artifacts = self.root / ".artifacts" / "i18n"
        artifacts.mkdir(parents=True, exist_ok=True)
        (artifacts / "projection-cache-v1").symlink_to(outside, target_is_directory=True)
        with mock.patch.dict(os.environ, ON):
            queue.rebuild(self.root)
        self.assertEqual(self.last_reason(), "cache path component is not an ordinary directory")
        self.assertEqual(os.listdir(outside), [])

    def test_failed_replay_is_not_cached_and_error_surfaces(self):
        with mock.patch.dict(os.environ, ON), \
                mock.patch.object(queue, "_batch_rows", side_effect=wp1.ProductionReviewError("boom")):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "boom"):
                queue.rebuild(self.root)
        self.assertFalse(cache.cache_directory(self.root).exists())

    def test_store_failure_never_fails_the_business_replay(self):
        with mock.patch.dict(os.environ, ON), \
                mock.patch.object(cache, "_encode", side_effect=RuntimeError("encoder bug")):
            report = queue.rebuild(self.root)
        self.assertTrue(report["ok"])
        self.assertEqual(self.last_reason(), "cache write failed: RuntimeError")



class FifoCacheFileTests(_Fixture):
    """NR-001: a writer-less FIFO under the cache name must miss, never block.

    Every open runs in a child process with a short timeout, so a regression
    ends the test instead of hanging it.
    """
    TIMEOUT = 20
    SCRIPT = (
        "import hashlib, json, os, sys\n"
        "from pathlib import Path\n"
        f"sys.path.insert(0, {str(REPO)!r})\n"
        "from tools.i18nlib import production_review as wp1\n"
        "from tools.i18nlib import production_review_v2_lite_queue as q, projection_cache as c\n"
        "root, mode = Path(sys.argv[1]), sys.argv[2]\n"
        "if mode == 'old-flags':\n"
        "    os.open(sys.argv[3], os.O_RDONLY | os.O_NOFOLLOW)\n"
        "    raise SystemExit('old flags did not block')\n"
        "calls = []\n"
        "original = q._projection\n"
        "def spy(*a, **k):\n"
        "    calls.append(1)\n"
        "    if mode == 'fail':\n"
        "        raise wp1.ProductionReviewError('fifo replay boom')\n"
        "    return original(*a, **k)\n"
        "q._projection = spy\n"
        "with c.entry_scope('batch', 'start'):\n"
        "    direct = c.load(root, q._head(root, 'HEAD'), environment_ok=q._publication_git_environment)\n"
        "    load_events = list(c.events)\n"
        "    try:\n"
        "        p, progress = q.projection_and_progress_for(root, 'HEAD')\n"
        "        error = None\n"
        "    except wp1.ProductionReviewError as caught:\n"
        "        p, progress, error = None, None, str(caught)\n"
        "print(json.dumps({'direct': direct is None, 'load_events': load_events, 'calls': len(calls),\n"
        "    'error': error, 'digest': hashlib.sha256(repr(p).encode()).hexdigest(), 'progress': progress}))\n")

    def run_child(self, *arguments: str) -> subprocess.CompletedProcess:
        environment = {**os.environ, **ON}
        environment.pop(cache.TRACE_ENV, None)
        return subprocess.run([sys.executable, "-B", "-c", self.SCRIPT, str(self.root), *arguments],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment,
                              cwd=REPO, timeout=self.TIMEOUT)

    def plant_fifo(self) -> Path:
        # Seed from a child: the key must be the one a fresh process computes.
        seeded = self.run_child("ok")
        self.assertEqual(seeded.returncode, 0, seeded.stderr.decode(errors="replace"))
        path = self.cached_file()
        path.unlink()
        os.mkfifo(path)
        self.assertTrue(stat.S_ISFIFO(path.lstat().st_mode))
        return path

    def test_fifo_misses_quickly_and_replay_matches(self):
        self.plant_fifo()
        oracle, oracle_progress = _oracle(self.root)
        started = time.monotonic()
        result = self.run_child("ok")
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        self.assertLess(time.monotonic() - started, self.TIMEOUT)
        output = json.loads(result.stdout)
        self.assertTrue(output["direct"])
        self.assertEqual([(event["event"], event["reason"]) for event in output["load_events"]],
                         [("miss", "cache file is not an ordinary bounded file")])
        self.assertEqual(output["calls"], 1)
        self.assertIsNone(output["error"])
        self.assertEqual(output["digest"], hashlib.sha256(repr(oracle).encode()).hexdigest())
        self.assertEqual(output["progress"], oracle_progress)

    def test_fifo_miss_still_surfaces_the_replay_error(self):
        path = self.plant_fifo()
        result = self.run_child("fail")
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        output = json.loads(result.stdout)
        self.assertTrue(output["direct"])
        self.assertEqual(output["calls"], 1)
        self.assertEqual(output["error"], "fifo replay boom")
        self.assertTrue(stat.S_ISFIFO(path.lstat().st_mode))

    def test_negative_control_old_flags_block_on_the_same_fifo(self):
        path = self.plant_fifo()
        with self.assertRaises(subprocess.TimeoutExpired):
            subprocess.run([sys.executable, "-B", "-c", self.SCRIPT, str(self.root), "old-flags", str(path)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=REPO, timeout=2)


class MigrationBoundaryTests(_Fixture):
    def test_reconciliation_rows_round_trip_exactly(self):
        from tests.i18n import test_projection_stage1 as stage1_tests
        stage1_tests._Boundaries._publish_boundary(
            self, [self.replace(self.entries[0], target="revised target"), self.entries[1]], "changed")
        oracle, oracle_progress = _oracle(self.root)
        self.assertEqual({row[5] for row in oracle[4]}, {"unchanged", "target_changed", "removed"})
        self.assertTrue(any(row[2] is None and row[3] is None for row in oracle[4]))
        self.store()
        hit = self.load()
        self.assertIsNotNone(hit, cache.events)
        self.assert_equal_projection(hit[0], oracle)
        self.assertEqual(hit[1], oracle_progress)


class InputIdentityTests(_Fixture):
    def _fake_code_root(self) -> Path:
        code = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, code, True)
        (code / "tools" / "sub").mkdir(parents=True)
        (code / "i18n" / "quality").mkdir(parents=True)
        (code / "tools" / "a.py").write_text("A = 1\n")
        (code / "tools" / "sub" / "b.py").write_text("B = 1\n")
        (code / "tools" / "notes.txt").write_text("not code\n")
        (code / "i18n" / "quality" / "rules.json").write_text("{}\n")
        self._age(code)
        return code

    @staticmethod
    def _age(code: Path) -> None:
        past = time.time() - 3600
        for path in code.rglob("*"):
            os.utime(path, (past, past), follow_symlinks=False)

    def _store_with(self, code: Path) -> None:
        progress: dict = {}
        with reader.recording() as objects:
            projection = queue._projection(self.root, "HEAD", progress=progress)
        with mock.patch.dict(os.environ, ON):
            self.assertTrue(cache.store(self.root, projection, progress, objects, code_root=code,
                                        settings=cache.replay_settings(self.root),
                                        environment_ok=queue._publication_git_environment),
                            cache.events)

    def _load_with(self, code: Path):
        with mock.patch.dict(os.environ, ON), cache.entry_scope("batch", "start"):
            return cache.load(self.root, self.head, code_root=code,
                              environment_ok=queue._publication_git_environment)

    def test_implementation_and_rule_changes_miss_with_head_unchanged(self):
        changes = {
            "edited": lambda code: (code / "tools" / "sub" / "b.py").write_text("B = 2\n"),
            "added": lambda code: (code / "tools" / "c.py").write_text("C = 1\n"),
            "removed": lambda code: (code / "tools" / "a.py").unlink(),
            "rule": lambda code: (code / "i18n" / "quality" / "rules.json").write_text("{\"x\":1}\n"),
            "nested rule": lambda code: ((code / "i18n" / "quality" / "d").mkdir(),
                                         (code / "i18n" / "quality" / "d" / "e.sql").write_text("x")),
        }
        for name, change in changes.items():
            with self.subTest(change=name):
                shutil.rmtree(cache.cache_directory(self.root), ignore_errors=True)
                _reset_process_state()
                code = self._fake_code_root()
                self._store_with(code)
                self.assertIsNotNone(self._load_with(code))
                change(code)
                self._age(code)
                _reset_process_state()  # a new process sees only the new bytes
                self.assertIsNone(self._load_with(code))
                self.assertEqual(self.last_reason(), "no cache file for this key")
        # Non-code files outside the rule directory do not participate.
        _reset_process_state()
        shutil.rmtree(cache.cache_directory(self.root), ignore_errors=True)
        code = self._fake_code_root()
        self._store_with(code)
        (code / "tools" / "notes.txt").write_text("still not code\n")
        self._age(code)
        _reset_process_state()
        self.assertIsNotNone(self._load_with(code))

    def test_hot_edit_after_start_is_refused_for_the_rest_of_the_process(self):
        code = self._fake_code_root()
        self._store_with(code)
        self.assertIsNotNone(self._load_with(code))
        (code / "tools" / "a.py").write_text("A = 2\n")
        self._age(code)  # even with an old mtime, the frozen identity differs
        self.assertIsNone(self._load_with(code))
        self.assertEqual(self.last_reason(), "implementation changed during this process")
        (code / "tools" / "a.py").write_text("A = 1\n")
        self._age(code)
        self.assertIsNone(self._load_with(code))
        self.assertEqual(self.last_reason(), "implementation changed during this process")
        _reset_process_state()
        code = self._fake_code_root()
        (code / "tools" / "a.py").write_text("A = 3\n")  # fresh mtime: after process start
        self.assertIsNone(self._load_with(code))
        self.assertEqual(self.last_reason(), "code input modified after process start")

    def test_same_commit_other_root_is_isolated_even_with_the_right_file_name(self):
        twin = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, twin, True)
        subprocess.run(["git", "clone", "-q", str(self.root), str(twin)], check=True)
        self.assertEqual(queue._head(twin, "HEAD"), self.head)
        self.store()
        self.assertFalse(cache.cache_directory(twin).exists())
        self.assertIsNone(self.load(twin))
        # Plant the source file under the name the twin itself would compute.
        key = cache._key(twin, self.head, cache.CODE_ROOT)
        directory = cache.cache_directory(twin)
        directory.mkdir(parents=True)
        shutil.copyfile(self.cached_file(), directory / cache._file_name(key))
        self.assertIsNone(self.load(twin))
        self.assertEqual(self.last_reason(), "cache header, length or digest mismatch")

    def test_head_change_new_gate_file_misses_and_matches_oracle(self):
        self.store()
        (self.root / "tools").mkdir(exist_ok=True)
        (self.root / "tools" / "ci-gates.sh").write_text("#!/bin/sh\n")
        self.commit("add gate")
        oracle = _oracle(self.root)
        self.assertIsNone(self.load())
        self.assertEqual(self.last_reason(), "no cache file for this key")
        with mock.patch.dict(os.environ, ON), cache.entry_scope("batch", "start"):
            value, progress = queue.projection_and_progress_for(self.root, "HEAD")
        self.assert_equal_projection(value, oracle[0])
        self.assertEqual(progress, oracle[1])


class GitEnvironmentTests(_Fixture):
    def _git_path(self, *parts: str) -> Path:
        return Path(subprocess.check_output(["git", "rev-parse", "--absolute-git-dir"],
                                            cwd=self.root, text=True).strip(), *parts)

    def test_special_environments_miss(self):
        self.store()
        self.assertIsNotNone(self.load())
        cases = {
            "shallow": (lambda: self._git_path("shallow").write_text(self.head + "\n"),
                        lambda: self._git_path("shallow").unlink()),
            "grafts": (lambda: (self._git_path("info").mkdir(exist_ok=True),
                                self._git_path("info", "grafts").write_text(self.head + "\n")),
                       lambda: self._git_path("info", "grafts").unlink()),
            "replace": (lambda: subprocess.run(["git", "replace", "-f", self.head, f"{self.head}^"],
                                               cwd=self.root, check=True),
                        lambda: subprocess.run(["git", "replace", "-d", self.head], cwd=self.root,
                                               check=True, stdout=subprocess.DEVNULL)),
            "config": (lambda: subprocess.run(["git", "config", "core.commitGraph", "false"],
                                              cwd=self.root, check=True),
                       lambda: subprocess.run(["git", "config", "--unset", "core.commitGraph"],
                                              cwd=self.root, check=True)),
        }
        for name, (apply, undo) in cases.items():
            with self.subTest(case=name):
                apply()
                try:
                    self.assertIsNone(self.load())
                    self.assertEqual(self.last_reason(), "git environment is not the plain audited case")
                finally:
                    undo()
                self.assertIsNotNone(self.load())
        with mock.patch.dict(os.environ, {"GIT_OBJECT_DIRECTORY": str(self._git_path("objects"))}):
            self.assertIsNone(self.load())
        self.assertIsNotNone(self.load())

    def _loose(self, oid: str) -> Path:
        return self._git_path("objects", oid[:2], oid[2:])

    def test_missing_recorded_object_outside_the_commit_closure_misses(self):
        # An object the replay named that HEAD cannot reach, like public source
        # evidence fetched from elsewhere: only the recorded list protects it.
        extra = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=self.root, check=True,
                               input=b"unreachable evidence", stdout=subprocess.PIPE).stdout.decode().strip()
        progress: dict = {}
        with reader.recording() as objects:
            projection = queue._projection(self.root, "HEAD", progress=progress)
            reader.note_object(extra)
        with mock.patch.dict(os.environ, ON):
            self.assertTrue(cache.store(self.root, projection, progress, objects,
                                        settings=cache.replay_settings(self.root),
                                        environment_ok=queue._publication_git_environment))
        self.assertIsNotNone(self.load())
        self._loose(extra).unlink()
        self.assertIsNone(self.load())
        self.assertEqual(self.last_reason(), "recorded Git object is missing or unreadable")

    def test_missing_reachable_object_misses_and_the_replay_error_surfaces(self):
        _stored, _progress, objects = self.store()
        blob = subprocess.check_output(
            ["git", "rev-parse", "HEAD:evidence/production-review-v2-lite/batches/done/results.jsonl"],
            cwd=self.root, text=True).strip()
        self.assertIn(blob, objects)
        self._loose(blob).unlink()
        self.assertIsNone(self.load())
        self.assertEqual(self.last_reason(), "recorded Git object is missing or unreadable")
        with mock.patch.dict(os.environ, ON), cache.entry_scope("batch", "start"):
            with self.assertRaises(wp1.ProductionReviewError):
                queue.projection_for(self.root, "HEAD")

    def test_unrecorded_reachable_object_is_caught_by_connectivity(self):
        self.store()
        tree = subprocess.check_output(["git", "rev-parse", "HEAD:evidence/production-review-v2-lite/batches"],
                                       cwd=self.root, text=True).strip()
        # A subtree is read by ls-tree -r but never named by the reader.
        self._loose(tree).unlink()
        self.assertIsNone(self.load())
        self.assertEqual(self.last_reason(), "commit object closure is not connected")

    def test_incomplete_record_is_never_published(self):
        progress: dict = {}
        with reader.recording() as objects:
            projection = queue._projection(self.root, "HEAD", progress=progress)
            reader.note_object("bad\nname")
        with mock.patch.dict(os.environ, ON):
            self.assertFalse(cache.store(self.root, projection, progress, objects,
                                         settings=cache.replay_settings(self.root),
                                         environment_ok=queue._publication_git_environment))
        self.assertEqual(self.last_reason(), "replay named an object that cannot be rechecked")


class GitSettingsTests(_Fixture):
    """SR-001: diff.renames moves the located publication commit of a path
    that was a directory in the publication base, so it is part of the key."""

    BATCH = "evidence/production-review-v2-lite/batches/boundary"
    PATH = BATCH + "/raw/translation_surface_screen_v1/input.json"

    def _renames(self, value: str | None) -> None:
        if value is None:
            subprocess.run(["git", "config", "--unset-all", "diff.renames"], cwd=self.root)
        else:
            subprocess.run(["git", "config", "diff.renames", value], cwd=self.root, check=True)

    def _directory_to_file_history(self) -> str:
        """Publish a batch whose base holds its input.json path as a directory."""
        before = self.head
        self._publish_surface_batch(repair=False, entry_index=2, batch_name="boundary")
        published = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        input_raw = subprocess.check_output(["git", "show", f"{published}:{self.PATH}"], cwd=self.root)
        subprocess.run(["git", "reset", "-q", "--hard", before], cwd=self.root, check=True)
        (self.root / self.PATH).mkdir(parents=True)
        (self.root / self.PATH / "child").write_bytes(input_raw)
        base = self.commit("directory at the later evidence path")
        shutil.rmtree(self.root / self.PATH)
        subprocess.run(["git", "checkout", "-q", published, "--", self.BATCH], cwd=self.root, check=True)
        manifest_path = self.root / self.BATCH / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["base_commit"] = base
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        publication = self.commit("directory replaced by the same bytes as a file")
        self.head = publication
        return publication

    def _independent(self):
        """The no-cache oracle: (projection, progress) or the error it raises."""
        try:
            return _oracle(self.root)
        except wp1.ProductionReviewError as error:
            return error

    def _through_cache(self):
        with mock.patch.dict(os.environ, ON), cache.entry_scope("batch", "start"):
            try:
                return queue.projection_and_progress_for(self.root, "HEAD")
            except wp1.ProductionReviewError as error:
                return error

    def _assert_same(self, got, expected) -> None:
        if isinstance(expected, Exception):
            self.assertIsInstance(got, wp1.ProductionReviewError)
            self.assertEqual(str(got), str(expected))
        else:
            self.assertNotIsInstance(got, Exception, got)
            self.assert_equal_projection(got[0], expected[0])
            self.assertEqual(got[1], expected[1])

    def test_directory_to_file_history_depends_on_diff_renames_and_switch_misses(self):
        publication = self._directory_to_file_history()
        located = {}
        for value in ("true", "false"):
            self._renames(value)
            with reader.projection_scope(self.root):
                located[value] = queue._candidate_commits(self.root, "HEAD", self.PATH)
        self.assertNotIn(publication, located["true"])
        self.assertEqual(located["false"][0], publication)
        oracle = {}
        for value in ("false", "true", None):
            self._renames(value)
            oracle[value] = self._independent()
        self.assertNotIsInstance(oracle["false"], Exception)
        self.assertRegex(str(oracle["true"]), "not published in one commit")
        self.assertEqual(str(oracle[None]), str(oracle["true"]))  # Git's own default
        # One process, switching back and forth: each value only ever sees its
        # own replay; a success stored under one never answers for another.
        for value in ("false", "true", None, "false", "true"):
            with self.subTest(diff_renames=value):
                self._renames(value)
                cache.events.clear()
                self._assert_same(self._through_cache(), oracle[value])
                if value == "false":
                    self.assertIn(cache.events[-1]["event"], {"hit", "stored"}, cache.events)
                else:
                    self.assertEqual(cache.events[0]["event"], "miss")
                    self.assertFalse(any(event["event"] == "hit" for event in cache.events))
        self.assertEqual(len(list(cache.cache_directory(self.root).glob("v1-*.json"))), 1)
        self._renames("false")
        cache.events.clear()
        self._assert_same(self._through_cache(), oracle["false"])
        self.assertEqual(cache.events[0]["event"], "hit")

    def test_values_are_normalized_by_git_and_unreadable_values_refuse(self):
        observed = {}
        for value in ("true", "yes", "on", "1", "false", "no", "off", "0", None):
            self._renames(value)
            observed[value] = cache.replay_settings(self.root)
        self.assertEqual({observed[v]["diff.renames"] for v in ("true", "yes", "on", "1")}, {"true"})
        self.assertEqual({observed[v]["diff.renames"] for v in ("false", "no", "off", "0")}, {"false"})
        self.assertEqual(observed[None], {"diff.renames": "unset"})
        self._renames("on")
        self.store()
        self._renames("1")
        self.assertIsNotNone(self.load(), cache.events)
        self._renames("off")
        self.assertIsNone(self.load())
        self.assertEqual(self.last_reason(), "no cache file for this key")
        self._renames("copies")
        self.assertIsNone(cache.replay_settings(self.root))
        with self.assertRaises(cache._Skip):
            cache._git_settings(self.root)
        self.assertIsNone(self.load())
        # The value the replay's own commands inherit, including an include file.
        self._renames(None)
        include = self.root / ".artifacts" / "renames.gitconfig"
        include.parent.mkdir(exist_ok=True)
        include.write_text("[diff]\n\trenames = false\n")
        subprocess.run(["git", "config", "include.path", str(include)], cwd=self.root, check=True)
        self.assertEqual(cache.replay_settings(self.root), {"diff.renames": "false"})

    def test_store_refuses_settings_other_than_the_replays(self):
        self._renames("true")
        before = cache.replay_settings(self.root)
        self._renames("false")
        projection, progress = _oracle(self.root)
        with mock.patch.dict(os.environ, ON):
            for settings in (before, None):
                self.assertFalse(cache.store(self.root, projection, progress, set(), settings=settings,
                                             environment_ok=queue._publication_git_environment))
                self.assertEqual(self.last_reason(),
                                 "git settings changed or unreadable during the replay")
        self.assertFalse(list(cache.cache_directory(self.root).glob("v1-*.json")))
        # Through the real replay: a change between the snapshot and the store.
        with mock.patch.dict(os.environ, ON), \
                mock.patch.object(cache, "replay_settings", return_value=before):
            queue.projection_and_progress_for(self.root, "HEAD")
        self.assertEqual(self.last_reason(), "git settings changed or unreadable during the replay")
        self.assertFalse(list(cache.cache_directory(self.root).glob("v1-*.json")))


class RetentionAndConcurrencyTests(_Fixture):
    def test_concurrent_same_key_publication_is_atomic(self):
        projection, progress = _oracle(self.root)
        with reader.recording() as objects:
            queue._projection(self.root, "HEAD")
        results: list[bool] = []

        def publish():
            with mock.patch.dict(os.environ, ON):
                results.append(cache.store(self.root, projection, progress, set(objects),
                                           settings=cache.replay_settings(self.root),
                                           environment_ok=queue._publication_git_environment))

        # Environment is process-wide: set once, then publish concurrently.
        with mock.patch.dict(os.environ, ON):
            threads = [threading.Thread(target=publish) for _ in range(4)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(120)
        self.assertEqual(results, [True] * 4)
        self.assertEqual(len(list(cache.cache_directory(self.root).iterdir())), 1)
        hit = self.load()
        self.assertIsNotNone(hit)
        self.assert_equal_projection(hit[0], projection)

    def test_retention_keeps_three_commits_and_only_own_files(self):
        directory = cache.cache_directory(self.root)
        commits = []
        for index in range(4):
            (self.root / f"note-{index}.txt").write_text(str(index))
            commits.append(self.commit(f"note {index}"))
            self.store()
            if index == 0:
                directory.joinpath("unrelated.json").write_text("keep")
                directory.joinpath(f"v1-{'f' * 40}-{'0' * 32}.json.bak").write_text("keep")
                os.symlink(directory / "unrelated.json", directory / f"v1-{'e' * 40}-{'0' * 32}.json")
            time.sleep(0.01)
        names = sorted(path.name for path in directory.iterdir())
        kept = {name[3:43] for name in names if cache._NAME.fullmatch(name) and not (directory / name).is_symlink()}
        self.assertEqual(kept, set(commits[1:]))
        self.assertIn("unrelated.json", names)
        self.assertIn(f"v1-{'f' * 40}-{'0' * 32}.json.bak", names)
        self.assertTrue((directory / f"v1-{'e' * 40}-{'0' * 32}.json").is_symlink())

    def test_total_cap_evicts_oldest_but_never_the_new_file(self):
        directory = cache.cache_directory(self.root)
        self.store()
        first = self.cached_file()
        size = first.stat().st_size
        (self.root / "note.txt").write_text("x")
        self.commit("note")
        with mock.patch.object(cache, "MAX_TOTAL_BYTES", size + size // 2):
            self.store()
        remaining = [path for path in directory.iterdir() if cache._NAME.fullmatch(path.name)]
        self.assertEqual(len(remaining), 1)
        self.assertNotEqual(remaining[0].name, first.name)
        self.assertIsNotNone(self.load())

    def test_stale_temporary_files_are_removed_fresh_ones_kept(self):
        directory = cache.cache_directory(self.root)
        self.store()
        stale = directory / (cache._TEMP_PREFIX + "stale")
        fresh = directory / (cache._TEMP_PREFIX + "fresh")
        stale.write_text("x")
        fresh.write_text("y")
        old = time.time() - cache.STALE_TEMP_SECONDS - 10
        os.utime(stale, (old, old))
        cache._evict(directory, self.cached_file().name)
        self.assertFalse(stale.exists())
        self.assertTrue(fresh.exists())


class HarnessTests(_Fixture):
    def _run(self, mode: str, output: Path, *, check: bool = True) -> subprocess.CompletedProcess:
        environment = dict(os.environ)
        environment.pop(cache.MODE_ENV, None)
        return subprocess.run(
            [sys.executable, "-B", str(REPO / "tools/orchestration/benchmark_projection_cache.py"),
             "run", "--mode", mode, "--root", str(self.root), "--treeish", "HEAD",
             "--output", str(output), "--audit-opens"],
            check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment,
            cwd=REPO, timeout=300)

    def test_off_cold_warm_samples_are_identical_and_warm_needs_a_file(self):
        from tools.orchestration import benchmark_projection_cache as harness
        out = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, out, True)
        failed = self._run("warm", out / "warm-0.json", check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn(b"warm run needs a cache file", failed.stderr)
        self.assertFalse((out / "warm-0.json").exists())
        for mode in ("off", "cold", "warm"):
            self._run(mode, out / f"{mode}.json")
        samples = [json.loads((out / f"{mode}.json").read_text()) for mode in ("off", "cold", "warm")]
        self.assertEqual([sample["cache_events"] for sample in samples][0], [])
        self.assertEqual([event["event"] for event in samples[1]["cache_events"]], ["miss", "stored"])
        self.assertEqual([event["event"] for event in samples[2]["cache_events"]], ["hit"])
        oracle, oracle_progress = _oracle(self.root)
        self.assertEqual(samples[0]["identity"]["overrides_d"],
                         hashlib.sha256(repr(oracle[3]).encode()).hexdigest())
        self.assertEqual(samples[2]["progress"], oracle_progress)
        report = harness.compare(samples)
        for name in ("identity_identical", "progress_identical", "head_and_queue_unchanged",
                     "every_mode_sampled", "same_implementation_code_sha256"):
            self.assertTrue(report["checks"][name]["passed"], report["checks"][name])
        # The off run's audited opens stay inside code, rules and the interpreter.
        opened = samples[0]["opened_files"]
        self.assertIsInstance(opened, list)
        self.assertFalse([path for path in opened if path.startswith(str(self.root.resolve()))
                          and "/.artifacts/" not in path], opened)
        # Re-running into an existing output never overwrites it.
        again = self._run("off", out / "off.json", check=False)
        self.assertNotEqual(again.returncode, 0)

    def test_active_checkpoint_refuses_to_measure(self):
        checkpoint = queue.checkpoint_path(self.root)
        checkpoint.write_text("{}")
        out = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, out, True)
        result = self._run("off", out / "off.json", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"active queue checkpoint", result.stderr)


class TerminationProbeTests(unittest.TestCase):
    def test_symlink_loop_in_code_root_terminates_quickly(self):
        code = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, code, True)
        (code / "tools").mkdir()
        (code / "i18n" / "quality").mkdir(parents=True)
        (code / "tools" / "loop").symlink_to(code / "tools", target_is_directory=True)
        past = time.time() - 3600
        for path in code.rglob("*"):
            os.utime(path, (past, past), follow_symlinks=False)
        script = (f"import sys; sys.path.insert(0, {str(REPO)!r})\n"
                  "from pathlib import Path\n"
                  "from tools.i18nlib import projection_cache as c\n"
                  "try:\n"
                  f"    c.implementation_identity(Path({str(code)!r}))\n"
                  "except c._Skip as e:\n"
                  "    print(e)\n")
        output = subprocess.run([sys.executable, "-B", "-c", script], check=True, timeout=20,
                                stdout=subprocess.PIPE, text=True).stdout
        self.assertEqual(output.strip(), "code input contains a symlinked directory")


class ParentEnvironmentTests(unittest.TestCase):
    """A shell exporting the switch must not change what the fixtures test."""

    # Each failed under a parent ``I18N_PROJECTION_CACHE=on`` before the
    # fixtures pinned the production default: a setUp-time publication, or a
    # disk hit turning a counted replay into zero.
    SENSITIVE = (
        "tests.i18n.test_projection_cache.SwitchAndEntryTests.test_off_never_reads_writes_or_creates",
        "tests.i18n.test_repair_steps.RepairStepTests.test_two_preflights_match_standalone_bytes_and_replay_once",
        "tests.i18n.test_production_review_v2_lite_queue.ProjectionChainTests."
        "test_issue_chain_wrapper_projects_once_and_matches_separate_calls",
    )

    def test_pin_is_scoped_to_the_case_and_restores_the_parent(self):
        seen = []

        class Probe(unittest.TestCase):
            def setUp(inner):
                migration_tests.pin_projection_cache_default(inner)

            def runTest(inner):
                seen.append((os.environ.get(cache.MODE_ENV), os.environ.get(cache.TRACE_ENV)))

        with mock.patch.dict(os.environ, {cache.MODE_ENV: "on", cache.TRACE_ENV: "1"}):
            result = unittest.TestResult()
            Probe().run(result)
            self.assertTrue(result.wasSuccessful(), result.errors + result.failures)
            self.assertEqual(seen, [(None, None)])
            self.assertEqual(os.environ[cache.MODE_ENV], "on")
            self.assertEqual(os.environ[cache.TRACE_ENV], "1")

    def _parent_on(self, argv: list[str]) -> subprocess.CompletedProcess:
        environment = {**os.environ, cache.MODE_ENV: "on"}
        environment.pop(cache.TRACE_ENV, None)
        return subprocess.run([sys.executable, "-B", *argv], cwd=REPO, env=environment,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                              timeout=600)

    def test_direct_unittest_entry_under_parent_on(self):
        result = self._parent_on(["-m", "unittest", *self.SENSITIVE])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn(f"Ran {len(self.SENSITIVE)} tests", result.stdout)

    def test_test_groups_loader_entry_under_parent_on(self):
        # The registry loader and runner used by the gate, restricted to the
        # sensitive cases; the parent switch must be intact afterwards.
        script = (
            "import json, os, sys, unittest\n"
            "from pathlib import Path\n"
            "sys.path.insert(0, os.getcwd())\n"
            "from tools import test_groups as g\n"
            "config = g.validate_registry(Path.cwd(), json.loads(g.DEFAULT_CONFIG.read_text()))\n"
            "suite = g.load_group(config, 'production-shadow-surface-ledger')\n"
            "wanted = set(sys.argv[1:])\n"
            "cases = [case for case in g.test_cases(suite) if case.id() in wanted]\n"
            "assert len(cases) == len(wanted), cases\n"
            "ok = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(cases)).wasSuccessful()\n"
            f"print('PARENT', os.environ.get({cache.MODE_ENV!r}))\n"
            "sys.exit(0 if ok else 1)\n")
        result = self._parent_on(["-c", script, *self.SENSITIVE])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PARENT on", result.stdout)


def _edit(body: bytes, change) -> bytes:
    payload = json.loads(body)
    change(payload)
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


if __name__ == "__main__":
    unittest.main()
