#!/usr/bin/env python3
"""Fail-closed provenance preflight for contextual translation snapshots.

This intentionally uses a small, deterministic lexical scanner rather than the
locale loader or a Lua runtime.  It recognizes only ordinary quoted Lua 5.1
string literals where the preflight needs source text.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PAYLOAD_KEYS = frozenset(
    {
        "contract",
        "ordered_revision_keys",
        "translation_snapshot",
        "fixed_source_identity",
        "terminology_snapshot",
        "bounded_context",
        "rendered_briefing",
    }
)
SCOPE_KEYS = frozenset({"schema_version", "allowed_files", "anchor_scopes"})
ANCHOR_SCOPE_KEYS = frozenset({"file", "section_path", "ordered_titles"})
TITLE_MARKER = "[Book "


class InputError(ValueError):
    """The caller supplied an unsafe or malformed input artifact."""


class PreflightFailure(ValueError):
    """A well-formed scope proves that the snapshot is out of provenance."""


@dataclass(frozen=True)
class PreflightResult:
    status: str
    errors: tuple[str, ...] = ()

    @property
    def exit_code(self) -> int:
        return {"PREFLIGHT_VERIFIED": 0, "PREFLIGHT_FAILED": 1}.get(
            self.status, 2
        )


@dataclass(frozen=True)
class Call:
    start: int
    source: str


@dataclass(frozen=True)
class Section:
    start: int
    path: str


def _is_ident_start(char: str) -> bool:
    return char == "_" or char.isascii() and char.isalpha()


def _is_ident_part(char: str) -> bool:
    return char == "_" or char.isascii() and char.isalnum()


def _long_bracket_opening(text: str, start: int) -> tuple[int, str] | None:
    """Return the content start and closing delimiter for a long bracket."""
    if start >= len(text) or text[start] != "[":
        return None
    cursor = start + 1
    while cursor < len(text) and text[cursor] == "=":
        cursor += 1
    if cursor >= len(text) or text[cursor] != "[":
        return None
    return cursor + 1, "]" + "=" * (cursor - start - 1) + "]"


def _skip_long_bracket(text: str, start: int) -> int | None:
    """Return the end of a Lua long bracket, or None when it is not one."""
    opening = _long_bracket_opening(text, start)
    if opening is None:
        return None
    content_start, closing = opening
    end = text.find(closing, content_start)
    if end < 0:
        raise InputError("unterminated Lua long bracket")
    return end + len(closing)


def _skip_space_and_comments(text: str, cursor: int) -> int:
    while cursor < len(text):
        if text[cursor].isspace():
            cursor += 1
            continue
        if not text.startswith("--", cursor):
            return cursor
        cursor += 2
        long_end = _skip_long_bracket(text, cursor)
        if long_end is not None:
            cursor = long_end
            continue
        newline = text.find("\n", cursor)
        cursor = len(text) if newline < 0 else newline + 1
    return cursor


def _decode_lua_string(text: str, start: int) -> tuple[str, int]:
    if start >= len(text) or text[start] not in ("'", '"'):
        raise InputError("expected ordinary quoted Lua string")
    quote = text[start]
    cursor = start + 1
    decoded = bytearray()
    simple_escapes = {
        "a": 0x07,
        "b": 0x08,
        "f": 0x0C,
        "n": 0x0A,
        "r": 0x0D,
        "t": 0x09,
        "v": 0x0B,
        "\\": 0x5C,
        "\"": 0x22,
        "'": 0x27,
    }
    while cursor < len(text):
        char = text[cursor]
        if char == quote:
            try:
                return bytes(decoded).decode("utf-8", errors="strict"), cursor + 1
            except UnicodeDecodeError as error:
                raise InputError("Lua string does not contain valid UTF-8") from error
        if char in "\r\n":
            raise InputError("newline in ordinary Lua string")
        if char != "\\":
            decoded.extend(char.encode("utf-8"))
            cursor += 1
            continue
        cursor += 1
        if cursor >= len(text):
            raise InputError("unterminated Lua escape")
        escaped = text[cursor]
        if escaped in "\r\n":
            if escaped == "\r" and cursor + 1 < len(text) and text[cursor + 1] == "\n":
                cursor += 1
            decoded.append(0x0A)
            cursor += 1
            continue
        if escaped in "0123456789":
            end = cursor
            while end < len(text) and end < cursor + 3 and text[end] in "0123456789":
                end += 1
            value = int(text[cursor:end])
            if value > 255:
                raise InputError("Lua decimal escape exceeds 255")
            decoded.append(value)
            cursor = end
            continue
        if escaped not in simple_escapes:
            raise InputError(f"unsupported Lua escape \\{escaped}")
        decoded.append(simple_escapes[escaped])
        cursor += 1
    raise InputError("unterminated ordinary Lua string")


def _decode_lua_long_bracket(text: str, start: int) -> tuple[str, int]:
    """Decode a Lua 5.1 long string, including its initial-newline rule."""
    opening = _long_bracket_opening(text, start)
    if opening is None:
        raise InputError("expected a Lua long-bracket literal")
    content_start, closing = opening
    end = text.find(closing, content_start)
    if end < 0:
        raise InputError("unterminated Lua long bracket")
    source = text[content_start:end]
    if source.startswith("\r\n"):
        source = source[2:]
    elif source.startswith(("\n", "\r")):
        source = source[1:]
    return source, end + len(closing)


def _scan_complete_t_call(
    text: str, identifier_start: int, open_paren: int
) -> tuple[str, int]:
    """Parse one global t call far enough to prove it is complete.

    The first argument must be a complete literal followed by either the call's
    closing parenthesis or a comma.  The remaining arguments are lexed only for
    balanced delimiters, with strings and comments skipped as opaque literals.
    """
    argument = _skip_space_and_comments(text, open_paren + 1)
    if argument >= len(text):
        raise InputError(
            f"unsupported dynamic or non-literal first argument to t(...) at offset {identifier_start}"
        )
    if text[argument] in ("'", '"'):
        source, cursor = _decode_lua_string(text, argument)
    elif text[argument] == "[":
        source, cursor = _decode_lua_long_bracket(text, argument)
    else:
        raise InputError(
            f"unsupported dynamic or non-literal first argument to t(...) at offset {identifier_start}"
        )

    cursor = _skip_space_and_comments(text, cursor)
    if cursor >= len(text) or text[cursor] not in (",", ")"):
        raise InputError(
            f"first argument to t(...) is not a complete literal at offset {identifier_start}"
        )
    if text[cursor] == ")":
        return source, cursor + 1

    delimiters = ["("]
    cursor += 1
    matching = {")": "(", "]": "[", "}": "{"
    }
    while cursor < len(text):
        if text.startswith("--", cursor):
            cursor = _skip_space_and_comments(text, cursor)
            continue
        char = text[cursor]
        if char in ("'", '"'):
            _, cursor = _decode_lua_string(text, cursor)
            continue
        long_end = _skip_long_bracket(text, cursor)
        if long_end is not None:
            cursor = long_end
            continue
        if char in "([{":
            delimiters.append(char)
            cursor += 1
            continue
        if char in ")]}":
            if not delimiters or matching[char] != delimiters[-1]:
                raise InputError(f"unbalanced t(...) call at offset {identifier_start}")
            delimiters.pop()
            cursor += 1
            if not delimiters:
                return source, cursor
            continue
        cursor += 1
    raise InputError(f"unterminated t(...) call at offset {identifier_start}")


def _scan_lua(text: str) -> tuple[list[Section], list[Call]]:
    """Find real section markers and literal-first-argument t(...) calls."""
    sections: list[Section] = []
    calls: list[Call] = []
    cursor = 0
    previous_token: str | None = None
    while cursor < len(text):
        if text.startswith("--", cursor):
            cursor = _skip_space_and_comments(text, cursor)
            continue
        if text[cursor] in ("'", '"'):
            _, cursor = _decode_lua_string(text, cursor)
            previous_token = "literal"
            continue
        long_end = _skip_long_bracket(text, cursor)
        if long_end is not None:
            cursor = long_end
            previous_token = "literal"
            continue
        if not _is_ident_start(text[cursor]):
            if not text[cursor].isspace():
                if text.startswith("...", cursor):
                    previous_token = "..."
                    cursor += 3
                    continue
                if text.startswith("..", cursor):
                    previous_token = ".."
                    cursor += 2
                    continue
                previous_token = text[cursor]
            cursor += 1
            continue
        start = cursor
        cursor += 1
        while cursor < len(text) and _is_ident_part(text[cursor]):
            cursor += 1
        identifier = text[start:cursor]
        is_member_access = previous_token in (".", ":")
        previous_token = "identifier"
        after = _skip_space_and_comments(text, cursor)
        if (
            not is_member_access
            and identifier == "section"
            and after < len(text)
            and text[after] in ("'", '"')
        ):
            path, cursor = _decode_lua_string(text, after)
            sections.append(Section(start, path))
            previous_token = "literal"
            continue
        if not is_member_access and identifier == "t" and after < len(text) and text[after] == "(":
            source, _ = _scan_complete_t_call(text, start, after)
            calls.append(Call(start, source))
            # Continue lexing the verified call body so nested global t(...) calls
            # are discoverable, while strings/comments remain skipped by the loop.
            cursor = _skip_space_and_comments(text, cursor)
            previous_token = "literal"
            continue
    return sections, calls


def _is_chapter_title(source: str) -> bool:
    """The one production detector used for anchors and window boundaries."""
    if TITLE_MARKER not in source or ", Chapter " not in source:
        return False
    left = source.find(TITLE_MARKER) + len(TITLE_MARKER)
    middle = source.find(", Chapter ", left)
    right = source.find("]", middle + len(", Chapter "))
    return (
        middle > left
        and right > middle + len(", Chapter ")
        and source[left:middle].isdigit()
        and source[middle + len(", Chapter ") : right].isdigit()
        and source.startswith("] - ", right)
    )


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError) as error:
        raise InputError(f"cannot read {label}: {error}") from error
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise InputError(f"invalid {label} JSON: {error.msg}") from error
    if not isinstance(value, dict):
        raise InputError(f"{label} must be a JSON object")
    return value


def _require_string(value: Any, label: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str) or nonempty and not value:
        raise InputError(f"{label} must be a {'non-empty ' if nonempty else ''}string")
    return value


def _validate_payload(payload: dict[str, Any]) -> list[str]:
    if set(payload) != PAYLOAD_KEYS:
        raise InputError("payload must have exactly the seven translation_contextual_v1 keys")
    if payload["contract"] != "translation_contextual_v1":
        raise InputError("payload contract must be translation_contextual_v1")
    for key in ("contract", "fixed_source_identity", "terminology_snapshot", "rendered_briefing"):
        _require_string(payload[key], f"payload.{key}", nonempty=False)
    revision_keys = payload["ordered_revision_keys"]
    if not isinstance(revision_keys, list) or not revision_keys:
        raise InputError("payload.ordered_revision_keys must be a non-empty array")
    if any(not isinstance(key, str) or not key for key in revision_keys) or len(set(revision_keys)) != len(revision_keys):
        raise InputError("payload.ordered_revision_keys must contain unique non-empty strings")
    snapshot = payload["translation_snapshot"]
    context = payload["bounded_context"]
    if not isinstance(snapshot, list) or not isinstance(context, list):
        raise InputError("payload snapshot and context must be arrays")
    if len(snapshot) != len(revision_keys) or len(context) != len(revision_keys):
        raise InputError("payload arrays must match ordered_revision_keys")
    sources: list[str] = []
    for index, entry in enumerate(snapshot):
        if not isinstance(entry, dict) or set(entry) != {"revision_key", "source", "target"}:
            raise InputError(f"payload.translation_snapshot[{index}] has an invalid shape")
        if entry["revision_key"] != revision_keys[index]:
            raise InputError("payload.translation_snapshot order does not match revision keys")
        sources.append(_require_string(entry["source"], f"payload.translation_snapshot[{index}].source"))
        _require_string(entry["target"], f"payload.translation_snapshot[{index}].target", nonempty=False)
    for index, entry in enumerate(context):
        if not isinstance(entry, dict) or set(entry) != {"revision_key", "context"}:
            raise InputError(f"payload.bounded_context[{index}] has an invalid shape")
        if entry["revision_key"] != revision_keys[index]:
            raise InputError("payload.bounded_context order does not match revision keys")
        _require_string(entry["context"], f"payload.bounded_context[{index}].context", nonempty=False)
    return sources


def _safe_workspace_file(root: Path, raw_path: str, label: str) -> Path:
    path = Path(_require_string(raw_path, label))
    if path.is_absolute() or any(part == ".." for part in path.parts):
        raise InputError(f"{label} must be a workspace-relative non-traversing path")
    candidate = root / path
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise InputError(f"{label} must not traverse a symlink")
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, ValueError) as error:
        raise InputError(f"{label} does not resolve: {error}") from error
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise InputError(f"{label} escapes the workspace") from error
    if not resolved.is_file() or resolved.is_symlink():
        raise InputError(f"{label} must name an ordinary file")
    return resolved


def _validate_scope(scope: dict[str, Any], root: Path) -> tuple[list[dict[str, Any]], set[str]]:
    if (
        set(scope) != SCOPE_KEYS
        or type(scope.get("schema_version")) is not int
        or scope["schema_version"] != 1
    ):
        raise InputError("scope must have schema_version=1 and exactly its declared keys")
    allowed_files = scope["allowed_files"]
    anchor_scopes = scope["anchor_scopes"]
    if not isinstance(allowed_files, list) or not allowed_files:
        raise InputError("scope.allowed_files must be a non-empty array")
    if not isinstance(anchor_scopes, list) or not anchor_scopes:
        raise InputError("scope.anchor_scopes must be a non-empty array")
    normalized_allowed: set[str] = set()
    for index, raw_path in enumerate(allowed_files):
        resolved = _safe_workspace_file(root, raw_path, f"scope.allowed_files[{index}]")
        relative = resolved.relative_to(root).as_posix()
        if relative in normalized_allowed:
            raise InputError("scope.allowed_files contains a duplicate file")
        normalized_allowed.add(relative)
    scope_keys: set[tuple[str, str]] = set()
    all_titles: set[str] = set()
    validated: list[dict[str, Any]] = []
    for index, entry in enumerate(anchor_scopes):
        if not isinstance(entry, dict) or set(entry) != ANCHOR_SCOPE_KEYS:
            raise InputError(f"scope.anchor_scopes[{index}] has an invalid shape")
        resolved = _safe_workspace_file(root, entry["file"], f"scope.anchor_scopes[{index}].file")
        relative = resolved.relative_to(root).as_posix()
        if relative not in normalized_allowed:
            raise InputError("anchor scope file is not in scope.allowed_files")
        section_path = _require_string(entry["section_path"], f"scope.anchor_scopes[{index}].section_path")
        scope_key = (relative, section_path)
        if scope_key in scope_keys:
            raise InputError("scope.anchor_scopes contains a duplicate scope")
        scope_keys.add(scope_key)
        titles = entry["ordered_titles"]
        if not isinstance(titles, list) or not titles:
            raise InputError("anchor scope ordered_titles must be a non-empty array")
        checked_titles = [_require_string(title, "anchor title") for title in titles]
        if len(set(checked_titles)) != len(checked_titles):
            raise InputError("anchor scope contains a duplicate title")
        if any(title in all_titles for title in checked_titles):
            raise InputError("scope contains a duplicate title")
        all_titles.update(checked_titles)
        validated.append({"file": relative, "section_path": section_path, "ordered_titles": checked_titles})
    return validated, normalized_allowed


def _allowed_call_starts(text: str, section_path: str, titles: list[str]) -> set[int]:
    sections, calls = _scan_lua(text)
    matching_sections = [section for section in sections if section.path == section_path]
    if len(matching_sections) != 1:
        raise PreflightFailure(f"section_path {section_path!r} does not match exactly one section")
    section = matching_sections[0]
    next_section = min((item.start for item in sections if item.start > section.start), default=len(text))
    section_calls = [call for call in calls if section.start < call.start < next_section]
    title_calls = [call for call in section_calls if _is_chapter_title(call.source)]
    anchors: list[Call] = []
    for title in titles:
        matches = [call for call in title_calls if call.source == title]
        if len(matches) != 1:
            raise PreflightFailure(f"anchor title {title!r} does not match exactly one actual chapter title")
        anchors.append(matches[0])
    anchor_offsets = [anchor.start for anchor in anchors]
    if anchor_offsets != sorted(anchor_offsets):
        raise PreflightFailure("declared anchor order does not equal file order")
    allowed: set[int] = set()
    for anchor in anchors:
        boundary = min(
            [next_section]
            + [title.start for title in title_calls if title.start > anchor.start]
        )
        allowed.update(call.start for call in section_calls if anchor.start <= call.start < boundary)
    return allowed


def run_preflight(
    scope_path: Path | str, payload_path: Path | str, *, workspace_root: Path | str | None = None
) -> PreflightResult:
    """Validate a contextual payload against task-declared chapter anchor windows."""
    try:
        root = Path.cwd() if workspace_root is None else Path(workspace_root)
        root = root.resolve(strict=True)
        if not root.is_dir():
            raise InputError("workspace root is not a directory")
        scope = _read_json(Path(scope_path), "scope")
        payload = _read_json(Path(payload_path), "payload")
        sources = _validate_payload(payload)
        scopes, _ = _validate_scope(scope, root)
        in_scope_sources: set[str] = set()
        for anchor_scope in scopes:
            path = root / anchor_scope["file"]
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                raise InputError(f"cannot read scoped Lua file: {error}") from error
            starts = _allowed_call_starts(text, anchor_scope["section_path"], anchor_scope["ordered_titles"])
            _, calls = _scan_lua(text)
            in_scope_sources.update(call.source for call in calls if call.start in starts)
        missing = [source for source in sources if source not in in_scope_sources]
        if missing:
            raise PreflightFailure("snapshot source is absent from declared anchor windows: " + repr(missing[0]))
    except PreflightFailure as error:
        return PreflightResult("PREFLIGHT_FAILED", (str(error),))
    except (InputError, OSError, ValueError) as error:
        return PreflightResult("INPUT_ERROR", (str(error),))
    return PreflightResult("PREFLIGHT_VERIFIED")


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 2:
        print("INPUT_ERROR: usage: contextual_anchor_preflight.py SCOPE.json PAYLOAD.json", file=sys.stderr)
        return 2
    result = run_preflight(arguments[0], arguments[1])
    stream = sys.stdout if result.exit_code == 0 else sys.stderr
    print(result.status + (": " + result.errors[0] if result.errors else ""), file=stream)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
