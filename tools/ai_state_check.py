#!/usr/bin/env python3
"""Validate .ai/task/STATE.json schema and state-machine transition legality.

Mechanical enforcement tool for the multi-agent orchestration protocol
(AGENTS.md / .ai/roles/orchestrator.md). Uses only the Python standard
library. The authoritative schema, state set and transition table come from
.ai/task/SPEC.md (orchestration-dryrun-001).

Exit codes:
  0  file is valid
  1  schema or state-machine violation (details on stderr)
  2  file unreadable, not valid JSON, or usage error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Authoritative state set (SPEC.md).
STATES = (
    "PLAN",
    "IMPLEMENT",
    "IMPLEMENTATION_VALIDATE",
    "REVIEW",
    "ADJUDICATE",
    "FIX",
    "TEST",
    "RE_REVIEW",
    "FINAL_REVIEW",
    "FINAL_VALIDATE",
    "WAIT_USER",
    "STOP",
    "DONE",
)

_STATE_SET = frozenset(STATES)

# Authoritative transition table (SPEC.md). Terminal states have no outgoing
# transitions.
TRANSITIONS = {
    "PLAN": ("REVIEW", "IMPLEMENT"),
    "IMPLEMENT": ("IMPLEMENTATION_VALIDATE",),
    "IMPLEMENTATION_VALIDATE": ("REVIEW", "FIX", "STOP"),
    "REVIEW": ("ADJUDICATE",),
    "ADJUDICATE": ("FIX", "WAIT_USER", "FINAL_REVIEW"),
    "FIX": ("TEST",),
    "TEST": ("RE_REVIEW",),
    "RE_REVIEW": ("ADJUDICATE",),
    "FINAL_REVIEW": ("FINAL_VALIDATE", "FIX", "STOP"),
    "FINAL_VALIDATE": ("DONE", "FIX", "STOP"),
    "WAIT_USER": ("ADJUDICATE", "STOP"),
    "STOP": (),
    "DONE": (),
}

_TRANSITION_SET = {state: frozenset(dsts) for state, dsts in TRANSITIONS.items()}

# Required top-level fields in canonical order (SPEC.md).
REQUIRED_FIELDS = (
    "task_id",
    "mode",
    "baseline",
    "state",
    "cycle",
    "max_cycles",
    "step",
    "plan_rev",
    "executor",
    "reviewer",
    "accepted_findings",
    "rejected_findings",
    "deferred_findings",
    "last_action",
    "last_error",
    "retry_count",
    "updated_at",
)

# Required fields for the executor / reviewer objects.
_ROLE_FIELDS = ("provider", "model_id", "agent_id")

# Required fields for each history entry.
HISTORY_FIELDS = ("from", "to", "step", "at")


def _is_int(value: object) -> bool:
    """True for a real int; bool is not accepted as an int."""
    return isinstance(value, int) and not isinstance(value, bool)


def _check_str(value: object, name: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(
            f"field '{name}' must be a string, got {type(value).__name__}"
        )


def _check_int(value: object, name: str, minimum: int, errors: list[str]) -> None:
    if not _is_int(value):
        errors.append(
            f"field '{name}' must be an integer, got {type(value).__name__}"
        )
    elif value < minimum:
        errors.append(f"field '{name}' must be >= {minimum}, got {value}")


def _validate_role(obj: object, name: str, errors: list[str]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"field '{name}' must be an object, got {type(obj).__name__}")
        return
    missing = [field for field in _ROLE_FIELDS if field not in obj]
    if missing:
        errors.append(
            f"field '{name}' missing required field(s): " + ", ".join(missing)
        )
    for field in ("provider", "model_id"):
        if field in obj:
            _check_str(obj[field], f"{name}.{field}", errors)
    if "agent_id" in obj:
        agent_id = obj["agent_id"]
        if agent_id is not None and not isinstance(agent_id, str):
            errors.append(
                f"field '{name}.agent_id' must be a string or null, "
                f"got {type(agent_id).__name__}"
            )


def _validate_history(history: object, state: object, errors: list[str]) -> None:
    if not isinstance(history, list):
        errors.append(f"field 'history' must be a list, got {type(history).__name__}")
        return
    if not history:
        errors.append("field 'history' must be non-empty when present")
        return

    prev_to: object = None
    prev_step: object = None
    for index, item in enumerate(history):
        where = f"history[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{where} must be an object, got {type(item).__name__}")
            continue
        missing = [field for field in HISTORY_FIELDS if field not in item]
        if missing:
            errors.append(
                f"{where} missing required field(s): " + ", ".join(missing)
            )

        frm = item.get("from")
        to = item.get("to")
        step = item.get("step")
        at = item.get("at")

        if frm is not None:
            _check_str(frm, f"{where}.from", errors)
            if isinstance(frm, str) and frm not in _STATE_SET:
                errors.append(f"{where}.from has invalid state '{frm}'")
        if "to" in item:
            _check_str(to, f"{where}.to", errors)
            if isinstance(to, str) and to not in _STATE_SET:
                errors.append(f"{where}.to has invalid state '{to}'")
        if "step" in item:
            _check_int(step, f"{where}.step", 1, errors)
        if "at" in item:
            _check_str(at, f"{where}.at", errors)

        # Transition legality (SPEC.md table).
        if isinstance(frm, str) and isinstance(to, str):
            if frm in _STATE_SET and to in _STATE_SET:
                if to not in _TRANSITION_SET.get(frm, frozenset()):
                    errors.append(f"{where} illegal transition {frm} -> {to}")
        elif frm is None and isinstance(to, str):
            # A null source is only meaningful as the genesis entry.
            if index > 0 and prev_to is not None:
                errors.append(
                    f"{where}.from must equal previous 'to' ({prev_to}); "
                    "null 'from' is only allowed for the first entry"
                )

        # Adjacency: each entry (after the first) must continue the chain.
        if index > 0 and isinstance(frm, str) and prev_to is not None:
            if frm != prev_to:
                errors.append(
                    f"{where}.from ({frm}) does not match previous 'to' ({prev_to})"
                )

        # Steps must be strictly increasing across the history.
        if _is_int(step):
            if prev_step is not None and step <= prev_step:
                errors.append(
                    f"{where}.step ({step}) is not strictly increasing "
                    f"(previous {prev_step})"
                )
            prev_step = step

        prev_to = to

    # The last recorded state must agree with the current top-level state.
    if isinstance(history[-1], dict) and isinstance(state, str):
        last_to = history[-1].get("to")
        if last_to is not None and last_to != state:
            errors.append(
                f"history last 'to' ({last_to}) does not match field "
                f"'state' ({state})"
            )


def _validate_document(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return [
            f"top-level value must be an object, got {type(data).__name__}"
        ]

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        errors.append("missing required field(s): " + ", ".join(missing))

    if "task_id" in data:
        _check_str(data["task_id"], "task_id", errors)
        if not data["task_id"]:
            errors.append("field 'task_id' must not be empty")
    if "mode" in data:
        if data["mode"] not in ("implement", "review_only"):
            errors.append(
                "field 'mode' must be 'implement' or 'review_only', "
                f"got {data['mode']!r}"
            )
    if "baseline" in data and not isinstance(data["baseline"], dict):
        errors.append(
            f"field 'baseline' must be an object, got {type(data['baseline']).__name__}"
        )
    if "state" in data:
        _check_str(data["state"], "state", errors)
        if isinstance(data["state"], str) and data["state"] not in _STATE_SET:
            errors.append(f"field 'state' has invalid state '{data['state']}'")
    if "cycle" in data:
        _check_int(data["cycle"], "cycle", 0, errors)
    if "max_cycles" in data:
        _check_int(data["max_cycles"], "max_cycles", 1, errors)
    if (
        "cycle" in data
        and "max_cycles" in data
        and _is_int(data["cycle"])
        and _is_int(data["max_cycles"])
        and data["cycle"] > data["max_cycles"]
    ):
        errors.append(
            f"field 'cycle' ({data['cycle']}) exceeds 'max_cycles' "
            f"({data['max_cycles']})"
        )
    if "step" in data:
        _check_int(data["step"], "step", 1, errors)
    if "plan_rev" in data:
        _check_int(data["plan_rev"], "plan_rev", 0, errors)
    if "executor" in data:
        _validate_role(data["executor"], "executor", errors)
    if "reviewer" in data:
        _validate_role(data["reviewer"], "reviewer", errors)
    for field in ("accepted_findings", "rejected_findings", "deferred_findings"):
        if field in data and not isinstance(data[field], list):
            errors.append(
                f"field '{field}' must be a list, got {type(data[field]).__name__}"
            )
    if "last_action" in data:
        _check_str(data["last_action"], "last_action", errors)
    if "last_error" in data:
        _check_str(data["last_error"], "last_error", errors)
    if "retry_count" in data:
        _check_int(data["retry_count"], "retry_count", 0, errors)
    if "updated_at" in data:
        _check_str(data["updated_at"], "updated_at", errors)
    if "history" in data:
        _validate_history(data["history"], data.get("state"), errors)

    return errors


def validate(path: str) -> tuple[int, str]:
    """Validate a STATE.json file.

    Returns (exit_code, message):

    * 0 — file is valid (message is empty);
    * 1 — schema or state-machine violation (message lists the problems);
    * 2 — file unreadable or not valid JSON.
    """
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return 2, f"cannot read file '{path}': {exc}"
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return 2, f"invalid JSON in '{path}': {exc}"

    errors = _validate_document(data)
    if errors:
        return 1, "; ".join(errors)
    return 0, ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ai_state_check",
        description=(
            "Validate .ai/task/STATE.json schema and state-machine transitions."
        ),
    )
    parser.add_argument(
        "state_file",
        nargs="?",
        help="path to STATE.json (not needed with --list-transitions)",
    )
    parser.add_argument(
        "--list-transitions",
        action="store_true",
        help="print all states and allowed transitions, then exit",
    )
    args = parser.parse_args(argv)

    if args.list_transitions:
        print(f"States ({len(STATES)}): " + ", ".join(STATES))
        print("Transitions:")
        for src, dsts in TRANSITIONS.items():
            if dsts:
                print(f"  {src} -> " + ", ".join(dsts))
            else:
                print(f"  {src} -> (terminal, no outgoing transitions)")
        return 0

    if not args.state_file:
        parser.error("state_file is required unless --list-transitions is given")
    code, message = validate(args.state_file)
    if message:
        print(message, file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
