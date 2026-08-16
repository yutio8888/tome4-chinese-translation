#!/usr/bin/env python3
"""Run the lightweight guard for active, runtime-neutral Paseo contracts."""

from __future__ import annotations

import sys
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
)
ACTIVE_FILES = ("AGENTS.md", *ROLE_FILES, *CONTRACT_FILES)

REQUIRED_MARKERS = {
    "AGENTS.md": ("role", "purpose", "PASEO_AGENT_ID", "ParentAgentId", "WAIT_USER"),
    ".ai/roles/executor.md": ("role=executor",),
    ".ai/roles/orchestrator.md": ("ORCHESTRATOR", "PASEO_AGENT_ID"),
    ".ai/roles/reviewer.md": ("role=reviewer", "purpose"),
    ".ai/roles/scout.md": ("role=scout",),
    ".ai/roles/senior-reviewer.md": ("role=senior-reviewer", "purpose"),
    "docs/paseo-orchestration-v2-contract.md": (
        "purpose=normal_review",
        "purpose=translation_contextual_v1",
        "candidate_ref",
        "orchestration_transport",
    ),
    "docs/paseo-translation-context-review-v1-contract.md": (
        "role=reviewer",
        "purpose=translation_contextual_v1",
        "candidate_identity",
        "dispatch_id",
    ),
}

# These are runtime identities or routing fields. Generic words such as
# "provider" and "model" remain allowed when describing the external API.
FORBIDDEN_RUNTIME_MARKERS = (
    "command-code-goat/",
    "opencode-go/",
    "openai-codex/",
    "gpt-5.6-",
    "claude-opus-",
    "runtime_tuple",
    "thinkingOptionId",
    "fallback_reason",
)


def main() -> int:
    errors: list[str] = []
    texts: dict[str, str] = {}

    for relative in ACTIVE_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing active file: {relative}")
            continue
        texts[relative] = path.read_text(encoding="utf-8")

    for relative, markers in REQUIRED_MARKERS.items():
        text = texts.get(relative, "")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative}: missing required marker {marker!r}")

    for relative, text in texts.items():
        for marker in FORBIDDEN_RUNTIME_MARKERS:
            if marker in text:
                errors.append(f"{relative}: fixed runtime marker {marker!r}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {len(texts)} active Paseo documents are role-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
