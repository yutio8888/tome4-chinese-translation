"""Incremental invalidation tests (contract/0.1-rc3 §8): G8 whole-set
canonical self-check, the §8.3 round-trip parity contract and the
affected-set mapping."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.config import ComponentSpec, SourceMount  # noqa: E402
from i18nlib.fingerprint import canonical_findings_form  # noqa: E402
from i18nlib.invalidation import (  # noqa: E402
    affected_for_source_domain,
    parity_check,
    section_to_source_git_path,
    source_git_path_to_section,
)
from i18nlib.invalidation import self_check as canonical_self_check  # noqa: E402
from i18nlib.invalidation import incremental_findings  # noqa: E402

from tests.i18n.fingerprint.test_fingerprint import _record  # noqa: E402


def _component(**overrides) -> ComponentSpec:
    defaults = dict(
        id="tome",
        translation="mod-tome.lua",
        copy_fragment=None,
        source_repository="engine",
        sources=(
            SourceMount(git_path="game/modules/tome", mount="mod-tome"),
            SourceMount(git_path="game/engines/default/data", mount="engine/data"),
        ),
        protected_source=None,
        source_baseline=None,
        extract_by_default=True,
        official_locale=None,
        full_output=None,
        addon_eligible=True,
    )
    defaults.update(overrides)
    return ComponentSpec(**defaults)


class SectionMappingTests(unittest.TestCase):
    def test_forward_mapping(self) -> None:
        component = _component()
        self.assertEqual(
            source_git_path_to_section(
                component, "game/modules/tome/data/talents/spells/fire.lua"
            ),
            "mod-tome/data/talents/spells/fire.lua",
        )
        self.assertEqual(
            source_git_path_to_section(component, "game/modules/tome/init.lua"),
            "mod-tome/init.lua",
        )
        self.assertIsNone(
            source_git_path_to_section(component, "game/modules/example/init.lua")
        )

    def test_round_trip_parity(self) -> None:
        """§8.3 parity: every real section must round-trip."""
        sections = [
            "mod-tome/data/talents/spells/fire.lua",
            "mod-tome/init.lua",
            "engine/data/quests/main.lua",
        ]
        self.assertEqual(parity_check(_component(), sections), [])
        broken = sections + ["mod-other/x.lua"]
        self.assertEqual(len(parity_check(_component(), broken)), 1)

    def test_affected_set_ignores_other_components(self) -> None:
        affected = affected_for_source_domain(
            _component(),
            [
                "game/modules/tome/data/x.lua",
                "game/modules/example/y.lua",
                "game/modules/tome/readme.txt",
            ],
        )
        self.assertEqual(affected.sections, {"mod-tome/data/x.lua"})


class IncrementalAlgorithmTests(unittest.TestCase):
    def test_f_new_keeps_unaffected_and_replaces_affected(self) -> None:
        all_records = {
            "affected": _record(tu_uid="TU-AFFECTED", fingerprint="a" * 64),
            "kept": _record(tu_uid="TU-KEPT", fingerprint="k" * 64),
        }
        recomputed = [_record(tu_uid="TU-AFFECTED", fingerprint="n" * 64)]
        result = incremental_findings(
            previous=list(all_records.values()),
            affected_tu_uids={"TU-AFFECTED"},
            recomputed=recomputed,
        )
        self.assertEqual(
            {record.tu_uid for record in result}, {"TU-AFFECTED", "TU-KEPT"}
        )
        self.assertNotIn(
            all_records["affected"].fingerprint,
            {record.fingerprint for record in result},
        )

    def test_g8_canonical_self_check(self) -> None:
        """G8: a consistent partition makes incremental == full byte-wise."""
        full = [
            _record(tu_uid="TU-A", fingerprint="a" * 64),
            _record(tu_uid="TU-B", fingerprint="b" * 64),
            _record(tu_uid="TU-C", fingerprint="c" * 64),
        ]
        affected = {"TU-B"}
        recomputed = [_record(tu_uid="TU-B", fingerprint="b2" * 32)]
        # An adversarial recompute that matches the full set.
        full_recomputed = [
            record for record in full if record.tu_uid != "TU-B"
        ] + recomputed
        incremental = incremental_findings(
            previous=full, affected_tu_uids=affected, recomputed=recomputed
        )
        self.assertEqual(
            canonical_findings_form(incremental),
            canonical_findings_form(full_recomputed),
        )
        self.assertTrue(
            canonical_self_check(incremental=incremental, full=full_recomputed)
        )
        # A wrong partition must be detected.
        self.assertFalse(
            canonical_self_check(incremental=incremental, full=full)
        )

    def test_self_check_writes_artifacts_on_mismatch(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="tome4-i18n-selfcheck-") as tmp:
            directory = Path(tmp)
            passed = canonical_self_check(
                incremental=[_record(fingerprint="x" * 64)],
                full=[_record(fingerprint="y" * 64)],
                artifact_directory=directory,
            )
            self.assertFalse(passed)
            self.assertTrue((directory / "incremental-canonical.jsonl").is_file())
            self.assertTrue((directory / "full-canonical.jsonl").is_file())


if __name__ == "__main__":
    unittest.main()
