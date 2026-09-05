"""Toolchain tests: review bundle."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import ROOT
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import i18nlib.quality as quality_module
from i18nlib import TOOL_VERSION
from i18nlib.config import load_manifest
from i18nlib.errors import AgentError, ValidationError
from i18nlib.locale_model import LocaleLoader
from i18nlib.pi_file_review import run_pi_file_review
from i18nlib.pi_review import (
    TRANSLATION_REVIEW_PROVIDER_CWD,
    _review_cache_key,
    _validate_findings,
    run_pi_review,
)
from i18nlib.pi_tmux import run_tmux_review
from i18nlib.review import (
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    _bundle_id,
    _redact_absolute_paths,
    _review_index_id,
    _translation_bundle_payload,
    _validate_findings_for_remediation,
    validate_review_bundle,
)
from i18nlib.runtime import LuaRuntime
from i18nlib.translation_review import (
    DEFAULT_TRANSLATION_CHARACTER_BUDGET,
    TRANSLATION_REVIEW_ASSESSMENT_CONTRACT,
    TRANSLATION_REVIEW_BUNDLE_CONTRACT,
    TRANSLATION_REVIEW_CHANNEL,
    TRANSLATION_REVIEW_NORMALIZER_CONTRACT,
    TRANSLATION_REVIEW_RUNNER_CONTRACT,
    TRANSLATION_REVIEW_SCHEMA_VERSION,
    build_translation_item,
    load_translation_review_policy,
    make_evaluator_identity,
    partition_translation_items,
    revalidate_translation_assessment,
    translation_item_character_count,
    translation_provider_message,
    translation_provider_payload,
    translation_selection_sha256,
    validate_translation_model_output,
    write_translation_inventory,
)


class ReviewBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    def _write_bundle(self, directory: Path, payload: dict[str, object]) -> Path:
        payload["bundle_id"] = _bundle_id(payload)
        path = directory / "bundle.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def _base(self, kind: str) -> dict[str, object]:
        return {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "tool_version": TOOL_VERSION,
            "version": self.manifest.version,
            "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
            "kind": kind,
        }

    def test_review_bundle_schema_rejects_non_integer_versions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-schema-") as temporary:
            directory = Path(temporary)
            for schema_version in (True, 1.0):
                with self.subTest(schema_version=schema_version):
                    payload = self._base("translations")
                    payload["schema_version"] = schema_version
                    path = self._write_bundle(directory, payload)
                    with self.assertRaisesRegex(
                        ValidationError, "unsupported review bundle schema"
                    ):
                        validate_review_bundle(self.manifest, path)

    def test_remediation_review_schema_rejects_non_integer_versions(self) -> None:
        bundle = {
            "kind": "translations",
            "bundle_id": "bundle-schema-fixture",
            "items": [],
        }
        for schema_version in (True, 1.0):
            with self.subTest(schema_version=schema_version):
                review = json.loads(
                    json.dumps(
                        {
                            "schema_version": schema_version,
                            "review_contract": REVIEW_CONTRACT,
                            "bundle_id": bundle["bundle_id"],
                            "findings": [],
                        }
                    )
                )
                with self.assertRaisesRegex(
                    ValidationError, "validated review has an unsupported schema"
                ):
                    _validate_findings_for_remediation(bundle, review)

    def test_model_review_schema_rejects_non_integer_versions(self) -> None:
        bundle = {
            "kind": "translations",
            "bundle_id": "bundle-model-schema-fixture",
            "items": [],
        }
        for schema_version in (True, 1.0):
            with self.subTest(schema_version=schema_version):
                output = json.loads(
                    json.dumps(
                        {
                            "schema_version": schema_version,
                            "review_contract": REVIEW_CONTRACT,
                            "bundle_id": bundle["bundle_id"],
                            "findings": [],
                        }
                    )
                )
                with self.assertRaisesRegex(
                    ValidationError, "Pi review has an unsupported schema"
                ):
                    _validate_findings(bundle, output, strict=False)

    def test_translation_review_bundle_is_valid(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-test-") as temporary:
            payload = self._base("translations")
            payload.update(
                {
                    "component": "boot",
                    "items": [
                        {
                            "item_id": "translation-fixture",
                            "component": "boot",
                            "section": "fixture/dialog.lua",
                            "source": "%s has %d",
                            "target": "%d 属于 %s",
                            "source_tag": "tformat",
                            "args_order": [2, 1],
                            "special": None,
                        }
                    ],
                }
            )
            path = self._write_bundle(Path(temporary), payload)
            with self.assertRaisesRegex(
                ValidationError, "historical artifacts"
            ):
                validate_review_bundle(self.manifest, path)
            self.assertEqual(
                validate_review_bundle(
                    self.manifest, path, allow_legacy_translations=True
                )["kind"],
                "translations",
            )

    def test_code_review_bundle_rejects_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-test-") as temporary:
            payload = self._base("code")
            payload["files"] = [
                {
                    "item_id": "code-fixture",
                    "path": "/private/protected.lua",
                    "status": "M ",
                    "diff": "fixture",
                }
            ]
            path = self._write_bundle(Path(temporary), payload)
            with self.assertRaises(ValidationError):
                validate_review_bundle(self.manifest, path)

    def test_code_review_bundle_accepts_manifest_declared_files(self) -> None:
        declared = [
            component.copy_fragment
            for component in self.manifest.components
            if component.copy_fragment
        ]
        declared.extend(self.manifest.manual_definitions)
        self.assertTrue(declared)
        with tempfile.TemporaryDirectory(prefix="tome4-review-test-") as temporary:
            payload = self._base("code")
            payload["files"] = [
                {
                    "item_id": f"code-fixture-{index}",
                    "path": path,
                    "status": "M ",
                    "diff": "fixture",
                }
                for index, path in enumerate(declared)
            ]
            path = self._write_bundle(Path(temporary), payload)
            validated = validate_review_bundle(self.manifest, path)

        self.assertEqual(
            {item["path"] for item in validated["files"]}, set(declared)
        )

    def test_code_review_bundle_rejects_undeclared_root_lua(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-test-") as temporary:
            payload = self._base("code")
            payload["files"] = [
                {
                    "item_id": "code-fixture",
                    "path": "undeclared-review-file.lua",
                    "status": "M ",
                    "diff": "fixture",
                }
            ]
            path = self._write_bundle(Path(temporary), payload)
            with self.assertRaises(ValidationError):
                validate_review_bundle(self.manifest, path)

    def test_review_bundle_redacts_absolute_paths(self) -> None:
        redacted, count = _redact_absolute_paths(
            "--- /dev/null\n"
            "+++ b/tools/new.py\n"
            "+path /Users/yun/projects/t-engine4/game/dlcs/file.lua\n"
            "--- a/tools/deleted.py\n"
            "+++ /dev/null\n"
        )
        self.assertEqual(count, 1)
        self.assertNotIn("/Users/yun", redacted)
        self.assertEqual(redacted.count("/dev/null"), 2)
        ordinary_dev_null, ordinary_count = _redact_absolute_paths("path /dev/null")
        self.assertEqual(ordinary_count, 1)
        self.assertNotIn("/dev/null", ordinary_dev_null)
        pattern, pattern_count = _redact_absolute_paths("gsub(\"([/])\")")
        self.assertEqual(pattern_count, 0)
        self.assertIn("([/])", pattern)

    def test_review_index_identity_ignores_run_local_paths(self) -> None:
        payload = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "tool_version": TOOL_VERSION,
            "version": self.manifest.version,
            "manifest_sha256": hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
            "scope": {"translations": False, "code": True, "protected_sources": False},
            "redacted_absolute_path_count": 0,
            "bundles": [
                {
                    "bundle_id": "bundle-fixture",
                    "kind": "code",
                    "offset": 0,
                    "count": 1,
                    "total": 1,
                    "path": "/first/run/bundle.json",
                }
            ],
            "run_directory": "/first/run",
            "index": "/first/run/review-index.json",
        }
        first = _review_index_id(payload)
        payload["run_directory"] = "/second/run"
        payload["index"] = "/second/run/review-index.json"
        payload["bundles"][0]["path"] = "/second/run/bundle.json"
        self.assertEqual(first, _review_index_id(payload))

    def test_strict_review_normalizes_host_finding_refs(self) -> None:
        bundle = self._base("code")
        bundle["files"] = [
            {
                "item_id": "code-b",
                "path": "tools/b.py",
                "status": "M ",
                "diff": "fixture",
            },
            {
                "item_id": "code-a",
                "path": "tools/a.py",
                "status": "M ",
                "diff": "fixture",
            },
        ]
        bundle["bundle_id"] = _bundle_id(bundle)
        output = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "bundle_id": bundle["bundle_id"],
            "findings": [
                {
                    "finding_id": "model-b",
                    "severity": "minor",
                    "category": "code",
                    "item_id": "code-b",
                    "path": "tools/b.py",
                    "title": "B",
                    "body": "B body",
                },
                {
                    "finding_id": "model-a",
                    "severity": "major",
                    "category": "code",
                    "item_id": "code-a",
                    "path": "tools/a.py",
                    "title": "A",
                    "body": "A body",
                },
            ],
        }
        summary, normalized = _validate_findings(bundle, output, strict=True)
        self.assertEqual(summary["findings"], 2)
        self.assertEqual(
            [finding["finding_id"] for finding in normalized["findings"]],
            ["R-001", "R-002"],
        )
        self.assertEqual(
            [finding["model_finding_id"] for finding in normalized["findings"]],
            ["model-a", "model-b"],
        )
        self.assertEqual(len(normalized["decision_digest"]), 64)
        self.assertEqual(len(normalized["review_id"]), 64)

    def test_strict_review_rejects_unknown_model_fields(self) -> None:
        bundle = self._base("code")
        bundle["files"] = [
            {
                "item_id": "code-fixture",
                "path": "tools/i18n",
                "status": "M ",
                "diff": "fixture",
            }
        ]
        bundle["bundle_id"] = _bundle_id(bundle)
        output = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "bundle_id": bundle["bundle_id"],
            "verdict": "approved",
            "findings": [],
        }
        with self.assertRaises(ValidationError):
            _validate_findings(bundle, output, strict=True)
        summary, normalized = _validate_findings(bundle, output, strict=False)
        self.assertEqual(summary["findings"], 0)
        self.assertNotIn("verdict", normalized)


class TranslationReviewV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.policy, cls.policy_sha256 = load_translation_review_policy(
            cls.manifest.root
        )
        cls.component = cls.manifest.component("boot")
        document = LocaleLoader(LuaRuntime(cls.manifest)).load_path(
            cls.manifest.root / cls.component.translation,
            logical_path=cls.component.translation,
        )
        entry = next(
            value
            for value in document.translations
            if value.get("source") and value.get("target")
        )
        cls.item = build_translation_item(
            version=cls.manifest.version,
            component=cls.component.id,
            ordinal=document.translations.index(entry),
            entry=entry,
        )
        cls.canonical_items = [
            build_translation_item(
                version=cls.manifest.version,
                component=cls.component.id,
                ordinal=ordinal,
                entry=value,
            )
            for ordinal, value in enumerate(document.translations)
        ]
        cls.inventory_sha256, cls.inventory_membership = (
            write_translation_inventory(
                root=cls.manifest.root,
                tool_version=TOOL_VERSION,
                version=cls.manifest.version,
                component=cls.component.id,
                translation_sha256=hashlib.sha256(
                    (cls.manifest.root / cls.component.translation).read_bytes()
                ).hexdigest(),
                items=cls.canonical_items,
            )
        )

    def _bundle(self, items: list[dict[str, object]] | None = None) -> dict[str, object]:
        selected = list(items or [self.item])
        character_count = sum(
            translation_item_character_count(item) for item in selected
        )
        payload = _translation_bundle_payload(
            tool_version=TOOL_VERSION,
            version=self.manifest.version,
            manifest_sha256=hashlib.sha256(self.manifest.raw_bytes).hexdigest(),
            identity_indexes_sha256=quality_module._identity_indexes_sha256(
                self.manifest
            ),
            component=self.component.id,
            translation_sha256=hashlib.sha256(
                (self.manifest.root / self.component.translation).read_bytes()
            ).hexdigest(),
            offset=0,
            total=len(selected),
            batch=selected,
            character_count=character_count,
            character_budget=DEFAULT_TRANSLATION_CHARACTER_BUDGET,
            oversized_single_item=False,
            policy_sha256=self.policy_sha256,
            inventory_sha256=self.inventory_sha256,
            selection_sha256=translation_selection_sha256(selected),
            membership=[
                self.inventory_membership[item["ordinal"]] for item in selected
            ],
        )
        payload["bundle_id"] = _bundle_id(payload)
        return payload

    def _evaluator(self, bundle: dict[str, object]) -> dict[str, object]:
        return make_evaluator_identity(
            provider="fixture",
            model="fixture-model",
            thinking="high",
            prompt_sha256="1" * 64,
            policy_sha256=self.policy_sha256,
            bundle=bundle,
        )

    def _finding(self, **overrides: object) -> dict[str, object]:
        finding: dict[str, object] = {
            "phenomenon": "other",
            "meaning_change": "unknown",
            "source_evidence": {
                "quote": self.item["source"],
                "occurrence": 1,
            },
            "target_evidence": {
                "quote": self.item["target"],
                "occurrence": 1,
            },
            "explanation": "The bounded texts express different observable meaning.",
        }
        finding.update(overrides)
        return finding

    def _output(
        self,
        *,
        findings: list[dict[str, object]] | None = None,
        assessment_state: str = "assessed",
    ) -> dict[str, object]:
        return {
            "items": [
                {
                    "revision_id": self.item["revision_id"],
                    "assessment_state": assessment_state,
                    "findings": [] if findings is None else findings,
                }
            ]
        }

    def test_bundle_is_revision_bound_and_excludes_facts_and_terminology(self) -> None:
        bundle = self._bundle()
        self.assertEqual(bundle["schema_version"], TRANSLATION_REVIEW_SCHEMA_VERSION)
        self.assertEqual(bundle["review_contract"], TRANSLATION_REVIEW_BUNDLE_CONTRACT)
        self.assertEqual(bundle["channel"], TRANSLATION_REVIEW_CHANNEL)
        self.assertNotIn("terminology", bundle)
        self.assertNotIn("terminology_sha256", bundle)
        self.assertEqual(
            bundle["items"][0]["item_id"],
            "translation-" + bundle["items"][0]["revision_id"],
        )
        with tempfile.TemporaryDirectory(prefix="translation-review-v2-") as temporary:
            path = Path(temporary) / "bundle.json"
            path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
            with (
                patch(
                    "i18nlib.review.LuaRuntime",
                    side_effect=AssertionError("bundle validation launched Lua"),
                ),
                patch(
                    "i18nlib.review.LocaleLoader",
                    side_effect=AssertionError("bundle validation rebuilt inventory"),
                ),
            ):
                validated = validate_review_bundle(self.manifest, path)
        self.assertEqual(validated, bundle)

    def test_complete_bundle_rejects_wrong_selection_digest(self) -> None:
        bundle = self._bundle()
        bundle["selection_sha256"] = "0" * 64
        bundle["bundle_id"] = _bundle_id(
            {key: value for key, value in bundle.items() if key != "bundle_id"}
        )
        with tempfile.TemporaryDirectory(prefix="translation-review-selection-") as temporary:
            path = Path(temporary) / "bundle.json"
            path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "selection digest"):
                validate_review_bundle(self.manifest, path)

    def test_bundle_items_must_match_current_canonical_ordinals(self) -> None:
        invented_entry = {
            "section": "invented/not-canonical.lua",
            "source": "Invented source",
            "target": "伪造译文",
            "source_tag": None,
            "args_order": None,
            "special": None,
            "line": 1,
        }
        invented = build_translation_item(
            version=self.manifest.version,
            component=self.component.id,
            ordinal=self.item["ordinal"],
            entry=invented_entry,
        )
        wrong_ordinal = dict(self.item)
        wrong_ordinal["ordinal"] += 1
        for label, item in (("invented", invented), ("wrong ordinal", wrong_ordinal)):
            with self.subTest(label=label), tempfile.TemporaryDirectory(
                prefix="translation-review-v2-lineage-"
            ) as temporary:
                bundle = self._bundle([item])
                path = Path(temporary) / "bundle.json"
                path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
                with self.assertRaisesRegex(
                    ValidationError, "does not match canonical inventory"
                ):
                    validate_review_bundle(self.manifest, path)

    def test_bundle_rejects_duplicate_canonical_ordinal(self) -> None:
        document = LocaleLoader(LuaRuntime(self.manifest)).load_path(
            self.manifest.root / self.component.translation,
            logical_path=self.component.translation,
        )
        second_entry = next(
            entry
            for ordinal, entry in enumerate(document.translations)
            if ordinal != self.item["ordinal"]
            and entry.get("source")
            and entry.get("target")
        )
        second = build_translation_item(
            version=self.manifest.version,
            component=self.component.id,
            ordinal=document.translations.index(second_entry),
            entry=second_entry,
        )
        second["ordinal"] = self.item["ordinal"]
        bundle = self._bundle([self.item, second])
        with tempfile.TemporaryDirectory(
            prefix="translation-review-v2-duplicate-ordinal-"
        ) as temporary:
            path = Path(temporary) / "bundle.json"
            path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "repeats a canonical ordinal"):
                validate_review_bundle(self.manifest, path)

    def test_bundle_rejects_reversed_membership_and_impossible_total(self) -> None:
        second = next(
            item
            for item in self.canonical_items
            if item["ordinal"] > self.item["ordinal"]
        )
        reversed_bundle = self._bundle([second, self.item])
        impossible_total = self._bundle()
        impossible_total["selection"]["total"] = len(self.canonical_items) + 1
        impossible_total["bundle_id"] = _bundle_id(
            {
                key: value
                for key, value in impossible_total.items()
                if key != "bundle_id"
            }
        )
        for label, bundle, message in (
            ("reversed", reversed_bundle, "out of order"),
            ("impossible total", impossible_total, "exceeds the canonical inventory"),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory(
                prefix="translation-review-v2-selection-"
            ) as temporary:
                path = Path(temporary) / "bundle.json"
                path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
                with self.assertRaisesRegex(ValidationError, message):
                    validate_review_bundle(self.manifest, path)

    def test_partition_obeys_character_budget_and_marks_single_oversize(self) -> None:
        first = dict(self.item)
        second = dict(self.item)
        second["revision_id"] = "2" * 64
        second["item_id"] = "translation-" + second["revision_id"]
        item_size = translation_item_character_count(first)
        batches = partition_translation_items(
            [first, second], max_items=50, character_budget=item_size
        )
        self.assertEqual([len(batch) for _, batch, _, _ in batches], [1, 1])
        self.assertEqual([offset for offset, _, _, _ in batches], [0, 1])
        oversized = partition_translation_items(
            [first], max_items=50, character_budget=item_size - 1
        )
        self.assertTrue(oversized[0][3])

    def test_model_must_cover_every_revision_in_order(self) -> None:
        bundle = self._bundle()
        evaluator = self._evaluator(bundle)
        with self.assertRaisesRegex(ValidationError, "cover every bundle item"):
            validate_translation_model_output(
                bundle=bundle,
                output={"items": []},
                policy=self.policy,
                policy_sha256=self.policy_sha256,
                evaluator=evaluator,
            )
        output = self._output()
        output["items"][0]["revision_id"] = "0" * 64
        with self.assertRaisesRegex(ValidationError, "out of order"):
            validate_translation_model_output(
                bundle=bundle,
                output=output,
                policy=self.policy,
                policy_sha256=self.policy_sha256,
                evaluator=evaluator,
            )

    def test_model_cannot_supply_host_owned_classification(self) -> None:
        bundle = self._bundle()
        evaluator = self._evaluator(bundle)
        finding = self._finding(severity="major")
        with self.assertRaisesRegex(ValidationError, "unknown fields: severity"):
            validate_translation_model_output(
                bundle=bundle,
                output=self._output(findings=[finding]),
                policy=self.policy,
                policy_sha256=self.policy_sha256,
                evaluator=evaluator,
            )

    def test_exact_evidence_becomes_pending_host_queue(self) -> None:
        bundle = self._bundle()
        summary, assessment = validate_translation_model_output(
            bundle=bundle,
            output=self._output(findings=[self._finding()]),
            policy=self.policy,
            policy_sha256=self.policy_sha256,
            evaluator=self._evaluator(bundle),
        )
        normalized = assessment["items"][0]["findings"][0]
        self.assertEqual(assessment["review_contract"], TRANSLATION_REVIEW_ASSESSMENT_CONTRACT)
        self.assertEqual(normalized["disposition"], "pending")
        self.assertIsNone(normalized["severity"])
        self.assertEqual(normalized["finding_id"], "R-001")
        self.assertEqual(summary["manual_queue"], 1)
        self.assertFalse(summary["overall_translation_clean"])

    def test_explanation_rewording_preserves_claim_identity(self) -> None:
        bundle = self._bundle()
        evaluator = self._evaluator(bundle)
        _, first = validate_translation_model_output(
            bundle=bundle,
            output=self._output(findings=[self._finding()]),
            policy=self.policy,
            policy_sha256=self.policy_sha256,
            evaluator=evaluator,
        )
        _, second = validate_translation_model_output(
            bundle=bundle,
            output=self._output(
                findings=[self._finding(explanation="Same span, reworded explanation.")]
            ),
            policy=self.policy,
            policy_sha256=self.policy_sha256,
            evaluator=evaluator,
        )
        first_finding = first["items"][0]["findings"][0]
        second_finding = second["items"][0]["findings"][0]
        self.assertEqual(first_finding["finding_key"], second_finding["finding_key"])
        self.assertNotEqual(first["assessment_id"], second["assessment_id"])

    def test_evidence_must_resolve_exactly_and_omission_may_use_missing_target(self) -> None:
        bundle = self._bundle()
        evaluator = self._evaluator(bundle)
        missing = self._finding(
            source_evidence={"quote": "not present", "occurrence": 1}
        )
        with self.assertRaisesRegex(ValidationError, "does not resolve"):
            validate_translation_model_output(
                bundle=bundle,
                output=self._output(findings=[missing]),
                policy=self.policy,
                policy_sha256=self.policy_sha256,
                evaluator=evaluator,
            )
        omission = self._finding(
            phenomenon="omission",
            meaning_change="omitted",
            target_evidence={"quote": "", "occurrence": 0},
        )
        _, assessment = validate_translation_model_output(
            bundle=bundle,
            output=self._output(findings=[omission]),
            policy=self.policy,
            policy_sha256=self.policy_sha256,
            evaluator=evaluator,
        )
        self.assertEqual(
            assessment["items"][0]["findings"][0]["normalized_target_evidence"]["state"],
            "missing",
        )

    def test_incompatible_taxonomy_and_duplicate_claims_are_rejected(self) -> None:
        bundle = self._bundle()
        evaluator = self._evaluator(bundle)
        incompatible = self._finding(phenomenon="addition", meaning_change="omitted")
        with self.assertRaisesRegex(ValidationError, "incompatible"):
            validate_translation_model_output(
                bundle=bundle,
                output=self._output(findings=[incompatible]),
                policy=self.policy,
                policy_sha256=self.policy_sha256,
                evaluator=evaluator,
            )
        finding = self._finding()
        with self.assertRaisesRegex(ValidationError, "duplicate semantic observation"):
            validate_translation_model_output(
                bundle=bundle,
                output=self._output(findings=[finding, dict(finding)]),
                policy=self.policy,
                policy_sha256=self.policy_sha256,
                evaluator=evaluator,
            )

    def test_context_insufficient_without_finding_still_routes_manual(self) -> None:
        bundle = self._bundle()
        summary, assessment = validate_translation_model_output(
            bundle=bundle,
            output=self._output(assessment_state="context-insufficient"),
            policy=self.policy,
            policy_sha256=self.policy_sha256,
            evaluator=self._evaluator(bundle),
        )
        self.assertEqual(summary["context_insufficient_items"], 1)
        self.assertEqual(assessment["manual_queue"][0]["route_type"], "item")
        self.assertIsNone(assessment["manual_queue"][0]["finding_id"])

    def test_v2_observations_cannot_enter_legacy_remediation(self) -> None:
        bundle = self._bundle()
        _, assessment = validate_translation_model_output(
            bundle=bundle,
            output=self._output(findings=[self._finding()]),
            policy=self.policy,
            policy_sha256=self.policy_sha256,
            evaluator=self._evaluator(bundle),
        )
        with self.assertRaisesRegex(ValidationError, "cannot be remediated directly"):
            _validate_findings_for_remediation(bundle, assessment)
        relabeled_legacy = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "review_contract": REVIEW_CONTRACT,
            "bundle_id": bundle["bundle_id"],
            "review_id": "relabeled",
            "findings": [
                {
                    "finding_id": "R-001",
                    "item_id": self.item["item_id"],
                    "severity": "major",
                    "category": "translation",
                    "title": "Relabeled observation",
                    "body": "Must not bypass the translation v2 boundary.",
                }
            ],
        }
        with self.assertRaisesRegex(ValidationError, "cannot be remediated directly"):
            _validate_findings_for_remediation(bundle, relabeled_legacy)

    def test_cache_identity_separates_v1_and_v2_contracts(self) -> None:
        common = {
            "bundle_id": "a" * 64,
            "provider": "fixture",
            "model": "fixture-model",
            "thinking": "high",
            "prompt_sha256": "b" * 64,
            "strict": True,
        }
        legacy = _review_cache_key(**common)
        translation = _review_cache_key(
            **common,
            review_contract=TRANSLATION_REVIEW_ASSESSMENT_CONTRACT,
            policy_sha256=self.policy_sha256,
            normalizer_contract=TRANSLATION_REVIEW_NORMALIZER_CONTRACT,
        )
        changed_normalizer = _review_cache_key(
            **common,
            review_contract=TRANSLATION_REVIEW_ASSESSMENT_CONTRACT,
            policy_sha256=self.policy_sha256,
            normalizer_contract="future-normalizer",
        )
        self.assertNotEqual(legacy, translation)
        self.assertNotEqual(translation, changed_normalizer)

    def test_cached_assessment_corruption_is_a_controlled_validation_error(self) -> None:
        bundle = self._bundle()
        evaluator = self._evaluator(bundle)
        _, assessment = validate_translation_model_output(
            bundle=bundle,
            output=self._output(findings=[self._finding()]),
            policy=self.policy,
            policy_sha256=self.policy_sha256,
            evaluator=evaluator,
        )
        non_array = json.loads(json.dumps(assessment))
        non_array["items"] = None
        missing_raw_field = json.loads(json.dumps(assessment))
        del missing_raw_field["items"][0]["findings"][0]["explanation"]
        for label, corrupted in (
            ("non-array items", non_array),
            ("missing raw finding field", missing_raw_field),
        ):
            with self.subTest(label=label), self.assertRaises(ValidationError):
                revalidate_translation_assessment(
                    bundle=bundle,
                    assessment=corrupted,
                    policy=self.policy,
                    policy_sha256=self.policy_sha256,
                    evaluator=evaluator,
                )

    def test_headless_runner_uses_v2_prompt_and_host_envelope(self) -> None:
        bundle = self._bundle()
        with tempfile.TemporaryDirectory(prefix="translation-review-v2-runner-") as temporary:
            directory = Path(temporary)
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
            arguments_path = directory / "arguments.json"
            fake_pi = directory / "fake-pi"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
Path(os.environ["FAKE_PI_ARGUMENTS"]).write_text(json.dumps(sys.argv[1:]), encoding="utf-8")
Path(os.environ["FAKE_PI_CWD"]).write_text(os.getcwd(), encoding="utf-8")
bundle = json.loads(sys.stdin.buffer.read())
Path(os.environ["FAKE_ORIGINAL_BUNDLE"]).write_text('{"tampered":true}', encoding="utf-8")
print(json.dumps({"items": [{"revision_id": item["revision_id"], "assessment_state": "assessed", "findings": []} for item in bundle["items"]]}, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            previous = os.environ.get("FAKE_PI_ARGUMENTS")
            previous_original = os.environ.get("FAKE_ORIGINAL_BUNDLE")
            previous_cwd = os.environ.get("FAKE_PI_CWD")
            os.environ["FAKE_PI_ARGUMENTS"] = str(arguments_path)
            os.environ["FAKE_ORIGINAL_BUNDLE"] = str(bundle_path)
            cwd_path = directory / "cwd.txt"
            os.environ["FAKE_PI_CWD"] = str(cwd_path)
            try:
                report = run_pi_review(
                    bundle_path=bundle_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    pi_executable=str(fake_pi),
                    use_cache=False,
                )
            finally:
                if previous is None:
                    os.environ.pop("FAKE_PI_ARGUMENTS", None)
                else:
                    os.environ["FAKE_PI_ARGUMENTS"] = previous
                if previous_original is None:
                    os.environ.pop("FAKE_ORIGINAL_BUNDLE", None)
                else:
                    os.environ["FAKE_ORIGINAL_BUNDLE"] = previous_original
                if previous_cwd is None:
                    os.environ.pop("FAKE_PI_CWD", None)
                else:
                    os.environ["FAKE_PI_CWD"] = previous_cwd
            arguments = json.loads(arguments_path.read_text(encoding="utf-8"))
            assessment = json.loads(Path(report["review"]).read_text(encoding="utf-8"))
            provider_cwd = cwd_path.read_text(encoding="utf-8")
        self.assertEqual(report["mode"], "translation-semantic-observations-v2")
        self.assertEqual(report["review_contract"], TRANSLATION_REVIEW_ASSESSMENT_CONTRACT)
        self.assertEqual(assessment["review_contract"], TRANSLATION_REVIEW_ASSESSMENT_CONTRACT)
        self.assertEqual(assessment["evaluator"]["provider"], "fixture")
        self.assertIn("translation semantic reviewer v2", " ".join(arguments))
        self.assertIn("--no-tools", arguments)
        self.assertEqual(
            arguments[arguments.index("--append-system-prompt") + 1], ""
        )
        self.assertFalse(any(value.startswith("@") for value in arguments))
        sent_path = Path(report["provider_payload"])
        self.assertNotEqual(sent_path, bundle_path)
        self.assertEqual(
            json.loads(sent_path.read_text(encoding="utf-8")),
            translation_provider_payload(bundle),
        )
        self.assertEqual(sent_path.read_bytes(), translation_provider_message(bundle))
        expected_provider_cwd = str(TRANSLATION_REVIEW_PROVIDER_CWD)
        self.assertEqual(provider_cwd, expected_provider_cwd)
        self.assertEqual(report["provider_cwd"], expected_provider_cwd)
        self.assertEqual(
            json.loads(
                Path(report["validated_bundle"]).read_text(encoding="utf-8")
            ),
            bundle,
        )
        self.assertEqual(
            hashlib.sha256(sent_path.read_bytes()).hexdigest(),
            report["payload_sha256"],
        )
        self.assertEqual(sent_path.stat().st_size, report["payload_bytes"])
        self.assertEqual(
            assessment["evaluator"]["bundle_payload_sha256"],
            report["payload_sha256"],
        )
        self.assertEqual(
            assessment["evaluator"]["bundle_payload_bytes"],
            report["payload_bytes"],
        )
        self.assertEqual(
            assessment["evaluator"]["runner_contract"],
            TRANSLATION_REVIEW_RUNNER_CONTRACT,
        )
        source_prompt = arguments[arguments.index("--system-prompt") + 1]
        self.assertEqual(
            report["prompt_sha256"],
            hashlib.sha256(
                (
                    source_prompt
                    + "\nCurrent working directory: "
                    + str(TRANSLATION_REVIEW_PROVIDER_CWD)
                ).encode("utf-8")
            ).hexdigest(),
        )

    def test_runner_rejects_index_bundle_id_mismatch_before_staging(self) -> None:
        bundle = self._bundle()
        with tempfile.TemporaryDirectory(prefix="translation-review-index-bind-") as temporary:
            path = Path(temporary) / "bundle.json"
            path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
            with patch("i18nlib.pi_review.create_run_directory") as create_run:
                with self.assertRaisesRegex(ValidationError, "expected index identity"):
                    run_pi_review(
                        bundle_path=path,
                        provider="fixture",
                        model="fixture-model",
                        thinking="high",
                        timeout=30,
                        strict=True,
                        pi_executable=str(Path(temporary) / "must-not-run"),
                        use_cache=False,
                        expected_bundle_id="0" * 64,
                    )
            create_run.assert_not_called()

    def test_tmux_foreground_runner_uses_digest_bound_stdin(self) -> None:
        bundle = self._bundle()
        with tempfile.TemporaryDirectory(prefix="translation-review-v2-tmux-") as temporary:
            directory = Path(temporary)
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
            arguments_path = directory / "arguments.json"
            cwd_path = directory / "cwd.txt"
            fake_pi = directory / "fake-pi"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
Path(os.environ["FAKE_PI_ARGUMENTS"]).write_text(json.dumps(sys.argv[1:]), encoding="utf-8")
Path(os.environ["FAKE_PI_CWD"]).write_text(os.getcwd(), encoding="utf-8")
bundle = json.loads(sys.stdin.buffer.read())
print(json.dumps({"items": [{"revision_id": item["revision_id"], "assessment_state": "assessed", "findings": []} for item in bundle["items"]]}, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            with patch.dict(
                os.environ,
                {
                    "FAKE_PI_ARGUMENTS": str(arguments_path),
                    "FAKE_PI_CWD": str(cwd_path),
                    "TMUX": "",
                },
            ):
                report = run_tmux_review(
                    bundle_path=bundle_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    use_cache=False,
                    force=False,
                    pi_executable=str(fake_pi),
                    tmux_executable=str(directory / "unused-tmux"),
                    fallback="foreground",
                )
            arguments = json.loads(arguments_path.read_text(encoding="utf-8"))
            provider_cwd = cwd_path.read_text(encoding="utf-8")
        job = json.loads(
            (Path(report["run_directory"]) / "job.json").read_text(encoding="utf-8")
        )
        self.assertTrue(report["ok"])
        self.assertEqual(report["execution"], "foreground")
        self.assertEqual(
            arguments[arguments.index("--append-system-prompt") + 1], ""
        )
        self.assertFalse(any(value.startswith("@") for value in arguments))
        expected_provider_cwd = str(TRANSLATION_REVIEW_PROVIDER_CWD)
        self.assertEqual(provider_cwd, expected_provider_cwd)
        self.assertEqual(job["cwd"], expected_provider_cwd)
        self.assertEqual(job["stdin_path"], report["provider_payload"])
        self.assertEqual(job["stdin_sha256"], report["payload_sha256"])
        self.assertEqual(job["stdin_bytes"], report["payload_bytes"])
        self.assertEqual(
            Path(job["stdin_path"]).read_bytes(), translation_provider_message(bundle)
        )

    def test_legacy_file_reviewer_rejects_translation_v2_before_pi(self) -> None:
        bundle = self._bundle()
        with tempfile.TemporaryDirectory(prefix="translation-review-v2-files-") as temporary:
            bundle_path = Path(temporary) / "bundle.json"
            bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "claim-bound"):
                run_pi_file_review(
                    bundle_path=bundle_path,
                    provider="fixture",
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    pi_executable=str(Path(temporary) / "must-not-run"),
                )

    def test_v2_cache_revalidates_host_assessment_before_reuse(self) -> None:
        bundle = self._bundle()
        with tempfile.TemporaryDirectory(prefix="translation-review-v2-cache-") as temporary:
            directory = Path(temporary)
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
            fake_pi = directory / "fake-pi"
            fake_pi.write_text(
                """#!/usr/bin/env python3
