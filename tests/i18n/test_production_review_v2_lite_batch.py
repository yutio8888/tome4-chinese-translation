from __future__ import annotations
import unittest
import copy
import hashlib
import json
from pathlib import Path
from unittest import mock
from tests.i18n import test_production_review_v2_lite_queue as queue_fixtures
from tools.i18nlib import production_review_v2_lite_queue as queue
import ai_state_check
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



class MixedRunConsumerTests(queue_fixtures.QueueFixture):
    """Synthetic reviews only, in a disposable fixture repository; real consumers."""

    def _prepare(self, sizes):
        self.entries = []
        for run_index, size in enumerate(sizes):
            for index in range(size):
                entry = self._entry(f'{run_index}-{index}')
                entry['component'] = ['engine', 'boot', 'tome', 'cults'][run_index]
                core = dict(component=entry['component'], duplicate_index=0, function_name='t',
                            normalized_source_tag='', section='fixture', source=entry['source'],
                            translation_path='tome.lua')
                entry['call_locator'] = queue_fixtures.catalog._plain_id(
                    queue_fixtures.catalog.CALL_LOCATOR_KIND, 'locator', core)
                entry['logical_entry_identity'] = surface.logical_entry_identity(
                    component=entry['component'], normalized_path=entry['normalized_path'],
                    call_locator=entry['call_locator'], source_tag=entry['source_tag'])
                entry['fixed_source_identity'] = 'commit:' + str(run_index + 1) * 40
                entry['entry_revision_identity'] = surface.entry_revision_identity(
                    logical_entry_identity=entry['logical_entry_identity'], source=entry['source'],
                    target=entry['target'], fixed_source_identity=entry['fixed_source_identity'],
                    terminology_snapshot=entry['terminology_snapshot_sha256'],
                    rules_version=entry['rules_version'], args_order=None)
                self.entries.append(entry)
        self._write_catalog()
        self._rewrite_catalog(self.entries)
        self._commit('synthetic mixed catalog')
        queue.init(self.root)
        batch.start(self.root, limit=sum(sizes))
        checkpoint = batch.show(self.root)
        self.assertEqual(len(checkpoint['selected']), sum(sizes))
        return checkpoint

    def _verify_run(self, checkpoint, run, refs):
        task_id = checkpoint['batch_id'] + (f"-surface-{run['run_index']:03d}"
                                           if len(batch.surface_payloads(checkpoint)) > 1 else '')
        task_dir = f'.ai/task/{task_id}'
        draft_path = f'{task_dir}/SURFACE-SCREEN-INPUT.json'
        def write(path, value):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(surface.canonical_bytes(value))
        write(draft_path, batch._payload(run))
        group = None
        if refs[0]['group_manifest_path']:
            group = json.loads(Path(refs[0]['group_manifest_path']).read_bytes())
            self.assertEqual(group['payload']['task_id'], task_id)
            group_path = f"{task_dir}/SURFACE-SCREEN-GROUP-{group['payload']['group_id']}.json"
            write(group_path, group)
        state = dict(schema_version=5, task_id=task_id, mode='review_only',
                     change_class='translation_workflow', state='DONE', cycle=0, max_cycles=3,
                     workspace_id='fixture-workspace', orchestrator_agent_id='fixture-orchestrator',
                     review_contracts=[surface.CONTRACT], pending_review_contracts=[],
                     completed_review_contracts=[surface.CONTRACT], open_accepted_findings=[],
                     deferred_findings=[], child_dispatches=[], review_records=[], senior_review_records=[],
                     surface_screen_input_path=draft_path)
        bound = [draft_path]
        outputs = {}
        for index, ref in enumerate(refs):
            envelope = json.loads(Path(ref['input_path']).read_bytes())
            dispatch_id = (group['payload']['lanes'][index]['dispatch_id'] if group else
                           f"full-{run['run_index']:03d}")
            input_path = f'{task_dir}/SURFACE-SCREEN-ENVELOPE-{dispatch_id}.json'
            write(input_path, envelope)
            output = dict(contract=surface.CONTRACT, candidate_identity=ref['candidate_identity'],
                          results=[dict(entry_revision_identity=e['entry_revision_identity'], verdict='OK')
                                   for e in envelope['payload']['entries']])
            raw_path = f'.ai/reviews/{task_id}/raw-{dispatch_id}.txt'
            write(raw_path, output)
            raw = (self.root / raw_path).read_bytes()
            surface.validate_result_bytes(Path(ref['input_path']).read_bytes(), raw)
            outputs[checkpoint['surface'].index(ref)] = raw
            record = dict(task_id=task_id, review_contract=surface.CONTRACT, review_phase='REVIEW',
                          cycle=0, attempt=checkpoint['attempt'], reviewer_role='REVIEWER',
                          purpose=surface.CONTRACT, dispatch_id=dispatch_id,
                          agent_id=f'synthetic-{task_id}-{dispatch_id}', workspace_id='fixture-workspace',
                          parent_agent_id='fixture-orchestrator', lineage_verified=True, result='PASS',
                          review_kind='lane' if group else 'full', candidate_identity=ref['candidate_identity'],
                          input_path=input_path, raw_output_path=raw_path,
                          raw_output_sha256=hashlib.sha256(raw).hexdigest())
            child = dict(dispatch_id=dispatch_id, role='REVIEWER', purpose=surface.CONTRACT,
                         agent_id=record['agent_id'], parent_agent_id='fixture-orchestrator',
                         workspace_id='fixture-workspace', lineage_verified=True,
                         lifecycle='archived', archive_confirmed=True,
                         candidate_identity=ref['candidate_identity'], input_path=input_path,
                         labels=dict(task_id=task_id, role='reviewer', purpose=surface.CONTRACT,
                                     candidate_identity=ref['candidate_identity'], dispatch_id=dispatch_id))
            if group:
                boundary = group['payload']['lane_boundaries'][index]
                record['lane'] = dict(group_id=group['payload']['group_id'],
                    group_identity=group['group_identity'], group_manifest_path=group_path,
                    index=boundary['index'], count=4, offset=boundary['offset'], length=boundary['length'])
                child.update(lane_group_identity=group['group_identity'], lane_index=boundary['index'])
                child['labels'].update(lane_group_identity=group['group_identity'], lane_index=str(boundary['index']))
            record_path = f'{task_dir}/review-{dispatch_id}.json'
            write(record_path, record)
            state['review_records'].append(record_path)
            state['child_dispatches'].append(child)
            bound.extend([input_path, raw_path])
        if group:
            surface_manifest.validate_group_manifest(group, root=self.root, manifest_path=group_path)
        state['surface_evidence_binding'] = dict(algorithm='surface-evidence-binding/1', task_id=task_id,
            terminal='whole_screen', artifact_sha256={path: hashlib.sha256((self.root / path).read_bytes()).hexdigest()
                                                     for path in bound})
        state_path = f'{task_dir}/STATE.json'
        write(state_path, state)
        checked = ai_state_check.check_state(self.root / state_path, workspace_root=self.root, target='DONE')
        self.assertEqual(checked.outcome, 'DONE_VERIFIED', checked.detail)
        # A real terminal must reject missing completion records, even with valid raw results.
        incomplete = copy.deepcopy(state)
        incomplete['review_records'].pop()
        write(state_path, incomplete)
        rejected = ai_state_check.check_state(self.root / state_path, workspace_root=self.root, target='DONE')
        self.assertNotEqual(rejected.outcome, 'DONE_VERIFIED')
        write(state_path, state)
        return task_id, outputs

    def _round_trip(self, sizes):
        before = self._prepare(sizes)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        self.assertEqual(checkpoint['selected'], before['selected'])
        runs = batch.partition_surface_entries(checkpoint['entry_snapshots'])
        self.assertEqual(sorted(len(run['entries']) for run in runs), sorted(sizes))
        outputs, task_ids = {}, []
        for run in runs:
            refs = [ref for ref in checkpoint['surface'] if ref['run_index'] == run['run_index']]
            task_id, accepted = self._verify_run(checkpoint, run, refs)
            task_ids.append(task_id)
            outputs.update({str(k): v for k, v in accepted.items()})
        self.assertEqual(len(set(task_ids)), len(sizes))
        frozen = queue.checkpoint_path(self.root).read_bytes()
        self.assertTrue(batch.surface_export(self.root)['ok'])
        self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), frozen)
        for wrong in (dict(list(outputs.items())[1:]), {**outputs, 'extra': next(iter(outputs.values()))}):
            with self.assertRaises(wp1.ProductionReviewError):
                batch.surface_import(self.root, wrong)
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), frozen)
        self.assertEqual(batch.surface_import(self.root, outputs)['imported'], sum(sizes))
        imported = batch.show(self.root)
        self.assertEqual(imported['selected'], before['selected'])
        updates = [revision for ref in imported['surface'] for revision in ref['intended_state_updates']]
        self.assertEqual(len(updates), sum(sizes))
        self.assertEqual(set(updates), set(before['selected']))
        self.assertEqual(batch.surface_import(self.root, outputs)['imported'], 0)

    def test_actual_next_batch_run_sizes_round_trip(self):
        self._round_trip([21, 37, 22])

    def test_mixed_full_1_2_3_and_four_lane_round_trip(self):
        self._round_trip([1, 2, 3, 4])

    def test_single_run_keeps_historical_task_path(self):
        self._round_trip([4])

    def test_single_full_keeps_historical_task_path(self):
        self._round_trip([1])

    def test_historical_multi_run_stored_groups_remain_readable(self):
        before = self._prepare([4, 5])
        original = surface_manifest.build_group
        def historical_group(payload, **kwargs):
            kwargs['task_id'] = before['batch_id']
            return original(payload, **kwargs)
        # Reproduce pre-fix export format, without changing consumer or stored schema.
        with mock.patch.object(surface_manifest, 'build_group', side_effect=historical_group):
            batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        paths = [queue.checkpoint_path(self.root)]
        for ref in checkpoint['surface']:
            paths.extend([Path(ref['input_path']), Path(ref['group_manifest_path'])])
        old_bytes = {path: path.read_bytes() for path in paths}
        batch.surface_export(self.root)
        self.assertEqual({path: path.read_bytes() for path in paths}, old_bytes)
        outputs = {}
        for i, ref in enumerate(checkpoint['surface']):
            envelope = json.loads(Path(ref['input_path']).read_bytes())
            outputs[str(i)] = surface.canonical_bytes(dict(contract=surface.CONTRACT,
                candidate_identity=ref['candidate_identity'], results=[
                    dict(entry_revision_identity=e['entry_revision_identity'], verdict='OK')
                    for e in envelope['payload']['entries']]))
        self.assertEqual(batch.surface_import(self.root, outputs)['imported'], 9)


if __name__ == '__main__':
    unittest.main()
