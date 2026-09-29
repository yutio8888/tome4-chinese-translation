"""Freeze the already-authorized remaining 40-entry research groups, without reviews."""
import csv
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

SERIES = Path(__file__).resolve().parent
EXPERIMENTS = SERIES.parent
BASE = EXPERIMENTS.parent
OLD = EXPERIMENTS / "abc-40-b096-20260923"
COMMIT = "624a67329fe2ad440c5b344785a9c73fcf22ae63"


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def git(*args):
    return subprocess.check_output(["git", *args])


def main():
    series = json.loads((SERIES / "STATE.json").read_text())
    inventory = json.loads((BASE / "inventory.json").read_text())
    indexed = {e["audit_id"]: e for e in inventory["entries"]}
    access = json.loads((BASE / "source-access.json").read_text())
    dlc = json.loads((SERIES / "DLC-SOURCE-REGISTRY.json").read_text())
    terms = []
    for path in sorted(Path("terminology").glob("*.tsv")):
        terms.extend(list(csv.DictReader(path.open(), delimiter="\t")))
    locale_cache = {}
    baseline = {
        "head": git("rev-parse", "HEAD").decode().strip(),
        "git_status": git("status", "--short").decode(),
        "locale_sha256": {p: sha(Path(p).read_bytes()) for p in json.loads((OLD / "BASELINE.json").read_text())["locale_sha256"]},
        "campaign_state_sha256": sha((BASE / "STATE.json").read_bytes()),
        "inventory_sha256": sha((BASE / "inventory.json").read_bytes()),
        "prior_experiment": OLD.name,
        "prior_experiment_files_sha256": {str(p.relative_to(OLD)): sha(p.read_bytes()) for p in OLD.rglob("*") if p.is_file()},
    }
    for group in series["groups"]:
        if group["index"] < 4:
            continue
        root = EXPERIMENTS / group["directory"]
        if root.exists():
            raise RuntimeError(f"Refuse overwrite {root}")
        root.mkdir()
        rows = [indexed[eid] for eid in group["entry_ids"]]
        assert len(rows) == 40 and all(e["gemini_status"] == "queued" and e["prior_spotcheck"] is None for e in rows)
        dump(root / "entries.json", rows)
        context_parts, frozen_sources, sections_meta = [], {}, []
        for logical_path in sorted({e["logical_path"] for e in rows}):
            if logical_path not in locale_cache:
                locale_cache[logical_path] = git("show", inventory["snapshot_commit"] + ":" + logical_path).decode()
            locale = locale_cache[logical_path]
            sections = sorted({e["section"] for e in rows if e["logical_path"] == logical_path})
            marks = list(re.finditer(r'^section "([^"]+)"', locale, re.M))
            found = [locale[m.start():marks[n+1].start() if n+1 < len(marks) else len(locale)]
                     for n, m in enumerate(marks) if m.group(1) in sections]
            assert len(found) == len(sections)
            context_parts.extend(found)
            for section in sections:
                component = next(e["component"] for e in rows if e["section"] == section)
                if component in dlc:
                    src = SERIES / "sources" / component / section
                    blob = src.read_bytes()
                    assert sha(blob) == dlc[component]["files_sha256"][section]
                    relative = "dlc/" + component + "/" + section
                    pin = "unpinned"
                elif component in {"addon-dev", "items-vault", "possessors"}:
                    sections_meta.append({"section": section, "component": component,
                                          "source_pinning": "unavailable", "source_path": None})
                    continue
                else:
                    matches = [(prefix, replacement) for prefix, replacement in access["engine"]["mappings"].items()
                               if section.startswith(prefix)]
                    assert matches
                    prefix, replacement = max(matches, key=lambda pair: len(pair[0]))
                    path = replacement + section[len(prefix):]
                    blob = subprocess.check_output(["git", "-C", "/workspace/t-engine4", "show", COMMIT + ":" + path])
                    relative = path
                    pin = COMMIT
                dest = root / "sources" / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(blob)
                frozen_sources[relative] = sha(blob)
                sections_meta.append({"section": section, "component": component, "source_pinning": pin,
                                      "source_path": "sources/" + relative})
        (root / "context.lua").write_text("\n".join(context_parts))
        selected_components = sorted({e["component"] for e in rows})
        dlc_refs = {c: {"source_pinning": "unpinned",
                       "root": str((SERIES / "sources" / c).resolve()),
                       "files_sha256": dlc[c]["files_sha256"]}
                    for c in selected_components if c in dlc}
        dump(root / "source-access.json", {
            "engine_repository": "/workspace/t-engine4", "engine_commit": COMMIT,
            "files_sha256": frozen_sources, "sections": sections_meta, "dlc_additional_sources": dlc_refs,
            "unavailable_components": [c for c in selected_components if c in {"addon-dev", "items-vault", "possessors"}],
            "rule": "Entry source files allowed; additional single files only along explicit calls/symbols. DLC snapshot unpinned; never substitute engine commit."
        })
        header = (OLD / "INPUT.md").read_text().split("## entry-03212")[0]
        first, last = rows[0]["audit_id"], rows[-1]["audit_id"]
        header = header.replace("entry-03212–03251", first + "–" + last).replace("entry-03212", first)
        header = header.replace("统一复核规则 v3（临时文件许可）", "统一复核规则 v3-source（临时文件与混合来源）")
        header = header.replace("abc40-b096-", root.name + "-")
        header = re.sub(r"2\. 游戏机制.*?不得仅凭变量名或英文猜机制。",
            "2. 游戏机制以可核验的实际源码行为为准。本体固定commit " + COMMIT +
            "；DLC使用source-access列明且哈希固定的公开快照，源码仓库/commit未固定，必须显式标注。DLC机制疑点可陈述快照内已证事实，但目标版本适用性缺口保留待确认，不将引擎commit套用DLC。缺源码的组件仅确认文本或格式直接可证的问题，机制依赖疑点待确认。英文、术语或旧译不能覆盖源码；沿袭上游的误述和翻译新增分开，不仅凭变量名猜机制。",
            header)
        header = re.sub(r"3\. 可读本 INPUT.*?可搜索这些文件内的文本。",
            "3. 可读本INPUT、entries.json、context.lua、source-access.json及其中sections列明的本组sources文件。可在这些单文件内搜索。源码缺失已明确列在unavailable_components，不把其他组件同名代码当作它的证据。", header)
        header = re.sub(r"4\. 需要追调用链时，.*?无法在该边界内找到证据时写待确认。",
            "4. 追调用链时，本体只能git -C /workspace/t-engine4 show " + COMMIT +
            ":<明确相关的单文件path>；DLC只能读取source-access中dlc_additional_sources列明、哈希匹配的相关单文件。每个新增文件说明哪个已读调用/符号/require引入。禁止当前源码工作树、其他commit、整目录git grep/rg/find或历史审核查找；不能读取共享DLC快照中的locales等其他语言答案。证据不足写待确认。", header)
        blocks = [header]
        for e in rows:
            blocks.append(f"## {e['audit_id']}\n位置：{e['logical_path']}:{e['line']}；section：{e['section']}；source_tag：{e['source_tag']}；args_order：{e['args_order']}；special：{e['special']}\n\n原文：\n```text\n{e['source']}\n```\n译文：\n```text\n{e['target']}\n```\n")
        source_text = "\n".join(e["source"].lower() for e in rows)
        columns = ["source", "target", "category", "domain", "source_tag", "status", "scope", "notes"]
        relevant = [t for t in terms if t.get("source") and t["source"].lower() in source_text]
        unique = {tuple(t.get(k, "") for k in columns) for t in relevant}
        blocks += ["## 相关术语快照\n仅按source_tag/category/语境适用；existing不构成强制改名。\n```tsv",
                   "\t".join(columns), *["\t".join(t) for t in sorted(unique)], "```\n"]
        (root / "INPUT.md").write_text("\n".join(blocks))
        dump(root / "BASELINE.json", dict(baseline, sample_rule="series frozen queue order; exclude previously reviewed entries"))
        dump(root / "SCOPE.json", {"mode": "review_only_research", "entries": group["entry_ids"],
                                  "write_allowed": [str(root) + "/**"], "temporary_files": "task-specific allowed",
                                  "production_writes": False, "components": selected_components})
        for name in ["SPEC.md", "PLAN.md", "SCORING-RULES.md"]:
            text = (OLD / name).read_text().replace("batch-096", f"series-group-{group['index']:02}")
            text = text.replace("entry-03212–03251", first + "–" + last)
            text += "\n本组属于用户授权累计20组；完成后自动推进。来源规则以本组INPUT和source-access为准：本体固定commit，DLC快照commit未固定，缺源码机制项pending。40条可能跨旧生产batch边界，绝不复用已审条目。\n"
            (root / name).write_text(text)
        for name in ["score.py", "record.py", "extract_observations.py", "build_scoring.py", "render_findings.py"]:
            (root / name).write_text((OLD / name).read_text().replace("b096", f"g{group['index']:02}"))
        dump(root / "STATE.json", {"task_id": root.name, "series_group": group["index"], "mode": "review_only",
                                  "state": "FROZEN", "orchestration_transport": "mcp",
                                  "workspace_id": series["workspace_id"],
                                  "orchestrator_agent_id": series["orchestrator_agent_id"],
                                  "strict_contract_completion_claimed": False,
                                  "user_authorization": series["user_authorization"], "child_dispatches": [],
                                  "reference_plan": "blind full40 then fresh anonymous adjudication; provisional model reference"})
        frozen = ["INPUT.md", "entries.json", "context.lua", "source-access.json", "SPEC.md", "PLAN.md",
                  "SCORING-RULES.md", "SCOPE.json"]
        files = [root / p for p in frozen] + list((root / "sources").rglob("*.lua")) if (root / "sources").exists() else [root / p for p in frozen]
        dump(root / "FREEZE.json", {"files_sha256": {str(p.relative_to(root)): sha(p.read_bytes()) for p in files},
                                  "count": 40, "engine_commit": COMMIT, "dlc_commit": "unpinned"})
        for folder in ["reports", "raw", "dispatches"]:
            (root / folder).mkdir()
        prompt = ("你是本任务 REVIEWER，purpose=translation_contextual_v1。沿用用户授权的自然语言实验旁路；"
                  "只读冻结输入及其明确允许的材料，临时文件按输入中的用户许可执行。独立完成全部40条复核，"
                  "不读其他报告，不创建子agent，不修改仓库，不声称生产DONE_VERIFIED。唯一入口：" +
                  str((root / "INPUT.md").resolve()))
        (root / "dispatches/common-prompt.txt").write_text(prompt)
        group["state"] = "FROZEN"
        group["input_sha256"] = sha((root / "INPUT.md").read_bytes())
        print(group["index"], len(rows), selected_components, len(frozen_sources))
    dump(SERIES / "STATE.json", series)


if __name__ == "__main__":
    main()

