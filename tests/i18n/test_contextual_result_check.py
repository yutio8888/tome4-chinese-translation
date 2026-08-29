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
import contextual_result_check as check


def payload(keys: list[str] | None = None) -> dict[str, object]:
    keys = keys or ["r1", "r2"]
    return {
        "contract": "translation_contextual_v2",
        "ordered_revision_keys": keys,
        "translation_snapshot": [{"revision_key": key, "source": f"S {key}", "target": f"T {key}"} for key in keys],
        "fixed_source_identity": "commit:" + "1" * 40,
        "terminology_snapshot": "术语",
        "bounded_context": [{"revision_key": key, "context": f"C {key}"} for key in keys],
        "rendered_briefing": "briefing",
    }


class ContextualResultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = payload()
        self.identity = hashlib.sha256(check.canonical_payload_bytes(self.payload)).hexdigest()
        self.envelope = {"candidate_identity": self.identity, "payload": self.payload}
        self.result = {
            "contract": "translation_contextual_v2", "candidate_identity": self.identity,
            "verdicts": [
                {"revision_key": "r1", "verdict": "OK"},
                {"revision_key": "r2", "verdict": "ISSUE", "observation": "source-bound issue"},
            ],
        }

    def test_minimal_vector_and_valid_result(self) -> None:
        minimal = payload(["r1"])
        minimal.update({
            "translation_snapshot": [{"revision_key": "r1", "source": "Hello world", "target": "你好，世界"}],
            "fixed_source_identity": "commit:61bb370c33e46c4df4b2bbfd56113a0de1822300",
            "terminology_snapshot": "术语：zone=区域",
            "bounded_context": [{"revision_key": "r1", "context": "tag=talents/foo; nearby: A, B"}],
            "rendered_briefing": "有界语境审核 briefing：revision r1",
        })
        self.assertEqual(hashlib.sha256(check.canonical_payload_bytes(minimal)).hexdigest(), "fb95fa08bd65b4f626bb1b5f0f5a2035a72ef359d584cb088c30609f3fa94067")
        self.assertEqual(check.validate_result(self.result, self.envelope), self.result)

    def test_strict_json_rejections(self) -> None:
        good = json.dumps(self.result, ensure_ascii=False, separators=(",", ":")).encode()
        invalid = [
            b'{"contract":"translation_contextual_v2","contract":"translation_contextual_v2","candidate_identity":"' + self.identity.encode() + b'","verdicts":[]}',
            b"\xef\xbb\xbf" + good, good + b" prose", b"```json\n" + good + b"\n```",
            b'{"x":NaN}', b'{"x":Infinity}', b"\xff",
        ]
        for raw in invalid:
            with self.subTest(raw=raw[:20]), self.assertRaises((check.ContractError, check.InputError)):
                check.strict_json_bytes(raw, label="test")

    def test_result_schema_negative_matrix(self) -> None:
        mutations = []
        wrong_identity = dict(self.result); wrong_identity["candidate_identity"] = "0" * 64; mutations.append(wrong_identity)
        missing = dict(self.result); missing["verdicts"] = missing["verdicts"][:1]; mutations.append(missing)
        duplicate = dict(self.result); duplicate["verdicts"] = [self.result["verdicts"][0], self.result["verdicts"][0]]; mutations.append(duplicate)
        reordered = dict(self.result); reordered["verdicts"] = list(reversed(self.result["verdicts"])); mutations.append(reordered)
        foreign = json.loads(json.dumps(self.result)); foreign["verdicts"][0]["revision_key"] = "foreign"; mutations.append(foreign)
        extra = dict(self.result); extra["witness"] = "x"; mutations.append(extra)
        bad_verdict = json.loads(json.dumps(self.result)); bad_verdict["verdicts"][0]["verdict"] = "PASS"; mutations.append(bad_verdict)
        ok_observation = json.loads(json.dumps(self.result)); ok_observation["verdicts"][0]["observation"] = "x"; mutations.append(ok_observation)
        missing_observation = json.loads(json.dumps(self.result)); del missing_observation["verdicts"][1]["observation"]; mutations.append(missing_observation)
        empty_observation = json.loads(json.dumps(self.result)); empty_observation["verdicts"][1]["observation"] = " \n"; mutations.append(empty_observation)
        for value in mutations:
            with self.subTest(value=value), self.assertRaises(check.ContractError):
                check.validate_result(value, self.envelope)

    def test_cli_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            envelope = directory / "envelope.json"; raw = directory / "raw.txt"
            envelope.write_text(json.dumps(self.envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")
            raw.write_text(json.dumps(self.result, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            command = [sys.executable, "-B", str(TOOLS / "contextual_result_check.py"), str(envelope), str(raw)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            raw.write_text("{}", encoding="utf-8")
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
            raw.write_bytes(b"\xff")
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
            self.assertEqual(subprocess.run(command[:-1] + [str(directory / "missing")], capture_output=True).returncode, 2)

    def test_cli_rejects_lone_surrogate_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            envelope = directory / "envelope.json"
            raw = directory / "raw.txt"
            envelope.write_bytes(json.dumps(
                self.envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            ).encode("utf-8"))
            invalid = json.dumps(
                self.result, ensure_ascii=False, separators=(",", ":"),
            ).replace("source-bound issue", "\\ud800")
            raw.write_bytes(invalid.encode("utf-8"))
            completed = subprocess.run(
                [sys.executable, "-B", str(TOOLS / "contextual_result_check.py"), str(envelope), str(raw)],
                capture_output=True, text=True,
            )
            self.assertEqual(completed.returncode, 1)
            self.assertIn("RESULT_FAILED:", completed.stdout)
            self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_exact_compact_envelope_and_raw_bytes_are_required(self) -> None:
        envelope = json.dumps(
            self.envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        raw = json.dumps(self.result, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.assertEqual(check.validate_result_bytes(envelope, raw), self.result)
        pretty_envelope = json.dumps(self.envelope, ensure_ascii=False).encode("utf-8")
        with self.assertRaisesRegex(check.ContractError, "canonical compact"):
            check.validate_result_bytes(pretty_envelope, raw)
        pretty_raw = json.dumps(self.result, ensure_ascii=False).encode("utf-8")
        with self.assertRaisesRegex(check.ContractError, "compact JSON"):
            check.validate_result_bytes(envelope, pretty_raw)


if __name__ == "__main__":
    unittest.main()
