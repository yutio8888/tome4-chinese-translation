"""Disposable verified historical predecessor results, never production evidence.

The only caller is the recursive boundary in full_review._check. Instrumentation
is scoped to that computation, including all nested predecessors and helpers.
Nested hits merge their reverified observations into every enclosing result.
The same-user, accidental-corruption trust boundary matches projection_cache.
"""
from __future__ import annotations

import builtins
from collections import Counter
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import io
import sysconfig
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import threading
import time

from . import projection_cache as precedent

CACHE_RELATIVE = Path('.artifacts/i18n/full-review-cache-v1')
FORMAT = 'verified-historical-predecessor-v1'
# Export (outputs-only) and merge (complete) checks use different keys. Each
# recent entry is ~300 MB and grows a few MB per round, so the caps must hold
# both kinds for the latest rounds; at 512 MiB they evicted each other and
# every merge replayed the chain from round-v1 (measured 2026-10-22).
MAX_ENTRIES = 8
MAX_TOTAL_BYTES = 4 * 1024 * 1024 * 1024
_NAME = re.compile(r'v1-[0-9a-f]{64}\.json\Z')
_TEMP = re.compile(r'\.v1-tmp-[a-z0-9_]{8}\Z')
STALE_TEMP_SECONDS = 3600
_active = ContextVar('full_review_dependencies', default=None)
# Patching is short-lived but computation-wide. Other threads delegate normally;
# simultaneous recorders serialize, while readers/publishers need no service lock.
_instrument_lock = threading.RLock()
_audit_installed = False
events = []


def event(kind, reason, **fields):
    events.append({'event': kind, 'reason': reason, **fields})
    if os.environ.get('I18N_FULL_REVIEW_CACHE_TRACE') == '1':
        try:
            print(f'full-review-cache: {kind} {reason} {fields}', file=sys.stderr)
        except (OSError, ValueError):
            pass  # Diagnostic output failure cannot change a checker result.


def enabled():
    return os.environ.get('I18N_FULL_REVIEW_CACHE') == 'on'


def canonical(value):
    return precedent._canonical(value)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pack(value):
    """Tagged containers preserve keys, insertion order, tuples and sets exactly."""
    kind = type(value)
    if kind in (str, int, float, bool, type(None)):
        if kind is float:
            canonical(value)  # refuse NaN/infinity, retain -0.0 and float type
        return ['atom', value]
    if kind is dict:
        return ['dict', [[pack(k), pack(v)] for k, v in value.items()]]
    if kind in (list, tuple, set):
        items = [pack(v) for v in value]
        if kind is set:
            items.sort(key=canonical)
        return [kind.__name__, items]
    raise ValueError(f'unsupported value type: {kind.__name__}')


def unpack(value):
    if type(value) is not list or len(value) != 2 or type(value[0]) is not str:
        raise ValueError('invalid tagged value')
    tag, data = value
    if tag == 'atom' and type(data) in (str, int, float, bool, type(None)):
        if type(data) is float:
            canonical(data)
        return data
    if type(data) is not list:
        raise ValueError('invalid container')
    if tag == 'dict':
        result = {}
        for row in data:
            if type(row) is not list or len(row) != 2:
                raise ValueError('invalid mapping pair')
            k, v = map(unpack, row)
            if k in result:
                raise ValueError('duplicate mapping key')
            result[k] = v
        return result
    items = [unpack(v) for v in data]
    if tag == 'list':
        return items
    if tag == 'tuple':
        return tuple(items)
    if tag == 'set':
        result = set(items)
        if len(result) != len(items):
            raise ValueError('duplicate set member')
        return result
    raise ValueError('unknown tag')


@contextmanager
def paused():
    token = _active.set(None)
    try:
        yield
    finally:
        _active.reset(token)


def read_bytes(path):
    """Ordinary helper's exact observed bytes, without a second file open."""
    recorder = _active.get()
    if recorder is None:
        return path.read_bytes()
    with paused():
        raw = path.read_bytes()
    recorder.observe('file', path, value=[len(raw), digest(raw)])
    return raw


def _path(path):
    if isinstance(path, int):
        raise ValueError('descriptor input cannot be tracked')
    # Preserve '..' after symlinks: lexical normalization can name another file.
    name = os.fsdecode(path)
    return name if os.path.isabs(name) else os.path.join(os.getcwd(), name)


