#!/usr/bin/env python3
"""Rebuild the 2026-09-23 modified-entry review reconciliation.

The script is deliberately repository-local and deterministic.  It reads frozen
campaign/research evidence and writes only its own directory.  It does not make
translation-quality decisions: statuses below are copied from existing records,
while validity describes input/protocol eligibility only.
"""

from __future__ import annotations
from pathlib import Path

# Candidate 02 delegates to the exact schema adapters.  Keeping this stable
# public entry point preserves the documented replay command.
exec((Path(__file__).with_name("reconcile_v2.py")).read_text(encoding="utf-8"), {"__name__": "__main__", "__file__": str(Path(__file__).with_name("reconcile_v2.py"))})
raise SystemExit

import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


OUT = Path(__file__).resolve().parent
CAMPAIGN = OUT.parent
ROOT = CAMPAIGN.parents[2]
EXPERIMENTS = CAMPAIGN / "experiments"
SCOPE_CAL = ROOT / "evidence/translation-audit/scope-rule-calibration-20260923"
ENTRY_RE = re.compile(r"entry-\d{5}")
HEADING_RE = re.compile(r"^(#{1,6})\s+.*?(entry-\d{5}).*$", re.M | re.I)
ENTRY_SECTION_RE = re.compile(
    r"^(?:#{1,6}\s+[^\n]*?|[-*]\s+\*{0,2}|\|\s*\*{0,2})(entry-\d{5})\b",
    re.M | re.I,
)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def csv_text(rows: list[dict], fields: list[str]) -> str:
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


used_inputs: set[Path] = set()


