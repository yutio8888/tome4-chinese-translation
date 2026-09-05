#!/usr/bin/env python3
"""Public full-gate entry; no environment marker or saved-receipt bypass."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18nlib import gate_results


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv not in ([], ["--skip-build"]):
        print("Usage: tools/ci-gates.sh [--skip-build]", file=sys.stderr)
        print("ERROR: expected no arguments or exactly --skip-build", file=sys.stderr)
        return 2
    result = gate_results.run(Path(__file__).resolve().parents[1], skip_build=bool(argv))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
