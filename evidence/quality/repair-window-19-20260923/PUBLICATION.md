# 修复窗口19发布记录

修复窗口19仅处理审核265确认的4条问题，未扩大范围：

- 念动弓说明补出“每回合”，将 `attack` 译为“命中”并与同族条目保持一致，同时恢复行首 TAB。
- `Burrow` 说明第三行改回 TAB 分隔，并补出“土质墙壁”。
- `Nightshade` 陷阱补出“中毒”，明确4回合同时覆盖震慑与中毒。
- 野蛮种族记载仅修改 `mod-tome.lua` 中 `section mod-tome/load.lua` 下因后写覆盖而实际生效的那一行：改正首句、言语能力、近几百年、烈火纪末期、恶魔酸液/黑暗之云，将 `supported by` 改为研究支持该理论，并按 `FINAL(1)` 修正俗称、召唤主语、“被证明是不可能的”与 `extremely slender` 四处。

任务 `repair-w19-20260923` 中，`execute-01`（`codex/gpt-5.6-sol`）实施4条修改。`REVIEW(0)/full`（`codex/gpt-6-sol`）给出2 OK / 2 ISSUE，两项均确认；`execute-02` 完成修复。`FINAL(1)/full`（`claude-opus-5-5`）对野蛮种族记载给出1 ISSUE，确认4处子串；`execute-03` 完成修复。`RE_REVIEW(2)/full`（`codex/gpt-6-sol`）给出4 OK；该 reviewer 经 Paseo 终端绕过沙箱只读授权文件，宿主逐条审计并关闭终端。`FINAL(3)` 第一次尝试 `f3a1` 的结论前带英文导语，判定 `output_valid=false`，不入账；第二次尝试 `f3a2` 给出4 OK，任务收敛。完整门禁17/17通过，包含严格构建，状态为 `DONE_VERIFIED`。

译文提交为 `e602df35477fe2a6f2ffa9fd66029b51e83186a7`；新 catalog 为 `c5085a75a7796f11c91d64f39f454ac2f10dea491b28565222fdea5883057d35`；migration 为 `e5935d7e04f86d7d3a09d9a9e6d2afcc69c0f5e3a8c8b1ace3fac0e7a1649fec`。迁移结果为4条 `revision_changed`、29,824条 `unchanged`、0条 `ambiguous/unmapped`，4个 successor 待重新审核且不继承 `done`。本窗口无新增 pending。

范围外遗留：同一 source 的 `lore/misc` 段那一行因运行时被覆盖而不生效，仍保留旧句；本窗口未修改，留待后续审核。

3 个 executor child、4 个有效 reviewer child 以及无效的 `f3a1` reviewer child 均已归档确认；本 publication child 待宿主归档。冻结编排证据见[编排快照](orchestration/)，PACK-MANIFEST 逐字副本位于[窗口根目录](orchestration-pack-manifest.json)，逐字复制的发布附件见[publication](publication/)，迁移记录见[迁移文件](../../production-review-v2-lite/migrations/e5935d7e04f86d7d3a09d9a9e6d2afcc69c0f5e3a8c8b1ace3fac0e7a1649fec.json)。本证据提交、第二次 queue rebuild 与 push 均由宿主后续执行，尚未宣称完成；随后继续审核266（默认80条）。