def use(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(path)
    used_inputs.add(path.resolve())
    return path


inventory_path = use(CAMPAIGN / "inventory.json")
state_path = use(CAMPAIGN / "STATE.json")
inventory_doc = load(inventory_path)
inventory = inventory_doc["entries"]
old_state = load(state_path)
ids = [row["audit_id"] for row in inventory]
id_set = set(ids)
if len(ids) != 4144 or len(id_set) != 4144:
    raise SystemExit("inventory must contain exactly 4144 unique audit IDs")

entries = {}
for row in inventory:
    eid = row["audit_id"]
    entries[eid] = {
        "entry_id": eid,
        "component": row["component"],
        "logical_path": row["logical_path"],
        "line": row["line"],
        "section": row["section"],
        "source_tag": row["source_tag"],
        "snapshot_sha256": row["snapshot_sha256"],
        "original_batch": None,
        "events": [],
        "coverage": {
            "initial": False,
            "cross": False,
            "experiment": False,
            "adjudication": False,
        },
        "todo_status": [],
    }

unknown_ids: set[str] = set()
event_keys: set[tuple] = set()


def add_event(
    eid: str,
    *,
    layer: str,
    source: Path,
    valid: bool,
    kind: str,
    qualification: str = "",
    identity: str = "entry_id_membership",
    input_source: Path | None = None,
) -> None:
    if eid not in id_set:
        unknown_ids.add(eid)
        return
    key = (eid, layer, rel(source), valid, kind, qualification)
    if key in event_keys:
        return
    event_keys.add(key)
    use(source)
    input_source = input_source or source
    use(input_source)
    event = {
        "layer": layer,
        "kind": kind,
        "source": rel(source),
        "source_sha256": sha256(source),
        "input": rel(input_source),
        "input_sha256": sha256(input_source),
        "valid": valid,
        "qualification": qualification or None,
        "identity_check": identity,
    }
    entries[eid]["events"].append(event)
    if valid and layer in entries[eid]["coverage"]:
        entries[eid]["coverage"][layer] = True


# Exact batch membership is taken from frozen entry_ids, never numeric ranges.
batch_by_id = {}
batch_input_mismatches = []
for batch in old_state["batches"]:
    batch_input = use(ROOT / batch["input_path"])
    if sha256(batch_input) != batch["input_sha256"]:
        batch_input_mismatches.append(batch["batch_id"])
    for eid in batch["entry_ids"]:
        if eid not in id_set:
            unknown_ids.add(eid)
        batch_by_id[eid] = batch["batch_id"]
        if eid in entries:
            entries[eid]["original_batch"] = batch["batch_id"]


def report_ids(path: Path) -> list[str]:
    text = use(path).read_text(encoding="utf-8")
    # Coverage requires an actual per-entry section, not a range in prose or an
    # entry mentioned merely as comparison evidence inside another section.
    return list(dict.fromkeys(m.group(1).lower() for m in ENTRY_SECTION_RE.finditer(text)))


# Primary campaign reports.  STATE-selected output wins; when STATE is stale,
# the highest landed retry for that batch is the recoverable result.
primary_sources = {}
campaign_report_validity: dict[Path, tuple[bool, str | None]] = {}
for batch in old_state["batches"]:
    number = batch["batch_id"].split("-")[-1]
    candidates = sorted((CAMPAIGN / "reports").glob(f"gemini-{number}-*.md"))
    selected_paths: set[Path] = set()
    raw = batch.get("raw_output_path")
    if raw and (ROOT / raw).is_file():
        selected_paths.add(ROOT / raw)
    supplement = batch.get("supplement_raw_output_path")
    if supplement and (ROOT / supplement).is_file():
        selected_paths.add(ROOT / supplement)
    coverage_note = batch.get("coverage_note", "")
    for candidate in candidates:
        if candidate.stem in coverage_note:
            selected_paths.add(candidate)
    if not selected_paths and candidates:
        selected_paths.add(candidates[-1])
    if selected_paths:
        primary_sources[batch["batch_id"]] = sorted(selected_paths)
    for candidate in candidates:
        valid = candidate in selected_paths
        why = "selected_primary_or_complement" if valid else "superseded_retry_or_duplicate"
        campaign_report_validity[candidate.resolve()] = (valid, None if valid else why)
        for eid in report_ids(candidate):
            if eid in batch["entry_ids"]:
                add_event(
                    eid,
                    layer="initial",
                    source=candidate,
                    valid=valid,
                    kind="campaign_primary",
                    qualification=why,
                    identity="explicit_report_id_in_frozen_batch",
                    input_source=ROOT / batch["input_path"],
                )


# Ten prior spotchecks: require ID mapping plus exact source and target text in
# the original report.  This intentionally does not trust the old total of ten.
spot_path = use(
    ROOT
    / "evidence/spotchecks/modified-translation-spotcheck-20260921/reviewer-full-02.md"
)
spot_text = spot_path.read_text(encoding="utf-8")
spot_workset_path = use(
    ROOT / "evidence/spotchecks/modified-translation-spotcheck-20260921/workset.json"
)
spot_workset = {row["revision_key"]: row for row in load(spot_workset_path)["entries"]}
prior_identity_failures = []
for inv in inventory:
    if not inv.get("prior_spotcheck"):
        continue
    frozen = spot_workset.get(inv["prior_spotcheck"])
    ok = bool(
        frozen
        and inv["prior_spotcheck"] in spot_text
        and frozen["source"] == inv["source"]
        and frozen["target"] == inv["target"]
        and frozen["section"] == inv["section"]
        and frozen["line"] == inv["line"]
    )
    if not ok:
        prior_identity_failures.append(inv["audit_id"])
    add_event(
        inv["audit_id"],
        layer="initial",
        source=spot_path,
        valid=ok,
        kind="prior_spotcheck",
        qualification=inv["prior_spotcheck"],
        identity="spot_id_plus_workset_source_target_section_line_exact",
        input_source=spot_workset_path,
    )


# Cross reports.  The revoked sol-091-01 is retained as invalid evidence and
# sol-091-02 is the effective replacement.  Landed sol-092-01 repairs stale STATE.
for cross in old_state["cross_reviews"]:
    cid = cross.get("cross_id", "")
    suffix = cid.removeprefix("cross-batch-")
    candidates = sorted((CAMPAIGN / "reports").glob(f"sol-{suffix}-*.md"))
    raw = cross.get("raw_output_path")
    cross_input = ROOT / cross["input_path"] if cross.get("input_path") else None
    selected = ROOT / raw if raw and (ROOT / raw).is_file() else None
    if cid == "cross-batch-091":
        replacement = CAMPAIGN / "reports/sol-091-02.md"
        selected = replacement if replacement.is_file() else selected
    elif not selected and candidates:
        selected = candidates[-1]
    for candidate in candidates:
        valid = candidate == selected and candidate.name != "sol-091-01.md"
        qualification = "selected_cross"
        if candidate.name == "sol-091-01.md":
            qualification = "revoked_wrong_input_replaced_by_sol-091-02"
        elif not valid:
            qualification = "superseded_cross"
        campaign_report_validity[candidate.resolve()] = (
            valid,
            None if valid else qualification,
        )
        allowed = set(cross.get("entry_ids", []))
        for eid in report_ids(candidate):
            if eid in allowed:
                add_event(
                    eid,
                    layer="cross",
                    source=candidate,
                    valid=valid,
                    kind="campaign_cross",
                    qualification=qualification,
                    identity="explicit_report_id_in_cross_input",
                    input_source=cross_input,
                )

prior_cross = CAMPAIGN / "reports/sol-prior-01.md"
if prior_cross.is_file():
    for eid in report_ids(prior_cross):
        add_event(
            eid,
            layer="cross",
            source=prior_cross,
            valid=True,
            kind="prior_spotcheck_cross",
            qualification="selected_cross",
            input_source=CAMPAIGN / "cross-prior-spot06.md",
        )


# ABC groups 1-14: actual group entry_ids from the cumulative STATE are the
# authority.  Group 1's protocol anomaly qualifies, but does not erase, coverage.
abc_state_path = use(EXPERIMENTS / "abc20-20260923/STATE.json")
abc_state = load(abc_state_path)
abc_groups = {}
for group in abc_state["groups"]:
    abc_groups[group["index"]] = group
    directory = EXPERIMENTS / group["directory"]
    source = directory / "STATE.json"
    valid = group["index"] <= 14 and group.get("state") == "DONE"
    qualification = "group1_protocol_anomaly_readonly_coverage" if group["index"] == 1 else "completed_group"
    for eid in group["entry_ids"]:
        add_event(
            eid,
            layer="experiment",
            source=source,
            valid=valid,
            kind="abc_group",
            qualification=qualification,
            identity="abc20_state_explicit_group_entry_id",
            input_source=(directory / "entries.json") if (directory / "entries.json").is_file() else abc_state_path,
        )
        merged = directory / "MERGED-FINDINGS.json"
        reference = directory / "REFERENCE.json"
        adjudication_source = merged if merged.is_file() else reference if reference.is_file() else None
        if adjudication_source:
            add_event(
                eid,
                layer="adjudication",
                source=adjudication_source,
                valid=valid,
                kind="abc_reference",
                qualification=("reference_not_human_truth;" + qualification),
                identity="abc20_state_explicit_group_entry_id",
                input_source=(directory / "entries.json") if (directory / "entries.json").is_file() else abc_state_path,
            )


def rows_from_entries(path: Path) -> list[dict]:
    doc = load(use(path))
    return doc.get("entries", doc) if isinstance(doc, dict) else doc


# Calibrated pilot and process A/B are overlapping research samples.  Events are
# per-entry and therefore de-duplicate global coverage automatically.
pilot_entries = rows_from_entries(EXPERIMENTS / "calibrated-pilot40-20260923/entries.json")
pilot_findings = EXPERIMENTS / "calibrated-pilot40-20260923/FINDINGS.md"
for row in pilot_entries:
    add_event(row["audit_id"], layer="experiment", source=pilot_findings, valid=True,
              kind="calibrated_pilot", qualification="research_only")
    add_event(row["audit_id"], layer="adjudication", source=pilot_findings, valid=True,
              kind="calibrated_host_result", qualification="host_reference_not_human_gold")

ab_entries = rows_from_entries(EXPERIMENTS / "process-ab40-20260923/entries.json")
ab_final = EXPERIMENTS / "process-ab40-20260923/FINAL-ENTRY-RESULTS.json"
for row in ab_entries:
    add_event(row["audit_id"], layer="experiment", source=ab_final, valid=True,
              kind="process_ab", qualification="research_only")
    add_event(row["audit_id"], layer="adjudication", source=ab_final, valid=True,
              kind="process_ab_host_result", qualification="host_reference_not_human_gold")


# Calibration-10 is a duplicate sample of ABC entries.  Preserve its explicit
# mapping and final provisional host result without inflating unique coverage.
cal10_map_path = use(EXPERIMENTS / "calibration-10-20260923/HOST-MAPPING.json")
cal10_result_path = use(EXPERIMENTS / "calibration-10-20260923/RESULT.json")
for row in load(cal10_map_path):
    add_event(row["entry_id"], layer="experiment", source=cal10_result_path, valid=True,
              kind="calibration10", qualification="duplicate_research_sample")
    add_event(row["entry_id"], layer="adjudication", source=cal10_result_path, valid=True,
              kind="calibration10_host_result", qualification="provisional_not_human_gold")


# Flash: dev comes from the AB reference and is not a new independent truth;
# holdout reference is explicitly provisional.  Wrong-input duplicate reports
# remain in the source manifest/findings as invalid and never add coverage.
flash = EXPERIMENTS / "gemini-flash-tuning-20260923"
flash_ledger_path = use(flash / "RUN-LEDGER.json")
flash_ledger = load(flash_ledger_path)
flash_excluded = {r["dispatch"] for r in flash_ledger if r.get("excluded_assignment")}
flash_final = use(flash / "HOLDOUT-FINAL-ADJUDICATION.json")
for subset, qualifier in (
    ("dev", "derived_from_process_ab_reference_not_independent_truth"),
    ("holdout", "host_provisional_holdout_reference_not_human_gold"),
):
    source = flash / subset / "entries.json"
    for row in rows_from_entries(source):
        eid = row["audit_id"]
        add_event(eid, layer="experiment", source=source, valid=True,
                  kind=f"flash_{subset}", qualification="repeated_sessions_count_once")
        add_event(eid, layer="adjudication", source=flash_final, valid=True,
                  kind=f"flash_{subset}_reference", qualification=qualifier)


# Later scope calibration is existing evidence, not a new semantic decision.
scope_affected_path = use(SCOPE_CAL / "AFFECTED.json")
scope_affected = load(scope_affected_path)
for row in scope_affected["records"]:
    for eid in row.get("inventory_audit_ids", []):
        add_event(eid, layer="adjudication", source=scope_affected_path, valid=True,
                  kind="scope_rule_calibration", qualification="bounded_terminology_scope_only")


# User-calibrated boundaries: exact IDs from calibration-10 mappings/crosswalk.
calibration_notes = {
    "entry-03627": "用户定标：主句已限定造成伤害时，first attacked/first hit 的歧义仅作需澄清/advisory，不计确认错译。",
    "entry-03605": "用户定标：文明人→普通人仅作需澄清/advisory，不计确认错译。",
    "entry-03595": "用户定标：‘受到熵能反冲’概括施加与增强仅作需澄清/advisory，不计确认错译。",
}


# ----- Finding ledger -----------------------------------------------------

findings_by_entry: dict[str, list[dict]] = defaultdict(list)
finding_dedup: dict[tuple[str, str], dict] = {}


def status_mentions(text: str) -> list[str]:
    lower = text.lower()
    found = []
    tests = (
        ("confirmed", r"\bconfirmed\b|结论[：:]?\s*确认|已确认|确认错译"),
        ("pending", r"\bpending\b|待确认|待决|证据不足"),
        ("advisory", r"\badvisory\b|细微观察|需(?:要)?澄清|建议"),
        ("refuted", r"\brefuted\b|撤销|不成立|已驳回"),
    )
    for status, pattern in tests:
        if re.search(pattern, lower, re.I):
            found.append(status)
    if re.search(r"\bISSUE\b|有问题|存在问题", text, re.I) and "confirmed" not in found:
        found.append("unadjudicated_observation")
    return found


def add_finding(
    eid: str,
    *,
    source: Path,
    line_start: int,
    line_end: int,
    text: str,
    statuses: list[str],
    validity: str,
    author: str,
    record_kind: str,
    exclusion_reason: str | None = None,
    canonical_id: str | None = None,
    local_number: str | None = None,
) -> None:
    if eid not in id_set:
        unknown_ids.add(eid)
        return
    normalized = re.sub(r"\s+", " ", text).strip()
    fingerprint = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    key = (eid, fingerprint)
    locator = f"{rel(source)}#L{line_start}-L{line_end}"
    use(source)
    if key in finding_dedup:
        finding_dedup[key]["also_at"].append(locator)
        return
    record = {
        "finding_id": canonical_id or f"F-{eid[6:]}-{fingerprint[:12]}",
        "entry_id": eid,
        "statuses": statuses or ["unadjudicated_observation"],
        "original_text": text.strip(),
        "source": rel(source),
        "source_sha256": sha256(source),
        "locator": {
            "line_start": line_start,
            "line_end": line_end,
            "local_number": local_number,
        },
        "author": author,
        "record_kind": record_kind,
        "validity": validity,
        "exclusion_reason": exclusion_reason,
        "also_at": [],
        "related_candidates": [],
    }
    findings_by_entry[eid].append(record)
    finding_dedup[key] = record


def author_for(path: Path) -> str:
    name = path.name.lower()
    if "gemini" in name or "f00" in name or "f01" in name or "f10" in name or "f11" in name:
        return "gemini"
    if name.startswith("sol-") or name in {"a2.md", "b2.md", "b3.md", "p.md"}:
        return "reviewer_or_process_arm"
    if "adjudication" in name or "finding" in name or "reference" in name:
        return "host_or_adjudicator"
    return "record_author_unspecified"


def scan_markdown(path: Path, *, validity: str = "valid", exclusion: str | None = None) -> None:
    text = use(path).read_text(encoding="utf-8")
    matches = list(ENTRY_SECTION_RE.finditer(text))
    line_starts = [0]
    for m in re.finditer("\n", text):
        line_starts.append(m.end())
    def line_no(offset: int) -> int:
        import bisect
        return bisect.bisect_right(line_starts, offset)
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():end].rstrip()
        statuses = status_mentions(block)
        clear_only = re.search(r"未发现问题|\bstatus\s*[:：]?\s*OK\b|结论[：:]?\s*OK", block, re.I)
        if clear_only and not statuses:
            continue
        if not statuses and not re.search(r"claim|观察|疑点|问题|issue|pending|advisory", block, re.I):
            continue
        add_finding(
            match.group(1).lower(), source=path,
            line_start=line_no(match.start()), line_end=line_no(end),
            text=block, statuses=statuses, validity=validity,
            author=author_for(path), record_kind="natural_language_entry_block",
            exclusion_reason=exclusion,
        )


