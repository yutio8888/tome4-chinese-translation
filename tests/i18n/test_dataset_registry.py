from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.dataset_registry import (
    build_registry_fragment,
    excluded_revision_ids,
    load_registry,
    validate_registry,
    validate_registry_fragment,
)
from i18nlib.errors import ValidationError
from i18nlib.quality_contracts import canonical_sha256


def make_entry(index: int = 0, revision_ids: list[str] | None = None) -> dict:
    revision_ids = revision_ids or [f"{index:064x}", f"{index + 1:064x}"]
    return {
        "dataset_id": f"dataset-{index}",
        "purpose": "facts-study-candidate-set",
        "status": "frozen",
        "sample_contract": "tome4-quality-facts-study-sample-v1",
        "sample_id": f"{index + 2:064x}",
        "sample_sha256": f"{index + 3:064x}",
        "sample_reference": None,
        "revision_ids": sorted(set(revision_ids)),
        "revision_ids_sha256": canonical_sha256(sorted(set(revision_ids))),
        "excluded_from_calibration": True,
        "excluded_from_holdout": True,
        "excluded_from_facts_curation": True,
        "scope": {"natural": len(revision_ids), "controlled": 0},
        "disposition": "test entry",
    }


def make_registry(entries: list[dict] | None = None) -> dict:
    entries = entries or [make_entry(0), make_entry(2)]
    value = {
        "contract": "tome4-quality-dataset-registry-v1",
        "schema_version": 1,
        "entries": entries,
        "registry_id": "",
    }
    value["registry_id"] = canonical_sha256(
        {"contract": value["contract"], "schema_version": 1, "entries": entries}
    )
    return value


class RegistryValidationTests(unittest.TestCase):
    def test_valid_registry_passes(self):
        registry = make_registry()
        self.assertEqual(validate_registry(registry)["registry_id"], registry["registry_id"])

    def test_duplicate_dataset_id_fails(self):
        registry = make_registry([make_entry(0), make_entry(0)])
        with self.assertRaises(ValidationError):
            validate_registry(registry)

    def test_duplicate_sample_id_fails(self):
        left = make_entry(0)
        right = make_entry(2)
        right["sample_id"] = left["sample_id"]
        with self.assertRaises(ValidationError):
            validate_registry(make_registry([left, right]))

    def test_overlapping_revision_sets_fail(self):
        left = make_entry(0)
        right = make_entry(2, revision_ids=[f"{1:064x}", f"{9:064x}"])
        with self.assertRaises(ValidationError):
            validate_registry(make_registry([left, right]))

    def test_digest_mismatch_fails(self):
        registry = make_registry()
        registry["entries"][0]["revision_ids_sha256"] = "0" * 64
        with self.assertRaises(ValidationError):
            validate_registry(registry)

    def test_unsorted_or_duplicate_revision_ids_fail(self):
        entry = make_entry(0)
        entry["revision_ids"] = [f"{1:064x}", f"{0:064x}"]
        with self.assertRaises(ValidationError):
            validate_registry(make_registry([entry]))

    def test_unknown_field_fails(self):
        registry = make_registry()
        registry["entries"][0]["extra"] = True
        with self.assertRaises(ValidationError):
            validate_registry(registry)

    def test_registry_id_not_canonical_fails(self):
        registry = make_registry()
        registry["registry_id"] = "1" * 64
        with self.assertRaises(ValidationError):
            validate_registry(registry)

    def test_sample_id_without_sha_fails(self):
        entry = make_entry(0)
        entry["sample_sha256"] = None
        with self.assertRaises(ValidationError):
            validate_registry(make_registry([entry]))

    def test_null_sample_id_requires_reference(self):
        entry = make_entry(0)
        entry["sample_id"] = None
        entry["sample_sha256"] = None
        with self.assertRaises(ValidationError):
            validate_registry(make_registry([entry]))
        entry["sample_reference"] = {
            "logical_path": "runs/x/manifest.json",
            "file_sha256": "a" * 64,
        }
        validate_registry(make_registry([entry]))

    def test_scope_must_be_positive_total(self):
        entry = make_entry(0)
        entry["scope"] = {"natural": 0, "controlled": 0}
        with self.assertRaises(ValidationError):
            validate_registry(make_registry([entry]))


class RegistryLoadTests(unittest.TestCase):
    def test_load_versioned_registry(self):
        manifest = SimpleNamespace(root=ROOT)
        registry = load_registry(manifest)
        ids = {entry["dataset_id"] for entry in registry["entries"]}
        self.assertIn("official-120-v1", ids)
        self.assertIn("calibration-32-v2", ids)
        self.assertIn("holdout-32-v2", ids)
        self.assertIn("exploratory-12-v1", ids)
        self.assertIn("facts-pilot-failed-v1", ids)
        self.assertIn("facts-random-candidates-v2", ids)
        self.assertIn("facts-long-source-candidates-v2", ids)
        self.assertIn("facts-long-source-discarded-v1", ids)
        total = sum(len(entry["revision_ids"]) for entry in registry["entries"])
        self.assertEqual(total, 276)

    def test_exclusion_union(self):
        registry = load_registry(SimpleNamespace(root=ROOT))
        excluded = excluded_revision_ids(registry, scopes=("facts-curation",))
        self.assertEqual(len(excluded), 276)
        calibration_only = excluded_revision_ids(registry, scopes=("calibration",))
        self.assertEqual(len(calibration_only), 276)

    def test_historical_exclusion_subset(self):
        registry = load_registry(SimpleNamespace(root=ROOT))
        pilot = next(e for e in registry["entries"] if e["dataset_id"] == "facts-pilot-failed-v1")
        historical = json.loads(
            (ROOT / "i18n" / "quality" / "facts-study-exclusions-v1.json").read_text()
        )
        registered = set(pilot["revision_ids"])
        for lineage in historical["lineages"]:
            self.assertTrue(set(lineage["revision_ids"]) <= registered)


class FragmentTests(unittest.TestCase):
    def test_fragment_round_trip(self):
        entry = make_entry(5)
        fragment = build_registry_fragment(entry)
        self.assertEqual(fragment["contract"], "tome4-quality-dataset-registry-fragment-v1")
        validated = validate_registry_fragment(fragment)
        self.assertEqual(validated["entry"], entry)

    def test_fragment_id_is_canonical(self):
        entry = make_entry(5)
        first = build_registry_fragment(entry)
        second = build_registry_fragment(copy.deepcopy(entry))
        self.assertEqual(first["fragment_id"], second["fragment_id"])
        self.assertEqual(
            first["fragment_id"],
            canonical_sha256(
                {"contract": "tome4-quality-dataset-registry-fragment-v1",
                 "schema_version": 1, "entry": entry}
            ),
        )

    def test_fragment_rejects_invalid_entry(self):
        entry = make_entry(5)
        entry["revision_ids_sha256"] = "0" * 64
        with self.assertRaises(ValidationError):
            build_registry_fragment(entry)


if __name__ == "__main__":
    unittest.main()
