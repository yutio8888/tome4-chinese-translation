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
import surface_screen_result_check as check


def entry(index: int = 1, *, component: str = "tome", path: str = "mod.lua") -> dict[str, str]:
    return {
        "component": component,
        "normalized_path": path,
        "call_locator": f"section/{index}",
        "source_tag": f"tag-{index}",
        "source": f"Source {index}",
        "target": f"Target {index}",
    }


def payload(entries: list[dict[str, str]] | None = None) -> dict[str, object]:
    entries = entries if entries is not None else [entry(1)]
    return {
        "contract": "translation_surface_screen_v1",
        "entries": entries,
        "fixed_source_identity": "commit:" + "1" * 40,
        "terminology_snapshot": "术语",
        "rules_version": "surface-rules/1",
        "rendered_briefing": "briefing",
    }


def complete(entry_value: dict[str, str], scalars: dict[str, str]) -> dict[str, str]:
    value = dict(entry_value)
    value["logical_entry_identity"] = check.logical_entry_identity(
        component=value["component"], normalized_path=value["normalized_path"],
        call_locator=value["call_locator"], source_tag=value["source_tag"],
    )
    value["entry_revision_identity"] = check.entry_revision_identity(
        logical_entry_identity=value["logical_entry_identity"],
        source=value["source"], target=value["target"],
        fixed_source_identity=scalars["fixed_source_identity"],
        terminology_snapshot=scalars["terminology_snapshot"],
        rules_version=scalars["rules_version"],
    )
    return value


def ordered_payload(count: int) -> dict[str, object]:
    scalars = {
        "fixed_source_identity": "commit:" + "1" * 40,
        "terminology_snapshot": "术语",
        "rules_version": "surface-rules/1",
    }
    entries = [complete(entry(i), scalars) for i in range(1, count + 1)]
    entries.sort(key=lambda value: value["entry_revision_identity"])
    return payload(entries)