# Campaign model reports are all indexed, including revoked/superseded sources.
for path in sorted((CAMPAIGN / "reports").glob("*.md")):
    eligible, reason = campaign_report_validity.get(path.resolve(), (True, None))
    validity = "valid" if eligible else "invalid"
    exclusion = reason
    if path.name == "sol-091-01.md":
        validity = "invalid"
        exclusion = "wrong frozen input; superseded by sol-091-02"
    scan_markdown(path, validity=validity, exclusion=exclusion)

# Final and raw natural-language research reports.  Prompts/timelines are not
# reports and are intentionally outside the finding corpus.
md_sources: set[Path] = set()
for directory in sorted(EXPERIMENTS.glob("*")):
    for pattern in ("reports/*.md", "FINDINGS.md", "ADJUDICATION.md", "MERGED-FINDINGS.md", "REPORT.md"):
        md_sources.update(directory.glob(pattern))
for path in sorted(md_sources):
    validity = "valid"
    exclusion = None
    if path.parent.name == "reports" and path.parent.parent == flash:
        dispatch = path.stem.removesuffix("-full")
        if dispatch in flash_excluded:
            validity = "invalid"
            exclusion = "Flash wrong-input/duplicate assignment; excluded by RUN-LEDGER"
    scan_markdown(path, validity=validity, exclusion=exclusion)