def _observation(kind, path, arg=None):
    """Run only with recording paused. Metadata equality never substitutes for hash."""
    if kind == 'file':
        try:
            # Inputs may have changed type since publication. Nonblocking open
            # prevents FIFO/device replacement from hanging dependency checks.
            if not stat.S_ISREG(os.stat(path).st_mode):
                raise ValueError('nonordinary input')
            fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
            with os.fdopen(fd, 'rb') as stream:
                status = os.fstat(stream.fileno())
                if not stat.S_ISREG(status.st_mode):
                    raise ValueError('nonordinary input')
                raw = stream.read(status.st_size + 1)
            return [len(raw), digest(raw)]
        except OSError as error:
            return {'error': error.errno}
    if kind == 'names':
        try:
            return sorted(os.listdir(path))
        except OSError as error:
            return {'error': error.errno}
    if kind == 'link':
        try:
            return os.readlink(path)
        except OSError as error:
            return {'error': error.errno}
    if kind == 'probe':
        try:
            return _probe_value(os.stat(path, follow_symlinks=arg))
        except OSError as error:
            return ['error', error.errno]
    raise ValueError('unknown dependency kind')


class Recorder:
    def __init__(self):
        self.dependencies = {}
        self.invalid = None

    def observe(self, kind, path, arg=None, value=None):
        try:
            with paused():
                name = _path(path)
                if value is None:
                    value = _observation(kind, name, arg)
                key = (kind, name, arg)
                old = self.dependencies.setdefault(key, value)
                if old != value:
                    self.invalid = 'input changed during computation'
        except Exception as error:
            self.invalid = f'unrecordable {kind}: {type(error).__name__}'

    def rows(self):
        return [[kind, path, arg, value] for (kind, path, arg), value in sorted(
            self.dependencies.items(), key=lambda item: repr(item[0]))]


# Audited historical consumers use only existence/errno and S_IS* type tests,
# including pathlib/os.path predicates. They never inspect permission bits or
# other stat fields. Content and enumerated names have separate observations.
# See REPORT's consumer audit; changes to that graph change implementation identity.
def _probe_value(status):
    return ['type', stat.S_IFMT(status.st_mode)]



def _audit(name, args):
    recorder = _active.get()
    if recorder is not None and name in {
            'open', 'os.listdir', 'os.scandir', 'subprocess.Popen', 'os.system',
            'os.posix_spawn', 'os.exec', 'os.fork'}:
        # Wrapped ordinary reads/listings pause around the actual call. Anything
        # reaching here is an untracked fd/C-extension read or external operation.
        recorder.invalid = f'untracked operation: {name}'


