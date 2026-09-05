"""Toolchain tests: quality config."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
import copy
from dataclasses import replace
import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import i18nlib.quality as quality_module
from i18nlib.config import Manifest, load_manifest
from i18nlib.errors import ConfigurationError
from i18nlib.lint import stable_entry_id
from i18nlib.locale_model import LocaleDocument, LocaleLoader
from i18nlib.quality import (
    build_inventory,
    compute_revision_id,
    compute_revision_uid,
    compute_tu_uid,
    compute_unit_id,
    tu_uid_fallback,
    generate_sample,
    load_quality_policy,
    load_taxonomy,
    structure_signature,
)
from i18nlib.workset import _relevant_terms


class QualityConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    @classmethod
    def _current_taxonomy(cls) -> dict[str, object]:
        path = cls.manifest.root / "i18n" / "quality" / "taxonomy-v1.json"
        return json.loads(path.read_text(encoding="utf-8"))

    @classmethod
    def _current_policy(cls) -> dict[str, object]:
        path = cls.manifest.root / "i18n" / "quality" / "policy-v1.json"
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _write_taxonomy(root: Path, taxonomy: dict[str, object]) -> None:
        path = root / "i18n" / "quality" / "taxonomy-v1.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(taxonomy, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _write_policy(root: Path, policy: dict[str, object]) -> None:
        path = root / "i18n" / "quality" / "policy-v1.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(policy, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _mutate_policy_path(
        policy: dict[str, object],
        path: tuple[str | int, ...],
        value: object,
        delete: object,
    ) -> None:
        parent: object = policy
        for part in path[:-1]:
            parent = parent[part]  # type: ignore[index]
        if value is delete:
            del parent[path[-1]]  # type: ignore[index]
        else:
            parent[path[-1]] = value  # type: ignore[index]

    def test_quality_taxonomy_loads_current_file_without_normalization(self) -> None:
        original = self._current_taxonomy()
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-taxonomy-valid-"
        ) as temporary:
            root = Path(temporary)
            self._write_taxonomy(root, copy.deepcopy(original))
            manifest = replace(self.manifest, root=root)
            loaded = load_taxonomy(manifest)

        canonical = lambda value: hashlib.sha256(  # noqa: E731
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(loaded, original)
        self.assertEqual(canonical(loaded), canonical(original))
        with patch.object(quality_module, "_read_json", return_value=original):
            self.assertIs(load_taxonomy(self.manifest), original)

    def test_quality_taxonomy_rejects_malformed_consumed_fields(self) -> None:
        original = self._current_taxonomy()
        delete = object()
        profiles_without_ui = [
            item for item in original["profiles"] if item["id"] != "ui"  # type: ignore[index]
        ]
        severities_without_note = [
            item
            for item in original["severities"]  # type: ignore[union-attr]
            if item["id"] != "note"
        ]
        confidence_without_c4 = [
            item
            for item in original["confidence_levels"]  # type: ignore[union-attr]
            if item["id"] != "C4"
        ]
        grades_without_gold = [
            item
            for item in original["grades"]  # type: ignore[union-attr]
            if item["id"] != "Gold"
        ]
        reuse_without_no_reuse = [
            item
            for item in original["reuse_scopes"]  # type: ignore[union-attr]
            if item["id"] != "no-reuse"
        ]
        duplicate_merge_pairs = copy.deepcopy(original["mergeable_codes"])
        duplicate_merge_pairs.append(  # type: ignore[union-attr]
            list(reversed(duplicate_merge_pairs[0]))  # type: ignore[index]
        )
        cases = (
            (
                "contract-list",
                ("contract",),
                [],
                "quality taxonomy.contract",
            ),
            (
                "schema-bool",
                ("schema_version",),
                True,
                "quality taxonomy.schema_version",
            ),
            ("profiles-bool", ("profiles",), True, "quality taxonomy.profiles"),
            (
                "severities-string",
                ("severities",),
                "minor",
                "quality taxonomy.severities",
            ),
            (
                "error-codes-empty",
                ("error_codes",),
                [],
                "quality taxonomy.error_codes",
            ),
            (
                "reuse-item-list",
                ("reuse_scopes", 0),
                [],
                "quality taxonomy.reuse_scopes[0]",
            ),
            (
                "confidence-id-bool",
                ("confidence_levels", 0, "id"),
                True,
                "quality taxonomy.confidence_levels[0].id",
            ),
            (
                "grade-id-duplicate",
                ("grades", 1, "id"),
                original["grades"][0]["id"],  # type: ignore[index]
                "quality taxonomy.grades[1].id",
            ),
            (
                "required-profile-missing",
                ("profiles",),
                profiles_without_ui,
                "quality taxonomy.profiles",
            ),
            (
                "exact-severity-missing",
                ("severities",),
                severities_without_note,
                "quality taxonomy.severities",
            ),
            (
                "exact-confidence-missing",
                ("confidence_levels",),
                confidence_without_c4,
                "quality taxonomy.confidence_levels",
            ),
            (
                "exact-grade-missing",
                ("grades",),
                grades_without_gold,
                "quality taxonomy.grades",
            ),
            (
                "exact-reuse-missing",
                ("reuse_scopes",),
                reuse_without_no_reuse,
                "quality taxonomy.reuse_scopes",
            ),
            (
                "categories-item-list",
                ("error_categories", 0),
                [],
                "quality taxonomy.error_categories[0]",
            ),
            (
                "vector-string",
                ("quality_vector_dimensions",),
                "accuracy",
                "quality taxonomy.quality_vector_dimensions",
            ),
            (
                "risk-flag-duplicate",
                ("risk_flags", 1),
                original["risk_flags"][0],  # type: ignore[index]
                "quality taxonomy.risk_flags[1]",
            ),
            (
                "error-category-reference",
                ("error_codes", 0, "category"),
                "unknown-category",
                "quality taxonomy.error_codes[0].category",
            ),
            (
                "error-severity-reference",
                ("error_codes", 0, "default_severity"),
                "critical",
                "quality taxonomy.error_codes[0].default_severity",
            ),
            (
                "source-tag-map-list",
                ("source_tag_profiles",),
                [],
                "quality taxonomy.source_tag_profiles",
            ),
            (
                "source-tag-empty-key",
                ("source_tag_profiles",),
                {"": "ui"},
                "quality taxonomy.source_tag_profiles['']",
            ),
            (
                "term-profile-reference",
                ("term_category_profiles", "T.GAME.TALENT"),
                "missing-profile",
                "quality taxonomy.term_category_profiles['T.GAME.TALENT']",
            ),
            (
                "section-rules-bool",
                ("section_pattern_profiles",),
                True,
                "quality taxonomy.section_pattern_profiles",
            ),
            (
                "section-rule-item-list",
                ("section_pattern_profiles", 0),
                [],
                "quality taxonomy.section_pattern_profiles[0]",
            ),
            (
                "section-pattern-empty",
                ("section_pattern_profiles", 0, "pattern"),
                "",
                "quality taxonomy.section_pattern_profiles[0].pattern",
            ),
            (
                "section-profile-reference",
                ("section_pattern_profiles", 0, "profile"),
                "missing-profile",
                "quality taxonomy.section_pattern_profiles[0].profile",
            ),
            (
                "section-confidence",
                ("section_pattern_profiles", 0, "confidence"),
                "certain",
                "quality taxonomy.section_pattern_profiles[0].confidence",
            ),
            (
                "length-id-duplicate",
                ("length_bins", 1, "id"),
                original["length_bins"][0]["id"],  # type: ignore[index]
                "quality taxonomy.length_bins[1].id",
            ),
            (
                "length-max-bool",
                ("length_bins", 0, "max"),
                True,
                "quality taxonomy.length_bins[0].max",
            ),
            (
                "length-max-out-of-order",
                ("length_bins", 1, "max"),
                10,
                "quality taxonomy.length_bins[1].max",
            ),
            (
                "length-null-before-last",
                ("length_bins", 0, "max"),
                None,
                "quality taxonomy.length_bins[0].max",
            ),
            (
                "length-last-not-null",
                ("length_bins", 3, "max"),
                300,
                "quality taxonomy.length_bins[3].max",
            ),
            (
                "length-max-missing",
                ("length_bins", 0, "max"),
                delete,
                "quality taxonomy.length_bins[0].max",
            ),
            (
                "classifier-version-empty",
                ("profile_classifier_version",),
                "",
                "quality taxonomy.profile_classifier_version",
            ),
            (
                "risk-version-list",
                ("risk_rule_version",),
                [],
                "quality taxonomy.risk_rule_version",
            ),
            (
                "merge-pair-not-two",
                ("mergeable_codes", 0),
                ["ACC_OMISSION"],
                "quality taxonomy.mergeable_codes[0]",
            ),
            (
                "merge-pair-same",
                ("mergeable_codes", 0),
                ["ACC_OMISSION", "ACC_OMISSION"],
                "quality taxonomy.mergeable_codes[0][1]",
            ),
            (
                "merge-pair-unknown",
                ("mergeable_codes", 0),
                ["ACC_OMISSION", "UNKNOWN_CODE"],
                "quality taxonomy.mergeable_codes[0][1]",
            ),
            (
                "merge-pair-unordered-duplicate",
                ("mergeable_codes",),
                duplicate_merge_pairs,
                f"quality taxonomy.mergeable_codes["
                f"{len(duplicate_merge_pairs) - 1}]",
            ),
        )

        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-taxonomy-invalid-"
        ) as temporary:
            root = Path(temporary)
            manifest = replace(self.manifest, root=root)
            for name, field_path, value, error_path in cases:
                with self.subTest(name=name):
                    taxonomy = copy.deepcopy(original)
                    self._mutate_policy_path(
                        taxonomy, field_path, value, delete
                    )
                    self._write_taxonomy(root, taxonomy)
                    with self.assertRaises(ConfigurationError) as raised:
                        load_taxonomy(manifest)
                    self.assertIn(error_path, str(raised.exception))

    def test_quality_taxonomy_read_errors_are_configuration_errors(self) -> None:
        cases = (("missing", None), ("invalid-json", "{"), ("non-object", "[]"))
        for name, payload in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory(
                prefix="tome4-quality-taxonomy-read-error-"
            ) as temporary:
                root = Path(temporary)
                if payload is not None:
                    path = root / "i18n" / "quality" / "taxonomy-v1.json"
                    path.parent.mkdir(parents=True)
                    path.write_text(payload, encoding="utf-8")
                with self.assertRaises(ConfigurationError) as raised:
                    load_taxonomy(replace(self.manifest, root=root))
                self.assertIn("quality taxonomy.root", str(raised.exception))

    def test_invalid_taxonomy_blocks_downstream_quality_inputs(self) -> None:
        taxonomy = self._current_taxonomy()
        taxonomy["profiles"] = True
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-taxonomy-preflight-"
        ) as temporary:
            root = Path(temporary)
            self._write_taxonomy(root, taxonomy)
            self._write_policy(root, self._current_policy())
            manifest = replace(self.manifest, root=root)
            loader = Mock(spec=LocaleLoader)

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
                patch.object(
                    quality_module, "_load_terminology"
                ) as load_terminology_mock,
            ):
                with self.assertRaises(ConfigurationError):
                    build_inventory(manifest, loader)
            load_policy_mock.assert_called_once_with(manifest)
            load_taxonomy_mock.assert_called_once_with(manifest)
            load_terminology_mock.assert_not_called()
            loader.load_path.assert_not_called()

            with patch.object(
                quality_module, "read_inventory_file"
            ) as read_inventory_mock:
                with self.assertRaises(ConfigurationError):
                    generate_sample(manifest, root / "unused-inventory.jsonl")
            read_inventory_mock.assert_not_called()

    def test_invalid_policy_blocks_all_inventory_inputs(self) -> None:
        policy = copy.deepcopy(self._current_policy())
        policy["dry_run"]["coverage_constraints"][0]["values"] = [True]
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-inventory-preflight-"
        ) as temporary:
            root = Path(temporary)
            self._write_policy(root, policy)
            manifest = replace(self.manifest, root=root)
            loader = Mock(spec=LocaleLoader)

            with (
                patch.object(
                    quality_module, "load_taxonomy"
                ) as load_taxonomy_mock,
                patch.object(
                    quality_module, "_load_terminology"
                ) as load_terminology_mock,
            ):
                with self.assertRaises(ConfigurationError) as raised:
                    build_inventory(manifest, loader)

        self.assertIn(
            "quality policy.dry_run.coverage_constraints[0].values[0]",
            str(raised.exception),
        )
        load_taxonomy_mock.assert_not_called()
        load_terminology_mock.assert_not_called()
        loader.load_path.assert_not_called()

    def test_inventory_loads_config_once_in_preflight_order(self) -> None:
        policy = self._current_policy()
        taxonomy = self._current_taxonomy()
        component = replace(
            self.manifest.components[0],
            translation="fixture.lua",
            copy_fragment=None,
        )
        manifest = replace(self.manifest, components=(component,))
        loader = Mock(spec=LocaleLoader)
        document = LocaleDocument(
            logical_path="fixture.lua",
            sha256="0" * 64,
            records=(),
        )
        events: list[str] = []

        def tracked_policy(candidate: Manifest) -> dict[str, object]:
            self.assertIs(candidate, manifest)
            events.append("policy")
            return policy

        def tracked_taxonomy(candidate: Manifest) -> dict[str, object]:
            self.assertIs(candidate, manifest)
            events.append("taxonomy")
            return taxonomy

        def tracked_terminology(path: Path) -> tuple[list[dict[str, str]], str]:
            self.assertEqual(path, manifest.root / manifest.terminology)
            events.append("terminology")
            return [], "1" * 64

        def tracked_locale(*args: object, **kwargs: object) -> LocaleDocument:
            events.append("locale")
            return document

        loader.load_path.side_effect = tracked_locale
        with (
            patch.object(
                quality_module,
                "load_quality_policy",
                side_effect=tracked_policy,
            ) as load_policy_mock,
            patch.object(
                quality_module,
                "load_taxonomy",
                side_effect=tracked_taxonomy,
            ) as load_taxonomy_mock,
            patch.object(
                quality_module,
                "_load_terminology",
                side_effect=tracked_terminology,
            ) as load_terminology_mock,
        ):
            inventory = build_inventory(manifest, loader)

        canonical = lambda value: hashlib.sha256(  # noqa: E731
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(events, ["policy", "taxonomy", "terminology", "locale"])
        load_policy_mock.assert_called_once_with(manifest)
        load_taxonomy_mock.assert_called_once_with(manifest)
        load_terminology_mock.assert_called_once_with(
            manifest.root / manifest.terminology
        )
        loader.load_path.assert_called_once_with(
            manifest.root / "fixture.lua", logical_path="fixture.lua"
        )
        self.assertEqual(inventory["policy_sha256"], canonical(policy))
        self.assertEqual(inventory["taxonomy_sha256"], canonical(taxonomy))

    def test_quality_policy_loads_current_file_without_normalization(self) -> None:
        original = self._current_policy()
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-valid-"
        ) as temporary:
            root = Path(temporary)
            self._write_policy(root, copy.deepcopy(original))
            manifest = replace(self.manifest, root=root)
            loaded = load_quality_policy(manifest)

        canonical = lambda value: hashlib.sha256(  # noqa: E731
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(loaded, original)
        self.assertEqual(canonical(loaded), canonical(original))
        with patch.object(quality_module, "_read_json", return_value=original):
            self.assertIs(load_quality_policy(self.manifest), original)

    def test_quality_policy_rejects_malformed_consumed_fields(self) -> None:
        delete = object()
        cases = (
            ("strict-missing", ("strict_unknown_fields",), delete, "quality policy.strict_unknown_fields"),
            ("strict-int", ("strict_unknown_fields",), 1, "quality policy.strict_unknown_fields"),
            ("pilot-missing", ("pilot",), delete, "quality policy.pilot"),
            ("pilot-not-object", ("pilot",), [], "quality policy.pilot"),
            ("pilot-seed-empty", ("pilot", "seed"), "", "quality policy.pilot.seed"),
            ("pilot-size-bool", ("pilot", "size"), True, "quality policy.pilot.size"),
            ("pilot-size-string", ("pilot", "size"), "120", "quality policy.pilot.size"),
            ("pilot-size-zero", ("pilot", "size"), 0, "quality policy.pilot.size"),
            ("buckets-not-object", ("pilot", "buckets"), [], "quality policy.pilot.buckets"),
            (
                "bucket-missing",
                ("pilot", "buckets", "contrast"),
                delete,
                "quality policy.pilot.buckets.contrast",
            ),
            (
                "bucket-extra",
                ("pilot", "buckets"),
                {"representative": 60, "risk-enriched": 40, "contrast": 20, "extra": 1},
                "quality policy.pilot.buckets['extra']",
            ),
            (
                "bucket-string",
                ("pilot", "buckets", "representative"),
                "60",
                "quality policy.pilot.buckets.representative",
            ),
            (
                "bucket-bool",
                ("pilot", "buckets", "representative"),
                True,
                "quality policy.pilot.buckets.representative",
            ),
            (
                "bucket-sum",
                ("pilot", "buckets", "representative"),
                61,
                "quality policy.pilot.buckets",
            ),
            (
                "one-evaluator",
                ("pilot", "evaluator_ids"),
                ["reviewer-a"],
                "quality policy.pilot.evaluator_ids",
            ),
            (
                "empty-evaluator",
                ("pilot", "evaluator_ids"),
                ["reviewer-a", ""],
                "quality policy.pilot.evaluator_ids[1]",
            ),
            (
                "duplicate-evaluator",
                ("pilot", "evaluator_ids"),
                ["same", "same"],
                "quality policy.pilot.evaluator_ids[1]",
            ),
            (
                "method-version-empty",
                ("pilot", "method_version"),
                "",
                "quality policy.pilot.method_version",
            ),
            ("dry-run-missing", ("dry_run",), delete, "quality policy.dry_run"),
            ("dry-run-not-object", ("dry_run",), [], "quality policy.dry_run"),
            ("dry-seed-empty", ("dry_run", "seed"), "", "quality policy.dry_run.seed"),
            ("dry-size-string", ("dry_run", "size"), "12", "quality policy.dry_run.size"),
            ("dry-size-bool", ("dry_run", "size"), True, "quality policy.dry_run.size"),
            (
                "dry-contract",
                ("dry_run", "contract"),
                "wrong-contract",
                "quality policy.dry_run.contract",
            ),
            (
                "dry-constraints-missing",
                ("dry_run", "coverage_constraints"),
                delete,
                "quality policy.dry_run.coverage_constraints",
            ),
            (
                "constraints-missing",
                ("coverage_constraints",),
                delete,
                "quality policy.coverage_constraints",
            ),
            (
                "risk-flags-not-list",
                ("risk_enrichment_flags",),
                {},
                "quality policy.risk_enrichment_flags",
            ),
            (
                "risk-flag-empty",
                ("risk_enrichment_flags",),
                [""],
                "quality policy.risk_enrichment_flags[0]",
            ),
            (
                "risk-flag-duplicate",
                ("risk_enrichment_flags",),
                ["same", "same"],
                "quality policy.risk_enrichment_flags[1]",
            ),
            (
                "groups-not-object",
                ("component_groups",),
                [],
                "quality policy.component_groups",
            ),
            (
                "group-empty-name",
                ("component_groups",),
                {"": ["engine"]},
                "quality policy.component_groups['']",
            ),
            (
                "group-members-not-list",
                ("component_groups", "core"),
                "engine",
                "quality policy.component_groups['core']",
            ),
            (
                "group-member-empty",
                ("component_groups", "core"),
                [""],
                "quality policy.component_groups['core'][0]",
            ),
            (
                "group-member-duplicate",
                ("component_groups", "core"),
                ["engine", "engine"],
                "quality policy.component_groups['core'][1]",
            ),
            (
                "component-crosses-groups",
                ("component_groups",),
                {"a": ["shared"], "b": ["shared"]},
                "quality policy.component_groups['b'][0]",
            ),
            (
                "neighbor-limit-bool",
                ("context_neighbor_limit",),
                True,
                "quality policy.context_neighbor_limit",
            ),
            (
                "neighbor-limit-negative",
                ("context_neighbor_limit",),
                -1,
                "quality policy.context_neighbor_limit",
            ),
            (
                "contrast-max-float",
                ("contrast_group_max_size",),
                6.0,
                "quality policy.contrast_group_max_size",
            ),
            (
                "contrast-max-small",
                ("contrast_group_max_size",),
                1,
                "quality policy.contrast_group_max_size",
            ),
        )

        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-invalid-"
        ) as temporary:
            root = Path(temporary)
            manifest = replace(self.manifest, root=root)
            for name, field_path, value, error_path in cases:
                with self.subTest(name=name):
                    policy = copy.deepcopy(self._current_policy())
                    self._mutate_policy_path(policy, field_path, value, delete)
                    self._write_policy(root, policy)
                    with self.assertRaises(ConfigurationError) as raised:
                        load_quality_policy(manifest)
                    self.assertIn(error_path, str(raised.exception))

    def test_quality_policy_rejects_malformed_constraints(self) -> None:
        valid_string = {
            "id": "fixture",
            "mode": "each",
            "feature": "profile",
            "min": 0,
            "values": ["fixture-profile"],
            "description": "fixture",
        }
        cases = (
            ("root-not-list", ("coverage_constraints",), {}, "quality policy.coverage_constraints"),
            ("item-not-object", ("coverage_constraints",), [[]], "quality policy.coverage_constraints[0]"),
            (
                "id-empty",
                ("coverage_constraints",),
                [{**valid_string, "id": ""}],
                "quality policy.coverage_constraints[0].id",
            ),
            (
                "id-duplicate",
                ("coverage_constraints",),
                [valid_string, {**valid_string}],
                "quality policy.coverage_constraints[1].id",
            ),
            (
                "mode-unknown",
                ("coverage_constraints",),
                [{**valid_string, "mode": "all"}],
                "quality policy.coverage_constraints[0].mode",
            ),
            (
                "mode-unhashable",
                ("coverage_constraints",),
                [{**valid_string, "mode": []}],
                "quality policy.coverage_constraints[0].mode",
            ),
            (
                "feature-unknown",
                ("coverage_constraints",),
                [{**valid_string, "feature": "taxonomy-only"}],
                "quality policy.coverage_constraints[0].feature",
            ),
            (
                "feature-unhashable",
                ("coverage_constraints",),
                [{**valid_string, "feature": {}}],
                "quality policy.coverage_constraints[0].feature",
            ),
            (
                "min-bool",
                ("coverage_constraints",),
                [{**valid_string, "min": True}],
                "quality policy.coverage_constraints[0].min",
            ),
            (
                "min-negative",
                ("coverage_constraints",),
                [{**valid_string, "min": -1}],
                "quality policy.coverage_constraints[0].min",
            ),
            (
                "values-empty",
                ("coverage_constraints",),
                [{**valid_string, "values": []}],
                "quality policy.coverage_constraints[0].values",
            ),
            (
                "value-unhashable",
                ("coverage_constraints",),
                [{**valid_string, "values": [["nested"]]}],
                "quality policy.coverage_constraints[0].values[0]",
            ),
            (
                "value-duplicate",
                ("coverage_constraints",),
                [{**valid_string, "values": ["same", "same"]}],
                "quality policy.coverage_constraints[0].values[1]",
            ),
            (
                "string-feature-bool",
                ("coverage_constraints",),
                [{**valid_string, "values": [True]}],
                "quality policy.coverage_constraints[0].values[0]",
            ),
            (
                "bool-feature-int",
                ("coverage_constraints",),
                [
                    {
                        **valid_string,
                        "feature": "structural_risk",
                        "values": [1],
                    }
                ],
                "quality policy.coverage_constraints[0].values[0]",
            ),
            (
                "description-not-string",
                ("coverage_constraints",),
                [{**valid_string, "description": None}],
                "quality policy.coverage_constraints[0].description",
            ),
            (
                "dry-not-list",
                ("dry_run", "coverage_constraints"),
                {},
                "quality policy.dry_run.coverage_constraints",
            ),
            (
                "dry-id-empty",
                ("dry_run", "coverage_constraints"),
                [{**valid_string, "id": ""}],
                "quality policy.dry_run.coverage_constraints[0].id",
            ),
        )

        delete = object()
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-constraint-invalid-"
        ) as temporary:
            root = Path(temporary)
            manifest = replace(self.manifest, root=root)
            for name, field_path, value, error_path in cases:
                with self.subTest(name=name):
                    policy = copy.deepcopy(self._current_policy())
                    self._mutate_policy_path(policy, field_path, value, delete)
                    self._write_policy(root, policy)
                    with self.assertRaises(ConfigurationError) as raised:
                        load_quality_policy(manifest)
                    self.assertIn(error_path, str(raised.exception))

    def test_quality_policy_does_not_cross_validate_taxonomy_values(self) -> None:
        policy = copy.deepcopy(self._current_policy())
        policy["coverage_constraints"] = [
            {
                "id": "unknown-profile",
                "mode": "each",
                "feature": "profile",
                "min": 0,
                "values": ["not-in-taxonomy"],
            },
            {
                "id": "unknown-component-group",
                "mode": "any",
                "feature": "component_group",
                "min": 0,
                "values": ["not-in-component-groups"],
            },
        ]
        policy["risk_enrichment_flags"] = ["not-in-taxonomy"]
        policy["component_groups"] = {"fixture-group": ["fixture-component"]}
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-no-taxonomy-"
        ) as temporary:
            root = Path(temporary)
            self._write_policy(root, policy)
            loaded = load_quality_policy(replace(self.manifest, root=root))
        self.assertEqual(loaded, policy)

    def test_generate_sample_rejects_policy_before_taxonomy_or_inventory(self) -> None:
        policy = copy.deepcopy(self._current_policy())
        policy["pilot"]["evaluator_ids"] = ["reviewer-a"]
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-preflight-"
        ) as temporary:
            root = Path(temporary)
            self._write_policy(root, policy)
            manifest = replace(self.manifest, root=root)
            with (
                patch.object(quality_module, "load_taxonomy") as load_taxonomy_mock,
                patch.object(
                    quality_module, "read_inventory_file"
                ) as read_inventory_mock,
            ):
                with self.assertRaises(ConfigurationError) as raised:
                    generate_sample(manifest, root / "unused-inventory.jsonl")
        self.assertIn(
            "quality policy.pilot.evaluator_ids", str(raised.exception)
        )
        load_taxonomy_mock.assert_not_called()
        read_inventory_mock.assert_not_called()

    def test_quality_policy_read_errors_are_configuration_errors(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-quality-policy-read-error-"
        ) as temporary:
            root = Path(temporary)
            path = root / "i18n" / "quality" / "policy-v1.json"
            path.parent.mkdir(parents=True)
            manifest = replace(self.manifest, root=root)
            for name, payload in (("invalid-json", "{"), ("non-object", "[]")):
                with self.subTest(name=name):
                    path.write_text(payload, encoding="utf-8")
                    with self.assertRaises(ConfigurationError) as raised:
                        load_quality_policy(manifest)
                    self.assertIn("quality policy", str(raised.exception))

    def test_quality_config_schemas_reject_non_integer_versions(self) -> None:
        cases = (
            (
                load_taxonomy,
                "taxonomy-v1.json",
                "tome4-quality-taxonomy-v1",
                "unsupported quality taxonomy schema",
            ),
            (
                load_quality_policy,
                "policy-v1.json",
                "tome4-quality-policy-v1",
                "unsupported quality policy schema",
            ),
        )
        with tempfile.TemporaryDirectory(prefix="tome4-quality-config-") as temporary:
            root = Path(temporary)
            quality_root = root / "i18n" / "quality"
            quality_root.mkdir(parents=True)
            manifest = replace(self.manifest, root=root)
            for loader, filename, contract, message in cases:
                for schema_version in (True, 1.0):
                    with self.subTest(
                        loader=loader.__name__, schema_version=schema_version
                    ):
                        (quality_root / filename).write_text(
                            json.dumps(
                                {
                                    "schema_version": schema_version,
                                    "contract": contract,
                                }
                            ),
                            encoding="utf-8",
                        )
                        with self.assertRaisesRegex(ConfigurationError, message):
                            loader(manifest)


class QualityIdentityTests(unittest.TestCase):
    """Phase-1 doc section 10.1: identity and invalidation semantics."""

    VERSION = "tome-1.7.6"

    def test_unit_id_matches_stable_entry_id(self) -> None:
        unit_id = compute_unit_id("tome", "data/talents/a.lua", "Rune of Reflection", None)
        self.assertEqual(
            unit_id,
            stable_entry_id("tome", "data/talents/a.lua", "Rune of Reflection", None),
        )

    def _revision(
        self,
        source: str,
        target: str,
        *,
        section: str = "s",
        source_tag: str | None = None,
        args_order: object = None,
        special: object = None,
        version: str = VERSION,
    ) -> str:
        unit_id = compute_unit_id("tome", section, source, source_tag)
        tu_uid = compute_tu_uid("tome", section, source, source_tag)
        revision_uid_value = compute_revision_uid(tu_uid, source)
        return compute_revision_id(
            version,
            unit_id,
            target,
            args_order,
            special,
            tu_uid=tu_uid,
            revision_uid_value=revision_uid_value,
            source=source,
        )

    def test_target_change_changes_revision(self) -> None:
        self.assertNotEqual(
            self._revision("source", "甲"),
            self._revision("source", "乙"),
        )

    def test_args_order_special_version_change_revision(self) -> None:
        base = self._revision("%s has %d", "%d 属于 %s", args_order=[2, 1])
        self.assertNotEqual(
            base, self._revision("%s has %d", "%d 属于 %s")
        )
        self.assertNotEqual(
            base, self._revision("%s has %d", "%d 属于 %s", args_order=[2, 1], special={"x": 1})
        )
        self.assertNotEqual(
            base, self._revision("%s has %d", "%d 属于 %s", args_order=[2, 1], version="tome-1.8.0")
        )

    def test_source_section_tag_change_unit_and_revision(self) -> None:
        self.assertNotEqual(
            self._revision("source", "target"),
            self._revision("source", "target", section="s2"),
        )
        self.assertNotEqual(
            self._revision("source", "target"),
            self._revision("source", "target", source_tag="say"),
        )
        self.assertNotEqual(
            self._revision("source", "target"),
            self._revision("source2", "target"),
        )

    def test_source_change_changes_revision_via_revision_uid(self) -> None:
        # Pilot A bridge: source change alters the source revision uid and
        # therefore the quality revision even when the TU stays the same.
        self.assertNotEqual(
            self._revision("source", "target"),
            self._revision("source2", "target"),
        )

    def test_revision_identity_ignores_lines_and_ordinals(self) -> None:
        revision = self._revision("source", "target")
        self.assertEqual(revision, self._revision("source", "target"))
        self.assertRegex(revision, r"^[0-9a-f]{64}$")

    def test_editorial_fallback_tu_is_deterministic(self) -> None:
        # Unmapped editorials fall back to the domain-separated
        # tu/fallback-editorial scheme, matching findings._bind.
        unit_id = compute_unit_id("tome", "s", "source", None)
        tu_uid = compute_tu_uid("tome", "s", "source", None)
        self.assertEqual(tu_uid, tu_uid_fallback(unit_id))
        self.assertNotEqual(tu_uid, unit_id)
        self.assertRegex(tu_uid, r"^[0-9a-f]{64}$")


class QualityStructureTests(unittest.TestCase):
    """Phase-1 doc section 10.2: structure and classification semantics."""

    def test_percent_percent_is_not_a_format_token(self) -> None:
        structure = structure_signature("100%% chance", "100%% 几率", None)
        self.assertEqual(structure["printf"]["source_raw"], [])
        self.assertEqual(structure["printf"]["target_raw"], [])

    def test_args_order_permutation_role_order(self) -> None:
        structure = structure_signature("%s has %d", "%d 属于 %s", [2, 1])
        self.assertEqual(structure["printf"]["source_conversions"], ["s", "d"])
        self.assertEqual(structure["printf"]["role_order"], ["d", "s"])
        self.assertEqual(structure["printf"]["target_conversions"], ["d", "s"])

    def test_markup_and_token_multisets(self) -> None:
        structure = structure_signature(
            "#GREEN#hit #RED#x#LAST#", "#GREEN#命中 #RED#x#LAST#", None
        )
        self.assertEqual(
            structure["markup"]["source"],
            {"#GREEN#": 1, "#RED#": 1, "#LAST#": 1},
        )
        self.assertEqual(structure["markup"]["source"], structure["markup"]["target"])
        self.assertEqual(structure["newlines"], {"source": 0, "target": 0})
        self.assertFalse(structure["multiline"])

    def test_invalid_args_order_yields_no_role_order(self) -> None:
        structure = structure_signature("%s has %d", "%s has %d", [1])
        self.assertIsNone(structure["printf"]["role_order"])

    def test_longer_overlapping_term_is_not_shadowed(self) -> None:
        from i18nlib.quality import _build_term_index, _relevant_terms_for

        rows = [
            {
                "source": "fire",
                "target": "火焰",
                "category": "T.GAME.DAMAGE",
                "domain": "combat",
                "source_tag": "damage type",
                "status": "preferred",
                "scope": "core",
                "notes": "",
            },
            {
                "source": "fire damage",
                "target": "火焰伤害",
                "category": "T.GAME.MISC",
                "domain": "combat",
                "source_tag": "damage type",
                "status": "existing",
                "scope": "core",
                "notes": "",
            },
        ]
        records, matcher, by_plain, nested_terms = _build_term_index(rows)
        terms = _relevant_terms_for(
            "fire damage on hit",
            "damage type",
            "tome",
            records,
            matcher,
            by_plain,
            nested_terms,
        )
        matched = [term["source"] for term in terms]
        self.assertIn("fire", matched)
        self.assertIn("fire damage", matched)
        # boundary must still prevent prefix matches inside words
        self.assertEqual(
            _relevant_terms_for(
                "fireball", "damage type", "tome", records, matcher, by_plain
            ),
            [],
        )

    def test_nested_term_index_matches_workset_at_ascii_boundaries(self) -> None:
        import re

        from i18nlib.quality import _build_term_index, _relevant_terms_for

        def term(
            source: str,
            target: str,
            *,
            source_tag: str = "_t",
            scope: str = "core",
        ) -> dict[str, str]:
            return {
                "source": source,
                "target": target,
                "category": "T.GAME.MISC",
                "domain": "combat",
                "source_tag": source_tag,
                "status": "preferred",
                "scope": scope,
                "notes": "fixture",
            }

        rows = [
            term("fire", "火焰"),
            term("fire damage", "火焰伤害"),
            term("light", "光系"),
            term("light", "光明"),
            term("light", "轻", source_tag="entity subtype"),
            term("light", "邪光", scope="dlc"),
            term("holy light", "圣光"),
            term("read", "读取"),
            term("dread", "惊骇"),
            term("Choker of Dread", "噩灵护符"),
            term("previous level", "前往上一层"),
            term("way to the previous level", "通往上一层的路"),
            term("through shadow", "穿过暗影"),
            term("passage through shadow realm", "暗影界通道"),
            term("delightful aura", "愉悦光环"),
        ]
        records, matcher, by_plain, nested_terms = _build_term_index(rows)
        self.assertIsNotNone(matcher)
        assert matcher is not None

        # Duplicate context rows remain addressable through by_plain, while
        # the expensive matcher and containment scan use each plain once.
        self.assertEqual(len(by_plain["light"]), 4)
        unique_plains = sorted(
            by_plain, key=lambda plain: (-len(plain), plain)
        )
        self.assertEqual(
            matcher.pattern,
            r"(?<![a-z0-9_])("
            + "|".join(re.escape(plain) for plain in unique_plains)
            + r")(?![a-z0-9_])",
        )

        self.assertIn("fire", nested_terms["fire damage"])
        self.assertIn("light", nested_terms["holy light"])
        self.assertIn("dread", nested_terms["choker of dread"])
        self.assertIn(
            "previous level", nested_terms["way to the previous level"]
        )
        self.assertIn(
            "through shadow", nested_terms["passage through shadow realm"]
        )
        self.assertNotIn("light", nested_terms.get("delightful aura", []))
        self.assertNotIn("read", nested_terms.get("choker of dread", []))

        expected_targets = {
            "fire damage": {"火焰", "火焰伤害"},
            "holy light": {"光系", "光明", "圣光"},
            "Choker of Dread": {"惊骇", "噩灵护符"},
            "way to the previous level": {"前往上一层", "通往上一层的路"},
            "passage through shadow realm": {"穿过暗影", "暗影界通道"},
            "delightful aura": {"愉悦光环"},
        }

        def applicable_key(row: dict[str, object]) -> tuple[object, ...]:
            return (
                row["source"],
                row["target"],
                row["category"],
                row["source_tag"],
                row["status"],
                row["scope"],
                row["notes"],
            )

        for entry_id, (source, targets) in enumerate(expected_targets.items()):
            with self.subTest(source=source):
                item = {
                    "entry_id": f"nested-{entry_id}",
                    "source": source,
                    "source_tag": "_t",
                }
                workset_terms = _relevant_terms(rows, [item], "tome")
                quality_terms = _relevant_terms_for(
                    source,
                    "_t",
                    "tome",
                    records,
                    matcher,
                    by_plain,
                    nested_terms,
                )
                self.assertEqual(
                    {term_row["target"] for term_row in quality_terms},
                    targets,
                )
                self.assertEqual(
                    {applicable_key(term_row) for term_row in quality_terms},
                    {applicable_key(term_row) for term_row in workset_terms},
                )

    def test_relevant_terms_carry_domain(self) -> None:
        from i18nlib.quality import _build_term_index, _relevant_terms_for

        rows = [
            {
                "source": "physical",
                "target": "物理",
                "category": "T.GAME.DAMAGE",
                "domain": "combat",
                "source_tag": "damage type",
                "status": "preferred",
                "scope": "core",
                "notes": "",
            }
        ]
        records, matcher, by_plain, _ = _build_term_index(rows)
        terms = _relevant_terms_for(
            "physical damage", "damage type", "tome", records, matcher, by_plain
        )
        self.assertEqual(len(terms), 1)
        self.assertEqual(terms[0]["domain"], "combat")
        self.assertEqual(terms[0]["match"], "partial")

    def test_section_patterns_are_segment_aware(self) -> None:
        from i18nlib.quality import classify_profile

        taxonomy = {
            "source_tag_profiles": {},
            "term_category_profiles": {},
            "section_pattern_profiles": [
                {"pattern": "ui", "profile": "ui", "confidence": "low"},
                {"pattern": "data/talents", "profile": "mechanics", "confidence": "high"},
            ],
        }
        # 'ui' must not match 'guilds' or 'quiz' as a bare substring;
        # punctuation keeps the source out of the structure fallback
        profile, _ = classify_profile(
            "Guild master!", None, "data/guilds/foo.lua", [], taxonomy
        )
        self.assertNotEqual(profile, "ui")
        profile, _ = classify_profile(
            "Quiz time?", None, "data/quiz/foo.lua", [], taxonomy
        )
        self.assertNotEqual(profile, "ui")
        # exact segment 'ui' still matches at any depth
        profile, confidence = classify_profile(
            "Quit", None, "data/dialogs/ui/foo.lua", [], taxonomy
        )
        self.assertEqual((profile, confidence), ("ui", "low"))
        # multi-segment patterns must appear as a contiguous segment sequence
        profile, confidence = classify_profile(
            "Bolt", None, "data/talents/mage/foo.lua", [], taxonomy
        )
        self.assertEqual((profile, confidence), ("mechanics", "high"))
        profile, _ = classify_profile(
            "Bolt", None, "data/talents_mage/foo.lua", [], taxonomy
        )
        self.assertNotEqual(profile, "mechanics")

    def test_profile_confidence_votes_use_semantic_order(self) -> None:
        from i18nlib.quality import classify_profile

        for first, second, expected in (
            ("high", "low", "high"),
            ("high", "medium", "high"),
            ("medium", "low", "medium"),
        ):
            with self.subTest(confidences=(first, second)):
                taxonomy = {
                    "source_tag_profiles": {},
                    "term_category_profiles": {},
                    "section_pattern_profiles": [
                        {
                            "pattern": "data",
                            "profile": "ui",
                            "confidence": first,
                        },
                        {
                            "pattern": "ui",
                            "profile": "ui",
                            "confidence": second,
                        },
                    ],
                }
                self.assertEqual(
                    classify_profile(
                        "Quit", None, "data/ui/foo.lua", [], taxonomy
                    ),
                    ("ui", expected),
                )

        conflicting_taxonomy = {
            "source_tag_profiles": {"talent": "mechanics"},
            "term_category_profiles": {},
            "section_pattern_profiles": [
                {"pattern": "ui", "profile": "ui", "confidence": "high"}
            ],
        }
        self.assertEqual(
            classify_profile(
                "Bolt",
                "talent",
                "data/ui/foo.lua",
                [],
                conflicting_taxonomy,
            ),
            ("mechanics", "low"),
        )

        single_vote_taxonomy = {
            "source_tag_profiles": {},
            "term_category_profiles": {},
            "section_pattern_profiles": [
                {"pattern": "ui", "profile": "ui", "confidence": "medium"}
            ],
        }
        self.assertEqual(
            classify_profile(
                "Quit", None, "data/ui/foo.lua", [], single_vote_taxonomy
            ),
            ("ui", "medium"),
        )
        self.assertEqual(
            classify_profile(
                "Quit",
                None,
                "data/dialogs/foo.lua",
                [],
                {
                    "source_tag_profiles": {},
                    "term_category_profiles": {},
                    "section_pattern_profiles": [],
                },
            ),
            ("ui", "low"),
        )


if __name__ == "__main__":
    unittest.main()