def structured_records(obj, source: Path, context: str = "root") -> None:
    if isinstance(obj, list):
        for i, value in enumerate(obj):
            structured_records(value, source, f"{context}[{i}]")
        return
    if not isinstance(obj, dict):
        return
    eid = obj.get("entry_id") or obj.get("audit_id") or obj.get("entry")
    if isinstance(eid, str) and ENTRY_RE.fullmatch(eid):
        statuses = []
        status = str(obj.get("status", "")).lower()
        if status == "issue": statuses.append("confirmed")
        elif status == "pending": statuses.append("pending")
        elif status in {"confirmed", "advisory", "refuted"}: statuses.append(status)
        for key, mapped in (("confirmed", "confirmed"), ("pending", "pending"),
                            ("advisory", "advisory"), ("refuted", "refuted")):
            if obj.get(key): statuses.append(mapped)
        if statuses:
            text = json.dumps(obj, ensure_ascii=False, sort_keys=True)
            add_finding(
                eid, source=source, line_start=1, line_end=1, text=text,
                statuses=list(dict.fromkeys(statuses)), validity="valid",
                author="host_or_adjudicator", record_kind="structured_record",
                canonical_id=(str(obj.get("id")) if obj.get("id") else None),
                local_number=context,
            )
    for key, value in obj.items():
        structured_records(value, source, f"{context}.{key}")


