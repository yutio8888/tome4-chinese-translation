"""Rebuild mechanical mappings and counts from the frozen source adjudication."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARMS = {"opus": "opus-01", "sol": "sol-01", "gemini": "gemini-01"}


def write(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def table_rows(text):
    for line in text.splitlines():
        if line.startswith("|") and line.endswith("|"):
            yield [cell.strip() for cell in line[1:-1].split("|")]


def plain(value):
    return value.replace("**", "").replace("`", "")


def main():
    report = (ROOT / "reports/adjudication-01.md").read_text()
    mapping = json.loads((ROOT / "ANON-MAPPING-HOST-ONLY.json").read_text())
    original = {o["observation_id"]: o for o in mapping["observations"]}
    refs, defects, decisions = [], {}, {}
    for cells in table_rows(report):
        key = plain(cells[0])
        if re.fullmatch(r"entry-\d{5}", key) and plain(cells[1]) in {"OK", "ISSUE", "PENDING"}:
            refs.append({"entry_id": key, "status": plain(cells[1]), "note": cells[2]})
        elif re.fullmatch(r"D\d+", key) and re.fullmatch(r"entry-\d{5}", plain(cells[1])):
            defects[key] = {"entry_id": plain(cells[1]), "evidence": " | ".join(cells[2:])}
        elif re.fullmatch(r"O\d+", key):
            assert key in original
            decisions[key] = {"status": plain(cells[1]), "defects": re.findall(r"D\d+", cells[2]),
                              "rationale": " | ".join(cells[3:])}
    expected = [e["audit_id"] for e in json.loads((ROOT / "entries.json").read_text())]
    assert [r["entry_id"] for r in refs] == expected
    assert set(decisions) == set(original), (len(decisions), len(original))
    for oid, decision in decisions.items():
        assert decision["status"] in {"confirmed", "refuted", "pending", "advisory", "mixed"}
        assert all(d in defects and defects[d]["entry_id"] == original[oid]["entry_id"]
                   for d in decision["defects"])
    for ref in refs:
        ref["defects"] = [d for d, v in defects.items() if v["entry_id"] == ref["entry_id"]]
        assert bool(ref["defects"]) == (ref["status"] == "ISSUE")
    reference = {"status": "provisional_model_adjudicated_not_human_gold",
                 "report": "reports/adjudication-01.md", "entries": refs,
                 "canonical_defects": defects, "observations": decisions,
                 "pending_observations": [o for o, v in decisions.items() if v["status"] == "pending"]}
    write("REFERENCE.json", reference)
    scoring = {"primary_eligibility": {a: True for a in ARMS},
               "protocol": "v3_temp_allowed_g17", "reference_status": reference["status"],
               "reference_report": reference["report"], "claim_counting_rule": "SCORING-RULES.md",
               "entries": []}
    for index, ref in enumerate(refs):
        row = {"entry_id": ref["entry_id"], "reference_status": ref["status"],
               "reference_defects": ref["defects"], "arms": {}}
        for arm, name in ARMS.items():
            raw = mapping["tables"][name][index]
            assert raw["entry_id"] == ref["entry_id"]
            value = {"verdict": raw["verdict"], "confirmed_defects": [], "refuted_claims": [],
                     "pending_claims": [], "advisory_claims": [], "observations": [],
                     "raw_table_note": raw["note"], "source_report": f"reports/{name}.md"}
            for oid, original_obs in original.items():
                if original_obs["origin"] != name or original_obs["entry_id"] != ref["entry_id"]:
                    continue
                decision = decisions[oid]
                value["observations"].append({"id": oid, "claim_id": original_obs["claim_id"],
                    "original_assertion": original_obs["original_assertion"], "adjudication": decision})
                if original_obs["original_assertion"] == "ISSUE":
                    value["confirmed_defects"].extend(decision["defects"])
                    if not decision["defects"] and decision["status"] in {"advisory", "refuted", "mixed"}:
                        value["refuted_claims"].append(oid)
                    elif decision["defects"] and "refuted" in decision["rationale"]:
                        value["refuted_claims"].append(oid + ".refuted_component")
                if original_obs["original_assertion"] == "PENDING" or decision["status"] == "pending":
                    value["pending_claims"].append(oid)
                if original_obs["original_assertion"] == "ADVISORY" or decision["status"] == "advisory":
                    value["advisory_claims"].append(oid)
            value["confirmed_defects"] = sorted(set(value["confirmed_defects"]))
            row["arms"][arm] = value
        scoring["entries"].append(row)
    write("SCORING.json", scoring)


if __name__ == "__main__":
    main()

