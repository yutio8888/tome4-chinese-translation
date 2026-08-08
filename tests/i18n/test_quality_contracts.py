from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.errors import ValidationError
from i18nlib.quality_contracts import (
    ArtifactRef,
    canonical_json_bytes,
    canonical_sha256,
    make_provenance,
    relative_path,
    subject_identity,
    validate_locator,
    validate_provenance,
    validate_resource,
    validate_subject,
)


class CanonicalHashTests(unittest.TestCase):
    def test_canonical_bytes_sort_keys_and_compact(self):
        value = {"b": 1, "a": [2, 1], "c": {"y": 2, "x": 1}}
        encoded = canonical_json_bytes(value)
        self.assertEqual(json.loads(encoded), value)
        self.assertEqual(
            encoded, b'{"a":[2,1],"b":1,"c":{"x":1,"y":2}}'
        )

    def test_sha256_deterministic_and_order_independent(self):
        left = canonical_sha256({"b": 1, "a": "x"})
        right = canonical_sha256({"a": "x", "b": 1})
        self.assertEqual(left, right)
        self.assertEqual(len(left), 64)
        self.assertNotEqual(left, canonical_sha256({"b": 1, "a": "y"}))

    def test_unicode_round_trip(self):
        digest = canonical_sha256({"text": "魔化精灵\n\u4e2d"})
        self.assertEqual(len(digest), 64)


class PathSafetyTests(unittest.TestCase):
    def test_relative_path_accepts_repository_paths(self):
        self.assertEqual(relative_path("data/talents.lua", "p"), "data/talents.lua")

    def test_relative_path_rejects_absolute(self):
        with self.assertRaises(ValidationError):
            relative_path("/etc/passwd", "p")

    def test_relative_path_rejects_dotdot(self):
        with self.assertRaises(ValidationError):
            relative_path("../outside.lua", "p")

    def test_relative_path_rejects_line_suffix(self):
        # The file identity must never embed a :line locator.
        with self.assertRaises(ValidationError):
            relative_path("data/talents.lua:12", "p")


class ProvenanceTests(unittest.TestCase):
    def test_terminology_provenance_round_trip(self):
        value = make_provenance(
            kind="terminology",
            repository="terminology",
            revision="HEAD",
            logical_path="terminology.tsv",
            file_sha256="1" * 64,
            locator={"type": "term-row", "row": 42},
        )
        validated = validate_provenance(value, "provenance")
        self.assertEqual(validated["kind"], "terminology")
        self.assertEqual(validated["locator"]["row"], 42)

    def test_public_source_line_range(self):
        value = make_provenance(
            kind="public-source",
            repository="tome4-dlcs",
            revision="abc123",
            logical_path="data/talents.lua",
            file_sha256="2" * 64,
            locator={"type": "line-range", "start_line": 10, "end_line": 20},
        )
        self.assertEqual(validate_provenance(value, "p")["resource"]["revision"], "abc123")

    def test_context_key_locator(self):
        value = make_provenance(
            kind="versioned-context",
            repository="terminology",
            revision="HEAD",
            logical_path="terminology.tsv",
            file_sha256="3" * 64,
            locator={"type": "context-key", "key": "Doomelf", "value": "魔化精灵"},
        )
        validate_provenance(value, "p")

    def test_line_range_must_be_legal(self):
        with self.assertRaises(ValidationError):
            validate_locator({"type": "line-range", "start_line": 5, "end_line": 2}, "l")
        with self.assertRaises(ValidationError):
            validate_locator({"type": "line-range", "start_line": 0, "end_line": 1}, "l")

    def test_unknown_kind_rejected(self):
        with self.assertRaises(ValidationError):
            validate_provenance(
                {
                    "kind": "model-recall",
                    "resource": {"repository": "r", "revision": "v", "logical_path": "a.txt", "file_sha256": "0" * 64},
                    "locator": {"type": "context-key", "key": "k", "value": "v"},
                },
                "p",
            )

    def test_terminology_kind_requires_tsv(self):
        with self.assertRaises(ValidationError):
            make_provenance(
                kind="terminology",
                repository="terminology",
                revision="HEAD",
                logical_path="data/other.tsv",
                file_sha256="1" * 64,
                locator={"type": "term-row", "row": 1},
            )

    def test_resource_rejects_line_in_path(self):
        with self.assertRaises(ValidationError):
            validate_resource(
                {"repository": "r", "revision": "v", "logical_path": "a.lua:12", "file_sha256": "0" * 64},
                "resource",
            )


class SubjectIdentityTests(unittest.TestCase):
    def test_canonical_subject(self):
        subject = subject_identity(kind="canonical-revision", revision_id="a" * 64)
        self.assertEqual(subject["kind"], "canonical-revision")

    def test_controlled_mutation_subject(self):
        subject = subject_identity(
            kind="controlled-mutation",
            revision_id="a" * 64,
            variant_target="变体",
            mutation_kind="number-flip",
            digest="b" * 64,
        )
        self.assertEqual(subject["variant_target"], "变体")

    def test_controlled_mutation_requires_fields(self):
        with self.assertRaises(ValidationError):
            subject_identity(kind="controlled-mutation", revision_id="a" * 64)

    def test_canonical_rejects_mutation_fields(self):
        with self.assertRaises(ValidationError):
            subject_identity(
                kind="canonical-revision", revision_id="a" * 64, variant_target="x"
            )

    def test_validate_subject_round_trip(self):
        value = {"kind": "canonical-revision", "revision_id": "c" * 64}
        self.assertEqual(validate_subject(value), value)


class ArtifactRefTests(unittest.TestCase):
    def test_artifact_ref_identity_and_hash(self):
        ref = ArtifactRef(
            subject={"kind": "canonical-revision", "revision_id": "a" * 64},
            provenance=make_provenance(
                kind="public-source",
                repository="tome4",
                revision="deadbeef",
                logical_path="data/talents.lua",
                file_sha256="2" * 64,
                locator={"type": "line-range", "start_line": 1, "end_line": 3},
            ),
        )
        clone = ArtifactRef(
            subject={"kind": "canonical-revision", "revision_id": "a" * 64},
            provenance=make_provenance(
                kind="public-source",
                repository="tome4",
                revision="deadbeef",
                logical_path="data/talents.lua",
                file_sha256="2" * 64,
                locator={"type": "line-range", "start_line": 1, "end_line": 3},
            ),
        )
        self.assertEqual(ref, clone)
        self.assertEqual(ref.sha256(), clone.sha256())
        self.assertEqual(len(ref.sha256()), 64)
        different = ArtifactRef(
            subject={"kind": "canonical-revision", "revision_id": "b" * 64},
            provenance=make_provenance(
                kind="public-source",
                repository="tome4",
                revision="deadbeef",
                logical_path="data/talents.lua",
                file_sha256="2" * 64,
                locator={"type": "line-range", "start_line": 1, "end_line": 3},
            ),
        )
        self.assertNotEqual(ref, different)


if __name__ == "__main__":
    unittest.main()
