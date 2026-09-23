"""Transcribe explicit adjudicator tables; never decide translation semantics."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    report = (ROOT / "reports/v2-adjudication-01.md").read_text()
    entry_matches = re.findall(r"^\| (entry-\d{5}) \| (OK|ISSUE) \| (.*?) \|$", report, re.M)
    defect_matches = re.findall(r"^\| (D\d{2}) \| (entry-\d{5}) \| (.*?) \|$", report, re.M)
    observation_matches = re.findall(r"^\| (O\d{3}) \| (\w+) \| (.*?) \| (.*?) \|$", report, re.M)
    assert len(entry_matches) == 40 and len(defect_matches) == 13 and len(observation_matches) == 52
    assert [o[0] for o in observation_matches] == [f"O{i:03}" for i in range(1, 53)]
    defects = {d: {"entry_id": e, "evidence": text} for d, e, text in defect_matches}
    observations = {
        oid: {"status": status, "defects": re.findall(r"D\d{2}", matched), "rationale": text}
        for oid, status, matched, text in observation_matches
    }
    reference = {
        "status": "provisional_model_adjudicated_not_human_gold",
        "report": "reports/v2-adjudication-01.md",
        "entries": [{"entry_id": e, "status": s, "note": text,
                     "defects": [d for d, v in defects.items() if v["entry_id"] == e]}
                    for e, s, text in entry_matches],
        "canonical_defects": defects,
        "observations": observations,
        "pending": [{"id": "P01", "observation": "O041", "entry_id": "entry-03206",
                     "reason": observations["O041"]["rationale"]}],
    }
    write("REFERENCE.json", reference)
    draft = json.loads((ROOT / "SCORING-DRAFT.json").read_text())
    draft["reference_status"] = reference["status"]
    draft["reference_report"] = reference["report"]
    draft["claim_counting_rule"] = (
        "Unique confirmed canonical defects count only from originally ISSUE observations. "
        "Each originally ISSUE observation with no matched defect and adjudicated advisory/refuted "
        "counts once as a false claim. A mixed observation matching a defect also counts one false "
        "component if the adjudicator explicitly labels a component refuted. This includes reasoning "
        "errors and is an auxiliary defect-and-evidence precision, not a uniformly segmented claim benchmark. "
        "Original ADVISORY/PENDING observations never gain retrospective positive credit."
    )
    for row, ref in zip(draft["entries"], reference["entries"]):
        assert row["entry_id"] == ref["entry_id"]
        row["reference_status"] = ref["status"]
        row["reference_defects"] = ref["defects"]
        for arm in row["arms"].values():
            for obs in arm.get("observations", []):
                decision = observations[obs["id"]]
                obs["adjudication"] = decision
                if obs["original_assertion"] == "ISSUE":
                    arm["confirmed_defects"].extend(decision["defects"])
                    if not decision["defects"] and decision["status"] in {"advisory", "refuted", "mixed"}:
                        arm["refuted_claims"].append(obs["id"])
                    elif decision["defects"] and "**refuted**" in decision["rationale"]:
                        arm["refuted_claims"].append(obs["id"] + ".refuted_component")
                if obs["original_assertion"] == "PENDING" or decision["status"] == "pending":
                    arm["pending_claims"].append(obs["id"])
                if obs["original_assertion"] == "ADVISORY" or decision["status"] == "advisory":
                    arm["advisory_claims"].append(obs["id"])
            arm["confirmed_defects"] = sorted(set(arm["confirmed_defects"]))
    write("SCORING.json", draft)


if __name__ == "__main__":
    main()
