from __future__ import annotations

import json
import hashlib
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
import sys

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib import TOOL_VERSION  # noqa: E402
from i18nlib.reviewer_compare import (  # noqa: E402
    _bundle_selected_items,
    _match_item,
    _metrics,
    _semantic_claim_jaccard,
    _sha,
    _implementation_sha256,
    _validate_gold_finding,
    load_comparison_policy,
    run_freeze,
    run_prepare,
    run_report,
    run_validate,
)
from i18nlib.errors import ValidationError  # noqa: E402
from i18nlib.config import load_manifest  # noqa: E402
from i18nlib.locale_model import LocaleLoader  # noqa: E402
from i18nlib.pi_review import _review_cache_key  # noqa: E402
from i18nlib.review import _translation_items_from_bytes, validate_review_bundle  # noqa: E402
from i18nlib.runtime import LuaRuntime  # noqa: E402
from i18nlib.translation_review import (  # noqa: E402
    TRANSLATION_REVIEW_ASSESSMENT_CONTRACT,
    TRANSLATION_REVIEW_NORMALIZER_CONTRACT,
    TRANSLATION_REVIEW_RUNNER_CONTRACT,
    load_translation_review_policy,
)


def _revision(number: int) -> str:
    return f"{number:064x}"


def _inventory_item(number: int, component: str) -> dict:
    return {
        "revision_id": _revision(10_000 + number),
        "unit_id": _revision(20_000 + number),
        "component": component,
        "section": f"section/{number}",
        "source": f"Source {number}",
        "target": f"目标 {number}",
        "source_tag": "_t",
        "occurrences": [{"ordinal": number, "line": number + 1}],
        "risk_flags": ["has-number"] if number % 2 else [],
        "gate_signals": {"needs_review": ["QG_CURRENT"]},
    }


def _runner_lineage(
    *, bundle_id: str, model: dict, prompt_sha256: str, payload: bytes
) -> dict:
    policy_sha256 = load_translation_review_policy(ROOT)[1]
    payload_sha256 = hashlib.sha256(payload).hexdigest()
    return {
        "tool_version": TOOL_VERSION,
        "review_contract": TRANSLATION_REVIEW_ASSESSMENT_CONTRACT,
        "prompt_sha256": prompt_sha256,
        "runner_contract": TRANSLATION_REVIEW_RUNNER_CONTRACT,
        "payload_sha256": payload_sha256,
        "payload_bytes": len(payload),
        "result_cache_key": _review_cache_key(
            bundle_id=bundle_id,
            provider=model["provider"],
            model=model["model"],
            thinking=model["thinking"],
            prompt_sha256=prompt_sha256,
            strict=True,
            review_contract=TRANSLATION_REVIEW_ASSESSMENT_CONTRACT,
            policy_sha256=policy_sha256,
            normalizer_contract=TRANSLATION_REVIEW_NORMALIZER_CONTRACT,
            payload_sha256=payload_sha256,
            runner_contract=TRANSLATION_REVIEW_RUNNER_CONTRACT,
        ),
        "strict": True,
    }


