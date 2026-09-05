"""Toolchain tests: quality validation."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import TEST_FIXTURE_ROOT, _UNSET
import copy
import contextlib
from dataclasses import replace
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import i18nlib.quality as quality_module
from i18nlib import TOOL_VERSION
from i18nlib.config import Manifest, load_manifest
from i18nlib.cli import main as cli_main
from i18nlib.errors import ValidationError
from i18nlib.locale_model import LocaleLoader
from i18nlib.quality import (
    ADJUDICATION_CONTRACT,
    ASSESSMENT_CONTRACT,
    SAMPLE_CONTRACT,
    compute_revision_id,
    compute_revision_uid,
    compute_tu_uid,
    compute_unit_id,
    generate_dry_run,
    generate_sample,
    load_quality_policy,
    load_taxonomy,
    run_report as run_quality_report,
    run_validation as run_quality_validation,
    structure_signature,
    validate_quality_run,
)


class QualityValidationFlagPreflightTests(unittest.TestCase):
    """Validation control flags fail before any artifact I/O."""

    manifest = SimpleNamespace(
        root=Path("/fixture-root"),
        version="fixture-version",
    )
    sample_path = Path("unused-sample.json")
    assessment_path = Path("unused-assessment.json")

    def _assert_rejected_without_io(
        self,
        function: object,
        *,
        strict: object,
        dry_run: object,
        expected_message: str,
    ) -> None:
        with (
            patch.object(quality_module, "load_taxonomy") as load_taxonomy_mock,
            patch.object(
                quality_module, "load_quality_policy"
            ) as load_quality_policy_mock,
            patch.object(quality_module, "_read_json") as read_json_mock,
            patch.object(
                quality_module, "_load_sample_file"
            ) as load_sample_file_mock,
            patch.object(
                quality_module, "_load_assessment"
            ) as load_assessment_mock,
            patch.object(
                quality_module, "create_quality_run_directory"
            ) as create_run_directory,
            patch.object(quality_module, "_write_jsonl") as write_jsonl_mock,
            patch.object(quality_module, "write_json") as write_json_mock,
        ):
            with self.assertRaisesRegex(ValidationError, expected_message):
                function(
                    self.manifest,
                    sample_path=self.sample_path,
                    assessment_paths=[self.assessment_path],
                    adjudication_path=None,
                    strict=strict,
                    dry_run=dry_run,
                )

        for mocked in (
            load_taxonomy_mock,
            load_quality_policy_mock,
            read_json_mock,
            load_sample_file_mock,
            load_assessment_mock,
            create_run_directory,
            write_jsonl_mock,
            write_json_mock,
        ):
            mocked.assert_not_called()

    def test_invalid_control_flag_types_fail_before_io(self) -> None:
        cases = (
            ("strict-zero", 0, False, "strict flag must be None or an exact bool"),
            ("strict-one", 1, False, "strict flag must be None or an exact bool"),
            (
                "strict-string",
                "false",
                False,
                "strict flag must be None or an exact bool",
            ),
            (
                "strict-float",
                1.0,
                False,
                "strict flag must be None or an exact bool",
            ),
            ("dry-zero", True, 0, "dry_run flag must be an exact bool"),
            ("dry-one", True, 1, "dry_run flag must be an exact bool"),
            ("dry-none", True, None, "dry_run flag must be an exact bool"),
            (
                "dry-string",
                True,
                "false",
                "dry_run flag must be an exact bool",
            ),
        )
        functions = (
            quality_module.validate_quality_run,
            quality_module.run_validation,
        )
        for function in functions:
            for label, strict, dry_run, expected_message in cases:
                with self.subTest(function=function.__name__, case=label):
                    self._assert_rejected_without_io(
                        function,
                        strict=strict,
                        dry_run=dry_run,
                        expected_message=expected_message,
                    )

    def test_valid_control_flags_continue_into_mocked_downstream(self) -> None:
        strict_cases = (
            (None, False, False),
            (None, True, True),
            (False, True, False),
            (True, False, True),
        )
        functions = (
            quality_module.validate_quality_run,
            quality_module.run_validation,
        )
        run_directory = (
            self.manifest.root
            / ".artifacts"
            / "i18n"
            / "quality"
            / "runs"
            / "fixture-validation"
        )
        for function in functions:
            for strict, policy_default, expected_strict in strict_cases:
                for dry_run in (False, True):
                    with self.subTest(
                        function=function.__name__,
                        strict=strict,
                        policy_default=policy_default,
                        dry_run=dry_run,
                    ):
                        taxonomy = {"contract": "fixture-taxonomy"}
                        policy = {
                            "strict_unknown_fields": policy_default,
                            "pilot": {
                                "evaluator_ids": ["reviewer-a", "reviewer-b"],
                                "method_version": "fixture-method-v1",
                            },
                        }
                        sample = {
                            "quality_contract": SAMPLE_CONTRACT,
                            "sample_id": "a" * 64,
                            "items_sha256": "c" * 64,
                            "items": [{"revision_id": "b" * 64}],
                        }
                        assessment = {
                            "evaluator_id": "reviewer-a",
                            "evaluator": {
                                "id": "reviewer-a",
                                "kind": "human",
                            },
                            "items": [],
                        }
                        with (
                            patch.object(
                                quality_module,
                                "load_taxonomy",
                                return_value=taxonomy,
                            ) as load_taxonomy_mock,
                            patch.object(
                                quality_module,
                                "load_quality_policy",
                                return_value=policy,
                            ) as load_quality_policy_mock,
                            patch.object(
                                quality_module, "_read_json"
                            ) as read_json_mock,
                            patch.object(
                                quality_module,
                                "_load_sample_file",
                                return_value=sample,
                            ) as load_sample_file_mock,
                            patch.object(
                                quality_module,
                                "_load_assessment",
                                return_value=(assessment, []),
                            ) as load_assessment_mock,
                            patch.object(
                                quality_module,
                                "_validate_assessment_items",
                                return_value=(assessment, []),
                            ) as validate_assessment_items,
                            patch.object(
                                quality_module,
                                "create_quality_run_directory",
                                return_value=run_directory,
                            ) as create_run_directory,
                            patch.object(
                                quality_module, "_write_jsonl"
                            ) as write_jsonl_mock,
                            patch.object(
                                quality_module, "write_json"
                            ) as write_json_mock,
                        ):
                            result = function(
                                self.manifest,
                                sample_path=self.sample_path,
                                assessment_paths=[self.assessment_path],
                                adjudication_path=None,
                                strict=strict,
                                dry_run=dry_run,
                            )

                        self.assertIs(result["strict"], expected_strict)
                        load_taxonomy_mock.assert_called_once_with(self.manifest)
                        load_quality_policy_mock.assert_called_once_with(
                            self.manifest
                        )
                        read_json_mock.assert_not_called()
                        load_sample_file_mock.assert_called_once_with(
                            self.sample_path,
                            manifest=self.manifest,
                            taxonomy=taxonomy,
                            qpolicy=policy,
                            dry_run=dry_run,
                        )
                        self.assertIs(
                            load_assessment_mock.call_args.args[3],
                            expected_strict,
                        )
                        self.assertIs(
                            validate_assessment_items.call_args.args[3],
                            expected_strict,
                        )
                        if function is quality_module.run_validation:
                            create_run_directory.assert_called_once_with(
                                self.manifest.root, "validation"
                            )
                            write_jsonl_mock.assert_called_once()
                            write_json_mock.assert_called_once()
                        else:
                            self.assertIs(result["dry_run"], dry_run)
                            create_run_directory.assert_not_called()
                            write_jsonl_mock.assert_not_called()
                            write_json_mock.assert_not_called()


class QualityValidationTests(unittest.TestCase):
    """Phase-1 doc section 10.4: assessment/adjudication safety checks."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.qpolicy = load_quality_policy(cls.manifest)
        cls.taxonomy = load_taxonomy(cls.manifest)
        cls.sample, cls.sample_path, cls.inventory_path = cls._make_sample()
        cls.dry_sample = generate_dry_run(cls.manifest, cls.inventory_path)
        cls.dry_sample_path = TEST_FIXTURE_ROOT / "quality-validation" / "dry-run.json"
        cls.dry_sample_path.write_text(
            json.dumps(cls.dry_sample, ensure_ascii=False), encoding="utf-8"
        )

    @classmethod
    def _make_sample(cls) -> tuple[dict[str, object], Path, Path]:
        entries = [
            cls._sample_entry(index)
            for index in range(320)
        ]
        directory = TEST_FIXTURE_ROOT / "quality-validation"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "inventory.jsonl"
        path.write_text(
            "\n".join(
                json.dumps(entry, ensure_ascii=False, sort_keys=True) for entry in entries
            )
            + "\n",
            encoding="utf-8",
        )
        path.with_name("inventory-manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "quality_contract": quality_module.INVENTORY_CONTRACT,
                    "tool_version": TOOL_VERSION,
                    "version": cls.manifest.version,
                    "manifest_sha256": hashlib.sha256(
                        cls.manifest.raw_bytes
                    ).hexdigest(),
                    "translation_inputs_sha256": (
                        quality_module._current_translation_inputs_sha256(
                            cls.manifest
                        )
                    ),
                    "identity_indexes_sha256": (
                        quality_module._identity_indexes_sha256(cls.manifest)
                    ),
                    "terminology_sha256": (
                        quality_module.terminology_store_sha256(
                            cls.manifest.root / cls.manifest.terminology
                        )
                    ),
                    "taxonomy_sha256": quality_module._canonical_sha256(
                        cls.taxonomy
                    ),
                    "policy_sha256": quality_module._canonical_sha256(
                        cls.qpolicy
                    ),
                    "inventory_sha256": quality_module._canonical_sha256(
                        entries
                    ),
                    "entries": len(entries),
                    "profile_classifier_version": cls.taxonomy[
                        "profile_classifier_version"
                    ],
                    "risk_rule_version": cls.taxonomy["risk_rule_version"],
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        sample = generate_sample(
            cls.manifest, path, seed="quality-validation-fixture"
        )
        sample_path = directory / "sample.json"
        sample_path.write_text(
            json.dumps(sample, ensure_ascii=False), encoding="utf-8"
        )
        return sample, sample_path, path

    @classmethod
    def _sample_entry(cls, index: int) -> dict[str, object]:
        unit_id = compute_unit_id("tome", "data/v.lua", f"source {index}", None)
        tu_uid = compute_tu_uid("tome", "data/v.lua", f"source {index}", None)
        revision_uid_value = compute_revision_uid(tu_uid, f"source {index}")
        revision_id = compute_revision_id(
            cls.manifest.version,
            unit_id,
            f"target {index}",
            None,
            None,
            tu_uid=tu_uid,
            revision_uid_value=revision_uid_value,
            source=f"source {index}",
        )
        structure = structure_signature(f"source {index}", f"target {index}", None)
        return {
            "unit_id": unit_id,
            "tu_uid": tu_uid,
            "revision_uid": revision_uid_value,
            "revision_id": revision_id,
            "version": cls.manifest.version,
            "component": "tome",
            "section": "data/v.lua",
            "source": f"source {index}",
            "target": f"target {index}",
            "source_tag": None,
            "args_order": None,
            "special": None,
            "occurrences": [
                {
                    "logical_path": "tome.lua",
                    "section": "data/v.lua",
                    "line": index + 1,
                    "ordinal": index,
                }
            ],
            "profile": "mechanics",
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

    def _assessment(
        self, evaluator_id: str, sample: dict[str, object]
    ) -> dict[str, object]:
        return {
            "schema_version": 1,
            "quality_contract": ASSESSMENT_CONTRACT,
            "sample_id": sample["sample_id"],
            "evaluator": {
                "kind": "human",
                "id": evaluator_id,
                "method_version": self.qpolicy["pilot"]["method_version"],
            },
            "items": [
                {
                    "revision_id": item["revision_id"],
                    "context_sufficient": True,
                    "profile_confirmed": item["profile"],
                    "findings": [],
                    "reuse_recommendation": "same-tag",
                }
                for item in sample["items"]
            ],
        }

    def _adjudication(
        self, sample: dict[str, object], assessments: list[dict[str, object]]
    ) -> dict[str, object]:
        return {
            "schema_version": 1,
            "quality_contract": ADJUDICATION_CONTRACT,
            "sample_id": sample["sample_id"],
            "items": [
                {
                    "revision_id": item["revision_id"],
                    "assessment_ids": [
                        assessment["evaluator"]["id"] for assessment in assessments
                    ],
                    "context_sufficient": True,
                    "resolved_findings": [],
                    "quality_vector": {
                        "accuracy": 4,
                        "mechanics_context": 4,
                        "terminology": 4,
                        "fluency": 4,
                        "style": None,
                        "ui_render": None,
                        "corpus_consistency": 4,
                    },
                    "confidence": "C3",
                    "provisional_grade": "Gold",
                    "reuse_scope": "same-tag",
                    "rationale": "fixture adjudication",
                }
                for item in sample["items"]
            ],
        }

    def _write(self, name: str, payload: dict[str, object]) -> Path:
        path = TEST_FIXTURE_ROOT / "quality-validation" / name
        path.write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )
        return path

    def _isolated_upstream_sample(
        self, root: Path
    ) -> tuple[Manifest, dict[str, object], Path]:
        translation_path = root / "canonical.lua"
        copy_fragment_path = root / "copy-fragment.lua"
        terminology_path = root / "terminology" / "fixture.tsv"
        terminology_path.parent.mkdir(parents=True, exist_ok=True)
        translation_path.write_bytes(b"-- canonical translation fixture\n")
        copy_fragment_path.write_bytes(b"-- copy fragment fixture\n")
        terminology_path.write_bytes(b"fixture terminology bytes\n")
        component = replace(
            self.manifest.component("tome"),
            translation="canonical.lua",
            copy_fragment="copy-fragment.lua",
        )
        manifest = replace(
            self.manifest,
            root=root,
            components=(component,),
            terminology="terminology/",
        )
        sample = copy.deepcopy(self.sample)
        sample["translation_inputs_sha256"] = (
            quality_module._current_translation_inputs_sha256(manifest)
        )
        sample["terminology_sha256"] = hashlib.sha256(
            terminology_path.read_bytes()
        ).hexdigest()
        sample["inventory_tool_version"] = TOOL_VERSION
        self._resign_sample(sample)
        sample_path = root / "sample.json"
        sample_path.write_text(
            json.dumps(sample, ensure_ascii=False), encoding="utf-8"
        )
        return manifest, sample, sample_path

    @staticmethod
    def _resign_sample(payload: dict[str, object]) -> None:
        common_fields = [
            "schema_version",
            "quality_contract",
            "seed",
            "size",
            "items_sha256",
        ]
        if payload["quality_contract"] == SAMPLE_CONTRACT:
            identity_fields = common_fields + [
                "taxonomy_sha256",
                "policy_sha256",
                "manifest_sha256",
                "translation_inputs_sha256",
                "terminology_sha256",
                "inventory_tool_version",
                "inventory_sha256",
                "bucket_targets",
                "bucket_counts",
                "revisions",
            ]
        else:
            identity_fields = common_fields + [
                "official_sample_id",
                "taxonomy_sha256",
                "policy_sha256",
                "manifest_sha256",
                "translation_inputs_sha256",
                "terminology_sha256",
                "inventory_tool_version",
                "inventory_sha256",
                "revisions",
            ]
        identity = {field: payload[field] for field in identity_fields}
        payload["sample_id"] = hashlib.sha256(
            json.dumps(
                identity,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    def _valid_run(
        self,
        assessment_a: dict[str, object] | None = None,
        assessment_b: dict[str, object] | None = None,
        adjudication: dict[str, object] | None = None,
        strict: bool = True,
    ) -> tuple[dict[str, object], ...]:
        a = assessment_a or self._assessment("reviewer-a", self.sample)
        b = assessment_b or self._assessment("reviewer-b", self.sample)
        adjudication = adjudication or self._adjudication(self.sample, [a, b])
        a_path = self._write("assessment-a.json", a)
        b_path = self._write("assessment-b.json", b)
        adjudication_path = self._write("adjudication.json", adjudication)
        return (
            validate_quality_run(
                self.manifest,
                sample_path=self.sample_path,
                assessment_paths=[a_path, b_path],
                adjudication_path=adjudication_path,
                strict=strict,
            ),
            a,
            b,
            adjudication,
        )

    def _resolved_finding_inputs(
        self,
    ) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        assessment_a = self._assessment("reviewer-a", self.sample)
        assessment_b = self._assessment("reviewer-b", self.sample)
        assessment_a["items"][0]["findings"] = [
            {
                "finding_id": "A-REF",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "source_span": "",
                "target_span": "",
                "body": "fixture assessment finding",
                "evidence_refs": [],
            }
        ]
        adjudication = self._adjudication(
            self.sample, [assessment_a, assessment_b]
        )
        adjudication["items"][0]["resolved_findings"] = [
            {
                "finding_id": "A-REF",
                "evaluator_id": "reviewer-a",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "state": "rejected",
                "body": "",
            }
        ]
        return assessment_a, assessment_b, adjudication

    def test_clean_pilot_validates(self) -> None:
        validation, _, _, _ = self._valid_run()
        self.assertTrue(validation["ok"])
        self.assertEqual(validation["errors"], [])

    def test_upstream_byte_changes_reject_old_sample_before_assessment_io(
        self,
    ) -> None:
        cases = (
            (
                "translation",
                "canonical.lua",
                "sample translation_inputs_sha256 is stale or invalid",
            ),
            (
                "copy-fragment",
                "copy-fragment.lua",
                "sample translation_inputs_sha256 is stale or invalid",
            ),
            (
                "terminology",
                "terminology/fixture.tsv",
                "sample terminology_sha256 is stale or invalid",
            ),
        )
        for label, relative_path, expected_error in cases:
            with self.subTest(input=label), tempfile.TemporaryDirectory(
                prefix=f"quality-upstream-{label}-"
            ) as temporary:
                root = Path(temporary)
                manifest, _, sample_path = self._isolated_upstream_sample(root)
                changed_path = root / relative_path
                changed_path.write_bytes(changed_path.read_bytes() + b"-- changed\n")
                with (
                    patch.object(
                        quality_module,
                        "load_taxonomy",
                        return_value=self.taxonomy,
                    ),
                    patch.object(
                        quality_module,
                        "load_quality_policy",
                        return_value=self.qpolicy,
                    ),
                    patch.object(
                        quality_module, "_load_assessment"
                    ) as load_assessment,
                ):
                    with self.assertRaisesRegex(
                        ValidationError, expected_error
                    ):
                        validate_quality_run(
                            manifest,
                            sample_path=sample_path,
                            assessment_paths=[root / "must-not-be-read.json"],
                            adjudication_path=None,
                            strict=True,
                        )
                load_assessment.assert_not_called()

    def test_sample_freshness_validation_does_not_rebuild_inventory_or_load_lua(
        self,
    ) -> None:
        with (
            patch.object(quality_module, "build_inventory") as build_inventory_mock,
            patch.object(LocaleLoader, "load_path") as load_path_mock,
        ):
            validation, _, _, _ = self._valid_run()

        self.assertTrue(validation["ok"], validation["errors"])
        build_inventory_mock.assert_not_called()
        load_path_mock.assert_not_called()

    def test_adjudication_resolved_finding_contract_table(self) -> None:
        assessment_a, assessment_b, adjudication = (
            self._resolved_finding_inputs()
        )
        validation, _, _, _ = self._valid_run(
            assessment_a=assessment_a,
            assessment_b=assessment_b,
            adjudication=adjudication,
            strict=True,
        )

        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(
            validation["adjudication"]["items"][0]["resolved_findings"][0][
                "body"
            ],
            "",
        )
        validation_path = self._write(
            "validation-report-resolved-finding-valid.json", validation
        )
        report = run_quality_report(self.manifest, validation_path)
        self.assertEqual(report["sample_id"], validation["sample_id"])

        cases = (
            ("finding-missing", "field", "finding_id", _UNSET,
             ".finding_id: must be a non-empty string"),
            ("finding-null", "field", "finding_id", None,
             ".finding_id: must be a non-empty string"),
            ("finding-empty", "field", "finding_id", "",
             ".finding_id: must be a non-empty string"),
            ("finding-non-string", "field", "finding_id", 7,
             ".finding_id: must be a non-empty string"),
            ("evaluator-missing", "field", "evaluator_id", _UNSET,
             ".evaluator_id: must be a non-empty string"),
            ("evaluator-null", "field", "evaluator_id", None,
             ".evaluator_id: must be a non-empty string"),
            ("evaluator-empty", "field", "evaluator_id", "",
             ".evaluator_id: must be a non-empty string"),
            ("evaluator-non-string", "field", "evaluator_id", ["reviewer-a"],
             ".evaluator_id: must be a non-empty string"),
            ("unknown-finding", "field", "finding_id", "A-GHOST",
             "does not exist in assessment"),
            ("wrong-evaluator", "field", "evaluator_id", "reviewer-b",
             "does not exist in assessment"),
            ("cross-revision", "cross-revision", None, None,
             "does not exist in assessment"),
            ("invalid-rationale", "field", "rationale", None,
             "rationale must be a string"),
        )

        def mutate(
            assessment: dict[str, object],
            adjudicated: dict[str, object],
            mutation: str,
            field: str | None,
            value: object,
        ) -> None:
            if mutation == "cross-revision":
                finding = assessment["items"][0]["findings"].pop()
                assessment["items"][1]["findings"].append(finding)
                return
            resolved = adjudicated["items"][0]["resolved_findings"][0]
            assert field is not None
            if value is _UNSET:
                resolved.pop(field)
            else:
                resolved[field] = copy.deepcopy(value)

        for label, mutation, field, value, expected_error in cases:
            with self.subTest(case=label, path="validate"):
                assessment_a, assessment_b, adjudication = (
                    self._resolved_finding_inputs()
                )
                mutate(assessment_a, adjudication, mutation, field, value)
                invalid, _, _, _ = self._valid_run(
                    assessment_a=assessment_a,
                    assessment_b=assessment_b,
                    adjudication=adjudication,
                    strict=True,
                )
                self.assertFalse(invalid["ok"], invalid["errors"])
                self.assertIn(expected_error, "\n".join(invalid["errors"]))

            with self.subTest(case=label, path="report"):
                forged = copy.deepcopy(validation)
                normalized_assessment_a = next(
                    assessment
                    for assessment in forged["assessments"]
                    if assessment["evaluator_id"] == "reviewer-a"
                )
                mutate(
                    normalized_assessment_a,
                    forged["adjudication"],
                    mutation,
                    field,
                    value,
                )
                validation_path = self._write(
                    f"validation-report-forged-resolved-{label}.json", forged
                )
                with patch.object(
                    quality_module, "create_quality_run_directory"
                ) as create_run_directory:
                    with self.assertRaisesRegex(
                        ValidationError, expected_error
                    ):
                        run_quality_report(self.manifest, validation_path)
                create_run_directory.assert_not_called()

    def test_adjudication_item_contract_table(self) -> None:
        cases = (
            (
                "single-valid-evaluator-subset",
                ["reviewer-a"],
                None,
                True,
                False,
                ("must exactly match valid assessment evaluator ids",),
            ),
            (
                "duplicate-evaluator-id",
                ["reviewer-a", "reviewer-b", "reviewer-a"],
                None,
                True,
                False,
                ("assessment_ids contains duplicates",),
            ),
            (
                "empty-id-array",
                [],
                None,
                True,
                False,
                ("assessment_ids must be a non-empty string array",),
            ),
            (
                "empty-id",
                ["reviewer-a", ""],
                None,
                True,
                False,
                ("assessment_ids[1]: must be a non-empty string",),
            ),
            (
                "object-id",
                ["reviewer-a", {"id": "reviewer-b"}],
                None,
                True,
                False,
                ("assessment_ids[1]: must be a non-empty string",),
            ),
            (
                "array-id",
                ["reviewer-a", ["reviewer-b"]],
                None,
                True,
                False,
                ("assessment_ids[1]: must be a non-empty string",),
            ),
            (
                "unknown-id",
                ["reviewer-a", "ghost-evaluator"],
                None,
                True,
                False,
                (
                    "must exactly match valid assessment evaluator ids",
                    "ghost-evaluator",
                ),
            ),
            (
                "empty-vector-nonstrict",
                _UNSET,
                "empty",
                False,
                False,
                ("quality_vector: missing dimensions",),
            ),
            (
                "missing-vector-dimension-nonstrict",
                _UNSET,
                "missing",
                False,
                False,
                ("quality_vector: missing dimensions ['accuracy']",),
            ),
            (
                "extra-vector-dimension-nonstrict",
                _UNSET,
                "extra",
                False,
                False,
                ("quality_vector: extra dimensions ['undeclared']",),
            ),
            (
                "boolean-vector-value",
                _UNSET,
                "boolean",
                True,
                False,
                ("quality_vector.accuracy: must be 0-4 or null",),
            ),
            (
                "float-vector-value",
                _UNSET,
                "float",
                True,
                False,
                ("quality_vector.accuracy: must be 0-4 or null",),
            ),
            (
                "valid-reversed-evaluator-order",
                ["reviewer-b", "reviewer-a"],
                None,
                True,
                True,
                (),
            ),
        )
        for (
            label,
            assessment_ids,
            vector_mutation,
            strict,
            expected_ok,
            expected_errors,
        ) in cases:
            with self.subTest(case=label):
                assessment_a = self._assessment("reviewer-a", self.sample)
                assessment_b = self._assessment("reviewer-b", self.sample)
                adjudication = self._adjudication(
                    self.sample, [assessment_a, assessment_b]
                )
                item = adjudication["items"][0]
                if assessment_ids is not _UNSET:
                    item["assessment_ids"] = copy.deepcopy(assessment_ids)
                vector = item["quality_vector"]
                if vector_mutation == "empty":
                    item["quality_vector"] = {}
                elif vector_mutation == "missing":
                    vector.pop("accuracy")
                elif vector_mutation == "extra":
                    vector["undeclared"] = 4
                elif vector_mutation == "boolean":
                    vector["accuracy"] = True
                elif vector_mutation == "float":
                    vector["accuracy"] = 4.0

                validation, _, _, _ = self._valid_run(
                    assessment_a=assessment_a,
                    assessment_b=assessment_b,
                    adjudication=adjudication,
                    strict=strict,
                )

                self.assertEqual(
                    validation["ok"], expected_ok, validation["errors"]
                )
                joined_errors = "\n".join(validation["errors"])
                for expected_error in expected_errors:
                    self.assertIn(expected_error, joined_errors)
                if expected_ok:
                    self.assertEqual(validation["errors"], [])
                    self.assertEqual(
                        validation["adjudication"]["items"][0][
                            "assessment_ids"
                        ],
                        assessment_ids,
                    )
                    self.assertEqual(
                        validation["sample_id"], self.sample["sample_id"]
                    )

    def test_dry_run_explicit_adjudication_binds_actual_assessments(self) -> None:
        cases = (
            ("one-exact", ("reviewer-a",), ("reviewer-a",), True),
            (
                "one-with-unprovided-evaluator",
                ("reviewer-a",),
                ("reviewer-a", "reviewer-b"),
                False,
            ),
            (
                "two-subset",
                ("reviewer-a", "reviewer-b"),
                ("reviewer-a",),
                False,
            ),
            (
                "two-reversed",
                ("reviewer-a", "reviewer-b"),
                ("reviewer-b", "reviewer-a"),
                True,
            ),
        )
        for label, evaluator_ids, adjudicated_ids, expected_ok in cases:
            with self.subTest(case=label):
                assessments = [
                    self._assessment(evaluator_id, self.dry_sample)
                    for evaluator_id in evaluator_ids
                ]
                assessment_paths = [
                    self._write(
                        f"assessment-dry-adjudication-{label}-{index}.json",
                        assessment,
                    )
                    for index, assessment in enumerate(assessments)
                ]
                adjudication = self._adjudication(
                    self.dry_sample, assessments
                )
                for item in adjudication["items"]:
                    item["assessment_ids"] = list(adjudicated_ids)
                adjudication_path = self._write(
                    f"adjudication-dry-{label}.json", adjudication
                )

                validation = validate_quality_run(
                    self.manifest,
                    sample_path=self.dry_sample_path,
                    assessment_paths=assessment_paths,
                    adjudication_path=adjudication_path,
                    strict=False,
                    dry_run=True,
                )

                self.assertEqual(
                    validation["ok"], expected_ok, validation["errors"]
                )
                if not expected_ok:
                    self.assertTrue(
                        any(
                            "must exactly match valid assessment evaluator ids"
                            in error
                            for error in validation["errors"]
                        ),
                        validation["errors"],
                    )

    def test_official_assessment_policy_binding_table(self) -> None:
        expected_method = self.qpolicy["pilot"]["method_version"]
        cases = (
            (
                "single-policy-evaluator-with-adjudication",
                (("reviewer-a", expected_method),),
                ("exactly two valid assessments",),
            ),
            (
                "single-typo-and-obsolete-method",
                (("reviewer-typo", "mqm-pilot-v0"),),
                ("evaluator.id", "evaluator.method_version"),
            ),
            (
                "two-with-wrong-id",
                (
                    ("reviewer-a", expected_method),
                    ("reviewer-typo", expected_method),
                ),
                ("evaluator.id",),
            ),
            (
                "two-with-wrong-method",
                (
                    ("reviewer-a", expected_method),
                    ("reviewer-b", "mqm-pilot-v0"),
                ),
                ("evaluator.method_version",),
            ),
        )
        for label, evaluator_specs, expected_errors in cases:
            with self.subTest(case=label):
                assessments = []
                assessment_paths = []
                for index, (evaluator_id, method_version) in enumerate(
                    evaluator_specs
                ):
                    assessment = self._assessment(evaluator_id, self.sample)
                    assessment["evaluator"]["method_version"] = method_version
                    assessments.append(assessment)
                    assessment_paths.append(
                        self._write(f"assessment-policy-{label}-{index}.json", assessment)
                    )
                adjudication_path = self._write(
                    f"adjudication-policy-{label}.json",
                    self._adjudication(self.sample, assessments),
                )

                validation = validate_quality_run(
                    self.manifest,
                    sample_path=self.sample_path,
                    assessment_paths=assessment_paths,
                    adjudication_path=adjudication_path,
                    strict=True,
                )

                self.assertFalse(validation["ok"])
                joined_errors = "\n".join(validation["errors"])
                for expected_error in expected_errors:
                    self.assertIn(expected_error, joined_errors)

    def test_official_assessment_order_is_irrelevant_for_validate_and_report(
        self,
    ) -> None:
        assessment_a = self._assessment("reviewer-a", self.sample)
        assessment_b = self._assessment("reviewer-b", self.sample)
        assessment_a_path = self._write("assessment-order-a.json", assessment_a)
        assessment_b_path = self._write("assessment-order-b.json", assessment_b)
        adjudication_path = self._write(
            "adjudication-order.json",
            self._adjudication(self.sample, [assessment_a, assessment_b]),
        )

        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[assessment_b_path, assessment_a_path],
            adjudication_path=adjudication_path,
            strict=True,
        )

        self.assertTrue(validation["ok"], validation["errors"])
        self.assertEqual(
            {assessment["evaluator_id"] for assessment in validation["assessments"]},
            {"reviewer-a", "reviewer-b"},
        )
        validation_path = self._write("validation-order-valid.json", validation)
        report = run_quality_report(self.manifest, validation_path)
        self.assertEqual(report["sample_id"], validation["sample_id"])

    def test_assessment_and_adjudication_schemas_reject_non_integer_versions(
        self,
    ) -> None:
        for artifact in ("assessment", "adjudication"):
            for schema_version in (True, 1.0):
                with self.subTest(
                    artifact=artifact, schema_version=schema_version
                ):
                    if artifact == "assessment":
                        assessment = self._assessment("reviewer-a", self.sample)
                        assessment["schema_version"] = schema_version
                        validation, _, _, _ = self._valid_run(
                            assessment_a=assessment
                        )
                    else:
                        assessment_a = self._assessment(
                            "reviewer-a", self.sample
                        )
                        assessment_b = self._assessment(
                            "reviewer-b", self.sample
                        )
                        adjudication = self._adjudication(
                            self.sample, [assessment_a, assessment_b]
                        )
                        adjudication["schema_version"] = schema_version
                        validation, _, _, _ = self._valid_run(
                            assessment_a=assessment_a,
                            assessment_b=assessment_b,
                            adjudication=adjudication,
                        )
                    self.assertFalse(validation["ok"])
                    self.assertTrue(
                        any(
                            f"unsupported {artifact} schema" in error
                            for error in validation["errors"]
                        ),
                        validation["errors"],
                    )

    def test_sample_file_schema_rejects_booleans_and_floats(self) -> None:
        for schema_version in (True, 1.0):
            with self.subTest(schema_version=schema_version):
                sample = json.loads(json.dumps(self.sample))
                sample["schema_version"] = schema_version
                sample_path = self._write(
                    f"sample-schema-{str(schema_version).lower()}.json",
                    sample,
                )
                with self.assertRaisesRegex(
                    ValidationError, "unsupported sample schema"
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                    )

    def test_report_embedded_sample_schema_rejects_booleans_and_floats(
        self,
    ) -> None:
        validation, _, _, _ = self._valid_run()
        for schema_version in (True, 1.0):
            with self.subTest(schema_version=schema_version):
                payload = json.loads(json.dumps(validation))
                payload["sample"]["schema_version"] = schema_version
                validation_path = self._write(
                    f"validation-sample-schema-{str(schema_version).lower()}.json",
                    payload,
                )
                with self.assertRaisesRegex(
                    ValidationError, "quality validation sample schema is invalid"
                ):
                    run_quality_report(self.manifest, validation_path)

    def test_report_rejects_failed_validation_with_multiple_errors(self) -> None:
        validation, _, _, _ = self._valid_run()
        validation["ok"] = False
        validation["errors"] = ["first fixture failure", "second fixture failure"]
        validation_path = self._write("validation-report-failed.json", validation)

        with self.assertRaises(ValidationError) as caught:
            run_quality_report(self.manifest, validation_path)
        self.assertIn("first fixture failure", str(caught.exception))
        self.assertIn("second fixture failure", str(caught.exception))

    def test_report_rejects_missing_or_invalid_ok(self) -> None:
        validation, _, _, _ = self._valid_run()
        cases = (("missing", None), ("string", "true"), ("integer", 1))
        for label, value in cases:
            with self.subTest(case=label):
                payload = json.loads(json.dumps(validation))
                if label == "missing":
                    payload.pop("ok")
                else:
                    payload["ok"] = value
                validation_path = self._write(
                    f"validation-report-{label}.json", payload
                )
                with self.assertRaisesRegex(
                    ValidationError, "quality validation ok flag is invalid"
                ):
                    run_quality_report(self.manifest, validation_path)

    def test_report_rejects_nonempty_errors_when_ok_is_true(self) -> None:
        validation, _, _, _ = self._valid_run()
        validation["errors"] = ["inconsistent success"]
        validation_path = self._write(
            "validation-report-inconsistent.json", validation
        )

        with self.assertRaisesRegex(ValidationError, "inconsistent success"):
            run_quality_report(self.manifest, validation_path)

    def test_report_rejects_validation_from_stale_quality_rules(self) -> None:
        validation, _, _, _ = self._valid_run()
        for field in ("taxonomy_sha256", "policy_sha256"):
            with self.subTest(field=field):
                stale = json.loads(json.dumps(validation))
                stale[field] = "0" * 64
                validation_path = self._write(
                    f"validation-report-stale-{field}.json", stale
                )
                with self.assertRaisesRegex(
                    ValidationError, rf"{field} is stale or invalid"
                ):
                    run_quality_report(self.manifest, validation_path)

        stale_manifest = json.loads(json.dumps(validation))
        stale_manifest["sample"]["manifest_sha256"] = "0" * 64
        self._resign_sample(stale_manifest["sample"])
        stale_manifest["sample_id"] = stale_manifest["sample"]["sample_id"]
        validation_path = self._write(
            "validation-report-stale-manifest.json", stale_manifest
        )
        with self.assertRaisesRegex(
            ValidationError, "sample manifest_sha256 is stale or invalid"
        ):
            run_quality_report(self.manifest, validation_path)

    def test_report_rejects_old_validation_tool_version_before_output(
        self,
    ) -> None:
        validation, _, _, _ = self._valid_run()
        for label, value in (("missing", _UNSET), ("old", "0.0.0")):
            with self.subTest(case=label):
                payload = copy.deepcopy(validation)
                if value is _UNSET:
                    payload.pop("tool_version")
                else:
                    payload["tool_version"] = value
                validation_path = self._write(
                    f"validation-report-tool-version-{label}.json", payload
                )
                with patch.object(
                    quality_module, "create_quality_run_directory"
                ) as create_run_directory:
                    with self.assertRaisesRegex(
                        ValidationError,
                        "tool_version does not match the current tool version",
                    ):
                        run_quality_report(self.manifest, validation_path)
                create_run_directory.assert_not_called()

    def test_report_rechecks_embedded_upstream_dependency_before_output(
        self,
    ) -> None:
        validation, _, _, _ = self._valid_run()
        payload = copy.deepcopy(validation)
        payload["sample"]["translation_inputs_sha256"] = "0" * 64
        self._resign_sample(payload["sample"])
        payload["sample_id"] = payload["sample"]["sample_id"]
        validation_path = self._write(
            "validation-report-stale-translation-inputs.json", payload
        )

        with patch.object(
            quality_module, "create_quality_run_directory"
        ) as create_run_directory:
            with self.assertRaisesRegex(
                ValidationError,
                "sample translation_inputs_sha256 is stale or invalid",
            ):
                run_quality_report(self.manifest, validation_path)
        create_run_directory.assert_not_called()

    def test_report_rechecks_embedded_full_item_payload_digest(self) -> None:
        validation, _, _, _ = self._valid_run()
        validation["sample"]["items"][0]["context_neighbors"].append(
            {
                "component": "tome",
                "section": "data/forged-report-context.lua",
                "source": "forged report context",
                "target": "伪造报告上下文",
                "source_tag": None,
            }
        )
        validation_path = self._write(
            "validation-report-forged-item-payload.json", validation
        )

        with patch.object(
            quality_module, "create_quality_run_directory"
        ) as create_run_directory:
            with self.assertRaisesRegex(
                ValidationError, "items_sha256 does not match items"
            ):
                run_quality_report(self.manifest, validation_path)
        create_run_directory.assert_not_called()

    def test_report_accepts_successful_validation(self) -> None:
        validation, _, _, _ = self._valid_run()
        validation_path = self._write("validation-report-valid.json", validation)

        report = run_quality_report(self.manifest, validation_path)

        self.assertEqual(report["sample_id"], validation["sample_id"])
        self.assertEqual(report["size"], len(self.sample["items"]))
        self.assertTrue((self.manifest.root / report["report_path"]).is_file())
        self.assertTrue((self.manifest.root / report["report_md"]).is_file())

    def test_report_rejects_forged_successful_assessment_identities_before_io(
        self,
    ) -> None:
        official, _, _, _ = self._valid_run()
        official_single = copy.deepcopy(official)
        official_single["assessments"] = official_single["assessments"][:1]

        official_wrong_id = copy.deepcopy(official)
        official_wrong_id["assessments"][1]["evaluator_id"] = "reviewer-typo"
        official_wrong_id["assessments"][1]["evaluator"]["id"] = "reviewer-typo"

        official_wrong_method = copy.deepcopy(official)
        official_wrong_method["assessments"][1]["evaluator"][
            "method_version"
        ] = "mqm-pilot-v0"

        official_mismatched_normalized_id = copy.deepcopy(official)
        official_mismatched_normalized_id["assessments"][1][
            "evaluator_id"
        ] = "reviewer-a"

        dry_assessment = self._assessment("reviewer-a", self.dry_sample)
        dry_assessment_path = self._write(
            "assessment-report-dry-valid.json", dry_assessment
        )
        dry_validation = validate_quality_run(
            self.manifest,
            sample_path=self.dry_sample_path,
            assessment_paths=[dry_assessment_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        self.assertTrue(dry_validation["ok"], dry_validation["errors"])

        dry_wrong_id = copy.deepcopy(dry_validation)
        dry_wrong_id["assessments"][0]["evaluator_id"] = "reviewer-typo"
        dry_wrong_id["assessments"][0]["evaluator"]["id"] = "reviewer-typo"

        dry_wrong_method = copy.deepcopy(dry_validation)
        dry_wrong_method["assessments"][0]["evaluator"][
            "method_version"
        ] = "mqm-pilot-v0"

        cases = (
            ("official-single", official_single, "exactly two assessments"),
            ("official-wrong-id", official_wrong_id, "evaluator.id"),
            (
                "official-wrong-method",
                official_wrong_method,
                "evaluator.method_version",
            ),
            (
                "official-normalized-id-mismatch",
                official_mismatched_normalized_id,
                "evaluator_id does not match",
            ),
            ("dry-wrong-id", dry_wrong_id, "evaluator.id"),
            ("dry-wrong-method", dry_wrong_method, "evaluator.method_version"),
        )
        for label, payload, expected_error in cases:
            with self.subTest(case=label):
                validation_path = self._write(
                    f"validation-report-forged-{label}.json", payload
                )
                with patch.object(
                    quality_module, "create_quality_run_directory"
                ) as create_run_directory:
                    with self.assertRaisesRegex(ValidationError, expected_error):
                        run_quality_report(self.manifest, validation_path)
                create_run_directory.assert_not_called()

    def test_report_rejects_forged_adjudication_contract_before_io(self) -> None:
        validation, _, _, _ = self._valid_run()
        cases = (
            ("assessment-subset", "assessment", "must exactly match"),
            ("non-string-assessment", "non-string", "non-empty string"),
            ("missing-vector-dimension", "missing", "missing dimensions"),
            ("extra-vector-dimension", "extra", "extra dimensions"),
        )
        for label, mutation, expected_error in cases:
            with self.subTest(case=label):
                payload = copy.deepcopy(validation)
                item = payload["adjudication"]["items"][0]
                if mutation == "assessment":
                    item["assessment_ids"] = ["reviewer-a"]
                elif mutation == "non-string":
                    item["assessment_ids"] = [
                        "reviewer-a",
                        {"id": "reviewer-b"},
                    ]
                elif mutation == "missing":
                    item["quality_vector"].pop("accuracy")
                elif mutation == "extra":
                    payload["strict"] = False
                    item["quality_vector"]["undeclared"] = 4
                validation_path = self._write(
                    f"validation-report-forged-adjudication-{label}.json",
                    payload,
                )

                with patch.object(
                    quality_module, "create_quality_run_directory"
                ) as create_run_directory:
                    with self.assertRaisesRegex(
                        ValidationError, expected_error
                    ):
                        run_quality_report(self.manifest, validation_path)
                create_run_directory.assert_not_called()

    def test_quality_report_cli_rejects_failure_and_accepts_success(self) -> None:
        validation, _, _, _ = self._valid_run()
        failed = {
            **validation,
            "ok": False,
            "errors": ["first fixture failure", "second fixture failure"],
        }
        failed_path = self._write("validation-report-cli-failed.json", failed)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = cli_main(
                [
                    "quality",
                    "report",
                    "--validation",
                    str(failed_path),
                    "--json",
                ]
            )
        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertNotIn("OK  quality report", stdout.getvalue())
        self.assertIn("first fixture failure", stderr.getvalue())
        self.assertIn("second fixture failure", stderr.getvalue())

        valid_path = self._write("validation-report-cli-valid.json", validation)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = cli_main(
                [
                    "quality",
                    "report",
                    "--validation",
                    str(valid_path),
                    "--json",
                ]
            )
        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(json.loads(stdout.getvalue())["sample_id"], validation["sample_id"])

    def test_current_official_and_dry_run_sample_identities_validate(self) -> None:
        validation, _, _, _ = self._valid_run()
        self.assertTrue(validation["ok"])

        assessment = self._assessment("reviewer-a", self.dry_sample)
        assessment_path = self._write("assessment-valid-dry-run.json", assessment)
        dry_validation = validate_quality_run(
            self.manifest,
            sample_path=self.dry_sample_path,
            assessment_paths=[assessment_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        self.assertTrue(dry_validation["ok"])

    def test_full_item_payload_tampering_keeps_old_id_and_is_rejected(self) -> None:
        assessment_a = self._assessment("reviewer-a", self.sample)
        assessment_b = self._assessment("reviewer-b", self.sample)
        adjudication = self._adjudication(
            self.sample, [assessment_a, assessment_b]
        )
        assessment_a_path = self._write(
            "assessment-item-payload-a.json", assessment_a
        )
        assessment_b_path = self._write(
            "assessment-item-payload-b.json", assessment_b
        )
        adjudication_path = self._write(
            "adjudication-item-payload.json", adjudication
        )

        def mutate_relevant_terms(item: dict[str, object]) -> None:
            item["relevant_terms"].append(
                {
                    "source": "forged term",
                    "target": "伪造术语",
                    "status": "preferred",
                }
            )

        def mutate_gate_signals(item: dict[str, object]) -> None:
            item["gate_signals"]["needs_review"].append("forged-signal")

        def mutate_context(item: dict[str, object]) -> None:
            item["context_neighbors"].append(
                {
                    "component": "tome",
                    "section": "data/forged.lua",
                    "source": "forged context",
                    "target": "伪造上下文",
                    "source_tag": None,
                }
            )

        def mutate_risk_flags(item: dict[str, object]) -> None:
            item["risk_flags"].append("forged-risk")

        cases = (
            ("relevant-terms", mutate_relevant_terms),
            ("gate-signals", mutate_gate_signals),
            ("context-neighbors", mutate_context),
            ("risk-flags", mutate_risk_flags),
        )
        for label, mutate in cases:
            with self.subTest(field=label):
                sample = copy.deepcopy(self.sample)
                original_sample_id = sample["sample_id"]
                mutate(sample["items"][0])
                self.assertEqual(sample["sample_id"], original_sample_id)
                sample_path = self._write(
                    f"tampered-item-payload-{label}.json", sample
                )

                with self.assertRaisesRegex(
                    ValidationError, "items_sha256 does not match items"
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[
                            assessment_a_path,
                            assessment_b_path,
                        ],
                        adjudication_path=adjudication_path,
                        strict=True,
                    )

    def test_items_digest_shape_and_binding_for_both_contracts(self) -> None:
        missing = object()
        mutations = (
            (
                "missing",
                missing,
                "sample identity is missing items_sha256",
            ),
            (
                "uppercase",
                "A" * 64,
                "items_sha256 is not a SHA-256 digest",
            ),
            (
                "non-string",
                ["not", "a", "digest"],
                "items_sha256 is not a SHA-256 digest",
            ),
            (
                "mismatch",
                "0" * 64,
                "items_sha256 does not match items",
            ),
        )
        for contract_label, original, dry_run in (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        ):
            for mutation_label, value, expected_error in mutations:
                with self.subTest(
                    contract=contract_label, mutation=mutation_label
                ):
                    sample = copy.deepcopy(original)
                    if value is missing:
                        sample.pop("items_sha256")
                    else:
                        sample["items_sha256"] = value
                    sample_path = self._write(
                        f"items-digest-{contract_label}-{mutation_label}.json",
                        sample,
                    )

                    with self.assertRaisesRegex(
                        ValidationError, expected_error
                    ):
                        validate_quality_run(
                            self.manifest,
                            sample_path=sample_path,
                            assessment_paths=[],
                            adjudication_path=None,
                            strict=True,
                            dry_run=dry_run,
                        )

    def test_dry_run_assessment_policy_binding_table(self) -> None:
        expected_method = self.qpolicy["pilot"]["method_version"]
        cases = (
            ("valid-policy-subset", "reviewer-b", expected_method, True, None),
            (
                "wrong-id",
                "reviewer-typo",
                expected_method,
                False,
                "evaluator.id",
            ),
            (
                "wrong-method",
                "reviewer-a",
                "mqm-pilot-v0",
                False,
                "evaluator.method_version",
            ),
        )
        for label, evaluator_id, method_version, expected_ok, expected_error in cases:
            with self.subTest(case=label):
                assessment = self._assessment(evaluator_id, self.dry_sample)
                assessment["evaluator"]["method_version"] = method_version
                assessment_path = self._write(
                    f"assessment-dry-policy-{label}.json", assessment
                )

                validation = validate_quality_run(
                    self.manifest,
                    sample_path=self.dry_sample_path,
                    assessment_paths=[assessment_path],
                    adjudication_path=None,
                    strict=True,
                    dry_run=True,
                )

                self.assertEqual(validation["ok"], expected_ok)
                if expected_error is not None:
                    self.assertTrue(
                        any(
                            expected_error in error
                            for error in validation["errors"]
                        ),
                        validation["errors"],
                    )

    def test_sample_item_identity_tampering_rejected_for_both_contracts(self) -> None:
        cases = (
            ("official-target", self.sample, False, "target", "revision_id"),
            ("official-source", self.sample, False, "source", "unit_id"),
            ("dry-run-args", self.dry_sample, True, "args_order", "revision_id"),
            ("dry-run-section", self.dry_sample, True, "section", "unit_id"),
        )
        for label, original, dry_run, field, expected_error in cases:
            with self.subTest(case=label):
                sample = json.loads(json.dumps(original))
                item = sample["items"][0]
                if field == "args_order":
                    item[field] = [1]
                else:
                    item[field] += "-tampered"
                sample_path = self._write(f"tampered-{label}.json", sample)
                with self.assertRaisesRegex(
                    ValidationError,
                    rf"{expected_error} does not match",
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                        dry_run=dry_run,
                    )

    def test_malformed_item_identity_type_raises_validation_error(self) -> None:
        for label, original, dry_run in (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        ):
            with self.subTest(contract=label):
                sample = json.loads(json.dumps(original))
                sample["items"][0]["component"] = ["not", "a", "string"]
                sample_path = self._write(f"malformed-item-{label}.json", sample)
                with self.assertRaisesRegex(
                    ValidationError, "sample item 0 component is invalid"
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                        dry_run=dry_run,
                    )

    def test_stale_sample_rule_digests_rejected_for_both_contracts(self) -> None:
        samples = (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        )
        for label, original, dry_run in samples:
            for field in (
                "manifest_sha256",
                "taxonomy_sha256",
                "policy_sha256",
                "translation_inputs_sha256",
                "terminology_sha256",
            ):
                with self.subTest(contract=label, field=field):
                    sample = json.loads(json.dumps(original))
                    sample[field] = "0" * 64
                    self._resign_sample(sample)
                    sample_path = self._write(
                        f"stale-{label}-{field}.json", sample
                    )
                    with self.assertRaisesRegex(
                        ValidationError, rf"{field} is stale or invalid"
                    ):
                        validate_quality_run(
                            self.manifest,
                            sample_path=sample_path,
                            assessment_paths=[],
                            adjudication_path=None,
                            strict=True,
                            dry_run=dry_run,
                        )

    def test_stale_inventory_tool_version_rejected_for_both_contracts(
        self,
    ) -> None:
        for label, original, dry_run in (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        ):
            with self.subTest(contract=label):
                sample = copy.deepcopy(original)
                sample["inventory_tool_version"] = "0.0.0"
                self._resign_sample(sample)
                sample_path = self._write(
                    f"stale-{label}-inventory-tool-version.json", sample
                )
                with self.assertRaisesRegex(
                    ValidationError,
                    "inventory_tool_version is stale or invalid",
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                        dry_run=dry_run,
                    )

    def test_wrong_sample_artifact_id_rejected_for_both_contracts(self) -> None:
        samples = (
            ("official", self.sample, False),
            ("dry-run", self.dry_sample, True),
        )
        for label, original, dry_run in samples:
            with self.subTest(contract=label):
                sample = json.loads(json.dumps(original))
                sample["sample_id"] = "0" * 64
                sample_path = self._write(f"wrong-id-{label}.json", sample)
                with self.assertRaisesRegex(
                    ValidationError,
                    "sample_id does not match canonical sample identity",
                ):
                    validate_quality_run(
                        self.manifest,
                        sample_path=sample_path,
                        assessment_paths=[],
                        adjudication_path=None,
                        strict=True,
                        dry_run=dry_run,
                    )

    def test_inventory_digest_is_shape_checked_and_bound_to_sample_id(self) -> None:
        malformed = json.loads(json.dumps(self.sample))
        malformed["inventory_sha256"] = "not-a-digest"
        self._resign_sample(malformed)
        malformed_path = self._write("malformed-inventory-digest.json", malformed)
        with self.assertRaisesRegex(
            ValidationError, "inventory_sha256 is not a SHA-256 digest"
        ):
            validate_quality_run(
                self.manifest,
                sample_path=malformed_path,
                assessment_paths=[],
                adjudication_path=None,
                strict=True,
            )

        unbound = json.loads(json.dumps(self.sample))
        unbound["inventory_sha256"] = "0" * 64
        unbound_path = self._write("unbound-inventory-digest.json", unbound)
        with self.assertRaisesRegex(
            ValidationError, "sample_id does not match canonical sample identity"
        ):
            validate_quality_run(
                self.manifest,
                sample_path=unbound_path,
                assessment_paths=[],
                adjudication_path=None,
                strict=True,
            )

    def test_dry_run_validation_without_adjudication(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        b = self._assessment("reviewer-b", self.sample)
        a_path = self._write("assessment-a-dry.json", a)
        b_path = self._write("assessment-b-dry.json", b)
        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path, b_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        self.assertTrue(validation["ok"])
        self.assertTrue(validation["dry_run"])
        self.assertEqual(validation["adjudication"], {"items": []})
        self.assertTrue(
            any("non-official" in warning for warning in validation["warnings"])
        )

    def test_dry_run_validation_runner_forwards_flag(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        a_path = self._write("assessment-runner-dry.json", a)
        report = run_quality_validation(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        validation = json.loads(
            (self.manifest.root / report["validation_path"]).read_text(encoding="utf-8")
        )
        self.assertTrue(report["ok"])
        self.assertTrue(validation["dry_run"])

    def test_official_sample_requires_adjudication(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        a_path = self._write("assessment-a-no-adjudication.json", a)
        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path],
            adjudication_path=None,
            strict=True,
        )
        self.assertFalse(validation["ok"])
        self.assertTrue(
            any("adjudication is required" in error for error in validation["errors"])
        )

    def test_dry_run_contract_sample_accepted_with_flag(self) -> None:
        dry_sample = self.dry_sample
        sample_path = self.dry_sample_path
        a = self._assessment("reviewer-a", dry_sample)
        a_path = self._write("assessment-a-dry-contract.json", a)
        validation = validate_quality_run(
            self.manifest,
            sample_path=sample_path,
            assessment_paths=[a_path],
            adjudication_path=None,
            strict=True,
            dry_run=True,
        )
        self.assertTrue(validation["ok"])
        self.assertTrue(validation["dry_run"])
        with self.assertRaises(ValidationError):
            validate_quality_run(
                self.manifest,
                sample_path=sample_path,
                assessment_paths=[a_path],
                adjudication_path=None,
                strict=True,
            )

    def test_policy_default_strict_rejects_unknown_fields(self) -> None:
        # policy-v1 declares strict_unknown_fields=true; validate without an
        # explicit --strict flag must still reject unknown fields.
        a = self._assessment("reviewer-a", self.sample)
        a["items"][0]["unexpected_field"] = "sneaky"
        a_path = self._write("assessment-a-strict.json", a)
        b = self._assessment("reviewer-b", self.sample)
        b_path = self._write("assessment-b-strict.json", b)
        adjudication = self._adjudication(self.sample, [a, b])
        adjudication_path = self._write("adjudication-strict.json", adjudication)
        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path, b_path],
            adjudication_path=adjudication_path,
            strict=None,
        )
        self.assertFalse(validation["ok"])
        self.assertTrue(any("unknown fields" in error for error in validation["errors"]))

    def test_root_and_evaluator_unknown_fields_rejected(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        a["unexpected_root"] = "sneaky"
        a_path = self._write("assessment-a-root.json", a)
        b = self._assessment("reviewer-b", self.sample)
        b["evaluator"]["unexpected_evaluator"] = "sneaky"
        b_path = self._write("assessment-b-root.json", b)
        adjudication = self._adjudication(self.sample, [a, b])
        adjudication_path = self._write("adjudication-root.json", adjudication)
        validation = validate_quality_run(
            self.manifest,
            sample_path=self.sample_path,
            assessment_paths=[a_path, b_path],
            adjudication_path=adjudication_path,
            strict=True,
        )
        self.assertFalse(validation["ok"])
        root_errors = [
            error for error in validation["errors"] if "unexpected_root" in error
        ]
        evaluator_errors = [
            error for error in validation["errors"]
            if "unexpected_evaluator" in error
        ]
        self.assertTrue(root_errors)
        self.assertTrue(evaluator_errors)

    def test_unknown_error_code_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"][0]["findings"] = [
            {
                "finding_id": "B-001",
                "error_code": "NOT_A_CODE",
                "severity": "major",
                "source_span": "",
                "target_span": "",
                "body": "fixture",
                "evidence_refs": [],
            }
        ]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("unknown error code" in error for error in validation["errors"]))

    def test_absolute_path_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"][1]["findings"] = [
            {
                "finding_id": "B-002",
                "error_code": "ACC_MISTRANSLATION",
                "severity": "major",
                "source_span": "",
                "target_span": "",
                "body": "see /Users/yun/private/file.lua for mechanics",
                "evidence_refs": [],
            }
        ]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("host absolute path" in error for error in validation["errors"]))

    def test_duplicate_finding_id_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"][2]["findings"] = [
            {
                "finding_id": "DUP",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "source_span": "",
                "target_span": "",
                "body": "one",
                "evidence_refs": [],
            },
            {
                "finding_id": "DUP",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "source_span": "",
                "target_span": "",
                "body": "two",
                "evidence_refs": [],
            },
        ]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("duplicate finding_id" in error for error in validation["errors"]))

    def test_incomplete_coverage_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"] = b["items"][:-1]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("incomplete coverage" in error for error in validation["errors"]))

    def test_sample_id_mismatch_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["sample_id"] = "0" * 64
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("sample_id does not match" in error for error in validation["errors"]))

    def test_unknown_revision_rejected(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"][0]["revision_id"] = "1" * 64
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])
        self.assertTrue(any("unknown revision_id" in error for error in validation["errors"]))

    def test_adjudication_missing_assessment_rejected(self) -> None:
        adjudication = self._adjudication(self.sample, [])
        adjudication["items"][0]["assessment_ids"] = ["ghost-evaluator"]
        validation, _, _, _ = self._valid_run(adjudication=adjudication)
        self.assertFalse(validation["ok"])
        self.assertTrue(
            any(
                "must exactly match valid assessment evaluator ids" in error
                for error in validation["errors"]
            )
        )

    def test_gold_with_confirmed_blocker_rejected(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        b = self._assessment("reviewer-b", self.sample)
        a["items"][3]["findings"] = [
            {
                "finding_id": "A-003",
                "error_code": "TECH_FORMAT",
                "severity": "blocker",
                "source_span": "0:4",
                "target_span": "0:4",
                "body": "missing argument",
                "evidence_refs": [],
            }
        ]
        adjudication = self._adjudication(self.sample, [a, b])
        for item in adjudication["items"]:
            if item["revision_id"] == a["items"][3]["revision_id"]:
                item["resolved_findings"] = [
                    {
                        "finding_id": "A-003",
                        "evaluator_id": "reviewer-a",
                        "error_code": "TECH_FORMAT",
                        "severity": "blocker",
                        "state": "confirmed",
                        "body": "missing argument",
                    }
                ]
        validation, _, _, _ = self._valid_run(
            assessment_a=a, adjudication=adjudication
        )
        self.assertFalse(validation["ok"])
        self.assertTrue(
            any("confirmed blocker/major" in error for error in validation["errors"])
        )

    def test_rejected_finding_does_not_block_grade(self) -> None:
        a = self._assessment("reviewer-a", self.sample)
        b = self._assessment("reviewer-b", self.sample)
        a["items"][4]["findings"] = [
            {
                "finding_id": "A-004",
                "error_code": "FLU_AWKWARD",
                "severity": "minor",
                "source_span": "",
                "target_span": "",
                "body": "subjective",
                "evidence_refs": [],
            }
        ]
        adjudication = self._adjudication(self.sample, [a, b])
        for item in adjudication["items"]:
            if item["revision_id"] == a["items"][4]["revision_id"]:
                item["resolved_findings"] = [
                    {
                        "finding_id": "A-004",
                        "evaluator_id": "reviewer-a",
                        "error_code": "FLU_AWKWARD",
                        "severity": "minor",
                        "state": "rejected",
                        "body": "subjective",
                        "rationale": "not a defect",
                    }
                ]
        validation, _, _, _ = self._valid_run(
            assessment_a=a, adjudication=adjudication
        )
        self.assertTrue(validation["ok"])

    def test_assessment_must_cover_all_sample_revisions(self) -> None:
        b = self._assessment("reviewer-b", self.sample)
        b["items"] = [
            item for item in b["items"] if item["revision_id"] != b["items"][0]["revision_id"]
        ]
        validation, _, _, _ = self._valid_run(assessment_b=b)
        self.assertFalse(validation["ok"])


if __name__ == "__main__":
    unittest.main()
