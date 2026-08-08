from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.config import load_manifest
from i18nlib.errors import ValidationError
from i18nlib.facts_curation import (
    CURATION_ASSESSMENT_CONTRACT,
    CURATION_CURATOR_ASSESSMENT_CONTRACT,
    CURATION_FACTS_AUTHOR_BUNDLE_CONTRACT,
    CURATION_GOLD_ADJUDICATION_CONTRACT,
    CURATION_GOLD_REVIEW_CONTRACT,
    CURATION_GOLD_CONTRACT,
    CURATION_PACKET_CONTRACT,
    CURATION_POOL_CONTRACT,
    CURATION_PREREG_CONTRACT,
    CURATION_SAMPLE_CONTRACT,
    CONTROLLED_MUTATION_CONTRACT,
    CONTROLLED_VARIANTS_CONTRACT,
    SELECTION_SEED,
    STRATA,
    build_candidate_pool,
    build_curator_bundle,
    build_facts_author_bundle,
    build_neutral_packets,
    build_preregistration,
    canonical_sha256,
    load_protocol,
    run_curation_build,
    run_curation_bundles,
    run_curation_prepare,
    run_curation_report,
    run_curation_select,
    run_curation_validate,
    select_final_sample,
    validate_curator_assessment,
    validate_gold,
    validate_gold_authoring_artifacts,
    validate_packets,
    validate_pool,
    validate_sample,
)
from i18nlib.facts_study import (
    build_schedule,
    load_arm_prompt,
    validate_historical_exclusions,
)
from i18nlib.report import write_json


# ---------------------------------------------------------------------------
# Fixture inventory: 25 term, 25 mechanics, 20 entity, 17 ui, 20 general
# ---------------------------------------------------------------------------


def _row(revision_id: str, source: str, profile: str, source_tag: str, section: str,
         relevant_terms: list[dict], target: str) -> dict:
    return {
        "revision_id": revision_id, "source": source, "source_tag": source_tag,
        "section": section, "profile": profile, "relevant_terms": relevant_terms,
        "context_neighbors": [], "args_order": None, "target": target,
    }


def fixture_rows_v4() -> list[dict]:
    """Long-source fixture for the v4 enriched band (>=300 chars)."""
    rows = []
    for index in range(25):
        rows.append(_row(
            hashlib.sha256(f"v4-term-{index}".encode()).hexdigest(),
            f"Term name {index}", "term-name", "talent name", "talents",
            [{"category": "T.PN.RACE", "domain": "creatures", "source": f"Term name {index}",
              "status": "existing", "match": "full"}],
            f"术语{index}",
        ))
    for index in range(40):
        rows.append(_row(
            hashlib.sha256(f"v4-mech-{index}".encode()).hexdigest(),
            f"Mechanic description {index} with numbers {index} and conditions: " + "x" * 300,
            "mechanics", "tformat", "talents",
            [{"category": "T.GAME.DAMAGE", "domain": "combat", "source": f"Mechanic {index}",
              "status": "existing", "match": "full"}],
            f"机制{index}",
        ))
    for index in range(30):
        rows.append(_row(
            hashlib.sha256(f"v4-ent-{index}".encode()).hexdigest(),
            f"Entity dialogue line {index} about a long journey: " + "y" * 320,
            "dialogue", "logPlayer", "dialogs",
            [{"category": "T.PN.PLACE", "domain": "places", "source": f"Place {index}",
              "status": "existing", "match": "full"}],
            f"实体{index}",
        ))
    for index in range(10):
        rows.append(_row(
            hashlib.sha256(f"v4-ui-{index}".encode()).hexdigest(),
            f"UI label {index}", "ui", "_t", "ui", [], f"界面{index}",
        ))
    for index in range(25):
        rows.append(_row(
            hashlib.sha256(f"v4-gen-{index}".encode()).hexdigest(),
            f"General narrative {index} with a condition: " + "w" * 300,
            "narrative", "_t", "lore", [], f"普通{index}",
        ))
    return rows


def fixture_rows() -> list[dict]:
    rows = []
    for index in range(25):
        rows.append(_row(
            hashlib.sha256(f"term-{index}".encode()).hexdigest(),
            f"Term name {index}", "term-name", "talent name", "talents",
            [{"category": "T.PN.RACE", "domain": "creatures", "source": f"Term name {index}",
              "status": "existing", "match": "full"}],
            f"术语{index}",
        ))
    for index in range(25):
        rows.append(_row(
            hashlib.sha256(f"mech-{index}".encode()).hexdigest(),
            f"Mechanic {index}: " + "x" * 120, "mechanics", "tformat", "talents",
            [], f"机制{index}",
        ))
    for index in range(20):
        rows.append(_row(
            hashlib.sha256(f"ent-{index}".encode()).hexdigest(),
            f"Entity line {index}: " + "y" * 120, "dialogue", "logPlayer", "dialogs",
            [{"category": "T.PN.PLACE", "domain": "places", "source": f"Place {index}",
              "status": "existing", "match": "full"}],
            f"实体{index}",
        ))
    for index in range(2):
        rows.append(_row(
            hashlib.sha256(f"ui-long-{index}".encode()).hexdigest(),
            f"UI long {index}: " + "z" * 100, "ui", "_t", "ui", [], f"界面长{index}",
        ))
    for index in range(15):
        rows.append(_row(
            hashlib.sha256(f"ui-{index}".encode()).hexdigest(),
            f"UI label {index}", "ui", "_t", "ui", [], f"界面{index}",
        ))
    for index in range(20):
        rows.append(_row(
            hashlib.sha256(f"gen-{index}".encode()).hexdigest(),
            f"General {index}: " + "w" * 100, "narrative", "_t", "lore", [], f"普通{index}",
        ))
    return rows


def _write_inventory(root: Path, rows: list[dict]) -> Path:
    path = root / "inventory.jsonl"
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    return path


def _frozen_facts(pool: dict, facts: dict, actor: str = "facts-human") -> dict:
    facts = copy.deepcopy(facts)
    facts["status"] = "frozen"
    facts["authoring_lineage"]["actor_id"] = actor
    for index, item in enumerate(facts["items"]):
        if item["facts"]:
            continue
        item["facts"] = [{
            "fact_id": f"fact-{index:016x}",
            "fact_type": "mechanism",
            "statement": f"Verified supplemental fact {index}",
            "provenance": {
                "kind": "public-source",
                "resource": {
                    "repository": "tome4", "revision": "abc123",
                    "logical_path": "data/talents.lua",
                    "file_sha256": "2" * 64,
                },
                "locator": {"type": "line-range", "start_line": 1, "end_line": 2},
            },
        }]
    return facts


