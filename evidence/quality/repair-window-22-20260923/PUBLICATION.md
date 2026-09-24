# 修复窗口22发布记录

修复窗口22仅处理审核268确认的6条问题，未扩大范围：

- 欺诈斗篷生效日志改为“一层幻影出现在#Target#周围，让%s看起来像人类”。
- 电鳗尾炼金说明改为“电鳗到哪儿为止、尾巴又从哪儿开始？其实没多大关系”。
- 厄奇斯成就补回“疯狂的”与“猛攻”。
- 太阳堡垒创建者挂坠改为“赤铁矿之月遮蔽金色太阳”。
- 腐化蒸汽补回主语，改为“腐化的蒸汽在目标位置升起”。
- 分裂（Mitosis）补回视线内、召唤上限、技能激活期间三处限定，并恢复为与原文一致的7行。

任务 `repair-w22-20260923` 中，`execute-01`（`codex/gpt-5.6-sol`）实施6条修改。`REVIEW(0)/full`（`codex/gpt-6-sol`）给出5 OK / 1 ISSUE，确认欺诈斗篷日志漏译“出现”；`execute-02` 完成修复。`FINAL(1)/full`（`claude-opus-5-5`）给出5 OK / 1 ISSUE，确认电鳗句将 `stop` 译成起点，该问题源于宿主 SPEC 的措辞；`execute-03` 完成修复。`RE_REVIEW(2)/full`（`codex/gpt-6-sol`）给出5 OK / 1 ISSUE，该 ISSUE 认为 `Cunning` 应译为“狡诈”，宿主因“灵巧”为本库既有属性名而驳回。`FINAL(3)/full`（`claude-opus-5-5`）给出6 OK，任务收敛。完整门禁全部通过，包含严格构建，状态为 `DONE_VERIFIED`。

译文提交为 `e3ad691d2819f29598d974d99d0139a3b373de20`；新 catalog 为 `b239aafd8d5887f41de2065795f6913737ac9847cac1725c390e2fc2a421a197`；migration 为 `1cd5583de937a86439dcbc7ae0c2953e201574c2c53aa687ab592d39a5479508`。迁移结果为6条 `revision_changed`、29,822条 `unchanged`、0条 `ambiguous/unmapped`，6个 successor 待重新审核且不继承 `done`。本窗口无新增 pending。

本窗口的流程教训是：SPEC 中给出的示例译文本身也必须逐词对照原文。

3个 executor child 与4个 reviewer child 均已归档确认；本 publication child 待宿主归档。冻结编排证据见[编排快照](orchestration/)，PACK-MANIFEST 逐字副本位于[窗口根目录](orchestration-pack-manifest.json)，逐字复制的发布附件见[publication](publication/)，迁移记录见[迁移文件](../../production-review-v2-lite/migrations/1cd5583de937a86439dcbc7ae0c2953e201574c2c53aa687ab592d39a5479508.json)。本证据提交、第二次 queue rebuild 与 push 均由宿主后续执行，尚未宣称完成；随后继续审核269（默认80条）。
