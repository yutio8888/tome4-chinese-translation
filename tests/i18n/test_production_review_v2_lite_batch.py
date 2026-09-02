from __future__ import annotations
import unittest
from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite_batch as batch
import surface_screen_manifest as surface_manifest
import surface_screen_result_check as surface


def row(identity, fixed="commit:" + "a" * 40, size=1, last=True):
    return {"entry_revision_identity": identity, "logical_entry_identity": "a" * 64,
            "fixed_source_identity": fixed, "terminology_snapshot_sha256": "t" * 64,
            "rules_version": "rules", "component": "tome", "source": "s", "target": "t",
            "source_tag": "", "normalized_path": "tome.lua", "call_locator": "c" * 64,
            "risk": {"has_args_order": False, "has_special": False, "component_group_size": size,
                     "component_group_last": last, "source_utf8_bytes": 1, "target_utf8_bytes": 1}}


class BatchBoundaryTests(unittest.TestCase):
    def test_limit_boundaries_and_stable_selection(self):
        rows = [row(format(i, "064x"), size=i) for i in range(1, 81)]
        self.assertEqual(batch.stable_selection(rows, {}, retry_blocked=False, limit=0), [])
        self.assertEqual(len(batch.stable_selection(rows, {}, retry_blocked=False, limit=80)), 80)
        with self.assertRaises(Exception): batch.stable_selection(rows, {}, retry_blocked=False, limit=81)
        self.assertEqual([r["entry_revision_identity"] for r in batch.stable_selection(rows, {}, retry_blocked=False)],
                         [r["entry_revision_identity"] for r in batch.stable_selection(rows, {}, retry_blocked=False)])

    def test_normal_and_blocked_domains_do_not_mix(self):
        rows = [row("1" * 64), row("2" * 64), row("3" * 64)]
        self.assertEqual([r["entry_revision_identity"] for r in batch.stable_selection(rows, {"1" * 64: "blocked"}, retry_blocked=True)], ["1" * 64])
        self.assertEqual({r["entry_revision_identity"] for r in batch.stable_selection(rows, {"1" * 64: "blocked"}, retry_blocked=False)}, {"2" * 64, "3" * 64})

    def test_partition_is_identity_homogeneous_and_parent_remappable(self):
        rows = [row("a" * 64), row("b" * 64, fixed="commit:" + "b" * 40), row("c" * 64)]
        runs = batch.partition_surface_entries(rows)
        self.assertEqual(sorted(i for run in runs for i in run["parent_indexes"]), [0, 1, 2])
        self.assertEqual([run["parent_indexes"] for run in runs], [[0, 2], [1]])
        for run in runs:
            self.assertEqual(run["entries"], sorted(run["entries"], key=lambda item: item["entry_revision_identity"]))
            self.assertEqual(len({(e["entry_revision_identity"]) for e in run["entries"]}), len(run["entries"]))

    def test_v2_surface_projection_preserves_pilot_runtime_argument_order(self):
        value = row("f" * 64)
        value["rules_version"] = surface.IDENTITY_RULES_V2
        value["source"] = "%s has %d"
        value["target"] = "%d belongs to %s"
        value["risk"] = dict(value["risk"], has_args_order=True, args_order=[2, 1])
        value["logical_entry_identity"] = surface.logical_entry_identity(
            component=value["component"], normalized_path=value["normalized_path"],
            call_locator=value["call_locator"], source_tag=value["source_tag"])
        value["entry_revision_identity"] = surface.entry_revision_identity(
            logical_entry_identity=value["logical_entry_identity"], source=value["source"],
            target=value["target"], fixed_source_identity=value["fixed_source_identity"],
            terminology_snapshot=value["terminology_snapshot_sha256"],
            rules_version=value["rules_version"], args_order=[2, 1])
        projected = batch._surface_entry(value)
        self.assertEqual(projected["args_order"], [2, 1])
        payload = batch._payload({"identity": (value["fixed_source_identity"],
                                                   value["terminology_snapshot_sha256"],
                                                   value["rules_version"]),
                                 "entries": [projected]})
        surface.validate_payload(payload)
        runtime_values = ["ability", 7]
        self.assertEqual([runtime_values[index - 1] for index in projected["args_order"]], [7, "ability"])
        missing = dict(value)
        missing["risk"] = dict(missing["risk"])
        missing["risk"].pop("args_order")
        with self.assertRaises(wp1.ProductionReviewError):
            batch._surface_entry(missing)

    def test_v2_contextual_projection_discloses_args_order_and_binds_candidate_bytes(self):
        def contextual_row(args_order):
            value = row("f" * 64)
            value["rules_version"] = surface.IDENTITY_RULES_V2
            value["section"] = "fixture"
            value["source"] = "%s has %d"
            value["target"] = "%d belongs to %s"
            value["risk"] = dict(value["risk"], has_args_order=True, args_order=args_order)
            value["logical_entry_identity"] = surface.logical_entry_identity(
                component=value["component"], normalized_path=value["normalized_path"],
                call_locator=value["call_locator"], source_tag=value["source_tag"])
            value["entry_revision_identity"] = surface.entry_revision_identity(
                logical_entry_identity=value["logical_entry_identity"], source=value["source"],
                target=value["target"], fixed_source_identity=value["fixed_source_identity"],
                terminology_snapshot=value["terminology_snapshot_sha256"],
                rules_version=value["rules_version"], args_order=args_order)
            return value

        reordered = contextual_row([2, 1])
        run = {"identity": (reordered["fixed_source_identity"],
                             reordered["terminology_snapshot_sha256"],
                             reordered["rules_version"]),
               "entries": [reordered]}
        payload = batch._contextual_payload(run)
        self.assertEqual(
            payload["bounded_context"][0]["context"], "fixture args_order={2,1}")
        first_bytes = contextual_row([1, 2])
        first_payload = batch._contextual_payload({**run, "entries": [first_bytes]})
        self.assertNotEqual(surface.canonical_bytes(payload), surface.canonical_bytes(first_payload))

        historical = row("e" * 64)
        historical["section"] = "fixture"
        historical_payload = batch._contextual_payload({
            "identity": (historical["fixed_source_identity"],
                         historical["terminology_snapshot_sha256"],
                         historical["rules_version"]),
            "entries": [historical]})
        self.assertEqual(historical_payload["bounded_context"][0]["context"], "fixture")

    def test_surface_manifest_boundary_builders_use_real_consumer_forms(self):
        def surface_rows(count):
            result = []
            for i in range(count):
                value = row(format(i, "064x"))
                value["call_locator"] = "fixture/" + format(i, "064x")
                value["logical_entry_identity"] = __import__("surface_screen_result_check").logical_entry_identity(
                    component=value["component"], normalized_path=value["normalized_path"],
                    call_locator=value["call_locator"], source_tag=value["source_tag"])
                value["entry_revision_identity"] = __import__("surface_screen_result_check").entry_revision_identity(
                    logical_entry_identity=value["logical_entry_identity"], source=value["source"], target=value["target"],
                    fixed_source_identity=value["fixed_source_identity"], terminology_snapshot=value["terminology_snapshot_sha256"], rules_version=value["rules_version"])
                result.append(batch._surface_entry(value))
            return sorted(result, key=lambda item: item["entry_revision_identity"])
        for count in (1, 3):
            payload = batch._payload({"identity": ("commit:" + "a" * 40, "t" * 64, "rules"),
                                      "entries": surface_rows(count)})
            envelope, _path, _ = surface_manifest.build_full(payload, task_id="batch-test", dispatch_id=f"full-{count}")
            self.assertEqual(len(envelope["payload"]["entries"]), count)
        for count in (4, 79, 80):
            entries = surface_rows(count)
            payload = batch._payload({"identity": ("commit:" + "a" * 40, "t" * 64, "rules"), "entries": entries})
            manifest, _path, envelopes = surface_manifest.build_group(
                payload, task_id="batch-test", group_id=f"group-{count}", review_phase="REVIEW",
                cycle=0, attempt=1, dispatch_ids=[f"lane-{count}-{i}" for i in range(4)])
            self.assertEqual(len(envelopes), 4)
            self.assertEqual(sum(len(item[1]["payload"]["entries"]) for item in envelopes), count)
            self.assertEqual(manifest["payload"]["lane_count"], 4)

    def test_malformed_optional_hashes_are_controlled(self):
        ref = {"run_index": 0, "lane_index": 0, "contract": "translation_surface_screen_v1",
               "input_path": "input.json", "input_sha256": "i" * 64,
               "output_path": None, "output_sha256": None, "validator_status": "prepared",
               "candidate_identity": "c" * 64, "parent_indexes": [0],
               "intended_state_updates": None, "group_manifest_path": None,
               "group_manifest_sha256": None}
        for key in ("output_sha256", "group_manifest_sha256"):
            malformed = dict(ref)
            malformed[key] = 1
            with self.assertRaises(wp1.ProductionReviewError):
                batch._validate_surface_ref(malformed, 0)

    def test_checkpoint_schema_has_one_active_path_and_seven_state_cap(self):
        self.assertEqual(batch.MAX_BATCH, 80)
        self.assertEqual(len(batch.PHASES), 7)
        self.assertEqual(batch.PHASES, {"reserved", "surface_ready", "surface_collected", "deep_ready", "deep_collected", "adjudicated", "commit_ready"})
        self.assertEqual(batch.CHECKPOINT_KEYS - {"schema_version", "kind"}, batch.CHECKPOINT_KEYS - {"schema_version", "kind"})


if __name__ == "__main__": unittest.main()