@contextmanager
def recording(recorder):
    """Capture pathlib and helper I/O, restoring every patched API on exit.

    No helper is allowed to invisibly read pinned bytes from an existing reader:
    even a warm FixedReader method invalidates publication. Raw descriptor reads
    and subprocesses are similarly refused through the audit hook.
    """
    global _audit_installed
    if _active.get() is not None:
        # The enclosing scope already installed the context-aware wrappers.
        token = _active.set(recorder)
        try:
            yield
        finally:
            _active.reset(token)
        return
    from orchestration.build_evidence_pack import FixedReader
    with _instrument_lock:
        if not _audit_installed:
            sys.addaudithook(_audit)
            _audit_installed = True
        patches = []

        def patch(obj, name, replacement):
            old = getattr(obj, name)
            patches.append((obj, name, old))
            setattr(obj, name, replacement(old))

        def opened(original):
            def call(path, mode='r', *args, **kwargs):
                current = _active.get()
                if current is None:
                    return original(path, mode, *args, **kwargs)
                try:
                    with paused():
                        stream = original(path, mode, *args, **kwargs)
                except OSError as error:
                    current.observe('file', path, value={'error': error.errno})
                    raise
                if kwargs.get('opener') is not None:
                    current.invalid = 'custom opener cannot be audited'
                if not isinstance(mode, str) or any(c in mode for c in 'wax+'):
                    current.invalid = 'write or unknown open mode'
                else:
                    try:
                        # Hash this exact open file description, not a second
                        # path lookup that could observe a replacement inode.
                        with paused():
                            fd = stream.fileno()
                            status = os.fstat(fd)
                            if not stat.S_ISREG(status.st_mode):
                                raise ValueError('nonordinary input')
                            offset, content = 0, hashlib.sha256()
                            # Bound progress by the initial descriptor size even
                            # if another process keeps appending. Final dependency
                            # verification will refuse a changed input.
                            while offset < status.st_size:
                                block = os.pread(fd, min(1024 * 1024, status.st_size - offset), offset)
                                if not block:
                                    break
                                content.update(block)
                                offset += len(block)
                        current.observe('file', path, value=[offset, content.hexdigest()])
                    except Exception as error:
                        current.invalid = f'unrecordable open: {type(error).__name__}'
                return stream
            return call

        def probed(original):
            def call(path, *args, **kwargs):
                current = _active.get()
                if current is None:
                    return original(path, *args, **kwargs)
                follow = kwargs.get('follow_symlinks', original is originals['stat'])
                if args or kwargs.get('dir_fd') is not None:
                    current.invalid = 'relative descriptor stat'
                try:
                    result = original(path, *args, **kwargs)
                except OSError as error:
                    current.observe('probe', path, follow, ['error', error.errno])
                    raise
                current.observe('probe', path, follow, _probe_value(result))
                return result
            return call

        class Entry:
            def __init__(self, entry):
                self._entry = entry
                self.name, self.path = entry.name, entry.path
            def __fspath__(self):
                return self.path
            def _observe(self, follow, predicate=None, expected=None):
                current = _active.get()
                if current is None:
                    return
                # Return native DirEntry results, including its own cached type
                # bits. Additional observation must never introduce a stat error
                # into an otherwise successful directory traversal.
                try:
                    status = self._entry.stat(follow_symlinks=follow)
                    current.observe('probe', self.path, follow, _probe_value(status))
                    if predicate is not None and predicate(status.st_mode) != expected:
                        current.invalid = 'directory entry changed during observation'
                except OSError:
                    current.invalid = 'directory entry cannot be observed reliably'
            def stat(self, *, follow_symlinks=True):
                try:
                    result = self._entry.stat(follow_symlinks=follow_symlinks)
                except OSError as error:
                    current = _active.get()
                    if current is not None:
                        current.observe('probe', self.path, follow_symlinks, ['error', error.errno])
                    raise
                current = _active.get()
                if current is not None:
                    current.observe('probe', self.path, follow_symlinks, _probe_value(result))
                return result
            def is_dir(self, *, follow_symlinks=True):
                result = self._entry.is_dir(follow_symlinks=follow_symlinks)
                self._observe(follow_symlinks, stat.S_ISDIR, result)
                return result
            def is_file(self, *, follow_symlinks=True):
                result = self._entry.is_file(follow_symlinks=follow_symlinks)
                self._observe(follow_symlinks, stat.S_ISREG, result)
                return result
            def is_symlink(self):
                result = self._entry.is_symlink()
                self._observe(False, stat.S_ISLNK, result)
                return result
            def inode(self):
                result = self._entry.inode()
                current = _active.get()
                if current is not None:
                    current.invalid = 'DirEntry inode is not a type-only probe'
                return result

        class Scan:
            def __init__(self, entries):
                self.entries = iter(entries)
            def __iter__(self):
                return self
            def __next__(self):
                return next(self.entries)
            def __enter__(self):
                return self
            def __exit__(self, *args):
                self.close()
            def close(self):
                pass

        def scanned(original):
            def call(path='.'):
                current = _active.get()
                if current is None:
                    return original(path)
                try:
                    with paused():
                        with original(path) as stream:
                            entries = list(stream)
                except OSError as error:
                    current.observe('names', path, value={'error': error.errno})
                    raise
                current.observe('names', path, value=sorted(e.name for e in entries))
                return Scan([Entry(e) for e in entries])
            return call

        def listed(original):
            def call(path='.'):
                current = _active.get()
                try:
                    with paused():
                        result = original(path)
                except OSError as error:
                    if current is not None:
                        current.observe('names', path, value={'error': error.errno})
                    raise
                if current is not None:
                    current.observe('names', path, value=sorted(result))
                return result
            return call

        def linked(original):
            def call(path, *args, **kwargs):
                current = _active.get()
                try:
                    result = original(path, *args, **kwargs)
                except OSError as error:
                    if current is not None:
                        current.observe('link', path, value={'error': error.errno})
                    raise
                if current is not None:
                    if args or kwargs:
                        current.invalid = 'relative descriptor readlink'
                    current.observe('link', path, value=result)
                return result
            return call

        def source(original):
            def call(*args, **kwargs):
                current = _active.get()
                if current is not None:
                    current.invalid = 'historical FixedReader access'
                return original(*args, **kwargs)
            return call

        originals = {'stat': os.stat}
        token = _active.set(recorder)
        try:
            patch(builtins, 'open', opened)
            patch(io, 'open', opened)
            patch(os, 'stat', probed)
            patch(os, 'lstat', probed)
            patch(os, 'scandir', scanned)
            patch(os, 'listdir', listed)
            patch(os, 'readlink', linked)
            for name in ('tree', 'pinned', 'unpinned'):
                patch(FixedReader, name, source)
            yield
        finally:
            _active.reset(token)
            for obj, name, original in reversed(patches):
                setattr(obj, name, original)


