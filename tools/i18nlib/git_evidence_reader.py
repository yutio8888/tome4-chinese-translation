"""Immutable Git bytes cached only inside one synchronous projection call.

Also caches objects *derived* from those bytes, keyed by the same immutable
content identity.  A projection revisits the same catalog blobs dozens of
times (97 batch base commits resolve to 43 distinct catalog contents), and
re-parsing identical bytes cannot produce a different answer.

Raw blob *bytes* are the one cache with a hard budget: a full-history replay
touches a few GiB of historical catalog/manifest bytes but only needs a bounded
window at a time, so an LRU keyed by blob OID keeps at most
``BLOB_CACHE_LIMIT_BYTES``.  A single blob larger than the budget is returned
uncached.  Tree bytes keep their unbounded cache; they are two orders of
magnitude smaller and are re-decoded by consumers.

The scope also owns the projection-local row and tuple pools used to reuse
complete, equal canonical rows and compact migration mappings across catalogs.
They are keyed by content, never by revision identity alone, and are dropped in
``projection_scope``'s ``finally`` together with the reader itself.
"""
from __future__ import annotations

from collections import OrderedDict
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
import re
from typing import Callable, Iterator


BLOB_CACHE_LIMIT_BYTES = 128 * 1024 * 1024


class GitEvidenceReader:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.blobs: "OrderedDict[str, bytes]" = OrderedDict()
        self.blob_bytes = 0
        self.trees: dict[str, bytes] = {}
        self.derived: dict[tuple[str, str], object] = {}
        # Canonical digest -> (canonical digest string, complete equal row).
        self.rows: dict[str, tuple[str, dict]] = {}
        # Complete compact migration tuple -> the one pooled equal tuple.
        self.tuples: dict[tuple, tuple] = {}

    def read(self, kind: str, object_id: str, load: Callable[[], bytes]) -> bytes:
        if kind == "blob":
            return self._read_blob(object_id, load)
        cache = self.trees
        if object_id not in cache:
            cache[object_id] = load()
        return cache[object_id]

    def _read_blob(self, object_id: str, load: Callable[[], bytes]) -> bytes:
        cached = self.blobs.get(object_id)
        if cached is not None:
            self.blobs.move_to_end(object_id)
            return cached
        data = load()
        limit = BLOB_CACHE_LIMIT_BYTES
        if len(data) > limit:
            # Too large to hold; return it without displacing the LRU window.
            return data
        self.blobs[object_id] = data
        self.blob_bytes += len(data)
        while self.blob_bytes > limit and self.blobs:
            _evicted_id, evicted = self.blobs.popitem(last=False)
            self.blob_bytes -= len(evicted)
        return data

    def derive(self, kind: str, identity: str, load: Callable[[], object]) -> object:
        key = (kind, identity)
        if key not in self.derived:
            self.derived[key] = load()
        return self.derived[key]

    def intern_row(self, digest: str, row: dict) -> tuple[str, dict]:
        """Reuse one complete canonical row only when the digest AND row match.

        Callers on the hot path hold an already verified reader (one
        ``active_reader`` lookup per catalog, not per row), so this method never
        re-resolves the root.  A digest alone is not enough: a SHA-256 collision
        must never silently bind one catalog to another catalog's bytes, so the
        whole row is compared before the pooled object is handed back.
        """
        pooled = self.rows.get(digest)
        if pooled is not None:
            if pooled[1] == row:
                return pooled
            # Same digest, different content: never merge, never overwrite.
            return digest, row
        self.rows[digest] = (digest, row)
        return digest, row

    def intern_tuple(self, value: tuple) -> tuple:
        """Reuse one complete compact mapping tuple by its exact value."""
        pooled = self.tuples.get(value)
        if pooled is None:
            self.tuples[value] = value
            return value
        return pooled


_active: ContextVar[GitEvidenceReader | None] = ContextVar("git_evidence_reader", default=None)


def active_reader(root: Path) -> GitEvidenceReader | None:
    """The reader for this exact root inside the current projection, else None."""
    reader = _active.get()
    if reader is None or reader.root != root.resolve():
        return None
    return reader


@contextmanager
def projection_scope(root: Path) -> Iterator[None]:
    # Always create a fresh scope, including nested projections. Reset on errors
    # restores the enclosing reader; clearing also releases any retained context.
    reader = GitEvidenceReader(root)
    token = _active.set(reader)
    try:
        yield
    finally:
        _active.reset(token)
        reader.blobs.clear()
        reader.blob_bytes = 0
        reader.trees.clear()
        reader.derived.clear()
        reader.rows.clear()
        reader.tuples.clear()


def read(root: Path, kind: str, object_id: str, git: Callable[..., bytes],
         *args: str) -> bytes:
    reader = _active.get()
    if reader is None or reader.root != root.resolve():
        return git(root, *args, object_id)
    if re.fullmatch(r"[0-9a-f]{40}", object_id) is None:
        # Resolve the expression BEFORE peeling: in HEAD:path^{blob}, Git
        # interprets the suffix as part of the path, not a type assertion.
        # Aliases are resolved every time, never stored as cache keys.
        resolved = git(root, "rev-parse", "--verify", object_id).decode("ascii").strip()
        if re.fullmatch(r"[0-9a-f]{40}", resolved) is None:
            return git(root, *args, object_id)
        object_id = git(root, "rev-parse", "--verify", f"{resolved}^{{{kind}}}").decode("ascii").strip()
    if re.fullmatch(r"[0-9a-f]{40}", object_id) is None:
        # Preserve the underlying Git/error contract for non-SHA1 repositories.
        return git(root, *args, object_id)
    return reader.read(kind, object_id, lambda: git(root, *args, object_id))


def derive(root: Path, kind: str, identity: str, load: Callable[[], object]) -> object:
    """Reuse an object derived from immutable Git content within one projection.

    Outside a projection scope this is a plain call, so behaviour is unchanged.
    """
    reader = _active.get()
    if reader is None or reader.root != root.resolve():
        return load()
    return reader.derive(kind, identity, load)


def intern_row(root: Path, digest: str, row: dict) -> tuple[str, dict]:
    """Scoped convenience wrapper around :meth:`GitEvidenceReader.intern_row`.

    Hot per-row loops must not call this: it resolves and verifies the root on
    every call.  They fetch ``active_reader(root)`` once per catalog instead and
    then call the reader method directly.  Outside a projection scope this is
    the identity function.
    """
    reader = active_reader(root)
    if reader is None:
        return digest, row
    return reader.intern_row(digest, row)


def intern_tuple(root: Path, value: tuple) -> tuple:
    """Scoped convenience wrapper around :meth:`GitEvidenceReader.intern_tuple`.

    Same rule as :func:`intern_row`: per-row loops use the verified reader
    directly instead of re-resolving the root for every tuple.
    """
    reader = active_reader(root)
    if reader is None:
        return value
    return reader.intern_tuple(value)
