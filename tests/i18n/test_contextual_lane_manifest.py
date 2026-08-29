from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import contextual_lane_manifest as lanes
import contextual_result_check as result_check


class LaneManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".artifacts" / "i18n")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        keys = [f"r{i}" for i in range(1, 11)]
        self.draft = {
            "contract": "translation_contextual_v2", "ordered_revision_keys": keys,
            "translation_snapshot": [{"revision_key": k, "source": f"S{k}", "target": f"T{k}"} for k in keys],
            "fixed_source_identity": "commit:" + "2" * 40, "terminology_snapshot": "terms",
            "bounded_context": [{"revision_key": k, "context": f"C{k}"} for k in keys],
            "rendered_briefing": "lane neutral",
        }
        self.manifest, self.envelopes = lanes.build_group(
            self.draft, task_id="task-1", group_id="group-1", review_phase="REVIEW",
            cycle=0, attempt=1, dispatch_ids=["lane-1", "lane-2", "lane-3", "lane-4"],
        )
        for relative, envelope in self.envelopes:
            path = self.root / relative; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(lanes.canonical_bytes(envelope))
        self.path = ".ai/task/task-1/CONTEXTUAL-LANE-GROUP-group-1.json"
        path = self.root / self.path; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(lanes.canonical_bytes(self.manifest))

    def test_partition_and_manifest(self) -> None:
        self.assertEqual(lanes.partition(10), [
            {"index": 1, "offset": 0, "length": 3}, {"index": 2, "offset": 3, "length": 3},
            {"index": 3, "offset": 6, "length": 2}, {"index": 4, "offset": 8, "length": 2},
        ])
        self.assertEqual(lanes.validate_manifest(self.manifest, root=self.root, manifest_path=self.path), self.manifest)
        with self.assertRaises(result_check.ContractError): lanes.partition(3)
        self.assertLessEqual(len(lanes.PROMPT_TEMPLATE.encode("utf-8")), 800)
        self.assertLessEqual(len(lanes.render_dispatch_prompt("0" * 64, ".ai/task/t/CONTEXTUAL-ENVELOPE-d.json").encode("utf-8")), 800)

    def test_payload_rendered_briefing_is_not_a_dispatch_prompt_budget(self) -> None:
        draft = json.loads(json.dumps(self.draft))
        draft["rendered_briefing"] = "语境" * 1000
        manifest, _ = lanes.build_group(
            draft, task_id="task-1", group_id="group-2", review_phase="REVIEW",
            cycle=0, attempt=1, dispatch_ids=["long-1", "long-2", "long-3", "long-4"],
        )
        self.assertEqual(manifest["payload"]["lane_count"], 4)

    def test_manifest_negative_matrix(self) -> None:
        def fails(mutate) -> None:
            value = json.loads(json.dumps(self.manifest))
            mutate(value)
            value["group_identity"] = __import__("hashlib").sha256(lanes.canonical_bytes(value["payload"])).hexdigest()
            with self.assertRaises((result_check.ContractError, result_check.InputError)):
                lanes.validate_manifest(value, root=self.root, manifest_path=self.path)
        fails(lambda value: value["payload"].update(task_id="wrong"))
        fails(lambda value: value["payload"].update(review_phase="FINAL_REVIEW"))
        fails(lambda value: value["payload"].update(attempt=0))
        fails(lambda value: value["payload"].update(lane_count=3))
        fails(lambda value: value["payload"]["lane_boundaries"][1].update(offset=4))
        fails(lambda value: value["payload"]["lanes"][0].update(dispatch_id="foreign"))
        fails(lambda value: value["payload"]["lanes"][0].update(input_path="../escape"))
        fails(lambda value: value["payload"]["lanes"][0].update(candidate_identity="0" * 64))
        envelope_path = self.root / self.envelopes[0][0]
        original = envelope_path.read_bytes()
        envelope = json.loads(original); envelope["payload"]["ordered_revision_keys"][0] = "drift"
        envelope_path.write_bytes(lanes.canonical_bytes(envelope))
        with self.assertRaises(result_check.ContractError):
            lanes.validate_manifest(self.manifest, root=self.root, manifest_path=self.path)
        envelope_path.write_bytes(original)

    def test_symlink_check_and_idempotent_write(self) -> None:
        target = self.root / "target"; target.write_bytes(b"x")
        link = self.root / "link"; link.symlink_to(target)
        with self.assertRaises(result_check.InputError): lanes._ordinary_file(self.root, "link", "test")
        output = self.root / "out"
        lanes._write_idempotent(output, b"same", root=self.root)
        lanes._write_idempotent(output, b"same", root=self.root)
        with self.assertRaises(result_check.InputError):
            lanes._write_idempotent(output, b"different", root=self.root)

    def test_public_check_rejects_noncanonical_lane_envelope_bytes(self) -> None:
        envelope_path = self.root / self.envelopes[0][0]
        envelope = self.envelopes[0][1]
        command = [
            sys.executable, "-B", str(TOOLS / "contextual_lane_manifest.py"),
            "check", self.path, "--root", str(self.root),
        ]
        for invalid in (
            json.dumps(envelope, ensure_ascii=False, indent=2).encode("utf-8"),
            lanes.canonical_bytes(envelope) + b"\n",
        ):
            with self.subTest(suffix=invalid[-1:]):
                envelope_path.write_bytes(invalid)
                completed = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(completed.returncode, 1)
                self.assertIn("MANIFEST_FAILED:", completed.stdout)
                self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_public_check_rejects_lone_surrogate_without_traceback(self) -> None:
        manifest_path = self.root / self.path
        manifest_path.write_bytes(
            manifest_path.read_bytes().replace(b'"terms"', b'"\\ud800"')
        )
        completed = subprocess.run(
            [
                sys.executable, "-B", str(TOOLS / "contextual_lane_manifest.py"),
                "check", self.path, "--root", str(self.root),
            ],
            capture_output=True, text=True,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertIn("MANIFEST_FAILED:", completed.stdout)
        self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_symlinked_publication_ancestor_is_rejected_before_write(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        ancestor = self.root / "linked"
        ancestor.symlink_to(outside, target_is_directory=True)
        destination = ancestor / "task" / "task-1" / "envelope.json"
        with self.assertRaisesRegex(result_check.InputError, "publication path traverses a symlink"):
            lanes._write_idempotent(destination, b"{}", root=self.root)
        self.assertFalse((outside / "task").exists())


if __name__ == "__main__":
    unittest.main()