def verify(rows):
    if type(rows) is not list or not rows:
        raise ValueError('missing dependencies')
    seen = set()
    for row in rows:
        if type(row) is not list or len(row) != 4:
            raise ValueError('invalid dependency')
        kind, path, arg, value = row
        if (kind not in ('file', 'names', 'probe', 'link') or type(path) is not str or
                not os.path.isabs(path) or (kind == 'probe' and type(arg) is not bool) or
                (kind != 'probe' and arg is not None)):
            raise ValueError('invalid dependency fields')
        key = (kind, path, arg)
        if key in seen:
            raise ValueError('duplicate dependency')
        seen.add(key)
        if canonical(_observation(kind, path, arg)) != canonical(value):
            raise ValueError(f'dependency changed: {kind} {path}')


def _directory(root, create):
    current = root.resolve()
    for name in CACHE_RELATIVE.parts:
        current = current / name
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            if not create:
                raise ValueError('no cache directory')
            try:
                current.mkdir(mode=0o700)
            except FileExistsError:
                pass
            mode = current.lstat().st_mode
        if not stat.S_ISDIR(mode):
            raise ValueError('nonordinary cache directory')
    return current


def _load(path, key):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        status = os.fstat(stream.fileno())
        if not stat.S_ISREG(status.st_mode) or status.st_size > MAX_TOTAL_BYTES:
            raise ValueError('nonordinary or oversized entry')
        raw = stream.read(MAX_TOTAL_BYTES + 1)
        if len(raw) > MAX_TOTAL_BYTES:
            raise ValueError('entry grew beyond size bound')
    envelope = precedent._strict_json(raw)
    if (type(envelope) is not dict or set(envelope) != {'payload', 'sha256'} or
            type(envelope['payload']) is not dict or
            digest(canonical(envelope['payload'])) != envelope['sha256']):
        raise ValueError('payload digest/schema mismatch')
    payload = envelope['payload']
    if set(payload) != {'key', 'dependencies', 'value'} or canonical(payload['key']) != canonical(key):
        raise ValueError('entry key/schema mismatch')
    result = unpack(payload['value'])
    start = time.perf_counter()
    verify(payload['dependencies'])
    return result, payload['dependencies'], time.perf_counter() - start


def _publish(root, name, raw):
    if len(raw) > MAX_TOTAL_BYTES:
        raise ValueError('oversized entry')
    directory = _directory(root, True)
    temporary = None
    try:
        fd, temporary = tempfile.mkstemp(prefix='.v1-tmp-', dir=directory)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, directory / name)
        temporary = None
        _evict(directory, name)
    finally:
        if temporary is not None:
            os.unlink(temporary)


def _evict(directory, keep):
    files = {}
    now = time.time()
    for path in directory.iterdir():
        own_entry = _NAME.fullmatch(path.name)
        own_temp = _TEMP.fullmatch(path.name)
        if not own_entry and not own_temp:
            continue
        try:
            status = path.lstat()
        except FileNotFoundError:
            # Another publisher/evictor may replace or remove a listed name.
            continue
        if not stat.S_ISREG(status.st_mode):
            continue
        if own_temp:
            if now - status.st_mtime > STALE_TEMP_SECONDS:
                path.unlink(missing_ok=True)
            continue
        # Concurrent replacements can make readdir repeat a name. Count each
        # entry once, and never mistake duplicate enumeration for extra files.
        files[path.name] = (path.name == keep, status.st_mtime_ns, path.name, status.st_size)
    total, count = 0, 0
    for _, _, name, size in sorted(files.values(), reverse=True):
        if count < MAX_ENTRIES and total + size <= MAX_TOTAL_BYTES:
            total += size
            count += 1
        else:
            (directory / name).unlink(missing_ok=True)


def _include(parent, rows, invalid=None):
    if parent is not None:
        for kind, path, arg, value in rows:
            parent.observe(kind, path, arg, value)
        if invalid:
            parent.invalid = invalid


_tools = (precedent.CODE_ROOT / 'tools').resolve()
_identity_frozen = None
_identity_poisoned = False


