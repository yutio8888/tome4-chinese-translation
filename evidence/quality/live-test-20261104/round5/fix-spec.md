# 修复任务：实机测试第五轮问题（r5-opus，22 条中按下列裁决执行）

你是本仓库 `/workspace/tome4-chinese-translation` 的唯一写入者（EXECUTOR）。可改任何 *.lua 译文文件（含 DLC、engine），**不改**工具、文档、terminology/（若某处改动与 terminology/ 中 preferred 行冲突，停下并在报告中说明，不改该处）。不提交 git。
问题原文（含屏幕原文、英文、库内行号、建议）见 `/tmp/r5fix/findings.jsonl`，按 id 对照。

## 通用要求
- 只改 target（第二个字符串）或按本单要求**新增** t(...) 行；保留占位符个数与顺序、颜色码、换行。
- 同一英文 source（同 tag）在多个 *.lua 出现时必须同步修改（`grep -n -F` 全仓查）。
- **每改一条，把占位符代入示例值，连同它被嵌入的上下文句一起通读**，确保通顺、无病句、中文全角标点、中文词之间无多余半角空格（数字与中文之间的空格按本库习惯保留）。
- 全部改完运行 `TOME_LUAJIT=/usr/bin/luajit TOME_LUAROCKS_ROOT=/opt/tome4-luarocks python3 -B tools/i18n lint --strict`，必须 0 errors。

## 执行
- r5-opus-01：717/718/721 名称后缀模板的半角「, 」改全角「，」，与 719/720/723/724 一致。
- r5-opus-02：手札标题 19707「残破的纸片（巨魔沼泽）」改为与物品名一致的「破烂的碎纸片（巨魔沼泽）」。
- r5-opus-03：1079 楼梯提示改全角括号，引号与按键写法通顺，如「这里有%s（按“<”“>”键或右键使用）。」。先查 %s 实际代入（a_an 的中文结果是否已含「一个」），保证代入后不重复不缺量词。
- r5-opus-04：11448「给%s的信 (%d)」改「写给%s的信 (%d)」。
- r5-opus-05：16653 手札标题「日记页（卡·普尔）」改「日记书页（卡·普尔）」；若同族还有其他「日记页（…）」手札标题，一并统一。
- r5-opus-06：通用地形名 next level / previous level（约 8 处「前往下一层」「前往上一层」，entity name）改为名词「通往下一层的通道」「通往上一层的通道」；核对代入 1079 后读作「这里有一个通往下一层的通道（…）」。不要改已有专用译名（如巨魔沼泽「通往下一层的路」）。
- r5-opus-07：20217 护送任务名模板改全角括号「护送：%s（…）」，括号内保持原有结构。
- r5-opus-08：符文/纹身短描述后缀整组（findings 列出的 25880–26016 一带全部）统一：分隔符用全角「；」，前后不加空格；项目顺序统一为「名称 数值」，如「减伤 %d%%；解除 %s；持续 %d；冷却 %d」「加速 %d%%；冷却 %d」；补上缺失的分隔符。逐条对照英文，不得丢项。
- r5-opus-09 / 16：175「%d 治疗」改「%d 点治疗」，174 同族同步（括号改全角）；501 `#Target# receives %s from #Source#.` 改「#Target#从#Source#获得%s。」；500 保持「#Source#受到%s。」。通读「棕色霉菌受到88 点治疗。」「Opus从纹身：治疗获得69 点治疗。」。
- r5-opus-10：43118（及 1766 帮助文本同句）Dexterity 说明中 agile 不得译作「灵巧」（Cunning 的正式译名），改如「身手灵活、反应警觉」。
- r5-opus-11：29779 去掉颜色码两侧空格：「一股#LIGHT_BLUE#冰冷的水流#LAST#从地面涌出！」。
- r5-opus-12：835「技能%s: 」改「技能%s：」。
- r5-opus-13：月份 Wintertide「霜华」→「霜华月」、Summertide「炎华」→「炎华月」（3892、3898 及全仓同 source 同步）；先查 terminology/ 是否有 preferred 行，有则停下说明。
- r5-opus-14：新增 `t("Easy", "简单", "birth descriptor name")`，放在 3210 `Easier` 条目旁；再查无 context 的 `_t(e.descriptor.difficulty)` 路径是否需要 `"_t"` 版 Easy 条目，若需要且不与其他 "Easy" 用法冲突则一并新增。
- r5-opus-15：24529「#Target#挡住了#Source#！」去空格。
- r5-opus-19：42047–42051 任务横幅五条去掉中文词间空格（颜色码位置保留），如「#LIGHT_GREEN#新#LAST#任务！」「任务#AQUAMARINE#更新了！」。
- r5-opus-20：26735 伤害来源名「近战报复」改「近战反伤」，与 168「近战反伤：」、26736 一致；816、35704 不改。
- r5-opus-21：bear paw「熊爪」改「熊掌」（11055、13581、13650 等全仓同步）。
- r5-opus-22：新增 6 条 entity name：wet/soaked/drenched honey tree、wet/soaked/drenched giant venus flytrap。先查库内 honey tree、giant venus flytrap 的现有译名，前缀译「湿漉漉的／浸透的／湿透的」（或更自然的区分），放在原名条目附近，第三参数用 "entity name"。
- r5-opus-23（及 18 调查）：先查库内 "shield" 的全部条目与 tag。若无 "entity combat talented" tag 的 shield，新增 `t("shield", "盾牌", "entity combat talented")`（r5-opus-23）。r5-opus-18（Actor.lua 无 context 的 `_t(speed_type)`）：**只调查不改**——在报告中说明无 tag 的 "shield" 条目现为何值、被哪些地方使用、改它会影响什么。

## 不执行
r5-opus-17（上游 :format 分支，需代码钩子）。

## 完成后
写 `/tmp/r5fix/report.md`：逐条 文件:行、旧/新 target（新增行注明）、代入后的通读句、r5-opus-18 调查结论、lint 结果。最终回复一行：`EXECUTOR r5fix DONE edits=<条数>`。
