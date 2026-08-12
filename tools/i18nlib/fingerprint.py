"""Finding fingerprint and Rule Registry (contract/0.1-rc3 §6, §9)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .errors import ConfigurationError, ContractError
from .lint import Issue, extract_format_tokens


@dataclass(frozen=True)
class RuleEntry:
    rule_id: str
    schema_version: int
    severity: str
    trust_class: str
    subject_kind: str
    evidence_key_spec: str
    pilot: str
    source: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "schema_version": self.schema_version,
            "severity": self.severity,
            "trust_class": self.trust_class,
            "subject_kind": self.subject_kind,
            "evidence_key_spec": self.evidence_key_spec,
            "pilot": self.pilot,
            "source": self.source,
        }


@dataclass(frozen=True)
class RuleRegistry:
    path: Path
    rules: dict[str, RuleEntry]

    @classmethod
    def load(cls, path: Path) -> "RuleRegistry":
        try:
            data = json.loads(path.read_bytes())
        except OSError as error:
            raise ContractError(f"cannot read rule registry: {path}") from error
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ContractError(
                f"invalid rule registry JSON: {path}: {error}"
            ) from error
        if not isinstance(data, dict):
            raise ConfigurationError("rule registry root must be an object")
        if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
            raise ConfigurationError("unsupported rule registry schema")
        rules_data = data.get("rules")
        if not isinstance(rules_data, list) or not rules_data:
            raise ConfigurationError("rule registry 'rules' must be a non-empty array")
        allowed_specs = frozenset(
            {"conversion-pair", "formatter-tag", "constant", "anchor-key", "runtime-key", "policy-ref"}
        )
        rules: dict[str, RuleEntry] = {}
        for index, entry in enumerate(rules_data):
            label = f"rules-registry rules[{index}]"
            if not isinstance(entry, dict):
                raise ConfigurationError(f"{label} must be an object")
            rule_id = entry.get("rule_id")
            if not isinstance(rule_id, str) or not rule_id:
                raise ConfigurationError(f"{label}.rule_id must be a non-empty string")
            schema_version = entry.get("schema_version")
            if type(schema_version) is not int or schema_version < 1:
                raise ConfigurationError(f"{label}.schema_version must be a positive integer")
            severity = entry.get("severity")
            if severity not in ("error", "warning", "context"):
                raise ConfigurationError(f"{label}.severity is invalid")
            trust_class = entry.get("trust_class")
            if trust_class not in ("A", "B", "C", "D"):
                raise ConfigurationError(f"{label}.trust_class is invalid")
            subject_kind = entry.get("subject_kind")
            if subject_kind not in ("translation_unit", "entity"):
                raise ConfigurationError(f"{label}.subject_kind is invalid")
            evidence_key_spec = entry.get("evidence_key_spec")
            if evidence_key_spec not in allowed_specs:
                raise ConfigurationError(
                    f"{label}.evidence_key_spec is not registered: "
                    f"{evidence_key_spec!r}"
                )
            pilot = entry.get("pilot")
            if not isinstance(pilot, str) or not pilot:
                raise ConfigurationError(f"{label}.pilot must be a non-empty string")
            if trust_class != "A":
                # Phase 0/1 enables only deterministic class-A rules.
                raise ConfigurationError(
                    f"{label}: trust_class != 'A' rules are disabled in Phase 0/1"
                )
            if rule_id in rules:
                raise ConfigurationError(f"duplicate rule_id: {rule_id}")
            source = entry.get("source")
            if source is not None and not isinstance(source, str):
                raise ConfigurationError(f"{label}.source must be a string or null")
            rules[rule_id] = RuleEntry(
                rule_id=rule_id,
                schema_version=schema_version,
                severity=severity,
                trust_class=trust_class,
                subject_kind=subject_kind,
                evidence_key_spec=evidence_key_spec,
                pilot=pilot,
                source=source,
            )
        return cls(path=path, rules=rules)

    def require(self, rule_id: str) -> RuleEntry:
        try:
            return self.rules[rule_id]
        except KeyError as error:
            raise ContractError(
                f"rule_id {rule_id!r} is not registered; "
                "fingerprint generation fails closed"
            ) from error


# --------------------------------------------------------------------------
# Evidence keys (§6.2)


def _collision_id(component: str, source: str, source_tag: str | None) -> str:
    tag_value = "<nil>" if source_tag is None else f"<string>{source_tag}"
    return hashlib.sha256(
        "\0".join((component, source, tag_value)).encode("utf-8")
    ).hexdigest()


def evidence_key_conversion_pair(source: str, target: str) -> str:
    source_tokens = extract_format_tokens(source)
    target_tokens = extract_format_tokens(target)
    source_sequence = ",".join(token.conversion for token in source_tokens)
    target_sequence = ",".join(token.conversion for token in target_tokens)
    return f"conv:{source_sequence}|{target_sequence}"


def _canonical_args_order(args_order: Any) -> str:
    if args_order is None:
        return ""
    if isinstance(args_order, list) and all(
        isinstance(index, int) and not isinstance(index, bool)
        for index in args_order
    ):
        return ",".join(str(index) for index in args_order)
    return ""


def evidence_key_formatter_tag(source_tag: str | None, args_order: Any) -> str:
    tag_value = "<nil>" if source_tag is None else source_tag
    return f"tag:{tag_value}|args:{_canonical_args_order(args_order)}"


def evidence_key_runtime(component: str, source: str, source_tag: str | None) -> str:
    return "collide:" + _collision_id(component, source, source_tag)[:16]


def evidence_key_anchor(anchor_key: str) -> str:
    return f"dup:{anchor_key}"


def build_evidence_key(
    spec: str,
    *,
    entry: dict[str, Any] | None = None,
    component: str | None = None,
    anchor_key: str | None = None,
) -> str:
    if spec == "conversion-pair":
        if entry is None:
            raise ConfigurationError("conversion-pair evidence requires an entry")
        return evidence_key_conversion_pair(entry["source"], entry["target"])
    if spec == "formatter-tag":
        if entry is None:
            raise ConfigurationError("formatter-tag evidence requires an entry")
        return evidence_key_formatter_tag(
            entry.get("source_tag"), entry.get("args_order")
        )
    if spec == "constant":
        return "empty"
    if spec == "anchor-key":
        if anchor_key is None:
            raise ConfigurationError("anchor-key evidence requires an anchor_key")
        return evidence_key_anchor(anchor_key)
    if spec == "runtime-key":
        if entry is None or component is None:
            raise ConfigurationError("runtime-key evidence requires entry and component")
        return evidence_key_runtime(
            component, entry["source"], entry.get("source_tag")
        )
    if spec == "policy-ref":
        raise ConfigurationError("policy-ref evidence is not enabled before Phase 2")
    raise ConfigurationError(f"unknown evidence_key_spec: {spec!r}")


# --------------------------------------------------------------------------
# Fingerprint formula (§6.1, frozen)


def finding_fingerprint(
    *,
    rule_id: str,
    rule_schema_version: int,
    subject_tu_uid: str,
    participants: tuple[str, ...],
    evidence_key: str,
) -> str:
    payload = "\0".join(
        (
            "fp/1",
            rule_id,
            str(rule_schema_version),
            subject_tu_uid,
            "\0".join(sorted(participants)),
            evidence_key,
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FindingRecord:
    issue: Issue
    rule_id: str
    rule_schema_version: int
    tu_uid: str
    participants: tuple[str, ...]
    evidence_key: str
    fingerprint: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self.issue)
        data.update(
            {
                "rule_id": self.rule_id,
                "rule_schema_version": self.rule_schema_version,
                "tu_uid": self.tu_uid,
                "participants": list(self.participants),
                "evidence_key": self.evidence_key,
                "fingerprint": self.fingerprint,
            }
        )
        return data


_CANONICAL_FIELD_ORDER = (
    "severity",
    "code",
    "message",
    "logical_path",
    "line",
    "entry_id",
    "rule_id",
    "rule_schema_version",
    "tu_uid",
    "participants",
    "evidence_key",
    "fingerprint",
)


def canonical_finding_json(record: FindingRecord) -> str:
    """Deterministic single-line JSON with the §8.4 canonical field order."""
    data = record.to_dict()
    ordered = [(key, data[key]) for key in _CANONICAL_FIELD_ORDER if key in data]
    # Any future extra fields are appended sorted for determinism.
    extra = sorted(set(data) - set(_CANONICAL_FIELD_ORDER))
    ordered.extend((key, data[key]) for key in extra)
    return (
        json.dumps(
            dict(ordered), ensure_ascii=False, sort_keys=False, separators=(",", ":")
        )
        + "\n"
    )


def canonical_findings_form(records: Iterable[FindingRecord]) -> bytes:
    """§8.4: whole-set canonical form.

    Records are sorted by the (fingerprint, rule_id, tu_uid, severity, code)
    tuple in ascending order; each record is serialized with the fixed field
    order, UTF-8, '\n' line endings, no trailing blank line.
    """
    ordered = sorted(records, key=finding_sort_key)
    lines = [canonical_finding_json(record) for record in ordered]
    return "".join(lines).encode("utf-8")


def finding_sort_key(record: FindingRecord) -> tuple[Any, ...]:
    return (
        record.fingerprint,
        record.rule_id,
        record.tu_uid,
        record.issue.severity,
        record.issue.code,
    )