def implementation_identity():
    """Projection identity rules, excluding only the caller's __main__ file."""
    global _identity_frozen, _identity_poisoned
    if _identity_poisoned:
        raise ValueError('implementation changed during this process')
    started = precedent._process_start_ns()
    if started is None:
        raise ValueError('process start time unavailable')
    bound = started - precedent.HOT_EDIT_MARGIN_NS
    identity = {'code_sha256': precedent._code_digest(precedent.CODE_ROOT, bound),
                'runtime': precedent._runtime()}
    if _identity_frozen is None:
        _identity_frozen = identity
    if identity != _identity_frozen:
        _identity_poisoned = True
        raise ValueError('implementation changed during this process')
    stdlib = {Path(sysconfig.get_paths()[name]).resolve() for name in ('stdlib', 'platstdlib')}
    modules = []
    for name, module in sorted(dict(sys.modules).items()):
        file = getattr(module, '__file__', None)
        if name == '__main__' or not isinstance(file, str):
            continue
        path = Path(file).resolve()
        if path.is_relative_to(_tools):
            if path.suffix != '.py' and path.relative_to(precedent.CODE_ROOT) not in precedent.ENTRY_SCRIPTS:
                raise ValueError(f'loaded tools module has no source: {name}')
            if not path.is_file():
                raise ValueError(f'loaded tools module missing: {name}')
            continue
        if (any(path.is_relative_to(base) for base in stdlib) and
                not any(part in ('site-packages', 'dist-packages') for part in path.parts)):
            continue
        if path.stat().st_mtime_ns >= bound:
            raise ValueError(f'loaded module modified after process start: {name}')
        modules.append([name, str(path), digest(path.read_bytes())])
    return {**identity, 'modules': modules}


def predecessor(manifest, directory, seal, outputs_only, compute):
    """A failure of compute is never caught; all cache faults only cost replay."""
    if not enabled():
        return compute()
    parent = _active.get()
    root = manifest.root
    # Cache management and identity checks are not business inputs. In a nested
    # scope, hide only this I/O; successful observations are explicitly composed.
    with paused():
        try:
            # The historical task predicate imports this validator lazily.
            __import__('ai_state_check')
            implementation = implementation_identity()
            key = {'format': FORMAT, 'implementation': implementation,
                   'root': str(root.resolve()), 'directory': str(Path(directory).resolve()),
                   'root_argument': str(root), 'directory_argument': str(Path(directory)),
                   'cwd': os.getcwd(),
                   'seal_sha256': digest(canonical(seal)), 'outputs_only': outputs_only,
                   'manifest_sha256': digest(manifest.raw_bytes)}
            name = 'v1-' + digest(canonical(key)) + '.json'
        except Exception as error:
            event('skip', f'identity: {error}')
            key = None
    if key is None:
        # Restore the enclosing recorder before falling back, so its result still
        # includes every input even when this inner key cannot be used.
        return compute()
    with paused():
        try:
            result, rows, seconds = _load(_directory(root, False) / name, key)
            if implementation_identity() != implementation:
                raise ValueError('implementation changed')
        except Exception as error:
            event('miss', str(error), directory=str(directory), outputs_only=outputs_only)
            hit = False
        else:
            event('hit', 'all dependencies reverified', dependencies=dict(Counter(r[0] for r in rows)),
                  verification_seconds=seconds, file=name)
            hit = True
    if hit:
        _include(parent, rows)
        return result
    # Establish cache usability before spending time recording a cold replay.
    with paused():
        try:
            _directory(root, True)
            usable = True
        except Exception as error:
            event('skip', f'cache directory: {error}')
            usable = False
    if not usable:
        return compute()
    recorder = Recorder()
    with recording(recorder):
        result = compute()
    rows = recorder.rows()
    _include(parent, rows, recorder.invalid)
    if parent is not None:
        # Publish only the requested outer predecessor. Nested hits are useful
        # when a newer round extends a prior run, but publishing every older
        # miss would evict those recent keys and serialize the whole chain N times.
        with paused():
            event('skip', 'nested miss composed into outer result')
        return result
    with paused():
        try:
            if recorder.invalid:
                raise ValueError(recorder.invalid)
            start = time.perf_counter()
            verify(rows)
            seconds = time.perf_counter() - start
            if implementation_identity() != implementation:
                raise ValueError('implementation changed')
            value = pack(result)
            if pack(unpack(value)) != value:
                raise ValueError('value is not lossless')
            payload = {'key': key, 'dependencies': rows, 'value': value}
            raw = canonical({'payload': payload, 'sha256': digest(canonical(payload))})
            _publish(root, name, raw)
            event('publish', 'verified historical result', file=name, bytes=len(raw),
                  dependencies=dict(Counter(r[0] for r in rows)), verification_seconds=seconds)
        except Exception as error:
            event('skip', str(error))
    return result
