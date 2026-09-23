# 修复窗口20发布记录

修复窗口20仅处理审核266确认的7条问题，未扩大范围：

- 念力核心项圈外观保留“似乎”，去掉增译的“所有”。
- 邪眼的 `bloodshot` 改为“布满血丝”。
- `Utterly Destroyed` 说明中的 `creature` 改为“生物”，`thrill of the death` 改为“击杀带来的快感”。
- 离线模式说明将版本检查改为“版本检查：不再检查插件是否有新版本”；按复审把“角色备份”改为“角色仓库……上传到在线仓库来展示你的荣耀”，补出“有关游戏更新的信息”，并把错位的空行移回原位。
- 时空法术类别说明改为“操控时间的法术学派”。
- 梅琳达成就改为“落难少女拯救者”。
- 蛛毒魔棒未鉴定名中的 `wand` 改为“魔杖”。

任务 `repair-w20-20260923` 中，`execute-01`（`codex/gpt-5.6-sol`）实施7条修改。`REVIEW(0)/full`（`codex/gpt-6-sol`）给出6 OK / 1 ISSUE，确认 `Characters vault` 被误译为角色备份，并增译了 `te4.org`；`execute-02` 仅修改该行。`FINAL(1)/full`（`claude-opus-5-5`）给出6 OK / 1 ISSUE，确认空行错位（LF 总数未变，但空行从“游戏内新闻”之后移到了 `CRIMSON` 警告之前），并确认漏译“有关游戏更新的信息”；`execute-03` 完成修复。`RE_REVIEW(2)/full`（`codex/gpt-6-sol`）与 `FINAL(3)/full`（`claude-opus-5-5`）均给出7 OK，任务收敛。完整门禁17/17通过，包含严格构建，状态为 `DONE_VERIFIED`。

译文提交为 `ffa53351b8e490c859ec029fdc655bd4c8f3bab5`；新 catalog 为 `e97aaf89de5fca113d500beccb80df23b2c5731eb3f8215495e93805b6c4c76c`；migration 为 `99c7ebd419a3f9ceebf2bba12de24d4561cbba3805972d941cda1f7fa83c6def`。迁移结果为7条 `revision_changed`、29,821条 `unchanged`、0条 `ambiguous/unmapped`，7个 successor 待重新审核且不继承 `done`。本窗口无新增 pending。

本窗口的流程教训是：`verify.py` 只比较 LF/TAB 数量，无法发现空行位置发生移动；多段 target 必须逐行比较空行下标。

3 个 executor child 与4个 reviewer child 均已归档确认；本 publication child 待宿主归档。冻结编排证据见[编排快照](orchestration/)，PACK-MANIFEST 逐字副本位于[窗口根目录](orchestration-pack-manifest.json)，逐字复制的发布附件见[publication](publication/)，迁移记录见[迁移文件](../../production-review-v2-lite/migrations/99c7ebd419a3f9ceebf2bba12de24d4561cbba3805972d941cda1f7fa83c6def.json)。本证据提交、第二次 queue rebuild 与 push 均由宿主后续执行，尚未宣称完成；随后继续审核267（默认80条）。