structured_paths = [
    EXPERIMENTS / "abc20-20260923/REPORT-DATA.json",
    EXPERIMENTS / "calibration-10-20260923/CLAIM-CROSSWALK.json",
    EXPERIMENTS / "calibration-10-20260923/RESULT.json",
    ab_final,
    EXPERIMENTS / "process-ab40-20260923/ADJUDICATION.json",
    flash / "HOST-DEV-REFERENCE.json",
    flash / "HOLDOUT-REFERENCE-FREEZE.json",
    flash / "HOLDOUT-FINAL-ADJUDICATION.json",
    scope_affected_path,
]
structured_paths += sorted(EXPERIMENTS.glob("abc*/MERGED-FINDINGS.json"))
structured_paths += sorted(EXPERIMENTS.glob("abc20-g*/MERGED-FINDINGS.json"))
for path in structured_paths:
    if path.is_file():
        use(path)
        structured_records(load(path), path)

# Attach the later user calibration as a note, while preserving every old status.
cal_source = use(EXPERIMENTS / "calibration-10-20260923/CLAIM-CROSSWALK.json")
for eid, note in calibration_notes.items():
    add_finding(
        eid, source=cal_source, line_start=1, line_end=1, text=note,
        statuses=["advisory"], validity="valid", author="user_calibration",
        record_kind="later_user_scope_note", canonical_id=f"USER-CAL-{eid}",
    )


# Preserve association candidates without merging by wording: same entry with
# records from multiple files gets source-level related_candidates only.
for eid, records in findings_by_entry.items():
    distinct = sorted({r["source"] for r in records})
    if len(distinct) > 1:
        for record in records:
            record["related_candidates"] = [p for p in distinct if p != record["source"]]


# ----- Backlog and derived summaries -------------------------------------