class SurfaceIdentityTests(unittest.TestCase):
    def test_rules_v1_recipe_is_frozen_and_rules_v2_omits_only_terminology(self):
        common = dict(logical_entry_identity="a" * 64, source="source", target="target",
                      fixed_source_identity="commit:" + "b" * 40)
        v1 = check.entry_revision_identity(
            **common, terminology_snapshot="terms-one",
            rules_version="production-review-v2-lite-rules-v1")
        historical = hashlib.sha256(check.canonical_bytes({
            "schema_version": 1, "logical_entry_identity": "a" * 64,
            "source_sha256": hashlib.sha256(b"source").hexdigest(),
            "target_sha256": hashlib.sha256(b"target").hexdigest(),
            "fixed_source_identity": "commit:" + "b" * 40,
            "terminology_snapshot_sha256": hashlib.sha256(b"terms-one").hexdigest(),
            "rules_version": "production-review-v2-lite-rules-v1",
        })).hexdigest()
        self.assertEqual(v1, historical)
        v2_one = check.entry_revision_identity(
            **common, terminology_snapshot="terms-one",
            rules_version=check.IDENTITY_RULES_V2)
        v2_two = check.entry_revision_identity(
            **common, terminology_snapshot="terms-two",
            rules_version=check.IDENTITY_RULES_V2)
        self.assertEqual(v2_one, v2_two)
        self.assertNotEqual(v1, v2_one)
        for field, value in (("source", "changed source"), ("target", "changed target"),
                             ("fixed_source_identity", "commit:" + "c" * 40),
                             ("logical_entry_identity", "d" * 64)):
            changed = dict(common); changed[field] = value
            self.assertNotEqual(v2_one, check.entry_revision_identity(
                **changed, terminology_snapshot="terms-two",
                rules_version=check.IDENTITY_RULES_V2))
        self.assertNotEqual(v2_one, check.entry_revision_identity(
            **common, terminology_snapshot="terms-two",
            rules_version="production-review-v2-lite-rules-v3"))

    def test_identity_recipe_vectors(self) -> None:
        logical = check.logical_entry_identity(
            component="tome", normalized_path="mod.lua",
            call_locator="section/1", source_tag="tag-1",
        )
        expected = hashlib.sha256(json.dumps(
            {"schema_version": 1, "component": "tome", "normalized_path": "mod.lua",
             "call_locator": "section/1", "source_tag": "tag-1"},
            ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")).hexdigest()
        self.assertEqual(logical, expected)
        revision = check.entry_revision_identity(
            logical_entry_identity=logical, source="S", target="T",
            fixed_source_identity="commit:" + "2" * 40,
            terminology_snapshot="术语", rules_version="r/1",
        )
        expected_revision = hashlib.sha256(json.dumps(
            {"schema_version": 1, "logical_entry_identity": logical,
             "source_sha256": hashlib.sha256(b"S").hexdigest(),
             "target_sha256": hashlib.sha256(b"T").hexdigest(),
             "fixed_source_identity": "commit:" + "2" * 40,
             "terminology_snapshot_sha256": hashlib.sha256("术语".encode()).hexdigest(),
             "rules_version": "r/1"},
            ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")).hexdigest()
        self.assertEqual(revision, expected_revision)

    def test_source_tag_change_moves_logical_identity_but_target_fix_does_not(self) -> None:
        base = check.logical_entry_identity(
            component="tome", normalized_path="mod.lua",
            call_locator="section/1", source_tag="tag-1",
        )
        retagged = check.logical_entry_identity(
            component="tome", normalized_path="mod.lua",
            call_locator="section/1", source_tag="tag-2",
        )
        self.assertNotEqual(base, retagged)
        scalars = {
            "fixed_source_identity": "commit:" + "1" * 40,
            "terminology_snapshot": "terms", "rules_version": "r/1",
        }
        first = check.entry_revision_identity(
            logical_entry_identity=base, source="S", target="T1", **scalars
        )
        fixed = check.entry_revision_identity(
            logical_entry_identity=base, source="S", target="T2", **scalars
        )
        self.assertNotEqual(first, fixed)

    def test_path_safety_and_call_locator_rules(self) -> None:
        for bad in ("", "/abs/lua", "a/../b.lua", "./a.lua", "a//b.lua", "a/b/", ".", "..", "a\\b.lua", "a\x00b"):
            with self.subTest(path=bad), self.assertRaises(check.ContractError):
                check.normalize_relative_path(bad)
        self.assertEqual(check.normalize_relative_path("lua/mod/tome.lua"), "lua/mod/tome.lua")
        for line_like in ("1", "123", "L12", "line 12", "line:12", "l#12", "LINE-12"):
            with self.subTest(locator=line_like):
                self.assertTrue(check.is_line_number_like(line_like))
        for stable in ("section/12", "talents.critical_strength.name", "call-0007"):
            self.assertFalse(check.is_line_number_like(stable))

    def test_call_locator_positive_grammar_and_line_forms(self) -> None:
        stable = [
            "a" * 64,
            "section/call-0001",
            "talents.critical_strength.name",
            "mod/newEntity/name",
            "newEntity.combat_talented",
            "section/sub/call_0009",
        ]
        for locator in stable:
            with self.subTest(locator=locator):
                self.assertEqual(check.validate_call_locator(locator), locator)
        rejected = [
            "", "1", "123", "L12", "line 12", "line:12", "l#12", "LINE-12",
            # file:line / raw-line embedded forms
            "mod.lua:120", "lua/mod.lua:9", "path:12:34", "section/:12",
            "section/L7", "foo/line-12", "calls/#42",
            # Not a stable token path at all
            "sp ace/1", "section//call", "section/call 1", "tls/证书/1",
            "plain-token", "...", "-", "a/./b",
        ]
        for locator in rejected:
            with self.subTest(locator=locator), self.assertRaises(check.ContractError):
                check.validate_call_locator(locator)
        # The payload validator uses the same positive grammar.
        scalars = {
            "fixed_source_identity": "commit:" + "1" * 40,
            "terminology_snapshot": "术语",
            "rules_version": "surface-rules/1",
        }
        with_line = complete(entry(1), scalars)
        with_line["call_locator"] = "lua/mod.lua:120"
        broken = payload([with_line])
        with self.assertRaises(check.ContractError):
            check.validate_payload(broken)

    def test_call_locator_rejects_path_prefixed_line_token(self) -> None:
        # C2-09: a call_locator formed as the entry normalized_path followed
        # by a numeric line token is a raw line form in disguise and fails
        # closed, while unrelated hierarchical numeric keys stay valid.
        scalars = {
            "fixed_source_identity": "commit:" + "1" * 40,
            "terminology_snapshot": "术语",
            "rules_version": "surface-rules/1",
        }
        for locator in (
            "mod.lua/42", "mod.lua.42", "mod.lua:42",
        ):
            with self.subTest(locator=locator):
                forged = entry(1)
                forged["call_locator"] = locator
                broken = payload([complete(forged, scalars)])
                with self.assertRaises(check.ContractError):
                    check.validate_payload(broken)
        # Legitimate hierarchical numeric keys unrelated to the entry path.
        for locator in ("3/2/1", "functions/3", "section/5.1.2", "index/2024/12"):
            with self.subTest(locator=locator):
                keyed = entry(1)
                keyed["call_locator"] = locator
                check.validate_payload(payload([complete(keyed, scalars)]))
        # The entry's own normalized_path participates: the same numeric
        # suffix under a different normalized_path remains acceptable.
        shifted = entry(1)
        shifted["normalized_path"] = "other/mod.lua"
        shifted["call_locator"] = "mod.lua/42"
        check.validate_payload(payload([complete(shifted, scalars)]))


class SurfacePayloadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scalars = {
            "fixed_source_identity": "commit:" + "1" * 40,
            "terminology_snapshot": "术语",
            "rules_version": "surface-rules/1",
        }
        entries = [complete(entry(i), self.scalars) for i in (1, 2)]
        entries.sort(key=lambda value: value["entry_revision_identity"])
        self.entries = entries
        self.payload = payload(entries)
        self.identity = hashlib.sha256(check.canonical_payload_bytes(self.payload)).hexdigest()

    def test_valid_payload_and_envelope(self) -> None:
        self.assertEqual(check.validate_payload(self.payload), self.payload)
        envelope = {"candidate_identity": self.identity, "payload": self.payload}
        validated, identity = check.validate_envelope(envelope)
        self.assertEqual(identity, self.identity)
        self.assertEqual(validated, self.payload)

    def test_rules_v2_payload_retains_exact_terminology_provenance(self) -> None:
        scalars = dict(self.scalars, rules_version=check.IDENTITY_RULES_V2)
        original = payload([complete(entry(1), scalars)])
        original.update(scalars)
        changed_scalars = dict(scalars, terminology_snapshot="其他术语")
        changed = payload([complete(entry(1), changed_scalars)])
        changed.update(changed_scalars)
        self.assertEqual(original["entries"][0]["entry_revision_identity"],
                         changed["entries"][0]["entry_revision_identity"])
        self.assertNotEqual(check.canonical_payload_bytes(original),
                            check.canonical_payload_bytes(changed))
        for value in (original, changed):
            identity = hashlib.sha256(check.canonical_payload_bytes(value)).hexdigest()
            check.validate_envelope({"candidate_identity": identity, "payload": value})

    def test_real_payload_and_envelope_consumers_reject_production_shadows(self) -> None:
        shadow_batch = {
            "schema_version": 1,
            "kind": "shadow_batch_draft_v1",
            "markers": {"authoritative": False, "dispatchable": False, "promotable": False},
            "shadow_batch_id": "a" * 64,
            "shadow_policy_id": "b" * 64,
        }
        with self.assertRaisesRegex(check.ContractError, "non-dispatchable"):
            check.validate_payload(shadow_batch)
        with self.assertRaisesRegex(check.ContractError, "non-dispatchable"):
            check.validate_envelope({"candidate_identity": "c" * 64, "payload": shadow_batch})
        shadow_policy = dict(shadow_batch, kind="shadow_queue_policy_v1")
        shadow_policy.pop("shadow_batch_id")
        with self.assertRaisesRegex(check.ContractError, "non-dispatchable"):
            check.validate_envelope(shadow_policy)

    def test_payload_negative_matrix(self) -> None:
        def fails(mutate) -> None:
            value = json.loads(json.dumps(self.payload))
            mutate(value)
            with self.assertRaises(check.ContractError):
                check.validate_payload(value)
        fails(lambda value: value.update(contract="translation_contextual_v2"))
        fails(lambda value: value.update(extra="x"))
        fails(lambda value: value.pop("rules_version"))
        fails(lambda value: value.update(rules_version=""))
        fails(lambda value: value.update(fixed_source_identity="commit:xyz"))
        fails(lambda value: value.update(fixed_source_identity="sha256:" + "1" * 64))
        fails(lambda value: value.update(entries=[]))
        fails(lambda value: value.update(rendered_briefing="briefing " + "a" * 64))
        fails(lambda value: value["entries"].reverse())
        fails(lambda value: value["entries"].append(dict(value["entries"][-1])))
        fails(lambda value: value["entries"][0].pop("logical_entry_identity"))
        # An identity mismatch fails closed even when the shape is correct.
        swapped = json.loads(json.dumps(self.payload))
        swapped["entries"][0]["entry_revision_identity"] = "0" * 64
        with self.assertRaises(check.ContractError):
            check.validate_payload(swapped)
        drift = json.loads(json.dumps(self.payload))
        drift["terminology_snapshot"] = "其他术语"
        with self.assertRaises(check.ContractError):
            check.validate_payload(drift)

    def test_result_validation(self) -> None:
        envelope = {"candidate_identity": self.identity, "payload": self.payload}
        results = [
            {"entry_revision_identity": self.entries[0]["entry_revision_identity"], "verdict": "OK"},
            {
                "entry_revision_identity": self.entries[1]["entry_revision_identity"],
                "verdict": "ISSUE", "observation": "占位符被破坏",
            },
        ]
        result = {
            "contract": "translation_surface_screen_v1",
            "candidate_identity": self.identity, "results": results,
        }
        self.assertEqual(check.validate_result(result, envelope), result)
        raw = check.canonical_bytes(result)
        self.assertEqual(check.validate_result_bytes(check.canonical_bytes(envelope), raw), result)
        pretty = json.dumps(result, ensure_ascii=False).encode("utf-8")
        with self.assertRaisesRegex(check.ContractError, "canonical compact"):
            check.validate_result_bytes(check.canonical_bytes(envelope), pretty)

    def test_result_negative_matrix(self) -> None:
        envelope = {"candidate_identity": self.identity, "payload": self.payload}
        ok_item = {"entry_revision_identity": self.entries[0]["entry_revision_identity"], "verdict": "OK"}
        issue_item = {
            "entry_revision_identity": self.entries[1]["entry_revision_identity"],
            "verdict": "ISSUE", "observation": "problem",
        }
        base = {
            "contract": "translation_surface_screen_v1",
            "candidate_identity": self.identity, "results": [ok_item, issue_item],
        }
        mutations = []
        wrong_identity = dict(base); wrong_identity["candidate_identity"] = "0" * 64; mutations.append(wrong_identity)
        truncated = dict(base); truncated["results"] = truncated["results"][:1]; mutations.append(truncated)
        duplicate = dict(base); duplicate["results"] = [ok_item, ok_item]; mutations.append(duplicate)
        reordered = dict(base); reordered["results"] = list(reversed(base["results"])); mutations.append(reordered)
        foreign = json.loads(json.dumps(base)); foreign["results"][0]["entry_revision_identity"] = "1" * 64; mutations.append(foreign)
        extra = dict(base); extra["severity"] = "high"; mutations.append(extra)
        bad_verdict = json.loads(json.dumps(base)); bad_verdict["results"][0]["verdict"] = "PASS"; mutations.append(bad_verdict)
        ok_with_observation = json.loads(json.dumps(base)); ok_with_observation["results"][0]["observation"] = "x"; mutations.append(ok_with_observation)
        empty_observation = json.loads(json.dumps(base)); empty_observation["results"][1]["observation"] = "  "; mutations.append(empty_observation)
        missing_observation = json.loads(json.dumps(base)); del missing_observation["results"][1]["observation"]; mutations.append(missing_observation)
        fix_suggestion = json.loads(json.dumps(base)); fix_suggestion["results"][1]["suggested_fix"] = "do x"; mutations.append(fix_suggestion)
        for value in mutations:
            with self.subTest(value=value), self.assertRaises(check.ContractError):
                check.validate_result(value, envelope)

    def test_strict_json_rejections(self) -> None:
        good = check.canonical_bytes(self.payload)
        invalid = [
            b"\xef\xbb\xbf" + good, good + b"\n", b"```json\n" + good + b"\n```",
            b'{"a":NaN}', b'{"a":Infinity}', b"\xff",
            b'{"contract":"translation_surface_screen_v1","contract":"x"}',
        ]
        for raw in invalid:
            with self.subTest(raw=raw[:16]), self.assertRaises((check.ContractError, check.InputError)):
                check.strict_json_bytes(raw, label="test")

    def test_prompt_template_budget(self) -> None:
        self.assertLessEqual(len(check.PROMPT_TEMPLATE.encode("utf-8")), 800)
        prompt = check.render_dispatch_prompt("a" * 64, ".ai/task/t/SURFACE-SCREEN-ENVELOPE-d.json")
        self.assertLessEqual(len(prompt.encode("utf-8")), 800)
        with self.assertRaises(check.ContractError):
            check.render_dispatch_prompt("SHORT", "path")


class SurfaceResultCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scalars = {
            "fixed_source_identity": "commit:" + "1" * 40,
            "terminology_snapshot": "术语",
            "rules_version": "surface-rules/1",
        }
        entries = [complete(entry(i), self.scalars) for i in (1, 2)]
        entries.sort(key=lambda value: value["entry_revision_identity"])
        self.payload = payload(entries)
        self.identity = hashlib.sha256(check.canonical_payload_bytes(self.payload)).hexdigest()
        self.envelope = {"candidate_identity": self.identity, "payload": self.payload}
        self.result = {
            "contract": "translation_surface_screen_v1",
            "candidate_identity": self.identity,
            "results": [
                {"entry_revision_identity": entries[0]["entry_revision_identity"], "verdict": "OK"},
                {"entry_revision_identity": entries[1]["entry_revision_identity"], "verdict": "OK"},
            ],
        }

    def test_cli_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            envelope = directory / "envelope.json"; raw = directory / "raw.txt"
            envelope.write_bytes(check.canonical_bytes(self.envelope))
            raw.write_bytes(check.canonical_bytes(self.result))
            command = [sys.executable, "-B", str(TOOLS / "surface_screen_result_check.py"), str(envelope), str(raw)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            raw.write_text("{}", encoding="utf-8")
            completed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 1)
            self.assertIn("RESULT_FAILED:", completed.stdout)
            raw.write_bytes(b"\xff")
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
            self.assertEqual(
                subprocess.run(command[:-1] + [str(directory / "missing")], capture_output=True).returncode, 2
            )

    def test_cli_real_consumer_rejects_shadow_envelope(self) -> None:
        shadow = {
            "schema_version": 1,
            "kind": "shadow_batch_draft_v1",
            "markers": {"authoritative": False, "dispatchable": False, "promotable": False},
            "shadow_batch_id": "a" * 64,
            "shadow_policy_id": "b" * 64,
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            envelope = directory / "envelope.json"
            raw = directory / "raw.txt"
            envelope.write_bytes(check.canonical_bytes(shadow))
            raw.write_bytes(b"{}")
            completed = subprocess.run(
                [sys.executable, "-B", str(TOOLS / "surface_screen_result_check.py"),
                 str(envelope), str(raw)], capture_output=True, text=True,
            )
            self.assertEqual(completed.returncode, 1)
            self.assertIn("non-dispatchable production shadow", completed.stdout)
            self.assertNotIn("Traceback", completed.stdout + completed.stderr)

    def test_cli_rejects_duplicate_json_keys_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            envelope = directory / "envelope.json"; raw = directory / "raw.txt"
            envelope.write_bytes(check.canonical_bytes(self.envelope))
            raw.write_bytes(
                b'{"contract":"translation_surface_screen_v1","contract":"translation_surface_screen_v1",'
                b'"candidate_identity":"' + self.identity.encode() + b'","results":[]}'
            )
            completed = subprocess.run(
                [sys.executable, "-B", str(TOOLS / "surface_screen_result_check.py"), str(envelope), str(raw)],
                capture_output=True, text=True,
            )
            self.assertEqual(completed.returncode, 1)
            self.assertIn("RESULT_FAILED:", completed.stdout)
            self.assertNotIn("Traceback", completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
