"""Run exactly one preregistered Facts-study external slot."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .config import load_manifest
from .errors import AgentError, ConfigurationError, I18nToolError, ValidationError
from .facts_study import (
    ASSESSMENT_CONTRACT, canonical_sha256, load_arm_prompt, load_study_inputs,
    pi_executable_identity, study_harness_sha256, validate_assessment,
    validate_execution_manifest,
)
from .pi_agent import _pi_environment
from .pi_file_review import _run_file_review_process
from .pi_quality import _decode_quality_model_output, build_quality_evaluator_command
from .facts_curation import (
    CURATION_ASSESSMENT_CONTRACT,
    load_curation_inputs,
    validate_assessment as validate_assessment_v2,
)
from .quality import create_quality_run_directory
from .quality_v2 import read_json_object
from .report import write_json




def _edits_le_one(left: str, right: str) -> bool:
    """True when edit distance is at most one (substitution/insertion/deletion)."""
    if left == right:
        return True
    if abs(len(left) - len(right)) > 1:
        return False
    if len(left) == len(right):
        return sum(a != b for a, b in zip(left, right)) == 1
    short, long = (left, right) if len(left) < len(right) else (right, left)
    for index in range(len(long)):
        if long[:index] + long[index + 1:] == short:
            return True
    return False


def _repair_and_order_items(raw_items: list[dict[str, Any]], sample_items: list[dict[str, Any]]) -> tuple[list[dict[str, Any]] | None, list[tuple[str, str]], list[str]]:
    """Order raw items by the sample and repair single-character revision
    transcription errors; returns (ordered, repairs, errors)."""
    sample_ids = [item["revision_id"] for item in sample_items]
    sample_set = set(sample_ids)
    by_id: dict[str, dict[str, Any]] = {}
    repairs: list[tuple[str, str]] = []
    for item in raw_items:
        if not isinstance(item, dict):
            return None, repairs, ["raw item is not an object"]
        rid = item.get("revision_id")
        if not isinstance(rid, str) or not (63 <= len(rid) <= 65):
            return None, repairs, [f"item revision_id invalid: {str(rid)[:20]!r}"]
        if rid in sample_set:
            by_id[rid] = item
            continue
        candidates = [sid for sid in sample_ids if _edits_le_one(rid, sid)]
        if len(candidates) == 1:
            item["revision_id"] = candidates[0]
            by_id[candidates[0]] = item
            repairs.append((rid, candidates[0]))
        else:
            return None, repairs, [f"item revision_id unrecognized: {rid[:20]}..."]
    ordered: list[dict[str, Any]] = []
    for sid in sample_ids:
        if sid not in by_id:
            return None, repairs, [f"missing item: {sid[:20]}..."]
        ordered.append(by_id[sid])
    if len(ordered) != len(raw_items):
        return None, repairs, ["duplicate or overlapping items"]
    return ordered, repairs, []

DEFAULT_TIMEOUT = 1200


class _TransmissionFailure(RuntimeError):
    """Provider produced no final assistant text (retryable under manifest)."""


def _claim_slot(root: Path, preregistration_id: str, slot: dict[str, Any], schedule: list[dict[str, Any]], authorization_id: str, execution_id: str, enforce_order: bool = True) -> Path:
    directory = root / ".artifacts" / "i18n" / "quality" / "facts-study-campaigns" / preregistration_id
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    authorization_sha256 = hashlib.sha256(authorization_id.encode()).hexdigest()
    if enforce_order:
        for earlier in sorted(schedule, key=lambda value: value["ordinal"]):
            if earlier["ordinal"] >= slot["ordinal"]:
                break
            earlier_path = directory / f"{earlier['slot_id']}.json"
            if not earlier_path.is_file():
                raise ValidationError(
                    f"facts study execution order is frozen; consume ordinal {earlier['ordinal']} before {slot['ordinal']}"
                )
            earlier_ledger = read_json_object(earlier_path, "facts study earlier slot ledger")
            earlier_state = earlier_ledger.get("state")
            if earlier_state not in ("succeeded", "failed"):
                raise ValidationError(f"earlier facts study slot is not terminal: {earlier['slot_id']}")
            if earlier_ledger.get("authorization_sha256") != authorization_sha256:
                raise ValidationError(
                    "Facts study authorization identity differs from the already consumed campaign slots"
                )
    # Parallel mode still requires one shared authorization identity across
    # every consumed slot; slot uniqueness/non-replacement is enforced by the
    # O_EXCL claim below.  A concurrently written ledger may be briefly
    # unreadable; retry shortly, then skip (the final lineage validation
    # checks every ledger).
    import time as _time

    for path in sorted(directory.glob("*.json")):
        if path.name == f"{slot['slot_id']}.json":
            continue
        earlier_ledger = None
        for attempt in range(5):
            try:
                earlier_ledger = read_json_object(path, "facts study earlier slot ledger")
                break
            except ValidationError:
                _time.sleep(0.3 * (attempt + 1))
        if earlier_ledger is None:
            continue
        if earlier_ledger.get("authorization_sha256") != authorization_sha256:
            raise ValidationError(
                "Facts study authorization identity differs from the already consumed campaign slots"
            )
    slot_id = slot["slot_id"]
    path = directory / f"{slot_id}.json"
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise ValidationError(f"facts study slot is already consumed and cannot be replaced: {slot_id}") from error
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump({
            "contract": "tome4-quality-facts-study-slot-ledger-v1",
            "preregistration_id": preregistration_id, "slot_id": slot_id,
            "state": "claimed", "authorization_sha256": authorization_sha256,
            "execution_id": execution_id,
        }, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
    return path


def _update_slot(path: Path, *, state: str, report: str, report_sha256: str) -> None:
    value = read_json_object(path, "facts study slot ledger")
    value["state"] = state
    value["runner_report"] = report
    value["runner_report_sha256"] = report_sha256
    write_json(path, value)


def run_slot(
    *, sample_path: Path, facts_path: Path, neutral_path: Path, gold_path: Path,
    preregistration_path: Path, bundle_paths: list[Path], slot_id: str,
    execution_manifest_path: Path | None = None, authorization_id: str | None = None,
    pool_path: Path | None = None, facts_pool_path: Path | None = None,
    timeout: int = DEFAULT_TIMEOUT, pi_executable: str | None = None,
) -> dict[str, Any]:
    started = time.monotonic()
    manifest = load_manifest()
    prereg_raw = read_json_object(preregistration_path, "facts study preregistration")
    if prereg_raw.get("contract") == "tome4-quality-facts-study-preregistration-v2":
        if execution_manifest_path is None:
            raise ValidationError(
                "offline-frozen curation preregistrations cannot be executed externally; "
                "a user-authorized execution manifest is required"
            )
        execution_manifest = read_json_object(execution_manifest_path, "facts study execution manifest")
        validate_execution_manifest(execution_manifest, preregistration=prereg_raw)
        if not execution_manifest["authorization"]["authorization_id"].strip():
            raise ValidationError("execution manifest authorization_id is empty")
        authorization_id = execution_manifest["authorization"]["authorization_id"]
        enforce_order = execution_manifest["execution"]["mode"] != "parallel"
        transmission_retries = execution_manifest["execution"]["retry"]["transmission_failure_max_retries"]
    else:
        enforce_order = True
        transmission_retries = 0
    if authorization_id is None:
        raise ValidationError("a new explicit Facts-study external authorization ID is required")
    if prereg_raw.get("contract") == "tome4-quality-facts-study-preregistration-v2":
        if pool_path is None or facts_pool_path is None:
            raise ValidationError("curation v2 slots require --pool and --facts-pool")
        sample, facts, neutral, _, prereg, bundles = load_curation_inputs(
            manifest, pool_path=pool_path, sample_path=sample_path,
            facts_pool_path=facts_pool_path, facts_path=facts_path,
            neutral_path=neutral_path, gold_path=gold_path,
            prereg_path=preregistration_path, bundle_paths=bundle_paths,
            harness_sha256=study_harness_sha256(),
        )
    else:
        sample, facts, _, _, prereg, bundles = load_study_inputs(
            manifest, sample_path=sample_path, facts_path=facts_path,
            neutral_path=neutral_path, gold_path=gold_path,
            prereg_path=preregistration_path, bundle_paths=bundle_paths,
        )
    slots = [slot for slot in prereg.get("schedule", []) if slot.get("slot_id") == slot_id]
    if len(slots) != 1:
        raise ValidationError(f"slot is not uniquely preregistered: {slot_id}")
    slot = slots[0]
    bundle = bundles[slot["arm"]]
    prompt = load_arm_prompt(manifest, slot["arm"])
    if hashlib.sha256(prompt.encode()).hexdigest() != slot["prompt_sha256"]:
        raise ValidationError("facts study slot prompt identity mismatch")
    if prereg.get("cache_policy") != "disabled" or prereg.get("replacement_policy") != "forbidden":
        raise ValidationError("facts study runner requires disabled cache and forbidden replacement")
    if not authorization_id.strip():
        raise ValidationError("a new explicit Facts-study external authorization ID is required")

    run = create_quality_run_directory(manifest.root, f"pi-facts-study-{slot_id}")
    run.chmod(0o700)
    local_bundle = run / "bundle.json"
    write_json(local_bundle, bundle)
    raw_path, stderr_path = run / "raw-output.txt", run / "pi-stderr.txt"
    assessment_path, report_path = run / "assessment.json", run / "runner-report.json"
    execution_id = hashlib.sha256(os.urandom(32)).hexdigest()
    ledger = _claim_slot(manifest.root, prereg["preregistration_id"], slot, prereg["schedule"], authorization_id, execution_id, enforce_order=enforce_order)
    report: dict[str, Any] = {
        "contract": "tome4-quality-facts-study-runner-report-v1", "ok": False,
        "study_id": sample["study_id"], "preregistration_id": prereg["preregistration_id"],
        "slot_id": slot_id, "ordinal": slot["ordinal"], "arm": slot["arm"],
        "seed": slot["seed"],
        "execution_id": execution_id,
        "provider": slot["provider"], "model": slot["model"], "thinking": slot["thinking"],
        "harness_sha256": study_harness_sha256(),
        "pi_executable": prereg["pi_executable"],
        "cache_decision": "disabled", "replacement_policy": "forbidden",
        "attempts": 1, "charged_or_possible_transfers": 1, "shards": 1,
        "blind_inputs": {"gold": False, "other_assessments": False, "anchors": False, "holdout": False},
        "report": str(report_path), "run_directory": str(run),
        "runner_report_id": "",
    }
    executable = pi_executable or prereg["pi_executable"]["path"]
    try:
        actual_pi_identity = pi_executable_identity(executable)
    except ConfigurationError as error:
        actual_pi_identity = None
        report.update(error=str(error), elapsed_seconds=round(time.monotonic() - started, 6))
    if actual_pi_identity != prereg["pi_executable"]:
        report.update(error="Pi executable identity does not match preregistration", elapsed_seconds=round(time.monotonic() - started, 6))
        report["runner_report_id"] = canonical_sha256({key: value for key, value in report.items() if key not in ("runner_report_id", "report", "run_directory", "elapsed_seconds")})
        write_json(report_path, report)
        _update_slot(ledger, state="failed", report=str(report_path), report_sha256=hashlib.sha256(report_path.read_bytes()).hexdigest())
        raise AgentError("Pi executable identity mismatch; the claimed slot remains consumed")
    command = build_quality_evaluator_command(
        executable=executable, provider=slot["provider"], model=slot["model"],
        thinking=slot["thinking"], system_prompt=prompt, bundle_path=Path(local_bundle.name),
    )
    command[-1] += f" Preregistered run seed: {slot['seed']}."
    from .proposal import extract_event_stream_output as _extract_stream
    attempts = 0
    last_error: Exception | None = None
    while True:
        attempts += 1
        try:
            result = _run_file_review_process(
                command, cwd=run, env=_pi_environment(manifest.root, slot["provider"]),
                timeout=timeout, raw_output_path=raw_path, stderr_path=stderr_path,
            )
            if result.returncode != 0 or not result.stdout.strip():
                raise AgentError(f"Pi exited with status {result.returncode}")
            # Transmission-layer failures: the provider produced no final
            # assistant text (thinking-only or interrupted stream).  Such
            # failures are retryable under an authorized manifest; content
            # failures are not.
            if not _extract_stream(result.stdout, "Facts study output").strip():
                raise _TransmissionFailure("provider produced no final assistant text")
            output, normalization = _decode_quality_model_output(result.stdout)
            if set(output) != {"items"} or not isinstance(output["items"], list):
                raise ValidationError("Facts study model must return exactly an items array")
            ordered_items, repairs, repair_errors = _repair_and_order_items(output["items"], sample["items"])
            if repair_errors:
                raise ValidationError("items repair failed: " + "; ".join(repair_errors))
            output["items"] = ordered_items
            assessment_contract = (
                CURATION_ASSESSMENT_CONTRACT
                if prereg_raw.get("contract") == "tome4-quality-facts-study-preregistration-v2"
                else ASSESSMENT_CONTRACT
            )
            assessment = {
                "contract": assessment_contract, "schema_version": 1,
                "study_id": sample["study_id"], "slot_id": slot_id,
                "evaluator": {key: slot[key] for key in ("evaluator_id", "provider", "model", "thinking")},
                "bundle_id": bundle["bundle_id"], "bundle_sha256": canonical_sha256(bundle),
                "prompt_sha256": slot["prompt_sha256"], "assessment_state": "complete",
                "items": output["items"],
            }
            if assessment_contract == CURATION_ASSESSMENT_CONTRACT:
                evidence_stats: dict[str, int] = {}
                normalized = validate_assessment_v2(
                    assessment, sample=sample, facts=facts, bundle=bundle, slot=slot,
                    evidence_stats=evidence_stats,
                )
            else:
                evidence_stats = {}
                normalized = validate_assessment(assessment, sample=sample, facts=facts, bundle=bundle, slot=slot)
            write_json(assessment_path, assessment)
            evidence_normalizations = evidence_stats.get("evidence_punctuation_normalized", 0)
            dropped_findings = evidence_stats.get("dropped_findings", 0)
            normalization_parts = []
            if repairs:
                normalization_parts.append(f"transcription-repairs:{len(repairs)}")
            if evidence_normalizations:
                normalization_parts.append(f"evidence-punctuation-normalized:{evidence_normalizations}")
            if dropped_findings:
                normalization_parts.append(f"dropped-findings:{dropped_findings}")
            report.update(
                ok=True, assessment=str(assessment_path), attempts=attempts,
                charged_or_possible_transfers=attempts,
                normalization=",".join(normalization_parts) if normalization_parts else normalization,
                evidence_normalizations=evidence_normalizations,
                dropped_findings=dropped_findings,
                transcription_repairs=len(repairs),
                assessment_sha256=hashlib.sha256(assessment_path.read_bytes()).hexdigest(),
                raw_output_sha256=hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                findings=sum(len(item["findings"]) for item in normalized["items"]),
            )
            last_error = None
            break
        except _TransmissionFailure as error:
            last_error = error
            if attempts <= transmission_retries:
                report["attempts"] = attempts
                report["charged_or_possible_transfers"] = attempts
                report["transmission_retry"] = True
                continue
            report["error"] = str(error)
            break
        except subprocess.TimeoutExpired as error:
            # A per-slot timeout is a pure transmission-layer failure (no
            # model evaluation was produced) and retryable under the manifest.
            last_error = error
            if attempts <= transmission_retries:
                report["attempts"] = attempts
                report["charged_or_possible_transfers"] = attempts
                report["transmission_retry"] = True
                report["transmission_timeout"] = True
                continue
            report["error"] = str(error)
            break
        except (AgentError, ValidationError, OSError) as error:
            last_error = error
            report["error"] = str(error)
            break
    if last_error is not None:
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        report["attempts"] = attempts
        report["charged_or_possible_transfers"] = attempts
        report["runner_report_id"] = canonical_sha256({key: value for key, value in report.items() if key not in ("runner_report_id", "report", "run_directory", "elapsed_seconds")})
        write_json(report_path, report)
        _update_slot(ledger, state="failed", report=str(report_path), report_sha256=hashlib.sha256(report_path.read_bytes()).hexdigest())
        raise AgentError(f"Facts study slot {slot_id} failed and remains consumed: {last_error}; report: {report_path}") from last_error
    report["elapsed_seconds"] = round(time.monotonic() - started, 6)
    report["runner_report_id"] = canonical_sha256({key: value for key, value in report.items() if key not in ("runner_report_id", "report", "run_directory", "elapsed_seconds")})
    write_json(report_path, report)
    _update_slot(ledger, state="succeeded", report=str(report_path), report_sha256=hashlib.sha256(report_path.read_bytes()).hexdigest())
    return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one frozen facts-study-v1 slot")
    parser.add_argument("--sample", required=True, type=Path)
    parser.add_argument("--facts", required=True, type=Path)
    parser.add_argument("--neutral", required=True, type=Path)
    parser.add_argument("--gold", required=True, type=Path)
    parser.add_argument("--preregistration", required=True, type=Path)
    parser.add_argument(
        "--bundle", action="append", required=True, type=Path,
        help="one frozen arm bundle; repeat exactly seven times",
    )
    parser.add_argument("--slot", required=True)
    parser.add_argument("--pool", type=Path, help="curation pool.json (required for v2 preregistrations)")
    parser.add_argument("--facts-pool", type=Path, help="80-item pool facts packet (required for v2 preregistrations)")
    parser.add_argument(
        "--execution-manifest", type=Path,
        help="user-authorized execution manifest (required for offline-frozen v2 preregistrations)",
    )
    parser.add_argument(
        "--authorization-id",
        help="legacy explicit authorization ID for v1 preregistrations",
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--pi-executable")
    return parser


def main(argv: list[str] | None = None) -> int:
    os.umask(0o077)
    arguments = _parser().parse_args(argv)
    try:
        report = run_slot(
            sample_path=arguments.sample, facts_path=arguments.facts,
            neutral_path=arguments.neutral, gold_path=arguments.gold,
            preregistration_path=arguments.preregistration, bundle_paths=arguments.bundle,
            slot_id=arguments.slot, execution_manifest_path=arguments.execution_manifest,
            authorization_id=arguments.authorization_id,
            pool_path=arguments.pool, facts_pool_path=arguments.facts_pool,
            timeout=arguments.timeout, pi_executable=arguments.pi_executable,
        )
    except I18nToolError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return error.exit_code
    print(f"OK  Facts study slot={report['slot_id']} findings={report['findings']} cache=disabled")
    print(f"Assessment: {report['assessment']}")
    print(f"Report: {report['report']}")
    return 0
