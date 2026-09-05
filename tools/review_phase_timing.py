#!/usr/bin/env python3
"""Offline orchestration wall timing; no production state or review semantics."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('source_verification', 'prepare_dispatch', 'wait_reviewers',
          'import_adjudication', 'gates', 'closure')
COUNTS = ('child_count', 'retry_count', 'actual_tokens')


def clock_sample():
    # Linux boot + time namespace identifies the cross-process monotonic domain.
    domain = (Path('/proc/sys/kernel/random/boot_id').read_text().strip()
              + ':' + os.readlink('/proc/self/ns/time') + ':CLOCK_BOOTTIME')
    return {'utc': datetime.now(timezone.utc).isoformat(),
            'monotonic_ns': time.clock_gettime_ns(time.CLOCK_BOOTTIME), 'clock_domain': domain}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def count(value):
    require(type(value) is int and value >= 0, 'count must be a nonnegative integer')


def validate(data):
    require(isinstance(data, dict) and set(data) == {'version', 'batch_id', 'base_commit',
            'selected', 'concurrency', 'events'}, 'invalid log fields')
    require(type(data['version']) is int and data['version'] == 1, 'invalid version')
    require(isinstance(data['batch_id'], str) and data['batch_id'].strip(), 'missing batch identity')
    require(isinstance(data['base_commit'], str) and
            re.fullmatch(r'[0-9a-f]{40}', data['base_commit']), 'base commit must be full Git SHA-1')
    count(data['selected'])
    require(1 <= data['selected'] <= 80, 'selected must be actual revision count in 1..80')
    if data['concurrency'] != 'unknown':
        count(data['concurrency'])
        require(data['concurrency'] > 0, 'concurrency must be positive')
    events = data['events']
    require(isinstance(events, list) and events, 'missing events')
    previous = None
    for index, event in enumerate(events):
        require(isinstance(event, dict), 'invalid event')
        kind = event.get('kind')
        require(kind in ('start', 'mark', 'finish'), 'invalid event kind')
        keys = {'kind', 'utc', 'monotonic_ns', 'clock_domain'}
        keys |= {'counts', 'incomplete_reason'} if kind == 'finish' else {'phase', 'missing_reason'}
        require(set(event) == keys, 'invalid event fields')
        require(isinstance(event['utc'], str), 'invalid UTC')
        utc = datetime.fromisoformat(event['utc'])
        require(utc.utcoffset() is not None and utc.utcoffset().total_seconds() == 0, 'timestamp must be UTC')
        count(event['monotonic_ns'])
        require(event['monotonic_ns'] <= 2**63 - 1, 'monotonic timestamp outside supported range')
        require(isinstance(event['clock_domain'], str) and event['clock_domain'], 'missing clock domain')
        require((index == 0) == (kind == 'start'), 'start must occur exactly once, first')
        if previous:
            require(previous['kind'] != 'finish', 'event after finish')
            require(event['clock_domain'] == previous['clock_domain'], 'monotonic clock domain changed')
            require(event['monotonic_ns'] >= previous['monotonic_ns'], 'monotonic clock went backwards')
        if kind == 'finish':
            require(isinstance(event['counts'], dict) and set(event['counts']) == set(COUNTS), 'invalid counts')
            for value in event['counts'].values():
                if value != 'unknown':
                    count(value)
            require(isinstance(event['incomplete_reason'], str), 'invalid incomplete reason')
        else:
            require(event['phase'] in (*PHASES, 'unknown'), 'invalid phase')
            reason = event['missing_reason']
            require(isinstance(reason, str), 'invalid missing reason')
            require(bool(reason.strip()) == (event['phase'] == 'unknown'), 'unknown phase requires missing reason; known phase forbids it')
        previous = event
    return data


def summary(data):
    validate(data)
    events = data['events']
    elapsed = {phase: 0 for phase in (*PHASES, 'unknown')}
    for left, right in zip(events, events[1:]):
        elapsed[left['phase']] += right['monotonic_ns'] - left['monotonic_ns']
    finished = events[-1]['kind'] == 'finish'
    complete = finished and not events[-1]['incomplete_reason'] and not any(
        e.get('phase') == 'unknown' for e in events)
    measured = (events[-1]['monotonic_ns'] - events[0]['monotonic_ns']) / 1e9
    return {key: data[key] for key in ('batch_id', 'base_commit', 'selected', 'concurrency')} | {
        'finished': finished, 'timing_complete': complete,
        'started_at': events[0]['utc'], 'finished_at': events[-1]['utc'] if finished else 'unknown',
        'phase_seconds_recorded': {key: value / 1e9 for key, value in elapsed.items()},
        'recorded_wall_seconds': measured,
        'total_wall_seconds': measured if complete else 'unknown',
        'selected_per_hour': data['selected'] * 3600 / measured if complete and measured > 0 else 'unknown',
        'missing_reasons': [e['missing_reason'] for e in events if e.get('missing_reason')]
                          + ([events[-1]['incomplete_reason']] if finished and events[-1]['incomplete_reason'] else [])
                          + ([] if finished else ['not finished; open interval is not counted']),
        'counts': events[-1]['counts'] if finished else dict.fromkeys(COUNTS, 'unknown'),
    }


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def log_path(raw):
    root = ROOT.resolve()
    allowed = root / '.artifacts' / 'i18n'
    require(allowed.resolve() == allowed, 'artifact root must not traverse symlinks')
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    require('..' not in path.parts, 'parent traversal forbidden')
    require(path.resolve() == path, 'symlink paths forbidden')
    require(path.is_relative_to(allowed) and path != allowed, 'log must be below .artifacts/i18n/')
    if path.exists():
        require(path.is_file() and path.stat().st_nlink == 1, 'log must be a regular non-hardlinked file')
    return path


@contextmanager
def locked_directory(path):
    # Serialize cooperating commands without persistent lock files.
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        os.close(descriptor)


def save(path, data):
    payload = json.dumps(validate(data), ensure_ascii=False, indent=2) + '\n'
    name = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix='.timing-', delete=False) as stream:
            name = stream.name
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('start', 'mark', 'finish', 'summary'):
        p = sub.add_parser(command)
        p.add_argument('--log', required=True, help='explicit path below repository .artifacts/i18n/')
        if command == 'start':
            p.add_argument('--batch-id', required=True)
            p.add_argument('--base-commit', required=True)
            p.add_argument('--selected', type=int, required=True)
            p.add_argument('--concurrency', type=int)
        if command in ('start', 'mark'):
            p.add_argument('--phase', choices=(*PHASES, 'unknown'), required=True)
            p.add_argument('--missing-reason', default='')
        if command == 'finish':
            for field in COUNTS:
                p.add_argument('--' + field.replace('_', '-'), type=int)
            p.add_argument('--incomplete-reason', default='')
    args = parser.parse_args(argv)
    try:
        path = log_path(args.log)
        if args.command == 'start':
            path.parent.mkdir(parents=True, exist_ok=True)
        with locked_directory(path.parent):
            path = log_path(args.log)
            if args.command == 'start':
                require(not path.exists(), 'log already exists; start refused')
                data = {'version': 1, 'batch_id': args.batch_id, 'base_commit': args.base_commit,
                        'selected': args.selected, 'concurrency': args.concurrency if args.concurrency is not None else 'unknown', 'events': []}
            else:
                data = validate(json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object))
            if args.command != 'summary':
                require(not data['events'] or data['events'][-1]['kind'] != 'finish', 'log already finished')
                event = {'kind': args.command, **clock_sample()}
                if args.command == 'finish':
                    event.update(counts={key: getattr(args, key) if getattr(args, key) is not None else 'unknown'
                                         for key in COUNTS}, incomplete_reason=args.incomplete_reason)
                else:
                    event.update(phase=args.phase, missing_reason=args.missing_reason)
                data['events'].append(event)
                save(path, data)
            print(json.dumps(summary(data), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
