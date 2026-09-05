"""Independent metric behavior, including exact migration loss and overlap."""
import unittest

from tools.i18nlib.production_review_v2_lite_progress import Progress
from tools.i18nlib import production_review_v2_lite_queue as queue


def entry(revision):
    return {"entry_revision_identity": revision}


def row(revision, state="done", digest=None):
    return (revision, "logical-" + revision, state, "batch", 1, digest or revision, "stamp")


def result(revision, *, surface="OK", level="surface_only"):
    return {"entry_revision_identity": revision, "surface_verdict": surface, "completion_level": level}


def edge(old, new, disposition="revision_changed", *, old_logical=None, new_logical=None):
    return {"rows_by_old": {old: {
        "old_logical_entry_identity": old_logical or "logical-" + old,
        "new_logical_entry_identity": new_logical or "logical-" + old,
        "new_entry_revision_identity": new, "disposition": disposition}}}


class ProgressTests(unittest.TestCase):
    def assert_totals(self, report, expected):
        self.assertEqual(sum(cell["count"] for cell in report["classification"]), report["eligible"])
        self.assertEqual([m["count"] for m in report["metrics"].values()], expected)
        for name, metric in report["metrics"].items():
            self.assertEqual(sum(cell["count"] for cell in report["classification"] if cell[name]), metric["count"])
            self.assertEqual(metric["denominator"], report["eligible"])

    def test_surface_deep_both_repair_duplicates_and_superseded_repair(self):
        progress = Progress([entry(x) for x in "abcdef"])
        rows = [row("a"), row("b"), row("c"), row("d", "repair_required"),
                row("e", "repair_required", "old-e")]
        results = [result("a"), result("b", surface=None, level="deep_reviewed"),
                   result("c", surface="ISSUE", level="deep_reviewed"),
                   result("d", surface="ISSUE", level="deep_reviewed"),
                   result("e", surface="ISSUE", level="deep_reviewed")]
        progress.observe(rows, rows, results, [])
        progress.observe(rows, rows, results, [])
        # Latest surface-only result resolves repair but does not erase deep coverage.
        latest = row("e", digest="new-e")
        progress.observe([latest], [latest], [result("e")], [])
        report = progress.report(rows[:-1] + [latest])
        self.assert_totals(report, [4, 4, 1, 0])
        self.assertEqual(report["committed_done_by_completion_level"], {"surface_only": 2, "deep_reviewed": 2})

    def test_changed_reverted_identity_cannot_regain_old_raw_coverage(self):
        progress = Progress([entry("a")])
        chain = [edge("a", "b"), edge("b", "a", old_logical="logical-a")]
        rows = [row("a")]
        carried = queue._unchanged_rows_through_chain(rows, chain, {"a"})
        self.assertEqual(carried, [])
        progress.observe(rows, carried, [result("a")], chain)
        self.assert_totals(progress.report([]), [0, 0, 0, 1])
        self.assertEqual(progress.report([])["invalidated_without_current_review"], 1)
        # An actual new review restores coverage; the historical loss remains.
        progress.observe(rows, rows, [result("a")], [])
        self.assert_totals(progress.report(rows), [1, 0, 0, 1])
        self.assertEqual(progress.report(rows)["invalidated_without_current_review"], 0)

    def test_exact_chain_moves_removed_unmapped_ambiguous_and_missing_links(self):
        for disposition in ("removed", "unmapped", "ambiguous"):
            with self.subTest(disposition=disposition):
                progress = Progress([entry("a")])
                progress.observe([row("a")], [], [result("a")], [edge("a", None, disposition)])
                self.assert_totals(progress.report([]), [0, 0, 0, 0])
        progress = Progress([entry("c"), entry("unrelated")])
        chain = [edge("a", "b"), edge("b", "c", "logical_moved",
                 old_logical="logical-a", new_logical="logical-c")]
        progress.observe([row("a")], [], [result("a")], chain)
        self.assert_totals(progress.report([]), [0, 0, 0, 1])
        for broken in ([edge("a", "b"), edge("other", "c")],
                       [edge("a", "c", old_logical="wrong")],
                       [edge("a", "outside")]):
            progress = Progress([entry("c")])
            progress.observe([row("a")], [], [result("a")], broken)
            self.assert_totals(progress.report([]), [0, 0, 0, 0])

    def test_unchanged_chain_and_zero_eligible(self):
        progress = Progress([entry("a")])
        rows = [row("a")]
        chain = [edge("a", "a", "unchanged")] * 3
        progress.observe(rows, queue._unchanged_rows_through_chain(rows, chain, {"a"}), [result("a")], chain)
        self.assert_totals(progress.report(rows), [1, 0, 0, 0])
        empty = Progress([]).report([])
        self.assert_totals(empty, [0, 0, 0, 0])
        self.assertTrue(all(metric["ratio"] is None for metric in empty["metrics"].values()))
