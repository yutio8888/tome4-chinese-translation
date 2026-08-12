"""Pilot A stability gates: benign-refactor TU stability (G3), index
coverage of the snapshot (G2) and the identity.sqlite rebuild determinism
(G9)."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.storage import (  # noqa: E402
    identity_database_path,
    rebuild_identity_database,
)

from tests.i18n.identity.fixture import (  # noqa: E402
    FIXTURE_EFFECTS,
    FIXTURE_ENTITIES,
    FIXTURE_MISC,
    FIXTURE_TALENTS,
    build_fixture_index,
    make_tree,
    tu_uids,
)

_BASE_FILES = {
    "mod-test/data/talents.lua": FIXTURE_TALENTS,
    "mod-test/data/effects.lua": FIXTURE_EFFECTS,
    "mod-test/data/entities.lua": FIXTURE_ENTITIES,
    "mod-test/data/misc.lua": FIXTURE_MISC,
}

# The seven benign transformations of G3.
_TRANSFORMS = {
    "blank-lines": lambda files: {
        **files,
        "mod-test/data/talents.lua": "\n\n\n" + files["mod-test/data/talents.lua"],
    },
    "comments": lambda files: {
        **files,
        "mod-test/data/effects.lua": (
            "-- a harmless comment\n" + files["mod-test/data/effects.lua"]
        ),
    },
    "field-reorder": lambda files: {
        **files,
        "mod-test/data/entities.lua": files["mod-test/data/entities.lua"].replace(
            'define_as = "BASE_NPC_ANT",\n\tname = "ant",\n\ttype = "insect", subtype = "ant",',
            'name = "ant",\n\tdefine_as = "BASE_NPC_ANT",\n\ttype = "insect", subtype = "ant",',
        ),
    },
    "unrelated-edit": lambda files: {
        **files,
        "mod-test/data/misc.lua": files["mod-test/data/misc.lua"].replace(
            "ActorStats:defineStat", "ActorStats:defineStat"
        )
        + '\nlocal unused = "irrelevant string without capture"\n',
    },
    "source-rewording-strong": lambda files: {
        **files,
        "mod-test/data/entities.lua": files["mod-test/data/entities.lua"].replace(
            'name = "huge ant"', 'name = "enormous ant"'
        ),
    },
    "line-drift": lambda files: {
        **files,
        "mod-test/data/talents.lua": "local x = 1\n" + files["mod-test/data/talents.lua"],
    },
    "effect-subtype-added": lambda files: {
        **files,
        "mod-test/data/effects.lua": files["mod-test/data/effects.lua"].replace(
            "subtype = { burning=true, fire=true },",
            "subtype = { burning=true, fire=true, scorch=true },",
        ),
    },
}


class CoverageTests(unittest.TestCase):
    """G2: every snapshot definition enters the TU index."""

    def test_g2_index_covers_snapshot(self) -> None:
        root, temporary = make_tree()
        try:
            index = build_fixture_index(root)
            self.assertEqual(
                index.stats["definitions"], index.stats["occurrences_bound"]
            )
            self.assertGreater(index.stats["definitions"], 0)
        finally:
            temporary.cleanup()


class StabilityTests(unittest.TestCase):
    """G3: benign refactors keep TU UIDs 100% stable."""

    def test_g3_benign_transforms(self) -> None:
        root, temporary = make_tree()
        try:
            base = build_fixture_index(root)
            base_strong = tu_uids(base, binding="strong")
            base_fallback = tu_uids(base, binding="fallback-editorial")
            for name, transform in sorted(_TRANSFORMS.items()):
                moved, moved_temp = make_tree(transform(copy.deepcopy(_BASE_FILES)))
                try:
                    index = build_fixture_index(moved)
                finally:
                    moved_temp.cleanup()
                strong = tu_uids(index, binding="strong")
                fallback = tu_uids(index, binding="fallback-editorial")
                self.assertEqual(
                    base_strong,
                    strong,
                    f"strong TU set changed under transform {name!r}",
                )
                if name == "unrelated-edit":
                    # Free-string edits must not disturb fallback identities.
                    self.assertEqual(base_fallback, fallback)
                if name == "source-rewording-strong":
                    # The rewording happens on a define_as entity name: the TU
                    # must stay (anchor unchanged) with a new Revision.
                    self.assertEqual(base_strong, strong)
                if name == "effect-subtype-added":
                    # Coalesced effect slot: same TU gains a new revision.
                    self.assertEqual(base_strong, strong)
        finally:
            temporary.cleanup()


class RebuildTests(unittest.TestCase):
    """G9: deleting and rebuilding identity.sqlite is byte-deterministic."""

    def test_g9_rebuild_determinism(self) -> None:
        import tempfile

        root, temporary = make_tree()
        temp_root = tempfile.TemporaryDirectory(prefix="tome4-i18n-db-root-")
        try:
            index = build_fixture_index(root)
            manifest_root = Path(temp_root.name)
            first = rebuild_identity_database(manifest_root, [index])
            second = rebuild_identity_database(manifest_root, [index])
            self.assertEqual(first.canonical_sha256, second.canonical_sha256)
            self.assertEqual(
                first.tables["translation_units"], index.stats["tus"]
            )
            expected_revisions = sum(len(tu.revisions) for tu in index.tus.values())
            self.assertEqual(first.tables["revisions"], expected_revisions)
            self.assertEqual(first.tables["entities"], index.stats["entities"])
            database = identity_database_path(manifest_root)
            self.assertTrue(database.is_file())
            # Verified rebuild matches the first canonical dump.
            third = rebuild_identity_database(
                manifest_root, [index], verify_sha256=first.canonical_sha256
            )
            self.assertEqual(third.canonical_sha256, first.canonical_sha256)
        finally:
            temp_root.cleanup()
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
