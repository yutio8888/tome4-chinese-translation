"""Versioned gate execution with read-audited same-round unit-test reuse.

Schema 2 always executes. Schema 3 binds every audited test input (repository,
Git, native and listed ignored inputs); every other check, including build,
executes per receipt. Consumers validate frozen source chains; only gate-time
reuse decisions and same-invocation validation compare live test identities.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import stat
import subprocess
import tempfile

from . import TOOL_VERSION
from .gate_binding_cache import BindingCache, strict_json

VERSION = "ci-gates-v2"
PYTHON = ["python3", "-B"]
CHECKS = [
    ("01-doctor", PYTHON + ["tools/i18n", "doctor"]),
    ("02-strict-lint", PYTHON + ["tools/i18n", "lint", "--strict"]),
    ("03-test-group-registration", PYTHON + ["tools/test_groups.py", "--check"]),
    ("03-toolchain-unit-tests", PYTHON + ["tools/test_groups.py", "--group", "toolchain"]),
    ("04-quality-facts-unit-tests", PYTHON + ["tools/test_groups.py", "--group", "quality-facts"]),
    ("04-semantic-claim-unit-tests", PYTHON + ["tools/test_groups.py", "--group", "semantic-claim"]),
    ("04-semantic-claims-strict-registry", PYTHON + ["tools/i18n", "claims", "check", "--registry", "evidence/quality/semantic-claim-regressions-v1.json", "--strict"]),
    ("05-contract-suite-unit-tests", PYTHON + ["tools/test_groups.py", "--group", "contract-suite"]),
    ("05-production-shadow-surface-ledger-tests", PYTHON + ["tools/test_groups.py", "--group", "production-shadow-surface-ledger"]),
    ("06-runtime-collision-scan", PYTHON + ["tools/scan_runtime_collisions.py"]),
    ("07-runtime-key-classification", PYTHON + ["tools/classify_runtime_keys.py"]),
    ("08-terminology-static-audit", PYTHON + ["tools/audit_static.py"]),
    ("09-terminology-dynamic-audit", PYTHON + ["tools/audit_dynamic.py"]),
    ("10-domain-annotation", PYTHON + ["tools/annotate_domains.py"]),
    ("11-worktree-whitespace", ["git", "diff", "--check"]),
    ("11-staged-whitespace", ["git", "diff", "--cached", "--check"]),
    ("12-core-addon-build", PYTHON + ["tools/i18n", "build", "--profile", "addon", "--component", "tome", "--require-complete"]),
]
COVERAGE = {
    "tests/i18n/test_surface_screen_manifest.py": "05-production-shadow-surface-ledger-tests",
    "tests/i18n/test_surface_screen_result_check.py": "05-production-shadow-surface-ledger-tests",
    "tests/i18n/test_contextual_result_check.py": "05-contract-suite-unit-tests",
}


class GateError(ValueError):
    pass


class _UncoveredTestInput(GateError):
    """An audited external input now resolves into a lane-mutated prefix."""


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def checks(skip_build=False):
    return copy.deepcopy(CHECKS[:-1] if skip_build else CHECKS)


def candidate(batch_id, catalog_id, base_commit, policy_sha256, revisions):
    """Both producer and replay derive this from their validated batch, not a supplied hash."""
    return {"batch_id": batch_id, "catalog_id": catalog_id, "base_commit": base_commit,
            "policy_sha256": policy_sha256, "ordered_revisions": list(revisions)}


def _git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.PIPE)


def _file_identity(path):
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return ["absent"]
    if stat.S_ISLNK(mode):
        return ["symlink", os.readlink(path)]
    if not stat.S_ISREG(mode):
        raise GateError(f"gate input is not an ordinary file: {path}")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return [stat.S_IMODE(mode), h.hexdigest()]


def binding(root, selected=None, skip_build=False, *, use_cache=None):
    root = Path(root).resolve()
    # Include index blobs and actual file bytes (including untracked nonignored inputs).
    # Ignored prospective/log files cannot invalidate a receipt; tracked ignored files can.
    names = sorted(set(_git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0")) - {b""})
    enabled = os.environ.get("I18N_GATE_BINDING_CACHE") != "off" if use_cache is None else use_cache
    cache = BindingCache(root) if enabled else None
    files = {os.fsdecode(name): (cache.identity(os.fsdecode(name), root / os.fsdecode(name), _file_identity)
                                if cache else _file_identity(root / os.fsdecode(name))) for name in names}
    if cache:
        cache.save()
    config = {name: value for name, value in files.items()
              if name.startswith(("i18n/", "terminology/")) or name == "tests/i18n/test_groups.json"}
    config["environment_sha256"] = digest(dict(os.environ))
    selected = copy.deepcopy(selected)
    return {"candidate": selected, "candidate_sha256": digest(selected),
            "worktree_sha256": digest({"files": files, "index": _git(root, "ls-files", "--stage", "-z").hex()}),
            "tool_commit": _git(root, "rev-parse", "HEAD").decode().strip(),
            "tool_version": TOOL_VERSION, "runner_version": VERSION,
            "python_version": platform.python_version(), "config_sha256": digest(config),
            "check_set_sha256": digest(checks(skip_build)), "skip_build": skip_build}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def _execute(argv, root, log):
    with log.open("wb") as stream:
        try:
            return subprocess.run(argv, cwd=root, stdout=stream, stderr=subprocess.STDOUT, check=False).returncode
        except OSError as error:
            stream.write(str(error).encode("utf-8", "replace"))
            return 127


def run(root, selected=None, skip_build=False, *, execute=None, reuse_round=None, reuse=True):
    """Default schema 2; full-review opts into explicit schema-3 same-round reuse."""
    root = Path(root).resolve()
    log_root = root / ".artifacts/i18n/ci-gates"
    log_root.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="run.", dir=log_root))
    print(f"CI gate log directory: {directory}", flush=True)
    result = {"schema_version": 2, "binding": None, "coverage": COVERAGE.copy(),
              "started_at": _now(), "finished_at": None, "complete": False,
              "success": False, "checks": [], "error": None}
    execute = _execute if execute is None else execute
    identities = {}
    if reuse_round is not None:
        reuse_round = _round_path(root, reuse_round)
        result.update(schema_version=3, reuse_round=reuse_round)
    try:
        result["binding"] = binding(root, selected, skip_build)
        if reuse_round is not None:
            identities = test_identities(root, skip_build)
        sources = _reuse_sources(root, reuse_round, identities) if reuse_round and reuse and os.environ.get("I18N_GATE_TEST_REUSE") != "off" else {}
        for check_id, argv in checks(skip_build):
            if check_id in sources:
                record = copy.deepcopy(sources[check_id])
                result["checks"].append(record)
                print(f"REUSE {check_id} ({record['reuse']['receipt_path']})", flush=True)
                continue
            log = directory / (check_id + ".log")
            start = _now()
            code = execute(argv, root, log)
            record = {"id": check_id, "argv": argv, "command": shlex.join(argv),
                      "exit_code": code, "log_path": log.relative_to(root).as_posix(),
                      "output_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
                      "started_at": start, "finished_at": _now()}
            if check_id in identities:
                record['test_identity_sha256'] = identities[check_id]
            result["checks"].append(record)
            print(f"{'PASS' if code == 0 else 'FAIL'}  {check_id} (log: {log})", flush=True)
        if result["binding"] != binding(root, selected, skip_build):
            raise GateError("gate binding changed during execution")
        if identities and identities != test_identities(root, skip_build):
            raise GateError("gate test identity changed during execution")
        result["complete"] = True
        result["success"] = all("reuse" in item or (type(item["exit_code"]) is int and item["exit_code"] == 0) for item in result["checks"])
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        result["error"] = str(error)
    finally:
        result["finished_at"] = _now()
        (directory / "results.json").write_bytes(canonical(result) + b"\n")
    print("ALL GATES PASSED" if result["success"] else "GATES FAILED", flush=True)
    return result


def _require(condition, message):
    if not condition:
        raise GateError(message)


def _hash(value, length=64):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{%d}" % length, value) is not None


def _time(value):
    _require(isinstance(value, str), "gate timestamp must be text")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise GateError("invalid gate timestamp") from error
    _require(parsed.tzinfo is not None, "gate timestamp requires timezone")
    return parsed


def validate(result, *, selected=None, expected_binding=None, require_full=True, root=None, receipt_path=None, expected_test_identities=None):
    """Validate definitions/source chains; live identities are an explicit gate-time opt-in."""
    return _validate(result, selected=selected, expected_binding=expected_binding,
                     require_full=require_full, root=root, receipt_path=receipt_path, historical=False,
                     expected_test_identities=expected_test_identities)


def validate_historical(result, *, selected, root=None, receipt_path=None):
    """Replay recorded definitions, never authorize production execution or reuse."""
    return _validate(result, selected=selected, root=root, receipt_path=receipt_path, historical=True)


def _validate(result, *, selected, expected_binding=None, require_full=True, root=None,
              historical=False, receipt_path=None, visiting=frozenset(), validated=None,
              expected_test_identities=None):
    validated = {} if validated is None else validated
    _require(isinstance(result, dict) and set(result) == {
        "schema_version", "binding", "coverage", "started_at", "finished_at", "complete", "success", "checks", "error"} | ({"reuse_round"} if result.get("schema_version") == 3 else set()), "gate result exact schema mismatch")
    _require(type(result["schema_version"]) is int and result["schema_version"] in (2, 3), "gate schema version mismatch")
    _require(result["complete"] is True and result["success"] is True and result["error"] is None, "gate result failed or incomplete")
    if result['schema_version'] == 3:
        _require(root is not None, "schema 3 requires receipt root")
        round_path = _round_path(root, result['reuse_round'])
        _require(isinstance(selected, dict) and 'full_review_task' in selected and isinstance(selected.get('round_id'), str), "schema 3 requires full-review selection")
        if receipt_path is not None:
            locator = _source_path(root, round_path, receipt_path)
            _require(locator not in visiting, "gate reuse cycle")
            _require(len(visiting) < 64, 'gate reuse depth limit')
            visiting = visiting | {locator}
    start, end = _time(result["started_at"]), _time(result["finished_at"])
    _require(start <= end, "gate result time order")
    b = result["binding"]
    _require(isinstance(b, dict) and set(b) == {"candidate", "candidate_sha256", "worktree_sha256", "tool_commit", "tool_version", "runner_version", "python_version", "config_sha256", "check_set_sha256", "skip_build"}, "gate binding exact schema mismatch")
    _require(type(b["skip_build"]) is bool and (not require_full or not b["skip_build"]), "full gate build required")
    for field in ("candidate_sha256", "worktree_sha256", "config_sha256", "check_set_sha256"):
        _require(_hash(b[field]), f"invalid gate {field}")
    _require(_hash(b["tool_commit"], 40), "invalid gate tool commit")
    _require(isinstance(b["runner_version"], str)
             and re.fullmatch(r"ci-gates-v[1-9][0-9]*", b["runner_version"]) is not None
             and (historical or b["runner_version"] == VERSION)
             and isinstance(b["tool_version"], str)
             and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", b["tool_version"]) is not None
             and isinstance(b["python_version"], str)
             and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", b["python_version"]) is not None, "invalid gate version")
    _require(b["candidate"] == selected and b["candidate_sha256"] == digest(selected), "gate candidate binding mismatch")
    if selected is not None:
        # preflight requires HEAD == batch base; replay can recheck this fact
        # without access to ignored logs or the original dirty worktree.
        _require(isinstance(selected, dict) and b["tool_commit"] == selected.get("base_commit"), "gate tool commit/batch base mismatch")
    records = result["checks"]
    _require(isinstance(records, list) and bool(records), "gate check set incomplete")
    definitions = []
    seen = set()
    for record in records:
        _record_schema(record, result['schema_version'])
        check_id, argv = record["id"], record["argv"]
        _require(isinstance(check_id, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", check_id) is not None,
                 "invalid gate check ID")
        _require(check_id not in seen, "duplicate gate check ID")
        seen.add(check_id)
        _require(isinstance(argv, list) and bool(argv)
                 and all(isinstance(arg, str) and bool(arg) and "\0" not in arg for arg in argv),
                 "invalid gate check argv")
        definitions.append((check_id, argv))
    _require(b["check_set_sha256"] == digest(definitions), "gate check set binding mismatch")
    if not historical:
        _require(definitions == checks(b["skip_build"]), "gate check ID/command mismatch")
    if expected_binding is not None:
        _require(b == expected_binding, "gate live binding mismatch")
    coverage = result["coverage"]
    _require(isinstance(coverage, dict) and bool(coverage)
             and all(isinstance(name, str) and bool(name.strip())
                     and isinstance(owner, str) and owner in seen for name, owner in coverage.items()),
             "invalid gate consumer coverage")
    if not historical:
        _require(coverage == COVERAGE, "gate consumer coverage mismatch")
    if result['schema_version'] == 3 and expected_test_identities is not None:
        for record in records:
            _require(record.get('test_identity_sha256') == expected_test_identities.get(record['id']),
                     'live test identity mismatch')
    previous = start
    for record, (check_id, argv) in zip(records, definitions):
        _record_schema(record, result['schema_version'])
        _require(record["id"] == check_id and record["argv"] == argv and record["command"] == shlex.join(argv), "gate check ID/command mismatch")
        if 'reuse' in record:
            _validate_reuse(result, record, root, historical, visiting, validated)
            continue
        if 'test_identity_sha256' in record:
            _require(_hash(record['test_identity_sha256']), "invalid test identity")
        _require(type(record["exit_code"]) is int and record["exit_code"] == 0, "gate command failed")
        _require(_hash(record["output_sha256"]), "invalid gate output hash")
        path = record["log_path"]
        _require(isinstance(path, str) and re.fullmatch(r"\.artifacts/i18n/ci-gates/run\.[\w-]+/" + re.escape(check_id) + r"\.log", path) is not None, "invalid gate log path")
        a, z = _time(record["started_at"]), _time(record["finished_at"])
        _require(previous <= a <= z <= end, "gate check time order")
        previous = z
        if root is not None:
            log = (Path(root) / receipt_path).parent / check_id / 'output.log' if receipt_path is not None else Path(root) / path
            _require(not log.is_symlink() and hashlib.sha256(log.read_bytes()).hexdigest() == record["output_sha256"], "gate log hash mismatch")
    return result


# Read audits and exclusions are documented in the maintenance REPORT. Toolchain
# stays excluded: it reads live full-review paths and mutable inventory caches.
# Quality-facts reads the installed Pi/Node closure; it must execute each time.
NARROW_TESTS = frozenset({'03-test-group-registration'})
BROAD_TESTS = frozenset({'04-semantic-claim-unit-tests', '05-contract-suite-unit-tests',
                         '05-production-shadow-surface-ledger-tests'})
REUSABLE_TESTS = NARROW_TESTS | BROAD_TESTS
TEST_EXCLUDED_PREFIXES = ('evidence/full-review/', '.ai/task/', '.ai/reviews/', '.artifacts/')
TEST_IGNORED_INPUTS = ('.artifacts/i18n/production-review/reconciliation.json',
                       '.artifacts/.gitignore', '.artifacts/i18n/.gitignore')
EXECUTED_FIELDS = {'id', 'argv', 'command', 'exit_code', 'log_path', 'output_sha256', 'started_at', 'finished_at'}
REUSED_FIELDS = {'id', 'argv', 'command', 'output_sha256', 'test_identity_sha256', 'reuse'}


def _test_external_inputs(root, cache):
    """Bind audited native children, Lua modules and immutable extractor inputs.

    Child-created fixtures are not preexisting inputs. Git's object IDs bind
    historical trees; replacement refs, shallow/graft boundaries and effective
    configuration are bound separately, including check-ignore's exclude files.
    """
    files = {}
    def add(path):
        path = Path(path)
        resolved = path.resolve()
        if resolved.is_relative_to(root):
            target = resolved.relative_to(root).as_posix()
            if target.startswith(TEST_EXCLUDED_PREFIXES) and target not in TEST_IGNORED_INPUTS:
                raise _UncoveredTestInput(f'external test input resolves into excluded prefix: {path}')
        for value in (path, resolved):
            key = str(value)
            files[key] = cache.identity(key, value, _file_identity) if cache else _file_identity(value)
    git = {'refs': _git(root, 'for-each-ref', '--format=%(refname) %(objectname)').hex(),
           'config': _git(root, 'config', '--null', '--list', '--show-origin').hex()}
    for name in ('info/exclude', 'info/grafts', 'shallow'):
        add(root / os.fsdecode(_git(root, 'rev-parse', '--git-path', name)).strip())
    add(Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / 'git/ignore')
    excludes = subprocess.run(['git', 'config', '--path', '--get', 'core.excludesfile'],
                              cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if excludes.returncode == 0:
        path = Path(os.fsdecode(excludes.stdout).strip()).expanduser()
        add(path if path.is_absolute() else root / path)
    manifest_path = root / 'i18n/versions/tome-1.7.6.json'
    if manifest_path.is_file():
        from .config import load_manifest
        from .runtime import LuaRuntime
        manifest = load_manifest(manifest_path=manifest_path)
        runtime = LuaRuntime(manifest)
        executables = [runtime.luajit.resolve()]
        executables.extend(Path(p).resolve() for name in ('git', 'sh', 'bash', 'ldd', 'node', 'env')
                           if (p := shutil.which(name)))
        native = executables + [p for base in (runtime.lua_share, runtime.lua_lib)
                                for p in base.rglob('*') if p.is_file()]
        for path in native:
            add(path)
            if path.suffix == '.so' or path in executables:
                probe = subprocess.run(['ldd', str(path)], cwd=root, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, check=False)
                for library in re.findall(rb'(/[^\s()]+)', probe.stdout):
                    add(os.fsdecode(library))
        repo = manifest.repository_path(manifest.extractor.repository)
        def source(*args):
            return _git(root, '-C', str(repo), *args)
        git['extractor'] = {
            'root': source('rev-parse', '--show-toplevel').hex(),
            'head': source('rev-parse', '--verify', 'HEAD').hex(),
            'commit': source('rev-parse', '--verify', manifest.extractor.commit + '^{commit}').hex(),
            'archive': hashlib.sha256(source('archive', '--format=tar', manifest.extractor.commit,
                         '--', ':(glob)' + manifest.extractor.git_path + '/**/*.lua')).hexdigest()}
    return {'git': git, 'files': files}


def test_identities(root, skip_build=False):
    root = Path(root).resolve()
    names = {os.fsdecode(n) for n in _git(root, 'ls-files', '-z', '--cached', '--others',
                                         '--exclude-standard').split(b'\0') if n}
    names = {n for n in names if not n.startswith(TEST_EXCLUDED_PREFIXES)}
    # Python may read existing bytecode even under -B; registry lists ignored
    # tests too. Include both rather than assuming only source files are read.
    extra = {p.relative_to(root).as_posix() for prefix in ('tests', 'tools', 'i18n')
             for pattern in ('test_*.py', '*.pyc') for p in (root / prefix).rglob(pattern)}
    names.update(extra)
    names.update(TEST_IGNORED_INPUTS)  # absences are identities, too
    cache = BindingCache(root) if os.environ.get('I18N_GATE_BINDING_CACHE') != 'off' else None
    files = {}
    for name in sorted(names):
        path = root / name
        value = cache.identity(name, path, _file_identity) if cache else _file_identity(path)
        try:
            resolved = path.resolve()
        except (OSError, RuntimeError):
            return {}  # Unresolvable input: execute every check, never reuse.
        if resolved != path:
            # Test reads follow links (including symlink directory ancestors).
            # Unlisted/excluded targets cannot be qualified by the read audit.
            if not resolved.is_relative_to(root):
                return {}
            target = resolved.relative_to(root).as_posix()
            if target not in names or (target.startswith(TEST_EXCLUDED_PREFIXES)
                                       and target not in TEST_IGNORED_INPUTS):
                return {}
            content = cache.identity(target, resolved, _file_identity) if cache else _file_identity(resolved)
            value = [value, target, content]
        files[name] = value
    common = {'environment': dict(os.environ), 'python': platform.python_version(),
              'tool_version': TOOL_VERSION, 'runner_version': VERSION}
    narrow = dict(common, files={n: v for n, v in files.items() if n.startswith(('tools/', 'tests/', 'i18n/'))})
    try:
        external = _test_external_inputs(root, cache)
    except _UncoveredTestInput:
        return {}
    broad = dict(common, files=files, head=_git(root, 'rev-parse', 'HEAD').hex(),
                 index=_git(root, 'ls-files', '--stage', '-z').hex(),
                 external=external)
    if cache:
        # Do not evict the large full binding's excluded evidence hashes.
        cache.save(keep_existing=True)
    return {name: digest(dict(narrow if name in NARROW_TESTS else broad, argv=argv))
            for name, argv in checks(skip_build) if name in REUSABLE_TESTS}


def _record_schema(record, schema):
    _require(isinstance(record, dict), 'gate check must be object')
    eligible = schema == 3 and isinstance(record.get('id'), str) and record['id'] in REUSABLE_TESTS
    fields = REUSED_FIELDS if 'reuse' in record else EXECUTED_FIELDS | (
        {'test_identity_sha256'} if eligible and 'test_identity_sha256' in record else set())
    _require(set(record) == fields and ('reuse' not in record or eligible), 'gate check exact schema mismatch')


def _round_path(root, value):
    _require(isinstance(value, (str, Path)), 'invalid reuse round')
    root = Path(root).resolve()
    p = Path(value)
    p = p if p.is_absolute() else root / p
    relative = p.relative_to(root).as_posix() if p.is_relative_to(root) else ''
    _require(relative.startswith(('evidence/full-review/', '.artifacts/i18n/')) and '..' not in p.parts
             and p.resolve() == p and relative != '.artifacts/i18n/', 'invalid reuse round path')
    return relative


def _source_path(root, round_path, value):
    _require(isinstance(value, (str, Path)), 'invalid source receipt path')
    p = Path(value)
    root = Path(root).resolve()
    p = p if p.is_absolute() else root / p
    _require(p.is_relative_to(root), 'source receipt outside root')
    relative = p.relative_to(root).as_posix()
    _require(relative.startswith(round_path + '/task-gates/') and relative.endswith('/results.json')
             and '..' not in p.parts and p.resolve() == p, 'source receipt outside same-round task-gates')
    return relative


def _validate_reuse(result, record, root, historical, visiting, validated):
    reuse = record['reuse']
    _require(isinstance(reuse, dict) and set(reuse) == {'receipt_path', 'receipt_sha256', 'log_sha256'}, 'invalid gate reuse record')
    for value in (reuse['receipt_sha256'], reuse['log_sha256'], record['test_identity_sha256'], record['output_sha256']):
        _require(_hash(value), 'invalid reuse hash')
    path = _source_path(root, result['reuse_round'], reuse['receipt_path'])
    _require(path not in visiting, 'gate reuse cycle')
    try:
        raw = (Path(root) / path).read_bytes()
        _require(hashlib.sha256(raw).hexdigest() == reuse['receipt_sha256'], 'source receipt hash mismatch')
        source = strict_json(raw)
        _require(isinstance(source, dict), 'source receipt must be object')
        _require(source.get('schema_version') == 3 and source.get('reuse_round') == result['reuse_round'], 'source reuse round mismatch')
        _require(source['binding']['candidate']['round_id'] == result['binding']['candidate']['round_id'], 'source round identity mismatch')
        key = (path, reuse['receipt_sha256'])
        if key not in validated:
            _validate(source, selected=source['binding']['candidate'], root=root, receipt_path=path,
                      historical=historical, visiting=visiting, validated=validated)
            validated[key] = True
        _require(_time(source['finished_at']) <= _time(result['started_at']), 'source receipt is not earlier PASS')
        source_record = next((r for r in source['checks'] if r['id'] == record['id']), None)
        _require(source_record is not None and source_record['argv'] == record['argv']
                 and source_record.get('test_identity_sha256') == record['test_identity_sha256']
                 and source_record['output_sha256'] == record['output_sha256'] == reuse['log_sha256'], 'source test identity/output mismatch')
        # This log is archived with the source receipt, independent of ignored run logs.
        log = Path(root) / path
        log = log.parent / record['id'] / 'output.log'
        _require(not log.is_symlink() and hashlib.sha256(log.read_bytes()).hexdigest() == reuse['log_sha256'], 'source check log hash mismatch')
    except (OSError, KeyError, TypeError, ValueError) as error:
        raise GateError('gate reuse rejected: ' + str(error)) from error


def record_output(root, record):
    """Effective log bytes for archival; reused checks never fabricate execution."""
    if 'reuse' in record:
        p = Path(root) / record['reuse']['receipt_path']
        return (p.parent / record['id'] / 'output.log').read_bytes()
    return (Path(root) / record['log_path']).read_bytes()


def _reuse_sources(root, round_path, identities):
    found = {}
    for path in sorted((Path(root) / round_path / 'task-gates').glob('*/*/results.json')):
        try:
            raw = path.read_bytes()
            source = strict_json(raw)
            if not isinstance(source, dict) or source.get('schema_version') != 3 or source.get('reuse_round') != round_path:
                continue
            validate(source, selected=source['binding']['candidate'], root=root, receipt_path=path)
            for record in source['checks']:
                name = record['id']
                if name in identities and record.get('test_identity_sha256') == identities[name]:
                    found.setdefault(name, {'id': name, 'argv': record['argv'], 'command': record['command'],
                        'output_sha256': record['output_sha256'], 'test_identity_sha256': identities[name],
                        'reuse': {'receipt_path': path.relative_to(root).as_posix(),
                                  'receipt_sha256': hashlib.sha256(raw).hexdigest(), 'log_sha256': record['output_sha256']}})
        except (OSError, ValueError, KeyError, TypeError):
            continue  # An unusable cache source costs execution, never PASS.
    return found