for eid, row in entries.items():
    if not any(row["coverage"].values()):
        row["todo_status"].append("no_valid_entry_review")
    valid_findings = [f for f in findings_by_entry.get(eid, []) if f["validity"] == "valid"]
    statuses = {s for f in valid_findings for s in f["statuses"]}
    if valid_findings and not (row["coverage"]["cross"] or row["coverage"]["adjudication"]):
        row["todo_status"].append("reported_observation_not_crossed")
    if "pending" in statuses:
        row["todo_status"].append("pending_fact_or_source")
    if "confirmed" in statuses and "refuted" in statuses:
        row["todo_status"].append("scale_or_status_conflict")
    if eid in calibration_notes:
        row["todo_status"].append("user_calibrated_advisory_boundary")

coverage_rows = [entries[eid] for eid in ids]
coverage_csv_rows = []
for row in coverage_rows:
    valid_sources = sorted({e["source"] for e in row["events"] if e["valid"]})
    invalid_sources = sorted({e["source"] for e in row["events"] if not e["valid"]})
    coverage_csv_rows.append({
        "entry_id": row["entry_id"], "component": row["component"],
        "logical_path": row["logical_path"], "line": row["line"],
        "section": row["section"], "original_batch": row["original_batch"] or "",
        "initial": str(row["coverage"]["initial"]).lower(),
        "cross": str(row["coverage"]["cross"]).lower(),
        "experiment": str(row["coverage"]["experiment"]).lower(),
        "adjudication": str(row["coverage"]["adjudication"]).lower(),
        "todo_status": ";".join(row["todo_status"]),
        "valid_sources": ";".join(valid_sources),
        "invalid_sources": ";".join(invalid_sources),
    })

finding_entries = []
for eid in ids:
    records = sorted(findings_by_entry.get(eid, []), key=lambda r: (r["source"], r["locator"]["line_start"], r["finding_id"]))
    if records:
        finding_entries.append({"entry_id": eid, "records": records})

backlog_categories = defaultdict(list)
for eid in ids:
    for category in entries[eid]["todo_status"]:
        backlog_categories[category].append(eid)
backlog = {
    "schema_version": 1,
    "categories": [
        {"category": category, "count": len(eids), "entry_ids": eids}
        for category, eids in sorted(backlog_categories.items())
    ],
    "formal_completion_rule": "A model report or experimental reference alone does not imply production completion.",
}
backlog_csv_rows = [
    {"category": category, "entry_id": eid, "component": entries[eid]["component"],
     "original_batch": entries[eid]["original_batch"] or ""}
    for category, eids in sorted(backlog_categories.items()) for eid in eids
]

layer_counts = {layer: sum(1 for r in coverage_rows if r["coverage"][layer])
                for layer in ("initial", "cross", "experiment", "adjudication")}
any_valid = sum(1 for r in coverage_rows if any(r["coverage"].values()))
valid_event_count = sum(1 for r in coverage_rows for e in r["events"] if e["valid"])
invalid_event_count = sum(1 for r in coverage_rows for e in r["events"] if not e["valid"])
finding_status_counts = Counter(
    status for item in finding_entries for record in item["records"]
    for status in record["statuses"] if record["validity"] == "valid"
)

# Source limitations and anomalies are explicit rather than silently repaired.
anomalies = [
    {
        "code": "OLD_STATE_STALE",
        "detail": "STATE remaining/covered fields predate landed gemini-094-01 and sol-092-01; coverage is rebuilt from explicit entry IDs and files.",
    },
    {
        "code": "SOL_091_WRONG_INPUT",
        "detail": "sol-091-01 is retained but invalid; sol-091-02 is the effective cross result.",
    },
    {
        "code": "ABC_GROUP1_PROTOCOL",
        "detail": "ABC group 1 has a comparison-protocol anomaly; real read-only entry coverage remains qualified, not erased.",
    },
    {
        "code": "ABC_15_20_NOT_RUN",
        "detail": "ABC groups 15-20 were frozen/undispatched and do not count as completed coverage.",
    },
    {
        "code": "FLASH_INVALID_ASSIGNMENTS",
        "detail": "Two Flash wrong-input/duplicate assignments are indexed as invalid and add no independent coverage.",
        "dispatches": sorted(flash_excluded),
    },
    {
        "code": "REFERENCE_NOT_HUMAN_TRUTH",
        "detail": "ABC, AB, calibration and Flash host references retain their recorded status but are not promoted to human gold or production completion.",
    },
    {
        "code": "DLC_PROVENANCE_LIMIT",
        "detail": "Several DLC snapshots lack a fixed source repository commit/target-version mapping; existing pending applicability remains pending.",
    },
]

