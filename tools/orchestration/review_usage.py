#!/usr/bin/env python3
"""Compare explicit, provider-neutral per-request usage records on stdout."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat
import sys

MAX_BYTES = 8 * 1024 * 1024
MAX_RECORDS = 10000
SCHEMA = "review-usage-records/1"
COUNTERS = ("input_tokens", "output_tokens")
RELATIONSHIPS = ("subset_of_input", "separately_measured")
SCOPES = ("request", "last_usage_snapshot")


class UsageError(ValueError):
    pass


def _object(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise UsageError(f"{label} requires exactly: {', '.join(keys)}")
    return value


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise UsageError(f"{label} must be a nonempty string")
    return value


def _counter(value, label):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise UsageError(f"{label} must be null or a nonnegative integer (bool is invalid)")
    return value


def _instant(value, label):
    _text(value, label)
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError as error:
        raise UsageError(f"{label} must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise UsageError(f"{label} must include an offset")
    return parsed.astimezone(timezone.utc)


def validate(document):
    _object(document, ("schema", "records"), "document")
    if document["schema"] != SCHEMA:
        raise UsageError(f"schema must be {SCHEMA}")
    records = document["records"]
    if not isinstance(records, list) or len(records) > MAX_RECORDS:
        raise UsageError(f"records must be an array of at most {MAX_RECORDS} items")
    seen = set()
    normalized = []
    record_keys = ("request_id", "role", "batch", "phase", "counter_scope", "usage", "interval")
    for index, record in enumerate(records):
        label = f"records[{index}]"
        _object(record, record_keys, label)
        request_id = _text(record["request_id"], label + ".request_id")
        if request_id in seen:
            raise UsageError(f"duplicate request_id: {request_id}")
        seen.add(request_id)
        if record["role"] not in ("ORCHESTRATOR", "CHILD"):
            raise UsageError(label + ".role must be ORCHESTRATOR or CHILD")
        batch = _text(record["batch"], label + ".batch")
        phase = _text(record["phase"], label + ".phase")
        if record["counter_scope"] not in SCOPES:
            raise UsageError(label + ".counter_scope must be request or last_usage_snapshot")
        usage = _object(record["usage"], ("input_tokens", "cached_input", "output_tokens"), label + ".usage")
        input_tokens = _counter(usage["input_tokens"], label + ".usage.input_tokens")
        output_tokens = _counter(usage["output_tokens"], label + ".usage.output_tokens")
        cached = usage["cached_input"]
        if cached is not None:
            _object(cached, ("tokens", "relationship"), label + ".usage.cached_input")
            cached_tokens = _counter(cached["tokens"], label + ".usage.cached_input.tokens")
            if cached_tokens is None:
                raise UsageError(label + ".usage.cached_input.tokens cannot be null; use cached_input=null")
            if cached["relationship"] not in RELATIONSHIPS:
                raise UsageError(label + ".usage.cached_input.relationship is invalid")
            if (cached["relationship"] == "subset_of_input" and input_tokens is not None
                    and cached_tokens > input_tokens):
                raise UsageError(label + ": cached subset exceeds input_tokens")
            cached = {"tokens": cached_tokens, "relationship": cached["relationship"]}
        interval = record["interval"]
        parsed_interval = None
        if interval is not None:
            _object(interval, ("started_at", "ended_at"), label + ".interval")
            started = _instant(interval["started_at"], label + ".interval.started_at")
            ended = _instant(interval["ended_at"], label + ".interval.ended_at")
            if ended < started:
                raise UsageError(label + ".interval ends before it starts")
            parsed_interval = (started, ended)
        normalized.append({
            "request_id": request_id,
            "role_group": "ORCHESTRATOR" if record["role"] == "ORCHESTRATOR" else "CHILDREN",
            "batch": batch,
            "phase": phase,
            "counter_scope": record["counter_scope"],
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cached_input": cached,
            "interval": parsed_interval,
        })
    return normalized


def _metric(records, name):
    values = [record[name] for record in records]
    known = [value for value in values if value is not None]
    return {"known_sum": sum(known) if known else None,
            "known_records": len(known), "unknown_records": len(values) - len(known)}


def _cached(records):
    result = {}
    for relationship in RELATIONSHIPS:
        selected = [record["cached_input"]["tokens"] for record in records
                    if record["cached_input"] is not None
                    and record["cached_input"]["relationship"] == relationship]
        result[relationship] = {"known_sum": sum(selected) if selected else None,
                                "known_records": len(selected)}
    result["unknown_records"] = sum(record["cached_input"] is None for record in records)
    return result


def _uncached_subset(records):
    known = []
    for record in records:
        cached = record["cached_input"]
        if (record["input_tokens"] is not None and cached is not None
                and cached["relationship"] == "subset_of_input"):
            known.append(record["input_tokens"] - cached["tokens"])
    return {"known_sum": sum(known) if known else None, "known_records": len(known),
            "unknown_records": len(records) - len(known)}


def _elapsed(records):
    intervals = [record["interval"] for record in records if record["interval"] is not None]
    if not intervals:
        elapsed = None
    else:
        elapsed = round((max(end for _, end in intervals) - min(start for start, _ in intervals)).total_seconds() * 1000, 3)
    return {"observed_span_ms": elapsed, "interval_records": len(intervals),
            "missing_interval_records": len(records) - len(intervals)}


def _measurement(records):
    return {
        "records": len(records),
        "input_tokens": _metric(records, "input_tokens"),
        "cached_input_tokens": _cached(records),
        "input_excluding_cached_subset_tokens": _uncached_subset(records),
        "output_tokens": _metric(records, "output_tokens"),
    }


def _group(records):
    return {
        "records": len(records),
        "elapsed": _elapsed(records),
        "measurements": {scope: _measurement([r for r in records if r["counter_scope"] == scope])
                         for scope in SCOPES},
    }


def report(records):
    role_groups = {role: _group([r for r in records if r["role_group"] == role])
                   for role in ("ORCHESTRATOR", "CHILDREN")}
    scope_keys = sorted({(r["batch"], r["phase"]) for r in records})
    scopes = []
    for batch, phase in scope_keys:
        selected = [r for r in records if r["batch"] == batch and r["phase"] == phase]
        scopes.append({"batch": batch, "phase": phase,
                       "elapsed": _elapsed(selected),
                       "role_groups": {role: _group([r for r in selected if r["role_group"] == role])
                                       for role in ("ORCHESTRATOR", "CHILDREN")}})
    return {
        "schema": "review-usage-report/1",
        "records": len(records),
        "semantics": {
            "missing_counters": "unknown, never measured zero",
            "last_usage_snapshot": "snapshot only, never a whole-session total",
            "elapsed": "observed min-start to max-end span; overlapping requests are not summed",
            "cost": "not calculated",
        },
        "role_groups": role_groups,
        "scopes": scopes,
    }


def load(path):
    try:
        if not stat.S_ISREG(path.lstat().st_mode):
            raise UsageError("input must be a regular file (symlinks and special files are rejected)")
        with path.open("rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise UsageError("input changed or is not a regular file")
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise UsageError(f"input exceeds {MAX_BYTES} bytes")
        return json.loads(data, object_pairs_hook=_reject_duplicates)
    except (OSError, json.JSONDecodeError) as error:
        raise UsageError(str(error)) from error


def _reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise UsageError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path, help="one explicit review-usage-records/1 JSON file")
    args = parser.parse_args(argv)
    try:
        result = report(validate(load(args.records)))
    except UsageError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
