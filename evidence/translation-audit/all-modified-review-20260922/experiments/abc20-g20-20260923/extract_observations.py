"""Mechanical extraction only: preserve exact source blocks and original assertions."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORTS = ["opus-01", "sol-01", "gemini-01", "reference-blind-01"]
STATES = {"存在问题": "ISSUE", "未发现问题": "OK", "仅建议": "ADVISORY", "待确认": "PENDING"}


def extract(names):
    observations, tables = [], {}
    for name in names:
        path = ROOT / "reports" / (name + ".md")
        text = path.read_text()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows = re.findall(r"^\|\s*(entry-\d{5})\s*\|\s*(未发现问题|存在问题|仅建议|待确认)\s*\|\s*(.*?)\s*\|$", text, re.M)
        assert len(rows) == 40, (name, len(rows))
        tables[name] = [{"entry_id": e, "verdict": STATES[s], "note": n} for e, s, n in rows]
        headings = list(re.finditer(r"^###\s+(C\d+)\s*\|\s*(entry-\d{5})\s*\|\s*(存在问题|仅建议|待确认).*?$", text, re.M))
        assert headings, name
        for heading in headings:
            following = re.search(r"^#{1,3} ", text[heading.end():], re.M)
            end = heading.end() + following.start() if following else len(text)
            footer = text.find("\n本次共判定：", heading.end())
            if footer >= 0:
                end = min(end, footer)
            block = text[heading.start():end]
            observations.append({"origin": name, "claim_id": heading[1], "entry_id": heading[2],
                                 "original_assertion": STATES[heading[3]], "text": block,
                                 "start": heading.start(), "end": end, "source_sha256": digest})
    observations.sort(key=lambda o: (o["entry_id"], o["text"]))
    for index, observation in enumerate(observations, 1):
        observation["observation_id"] = f"O{index:03}"
    return {"rule": "exact text blocks sorted by entry and text, no semantic merging",
            "tables": tables, "observations": observations}


if __name__ == "__main__":
    import sys
    names = REPORTS if "--complete" in sys.argv else REPORTS[:3]
    result = extract(names)
    dest = "ANON-MAPPING-HOST-ONLY.json" if "--complete" in sys.argv else "EXTRACTION-PARTIAL.json"
    (ROOT / dest).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"reports": names, "observations": len(result["observations"])}))
