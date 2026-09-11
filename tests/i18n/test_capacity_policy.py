"""Capacity policy registry and the version dispatch that reads receipts."""
from __future__ import annotations

import unittest
from unittest import mock

from tools.i18nlib import capacity_policy
from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as catalog
from tools.i18nlib import production_review_v2_lite_evidence as evidence


class CapacityPolicyTests(unittest.TestCase):
    def test_registry_is_append_only_and_digest_bound(self):
        self.assertEqual(capacity_policy.LEGACY_TRACKED_LIMIT, 128 * 1024 * 1024)
        self.assertEqual(capacity_policy.CURRENT_TRACKED_LIMIT, 512 * 1024 * 1024)
        self.assertIn(capacity_policy.LEGACY_POLICY_ID, capacity_policy.POLICY_IDS)
        self.assertIn(capacity_policy.CURRENT_POLICY_ID, capacity_policy.POLICY_IDS)
        # Two policies must never share a digest, or a receipt could be read
        # under the wrong ceiling while still verifying.
        digests = {policy: capacity_policy.digest(policy)
                   for policy in capacity_policy.POLICY_IDS}
        self.assertEqual(len(set(digests.values())), len(digests))

    def test_unknown_policy_and_wrong_digest_fail_closed(self):
        with self.assertRaisesRegex(wp1.ProductionReviewError, "unknown capacity policy"):
            capacity_policy.limit("no-such-policy-v9")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "does not match policy"):
            capacity_policy.resolve(capacity_policy.CURRENT_POLICY_ID,
                                    capacity_policy.digest(capacity_policy.LEGACY_POLICY_ID))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "not a lowercase SHA-256"):
            capacity_policy.resolve(capacity_policy.CURRENT_POLICY_ID, "nope")

    def test_editing_a_limit_in_place_invalidates_its_receipts(self):
        """A policy is bound by digest, so redefining it cannot reinterpret receipts."""
        recorded = capacity_policy.digest(capacity_policy.CURRENT_POLICY_ID)
        edited = capacity_policy.document(capacity_policy.CURRENT_POLICY_ID)
        edited["tracked_limit_bytes"] = 1024
        with mock.patch.dict(capacity_policy._DOCUMENTS,
                             {capacity_policy.CURRENT_POLICY_ID: edited}):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "does not match policy"):
                capacity_policy.resolve(capacity_policy.CURRENT_POLICY_ID, recorded)

    def test_describe_states_the_ceiling_actually_in_force(self):
        self.assertEqual(capacity_policy.describe(128 * 1024 * 1024), "128 MiB")
        self.assertEqual(capacity_policy.describe(512 * 1024 * 1024), "512 MiB")
        self.assertEqual(capacity_policy.describe(5), "5 bytes")


class ConsumerBoundaryTests(unittest.TestCase):
    """limit-1 / limit / limit+1 for every consumer of the current ceiling."""

    def test_evidence_prospective_bytes_boundary(self):
        # The real ceiling is asserted separately; the boundary itself is
        # exercised at a small patched ceiling so the test does not allocate
        # half a gigabyte to prove an inequality.
        self.assertEqual(evidence.MAX_TRACKED_BYTES, capacity_policy.CURRENT_TRACKED_LIMIT)
        with mock.patch.object(evidence, "MAX_TRACKED_BYTES", 16):
            for size in (15, 16):
                with self.subTest(size=size):
                    self.assertEqual(evidence.prospective_bytes([b"x" * size]), size)
            with self.assertRaisesRegex(wp1.ProductionReviewError, "exceeds 16 bytes"):
                evidence.prospective_bytes([b"x" * 17])

    def test_catalog_prospective_occupancy_boundary(self):
        self.assertEqual(catalog.TRACKED_LIMIT, capacity_policy.CURRENT_TRACKED_LIMIT)
        path = "evidence/production-review-v2-lite/boundary"
        with mock.patch.object(catalog, "TRACKED_LIMIT", 16):
            for size in (15, 16):
                with self.subTest(size=size):
                    self.assertEqual(catalog.prospective_occupancy({}, {path: b"x" * size}), size)
            with self.assertRaisesRegex(wp1.ProductionReviewError, "exceeds 16 bytes"):
                catalog.prospective_occupancy({}, {path: b"x" * 17})

    def test_the_two_module_constants_are_one_policy(self):
        """A single registry, so the four consumers cannot drift apart."""
        self.assertEqual(evidence.MAX_TRACKED_BYTES, catalog.TRACKED_LIMIT)


if __name__ == "__main__":
    unittest.main()
