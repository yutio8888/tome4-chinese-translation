#!/usr/bin/env python3
"""Validate the single CI test registry and run one group, including load_tests hooks."""

import argparse
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "tests/i18n/test_groups.json"


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def validate_registry(root, config):
    if not isinstance(config, dict) or set(config) != {"groups", "indirect", "excluded"}:
        raise ValueError("registry requires exactly groups, indirect, excluded")
    groups, indirect, excluded = (config[k] for k in ("groups", "indirect", "excluded"))
    if not all(isinstance(v, dict) for v in (groups, indirect, excluded)) or not groups:
        raise ValueError("registry sections must be objects; groups must not be empty")
    registered = set()

    def register(path):
        if not isinstance(path, str):
            raise ValueError("test path must be a string")
        parsed = PurePosixPath(path)
        if (not path.startswith("tests/") or str(parsed) != path
                or ".." in parsed.parts or not parsed.name.startswith("test_")
                or parsed.suffix != ".py" or not (root / path).is_file()):
            raise ValueError(f"invalid or missing test path: {path}")
        if path in registered:
            raise ValueError(f"test registered more than once: {path}")
        registered.add(path)

    direct = set()
    for name, paths in groups.items():
        if not isinstance(name, str) or not name.strip() or not isinstance(paths, list) or not paths:
            raise ValueError("each group needs a name and nonempty test path list")
        for path in paths:
            register(path)
            direct.add(path)
    for path, entry in indirect.items():
        register(path)
        if (not isinstance(entry, dict) or set(entry) != {"via", "reason"}
                or not isinstance(entry["via"], str) or entry["via"] not in direct
                or not isinstance(entry["reason"], str) or not entry["reason"].strip()):
            raise ValueError(f"indirect test needs a direct via and reason: {path}")
    for path, reason in excluded.items():
        register(path)
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"excluded test needs a reason: {path}")
    discovered = {p.relative_to(root).as_posix() for p in (root / "tests").rglob("test_*.py")}
    missing = discovered - registered
    if missing:
        raise ValueError(f"unregistered tests: {', '.join(sorted(missing))}")
    return config


def test_cases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from test_cases(item)
        else:
            yield item


def load_group(config, group):
    if group not in config["groups"]:
        raise ValueError(f"unknown test group: {group}")
    paths = config["groups"][group]
    loader = unittest.TestLoader()
    try:
        suite = loader.loadTestsFromNames([p[:-3].replace("/", ".") for p in paths])
    except Exception as error:
        raise ValueError(f"test loading failed: {error}") from error
    if loader.errors:
        raise ValueError("test loading failed:\n" + "\n".join(loader.errors))
    cases = list(test_cases(suite))
    ids = Counter(case.id() for case in cases)
    duplicates = sorted(key for key, count in ids.items() if count > 1)
    if duplicates:
        raise ValueError(f"duplicate loaded tests: {duplicates}")
    counts = Counter(type(case).__module__.replace(".", "/") + ".py" for case in cases)
    indirect = {p for p, entry in config["indirect"].items() if entry["via"] in paths}
    unexpected = set(counts) - set(paths) - indirect
    missing = indirect - set(counts)
    if unexpected or missing:
        raise ValueError(f"loaded module mismatch: unexpected={sorted(unexpected)}, missing indirect={sorted(missing)}")
    for path in [*paths, *sorted(indirect)]:
        print(f"MODULE {path}: {counts[path]} tests" + (" (indirect)" if path in indirect else ""), flush=True)
    return suite


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--group")
    args = parser.parse_args(argv)
    try:
        config = validate_registry(args.root, json.loads(
            args.config.read_text(encoding="utf-8"), object_pairs_hook=unique_object))
        if args.check:
            print("PASS test group registration")
            return 0
        sys.path.insert(0, str(args.root.resolve()))
        suite = load_group(config, args.group)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
