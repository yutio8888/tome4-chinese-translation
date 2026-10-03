# 机制改写有界撤回

mode=implement; change_class=standard; schema5; max_cycles3。此为用户已明确授权的恢复及撤回范围核验，不是新一轮源码机制校对或正式生产批次。采用code_legacy_v1复审冻结的撤回清单、恢复逻辑和实际diff，核验用户选择是否准确落实；不把复审解释为旧译文机制正确性的背书。

用户要求：撤回“本轮因英文与代码不一致而做的机制改写”，包括追加解释及直接改变数值/条件/范围；保留普通翻译修正。只在翻译仓库撤回并讨论；对外仓库、标签、0.3.2 Release和资产全部不动。近期MMR-026“生命汲取（物理）”术语决定保留；UPSTREAM054撤销原问题、保留当前译文的决定保留。

允许唯一EXECUTOR修改文件见SCOPE（五个Lua对应有界target，必要的历史args_order变更必须逐项解释，默认不动其他字段）；允许写自身/tmp及.artifacts/i18n/mechanics-rollback-20261003/executor-report.json。不得改术语库、工具、角色、旧evidence、.ai、用户文档或外部仓库；不stage/commit、不创建child。

INVENTORY是固定bfde8c53（本轮修正前）→当前HEAD全部差异，不是自动撤回名单。按用户授权对每条及各子句分类：机制说明与英文不一致→撤回；忠实英文/术语/格式/普通语义修正→保留；混合→恢复机制部分且保留普通修正。不得仅凭UPSTREAM编号决定所有内容，更不得整文件git revert。注意原workset.original_entry.after才是修正前，before是更早译本不要用错。

原132个UPSTREAM/MMR-UPSTREAM claim的131项修正及一项已撤销为定位线索；另外复审中发现的机制解释也要撤回，包括package003 Dominate、亲和相关、MMR-002等，以及014暮光回响同键副本。三个已知混合项：entry412保留nearby→附近而非相邻；1201保留触手两侧以施法者为中心而非目标；1500保留全局速度术语。每个upstream条目内另外补入的普通翻译修正同样应保留。按英文辨别，别重新以代码发现新修订。

可读当前仓库资料、旧批次evidence及固定Git历史以恢复上下文，不需要重新作游戏源码机制结论。报告逐条给baseline/current/final、动作与理由、保留的普通修正、撤回的机制改写、涉及原claim及后加finding、字节/字段不变量证明；覆盖INVENTORY所有差异并说明遗漏/新增。同运行键副本保持一致。术语“生命汲取（物理）”及其他正常名称、格式、占位符/markup/newline修复保留。若恢复baseline会破坏strict lint则只保留必要ASCII空格，不借机润色。

验收：准确选择恢复范围、完整清单、逆向目标范围证明、LuaJIT逐字段、严格lint、运行键冲突/分类、严格核心addon与实际DLC消费端dry-run、独立范围复审及终审、所有child归档、DONE验证；保留历史证据，另记本次撤回，不抹去过去记录。不宣布“已重新证明所有机制”。

## 冻结复审输入

本轮审查落实用户撤回范围是否完整准确，不重新认可或修复游戏机制；旧译文中原有问题不计本次缺陷。特别检查错误撤回普通翻译修正、漏撤本轮机制重写、字段/字节/占位符回归。判断不依赖旧claim编号。

- 全部165条三方对照（pre-repair／pre-rollback／final）、英文原文与候选分类：.ai/task/mechanics-rollback-20261003/CANDIDATE-FINAL_REVIEW-1-1.json，SHA256 `b0b2beebd6924f845efce8ae5d2129f25ce35be5dfdb2487f8ec24bade5fe720`。分类理由是待核验的 proposer assertion。
- 独立宿主范围证明：.ai/task/mechanics-rollback-20261003/PROOF-FINAL_REVIEW-1-1.json，SHA256 `55af0cef0d81b7a87265298a103caee07e9d653467c5aa8ebfc2cf484fb5a2d8`。
- 任务diff：.ai/task/mechanics-rollback-20261003/CODE_DIFF-FINAL_REVIEW-1-1.patch。可复现配方：`git diff a8f2260c28d07ac3136d4e44aa0d3e4d76882c90 -- mod-tome.lua tome-ashes-urhrok.lua tome-cults.lua tome-orcs.lua`。
- 变更文件集：mod-tome.lua, tome-ashes-urhrok.lua, tome-cults.lua, tome-orcs.lua；engine.lua 在165项清单内但未改。
- 可只读核对以上冻结输入及这些四个当前Lua、对应任务baseline和pre-repair快照；不读当前任务的其他review结果，不写任何文件，不运行会写报告的工具。无需重查游戏源码或重跑构建。
- 待交付的新撤回证据是任务记录，后续由宿主保存这些冻结字节与复审记录；旧批次证据全部保持原样。

normal_review 输出每项恰为 ID / Severity / File / Location / Problem / Evidence / Impact / Recommended fix，severity仅 blocker|high|medium|low，末尾 VERDICT: PASS|CHANGES_REQUIRED。无finding时仅输出 VERDICT: PASS。
