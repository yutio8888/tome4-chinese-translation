"""Versioned tracked-evidence capacity policies.

The combined production budget is a *policy*, not a constant.  Raising the
current ceiling must not retroactively widen the acceptance domain of evidence
that was recorded under the old one, so every receipt is read under the policy
it was written against:

* receipts with no capacity policy binding (gates schema 1 and 2) are historical
  and are always read under :data:`LEGACY_POLICY_ID`, whatever the current
  policy happens to be;
* receipts that carry ``capacity_policy_id`` / ``capacity_policy_sha256``
  (gates schema 3) are read under exactly the policy they name, and the digest
  must match this registry's text for that policy.

A policy is identified by its id and bound by the SHA-256 of its canonical
document, so a receipt cannot be reinterpreted by editing a limit in place:
changing the number changes the digest, and the old receipt stops matching.
"""
from __future__ import annotations

import hashlib
from typing import Any

from . import production_review as wp1

KIND = "production_review_v2_lite_capacity_policy_v1"

# Every policy ever used, kept forever.  Entries are append-only: deleting or
# editing one would orphan every receipt recorded under it.
_DOCUMENTS: dict[str, dict[str, Any]] = {
    "legacy-128mib-v1": {
        "schema_version": 1,
        "kind": KIND,
        "policy_id": "legacy-128mib-v1",
        "tracked_limit_bytes": 128 * 1024 * 1024,
    },
    "expanded-512mib-v1": {
        "schema_version": 1,
        "kind": KIND,
        "policy_id": "expanded-512mib-v1",
        "tracked_limit_bytes": 512 * 1024 * 1024,
    },
}

LEGACY_POLICY_ID = "legacy-128mib-v1"
CURRENT_POLICY_ID = "expanded-512mib-v1"

POLICY_IDS = frozenset(_DOCUMENTS)


def document(policy_id: object) -> dict[str, Any]:
    """Return the canonical document for one known policy."""
    if not isinstance(policy_id, str) or policy_id not in _DOCUMENTS:
        raise wp1.ProductionReviewError(f"unknown capacity policy: {policy_id!r}")
    return dict(_DOCUMENTS[policy_id])


def canonical_bytes(policy_id: object) -> bytes:
    return wp1.canonical_bytes(document(policy_id))


def digest(policy_id: object) -> str:
    return hashlib.sha256(canonical_bytes(policy_id)).hexdigest()


def limit(policy_id: object) -> int:
    return document(policy_id)["tracked_limit_bytes"]


def resolve(policy_id: object, policy_sha256: object) -> int:
    """Return the byte ceiling a receipt was written against.

    Both the id and the digest must match this registry, so a receipt binds to
    the exact policy text rather than to a name that could be redefined later.
    """
    expected = digest(policy_id)
    if not isinstance(policy_sha256, str) or not wp1.SHA256_RE.fullmatch(policy_sha256):
        raise wp1.ProductionReviewError("capacity policy digest is not a lowercase SHA-256")
    if policy_sha256 != expected:
        raise wp1.ProductionReviewError(
            f"capacity policy digest does not match policy {policy_id!r}")
    return limit(policy_id)


def describe(byte_limit: int) -> str:
    """Render a ceiling the way the error messages state it."""
    if byte_limit % (1024 * 1024) == 0:
        return f"{byte_limit // (1024 * 1024)} MiB"
    return f"{byte_limit} bytes"


LEGACY_TRACKED_LIMIT = limit(LEGACY_POLICY_ID)
CURRENT_TRACKED_LIMIT = limit(CURRENT_POLICY_ID)