def _curator_assessment(pool: dict, *, fact_dependent_count: int = 8) -> dict:
    """Stratum-balanced classification covering all five strata in the final 20."""
    classifications: dict[int, str] = {}
    fact_traps: set[int] = set()
    # pool index -> stratum map: term 0-19, mech 20-39, ent 40-54, ui 55-69, gen 70-79
    fd = [0, 20, 40, 55, 70, 1, 21, 41][:fact_dependent_count]
    surface = [56, 71, 2, 22, 42, 57]
    clean = [72, 3, 23, 43, 58]
    acceptable = [73]
    for index in fd:
        classifications[index] = "fact-dependent-defect"
    for index in surface:
        classifications[index] = "surface-defect"
    for index in clean:
        classifications[index] = "clean"
    for index in acceptable:
        classifications[index] = "acceptable-localization"
    fact_traps = {72, 43, 58}
    items = []
    for index, item in enumerate(pool["items"]):
        classification = classifications.get(index, "unsuitable-uncertain")
        items.append({
            "revision_id": item["revision_id"],
            "classification": classification,
            "fact_trap": index in fact_traps,
            "notes": "",
        })
    curator = {
        "contract": CURATION_CURATOR_ASSESSMENT_CONTRACT, "schema_version": 1,
        "pool_id": pool["pool_id"], "curator_id": "curator-human", "status": "frozen",
        "lineage": {
            "facts_packet_sha256": "0" * 64, "curator_bundle_sha256": "0" * 64,
            "controlled_mutations_seen": False, "gold_seen": False,
        },
        "language_declaration": {
            "facts_statements_language": "english-metalanguage", "verified": True,
        },
        "items": items, "assessment_id": "",
    }
    curator["assessment_id"] = canonical_sha256(
        {key: value for key, value in curator.items() if key != "assessment_id"}
    )
    return curator


def _curator_assessment_v4(pool: dict, *, fd_count: int = 8) -> dict:
    """Stratum-balanced curator assessment for the v4 pool layout."""
    by_stratum: dict[str, list[int]] = {}
    for index, item in enumerate(pool["items"]):
        by_stratum.setdefault(item["stratum"], []).append(index)
    # quota coverage across all five strata; every index used exactly once
    term, mech, ent, ui, gen = (by_stratum[s] for s in (
        "term-proper-name", "mechanism-condition-number", "entity-relation",
        "ui-role", "general-semantic-clean-control",
    ))
    fd = [term[0], mech[0], ent[0], ui[0], gen[0], term[1], mech[1], ent[1],
          term[5], mech[5], ent[5], gen[5], mech[6]]
    fd = fd[:fd_count]
    surface = [ui[1], gen[1], mech[3], ent[3], term[3], ui[2]]
    clean = [term[4], mech[4], ent[4], ui[3], gen[3]]
    acceptable = [gen[4]]
    classifications: dict[int, str] = {}
    for index in fd:
        classifications[index] = "fact-dependent-defect"
    for index in surface:
        classifications[index] = "surface-defect"
    for index in clean:
        classifications[index] = "clean"
    for index in acceptable:
        classifications[index] = "acceptable-localization"
    fact_traps = set(clean[1:4])
    items = []
    for index, item in enumerate(pool["items"]):
        items.append({
            "revision_id": item["revision_id"],
            "classification": classifications.get(index, "unsuitable-uncertain"),
            "fact_trap": index in fact_traps,
            "notes": "",
        })
    return {
        "contract": CURATION_CURATOR_ASSESSMENT_CONTRACT, "schema_version": 1,
        "pool_id": pool["pool_id"], "curator_id": "curator-human-v4", "status": "frozen",
        "lineage": {
            "facts_packet_sha256": "0" * 64, "curator_bundle_sha256": "0" * 64,
            "controlled_mutations_seen": False, "gold_seen": False,
        },
        "language_declaration": {"facts_statements_language": "english-metalanguage", "verified": True},
        "items": items, "assessment_id": "",
    }


def _gold_items(result: dict, *, addressed: int = 8, unaddressed: int = 8) -> list[dict]:
    """Exhaustive gold items meeting the frozen minima (draft lineage)."""
    sample = result["sample"]
    facts = result["frozen_packet"]
    facts_by_id = {entry["revision_id"]: [fact["fact_id"] for fact in entry["facts"]] for entry in facts["items"]}
    gold_items = copy.deepcopy(result["gold"]["items"])
    by_revision = {item["revision_id"]: item for item in gold_items}
    addressed_left = addressed
    unaddressed_left = unaddressed
    extra_unaddressed_left = min(2, unaddressed)
    claim_serial = 0
    for sample_item in sample["items"]:
        classification = sample_item["selection_classification"]
        gold_item = by_revision[sample_item["revision_id"]]
        claims = []
        if classification == "fact-dependent-defect":
            fact_ids = facts_by_id[sample_item["revision_id"]]
            if addressed_left:
                claims.append({
                    "claim_id": f"claim-{claim_serial:03d}", "error_family": "semantic",
                    "phenomenon": "number", "meaning_change": "strengthened",
                    "source_evidence": {"quote": "", "occurrence": 0, "whole_item": True},
                    "target_evidence": {"quote": "", "occurrence": 0, "whole_item": True},
                    "fact_ids": fact_ids[:1] if fact_ids else [], "requires_manual": False,
                })
                claim_serial += 1
                addressed_left -= 1
            if extra_unaddressed_left and len(claims) == 1:
                claims.append({
                    "claim_id": f"claim-{claim_serial:03d}", "error_family": "ui",
                    "phenomenon": "ambiguity", "meaning_change": "made-ambiguous",
                    "source_evidence": {"quote": "", "occurrence": 0, "whole_item": True},
                    "target_evidence": {"quote": "", "occurrence": 0, "whole_item": True},
                    "fact_ids": [], "requires_manual": False,
                })
                claim_serial += 1
                extra_unaddressed_left -= 1
                unaddressed_left -= 1
        elif classification == "surface-defect":
            if unaddressed_left:
                claims.append({
                    "claim_id": f"claim-{claim_serial:03d}", "error_family": "terminology",
                    "phenomenon": "terminology", "meaning_change": "reassigned",
                    "source_evidence": {"quote": "", "occurrence": 0, "whole_item": True},
                    "target_evidence": {"quote": "", "occurrence": 0, "whole_item": True},
                    "fact_ids": [], "requires_manual": False,
                })
                claim_serial += 1
                unaddressed_left -= 1
        gold_item["claims"] = claims
    if addressed_left or unaddressed_left:
        raise AssertionError("fixture could not fill claim quotas")
    return gold_items


class CurationFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()
        cls.protocol = load_protocol(cls.manifest)

    def setUp(self):
        self.rows = fixture_rows()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inventory_path = _write_inventory(self.root, self.rows)
        from i18nlib.dataset_registry import excluded_revision_ids, load_registry
        required = excluded_revision_ids(load_registry(self.manifest))
        for lineage in json.loads(
            (ROOT / "i18n" / "quality" / "facts-study-exclusions-v1.json").read_text()
        )["lineages"]:
            required.update(lineage["revision_ids"])
        pool, author_bundle, facts, report = build_candidate_pool(
            inventory_path=self.inventory_path, exclusion_paths=[],
            seed="tome4-facts-study-curation-v1",
            required_excluded_ids=required,
        )
        self.pool = pool
        self.author_bundle = author_bundle
        self.facts = _frozen_facts(pool, facts)
        self.inventory = {row["revision_id"]: row for row in self.rows}

    def tearDown(self):
        self.temp.cleanup()

    def select(self, fact_dependent_count: int = 8, controlled: dict | None = None) -> dict:
        curator = _curator_assessment(self.pool, fact_dependent_count=fact_dependent_count)
        curator_bundle = build_curator_bundle(
            pool=self.pool, facts=self.facts, inventory=self.inventory
        )
        curator["lineage"] = {
            "facts_packet_sha256": canonical_sha256(self.facts),
            "curator_bundle_sha256": curator_bundle["curator_bundle_id"],
            "controlled_mutations_seen": False, "gold_seen": False,
        }
        curator["assessment_id"] = canonical_sha256(
            {key: value for key, value in curator.items() if key != "assessment_id"}
        )
        return select_final_sample(
            pool=self.pool, facts=self.facts, curator=curator,
            inventory=self.inventory, controlled_variants=controlled,
        )


class PoolBuildTests(CurationFixtureTests):
    def test_pool_has_80_items_with_frozen_stratum_counts(self):
        self.assertEqual(80, len(self.pool["items"]))
        self.assertEqual(
            self.pool["stratum_counts"],
            {"term-proper-name": 20, "mechanism-condition-number": 20,
             "entity-relation": 15, "ui-role": 15, "general-semantic-clean-control": 10},
        )
        validate_pool(self.pool)

    def test_selection_is_target_blind(self):
        blinded = copy.deepcopy(self.rows)
        for row in blinded:
            row["target"] = "替换后的目标文本 " + row["target"]
        path = _write_inventory(self.root, blinded)
        pool2, _, _, report2 = build_candidate_pool(
            inventory_path=path, exclusion_paths=[], seed="tome4-facts-study-curation-v1",
        )
        # the selection itself never reads the target: items are byte-identical;
        # only the inventory digest (and with it the pool_id) changes.
        self.assertEqual(self.pool["items"], pool2["items"])
        self.assertEqual(self.pool["stratum_counts"], pool2["stratum_counts"])
        self.assertNotEqual(self.pool["inventory_sha256"], pool2["inventory_sha256"])
        self.assertTrue(report2["target_blind"])

    def test_ui_stratum_relaxation_is_reported(self):
        report = build_candidate_pool(
            inventory_path=self.inventory_path, exclusion_paths=[],
            seed="tome4-facts-study-curation-v1",
        )[3]
        self.assertIn("ui-role", report["length_relaxations"])
        self.assertEqual(report["length_relaxations"]["ui-role"]["relaxed_short_filled"], 13)

    def test_exclusions_apply(self):
        from i18nlib.dataset_registry import excluded_revision_ids, load_registry
        historical = set()
        for lineage in json.loads(
            (ROOT / "i18n" / "quality" / "facts-study-exclusions-v1.json").read_text()
        )["lineages"]:
            historical.update(lineage["revision_ids"])
        required = excluded_revision_ids(load_registry(self.manifest)) | historical
        pool, _, _, _ = build_candidate_pool(
            inventory_path=self.inventory_path, exclusion_paths=[],
            seed="tome4-facts-study-curation-v1",
            required_excluded_ids=required,
        )
        self.assertTrue(required <= set(pool["excluded_revision_ids"]))

    def test_dedupe_by_public_input(self):
        duplicated = copy.deepcopy(self.rows)
        duplicated.append(copy.deepcopy(duplicated[0]))
        path = _write_inventory(self.root, duplicated)
        pool, _, _, _ = build_candidate_pool(
            inventory_path=path, exclusion_paths=[], seed="tome4-facts-study-curation-v1",
        )
        identities = [item["public_input_identity"] for item in pool["items"]]
        self.assertEqual(len(identities), len(set(identities)))

    def test_pool_validation_rejects_broken_band(self):
        bad = copy.deepcopy(self.pool)
        bad["items"][30]["source_length"] = 5  # mechanics item below 80 chars
        with self.assertRaises(ValidationError):
            validate_pool(bad)

    def test_pool_validation_rejects_non_canonical_id(self):
        bad = copy.deepcopy(self.pool)
        bad["pool_id"] = "1" * 64
        with self.assertRaises(ValidationError):
            validate_pool(bad)

    def test_author_bundle_is_target_blind(self):
        serialized = json.dumps(self.author_bundle, ensure_ascii=False)
        self.assertNotIn('"target"', serialized)
        self.assertNotIn("目标", serialized)
        self.assertEqual(CURATION_FACTS_AUTHOR_BUNDLE_CONTRACT, self.author_bundle["contract"])
        self.assertEqual("english-metalanguage", self.author_bundle["fact_policy"]["language"])

    def test_facts_packet_validates_and_binds_author_bundle(self):
        validate_packets(self.facts, pool=self.pool, expected_kind="facts")
        self.assertEqual(
            self.facts["authoring_lineage"]["source_inputs_sha256"],
            canonical_sha256(self.author_bundle),
        )


