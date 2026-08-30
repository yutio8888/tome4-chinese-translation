#!/usr/bin/env python3
"""Strict append-only ledger for translation review entry-revision states.

The ledger is the long-term state machine of
docs/translation-review-production-convergence-spec.md section 4, keyed by the
stable ``logical_entry_identity`` and the versioned
``entry_revision_identity``.  It records only persisted state transitions; it
never infers coverage from provider, model, profile, or runtime names, and a
deferred (``sampling_queued``) entry is never reported as deep-reviewed.

The file is JSONL: each line is the canonical compact UTF-8 JSON of exactly
one immutable transition record.  Records are only ever appended; rewriting,
deleting, or reordering history fails closed.  Every transition carries a
closed-set machine ``reason_code`` — free-text causes are not accepted — and
an immutable snapshot/handoff ``provenance`` binding (artifact kind plus
SHA-256); invalidation is reachable only for identity-change causes, closed
revisions may be identity-invalidated into a new revision, and preference
alone can never reopen anything.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
from typing import Any

import surface_screen_result_check as check


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 1
INITIAL_STATE = "queued"
TERMINAL_STATES = frozenset({"closed"})
INACTIVE_STATES = frozenset({"invalidated"} | TERMINAL_STATES)
RECORD_KEYS = frozenset({
    "schema_version", "logical_entry_identity", "entry_revision_identity",
    "from_state", "to_state", "reason_code", "provenance", "recorded_by",
    "recorded_at", "parent_revision_identity",
    "migration_from_logical_entry_identity",
})
ENTRY_STATES = frozenset({
    "queued", "deterministic_pass", "deterministic_failed", "screened",
    "sampling_queued", "deep_queued", "deep_reviewed", "revalidated",
    "finding_observed", "adjudication", "fixed", "no_fix_closed",
    "invalidated", "reopened", "closed",
})
# Immutable snapshot/handoff provenance: every transition must cite the
# immutable artifact bytes it derives from by kind and SHA-256.
PROVENANCE_KEYS = frozenset({"kind", "sha256"})
PROVENANCE_KINDS = frozenset({
    "deterministic_layer", "surface_handoff", "deep_handoff",
    "repair_handoff", "adjudication_record", "revalidation_record",
    "revision_freeze_record", "reopen_evidence_record", "identity_snapshot",
})
# Identity-change causes are the only legal route into ``invalidated``; a
# closed revision may also be identity-invalidated into a new revision, while
# preference alone can never reopen or invalidate anything.  A logical
# locator or source_tag change creates a new logical identity and is
# therefore a logical-migration cause: its successor must carry an explicit
# migration edge (see replay).
IDENTITY_CHANGE_CODES = frozenset({
    "source_changed", "fixed_source_identity_changed",
    "terminology_snapshot_changed", "rules_version_changed",
    "call_locator_changed", "source_tag_changed",
})
LOGICAL_MIGRATION_CODES = frozenset({
    "call_locator_changed", "source_tag_changed",
})
REOPEN_EVIDENCE_CODES = frozenset({
    "new_fidelity_evidence", "new_completeness_evidence",
    "new_grammar_evidence", "new_terminology_evidence",
    "new_runtime_evidence", "new_translationese_evidence",
})
# Closed machine reason codes per named (from, to) migration.  A transition is
# legal exactly when its reason_code is allowed for that pair, so free text
# and out-of-cause transitions fail closed.
REASON_CODES: dict[tuple[str | None, str], frozenset[str]] = {
    (None, "queued"): frozenset({"revision_frozen"}),
    ("queued", "deterministic_pass"): frozenset({"deterministic_layer_passed"}),
    ("queued", "deterministic_failed"): frozenset({"deterministic_check_failed"}),
    ("deterministic_failed", "deterministic_pass"): frozenset({
        "deterministic_correction_applied",
    }),
    ("deterministic_pass", "screened"): frozenset({"surface_screen_completed"}),
    ("screened", "sampling_queued"): frozenset({"surface_ok_deferred"}),
    ("screened", "deep_queued"): frozenset({"surface_ok_selected", "surface_issue"}),
    ("sampling_queued", "deep_queued"): frozenset({"deferred_sampled"}),
    ("deep_queued", "deep_reviewed"): frozenset({"deep_review_completed"}),
    ("deep_reviewed", "revalidated"): frozenset({"deep_ok_revalidated"}),
    ("deep_reviewed", "finding_observed"): frozenset({"deep_issue_observed"}),
    ("finding_observed", "adjudication"): frozenset({"finding_observed"}),
    # pending stays pending via re-adjudication; refuted|advisory close via
    # revalidation; confirmed closes only through repair fixed|no_fix_closed.
    ("adjudication", "adjudication"): frozenset({"re_adjudication_pending_evidence"}),
    ("adjudication", "revalidated"): frozenset({"adjudicated_refuted_or_advisory"}),
    ("adjudication", "fixed"): frozenset({"repair_confirmed_applied"}),
    ("adjudication", "no_fix_closed"): frozenset({"no_fix_confirmed_close"}),
    ("fixed", "revalidated"): frozenset({"repair_revalidated"}),
    ("no_fix_closed", "revalidated"): frozenset({"no_fix_revalidated"}),
    ("revalidated", "closed"): frozenset({"revision_closed"}),
    ("closed", "reopened"): REOPEN_EVIDENCE_CODES,
    ("reopened", "deep_queued"): frozenset({"reopen_dispatched"}),
}
for _from_state in sorted(ENTRY_STATES - {"invalidated"}):
    REASON_CODES[(_from_state, "invalidated")] = IDENTITY_CHANGE_CODES
ALL_REASON_CODES = frozenset(
    code for codes in REASON_CODES.values() for code in codes
)
# Each named (from_state, to_state) migration also binds the immutable
# provenance kinds that may cite its evidence: a truthful kind for one
# transition is not automatically truthful for another.  The key set is
# exactly REASON_CODES' key set, so every legal transition has a provenance
# policy and every provenance kind outside the policy fails closed.
PROVENANCE_POLICY: dict[tuple[str | None, str], frozenset[str]] = {
    (None, "queued"): frozenset({"revision_freeze_record"}),
    ("queued", "deterministic_pass"): frozenset({"deterministic_layer"}),
    ("queued", "deterministic_failed"): frozenset({"deterministic_layer"}),
    ("deterministic_failed", "deterministic_pass"): frozenset({"deterministic_layer"}),
    ("deterministic_pass", "screened"): frozenset({"surface_handoff"}),
    ("screened", "sampling_queued"): frozenset({"surface_handoff"}),
    ("screened", "deep_queued"): frozenset({"surface_handoff"}),
    ("sampling_queued", "deep_queued"): frozenset({"deep_handoff"}),
    ("deep_queued", "deep_reviewed"): frozenset({"deep_handoff"}),
    ("deep_reviewed", "revalidated"): frozenset({"revalidation_record"}),
    ("deep_reviewed", "finding_observed"): frozenset({"deep_handoff"}),
    ("finding_observed", "adjudication"): frozenset({"adjudication_record"}),
    ("adjudication", "adjudication"): frozenset({"adjudication_record"}),
    ("adjudication", "revalidated"): frozenset({"adjudication_record"}),
    ("adjudication", "fixed"): frozenset({"repair_handoff"}),
    ("adjudication", "no_fix_closed"): frozenset({"adjudication_record"}),
    ("fixed", "revalidated"): frozenset({"revalidation_record"}),
    ("no_fix_closed", "revalidated"): frozenset({"revalidation_record"}),
    ("revalidated", "closed"): frozenset({"revision_freeze_record"}),
    ("closed", "reopened"): frozenset({"reopen_evidence_record"}),
    ("reopened", "deep_queued"): frozenset({"deep_handoff"}),
}
for _from_state in sorted(ENTRY_STATES - {"invalidated"}):
    PROVENANCE_POLICY[(_from_state, "invalidated")] = frozenset({"identity_snapshot"})
assert set(PROVENANCE_POLICY) == set(REASON_CODES)


class LedgerError(Exception):
    """A ledger record or file violates the append-only contract."""


def _identity(value: object, label: str) -> str:
    if not isinstance(value, str) or not check.SHA256.fullmatch(value):
        raise LedgerError(f"{label} must be 64 lowercase hexadecimal characters")
    return value


def _state(value: object, label: str) -> str:
    if not isinstance(value, str) or value not in ENTRY_STATES:
        raise LedgerError(f"{label} must be a named ledger phase state")
    return value


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise LedgerError(f"{label} must be a non-empty string")
    return value


def _reason_code(value: object) -> str:
    if not isinstance(value, str) or value not in ALL_REASON_CODES:
        raise LedgerError("reason_code must be a closed-set machine cause")
    return value


def _provenance(value: object) -> dict[str, str]:
    if not isinstance(value, dict) or frozenset(value) != PROVENANCE_KEYS:
        raise LedgerError("provenance must have exactly kind and sha256")
    if value["kind"] not in PROVENANCE_KINDS:
        raise LedgerError("provenance kind is not a named artifact kind")
    if not isinstance(value["sha256"], str) or not check.SHA256.fullmatch(value["sha256"]):
        raise LedgerError("provenance sha256 must be 64 lowercase hexadecimal characters")
    return value


def validate_record(record: object) -> dict[str, Any]:
    """Validate one transition record's exact shape without replay context."""
    if not isinstance(record, dict) or frozenset(record) != RECORD_KEYS:
        raise LedgerError("ledger record must have exactly the eleven canonical keys")
    if type(record["schema_version"]) is not int or record["schema_version"] != SCHEMA_VERSION:
        raise LedgerError("ledger record schema_version must be integer 1")
    _identity(record["logical_entry_identity"], "logical_entry_identity")
    _identity(record["entry_revision_identity"], "entry_revision_identity")
    _state(record["to_state"], "to_state")
    from_state = record["from_state"]
    if from_state is not None:
        _state(from_state, "from_state")
    _reason_code(record["reason_code"])
    _provenance(record["provenance"])
    _nonempty(record["recorded_by"], "recorded_by")
    _nonempty(record["recorded_at"], "recorded_at")
    parent = record["parent_revision_identity"]
    if parent is not None:
        _identity(parent, "parent_revision_identity")
    migration = record["migration_from_logical_entry_identity"]
    if migration is not None:
        _identity(migration, "migration_from_logical_entry_identity")
    return record  # type: ignore[return-value]


