#!/usr/bin/env python3
"""Check live contract versions and canonical clause declarations/references.

Only identity syntax is enforced here. Behavioral validators and host-process
coverage are mapped in docs/paseo-clause-test-coverage.md.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROLE_FILES = (
    ".ai/roles/executor.md",
    ".ai/roles/orchestrator.md",
    ".ai/roles/reviewer.md",
    ".ai/roles/scout.md",
    ".ai/roles/senior-reviewer.md",
)

CONTRACT_FILES = (
    "docs/paseo-orchestration-v2-contract.md",
    "docs/paseo-translation-context-review-v1-contract.md",
    "docs/paseo-translation-context-review-v2-contract.md",
    "docs/paseo-translation-surface-screen-v1-contract.md",
)

ACTIVE_FILES = ("AGENTS.md", *ROLE_FILES, *CONTRACT_FILES)

ROLE_CLAUSE_REFERENCES = {
    ".ai/roles/executor.md": (
        "P2-SINGLE-WRITER", "P2-DIRECT-LINEAGE", "P2-FRESH-RETRY", "P2-STOP-CLOSED",
    ),
    ".ai/roles/orchestrator.md": (
        "P2-SINGLE-WRITER", "P2-DIRECT-LINEAGE", "P2-LIVE-ROUTING",
        "P2-RUNTIME-OBSERVATION", "P2-CANDIDATE-FREEZE",
        "P2-REVIEW-INDEPENDENCE", "P2-AUTHOR-PROVENANCE",
        "P2-MODEL-DIVERSITY", "P2-HARVEST-ARCHIVE", "P2-FRESH-RETRY",
        "P2-RECOVERY", "P2-STOP-CLOSED",
        "P2-TRANSLATION-CONVERGENCE",
        "P2-TRANSLATION-CONTEXT-V2",
        "P2-TRANSLATION-SURFACE-V1",
    ),
    ".ai/roles/reviewer.md": (
        "P2-READ-ONLY", "P2-CANDIDATE-FREEZE", "P2-REVIEW-INDEPENDENCE",
        "P2-STOP-CLOSED",
    ),
    ".ai/roles/scout.md": (
        "P2-READ-ONLY", "P2-DIRECT-LINEAGE", "P2-HARVEST-ARCHIVE",
    ),
    ".ai/roles/senior-reviewer.md": (
        "P2-READ-ONLY", "P2-CANDIDATE-FREEZE", "P2-REVIEW-INDEPENDENCE",
        "P2-STOP-CLOSED",
    ),
}

ROLE_CONTRACT_PATH = "docs/paseo-orchestration-v2-contract.md"

CONTRACT_VERSIONS = dict(zip(CONTRACT_FILES, (
    "paseo-orchestration/2.25-draft", "translation-contextual/1.6",
    "translation-contextual/2.0", "translation-surface-screen/1.0",
)))
EXPECTED_CLAUSES = frozenset(
    clause for clauses in ROLE_CLAUSE_REFERENCES.values() for clause in clauses
)
CLAUSE_REFERENCE = re.compile(r"\bP2-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*\b")
# The table under this exact heading is the sole declaration site. References
# in prose, later headings, examples or changelog rows cannot repair deletion.
DECLARATION_SECTION = "### 稳定条款 ID"
DECLARATION_ROW = re.compile(r"^\| `(P2-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)` \|[^\n]+\|$", re.M)


def declarations(text: str) -> list[str]:
    sections = text.split(DECLARATION_SECTION + "\n")
    if len(sections) != 2:
        return []
    body = re.split(r"^#{1,3} ", sections[1], maxsplit=1, flags=re.M)[0]
    return DECLARATION_ROW.findall(body)


def live_versions(text: str) -> list[str]:
    # Only the introductory header (before the first section) declares a
    # version. Historical mentions and examples never count.
    intro = re.split(r"^## ", text, maxsplit=1, flags=re.M)[0]
    matches = re.findall(
        r"^(?:> 契约版本：(?:`([^`\s]+)`(?:。|（)|([^`。\s]+)。)|版本 `([^`\s]+)`。)",
        intro, re.M,
    )
    return [next(value for value in groups if value) for groups in matches]



def main() -> int:
    errors: list[str] = []
    texts: dict[str, str] = {}
    for relative in ACTIVE_FILES:
        try:
            texts[relative] = (ROOT / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read active file: {relative}: {exc}")
    for relative, expected in CONTRACT_VERSIONS.items():
        versions = live_versions(texts.get(relative, ""))
        if versions != [expected]:
            errors.append(f"{relative}: live version must be exactly {expected!r}, got {versions!r}")
    declared = Counter(declarations(texts.get(ROLE_CONTRACT_PATH, "")))
    if set(declared) != EXPECTED_CLAUSES or any(n != 1 for n in declared.values()):
        errors.append(f"{ROLE_CONTRACT_PATH}: canonical clause declarations mismatch: "
                      f"missing={sorted(EXPECTED_CLAUSES - declared.keys())}, "
                      f"extra={sorted(declared.keys() - EXPECTED_CLAUSES)}, "
                      f"duplicates={sorted(k for k, n in declared.items() if n != 1)}")
    for relative, text in texts.items():
        references = set(CLAUSE_REFERENCE.findall(text))
        unknown = references - declared.keys()
        if unknown:
            errors.append(f"{relative}: undeclared clause references {sorted(unknown)}")
        if relative in ROLE_CLAUSE_REFERENCES:
            expected = set(ROLE_CLAUSE_REFERENCES[relative])
            if references != expected:
                errors.append(f"{relative}: role clause references mismatch: "
                              f"missing={sorted(expected - references)}, extra={sorted(references - expected)}")
            if ROLE_CONTRACT_PATH not in text:
                errors.append(f"{relative}: missing clause authority link")
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(texts)} active Paseo documents; 4 live versions, {len(declared)} clause declarations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
