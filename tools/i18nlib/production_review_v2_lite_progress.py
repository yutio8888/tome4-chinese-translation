"""Invocation-local progress derived only from validated committed queue evidence."""
from __future__ import annotations

from collections import Counter
from typing import Any


class Progress:
    """Collect metadata during the existing replay, without changing business rows."""

    def __init__(self, entries: list[dict[str, Any]]):
        self.current = {row["entry_revision_identity"] for row in entries}
        self.surface: set[str] = set()
        self.deep: set[str] = set()
        self.invalidated: set[str] = set()
        self.levels: dict[str, str] = {}

    def observe(self, source_rows, valid_rows, results, chain):
        # valid_rows already obey the queue's exact unchanged-chain carry rule.
        by_revision = {row["entry_revision_identity"]: row for row in results}
        for row in valid_rows:
            result = by_revision[row[0]]
            if result["surface_verdict"] in {"OK", "ISSUE"}:
                self.surface.add(row[0])
            if result["completion_level"] == "deep_reviewed":
                self.deep.add(row[0])
            self.levels[row[5]] = result["completion_level"]
        for row in source_rows:
            revision, logical = row[:2]
            changed = False
            # Finite validated chain; stop at the first missing/ambiguous link.
            # Follow exact logical moves too, never infer a successor by text.
            for edge in chain:
                mapping = edge["rows_by_old"].get(revision)
                if (mapping is None or mapping["old_logical_entry_identity"] != logical or
                        mapping["disposition"] not in {"unchanged", "revision_changed", "logical_moved"}):
                    break
                successor = mapping["new_entry_revision_identity"]
                changed = changed or successor != revision
                revision, logical = successor, mapping["new_logical_entry_identity"]
            else:
                if changed and revision in self.current:
                    self.invalidated.add(revision)

    def report(self, overrides):
        latest = {row[0]: row[2] for row in overrides}
        repair = {revision for revision, state in latest.items() if state == "repair_required"}
        done_levels = Counter(self.levels[row[5]] for row in overrides if row[2] == "done")
        # The four flags are independent; all 16 cells are emitted, including
        # zeros, so each numerator and the shared denominator are reproducible.
        cells = Counter((revision in self.surface, revision in self.deep,
                         revision in repair, revision in self.invalidated)
                        for revision in self.current)
        classification = [
            {"surface_covered": s, "deep_reviewed": d, "pending_repair": r,
             "historical_revision_invalidated": i, "count": cells[s, d, r, i]}
            for s in (False, True) for d in (False, True)
            for r in (False, True) for i in (False, True)]
        eligible = len(self.current)
        counts = {"surface_covered": len(self.surface), "deep_reviewed": len(self.deep),
                  "pending_repair": len(repair),
                  "historical_revision_invalidated": len(self.invalidated)}
        return {
            "basis": "committed_evidence", "eligible": eligible,
            "metrics": {key: {"count": count, "denominator": eligible,
                              "ratio": count / eligible if eligible else None}
                        for key, count in counts.items()},
            "invalidated_without_current_review": len(self.invalidated - self.surface - self.deep),
            "classification": classification,
            "committed_done_by_completion_level": {
                level: done_levels[level] for level in ("surface_only", "deep_reviewed")},
        }
