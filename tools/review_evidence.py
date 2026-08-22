#!/usr/bin/env python3
"""Deterministic inventory and referential checks for Paseo review evidence.

The commands in this module are deliberately local and read-only.  They do
not infer whether a reviewer's claim is correct; they only enumerate the
persisted records and verify that a proposer-authored reconciliation refers to
the records and findings it names.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = re.compile(r"^\.ai/reviews/(?!$).+")
COMPOSITE_REF = re.compile(r"^(?P<review>\.ai/reviews/.+) / (?P<id>[^/]+)$")
METADATA_FIELDS = (
    "task_id", "dispatch_id", "agent_id", "reviewer_role", "purpose",
    "review_contract", "review_phase", "cycle", "attempt", "candidate_ref",
)
RECONCILIATION_KEYS = frozenset({
    "schema_version", "task_id", "source_reviews", "claims", "findings",
})
CLAIM_KEYS = frozenset({"id", "text"})
FINDING_KEYS = frozenset({
    "review", "id", "disposition", "claims", "classification", "duplicate_of", "reason",
})


@dataclass(frozen=True)
class CheckResult:
    outcome: str
    detail: str
    exit_code: int


class InputError(Exception):
    """An unreadable, malformed, unsafe, or otherwise unusable input."""


class ContractError(Exception):
    """A readable JSON value that violates an evidence contract."""


def _result(outcome: str, detail: str, exit_code: int) -> CheckResult:
    return CheckResult(outcome, detail, exit_code)


def _root_path(root: str | Path) -> Path:
    try:
        return Path(root).resolve(strict=True)
    except OSError as error:
        raise InputError(f"root is not an existing directory: {root!r}") from error


def _read_json(path: Path, label: str) -> Any:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise InputError(f"cannot read {label}: {error}") from error
    try:
        return json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError as error:
        raise InputError(f"{label} is not UTF-8: {error}") from error
    except json.JSONDecodeError as error:
        raise InputError(f"{label} is not valid JSON: {error}") from error


def _workspace_relative(path: Path, root: Path, label: str) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError as error:
        raise InputError(f"{label} escapes root: {path}") from error


def _review_file(value: object, *, root: Path, label: str, allow_absolute: bool = False) -> tuple[Path, str]:
    if not isinstance(value, str) or not value:
        raise ContractError(f"{label} must be a non-empty path beneath .ai/reviews/")
    supplied = Path(value)
    if supplied.is_absolute() and not allow_absolute:
        raise InputError(f"{label} must be workspace-relative: {value!r}")
    if not supplied.is_absolute() and ".." in supplied.parts:
        raise InputError(f"{label} escapes the workspace: {value!r}")
    candidate = supplied if supplied.is_absolute() else root / supplied
    reviews = root / ".ai" / "reviews"
    try:
        resolved_reviews = reviews.resolve(strict=True)
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(resolved_reviews)
        resolved.relative_to(root)
    except (OSError, ValueError) as error:
        raise InputError(f"{label} is not an existing ordinary file beneath .ai/reviews/: {value!r}") from error
    if candidate.is_symlink() or not resolved.is_file():
        raise InputError(f"{label} must name an ordinary file: {value!r}")
    relative = _workspace_relative(resolved, root, label)
    if not REVIEW_PATH.fullmatch(relative):
        raise InputError(f"{label} is not beneath .ai/reviews/: {value!r}")
    return resolved, relative


def _source_record(path: Path, relative: str) -> dict[str, Any]:
    value = _read_json(path, f"review record {relative}")
    if not isinstance(value, dict):
        raise ContractError(f"review record {relative} must be an object")
    return value


def _inventory_item(path: Path, relative: str) -> dict[str, Any]:
    record = _source_record(path, relative)
    item: dict[str, Any] = {"path": relative}
    missing: list[str] = []
    for field in METADATA_FIELDS:
        if field in record:
            item[field] = record[field]
        else:
            item[field] = None
            missing.append(field)
    findings = record.get("findings")
    if "findings" not in record:
        missing.append("findings")
    if isinstance(findings, list):
        extracted: list[dict[str, Any]] = []
        for finding in findings:
            if isinstance(finding, dict):
                extracted.append({
                    "id": finding.get("id"),
                    "reported_severity_raw": finding.get("reported_severity"),
                    "adjudication_raw": finding.get(
                        "orchestrator_adjudication",
                        finding.get("adjudication"),
                    ),
                })
            else:
                extracted.append({
                    "id": None,
                    "reported_severity_raw": None,
                    "adjudication_raw": None,
                })
        item["has_findings_array"] = True
        item["finding_count"] = len(findings)
        item["findings"] = extracted
    else:
        if "findings" in record:
            missing.append("findings_array")
        item["has_findings_array"] = False
        item["finding_count"] = 0
        item["findings"] = []
    item["missing_fields"] = missing
    return item


def inventory(paths: list[str | Path], *, root: str | Path = ROOT) -> list[dict[str, Any]]:
    """Extract raw metadata and finding IDs from review records."""
    root_path = _root_path(root)
    result: list[dict[str, Any]] = []
    for index, value in enumerate(paths):
        path, relative = _review_file(value if isinstance(value, str) else str(value), root=root_path,
                                       label=f"review[{index}]", allow_absolute=True)
        result.append(_inventory_item(path, relative))
    return result


def _json_value(data_or_bytes: object, label: str) -> Any:
    if isinstance(data_or_bytes, (bytes, bytearray)):
        try:
            return json.loads(bytes(data_or_bytes).decode("utf-8"))
        except UnicodeDecodeError as error:
            raise InputError(f"{label} is not UTF-8: {error}") from error
        except json.JSONDecodeError as error:
            raise InputError(f"{label} is not valid JSON: {error}") from error
    if isinstance(data_or_bytes, str):
        try:
            return json.loads(data_or_bytes)
        except json.JSONDecodeError as error:
            raise InputError(f"{label} is not valid JSON: {error}") from error
    return data_or_bytes


def _load_source_findings(source_reviews: list[object], *, root: Path) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], None]]:
    records: dict[str, dict[str, Any]] = {}
    pairs: dict[tuple[str, str], None] = {}
    for index, value in enumerate(source_reviews):
        path, relative = _review_file(value, root=root, label=f"source_reviews[{index}]")
        if relative in records:
            raise ContractError(f"source_reviews contains duplicate path {relative!r}")
        record = _source_record(path, relative)
        findings = record.get("findings", [])
        if findings is None:
            findings = []
        if not isinstance(findings, list):
            raise ContractError(f"source review {relative} findings must be an array when present")
        for finding_index, finding in enumerate(findings):
            if not isinstance(finding, dict):
                raise ContractError(f"source review {relative} findings[{finding_index}] must be an object")
            finding_id = finding.get("id")
            if not isinstance(finding_id, str) or not finding_id:
                raise ContractError(f"source review {relative} findings[{finding_index}] id must be non-empty")
            pair = (relative, finding_id)
            if pair in pairs:
                raise ContractError(f"source review {relative} has duplicate finding id {finding_id!r}")
            pairs[pair] = None
        records[relative] = record
    return records, pairs


def _check_reconciliation(value: object, *, root: Path) -> None:
    data = _json_value(value, "reconciliation")
    if not isinstance(data, dict) or set(data) != RECONCILIATION_KEYS:
        raise ContractError("reconciliation must have exactly schema_version, task_id, source_reviews, claims, and findings")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ContractError("schema_version must be exactly 1")
    if not isinstance(data["task_id"], str) or not data["task_id"]:
        raise ContractError("task_id must be a non-empty string")
    source_reviews = data["source_reviews"]
    claims = data["claims"]
    entries = data["findings"]
    if not isinstance(source_reviews, list):
        raise ContractError("source_reviews must be an array")
    if not isinstance(claims, list):
        raise ContractError("claims must be an array")
    if not isinstance(entries, list):
        raise ContractError("findings must be an array")
    if not source_reviews and (claims or entries):
        raise ContractError("source_reviews may be empty only when claims and findings are empty")
    _, source_pairs = _load_source_findings(source_reviews, root=root)
    if not source_reviews and not source_pairs and (claims or entries):
        raise ContractError("empty source_reviews cannot support claims or findings")

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict) or set(claim) != CLAIM_KEYS:
            raise ContractError(f"claims[{index}] must have exactly id and text")
        claim_id, text = claim["id"], claim["text"]
        if not isinstance(claim_id, str) or not claim_id:
            raise ContractError(f"claims[{index}].id must be a non-empty string")
        if claim_id in claim_ids:
            raise ContractError(f"duplicate claim id {claim_id!r}")
        if not isinstance(text, str):
            raise ContractError(f"claims[{index}].text must be a string")
        claim_ids.add(claim_id)

    entry_by_pair: dict[tuple[str, str], dict[str, Any]] = {}
    included_claim_refs: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not set(entry).issubset(FINDING_KEYS):
            raise ContractError(f"findings[{index}] contains unknown fields")
        required = {"review", "id", "disposition"}
        if not required.issubset(entry):
            raise ContractError(f"findings[{index}] must contain review, id, and disposition")
        review, finding_id, disposition = entry["review"], entry["id"], entry["disposition"]
        if not isinstance(review, str) or not isinstance(finding_id, str) or not finding_id:
            raise ContractError(f"findings[{index}] must use a string composite review/id reference")
        if review not in {item for item in source_reviews if isinstance(item, str)}:
            raise ContractError(f"findings[{index}] review is not in source_reviews: {review!r}")
        pair = (review, finding_id)
        if pair not in source_pairs:
            raise ContractError(f"unknown finding reference {review}/{finding_id}")
        if pair in entry_by_pair:
            raise ContractError(f"duplicate disposition {review}/{finding_id}")
        if "classification" in entry and not isinstance(entry["classification"], str):
            raise ContractError(f"classification for {review}/{finding_id} must be a string")
        if disposition not in {"included", "excluded", "duplicate_of"}:
            raise ContractError(f"findings[{index}].disposition is invalid: {disposition!r}")
        if disposition == "included":
            refs = entry.get("claims")
            if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or not ref for ref in refs):
                raise ContractError(f"included finding {review}/{finding_id} must have non-empty claims")
            if len(refs) != len(set(refs)):
                raise ContractError(f"included finding {review}/{finding_id} has duplicate claim refs")
            unknown_claims = [ref for ref in refs if ref not in claim_ids]
            if unknown_claims:
                raise ContractError(f"included finding {review}/{finding_id} references unknown claim {unknown_claims[0]!r}")
            included_claim_refs.update(refs)
        elif disposition == "excluded":
            reason = entry.get("reason")
            if not isinstance(reason, str) or not reason:
                raise ContractError(f"excluded finding {review}/{finding_id} requires a non-empty reason")
        else:
            reason = entry.get("reason")
            target = entry.get("duplicate_of")
            if not isinstance(reason, str) or not reason:
                raise ContractError(f"duplicate finding {review}/{finding_id} requires a non-empty reason")
            if not isinstance(target, dict) or set(target) != {"review", "id"}:
                raise ContractError(f"duplicate finding {review}/{finding_id} requires a composite duplicate_of")
            target_pair = (target.get("review"), target.get("id"))
            if target_pair == pair:
                raise ContractError(f"duplicate finding {review}/{finding_id} cannot duplicate itself")
            if target_pair not in source_pairs:
                raise ContractError(f"duplicate finding {review}/{finding_id} targets an unknown finding")
        entry_by_pair[pair] = entry

    missing = sorted(set(source_pairs) - set(entry_by_pair))
    if missing:
        review, finding_id = missing[0]
        raise ContractError(f"missing disposition {review}/{finding_id}")
    if set(entry_by_pair) != set(source_pairs):
        raise ContractError("reconciliation finding references are not exactly source finding references")

    for pair, entry in entry_by_pair.items():
        if entry["disposition"] != "duplicate_of":
            continue
        target = entry["duplicate_of"]
        target_pair = (target["review"], target["id"])
        target_entry = entry_by_pair.get(target_pair)
        if target_entry is None:
            raise ContractError(f"duplicate finding {pair[0]}/{pair[1]} targets an unknown disposition")
        if target_entry.get("disposition") != "included":
            raise ContractError(f"duplicate finding {pair[0]}/{pair[1]} must target an included finding")

    unreferenced = sorted(claim_ids - included_claim_refs)
    if unreferenced:
        raise ContractError(f"claim {unreferenced[0]!r} is not referenced by an included finding")


def check_reconciliation(data_or_bytes: object, *, root: str | Path = ROOT) -> CheckResult:
    """Validate one reconciliation object or its frozen JSON bytes."""
    try:
        _check_reconciliation(data_or_bytes, root=_root_path(root))
    except ContractError as error:
        return _result("NEW_CONTRACT_FAILED", str(error), 1)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except (TypeError, ValueError, KeyError, AttributeError) as error:
        return _result("NEW_CONTRACT_FAILED", f"malformed JSON value ({error})", 1)
    return _result("RECONCILIATION_VERIFIED", "reconciliation referential integrity verified", 0)


def _composite_key(value: object) -> tuple[str, str]:
    if not isinstance(value, str):
        raise ContractError("scope-audit calibration/assessments keys must be composite strings")
    match = COMPOSITE_REF.fullmatch(value)
    if not match:
        raise ContractError(f"scope-audit key is not '<review path> / <finding id>': {value!r}")
    return match.group("review"), match.group("id")


def _check_audit(value: object, *, root: Path) -> None:
    data = _json_value(value, "scope-audit")
    if not isinstance(data, dict):
        raise ContractError("scope-audit record must be an object")
    source_reviews = data.get("source_reviews")
    if not isinstance(source_reviews, list) or not source_reviews:
        raise ContractError("scope-audit source_reviews must be a non-empty array")
    _, source_pairs = _load_source_findings(source_reviews, root=root)
    for field in ("calibration", "assessments"):
        if field not in data:
            continue
        mapping = data[field]
        if not isinstance(mapping, dict):
            raise ContractError(f"scope-audit {field} must be an object keyed by composite finding refs")
        for key in mapping:
            pair = _composite_key(key)
            if pair not in source_pairs:
                raise ContractError(f"scope-audit {field} key does not resolve: {key!r}")


def check_audit(data_or_bytes: object, *, root: str | Path = ROOT) -> CheckResult:
    """Validate composite source references in a scope-audit record."""
    try:
        _check_audit(data_or_bytes, root=_root_path(root))
    except ContractError as error:
        return _result("NEW_CONTRACT_FAILED", str(error), 1)
    except InputError as error:
        return _result("INPUT_ERROR", str(error), 2)
    except (TypeError, ValueError, KeyError, AttributeError) as error:
        return _result("NEW_CONTRACT_FAILED", f"malformed JSON value ({error})", 1)
    return _result("RECONCILIATION_VERIFIED", "scope-audit composite references verified", 0)


def check_scope_audit(data_or_bytes: object, *, root: str | Path = ROOT) -> CheckResult:
    """Compatibility alias for callers that name the scope-audit predicate."""
    return check_audit(data_or_bytes, root=root)


def render(data_or_bytes: object, *, root: str | Path = ROOT) -> str:
    """Render a validated reconciliation and counts derived from source records."""
    root_path = _root_path(root)
    data = _json_value(data_or_bytes, "reconciliation")
    result = check_reconciliation(data, root=root_path)
    if result.exit_code:
        raise ContractError(result.detail)
    source_records, _ = _load_source_findings(data["source_reviews"], root=root_path)
    rows = [
        "| Review | Finding | Cycle | Attempt | Disposition | Claims | Duplicate of | Reason |",
        "| --- | --- | ---: | ---: | --- | --- | --- | --- |",
    ]
    for entry in data["findings"]:
        record = source_records[entry["review"]]
        cycle = record.get("cycle")
        attempt = record.get("attempt")
        duplicate = entry.get("duplicate_of", {})
        duplicate_text = (
            f"{duplicate.get('review')} / {duplicate.get('id')}"
            if entry.get("disposition") == "duplicate_of" and isinstance(duplicate, dict) else ""
        )
        claims = ", ".join(entry.get("claims", [])) if isinstance(entry.get("claims"), list) else ""
        reason = entry.get("reason", "")
        rows.append(
            f"| {entry['review']} | {entry['id']} | {cycle!s} | {attempt!s} | "
            f"{entry['disposition']} | {claims} | {duplicate_text} | {reason} |"
        )
    counts: dict[object, int] = {}
    for relative, record in source_records.items():
        findings = record.get("findings", [])
        count = len(findings) if isinstance(findings, list) else 0
        cycle = record.get("cycle")
        counts[cycle] = counts.get(cycle, 0) + count
    lines = ["# Evidence reconciliation", "", *rows, "", "## Derived counts", ""]
    for cycle in sorted(counts, key=lambda item: (item is None, str(item))):
        lines.append(f"- cycle {cycle!s}: {counts[cycle]} findings")
    return "\n".join(lines) + "\n"


def _cli_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def _artifact_output(value: str, *, root: Path) -> Path:
    supplied = Path(value)
    output = supplied if supplied.is_absolute() else root / supplied
    artifact_root = (root / ".artifacts" / "i18n").resolve()
    resolved = output.resolve(strict=False)
    try:
        resolved.relative_to(artifact_root)
    except ValueError as error:
        raise InputError(f"--out must be beneath .artifacts/i18n: {value!r}") from error
    return resolved


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise InputError(f"invalid command-line arguments: {message}")


def main(argv: list[str] | None = None) -> int:
    parser = _ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    inventory_parser = subparsers.add_parser("inventory")
    inventory_parser.add_argument("paths", nargs="+")
    inventory_parser.add_argument("--out")
    inventory_parser.add_argument("--root", default=str(ROOT))
    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("path")
    render_parser.add_argument("--root", default=str(ROOT))
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("path")
    check_parser.add_argument("--root", default=str(ROOT))
    audit_parser = subparsers.add_parser("check-audit")
    audit_parser.add_argument("path")
    audit_parser.add_argument("--root", default=str(ROOT))
    try:
        args = parser.parse_args(argv)
        if args.command == "inventory":
            root_path = _root_path(args.root)
            output = _cli_json(inventory(args.paths, root=root_path))
            if args.out:
                out = _artifact_output(args.out, root=root_path)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(output, encoding="utf-8")
            else:
                print(output, end="")
            return 0
        try:
            payload = Path(args.path).read_bytes()
        except OSError as error:
            raise InputError(f"cannot read {args.path}: {error}") from error
        if args.command == "check":
            result = check_reconciliation(payload, root=args.root)
            print(f"{result.outcome}: {result.detail}")
            return result.exit_code
        if args.command == "check-audit":
            result = check_audit(payload, root=args.root)
            print(f"{result.outcome}: {result.detail}")
            return result.exit_code
        print(render(payload, root=args.root), end="")
        return 0
    except InputError as error:
        result = _result("INPUT_ERROR", str(error), 2)
        print(f"{result.outcome}: {result.detail}")
        return result.exit_code
    except (ContractError, OSError, TypeError, ValueError, KeyError, AttributeError) as error:
        result = _result("NEW_CONTRACT_FAILED", str(error), 1)
        print(f"{result.outcome}: {result.detail}")
        return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
