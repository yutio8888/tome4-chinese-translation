"""Toolchain tests: quality sampling."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import TEST_FIXTURE_ROOT
import copy
from dataclasses import replace
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
import i18nlib.quality as quality_module
from i18nlib import TOOL_VERSION
from i18nlib.config import Manifest, load_manifest
from i18nlib.errors import ValidationError
from i18nlib.lint import load_policy
from i18nlib.locale_model import LocaleDocument, LocaleLoader
from i18nlib.quality import (
    SAMPLE_CONTRACT,
    build_inventory,
    compute_revision_id,
    compute_revision_uid,
    compute_tu_uid,
    compute_unit_id,
    generate_dry_run,
    generate_sample,
    load_quality_policy,
    load_taxonomy,
    structure_signature,
)
from i18nlib.runtime import LuaRuntime


class QualitySampleOptionPreflightTests(unittest.TestCase):
    """Official sample options fail before rules, inventory, or artifacts."""

    manifest = SimpleNamespace(root=Path("/fixture-root"), raw_bytes=b"fixture")
    inventory_path = Path("unused-inventory.jsonl")

    @staticmethod
    def _policy() -> dict[str, object]:
        return {
            "pilot": {
                "buckets": {
                    "representative": 2,
                    "risk-enriched": 1,
                    "contrast": 1,
                },
                "seed": "policy-default-seed",
                "evaluator_ids": ["reviewer-a", "reviewer-b"],
                "method_version": "fixture-method-v1",
            }
        }

    @staticmethod
    def _sample(seed: str) -> dict[str, object]:
        return {
            "schema_version": 1,
            "quality_contract": SAMPLE_CONTRACT,
            "sample_id": "a" * 64,
            "items_sha256": "c" * 64,
            "seed": seed,
            "size": 4,
            "bucket_counts": {},
            "unmet_constraints": [],
            "coverage": {},
            "items": [{"revision_id": "b" * 64}],
        }

    def _assert_rejected_without_io(
        self,
        function: object,
        *,
        expected_message: str,
        **options: object,
    ) -> None:
        with (
            patch.object(quality_module, "load_quality_policy") as load_policy,
            patch.object(quality_module, "load_taxonomy") as load_taxonomy_mock,
            patch.object(quality_module, "read_inventory_file") as read_inventory,
            patch.object(
                quality_module, "_generate_sample_from_inventory"
            ) as generate_from_inventory,
            patch.object(
                quality_module, "create_quality_run_directory"
            ) as create_run_directory,
            patch.object(quality_module, "write_json") as write_json_mock,
        ):
            with self.assertRaisesRegex(ValidationError, expected_message):
                function(self.manifest, self.inventory_path, **options)

        for mocked in (
            load_policy,
            load_taxonomy_mock,
            read_inventory,
            generate_from_inventory,
            create_run_directory,
            write_json_mock,
        ):
            mocked.assert_not_called()

    def test_invalid_size_shapes_fail_without_io_for_public_paths(self) -> None:
        for function in (quality_module.generate_sample, quality_module.run_sample):
            for invalid_size in (True, 120.0, "120", 0, -1):
                with self.subTest(
                    function=function.__name__, size=invalid_size
                ):
                    self._assert_rejected_without_io(
                        function,
                        expected_message="pilot sample size must be an integer >= 1",
                        size=invalid_size,
                    )

    def test_invalid_seed_shapes_fail_without_io_for_public_paths(self) -> None:
        for function in (quality_module.generate_sample, quality_module.run_sample):
            for invalid_seed in (True, 1, 1.5, b"seed", ""):
                with self.subTest(
                    function=function.__name__, seed=invalid_seed
                ):
                    self._assert_rejected_without_io(
                        function,
                        expected_message="pilot sample seed must be a non-empty string",
                        seed=invalid_seed,
                    )

    def test_policy_size_mismatch_fails_before_later_io(self) -> None:
        for function in (quality_module.generate_sample, quality_module.run_sample):
            with self.subTest(function=function.__name__):
                policy = self._policy()
                with (
                    patch.object(
                        quality_module,
                        "load_quality_policy",
                        return_value=policy,
                    ) as load_policy,
                    patch.object(
                        quality_module, "load_taxonomy"
                    ) as load_taxonomy_mock,
                    patch.object(
                        quality_module, "read_inventory_file"
                    ) as read_inventory,
                    patch.object(
                        quality_module, "_generate_sample_from_inventory"
                    ) as generate_from_inventory,
                    patch.object(
                        quality_module, "create_quality_run_directory"
                    ) as create_run_directory,
                    patch.object(quality_module, "write_json") as write_json_mock,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"pilot sample size must be 4 for policy-v1 \(got 3\)",
                    ):
                        function(
                            self.manifest,
                            self.inventory_path,
                            size=3,
                            seed="fixture-seed",
                        )

                load_policy.assert_called_once_with(self.manifest)
                for mocked in (
                    load_taxonomy_mock,
                    read_inventory,
                    generate_from_inventory,
                    create_run_directory,
                    write_json_mock,
                ):
                    mocked.assert_not_called()

    def test_generate_sample_preserves_valid_default_and_exact_options(self) -> None:
        cases = (
            ({}, None, None, "policy-default-seed"),
            (
                {"size": 4, "seed": "explicit-seed"},
                4,
                "explicit-seed",
                "explicit-seed",
            ),
        )
        for options, expected_size, expected_seed, sample_seed in cases:
            with self.subTest(options=options):
                policy = self._policy()
                taxonomy = {"contract": "fixture-taxonomy"}
                entries: list[dict[str, object]] = []
                inventory_info = {"inventory_sha256": "c" * 64}
                sample = self._sample(sample_seed)
                with (
                    patch.object(
                        quality_module,
                        "load_quality_policy",
                        return_value=policy,
                    ) as load_policy,
                    patch.object(
                        quality_module,
                        "load_taxonomy",
                        return_value=taxonomy,
                    ) as load_taxonomy_mock,
                    patch.object(
                        quality_module,
                        "_load_inventory_bundle",
                        return_value=(entries, inventory_info),
                    ) as load_inventory_bundle,
                    patch.object(
                        quality_module,
                        "_generate_sample_from_inventory",
                        return_value=sample,
                    ) as generate_from_inventory,
                ):
                    result = quality_module.generate_sample(
                        self.manifest, self.inventory_path, **options
                    )

                self.assertIs(result, sample)
                load_policy.assert_called_once_with(self.manifest)
                load_taxonomy_mock.assert_called_once_with(self.manifest)
                load_inventory_bundle.assert_called_once_with(
                    self.manifest,
                    self.inventory_path,
                    taxonomy,
                    policy,
                )
                generate_from_inventory.assert_called_once_with(
                    self.manifest,
                    entries=entries,
                    inventory_info=inventory_info,
                    taxonomy=taxonomy,
                    qpolicy=policy,
                    size=expected_size,
                    seed=expected_seed,
                )

    def test_run_sample_loads_valid_inputs_once(self) -> None:
        cases = (
            ({}, None, None, "policy-default-seed"),
            (
                {"size": 4, "seed": "explicit-seed"},
                4,
                "explicit-seed",
                "explicit-seed",
            ),
        )
        run_directory = (
            self.manifest.root
            / ".artifacts"
            / "i18n"
            / "quality"
            / "runs"
            / "fixture-sample"
        )
        for options, expected_size, expected_seed, sample_seed in cases:
            with self.subTest(options=options):
                policy = self._policy()
                taxonomy = {"contract": "fixture-taxonomy"}
                entries: list[dict[str, object]] = []
                inventory_info = {"inventory_sha256": "c" * 64}
                sample = self._sample(sample_seed)
                with (
                    patch.object(
                        quality_module,
                        "load_quality_policy",
                        return_value=policy,
                    ) as load_policy,
                    patch.object(
                        quality_module,
                        "load_taxonomy",
                        return_value=taxonomy,
                    ) as load_taxonomy_mock,
                    patch.object(
                        quality_module,
                        "_load_inventory_bundle",
                        return_value=(entries, inventory_info),
                    ) as load_inventory_bundle,
                    patch.object(
                        quality_module,
                        "_generate_sample_from_inventory",
                        return_value=sample,
                    ) as generate_from_inventory,
                    patch.object(
                        quality_module,
                        "create_quality_run_directory",
                        return_value=run_directory,
                    ) as create_run_directory,
                    patch.object(quality_module, "write_json") as write_json_mock,
                ):
                    result = quality_module.run_sample(
                        self.manifest, self.inventory_path, **options
                    )

                self.assertEqual(result["seed"], sample_seed)
                self.assertEqual(result["items"], [{"revision_id": "b" * 64}])
                load_policy.assert_called_once_with(self.manifest)
                load_taxonomy_mock.assert_called_once_with(self.manifest)
                load_inventory_bundle.assert_called_once_with(
                    self.manifest,
                    self.inventory_path,
                    taxonomy,
                    policy,
                )
                generate_from_inventory.assert_called_once_with(
                    self.manifest,
                    entries=entries,
                    inventory_info=inventory_info,
                    taxonomy=taxonomy,
                    qpolicy=policy,
                    size=expected_size,
                    seed=expected_seed,
                )
                create_run_directory.assert_called_once_with(
                    self.manifest.root, "sample"
                )
                self.assertEqual(write_json_mock.call_count, 4)


class QualitySamplingTests(unittest.TestCase):
    """Phase-1 doc section 10.3: deterministic stratified sampling."""

    # Fields the sampling algorithm derives from the fixture inventory alone.
    # Pinning a hash over these keeps the determinism guarantee without binding
    # the test to the canonical translations.
    ALGORITHM_FIELDS = (
        "bucket_counts",
        "bucket_targets",
        "coverage",
        "items",
        "quality_contract",
        "revisions",
        "schema_version",
        "seed",
        "size",
        "unmet_constraints",
    )
    # Provenance digests bind a sample to the corpus and inputs it was drawn
    # from, so they move whenever those move.  They are checked by shape and,
    # for sample_id, by derivation; see _assert_provenance_is_derived.
    PROVENANCE_DIGEST_FIELDS = (
        "inventory_sha256",
        "items_sha256",
        "manifest_sha256",
        "policy_sha256",
        "taxonomy_sha256",
        "terminology_sha256",
        "translation_inputs_sha256",
    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.qpolicy = load_quality_policy(cls.manifest)
        cls.taxonomy = load_taxonomy(cls.manifest)
        cls.inventory = cls._make_fixture_inventory()

    # Full key sets per contract.  The pinned projection above only covers the
    # fields it enumerates, so without this a field added to the sample schema
    # would be silently left unchecked.  Asserting the whole key set makes any
    # schema change fail loudly and forces a decision about where it belongs.
    EXPECTED_SAMPLE_KEYS = frozenset(
        ALGORITHM_FIELDS + PROVENANCE_DIGEST_FIELDS + ("inventory_tool_version", "sample_id")
    )
    EXPECTED_DRY_RUN_KEYS = frozenset(
        EXPECTED_SAMPLE_KEYS - {"bucket_counts", "bucket_targets"}
    ) | {"official_sample_id"}

    def _assert_known_schema(self, sample: dict[str, object]) -> None:
        expected = (
            self.EXPECTED_DRY_RUN_KEYS
            if sample["quality_contract"] == quality_module.DRY_RUN_CONTRACT
            else self.EXPECTED_SAMPLE_KEYS
        )
        self.assertEqual(set(sample), set(expected))

    @classmethod
    def _algorithm_digest(cls, sample: dict[str, object]) -> str:
        projection = {
            field: sample[field] for field in cls.ALGORITHM_FIELDS if field in sample
        }
        serialized = (
            json.dumps(projection, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        ).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def _assert_provenance_is_derived(self, sample: dict[str, object]) -> None:
        """Assert provenance by derivation rather than by pinned value.

        `translation_inputs_sha256` is part of the sample identity
        (`quality.py::_SAMPLE_IDENTITY_FIELDS`), so `sample_id` is *designed* to
        change whenever the canonical translations change.  Pinning a literal
        here would make every translation batch fail this test and train
        maintainers to update the constant reflexively, which is exactly how a
        real sampling regression would slip through.
        """
        self.assertEqual(
            sample["sample_id"],
            quality_module._canonical_sha256(quality_module._sample_identity(sample)),
        )
        for field in self.PROVENANCE_DIGEST_FIELDS:
            if field in sample:
                self.assertRegex(str(sample[field]), r"^[0-9a-f]{64}$")

    @classmethod
    def _entry(
        cls,
        index: int,
        *,
        component: str,
        section: str,
        source: str,
        target: str,
        source_tag: str | None = None,
        profile: str,
        length_bin: str,
        enriched: bool = False,
        term_evidence: bool = False,
        line: int = 1,
    ) -> dict[str, object]:
        unit_id = compute_unit_id(component, section, source, source_tag)
        tu_uid = compute_tu_uid(component, section, source, source_tag)
        revision_uid_value = compute_revision_uid(tu_uid, source)
        revision_id = compute_revision_id(
            cls.manifest.version,
            unit_id,
            target,
            None,
            None,
            tu_uid=tu_uid,
            revision_uid_value=revision_uid_value,
            source=source,
        )
        structure = structure_signature(source, target, None)
        risk_flags = ["has-printf"] if enriched else []
        terms = (
            [
                {
                    "source": "fixture",
                    "target": "固定",
                    "category": "T.GAME.TALENT",
                    "source_tag": "",
                    "status": "preferred",
                    "scope": "core",
                    "notes": "fixture term",
                    "match": "partial",
                }
            ]
            if term_evidence
            else []
        )
        return {
            "unit_id": unit_id,
            "tu_uid": tu_uid,
            "revision_uid": revision_uid_value,
            "revision_id": revision_id,
            "version": cls.manifest.version,
            "component": component,
            "section": section,
            "source": source,
            "target": target,
            "source_tag": source_tag,
            "args_order": None,
            "special": None,
            "occurrences": [
                {
                    "logical_path": f"{component}.lua",
                    "section": section,
                    "line": line,
                    "ordinal": index,
                }
            ],
            "profile": profile,
            "profile_confidence": "high",
            "domain_hints": [],
            "relevant_terms": terms,
            "structure": structure,
            "gate_signals": {
                "lua_load_valid": True,
                "empty_target": False,
                "format_signature_match": None,
                "markup_multiset_match": True,
                "at_token_multiset_match": True,
                "runtime_collision": False,
                "needs_review": [],
            },
            "risk_flags": risk_flags,
            "source_length_bin": length_bin,
        }

    @classmethod
    def _make_fixture_inventory(cls) -> list[dict[str, object]]:
        profiles = [
            "mechanics", "term-name", "ui", "runtime-log",
            "dialogue", "narrative", "unknown",
        ]
        bins = ["short", "medium", "long", "very-long"]
        components = ["tome", "engine", "boot", "cults", "orcs", "example", "addon-dev"]
        entries: list[dict[str, object]] = []
        for index in range(320):
            entries.append(
                cls._entry(
                    index,
                    component=components[index % 7],
                    section=f"data/zone-{index % 3}/file-{index % 11}.lua",
                    source=f"fixture source {index}",
                    target=f"固定译文 {index}",
                    profile=profiles[index % 7],
                    length_bin=bins[index % 4],
                    enriched=index % 3 == 0,
                    term_evidence=index % 4 == 0,
                )
            )
        # contrast groups: one multi-target triplet and two pairs
        contrast_sources = [
            ("tome", "data/contrast/a.lua", "shared runtime key", "译法甲"),
            ("tome", "data/contrast/a.lua", "shared runtime key", "译法乙"),
            ("tome", "data/contrast/a.lua", "shared runtime key", "译法丙"),
            ("cults", "data/contrast/b.lua", "near #GREEN#dup#LAST# key", "近重复一"),
            ("cults", "data/contrast/b.lua", "near dup key", "近重复二"),
            ("boot", "data/contrast/c.lua", "repeat key", "重复一"),
            ("boot", "data/contrast/d.lua", "repeat key", "重复二"),
        ]
        for index, (component, section, source, target) in enumerate(
            contrast_sources, start=1000
        ):
            entries.append(
                cls._entry(
                    index,
                    component=component,
                    section=section,
                    source=source,
                    target=target,
                    profile="dialogue",
                    length_bin="short",
                )
            )
        return entries

    def _write_inventory(self, entries: list[dict[str, object]]) -> Path:
        directory = TEST_FIXTURE_ROOT / "quality-sampling"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "inventory.jsonl"
        path.write_text(
            "\n".join(
                json.dumps(entry, ensure_ascii=False, sort_keys=True) for entry in entries
            )
            + "\n",
            encoding="utf-8",
        )
        (directory / "inventory-manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "quality_contract": quality_module.INVENTORY_CONTRACT,
                    "tool_version": TOOL_VERSION,
                    "version": self.manifest.version,
                    "manifest_sha256": hashlib.sha256(
                        self.manifest.raw_bytes
                    ).hexdigest(),
                    "translation_inputs_sha256": (
                        quality_module._current_translation_inputs_sha256(
                            self.manifest
                        )
                    ),
                    "identity_indexes_sha256": (
                        quality_module._identity_indexes_sha256(self.manifest)
                    ),
                    "terminology_sha256": (
                        quality_module.terminology_store_sha256(
                            self.manifest.root / self.manifest.terminology
                        )
                    ),
                    "taxonomy_sha256": quality_module._canonical_sha256(
                        self.taxonomy
                    ),
                    "policy_sha256": quality_module._canonical_sha256(
                        self.qpolicy
                    ),
                    "inventory_sha256": quality_module._canonical_sha256(
                        entries
                    ),
                    "entries": len(entries),
                    "profile_classifier_version": self.taxonomy[
                        "profile_classifier_version"
                    ],
                    "risk_rule_version": self.taxonomy["risk_rule_version"],
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return path

    def test_inventory_manifest_preflight_and_jsonl_binding(self) -> None:
        cases = (
            ("missing", "missing", None, None, "root", False),
            ("invalid encoding", "raw", None, b"\xff", "root", False),
            ("invalid JSON", "raw", None, b"{", "root", False),
            ("non-object root", "raw", None, b"[]", "root", False),
            (
                "wrong contract",
                "set",
                "quality_contract",
                "old-contract",
                "quality_contract",
                False,
            ),
            (
                "bool schema",
                "set",
                "schema_version",
                True,
                "schema_version",
                False,
            ),
            (
                "missing tool version",
                "delete",
                "tool_version",
                None,
                "tool_version",
                False,
            ),
            (
                "old tool version",
                "set",
                "tool_version",
                "0.0.0",
                "tool_version",
                False,
            ),
            (
                "wrong version",
                "set",
                "version",
                "old-version",
                "version",
                False,
            ),
            (
                "stale manifest",
                "set",
                "manifest_sha256",
                "0" * 64,
                "manifest_sha256",
                False,
            ),
            (
                "missing translation inputs digest",
                "delete",
                "translation_inputs_sha256",
                None,
                "translation_inputs_sha256",
                False,
            ),
            (
                "missing identity indexes digest",
                "delete",
                "identity_indexes_sha256",
                None,
                "identity_indexes_sha256",
                False,
            ),
            (
                "stale identity indexes",
                "set",
                "identity_indexes_sha256",
                "0" * 64,
                "identity_indexes_sha256",
                False,
            ),
            (
                "stale translation inputs",
                "set",
                "translation_inputs_sha256",
                "0" * 64,
                "translation_inputs_sha256",
                False,
            ),
            (
                "stale terminology",
                "set",
                "terminology_sha256",
                "0" * 64,
                "terminology_sha256",
                False,
            ),
            (
                "stale taxonomy",
                "set",
                "taxonomy_sha256",
                "0" * 64,
                "taxonomy_sha256",
                False,
            ),
            (
                "stale policy",
                "set",
                "policy_sha256",
                "0" * 64,
                "policy_sha256",
                False,
            ),
            (
                "missing policy digest",
                "delete",
                "policy_sha256",
                None,
                "policy_sha256",
                False,
            ),
            (
                "wrong profile classifier",
                "set",
                "profile_classifier_version",
                "old-profile-classifier",
                "profile_classifier_version",
                False,
            ),
            (
                "wrong risk rules",
                "set",
                "risk_rule_version",
                "old-risk-rules",
                "risk_rule_version",
                False,
            ),
            ("bool count", "set", "entries", True, "entries", False),
            (
                "noncanonical digest",
                "set",
                "inventory_sha256",
                "A" * 64,
                "inventory_sha256",
                False,
            ),
            (
                "count mismatch",
                "set",
                "entries",
                len(self.inventory) + 1,
                "entries",
                True,
            ),
            (
                "digest mismatch",
                "set",
                "inventory_sha256",
                "0" * 64,
                "inventory_sha256",
                True,
            ),
        )
        functions = (
            generate_sample,
            generate_dry_run,
            quality_module.run_sample,
            quality_module.run_dry_run,
        )
        original_preflight = quality_module._read_inventory_manifest_preflight
        original_read_inventory = quality_module.read_inventory_file

        for name, operation, field, value, error_field, reads_jsonl in cases:
            with self.subTest(case=name):
                path = self._write_inventory(self.inventory)
                manifest_path = path.with_name("inventory-manifest.json")
                if operation == "missing":
                    manifest_path.unlink()
                elif operation == "raw":
                    manifest_path.write_bytes(value)
                else:
                    inventory_manifest = json.loads(
                        manifest_path.read_text(encoding="utf-8")
                    )
                    if operation == "delete":
                        del inventory_manifest[field]
                    else:
                        inventory_manifest[field] = value
                    manifest_path.write_text(
                        json.dumps(
                            inventory_manifest,
                            ensure_ascii=False,
                            sort_keys=True,
                        ),
                        encoding="utf-8",
                    )

                events: list[str] = []

                def tracked_preflight(*args: object) -> dict[str, object]:
                    events.append("manifest")
                    return original_preflight(*args)

                def tracked_inventory(
                    inventory_path: Path,
                ) -> tuple[list[dict[str, object]], dict[str, object]]:
                    events.append("inventory")
                    return original_read_inventory(inventory_path)

                with (
                    patch.object(
                        quality_module,
                        "_read_inventory_manifest_preflight",
                        side_effect=tracked_preflight,
                    ),
                    patch.object(
                        quality_module,
                        "read_inventory_file",
                        side_effect=tracked_inventory,
                    ) as read_inventory,
                    patch.object(
                        quality_module, "_validate_inventory_semantics"
                    ) as validate_semantics,
                    patch.object(
                        quality_module, "_generate_sample_from_inventory"
                    ) as generate_from_inventory,
                    patch.object(
                        quality_module, "_sampling_features"
                    ) as sampling_features,
                    patch.object(
                        quality_module, "create_quality_run_directory"
                    ) as create_run_directory,
                    patch.object(quality_module, "write_json") as write_json_mock,
                ):
                    for function in functions:
                        with self.subTest(case=name, function=function.__name__):
                            with self.assertRaisesRegex(
                                ValidationError,
                                rf"quality inventory manifest\.{error_field}",
                            ):
                                function(self.manifest, path)

                expected_events = (
                    ["manifest", "inventory"] * len(functions)
                    if reads_jsonl
                    else ["manifest"] * len(functions)
                )
                self.assertEqual(events, expected_events)
                self.assertEqual(
                    read_inventory.call_count,
                    len(functions) if reads_jsonl else 0,
                )
                for mocked in (
                    validate_semantics,
                    generate_from_inventory,
                    sampling_features,
                    create_run_directory,
                    write_json_mock,
                ):
                    mocked.assert_not_called()

    def test_inventory_record_contract_fails_before_sampling_helpers(self) -> None:
        cases = (
            (
                "missing source tag",
                lambda entry: entry.pop("source_tag"),
                "quality inventory record 1.source_tag",
            ),
            (
                "missing occurrence path",
                lambda entry: entry["occurrences"][0].pop("logical_path"),
                "quality inventory record 1.occurrences[0].logical_path",
            ),
            (
                "wrong occurrence line type",
                lambda entry: entry["occurrences"][0].__setitem__("line", "1"),
                "quality inventory record 1.occurrences[0].line",
            ),
            (
                "bool args order",
                lambda entry: entry.__setitem__("args_order", [True]),
                "quality inventory record 1.args_order[0]",
            ),
            (
                "bool occurrence ordinal",
                lambda entry: entry["occurrences"][0].__setitem__(
                    "ordinal", False
                ),
                "quality inventory record 1.occurrences[0].ordinal",
            ),
            (
                "empty occurrences",
                lambda entry: entry.__setitem__("occurrences", []),
                "quality inventory record 1.occurrences",
            ),
            (
                "noncanonical special",
                lambda entry: entry.__setitem__(
                    "special", {"value": float("nan")}
                ),
                "quality inventory record 1.special",
            ),
            (
                "wrong domain hint item type",
                lambda entry: entry.__setitem__("domain_hints", [1]),
                "quality inventory record 1.domain_hints[0]",
            ),
            (
                "wrong relevant term item type",
                lambda entry: entry.__setitem__("relevant_terms", ["term"]),
                "quality inventory record 1.relevant_terms[0]",
            ),
            (
                "wrong structure type",
                lambda entry: entry.__setitem__("structure", []),
                "quality inventory record 1.structure",
            ),
        )
        for function in (generate_sample, generate_dry_run):
            for name, mutate, expected_path in cases:
                with self.subTest(function=function.__name__, case=name):
                    valid = copy.deepcopy(self.inventory[0])
                    invalid = copy.deepcopy(self.inventory[1])
                    mutate(invalid)
                    path = self._write_inventory([valid, invalid])
                    with (
                        patch.object(
                            quality_module, "_generate_sample_from_inventory"
                        ) as generate_from_inventory,
                        patch.object(
                            quality_module, "_contrast_groups"
                        ) as contrast_groups,
                        patch.object(
                            quality_module, "_entry_features"
                        ) as entry_features,
                        patch.object(
                            quality_module, "_build_sample_items"
                        ) as build_sample_items,
                    ):
                        with self.assertRaises(ValidationError) as raised:
                            function(self.manifest, path)

                    self.assertIn(expected_path, str(raised.exception))
                    for mocked in (
                        generate_from_inventory,
                        contrast_groups,
                        entry_features,
                        build_sample_items,
                    ):
                        mocked.assert_not_called()

    def test_inventory_semantics_fail_before_sampling_or_output(self) -> None:
        cases = (
            (
                "wrong version",
                lambda entry: entry.__setitem__("version", "tome-old"),
                "version",
            ),
            (
                "undeclared component",
                lambda entry: entry.__setitem__("component", "undeclared"),
                "component",
            ),
            (
                "wrong unit id",
                lambda entry: entry.__setitem__("unit_id", "0" * 64),
                "unit_id",
            ),
            (
                "wrong revision id",
                lambda entry: entry.__setitem__("revision_id", "0" * 64),
                "revision_id",
            ),
            (
                "unknown profile",
                lambda entry: entry.__setitem__("profile", "undeclared"),
                "profile",
            ),
            (
                "unknown risk flag",
                lambda entry: entry.__setitem__(
                    "risk_flags", ["undeclared-risk"]
                ),
                "risk_flags",
            ),
            (
                "unknown length bin",
                lambda entry: entry.__setitem__(
                    "source_length_bin", "undeclared"
                ),
                "source_length_bin",
            ),
        )
        for function in (generate_sample, generate_dry_run):
            for name, mutate, field in cases:
                with self.subTest(function=function.__name__, case=name):
                    valid = copy.deepcopy(self.inventory[0])
                    invalid = copy.deepcopy(self.inventory[1])
                    mutate(invalid)
                    path = self._write_inventory([valid, invalid])
                    with (
                        patch.object(
                            quality_module, "_sampling_features"
                        ) as sampling_features,
                        patch.object(
                            quality_module, "_contrast_groups"
                        ) as contrast_groups,
                        patch.object(
                            quality_module, "_select_bucket"
                        ) as select_bucket,
                        patch.object(
                            quality_module, "_generate_sample_from_inventory"
                        ) as generate_from_inventory,
                        patch.object(
                            quality_module, "create_quality_run_directory"
                        ) as create_run_directory,
                        patch.object(quality_module, "write_json") as write_json_mock,
                    ):
                        with self.assertRaises(ValidationError) as raised:
                            function(self.manifest, path)

                    self.assertIn(
                        f"quality inventory record 1.{field}",
                        str(raised.exception),
                    )
                    for mocked in (
                        sampling_features,
                        contrast_groups,
                        select_bucket,
                        generate_from_inventory,
                        create_run_directory,
                        write_json_mock,
                    ):
                        mocked.assert_not_called()

    def test_inventory_semantics_accept_valid_fixture_without_mutation(self) -> None:
        entries = copy.deepcopy(self.inventory)
        expected = copy.deepcopy(entries)

        quality_module._validate_inventory_semantics(
            entries, self.manifest, self.taxonomy
        )

        self.assertEqual(entries, expected)

    def test_valid_inventory_record_contract_preserves_order_and_digest(self) -> None:
        expected = copy.deepcopy(self.inventory[:3])
        path = self._write_inventory(expected)
        loaded, info = quality_module.read_inventory_file(path)

        self.assertEqual(loaded, expected)
        self.assertEqual(
            [entry["revision_id"] for entry in loaded],
            [entry["revision_id"] for entry in expected],
        )
        self.assertEqual(
            info["inventory_sha256"], quality_module._canonical_sha256(expected)
        )

    def test_sample_is_deterministic_and_satisfies_constraints(self) -> None:
        path = self._write_inventory(self.inventory)
        first = generate_sample(self.manifest, path)
        second = generate_sample(self.manifest, path)
        self._assert_known_schema(first)
        self.assertEqual(
            self._algorithm_digest(first),
            "ff8fa6e7c7963fdb15ca6b46626f09f4ce95c3dd3ca7d29802e4388c701c5479",
        )
        self._assert_provenance_is_derived(first)
        self.assertEqual(
            first["items_sha256"],
            quality_module._canonical_sha256(first["items"]),
        )
        self.assertEqual(first["sample_id"], second["sample_id"])
        self.assertEqual(first["items"], second["items"])
        self.assertEqual(first["size"], 120)
        self.assertEqual(first["unmet_constraints"], [])
        revisions = [item["revision_id"] for item in first["items"]]
        self.assertEqual(len(revisions), len(set(revisions)))
        buckets = [item["bucket"] for item in first["items"]]
        self.assertEqual(
            sum(buckets.count(bucket) for bucket in ("representative", "risk-enriched", "contrast")),
            120,
        )
        self.assertEqual(
            len({(r, b) for r, b in zip(revisions, buckets)}), 120,
        )

    def test_context_neighbors_use_identity_index_without_equality_scans(self) -> None:
        class EqualityCountingDict(dict[str, object]):
            comparisons = 0

            def __eq__(self, other: object) -> bool:
                type(self).comparisons += 1
                return super().__eq__(other)

        def entry(
            index: int, component: str, source: str, line: int
        ) -> EqualityCountingDict:
            item = EqualityCountingDict(
                self._entry(
                    index,
                    component=component,
                    section=f"data/{source}.lua",
                    source=source,
                    target=f"target {source}",
                    profile="ui",
                    length_bin="short",
                    line=line,
                )
            )
            item["profile_confidence"] = "medium"
            return item

        a_first = entry(1, "tome", "a-first", 10)
        a_before = entry(2, "tome", "a-before", 20)
        a_middle = entry(3, "tome", "a-middle", 30)
        a_after = entry(4, "tome", "a-after", 40)
        a_last = entry(5, "tome", "a-last", 50)
        b_first = entry(6, "engine", "b-first", 10)
        b_middle = entry(7, "engine", "b-middle", 20)
        b_last = entry(8, "engine", "b-last", 30)
        entries = [
            a_middle,
            b_last,
            a_first,
            b_first,
            a_last,
            a_before,
            b_middle,
            a_after,
        ]
        foreign = self._entry(
            9,
            component="tome",
            section="data/foreign.lua",
            source="foreign",
            target="foreign target",
            profile="ui",
            length_bin="short",
            line=35,
        )
        foreign["profile_confidence"] = "medium"

        items = quality_module._build_sample_items(
            entries=entries,
            ordered=[a_first, a_middle, a_last, b_middle, foreign],
            contrast_ids=set(),
            risk_selected_ids=set(),
            contrast_group_of={},
            contrast=[],
            qpolicy={"context_neighbor_limit": 2},
        )

        self.assertEqual(EqualityCountingDict.comparisons, 0)
        self.assertEqual(
            [
                [neighbor["source"] for neighbor in item["context_neighbors"]]
                for item in items
            ],
            [
                ["a-before", "a-middle"],
                ["a-first", "a-before", "a-after", "a-last"],
                ["a-middle", "a-after"],
                ["b-first", "b-last"],
                [],
            ],
        )
        self.assertEqual(
            items[1]["context_neighbors"][0],
            {
                "component": "tome",
                "section": "data/a-first.lua",
                "source": "a-first",
                "target": "target a-first",
                "source_tag": None,
            },
        )

    def test_contrast_pairs_are_never_split(self) -> None:
        path = self._write_inventory(self.inventory)
        sample = generate_sample(self.manifest, path)
        groups: dict[str, list[str]] = {}
        for item in sample["items"]:
            if item["contrast_group"]:
                groups.setdefault(item["contrast_group"], []).append(item["revision_id"])
        self.assertGreaterEqual(len(groups), 2)
        by_source: dict[str, list[str]] = {}
        for item in self.inventory:
            if item["section"].startswith("data/contrast"):
                by_source.setdefault(item["source"], []).append(item["revision_id"])
        sample_revisions = {item["revision_id"] for item in sample["items"]}
        for members in by_source.values():
            if members:
                self.assertTrue(
                    all(member in sample_revisions for member in members)
                    or all(member not in sample_revisions for member in members),
                    "contrast pair must be sampled as a whole",
                )

    def test_different_seed_changes_selection_but_keeps_constraints(self) -> None:
        path = self._write_inventory(self.inventory)
        first = generate_sample(self.manifest, path, seed="seed-a")
        second = generate_sample(self.manifest, path, seed="seed-b")
        self.assertNotEqual(first["sample_id"], second["sample_id"])
        self.assertNotEqual(
            [item["revision_id"] for item in first["items"]],
            [item["revision_id"] for item in second["items"]],
        )
        self.assertEqual(second["unmet_constraints"], [])

    def test_overlapping_contrast_groups_are_never_split(self) -> None:
        # Group 1 (multi-target): A1/A2 share runtime key 'overlap key' with
        # different targets. Group 2 (near-duplicate): A1 and B1 share the
        # normalized source ('overlap key' vs 'overlap key.'). A1 is claimed by
        # whichever group is selected first; the other group must be skipped
        # whole instead of sampling its remaining member alone.
        def entry(
            index: int, source: str, target: str, section: str
        ) -> dict[str, object]:
            unit_id = compute_unit_id("tome", section, source, None)
            tu_uid = compute_tu_uid("tome", section, source, None)
            revision_uid_value = compute_revision_uid(tu_uid, source)
            revision_id = compute_revision_id(
                self.manifest.version,
                unit_id,
                target,
                None,
                None,
                tu_uid=tu_uid,
                revision_uid_value=revision_uid_value,
                source=source,
            )
            structure = structure_signature(source, target, None)
            return {
                "unit_id": unit_id,
                "tu_uid": tu_uid,
                "revision_uid": revision_uid_value,
                "revision_id": revision_id,
                "version": self.manifest.version,
                "component": "tome",
                "section": section,
                "source": source,
                "target": target,
                "source_tag": None,
                "args_order": None,
                "special": None,
                "occurrences": [
                    {
                        "logical_path": "tome.lua",
                        "section": section,
                        "line": index + 1,
                        "ordinal": index,
                    }
                ],
                "profile": "ui",
                "profile_confidence": "high",
                "domain_hints": [],
                "relevant_terms": [],
                "structure": structure,
                "gate_signals": {
                    "lua_load_valid": True,
                    "empty_target": False,
                    "format_signature_match": None,
                    "markup_multiset_match": True,
                    "at_token_multiset_match": True,
                    "runtime_collision": False,
                    "needs_review": [],
                },
                "risk_flags": [],
                "source_length_bin": "short",
            }

        entries: list[dict[str, object]] = []
        for index in range(130):
            entries.append(
                entry(index + 10, f"filler {index}", f"填充 {index}", "data/x.lua")
            )
        entries.append(entry(0, "overlap key", "译法甲", "data/contrast/a.lua"))
        entries.append(entry(1, "overlap key", "译法乙", "data/contrast/a.lua"))
        entries.append(entry(2, "overlap key ", "译法甲", "data/contrast/b.lua"))
        path = self._write_inventory(entries)
        sample = generate_sample(self.manifest, path, seed="overlap-fixture")
        sampled = {item["revision_id"] for item in sample["items"]}
        from i18nlib.quality import _contrast_groups

        loaded_entries = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        original_groups = _contrast_groups(loaded_entries, self.qpolicy)
        for _, members in original_groups:
            member_ids = {member["revision_id"] for member in members}
            if any(member in sampled for member in member_ids):
                self.assertTrue(
                    all(member in sampled for member in member_ids),
                    "a contrast group must never be split",
                )
        a1_rev = next(
            e["revision_id"]
            for e in entries
            if e["source"] == "overlap key" and e["target"] == "译法甲"
        )
        # A1 belongs to both groups, so it is always sampled with one of them
        self.assertIn(a1_rev, sampled)
        self.assertEqual(sample["size"], 120)

    def test_unmet_constraints_are_reported_not_silent(self) -> None:
        entries = [
            self._entry(
                index,
                component="tome",
                section="data/x.lua",
                source=f"only ui {index}",
                target=f"只有界面 {index}",
                profile="ui",
                length_bin="short",
            )
            for index in range(140)
        ]
        path = self._write_inventory(entries)
        sample = generate_sample(self.manifest, path)
        self.assertEqual(sample["size"], 120)
        self.assertGreaterEqual(len(sample["unmet_constraints"]), 4)
        unmet_ids = {unmet["id"] for unmet in sample["unmet_constraints"]}
        self.assertIn("profile-min", unmet_ids)
        self.assertIn("length-bin-min", unmet_ids)

    def test_wrong_sample_size_is_rejected(self) -> None:
        path = self._write_inventory(self.inventory)
        with self.assertRaises(ValidationError):
            generate_sample(self.manifest, path, size=99)

    def test_dry_run_is_deterministic_and_disjoint_from_official(self) -> None:
        path = self._write_inventory(self.inventory)
        first = generate_dry_run(self.manifest, path)
        second = generate_dry_run(self.manifest, path)
        self.assertIs(type(first), dict)
        self._assert_known_schema(first)
        self.assertEqual(
            self._algorithm_digest(first),
            "99b781a60d35d0a8107d54072f7642e324871e041494720455783bcfbf01fda1",
        )
        self._assert_provenance_is_derived(first)
        self.assertEqual(
            first["items_sha256"],
            quality_module._canonical_sha256(first["items"]),
        )
        self.assertEqual(first["sample_id"], second["sample_id"])
        self.assertEqual(first["items"], second["items"])
        self.assertEqual(first["size"], 12)
        self.assertEqual(first["unmet_constraints"], [])
        official = generate_sample(self.manifest, path)
        dry_ids = {item["revision_id"] for item in first["items"]}
        official_ids = {item["revision_id"] for item in official["items"]}
        self.assertTrue(dry_ids.isdisjoint(official_ids))
        self.assertEqual(first["official_sample_id"], official["sample_id"])
        revisions = [item["revision_id"] for item in first["items"]]
        self.assertEqual(len(revisions), len(set(revisions)))

    def test_run_dry_run_reuses_loaded_policy_for_templates(self) -> None:
        path = self._write_inventory(self.inventory)
        first_policy = copy.deepcopy(self.qpolicy)
        first_policy["pilot"]["evaluator_ids"] = [
            "first-reviewer-a",
            "first-reviewer-b",
        ]
        first_policy["pilot"]["method_version"] = "first-method"
        inventory_manifest_path = path.with_name("inventory-manifest.json")
        inventory_manifest = json.loads(
            inventory_manifest_path.read_text(encoding="utf-8")
        )
        inventory_manifest["policy_sha256"] = quality_module._canonical_sha256(
            first_policy
        )
        inventory_manifest_path.write_text(
            json.dumps(inventory_manifest, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        second_policy = copy.deepcopy(self.qpolicy)
        second_policy["pilot"]["evaluator_ids"] = [
            "second-reviewer-a",
            "second-reviewer-b",
        ]
        second_policy["pilot"]["method_version"] = "second-method"
        run_directory = (
            TEST_FIXTURE_ROOT / "quality-sampling" / "dry-run-policy-reuse"
        )
        policies = iter((first_policy, second_policy))
        events: list[str] = []

        def tracked_policy(manifest: Manifest) -> dict[str, object]:
            events.append("policy")
            return next(policies)

        def tracked_taxonomy(manifest: Manifest) -> dict[str, object]:
            events.append("taxonomy")
            return load_taxonomy(manifest)

        original_read_inventory = quality_module.read_inventory_file

        def tracked_inventory(
            inventory_path: Path,
        ) -> tuple[list[dict[str, object]], dict[str, object]]:
            events.append("inventory")
            return original_read_inventory(inventory_path)

        with (
            patch.object(
                quality_module,
                "load_quality_policy",
                side_effect=tracked_policy,
            ) as load_policy,
            patch.object(
                quality_module,
                "load_taxonomy",
                side_effect=tracked_taxonomy,
            ) as load_taxonomy_mock,
            patch.object(
                quality_module,
                "read_inventory_file",
                side_effect=tracked_inventory,
            ) as read_inventory,
            patch.object(
                quality_module,
                "create_quality_run_directory",
                return_value=run_directory,
            ),
            patch.object(quality_module, "write_json") as write_json_mock,
        ):
            result = quality_module.run_dry_run(self.manifest, path)

        load_policy.assert_called_once_with(self.manifest)
        load_taxonomy_mock.assert_called_once_with(self.manifest)
        read_inventory.assert_called_once_with(path)
        self.assertEqual(events, ["policy", "taxonomy", "inventory"])
        self.assertEqual(
            result["policy_sha256"],
            quality_module._canonical_sha256(first_policy),
        )
        templates = [
            mocked_call.args[1]
            for mocked_call in write_json_mock.call_args_list
            if mocked_call.args[0].name.startswith("assessment-template-")
        ]
        self.assertEqual(
            [template["evaluator"]["id"] for template in templates],
            first_policy["pilot"]["evaluator_ids"],
        )
        self.assertEqual(
            {template["evaluator"]["method_version"] for template in templates},
            {first_policy["pilot"]["method_version"]},
        )
        self.assertTrue(
            all(template["sample_id"] == result["sample_id"] for template in templates)
        )

    def test_dry_run_loads_inputs_once_without_mutating_inventory(self) -> None:
        path = self._write_inventory(self.inventory)
        original_read_inventory = quality_module.read_inventory_file
        original_load_policy = quality_module.load_quality_policy
        original_load_taxonomy = quality_module.load_taxonomy
        original_entry_features = quality_module._entry_features
        loaded_entries: list[list[dict[str, object]]] = []
        original_revision_order: list[str] = []
        original_entry_payloads: list[str] = []

        def tracked_read_inventory(
            inventory_path: Path,
        ) -> tuple[list[dict[str, object]], dict[str, object]]:
            entries, inventory_info = original_read_inventory(inventory_path)
            loaded_entries.append(entries)
            original_revision_order.extend(entry["revision_id"] for entry in entries)
            original_entry_payloads.extend(
                json.dumps(entry, ensure_ascii=False, sort_keys=True)
                for entry in entries
            )
            return entries, inventory_info

        with (
            patch.object(
                quality_module,
                "read_inventory_file",
                side_effect=tracked_read_inventory,
            ) as read_inventory,
            patch.object(
                quality_module,
                "load_quality_policy",
                wraps=original_load_policy,
            ) as load_policy,
            patch.object(
                quality_module,
                "load_taxonomy",
                wraps=original_load_taxonomy,
            ) as load_taxonomy_mock,
            patch.object(
                quality_module,
                "_entry_features",
                wraps=original_entry_features,
            ) as entry_features,
        ):
            dry_run = generate_dry_run(self.manifest, path)

        self.assertEqual(read_inventory.call_count, 1)
        self.assertEqual(load_policy.call_count, 1)
        self.assertEqual(load_taxonomy_mock.call_count, 1)
        self.assertEqual(entry_features.call_count, len(self.inventory))
        self.assertEqual(len(loaded_entries), 1)
        self.assertEqual(len(loaded_entries[0]), len(self.inventory))
        self.assertEqual(
            [entry["revision_id"] for entry in loaded_entries[0]],
            original_revision_order,
        )
        self.assertEqual(
            [
                json.dumps(entry, ensure_ascii=False, sort_keys=True)
                for entry in loaded_entries[0]
            ],
            original_entry_payloads,
        )
        self.assertTrue(all("_features" not in entry for entry in loaded_entries[0]))
        official = generate_sample(self.manifest, path)
        self.assertEqual(dry_run["official_sample_id"], official["sample_id"])
        self._assert_provenance_is_derived(official)

    def test_dry_run_does_not_cache_mutable_inventory_between_calls(self) -> None:
        path = self._write_inventory(self.inventory)
        original_read_inventory = quality_module.read_inventory_file
        loaded_entries: list[list[dict[str, object]]] = []

        def tracked_read_inventory(
            inventory_path: Path,
        ) -> tuple[list[dict[str, object]], dict[str, object]]:
            entries, inventory_info = original_read_inventory(inventory_path)
            loaded_entries.append(entries)
            return entries, inventory_info

        with patch.object(
            quality_module,
            "read_inventory_file",
            side_effect=tracked_read_inventory,
        ) as read_inventory:
            first = generate_dry_run(self.manifest, path)
            second = generate_dry_run(self.manifest, path)

        self.assertEqual(read_inventory.call_count, 2)
        self.assertEqual(first, second)
        self.assertIsNot(loaded_entries[0], loaded_entries[1])
        self.assertTrue(
            all(
                first_entry is not second_entry
                for first_entry, second_entry in zip(
                    loaded_entries[0], loaded_entries[1]
                )
            )
        )
        self.assertTrue(
            all(
                "_features" not in entry
                for entries in loaded_entries
                for entry in entries
            )
        )


class QualityRuntimeSemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_manifest = load_manifest()
        cls.manifest = replace(
            cls.base_manifest,
            components=(
                replace(
                    cls.base_manifest.components[0],
                    id="alpha",
                    translation="alpha.lua",
                    copy_fragment=None,
                ),
                replace(
                    cls.base_manifest.components[1],
                    id="beta",
                    translation="beta.lua",
                    copy_fragment=None,
                ),
            ),
        )

    @staticmethod
    def _document(
        logical_path: str, records: tuple[dict[str, object], ...]
    ) -> LocaleDocument:
        return LocaleDocument(
            logical_path=logical_path,
            sha256="0" * 64,
            records=records,
        )

    @staticmethod
    def _record(
        source: str,
        target: str,
        section: str,
        *,
        args_order: object = None,
        special: object = None,
    ) -> dict[str, object]:
        return {
            "kind": "translation",
            "source": source,
            "target": target,
            "source_tag": None,
            "section": section,
            "args_order": args_order,
            "special": special,
        }

    def test_inventory_translation_digest_uses_loaded_bytes_in_consumption_order(
        self,
    ) -> None:
        manifest = replace(
            self.base_manifest,
            components=(
                replace(
                    self.base_manifest.components[0],
                    id="alpha",
                    copy_fragment="shared.lua",
                    translation="shared.lua",
                ),
                replace(
                    self.base_manifest.components[1],
                    id="beta",
                    copy_fragment="shared.lua",
                    translation="shared.lua",
                ),
            ),
        )
        loaded_sha256 = tuple(str(index) * 64 for index in range(1, 5))
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = tuple(
            LocaleDocument(
                logical_path="shared.lua",
                sha256=sha256,
                records=(),
            )
            for sha256 in loaded_sha256
        )

        inventory = build_inventory(manifest, loader)

        self.assertEqual(loader.load_path.call_count, 4)
        self.assertEqual(
            inventory["translation_inputs_sha256"],
            quality_module._canonical_sha256(
                [
                    {
                        "component": component,
                        "role": role,
                        "logical_path": "shared.lua",
                        "sha256": sha256,
                    }
                    for (component, role), sha256 in zip(
                        (
                            ("alpha", "copy_fragment"),
                            ("alpha", "translation"),
                            ("beta", "copy_fragment"),
                            ("beta", "translation"),
                        ),
                        loaded_sha256,
                    )
                ]
            ),
        )

    def test_inventory_and_contrast_groups_use_complete_runtime_semantics(
        self,
    ) -> None:
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = (
            self._document(
                "alpha.lua",
                (
                    self._record(
                        "Within args %s %s",
                        "参数 %s %s",
                        "alpha/args.lua",
                        args_order=[1, 2],
                    ),
                    self._record(
                        "Within args %s %s",
                        "参数 %s %s",
                        "alpha/args.lua",
                        args_order=[2, 1],
                    ),
                    self._record(
                        "Within special",
                        "特殊",
                        "alpha/special.lua",
                        special={"nested": [True]},
                    ),
                    self._record(
                        "Within special",
                        "特殊",
                        "alpha/special.lua",
                        special={"nested": [1]},
                    ),
                    self._record(
                        "Across components",
                        "跨组件",
                        "alpha/cross.lua",
                        special={"nested": [False]},
                    ),
                ),
            ),
            self._document(
                "beta.lua",
                (
                    self._record(
                        "Across components",
                        "跨组件",
                        "beta/cross.lua",
                        special={"nested": [0]},
                    ),
                ),
            ),
        )

        inventory = build_inventory(self.manifest, loader)
        entries = inventory["entries_list"]

        within = [
            entry for entry in entries if entry["source"].startswith("Within")
        ]
        across = [
            entry for entry in entries if entry["source"] == "Across components"
        ]
        self.assertEqual(len(within), 4)
        self.assertTrue(
            all(entry["gate_signals"]["runtime_collision"] for entry in within)
        )
        self.assertEqual(len(across), 2)
        self.assertTrue(
            all(
                entry["gate_signals"]["cross_component_variant"]
                for entry in across
            )
        )
        self.assertTrue(
            all(
                not entry["gate_signals"]["runtime_collision"]
                for entry in across
            )
        )

        groups = quality_module._contrast_groups(
            entries, load_quality_policy(self.base_manifest)
        )
        multi_value_sources = {
            members[0]["source"]
            for group_id, members in groups
            if group_id.startswith("multi-value:")
        }
        self.assertEqual(
            multi_value_sources, {"Within args %s %s", "Within special"}
        )
        invalid_entry = dict(entries[0])
        invalid_entry["special"] = {"value": float("inf")}
        with self.assertRaises(ValidationError):
            quality_module._contrast_groups(
                [invalid_entry, entries[1]],
                load_quality_policy(self.base_manifest),
            )

    def test_noncanonical_inventory_semantics_fail_before_report_write(
        self,
    ) -> None:
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = (
            self._document(
                "alpha.lua",
                (
                    self._record(
                        "Invalid",
                        "无效",
                        "alpha/invalid.lua",
                        special={"value": float("nan")},
                    ),
                ),
            ),
            self._document(
                "beta.lua",
                (self._record("Valid", "有效", "beta/valid.lua"),),
            ),
        )
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-semantics-"
        ) as temporary:
            old_run = Path(temporary)
            old_inventory = old_run / "inventory.jsonl"
            old_manifest = old_run / "inventory-manifest.json"
            old_inventory.write_bytes(b"old inventory\n")
            old_manifest.write_bytes(b"old manifest\n")
            with patch.object(
                quality_module,
                "create_quality_run_directory",
                return_value=old_run,
            ) as create_run:
                with self.assertRaises(ValidationError):
                    quality_module.run_inventory(self.manifest, loader)

            create_run.assert_not_called()
            self.assertEqual(old_inventory.read_bytes(), b"old inventory\n")
            self.assertEqual(old_manifest.read_bytes(), b"old manifest\n")


class QualityInventoryIntegrationTests(unittest.TestCase):
    """Phase-1 doc section 10.5: real-corpus inventory conservation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.runtime = LuaRuntime(cls.manifest)
        cls.runtime.doctor()
        cls.loader = LocaleLoader(cls.runtime)

    def test_inventory_conserves_loader_counts_and_is_deterministic(self) -> None:
        with (
            patch.object(
                quality_module,
                "load_quality_policy",
                wraps=load_quality_policy,
            ) as load_policy_mock,
            patch.object(
                quality_module,
                "load_taxonomy",
                wraps=load_taxonomy,
            ) as load_taxonomy_mock,
        ):
            first = build_inventory(self.manifest, self.loader)
        load_policy_mock.assert_called_once_with(self.manifest)
        load_taxonomy_mock.assert_called_once_with(self.manifest)

        canonical = lambda value: hashlib.sha256(  # noqa: E731
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(
            first["policy_sha256"], canonical(load_quality_policy(self.manifest))
        )
        self.assertEqual(
            first["taxonomy_sha256"], canonical(load_taxonomy(self.manifest))
        )
        loader_translations = 0
        for component in self.manifest.components:
            paths = [component.translation]
            if component.copy_fragment:
                paths.insert(0, component.copy_fragment)
            for logical_path in paths:
                document = self.loader.load_path(
                    self.manifest.root / logical_path, logical_path=logical_path
                )
                loader_translations += len(document.translations)
        self.assertEqual(first["summary"]["occurrences"], loader_translations)
        self.assertEqual(first["summary"]["entries"], len(first["entries_list"]))
        self.assertGreater(first["summary"]["entries"], 10000)
        second = build_inventory(self.manifest, self.loader)
        self.assertEqual(first["inventory_sha256"], second["inventory_sha256"])
        self.assertEqual(first["entries_list"], second["entries_list"])


if __name__ == "__main__":
    unittest.main()
