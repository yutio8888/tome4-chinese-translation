"""Replay the pilot's mechanical counts from explicitly adjudicated rows.

This never decides translation semantics. Run: python3 -B score.py SCORING.json.
"""
import itertools
import json
import sys

ARMS = ("opus", "sol", "gemini")
DEFINITE = {"ISSUE", "OK", "ADVISORY"}


def correct(row, arm):
    observation = row["arms"][arm]
    if observation["verdict"] not in DEFINITE:
        return False
    if row["reference_status"] == "OK":
        return observation["verdict"] in {"OK", "ADVISORY"}
    return observation["verdict"] == "ISSUE" and bool(
        set(observation["confirmed_defects"]) & set(row["reference_defects"])
    )


def ratio(n, d):
    return {"numerator": n, "denominator": d, "rate": n / d if d else None}


def score(data):
    rows = data["entries"]
    eligibility = data.get("primary_eligibility", {a: True for a in ARMS})
    assert set(eligibility) == set(ARMS)
    assert len(rows) == 40 and len({r["entry_id"] for r in rows}) == 40
    for row in rows:
        assert row["reference_status"] in {"OK", "ISSUE", "PENDING"}
        assert set(row["arms"]) == set(ARMS)
        assert bool(row["reference_defects"]) == (row["reference_status"] == "ISSUE")
        for arm in ARMS:
            a = row["arms"][arm]
            assert a["verdict"] in DEFINITE | {"PENDING", "MISSING"}
            assert set(a["confirmed_defects"]) <= set(row["reference_defects"])
            for field in ("confirmed_defects", "refuted_claims", "pending_claims"):
                assert len(a[field]) == len(set(a[field])), (row["entry_id"], arm, field)
    resolved = [r for r in rows if r["reference_status"] != "PENDING"]
    common = [r for r in resolved if all(r["arms"][a]["verdict"] in DEFINITE for a in ARMS)]
    result = {
        "reference_status": "provisional model-adjudicated reference, not human gold",
        "primary_eligibility": eligibility,
        "formal_three_arm_comparison_available": all(eligibility.values()),
        "ineligible_arm_metrics": "diagnostic only; exclude from compliant-arm rankings",
        "total": len(rows), "resolved_reference": len(resolved),
        "reference_pending": [r["entry_id"] for r in rows if r not in resolved],
        "common_denominator": len(common), "arms": {}, "paired": {},
    }
    positives = sum(r["reference_status"] == "ISSUE" for r in resolved)
    for arm in ARMS:
        matched = sum(r["reference_status"] == "ISSUE" and correct(r, arm) for r in resolved)
        reported = [r for r in resolved if r["arms"][arm]["verdict"] == "ISSUE"]
        false_positive_entries = [r["entry_id"] for r in reported if r["reference_status"] == "OK"]
        wrong_reason = [r["entry_id"] for r in reported if r["reference_status"] == "ISSUE" and not correct(r, arm)]
        missed = [r["entry_id"] for r in resolved if r["reference_status"] == "ISSUE" and not correct(r, arm)]
        result["arms"][arm] = {
            "eligible_for_primary": eligibility[arm],
            "common_accuracy": ratio(sum(correct(r, arm) for r in common), len(common)),
            "all_resolved_accuracy_abstention_not_correct": ratio(sum(correct(r, arm) for r in resolved), len(resolved)),
            "issue_entry_precision_with_correct_reason": ratio(matched, len(reported)),
            "issue_entry_recall": ratio(matched, positives),
            "false_positive_entries": false_positive_entries,
            "wrong_reason_positive_entries": wrong_reason,
            "false_negative_entries": missed,
            "model_abstentions": [r["entry_id"] for r in resolved if r["arms"][arm]["verdict"] not in DEFINITE],
            "verdict_counts_all40": {v: sum(r["arms"][arm]["verdict"] == v for r in rows) for v in sorted(DEFINITE | {"PENDING", "MISSING"})},
        }
        known_correct = sum(correct(r, arm) for r in resolved)
        possible_extra = sum(r["reference_status"] == "PENDING" and r["arms"][arm]["verdict"] in DEFINITE for r in rows)
        result["arms"][arm]["all40_unresolved_reference_bounds_not_confidence_interval"] = {
            "lower": known_correct / len(rows),
            "upper": (known_correct + possible_extra) / len(rows),
        }
        true_claims = sum(len(set(r["arms"][arm]["confirmed_defects"])) for r in resolved if r["arms"][arm]["verdict"] == "ISSUE")
        false_claims = sum(len(r["arms"][arm]["refuted_claims"]) for r in resolved if r["arms"][arm]["verdict"] == "ISSUE")
        all_defects = sum(len(set(r["reference_defects"])) for r in resolved)
        result["arms"][arm]["claim_precision_resolved_only"] = ratio(true_claims, true_claims + false_claims)
        result["arms"][arm]["claim_recall"] = ratio(true_claims, all_defects)
        result["arms"][arm]["pending_claim_count"] = sum(len(r["arms"][arm]["pending_claims"]) for r in rows)
    for left, right in itertools.combinations(ARMS, 2):
        result["paired"][left + "_vs_" + right] = {
            "eligible_for_primary": eligibility[left] and eligibility[right],
            "left_only_correct": [r["entry_id"] for r in common if correct(r, left) and not correct(r, right)],
            "right_only_correct": [r["entry_id"] for r in common if correct(r, right) and not correct(r, left)],
            "both_correct": sum(correct(r, left) and correct(r, right) for r in common),
            "both_incorrect": sum(not correct(r, left) and not correct(r, right) for r in common),
        }
    return result


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as stream:
        print(json.dumps(score(json.load(stream)), ensure_ascii=False, indent=2))
