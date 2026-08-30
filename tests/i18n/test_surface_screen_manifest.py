from __future__ import annotations

import hashlib
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
import surface_screen_manifest as manifest
import surface_screen_result_check as check


SCALARS = {
    "fixed_source_identity": "commit:" + "3" * 40,
    "terminology_snapshot": "术语",
    "rules_version": "surface-rules/1",
}


def _entry(index: int) -> dict[str, str]:
    logical = check.logical_entry_identity(
        component="tome", normalized_path="lua/mod.lua",
        call_locator=f"section/call-{index:04d}", source_tag=f"tag-{index}",
    )
    return {
        "component": "tome", "normalized_path": "lua/mod.lua",
        "call_locator": f"section/call-{index:04d}", "source_tag": f"tag-{index}",
        "source": f"Source {index}", "target": f"Target {index}",
        "logical_entry_identity": logical,
        "entry_revision_identity": check.entry_revision_identity(
            logical_entry_identity=logical, source=f"Source {index}",
            target=f"Target {index}", **SCALARS,
        ),
    }


def draft(count: int) -> dict[str, object]:
    entries = sorted((_entry(i) for i in range(1, count + 1)), key=lambda e: e["entry_revision_identity"])
    return {"contract": check.CONTRACT, **SCALARS, "rendered_briefing": "lane neutral", "entries": entries}


class SurfaceManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".artifacts" / "i18n")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_batching_cardinality_boundaries(self) -> None:
        self.assertEqual(manifest.plan([])["action"], "no_dispatch")
        for count in (1, 2, 3):
            plan = manifest.plan(draft(count)["entries"])
            self.assertEqual(plan["action"], "full")
            self.assertEqual(plan["screen_count"], count)
        for count in (4, 5, 79, 80):
            plan = manifest.plan(draft(count)["entries"])
            self.assertEqual(plan["action"], "lanes")
            boundaries = plan["lane_boundaries"]
            self.assertEqual([b["length"] for b in boundaries], [
                count // 4 + (1 if count % 4 >= 1 else 0),
                count // 4 + (1 if count % 4 >= 2 else 0),
                count // 4 + (1 if count % 4 >= 3 else 0),
                count // 4,
            ])
            self.assertEqual(sum(b["length"] for b in boundaries), count)
            self.assertEqual([b["index"] for b in boundaries], [1, 2, 3, 4])
            offsets = [b["offset"] for b in boundaries]
            self.assertEqual(offsets, [0, boundaries[0]["length"],
                                       boundaries[0]["length"] + boundaries[1]["length"],
                                       boundaries[0]["length"] + boundaries[1]["length"] + boundaries[2]["length"]])
            for boundary in boundaries:
                self.assertGreater(boundary["length"], 0)
        over = manifest.plan(draft(100)["entries"])
        self.assertEqual(over["action"], "carry_over_required")
        self.assertEqual((over["screen_count"], over["carry_over_count"]), (80, 20))
        screen, carry = manifest.split_carry_over(draft(100)["entries"])
        self.assertEqual(len(screen), 80)
        self.assertEqual(len(carry), 20)
        self.assertEqual([e["entry_revision_identity"] for e in screen + carry],
                         [e["entry_revision_identity"] for e in draft(100)["entries"]])
        self.assertEqual(carry[0]["entry_revision_identity"], draft(100)["entries"][80]["entry_revision_identity"])

    def test_partition_rejects_out_of_band_counts(self) -> None:
        for count in (0, 1, 3, 81, 100):
            with self.subTest(count=count), self.assertRaises(check.ContractError):
                manifest.partition(count)

    def test_surface_group_phase_only_allows_review(self) -> None:
        # C2-07: surface manifest/group artifacts allow only REVIEW; fresh
        # retries increase attempt and use fresh IDs, never RE_REVIEW.
        self.assertEqual(manifest.PHASES, frozenset({"REVIEW"}))
        with self.assertRaises(check.ContractError) as caught:
            manifest.build_group(
                draft(5), task_id="task-1", group_id="group-re",
                review_phase="RE_REVIEW", cycle=0, attempt=1,
                dispatch_ids=[f"lane-{index}" for index in range(1, 5)],
            )
        self.assertIn("REVIEW", str(caught.exception))
        # The CLI no longer offers RE_REVIEW as a phase choice.
        completed = subprocess.run([
            sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
            "build", "--help",
        ], capture_output=True, text=True)
        self.assertNotIn("RE_REVIEW", completed.stdout)

    def test_build_full_and_group_produce_verifiable_artifacts(self) -> None:
        full_payload = draft(2)
        envelope, path, _ = manifest.build_full(
            full_payload, task_id="task-1", dispatch_id="full-1",
        )
        identity = hashlib.sha256(check.canonical_payload_bytes(full_payload)).hexdigest()
        self.assertEqual(envelope["candidate_identity"], identity)
        self.assertEqual(path, ".ai/task/task-1/SURFACE-SCREEN-ENVELOPE-full-1.json")
        group_payload = draft(6)
        group, group_path, envelopes = manifest.build_group(
            group_payload, task_id="task-1", group_id="group-1", review_phase="REVIEW",
            cycle=0, attempt=1, dispatch_ids=["lane-1", "lane-2", "lane-3", "lane-4"],
        )
        self.assertEqual(group_path, ".ai/task/task-1/SURFACE-SCREEN-GROUP-group-1.json")
        union = []
        for boundary in group["payload"]["lane_boundaries"]:
            start, end = boundary["offset"], boundary["offset"] + boundary["length"]
            union.extend(group["payload"]["workset"]["entries"][start:end])
        self.assertEqual([e["entry_revision_identity"] for e in union],
                         [e["entry_revision_identity"] for e in group_payload["entries"]])
        for relative, lane_envelope in envelopes:
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
            (self.root / relative).write_bytes(check.canonical_bytes(lane_envelope))
        (self.root / group_path).parent.mkdir(parents=True, exist_ok=True)
        (self.root / group_path).write_bytes(check.canonical_bytes(group))
        self.assertEqual(
            manifest.validate_group_manifest(group, root=self.root, manifest_path=group_path), group
        )

    def test_build_full_writes_and_group_negative_matrix(self) -> None:
        group, group_path, envelopes = manifest.build_group(
            draft(5), task_id="task-1", group_id="group-1", review_phase="REVIEW",
            cycle=1, attempt=2, dispatch_ids=["lane-1", "lane-2", "lane-3", "lane-4"],
        )
        for relative, envelope in envelopes:
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
            (self.root / relative).write_bytes(check.canonical_bytes(envelope))
        (self.root / group_path).parent.mkdir(parents=True, exist_ok=True)
        (self.root / group_path).write_bytes(check.canonical_bytes(group))

        def fails(mutate) -> None:
            value = json.loads(json.dumps(group))
            mutate(value)
            value["group_identity"] = hashlib.sha256(check.canonical_bytes(value["payload"])).hexdigest()
            with self.assertRaises((check.ContractError, check.InputError)):
                manifest.validate_group_manifest(value, root=self.root, manifest_path=group_path)
        fails(lambda value: value["payload"].update(task_id="wrong"))
        fails(lambda value: value["payload"].update(review_phase="FINAL_REVIEW"))
        fails(lambda value: value["payload"].update(lane_count=3))
        fails(lambda value: value["payload"]["lane_boundaries"][1].update(offset=1))
        fails(lambda value: value["payload"]["lanes"][0].update(dispatch_id="foreign"))
        fails(lambda value: value["payload"]["lanes"][0].update(input_path="../escape"))
        fails(lambda value: value["payload"]["lanes"][0].update(candidate_identity="0" * 64))
        fails(lambda value: value["payload"]["workset"]["entries"].pop())
        fails(lambda value: value["payload"]["workset"].update(rendered_briefing="drifted"))
        fails(lambda value: value["payload"].pop("attempt"))
        # Envelope byte drift fails closed.
        envelope_path = self.root / envelopes[0][0]
        original = envelope_path.read_bytes()
        envelope = json.loads(original)
        envelope["payload"]["entries"][0]["source"] = "drifted"
        envelope_path.write_bytes(check.canonical_bytes(envelope))
        with self.assertRaises(check.ContractError):
            manifest.validate_group_manifest(group, root=self.root, manifest_path=group_path)
        envelope_path.write_bytes(original)

    def test_build_cli_zero_records_no_dispatch_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            draft_path = Path(temporary) / "draft.json"
            draft_path.write_bytes(check.canonical_bytes(draft(0)))
            # C2-03: the n=0 build must declare no dispatch inputs at all.
            completed = subprocess.run([
                sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                "build", str(draft_path), "--task-id", "task-1",
                "--root", temporary,
            ], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0)
            self.assertIn("ZERO_RECORDED .ai/task/task-1/SURFACE-SCREEN-ZERO.json", completed.stdout)
            artifact = Path(temporary) / ".ai" / "task" / "task-1" / "SURFACE-SCREEN-ZERO.json"
            self.assertTrue(artifact.is_file())
            payload = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertEqual(
                payload,
                manifest.build_zero_payload(task_id="task-1"),
            )
            self.assertEqual(payload["algorithm"], "surface-zero-workset/1")
            self.assertEqual(
                payload["workset_identity"],
                manifest.build_zero_workset_identity(),
            )
            # No dispatch envelope or group manifest may exist for n=0.
            task_dir = Path(temporary) / ".ai" / "task" / "task-1"
            self.assertEqual(
                sorted(item.name for item in task_dir.iterdir()),
                ["SURFACE-SCREEN-ZERO.json"],
            )
            # Any dispatch/group/cycle/attempt input fails closed for n=0.
            for extra in (
                ["--dispatch-id", "d1"], ["--group-id", "g1"],
                ["--cycle", "0"], ["--attempt", "1"],
            ):
                rejected = subprocess.run([
                    sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                    "build", str(draft_path), "--task-id", "task-1", *extra,
                    "--root", temporary,
                ], capture_output=True, text=True)
                self.assertNotEqual(rejected.returncode, 0)
                self.assertIn("must not declare dispatch inputs", rejected.stdout)
            # Idempotent re-run keeps identical bytes.
            rerun = subprocess.run([
                sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                "build", str(draft_path), "--task-id", "task-1",
                "--root", temporary,
            ], capture_output=True, text=True)
            self.assertEqual(rerun.returncode, 0)
            verified = subprocess.run([
                sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                "check-zero", ".ai/task/task-1/SURFACE-SCREEN-ZERO.json",
                "--root", temporary,
            ], capture_output=True, text=True)
            self.assertEqual(verified.returncode, 0)
            self.assertIn("ZERO_VERIFIED", verified.stdout)
            self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_zero_payload_rejects_drift_and_foreign_shapes(self) -> None:
        good = manifest.build_zero_payload(task_id="task-1")
        self.assertEqual(manifest.validate_zero_payload(good), good)
        bad_shapes = []
        drifted = dict(good); drifted["proves_no_surface_dispatch"] = False
        bad_shapes.append(drifted)
        counted = dict(good); counted["screen_count"] = 1
        bad_shapes.append(counted)
        free_text = dict(good); free_text["reason"] = "felt empty"
        bad_shapes.append(free_text)
        provider = dict(good); provider["provider"] = "x"
        bad_shapes.append(provider)
        unbound = dict(good); unbound["task_id"] = "../escape"
        bad_shapes.append(unbound)
        tampered_workset = dict(good); tampered_workset["workset_identity"] = "0" * 64
        bad_shapes.append(tampered_workset)
        wrong_algorithm = dict(good); wrong_algorithm["algorithm"] = "surface-zero-workset/2"
        bad_shapes.append(wrong_algorithm)
        dropped_workset = {
            key: value for key, value in good.items() if key != "workset_identity"
        }
        bad_shapes.append(dropped_workset)
        for value in bad_shapes:
            with self.subTest(value=value), self.assertRaises(check.ContractError):
                manifest.validate_zero_payload(value)

    def test_build_cli_overflow_records_pre_manifest_carry_over(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            draft_path = Path(temporary) / "draft.json"
            big = draft(101)
            draft_path.write_bytes(check.canonical_bytes(big))
            completed = subprocess.run([
                sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                "build", str(draft_path), "--task-id", "task-1", "--group-id", "g1",
                "--cycle", "0", "--attempt", "1",
                "--dispatch-id", "d1", "--dispatch-id", "d2",
                "--dispatch-id", "d3", "--dispatch-id", "d4",
                "--root", temporary,
            ], capture_output=True, text=True)
            # n>80 still fails closed for manifest construction...
            self.assertEqual(completed.returncode, 1)
            self.assertIn("MANIFEST_FAILED:", completed.stdout)
            # ...but the canonical pre-manifest carry-over artifact is persisted.
            self.assertIn(
                "CARRY_OVER_REQUIRED .ai/task/task-1/SURFACE-SCREEN-CARRY-OVER.json",
                completed.stdout,
            )
            relative = ".ai/task/task-1/SURFACE-SCREEN-CARRY-OVER.json"
            artifact = Path(temporary) / relative
            self.assertTrue(artifact.is_file())
            payload = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertEqual(payload["algorithm"], "surface-carry-over/1")
            self.assertEqual(
                (payload["original_count"], payload["screen_count"], payload["carry_over_count"]),
                (101, 80, 21),
            )
            expected_keys = [
                entry["entry_revision_identity"] for entry in big["entries"]
            ]
            self.assertEqual(
                payload["ordered_screen_entry_revision_identities"]
                + payload["ordered_carry_over_entry_revision_identities"],
                expected_keys,
            )
            verified = subprocess.run([
                sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                "check-carry-over", relative, "--draft", str(draft_path),
                "--root", temporary,
            ], capture_output=True, text=True)
            self.assertEqual(verified.returncode, 0)
            self.assertIn("CARRY_OVER_VERIFIED", verified.stdout)
            self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_carry_over_payload_negative_matrix(self) -> None:
        big = draft(85)
        good = manifest.build_carry_over_payload(big, task_id="task-1")
        self.assertEqual(
            manifest.validate_carry_over_payload(good, entries=big["entries"]), good
        )
        # n<=80 must never claim a carry-over.
        with self.assertRaises(check.ContractError):
            manifest.build_carry_over_payload(draft(80), task_id="task-1")
        mutations = []
        algorithm = dict(good); algorithm["algorithm"] = "mystery/0"
        mutations.append(algorithm)
        lost = json.loads(json.dumps(good)); lost["carry_over_count"] = 4
        lost["ordered_carry_over_entry_revision_identities"].pop()
        mutations.append(lost)
        swapped = json.loads(json.dumps(good))
        swapped["ordered_screen_entry_revision_identities"].reverse()
        mutations.append(swapped)
        overlap = json.loads(json.dumps(good))
        overlap["ordered_carry_over_entry_revision_identities"][0] = \
            overlap["ordered_screen_entry_revision_identities"][0]
        mutations.append(overlap)
        tiny = json.loads(json.dumps(good)); tiny["screen_count"] = 79
        mutations.append(tiny)
        for value in mutations:
            with self.subTest(value=value), self.assertRaises(check.ContractError):
                manifest.validate_carry_over_payload(value, entries=big["entries"])
        # A workset drift also fails against the frozen original ordering.
        drifted = draft(85)
        for entry in drifted["entries"]:
            entry["source"] = entry["source"] + " drifted"
        for entry in drifted["entries"]:
            entry["entry_revision_identity"] = check.entry_revision_identity(
                logical_entry_identity=entry["logical_entry_identity"],
                source=entry["source"], target=entry["target"],
                fixed_source_identity=SCALARS["fixed_source_identity"],
                terminology_snapshot=SCALARS["terminology_snapshot"],
                rules_version=SCALARS["rules_version"],
            )
        drifted["entries"].sort(key=lambda entry: entry["entry_revision_identity"])
        with self.assertRaises(check.ContractError):
            manifest.validate_carry_over_payload(good, entries=drifted["entries"])

    def test_plan_and_check_cli(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            draft_path = Path(temporary) / "draft.json"
            draft_path.write_bytes(check.canonical_bytes(draft(5)))
            plan = subprocess.run([
                sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                "plan", str(draft_path),
            ], capture_output=True, text=True)
            self.assertEqual(plan.returncode, 0)
            self.assertIn('"action":"lanes"', plan.stdout)
            group, group_path, envelopes = manifest.build_group(
                draft(5), task_id="task-1", group_id="group-1", review_phase="REVIEW",
                cycle=0, attempt=1, dispatch_ids=["lane-1", "lane-2", "lane-3", "lane-4"],
            )
            task_dir = Path(temporary) / ".ai" / "task" / "task-1"
            task_dir.mkdir(parents=True)
            for relative, envelope in envelopes:
                (Path(temporary) / relative).write_bytes(check.canonical_bytes(envelope))
            (Path(temporary) / group_path).write_bytes(check.canonical_bytes(group))
            verified = subprocess.run([
                sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                "check", group_path, "--root", temporary,
            ], capture_output=True, text=True)
            self.assertEqual(verified.returncode, 0)
            self.assertIn("MANIFEST_VERIFIED", verified.stdout)

    def test_noncanonical_manifest_bytes_are_rejected(self) -> None:
        group, group_path, envelopes = manifest.build_group(
            draft(4), task_id="task-1", group_id="group-1", review_phase="REVIEW",
            cycle=0, attempt=1, dispatch_ids=["lane-1", "lane-2", "lane-3", "lane-4"],
        )
        for relative, envelope in envelopes:
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
            (self.root / relative).write_bytes(check.canonical_bytes(envelope))
        manifest_file = self.root / group_path
        manifest_file.parent.mkdir(parents=True, exist_ok=True)
        manifest_file.write_bytes(
            json.dumps(group, ensure_ascii=False, indent=2).encode("utf-8")
        )
        completed = subprocess.run([
            sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
            "check", group_path, "--root", str(self.root),
        ], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 1)
        self.assertIn("MANIFEST_FAILED:", completed.stdout)

    def test_non_object_draft_entry_and_failing_manifest_path(self) -> None:
        # CF-16: a non-object draft entry is rejected with the tool taxonomy
        # and without a traceback; lane-level manifest failures report the
        # actual failing lane manifest path.
        with tempfile.TemporaryDirectory() as temporary:
            draft_path = Path(temporary) / "draft.json"
            payload = draft(2)
            payload["entries"][1] = "not an object"
            draft_path.write_bytes(check.canonical_bytes(payload))
            completed = subprocess.run([
                sys.executable, "-B", str(TOOLS / "surface_screen_manifest.py"),
                "plan", str(draft_path),
            ], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 1)
            self.assertIn("MANIFEST_FAILED:", completed.stdout)
            self.assertIn("tool taxonomy", completed.stdout)
            self.assertNotIn("Traceback", completed.stdout + completed.stderr)
        group, group_path, envelopes = manifest.build_group(
            draft(5), task_id="task-1", group_id="group-1", review_phase="REVIEW",
            cycle=0, attempt=1, dispatch_ids=["lane-1", "lane-2", "lane-3", "lane-4"],
        )
        for relative, envelope in envelopes:
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
            (self.root / relative).write_bytes(check.canonical_bytes(envelope))
        drifted = json.loads(json.dumps(group))
        drifted["payload"]["lanes"][1]["candidate_identity"] = "0" * 64
        drifted["group_identity"] = hashlib.sha256(
            check.canonical_bytes(drifted["payload"])
        ).hexdigest()
        with self.assertRaisesRegex(
            check.ContractError, group_path.replace(".", r"\.")
        ):
            manifest.validate_group_manifest(drifted, root=self.root, manifest_path=group_path)

    def test_symlink_and_idempotent_publication(self) -> None:
        target = self.root / "target"; target.write_bytes(b"x")
        link = self.root / "link"; link.symlink_to(target)
        with self.assertRaises(check.InputError):
            manifest._ordinary_file(self.root, "link", "test")
        output = self.root / "out"
        manifest._write_idempotent(output, b"same", root=self.root)
        manifest._write_idempotent(output, b"same", root=self.root)
        with self.assertRaises(check.InputError):
            manifest._write_idempotent(output, b"different", root=self.root)
        outside = self.root / "outside"; outside.mkdir()
        ancestor = self.root / "linked"; ancestor.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(check.InputError, "publication path traverses a symlink"):
            manifest._write_idempotent(ancestor / "task" / "envelope.json", b"{}", root=self.root)
        self.assertFalse((outside / "task").exists())


if __name__ == "__main__":
    unittest.main()