class CurationFlowTests(CurationFixtureTests):
    def test_natural_selection_meets_all_quotas(self):
        result = self.select()
        self.assertEqual("selected", result["status"])
        sample = result["sample"]
        self.assertEqual(20, len(sample["items"]))
        validate_sample(sample, pool=self.pool, required_excluded=set(self.pool["excluded_revision_ids"]))
        self.assertEqual(
            {item["stratum"] for item in sample["items"]}, set(STRATA)
        )
        origins = [item["origin"] for item in sample["items"]]
        self.assertTrue(all(origin == "natural" for origin in origins))
        report = result["selection_report"]
        self.assertEqual(8, report["selected_counts"]["fact-dependent-defect"])
        self.assertEqual(6, report["selected_counts"]["surface-defect"])
        self.assertEqual(5, report["selected_counts"]["clean"])
        self.assertEqual(1, report["selected_counts"]["acceptable-localization"])
        self.assertEqual(3, report["fact_traps"])

    def test_shortfall_returns_exit_code_2_with_request(self):
        result = self.select(fact_dependent_count=4)
        self.assertEqual("shortfall", result["status"])
        self.assertEqual(4, result["shortfall"]["fact_dependent_needed"])
        request = result["controlled_variant_request"]
        self.assertEqual("tome4-quality-controlled-variants-request-v1", request["contract"])
        self.assertEqual(4, len(request["items"]))

    def test_controlled_fill_completes_quota_and_hides_lineage(self):
        shortfall = self.select(fact_dependent_count=6)
        self.assertEqual("shortfall", shortfall["status"])
        request = shortfall["controlled_variant_request"]
        variants = []
        for request_item in request["items"][:2]:
            variant_target = "变体" + request_item["target"]
            variants.append({
                "revision_id": request_item["revision_id"],
                "variant_target": variant_target,
                "mutation_kind": "number-flip",
                "digest": canonical_sha256({
                    "contract": CONTROLLED_MUTATION_CONTRACT,
                    "base_revision_id": request_item["revision_id"],
                    "variant_target": variant_target,
                    "mutation_kind": "number-flip",
                }),
            })
        controlled = {
            "contract": CONTROLLED_VARIANTS_CONTRACT, "schema_version": 1,
            "pool_id": self.pool["pool_id"], "items": variants, "variants_id": "",
        }
        controlled["variants_id"] = canonical_sha256(
            {key: value for key, value in controlled.items() if key != "variants_id"}
        )
        result = self.select(fact_dependent_count=6, controlled=controlled)
        self.assertEqual("selected", result["status"])
        sample = result["sample"]
        controlled_items = [item for item in sample["items"] if item["origin"] == "controlled"]
        self.assertEqual(2, len(controlled_items))
        for item in controlled_items:
            self.assertEqual(item["revision_id"], item["mutation_lineage"]["digest"])
            self.assertEqual(item["target"], item["mutation_lineage"]["variant_target"])
            self.assertNotEqual(item["revision_id"], item["mutation_lineage"]["base_revision_id"])
        validate_sample(sample, pool=self.pool, required_excluded=set(self.pool["excluded_revision_ids"]))
        # natural/controlled counts are separable
        self.assertEqual(2, sum(item["origin"] == "controlled" for item in sample["items"]))
        self.assertEqual(18, sum(item["origin"] == "natural" for item in sample["items"]))

    def test_controlled_variant_structure_break_rejected(self):
        shortfall = self.select(fact_dependent_count=7)
        request = shortfall["controlled_variant_request"]
        request_item = request["items"][0]
        variants = [{
            "revision_id": request_item["revision_id"],
            "variant_target": "变体 %s 破坏格式",  # adds a printf token
            "mutation_kind": "number-flip",
            "digest": "0" * 64,
        }]
        controlled = {
            "contract": CONTROLLED_VARIANTS_CONTRACT, "schema_version": 1,
            "pool_id": self.pool["pool_id"], "items": variants, "variants_id": "",
        }
        controlled["variants_id"] = canonical_sha256(
            {key: value for key, value in controlled.items() if key != "variants_id"}
        )
        with self.assertRaises(ValidationError):
            self.select(fact_dependent_count=7, controlled=controlled)

    def test_controlled_variant_bad_digest_rejected(self):
        shortfall = self.select(fact_dependent_count=7)
        request = shortfall["controlled_variant_request"]
        request_item = request["items"][0]
        variants = [{
            "revision_id": request_item["revision_id"],
            "variant_target": "变体" + request_item["target"],
            "mutation_kind": "number-flip",
            "digest": "1" * 64,
        }]
        controlled = {
            "contract": CONTROLLED_VARIANTS_CONTRACT, "schema_version": 1,
            "pool_id": self.pool["pool_id"], "items": variants, "variants_id": "",
        }
        controlled["variants_id"] = canonical_sha256(
            {key: value for key, value in controlled.items() if key != "variants_id"}
        )
        with self.assertRaises(ValidationError):
            self.select(fact_dependent_count=7, controlled=controlled)

    def test_controlled_without_shortfall_rejected(self):
        result = self.select()
        self.assertEqual("selected", result["status"])
        # the same curator assessment has no shortfall, so controlled input is invalid
        with self.assertRaises(ValidationError):
            select_final_sample(
                pool=self.pool, facts=self.facts,
                curator=_curator_assessment(self.pool),
                inventory=self.inventory,
                controlled_variants={
                    "contract": CONTROLLED_VARIANTS_CONTRACT, "schema_version": 1,
                    "pool_id": self.pool["pool_id"], "items": [], "variants_id": "0" * 64,
                },
            )

    def test_controlled_fill_shortfall_revisions_must_match(self):
        shortfall = self.select(fact_dependent_count=6)
        request = shortfall["controlled_variant_request"]
        # fill only one of two needed revisions
        request_item = request["items"][0]
        variant_target = "变体" + request_item["target"]
        variants = [{
            "revision_id": request_item["revision_id"],
            "variant_target": variant_target,
            "mutation_kind": "number-flip",
            "digest": canonical_sha256({
                "contract": CONTROLLED_MUTATION_CONTRACT,
                "base_revision_id": request_item["revision_id"],
                "variant_target": variant_target,
                "mutation_kind": "number-flip",
            }),
        }]
        controlled = {
            "contract": CONTROLLED_VARIANTS_CONTRACT, "schema_version": 1,
            "pool_id": self.pool["pool_id"], "items": variants, "variants_id": "",
        }
        controlled["variants_id"] = canonical_sha256(
            {key: value for key, value in controlled.items() if key != "variants_id"}
        )
        with self.assertRaises(ValidationError):
            self.select(fact_dependent_count=6, controlled=controlled)

    def test_evaluator_bundle_hides_origin_mutation_and_gold(self):
        result = self.select()
        sample = result["sample"]
        from i18nlib.facts_curation import build_bundle
        neutral = build_neutral_packets(result["frozen_packet"], pool_id=self.pool["pool_id"])
        prompts = {arm: load_arm_prompt(self.manifest, arm) for arm in
                   ("A", "B", "C", "D", "N", "L", "F")}
        bundle = build_bundle(
            sample=sample, facts=result["frozen_packet"], neutral=neutral, arm="C",
            prompt_sha256=hashlib.sha256(prompts["C"].encode()).hexdigest(),
        )
        serialized = json.dumps(bundle, ensure_ascii=False)
        for forbidden in ("origin", "mutation_lineage", "selection_classification", "gold", "curator"):
            self.assertNotIn(forbidden, serialized)
        for item in bundle["items"]:
            self.assertNotIn("origin", item)
            self.assertNotIn("mutation_lineage", item)
        # authoring bundle and curator bundle stay separate
        curator_bundle = build_curator_bundle(pool=self.pool, facts=self.facts, inventory=self.inventory)
        self.assertNotIn("gold", json.dumps(curator_bundle, ensure_ascii=False))
        self.assertNotIn('"target"', json.dumps(self.author_bundle, ensure_ascii=False))


