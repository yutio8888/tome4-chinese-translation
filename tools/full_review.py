#!/usr/bin/env python3
"""Offline full-review round and isolated Engine release entry point."""
from pathlib import Path
import argparse
from contextlib import redirect_stdout
import json
import sys
import zipfile
import subprocess
import contextual_result_check as contextual

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18nlib import full_review as review
from i18nlib import release_candidate as release
from i18nlib.cli_common import _inject_public_dlc_env
from i18nlib.config import load_manifest
from i18nlib.errors import I18nToolError


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    inv = commands.add_parser('inventory')
    inv.add_argument('--round-id', required=True)
    inv.add_argument('--directory', required=True, type=Path)
    inv.add_argument('--snapshot-report', action='append', required=True, type=Path)
    inv.add_argument('--source-provenance', type=Path)
    succ = commands.add_parser('successor')
    succ.add_argument('--directory', required=True, type=Path)
    succ.add_argument('--output', required=True, type=Path)
    succ.add_argument('--request', required=True, type=Path)
    exp = commands.add_parser('export')
    exp.add_argument('--directory', required=True, type=Path)
    exp.add_argument('--selection', required=True, type=Path)
    exp.add_argument('--source-workset', required=True, type=Path)
    exp.add_argument('--scope', required=True, type=Path)
    exp.add_argument('--export-id', required=True)
    exp.add_argument('--lane', required=True, choices=['A', 'B'])
    exp.add_argument('--task-id', required=True)
    exp.add_argument('--dispatch-id', required=True)
    exp.add_argument('--workspace-id', required=True)
    exp.add_argument('--parent-agent-id', required=True)
    gates = commands.add_parser('task-gates')
    gates.add_argument('--directory', required=True, type=Path)
    gates.add_argument('--export-id', required=True)
    gates.add_argument('--results', type=Path, help='recover archival of an exact task-bound run; never reuse another task receipt')
    imp = commands.add_parser('import')
    imp.add_argument('--directory', required=True, type=Path)
    imp.add_argument('--export-id', required=True)
    imp.add_argument('--raw', required=True, type=Path)
    imp.add_argument('--binding', required=True, type=Path)
    check = commands.add_parser('check')
    check.add_argument('--directory', required=True, type=Path)
    check.add_argument('--require-complete', action='store_true')
    check.add_argument('--require-release-ready', action='store_true')
    assemble = commands.add_parser('assemble')
    assemble.add_argument('--candidate-id', required=True)
    assemble.add_argument('--release-commit', required=True)
    install = commands.add_parser('install')
    install.add_argument('--candidate', required=True, type=Path)
    install.add_argument('--target', required=True, type=Path)
    install.add_argument('--target-spec', required=True, type=Path)
    install.add_argument('--operation-id', required=True)
    restore = commands.add_parser('restore')
    restore.add_argument('--target', required=True, type=Path)
    restore.add_argument('--operation-id', required=True)
    args = parser.parse_args(argv)
    _inject_public_dlc_env()
    manifest = load_manifest()
    try:
        # Runtime operational round writes must be tracked evidence or ignored fixtures.
        for field in ('directory', 'output'):
            if not hasattr(args, field):
                continue
            directory = getattr(args, field).absolute()
            if '..' in directory.parts or directory != directory.resolve():
                raise review.FullReviewError('round directory must have an exact normalized physical path')
            allowed = [manifest.root / 'evidence/full-review', manifest.root / '.artifacts/i18n']
            if not any(directory != p and directory.is_relative_to(p) for p in allowed):
                raise review.FullReviewError('round directory must be evidence/full-review/<round> or ignored fixture')
        if args.command == 'inventory':
            result = review.inventory(manifest, args.round_id, args.directory, args.snapshot_report, args.source_provenance)
        elif args.command == 'successor':
            result = review.successor(manifest, args.directory, args.output, args.request)
        elif args.command == 'export':
            result = review.export(manifest, args.directory, review.read(args.selection), args.source_workset,
                args.scope, export_id=args.export_id, lane=args.lane, task_id=args.task_id,
                dispatch_id=args.dispatch_id, workspace_id=args.workspace_id, parent_agent_id=args.parent_agent_id)
        elif args.command == 'task-gates':
            with redirect_stdout(sys.stderr):
                result = review.task_gates(manifest, args.directory, args.export_id, args.results)
        elif args.command == 'import':
            result = review.import_result(manifest, args.directory, args.export_id, args.raw, args.binding)
        elif args.command == 'check':
            result = review.check(manifest, args.directory, require_complete=args.require_complete or args.require_release_ready)
            if args.require_release_ready and not result['release_ready']:
                raise review.FullReviewError('review coverage may be complete; final Engine/game release readiness is unverified')
        elif args.command == 'assemble':
            result = release.assemble(manifest, args.candidate_id, args.release_commit)
        elif args.command == 'install':
            result = release.install(manifest, args.candidate, args.target, args.target_spec, args.operation_id)
        else:
            result = release.restore(manifest, args.target, args.operation_id)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (ValueError, OSError, KeyError, TypeError, contextual.ContractError, contextual.InputError,
            I18nToolError, zipfile.BadZipFile, subprocess.TimeoutExpired) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
