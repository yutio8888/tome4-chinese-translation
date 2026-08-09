from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.config import load_manifest
from i18nlib.errors import ValidationError
from i18nlib.facts_study import (
    _tree_identity,
    ARMS, ASSESSMENT_CONTRACT, PACKET_CONTRACT, SAMPLE_CONTRACT, align_claims,
    build_bundle, build_candidate_sample, build_facts_author_bundle, build_fake_assessments, build_neutral_packets,
    build_preregistration, build_report, build_schedule, canonical_sha256,
    load_arm_prompt, load_historical_exclusions, load_protocol, load_study_inputs,
    run_report, run_validate,
    study_harness_identity,
    union_and_dedupe, validate_gold,
    validate_assessment, validate_gold_authoring_artifacts,
    validate_external_run_lineage, validate_neutral_equivalence, validate_packets,
    validate_historical_exclusions, validate_sample,
)
from i18nlib.pi_facts_study import _claim_slot
from i18nlib.report import write_json


def fixture():
    items = []
    strata = [
        "ordinary-semantic", "term-name", "condition-number-mechanism", "ui",
        "acceptable-localization",
    ]
    for index in range(20):
        items.append({
            "index": index, "revision_id": hashlib.sha256(f"r{index}".encode()).hexdigest(),
            "source": f"Source {index}", "target": f"目标 {index}",
            "item_kind": ("semantic", "term", "mechanics", "ui", "localization")[index % 5],
            "source_tag": "test", "bounded_context": [], "stratum": strata[index % 5],
        })
    exclusion_registry = json.loads(
        (ROOT / "i18n" / "quality" / "facts-study-exclusions-v1.json").read_text()
    )
    historical_exclusions = sorted({
        revision_id
        for lineage in exclusion_registry["lineages"]
        for revision_id in lineage["revision_ids"]
    })
    sample = {
        "contract": SAMPLE_CONTRACT, "schema_version": 1,
        "study_id": "", "seed": "fixture",
        "inventory_sha256": "1" * 64, "excluded_revision_ids": historical_exclusions,
        "exclusion_revision_ids_sha256": canonical_sha256(historical_exclusions),
        "items": items,
    }
    sample["study_id"] = canonical_sha256({
        "contract": SAMPLE_CONTRACT, "seed": sample["seed"],
        "inventory_sha256": sample["inventory_sha256"],
        "excluded": sample["excluded_revision_ids"], "items": sample["items"],
    })
    facts = {
        "contract": PACKET_CONTRACT, "schema_version": 1,
        "study_id": sample["study_id"], "packet_kind": "facts", "status": "frozen",
        "non_exhaustive": True, "supplemental_only": True,
        "authoring_lineage": {
            "role": "facts-author", "actor_id": "facts-human",
            "target_defects_seen": False, "gold_seen": False,
            "common_input_restatements_excluded": True,
            "source_inputs_sha256": canonical_sha256(build_facts_author_bundle(sample)),
        },
        "items": [],
    }
    for index, item in enumerate(items):
        facts["items"].append({"revision_id": item["revision_id"], "facts": [{
            "fact_id": f"fact-{index:016x}", "fact_type": "mechanism",
            "statement": f"Verified atomic context {index}",
            "provenance": {"kind": "public-source", "reference": f"fixture:{index}", "sha256": "3" * 64},
        }]})
    gold_items = []
    claim_serial = 0
    for index, item in enumerate(items):
        clean = index >= 15
        claims = []
        if not clean:
            count = 2 if index == 0 else 1
            for subindex in range(count):
                claims.append({
                    "claim_id": f"claim-{index:02d}-{subindex:x}", "error_family": "semantic",
                    "phenomenon": "condition", "meaning_change": "reversed",
                    "source_evidence": {"quote": item["source"], "occurrence": 1},
                    "target_evidence": {"quote": item["target"], "occurrence": 1},
                    "fact_ids": [f"fact-{index:016x}"] if claim_serial < 8 else [],
                    "requires_manual": False,
                })
                claim_serial += 1
        gold_items.append({
            "revision_id": item["revision_id"], "clean": clean,
            "fact_trap": index in (15, 16, 17),
            "acceptable_localization": index in (18, 19), "claims": claims,
        })
    gold = {
        "contract": "tome4-quality-facts-study-gold-v1", "schema_version": 1,
        "study_id": sample["study_id"], "status": "frozen",
        "review_lineage": {
            "reviewer_ids": ["human-a", "human-b"],
            "review_artifact_sha256s": ["4" * 64, "5" * 64],
            "adjudicator_id": "human-c", "adjudication_artifact_sha256": "6" * 64,
        },
        "items": gold_items,
    }
    return sample, facts, gold


class FactsStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()
        cls.protocol = load_protocol(cls.manifest)

    def setUp(self):
        self.sample, self.facts, self.gold = fixture()
        validate_sample(self.sample)
        validate_packets(self.facts, sample=self.sample, expected_kind="facts")
        self.neutral = build_neutral_packets(self.facts, sample=self.sample)
        validate_packets(self.neutral, sample=self.sample, expected_kind="neutral")
        self.prompts = {arm: load_arm_prompt(self.manifest, arm) for arm in ARMS}
        self.bundles = {
            arm: build_bundle(
                sample=self.sample, facts=self.facts, neutral=self.neutral, arm=arm,
                prompt_sha256=hashlib.sha256(self.prompts[arm].encode()).hexdigest(),
            ) for arm in ARMS
        }

    def prereg(self):
        return build_preregistration(
            protocol=self.protocol, sample=self.sample, facts=self.facts,
            neutral=self.neutral, gold=self.gold, bundles=self.bundles,
            prompts=self.prompts,
        )

    def test_prompt_common_block_is_byte_identical(self):
        def common(text):
            return text.split("<!-- COMMON-V1-START -->", 1)[1].split("<!-- COMMON-V1-END -->", 1)[0]
        self.assertEqual(1, len({common(prompt) for prompt in self.prompts.values()}))
        self.assertIn("exhaustively", self.prompts["B"])
        self.assertNotIn("exhaustively", self.prompts["A"])
        checklist_off = "<!-- CHECKLIST-OFF-V1 -->\nInspect each item for clearly observable substantive errors. No exhaustive checklist is required."
        checklist_on = "<!-- CHECKLIST-ON-V1 -->\nFor every item, exhaustively check: omitted or added meaning; wrong condition, number, scope, polarity, entity relation, timing, or mechanism; noncanonical terminology or proper names supported by the visible text; and changed UI meaning. Accept faithful localization that is not literal."
        self.assertIn(checklist_off, self.prompts["A"])
        self.assertIn(checklist_off, self.prompts["C"])
        for arm in ("B", "D", "N", "L"):
            self.assertIn(checklist_on, self.prompts[arm])
        facts_first = "<!-- FACTS-FIRST-V1 -->\nEach item includes a non-exhaustive supplemental Facts packet before the translation block. Facts are verified context, not hints about whether an error exists. Cite supporting fact_id values only when the claim actually depends on them."
        self.assertIn(facts_first, self.prompts["C"])
        self.assertIn(facts_first, self.prompts["D"])

    def test_bundle_views_do_not_leak_hidden_inputs(self):
        forbidden = {"relevant_terms", "domain_hints", "risk_flags", "gate_signals", "gold", "anchors"}
        for arm in ("A", "B"):
            self.assertFalse(any(forbidden & set(item) for item in self.bundles[arm]["items"]))
            self.assertTrue(all([block["block_type"] for block in item["content_blocks"]] == ["translation"] for item in self.bundles[arm]["items"]))
        self.assertTrue(all([block["block_type"] for block in item["content_blocks"]] == ["supplemental", "translation"] for item in self.bundles["F"]["items"]))
        self.assertTrue(all([block["block_type"] for block in item["content_blocks"]] == ["translation", "supplemental"] for item in self.bundles["L"]["items"]))
        self.assertNotIn("assessment", json.dumps(self.bundles["F"]))
        author_bundle = build_facts_author_bundle(self.sample)
        serialized = json.dumps(author_bundle, ensure_ascii=False)
        self.assertNotIn('"target"', serialized)
        self.assertNotIn("目标", serialized)
        self.assertEqual("tome4-quality-facts-author-bundle-v2", author_bundle["contract"])
        self.assertEqual(0, author_bundle["fact_policy"]["min_facts_per_item"])
        self.assertEqual("forbidden", author_bundle["fact_policy"]["common_input_restatements"])

    def test_neutral_packet_shape_and_canonical_byte_length(self):
        validate_neutral_equivalence(self.facts, self.neutral)
        for left, right in zip(self.facts["items"], self.neutral["items"]):
            lraw = json.dumps(left["facts"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
            rraw = json.dumps(right["facts"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
            self.assertEqual(len(lraw), len(rraw))
        escaped = copy.deepcopy(self.facts)
        escaped["items"][0]["facts"][0]["statement"] = 'Mechanic says "quoted" and \\escaped\nnext.'
        neutral = build_neutral_packets(escaped, sample=self.sample)
        validate_neutral_equivalence(escaped, neutral)

    def test_frozen_gold_requires_real_lineage_and_minima(self):
        validate_gold(self.gold, sample=self.sample, facts=self.facts)
        bad = copy.deepcopy(self.gold)
        bad["review_lineage"]["reviewer_ids"] = ["same", "same"]
        with self.assertRaises(ValidationError):
            validate_gold(bad, sample=self.sample, facts=self.facts)

    def test_frozen_gold_binds_two_review_files_and_adjudication(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            review_paths = []
            reviewer_ids = ["review-a", "review-b"]
            for index, reviewer_id in enumerate(reviewer_ids):
                path = root / f"review-{index}.json"
                write_json(path, {
                    "contract": "tome4-quality-facts-study-gold-review-v1",
                    "schema_version": 1, "study_id": self.sample["study_id"],
                    "reviewer_id": reviewer_id, "independent": True,
                    "items": self.gold["items"],
                })
                review_paths.append(path)
            review_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in review_paths]
            adjudication_path = root / "adjudication.json"
            write_json(adjudication_path, {
                "contract": "tome4-quality-facts-study-gold-adjudication-v1",
                "schema_version": 1, "study_id": self.sample["study_id"],
                "status": "frozen", "adjudicator_id": "adjudicator",
                "review_artifact_sha256s": review_hashes, "items": self.gold["items"],
            })
            gold = copy.deepcopy(self.gold)
            gold["review_lineage"] = {
                "reviewer_ids": reviewer_ids, "review_artifact_sha256s": review_hashes,
                "adjudicator_id": "adjudicator",
                "adjudication_artifact_sha256": hashlib.sha256(adjudication_path.read_bytes()).hexdigest(),
            }
            validate_gold(gold, sample=self.sample, facts=self.facts)
            validate_gold_authoring_artifacts(
                review_paths=review_paths, adjudication_path=adjudication_path,
                gold=gold, sample=self.sample, facts=self.facts,
            )
            bad = copy.deepcopy(gold)
            bad["review_lineage"]["adjudicator_id"] = reviewer_ids[0]
            with self.assertRaises(ValidationError):
                validate_gold(bad, sample=self.sample, facts=self.facts)

    def test_fact_ids_are_globally_unique(self):
        bad = copy.deepcopy(self.facts)
        bad["items"][1]["facts"][0]["fact_id"] = bad["items"][0]["facts"][0]["fact_id"]
        with self.assertRaises(ValidationError):
            validate_packets(bad, sample=self.sample, expected_kind="facts")

    def test_supplemental_fact_policy_allows_zero_and_rejects_common_input_restatements(self):
        empty = copy.deepcopy(self.facts)
        empty["items"][0]["facts"] = []
        validate_packets(empty, sample=self.sample, expected_kind="facts")

        restatement = copy.deepcopy(self.facts)
        restatement["items"][0]["facts"][0]["provenance"] = {
            "kind": "public-source",
            "reference": "facts-author-bundle.json#/items/0/source",
            "sha256": "3" * 64,
        }
        with self.assertRaises(ValidationError):
            validate_packets(restatement, sample=self.sample, expected_kind="facts")

        legacy_kind = copy.deepcopy(self.facts)
        legacy_kind["items"][0]["facts"][0]["provenance"]["kind"] = "bundle-source"
        with self.assertRaises(ValidationError):
            validate_packets(legacy_kind, sample=self.sample, expected_kind="facts")

        unattested = copy.deepcopy(self.facts)
        unattested["authoring_lineage"]["common_input_restatements_excluded"] = False
        with self.assertRaises(ValidationError):
            validate_packets(unattested, sample=self.sample, expected_kind="facts")

    def test_empty_fact_items_preserve_neutral_shape_and_facts_only_validation(self):
        facts = copy.deepcopy(self.facts)
        facts["items"][0]["facts"] = []
        neutral = build_neutral_packets(facts, sample=self.sample)
        validate_packets(neutral, sample=self.sample, expected_kind="neutral")
        validate_neutral_equivalence(facts, neutral)
        self.assertEqual([], neutral["items"][0]["facts"])

    def test_neutral_fact_ids_are_host_generated_and_cannot_leak_encoded_claims(self):
        encoded = copy.deepcopy(self.facts)
        encoded["items"][0]["facts"][0]["fact_id"] = "fact-666972652d64616d"
        validate_packets(encoded, sample=self.sample, expected_kind="facts")
        neutral = build_neutral_packets(encoded, sample=self.sample)
        self.assertNotEqual(encoded["items"][0]["facts"][0]["fact_id"], neutral["items"][0]["facts"][0]["fact_id"])
        self.assertTrue(all(
            len(fact["fact_id"]) == 21
            and fact["fact_id"].startswith("fact-")
            and all(character in "0123456789abcdef" for character in fact["fact_id"][5:])
            for item in neutral["items"]
            for fact in item["facts"]
        ))
        tampered = copy.deepcopy(neutral)
        tampered["items"][0]["facts"][0]["fact_id"] = "fact-666972652d64616d"
        with self.assertRaises(ValidationError):
            validate_packets(tampered, sample=self.sample, expected_kind="neutral")

    def test_preregistration_binds_shared_runner_code_and_pi_executable(self):
        identity = study_harness_identity()
        self.assertIn("i18nlib/pi_quality.py", identity)
        self.assertIn("i18nlib/pi_agent.py", identity)
        self.assertIn("i18nlib/pi_file_review.py", identity)
        self.assertIn("pi-quality-facts-study", identity)
        prereg = self.prereg()
        self.assertEqual(canonical_sha256(identity), prereg["harness_sha256"])
        self.assertEqual(64, len(prereg["pi_executable"]["sha256"]))
        self.assertTrue(Path(prereg["pi_executable"]["path"]).is_file())
        self.assertGreater(prereg["pi_executable"]["package_tree"]["file_count"], 1)
        self.assertGreater(prereg["pi_executable"]["node_tree"]["file_count"], 1)

    def test_runtime_tree_identity_changes_when_a_transitive_dependency_changes(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            dependency = root / "main.js"
            dependency.write_text("first", encoding="utf-8")
            first = _tree_identity(root)
            dependency.write_text("second", encoding="utf-8")
            second = _tree_identity(root)
            self.assertNotEqual(first["sha256"], second["sha256"])

    def test_campaign_rejects_a_different_authorization_before_claiming_slot(self):
        schedule = [
            {"slot_id": "slot-1", "ordinal": 1},
            {"slot_id": "slot-2", "ordinal": 2},
        ]
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            first_path = _claim_slot(
                root, "p" * 64, schedule[0], schedule, "authorization-a", "1" * 64
            )
            first = json.loads(first_path.read_text(encoding="utf-8"))
            first["state"] = "succeeded"
            write_json(first_path, first)
            with self.assertRaises(ValidationError):
                _claim_slot(
                    root, "p" * 64, schedule[1], schedule,
                    "authorization-b", "2" * 64,
                )
            second_path = first_path.parent / "slot-2.json"
            self.assertFalse(second_path.exists())
            claimed = _claim_slot(
                root, "p" * 64, schedule[1], schedule,
                "authorization-a", "2" * 64,
            )
            self.assertEqual(second_path, claimed)

    def test_schedule_is_recomputable_and_exact(self):
        first = build_schedule(self.protocol, self.bundles, self.prompts)
        second = build_schedule(self.protocol, self.bundles, self.prompts)
        self.assertEqual(first, second)
        self.assertEqual(33, len(first))
        self.assertEqual(list(range(1, 34)), sorted(slot["ordinal"] for slot in first))
        self.assertTrue(all(slot["cache"] == "disabled" and slot["retry_policy"] == "none" for slot in first))

    def test_fake_runner_replays_all_33_slots_and_report(self):
        prereg = self.prereg()
        assessments = build_fake_assessments(
            preregistration=prereg, sample=self.sample, gold=self.gold,
            bundles=self.bundles,
        )
        self.assertEqual(33, len(assessments))
        slot_map = {slot["slot_id"]: slot for slot in prereg["schedule"]}
        assessments = {
            slot_id: validate_assessment(
                value, sample=self.sample, facts=self.facts,
                bundle=self.bundles[slot_map[slot_id]["arm"]], slot=slot_map[slot_id],
            )
            for slot_id, value in assessments.items()
        }
        report = build_report(
            preregistration=prereg,
            gold=validate_gold(self.gold, sample=self.sample, facts=self.facts),
            assessments=assessments, sample=self.sample, protocol=self.protocol,
        )
        self.assertFalse(report["holdout_clearance"])
        self.assertEqual(33, len(report["run_metrics"]))
        self.assertEqual(6, len(report["two_stage_metrics"]))
        self.assertEqual(8, report["run_metrics"]["luna-b-1"]["counts"]["true_positive"])
        self.assertEqual(8, report["run_metrics"]["luna-f-1"]["counts"]["true_positive"])
        self.assertEqual(16, report["two_stage_metrics"]["luna-t-1"]["counts"]["true_positive"])
        self.assertEqual(1.0, report["pooled_metrics"]["luna"]["T"]["precision"]["value"])
        self.assertEqual(1.0, report["pooled_metrics"]["luna"]["T"]["recall"]["value"])
        self.assertIn("T-B", report["paired_item_bootstrap"]["luna"])
        self.assertEqual(2000, report["paired_item_bootstrap"]["luna"]["T-B"]["per_run"][0]["recall"]["replicates"])
        self.assertEqual(2000, report["paired_item_bootstrap"]["luna"]["T-B"]["pooled"]["recall"]["replicates"])

    def test_fake_validation_artifacts_round_trip_into_report(self):
        prereg = self.prereg()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            paths = {}
            for name, value in (("sample", self.sample), ("facts", self.facts),
                                ("neutral", self.neutral), ("gold", self.gold),
                                ("prereg", prereg)):
                paths[name] = root / f"{name}.json"
                write_json(paths[name], value)
            bundle_paths = []
            for arm, bundle in self.bundles.items():
                path = root / f"bundle-{arm.lower()}.json"
                write_json(path, bundle)
                bundle_paths.append(path)
            forged = copy.deepcopy(prereg)
            forged["schedule"][0]["provider"] = "forged-provider"
            forged["preregistration_id"] = canonical_sha256({
                key: value for key, value in forged.items() if key != "preregistration_id"
            })
            forged_path = root / "forged-prereg.json"
            write_json(forged_path, forged)
            with self.assertRaises(ValidationError):
                load_study_inputs(
                    self.manifest, sample_path=paths["sample"], facts_path=paths["facts"],
                    neutral_path=paths["neutral"], gold_path=paths["gold"],
                    prereg_path=forged_path, bundle_paths=bundle_paths,
                )
            counter = 0
            def run_directory(_repo, kind):
                nonlocal counter
                counter += 1
                path = root / f"run-{counter}-{kind}"
                path.mkdir()
                return path
            with patch("i18nlib.facts_study.create_quality_run_directory", side_effect=run_directory):
                validation = run_validate(
                    self.manifest, sample_path=paths["sample"], facts_path=paths["facts"],
                    neutral_path=paths["neutral"], gold_path=paths["gold"],
                    prereg_path=paths["prereg"], bundle_paths=bundle_paths,
                    assessment_paths=[], runner_report_paths=[], fake_runner=True,
                )
                report = run_report(self.manifest, validation_path=Path(validation["validation"]))
            self.assertEqual(33, len(report["run_metrics"]))
            self.assertFalse(report["holdout_clearance"])
            self.assertFalse(report["external_evidence"])
            self.assertEqual("non-evidentiary-offline-replay", report["decision"]["result"])
            with patch("i18nlib.facts_study.create_quality_run_directory", side_effect=run_directory):
                with self.assertRaises(ValidationError):
                    run_validate(
                        self.manifest, sample_path=paths["sample"], facts_path=paths["facts"],
                        neutral_path=paths["neutral"], gold_path=paths["gold"],
                        prereg_path=paths["prereg"], bundle_paths=bundle_paths,
                        assessment_paths=[Path(path) for path in validation["assessments"].values()],
                        runner_report_paths=[], fake_runner=False,
                    )

    def test_external_lineage_requires_all_runner_reports_and_ledgers(self):
        prereg = self.prereg()
        assessments = build_fake_assessments(
            preregistration=prereg, sample=self.sample, gold=self.gold,
            bundles=self.bundles,
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            assessment_paths = {}
            report_paths = []
            campaign = root / ".artifacts" / "i18n" / "quality" / "facts-study-campaigns" / prereg["preregistration_id"]
            campaign.mkdir(parents=True)
            authorization_sha = "a" * 64
            for slot in prereg["schedule"]:
                slot_id = slot["slot_id"]
                assessment_path = root / "assessments" / f"{slot_id}.json"
                write_json(assessment_path, assessments[slot_id])
                assessment_paths[slot_id] = assessment_path
                report_path = root / "reports" / f"{slot_id}.json"
                execution_id = hashlib.sha256(f"exec:{slot_id}".encode()).hexdigest()
                report = {
                    "contract": "tome4-quality-facts-study-runner-report-v1", "ok": True,
                    "study_id": self.sample["study_id"], "preregistration_id": prereg["preregistration_id"],
                    "slot_id": slot_id, "ordinal": slot["ordinal"], "arm": slot["arm"],
                    "seed": slot["seed"], "execution_id": execution_id,
                    "provider": slot["provider"], "model": slot["model"], "thinking": slot["thinking"],
                    "harness_sha256": prereg["harness_sha256"],
                    "pi_executable": prereg["pi_executable"],
                    "cache_decision": "disabled", "replacement_policy": "forbidden",
                    "attempts": 1, "charged_or_possible_transfers": 1, "shards": 1,
                    "blind_inputs": {"gold": False, "other_assessments": False, "anchors": False, "holdout": False},
                    "report": str(report_path), "run_directory": str(report_path.parent),
                    "runner_report_id": "", "assessment": str(assessment_path),
                    "normalization": "none", "assessment_sha256": hashlib.sha256(assessment_path.read_bytes()).hexdigest(),
                    "raw_output_sha256": "b" * 64, "findings": 0, "elapsed_seconds": 1.0,
                }
                report["runner_report_id"] = canonical_sha256({
                    key: value for key, value in report.items()
                    if key not in ("runner_report_id", "report", "run_directory", "elapsed_seconds")
                })
                write_json(report_path, report)
                report_paths.append(report_path)
                write_json(campaign / f"{slot_id}.json", {
                    "contract": "tome4-quality-facts-study-slot-ledger-v1",
                    "preregistration_id": prereg["preregistration_id"], "slot_id": slot_id,
                    "state": "succeeded", "authorization_sha256": authorization_sha,
                    "execution_id": execution_id, "runner_report": str(report_path),
                    "runner_report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
                })
            validated = validate_external_run_lineage(
                SimpleNamespace(root=root), prereg=prereg,
                assessment_paths_by_slot=assessment_paths,
                runner_report_paths=report_paths,
            )
            self.assertEqual(33, len(validated))
            with self.assertRaises(ValidationError):
                validate_external_run_lineage(
                    SimpleNamespace(root=root), prereg=prereg,
                    assessment_paths_by_slot=assessment_paths,
                    runner_report_paths=report_paths[:-1],
                )

    def test_host_union_is_symmetric_permutation_invariant_and_no_double_count(self):
        prereg = self.prereg()
        assessments = build_fake_assessments(preregistration=prereg, sample=self.sample, gold=self.gold, bundles=self.bundles)
        slot_map = {slot["slot_id"]: slot for slot in prereg["schedule"]}
        b = validate_assessment(
            assessments["luna-b-1"], sample=self.sample, facts=self.facts,
            bundle=self.bundles["B"], slot=slot_map["luna-b-1"],
        )
        f = validate_assessment(
            assessments["luna-f-1"], sample=self.sample, facts=self.facts,
            bundle=self.bundles["F"], slot=slot_map["luna-f-1"],
        )
        left = union_and_dedupe(b, f)
        right = union_and_dedupe(f, b)
        self.assertEqual(left, right)
        shuffled = copy.deepcopy(b)
        for item in shuffled["items"]:
            item["findings"].reverse()
        self.assertEqual(left, union_and_dedupe(shuffled, f))
        expected = sum(len(item["claims"]) for item in self.gold["items"])
        self.assertEqual(expected, sum(len(findings) for findings in left.values()))
        overlap_left = copy.deepcopy(b)
        overlap_right = copy.deepcopy(b)
        overlap_left["items"][7]["findings"][0]["explanation"] = "left wording"
        overlap_right["items"][7]["findings"][0]["explanation"] = "right wording"
        self.assertEqual(
            union_and_dedupe(overlap_left, overlap_right),
            union_and_dedupe(overlap_right, overlap_left),
        )

        def finding(start, end, label):
            value = copy.deepcopy(overlap_left["items"][7]["findings"][0])
            value["source_evidence"].update(state="exact", start=start, end=end)
            value["target_evidence"].update(state="exact", start=start, end=end)
            value["explanation"] = label
            value["supported_fact_ids"] = []
            return value

        ambiguous_left = {"items": [{
            "revision_id": "ambiguous",
            "findings": [finding(0, 2, "left-a"), finding(1, 3, "left-b")],
        }]}
        ambiguous_right = {"items": [{
            "revision_id": "ambiguous",
            "findings": [
                finding(0, 1, "right-a"), finding(0, 3, "right-b"),
                finding(1, 5, "right-c"),
            ],
        }]}
        self.assertEqual(
            union_and_dedupe(ambiguous_left, ambiguous_right),
            union_and_dedupe(ambiguous_right, ambiguous_left),
        )

    def test_alignment_is_deterministic_and_does_not_chain_merge(self):
        claims = validate_gold(self.gold, sample=self.sample, facts=self.facts)["items"][0]["claims"]
        self.assertEqual(align_claims(claims, claims), align_claims(claims, claims))
        self.assertEqual(2, len(align_claims(claims, claims)))
        forward = {(claims[left]["claim_id"], claims[right]["claim_id"]) for left, right in align_claims(claims, claims)}
        reversed_claims = list(reversed(claims))
        permuted = {(reversed_claims[left]["claim_id"], claims[right]["claim_id"]) for left, right in align_claims(reversed_claims, claims)}
        symmetric = {(claims[right]["claim_id"], claims[left]["claim_id"]) for left, right in align_claims(claims, claims)}
        self.assertEqual(forward, permuted)
        self.assertEqual(forward, symmetric)

    def test_contracts_are_isolated_from_legacy(self):
        self.assertEqual("tome4-quality-facts-study-assessment-v1", ASSESSMENT_CONTRACT)
        self.assertEqual("tome4-quality-fact-packet-v2", PACKET_CONTRACT)
        self.assertNotEqual("tome4-quality-assessment-v3", ASSESSMENT_CONTRACT)
        self.assertNotEqual("tome4-quality-sample-v1", SAMPLE_CONTRACT)
        legacy_schema = json.loads(
            (ROOT / "i18n" / "quality" / "schemas" / "fact-packet-v1.schema.json").read_text()
        )
        self.assertEqual("tome4-quality-fact-packet-v1", legacy_schema["$id"])
        legacy_packet = copy.deepcopy(self.facts)
        legacy_packet["contract"] = "tome4-quality-fact-packet-v1"
        legacy_packet.pop("supplemental_only")
        legacy_packet["authoring_lineage"].pop("common_input_restatements_excluded")
        with self.assertRaises(ValidationError):
            validate_packets(legacy_packet, sample=self.sample, expected_kind="facts")

    def test_failed_pilot_revisions_are_required_historical_exclusions(self):
        required = load_historical_exclusions(self.manifest)
        self.assertEqual(20, len(required))
        validate_historical_exclusions(self.manifest, self.sample)
        bad = copy.deepcopy(self.sample)
        bad["excluded_revision_ids"] = bad["excluded_revision_ids"][1:]
        bad["exclusion_revision_ids_sha256"] = canonical_sha256(bad["excluded_revision_ids"])
        bad["study_id"] = canonical_sha256({
            "contract": SAMPLE_CONTRACT, "seed": bad["seed"],
            "inventory_sha256": bad["inventory_sha256"],
            "excluded": bad["excluded_revision_ids"], "items": bad["items"],
        })
        validate_sample(bad)
        with self.assertRaises(ValidationError):
            validate_historical_exclusions(self.manifest, bad)

    def test_sample_cannot_overlap_frozen_exclusions(self):
        bad = copy.deepcopy(self.sample)
        bad["excluded_revision_ids"] = [bad["items"][0]["revision_id"]]
        bad["exclusion_revision_ids_sha256"] = canonical_sha256(bad["excluded_revision_ids"])
        bad["study_id"] = canonical_sha256({
            "contract": SAMPLE_CONTRACT, "seed": bad["seed"],
            "inventory_sha256": bad["inventory_sha256"],
            "excluded": bad["excluded_revision_ids"], "items": bad["items"],
        })
        with self.assertRaises(ValidationError):
            validate_sample(bad)

    def test_long_source_seed_is_bounded_and_inherits_exclusion_lineage(self):
        profiles = ("dialogue", "mechanics", "narrative", "runtime-log", "term-name", "ui", "unknown")
        lengths = (10, 100, 500, 1000, 1400, 1700)
        rows = []
        for profile in profiles:
            for length in lengths:
                rows.append({
                    "revision_id": hashlib.sha256(f"{profile}:{length}".encode()).hexdigest(),
                    "source": profile + ":" + "s" * (length - len(profile) - 1),
                    "target": "目标", "profile": profile,
                    "item_kind": "semantic", "source_tag": "test", "context_neighbors": [],
                })
        excluded = rows[0]["revision_id"]
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            inventory = root / "inventory.jsonl"
            inventory.write_text("".join(json.dumps(row) + "\n" for row in rows))
            exclusion = root / "prior-sample.json"
            write_json(exclusion, {"excluded_revision_ids": [excluded], "items": []})
            sample, _, _ = build_candidate_sample(
                inventory_path=inventory, exclusion_paths=[exclusion],
                seed="tome4-facts-study-v2-long-source-v1-test",
            )
        self.assertIn(excluded, sample["excluded_revision_ids"])
        self.assertNotIn(excluded, {item["revision_id"] for item in sample["items"]})
        self.assertEqual(20, len({(item["source"], item["target"]) for item in sample["items"]}))
        self.assertEqual([1400] * len(profiles), [len(item["source"]) for item in sample["items"][:len(profiles)]])
        self.assertLessEqual(max(len(item["source"]) for item in sample["items"]), 1700)


if __name__ == "__main__":
    unittest.main()