def gold_fixture(result: dict, *, addressed: int = 8, unaddressed: int = 8) -> dict:
    sample = result["sample"]
    items = _gold_items(result, addressed=addressed, unaddressed=unaddressed)
    return {
        "contract": CURATION_GOLD_CONTRACT, "schema_version": 1,
        "study_id": sample["study_id"], "status": "draft",
        "review_lineage": {
            "reviewer_ids": ["", ""], "review_artifact_sha256s": ["", ""],
            "adjudicator_id": "", "adjudication_artifact_sha256": "",
        },
        "items": items,
    }


class GoldValidationTests(CurationFixtureTests):
    def _freeze(self, result: dict, gold: dict) -> dict:
        sample = result["sample"]
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            review_paths = []
            for index, reviewer_id in enumerate(("gold-a", "gold-b")):
                path = root / f"review-{index}.json"
                write_json(path, {
                    "contract": CURATION_GOLD_REVIEW_CONTRACT, "schema_version": 1,
                    "study_id": sample["study_id"], "reviewer_id": reviewer_id,
                    "independent": True, "items": gold["items"],
                })
                review_paths.append(path)
            hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in review_paths]
            adjudication_path = root / "adjudication.json"
            write_json(adjudication_path, {
                "contract": CURATION_GOLD_ADJUDICATION_CONTRACT, "schema_version": 1,
                "study_id": sample["study_id"], "status": "frozen",
                "adjudicator_id": "gold-c", "review_artifact_sha256s": hashes,
                "items": gold["items"],
            })
            gold["status"] = "frozen"
            gold["review_lineage"] = {
                "reviewer_ids": ["gold-a", "gold-b"],
                "review_artifact_sha256s": hashes,
                "adjudicator_id": "gold-c",
                "adjudication_artifact_sha256": hashlib.sha256(adjudication_path.read_bytes()).hexdigest(),
            }
            validate_gold(gold, sample=sample, facts=result["frozen_packet"])
            validate_gold_authoring_artifacts(
                review_paths=review_paths, adjudication_path=adjudication_path,
                gold=gold, sample=sample, facts=result["frozen_packet"],
            )
            return gold, review_paths, adjudication_path

    def test_frozen_gold_meets_all_minima(self):
        result = self.select()
        gold = gold_fixture(result)
        self._freeze(result, gold)

    def test_addressed_claim_quota_insufficient_fails(self):
        result = self.select()
        gold = gold_fixture(result, addressed=5)
        sample = result["sample"]
        gold["status"] = "frozen"
        gold["review_lineage"] = {
            "reviewer_ids": ["a", "b"], "review_artifact_sha256s": ["1" * 64, "2" * 64],
            "adjudicator_id": "c", "adjudication_artifact_sha256": "3" * 64,
        }
        with self.assertRaises(ValidationError):
            validate_gold(gold, sample=sample, facts=result["frozen_packet"])

    def test_wrong_fact_reference_fails(self):
        result = self.select()
        gold = gold_fixture(result)
        claim = next(
            claim for item in gold["items"] for claim in item["claims"] if claim["fact_ids"]
        )
        claim["fact_ids"] = ["fact-0000000000000000"]
        gold["status"] = "frozen"
        gold["review_lineage"] = {
            "reviewer_ids": ["a", "b"], "review_artifact_sha256s": ["1" * 64, "2" * 64],
            "adjudicator_id": "c", "adjudication_artifact_sha256": "3" * 64,
        }
        with self.assertRaises(ValidationError):
            validate_gold(gold, sample=result["sample"], facts=result["frozen_packet"])

    def test_role_identity_conflicts_fail(self):
        result = self.select()
        gold = gold_fixture(result)
        gold["status"] = "frozen"
        gold["review_lineage"] = {
            "reviewer_ids": ["same", "same"],
            "review_artifact_sha256s": ["1" * 64, "2" * 64],
            "adjudicator_id": "c", "adjudication_artifact_sha256": "3" * 64,
        }
        with self.assertRaises(ValidationError):
            validate_gold(gold, sample=result["sample"], facts=result["frozen_packet"])
        gold["review_lineage"]["reviewer_ids"] = ["a", "b"]
        gold["review_lineage"]["adjudicator_id"] = "a"
        with self.assertRaises(ValidationError):
            validate_gold(gold, sample=result["sample"], facts=result["frozen_packet"])
        gold["review_lineage"]["adjudicator_id"] = "c"

    def test_adjudication_mismatch_fails(self):
        result = self.select()
        gold = gold_fixture(result)
        sample = result["sample"]
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            review_paths = []
            for index, reviewer_id in enumerate(("gold-a", "gold-b")):
                path = root / f"review-{index}.json"
                write_json(path, {
                    "contract": CURATION_GOLD_REVIEW_CONTRACT, "schema_version": 1,
                    "study_id": sample["study_id"], "reviewer_id": reviewer_id,
                    "independent": True, "items": gold["items"],
                })
                review_paths.append(path)
            hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in review_paths]
            adjudication_path = root / "adjudication.json"
            tampered = copy.deepcopy(gold["items"])
            tampered[0]["clean"] = not tampered[0]["clean"]
            write_json(adjudication_path, {
                "contract": CURATION_GOLD_ADJUDICATION_CONTRACT, "schema_version": 1,
                "study_id": sample["study_id"], "status": "frozen",
                "adjudicator_id": "gold-c", "review_artifact_sha256s": hashes,
                "items": tampered,
            })
            gold["status"] = "frozen"
            gold["review_lineage"] = {
                "reviewer_ids": ["gold-a", "gold-b"],
                "review_artifact_sha256s": hashes,
                "adjudicator_id": "gold-c",
                "adjudication_artifact_sha256": hashlib.sha256(adjudication_path.read_bytes()).hexdigest(),
            }
            with self.assertRaises(ValidationError):
                validate_gold_authoring_artifacts(
                    review_paths=review_paths, adjudication_path=adjudication_path,
                    gold=gold, sample=sample, facts=result["frozen_packet"],
                )

    def test_facts_author_must_not_be_reviewer(self):
        result = self.select()
        gold = gold_fixture(result)
        sample = result["sample"]
        gold["status"] = "frozen"
        gold["review_lineage"] = {
            "reviewer_ids": ["facts-human", "b"],
            "review_artifact_sha256s": ["1" * 64, "2" * 64],
            "adjudicator_id": "c", "adjudication_artifact_sha256": "3" * 64,
        }
        with self.assertRaises(ValidationError):
            validate_gold(gold, sample=sample, facts=result["frozen_packet"])


