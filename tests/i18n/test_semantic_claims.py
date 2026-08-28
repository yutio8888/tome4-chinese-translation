from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
REGISTRY = ROOT / "evidence" / "quality" / "semantic-claim-regressions-v1.json"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.cli import main as cli_main
from i18nlib.errors import ValidationError
from i18nlib.semantic_claims import check_registry, validate_registry


class SemanticClaimRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def assert_invalid(self, value: dict, message: str | None = None) -> None:
        with self.assertRaises(ValidationError) as caught:
            validate_registry(value)
        if message is not None:
            self.assertIn(message, str(caught.exception))

    def assert_valid(self, value: dict) -> None:
        validate_registry(value)

    def test_normative_registry_passes(self):
        report = check_registry(REGISTRY, strict=True)
        self.assertEqual(report["numeric_claims"], 1)
        self.assertEqual(report["reviewer_briefings"], 1)
        self.assertEqual(report["runtime_compositions"], 1)
        self.assertEqual(report["pending"], 1)

    def test_cli_entry_passes(self):
        self.assertEqual(
            cli_main(["claims", "check", "--registry", str(REGISTRY), "--strict"]),
            0,
        )

    def test_default_registry_is_independent_of_current_directory(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                self.assertEqual(cli_main(["claims", "check", "--strict"]), 0)
            finally:
                os.chdir(previous)

    def test_schema_version_rejects_non_integer_values(self):
        for version in (True, 1.0, "1"):
            with self.subTest(version=version):
                value = copy.deepcopy(self.registry)
                value["schema_version"] = version
                self.assert_invalid(value, "expected integer")

    def test_extra_key_rejected(self):
        value = copy.deepcopy(self.registry)
        value["numeric_claims"][0]["runtime_formula"] = "0.5 + 0.5"
        self.assert_invalid(value, "extra=['runtime_formula']")

    def test_duplicate_id_rejected_across_record_types(self):
        value = copy.deepcopy(self.registry)
        value["reviewer_briefings"][0]["briefing_id"] = value["numeric_claims"][0]["claim_id"]
        self.assert_invalid(value, "duplicate ID")

    def test_unsafe_and_absolute_paths_rejected(self):
        for path in (
            "../damage_types.lua",
            "/tmp/damage_types.lua",
            "game\\damage_types.lua",
            json.loads('"game\\u0000damage_types.lua"'),
        ):
            with self.subTest(path=path):
                value = copy.deepcopy(self.registry)
                value["numeric_claims"][0]["anchors"][0]["path"] = path
                self.assert_invalid(value, "path")

    def test_unpinned_confirmed_claim_rejected(self):
        value = copy.deepcopy(self.registry)
        value["numeric_claims"][0]["anchors"][0]["source_pinned"] = False
        self.assert_invalid(value, "unpinned required anchor")

    def test_missing_placeholder_binding_rejected(self):
        value = copy.deepcopy(self.registry)
        del value["numeric_claims"][0]["anchors"][0]["placeholder_expression"]
        self.assert_invalid(value, "placeholder_expression")

    def test_missing_revision_and_symbol_rejected(self):
        for field in ("revision", "symbol"):
            with self.subTest(field=field):
                value = copy.deepcopy(self.registry)
                value["numeric_claims"][0]["anchors"][0][field] = ""
                self.assert_invalid(value, field)

    def test_unknown_enum_rejected(self):
        value = copy.deepcopy(self.registry)
        value["numeric_claims"][0]["scope"] = "per_round"
        self.assert_invalid(value, "unknown enum")

    def test_wrong_type_rejected(self):
        value = copy.deepcopy(self.registry)
        value["numeric_claims"][0]["placeholder_index"] = True
        self.assert_invalid(value, "expected integer")

    def test_complete_raw_format_tokens_must_match(self):
        value = copy.deepcopy(self.registry)
        value["numeric_claims"][0]["target_text"] = value["numeric_claims"][0][
            "target_text"
        ].replace("%0.2f", "%f")
        self.assert_invalid(value, "format tokens do not match args_order")

    def test_numeric_claim_args_order_supports_reordered_damage_tokens(self):
        value = copy.deepcopy(self.registry)
        claim = value["numeric_claims"][0]
        claim["source_text"] = "Deals %0.2f damage over %d turns."
        claim["target_text"] = "%d 回合内造成 %0.2f 伤害。"
        claim["placeholder_index"] = 1
        claim["placeholder_token"] = "%0.2f"
        claim["args_order"] = [2, 1]
        claim["target_assertions"] = {
            "required": ["%d 回合内造成 %0.2f 伤害"],
            "forbidden": ["每回合造成 %0.2f 伤害"],
        }
        self.assert_valid(value)

        claim["args_order"] = None
        self.assert_invalid(value, "format tokens do not match args_order")

        claim["args_order"] = [1, 1]
        self.assert_invalid(value, "must be a permutation")

    def test_numeric_claim_and_briefing_require_args_order_field(self):
        for collection in ("numeric_claims", "reviewer_briefings"):
            with self.subTest(collection=collection):
                value = copy.deepcopy(self.registry)
                del value[collection][0]["args_order"]
                self.assert_invalid(value, "args_order")

    def test_canonical_tokenizer_handles_escaped_percent_and_lua_q(self):
        escaped = copy.deepcopy(self.registry)
        claim = escaped["numeric_claims"][0]
        claim["source_text"] = "100%% ready: " + claim["source_text"]
        claim["target_text"] = "100%% 就绪：" + claim["target_text"]
        self.assert_valid(escaped)

        lua_q = copy.deepcopy(self.registry)
        claim = lua_q["numeric_claims"][0]
        for field in ("source_text", "target_text", "placeholder_token"):
            claim[field] = claim[field].replace("%0.2f", "%q")
        for field in ("required", "forbidden"):
            claim["target_assertions"][field] = [
                fragment.replace("%0.2f", "%q")
                for fragment in claim["target_assertions"][field]
            ]
        self.assert_valid(lua_q)

        python_r = copy.deepcopy(lua_q)
        claim = python_r["numeric_claims"][0]
        for field in ("source_text", "target_text", "placeholder_token"):
            claim[field] = claim[field].replace("%q", "%r")
        for field in ("required", "forbidden"):
            claim["target_assertions"][field] = [
                fragment.replace("%q", "%r")
                for fragment in claim["target_assertions"][field]
            ]
        self.assert_invalid(python_r, "exceeds 0 source placeholders")

    def test_wrong_scope_for_mixed_decomposition_rejected(self):
        value = copy.deepcopy(self.registry)
        value["numeric_claims"][0]["scope"] = "per_tick"
        self.assert_invalid(value, "per_tick scope")

    def test_fraction_arithmetic_mismatch_rejected(self):
        value = copy.deepcopy(self.registry)
        periodic = value["numeric_claims"][0]["decomposition"]["components"][1]
        periodic["fraction_of_input"] = {"numerator": 1, "denominator": 5}
        self.assert_invalid(value, "component fractions sum")

    def test_fireburn_per_turn_regression_rejected(self):
        value = copy.deepcopy(self.registry)
        claim = value["numeric_claims"][0]
        claim["target_text"] = claim["target_text"].replace(
            "3 回合内造成 %0.2f 火焰伤害", "每回合造成 %0.2f 火焰伤害"
        )
        self.assert_invalid(value, "required fragment absent")

    def test_duration_and_tick_count_are_independent(self):
        value = copy.deepcopy(self.registry)
        value["numeric_claims"][0]["decomposition"]["tick_count"] = 2
        self.assert_invalid(value, "periodic component count 3 != tick_count 2")

    def test_explicitness_relation_is_mechanically_enforced(self):
        value = copy.deepcopy(self.registry)
        claim = value["numeric_claims"][0]
        claim["source_explicitness"] = "ambiguous_scope"
        self.assert_invalid(value, "requires justification")

        claim["explicitation_justified"] = True
        claim["status"] = "pending"
        self.assert_invalid(value, "pending or unpinned claim")

        claim["status"] = "confirmed"
        self.assert_valid(value)

        claim["source_explicitness"] = "explicit_scope"
        self.assert_invalid(value, "requires increased target explicitness")

    def test_fixed_decomposition_allows_pure_immediate_and_expire(self):
        immediate = copy.deepcopy(self.registry)
        claim = immediate["numeric_claims"][0]
        claim["scope"] = "on_apply"
        claim["decomposition"] = {
            "kind": "fixed_fraction",
            "applicability": "unconditional",
            "duration_turns": 0,
            "tick_count": 0,
            "components": [{
                "phase": "on_apply",
                "fraction_of_input": {"numerator": 1, "denominator": 1},
                "count": 1,
            }],
            "total_fraction_of_input": {"numerator": 1, "denominator": 1},
        }
        self.assert_valid(immediate)

        expire = copy.deepcopy(immediate)
        claim = expire["numeric_claims"][0]
        claim["scope"] = "on_expire"
        claim["decomposition"]["duration_turns"] = 3
        claim["decomposition"]["components"][0]["phase"] = "on_expire"
        self.assert_valid(expire)

    def test_fixed_decomposition_rejects_invalid_zero_tick_combinations(self):
        no_periodic = copy.deepcopy(self.registry)
        claim = no_periodic["numeric_claims"][0]
        claim["scope"] = "on_apply"
        claim["decomposition"] = {
            "kind": "fixed_fraction",
            "applicability": "unconditional",
            "duration_turns": 0,
            "tick_count": 1,
            "components": [{
                "phase": "on_apply",
                "fraction_of_input": {"numerator": 1, "denominator": 1},
                "count": 1,
            }],
            "total_fraction_of_input": {"numerator": 1, "denominator": 1},
        }
        self.assert_invalid(no_periodic, "without periodic components requires tick_count 0")

        zero_duration_expire = copy.deepcopy(no_periodic)
        decomposition = zero_duration_expire["numeric_claims"][0]["decomposition"]
        zero_duration_expire["numeric_claims"][0]["scope"] = "on_expire"
        decomposition["tick_count"] = 0
        decomposition["components"][0]["phase"] = "on_expire"
        self.assert_invalid(zero_duration_expire, "requires positive duration_turns")

    def test_fireburn_is_effect_absent_and_anchored_to_effect_consumers(self):
        claim = self.registry["numeric_claims"][0]
        self.assertEqual(claim["decomposition"]["applicability"], "effect_absent")
        anchors = {anchor["symbol"]: anchor for anchor in claim["anchors"]}
        self.assertEqual(anchors["newTalent Flame.action"]["line_hint"], 49)
        self.assertEqual(anchors["newTalent Flame.info"]["line_hint"], 85)
        self.assertEqual(anchors["EFF_BURNING.on_timeout"]["line_hint"], 438)
        self.assertEqual(anchors["EFF_BURNING.on_merge"]["line_hint"], 434)

    def test_reviewer_briefing_rejects_prefilled_conclusion(self):
        for field, content in (
            ("scope", "total_over_effect"),
            ("components", []),
            ("expected_verdict", "supported"),
        ):
            with self.subTest(field=field):
                value = copy.deepcopy(self.registry)
                value["reviewer_briefings"][0][field] = content
                self.assert_invalid(value, f"extra=['{field}']")

    def test_reviewer_briefing_binds_candidate_raw_token_permutation(self):
        missing = copy.deepcopy(self.registry)
        missing["reviewer_briefings"][0]["candidate_target"] = "没有数值参数"
        self.assert_invalid(missing, "format tokens do not match args_order")

        drift = copy.deepcopy(self.registry)
        drift["reviewer_briefings"][0]["candidate_target"] = drift[
            "reviewer_briefings"
        ][0]["candidate_target"].replace("%0.2f", "%f")
        self.assert_invalid(drift, "format tokens do not match args_order")

        reordered = copy.deepcopy(self.registry)
        briefing = reordered["reviewer_briefings"][0]
        briefing["source_text"] = "Deals %0.2f damage over %d turns."
        briefing["candidate_target"] = "%d 回合内造成 %0.2f 伤害。"
        briefing["placeholder_index"] = 1
        briefing["placeholder_token"] = "%0.2f"
        self.assert_invalid(reordered, "format tokens do not match args_order")
        briefing["args_order"] = [2, 1]
        self.assert_valid(reordered)

    def test_runtime_composition_wrong_order_rejected(self):
        value = copy.deepcopy(self.registry)
        value["runtime_compositions"][0]["args_order"] = [2, 1]
        self.assert_invalid(value, "rendered sentence mismatch")

    def test_runtime_composition_duplicate_grammar_rejected(self):
        value = copy.deepcopy(self.registry)
        case = value["runtime_compositions"][0]
        case["target_template"] = "%s的%s射击打偏了。"
        case["renderings"][0]["rendered_sentence"] = "格鲁什的他的射击打偏了。"
        case["renderings"][0]["assertions"]["required"] = ["格鲁什的他的射击打偏了。"]
        self.assert_invalid(value, "forbidden fragment present")

    def test_runtime_composition_freezes_all_surface_variants(self):
        case = self.registry["runtime_compositions"][0]
        self.assertEqual(
            [[variant["sample_value"] for variant in placeholder["variants"]]
             for placeholder in case["placeholders"]],
            [["格鲁什", "某物"], ["他的", "她", "它的"]],
        )
        self.assertEqual(len(case["renderings"]), 6)
        self.assertEqual(
            [rendering["rendered_sentence"] for rendering in case["renderings"]],
            [
                "格鲁什未能命中目标；这一枪记在他的名下。",
                "格鲁什未能命中目标；这一枪记在她名下。",
                "格鲁什未能命中目标；这一枪记在它的名下。",
                "某物未能命中目标；这一枪记在他的名下。",
                "某物未能命中目标；这一枪记在她名下。",
                "某物未能命中目标；这一枪记在它的名下。",
            ],
        )

    def test_runtime_composition_rejects_old_feminine_sentence(self):
        value = copy.deepcopy(self.registry)
        rendering = value["runtime_compositions"][0]["renderings"][1]
        rendering["rendered_sentence"] = "格鲁什没能命中目标；那一枪是她。"
        rendering["assertions"]["required"] = [rendering["rendered_sentence"]]
        self.assert_invalid(value, "rendered sentence mismatch")

    def test_runtime_variant_anchors_are_exact_nonempty_and_required(self):
        singular = copy.deepcopy(self.registry)
        variant = singular["runtime_compositions"][0]["placeholders"][0]["variants"][0]
        variant["anchor"] = variant.pop("anchors")[0]
        self.assert_invalid(singular, "anchors")

        empty = copy.deepcopy(self.registry)
        empty["runtime_compositions"][0]["placeholders"][0]["variants"][0][
            "anchors"
        ] = []
        self.assert_invalid(empty, "non-empty anchor array")

        missing_anchor_field = copy.deepcopy(self.registry)
        del missing_anchor_field["runtime_compositions"][0]["placeholders"][1][
            "variants"
        ][0]["anchors"][1]["path"]
        self.assert_invalid(missing_anchor_field, "path")

        no_required = copy.deepcopy(self.registry)
        anchors = no_required["runtime_compositions"][0]["placeholders"][0]["variants"][0][
            "anchors"
        ]
        for anchor in anchors:
            anchor["required"] = False
        self.assert_invalid(no_required, "at least one anchor must be required")

        confirmed_unpinned = copy.deepcopy(self.registry)
        confirmed_unpinned["runtime_compositions"][0]["status"] = "confirmed"
        self.assert_invalid(confirmed_unpinned, "unpinned required anchor")

    def test_runtime_variant_provenance_covers_adjudicated_layers(self):
        case = self.registry["runtime_compositions"][0]
        variants = {
            variant["variant_id"]: variant
            for placeholder in case["placeholders"]
            for variant in placeholder["variants"]
        }
        unseen = variants["unseen-something"]["anchors"]
        self.assertEqual(
            [(anchor["path"], anchor["line_hint"]) for anchor in unseen],
            [
                ("tome-orcs/data/talents/steam/gunslinging.lua", 114),
                ("tome-orcs/data/talents/steam/gunslinging.lua", 115),
                ("tome-orcs.lua", 5104),
            ],
        )
        for variant_id, helper_line, locale_line in (
            ("masculine-his", 942, 1409),
            ("feminine-her", 940, 1407),
            ("neuter-its", 941, 1408),
        ):
            anchors = variants[variant_id]["anchors"]
            self.assertEqual(
                [(anchor["path"], anchor["line_hint"]) for anchor in anchors],
                [
                    ("tome-orcs/data/talents/steam/gunslinging.lua", 115),
                    ("game/engines/default/engine/utils.lua", helper_line),
                    ("engine.lua", locale_line),
                ],
            )
            self.assertEqual(anchors[2]["revision"], "8c9b065601c4545d9f19e6983bb2c5088561be10")

    def test_runtime_composition_requires_complete_variant_cross_product(self):
        value = copy.deepcopy(self.registry)
        value["runtime_compositions"][0]["renderings"].pop()
        self.assert_invalid(value, "cover every variant combination")

    def test_runtime_composition_compares_raw_tokens_and_ignores_escaped_percent(self):
        drift = copy.deepcopy(self.registry)
        drift["runtime_compositions"][0]["source_template"] = "%10s misses %s shot."
        self.assert_invalid(drift, "only supports raw bare %s")

        escaped = copy.deepcopy(self.registry)
        case = escaped["runtime_compositions"][0]
        case["source_template"] = "100%%: " + case["source_template"]
        case["target_template"] = "100%%：" + case["target_template"]
        for rendering in case["renderings"]:
            rendering["rendered_sentence"] = "100%：" + rendering["rendered_sentence"]
            rendering["assertions"]["required"] = [
                "100%：" + fragment for fragment in rendering["assertions"]["required"]
            ]
        self.assert_valid(escaped)

    def test_runtime_composition_rejects_invalid_percent_on_both_template_sides(self):
        for field in ("source_template", "target_template"):
            for invalid in ("%r", "%a", "%*s", "%"):
                with self.subTest(field=field, invalid=invalid):
                    value = copy.deepcopy(self.registry)
                    case = value["runtime_compositions"][0]
                    case[field] += invalid
                    if field == "target_template":
                        for rendering in case["renderings"]:
                            rendering["rendered_sentence"] += invalid
                    self.assert_invalid(value, "invalid percent sequence")

    def test_runtime_composition_accepts_only_raw_bare_s(self):
        self.assert_valid(copy.deepcopy(self.registry))
        for token in ("%10s", "%.2s", "%-s"):
            with self.subTest(token=token):
                value = copy.deepcopy(self.registry)
                case = value["runtime_compositions"][0]
                case["source_template"] = case["source_template"].replace("%s", token)
                case["target_template"] = case["target_template"].replace("%s", token)
                self.assert_invalid(value, "only supports raw bare %s")

    def test_runtime_composition_renders_lua_q_in_complete_sentences(self):
        value = copy.deepcopy(self.registry)
        case = value["runtime_compositions"][0]
        case["source_template"] = "%10q misses %--q shot."
        case["target_template"] = "%10q未能命中目标；这一枪记在%--q名下。"
        samples = {
            variant["variant_id"]: variant["sample_value"]
            for placeholder in case["placeholders"]
            for variant in placeholder["variants"]
        }
        for rendering in case["renderings"]:
            first, second = (samples[variant_id] for variant_id in rendering["variant_ids"])
            sentence = f'"{first}"未能命中目标；这一枪记在"{second}"名下。'
            rendering["rendered_sentence"] = sentence
            rendering["assertions"] = {"required": [sentence], "forbidden": []}
        self.assert_valid(value)

    def test_runtime_composition_rejects_lua51_scanformat_overflow(self):
        for token, message in (
            ("%100q", "at most two width digits"),
            ("%.100q", "at most two precision digits"),
            ("%-+ #0-q", "at most five flag characters"),
        ):
            with self.subTest(token=token):
                value = copy.deepcopy(self.registry)
                case = value["runtime_compositions"][0]
                case["source_template"] = case["source_template"].replace("%s", token, 1)
                case["target_template"] = case["target_template"].replace("%s", token, 1)
                self.assert_invalid(value, message)

    def test_runtime_composition_rejects_numeric_conversions(self):
        for conversion in ("d", "u"):
            with self.subTest(conversion=conversion):
                value = copy.deepcopy(self.registry)
                case = value["runtime_compositions"][0]
                case["source_template"] = case["source_template"].replace(
                    "%s", f"%{conversion}"
                )
                case["target_template"] = case["target_template"].replace(
                    "%s", f"%{conversion}"
                )
                self.assert_invalid(
                    value,
                    "runtime composition v1 only supports %s and %q conversions",
                )

    def test_runtime_composition_requires_string_samples(self):
        for sample in (3, 3.0, True, ""):
            with self.subTest(sample=sample):
                value = copy.deepcopy(self.registry)
                value["runtime_compositions"][0]["placeholders"][0]["variants"][0][
                    "sample_value"
                ] = sample
                self.assert_invalid(value, "expected non-empty string")

    def test_runtime_composition_lua_q_allows_quotes_backslashes_and_lf(self):
        value = copy.deepcopy(self.registry)
        case = value["runtime_compositions"][0]
        case["source_template"] = "%q / %q"
        case["target_template"] = "%q与%q。"
        case["placeholders"][0]["variants"] = [
            case["placeholders"][0]["variants"][0]
        ]
        case["placeholders"][1]["variants"] = [
            case["placeholders"][1]["variants"][0]
        ]
        case["placeholders"][0]["variants"][0]["sample_value"] = '格"鲁\\什\n'
        case["placeholders"][1]["variants"][0]["sample_value"] = "她"
        expected = '"格\\"鲁\\\\什\\\n"与"她"。'
        rendering = case["renderings"][0]
        case["renderings"] = [rendering]
        rendering["rendered_sentence"] = expected
        rendering["assertions"] = {"required": [expected], "forbidden": []}
        self.assert_valid(value)

    def test_runtime_composition_lua_q_rejects_unsafe_controls(self):
        for character in ("\r", "\0", "\t", "\x01", "\x1f", "\x7f"):
            with self.subTest(codepoint=ord(character)):
                value = copy.deepcopy(self.registry)
                case = value["runtime_compositions"][0]
                case["source_template"] = case["source_template"].replace("%s", "%q")
                case["target_template"] = case["target_template"].replace("%s", "%q")
                case["placeholders"][0]["variants"][0]["sample_value"] += character
                self.assert_invalid(value, "must not contain C0 controls except LF or DEL")

    def test_duplicate_json_object_key_rejected(self):
        raw = REGISTRY.read_text(encoding="utf-8")
        mutated = raw.replace('"schema_version": 1,', '"schema_version": 1,\n  "schema_version": 1,', 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(mutated, encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "duplicate object key"):
                check_registry(path, strict=True)

    def test_invalid_utf8_is_validation_error_and_cli_exit_5_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_bytes(b'\xff{"schema_version": 1}')
            with self.assertRaisesRegex(ValidationError, "invalid semantic claim registry UTF-8"):
                check_registry(path, strict=True)

            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(ROOT / "tools" / "i18n"),
                    "claims",
                    "check",
                    "--registry",
                    str(path),
                    "--strict",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 5)
            self.assertIn("ERROR: invalid semantic claim registry UTF-8", completed.stderr)
            self.assertNotIn("Traceback", completed.stderr)


if __name__ == "__main__":
    unittest.main()