baseline_path = use(ROOT / ".ai/task/modified-review-reconcile-20260923/BASELINE.json")
baseline_hashes = load(baseline_path)["sha256"]
baseline_missing = []
baseline_mismatches = []
for source_path, expected in baseline_hashes.items():
    candidate = ROOT / source_path
    if not candidate.is_file():
        baseline_missing.append(source_path)
    else:
        actual = sha256(candidate)
        if actual != expected:
            baseline_mismatches.append({"path": source_path, "expected": expected, "actual": actual})

validation = {
    "schema_version": 1,
    "checks": {
        "inventory_count_4144": len(coverage_rows) == 4144,
        "inventory_ids_unique": len({r["entry_id"] for r in coverage_rows}) == 4144,
        "unknown_ids_empty": not unknown_ids,
        "prior_10_identity_count": sum(1 for r in inventory if r.get("prior_spotcheck")) == 10,
        "prior_identity_failures_empty": not prior_identity_failures,
        "abc_completed_group_count_14": sum(1 for g in abc_state["groups"] if g["index"] <= 14 and g.get("state") == "DONE") == 14,
        "abc_completed_unique_entries_560": len({eid for g in abc_state["groups"] if g["index"] <= 14 for eid in g["entry_ids"]}) == 560,
        "abc_groups_15_20_not_completed": not any(g.get("state") == "DONE" for g in abc_state["groups"] if g["index"] >= 15),
        "sol_091_01_never_valid": all(not e["valid"] for r in coverage_rows for e in r["events"] if e["source"].endswith("sol-091-01.md")),
        "sol_091_02_valid": any(e["valid"] for r in coverage_rows for e in r["events"] if e["source"].endswith("sol-091-02.md")),
        "gemini_094_landed_counted": any(e["valid"] for r in coverage_rows for e in r["events"] if e["source"].endswith("gemini-094-01.md")),
        "sol_092_landed_counted": any(e["valid"] for r in coverage_rows for e in r["events"] if e["source"].endswith("sol-092-01.md")),
        "all_valid_events_have_hash": all(e.get("source_sha256") for r in coverage_rows for e in r["events"] if e["valid"]),
        "all_valid_events_have_input_hash": all(e.get("input_sha256") for r in coverage_rows for e in r["events"] if e["valid"]),
        "all_batch_input_hashes_match_state": not batch_input_mismatches,
        "mixed_confirmed_pending_preserved": any({"confirmed", "pending"}.issubset({s for f in findings_by_entry[eid] for s in f["statuses"]}) for eid in findings_by_entry),
        "user_calibration_exact_three_ids": set(calibration_notes) == {"entry-03627", "entry-03605", "entry-03595"},
        "all_11190_frozen_existing_files_unchanged": not baseline_missing and not baseline_mismatches and len(baseline_hashes) == 11190,
    },
    "counts": {
        "entries": len(coverage_rows), "entries_with_any_valid_review": any_valid,
        "valid_events": valid_event_count, "invalid_events": invalid_event_count,
        "finding_entries": len(finding_entries), "finding_records": sum(len(x["records"]) for x in finding_entries),
        "finding_status_mentions": dict(sorted(finding_status_counts.items())),
        "coverage_layers": layer_counts,
        "backlog": {k: len(v) for k, v in sorted(backlog_categories.items())},
    },
    "unknown_ids": sorted(unknown_ids),
    "prior_identity_failures": prior_identity_failures,
    "batch_input_mismatches": batch_input_mismatches,
    "baseline": {
        "checked_files": len(baseline_hashes),
        "missing": baseline_missing,
        "mismatches": baseline_mismatches,
    },
    "anomalies": anomalies,
}

if not all(validation["checks"].values()):
    failed = [k for k, value in validation["checks"].items() if not value]
    raise SystemExit("validation failed: " + ", ".join(failed))

# Add human-facing historical inputs to the manifest even when not used as a
# coverage authority, because README explains their stale snapshot status.
for name in ("PROGRESS.md", "HUMAN-REVIEW.md", "CHECKS.md", "INVENTORY-CORRECTIONS.md", "PLAN.md"):
    path = CAMPAIGN / name
    if path.is_file():
        use(path)
for path in (SCOPE_CAL / "REPORT.md", SCOPE_CAL / "VERIFICATION.json"):
    if path.is_file():
        use(path)

manifest = {
    "schema_version": 1,
    "root": ".",
    "inputs": [
        {"path": rel(path), "sha256": sha256(path), "bytes": path.stat().st_size}
        for path in sorted(used_inputs, key=rel)
    ],
    "policy": "Every file read as evidence or explanatory history is hashed. Generated outputs are excluded to avoid circular hashes.",
}

