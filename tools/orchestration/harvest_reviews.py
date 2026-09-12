#!/usr/bin/env python3
"""Save exact notified terminal outputs before strict validation; never parse logs.

--captures is a local map of task_id|dispatch_id to {terminal_path, raw_path}.
It is not MCP wire schema. Each member must have a finish notification.
Accepted import files are published by close_review_tasks after archive confirmation.
"""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_lifecycle as lifecycle


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('children')
    p.add_argument('outdir')
    p.add_argument('--key', choices=['results', 'verdicts'], default='results')
    p.add_argument('--captures', required=True)
    p.add_argument('--notified', action='store_true', required=True)
    a = p.parse_args(argv)
    j = lifecycle.Journal(a.children)
    bad = []
    for key, files in lifecycle.read(a.captures).items():
        row = j.get(key)
        expected = 'results' if row['purpose'] == lifecycle.SURFACE else 'verdicts'
        lifecycle.require(a.key == expected, 'result key does not match frozen contract')
        if not j.harvest(key, lifecycle.read(files['terminal_path']), Path(files['raw_path']).read_bytes(),
                         Path(a.outdir) / 'diagnostics', notified=a.notified):
            bad.append(key)
    lifecycle.require(not bad, f'invalid outputs retained; archive before fresh retry: {bad}')
    print('RAW_VALIDATED; archive confirmations and complete-stage close still required')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError) as error:
        print(f'HARVEST_FAILED: {error}', file=sys.stderr)
        sys.exit(1)