def _reason_allowed(from_state: str | None, to_state: str, reason_code: str) -> bool:
    return reason_code in REASON_CODES.get((from_state, to_state), frozenset())


def _canonical_line(record: dict[str, Any]) -> bytes:
    return check.canonical_bytes(record)


def replay(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Replay the append-only history and return per-logical state.

    The mapping is ``logical_entry_identity -> {entry_revision_identity ->
    latest state}``.  Replay also enforces the transition-specific provenance
    policy and the logical-migration edge discipline.
    """
    revisions: dict[str, dict[str, dict[str, Any]]] = {}
    order: dict[str, list[str]] = {}
    revision_owner: dict[str, str] = {}
    last_invalidation_reason: dict[str, str] = {}
    pending_logical_migration: str | None = None
    # A logical-migration invalidation opens exactly one single-consumption
    # pending edge: it must be consumed immediately by the successor revision
    # citing it, and a consumed source can never be cited again (fork) or
    # spawn further revisions without consuming a new pending edge itself.
    consumed_logical_migrations: set[str] = set()
    for index, record in enumerate(records):
        try:
            validate_record(record)
        except LedgerError as error:
            raise LedgerError(f"ledger line {index + 1}: {error}") from error
        logical = record["logical_entry_identity"]
        revision = record["entry_revision_identity"]
        from_state = record["from_state"]
        to_state = record["to_state"]
        allowed_kinds = PROVENANCE_POLICY.get((from_state, to_state))
        if allowed_kinds is None:
            raise LedgerError(
                f"ledger line {index + 1}: transition {from_state!r} -> {to_state!r} "
                "is not a named migration"
            )
        if record["provenance"]["kind"] not in allowed_kinds:
            raise LedgerError(
                f"ledger line {index + 1}: provenance kind "
                f"{record['provenance']['kind']!r} is not allowed for the "
                f"transition {from_state!r} -> {to_state!r}"
            )
        # A logical-cause invalidation must be followed immediately by the
        # successor revision carrying the explicit migration edge.  A logical
        # identity can never migrate to itself, and the pending edge is
        # single consumption: only the adjacent successor record may cite it.
        successor = False
        if pending_logical_migration is not None:
            successor = (
                revision not in revisions.get(logical, {})
                and record["migration_from_logical_entry_identity"]
                == pending_logical_migration
                and logical != pending_logical_migration
            )
            if not successor:
                raise LedgerError(
                    f"ledger line {index + 1}: logical migration of "
                    f"{pending_logical_migration} must be followed immediately "
                    "by the successor revision carrying its migration edge"
                )
        # An entry_revision_identity is globally unique: the revision recipe
        # binds it to exactly one logical identity, so reuse across logical
        # identities is an identity collision and fails closed.
        previous_owner = revision_owner.setdefault(revision, logical)
        if previous_owner != logical:
            raise LedgerError(
                f"ledger line {index + 1}: entry_revision_identity {revision} is "
                f"reused across logical identities"
            )
        chain = revisions.setdefault(logical, {})
        sequence = order.setdefault(logical, [])
        if revision not in chain:
            # A new revision must start the named state machine.
            if from_state is not None or to_state != INITIAL_STATE:
                raise LedgerError(
                    f"ledger line {index + 1}: revision {revision} must start at {INITIAL_STATE}"
                )
            if not _reason_allowed(None, to_state, record["reason_code"]):
                raise LedgerError(
                    f"ledger line {index + 1}: reason_code is not allowed for starting {to_state!r}"
                )
            previous = sequence[-1] if sequence else None
            parent = record["parent_revision_identity"]
            migration = record["migration_from_logical_entry_identity"]
            if previous is None:
                if parent is not None:
                    raise LedgerError(
                        f"ledger line {index + 1}: first revision of a logical identity must have a null parent"
                    )
                if migration is not None:
                    if migration in consumed_logical_migrations:
                        raise LedgerError(
                            f"ledger line {index + 1}: logical migration edge from "
                            f"{migration} was already consumed by a successor; "
                            "fork or reuse is rejected"
                        )
                    migrated = revisions.get(migration)
                    if migrated is None or not migrated or \
                            list(migrated.values())[-1] != "invalidated":
                        raise LedgerError(
                            f"ledger line {index + 1}: migration edge must cite an invalidated logical identity"
                        )
                    if last_invalidation_reason.get(migration) not in LOGICAL_MIGRATION_CODES:
                        raise LedgerError(
                            f"ledger line {index + 1}: migration edge must cite a "
                            f"logical-identity change ({sorted(LOGICAL_MIGRATION_CODES)})"
                        )
                    consumed_logical_migrations.add(migration)
            else:
                # New revision under the same logical identity: only an
                # invalidated predecessor may spawn it.  A migration edge is
                # legal only as the adjacent successor of a pending logical
                # migration (a truthful revert to a previously used logical
                # identity cites the different pending source); any other
                # edge fails closed.  A logical identity that already
                # migrated away may not spawn further revisions without
                # consuming a new pending edge (fork/resurrection).
                if parent != previous:
                    raise LedgerError(
                        f"ledger line {index + 1}: parent_revision_identity must bind the "
                        "latest invalidated revision of the same logical identity"
                    )
                latest_state = list(chain.values())[-1]
                if latest_state != "invalidated":
                    raise LedgerError(
                        f"ledger line {index + 1}: a new revision may only follow an invalidated one"
                    )
                if migration is not None:
                    if not successor:
                        raise LedgerError(
                            f"ledger line {index + 1}: a same-logical revision may only declare "
                            "the adjacent pending logical migration edge as its migration source"
                        )
                    consumed_logical_migrations.add(migration)
                    # C4-04: a truthful migration revival clears the revived
                    # identity's consumed-away marker, so later ordinary
                    # revision bumps under it remain legal; duplicate/fork
                    # citation of the consumed source stays rejected.
                    consumed_logical_migrations.discard(logical)
                elif logical in consumed_logical_migrations:
                    raise LedgerError(
                        f"ledger line {index + 1}: logical identity {logical} already "
                        "migrated away to a successor; spawning a further revision "
                        "without a migration edge is a fork"
                    )
            chain[revision] = to_state
            sequence.append(revision)
            if successor:
                # Single consumption: the pending edge dies with its successor.
                pending_logical_migration = None
            continue
        current = chain[revision]
        if from_state != current:
            raise LedgerError(
                f"ledger line {index + 1}: from_state {from_state!r} does not match "
                f"the replayed state {current!r}"
            )
        if not _reason_allowed(from_state, to_state, record["reason_code"]):
            raise LedgerError(
                f"ledger line {index + 1}: transition {from_state!r} -> {to_state!r} "
                f"with reason_code {record['reason_code']!r} is not a named migration"
            )
        chain[revision] = to_state
        if to_state == "invalidated":
            last_invalidation_reason[logical] = record["reason_code"]
            if record["reason_code"] in LOGICAL_MIGRATION_CODES:
                pending_logical_migration = logical
    for logical, chain in revisions.items():
        active = [
            revision for revision, state in chain.items()
            if state not in INACTIVE_STATES
        ]
        if len(active) > 1:
            raise LedgerError(
                f"logical identity {logical} has more than one active revision"
            )
    return revisions


def parse_ledger_bytes(raw: bytes, *, label: str = "ledger") -> list[dict[str, Any]]:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise LedgerError(f"{label} must not contain a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise LedgerError(f"{label} is not UTF-8: {error}") from error
    if text and not text.endswith("\n"):
        raise LedgerError(f"{label} must end with a newline after the last record")
    records: list[dict[str, Any]] = []
    lines = text.split("\n")[:-1] if text else []
    for number, line in enumerate(lines, start=1):
        if not line:
            raise LedgerError(f"{label} line {number} is empty")
        try:
            record = check.strict_json_bytes(line.encode("utf-8"), label=f"{label} line {number}")
        except (check.ContractError, check.InputError) as error:
            raise LedgerError(f"{label} line {number}: {error}") from error
        if not isinstance(record, dict):
            raise LedgerError(f"{label} line {number} must be a JSON object")
        try:
            if _canonical_line(record) != line.encode("utf-8"):
                raise LedgerError(
                    f"{label} line {number} is not canonical compact JSON"
                )
        except check.ContractError as error:
            raise LedgerError(f"{label} line {number}: {error}") from error
        records.append(record)
    seen: dict[bytes, int] = {}
    for number, record in enumerate(records, start=1):
        line = _canonical_line(record)
        if line in seen:
            raise LedgerError(
                f"{label} line {number} duplicates immutable line {seen[line]}"
            )
        seen[line] = number
    return records


def load_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.is_file() or path.is_symlink():
        raise LedgerError(f"ledger is not an ordinary file: {path}")
    return parse_ledger_bytes(path.read_bytes())


def append_record(path: Path, record: dict[str, Any]) -> str:
    """Validate and append one transition record; idempotent for the last line."""
    validate_record(record)
    line = _canonical_line(record)
    records = load_ledger(path) if path.is_file() else []
    if records:
        # The existing history must replay cleanly BEFORE the idempotent
        # return: malformed existing history can never report success, not
        # even as ALREADY_PRESENT.
        replay(records)
        if _canonical_line(records[-1]) == line:
            return "ALREADY_PRESENT"
        # An exact duplicate of any earlier immutable event is rejected even
        # when it would replay as a legal transition: re-appending it would
        # permanently corrupt the append-only history.
        if any(_canonical_line(record) == line for record in records):
            raise LedgerError(
                "record duplicates an immutable event already in the ledger; "
                "only the exact last line is idempotent"
            )
    # The proposed event must replay as a legal next event of the prospective
    # history — including the very first record of an empty ledger, whose
    # revision start must satisfy the same named machine as any later one.
    replay([*records, record])
    with open(path, "ab") as handle:
        handle.write(line + b"\n")
        handle.flush()
        os.fsync(handle.fileno())
    return "APPENDED"


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Honest per-logical coverage summary; deferred is never deep-reviewed."""
    revisions = replay(records)
    entries: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for logical, chain in revisions.items():
        # Insertion order of the replayed chain is the append-only creation order.
        latest_revision = list(chain)[-1]
        latest_state = chain[latest_revision]
        counts[latest_state] = counts.get(latest_state, 0) + 1
        entries.append({
            "logical_entry_identity": logical,
            "revision_count": len(chain),
            "latest_revision_identity": latest_revision,
            "latest_state": latest_state,
        })
    deferred = counts.get("sampling_queued", 0)
    return {
        "schema_version": SCHEMA_VERSION,
        "logical_entries": sorted(entries, key=lambda item: item["logical_entry_identity"]),
        "state_counts": dict(sorted(counts.items())),
        "deep_reviewed": counts.get("deep_reviewed", 0) + counts.get("revalidated", 0)
        + counts.get("closed", 0),
        "deferred_sampling_queued": deferred,
        "deferred_is_not_deep_reviewed": True,
    }


def _resolve(root: str, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise check.InputError(f"ledger path escapes the workspace: {relative}")
    resolved_root = Path(root).resolve()
    if any(
        (resolved_root / Path(*path.parts[:index])).is_symlink()
        for index in range(1, len(path.parts) + 1)
    ):
        raise check.InputError(f"ledger path traverses a symlink: {relative}")
    return resolved_root / path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("check", "append", "summary"))
    parser.add_argument("ledger")
    parser.add_argument("record", nargs="?")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)
    try:
        path = _resolve(args.root, args.ledger)
        if args.command == "check":
            records = load_ledger(path)
            replay(records)
            print(f"LEDGER_VERIFIED records={len(records)}")
            return 0
        if args.command == "summary":
            records = load_ledger(path)
            print(f"SUMMARY {check.canonical_bytes(summarize(records)).decode('utf-8')}")
            return 0
        if not args.record:
            raise LedgerError("append requires a record JSON file ('-' for stdin)")
        raw = sys.stdin.buffer.read() if args.record == "-" else Path(args.record).read_bytes()
        record = check.strict_json_bytes(raw, label="record")
        outcome = append_record(path, record)
        print(f"LEDGER_{outcome}")
        return 0
    except OSError as error:
        print(f"INPUT_ERROR: {error}")
        return 2
    except (LedgerError, check.ContractError, check.InputError) as error:
        kind = "INPUT_ERROR" if isinstance(error, check.InputError) else "LEDGER_FAILED"
        print(f"{kind}: {error}")
        return 2 if isinstance(error, check.InputError) else 1


if __name__ == "__main__":
    sys.exit(main())
