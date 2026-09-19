# 翻译审核当前交接

更新时间：2026-09-19（修复批 232 完成后）

## 当前状态

- **生产审核已由维护者恢复**（2026-09-19 本会话）。审核与修复保持严格 1:1 交替。
- 审核批已完成至 210，**修复批已完成至 232**；下一步是**审核批 211**（80 条）。
- 修复批 232：repair commit `31759f7`（20 条裁决项 + 同族一并，共 36 处、27 个 revision），
  evidence commit `34ed49d`（migration `ecc3c5d8`，new catalog `b368b80b`，old `29899e2f`，
  queued_successors 27，ambiguous 0 / unmapped 0）。luac OK、lint 0 errors、runtime collisions 0。
- rebuild 后 `repair_required=131 → 111`，`blocked=20`，queue check 干净，无活动批次。
- 恢复前须重查 queue、工作树、当前 HEAD 和任务状态。注意：**任何与批次无关的提交都会让
  queue 报 evidence-head drift**，须先 `production queue rebuild`（约 2m45s）再跑 migration。
- 当前会话只授权本地工作，**未授权 push、开 PR 或发布**。本地有 3 个未 push 提交
  （`7964eb1`、`31759f7`、`34ed49d`）。

## 修复批 232 已处理（不再重复）

批 210 三项优先（含纠正修复批 231 自身错误）：刻印 lore `herbal infusions`「草药输液」→
**「草本纹身」**（库内既定，见 docs/handoff-history §290）+ most common 比较限定；
Block `the wielder`→持有者；Weisman 信件 pomposity/false heroics/town square/At first/limb。

FIFO 最旧实质项 17 项：venture inside the Peak（同族 2 处）、Nature's Defiance（damage
affinity→伤害亲和 + each turn + devotion）、Wrap of Stone desc、Aletta 幽灵、clawed
dragon-scale gloves→龙鳞、Tract of Destruction→毁灭之卷 + Nalorën lands、cloudy→浑浊、
Ooze Spit、countershot、Parasitic Leeches→寄生水蛭（同族 5 处）、Malleable Body
（致命打击→暴击）、圣光沉稳攻击、Foresight 暴击减免→几率无视暴击伤害（同族 3 处）、
pays up to、roll to→翻筋斗、elixirs + 施受方向、Trance of Purity 逐个累减。

**修复批 232 新增待维护者**：`Artelia Firstborn`「亚特莱长子」——Firstborn 为称号（「最初
诞生/苏醒者」），Artelia 出自女性名表，「长子」凭空指派性别；需新拟称号，留维护者。

## 下一批范围

**审核批 211**（80 条），按 WP2-Lite 正式入口执行：surface 4 lane（并发上限 3）+
contextual v2 single full，证据先提交并 finalize，修复另建任务（修复批 233）。

修复批 233 恢复时仍按 FIFO 取 `repair_required` 最旧约 20 条实质项；最旧约 30 条仍是长期
维护者待办与已知表层误报（`Archmagi`→元素法师），每批重遇再跳过。

## 待维护者裁决

下列专名或全局术语决定不得在普通修复批内自行裁决：

`Shantiz`、`Continuum Destabilization`、`Feed Strengths`、`Corrupted Negation`、
`archery prowess`、`Pushy elf`、`Hurricane`、`Sapphire`（2 项）、`Dirge Intoner`、
`-Attenuate`、`Summertide`、`the Darkness`、`Arena Master` 头衔、`slimy` 词缀、
`Massive Blow`、`Sudden Growth`、`slime mold`、`Power/Range` 面板、`blood-etched`、
`Intricate Tools`、`Flexible Combat`、`Curse of Shrouds`、`Reabsorb`、`Empty Hand`、
`Epoch's Curve`、`Hide in Plain Sight`、`Artelia Firstborn`。

权威逐条明细仍在维护者记忆 `repair-batch-cursor`；这里只保留当前交接所需清单。

## 已知机制与操作事实

- 表层筛查使用 4 lane、并发上限 3；交叉复核使用 1 个 full child。具体 provider/model 选择仍以恢复时可用 profile 和任务契约为准，本文件不改变选择政策。
- 表层派发、finish 通知、收获、归档和恢复使用 [orchestration README](tools/orchestration/README.md) 的当前入口；不得轮询猜测完成状态。
- freeze MISS：真正死键按既有 host-block 流程处理；运行期拼接或小写实体名（form #7/#8）不是死键。batch 208 的 `gem.lua` / `alchemist lapis lazuli` 暴露了 `freeze_workset.py` 只在 `source_tag == 'entity name'` 校验 concat、漏掉 `alchemist gem` 标签的缺口；该工具修复仍待维护者另行授权。
- 固定版本机制事实优先于既有译文、术语库和模型 finding；DLC 来源未固定时必须记录实际公开源码来源与未固定状态。

## 当前入口与历史

- 正式操作和验收：[代理工作流](docs/agent-workflow.md)、[编排说明](tools/orchestration/README.md)。
- 适用契约：[surface screen v1](docs/paseo-translation-surface-screen-v1-contract.md)、[context review v2](docs/paseo-translation-context-review-v2-contract.md)。
- 2026-09-19 以前的完整交接、旧性能任务状态、历史批次表和事故记录已归档到
  [历史交接存档](docs/handoff-history-through-20260919.md)。归档内容仅供追溯，**不构成当前授权**。