dump(OUT / "SOURCE-MANIFEST.json", manifest)
dump(OUT / "COVERAGE.json", {"schema_version": 1, "inventory_sha256": sha256(inventory_path), "entries": coverage_rows})
(OUT / "COVERAGE.csv").write_text(csv_text(coverage_csv_rows, list(coverage_csv_rows[0])), encoding="utf-8")
dump(OUT / "FINDINGS.json", {"schema_version": 1, "entries": finding_entries})
dump(OUT / "BACKLOG.json", backlog)
(OUT / "BACKLOG.csv").write_text(csv_text(backlog_csv_rows, ["category", "entry_id", "component", "original_batch"]), encoding="utf-8")
dump(OUT / "VALIDATION.json", validation)

finding_lines = [
    "# 问题与待确认入口", "",
    "本文件由 `generate.py` 从既有记录生成；不新增语义裁决。完整原文块、状态、作者/来源、行号和排除理由见 `FINDINGS.json`。", "",
    f"共 {len(finding_entries)} 个 entry、{sum(len(x['records']) for x in finding_entries)} 条去重记录。有效状态提及："
    + "，".join(f"{k}={v}" for k, v in sorted(finding_status_counts.items())) + "。", "",
]
for item in finding_entries:
    statuses = Counter(s for r in item["records"] if r["validity"] == "valid" for s in r["statuses"])
    finding_lines.append(f"- `{item['entry_id']}`：" + "，".join(f"{k}={v}" for k, v in sorted(statuses.items())) + f"；记录 {len(item['records'])} 条")
(OUT / "FINDINGS.md").write_text("\n".join(finding_lines) + "\n", encoding="utf-8")

readme = f"""# 已修改译文审核统一台账（2026-09-23）

这是 4144 条真实 inventory entry-ID 的统一证据入口。它只归并既有覆盖、问题和待确认记录，不新增译文语义裁决，也不表示生产 `DONE_VERIFIED`。

## 当前统计

- 母表：4144 个唯一 entry；未知 ID：0。
- 至少有一种有效逐条审核/实验/裁决记录：{any_valid}；完全没有有效逐条记录：{len(backlog_categories.get('no_valid_entry_review', []))}。
- 分层去重覆盖：初审 {layer_counts['initial']}、交叉 {layer_counts['cross']}、实验 {layer_counts['experiment']}、裁决/参考 {layer_counts['adjudication']}。各层可重叠，不可相加当作全局完成数。
- 有效事件 {valid_event_count}，无效/撤销事件 {invalid_event_count}；问题记录覆盖 {len(finding_entries)} 个 entry。
- ABC 按累计 STATE 的真实 groups 1–14 计 560 个唯一 entry；group 1 保留协议异常资格说明，groups 15–20 未运行。

## 文件

- `COVERAGE.json` / `COVERAGE.csv`：4144 条母表、原 batch、事件来源/哈希/有效性、四层覆盖和待办。
- `FINDINGS.json` / `FINDINGS.md`：逐 entry 的既有 confirmed/pending/advisory/refuted/未裁决观察；自然语言块原文保底，带精确文件和行号。同文重印按内容哈希去重，跨来源只建立关联候选。
- `BACKLOG.json` / `BACKLOG.csv`：无有效逐条审核、报告未交叉、事实/来源待确认、尺度/状态冲突和用户校准边界分列。
- `SOURCE-MANIFEST.json`：本次实际读取输入的路径、SHA-256 与字节数。
- `VALIDATION.json`：机械验收、异常与已知来源限制。
- `generate.py`：可重放生成器；在仓库根目录运行 `python3 evidence/translation-audit/all-modified-review-20260922/reconciled-20260923/generate.py`。

## 旧状态修正与边界

旧 `STATE.json` / `PROGRESS.md` 是历史快照：其 remaining、缺失 covered_entry_ids 与 dispatched 状态不能覆盖已落盘事实。本台账逐文件恢复 `gemini-094-01` 与 `sol-092-01`；撤销的 `sol-091-01` 仅作无效来源保留，由 `sol-091-02` 替代。既有10条抽查按 inventory ID 加源文/译文精确文本验证，不用旧总数补覆盖。

校准 pilot40、process-AB40 和 Flash 以 entry-ID 去重。Flash 开发参考源自 AB，不成为第二套独立真值；留出参考标为宿主暂定；两份错输入/重复报告不增加有效覆盖。用户定标仅落到显式映射的 `entry-03627`、`entry-03605`、`entry-03595`，旧状态仍原样保留。

实验 reference、宿主裁决和模型共识都不自动等于人工真值或生产修复。DLC 来源 commit/目标版本映射未固定处，原有 pending 继续保留。需要继续工作时从 `BACKLOG.json` 选择相应类别并回到 `FINDINGS.json` 的原始来源，不应从旧 remaining 数字恢复。
"""
(OUT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    print(json.dumps(validation["counts"], ensure_ascii=False, sort_keys=True))