class V4EnrichedPoolTests(unittest.TestCase):
    """v4 protocol: long-source enriched source-side pool."""

    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()
        cls.protocol = load_protocol(cls.manifest, version="v4")

    def setUp(self):
        self.rows = fixture_rows_v4()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inventory_path = _write_inventory(self.root, self.rows)

    def tearDown(self):
        self.temp.cleanup()

    def build(self, **kwargs):
        return build_candidate_pool(
            inventory_path=self.inventory_path, exclusion_paths=[],
            seed="tome4-facts-study-curation-enriched-v1", protocol=self.protocol,
            **kwargs,
        )

    def test_v4_stratum_targets_and_length_band(self):
        pool, author, facts, report = self.build()
        self.assertEqual(80, len(pool["items"]))
        self.assertEqual(
            pool["stratum_counts"],
            {"term-proper-name": 6, "mechanism-condition-number": 30,
             "entity-relation": 25, "ui-role": 4, "general-semantic-clean-control": 15},
        )
        self.assertIsNone(report.get("protocol_version"))  # set by run_curation_build
        # non-exempt strata must be >= 300 chars
        for item in pool["items"]:
            if item["stratum"] in ("mechanism-condition-number", "entity-relation", "general-semantic-clean-control"):
                self.assertGreaterEqual(item["source_length"], 300)
        validate_pool(pool)

    def test_v4_prefers_long_sources(self):
        pool, _, _, _ = self.build()
        mech = [item for item in pool["items"] if item["stratum"] == "mechanism-condition-number"]
        lengths = sorted((item["source_length"] for item in mech), reverse=True)
        # the 30 picked items must be the 30 longest candidates available
        all_mech = sorted(
            (len(r["source"]) for r in self.rows if r["source"].startswith("Mechanic description")),
            reverse=True,
        )
        self.assertEqual(lengths, all_mech[:30])

    def test_v4_target_blind(self):
        blinded = copy.deepcopy(self.rows)
        for row in blinded:
            row["target"] = "替换 " + row["target"]
        path = _write_inventory(self.root, blinded)
        pool1, _, _, _ = self.build()
        pool2, _, _, report2 = build_candidate_pool(
            inventory_path=path, exclusion_paths=[],
            seed="tome4-facts-study-curation-enriched-v1", protocol=self.protocol,
        )
        self.assertEqual(pool1["items"], pool2["items"])
        self.assertTrue(report2["target_blind"])

    def test_v4_risk_bonus_affects_ranking(self):
        # sources with number/condition risk flags rank above same-length peers
        rows = copy.deepcopy(self.rows)
        # strip the numbers/conditions from one fixture row to make a control
        pool, _, _, _ = self.build()
        self.assertTrue(pool["selection_inputs"]["prefer_long_source"])
        self.assertIn("source-has-number-or-unit", pool["selection_inputs"]["risk_bonus"])

    def test_v4_pool_validation_rejects_band_violation(self):
        pool, _, _, _ = self.build()
        bad = copy.deepcopy(pool)
        # a mechanics item below the 300 minimum
        bad["items"][20]["source_length"] = 150
        with self.assertRaises(ValidationError):
            validate_pool(bad)

    def test_v4_select_quota_flow_on_enriched_pool(self):
        pool, author, facts, report = self.build()
        facts = _frozen_facts(pool, facts)
        inventory = {row["revision_id"]: row for row in self.rows}
        # enriched pools make defect candidates plentiful: use the standard
        # curator fixture (stratum-balanced classifications still apply)
        curator = _curator_assessment_v4(pool)
        curator_bundle = build_curator_bundle(pool=pool, facts=facts, inventory=inventory)
        curator["lineage"] = {
            "facts_packet_sha256": canonical_sha256(facts),
            "curator_bundle_sha256": curator_bundle["curator_bundle_id"],
            "controlled_mutations_seen": False, "gold_seen": False,
        }
        curator["assessment_id"] = canonical_sha256(
            {key: value for key, value in curator.items() if key != "assessment_id"}
        )
        result = select_final_sample(
            pool=pool, facts=facts, curator=curator,
            inventory=inventory, controlled_variants=None,
        )
        self.assertEqual("selected", result["status"])
        validate_sample(result["sample"], pool=pool, required_excluded=set(pool["excluded_revision_ids"]))
        self.assertEqual(
            {item["stratum"] for item in result["sample"]["items"]}, set(STRATA)
        )


class V5QuotaSelectionTests(V4EnrichedPoolTests):
    """v5 corpus-aligned quotas: 12 fd + 2 surface + 6 clean/acceptable."""

    def test_v5_quota_selection_on_enriched_pool(self):
        pool, author, facts, report = self.build()
        facts = _frozen_facts(pool, facts)
        inventory = {row["revision_id"]: row for row in self.rows}
        curator = _curator_assessment_v4(pool, fd_count=13)
        curator_bundle = build_curator_bundle(pool=pool, facts=facts, inventory=inventory)
        curator["lineage"] = {
            "facts_packet_sha256": canonical_sha256(facts),
            "curator_bundle_sha256": curator_bundle["curator_bundle_id"],
            "controlled_mutations_seen": False, "gold_seen": False,
        }
        curator["assessment_id"] = canonical_sha256(
            {key: value for key, value in curator.items() if key != "assessment_id"}
        )
        quota = {
            "fact_dependent": 12, "surface": 2, "clean_acceptable": 6,
            "clean_min": 5, "fact_traps_min": 3,
            "addressed_claims_min": 8, "unaddressed_claims_min": 8,
        }
        result = select_final_sample(
            pool=pool, facts=facts, curator=curator, inventory=inventory,
            quota=quota, seed="tome4-facts-study-curation-v5-select-v1",
        )
        self.assertEqual("selected", result["status"])
        sample = result["sample"]
        validate_sample(sample, pool=pool, required_excluded=set(pool["excluded_revision_ids"]))
        self.assertEqual(20, len(sample["items"]))
        report = result["selection_report"]
        self.assertEqual(12, report["selected_counts"]["fact-dependent-defect"])
        self.assertEqual(2, report["selected_counts"]["surface-defect"])
        self.assertEqual(0, report["selected_counts"]["controlled"])
        self.assertEqual(5, report["selected_counts"]["clean"])
        self.assertEqual(
            {item["stratum"] for item in sample["items"]}, set(STRATA)
        )

    def test_v5_quota_rejects_insufficient_surface(self):
        pool, author, facts, report = self.build()
        facts = _frozen_facts(pool, facts)
        inventory = {row["revision_id"]: row for row in self.rows}
        curator = _curator_assessment_v4(pool, fd_count=13)
        # keep only one surface item (quota needs 2)
        count = 0
        for entry in curator["items"]:
            if entry["classification"] == "surface-defect" and count < 5:
                entry["classification"] = "clean"
                count += 1
        curator_bundle = build_curator_bundle(pool=pool, facts=facts, inventory=inventory)
        curator["lineage"] = {
            "facts_packet_sha256": canonical_sha256(facts),
            "curator_bundle_sha256": curator_bundle["curator_bundle_id"],
            "controlled_mutations_seen": False, "gold_seen": False,
        }
        curator["assessment_id"] = canonical_sha256(
            {key: value for key, value in curator.items() if key != "assessment_id"}
        )
        quota = {
            "fact_dependent": 12, "surface": 2, "clean_acceptable": 6,
            "clean_min": 5, "fact_traps_min": 3,
            "addressed_claims_min": 8, "unaddressed_claims_min": 8,
        }
        with self.assertRaises(ValidationError):
            select_final_sample(
                pool=pool, facts=facts, curator=curator, inventory=inventory,
                quota=quota, seed="tome4-facts-study-curation-v5-select-v1",
            )


