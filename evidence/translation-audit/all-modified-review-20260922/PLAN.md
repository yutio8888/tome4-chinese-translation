# 全部已修改译文复核工作计划

## 范围

用户确认：本轮生产审核启动以来全部译文修改。首批 batch-c7f8a5c77bbeaa7f3b89 的 manifest.base_commit 为 `d77becdaf5f9860cae396741a4f1f319bb4ef5d5`；终点为 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。基线来源是实际首批 evidence，而非任意日期。扫描 manifest 全部 11 组件，逐个加载基线和 157 次相关 first-parent 提交的 LuaJIT 语义记录，对比 source/section/source_tag/重复项序号及 target/args_order/special。含新增/身份变化、标点、参数顺序与改后恢复；不依赖净 diff 或提交摘要。当前共 4144 条，4143 条净变更、1 条改后恢复；删除项 0。清单见 inventory.json，重算配方见 inventory-recipe.py（原始脚本使用任务临时输出路径，仅供复现，不修改译文）。

## 角色与用户授权例外

- ORCHESTRATOR：仅机械整理条目/覆盖/证据、写工作计划进度、派发/收获/归档。不得自行做译文语义裁决或修复。
- Gemini：Paseo / Antigravity / Gemini 3.8 Flash / High，只读逐条复核，中文自然语言输出，不强制 JSON。
- 交叉 REVIEWER：Paseo / Codex / GPT-5.6-Sol / Medium，只读核验 Gemini 的每个疑点及必要调用链，给出归因明确的 confirmed/refuted/pending/advisory。此处为用户明确要求的疑点交叉核验，允许读本次疑点，而非盲审。
- 以上当前用户指令覆盖仓库旧 JSON/宿主语义裁决/盲审输入要求，仅对本工作授权生效；不改全局规则。不伪造既有严格 contract checker 的 DONE_VERIFIED。任何结论都保留是谁提出/谁复核，模型严重程度不自动等于事实；不自动修复。

## 批次与顺序

既有抽查 11 条，其中 10 条属于本轮实际修改；这 10 条 Gemini 覆盖仅在 source/target 精确匹配后复用，旧宿主裁决不沿用；spot-06 全部疑点先交 Sol。其余 4134 条拆为 130 个批次，每批最多 40 条、source+target 合计约 28KB（单条超长可独占）。按组件、文件、原文出现顺序推进；不会忽略标点批量修正。最多同时 2 个 Gemini，加 1 个 Sol；如同一父级总并发限制更低则串行调整。

1. 先提交全部清单、计划、进度和输入包，再启动派发。
2. Gemini 返回后记录原文报告并核对逐条编号覆盖和只读哈希，不因 Markdown/JSON 格式重跑；仅补缺条目，不能把部分报告标为全批完成。
3. 所有疑点（包含 evidence 不足）进入 Sol 队列，按相关源码分组。Sol 可提出新疑点，原样记录；不由主代理压低/升级语义判断。
4. 交叉结果仍 pending 的列入人工复核清单；意见冲突保留两方意见与证据。confirmed 也仅记录为 Sol 交叉意见，不自动修改。
5. 每次收获后先归档并确认，再更新进度、派发下一批；无需逐批用户确认。主工作区、生产 catalog/queue/handoff 不写。
6. 全部 4144 条有 Gemini 覆盖且疑点均有 Sol 结果、child 全归档后交付总表。pending 是交付中的人工待决项，不伪称修复或全库无错。

## 输入与验证

固定版本公开源码依 source-access.json 按 git object 读取；DLC 目录复制到本 worktree 忽略缓存并记录逐文件 SHA-256，其来源仍未固定；possessors 未定位源码时如实标注，不能借用 engine pin。原始译文文件在本 audit 分支只读，派发前后检查 HEAD、git diff 与 locale SHA-256。所有判断性报告进 evidence，原始输出不重写。只读任务不跑生产发布/构建门禁。计划与进度先落盘，报告提交只在 audit 分支，不 push。
