#!/usr/bin/env python3
"""Single-writer, notification-driven review journal; no polling or agent discovery.

Transport methods consume/return captured MCP get_agent_status objects and exact
terminal bytes. The capture-file CLI is an orchestration interface, NOT MCP wire
schema. Never feed formatted CLI inspect/logs output to this adapter.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
from pathlib import Path
import re
import sys
import time
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _orch
import contextual_result_check as contextual
import surface_screen_result_check as surface
import surface_screen_manifest as manifests

SURFACE = surface.CONTRACT
CONTEXTUAL = 'translation_contextual_v2'


class LifecycleError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise LifecycleError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    # Captures may have transport whitespace; model output never goes through this.
    return json.loads(Path(path).read_bytes(), object_pairs_hook=contextual._reject_duplicate)


def immutable(path, raw):
    path = Path(path)
    if path.exists():
        require(path.read_bytes() == raw, f'immutable artifact changed: {path}')
    else:
        _orch.write_atomic(path, raw)


def timestamp(value):
    require(isinstance(value, str) and bool(value), 'missing timestamp')
    date = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(date.tzinfo is not None, 'timestamp must include timezone')
    return date.timestamp()


def validate_input(root, row):
    path = Path(row['input_path'])
    require(not path.is_absolute() and '..' not in path.parts, 'input must be repository-relative')
    require((root / path).resolve().is_relative_to(root.resolve()), 'input escapes root')
    require(not (root / path).is_symlink() and (root / path).is_file(), 'input must name an ordinary file')
    raw = (root / path).read_bytes()
    env = contextual.strict_json_bytes(raw, label='envelope')
    validator = surface if row['purpose'] == SURFACE else contextual
    _, identity = validator.validate_envelope(env)
    require(surface.canonical_bytes(env) == raw, 'envelope must be exact canonical bytes')
    require(identity == row['candidate_identity'], 'input candidate mismatch')
    if 'input_sha256' in row:
        require(digest(raw) == row['input_sha256'], 'frozen input SHA drift')
    return raw


def snapshot(capture, row, *, archived=False):
    """MCP status response scope verified against real captured response shape."""
    require(isinstance(capture, dict) and isinstance(capture.get('snapshot'), dict),
            'need complete MCP status response with snapshot; CLI inspect is insufficient')
    s = capture['snapshot']
    for field in ('id', 'workspaceId', 'cwd', 'labels', 'status', 'attentionReason', 'attentionTimestamp'):
        require(field in s, f'snapshot missing {field}')
    require(capture.get('status') == s['status'], 'status wrapper/snapshot mismatch')
    require(s['id'] and s['id'] != row['parent_agent_id'], 'root agent cannot be child')
    if row.get('agent_id'):
        require(s['id'] == row['agent_id'], 'agent ID mismatch')
    require(s['workspaceId'] == row['workspace_id'], 'workspace mismatch')
    require(s['cwd'] == row['cwd'], 'cwd mismatch')
    require(isinstance(s['labels'], dict), 'labels missing')
    for key, value in row['labels'].items():
        require(s['labels'].get(key) == value, f'label mismatch: {key}')
    if not archived:
        require('activeTurn' in s, 'snapshot missing activeTurn')
    return s


def is_archived(s):
    return s['status'] == 'closed' and bool(s.get('archivedAt')) and s.get('activeTurn') is None


def terminal(s):
    require('activeTurn' in s and s['activeTurn'] is None, 'child has active or unknown turn')
    require(s['status'] in ('idle', 'error'), 'not a natural terminal status')
    require(s['attentionReason'] in ('finished', 'error'), 'no terminal attention fact')
    timestamp(s['attentionTimestamp'])


def require_frozen_terminal(row, capture):
    frozen = row.get('terminal_capture')
    if frozen is not None:
        fields = ('id', 'workspaceId', 'cwd', 'labels', 'status', 'attentionReason',
                  'attentionTimestamp', 'activeTurn', 'provider', 'persistence', 'runtimeInfo')
        require(all(frozen['snapshot'].get(k) == capture['snapshot'].get(k) for k in fields),
                'frozen terminal capture changed')


def observation(s, captured_at):
    def field(key):
        return {'presence': 'present', 'value': deepcopy(s[key])} if key in s else {'presence': 'missing'}
    return dict(schema_version=1, source='live_agent_metadata', captured_at=captured_at,
                capture_status='captured', provider=field('provider'), model=field('model'),
                mode=field('currentModeId'), thinking=field('thinkingOptionId'))


# Only contract fields are copied into STATE. Journal timing/captures are diagnostic.
CHILD_KEYS = ('agent_id', 'dispatch_id', 'role', 'purpose', 'candidate_identity', 'input_path',
              'workspace_id', 'parent_agent_id', 'labels', 'lineage_verified', 'lifecycle',
              'archive_confirmed', 'archive_attempts_started', 'archived_at', 'last_error',
              'runtime_observation', 'candidate_author_agent_id', 'author_provider_resolution',
              'lane_index', 'lane_group_identity', 'output_valid', 'raw_output_path', 'raw_output_sha256')


class Journal:
    """One ORCHESTRATOR writer, one journal. Interrupted writes reconcile from it.

    No retry loop: each invocation consumes at most one archive attempt per child.
    All scans visit only the explicit finite plan/journal. No production queue IO.
    """
    def __init__(self, path, *, root=None):
        self.path = Path(path)
        self.root = Path(root or _orch.ROOT).resolve()
        self.rows = read(path) if self.path.exists() else []
        require(isinstance(self.rows, list), 'children journal must be a list')
        keys = [self.key(r) for r in self.rows]
        ids = [r['agent_id'] for r in self.rows if r.get('agent_id')]
        require(len(keys) == len(set(keys)) and len(ids) == len(set(ids)), 'duplicate dispatch or agent ID')

    @staticmethod
    def key(row):
        return f"{row['task_id']}|{row['dispatch_id']}"

    def get(self, key):
        hits = [r for r in self.rows if self.key(r) == key]
        require(len(hits) == 1, f'unknown/ambiguous dispatch: {key}')
        return hits[0]

    def save(self):
        mirrors = []
        # Validate every mirror before writing; persist authoritative STATE mirrors before returning to any external call.
        for task in sorted({r['task_id'] for r in self.rows}):
            path = self.root / '.ai/task' / task / 'STATE.json'
            state = read(path)
            rows = [r for r in self.rows if r['task_id'] == task]
            require(state.get('orchestration_transport') in ('cli', 'mcp')
                    and all(r.get('creation_transport') == state['orchestration_transport'] for r in rows),
                    'task creation transport mismatch')
            if state.get('state') in ('DONE', 'STOP'):
                continue
            require(state['task_id'] == task and state['workspace_id'] == rows[0]['workspace_id'],
                    'STATE task/workspace drift')
            require(state.get('orchestrator_agent_id') in (None, rows[0]['parent_agent_id']), 'STATE parent drift')
            require(state.get('mode') == 'review_only', 'helper only supports review_only')
            state['orchestrator_agent_id'] = rows[0]['parent_agent_id']
            children = state.setdefault('child_dispatches', [])
            for row in rows:
                if 'runtime_observation' not in row:
                    continue
                child = {k: deepcopy(row[k]) for k in CHILD_KEYS if k in row}
                old = [c for c in children if c.get('dispatch_id') == row['dispatch_id']]
                require(len(old) <= 1, 'duplicate STATE dispatch')
                if old:
                    for key in ('agent_id', 'candidate_identity', 'input_path', 'parent_agent_id', 'workspace_id'):
                        require(old[0].get(key) == child[key], f'STATE binding drift: {key}')
                    if 'runtime_observation' in old[0]:
                        require(old[0]['runtime_observation'] == child['runtime_observation'], 'first runtime observation drift')
                    old[0].update(child)
                else:
                    require(not any(c.get('agent_id') == child['agent_id'] for c in children), 'duplicate STATE agent')
                    children.append(child)
            state['updated_at'] = now()
            if any(r['archive_attempts_started'] >= 2 and not r['archive_confirmed']
                   for r in rows):
                wait = state.get('wait')
                if state['state'] == 'WAIT_USER':
                    require(isinstance(wait, dict) and wait.get('reason') == 'archive_pending'
                            and wait.get('resume_state') not in (None, 'WAIT_USER'), 'unknown WAIT_USER recovery point')
                else:
                    wait = dict(reason='archive_pending', resume_state=state['state'])
                state.update(state='WAIT_USER', wait=wait,
                             last_error='archive budget exhausted; readback required')
            elif isinstance(state.get('wait'), dict) and state['wait'].get('reason') == 'archive_pending':
                if all(self.settled(r) for r in rows):
                    resume = state['wait'].get('resume_state')
                    require(resume and resume != 'WAIT_USER', 'missing wait.resume_state')
                    state.update(state=resume, wait=None, last_error=None)
            mirrors.append((path, state))
        _orch.write_json_atomic(self.path, self.rows)
        for path, state in mirrors:
            _orch.write_json_atomic(path, state)

    @contextmanager
    def timed(self, row, category, operation):
        start, clock = now(), time.monotonic()
        event = dict(category=category, operation=operation, started_at=start)
        row.setdefault('timing', []).append(event)
        self.save()
        try:
            yield
        finally:
            event.update(ended_at=now(), elapsed_s=time.monotonic() - clock)
            self.save()

    @staticmethod
    def settled(row):
        if row.get('agent_id'):
            return row['archive_confirmed'] is True
        return row['status'] in ('prepared', 'confirmed_absent')

    def select_transport(self, tasks, transport):
        """Explicit selection before the first preparation; never migrate history."""
        require(transport in ('cli', 'mcp'), 'unknown creation transport')
        updates = []
        for task in tasks:
            path = self.root / '.ai/task' / task / 'STATE.json'
            state = read(path)
            require(state.get('state') not in ('DONE', 'STOP'), 'task is closed')
            require(not state.get('child_dispatches') and not any(r['task_id'] == task for r in self.rows),
                    'transport selection requires a task without history or preparation')
            state['orchestration_transport'] = transport
            updates.append((path, state))
        for path, state in updates:
            _orch.write_json_atomic(path, state)

    def prepare(self, specs, purpose, parent, workspace, prompt_builder, selection, *, transport='mcp'):
        require(purpose in (SURFACE, CONTEXTUAL), 'unsupported contract')
        require(transport in ('cli', 'mcp'), 'unknown creation transport')
        require(parent and workspace, 'parent/workspace required')
        prepared = []
        groups = {}
        for spec in specs:
            row = {k: spec[k] for k in ('task_id', 'dispatch_id', 'candidate_identity', 'input_path')}
            for name, limit in (('task_id', 127), ('dispatch_id', 31)):
                require(re.fullmatch(r'[0-9a-z][0-9a-z-]{0,' + str(limit) + '}', row[name]), f'unsafe {name}')
            row.update(purpose=purpose, role='REVIEWER', parent_agent_id=parent, workspace_id=workspace,
                       cwd=str(self.root), review_kind=spec.get('review_kind', 'full'), attempt=spec.get('attempt', 1),
                       creation_transport=transport, cycle=0, candidate_author_agent_id=None, author_provider_resolution='not_applicable')
            require(type(row['attempt']) is int and row['attempt'] >= 1, 'invalid attempt')
            require(row['review_kind'] in ('full', 'lane'), 'invalid review_kind')
            require(purpose == SURFACE or row['review_kind'] == 'full', 'contextual helper only supports full review_only')
            if row['review_kind'] == 'lane':
                gp = spec['group_manifest_path']
                if gp not in groups:
                    g = read(self.root / gp)
                    manifests.validate_group_manifest(g, root=self.root, manifest_path=gp)
                    groups[gp] = g
                g = groups[gp]
                p = g['payload']
                require(p['task_id'] == row['task_id'], 'group task mismatch')
                lane = next((l for l in p['lanes'] if l['dispatch_id'] == row['dispatch_id']), None)
                require(lane is not None and all(lane[k] == row[k] for k in ('input_path', 'candidate_identity')), 'lane binding mismatch')
                require(spec['index'] == lane['index'], 'lane index mismatch')
                boundary = p['lane_boundaries'][lane['index'] - 1]
                row.update(attempt=p['attempt'], cycle=p['cycle'], group_manifest_path=gp,
                           group_manifest_sha256=digest((self.root / gp).read_bytes()),
                           lane_group_identity=g['group_identity'], lane_index=lane['index'])
                row['lane'] = dict(count=4, group_id=p['group_id'], group_identity=g['group_identity'],
                                   group_manifest_path=gp, **boundary)
            row['input_sha256'] = digest(validate_input(self.root, row))
            if purpose == SURFACE and row['review_kind'] == 'full':
                require(row['input_path'] == f".ai/task/{row['task_id']}/SURFACE-SCREEN-ENVELOPE-{row['dispatch_id']}.json",
                        'surface full input path must bind dispatch')
                require(1 <= len(read(self.root / row['input_path'])['payload']['entries']) <= 3,
                        'surface full stage requires 1..3 entries')
            row['labels'] = dict(task_id=row['task_id'], role='reviewer', purpose=purpose,
                                 candidate_identity=row['candidate_identity'], dispatch_id=row['dispatch_id'],
                                 **{'paseo.parent-agent-id': parent})
            if row.get('lane'):
                row['labels'].update(lane_group_identity=row['lane_group_identity'], lane_index=str(row['lane_index']))
            prompt = prompt_builder(row['candidate_identity'], row['input_path'])
            require(len(prompt.encode('utf-8')) <= 800, 'prompt exceeds 800 bytes')
            row['create_parameters'] = dict(selection, workspaceId=workspace, cwd=str(self.root), labels=row['labels'], prompt=prompt)
            row.update(agent_id=None, status='prepared', lifecycle='active', archive_attempts_started=0,
                       archive_confirmed=False, prepared_at=now())
            if spec.get('retry_of'):
                row['retry_of'] = spec['retry_of']
            prepared.append(row)
        require(prepared, 'empty plan')
        require(len({self.key(r) for r in prepared}) == len(prepared), 'duplicate planned dispatch')
        for task in {r['task_id'] for r in prepared}:
            members = [r for r in prepared if r['task_id'] == task]
            self.stage(members, accepted=False)
            state = read(self.root / '.ai/task' / task / 'STATE.json')
            require(state.get('mode') == 'review_only' and state.get('state') not in ('DONE', 'STOP'), 'task is not open review_only')
            require(state.get('workspace_id') == workspace, 'STATE workspace mismatch')
            require(state.get('orchestrator_agent_id') in (None, parent), 'STATE parent mismatch')
            require(state.get('review_contracts') == [purpose], 'STATE contract mismatch')
            # Never silently switch an active task's transport or lose managed history.
            require(state.get('orchestration_transport') == transport, 'task creation transport mismatch; select explicitly before preparation')
            if state.get('child_dispatches'):
                known = {r.get('agent_id') for r in self.rows}
                require(all(c.get('agent_id') in known for c in state['child_dispatches']), 'STATE has history outside journal')
        for row in prepared:
            previous = next((r for r in self.rows if self.key(r) == self.key(row)), None)
            if previous:
                for field in ('candidate_identity', 'input_path', 'input_sha256', 'labels', 'workspace_id', 'cwd', 'attempt', 'create_parameters', 'creation_transport'):
                    require(previous.get(field) == row[field], f'prepared binding changed: {field}')
                require(previous['status'] != 'dispatching', 'ambiguous create; reconcile captured live metadata before re-emitting')
                require(previous['status'] != 'created', 'first live metadata still required before re-emitting')
                continue
            history = [r for r in self.rows if r['task_id'] == row['task_id']]
            require(all(self.settled(r) for r in history), 'archive all previous children before successor')
            if history:
                require(row['attempt'] > max(r['attempt'] for r in history), 'retry needs greater attempt')
                if purpose == CONTEXTUAL or row['review_kind'] == 'full':
                    old = self.get(row.get('retry_of', ''))
                    require(old in history and (old.get('output_valid') is False or (not old.get('agent_id') and self.settled(old))), 'retry must name failed attempt')
                    fields = ('candidate_identity', 'input_sha256', 'purpose', 'role', 'workspace_id', 'parent_agent_id')
                    if purpose == CONTEXTUAL:
                        fields += ('input_path',)
                    for field in fields:
                        require(row[field] == old[field], f'fresh retry changed {field}')
                else:
                    old = history[-1]
                    require(old.get('lane') and old['lane_group_identity'] != row['lane_group_identity']
                            and old['group_manifest_path'] != row['group_manifest_path'], 'surface retry needs fresh group')
                    oldg = read(self.root / old['group_manifest_path'])
                    newg = read(self.root / row['group_manifest_path'])
                    require(oldg['payload']['workset'] == newg['payload']['workset'], 'retry workset drift')
        # All lanes are checked before the first persisted preparation or create.
        existing = {self.key(r) for r in self.rows}
        self.rows.extend(r for r in prepared if self.key(r) not in existing)
        self.save()
        return [dict(key=self.key(r), task_id=r['task_id'], dispatch_id=r['dispatch_id'],
                     **r['create_parameters']) for r in self.rows
                if self.key(r) in {self.key(p) for p in prepared} and r['status'] in ('prepared', 'confirmed_absent')]

    def create_blocked(self, key):
        """Read-only stop gate for new work; existing-child recovery stays available."""
        row = self.get(key)
        state = read(self.root / '.ai/task' / row['task_id'] / 'STATE.json')
        if state.get('state') in ('DONE', 'STOP', 'WAIT_USER'):
            return 'new create blocked: task ' + state['state']
        if any(r['archive_attempts_started'] >= 2 and not r['archive_confirmed'] for r in self.rows):
            return 'new create blocked: unresolved archive budget exhausted'
        return None

    def create_intent(self, key, profiles_path):
        row = self.get(key)
        blocked = self.create_blocked(key)
        require(blocked is None, blocked)
        require(row['status'] in ('prepared', 'confirmed_absent'), 'create already attempted; never blindly repeat')
        require(row.get('create_attempts_started', 0) < 2, 'creation retry budget exhausted')
        require(not any(r is not row and r['status'] in ('dispatching', 'created') for r in self.rows),
                'first live metadata or reconciliation required before next create')
        require(row['attempt'] == max(r['attempt'] for r in self.rows if r['task_id'] == row['task_id']),
                'cannot create a superseded plan member')
        validate_input(self.root, row)
        profiles = Path(profiles_path).read_bytes()
        require(bool(json.loads(profiles)), 'empty live profiles capture')
        # The caller reads list_profiles immediately before EACH intent/create.
        attempt = row.get('create_attempts_started', 0) + 1
        path = self.path.parent / (row['task_id'] + '-' + row['dispatch_id'] + f'-create-{attempt}-profiles.json')
        immutable(path, profiles)
        started = now()
        row.setdefault('create_attempts', []).append(dict(attempt=attempt, started_at=started,
                profiles_path=str(path), profiles_sha256=digest(profiles)))
        row.update(status='dispatching', create_started_at=started, profiles_sha256=digest(profiles),
                   create_prompt_sha256=digest(row['create_parameters']['prompt'].encode('utf-8')),
                   create_attempts_started=attempt)
        self.save()
        return row['create_parameters']

    def reconcile_absent(self, key, evidence_path):
        """Consume a bounded host audit, not an invented remote wire response.

        The host attests complete enumeration and supplies unfiltered snapshots,
        original query/page evidence, and exact known-history exclusions. This
        helper recomputes filtering before cardinality; it never discovers agents.
        """
        row = self.get(key)
        require(row['status'] == 'dispatching' and not row.get('agent_id'), 'not an ambiguous unbound create')
        audit_raw = Path(evidence_path).read_bytes()
        audit = json.loads(audit_raw, object_pairs_hook=contextual._reject_duplicate)
        attempt = row['create_attempts_started']
        require(audit.get('schema') == 'review-create-reconciliation/1'
                and audit.get('key') == key and audit.get('create_attempt') == attempt,
                'reconciliation dispatch/attempt mismatch')
        require(timestamp(audit['queried_at']) >= timestamp(row['create_started_at']), 'stale reconciliation')
        expected = dict(workspace_id=row['workspace_id'], cwd=row['cwd'], labels=row['labels'])
        require(audit.get('filter') == expected, 'incomplete identity filter')
        require(audit.get('complete') is True and audit.get('includes_archived') is True
                and audit.get('lifecycle_filter') is None, 'query must be complete including all lifecycles')
        history = sorted(r['agent_id'] for r in self.rows if r.get('agent_id'))
        require(audit.get('excluded_history_ids') == history, 'history exclusions mismatch')
        pages = audit.get('pages')
        require(isinstance(pages, list) and len(pages) == 1, 'one complete bounded list_agents query required')
        seen, matches = set(), []
        for page in pages:
            require(page.get('cursor') is None and page.get('next_cursor') is None
                    and page.get('has_more') is False, 'incomplete page chain')
            request = page.get('request', {})
            args = request.get('arguments', {})
            require(request.get('tool') == 'list_agents' and set(args) == {'includeArchived', 'cwd', 'sinceHours', 'limit'}
                    and args['includeArchived'] is True and args['cwd'] == row['cwd']
                    and type(args['sinceHours']) is int and 1 <= args['sinceHours'] <= 720
                    and type(args['limit']) is int and 1 <= args['limit'] <= 200,
                    'full unfiltered list_agents request required')
            require(timestamp(audit['queried_at']) - args['sinceHours'] * 3600 < timestamp(row['create_started_at']),
                    'query time window excludes possible creation')
            response = page.get('response', {}).get('structuredContent', {})
            listed = response.get('agents')
            # Installed public MCP list_agents slices at limit without a cursor.
            # Equality to limit is ambiguous, never evidence of absence.
            require(isinstance(listed, list) and len(listed) < args['limit'], 'list truncated or completeness unknown')
            listed_ids = [item.get('id') for item in listed]
            require(len(listed_ids) == len(set(listed_ids)), 'duplicate list ID')
            entries = page.get('snapshots')
            require(isinstance(entries, list) and len(entries) == len(listed)
                    and {item.get('id') for item in entries} == set(listed_ids), 'snapshot coverage differs from raw list')
            for item in listed:
                captured = next(entry for entry in entries if entry.get('id') == item.get('id'))
                require(all(k in item and item[k] == captured.get(k) for k in ('id', 'cwd', 'labels')),
                        'list/snapshot identity changed')
            for item in entries:
                require(isinstance(item, dict) and all(k in item for k in ('id', 'workspaceId', 'cwd', 'labels'))
                        and isinstance(item['labels'], dict) and isinstance(item['id'], str) and item['id'],
                        'incomplete discovery identity')
                require(item['id'] not in seen, 'duplicate discovery ID')
                seen.add(item['id'])
                if item['id'] in history:
                    continue
                if (item['workspaceId'] == row['workspace_id'] and item['cwd'] == row['cwd']
                        and all(item['labels'].get(k) == v for k, v in row['labels'].items())):
                    matches.append(item['id'])
        require(not matches, 'nonzero reconciliation; bind unique complete capture or WAIT_USER')
        path = self.path.parent / (row['task_id'] + '-' + row['dispatch_id'] + f'-absent-{attempt}.json')
        immutable(path, audit_raw)
        row.setdefault('reconciliations', []).append(dict(create_attempt=attempt, evidence_path=str(path),
                   evidence_sha256=digest(audit_raw), excluded_history_ids=history, matched_ids=[], at=now()))
        row['status'] = 'confirmed_absent'
        self.save()

    def create_cli(self, key, profiles_path):
        row = self.get(key)
        require(row['creation_transport'] == 'cli', 'actual create path disagrees with task transport')
        parameters = self.create_intent(key, profiles_path)
        args = ['run', '--background', '--provider', parameters['provider'],
                '--thinking', parameters['thinkingOptionId'], '--mode', parameters['modeId'],
                '--workspace', parameters['workspaceId'], '--cwd', parameters['cwd']]
        for key_name, value in parameters['labels'].items():
            args.extend(['--label', key_name + '=' + value])
        args.extend(['--json', parameters['prompt']])
        # A failed/ambiguous call leaves its durable intent for reconciliation.
        with self.timed(row, 'tool_call', 'cli_create'):
            result = _orch.paseo_json(args, timeout=60)
            require(isinstance(result, dict), 'CLI create response must be an object')
            self.record_id(key, result.get('agentId'))
        return row['agent_id']  # created only; next child waits for live binding

    def record_id(self, key, aid):
        row = self.get(key)
        require(isinstance(aid, str) and aid and aid != row['parent_agent_id'], 'invalid child ID')
        require(row['status'] in ('dispatching', 'created', 'dispatched'), 'create-intent must precede create')
        require(not any(r is not row and r.get('agent_id') == aid for r in self.rows), 'duplicate agent ID')
        require(row.get('agent_id') in (None, aid), 'dispatch already bound to another agent')
        row['agent_id'] = aid
        if 'runtime_observation' not in row:
            row['status'] = 'created'
        self.save()

    def bind(self, key, capture):
        row = self.get(key)
        require(row['status'] in ('dispatching', 'created', 'dispatched'), 'create-intent must precede live binding')
        validate_input(self.root, row)
        s = snapshot(capture, row, archived=capture.get('status') == 'closed')
        require(not any(r is not row and r.get('agent_id') == s['id'] for r in self.rows), 'duplicate agent ID')
        update = dict(agent_id=s['id'], status='dispatched', lineage_verified=True,
                      first_live_capture=deepcopy(capture), runtime_observation=observation(s, now()),
                      live_observation_source='mcp_status_capture')
        if is_archived(s):
            timestamp(s['archivedAt'])
            update.update(lifecycle='archived', archive_confirmed=True, archived_at=s['archivedAt'])
        elif s['activeTurn'] is None:
            terminal(s)
            update['lifecycle'] = 'terminal'
        else:
            require(isinstance(s['activeTurn'], dict), 'invalid activeTurn shape')
        if 'runtime_observation' in row:
            self.save()  # also repairs a crash between journal and STATE writes
            return
        row.update(update)  # no shared mutation until every capture check succeeds
        self.save()

    def harvest(self, key, capture, raw, outdir, *, notified):
        row = self.get(key)
        require(notified is True, 'harvest requires a finish notification; no polling')
        require('runtime_observation' in row, 'first live metadata not bound')
        s = snapshot(capture, row)
        terminal(s)
        require(s['status'] == 'idle' and s['attentionReason'] == 'finished',
                'harvest needs successful natural completion; use explicit reject for error')
        require_frozen_terminal(row, capture)
        require(not row.get('archive_confirmed') and row.get('archive_attempts_started') == 0
                or row.get('validation_state') in ('completed', 'rejected'),
                'validation must precede archive')
        require(isinstance(raw, bytes), 'terminal output must be exact bytes')
        rejected = row.get('validation_state') == 'rejected' or bool(row.get('rejection'))
        path = Path(outdir) / row['task_id'] / (row['dispatch_id'] + '.raw')
        immutable(path, raw)  # diagnostics first, including invalid UTF-8 and failed results
        if 'raw_output_sha256' in row:
            require(row['raw_output_sha256'] == digest(raw), 'terminal output changed')
            if row.get('validation_state') in ('completed', 'rejected') or row.get('validation_error') or row.get('output_valid') is True:
                return row['output_valid']
        row.update(raw_output_path=str(path.resolve().relative_to(self.root)) if path.resolve().is_relative_to(self.root) else str(path.resolve()),
                   raw_output_sha256=digest(raw), terminal_capture=deepcopy(capture),
                   terminal_observed_at=now(), lifecycle='terminal', validation_state='pending')
        if rejected:
            row.update(validation_state='rejected', output_valid=False)
            self.save()
            return False
        with self.timed(row, 'harvest_validation', 'strict_result'):
            try:
                validator = surface if row['purpose'] == SURFACE else contextual
                validator.validate_result_bytes(validate_input(self.root, row), raw)
                row.update(output_valid=True, validation_state='completed')
            except (LifecycleError, contextual.ContractError, contextual.InputError,
                    surface.ContractError, surface.InputError, OSError) as error:
                row.update(output_valid=False, validation_error=str(error), validation_state='completed')
        return row['output_valid']

    def archive_intent(self, key, capture):
        row = self.get(key)
        require(row.get('validation_state') in ('completed', 'rejected'),
                'completed validation or explicit rejection must precede archive')
        s = snapshot(capture, row, archived=True)
        if is_archived(s):
            self.confirm_archive(key, capture)
            return False
        terminal(s)
        require_frozen_terminal(row, capture)
        require(row.get('output_valid') is not True or (s['status'] == 'idle' and s['attentionReason'] == 'finished'),
                'accepted output needs successful terminal')
        require(row['archive_attempts_started'] < 2, 'archive budget exhausted; WAIT_USER, readback only')
        row['archive_attempts_started'] += 1
        row.update(lifecycle='archive_pending', archive_confirmed=False, archive_started_at=now())
        self.save()  # budget durable in journal AND STATE before external operation
        return True

    def confirm_archive(self, key, capture):
        row = self.get(key)
        s = snapshot(capture, row, archived=True)
        if not is_archived(s):
            row.update(lifecycle='archive_pending', last_error='archive readback not confirmed')
            self.save()
            raise LifecycleError('archive readback not confirmed; no successor/phase transition')
        timestamp(s['archivedAt'])
        row.update(lifecycle='archived', archive_confirmed=True, archived_at=s['archivedAt'],
                   archived_capture=deepcopy(capture), archive_confirmed_at=now(), last_error=None)
        self.save()

    def reject(self, key, reason, evidence_path, *, capture=None, notified=False):
        """Record evidence-backed abandonment or scope/read-only invalidation.

        Strict JSON success is not proof of reviewer conduct. Never rewrite raw,
        and never revoke an already published acceptance through this helper.
        """
        row = self.get(key)
        require(row.get('agent_id') and row.get('lineage_verified') is True
                and 'runtime_observation' in row and isinstance(reason, str) and reason.strip(),
                'bound child and concrete rejection reason required')
        require(row['cwd'] == str(self.root) and row['role'] == 'REVIEWER'
                and row['purpose'] in (SURFACE, CONTEXTUAL), 'rejection root/role/purpose mismatch')
        for name, value in dict(task_id=row['task_id'], dispatch_id=row['dispatch_id'], role='reviewer',
                                purpose=row['purpose'], candidate_identity=row['candidate_identity'],
                                **{'paseo.parent-agent-id': row['parent_agent_id']}).items():
            require(row['labels'].get(name) == value, 'journal label binding mismatch')
        state = read(self.root / '.ai/task' / row['task_id'] / 'STATE.json')
        require(state.get('task_id') == row['task_id'] and state.get('workspace_id') == row['workspace_id']
                and state.get('orchestrator_agent_id') == row['parent_agent_id']
                and state.get('mode') == 'review_only' and state.get('state') not in ('DONE', 'STOP')
                and state.get('orchestration_transport') == row['creation_transport'],
                'rejection STATE/root binding mismatch')
        children = [c for c in state.get('child_dispatches', []) if c.get('dispatch_id') == row['dispatch_id']]
        require(len(children) == 1 and all(children[0].get(k) == row.get(k) for k in
                ('agent_id', 'role', 'purpose', 'workspace_id', 'parent_agent_id', 'labels',
                 'candidate_identity', 'input_path', 'runtime_observation', 'lineage_verified')),
                'rejection needs immutable registered STATE child')
        require(not state.get('review_records'), 'acceptance already published; explicit task repair required')
        validate_input(self.root, row)
        if capture is not None:
            require(notified is True, 'rejection capture requires a finish notification')
            require(row.get('terminal_capture', capture) == capture, 'frozen terminal capture changed')
        else:
            require('terminal_capture' in row, 'terminal evidence required before abandonment')
            capture = row['terminal_capture']
        s = snapshot(capture, row)
        terminal(s)
        first = snapshot(row['first_live_capture'], row)
        for snap in (first, s):
            if 'parentAgentId' in snap:
                require(snap['parentAgentId'] == row['parent_agent_id'], 'conflicting direct parent')
        raw = Path(evidence_path).read_bytes()
        require(bool(raw.strip()), 'rejection evidence is empty')
        path = self.path.parent / (row['task_id'] + '-' + row['dispatch_id'] + '-rejection-evidence')
        rejection = dict(reason=reason, evidence_path=str(path), evidence_sha256=digest(raw))
        require(row.get('rejection', rejection) == rejection, 'rejection evidence changed')
        evidence_exists = path.exists()
        immutable(path, raw)
        update = dict(output_valid=False, validation_state='rejected', rejection=rejection)
        if 'terminal_capture' not in row:
            update.update(terminal_capture=deepcopy(capture), terminal_observed_at=now(), lifecycle='terminal')
        # save validates every STATE mirror before writing. Keep the shared row,
        # including the first observation object, untouched if that validation fails.
        staged = deepcopy(self)
        staged.get(key).update(update)
        try:
            staged.save()
        except LifecycleError:
            # Mirror validation precedes all journal/STATE writes; discard only
            # evidence created by this rejected call, never an existing artifact.
            if not evidence_exists:
                path.unlink()
            raise
        row.update(update)

    def harvest_and_archive(self, key, transport, outdir, *, notified):
        """Injected transport: status(key), terminal_bytes(key), archive(key).

        Each method is one bounded call. A raised archive error still gets a
        readback; crash recovery starts with readback before consuming more budget.
        """
        row = self.get(key)
        require(notified is True, 'notification required')
        if row.get('validation_state') not in ('completed', 'rejected'):
            with self.timed(row, 'tool_call', 'terminal_status'):
                capture = transport.status(key)
            snapshot(capture, row)
            terminal(capture['snapshot'])
            try:
                with self.timed(row, 'tool_call', 'terminal_bytes'):
                    raw = ((self.root / row['raw_output_path']).read_bytes()
                           if row.get('validation_state') == 'pending' else transport.terminal_bytes(key))
            except Exception as error:
                row.update(lifecycle='terminal', terminal_capture=deepcopy(capture), terminal_observed_at=now())
                row.setdefault('terminal_fetch_errors', []).append(dict(at=now(), error=str(error)))
                self.save()
                return None  # unavailable is recoverable, never a completed invalid verdict
            else:
                self.harvest(key, capture, raw, outdir, notified=True)
        with self.timed(row, 'tool_call', 'pre_archive_status'):
            before = transport.status(key)
        if not self.archive_intent(key, before):
            return row['output_valid']
        try:
            with self.timed(row, 'tool_call', 'archive'):
                transport.archive(key)
        except Exception as error:
            row['last_error'] = str(error)
            self.save()
        with self.timed(row, 'archive_confirmation', 'archive_readback'):
            after = transport.status(key)
            self.confirm_archive(key, after)
        return row['output_valid']

    def stage(self, members, *, accepted=True):
        require(members, 'empty stage')
        first = members[0]
        for row in members:
            require(all(row[k] == first[k] for k in ('task_id', 'purpose', 'attempt', 'review_kind', 'cycle')), 'mixed stage')
        if first['review_kind'] == 'lane':
            require(len(members) == 4 and {r['lane_index'] for r in members} == {1, 2, 3, 4}, 'partial four-lane stage')
            require(len({r['lane_group_identity'] for r in members}) == 1, 'mixed lane groups')
            for row in members:
                gp = row['group_manifest_path']
                require(digest((self.root / gp).read_bytes()) == row['group_manifest_sha256'], 'manifest SHA drift')
            manifests.validate_group_manifest(read(self.root / first['group_manifest_path']),
                                               root=self.root, manifest_path=first['group_manifest_path'])
        else:
            require(len(members) == 1, 'full stage must have one member')
        if accepted:
            require(all(self.settled(r) for r in self.rows if r['task_id'] == first['task_id']), 'unarchived task history')
            require(first['attempt'] == max(r['attempt'] for r in self.rows if r['task_id'] == first['task_id']), 'cannot accept superseded stage')
            for row in members:
                require(row.get('output_valid') is True and row['archive_confirmed'] is True, 'invalid or unarchived member')
                raw = (self.root / row['raw_output_path']).read_bytes()
                require(digest(raw) == row['raw_output_sha256'], 'raw SHA drift')
                validator = surface if row['purpose'] == SURFACE else contextual
                validator.validate_result_bytes(validate_input(self.root, row), raw)
        return members

    def timing_report(self):
        """Intervals stay separate; only unions are reported as occupied wall time."""
        intervals = []
        for row in self.rows:
            for e in row.get('timing', []):
                intervals.append(dict(key=self.key(row), **e))
            live = row.get('first_live_capture', {}).get('snapshot', {})
            end = row.get('terminal_capture', {}).get('snapshot', {}).get('attentionTimestamp')
            start = (live.get('activeTurn') or {}).get('startedAt')
            if start and end:
                intervals.append(dict(key=self.key(row), category='model_window', started_at=start,
                                      ended_at=end, basis='activeTurn.startedAt to terminal attentionTimestamp'))
            for start, end, basis in ((end, row.get('terminal_observed_at'), 'terminal to harvest'),
                                      (row.get('prepared_at'), row.get('create_started_at'), 'preparation to create intent')):
                if start and end:
                    intervals.append(dict(key=self.key(row), category='orchestration_gap', started_at=start,
                                          ended_at=end, basis=basis))
            if row.get('archive_started_at') and row.get('archive_confirmed_at'):
                intervals.append(dict(key=self.key(row), category='archive_confirmation',
                                      started_at=row['archive_started_at'], ended_at=row['archive_confirmed_at'],
                                      basis='archive intent to confirmed readback, including external tool interval'))
        totals = {}
        for category in {i['category'] for i in intervals}:
            spans = sorted((timestamp(i['started_at']), timestamp(i['ended_at']))
                           for i in intervals if i['category'] == category and i.get('ended_at'))
            merged = []
            for start, end in spans:
                require(end >= start, 'negative timing interval')
                if merged and start <= merged[-1][1]:
                    merged[-1][1] = max(end, merged[-1][1])
                else:
                    merged.append([start, end])
            totals[category] = sum(end - start for start, end in merged)
        created = [r.get('first_live_capture', {}).get('snapshot', {}).get('createdAt') for r in self.rows]
        starts = [r.get('create_started_at') for r in self.rows]
        ends = [r.get('archive_confirmed_at') for r in self.rows]
        measured = lambda values: bool(values) and all(values)
        stage = dict(created_at_spread_s=max(map(timestamp, created)) - min(map(timestamp, created))
                     if measured(created) else None,
                     wall_s=max(map(timestamp, ends)) - min(map(timestamp, starts))
                     if measured(starts) and measured(ends) else None,
                     tool_calls=sum(len(r.get('wire_events', [])) for r in self.rows),
                     members=[dict(key=self.key(r), created_at=c,
                         terminal_at=r.get('terminal_capture', {}).get('snapshot', {}).get('attentionTimestamp'),
                         notification_received_at=r.get('notification_received_at'),
                         archive_started_at=r.get('archive_started_at'), archive_confirmed_at=r.get('archive_confirmed_at'))
                         for r, c in zip(self.rows, created)])
        return dict(stage=stage, intervals=intervals, union_seconds_by_category=totals,
                    note='Categories can overlap; do not sum as batch wall time. Missing endpoints are unmeasured.')


# Provider-native logs are an observation source, never a lifecycle transport.
NATIVE_MAX_BYTES = 16 * 1024 * 1024
NATIVE_MAX_LINES = 10000


def native_identity(s, *, required=True):
    """Read scoped persistence; present aliases must agree, never fill from profile."""
    p = s.get('persistence')
    if p is None and not required:
        p = {}
    require(isinstance(p, dict), 'native source requires persistence')
    provider, session = s.get('provider'), p.get('sessionId')
    require(provider in ('codex', 'claude', 'grok'), 'unsupported native provider')
    if required:
        require(isinstance(session, str) and session, 'missing persistence.sessionId')
        require(p.get('provider') == provider, 'persistence provider mismatch')
    scopes = [s, p]
    for container, key in ((s, 'runtimeInfo'), (p, 'metadata')):
        if key in container:
            require(isinstance(container[key], dict), f'invalid {key}')
            scopes.append(container[key])
    sessions = []
    for scope in scopes:
        if 'provider' in scope:
            # Grok is exposed by the agent API, but its native session is
            # persisted by the ACP runtime.  Keep the exception scoped to
            # persistence.metadata; every other provider alias must still
            # agree with the agent provider.
            allowed = ('acp',) if provider == 'grok' and scope is p.get('metadata') else (provider,)
            require(scope['provider'] in allowed, 'conflicting provider')
        if 'cwd' in scope:
            require(scope['cwd'] == s['cwd'], 'conflicting persistence cwd')
        for key in ('sessionId', 'threadId'):
            if key in scope and scope[key] is not None:
                require(isinstance(scope[key], str) and scope[key], 'invalid session alias')
                sessions.append(scope[key])
    if p.get('nativeHandle') is not None:
        require(isinstance(p['nativeHandle'], str) and p['nativeHandle'], 'invalid session alias')
        sessions.append(p['nativeHandle'])
    require(not sessions or all(v == sessions[0] for v in sessions), 'conflicting session identity')
    return provider, session or (sessions[0] if sessions else None)


def _native_text(content, kind):
    require(isinstance(content, list) and len(content) == 1
            and isinstance(content[0], dict) and content[0].get('type') == kind
            and isinstance(content[0].get('text'), str), 'native final/prompt requires one text block')
    return content[0]['text']


def _parse_native_final(data, *, provider, session_id, cwd, prompt, natural_success=False):
    """Pure bounded parser: no filesystem, journal, agent calls or hidden-text output.

    Only the two verified version/record dialects are supported. Returned bytes
    encode the selected original string directly, including all whitespace.
    """
    require(type(natural_success) is bool, 'natural_success must be explicit boolean')
    require(isinstance(data, bytes) and 0 < len(data) <= NATIVE_MAX_BYTES, 'native byte limit')
    require(data.endswith(b'\n'), 'incomplete native final line')
    lines = data.split(b'\n')[:-1]
    require(1 <= len(lines) <= NATIVE_MAX_LINES, 'native line limit')
    require(all(isinstance(v, str) and v for v in (session_id, cwd, prompt)), 'native binding missing')
    try:
        records = [json.loads(line.decode('utf-8'), object_pairs_hook=contextual._reject_duplicate)
                   for line in lines]
    except (ValueError, UnicodeError, RecursionError, contextual.ContractError):
        raise LifecycleError('invalid native JSONL (no partial recovery)') from None
    require(all(isinstance(r, dict) for r in records), 'invalid native record')
    if provider == 'codex':
        version = '0.153.0'
        require(records[0].get('type') == 'session_meta', 'missing initial session_meta')
        meta = records[0].get('payload', {})
        require(meta.get('cli_version') == version and meta.get('id') == session_id
                and meta.get('session_id', session_id) == session_id and meta.get('cwd') == cwd,
                'unsupported Codex version or session/cwd mismatch')
        starts, completes, contexts, users, finals = [], [], [], [], []
        allowed = {'session_meta', 'event_msg', 'response_item', 'world_state', 'turn_context', 'token_usage_record'}
        for i, r in enumerate(records):
            require(r.get('type') in allowed and type(r.get('ordinal')) is int and r['ordinal'] == i,
                    'unsupported Codex record or missing/noncontiguous ordinal')
            q = r.get('payload')
            require(isinstance(q, dict), 'invalid Codex payload')
            require(i == 0 or r['type'] != 'session_meta', 'multiple Codex sessions')
            if r['type'] == 'event_msg':
                require(q.get('type') in ('task_started', 'task_complete', 'item_completed', 'token_count'),
                        'unsupported Codex event')
                if q['type'] == 'task_started': starts.append(i)
                if q['type'] == 'task_complete': completes.append(i)
            if r['type'] == 'turn_context': contexts.append(i)
            if r['type'] == 'response_item':
                require(q.get('type') in ('message', 'reasoning', 'custom_tool_call', 'custom_tool_call_output'),
                        'unsupported Codex response item')
                if q['type'] == 'message':
                    require(q.get('role') in ('developer', 'user', 'assistant'), 'unknown Codex message role')
                    if q['role'] == 'user': users.append(i)
                    if q['role'] == 'assistant':
                        require(q.get('phase') in ('commentary', 'final_answer'), 'unknown assistant phase')
                        if q['phase'] == 'final_answer': finals.append(i)
        require(len(starts) == len(completes) == len(contexts) == len(finals) == 1
                and completes[0] == len(records) - 1, 'ambiguous/incomplete Codex single turn')
        start, end, context, final = starts[0], completes[0], contexts[0], finals[0]
        turn = records[start]['payload'].get('turn_id')
        require(isinstance(turn, str) and turn and start == 1, 'missing Codex turn start')
        # The verified environment bootstrap is a distinct three-block input,
        # before turn_context. It is never treated as a later user prompt.
        require(len(users) in (1, 2), 'new or ambiguous Codex user turn')
        prompt_index = users[-1]
        if len(users) == 2:
            boot = records[users[0]]['payload'].get('content')
            require(start < users[0] < context and isinstance(boot, list) and len(boot) == 3,
                    'unknown Codex bootstrap')
            for block, prefix in zip(boot, ('<recommended_plugins>\n', '# AGENTS.md instructions for ', '<environment_context>\n')):
                require(isinstance(block, dict) and block.get('type') == 'input_text'
                        and isinstance(block.get('text'), str) and block['text'].startswith(prefix),
                        'unknown Codex bootstrap block')
        require(start < context < prompt_index < final < end
                and records[context]['payload'].get('cwd') == cwd, 'Codex prompt/final ordering or cwd mismatch')
        require(_native_text(records[prompt_index]['payload'].get('content'), 'input_text') == prompt,
                'frozen creation prompt mismatch')
        message = records[final]['payload']
        text = _native_text(message.get('content'), 'output_text')
        require(isinstance(message.get('id'), str) and message['id'], 'missing Codex final message ID')
        require(message.get('internal_chat_message_metadata_passthrough', {}).get('turn_id') == turn
                and records[end]['payload'].get('turn_id') == turn
                and records[end]['payload'].get('last_agent_message') == text,
                'Codex final/task_complete mismatch')
        for i, r in enumerate(records):
            q = r['payload']
            scopes = [q, q.get('internal_chat_message_metadata_passthrough', {})]
            for scope in scopes:
                require(isinstance(scope, dict), 'invalid Codex turn metadata')
                for key in ('turn_id', 'root_turn_id'):
                    if key in scope: require(scope[key] == turn, 'multiple Codex turns')
                for key in ('thread_id', 'session_id'):
                    if key in scope: require(scope[key] == session_id, 'conflicting native session')
            if i > final and i != end:
                require(r['type'] == 'token_usage_record' or
                        (r['type'] == 'event_msg' and q.get('type') == 'token_count'),
                        'new output after Codex final')
            if r['type'] == 'response_item' and q.get('role') == 'assistant':
                require(i > prompt_index, 'assistant before frozen prompt')
        proof = dict(turn_id=turn, message_id=message['id'], prompt_line=prompt_index + 1,
                     final_line=final + 1, complete_line=end + 1)
    elif provider == 'claude':
        version = '2.1.259'
        nodes, users, ends = {}, [], []
        allowed = {'queue-operation', 'file-history-snapshot', 'user', 'assistant', 'attachment',
                   'atis-latch', 'last-prompt', 'ai-title'}
        for i, r in enumerate(records):
            require(r.get('type') in allowed, 'unsupported Claude record')
            if 'sessionId' in r: require(r['sessionId'] == session_id, 'Claude session mismatch')
            if 'cwd' in r: require(r['cwd'] == cwd, 'Claude cwd mismatch')
            if 'version' in r: require(r['version'] == version, 'unsupported Claude version')
            if r['type'] in ('user', 'assistant', 'attachment'):
                require(r.get('sessionId') == session_id and r.get('cwd') == cwd
                        and r.get('version') == version and r.get('isSidechain') is False,
                        'incomplete Claude node identity')
                uid = r.get('uuid')
                require(isinstance(uid, str) and uid and uid not in nodes and 'parentUuid' in r,
                        'duplicate/missing Claude UUID')
                require(r['parentUuid'] is None or r['parentUuid'] in nodes, 'broken Claude parent chain')
                nodes[uid] = (i, r)
            if r['type'] in ('user', 'assistant'):
                m = r.get('message')
                require(isinstance(m, dict) and m.get('role') == r['type']
                        and isinstance(m.get('content'), list) and m['content']
                        and all(isinstance(c, dict) for c in m['content']), 'invalid Claude message')
                if r['type'] == 'user':
                    if all(c.get('type') == 'tool_result' for c in m['content']):
                        require(r['parentUuid'] is not None, 'tool result without parent')
                    else:
                        require(_native_text(m['content'], 'text') == prompt, 'new user turn or prompt mismatch')
                        users.append(i)
                else:
                    require(m.get('stop_reason') in ('tool_use', 'end_turn')
                            and all(c.get('type') in ('thinking', 'text', 'tool_use') for c in m['content']),
                            'unsupported Claude assistant block/stop reason')
                    if m['stop_reason'] == 'end_turn': ends.append(i)
        require(len(users) == 1 and ends, 'missing/ambiguous Claude initial prompt or end_turn')
        prompt_index = users[0]
        require(records[prompt_index]['parentUuid'] is None
                and all(i >= prompt_index for i, r in nodes.values())
                and sum(r['parentUuid'] is None for i, r in nodes.values()) == 1, 'ambiguous Claude root')
        tail_index = len(records) - 1
        if records[tail_index]['type'] == 'atis-latch':
            latch = records[tail_index]
            require(set(latch) == {'type', 'atis', 'sessionId'}
                    and isinstance(latch['atis'], str)
                    and latch['sessionId'] == session_id, 'invalid Claude atis-latch')
            tail_index -= 1
        title_present = records[tail_index]['type'] == 'ai-title'
        if natural_success and title_present:
            title = records[tail_index]
            require(set(title) == {'type', 'aiTitle', 'sessionId'}
                    and isinstance(title['aiTitle'], str) and bool(title['aiTitle'])
                    and title['sessionId'] == session_id, 'invalid Claude ai-title')
            tail_index -= 1
        tail = records[tail_index]
        last_prompt = tail.get('type') == 'last-prompt'
        if last_prompt:
            require(tail.get('sessionId') == session_id and tail.get('leafUuid') in nodes,
                    'missing Claude final leaf')
            leaf = tail['leafUuid']
            final, message_record = nodes[leaf]
            require(final == tail_index - 1, 'Claude leaf is not terminal assistant')
        else:
            require(natural_success is True and not title_present, 'missing Claude final leaf')
            final, message_record = tail_index, tail
            leaf = message_record.get('uuid')
        require(message_record['type'] == 'assistant', 'Claude leaf is not terminal assistant')
        # Claude also writes these metadata records during tool execution.
        # They are not completion markers; keep the entire observed history.
        for i, record in enumerate(records[:final]):
            if record['type'] == 'last-prompt':
                require(record.get('leafUuid') in nodes and nodes[record['leafUuid']][0] < i,
                        'invalid historical Claude leaf')
            elif record['type'] == 'ai-title':
                require(set(record) == {'type', 'aiTitle', 'sessionId'}
                        and isinstance(record['aiTitle'], str) and bool(record['aiTitle'])
                        and record['sessionId'] == session_id, 'invalid historical Claude ai-title')
        message = message_record['message']
        require(message.get('stop_reason') == 'end_turn', 'Claude leaf is not end_turn')
        text = _native_text(message['content'], 'text')
        require(isinstance(message.get('id'), str) and message['id'], 'missing Claude message ID')
        # end_turn also labels the thinking block; only one text block is proven.
        require(ends in ([final], [final - 1, final]), 'ambiguous Claude final blocks')
        if len(ends) == 2:
            prev = records[final - 1]
            require(prev['uuid'] == message_record['parentUuid']
                    and prev['message'].get('id') == message['id']
                    and prev.get('requestId') == message_record.get('requestId')
                    and prev.get('apiBlockIndex') == 0 and message_record.get('apiBlockIndex') == 1
                    and len(prev['message']['content']) == 1
                    and prev['message']['content'][0].get('type') == 'thinking', 'ambiguous Claude thinking/text boundary')
        else:
            require(message_record.get('apiBlockIndex') == 0, 'missing Claude final block')
        require(all(r['message'].get('id') != message['id'] for r in records[:ends[0]] if r['type'] == 'assistant'),
                'split/ambiguous Claude final message')
        chain, uid = set(), leaf
        while uid is not None:  # parent points strictly backward, at most len(nodes)
            require(uid not in chain, 'cyclic Claude parent chain')
            chain.add(uid)
            uid = nodes[uid][1]['parentUuid']
        require(records[prompt_index]['uuid'] in chain
                and all(uid in chain or (r['type'] == 'user'
                        and r['parentUuid'] in chain
                        and all(c.get('type') == 'tool_result' for c in r['message']['content']))
                        for uid, (i, r) in nodes.items()), 'ambiguous Claude branch')
        proof = dict(message_id=message['id'], message_uuid=message_record['uuid'],
                     parent_uuid=message_record['parentUuid'], leaf_uuid=leaf,
                     prompt_line=prompt_index + 1, final_line=final + 1, complete_line=len(records),
                     completion_basis='natural_success' if natural_success else 'last-prompt',
                     last_prompt_present=last_prompt, ai_title_present=title_present)
    else:
        raise LifecycleError('unsupported native provider')
    try:
        raw = text.encode('utf-8', errors='strict')
        prompt_sha = digest(prompt.encode('utf-8', errors='strict'))
    except UnicodeError:
        raise LifecycleError('native text is not valid UTF-8') from None
    return raw, dict(schema_version=1, provider=provider, version=version, session_id=session_id,
                     cwd=cwd, prompt_sha256=prompt_sha, source_sha256=digest(data),
                     source_bytes=len(data), source_lines=len(records), raw_sha256=digest(raw),
                     raw_bytes=len(raw), **proof)


def parse_native_final(data, *, provider, session_id, cwd, prompt, natural_success=False):
    """Pure parse interface; malformed unsupported shapes fail without text leaks."""
    try:
        return _parse_native_final(data, provider=provider, session_id=session_id, cwd=cwd, prompt=prompt,
                                   natural_success=natural_success)
    except (KeyError, TypeError, AttributeError, IndexError, RecursionError):
        raise LifecycleError('unsupported/malformed native structure') from None


def _grok_jsonl(data, label):
    require(data and len(data) <= NATIVE_MAX_BYTES and data.endswith(b'\n'),
            f'incomplete or oversized Grok {label}')
    lines = data.split(b'\n')[:-1]
    require(1 <= len(lines) <= NATIVE_MAX_LINES and all(lines), f'invalid Grok {label} line count')
    try:
        records = [json.loads(line.decode('utf-8'), object_pairs_hook=contextual._reject_duplicate)
                   for line in lines]
    except (ValueError, UnicodeError, RecursionError, contextual.ContractError):
        raise LifecycleError(f'invalid Grok {label} JSONL') from None
    require(all(isinstance(r, dict) for r in records), f'invalid Grok {label} record')
    return records


def _parse_grok_native_final(sources, *, session_id, cwd, prompt, natural_success=False):
    """Bind the three observed Grok sources before selecting any assistant text."""
    require(type(natural_success) is bool and natural_success, 'Grok needs natural completion')
    require(all(isinstance(v, str) and v for v in (session_id, cwd, prompt)), 'native binding missing')
    require(set(sources) == {'summary.json', 'events.jsonl', 'chat_history.jsonl'},
            'missing Grok source')
    require(all(isinstance(v, bytes) and 0 < len(v) <= NATIVE_MAX_BYTES for v in sources.values())
            and sum(map(len, sources.values())) <= NATIVE_MAX_BYTES, 'Grok native byte limit')
    try:
        summary = json.loads(sources['summary.json'].decode('utf-8'),
                             object_pairs_hook=contextual._reject_duplicate)
    except (ValueError, UnicodeError, RecursionError, contextual.ContractError):
        raise LifecycleError('invalid Grok summary JSON') from None
    require(isinstance(summary, dict) and isinstance(summary.get('info'), dict), 'invalid Grok summary shape')
    info = summary['info']
    model = summary.get('current_model_id')
    require(info.get('id') == session_id and info.get('cwd') == cwd
            and isinstance(model, str) and model, 'Grok summary identity/cwd/model mismatch')
    events = _grok_jsonl(sources['events.jsonl'], 'events')
    chat = _grok_jsonl(sources['chat_history.jsonl'], 'chat history')
    summary_lines = sources['summary.json'].count(b'\n') + 1
    require(summary_lines + len(events) + len(chat) <= NATIVE_MAX_LINES,
            'Grok native line limit')
    starts = []
    event_types = {'mcp_config_resolved', 'mcp_server_starting', 'turn_started',
                   'mcp_server_connected', 'mcp_init_completed', 'loop_started',
                   'phase_changed', 'first_token', 'tool_started', 'tool_completed',
                   'permission_requested', 'permission_resolved', 'turn_ended'}
    mcp_bootstrap = {'mcp_config_resolved', 'mcp_server_starting',
                     'mcp_server_connected', 'mcp_init_completed'}
    for i, event in enumerate(events):
        kind = event.get('type')
        require(isinstance(kind, str) and kind in event_types,
                'unknown Grok event type/shape')
        if 'session_id' in event:
            require(event['session_id'] == session_id, 'Grok event session mismatch')
        if 'cwd' in event:
            require(event['cwd'] == cwd, 'Grok event cwd mismatch')
        if kind == 'turn_started':
            require(event.get('session_id') == session_id and type(event.get('turn_number')) is int
                    and event['turn_number'] == 0 and event.get('model_id') == model,
                    'Grok turn start identity/model mismatch')
            starts.append(i)
        elif kind == 'turn_ended':
            require(event.get('outcome') in ('completed', 'failed', 'cancelled', 'error'),
                    'unknown Grok turn outcome')
    require(len(starts) == 1 and starts[0] > 0
            and all(e.get('type') in mcp_bootstrap for e in events[:starts[0]]),
            'ambiguous Grok turn start or non-bootstrap prefix')
    require(events[-1].get('type') == 'turn_ended' and events[-1].get('outcome') == 'completed'
            and sum(e.get('type') == 'turn_ended' for e in events) == 1,
            'Grok final completion missing or ambiguous')
    users, assistants = [], []
    for i, record in enumerate(chat):
        kind = record.get('type')
        require(kind in {'system', 'user', 'reasoning', 'assistant', 'tool_result'},
                'unknown Grok chat type/shape')
        if kind == 'reasoning':
            require('content' not in record and isinstance(record.get('summary'), list),
                    'invalid Grok reasoning shape')
            for item in record['summary']:
                require(isinstance(item, dict), 'invalid Grok reasoning summary')
        elif kind == 'user':
            content = record.get('content')
            require(isinstance(content, list) and content
                    and all(isinstance(block, dict) and block.get('type') == 'text'
                            and isinstance(block.get('text'), str) for block in content),
                    'Grok user content requires text blocks')
            for block in content:
                try:
                    block['text'].encode('utf-8', errors='strict')
                except UnicodeError:
                    raise LifecycleError('Grok chat content is not valid UTF-8') from None
        else:
            require(isinstance(record.get('content'), str), 'invalid Grok chat content')
            try:
                record['content'].encode('utf-8', errors='strict')
            except UnicodeError:
                raise LifecycleError('Grok chat content is not valid UTF-8') from None
        if 'session_id' in record:
            require(record['session_id'] == session_id, 'Grok chat session mismatch')
        if 'cwd' in record:
            require(record['cwd'] == cwd, 'Grok chat cwd mismatch')
        if kind == 'user':
            users.append(i)
        elif kind == 'assistant':
            assistants.append(i)
    require(users and assistants and max(users) < min(assistants),
            'missing/ambiguous Grok prompt or assistant ordering')
    user_texts = [(i, ''.join(block['text'] for block in chat[i]['content'])) for i in users]
    query_records = [(i, text) for i, text in user_texts if text.count('<user_query>')
                     == text.count('</user_query>') == 1]
    info_records = [(i, text) for i, text in user_texts if text.count('<user_info>')
                    == text.count('</user_info>') == 1 and 'Workspace Path:' in text]
    require(sum(text.count('<user_query>') for _, text in user_texts)
            == sum(text.count('</user_query>') for _, text in user_texts) == 1
            and sum(text.count('<user_info>') for _, text in user_texts)
            == sum(text.count('</user_info>') for _, text in user_texts) == 1
            and len(query_records) == 1 and len(info_records) == 1,
            'unknown Grok prompt wrapper')
    query_line, query_record = query_records[0]
    info_line, info_record = info_records[0]
    require(query_line < min(assistants) and info_line < min(assistants),
            'Grok prompt context must precede assistants')
    query = query_record.split('<user_query>', 1)[1].split('</user_query>', 1)[0]
    # One newline on either side belongs to the XML-style host wrapper.
    if query.startswith('\n') and query.endswith('\n'):
        query = query[1:-1]
    user_info = info_record.split('<user_info>', 1)[1].split('</user_info>', 1)[0]
    paths = re.findall(r'(?m)^Workspace Path: ([^\r\n]+)$', user_info)
    require(query == prompt and paths == [cwd], 'Grok frozen prompt/cwd mismatch')
    final = assistants[-1]
    require(bool(chat[final]['content']), 'zero Grok final assistant text record')
    text = chat[final]['content']
    try:
        raw = text.encode('utf-8', errors='strict')
        prompt_sha = digest(prompt.encode('utf-8', errors='strict'))
    except UnicodeError:
        raise LifecycleError('Grok text is not valid UTF-8') from None
    file_shas = {name: digest(data) for name, data in sources.items()}
    return raw, dict(schema_version=1, provider='grok', version=model, session_id=session_id,
                     cwd=cwd, prompt_sha256=prompt_sha, source_file_sha256=file_shas,
                     source_sha256=digest(surface.canonical_bytes(file_shas)),
                     source_bytes=sum(map(len, sources.values())), source_lines=summary_lines + len(events) + len(chat),
                     raw_sha256=digest(raw), raw_bytes=len(raw),
                     prompt_line=query_line + 1, info_line=info_line + 1,
                     final_line=final + 1, complete_line=len(events))


def _read_grok_native_final(path, **binding):
    path = Path(path).absolute()
    session_id, cwd = binding.get('session_id'), binding.get('cwd')
    require(isinstance(session_id, str) and session_id and isinstance(cwd, str) and cwd,
            'missing Grok directory binding')
    before = path.lstat()
    require(stat.S_ISDIR(before.st_mode) and path.name == session_id
            and path.parent.name == quote(cwd, safe='') and path.parent.parent.name == 'sessions',
            'Grok session directory identity/cwd mismatch')
    sessions = path.parent.parent
    require(stat.S_ISDIR(sessions.lstat().st_mode) and stat.S_ISDIR(path.parent.lstat().st_mode),
            'Grok session parent must be an ordinary directory')
    matches = [p for p in sessions.iterdir() if p.is_dir() and (p / session_id).exists()]
    require(len(matches) == 1 and matches[0] == path.parent, 'missing/duplicate Grok session directory')
    def signature(s):
        return (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    sources, signatures = {}, {}
    for name in ('summary.json', 'events.jsonl', 'chat_history.jsonl'):
        source = path / name
        old = source.lstat()
        require(stat.S_ISREG(old.st_mode) and 0 < old.st_size <= NATIVE_MAX_BYTES,
                f'missing/oversized Grok {name}')
        fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, 'rb') as stream:
            require(signature(os.fstat(stream.fileno())) == signature(old), 'Grok file changed before read')
            data = stream.read(NATIVE_MAX_BYTES + 1)
            require(len(data) == old.st_size, 'incomplete/changed Grok read')
            stream.seek(0)
            require(stream.read(NATIVE_MAX_BYTES + 1) == data
                    and signature(os.fstat(stream.fileno())) == signature(old)
                    and signature(source.lstat()) == signature(old), 'Grok file changed during read')
        sources[name] = data
        signatures[name] = signature(old)
    require(signature(path.lstat()) == signature(before), 'Grok session directory changed during read')
    try:
        raw, proof = _parse_grok_native_final(sources, **{k: v for k, v in binding.items() if k != 'provider'})
    except (KeyError, TypeError, AttributeError, IndexError, RecursionError):
        raise LifecycleError('unsupported/malformed Grok structure') from None
    require(signature(path.lstat()) == signature(before)
            and all(signature((path / name).lstat()) == old for name, old in signatures.items()),
            'Grok source changed during parse')
    return raw, dict(proof, source_path=str(path), source_file_paths={name: str(path / name) for name in sources})


def read_native_final(path, **binding):
    """Read only one explicit ordinary file; reject replacement/growth/partial IO."""
    if binding.get('provider') == 'grok':
        return _read_grok_native_final(path, **binding)
    path = Path(path).absolute()
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), 'native log must be an ordinary file')
    def signature(s):
        return (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        require(signature(opened) == signature(before) and 0 < opened.st_size <= NATIVE_MAX_BYTES,
                'native file changed or exceeds byte limit')
        data = stream.read(NATIVE_MAX_BYTES + 1)
        require(len(data) == opened.st_size, 'incomplete/changed native read')
        raw, proof = parse_native_final(data, **binding)
        stream.seek(0)
        require(stream.read(NATIVE_MAX_BYTES + 1) == data, 'native bytes changed during read')
        require(signature(os.fstat(stream.fileno())) == signature(before)
                and signature(path.lstat()) == signature(before), 'native file changed during read')
    return raw, dict(proof, source_path=str(path))


def export_native_final(journal, key, capture, native_log, outdir, *, notified):
    """Notified, pre-archive export; errors are recoverable and never verdicts."""
    row = journal.get(key)
    folder = Path(outdir) / row['task_id'] / row['dispatch_id']
    try:
        require(notified is True and row.get('agent_id') and row.get('lineage_verified') is True
                and 'runtime_observation' in row, 'notification and registered live-bound direct child required')
        require(not row.get('archive_confirmed') and row.get('archive_attempts_started') == 0,
                'native export must precede archive; use pure parser for historical audit')
        require(row['cwd'] == str(journal.root) and row['role'] == 'REVIEWER'
                and row['purpose'] in (SURFACE, CONTEXTUAL), 'native root/role/purpose mismatch')
        for name, value in dict(task_id=row['task_id'], dispatch_id=row['dispatch_id'], role='reviewer',
                                purpose=row['purpose'], **{'paseo.parent-agent-id': row['parent_agent_id']}).items():
            require(row['labels'].get(name) == value, 'journal label binding mismatch')
        state = read(journal.root / '.ai/task' / row['task_id'] / 'STATE.json')
        require(state.get('task_id') == row['task_id'] and state.get('workspace_id') == row['workspace_id']
                and state.get('orchestrator_agent_id') == row['parent_agent_id']
                and state.get('state') not in ('DONE', 'STOP') and state.get('mode') == 'review_only'
                and state.get('orchestration_transport') == row['creation_transport'], 'native STATE/root binding mismatch')
        children = [c for c in state.get('child_dispatches', []) if c.get('dispatch_id') == row['dispatch_id']]
        require(len(children) == 1 and all(children[0].get(k) == row.get(k) for k in
                ('agent_id', 'role', 'purpose', 'workspace_id', 'parent_agent_id', 'labels',
                 'candidate_identity', 'input_path', 'runtime_observation', 'lineage_verified')),
                'native source needs immutable registered STATE child')
        validate_input(journal.root, row)
        s = snapshot(capture, row)
        terminal(s)
        require(s['status'] == 'idle' and s['attentionReason'] == 'finished', 'native source needs successful natural completion')
        provider, session = native_identity(s)
        first = snapshot(row['first_live_capture'], row)
        first_provider, first_session = native_identity(first, required=False)
        require(provider == first_provider and first_session in (None, session), 'immutable live native identity changed')
        require(row['runtime_observation']['provider'] == dict(presence='present', value=provider),
                'first runtime provider mismatch')
        for snap in (first, s):
            if 'parentAgentId' in snap:
                require(snap['parentAgentId'] == row['parent_agent_id'], 'conflicting direct parent')
        prompt = row['create_parameters']['prompt']
        require(isinstance(prompt, str) and row.get('create_prompt_sha256') == digest(prompt.encode('utf-8')),
                'missing/changed frozen creation prompt')
        if row.get('native_provenance'):
            require(row['native_provenance']['terminal_capture_sha256'] == digest(surface.canonical_bytes(capture)),
                    'frozen native terminal capture changed')
            proof = row['native_provenance']
            raw = Path(row['native_raw_path']).read_bytes()
            require(digest(raw) == proof['raw_sha256'], 'frozen native raw changed')
            require(read(Path(row['native_raw_path']).parent / 'provenance.json') == proof, 'frozen native proof changed')
            immutable(folder / 'provenance.json', surface.canonical_bytes(proof))
            immutable(folder / 'terminal.raw', raw)
            return raw
        row.update(terminal_capture=deepcopy(capture), terminal_observed_at=now(), lifecycle='terminal')
        with journal.timed(row, 'tool_call', 'native_read'):
            raw, proof = read_native_final(native_log, provider=provider, session_id=session, cwd=row['cwd'],
                                           prompt=prompt, natural_success=True)
        proof.update(key=key, agent_id=row['agent_id'], workspace_id=row['workspace_id'],
                     parent_agent_id=row['parent_agent_id'], labels=deepcopy(row['labels']),
                     input_sha256=row['input_sha256'],
                     terminal_capture_sha256=digest(surface.canonical_bytes(capture)),
                     first_live_capture_sha256=digest(surface.canonical_bytes(row['first_live_capture'])))
        old = row.get('native_provenance')
        require(old is None or old == proof, 'native provenance changed')
        immutable(folder / 'provenance.json', surface.canonical_bytes(proof))
        immutable(folder / 'terminal.raw', raw)
        row.update(native_provenance=proof, native_raw_path=str((folder / 'terminal.raw').absolute()),
                   terminal_capture=deepcopy(capture), terminal_observed_at=now(), lifecycle='terminal')
        journal.save()
        return raw
    except (ValueError, OSError, KeyError, TypeError, contextual.ContractError, contextual.InputError,
            surface.ContractError, surface.InputError) as error:
        # No native record text/prompt/thinking copied into diagnostics.
        errors = row.setdefault('terminal_fetch_errors', [])
        diagnostic = dict(source='native_log', source_path=str(Path(native_log).absolute()), at=now(), error=str(error))
        immutable(folder / f'error-{len(errors) + 1}.json', surface.canonical_bytes(diagnostic))
        errors.append(diagnostic)
        journal.save()
        raise


def mcp_payload(response, kind):
    """Only observed Paseo CallToolResult dialects; never guess nested SDK data.

    One text block duplicates structuredContent as JSON, optionally prefixed by
    the observed count/IDs display. Both copies must agree. A prose-only block
    is not a proven dialect and fails closed (the create display contains JSON).
    """
    require(isinstance(response, dict) and set(response) <= {'content', 'structuredContent', 'isError', '_meta'},
            'unsupported MCP envelope')
    require(response.get('isError', False) is False, 'MCP isError')
    content = response.get('content')
    require(isinstance(content, list) and len(content) == 1, 'multiple/missing MCP payloads')
    block = content[0]
    require(isinstance(block, dict) and set(block) == {'type', 'text'}
            and block['type'] == 'text' and isinstance(block['text'], str), 'unsupported MCP content')
    display = block['text']
    prefix = None
    if kind in ('create', 'profiles'):
        name = 'availableModes' if kind == 'create' else 'profiles'
        prefix = re.match(rf'{name}_count=(0|[1-9][0-9]*)\n{name}_ids=([^\n]*)\n\n', display)
        if prefix:
            display = display[prefix.end():]
    try:
        payload = json.loads(display, object_pairs_hook=contextual._reject_duplicate)
    except (ValueError, contextual.ContractError):
        raise LifecycleError('unsupported MCP text payload') from None
    require(isinstance(payload, dict), 'MCP payload must be object')
    if 'structuredContent' in response:
        require(surface.canonical_bytes(response['structuredContent']) == surface.canonical_bytes(payload),
                'conflicting MCP payloads')
    # Prefixed text has only been observed paired with structuredContent.
    require(prefix is None or 'structuredContent' in response, 'unproven MCP prefixed text-only shape')
    if kind == 'create':
        require(set(payload) == {'agentId', 'type', 'status', 'cwd', 'workspaceId', 'currentModeId',
                                'availableModes', 'lastMessage', 'permission', 'guidance'}, 'unknown create payload')
        items = payload['availableModes']
    elif kind == 'profiles':
        require(set(payload) == {'profiles'}, 'unknown profiles payload')
        items = payload['profiles']
    elif kind == 'status':
        require(set(payload) == {'status', 'snapshot'} and isinstance(payload['snapshot'], dict),
                'unknown status payload')
    elif kind == 'archive':
        require(set(payload) == {'success'} and payload['success'] is True, 'archive response unsuccessful')
    else:
        raise LifecycleError('unknown MCP operation')
    if kind in ('profiles', 'create'):
        require(isinstance(items, list) and all(isinstance(x, dict) and isinstance(x.get('id'), str)
                                              and x['id'] for x in items), 'invalid MCP items')
        ids = [x['id'] for x in items]
        require(len(ids) == len(set(ids)), 'duplicate MCP item ID')
        if prefix:
            require(int(prefix[1]) == len(items) and prefix[2] == ','.join(ids), 'MCP display/payload mismatch')
    return payload


def mcp_create_parameters(row, profiles, profile_id):
    matches = [p for p in profiles['profiles'] if p['id'] == profile_id]
    require(len(matches) == 1, 'profile selection missing/ambiguous')
    profile, frozen = matches[0], row['create_parameters']
    require(all(isinstance(profile.get(k), str) and profile[k] for k in ('provider', 'model')),
            'profile needs explicit provider/model')
    provider = profile['provider'] + '/' + profile['model']
    require(frozen['provider'] == provider, 'profile provider/model drift')
    settings = {}
    for source, target in (('modeId', 'modeId'), ('thinkingOptionId', 'thinkingOptionId'), ('featureValues', 'features')):
        for declared in (profile, frozen):
            if source in declared:
                value = declared[source]
                require(isinstance(value, dict) if source == 'featureValues' else isinstance(value, str) and bool(value),
                        f'invalid profile setting: {source}')
        require(source not in frozen or source not in profile
                or surface.canonical_bytes(frozen[source]) == surface.canonical_bytes(profile[source]),
                f'profile setting drift: {source}')
        if source in profile or source in frozen:
            settings[target] = deepcopy(profile[source] if source in profile else frozen[source])
    return dict(provider=provider, initialPrompt=frozen['prompt'], title=row['dispatch_id'],
                workspaceId=row['workspace_id'], labels=deepcopy(row['labels']), notifyOnFinish=True, settings=settings)


def host_event(journal, key, data, *, outdir, native_log=None):
    """One stdin event, one writer, no injected tools or scheduler inside Python."""
    row = journal.get(key)
    folder = Path(outdir) / row['task_id'] / row['dispatch_id'] / 'wire'
    require(isinstance(data, bytes) and 0 < len(data) <= NATIVE_MAX_BYTES, 'host event byte limit')
    # Save the entire shell-delivered envelope, even if validation rejects it.
    path = folder / (digest(data) + '.json')
    immutable(path, data)
    event = json.loads(data, object_pairs_hook=contextual._reject_duplicate)
    require(isinstance(event, dict) and set(event) <= {'op', 'response', 'profile_id', 'notified', 'notification_received_at', 'started_at', 'ended_at', 'operation'},
            'unknown host event fields')
    op = event.get('op')
    require(op in ('recover', 'profiles', 'create', 'bind', 'harvest', 'archive-intent', 'archive-response', 'archive-confirm', 'call-failed'),
            'unknown host operation')
    fields = {'op'} if op == 'recover' else {'op', 'started_at', 'ended_at', 'response'}
    if op == 'profiles': fields.add('profile_id')
    if op == 'harvest': fields.update(('notified', 'notification_received_at'))
    if op == 'call-failed': fields = {'op', 'operation', 'started_at', 'ended_at'}
    require(set(event) <= fields, 'host fields disagree with operation')
    journal.save()  # repair STATE before any subsequent external operation
    result = {}
    if op != 'recover':
        kind = {'profiles': 'profiles', 'create': 'create', 'archive-response': 'archive'}.get(op, 'status')
        if 'started_at' in event or 'ended_at' in event:
            require(timestamp(event['ended_at']) >= timestamp(event['started_at']), 'invalid host tool interval')
            timing = dict(category='tool_call', operation=op, started_at=event['started_at'], ended_at=event['ended_at'],
                          wire_sha256=digest(data))
            if timing not in row.setdefault('timing', []):
                row['timing'].append(timing)
        row.setdefault('wire_events', []).append(dict(op=op, path=str(path), sha256=digest(data)))
        journal.save()
        payload = None if op == 'call-failed' else mcp_payload(event.get('response'), kind)
        if op == 'call-failed':
            require(event.get('operation') in ('profiles', 'create', 'bind', 'harvest', 'archive-intent',
                                              'archive-response', 'archive-confirm') and 'response' not in event,
                    'invalid failed-call event')
        elif op == 'profiles':
            require(row['creation_transport'] == 'mcp', 'host recipe requires MCP creation')
            require(sum(not journal.settled(r) for r in journal.rows) < 3, 'capacity=3 exhausted')
            parameters = mcp_create_parameters(row, payload, event.get('profile_id'))
            journal.create_intent(key, path)
            row['create_attempts'][-1]['mcp_parameters'] = deepcopy(parameters)
            result['parameters'] = parameters
        elif op == 'create':
            require(payload['cwd'] == row['cwd'] and payload['workspaceId'] == row['workspace_id']
                    and payload['type'] == row['create_parameters']['provider'].split('/', 1)[0], 'create identity mismatch')
            journal.record_id(key, payload['agentId'])
        elif op == 'bind':
            journal.bind(key, payload)
        elif op == 'harvest':
            require(event.get('notified') is True, 'notification required')
            require(native_log, 'explicit native log required')
            received = event.get('notification_received_at')
            if received is not None:
                timestamp(received)
                row.setdefault('notification_received_at', received)
            raw = export_native_final(journal, key, payload, native_log, Path(outdir) / 'native', notified=True)
            result['output_valid'] = journal.harvest(key, payload, raw, Path(outdir) / 'raw', notified=True)
        elif op == 'archive-intent':
            result['archive'] = journal.archive_intent(key, payload)
        elif op == 'archive-response':
            require(row['archive_attempts_started'] > 0 and not row['archive_confirmed'], 'archive response without intent')
            # Success is not confirmation. Only independent status can release capacity.
        else:
            journal.confirm_archive(key, payload)
        journal.save()
    return dict(result, rows=[dict(key=journal.key(r), agent_id=r.get('agent_id'), status=r['status'],
                archive_confirmed=r['archive_confirmed'], archive_attempts_started=r['archive_attempts_started'],
                validation_state=r.get('validation_state'), live_bound='runtime_observation' in r,
                create_blocked=journal.create_blocked(journal.key(r))) for r in journal.rows])


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['create-intent', 'reconcile-absent', 'bind', 'harvest', 'reject', 'archive-intent', 'archive-confirm', 'native-export', 'timing', 'host-event'])
    p.add_argument('children')
    p.add_argument('key', nargs='?')
    p.add_argument('--capture')
    p.add_argument('--profiles')
    p.add_argument('--raw')
    p.add_argument('--native-log', help='explicit ordinary provider-native JSONL file')
    p.add_argument('--outdir')
    p.add_argument('--notified', action='store_true')
    p.add_argument('--reason')
    p.add_argument('--evidence')
    a = p.parse_args(argv)
    j = Journal(a.children)
    if a.action == 'timing':
        print(json.dumps(j.timing_report(), ensure_ascii=False, indent=2))
        return 0
    require(a.key, 'task_id|dispatch_id required')
    if a.action == 'host-event':
        require(a.outdir, '--outdir required')
        print(json.dumps(host_event(j, a.key, sys.stdin.buffer.read(NATIVE_MAX_BYTES + 1),
                                    outdir=a.outdir, native_log=a.native_log), ensure_ascii=False))
    elif a.action == 'create-intent':
        require(a.profiles, '--profiles required (fresh list_profiles response)')
        require(j.get(a.key)['creation_transport'] == 'mcp', 'CLI creation must use dispatch entrypoint')
        print(json.dumps(j.create_intent(a.key, a.profiles), ensure_ascii=False))
    elif a.action == 'native-export':
        require(a.outdir and a.capture and a.native_log, '--outdir, --capture and --native-log required')
        export_native_final(j, a.key, read(a.capture), a.native_log, a.outdir, notified=a.notified)
    elif a.action == 'reconcile-absent':
        require(a.evidence, '--evidence complete reconciliation audit required')
        j.reconcile_absent(a.key, a.evidence)
    elif a.action == 'reject':
        require(a.reason and a.evidence, '--reason and --evidence required')
        j.reject(a.key, a.reason, a.evidence, capture=read(a.capture) if a.capture else None,
                 notified=a.notified)
    else:
        require(a.capture, '--capture required')
        capture = read(a.capture)
        if a.action == 'bind':
            j.bind(a.key, capture)
        elif a.action == 'harvest':
            require(a.outdir and bool(a.raw) != bool(a.native_log), 'exactly one of --raw/--native-log and --outdir required')
            raw = (export_native_final(j, a.key, capture, a.native_log, Path(a.outdir) / 'native', notified=a.notified)
                   if a.native_log else Path(a.raw).read_bytes())
            return 0 if j.harvest(a.key, capture, raw, a.outdir, notified=a.notified) else 1
        elif a.action == 'archive-intent':
            # Exit 3 explicitly means already archived: do NOT call archive again.
            return 0 if j.archive_intent(a.key, capture) else 3
        else:
            j.confirm_archive(a.key, capture)
    return 0


def dispatch_main(kind, prompt_builder, provider, mode, argv=None):
    """Shared surface/contextual CLI; recipes are not advertised as MCP wire."""
    p = argparse.ArgumentParser()
    p.add_argument('plan')
    p.add_argument('children')
    p.add_argument('--emit')
    p.add_argument('--record')
    p.add_argument('--profiles', help='fresh host list_profiles capture for one CLI create')
    p.add_argument('--select-transport', choices=['cli', 'mcp'], help='explicit choice before first preparation')
    p.add_argument('--live', help='map task_id|dispatch_id to captured MCP status object')
    p.add_argument('--provider', default=provider)
    p.add_argument('--thinking', default='xhigh')
    p.add_argument('--mode', default=mode)
    a = p.parse_args(argv)
    try:
        j = Journal(a.children)
        if a.record or a.live:
            if a.record:
                for key, aid in read(a.record).items():
                    j.record_id(key, aid)
            if a.live:
                for key, capture in read(a.live).items():
                    j.bind(key, capture)
            pending = [j.key(r) for r in j.rows if r['status'] in ('dispatching', 'created')]
            require(not pending, f'first live metadata still required: {pending}')
            print('LIVE_BOUND')
            return
        require(a.emit or a.profiles, '--profiles required for CLI create; no agent created')
        plan = read(a.plan)
        specs = ([dict(lane, task_id=task) for task, v in sorted(plan.items()) for lane in v['lanes']]
                 if kind == 'surface' else plan)
        transport = 'mcp' if a.emit else 'cli'
        if a.select_transport:
            require(a.select_transport == transport, 'selected transport disagrees with creation path')
            j.select_transport({s['task_id'] for s in specs}, transport)
        recipes = j.prepare(specs, SURFACE if kind == 'surface' else CONTEXTUAL,
                            _orch.parent_agent_id(), _orch.workspace_id(), prompt_builder,
                            dict(provider=a.provider, thinkingOptionId=a.thinking, modeId=a.mode), transport=transport)
        if a.emit:
            _orch.write_json_atomic(a.emit, recipes)
            print(f'PREPARED {len(recipes)}; per-child create-intent + live binding required')
        else:
            require(recipes, 'no prepared member for CLI creation')
            key = recipes[0]['key']
            aid = j.create_cli(key, a.profiles)
            print(f'CREATED {key} {aid}; complete live binding required before next create')
    except (LifecycleError, OSError, ValueError, KeyError, contextual.ContractError,
            contextual.InputError, surface.ContractError, surface.InputError) as error:
        print(f'DISPATCH_FAILED: {error}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (LifecycleError, OSError, ValueError, KeyError, contextual.ContractError,
            contextual.InputError, surface.ContractError, surface.InputError) as error:
        print(f'LIFECYCLE_FAILED: {error}', file=sys.stderr)
        sys.exit(1)