class IntegrationTests(CurationFixtureTests):
    def _run_directory(self, root: Path):
        counter = {"n": 0}

        def factory(_repo, kind):
            counter["n"] += 1
            path = root / f"run-{counter['n']}-{kind}"
            path.mkdir()
            return path

        return factory

    def test_full_chain_80_to_fake_replay(self):
        result = self.select()
        sample = result["sample"]
        frozen_packet = result["frozen_packet"]
        gold = gold_fixture(result)
        neutral = build_neutral_packets(frozen_packet, pool_id=self.pool["pool_id"])
        validate_neutral_equivalence = __import__(
            "i18nlib.facts_curation", fromlist=["validate_neutral_equivalence"]
        ).validate_neutral_equivalence
        validate_neutral_equivalence(frozen_packet, neutral)
        prompts = {arm: load_arm_prompt(self.manifest, arm) for arm in
                   ("A", "B", "C", "D", "N", "L", "F")}
        from i18nlib.facts_curation import build_bundle
        bundles = {
            arm: build_bundle(
                sample=sample, facts=frozen_packet, neutral=neutral, arm=arm,
                prompt_sha256=hashlib.sha256(prompts[arm].encode()).hexdigest(),
            ) for arm in ("A", "B", "C", "D", "N", "L", "F")
        }
        schedule = build_schedule(self.protocol, bundles, prompts)
        self.assertEqual(33, len(schedule))

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            # freeze gold with real review/adjudication files
            review_paths = []
            for index, reviewer_id in enumerate(("gold-a", "gold-b")):
                path = root / f"review-{index}.json"
                write_json(path, {
                    "contract": CURATION_GOLD_REVIEW_CONTRACT, "schema_version": 1,
                    "study_id": sample["study_id"], "reviewer_id": reviewer_id,
                    "independent": True, "items": gold["items"],
                })
                review_paths.append(path)
            hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in review_paths]
            adjudication_path = root / "adjudication.json"
            write_json(adjudication_path, {
                "contract": CURATION_GOLD_ADJUDICATION_CONTRACT, "schema_version": 1,
                "study_id": sample["study_id"], "status": "frozen",
                "adjudicator_id": "gold-c", "review_artifact_sha256s": hashes,
                "items": gold["items"],
            })
            gold["status"] = "frozen"
            gold["review_lineage"] = {
                "reviewer_ids": ["gold-a", "gold-b"],
                "review_artifact_sha256s": hashes,
                "adjudicator_id": "gold-c",
                "adjudication_artifact_sha256": hashlib.sha256(adjudication_path.read_bytes()).hexdigest(),
            }
            paths = {}
            for name, value in (("pool", self.pool), ("sample", sample),
                                ("facts_pool", self.facts), ("facts", frozen_packet),
                                ("gold", gold)):
                paths[name] = root / f"{name}.json"
                write_json(paths[name], value)
            bundle_paths = []
            for arm, bundle in bundles.items():
                path = root / f"bundle-{arm.lower()}.json"
                write_json(path, bundle)
                bundle_paths.append(path)
            factory = self._run_directory(root)
            with patch(
                "i18nlib.facts_curation.create_quality_run_directory",
                side_effect=factory,
            ):
                bundled = run_curation_bundles(
                    self.manifest, pool_path=paths["pool"], sample_path=paths["sample"],
                    facts_pool_path=paths["facts_pool"], facts_path=paths["facts"],
                    gold_path=paths["gold"], gold_review_paths=review_paths,
                    gold_adjudication_path=adjudication_path,
                )
                self.assertEqual(33, bundled["slots"])
                prereg = json.loads(Path(bundled["preregistration"]).read_text())
                self.assertEqual(CURATION_PREREG_CONTRACT, prereg["contract"])
                self.assertEqual("offline-frozen", prereg["status"])
                neutral_path = Path(bundled["neutral"])
                with patch(
                    "i18nlib.facts_curation.create_quality_run_directory",
                    side_effect=factory,
                ):
                    validation = run_curation_validate(
                        self.manifest, pool_path=paths["pool"],
                        sample_path=paths["sample"], facts_pool_path=paths["facts_pool"],
                        facts_path=paths["facts"], neutral_path=neutral_path,
                        gold_path=paths["gold"], prereg_path=Path(bundled["preregistration"]),
                        bundle_paths=[Path(b) for b in bundled["bundles"].values()],
                        fake_runner=True, assessment_paths=[], runner_report_paths=[],
                    )
                    self.assertEqual("offline-fake-replay", validation["mode"])
                    report = run_curation_report(
                        self.manifest, validation_path=Path(validation["validation"])
                    )
                self.assertEqual(CURATION_ASSESSMENT_CONTRACT, "tome4-quality-facts-study-assessment-v2")
                self.assertEqual("non-evidentiary-offline-replay", report["decision"]["result"])
                self.assertFalse(report["holdout_clearance"])
                self.assertFalse(report["external_evidence"])
                self.assertEqual(33, len(report["run_metrics"]))
                self.assertIn("natural_pooled_metrics", report)
                self.assertIn("controlled_pooled_metrics", report)
                self.assertEqual(
                    "tome4-quality-facts-study-report-v2", report["contract"]
                )

    def test_run_curation_select_writes_valid_fragments_and_shortfall(self):
        from i18nlib.dataset_registry import validate_registry_fragment
        from i18nlib.facts_curation import run_curation_prepare, run_curation_select
        from i18nlib.report import write_json
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            pool_path = root / "pool.json"
            facts_path = root / "facts.json"
            write_json(pool_path, self.pool)
            write_json(facts_path, self.facts)
            factory = self._run_directory(root)
            with patch("i18nlib.facts_curation.create_quality_run_directory", side_effect=factory):
                prepared = run_curation_prepare(
                    self.manifest, pool_path=pool_path, facts_path=facts_path,
                    inventory_path=self.inventory_path,
                )
                with open(prepared["curator_bundle"], encoding="utf-8") as handle:
                    curator_bundle = json.load(handle)
                curator = _curator_assessment(self.pool)
                curator["lineage"] = {
                    "facts_packet_sha256": canonical_sha256(self.facts),
                    "curator_bundle_sha256": curator_bundle["curator_bundle_id"],
                    "controlled_mutations_seen": False, "gold_seen": False,
                }
                curator["assessment_id"] = canonical_sha256(
                    {k: v for k, v in curator.items() if k != "assessment_id"}
                )
                curator_path = root / "curator.json"
                write_json(curator_path, curator)
                selected = run_curation_select(
                    self.manifest, pool_path=pool_path, facts_path=facts_path,
                    curator_path=curator_path, inventory_path=self.inventory_path,
                    protocol_version="v3",
                )
                self.assertEqual(0, selected["status_code"])
                for path in selected["registry_fragments"]:
                    with open(path, encoding="utf-8") as handle:
                        validate_registry_fragment(json.load(handle))
                # shortfall path returns exit code 2 with a variant request
                short_curator = _curator_assessment(self.pool, fact_dependent_count=4)
                short_curator["lineage"] = {
                    "facts_packet_sha256": canonical_sha256(self.facts),
                    "curator_bundle_sha256": curator_bundle["curator_bundle_id"],
                    "controlled_mutations_seen": False, "gold_seen": False,
                }
                short_curator["assessment_id"] = canonical_sha256(
                    {k: v for k, v in short_curator.items() if k != "assessment_id"}
                )
                short_path = root / "short-curator.json"
                write_json(short_path, short_curator)
                with patch("i18nlib.facts_curation.create_quality_run_directory", side_effect=factory):
                    short = run_curation_select(
                        self.manifest, pool_path=pool_path, facts_path=facts_path,
                        curator_path=short_path, inventory_path=self.inventory_path,
                        protocol_version="v3",
                    )
                self.assertEqual(2, short["status_code"])
                with open(
                    short["controlled_variant_request"], encoding="utf-8"
                ) as handle:
                    request = json.load(handle)
                self.assertEqual(4, len(request["items"]))

    def test_execution_manifest_binds_frozen_prereg(self):
        from i18nlib.facts_study import (
            build_execution_manifest, validate_execution_manifest,
        )
        result = self.select()
        sample = result["sample"]
        frozen_packet = result["frozen_packet"]
        gold = gold_fixture(result)
        neutral = build_neutral_packets(frozen_packet, pool_id=self.pool["pool_id"])
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            review_paths = []
            for index, reviewer_id in enumerate(("gold-a", "gold-b")):
                path = root / f"review-{index}.json"
                write_json(path, {
                    "contract": CURATION_GOLD_REVIEW_CONTRACT, "schema_version": 1,
                    "study_id": sample["study_id"], "reviewer_id": reviewer_id,
                    "independent": True, "items": gold["items"],
                })
                review_paths.append(path)
            hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in review_paths]
            adjudication_path = root / "adjudication.json"
            write_json(adjudication_path, {
                "contract": CURATION_GOLD_ADJUDICATION_CONTRACT, "schema_version": 1,
                "study_id": sample["study_id"], "status": "frozen",
                "adjudicator_id": "gold-c", "review_artifact_sha256s": hashes,
                "items": gold["items"],
            })
            gold["status"] = "frozen"
            gold["review_lineage"] = {
                "reviewer_ids": ["gold-a", "gold-b"],
                "review_artifact_sha256s": hashes,
                "adjudicator_id": "gold-c",
                "adjudication_artifact_sha256": hashlib.sha256(adjudication_path.read_bytes()).hexdigest(),
            }
            prompts = {arm: load_arm_prompt(self.manifest, arm) for arm in
                       ("A", "B", "C", "D", "N", "L", "F")}
            from i18nlib.facts_curation import build_bundle, build_preregistration
            from i18nlib.facts_study import study_harness_sha256
            bundles = {
                arm: build_bundle(
                    sample=sample, facts=frozen_packet, neutral=neutral, arm=arm,
                    prompt_sha256=hashlib.sha256(prompts[arm].encode()).hexdigest(),
                ) for arm in ("A", "B", "C", "D", "N", "L", "F")
            }
            prereg = build_preregistration(
                protocol=self.protocol, sample=sample, facts=frozen_packet,
                neutral=neutral, gold=gold, bundles=bundles, prompts=prompts,
                harness_sha256=study_harness_sha256(),
            )
            manifest = build_execution_manifest(
                preregistration=prereg, authorization_id="user-auth-test",
                granted_at="2026-08-07T00:00:00Z",
            )
            self.assertEqual(
                "tome4-quality-facts-study-execution-manifest-v1", manifest["contract"]
            )
            self.assertEqual(33, len(manifest["schedule"]))
            validate_execution_manifest(manifest, preregistration=prereg)
            # tampering with the prereg breaks the binding
            tampered = copy.deepcopy(prereg)
            tampered["schedule"][0]["seed"] = "forged"
            with self.assertRaises(ValidationError):
                validate_execution_manifest(manifest, preregistration=tampered)

    def test_offline_frozen_preregistration_rejected_by_external_runner(self):
        from i18nlib.pi_facts_study import run_slot
        result = self.select()
        sample = result["sample"]
        frozen_packet = result["frozen_packet"]
        gold = gold_fixture(result)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            prereg = {
                "contract": CURATION_PREREG_CONTRACT, "schema_version": 1,
                "study_id": sample["study_id"], "pool_id": self.pool["pool_id"],
                "purpose": "facts-causal-study-only-no-holdout-clearance",
                "status": "offline-frozen", "preregistration_id": "0" * 64,
            }
            prereg_path = root / "prereg.json"
            write_json(prereg_path, prereg)
            with self.assertRaises(ValidationError) as caught:
                run_slot(
                    sample_path=root / "sample.json", facts_path=root / "facts.json",
                    neutral_path=root / "neutral.json", gold_path=root / "gold.json",
                    preregistration_path=prereg_path, bundle_paths=[],
                    slot_id="luna-a-1", authorization_id="auth",
                )
            self.assertIn("offline-frozen", str(caught.exception))

    def test_external_assessments_rejected_for_offline_frozen(self):
        result = self.select()
        with self.assertRaises(ValidationError):
            run_curation_validate(
                self.manifest, pool_path=Path("/nonexistent"), sample_path=Path("/nonexistent"),
                facts_pool_path=Path("/nonexistent"), facts_path=Path("/nonexistent"),
                neutral_path=Path("/nonexistent"), gold_path=Path("/nonexistent"),
                prereg_path=Path("/nonexistent"), bundle_paths=[],
                fake_runner=False, assessment_paths=[], runner_report_paths=[],
            )


if __name__ == "__main__":
    unittest.main()