import json
import sys
bundle = json.loads(sys.stdin.buffer.read())
print(json.dumps({"items": [{"revision_id": item["revision_id"], "assessment_state": "assessed", "findings": []} for item in bundle["items"]]}, ensure_ascii=False))
""",
                encoding="utf-8",
            )
            fake_pi.chmod(0o700)
            provider = f"fixture-v2-cache-{directory.name}"
            first = run_pi_review(
                bundle_path=bundle_path,
                provider=provider,
                model="fixture-model",
                thinking="high",
                timeout=30,
                strict=True,
                pi_executable=str(fake_pi),
                use_cache=True,
            )
            cache_path = (
                ROOT
                / ".artifacts"
                / "i18n"
                / "cache"
                / "pi-review"
                / f"{first['result_cache_key']}.json"
            )
            try:
                second = run_pi_review(
                    bundle_path=bundle_path,
                    provider=provider,
                    model="fixture-model",
                    thinking="high",
                    timeout=30,
                    strict=True,
                    pi_executable=str(directory / "must-not-run"),
                    use_cache=True,
                )
                tampered = json.loads(cache_path.read_text(encoding="utf-8"))
                tampered["review"]["manual_queue"] = [
                    {
                        "route_type": "item",
                        "revision_id": self.item["revision_id"],
                        "finding_id": None,
                        "reason_codes": ["tampered"],
                    }
                ]
                cache_path.write_text(json.dumps(tampered), encoding="utf-8")
                with self.assertRaisesRegex(AgentError, "cache validation failed"):
                    run_pi_review(
                        bundle_path=bundle_path,
                        provider=provider,
                        model="fixture-model",
                        thinking="high",
                        timeout=30,
                        strict=True,
                        pi_executable=str(directory / "must-not-run"),
                        use_cache=True,
                    )
            finally:
                cache_path.unlink(missing_ok=True)
        self.assertEqual(first["cache_decision"], "miss")
        self.assertEqual(second["cache_decision"], "hit")


if __name__ == "__main__":
    unittest.main()