class ReviewerComparisonTests(unittest.TestCase):
    def test_policy_freezes_requested_models(self) -> None:
        policy, digest = load_comparison_policy(ROOT)
        self.assertEqual(64, len(digest))
        self.assertEqual(
            ("deepseek-v4-flash", "max"),
            (policy["models"][0]["model"], policy["models"][0]["thinking"]),
        )
        self.assertEqual(
            ("gpt-5.6-sol", "medium"),
            (policy["models"][1]["model"], policy["models"][1]["thinking"]),
        )
        for path in sorted(
            (ROOT / "i18n" / "quality" / "schemas").glob(
                "reviewer-comparison-*.schema.json"
            )
        ):
            self.assertIsInstance(json.loads(path.read_text(encoding="utf-8")), dict)

    def test_prepare_prefers_four_release_components_deterministically(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reviewer-compare-prepare-") as temporary:
            directory = Path(temporary)
            inventory = directory / "inventory.jsonl"
            components = ["tome", "ashes-urhrok", "cults", "orcs", "engine"]
            values = [
                _inventory_item(index * 1000 + offset, component)
                for index, component in enumerate(components)
                for offset in range(80)
            ]
            inventory.write_text(
                "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in values),
                encoding="utf-8",
            )
            manifest = SimpleNamespace(
                root=ROOT,
                version="tome-1.7.6",
                components=[SimpleNamespace(id=value) for value in components],
            )
            outputs = iter((directory / "run-a", directory / "run-b"))
            with patch(
                "i18nlib.reviewer_compare.create_quality_run_directory",
                side_effect=lambda *_args: next(outputs),
            ):
                first = run_prepare(manifest, inventory_path=inventory)
                second = run_prepare(manifest, inventory_path=inventory)
            self.assertEqual(first["candidate_pool_id"], second["candidate_pool_id"])
            self.assertTrue(first["ready_for_gold_curation"])
            self.assertEqual(
                {"ashes-urhrok", "cults", "orcs", "tome"},
                set(first["component_counts"]),
            )
            self.assertEqual(256, first["candidate_count"])
            template = json.loads(Path(first["gold_template"]).read_text(encoding="utf-8"))
            self.assertIn(
                "an intentional or mechanics-justified adaptation remains substantive-difference",
                template["instructions"],
            )
            self.assertIn(
                "reserve no-substantive-difference for genuine proposition-level equivalence",
                template["instructions"],
            )

    def test_prepare_reports_historical_fallback_instead_of_fabricating_items(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reviewer-compare-fallback-") as temporary:
            directory = Path(temporary)
            inventory = directory / "inventory.jsonl"
            inventory.write_text(
                "".join(
                    json.dumps(_inventory_item(index, "tome"), ensure_ascii=False) + "\n"
                    for index in range(10)
                ),
                encoding="utf-8",
            )
            manifest = SimpleNamespace(
                root=ROOT,
                version="tome-1.7.6",
                components=[SimpleNamespace(id="tome")],
            )
            with patch(
                "i18nlib.reviewer_compare.create_quality_run_directory",
                return_value=directory / "run",
            ):
                report = run_prepare(manifest, inventory_path=inventory)
            self.assertFalse(report["ready_for_gold_curation"])
            self.assertEqual("unexposed-historical-revisions", report["fallback_required"])

    def test_prepare_binds_explicit_eligible_manual_inclusion(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reviewer-compare-include-") as temporary:
            directory = Path(temporary)
            inventory = directory / "inventory.jsonl"
            values = [_inventory_item(index, "tome") for index in range(300)]
            inventory.write_text(
                "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in values),
                encoding="utf-8",
            )
            included = values[-1]["revision_id"]
            manifest = SimpleNamespace(
                root=ROOT,
                version="tome-1.7.6",
                components=[SimpleNamespace(id="tome")],
            )
            with patch(
                "i18nlib.reviewer_compare.create_quality_run_directory",
                return_value=directory / "run",
            ):
                report = run_prepare(
                    manifest,
                    inventory_path=inventory,
                    manual_include_revision_ids=(included,),
                )
            pool = json.loads(Path(report["candidate_pool"]).read_text(encoding="utf-8"))
            self.assertEqual([included], pool["manual_include_revision_ids"])
            self.assertEqual(included, pool["items"][0]["revision_id"])
            self.assertEqual(1, report["manual_include_count"])

    def test_exact_phenomenon_meaning_and_overlapping_evidence_match(self) -> None:
        gold = {
            "source": "Deals 10 damage.",
            "target": "造成10点伤害。",
            "findings": [{
                "phenomenon": "number",
                "meaning_change": "strengthened",
                "accepted_classifications": [{
                    "phenomenon": "number", "meaning_change": "strengthened",
                }],
                "source_evidence": {"quote": "10", "occurrence": 1},
                "target_evidence": {"quote": "10", "occurrence": 1},
            }],
        }
        observed = {
            "assessment_state": "assessed",
            "findings": [{
                "phenomenon": "number",
                "meaning_change": "strengthened",
                "source_evidence": {"quote": "10", "occurrence": 1},
                "target_evidence": {"quote": "10", "occurrence": 1},
            }],
        }
        self.assertEqual((1, 0, 0), _match_item(gold, observed))
        observed["findings"][0]["meaning_change"] = "weakened"
        self.assertEqual((0, 1, 1), _match_item(gold, observed))

    def test_metrics_keep_major_recall_and_no_difference_false_positives_separate(self) -> None:
        gold = [
            {
                "revision_id": "major", "severity": "major",
                "semantic_state": "substantive-difference",
                "findings_exhaustive": True, "source": "A",
                "target": "甲", "findings": [{
                    "phenomenon": "polarity", "meaning_change": "reversed",
                    "accepted_classifications": [{
                        "phenomenon": "polarity", "meaning_change": "reversed",
                    }],
                    "source_evidence": {"quote": "A", "occurrence": 1},
                    "target_evidence": {"quote": "甲", "occurrence": 1},
                }],
            },
            {
                "revision_id": "clean", "severity": "clean",
                "semantic_state": "no-substantive-difference",
                "findings_exhaustive": True, "source": "B", "target": "乙",
                "findings": [],
            },
        ]
        observed = {
            "major": {
                "assessment_state": "assessed",
                "findings": [{
                    "phenomenon": "polarity", "meaning_change": "reversed",
                    "source_evidence": {"quote": "A", "occurrence": 1},
                    "target_evidence": {"quote": "甲", "occurrence": 1},
                }],
            },
            "clean": {
                "assessment_state": "assessed",
                "findings": [{
                    "phenomenon": "other", "meaning_change": "unknown",
                    "source_evidence": {"quote": "B", "occurrence": 1},
                    "target_evidence": {"quote": "乙", "occurrence": 1},
                }],
            },
        }
        metrics = _metrics(gold, observed)
        self.assertEqual(1.0, metrics["major_recall"])
        self.assertEqual(1.0, metrics["no_difference_false_positive_rate"])
        self.assertEqual(0.5, metrics["precision"])

    def test_missing_side_evidence_matches_curator_context_anchor(self) -> None:
        gold = {
            "source": "all foes in range 5 are drawn to it",
            "target": "将敌人拉过来（你可以开关此效果）",
            "findings": [{
                "phenomenon": "addition", "meaning_change": "added",
                "accepted_classifications": [{
                    "phenomenon": "addition", "meaning_change": "added",
                }],
                "source_evidence": {
                    "quote": "all foes in range 5 are drawn to it", "occurrence": 1,
                },
                "target_evidence": {
                    "quote": "将敌人拉过来（你可以开关此效果）", "occurrence": 1,
                },
            }],
        }
        observed = {
            "assessment_state": "assessed",
            "findings": [{
                "phenomenon": "addition", "meaning_change": "added",
                "source_evidence": {"quote": "", "occurrence": 0},
                "target_evidence": {"quote": "（你可以开关此效果）", "occurrence": 1},
            }],
        }
        self.assertEqual((1, 0, 0), _match_item(gold, observed))

    def test_gold_validator_accepts_canonical_missing_side_evidence(self) -> None:
        finding = {
            "phenomenon": "addition", "meaning_change": "added",
            "accepted_classifications": [{
                "phenomenon": "addition", "meaning_change": "added",
            }],
            "classification_rationale": "The target-only phrase is a genuine addition.",
            "source_evidence": {"quote": "", "occurrence": 0},
            "target_evidence": {"quote": "新增", "occurrence": 1},
        }
        self.assertEqual(
            finding,
            _validate_gold_finding(
                finding,
                {"root": ROOT, "source": "A", "target": "甲新增"},
                "fixture",
            ),
        )
        invalid = {**finding, "classification_rationale": "   "}
        with self.assertRaisesRegex(ValidationError, "classification_rationale"):
            _validate_gold_finding(
                invalid,
                {"root": ROOT, "source": "A", "target": "甲新增"},
                "fixture",
            )

    def test_gold_explicitly_accepts_equivalent_classification(self) -> None:
        gold = {
            "source": "flechettes remain embedded",
            "target": "毒镖会留在目标体内",
            "findings": [{
                "phenomenon": "entity-role", "meaning_change": "reassigned",
                "accepted_classifications": [
                    {"phenomenon": "entity-role", "meaning_change": "reassigned"},
                    {"phenomenon": "addition", "meaning_change": "added"},
                ],
                "source_evidence": {"quote": "flechettes", "occurrence": 1},
                "target_evidence": {"quote": "毒镖", "occurrence": 1},
            }],
        }
        observed = {
            "assessment_state": "assessed",
            "findings": [{
                "phenomenon": "addition", "meaning_change": "added",
                "source_evidence": {"quote": "flechettes", "occurrence": 1},
                "target_evidence": {"quote": "毒镖", "occurrence": 1},
            }],
        }
        self.assertEqual((1, 0, 0), _match_item(gold, observed))

    def test_non_exhaustive_gold_does_not_turn_extra_observations_into_false_positives(self) -> None:
        gold = [{
            "revision_id": "accepted", "severity": "clean",
            "semantic_state": "substantive-difference",
            "findings_exhaustive": False,
            "source": "A B", "target": "甲乙",
            "findings": [{
                "phenomenon": "other", "meaning_change": "reassigned",
                "accepted_classifications": [{
                    "phenomenon": "other", "meaning_change": "reassigned",
                }],
                "source_evidence": {"quote": "A", "occurrence": 1},
                "target_evidence": {"quote": "甲", "occurrence": 1},
            }],
        }]
        observed = {"accepted": {
            "assessment_state": "assessed",
            "findings": [
                {
                    "phenomenon": "other", "meaning_change": "reassigned",
                    "source_evidence": {"quote": "A", "occurrence": 1},
                    "target_evidence": {"quote": "甲", "occurrence": 1},
                },
                {
                    "phenomenon": "other", "meaning_change": "reassigned",
                    "source_evidence": {"quote": "B", "occurrence": 1},
                    "target_evidence": {"quote": "乙", "occurrence": 1},
                },
            ],
        }}
        metrics = _metrics(gold, observed)
        self.assertEqual(0, metrics["false_positive_findings"])
        self.assertEqual(1, metrics["unadjudicated_additional_findings"])
        self.assertFalse(metrics["precision_complete"])

    def test_semantic_stability_uses_evidence_clusters_not_taxonomy_bytes(self) -> None:
        gold = [{
            "revision_id": "r", "source": "when broken", "target": "被打断时",
        }]
        left = {"r": {"findings": [{
            "finding_key": "a", "phenomenon": "condition",
            "meaning_change": "omitted",
            "source_evidence": {"quote": "when broken", "occurrence": 1},
            "target_evidence": {"quote": "", "occurrence": 0},
        }]}}
        right = {"r": {"findings": [{
            "finding_key": "b", "phenomenon": "trigger-timing",
            "meaning_change": "omitted",
            "source_evidence": {"quote": "when broken", "occurrence": 1},
            "target_evidence": {"quote": "", "occurrence": 0},
        }]}}
        self.assertEqual(1.0, _semantic_claim_jaccard(left, right, gold))
        right["r"]["findings"][0]["meaning_change"] = "reassigned"
        right["r"]["findings"][0]["target_evidence"] = {
            "quote": "被打断时", "occurrence": 1,
        }
        self.assertEqual(0.0, _semantic_claim_jaccard(left, right, gold))

    def test_freeze_builds_24_content_slots_and_one_transport_retry(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reviewer-compare-freeze-") as temporary:
            directory = Path(temporary)
            components = ("tome", "ashes-urhrok", "cults", "orcs")
            candidates = []
            gold_items = []
            for index in range(64):
                component = components[(index % 32) // 8]
                revision = _revision(30_000 + index)
                candidates.append({
                    "rank": index + 1, "revision_id": revision,
                    "unit_id": _revision(40_000 + index), "component": component,
                    "section": f"section/{index}", "source": f"Source {index}",
                    "target": f"目标 {index}", "source_tag": "_t", "ordinal": index,
                    "risk_score": 0, "risk_flags": [],
                })
                within_split = index % 32
                if within_split < 12:
                    severity = "major"
                elif within_split < 16:
                    severity = "minor"
                elif within_split < 30:
                    severity = "clean"
                else:
                    severity = "context-insufficient"
                accepted_difference = severity == "clean" and within_split < 18
                findings = []
                if severity in {"major", "minor"} or accepted_difference:
                    findings = [{
                        "phenomenon": "other", "meaning_change": "unknown",
                        "accepted_classifications": [{
                            "phenomenon": "other", "meaning_change": "unknown",
                        }],
                        "classification_rationale": "Fixture primary classification.",
                        "source_evidence": {"quote": "Source", "occurrence": 1},
                        "target_evidence": {"quote": "目标", "occurrence": 1},
                    }]
                gold_items.append({
                    "revision_id": revision,
                    "split": "calibration" if index < 32 else "holdout",
                    "gold_state": (
                        "context-insufficient" if severity == "context-insufficient"
                        else "assessed"
                    ),
                    "semantic_state": (
                        "context-insufficient"
                        if severity == "context-insufficient"
                        else (
                            "substantive-difference"
                            if severity in {"major", "minor"} or accepted_difference
                            else "no-substantive-difference"
                        )
                    ),
                    "severity": severity,
                    "findings_exhaustive": (
                        severity == "clean" and not accepted_difference
                    ),
                    "adjudication_rationale": f"Fixture adjudication {index}.",
                    "controlled": False,
                    "findings": findings,
                })
            pool = {
                "contract": "tome4-reviewer-comparison-candidate-pool-v2",
                "schema_version": 2, "version": "tome-1.7.6",
                "policy_sha256": "0" * 64, "inventory_sha256": "1" * 64,
                "excluded_revision_ids_sha256": "2" * 64,
                "fallback_order": load_comparison_policy(ROOT)[0]["fallback_order"],
                "items": candidates,
            }
            pool["candidate_pool_id"] = _sha(pool)
            gold = {
                "contract": "tome4-reviewer-comparison-gold-v2",
                "schema_version": 2, "candidate_pool_id": pool["candidate_pool_id"],
                "human_confirmed": True, "fallback_stage": "none", "items": gold_items,
            }
            pool_path = directory / "pool.json"
            gold_path = directory / "gold.json"
            pool_path.write_text(json.dumps(pool, ensure_ascii=False), encoding="utf-8")
            gold_path.write_text(json.dumps(gold, ensure_ascii=False), encoding="utf-8")
            manifest = SimpleNamespace(root=ROOT, version="tome-1.7.6")

            def fake_bundles(_manifest, _loader, selected, run_directory, _policy):
                split = selected[0]["split"]
                return [{
                    "split": split, "component": component,
                    "bundle_id": _revision(50_000 + offset + (0 if split == "calibration" else 10)),
                    "bundle_sha256": _revision(60_000 + offset), "count": 8,
                    "item_character_count": 100, "item_character_budget": 16000,
                    "artifact_bytes": 200, "payload_bytes": 100,
                    "path": str(run_directory / "bundles" / split / component / "bundle.json"),
                } for offset, component in enumerate(components)]

            with patch(
                "i18nlib.reviewer_compare.create_quality_run_directory", return_value=directory / "run"
            ), patch(
                "i18nlib.reviewer_compare._bundle_selected_items", side_effect=fake_bundles
            ):
                report = run_freeze(
                    manifest, object(), pool_path=pool_path, gold_path=gold_path
                )
            self.assertEqual(24, report["planned_content_slots"])
            self.assertEqual(48, report["maximum_external_transfers"])
            template = json.loads((directory / "run" / "result-index-template.json").read_text())
            self.assertTrue(all(item == {
                "slot_id": item["slot_id"], "status": "pending",
                "assessment": None, "run_report": None,
            } for item in template["results"]))

    def test_provider_prompt_exposes_compatibility_matrix_and_scope_boundary(self) -> None:
        prompt = (ROOT / "i18n/prompts/pi-translation-reviewer-v2.md").read_text(encoding="utf-8")
        self.assertIn("The pair must be one of the following", prompt)
        self.assertIn("`entity-role`: `omitted`, `added`, `reversed`, `reassigned`", prompt)
        self.assertIn("changing “foes” to the broader “targets” is a scope change", prompt)
        self.assertIn("Never shorten, regenerate, reorder, or omit a `revision_id`", prompt)
        self.assertIn("translate, paraphrase, concatenate non-adjacent words", prompt)
        self.assertIn("on the source side whenever a genuine target addition", prompt)
        self.assertIn("Do not stop after reaching an", prompt)
        self.assertIn("intentional mechanics-aware adaptation", prompt)
        self.assertIn("item to `assessed`, and do not invent", prompt)
        self.assertIn("at most eight distinct findings per item", prompt)
        policy = load_comparison_policy(ROOT)[0]
        self.assertEqual(policy["max_items_per_bundle"], 2)
        self.assertEqual(policy["character_budget"], 16000)

    def test_report_stops_at_denied_calibration_without_holdout_metrics(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reviewer-compare-denied-") as temporary:
            directory = Path(temporary)
            revision = _revision(65_000)
            gold = {
                "contract": "tome4-reviewer-comparison-gold-v2", "schema_version": 2,
                "candidate_pool_id": "1" * 64, "human_confirmed": True,
                "fallback_stage": "none", "items": [{
                    "revision_id": revision, "split": "calibration", "gold_state": "assessed",
                    "semantic_state": "no-substantive-difference", "severity": "clean",
                    "findings_exhaustive": True,
                    "adjudication_rationale": "Fixture has no substantive difference.",
                    "controlled": False, "findings": [],
                }],
            }
            gold["gold_id"] = _sha(gold)
            gold_path = directory / "gold.json"
            gold_path.write_text(json.dumps(gold), encoding="utf-8")
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(json.dumps({"items": [{"revision_id": revision, "source": "A", "target": "甲"}]}), encoding="utf-8")
            prereg = {
                "contract": "tome4-reviewer-comparison-preregistration-v2", "schema_version": 2,
                "tool_version": TOOL_VERSION,
                "policy_sha256": load_comparison_policy(ROOT)[1],
                "implementation_sha256": _implementation_sha256(ROOT),
                "gold": str(gold_path), "gold_id": gold["gold_id"],
                "gold_sha256": hashlib.sha256(gold_path.read_bytes()).hexdigest(),
                "bundles": [{"path": str(bundle_path)}],
            }
            prereg["preregistration_id"] = _sha(prereg)
            prereg_path = directory / "prereg.json"
            prereg_path.write_text(json.dumps(prereg), encoding="utf-8")
            validation = {
                "contract": "tome4-reviewer-comparison-validation-v2", "schema_version": 2,
                "preregistration_id": prereg["preregistration_id"], "preregistration": str(prereg_path),
                "result_index": "fixture", "slot_reports": [], "observations": {},
                "holdout_cleared": False, "calibration_clearance": "denied",
                "calibration_checks": {"reviewer-a": {"passed": False}},
            }
            validation["validation_id"] = _sha(validation)
            validation_path = directory / "validation.json"
            validation_path.write_text(json.dumps(validation), encoding="utf-8")
            result = run_report(validation_path=validation_path)
            self.assertEqual("calibration-denied", result["decision"])
            report = json.loads(Path(result["report"]).read_text())
            self.assertEqual({}, report["metrics"])

    def test_validate_records_content_structure_failures_and_keeps_holdout_sealed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reviewer-compare-failure-") as temporary:
            directory = Path(temporary)
            policy, policy_sha = load_comparison_policy(ROOT)
            revision = _revision(66_000)
            bundle = {
                "bundle_id": _revision(66_001),
                "items": [{"revision_id": revision, "source": "foes", "target": "目标"}],
            }
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
            gold = {
                "contract": "tome4-reviewer-comparison-gold-v2", "schema_version": 2,
                "candidate_pool_id": "1" * 64, "human_confirmed": True,
                "fallback_stage": "none", "items": [{
                    "revision_id": revision, "split": "calibration", "gold_state": "assessed",
                    "semantic_state": "no-substantive-difference", "severity": "clean",
                    "findings_exhaustive": True,
                    "adjudication_rationale": "Fixture has no substantive difference.",
                    "controlled": False, "findings": [],
                }],
            }
            gold["gold_id"] = _sha(gold)
            gold_path = directory / "gold.json"
            gold_path.write_text(json.dumps(gold), encoding="utf-8")
            slots = []
            results = []
            payload = b"fixture-payload"
            prompt_sha256 = hashlib.sha256(
                (ROOT / "i18n/prompts/pi-translation-reviewer-v2.md").read_bytes()
            ).hexdigest()
            planned = [
                (round_number, model)
                for round_number in (1, 2) for model in policy["models"]
            ]
            for ordinal, (round_number, model) in enumerate(planned, start=1):
                slot_id = f"slot-{ordinal:03d}"
                slot = {
                    "slot_id": slot_id, "split": "calibration", "round": round_number,
                    "reviewer": model["alias"], "provider": model["provider"],
                    "model": model["model"], "thinking": model["thinking"],
                    "bundle": str(bundle_path), "bundle_id": bundle["bundle_id"],
                }
                slots.append(slot)
                report = {
                    "provider": model["provider"], "model": model["model"],
                    "thinking": model["thinking"], "bundle_id": bundle["bundle_id"],
                    "cache_decision": "disabled", "ok": False, "attempts": 1,
                    "failure_kind": "content-structure",
                    "pi_returncode": 0, "raw_output_sha256": "a" * 64,
                    "error": "Pi translation review finding pair is incompatible",
                    "elapsed_seconds": 1.0, "usage": None,
                    **_runner_lineage(
                        bundle_id=bundle["bundle_id"], model=model,
                        prompt_sha256=prompt_sha256, payload=payload,
                    ),
                }
                report_path = directory / f"{slot_id}-report.json"
                report_path.write_text(json.dumps(report), encoding="utf-8")
                results.append({
                    "slot_id": slot_id, "status": "content-structure-failure",
                    "assessment": None, "run_report": str(report_path),
                })
            holdout_slot = {
                **slots[0], "slot_id": "slot-005", "split": "holdout", "round": 1,
            }
            slots.append(holdout_slot)
            results.append({
                "slot_id": "slot-005", "status": "pending",
                "assessment": None, "run_report": None,
            })
            prereg = {
                "contract": "tome4-reviewer-comparison-preregistration-v2", "schema_version": 2,
                "tool_version": TOOL_VERSION, "version": "tome-1.7.6",
                "policy_sha256": policy_sha, "implementation_sha256": _implementation_sha256(ROOT),
                "gold": str(gold_path), "gold_id": gold["gold_id"],
                "gold_sha256": hashlib.sha256(gold_path.read_bytes()).hexdigest(),
                "prompt_sha256": prompt_sha256,
                "bundles": [{"path": str(bundle_path), "bundle_id": bundle["bundle_id"], "bundle_sha256": _sha(bundle)}],
                "slots": slots,
            }
            prereg["preregistration_id"] = _sha(prereg)
            prereg_path = directory / "prereg.json"
            prereg_path.write_text(json.dumps(prereg), encoding="utf-8")
            index = {
                "contract": "tome4-reviewer-comparison-result-index-v2", "schema_version": 2,
                "preregistration_id": prereg["preregistration_id"],
                "authorization_id": "authorized", "authorized_at": "now",
                "calibration_frozen_at": "later", "holdout_cleared": False,
                "holdout_cleared_at": None, "results": results,
            }
            index_path = directory / "index.json"
            index_path.write_text(json.dumps(index), encoding="utf-8")
            manifest = SimpleNamespace(root=ROOT, version="tome-1.7.6")
            with (
                patch("i18nlib.review.validate_review_bundle", return_value=bundle),
                patch(
                    "i18nlib.reviewer_compare.translation_provider_message",
                    return_value=payload,
                ),
                patch(
                    "i18nlib.reviewer_compare.create_quality_run_directory",
                    return_value=directory / "validation-run",
                ),
            ):
                output = run_validate(manifest, preregistration_path=prereg_path, result_index_path=index_path)
            validation = json.loads(Path(output["validation"]).read_text())
            self.assertEqual({"reviewer-a": 2, "reviewer-b": 2}, validation["structure_failures"]["calibration"])
            self.assertEqual(0.0, validation["calibration_schema_coverage"])
            self.assertEqual("denied", validation["calibration_clearance"])
            self.assertFalse(validation["holdout_cleared"])

            first_report_path = Path(results[0]["run_report"])
            first_report = json.loads(first_report_path.read_text())
            first_report_path.write_text(
                json.dumps({**first_report, "prompt_sha256": "f" * 64}),
                encoding="utf-8",
            )
            with (
                patch("i18nlib.review.validate_review_bundle", return_value=bundle),
                patch(
                    "i18nlib.reviewer_compare.translation_provider_message",
                    return_value=payload,
                ),
                self.assertRaisesRegex(ValidationError, "runner lineage"),
            ):
                run_validate(
                    manifest,
                    preregistration_path=prereg_path,
                    result_index_path=index_path,
                )
            first_report_path.write_text(json.dumps(first_report), encoding="utf-8")

            index["holdout_cleared"] = True
            index["holdout_cleared_at"] = "after-calibration"
            # Supply a failed holdout artifact too, so the validator reaches the
            # contradictory-clearance gate rather than merely rejecting pending coverage.
            results[-1] = {**results[0], "slot_id": "slot-005"}
            index_path.write_text(json.dumps(index), encoding="utf-8")
            with (
                patch("i18nlib.review.validate_review_bundle", return_value=bundle),
                patch(
                    "i18nlib.reviewer_compare.translation_provider_message",
                    return_value=payload,
                ),
            ):
                with self.assertRaisesRegex(ValidationError, "contradicts frozen calibration eligibility"):
                    run_validate(manifest, preregistration_path=prereg_path, result_index_path=index_path)

    def test_validate_uses_semantic_stability_flags_context_and_true_no_difference(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reviewer-compare-clearance-") as temporary:
            directory = Path(temporary)
            policy, policy_sha = load_comparison_policy(ROOT)
            revisions = (_revision(67_000), _revision(67_001))
            bundle = {
                "bundle_id": _revision(67_002),
                "items": [
                    {"revision_id": revisions[0], "source": "same", "target": "相同"},
                    {"revision_id": revisions[1], "source": "ambiguous", "target": "模糊"},
                ],
            }
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(json.dumps(bundle), encoding="utf-8")
            gold = {
                "contract": "tome4-reviewer-comparison-gold-v2",
                "schema_version": 2,
                "candidate_pool_id": "1" * 64,
                "human_confirmed": True,
                "fallback_stage": "none",
                "items": [
                    {
                        "revision_id": revisions[0], "split": "calibration",
                        "gold_state": "assessed",
                        "semantic_state": "no-substantive-difference",
                        "severity": "clean", "findings_exhaustive": True,
                        "adjudication_rationale": "Fixture is semantically equivalent.",
                        "controlled": False, "findings": [],
                    },
                    {
                        "revision_id": revisions[1], "split": "calibration",
                        "gold_state": "context-insufficient",
                        "semantic_state": "context-insufficient",
                        "severity": "context-insufficient", "findings_exhaustive": False,
                        "adjudication_rationale": "Fixture requires unavailable context.",
                        "controlled": False, "findings": [],
                    },
                ],
            }
            gold["gold_id"] = _sha(gold)
            gold_path = directory / "gold.json"
            gold_path.write_text(json.dumps(gold), encoding="utf-8")
            slots = []
            results = []
            payload = b"fixture-payload"
            prompt_sha256 = "2" * 64
            for ordinal, (round_number, model) in enumerate(
                (
                    (round_number, model)
                    for round_number in (1, 2)
                    for model in policy["models"]
                ),
                start=1,
            ):
                slot_id = f"slot-{ordinal:03d}"
                slots.append({
                    "slot_id": slot_id, "split": "calibration", "round": round_number,
                    "reviewer": model["alias"], "provider": model["provider"],
                    "model": model["model"], "thinking": model["thinking"],
                    "bundle": str(bundle_path), "bundle_id": bundle["bundle_id"],
                })
                assessment = {
                    "items": [
                        {"revision_id": revisions[0], "assessment_state": "assessed", "findings": []},
                        {"revision_id": revisions[1], "assessment_state": "context-insufficient", "findings": []},
                    ]
                }
                assessment_path = directory / f"{slot_id}-assessment.json"
                assessment_path.write_text(json.dumps(assessment), encoding="utf-8")
                report = {
                    "provider": model["provider"], "model": model["model"],
                    "thinking": model["thinking"], "bundle_id": bundle["bundle_id"],
                    "cache_decision": "disabled", "ok": True, "attempts": 1,
                    "elapsed_seconds": 1.0, "usage": None,
                    **_runner_lineage(
                        bundle_id=bundle["bundle_id"], model=model,
                        prompt_sha256=prompt_sha256, payload=payload,
                    ),
                }
                report_path = directory / f"{slot_id}-report.json"
                report_path.write_text(json.dumps(report), encoding="utf-8")
                results.append({
                    "slot_id": slot_id, "status": "success",
                    "assessment": str(assessment_path), "run_report": str(report_path),
                })
            prereg = {
                "contract": "tome4-reviewer-comparison-preregistration-v2",
                "schema_version": 2, "tool_version": TOOL_VERSION,
                "policy_sha256": policy_sha,
                "implementation_sha256": _implementation_sha256(ROOT),
                "gold": str(gold_path), "gold_id": gold["gold_id"],
                "gold_sha256": hashlib.sha256(gold_path.read_bytes()).hexdigest(),
                "prompt_sha256": prompt_sha256,
                "bundles": [{
                    "path": str(bundle_path), "bundle_id": bundle["bundle_id"],
                    "bundle_sha256": _sha(bundle),
                }],
                "slots": slots,
            }
            prereg["preregistration_id"] = _sha(prereg)
            prereg_path = directory / "prereg.json"
            prereg_path.write_text(json.dumps(prereg), encoding="utf-8")
            index = {
                "contract": "tome4-reviewer-comparison-result-index-v2",
                "schema_version": 2, "preregistration_id": prereg["preregistration_id"],
                "authorization_id": "authorized", "authorized_at": "now",
                "calibration_frozen_at": "later", "holdout_cleared": False,
                "holdout_cleared_at": None, "results": results,
            }
            index_path = directory / "index.json"
            index_path.write_text(json.dumps(index), encoding="utf-8")
            manifest = SimpleNamespace(root=ROOT, version="tome-1.7.6")
            with (
                patch("i18nlib.review.validate_review_bundle", return_value=bundle),
                patch(
                    "i18nlib.reviewer_compare.translation_provider_message",
                    return_value=payload,
                ),
                patch("i18nlib.reviewer_compare.make_evaluator_identity", return_value={}),
                patch(
                    "i18nlib.reviewer_compare.revalidate_translation_assessment",
                    side_effect=lambda **kwargs: ({}, kwargs["assessment"]),
                ),
                patch(
                    "i18nlib.reviewer_compare.create_quality_run_directory",
                    return_value=directory / "validation-run",
                ),
            ):
                output = run_validate(
                    manifest,
                    preregistration_path=prereg_path,
                    result_index_path=index_path,
                )
            validation = json.loads(Path(output["validation"]).read_text())
            self.assertEqual("cleared", validation["calibration_clearance"])
            for values in validation["calibration_checks"].values():
                self.assertEqual(1.0, values["semantic_claim_jaccard"])
                self.assertEqual(1.0, values["item_flag_agreement"])
                self.assertEqual(1.0, values["context_state_accuracy"])
                self.assertEqual(0.0, values["no_difference_false_positive_rate"])
                self.assertTrue(values["passed"])

    def test_selected_items_are_exact_production_v2_bundles(self) -> None:
        manifest = load_manifest()
        runtime = LuaRuntime(manifest)
        runtime.doctor()
        loader = LocaleLoader(runtime)
        selected = []
        for component in ("tome", "ashes-urhrok", "cults", "orcs"):
            spec = manifest.component(component)
            raw = (manifest.root / spec.translation).read_bytes()
            canonical = _translation_items_from_bytes(manifest, loader, component, raw)
            # Curated Gold order is independent of canonical file order.
            for item in reversed(canonical[:8]):
                selected.append({
                    "component": component, "revision_id": item["revision_id"],
                    "controlled": False, "split": "calibration",
                })
        with tempfile.TemporaryDirectory(prefix="reviewer-compare-v2-bundles-") as temporary:
            descriptors = _bundle_selected_items(
                manifest, loader, selected, Path(temporary), load_comparison_policy(ROOT)[0]
            )
            self.assertEqual(16, len(descriptors))
            self.assertEqual(32, sum(descriptor["count"] for descriptor in descriptors))
            for descriptor in descriptors:
                bundle = validate_review_bundle(manifest, Path(descriptor["path"]))
                self.assertEqual("tome4-translation-review-bundle-v2", bundle["review_contract"])
                self.assertLessEqual(descriptor["count"], 2)
                for item in bundle["items"]:
                    self.assertNotIn("semantic_state", item)
                    self.assertNotIn("adjudication_rationale", item)
                    self.assertNotIn("accepted_classifications", item)

    def test_report_applies_leak_first_winner_rule_to_frozen_gold(self) -> None:
        with tempfile.TemporaryDirectory(prefix="reviewer-compare-report-") as temporary:
            directory = Path(temporary)
            gold_items = []
            bundle_items = []
            observations = {}
            for index in range(64):
                revision = _revision(70_000 + index)
                split = "calibration" if index < 32 else "holdout"
                within_split = index % 32
                if within_split < 12:
                    severity = "major"
                elif within_split < 16:
                    severity = "minor"
                elif within_split < 30:
                    severity = "clean"
                else:
                    severity = "context-insufficient"
                accepted_difference = severity == "clean" and within_split < 18
                finding = {
                    "phenomenon": "other", "meaning_change": "unknown",
                    "accepted_classifications": [{
                        "phenomenon": "other", "meaning_change": "unknown",
                    }],
                    "classification_rationale": "Fixture primary classification.",
                    "source_evidence": {"quote": "Source", "occurrence": 1},
                    "target_evidence": {"quote": "目标", "occurrence": 1},
                }
                gold_items.append({
                    "revision_id": revision, "split": split,
                    "gold_state": (
                        "context-insufficient" if severity == "context-insufficient"
                        else "assessed"
                    ),
                    "semantic_state": (
                        "context-insufficient"
                        if severity == "context-insufficient"
                        else (
                            "substantive-difference"
                            if severity in {"major", "minor"} or accepted_difference
                            else "no-substantive-difference"
                        )
                    ),
                    "severity": severity,
                    "findings_exhaustive": (
                        severity == "clean" and not accepted_difference
                    ),
                    "adjudication_rationale": f"Fixture adjudication {index}.",
                    "controlled": False,
                    "findings": (
                        [finding]
                        if severity in {"major", "minor"} or accepted_difference
                        else []
                    ),
                })
                bundle_items.append({
                    "revision_id": revision, "source": f"Source {index}",
                    "target": f"目标 {index}",
                })
            for split, rounds in (("calibration", 2), ("holdout", 1)):
                revisions = [item for item in gold_items if item["split"] == split]
                for round_number in range(1, rounds + 1):
                    for reviewer in ("reviewer-a", "reviewer-b"):
                        key = f"{split}:{round_number}:{reviewer}"
                        observations[key] = {}
                        for item in revisions:
                            findings = []
                            if (
                                reviewer == "reviewer-a"
                                and item["semantic_state"] == "substantive-difference"
                            ):
                                findings = [{
                                    "finding_key": _sha([item["revision_id"], "finding"]),
                                    "phenomenon": "other", "meaning_change": "unknown",
                                    "source_evidence": {"quote": "Source", "occurrence": 1},
                                    "target_evidence": {"quote": "目标", "occurrence": 1},
                                }]
                            observations[key][item["revision_id"]] = {
                                "assessment_state": (
                                    "context-insufficient"
                                    if item["severity"] == "context-insufficient" else "assessed"
                                ),
                                "findings": findings,
                            }
            gold = {
                "contract": "tome4-reviewer-comparison-gold-v2", "schema_version": 2,
                "candidate_pool_id": "1" * 64, "human_confirmed": True,
                "fallback_stage": "none", "items": gold_items,
            }
            gold["gold_id"] = _sha(gold)
            gold_path = directory / "frozen-gold.json"
            gold_path.write_text(json.dumps(gold, ensure_ascii=False), encoding="utf-8")
            bundle_path = directory / "bundle.json"
            bundle_path.write_text(
                json.dumps({"items": bundle_items}, ensure_ascii=False), encoding="utf-8"
            )
            prereg = {
                "contract": "tome4-reviewer-comparison-preregistration-v2",
                "schema_version": 2, "tool_version": TOOL_VERSION,
                "policy_sha256": load_comparison_policy(ROOT)[1],
                "implementation_sha256": _implementation_sha256(ROOT),
                "gold": str(gold_path), "gold_id": gold["gold_id"],
                "gold_sha256": hashlib.sha256(gold_path.read_bytes()).hexdigest(),
                "bundles": [{"path": str(bundle_path)}],
            }
            prereg["preregistration_id"] = _sha(prereg)
            prereg_path = directory / "preregistration.json"
            prereg_path.write_text(json.dumps(prereg), encoding="utf-8")
            validation = {
                "contract": "tome4-reviewer-comparison-validation-v2", "schema_version": 2,
                "preregistration_id": prereg["preregistration_id"],
                "preregistration": str(prereg_path), "result_index": "fixture",
                "slot_reports": [
                    {"reviewer": reviewer, "attempts": 1, "elapsed_seconds": 1.0,
                     "payload_bytes": 10, "usage": None}
                    for reviewer in ("reviewer-a", "reviewer-b")
                ],
                "observations": observations,
            }
            validation["validation_id"] = _sha(validation)
            validation_path = directory / "validation.json"
            validation_path.write_text(json.dumps(validation), encoding="utf-8")
            report = run_report(validation_path=validation_path)
            self.assertEqual("winner:reviewer-a", report["decision"])


if __name__ == "__main__":
    unittest.main()
