# 复审修复（执行者规格，2026-11-09，第 0456 批）

你是 `/workspace/tome4-chinese-translation` 本任务唯一写入者。只改 `tome-orcs.lua` 中下列 4 条的译文（target），**不要 git add/commit/push，不改 source/tag，不动其他文件**。

复审意见原文：`/workspace/tome4-chinese-translation/evidence/lite-review/batches/0456/A.json` 与 `B.json`（verdict 为 ISSUE 的条目，id 见下）。DLC 源码在 `/workspace/tome4-dlcs/orcs/`（来源未固定）。

1. **6331a920c3a8**（Itchy dust，`Throw a handful of dust that is very itchy to touch.`）：末句「致痒强度受蒸汽强度加成」错。源码 data/talents/steam/other.lua 约 1110–1132：失败率只随技能等级，蒸汽强度是施加效果时的命中强度（对抗精神豁免）。改成如「施加瘙痒效果的命中判定受蒸汽强度加成」之类准确且自然的说法（参考库内其他「…的命中判定受…强度加成」/「apply power」类说法保持一致，grep 查）。
2. **07544275a701**（`The target is grappled by %s, pinning them, ...`）：「尾部链锯」改为与同技能描述一致的「尾部蒸汽链锯」（tome-orcs.lua 5334/5338/5341 附近）。
3. **0b1457dd6cae**（`We recognize that times are changing. ...`，源码 data/lore/primal-forest.lua 约 74–81）：按 A、B 意见逐点修正——恢复 it is possible／maybe／yet／some may 等限定语，删去增译（「远远」「看起来是」），把 experienced 译出，修正 a lone megalomaniac destroying much of Eyal 的主体与修饰关系，译出 this proves nothing about … 的论证关系；**并检查换行数**：target 的 LF 数必须等于 source 的 LF 数（B 指出结尾少一个换行）。
4. **4d8260ebdf43**（`The Steam Council has been called to order, ...`，源码 data/lore/palace-fumes.lua 约 90–112）：按 A、B 意见修——「终于能够主持会议，这是我的荣幸」类语序；「为……有了」句式杂糅；「[/i] 的」多余空格；「齐腰高的小傻战士们」生硬；「有无数兽人作战经验」成分残缺（与兽人作战的经验）；结尾辞职前发表长篇演说的先后关系（before），以及「演讲被另一个文件记载」生硬被动句。

## 要求
- 对照英文**整段逐句通读**，把同段里同类问题一并改掉，不要只改被点名的半句；不要改动没有问题的句子的风格。
- 占位符、[i]/[/i] 等标记、颜色码、换行数（LF）与 source 一致；续行 TAB 保持。
- 用 Python 精确替换（assert 命中 1 次），不要用 shell heredoc 写中文，不要整文件重写。
- 自检：`python3 /tmp/srccheck.py tome-orcs.lua` identical；`TOME_LUAJIT=/usr/bin/luajit TOME_LUAROCKS_ROOT=/opt/tome4-luarocks python3 -B tools/i18n lint --strict` 0 错误；`git diff --check` 无输出；用 luajit 加载 tome-orcs.lua 核对这 4 条 source/target 的 LF 数相等。
- 写 `/tmp/revchk/exec2-report.json`：每条 `{"id","old","new","note"}`（长文可只写改动的句子对）。
- 最终回复只写一行：`EXECUTOR revchk2 DONE n=4`。
